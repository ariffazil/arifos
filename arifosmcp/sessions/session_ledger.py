"""
SessionLedger — VAULT999 Unified Ledger

UNIFIED: PostgreSQL + Redis + Merkle Tree + EUREKA Sieve
Provides Merkle-chained, EUREKA-filtered, multi-backend audit trail.
Schema: VAULT999 v3 UNIFIED

DITEMPA BUKAN DIBERI
"""

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

# Try to import asyncpg for Postgres support
try:
    import asyncpg

    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False

# ═══ WIRE EXISTING COMPONENTS ═══
# Merkle tree from core.shared.crypto
# Redis MindVault from aaa_mcp.services.redis_client
from aaa_mcp.services.redis_client import MindVault

# EUREKA Sieve from aaa_mcp.vault.hardened
from aaa_mcp.vault.hardened import (
    HardenedEUREKASieve,
    should_seal_to_vault_hardened,
)
from core.shared.crypto import merkle_root


@dataclass
class VaultEntry:
    """VAULT999 v3 UNIFIED entry schema with Merkle root."""

    entry_id: str
    session_id: str
    timestamp: str
    verdict_type: str  # SEAL | VOID | PARTIAL | SABAR | 888_HOLD
    risk_level: str  # LOW | MEDIUM | HIGH | CRITICAL
    category: str
    environment: str
    payload: dict[str, Any]
    query_summary: str
    prev_hash: str
    entry_hash: str
    schema_version: str = "3.0"
    floors_checked: list[str] = None
    floors_failed: list[str] = None
    # UNIFIED: Merkle root for tamper-evident chain
    merkle_root: str = ""
    # UNIFIED: EUREKA score metadata
    eureka_score: float = 0.0
    eureka_verdict: str = "TRANSIENT"  # SEAL | SABAR | TRANSIENT

    def __post_init__(self):
        if self.floors_checked is None:
            self.floors_checked = []
        if self.floors_failed is None:
            self.floors_failed = []
        if not self.merkle_root:
            self.merkle_root = self.entry_hash  # Fallback


# Compatibility alias for legacy code
SessionEntry = VaultEntry


class SessionLedger:
    """
    VAULT999 UNIFIED Ledger — PostgreSQL + Redis + Merkle + EUREKA

    Unified backends:
    - PostgreSQL: Authoritative persistent ledger
    - Redis: Hot cache via MindVault
    - Merkle tree: Tamper-evident cryptographic chain
    - EUREKA sieve: Anomalous contrast filtering
    """

    # SQL for creating the vault table (UNIFIED with Merkle)
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS vault999 (
        id SERIAL PRIMARY KEY,
        entry_id VARCHAR(64) UNIQUE NOT NULL,
        session_id VARCHAR(128) NOT NULL,
        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        verdict_type VARCHAR(20) NOT NULL,
        risk_level VARCHAR(20) NOT NULL,
        category VARCHAR(64),
        environment VARCHAR(20),
        payload JSONB,
        query_summary TEXT,
        prev_hash VARCHAR(64),
        entry_hash VARCHAR(64) NOT NULL,
        merkle_root VARCHAR(64),  -- UNIFIED: Merkle tree root
        eureka_score FLOAT DEFAULT 0.0,  -- UNIFIED: EUREKA evaluation
        eureka_verdict VARCHAR(20) DEFAULT 'TRANSIENT',
        schema_version VARCHAR(10) DEFAULT '3.0',
        floors_checked TEXT[],
        floors_failed TEXT[],
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_vault999_session ON vault999(session_id);
    CREATE INDEX IF NOT EXISTS idx_vault999_verdict ON vault999(verdict_type);
    CREATE INDEX IF NOT EXISTS idx_vault999_timestamp ON vault999(timestamp DESC);
    CREATE INDEX IF NOT EXISTS idx_vault999_merkle ON vault999(merkle_root);
    """

    CREATE_APPROVAL_REGISTRY_SQL = """
    CREATE TABLE IF NOT EXISTS approval_registry (
        id SERIAL PRIMARY KEY,
        approval_id VARCHAR(128) UNIQUE NOT NULL,
        session_id VARCHAR(128) NOT NULL,
        nonce VARCHAR(128) NOT NULL,
        tool_name VARCHAR(64) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        UNIQUE(session_id, nonce, tool_name)
    );

    CREATE INDEX IF NOT EXISTS idx_approval_registry_session ON approval_registry(session_id);
    CREATE INDEX IF NOT EXISTS idx_approval_registry_nonce ON approval_registry(nonce);
    """

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.environ.get("DATABASE_URL")
        self._pool: asyncpg.Pool | None = None
        self._memory_ledger: list[VaultEntry] = []
        self._last_hash = "GENESIS"
        self._initialized = False
        # UNIFIED: Redis cache
        self._redis = MindVault()
        # UNIFIED: EUREKA sieve for filtering
        self._eureka = HardenedEUREKASieve(vault_ledger=self)
        # UNIFIED: Merkle history (entry hashes for tree computation)
        self._merkle_history: list[str] = []
        self._approval_registry_ids: set[str] = set()
        self._approval_registry_nonce_keys: set[tuple[str, str, str]] = set()

    @property
    def is_postgres_available(self) -> bool:
        """Check if Postgres is configured and available."""
        return ASYNCPG_AVAILABLE and bool(self.database_url)

    async def initialize(self) -> bool:
        """Initialize the ledger (create table if needed, load Merkle history)."""
        if self._initialized:
            return True

        # Always try to initialize (Redis + EUREKA work even without Postgres)
        try:
            if self.is_postgres_available:
                self._pool = await asyncpg.create_pool(
                    self.database_url, min_size=1, max_size=5, command_timeout=30
                )
                async with self._pool.acquire() as conn:
                    await conn.execute(self.CREATE_TABLE_SQL)
                    await conn.execute(self.CREATE_APPROVAL_REGISTRY_SQL)
                    # UNIFIED: Load last hash AND Merkle history
                    rows = await conn.fetch(
                        "SELECT entry_hash, merkle_root FROM vault999 ORDER BY id ASC LIMIT 1000"
                    )
                    if rows:
                        self._last_hash = rows[-1]["entry_hash"]
                        # Rebuild Merkle history from chain
                        self._merkle_history = [row["entry_hash"] for row in rows]
                        print(
                            f"[VAULT999] Loaded {len(rows)} entries, Merkle root: {rows[-1]['merkle_root'][:16]}..."
                        )

            # UNIFIED: Also load recent entries from Redis cache
            redis_state = self._redis.load("vault999_chain")
            if redis_state and not self._merkle_history:
                # Use Redis as warm cache if Postgres empty
                self._merkle_history = redis_state.get("history", [])
                self._last_hash = redis_state.get("last_hash", "GENESIS")

            self._initialized = True
            return True

        except Exception as e:
            print(f"[SessionLedger] Init warning: {e}, using memory fallback")
            self._initialized = True
            return False

    async def mark_approval_used(
        self,
        approval_id: str,
        session_id: str,
        nonce: str,
        tool_name: str,
    ) -> bool:
        """Persist replay marker; return False when approval was already used."""
        await self.initialize()

        normalized_approval_id = str(approval_id or "").strip()
        normalized_session_id = str(session_id or "").strip()
        normalized_nonce = str(nonce or "").strip()
        normalized_tool = str(tool_name or "").strip()
        nonce_key = (normalized_session_id, normalized_nonce, normalized_tool)

        if self._pool:
            try:
                async with self._pool.acquire() as conn:
                    row = await conn.fetchrow(
                        """
                        INSERT INTO approval_registry (approval_id, session_id, nonce, tool_name)
                        VALUES ($1, $2, $3, $4)
                        ON CONFLICT DO NOTHING
                        RETURNING id
                        """,
                        normalized_approval_id,
                        normalized_session_id,
                        normalized_nonce,
                        normalized_tool,
                    )
                return row is not None
            except Exception as e:
                print(f"[SessionLedger] approval_registry write failed: {e}")

        if (
            normalized_approval_id in self._approval_registry_ids
            or nonce_key in self._approval_registry_nonce_keys
        ):
            return False

        self._approval_registry_ids.add(normalized_approval_id)
        self._approval_registry_nonce_keys.add(nonce_key)
        return True

    def _compute_hash(self, entry: VaultEntry) -> str:
        """Compute SHA256 hash for Merkle chain."""
        data = f"{entry.prev_hash}:{entry.session_id}:{entry.timestamp}:{entry.verdict_type}:{json.dumps(entry.payload, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _generate_entry_id(self) -> str:
        """Generate unique entry ID."""
        import secrets

        return secrets.token_hex(8)

    async def seal(
        self,
        session_id: str,
        verdict_type: str,
        payload: dict[str, Any],
        query_summary: str = "",
        risk_level: str = "LOW",
        category: str = "general",
        environment: str = "prod",
        floors_checked: list[str] | None = None,
        floors_failed: list[str] | None = None,
        query: str = "",  # For EUREKA evaluation
        response: str = "",  # For EUREKA evaluation
        trinity_bundle: dict[str, Any] | None = None,  # For EUREKA evaluation
    ) -> VaultEntry:
        """
        UNIFIED: Seal a new entry into VAULT999 with Merkle + EUREKA + Redis.

        Returns the sealed VaultEntry with computed hash and Merkle root.
        """
        await self.initialize()

        # UNIFIED: Run EUREKA sieve evaluation if query/response provided
        eureka_score = 0.0
        eureka_verdict = "TRANSIENT"
        if query and trinity_bundle:
            try:
                should_seal, eureka_meta = await should_seal_to_vault_hardened(
                    query=query,
                    response=response or json.dumps(payload),
                    trinity_bundle=trinity_bundle,
                    vault_ledger=self,
                )
                eureka_score = eureka_meta.get("eureka_score", 0.0)
                eureka_verdict = eureka_meta.get("verdict", "TRANSIENT")
                # Override verdict_type if EUREKA says TRANSIENT
                if eureka_verdict == "TRANSIENT" and verdict_type == "SEAL":
                    verdict_type = "SABAR"  # Downgrade to cooling
            except Exception as e:
                print(f"[VAULT999] EUREKA evaluation error: {e}, proceeding without filter")

        entry = VaultEntry(
            entry_id=self._generate_entry_id(),
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            verdict_type=verdict_type,
            risk_level=risk_level,
            category=category,
            environment=environment,
            payload=payload,
            query_summary=query_summary,
            prev_hash=self._last_hash,
            entry_hash="",  # Computed below
            floors_checked=floors_checked or [],
            floors_failed=floors_failed or [],
            eureka_score=eureka_score,
            eureka_verdict=eureka_verdict,
        )

        entry.entry_hash = self._compute_hash(entry)

        # UNIFIED: Compute Merkle root
        self._merkle_history.append(entry.entry_hash)
        entry.merkle_root = merkle_root(self._merkle_history)
        self._last_hash = entry.entry_hash

        # UNIFIED: Persist to Redis (hot cache)
        try:
            self._redis.save(
                f"vault:{entry.entry_id}",
                {
                    "entry_id": entry.entry_id,
                    "session_id": entry.session_id,
                    "verdict": entry.verdict_type,
                    "hash": entry.entry_hash,
                    "merkle_root": entry.merkle_root,
                    "timestamp": entry.timestamp,
                },
                ttl=86400 * 7,  # 7 days
            )
            # Update chain state in Redis
            self._redis.save(
                "vault999_chain",
                {
                    "last_hash": self._last_hash,
                    "history_length": len(self._merkle_history),
                    "merkle_root": entry.merkle_root,
                },
            )
        except Exception as e:
            print(f"[VAULT999] Redis cache warning: {e}")

        # UNIFIED: Persist to Postgres (authoritative)
        if self._pool:
            try:
                async with self._pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO vault999 (
                            entry_id, session_id, timestamp, verdict_type, risk_level,
                            category, environment, payload, query_summary,
                            prev_hash, entry_hash, merkle_root, eureka_score, eureka_verdict,
                            schema_version, floors_checked, floors_failed
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
                        """,
                        entry.entry_id,
                        entry.session_id,
                        datetime.fromisoformat(entry.timestamp),
                        entry.verdict_type,
                        entry.risk_level,
                        entry.category,
                        entry.environment,
                        json.dumps(entry.payload),
                        entry.query_summary,
                        entry.prev_hash,
                        entry.entry_hash,
                        entry.merkle_root,
                        entry.eureka_score,
                        entry.eureka_verdict,
                        entry.schema_version,
                        entry.floors_checked,
                        entry.floors_failed,
                    )
            except Exception as e:
                print(f"[SessionLedger] Postgres write failed: {e}")
                self._memory_ledger.append(entry)
        else:
            self._memory_ledger.append(entry)

        return entry

    async def query(
        self,
        session_id: str | None = None,
        verdict_type: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[VaultEntry]:
        """Query the VAULT999 ledger."""
        await self.initialize()

        if self._pool:
            try:
                async with self._pool.acquire() as conn:
                    conditions = []
                    params = []
                    param_idx = 1

                    if session_id:
                        conditions.append(f"session_id = ${param_idx}")
                        params.append(session_id)
                        param_idx += 1

                    if verdict_type:
                        conditions.append(f"verdict_type = ${param_idx}")
                        params.append(verdict_type)
                        param_idx += 1

                    where_clause = " AND ".join(conditions) if conditions else "TRUE"

                    rows = await conn.fetch(
                        f"""
                        SELECT * FROM vault999 
                        WHERE {where_clause}
                        ORDER BY timestamp DESC
                        LIMIT ${param_idx} OFFSET ${param_idx + 1}
                        """,
                        *params,
                        limit,
                        offset,
                    )

                    return [
                        VaultEntry(
                            entry_id=row["entry_id"],
                            session_id=row["session_id"],
                            timestamp=row["timestamp"].isoformat() if row["timestamp"] else "",
                            verdict_type=row["verdict_type"],
                            risk_level=row["risk_level"],
                            category=row["category"] or "",
                            environment=row["environment"] or "",
                            payload=json.loads(row["payload"]) if row["payload"] else {},
                            query_summary=row["query_summary"] or "",
                            prev_hash=row["prev_hash"] or "",
                            entry_hash=row["entry_hash"],
                            schema_version=row["schema_version"] or "3.0",
                            floors_checked=list(row["floors_checked"] or []),
                            floors_failed=list(row["floors_failed"] or []),
                            # UNIFIED: New fields
                            merkle_root=row.get("merkle_root", ""),
                            eureka_score=row.get("eureka_score", 0.0),
                            eureka_verdict=row.get("eureka_verdict", "TRANSIENT"),
                        )
                        for row in rows
                    ]
            except Exception as e:
                print(f"[SessionLedger] Postgres query failed: {e}")

        # Memory fallback query
        entries = self._memory_ledger
        if session_id:
            entries = [e for e in entries if e.session_id == session_id]
        if verdict_type:
            entries = [e for e in entries if e.verdict_type == verdict_type]
        return entries[offset : offset + limit]

    async def verify_chain(self, limit: int = 100) -> dict[str, Any]:
        """
        UNIFIED: Verify Merkle chain integrity.

        Returns verification report with tamper detection.
        """
        await self.initialize()

        entries = await self.query(limit=limit)
        if not entries:
            return {"valid": True, "entries_checked": 0, "tampered": []}

        tampered = []
        for i, entry in enumerate(entries):
            # Verify entry hash
            computed_hash = self._compute_hash(entry)
            if computed_hash != entry.entry_hash:
                tampered.append({"entry_id": entry.entry_id, "field": "entry_hash"})
                continue

            # Verify chain continuity
            if i > 0:
                if entry.prev_hash != entries[i - 1].entry_hash:
                    tampered.append({"entry_id": entry.entry_id, "field": "chain_break"})

        # Verify Merkle root
        hashes = [e.entry_hash for e in entries]
        computed_root = merkle_root(hashes)
        latest_root = entries[-1].merkle_root if entries else ""

        return {
            "valid": len(tampered) == 0 and computed_root == latest_root,
            "entries_checked": len(entries),
            "tampered": tampered,
            "merkle_root": computed_root[:16] + "...",
            "latest_stored_root": latest_root[:16] + "..." if latest_root else "N/A",
        }

    async def close(self):
        """Close the database connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None


# Global ledger instance
_ledger: SessionLedger | None = None


async def get_ledger() -> SessionLedger:
    """Get or create the global SessionLedger instance."""
    global _ledger
    if _ledger is None:
        _ledger = SessionLedger()
        await _ledger.initialize()
    return _ledger


async def seal_memory(
    session_id: str, verdict: str, payload: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """
    Legacy compatibility function for APEX engine.
    Uses the new SessionLedger under the hood.
    """
    ledger = await get_ledger()
    entry = await ledger.seal(
        session_id=session_id, verdict_type=verdict, payload=payload, **kwargs
    )
    return {
        "verdict": entry.verdict_type,
        "seal_id": entry.entry_id,
        "entry_hash": entry.entry_hash,
    }


async def log_asi_decision(
    session_id: str,
    stage: str,
    query: str,
    asi_output: dict[str, Any],
    verdict: str = "SEAL",
    floors_checked: list[str] | None = None,
    floors_failed: list[str] | None = None,
) -> dict[str, Any]:
    """
    Log an ASI decision to VAULT for future fine-tuning (Ω Incident Logging).

    Args:
        session_id: Constitutional session token
        stage: "555" (empathy) or "666" (align)
        query: Original user query (will be anonymized)
        asi_output: ASI organ output (must include floor scores, stakeholder impact, metrics)
        verdict: Verdict from ASI stage (SEAL, SABAR, VOID)
        floors_checked: List of floors checked (optional)
        floors_failed: List of floors failed (optional)

    Returns:
        dict with seal_id and entry_hash
    """
    ledger = await get_ledger()

    # Anonymize query: store only hash and length
    query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
    query_len = len(query)

    # Prepare payload with ASI decision data
    payload = {
        "stage": stage,
        "query_hash": query_hash,
        "query_length": query_len,
        "asi_output": asi_output,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Determine risk level based on verdict and floor failures
    risk_level = "LOW"
    if verdict == "VOID":
        risk_level = "HIGH"
    elif verdict == "SABAR":
        risk_level = "MEDIUM"

    # Determine category
    category = "asi_decision"
    if stage == "555":
        category = "asi_empathy"
    elif stage == "666":
        category = "asi_align"

    checked = floors_checked or []
    failed = floors_failed or []
    entry = await ledger.seal(
        session_id=session_id,
        verdict_type=verdict,
        payload=payload,
        query_summary=f"{stage} ASI decision - query hash {query_hash}",
        risk_level=risk_level,
        category=category,
        environment="prod",
        floors_checked=checked,
        floors_failed=failed,
    )

    return {
        "verdict": entry.verdict_type,
        "seal_id": entry.entry_id,
        "entry_hash": entry.entry_hash,
    }


async def inject_memory(session_id: str, context: dict[str, Any]) -> bool:
    """
    Legacy compatibility function for memory injection.
    In VAULT999 v3, context is stored as part of the ledger entry payload.
    """
    # In the new architecture, memory injection is handled during seal
    # This function returns True for API compatibility
    return True
