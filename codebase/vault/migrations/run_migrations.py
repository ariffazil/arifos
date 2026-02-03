"""
VAULT999 Migration Runner
Ensures vault tables exist before operations.
"""

import asyncio
import os

try:
    import asyncpg
except ImportError:
    asyncpg = None


async def ensure_vault_tables():
    """Ensure vault_ledger and vault_head tables exist."""
    if asyncpg is None:
        return
    
    dsn = (
        os.environ.get("VAULT_POSTGRES_DSN")
        or os.environ.get("DATABASE_URL")
    )
    
    if not dsn:
        return  # Will fail later with proper error
    
    # Railway TCP proxy requires SSL
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    conn = await asyncpg.connect(dsn, ssl=ssl_context)
    try:
        # Create vault_ledger table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS vault_ledger (
                sequence BIGSERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                seal_id UUID NOT NULL,
                timestamp TIMESTAMPTZ NOT NULL,
                authority TEXT NOT NULL,
                verdict TEXT NOT NULL,
                seal_data JSONB NOT NULL,
                entry_hash TEXT NOT NULL UNIQUE,
                prev_hash TEXT,
                merkle_root TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        
        # Create indexes
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_vault_session 
            ON vault_ledger(session_id)
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_vault_timestamp 
            ON vault_ledger(timestamp)
        """)
        
        # Create vault_head table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS vault_head (
                id SMALLINT PRIMARY KEY DEFAULT 1,
                head_sequence BIGINT NOT NULL DEFAULT 0,
                head_entry_hash TEXT NOT NULL DEFAULT '',
                head_merkle_root TEXT NOT NULL DEFAULT '',
                updated_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        
        # Create vault_merkle_state table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS vault_merkle_state (
                id SMALLINT PRIMARY KEY DEFAULT 1,
                merkle_state JSONB,
                updated_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(ensure_vault_tables())
    print("Vault tables ensured.")
