"""
SessionLedger — VAULT999 Postgres Persistence Layer

Provides Merkle-chained audit trail for constitutional verdicts.
Schema: VAULT999 v3 (hybrid)

DITEMPA BUKAN DIBERI
"""

import os
import json
import hashlib
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

# Try to import asyncpg for Postgres support
try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False


@dataclass
class VaultEntry:
    """VAULT999 v3 entry schema."""
    entry_id: str
    session_id: str
    timestamp: str
    verdict_type: str  # SEAL | VOID | PARTIAL | SABAR | 888_HOLD
    risk_level: str  # LOW | MEDIUM | HIGH | CRITICAL
    category: str
    environment: str
    payload: Dict[str, Any]
    query_summary: str
    prev_hash: str
    entry_hash: str
    schema_version: str = "3.0"
    floors_checked: List[str] = None
    floors_failed: List[str] = None
    
    def __post_init__(self):
        if self.floors_checked is None:
            self.floors_checked = []
        if self.floors_failed is None:
            self.floors_failed = []


class SessionLedger:
    """
    VAULT999 Ledger — Immutable Merkle-chained audit trail.
    
    Supports:
    - Postgres backend (production)
    - In-memory fallback (development/testing)
    """
    
    # SQL for creating the vault table
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
        schema_version VARCHAR(10) DEFAULT '3.0',
        floors_checked TEXT[],
        floors_failed TEXT[],
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_vault999_session ON vault999(session_id);
    CREATE INDEX IF NOT EXISTS idx_vault999_verdict ON vault999(verdict_type);
    CREATE INDEX IF NOT EXISTS idx_vault999_timestamp ON vault999(timestamp DESC);
    """
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.environ.get("DATABASE_URL")
        self._pool: Optional[asyncpg.Pool] = None
        self._memory_ledger: List[VaultEntry] = []
        self._last_hash = "GENESIS"
        self._initialized = False
    
    @property
    def is_postgres_available(self) -> bool:
        """Check if Postgres is configured and available."""
        return ASYNCPG_AVAILABLE and bool(self.database_url)
    
    async def initialize(self) -> bool:
        """Initialize the ledger (create table if needed)."""
        if self._initialized:
            return True
        
        if not self.is_postgres_available:
            self._initialized = True
            return False  # Using memory fallback
        
        try:
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=5,
                command_timeout=30
            )
            async with self._pool.acquire() as conn:
                await conn.execute(self.CREATE_TABLE_SQL)
                # Get last hash for chain continuity
                row = await conn.fetchrow(
                    "SELECT entry_hash FROM vault999 ORDER BY id DESC LIMIT 1"
                )
                if row:
                    self._last_hash = row["entry_hash"]
            self._initialized = True
            return True
        except Exception as e:
            print(f"[SessionLedger] Postgres init failed: {e}, using memory fallback")
            self._initialized = True
            return False
    
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
        payload: Dict[str, Any],
        query_summary: str = "",
        risk_level: str = "LOW",
        category: str = "general",
        environment: str = "prod",
        floors_checked: Optional[List[str]] = None,
        floors_failed: Optional[List[str]] = None,
    ) -> VaultEntry:
        """
        Seal a new entry into the VAULT999 ledger.
        
        Returns the sealed VaultEntry with computed hash.
        """
        await self.initialize()
        
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
        )
        
        entry.entry_hash = self._compute_hash(entry)
        self._last_hash = entry.entry_hash
        
        # Persist to Postgres or memory
        if self._pool:
            try:
                async with self._pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO vault999 (
                            entry_id, session_id, timestamp, verdict_type, risk_level,
                            category, environment, payload, query_summary,
                            prev_hash, entry_hash, schema_version, floors_checked, floors_failed
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                        """,
                        entry.entry_id, entry.session_id, datetime.fromisoformat(entry.timestamp),
                        entry.verdict_type, entry.risk_level, entry.category, entry.environment,
                        json.dumps(entry.payload), entry.query_summary,
                        entry.prev_hash, entry.entry_hash, entry.schema_version,
                        entry.floors_checked, entry.floors_failed
                    )
            except Exception as e:
                print(f"[SessionLedger] Postgres write failed: {e}")
                self._memory_ledger.append(entry)
        else:
            self._memory_ledger.append(entry)
        
        return entry
    
    async def query(
        self,
        session_id: Optional[str] = None,
        verdict_type: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[VaultEntry]:
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
                        *params, limit, offset
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
        return entries[offset:offset + limit]
    
    async def close(self):
        """Close the database connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None


# Global ledger instance
_ledger: Optional[SessionLedger] = None


async def get_ledger() -> SessionLedger:
    """Get or create the global SessionLedger instance."""
    global _ledger
    if _ledger is None:
        _ledger = SessionLedger()
        await _ledger.initialize()
    return _ledger


async def seal_memory(
    session_id: str,
    verdict: str,
    payload: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    """
    Legacy compatibility function for APEX engine.
    Uses the new SessionLedger under the hood.
    """
    ledger = await get_ledger()
    entry = await ledger.seal(
        session_id=session_id,
        verdict_type=verdict,
        payload=payload,
        **kwargs
    )
    return {
        "verdict": entry.verdict_type,
        "seal_id": entry.entry_id,
        "entry_hash": entry.entry_hash
    }
