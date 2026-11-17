# SPDX-License-Identifier: Apache-2.0
"""Public, provider-neutral J-Jones Core interfaces."""

__version__ = "0.1.0a1"

from .evidence import EvidenceManifest, build_manifest, sha256_bytes, verify_manifest
from .notes import ValidationIssue, parse_front_matter, render_note, validate_note_metadata
from .prompt import UntrustedContent, build_prompt, minimum_prompt_token_bound
from .provider import (
    ExplicitAuthTransport,
    ProviderRequest,
    ProviderResponse,
    require_explicit_auth,
)
from .retrieval import LocalIndex, SearchResult
from .server import ServerConfig, create_server, start_server

__all__ = [
    "EvidenceManifest",
    "ExplicitAuthTransport",
    "LocalIndex",
    "ProviderRequest",
    "ProviderResponse",
    "SearchResult",
    "ServerConfig",
    "UntrustedContent",
    "ValidationIssue",
    "build_manifest",
    "build_prompt",
    "minimum_prompt_token_bound",
    "parse_front_matter",
    "render_note",
    "require_explicit_auth",
    "sha256_bytes",
    "validate_note_metadata",
    "verify_manifest",
    "create_server",
    "start_server",
]
