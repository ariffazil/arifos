-- Vault999 PostgreSQL schema

CREATE TABLE IF NOT EXISTS vault_ledger (
    sequence      BIGSERIAL PRIMARY KEY,
    session_id    TEXT NOT NULL,
    seal_id       UUID NOT NULL,
    timestamp     TIMESTAMPTZ NOT NULL,
    authority     TEXT NOT NULL,
    verdict       TEXT NOT NULL,
    seal_data     JSONB NOT NULL,
    entry_hash    TEXT NOT NULL UNIQUE,
    prev_hash     TEXT,
    merkle_root   TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS vault_head (
    id               SMALLINT PRIMARY KEY DEFAULT 1,
    head_sequence    BIGINT NOT NULL,
    head_entry_hash  TEXT NOT NULL,
    head_merkle_root TEXT NOT NULL,
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_vault_ledger_session ON vault_ledger (session_id);
CREATE INDEX IF NOT EXISTS idx_vault_ledger_verdict_time ON vault_ledger (verdict, timestamp);
CREATE INDEX IF NOT EXISTS idx_vault_ledger_time ON vault_ledger (timestamp);

-- Initialize head row if absent
INSERT INTO vault_head (id, head_sequence, head_entry_hash, head_merkle_root)
    SELECT 1, 0, repeat('0',64), repeat('0',64)
    WHERE NOT EXISTS (SELECT 1 FROM vault_head WHERE id = 1);
