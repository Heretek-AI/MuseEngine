"""
NoesisOS Persistent SQLite Daemon & Long-Horizon Mind Store (`noesis_persistent_daemon.py`)
===========================================================================================

Wires `NoesisCognitiveOS` into a durable SQLite storage engine so the agent's:
  - Plastic Personality Vector (`personality_state`)
  - Homeostatic Vital Signs (`homeostatic_state`)
  - Tier 1 Hippocampal Episodic Buffer (`episodic_memories`)
  - Tier 2 Neocortical Semantic Graph (`semantic_schemas`)
  - Tier 3 Cerebellar Procedural Skills (`procedural_skills`)
  - Tier 4 Autobiographical Identity Spine (`autobiographical_spine`)
  - Autonomous Tick Audit Log (`workspace_broadcast_log`)

survive across process restarts, allowing the agent to run as a continuous,
self-determining background daemon across days or weeks without context bloat.
Uses `sqlite3.Connection.serialize()` / `deserialize()` for atomic, lock-free
persistence across both local disks and network/FUSE filesystems.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
import sqlite3
import sys
import time
from typing import Any, Dict, List

OUTPUT_DIR = Path("/working_dir/c_d1c55802486763fb/artifacts/file_generation/ttl=63d/output")
if str(OUTPUT_DIR) not in sys.path:
    sys.path.insert(0, str(OUTPUT_DIR))

from autonomic_cognitive_os import (
    EpisodicMemoryItem,
    NoesisCognitiveOS,
    ProceduralSkill,
    SemanticSchemaNode,
)


class PersistentMindStore:
    """
    SQLite-backed durability layer for NoesisCognitiveOS.
    Supports atomic file serialization so it works on both standard POSIX disks
    and lockless FUSE/container mounts.
    """

    def __init__(self, db_path: str | Path = ":memory:"):
        self.db_path = Path(db_path) if db_path != ":memory:" else None
        self.conn = sqlite3.connect(":memory:")
        if self.db_path and self.db_path.exists() and self.db_path.stat().st_size > 0:
            raw_bytes = self.db_path.read_bytes()
            self.conn.deserialize(raw_bytes)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _flush_to_disk(self) -> None:
        if self.db_path is not None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.db_path.write_bytes(self.conn.serialize())

    def close(self) -> None:
        self._flush_to_disk()
        self.conn.close()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS mind_vitals (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                tick_count INTEGER NOT NULL,
                homeostasis_json TEXT NOT NULL,
                personality_json TEXT NOT NULL,
                total_raw_tokens_evicted INTEGER NOT NULL,
                updated_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS episodic_memories (
                episode_id TEXT PRIMARY KEY,
                tick INTEGER NOT NULL,
                summary TEXT NOT NULL,
                domain TEXT NOT NULL,
                salience REAL NOT NULL,
                zeigarnik_open INTEGER NOT NULL,
                strength REAL NOT NULL,
                consolidated INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS semantic_schemas (
                schema_id TEXT PRIMARY KEY,
                principle TEXT NOT NULL,
                source_episode_ids_json TEXT NOT NULL,
                confidence REAL NOT NULL,
                retrieval_count INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS procedural_skills (
                skill_name TEXT PRIMARY KEY,
                trigger_condition TEXT NOT NULL,
                compiled_operator TEXT NOT NULL,
                invocations INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS autobiographical_spine (
                seq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                milestone TEXT NOT NULL,
                created_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS workspace_broadcast_log (
                tick INTEGER PRIMARY KEY,
                winning_agent TEXT NOT NULL,
                self_determined_goal TEXT NOT NULL,
                bid_power REAL NOT NULL,
                parallel_eureka TEXT,
                outcome TEXT NOT NULL,
                free_energy REAL NOT NULL,
                temperament TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """
        )
        self.conn.commit()
        self._flush_to_disk()

    def save_os_state(self, os_kernel: NoesisCognitiveOS) -> None:
        cur = self.conn.cursor()
        now = time.time()

        homeo_dict = {
            "epistemic_hunger": os_kernel.homeostasis.epistemic_hunger,
            "zeigarnik_tension": os_kernel.homeostasis.zeigarnik_tension,
            "memory_entropy": os_kernel.homeostasis.memory_entropy,
            "cognitive_fatigue": os_kernel.homeostasis.cognitive_fatigue,
            "falsification_debt": os_kernel.homeostasis.falsification_debt,
        }
        pers_dict = os_kernel.personality.to_dict()

        cur.execute(
            """
            INSERT INTO mind_vitals (id, tick_count, homeostasis_json, personality_json, total_raw_tokens_evicted, updated_at)
            VALUES (1, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                tick_count = excluded.tick_count,
                homeostasis_json = excluded.homeostasis_json,
                personality_json = excluded.personality_json,
                total_raw_tokens_evicted = excluded.total_raw_tokens_evicted,
                updated_at = excluded.updated_at
            """,
            (
                os_kernel.tick_count,
                json.dumps(homeo_dict),
                json.dumps(pers_dict),
                os_kernel.memory.total_raw_tokens_evicted,
                now,
            ),
        )

        # Sync Tier 1: Episodic Buffer (replace with current surviving buffer)
        cur.execute("DELETE FROM episodic_memories")
        for ep in os_kernel.memory.episodic_buffer:
            cur.execute(
                """
                INSERT INTO episodic_memories
                (episode_id, tick, summary, domain, salience, zeigarnik_open, strength, consolidated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ep.episode_id,
                    ep.tick,
                    ep.summary,
                    ep.domain,
                    ep.salience,
                    int(ep.zeigarnik_open),
                    ep.strength,
                    int(ep.consolidated),
                ),
            )

        # Sync Tier 2: Semantic Schemas
        for sc in os_kernel.memory.semantic_graph.values():
            cur.execute(
                """
                INSERT INTO semantic_schemas
                (schema_id, principle, source_episode_ids_json, confidence, retrieval_count)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(schema_id) DO UPDATE SET
                    confidence = excluded.confidence,
                    retrieval_count = excluded.retrieval_count
                """,
                (
                    sc.schema_id,
                    sc.principle,
                    json.dumps(sc.source_episode_ids),
                    sc.confidence,
                    sc.retrieval_count,
                ),
            )

        # Sync Tier 3: Procedural Skills
        for sk in os_kernel.memory.procedural_skills.values():
            cur.execute(
                """
                INSERT INTO procedural_skills
                (skill_name, trigger_condition, compiled_operator, invocations)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(skill_name) DO UPDATE SET
                    invocations = excluded.invocations
                """,
                (sk.skill_name, sk.trigger_condition, sk.compiled_operator, sk.invocations),
            )

        # Sync Tier 4: Autobiographical Spine
        cur.execute("SELECT COUNT(*) AS cnt FROM autobiographical_spine")
        existing_cnt = cur.fetchone()["cnt"]
        for milestone in os_kernel.memory.autobiographical_spine[existing_cnt:]:
            cur.execute(
                "INSERT INTO autobiographical_spine (milestone, created_at) VALUES (?, ?)",
                (milestone, now),
            )

        # Sync latest broadcast log entry
        if os_kernel.execution_log:
            latest = os_kernel.execution_log[-1]
            cur.execute(
                """
                INSERT OR REPLACE INTO workspace_broadcast_log
                (tick, winning_agent, self_determined_goal, bid_power, parallel_eureka, outcome, free_energy, temperament, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    latest["tick"],
                    latest["winning_agent"],
                    latest["self_determined_goal"],
                    latest["bid_power"],
                    latest["parallel_eureka"],
                    latest["outcome"],
                    latest["free_energy"],
                    latest["temperament"],
                    now,
                ),
            )

        self.conn.commit()
        self._flush_to_disk()

    def load_into_os(self, os_kernel: NoesisCognitiveOS) -> bool:
        """
        Restores persisted state into `os_kernel` if a checkpoint exists.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM mind_vitals WHERE id = 1")
        row = cur.fetchone()
        if not row:
            return False

        os_kernel.tick_count = row["tick_count"]
        os_kernel.memory.total_raw_tokens_evicted = row["total_raw_tokens_evicted"]

        h_data = json.loads(row["homeostasis_json"])
        for k, v in h_data.items():
            setattr(os_kernel.homeostasis, k, v)

        p_data = json.loads(row["personality_json"])
        for k, v in p_data.items():
            setattr(os_kernel.personality, k, v)

        # Restore Tier 1
        cur.execute("SELECT * FROM episodic_memories ORDER BY tick ASC")
        os_kernel.memory.episodic_buffer = [
            EpisodicMemoryItem(
                episode_id=r["episode_id"],
                tick=r["tick"],
                summary=r["summary"],
                domain=r["domain"],
                salience=r["salience"],
                zeigarnik_open=bool(r["zeigarnik_open"]),
                strength=r["strength"],
                consolidated=bool(r["consolidated"]),
            )
            for r in cur.fetchall()
        ]

        # Restore Tier 2
        cur.execute("SELECT * FROM semantic_schemas")
        os_kernel.memory.semantic_graph = {
            r["schema_id"]: SemanticSchemaNode(
                schema_id=r["schema_id"],
                principle=r["principle"],
                source_episode_ids=json.loads(r["source_episode_ids_json"]),
                confidence=r["confidence"],
                retrieval_count=r["retrieval_count"],
            )
            for r in cur.fetchall()
        }

        # Restore Tier 3
        cur.execute("SELECT * FROM procedural_skills")
        os_kernel.memory.procedural_skills = {
            r["skill_name"]: ProceduralSkill(
                skill_name=r["skill_name"],
                trigger_condition=r["trigger_condition"],
                compiled_operator=r["compiled_operator"],
                invocations=r["invocations"],
            )
            for r in cur.fetchall()
        }

        # Restore Tier 4
        cur.execute("SELECT milestone FROM autobiographical_spine ORDER BY seq_id ASC")
        spine = [r["milestone"] for r in cur.fetchall()]
        if spine:
            os_kernel.memory.autobiographical_spine = spine

        return True

    def export_snapshot(self) -> Dict[str, Any]:
        cur = self.conn.cursor()
        vitals = dict(cur.execute("SELECT * FROM mind_vitals WHERE id = 1").fetchone() or {})
        episodes = [dict(r) for r in cur.execute("SELECT * FROM episodic_memories").fetchall()]
        schemas = [dict(r) for r in cur.execute("SELECT * FROM semantic_schemas").fetchall()]
        skills = [dict(r) for r in cur.execute("SELECT * FROM procedural_skills").fetchall()]
        spine = [r["milestone"] for r in cur.execute("SELECT milestone FROM autobiographical_spine ORDER BY seq_id ASC").fetchall()]
        logs = [dict(r) for r in cur.execute("SELECT * FROM workspace_broadcast_log ORDER BY tick ASC").fetchall()]
        return {
            "vitals": vitals,
            "tier1_episodic_buffer": episodes,
            "tier2_semantic_schemas": schemas,
            "tier3_procedural_skills": skills,
            "tier4_autobiographical_spine": spine,
            "broadcast_history": logs,
        }


async def run_persistent_daemon_demo() -> None:
    db_file = Path("/working_dir/c_d1c55802486763fb/artifacts/file_generation/ttl=63d/intermediate/noesis_mind.db")
    if db_file.exists():
        db_file.unlink()

    print("=" * 92)
    print("BOOTING NOESIS PERSISTENT COGNITIVE DAEMON (SESSION 1: TICKS 1..6)")
    print("=" * 92)
    store_1 = PersistentMindStore(db_file)
    os_session_1 = NoesisCognitiveOS(seed=31)
    for _ in range(6):
        entry = await os_session_1.step_autonomous_tick()
        store_1.save_os_state(os_session_1)
        print(
            f"  [Session 1 | Tick {entry['tick']:02d}] Winner={entry['winning_agent']:<28} "
            f"| FreeEnergy={entry['free_energy']:.3f} | Temperament={entry['temperament']}"
        )
    store_1.close()

    print("\n" + "=" * 92)
    print("SIMULATING PROCESS RESTART -> RE-HYDRATING MIND FROM SQLITE (SESSION 2: TICKS 7..12)")
    print("=" * 92)
    store_2 = PersistentMindStore(db_file)
    os_session_2 = NoesisCognitiveOS(seed=99)
    restored = store_2.load_into_os(os_session_2)
    print(
        f"  [Re-Hydrated Checkpoint] Restored={restored} | Resuming at Tick={os_session_2.tick_count} "
        f"| SemanticLaws={len(os_session_2.memory.semantic_graph)} "
        f"| CompiledSkills={len(os_session_2.memory.procedural_skills)}"
    )

    for _ in range(6):
        entry = await os_session_2.step_autonomous_tick()
        store_2.save_os_state(os_session_2)
        print(
            f"  [Session 2 | Tick {entry['tick']:02d}] Winner={entry['winning_agent']:<28} "
            f"| FreeEnergy={entry['free_energy']:.3f} | Temperament={entry['temperament']}"
        )

    snap = store_2.export_snapshot()
    print("\n" + "=" * 92)
    print("PERSISTENT SQLITE MIND STORE AUDIT SUMMARY")
    print("=" * 92)
    print(f"  - SQLite Database File            : {db_file.name} ({db_file.stat().st_size:,} bytes)")
    print(f"  - Total Broadcast Ticks Persisted : {len(snap['broadcast_history'])}")
    print(f"  - Active Tier-1 Episodic Memories : {len(snap['tier1_episodic_buffer'])}")
    print(f"  - Distilled Tier-2 Semantic Laws  : {len(snap['tier2_semantic_schemas'])}")
    print(f"  - Compiled Tier-3 Muscle Skills   : {len(snap['tier3_procedural_skills'])}")
    print(f"  - Tier-4 Autobiographical Entries : {len(snap['tier4_autobiographical_spine'])}")
    print("=" * 92)
    store_2.close()


if __name__ == "__main__":
    asyncio.run(run_persistent_daemon_demo())