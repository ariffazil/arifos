"""
Vault999 Persistent Ledger — PostgreSQL backend (append-only, hash-chained).

Guarantees:
- Append-only writes with prev_hash linking
- Deterministic entry_hash
- Ledger-wide Merkle root
- Concurrency-safe via advisory locks
- Full verification & inclusion proofs

TODO(scalability): Merkle root is O(N) on every append. Optimize with incremental
updates or periodic checkpoints for high-throughput scenarios.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

try:
    import asyncpg
except ImportError:
    asyncpg = None  # type: ignore[assignment]

GENESIS_HASH = "0" * 64
ADVISORY_LOCK_KEY = 999_911_777  # arbitrary constant for vault head


def _merkle_root(hashes: List[str]) -> str:
    """Compute Merkle root from a list of hashes."""
    if not hashes:
        return hashlib.sha256(b"EMPTY_LEDGER").hexdigest()
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level: List[str] = []
        for i in range(0, len(level), 2):
            next_level.append(
                hashlib.sha256((level[i] + level[i + 1]).encode("utf-8")).hexdigest()
            )
        level = next_level
    return level[0]


def _parse_seal_data(seal_data_val: Union[str, Dict[str, Any], Any]) -> Dict[str, Any]:
    """
    Parse seal_data from database row.
    
    Handles both JSONB (returns dict) and TEXT (returns str) column types.
    asyncpg with JSONB column returns Python dict directly.
    """
    if isinstance(seal_data_val, dict):
        return seal_data_val
    if isinstance(seal_data_val, str):
        try:
            parsed = json.loads(seal_data_val)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def should_use_postgres() -> bool:
    """Return True when Postgres backend is requested (default)."""
    backend = os.environ.get("VAULT_BACKEND", "postgres").lower()
    return backend == "postgres" or bool(os.environ.get("VAULT_POSTGRES_DSN") or os.environ.get("DATABASE_URL"))


def get_vault_dsn() -> str:
    """Get PostgreSQL DSN from environment."""
    dsn = (
        os.environ.get("VAULT_POSTGRES_DSN")
        or os.environ.get("DATABASE_URL")
    )
    if not dsn:
        raise RuntimeError(
            "DATABASE_URL or VAULT_POSTGRES_DSN environment variable must be set. "
            "Postgres DSN is required for VAULT999 persistence."
        )
    return dsn


@dataclass
class SealRow:
    sequence: int
    session_id: str
    seal_id: UUID
    timestamp: datetime
    authority: str
    verdict: str
    seal_data: Dict[str, Any]
    entry_hash: str
    prev_hash: Optional[str]
    merkle_root: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence": self.sequence,
            "session_id": self.session_id,
            "seal_id": str(self.seal_id),
            "timestamp": self.timestamp.isoformat(),
            "authority": self.authority,
            "verdict": self.verdict,
            "seal_data": self.seal_data,
            "entry_hash": self.entry_hash,
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
        }


class PersistentVaultLedger:
    """
    Async Postgres-backed ledger.
    
    NOTE: This class maintains a connection pool. For production use,
    instantiate once and reuse (via get_vault_ledger() singleton).
    Do not create/destroy pools per request.
    """

    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or get_vault_dsn()
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if asyncpg is None:
            raise RuntimeError(
                "asyncpg is not installed. Install with: pip install asyncpg"
            )
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=5)

    async def close(self):
        """Close pool. Call only on application shutdown."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    # ------------------------------------------------------------------ core
    async def append(
        self,
        session_id: str,
        verdict: str,
        seal_data: Dict[str, Any],
        authority: str,
        seal_id: Optional[UUID] = None,
    ) -> Dict[str, Any]:
        """
        Concurrency-safe append. Ensures single chain head via advisory lock.
        
        NOTE: This recomputes full Merkle tree O(N) for correctness.
        TODO: Optimize with incremental Merkle for high throughput.
        """
        await self.connect()
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SELECT pg_advisory_xact_lock($1)", ADVISORY_LOCK_KEY)

                # Get existing hashes for merkle + prev_hash
                rows = await conn.fetch("SELECT entry_hash FROM vault_ledger ORDER BY sequence")
                existing_hashes = [r["entry_hash"] for r in rows]
                prev_hash = existing_hashes[-1] if existing_hashes else GENESIS_HASH

                timestamp = datetime.now(timezone.utc)
                seal_id = seal_id or uuid4()
                entry_hash = self._compute_entry_hash(
                    session_id=session_id,
                    timestamp=timestamp,
                    authority=authority,
                    verdict=verdict,
                    seal_data=seal_data,
                    prev_hash=prev_hash,
                    seal_id=seal_id,
                )

                new_hashes = existing_hashes + [entry_hash]
                merkle_root = _merkle_root(new_hashes)

                # Serialize seal_data for DB (works for TEXT or JSONB column)
                seal_data_serialized = json.dumps(seal_data, sort_keys=True)
                row = await conn.fetchrow(
                    """
                    INSERT INTO vault_ledger
                        (session_id, seal_id, timestamp, authority, verdict,
                         seal_data, entry_hash, prev_hash, merkle_root)
                    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                    RETURNING sequence, created_at
                    """,
                    session_id,
                    seal_id,
                    timestamp,
                    authority,
                    verdict,
                    seal_data_serialized,
                    entry_hash,
                    prev_hash,
                    merkle_root,
                )

                sequence = row["sequence"]
                await self._ensure_head(conn, sequence, entry_hash, merkle_root)

                return {
                    "sequence_number": sequence,
                    "entry_hash": entry_hash,
                    "prev_hash": prev_hash,
                    "merkle_root": merkle_root,
                    "seal_id": str(seal_id),
                    "timestamp": timestamp.isoformat(),
                    "vault_backend": "postgres",
                }

    async def get_entries_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        await self.connect()
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT sequence, session_id, seal_id, timestamp, authority, verdict,
                       seal_data, entry_hash, prev_hash, merkle_root
                FROM vault_ledger
                WHERE session_id = $1
                ORDER BY sequence ASC
                """,
                session_id,
            )
            return [self._row_to_entry(r).to_dict() for r in rows]

    async def get_entry_by_sequence(self, sequence: int) -> Optional[Dict[str, Any]]:
        await self.connect()
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT sequence, session_id, seal_id, timestamp, authority, verdict,
                       seal_data, entry_hash, prev_hash, merkle_root
                FROM vault_ledger
                WHERE sequence = $1
                """,
                sequence,
            )
            return self._row_to_entry(row).to_dict() if row else None

    async def list_entries(self, cursor: Optional[int] = None, limit: int = 50) -> Dict[str, Any]:
        """List entries with pagination. cursor=None means start from latest."""
        # Clamp limit to reasonable range
        limit = max(1, min(limit, 1000))
        
        await self.connect()
        async with self._pool.acquire() as conn:
            # Use 'IS NOT NULL' check to handle cursor=0 correctly
            if cursor is not None:
                rows = await conn.fetch(
                    """
                    SELECT sequence, session_id, seal_id, timestamp, authority, verdict,
                           seal_data, entry_hash, prev_hash, merkle_root
                    FROM vault_ledger
                    WHERE sequence < $1
                    ORDER BY sequence DESC
                    LIMIT $2
                    """,
                    cursor,
                    limit + 1,
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT sequence, session_id, seal_id, timestamp, authority, verdict,
                           seal_data, entry_hash, prev_hash, merkle_root
                    FROM vault_ledger
                    ORDER BY sequence DESC
                    LIMIT $1
                    """,
                    limit + 1,
                )
            has_more = len(rows) > limit
            rows = rows[:limit]
            entries = [self._row_to_entry(r).to_dict() for r in rows]
            next_cursor = entries[-1]["sequence"] if entries and has_more else None
            return {"entries": entries, "next_cursor": next_cursor, "has_more": has_more}

    async def query_by_verdict(
        self,
        verdict: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        cursor: Optional[int] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """Query entries by verdict with optional time range and pagination."""
        # Clamp limit
        limit = max(1, min(limit, 1000))
        
        await self.connect()
        clauses = ["verdict = $1"]
        params: List[Any] = [verdict]
        idx = 2
        if start_time:
            clauses.append(f"timestamp >= ${idx}")
            params.append(start_time)
            idx += 1
        if end_time:
            clauses.append(f"timestamp <= ${idx}")
            params.append(end_time)
            idx += 1
        if cursor is not None:
            clauses.append(f"sequence < ${idx}")
            params.append(cursor)
            idx += 1
        where = " AND ".join(clauses)
        sql = f"""
            SELECT sequence, session_id, seal_id, timestamp, authority, verdict,
                   seal_data, entry_hash, prev_hash, merkle_root
            FROM vault_ledger
            WHERE {where}
            ORDER BY sequence DESC
            LIMIT ${idx}
        """
        params.append(limit + 1)
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
            has_more = len(rows) > limit
            rows = rows[:limit]
            entries = [self._row_to_entry(r).to_dict() for r in rows]
            next_cursor = entries[-1]["sequence"] if entries and has_more else None
            return {
                "entries": entries,
                "next_cursor": next_cursor,
                "has_more": has_more,
            }

    async def verify_chain(self) -> Dict[str, Any]:
        """Verify full chain integrity."""
        await self.connect()
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT sequence, session_id, seal_id, timestamp, authority, verdict,
                       seal_data, entry_hash, prev_hash
                FROM vault_ledger
                ORDER BY sequence ASC
                """
            )
            hashes: List[str] = []
            prev = GENESIS_HASH
            for row in rows:
                seq = row["sequence"]
                entry_hash = row["entry_hash"]
                prev_hash = row["prev_hash"] or GENESIS_HASH
                
                # Parse seal_data handling both JSONB (dict) and TEXT (str)
                seal_data = _parse_seal_data(row["seal_data"])
                
                recomputed = self._compute_entry_hash(
                    session_id=row["session_id"],
                    timestamp=row["timestamp"],
                    authority=row["authority"],
                    verdict=row["verdict"],
                    seal_data=seal_data,
                    prev_hash=prev_hash,
                    seal_id=row["seal_id"],
                )
                if recomputed != entry_hash:
                    return {
                        "valid": False,
                        "first_invalid_seq": seq,
                        "reason": "hash-mismatch",
                        "checked_count": len(hashes),
                    }
                if prev_hash != prev:
                    return {
                        "valid": False,
                        "first_invalid_seq": seq,
                        "reason": "prev-hash-mismatch",
                        "checked_count": len(hashes),
                    }
                hashes.append(entry_hash)
                prev = entry_hash

            root = _merkle_root(hashes)
            head = await conn.fetchrow(
                "SELECT head_entry_hash, head_merkle_root FROM vault_head WHERE id=1"
            )
            if head and head["head_entry_hash"] != (hashes[-1] if hashes else GENESIS_HASH):
                return {
                    "valid": False,
                    "first_invalid_seq": None,
                    "reason": "head-mismatch",
                    "checked_count": len(hashes),
                }
            if head and head["head_merkle_root"] != root:
                return {
                    "valid": False,
                    "first_invalid_seq": None,
                    "reason": "merkle-mismatch",
                    "checked_count": len(hashes),
                }
            return {
                "valid": True,
                "merkle_root": root,
                "entries": len(hashes),
                "checked_count": len(hashes),
            }

    async def get_merkle_proof(self, sequence: int) -> Optional[Dict[str, Any]]:
        """
        Get Merkle inclusion proof for a specific entry.
        
        Finds entry by sequence number (not index) to handle gaps correctly.
        """
        await self.connect()
        async with self._pool.acquire() as conn:
            # Fetch (sequence, entry_hash) pairs to locate by sequence
            rows = await conn.fetch(
                "SELECT sequence, entry_hash FROM vault_ledger ORDER BY sequence ASC"
            )
            
            # Build list of hashes and find index by sequence
            pairs = [(r["sequence"], r["entry_hash"]) for r in rows]
            hashes = [h for _, h in pairs]
            
            # Find index where sequence matches
            index = None
            for i, (seq, _) in enumerate(pairs):
                if seq == sequence:
                    index = i
                    break
            
            if index is None:
                return None
            
            idx = index
            proof: List[Dict[str, Any]] = []
            # CRITICAL: Copy hashes to avoid mutating original list
            level = list(hashes)
            
            while len(level) > 1:
                if len(level) % 2 == 1:
                    level.append(level[-1])
                is_right = idx % 2 == 1
                sibling = level[idx - 1] if is_right else level[idx + 1]
                proof.append({"hash": sibling, "position": "left" if is_right else "right"})
                idx = idx // 2
                next_level = []
                for i in range(0, len(level), 2):
                    next_level.append(hashlib.sha256((level[i] + level[i + 1]).encode()).hexdigest())
                level = next_level
            root = level[0]
            return {"root": root, "proof": proof, "leaf_index": index}

    # ------------------------------------------------------------------ helpers
    def _compute_entry_hash(
        self,
        session_id: str,
        timestamp: datetime,
        authority: str,
        verdict: str,
        seal_data: Dict[str, Any],
        prev_hash: Optional[str],
        seal_id: UUID,
    ) -> str:
        canonical = {
            "session_id": session_id,
            "timestamp": timestamp.isoformat(),
            "authority": authority,
            "verdict": verdict,
            "seal_data": seal_data,
            "prev_hash": prev_hash or GENESIS_HASH,
            "seal_id": str(seal_id),
        }
        canonical_json = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    def _row_to_entry(self, row) -> SealRow:
        """Convert database row to SealRow, handling JSONB/Text seal_data."""
        # Handle both JSONB (dict) and TEXT (str) column types
        seal_data = _parse_seal_data(row["seal_data"])
        
        return SealRow(
            sequence=row["sequence"],
            session_id=row["session_id"],
            seal_id=row["seal_id"],
            timestamp=row["timestamp"],
            authority=row["authority"],
            verdict=row["verdict"],
            seal_data=seal_data,
            entry_hash=row["entry_hash"],
            prev_hash=row["prev_hash"],
            merkle_root=row["merkle_root"],
        )

    async def _ensure_head(self, conn, sequence: int, entry_hash: str, merkle_root: str):
        exists = await conn.fetchrow("SELECT 1 FROM vault_head WHERE id=1")
        if exists:
            await conn.execute(
                """
                UPDATE vault_head
                SET head_sequence=$1, head_entry_hash=$2, head_merkle_root=$3, updated_at=now()
                WHERE id=1
                """,
                sequence,
                entry_hash,
                merkle_root,
            )
        else:
            await conn.execute(
                """
                INSERT INTO vault_head (id, head_sequence, head_entry_hash, head_merkle_root)
                VALUES (1, $1, $2, $3)
                """,
                sequence,
                entry_hash,
                merkle_root,
            )


# Singleton helper
_ledger_singleton: Optional[PersistentVaultLedger] = None


def get_vault_ledger() -> PersistentVaultLedger:
    """
    Get the singleton PersistentVaultLedger instance.
    
    For production, use this singleton to avoid creating multiple connection pools.
    The pool is created on first connect() and should be closed only on application shutdown.
    """
    global _ledger_singleton
    if _ledger_singleton is None:
        _ledger_singleton = PersistentVaultLedger()
    return _ledger_singleton
