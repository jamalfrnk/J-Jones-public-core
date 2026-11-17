# SPDX-License-Identifier: Apache-2.0
"""Deterministic local evidence hashing and manifest verification."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceManifest:
    evidence_id: str
    relative_path: str
    sha256: str
    size_bytes: int


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_manifest(evidence_id: str, relative_path: str, data: bytes) -> EvidenceManifest:
    if not evidence_id.strip() or Path(relative_path).is_absolute():
        raise ValueError("evidence_id must be non-empty and path must be relative")
    return EvidenceManifest(
        evidence_id=evidence_id,
        relative_path=relative_path.replace("\\", "/"),
        sha256=sha256_bytes(data),
        size_bytes=len(data),
    )


def verify_manifest(manifest: EvidenceManifest, data: bytes) -> bool:
    return manifest.size_bytes == len(data) and manifest.sha256 == sha256_bytes(data)
