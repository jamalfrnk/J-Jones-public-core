# SPDX-License-Identifier: Apache-2.0
"""Generic Markdown note front matter parsing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import yaml

BASELINE_REQUIRED_FIELDS = (
    "id",
    "title",
    "type",
    "status",
    "created_at",
    "updated_at",
    "tags",
    "sensitivity",
)
ALLOWED_STATUSES = frozenset({"draft", "active", "archived"})
ALLOWED_SENSITIVITIES = frozenset({"public", "internal", "restricted", "secret_prohibited"})


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("note must begin with a YAML front-matter delimiter")
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        raise ValueError("note front matter is not closed")
    try:
        metadata = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError as exc:
        raise ValueError("note front matter is not valid YAML") from exc
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise ValueError("note front matter must be a YAML mapping")
    return metadata, "\n".join(lines[closing + 1 :]).lstrip("\n")


def render_note(metadata: dict[str, Any], body: str) -> str:
    return (
        "---\n"
        + yaml.safe_dump(metadata, sort_keys=False, default_flow_style=False)
        + "---\n\n"
        + body.strip()
        + "\n"
    )


def validate_note_metadata(metadata: dict[str, Any]) -> list[ValidationIssue]:
    issues = [
        ValidationIssue(field, "required field is missing or empty")
        for field in BASELINE_REQUIRED_FIELDS
        if metadata.get(field) in (None, "")
    ]
    if metadata.get("status") not in ALLOWED_STATUSES:
        issues.append(ValidationIssue("status", "must be draft, active, or archived"))
    if metadata.get("sensitivity") not in ALLOWED_SENSITIVITIES:
        issues.append(ValidationIssue("sensitivity", "must use a supported classification"))
    if metadata.get("sensitivity") == "secret_prohibited":
        issues.append(ValidationIssue("sensitivity", "secret content cannot be canonicalized"))
    if not isinstance(metadata.get("tags"), list):
        issues.append(ValidationIssue("tags", "must be a list"))
    if not isinstance(metadata.get("type"), str) or not metadata.get("type"):
        issues.append(ValidationIssue("type", "must be a non-empty string"))
    return issues
