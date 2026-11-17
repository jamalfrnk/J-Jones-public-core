# SPDX-License-Identifier: Apache-2.0
"""Authenticated local HTTP boundary for public-Core integrations.

The server is intentionally small and dependency-free. Loopback reachability
is never treated as authentication. A client exchanges the configured API key
for an in-memory bearer session and must present that session on every
subsequent request.
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import secrets
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from . import __version__

_MAX_BODY_BYTES = 16 * 1024
_DEFAULT_SESSION_TTL_SECONDS = 3600


@dataclass(frozen=True)
class ServerConfig:
    """Safe local-server defaults.

    The public boundary has no tokenless mode. Non-loopback binding is an
    explicit opt-in and still requires authentication for every protected
    request.
    """

    host: str = "127.0.0.1"
    port: int = 0
    session_ttl_seconds: int = _DEFAULT_SESSION_TTL_SECONDS
    allow_non_loopback: bool = False

    def validate(self) -> None:
        if not self.host.strip():
            raise ValueError("host must be non-empty")
        if not 0 <= self.port <= 65535:
            raise ValueError("port must be between 0 and 65535")
        if self.session_ttl_seconds < 1:
            raise ValueError("session_ttl_seconds must be positive")
        if not self.allow_non_loopback and not is_loopback_host(self.host):
            raise ValueError(
                "non-loopback binding is disabled by default; explicit opt-in is required"
            )


def is_loopback_host(host: str) -> bool:
    """Return whether a host is a recognized loopback address or name."""
    normalized = host.strip().lower()
    if normalized == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


class ApiKeyAuthenticator:
    """Verify an API key without retaining the raw key."""

    def __init__(self, api_key: str) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("api_key must be non-empty")
        self._digest = self._digest_key(api_key)

    @staticmethod
    def _digest_key(api_key: str) -> bytes:
        return hashlib.sha256(api_key.encode("utf-8")).digest()

    def verify(self, api_key: str | None) -> bool:
        if not api_key:
            return False
        candidate = self._digest_key(api_key)
        return hmac.compare_digest(self._digest, candidate)


class SessionManager:
    """Issue short-lived in-memory bearer sessions after API-key exchange."""

    def __init__(self, ttl_seconds: int) -> None:
        if ttl_seconds < 1:
            raise ValueError("ttl_seconds must be positive")
        self._ttl_seconds = ttl_seconds
        self._sessions: dict[bytes, float] = {}
        self._lock = threading.Lock()

    def issue(self) -> tuple[str, int]:
        token = secrets.token_urlsafe(32)
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        expires_at = time.time() + self._ttl_seconds
        with self._lock:
            self._purge_expired_locked()
            self._sessions[digest] = expires_at
        return token, self._ttl_seconds

    def valid(self, token: str | None) -> bool:
        if not token:
            return False
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        with self._lock:
            self._purge_expired_locked()
            expires_at = self._sessions.get(digest)
        return expires_at is not None

    def _purge_expired_locked(self) -> None:
        now = time.time()
        for digest, expires_at in list(self._sessions.items()):
            if expires_at <= now:
                del self._sessions[digest]


def create_server(
    api_key: str,
    config: ServerConfig | None = None,
) -> ThreadingHTTPServer:
    """Create an authenticated local server; call serve_forever separately."""
    selected = config or ServerConfig()
    selected.validate()
    authenticator = ApiKeyAuthenticator(api_key)
    sessions = SessionManager(selected.session_ttl_seconds)

    class Handler(BaseHTTPRequestHandler):
        server_version = "J-Jones-Public-Core"

        def log_message(self, format: str, *args: Any) -> None:
            # Requests can contain sensitive paths or headers; do not emit them.
            return

        def _json(
            self,
            status: HTTPStatus,
            payload: dict[str, Any],
        ) -> None:
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> dict[str, Any] | None:
            raw_length = self.headers.get("Content-Length", "0")
            try:
                length = int(raw_length)
            except ValueError:
                return None
            if length < 0 or length > _MAX_BODY_BYTES:
                return None
            try:
                value = json.loads(self.rfile.read(length))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return None
            return value if isinstance(value, dict) else None

        def _bearer_token(self) -> str | None:
            header = self.headers.get("Authorization", "")
            scheme, _, token = header.partition(" ")
            if scheme.lower() != "bearer" or not token.strip():
                return None
            return token.strip()

        def _auth_required(self) -> bool:
            token = self._bearer_token()
            if sessions.valid(token):
                return True
            self._json(
                HTTPStatus.UNAUTHORIZED,
                {
                    "error": "explicit_authentication_required",
                    "message": (
                        "Loopback reachability does not authenticate a user. "
                        "Create a session with the configured API key."
                    ),
                    "fallbacks": [
                        {
                            "id": "api_key_session",
                            "action": "POST /v1/session with the configured API key",
                        },
                        {
                            "id": "desktop_sign_in",
                            "action": "Use the desktop sign-in screen when available",
                        },
                    ],
                },
            )
            return False

        def do_POST(self) -> None:
            if self.path != "/v1/session":
                self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            payload = self._read_json()
            candidate = payload.get("api_key") if payload else None
            if not isinstance(candidate, str) or not authenticator.verify(candidate):
                self._json(
                    HTTPStatus.UNAUTHORIZED,
                    {
                        "error": "authentication_failed",
                        "message": "The API key was not accepted.",
                        "fallbacks": [
                            {
                                "id": "retry_api_key",
                                "action": "Check the key and try again",
                            },
                            {
                                "id": "desktop_recovery",
                                "action": "Use the owner-controlled recovery flow",
                            },
                        ],
                    },
                )
                return
            token, expires_in = sessions.issue()
            self._json(
                HTTPStatus.CREATED,
                {
                    "access_token": token,
                    # Bearer is the HTTP authorization scheme, not a credential.
                    "token_type": "Bearer",  # nosec B105
                    "expires_in": expires_in,
                    "authentication": "explicit",
                },
            )

        def do_GET(self) -> None:
            if self.path == "/v1/health":
                if not self._auth_required():
                    return
                self._json(
                    HTTPStatus.OK,
                    {
                        "status": "ok",
                        "authentication": "explicit",
                        "tokenless_loopback": False,
                        "public_core_version": __version__,
                    },
                )
                return
            self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    server = ThreadingHTTPServer((selected.host, selected.port), Handler)
    server.daemon_threads = True
    return server


def start_server(api_key: str, config: ServerConfig | None = None) -> ThreadingHTTPServer:
    """Start a daemon-backed server for a desktop integration."""
    server = create_server(api_key, config)
    thread = threading.Thread(
        target=server.serve_forever,
        name="jjones-public-core-server",
        daemon=True,
    )
    thread.start()
    return server
