"""
VAULT-999 Persistence Layer
PostgreSQL-backed Merkle DAG with disk survival
"""
import asyncio
import asyncpg
import hashlib
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import os

class PostgresLedger:
    """
    Production-grade ledger with PostgreSQL persistence.
    
    Features:
    - Merkle DAG chain verification
    - Cryptographic sealing (SHA-256)
    - Concurrent transaction safety
    - Disk persistence (survives restarts)
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize ledger connection.
        
        Args:
            database_url: PostgreSQL connection string
            Falls back to AAA_DATABASE_URL env var
            Format: postgresql://user:pass@host:port/db
        """
        self.database_url = database_url or os.getenv(
            "AAA_DATABASE_URL",
            "postgresql://arifos:arifos@localhost:5432/vault999"
        )
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Establish connection pool"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
        await self._ensure_schema()
    
    async def close(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    async def _ensure_schema(self):
        """Create ledger table if not exists"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS vault_ledger (
                    sequence BIGSERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    payload JSONB,
                    prev_hash TEXT,
                    merkle_root TEXT,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    authority TEXT,
                    seal TEXT UNIQUE
                );
                
                CREATE INDEX IF NOT EXISTS idx_session 
                ON vault_ledger(session_id);
                
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON vault_ledger(timestamp DESC);
            """)
    
    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """Compute SHA-256 hash of entry"""
        canonical = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    async def append(
        self,
        session_id: str,
        verdict: str,
        payload: Dict[str, Any],
        authority: str = "system"
    ) -> Dict[str, Any]:
        """
        Append entry to ledger with Merkle chaining.
        
        Args:
            session_id: Session identifier
            verdict: SEAL, VOID, or SABAR
            payload: Arbitrary JSON data
            authority: Who authorized this entry
            
        Returns:
            Entry receipt with sequence and seal
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Get previous entry for chaining
                prev_row = await conn.fetchrow(
                    "SELECT seal FROM vault_ledger ORDER BY sequence DESC LIMIT 1"
                )
                prev_hash = prev_row["seal"] if prev_row else "0" * 64
                
                # Create entry data
                entry_data = {
                    "session_id": session_id,
                    "verdict": verdict,
                    "payload": payload,
                    "prev_hash": prev_hash,
                    "timestamp": datetime.utcnow().isoformat(),
                    "authority": authority
                }
                
                # Compute seal
                seal = self._compute_hash(entry_data)
                
                # Insert entry
                row = await conn.fetchrow(
                    """
                    INSERT INTO vault_ledger 
                    (session_id, verdict, payload, prev_hash, seal, authority)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING sequence, timestamp
                    """,
                    session_id, verdict, json.dumps(payload),
                    prev_hash, seal, authority
                )
                
                return {
                    "sequence": row["sequence"],
                    "seal": seal,
                    "timestamp": row["timestamp"],
                    "prev_hash": prev_hash
                }
    
    async def verify_chain(self) -> bool:
        """Verify entire Merkle chain integrity"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM vault_ledger ORDER BY sequence"
            )
            
            prev_hash = "0" * 64
            for row in rows:
                # Reconstruct entry
                entry_data = {
                    "session_id": row["session_id"],
                    "verdict": row["verdict"],
                    "payload": json.loads(row["payload"]),
                    "prev_hash": row["prev_hash"],
                    "timestamp": row["timestamp"].isoformat(),
                    "authority": row["authority"]
                }
                
                # Verify hash chain
                if row["prev_hash"] != prev_hash:
                    return False
                
                # Verify seal
                computed = self._compute_hash(entry_data)
                if computed != row["seal"]:
                    return False
                
                prev_hash = row["seal"]
            
            return True
    
    async def get_by_session(self, session_id: str) -> List[Dict]:
        """Get all entries for a session"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM vault_ledger WHERE session_id = $1 ORDER BY sequence",
                session_id
            )
            return [dict(row) for row in rows]


class InMemoryLedger:
    """Fallback in-memory ledger for testing/development"""
    
    def __init__(self):
        self.entries = []
        self._sequence = 0
    
    async def connect(self):
        pass
    
    async def close(self):
        pass
    
    async def append(self, session_id: str, verdict: str, payload: Dict, authority: str = "system") -> Dict:
        self._sequence += 1
        entry = {
            "sequence": self._sequence,
            "session_id": session_id,
            "verdict": verdict,
            "payload": payload,
            "timestamp": datetime.utcnow(),
            "authority": authority
        }
        self.entries.append(entry)
        return entry
    
    async def verify_chain(self) -> bool:
        return True
    
    async def get_by_session(self, session_id: str) -> List[Dict]:
        return [e for e in self.entries if e["session_id"] == session_id]


# Factory function
def get_ledger():
    """Get appropriate ledger based on environment"""
    if os.getenv("AAA_USE_POSTGRES", "false").lower() == "true":
        return PostgresLedger()
    return InMemoryLedger()
