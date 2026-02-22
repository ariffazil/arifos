-- VAULT999 Schema v2 Migration
-- Adds structured fields for better auditability
-- Based on AI governance best practices + external audit feedback

-- Add new columns to existing table
ALTER TABLE vault_ledger 
ADD COLUMN IF NOT EXISTS query_summary TEXT,
ADD COLUMN IF NOT EXISTS query_hash TEXT,
ADD COLUMN IF NOT EXISTS response_hash TEXT,
ADD COLUMN IF NOT EXISTS risk_level TEXT DEFAULT 'low',
ADD COLUMN IF NOT EXISTS risk_tags TEXT[],
ADD COLUMN IF NOT EXISTS intent TEXT,
ADD COLUMN IF NOT EXISTS category TEXT,
ADD COLUMN IF NOT EXISTS floors_checked TEXT[],
ADD COLUMN IF NOT EXISTS floors_passed TEXT[],
ADD COLUMN IF NOT EXISTS floors_failed TEXT[],
ADD COLUMN IF NOT EXISTS entropy_omega FLOAT,
ADD COLUMN IF NOT EXISTS tri_witness_score FLOAT,
ADD COLUMN IF NOT EXISTS peace_squared FLOAT,
ADD COLUMN IF NOT EXISTS genius_g FLOAT,
ADD COLUMN IF NOT EXISTS confidence FLOAT,
ADD COLUMN IF NOT EXISTS latency_ms INT,
ADD COLUMN IF NOT EXISTS human_override BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS override_reason TEXT,
ADD COLUMN IF NOT EXISTS override_by TEXT,
ADD COLUMN IF NOT EXISTS model_used TEXT,
ADD COLUMN IF NOT EXISTS sensitivity_level TEXT DEFAULT 'none',
ADD COLUMN IF NOT EXISTS tags TEXT[],
-- v2.1 additions (external audit feedback)
ADD COLUMN IF NOT EXISTS tool_chain TEXT[],
ADD COLUMN IF NOT EXISTS model_info JSONB,
ADD COLUMN IF NOT EXISTS override_info JSONB,
ADD COLUMN IF NOT EXISTS environment TEXT DEFAULT 'prod',
ADD COLUMN IF NOT EXISTS prompt_excerpt TEXT,
ADD COLUMN IF NOT EXISTS response_excerpt TEXT,
ADD COLUMN IF NOT EXISTS pii_level TEXT DEFAULT 'none',
ADD COLUMN IF NOT EXISTS actor_type TEXT,
ADD COLUMN IF NOT EXISTS actor_id TEXT;

-- Create indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_vault_verdict ON vault_ledger(verdict);
CREATE INDEX IF NOT EXISTS idx_vault_risk_level ON vault_ledger(risk_level);
CREATE INDEX IF NOT EXISTS idx_vault_timestamp ON vault_ledger(timestamp);
CREATE INDEX IF NOT EXISTS idx_vault_human_override ON vault_ledger(human_override) WHERE human_override = true;
CREATE INDEX IF NOT EXISTS idx_vault_tags ON vault_ledger USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_vault_risk_tags ON vault_ledger USING GIN(risk_tags);
CREATE INDEX IF NOT EXISTS idx_vault_floors_failed ON vault_ledger USING GIN(floors_failed);
CREATE INDEX IF NOT EXISTS idx_vault_category ON vault_ledger(category);
CREATE INDEX IF NOT EXISTS idx_vault_model ON vault_ledger(model_used);
-- v2.1 indexes
CREATE INDEX IF NOT EXISTS idx_vault_environment ON vault_ledger(environment);
CREATE INDEX IF NOT EXISTS idx_vault_tool_chain ON vault_ledger USING GIN(tool_chain);
CREATE INDEX IF NOT EXISTS idx_vault_actor ON vault_ledger(actor_type, actor_id);
CREATE INDEX IF NOT EXISTS idx_vault_pii ON vault_ledger(pii_level);

-- Add comment documenting the schema version
COMMENT ON TABLE vault_ledger IS 'VAULT999 Constitutional Ledger v2.1 - Enhanced schema with structured audit fields (external audit feedback incorporated)';
