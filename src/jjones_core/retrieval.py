# SPDX-License-Identifier: Apache-2.0
"""Small deterministic SQLite FTS5 index with rebuildable derived state."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SearchResult:
    note_id: str
    title: str
    body: str


class LocalIndex:
    """A derived local index; callers remain responsible for canonical truth."""

    def __init__(self, database: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(database))
        self.connection.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS notes USING fts5(note_id UNINDEXED, title, body)"
        )
        self.connection.commit()

    def clear(self) -> None:
        self.connection.execute("DELETE FROM notes")
        self.connection.commit()

    def rebuild(self, records: list[tuple[str, str, str]]) -> None:
        self.clear()
        self.connection.executemany(
            "INSERT INTO notes(note_id, title, body) VALUES (?, ?, ?)", records
        )
        self.connection.commit()

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        terms = [term for term in query.split() if term.isalnum()]
        if not terms:
            return []
        expression = " AND ".join(f'"{term}"' for term in terms[:32])
        rows = self.connection.execute(
            "SELECT note_id, title, body FROM notes WHERE notes MATCH ? LIMIT ?",
            (expression, max(1, min(limit, 100))),
        ).fetchall()
        return [SearchResult(str(a), str(b), str(c)) for a, b, c in rows]

    def close(self) -> None:
        self.connection.close()
