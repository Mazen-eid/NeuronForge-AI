"""Tiny SQLite state store for runs, used topics, and scheduled jobs."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT NOT NULL,
    topic TEXT,
    status TEXT NOT NULL,
    video_path TEXT,
    video_url TEXT,
    error TEXT,
    meta_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS used_topics (
    channel_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (channel_id, topic)
);
"""


class DB:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat(timespec="seconds")

    # --- runs ---
    def start_run(self, channel_id: str, topic: str | None = None) -> int:
        now = self._now()
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO runs (channel_id, topic, status, created_at, updated_at) "
                "VALUES (?, ?, 'running', ?, ?)",
                (channel_id, topic, now, now),
            )
            return cur.lastrowid  # type: ignore[return-value]

    def finish_run(
        self,
        run_id: int,
        status: str,
        *,
        video_path: str | None = None,
        video_url: str | None = None,
        error: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        with self._conn() as c:
            c.execute(
                "UPDATE runs SET status=?, video_path=?, video_url=?, error=?, meta_json=?, "
                "updated_at=? WHERE id=?",
                (
                    status,
                    video_path,
                    video_url,
                    error,
                    json.dumps(meta or {}, ensure_ascii=False),
                    self._now(),
                    run_id,
                ),
            )

    def recent_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    # --- used topics ---
    def mark_topic_used(self, channel_id: str, topic: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO used_topics (channel_id, topic, created_at) VALUES (?, ?, ?)",
                (channel_id, topic, self._now()),
            )

    def is_topic_used(self, channel_id: str, topic: str) -> bool:
        with self._conn() as c:
            row = c.execute(
                "SELECT 1 FROM used_topics WHERE channel_id=? AND topic=?",
                (channel_id, topic),
            ).fetchone()
        return row is not None
