# SPDX-License-Identifier: Apache-2.0
from jjones_core.notes import parse_front_matter, render_note, validate_note_metadata


def valid_metadata():
    return {
        "id": "n-1",
        "title": "A public note",
        "type": "research",
        "status": "active",
        "created_at": "2026-11-17T00:00:00Z",
        "updated_at": "2026-11-17T00:00:00Z",
        "tags": ["public"],
        "sensitivity": "public",
    }


def test_note_round_trip_and_validation():
    metadata = valid_metadata()
    parsed, body = parse_front_matter(render_note(metadata, "hello"))
    assert parsed == metadata
    assert body == "hello"
    assert validate_note_metadata(parsed) == []


def test_secret_content_is_rejected():
    metadata = valid_metadata()
    metadata["sensitivity"] = "secret_prohibited"
    assert any(issue.field == "sensitivity" for issue in validate_note_metadata(metadata))
