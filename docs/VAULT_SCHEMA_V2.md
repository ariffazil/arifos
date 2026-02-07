# VAULT999 Enhanced Schema v2

**Version:** 2.0  
**Status:** DEPLOYED  
**Purpose:** Structured audit fields for constitutional AI governance

---

## Overview

VAULT999 is the immutable, hash-chained ledger that records all constitutional decisions made by arifOS agents. Schema v2 adds structured fields for better auditability, pattern detection, and institutional memory.

---

## Schema Fields

### Core Identity (v1 — unchanged)

| Field | Type | Description |
|-------|------|-------------|
| `sequence` | SERIAL | Auto-increment primary key |
| `seal_id` | UUID | Unique entry identifier |
| `session_id` | TEXT | Logical session/conversation ID |
| `timestamp` | TIMESTAMPTZ | When decision was made (UTC) |
| `entry_hash` | TEXT | SHA-256 of entry content |
| `prev_hash` | TEXT | Hash of previous entry (chain link) |
| `merkle_root` | TEXT | Current Merkle tree root |

### Verdict (v1 — unchanged)

| Field | Type | Description |
|-------|------|-------------|
| `verdict` | TEXT | SEAL / VOID / PARTIAL / SABAR |
| `authority` | TEXT | Who sealed (mcp_server, system, user) |
| `seal_data` | JSONB | Full payload (contains v2 metadata) |

### NEW: Decision Context (v2)

| Field | Type | Description |
|-------|------|-------------|
| `query_summary` | TEXT | First ~200 chars of input (redacted) |
| `query_hash` | TEXT | SHA-256 of full input |
| `response_hash` | TEXT | SHA-256 of output |
| `intent` | TEXT | What was the user trying to do? |

### NEW: Risk & Classification (v2)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `risk_level` | TEXT | low, medium, high, critical | Triage level |
| `risk_tags` | TEXT[] | safety, financial, privacy, reputation | Risk categories |
| `category` | TEXT | finance, safety, content, code, governance | Domain category |
| `sensitivity_level` | TEXT | none, low, medium, high | PII/data sensitivity |

### NEW: Constitutional Enforcement (v2)

| Field | Type | Description |
|-------|------|-------------|
| `floors_passed` | TEXT[] | Floors that passed (F1, F2, etc.) |
| `floors_failed` | TEXT[] | Floors that failed |

### NEW: Metrics (v2)

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `entropy_omega` | FLOAT | 0.0–1.0 | Ω₀ uncertainty at decision |
| `tri_witness_score` | FLOAT | 0.0–1.0 | TW consensus metric |
| `peace_squared` | FLOAT | 0.0–1.0 | Peace² stability metric |
| `genius_g` | FLOAT | 0.0–1.0 | Genius G score |
| `confidence` | FLOAT | 0.0–1.0 | Decision confidence |
| `latency_ms` | INT | ≥0 | Governance check duration |

### NEW: Human Oversight (v2)

| Field | Type | Description |
|-------|------|-------------|
| `human_override` | BOOLEAN | Was 888 Judge override invoked? |
| `override_reason` | TEXT | Why override was granted |
| `override_by` | TEXT | Who overrode (e.g., arif-fazil) |

### NEW: Model Provenance (v2)

| Field | Type | Description |
|-------|------|-------------|
| `model_used` | TEXT | Which LLM made the decision |

### NEW: Searchability (v2)

| Field | Type | Description |
|-------|------|-------------|
| `tags` | TEXT[] | Arbitrary searchable tags |

---

## Query Examples

### Basic Queries

```bash
# Get last 10 entries
vault_query limit=10

# Filter by verdict
vault_query verdict=VOID limit=5

# Filter by session pattern
vault_query session_pattern="prod_*"

# Filter by date range
vault_query date_from=2026-02-01 date_to=2026-02-07
```

### v2 Enhanced Queries

```bash
# High-risk decisions only
vault_query risk_level=critical

# Decisions where 888 Judge overrode
vault_query human_override_only=true

# Filter by category
vault_query category=finance

# Filter by tag
vault_query tag=petronas
```

---

## Example Entry (v2)

```json
{
  "sequence": 42,
  "seal_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "telegram_arif_20260207",
  "timestamp": "2026-02-07T07:00:00Z",
  
  "verdict": "PARTIAL",
  "authority": "mcp_server",
  
  "query_summary": "Should I publish the PyPI package now?",
  "risk_level": "high",
  "category": "code",
  "intent": "publish",
  
  "floors_passed": ["F2", "F7", "F9"],
  "floors_failed": ["F1"],
  
  "entropy_omega": 0.06,
  "tri_witness_score": 0.79,
  "peace_squared": 1.0,
  "genius_g": 0.85,
  
  "human_override": false,
  "model_used": "claude-opus-4-5",
  
  "tags": ["arifos", "pypi", "deployment"],
  
  "entry_hash": "a1b2c3d4e5f6...",
  "prev_hash": "0987654321ab...",
  "merkle_root": "deadbeef1234..."
}
```

---

## Pattern Detection

vault_query automatically detects patterns:

```json
{
  "patterns": {
    "void_rate": 0.4,
    "total_queried": 10,
    "verdict_distribution": {"SEAL": 6, "VOID": 4},
    "risk_distribution": {"low": 5, "high": 3, "critical": 2},
    "avg_entropy_omega": 0.045
  }
}
```

---

## Migration

Run the migration to add v2 columns:

```sql
-- From: codebase/vault/migrations/002_enhanced_schema.sql
\i codebase/vault/migrations/002_enhanced_schema.sql
```

---

## Backwards Compatibility

- v1 entries continue to work (v2 fields are nullable)
- vault_query returns v2 metadata only when present
- vault_seal accepts all v2 fields as optional parameters

---

## Why These Fields?

Based on AI governance best practices:

| Field | Source | Purpose |
|-------|--------|---------|
| query_hash | ISACA, PWC | Integrity without storing full content |
| risk_level | PWC, Liminal | Triage and escalation |
| floors_failed | arifOS Constitution | Learn from violations |
| human_override | Databricks, Alation | Track sovereignty events |
| entropy_omega | APEX Theory | Uncertainty patterns |
| tags | Google ADR | Flexible categorization |

---

*DITEMPA BUKAN DIBERI* 🔥
