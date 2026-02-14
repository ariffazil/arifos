-- VAULT999 PostgreSQL Schema Initialization
-- Run automatically by docker-compose on postgres container startup
-- Compatible with Railway PostgreSQL plugin

-- Main ledger table: Immutable Merkle-chained audit trail
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
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_vault_session ON vault_ledger(session_id);
CREATE INDEX IF NOT EXISTS idx_vault_timestamp ON vault_ledger(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_vault_verdict ON vault_ledger(verdict);

-- Chain head tracking: For quick Merkle root verification
CREATE TABLE IF NOT EXISTS vault_head (
    id SMALLINT PRIMARY KEY DEFAULT 1,
    head_sequence BIGINT NOT NULL DEFAULT 0,
    head_entry_hash TEXT NOT NULL DEFAULT 'GENESIS',
    head_merkle_root TEXT NOT NULL DEFAULT 'GENESIS',
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Initialize head record
INSERT INTO vault_head (id, head_sequence, head_entry_hash, head_merkle_root)
VALUES (1, 0, 'GENESIS', 'GENESIS')
ON CONFLICT (id) DO NOTHING;

-- Optional: Session metadata table for extended tracking
CREATE TABLE IF NOT EXISTS vault_sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT now(),
    last_activity TIMESTAMPTZ DEFAULT now(),
    environment TEXT DEFAULT 'unknown',
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_sessions_created ON vault_sessions(created_at DESC);

-- Grant permissions (for Railway compatibility)
-- Note: Railway uses superuser, but this ensures compatibility with restricted users
GRANT ALL PRIVILEGES ON TABLE vault_ledger TO CURRENT_USER;
GRANT ALL PRIVILEGES ON TABLE vault_head TO CURRENT_USER;
GRANT ALL PRIVILEGES ON TABLE vault_sessions TO CURRENT_USER;
GRANT ALL PRIVILEGES ON SEQUENCE vault_ledger_sequence_seq TO CURRENT_USER;

-- Verify setup
DO $$
BEGIN
    RAISE NOTICE 'VAULT999 schema initialized successfully';
    RAISE NOTICE 'Tables created: vault_ledger, vault_head, vault_sessions';
END $$;
