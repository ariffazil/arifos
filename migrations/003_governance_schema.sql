-- Governance Floors: Track the status and thresholds for constitutional guardrails
CREATE TABLE IF NOT EXISTS governance_floors (
    floor_id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'degraded', 'violated')),
    seal_threshold FLOAT DEFAULT 0.8,
    instructions TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Cooling Queue: Manage tasks awaiting human approval (888_HOLD)
CREATE TABLE IF NOT EXISTS cooling_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_type TEXT NOT NULL,
    risk_class TEXT NOT NULL,
    judge_verdict TEXT NOT NULL,
    proposal_hash TEXT NOT NULL,
    session_id TEXT NOT NULL,
    status TEXT DEFAULT 'awaiting_human' CHECK (status IN ('awaiting_human', 'approved', 'rejected', 'expired')),
    payload JSONB,
    hold_initiated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Initial Floors
INSERT INTO governance_floors (floor_id, status, seal_threshold) VALUES
('F1_AMANAH', 'active', 0.9),
('F2_TRUTH', 'active', 0.9),
('F7_MIND', 'active', 0.8),
('F13_SOVEREIGN', 'active', 1.0)
ON CONFLICT (floor_id) DO NOTHING;
