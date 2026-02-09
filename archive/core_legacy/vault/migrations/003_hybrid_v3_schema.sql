-- VAULT999 Schema v3 Migration (Hybrid)
-- 22 columns → 14 columns (4 indexed + 9 JSONB + 1 backup)
-- Based on APEX theory compression + entropy optimization

-- Option 1: Create new table (recommended for clean migration)
CREATE TABLE IF NOT EXISTS vault_ledger_v3 (
  -- Core (keep as columns for indexing)
  seal_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp       TIMESTAMPTZ DEFAULT NOW(),
  
  -- Fast-query columns (indexed) — the 4 governance axes
  session_id      TEXT NOT NULL,
  verdict_type    TEXT NOT NULL,      -- SEAL/VOID/PARTIAL/SABAR
  risk_level      TEXT DEFAULT 'low', -- low/medium/high/critical
  environment     TEXT DEFAULT 'prod', -- test/staging/prod
  
  -- 9 JSONB Categories (APEX-aligned)
  identity        JSONB,  -- {session, actor_type, actor_id}
  chain           JSONB,  -- {seq, entry_hash, prev_hash, merkle}
  verdict         JSONB,  -- {type, authority}
  context         JSONB,  -- {summary, q_hash, r_hash, intent}
  risk            JSONB,  -- {level, tags[], category, pii}
  floors          JSONB,  -- {checked[], failed[]}
  metrics         JSONB,  -- {omega, tw, conf, latency}
  oversight       JSONB,  -- {override, reason, by}
  provenance      JSONB,  -- {model, model_info, tools[], env}
  
  -- Backup (full raw payload)
  seal_data       JSONB
);

-- Indexes for fast governance queries
CREATE INDEX IF NOT EXISTS idx_v3_session ON vault_ledger_v3(session_id);
CREATE INDEX IF NOT EXISTS idx_v3_verdict ON vault_ledger_v3(verdict_type);
CREATE INDEX IF NOT EXISTS idx_v3_risk ON vault_ledger_v3(risk_level);
CREATE INDEX IF NOT EXISTS idx_v3_environment ON vault_ledger_v3(environment);
CREATE INDEX IF NOT EXISTS idx_v3_timestamp ON vault_ledger_v3(timestamp);

-- GIN indexes for JSONB array queries
CREATE INDEX IF NOT EXISTS idx_v3_floors_failed ON vault_ledger_v3 USING GIN ((floors->'failed'));
CREATE INDEX IF NOT EXISTS idx_v3_risk_tags ON vault_ledger_v3 USING GIN ((risk->'tags'));
CREATE INDEX IF NOT EXISTS idx_v3_provenance_tools ON vault_ledger_v3 USING GIN ((provenance->'tools'));

-- JSONB path indexes for common queries
CREATE INDEX IF NOT EXISTS idx_v3_identity_actor ON vault_ledger_v3 ((identity->>'actor_id'));
CREATE INDEX IF NOT EXISTS idx_v3_oversight_override ON vault_ledger_v3 ((oversight->>'override'));
CREATE INDEX IF NOT EXISTS idx_v3_chain_hash ON vault_ledger_v3 ((chain->>'entry_hash'));

-- Comment documenting schema version
COMMENT ON TABLE vault_ledger_v3 IS 'VAULT999 Constitutional Ledger v3 (Hybrid) - APEX-aligned 9-category compression';

-- Migration from v2.1: Copy existing data
-- INSERT INTO vault_ledger_v3 (seal_id, timestamp, session_id, verdict_type, risk_level, environment, ...)
-- SELECT ... FROM vault_ledger;
-- (Run manually after verifying v3 schema)
