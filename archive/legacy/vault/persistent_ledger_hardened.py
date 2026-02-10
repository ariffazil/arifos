"""
HARDENED Vault999 Persistent Ledger — PostgreSQL backend (append-only, hash-chained).

Hardening features:
- Incremental Merkle tree: O(log N) append instead of O(N)
- Proper JSONB handling: Pass dict to asyncpg (not serialized string)
- Pre-vault seal contract: Enforces SEAL must be earned
- VOID is expensive: Requires tri-witness + floor validation
- Concurrency-safe via advisory locks
- Full verification & inclusion proofs

Doctrine: Theory of Anomalous Contrast (888_SOUL_VERDICT.md)
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

# Import incremental Merkle
try:
    from codebase.vault.incremental_merkle import PersistentMerkleState, sha256_hash
    INCREMENTAL_MERKLE_AVAILABLE = True
except ImportError:
    INCREMENTAL_MERKLE_AVAILABLE = False

try:
    import asyncpg
except ImportError:
    asyncpg = None  # type: ignore[assignment]

GENESIS_HASH = "0" * 64
ADVISORY_LOCK_KEY = 999_911_777


# =============================================================================
# SEAL CONTRACT: Pre-vault validation (VOID is expensive, SEAL is earned)
# =============================================================================

class SealContractViolation(Exception):
    """Raised when seal_data doesn't meet contract requirements."""
    pass


def enforce_seal_contract(seal_data: Dict[str, Any], verdict: str) -> None:
    """
    HARDENED: Enforce pre-vault seal contract.
    
    Theory of Anomalous Contrast:
    - VOID must be EXPENSIVE (requires tri-witness + justification)
    - SEAL must be EARNED (requires EUREKA score >= 0.75)
    - SABAR is DEFAULT (if no clear EUREKA)
    
    Raises SealContractViolation if contract not met.
    """
    # Required fields check
    required_top = ["query", "trinity"]
    for field in required_top:
        if field not in seal_data:
            raise SealContractViolation(f"Missing required field: {field}")
    
    trinity = seal_data.get("trinity", {})
    required_trinity = ["init", "agi", "asi", "apex"]
    for field in required_trinity:
        if field not in trinity:
            raise SealContractViolation(f"Missing trinity component: {field}")
    
    # Tri-witness validation
    apex = trinity.get("apex", {})
    tri_witness = apex.get("tri_witness")
    if tri_witness is None:
        raise SealContractViolation("Missing tri_witness in apex results")
    
    if not isinstance(tri_witness, (int, float)):
        raise SealContractViolation(f"tri_witness must be numeric, got {type(tri_witness)}")
    
    # SEAL requires high tri-witness
    if verdict == "SEAL" and tri_witness < 0.95:
        raise SealContractViolation(
            f"SEAL requires tri_witness >= 0.95, got {tri_witness}. "
            "Use SABAR for partial consensus."
        )
    
    # VOID requires justification
    if verdict == "VOID":
        failed_floors = apex.get("failed_floors", [])
        if not failed_floors:
            raise SealContractViolation(
                "VOID requires failed_floors justification. "
                "VOID must be expensive - cannot reject without reason."
            )
    
    # EUREKA validation for SEAL
    if verdict == "SEAL":
        eureka = seal_data.get("eureka", {})
        eureka_score = eureka.get("eureka_score", 0.0)
        eureka_verdict = eureka.get("verdict", "TRANSIENT")
        
        if eureka_verdict != "SEAL":
            raise SealContractViolation(
                f"Vault SEAL requires EUREKA verdict SEAL, got {eureka_verdict}. "
                f"EUREKA Score: {eureka_score:.2f}"
            )
        
        if eureka_score < 0.75:
            raise SealContractViolation(
                f"SEAL requires EUREKA score >= 0.75, got {eureka_score:.2f}. "
                "SEAL must be earned through anomalous contrast."
            )


# =============================================================================
# Merkle root computation (fallback if incremental not available)
# =============================================================================

def _merkle_root(hashes: List[str]) -> str:
    """Compute Merkle root from a list of hashes (O(N) fallback)."""
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


# =============================================================================
# Configuration
# =============================================================================

def should_use_postgres() -> bool:
    """Return True when Postgres backend is requested (default)."""
    backend = os.environ.get("VAULT_BACKEND", "postgres").lower()
    return backend == "postgres" or bool(
        os.environ.get("VAULT_POSTGRES_DSN") or os.environ.get("DATABASE_URL")
    )


def get_vault_dsn() -> str:
    """Get PostgreSQL DSN from environment."""
    dsn = os.environ.get("VAULT_POSTGRES_DSN") or os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError(
            "DATABASE_URL or VAULT_POSTGRES_DSN environment variable must be set. "
            "Postgres DSN is required for VAULT999 persistence."
        )
    return dsn


# =============================================================================
# Data classes
# =============================================================================

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


# =============================================================================
# Hardened Persistent Vault Ledger
# =============================================================================

class HardenedPersistentVaultLedger:
    """
    HARDENED Async Postgres-backed ledger.
    
    Features:
    - Incremental Merkle tree (O(log N) append)
    - Seal contract enforcement (VOID expensive, SEAL earned)
    - Proper JSONB handling (pass dict, not string)
    """

    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or get_vault_dsn()
        self._pool: Optional[asyncpg.Pool] = None
        self._merkle_state: Optional[PersistentMerkleState] = None

    async def connect(self):
        if asyncpg is None:
            raise RuntimeError(
                "asyncpg is not installed. Install with: pip install asyncpg"
            )
        if self._pool is None:
            # Railway TCP proxy requires SSL
            import ssl
            ssl_mode = os.environ.get("VAULT_SSL_MODE", "require")
            
            pool_kwargs = {"min_size": 1, "max_size": 5}
            
            if ssl_mode == "require":
                # Create SSL context that accepts Railway's cert
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                pool_kwargs["ssl"] = ssl_context
            elif ssl_mode == "disable":
                pool_kwargs["ssl"] = False
            
            self._pool = await asyncpg.create_pool(self.dsn, **pool_kwargs)
            # Load or initialize Merkle state
            if INCREMENTAL_MERKLE_AVAILABLE:
                self._merkle_state = await self._load_merkle_state()

    async def close(self):
        """Close pool. Call only on application shutdown."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def _load_merkle_state(self) -> PersistentMerkleState:
        """Load persisted Merkle state from database."""
        if not INCREMENTAL_MERKLE_AVAILABLE:
            return PersistentMerkleState()
        
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT merkle_state FROM vault_merkle_state WHERE id=1"
            )
            if row and row["merkle_state"]:
                return PersistentMerkleState.from_json(row["merkle_state"])
            return PersistentMerkleState()

    async def _save_merkle_state(self, conn):
        """Save Merkle state to database."""
        if not INCREMENTAL_MERKLE_AVAILABLE or not self._merkle_state:
            return
        
        state_json = self._merkle_state.to_json()
        exists = await conn.fetchrow("SELECT 1 FROM vault_merkle_state WHERE id=1")
        if exists:
            await conn.execute(
                "UPDATE vault_merkle_state SET merkle_state=$1, updated_at=now() WHERE id=1",
                json.dumps(state_json)
            )
        else:
            await conn.execute(
                "INSERT INTO vault_merkle_state (id, merkle_state) VALUES (1, $1)",
                json.dumps(state_json)
            )

    # ------------------------------------------------------------------ core (HARDENED)
    async def append(
        self,
        session_id: str,
        verdict: str,
        seal_data: Dict[str, Any],
        authority: str,
        seal_id: Optional[UUID] = None,
        skip_contract: bool = False,
    ) -> Dict[str, Any]:
        """
        HARDENED: Concurrency-safe append with seal contract enforcement.
        
        - O(log N) Merkle update (incremental)
        - Seal contract validation (VOID expensive, SEAL earned)
        - Proper JSONB handling (dict, not string)
        """
        # HARDENED: Enforce seal contract before DB write
        if not skip_contract:
            try:
                enforce_seal_contract(seal_data, verdict)
            except SealContractViolation as e:
                return {
                    "operation": "rejected",
                    "verdict": "VOID",
                    "reason": str(e),
                    "contract_violation": True,
                }
        
        await self.connect()
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SELECT pg_advisory_xact_lock($1)", ADVISORY_LOCK_KEY)

                # Get prev_hash (last entry)
                row = await conn.fetchrow(
                    "SELECT entry_hash FROM vault_ledger ORDER BY sequence DESC LIMIT 1"
                )
                prev_hash = row["entry_hash"] if row else GENESIS_HASH

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

                # HARDENED: Incremental Merkle (O(log N))
                if INCREMENTAL_MERKLE_AVAILABLE and self._merkle_state:
                    merkle_root = self._merkle_state.append_leaf(
                        entry_hash, 
                        await self._get_next_sequence(conn)
                    )
                    await self._save_merkle_state(conn)
                else:
                    # Fallback: O(N) full recompute
                    rows = await conn.fetch(
                        "SELECT entry_hash FROM vault_ledger ORDER BY sequence"
                    )
                    existing_hashes = [r["entry_hash"] for r in rows]
                    new_hashes = existing_hashes + [entry_hash]
                    merkle_root = _merkle_root(new_hashes)

                # HARDENED: Pass seal_data as dict (JSONB), not serialized string
                # asyncpg handles JSONB serialization automatically
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
                    seal_data,  # HARDENED: Pass dict for JSONB
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
                    "contract_enforced": not skip_contract,
                }

    async def _get_next_sequence(self, conn) -> int:
        """Get next sequence number."""
        row = await conn.fetchrow("SELECT MAX(sequence) as max_seq FROM vault_ledger")
        return (row["max_seq"] or 0) + 1

    # ------------------------------------------------------------------ query methods
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
        limit = max(1, min(limit, 1000))
        await self.connect()
        async with self._pool.acquire() as conn:
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
        self, verdict: str, start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None, cursor: Optional[int] = None, limit: int = 100
    ) -> Dict[str, Any]:
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
            return {"entries": entries, "next_cursor": next_cursor, "has_more": has_more}

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
                return {"valid": False, "first_invalid_seq": None, "reason": "head-mismatch"}
            if head and head["head_merkle_root"] != root:
                return {"valid": False, "first_invalid_seq": None, "reason": "merkle-mismatch"}
            return {"valid": True, "merkle_root": root, "entries": len(hashes)}

    async def get_merkle_proof(self, sequence: int) -> Optional[Dict[str, Any]]:
        """Get Merkle inclusion proof for a specific entry."""
        await self.connect()
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT sequence, entry_hash FROM vault_ledger ORDER BY sequence ASC"
            )
            pairs = [(r["sequence"], r["entry_hash"]) for r in rows]
            hashes = [h for _, h in pairs]
            index = None
            for i, (seq, _) in enumerate(pairs):
                if seq == sequence:
                    index = i
                    break
            if index is None:
                return None
            
            proof = []
            level = list(hashes)
            idx = index
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
            return {"root": level[0], "proof": proof, "leaf_index": index}

    # ------------------------------------------------------------------ helpers
    def _compute_entry_hash(
        self, session_id: str, timestamp: datetime, authority: str,
        verdict: str, seal_data: Dict[str, Any], prev_hash: Optional[str], seal_id: UUID
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
                sequence, entry_hash, merkle_root,
            )
        else:
            await conn.execute(
                """
                INSERT INTO vault_head (id, head_sequence, head_entry_hash, head_merkle_root)
                VALUES (1, $1, $2, $3)
                """,
                sequence, entry_hash, merkle_root,
            )


# Singleton
_ledger_singleton: Optional[HardenedPersistentVaultLedger] = None


def get_hardened_vault_ledger() -> HardenedPersistentVaultLedger:
    global _ledger_singleton
    if _ledger_singleton is None:
        _ledger_singleton = HardenedPersistentVaultLedger()
    return _ledger_singleton
