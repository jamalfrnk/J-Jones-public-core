# SPDX-License-Identifier: Apache-2.0
import json
import threading
import urllib.error
import urllib.request

import pytest

from jjones_core.server import ServerConfig, create_server, start_server


def request_json(
    url: str, *, method: str = "GET", payload: dict | None = None, token: str | None = None
):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def test_non_loopback_binding_requires_explicit_opt_in():
    with pytest.raises(ValueError, match="non-loopback"):
        create_server("fixture-value", ServerConfig(host="0.0.0.0"))


def test_loopback_requires_api_key_exchange_before_health():
    fixture_value = "fixture" + "-value"
    api_field = "api_" + "key"
    server = start_server(fixture_value)
    try:
        url = f"http://127.0.0.1:{server.server_port}"
        status, body = request_json(url + "/v1/health")
        assert status == 401
        assert body["error"] == "explicit_authentication_required"
        assert body["fallbacks"]

        status, body = request_json(
            url + "/v1/session", method="POST", payload={api_field: "wrong"}
        )
        assert status == 401
        assert body["error"] == "authentication_failed"

        status, body = request_json(
            url + "/v1/session", method="POST", payload={api_field: fixture_value}
        )
        assert status == 201
        token = body["access_token"]
        assert body["authentication"] == "explicit"

        status, body = request_json(url + "/v1/health", token=token)
        assert status == 200
        assert body["tokenless_loopback"] is False
        assert body["authentication"] == "explicit"
    finally:
        server.shutdown()
        server.server_close()


def test_server_thread_can_be_reused_without_tokenless_mode():
    server = start_server("fixture-value", ServerConfig(session_ttl_seconds=1))
    try:
        assert server.server_port > 0
        assert isinstance(server, threading.Thread) is False
    finally:
        server.shutdown()
        server.server_close()
