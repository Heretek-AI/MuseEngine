"""Durable memory: episodes (past problems and what came of them), notes
(lessons distilled by reflection), key/value agent state, and an audit log.

Backed by plain SQLite with ordinary transactions, so writes are atomic and a
crash cannot leave a half-written database. Use ``":memory:"`` for tests.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

_SCHEMA = """
CREATE TABLE IF NOT EXISTS episodes (
    id TEXT PRIMARY KEY,
    problem TEXT NOT NULL,
    summary TEXT NOT NULL,
    is_open INTEGER NOT NULL,
    created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    source_episode_ids TEXT NOT NULL,
    created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    at REAL NOT NULL,
    action TEXT NOT NULL,
    decision TEXT NOT NULL,
    detail TEXT NOT NULL
);
"""

_WORD = re.compile(r"[a-z][a-z0-9-]{2,}")
_STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "into", "without", "what",
    "why", "how", "are", "can", "does", "design", "explain", "which", "when", "while",
}


def _tokens(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if w not in _STOPWORDS}


@dataclass
class Episode:
    id: str
    problem: str
    summary: str
    is_open: bool
    created_at: float


class MemoryStore:
    def __init__(self, path: str | Path = ":memory:"):
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        with self.conn:
            self.conn.executescript(_SCHEMA)

    def close(self) -> None:
        self.conn.close()

    # -- episodes -----------------------------------------------------------

    def add_episode(self, problem: str, summary: str, is_open: bool = True) -> Episode:
        now = time.time()
        ep_id = "ep_" + hashlib.sha256(f"{problem}\0{now}".encode()).hexdigest()[:10]
        with self.conn:
            self.conn.execute(
                "INSERT INTO episodes (id, problem, summary, is_open, created_at) VALUES (?, ?, ?, ?, ?)",
                (ep_id, problem, summary, int(is_open), now),
            )
        return Episode(ep_id, problem, summary, is_open, now)

    def set_open(self, episode_id: str, is_open: bool) -> None:
        with self.conn:
            self.conn.execute("UPDATE episodes SET is_open = ? WHERE id = ?", (int(is_open), episode_id))

    def episodes(self, only_open: bool = False) -> List[Episode]:
        sql = "SELECT * FROM episodes" + (" WHERE is_open = 1" if only_open else "") + " ORDER BY created_at"
        return [self._episode(r) for r in self.conn.execute(sql)]

    def recall(self, query: str, k: int = 3) -> List[Episode]:
        """Past episodes most lexically related to ``query``; open ones get a small boost."""
        q = _tokens(query)
        if not q:
            return []
        scored = []
        for ep in self.episodes():
            overlap = len(q & _tokens(ep.problem + " " + ep.summary))
            if overlap:
                scored.append((overlap + (0.5 if ep.is_open else 0.0), ep.created_at, ep))
        scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
        return [ep for _, _, ep in scored[:k]]

    @staticmethod
    def _episode(row: sqlite3.Row) -> Episode:
        return Episode(row["id"], row["problem"], row["summary"], bool(row["is_open"]), row["created_at"])

    # -- notes --------------------------------------------------------------

    def add_note(self, text: str, source_episode_ids: List[str]) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO notes (text, source_episode_ids, created_at) VALUES (?, ?, ?)",
                (text, json.dumps(source_episode_ids), time.time()),
            )

    def notes(self) -> List[str]:
        return [r["text"] for r in self.conn.execute("SELECT text FROM notes ORDER BY id")]

    # -- state & audit --------------------------------------------------------

    def get_state(self, key: str, default: Any = None) -> Any:
        row = self.conn.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
        return json.loads(row["value"]) if row else default

    def set_state(self, key: str, value: Any) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO state (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, json.dumps(value)),
            )

    def audit(self, action: str, decision: str, detail: Optional[Dict[str, Any]] = None) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO audit (at, action, decision, detail) VALUES (?, ?, ?, ?)",
                (time.time(), action, decision, json.dumps(detail or {})),
            )

    def audit_log(self) -> List[Dict[str, Any]]:
        return [
            {"at": r["at"], "action": r["action"], "decision": r["decision"], "detail": json.loads(r["detail"])}
            for r in self.conn.execute("SELECT * FROM audit ORDER BY id")
        ]
