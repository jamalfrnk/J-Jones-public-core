# SPDX-License-Identifier: Apache-2.0
"""Provider-neutral request/response contracts with explicit auth gating."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    classification: str
    max_tokens: int = 1024

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt must be non-empty")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be positive")


@dataclass(frozen=True)
class ProviderResponse:
    content: str
    model: str
    tokens_used: int | None = None
    usage_reported: bool = False


class ExplicitAuthTransport(Protocol):
    def before_transport(self, request: ProviderRequest, *, auth_token: str) -> None: ...


def require_explicit_auth(auth_token: str | None) -> str:
    if not auth_token or not auth_token.strip():
        raise PermissionError("explicit authentication is required")
    return auth_token
