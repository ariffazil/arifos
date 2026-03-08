"""
arifosmcp.intelligence/core/vault_logger.py — Tri-Witness Consensus + VAULT999 Ledger

Implements the Tri-Witness (H+A+E) consensus scoring and writes sealed
decisions to the VAULT999 immutable ledger. Falls back to a local JSON
log when Postgres is unavailable (safe for local dev).

Floors enforced: F1 (Amanah/Auditability), F3 (Tri-Witness Consensus)
Authority: ARIF FAZIL (Sovereign)
Version: 2026.02.22-FORGE-KERNEL-SEAL
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# WitnessRecord — Immutable audit entry
# ---------------------------------------------------------------------------


@dataclass
class WitnessRecord:
    session_id: str
    query: str
    response: str
    floor_audit: dict[str, float]  # floor_id → score
    verdict: str
    witness_human: float  # H score [0.0, 1.0]
    witness_ai: float  # A score [0.0, 1.0]
    witness_earth: float  # E score [0.0, 1.0]
    timestamp: str  # ISO-8601 UTC
    seal_hash: str | None = None  # SHA-256 of record content

    @property
    def consensus_score(self) -> float:
        """W₃ = mean of H + A + E witness scores."""
        return (self.witness_human + self.witness_ai + self.witness_earth) / 3.0

    @property
    def consensus_passed(self) -> bool:
        """F3 threshold: W₃ ≥ 0.95"""
        return self.consensus_score >= 0.95


# ---------------------------------------------------------------------------
# VaultLogger
# ---------------------------------------------------------------------------


class VaultLogger:
    """
    Tri-Witness (H+A+E) consensus logger with VAULT999 ledger.

    Strategy:
      - If Postgres DSN is configured (via env VAULT999_DSN), write to DB.
      - Otherwise, append to a local JSONL file at `vault_path`.
    """

    _JSONL_FILENAME = "vault999.jsonl"

    def __init__(
        self,
        db_config: dict[str, str] | None = None,
        vault_path: str | None = None,
    ) -> None:
        self._conn: Any = None
        self._vault_path: Path

        # Attempt Postgres connection
        dsn = (db_config or {}).get("dsn") or os.environ.get("VAULT999_DSN", "")
        if dsn:
            self._conn = self._init_postgres(dsn)

        # Fallback JSON-lines path
        if vault_path:
            self._vault_path = Path(vault_path)
        else:
            # Default: store alongside arifosmcp.intelligence package root
            self._vault_path = (
                Path(__file__).parent.parent.parent / "VAULT999" / self._JSONL_FILENAME
            )
        self._vault_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def log_decision(
        self,
        session_id: str,
        query: str,
        response: str,
        floor_audit: dict[str, float],
        verdict: str,
        witness_human: float = 0.0,
        witness_earth: float = 0.0,
    ) -> WitnessRecord:
        """
        Create a Tri-Witness record and commit to VAULT999.

        F1 Amanah: Record is cryptographically sealed (SHA-256).
        F3 Consensus: W₃ = (H + A + E) / 3.
        AI witness (A) is always 1.0 — the system is always present.
        """
        record = WitnessRecord(
            session_id=session_id,
            query=query[:1024],  # Truncate for safety
            response=response[:2048],
            floor_audit=floor_audit,
            verdict=verdict,
            witness_human=max(0.0, min(1.0, witness_human)),
            witness_ai=1.0,  # AI always present
            witness_earth=max(0.0, min(1.0, witness_earth)),
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
        )
        record.seal_hash = self._compute_seal_hash(record)

        if self._conn:
            self._write_postgres(record)
        else:
            self._write_jsonl(record)

        return record

    def log_witness(
        self,
        session_id: str,
        agent_id: str,
        stage: str,
        statement: str,
        verdict: str,
        *,
        floor_audit: dict[str, float] | None = None,
        witness_human: float = 0.0,
        witness_earth: float = 0.0,
    ) -> WitnessRecord:
        """
        Backwards-compatible witness logger used by legacy triad modules.

        New code should prefer :meth:`log_decision`. This wrapper preserves the
        historical call signature:
            log_witness(session_id, agent_id, stage, statement, verdict)
        """
        response = json.dumps(
            {"agent_id": agent_id, "stage": stage, "verdict": verdict},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return self.log_decision(
            session_id=session_id,
            query=statement,
            response=response,
            floor_audit=floor_audit or {},
            verdict=verdict,
            witness_human=witness_human,
            witness_earth=witness_earth,
        )

    def get_session_records(self, session_id: str) -> list[dict]:
        """Retrieve all records for a session (JSONL fallback only)."""
        records = []
        if self._vault_path.exists():
            with open(self._vault_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                        if row.get("session_id") == session_id:
                            records.append(row)
                    except json.JSONDecodeError:
                        continue
        return records

    # ------------------------------------------------------------------
    # Internal: Postgres
    # ------------------------------------------------------------------

    def _init_postgres(self, dsn: str) -> Any:
        try:
            import psycopg2  # type: ignore[import]

            conn = psycopg2.connect(dsn)
            self._ensure_schema(conn)
            return conn
        except Exception:
            return None  # Graceful fallback to JSONL

    def _ensure_schema(self, conn: Any) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS vault999 (
            id            SERIAL PRIMARY KEY,
            session_id    TEXT NOT NULL,
            query         TEXT,
            response      TEXT,
            floor_audit   JSONB,
            verdict       TEXT,
            witness_human FLOAT,
            witness_ai    FLOAT,
            witness_earth FLOAT,
            consensus     FLOAT,
            seal_hash     TEXT UNIQUE,
            created_at    TIMESTAMPTZ DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS vault999_session_idx ON vault999(session_id);
        """
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    def _write_postgres(self, record: WitnessRecord) -> None:
        sql = """
        INSERT INTO vault999
            (session_id, query, response, floor_audit, verdict,
             witness_human, witness_ai, witness_earth, consensus, seal_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (seal_hash) DO NOTHING;
        """
        try:
            from psycopg2.extras import Json  # type: ignore[import]

            with self._conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        record.session_id,
                        record.query,
                        record.response,
                        Json(record.floor_audit),
                        record.verdict,
                        record.witness_human,
                        record.witness_ai,
                        record.witness_earth,
                        record.consensus_score,
                        record.seal_hash,
                    ),
                )
            self._conn.commit()
        except Exception:
            # Fallback to JSONL on write failure
            self._write_jsonl(record)

    # ------------------------------------------------------------------
    # Internal: JSONL fallback
    # ------------------------------------------------------------------

    def _write_jsonl(self, record: WitnessRecord) -> None:
        row = asdict(record)
        row["consensus_score"] = record.consensus_score
        with open(self._vault_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")

    # ------------------------------------------------------------------
    # Internal: Seal hash computation (F1 Amanah)
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_seal_hash(record: WitnessRecord) -> str:
        """SHA-256 of canonical record content for tamper-evidence."""
        content = json.dumps(
            {
                "session_id": record.session_id,
                "query": record.query,
                "response": record.response,
                "verdict": record.verdict,
                "timestamp": record.timestamp,
            },
            sort_keys=True,
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
