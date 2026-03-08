# EUREKA Sieve Specification
## Theory of Anomalous Contrast for VAULT999

**Version:** v55.3  
**Status:** HARDENED  
**Authority:** Muhammad Arif bin Fazil  
**Doctrine:** 888_SOUL_VERDICT.md

---

## I. THE PROBLEM: Tong Sampah Paradox

> If VAULT999 SEALs everything → **Tong sampah** (trash bin)
> - No curation, only hoarding
> - Entropy increases
> - Memory becomes noise

**Current State:** The database has test data like `{"k": 0, "nested": {"deep": true}}` — meaningless placeholders.

**Solution:** EUREKA Sieve — only meaningful insights enter the vault.

---

## II. THEORY OF ANOMALOUS CONTRAST

From `888_SOUL_VERDICT.md`:

```
VOID must be EXPENSIVE (high energy, high consensus)
SEAL must be EARNED (low entropy, high clarity)
SABAR is the DEFAULT (patience, retry, refine)
```

### The Four Velocities of Meaning

| Velocity | Measure | Question |
|----------|---------|----------|
| **Novelty** | 0-1 | Is this different from history? |
| **Entropy Reduction** | 0-1 | Did we reduce confusion? (ΔS ≤ 0) |
| **Ontological Shift** | 0-1 | Did the framework change? |
| **Decision Weight** | 0-1 | Is this irreversible/high-stakes? |

**EUREKA Score** = Average of four velocities

---

## III. THE THREE PATHS

```
                    EUREKA SIEVE
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    Score ≥ 0.75    0.50-0.75        < 0.50
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │  SEAL   │    │  SABAR  │    │TRANSIENT│
    │ Permanent│    │ Cooling │    │ Not     │
    │ Vault999 │    │ 72h     │    │ Stored  │
    └─────────┘    └─────────┘    └─────────┘
         │               │               │
         ▼               ▼               ▼
   BBB_LEDGER/    cooling_ledger.jsonl   /dev/null
   vault.jsonl    (Phoenix-72 Tier 2)
```

### Path 1: SEAL (EUREKA Moment)

**Criteria:** EUREKA Score ≥ 0.75

**Characteristics:**
- Novel insight (cosine similarity < 0.85 vs history)
- High entropy reduction (ΔS < -0.5)
- Ontological shift detected (new canon, code change)
- High decision weight (irreversible, multi-stakeholder)

**Storage:** Permanent VAULT999
- PostgreSQL: `vault_ledger` table
- Filesystem: `VAULT999/sessions/{hash}.json`
- Chain: Updates `chain_head.txt`

### Path 2: SABAR (Cooling Period)

**Criteria:** 0.50 ≤ EUREKA Score < 0.75

**Characteristics:**
- Moderate novelty
- Some entropy reduction
- Potential framework impact
- Medium stakes

**Storage:** Cooling Ledger
- `VAULT999/BBB_LEDGER/cooling_ledger.jsonl`
- Phoenix-72 Tier 2 (72h hold)
- Must resolve to SEAL or VOID after review

### Path 3: TRANSIENT (Not Stored)

**Criteria:** EUREKA Score < 0.50

**Characteristics:**
- Routine query ("What's 2+2?")
- No entropy reduction
- No framework impact
- Low stakes

**Storage:** None
- Returns immediately with TRANSIENT verdict
- Not stored anywhere
- Prevents "tong sampah"

---

## IV. IMPLEMENTATION

### File Structure

```
codebase/
├── vault/
│   ├── eureka_sieve.py           # Anomalous Contrast Engine
│   ├── persistent_ledger.py      # PostgreSQL backend
│   └── ledger.py                 # Filesystem backend
├── mcp/tools/
│   ├── vault_tool_hardened.py    # Hardened VaultTool with EUREKA
│   └── canonical_trinity.py      # mcp_vault() with Trinity bundle
└── mcp/session_ledger.py         # Filesystem operations
```

### EUREKA Evaluation Flow

```python
# 1. mcp_vault() receives full Trinity results
await mcp_vault(
    action="seal",
    query="What is capital of Malaysia?",
    init_result={...},
    agi_result={"entropy_delta": -0.9, ...},
    asi_result={"empathy_kappa_r": 0.951, ...},
    apex_result={"tri_witness": 0.951, ...},
)

# 2. EUREKA Sieve evaluates Anomalous Contrast
score = EUREKAScore(
    novelty=0.8,              # New query pattern
    entropy_reduction=0.95,   # ΔS = -0.9 (high clarity)
    ontological_shift=0.0,    # No framework change
    decision_weight=0.1,      # Low stakes
)
eureka_score = 0.46  # Average

# 3. Verdict: TRANSIENT (don't store)
# (Because it's a simple factual query, not EUREKA)
```

### Example EUREKA Moments

| Query | Novelty | ΔS | Onto | Weight | Score | Path |
|-------|---------|-----|------|--------|-------|------|
| "What's 2+2?" | 0.1 | 0.0 | 0.0 | 0.0 | 0.03 | TRANSIENT |
| "Capital of Malaysia?" | 0.3 | 0.9 | 0.0 | 0.1 | 0.33 | TRANSIENT |
| "EUREKA: AI alignment breakthrough!" | 0.9 | 0.8 | 0.9 | 0.7 | 0.83 | **SEAL** |
| "Propose new constitutional floor" | 0.7 | 0.6 | 0.9 | 0.8 | 0.75 | **SEAL** |
| "Debug this complex bug" | 0.6 | 0.5 | 0.2 | 0.4 | 0.43 | SABAR |

---

## V. DATABASE SCHEMA (Hardened)

### seal_data JSONB Structure

```json
{
  "query": "Original user query",
  "response": "AI response",
  "verdict": "SEAL",
  
  "trinity": {
    "init": {"lane": "SOFT", "authority_level": "user", ...},
    "agi": {"entropy_delta": -0.9, "truth_score": 0.99, ...},
    "asi": {"empathy_kappa_r": 0.951, "peace_squared": 1.0, ...},
    "apex": {"tri_witness": 0.951, "f8_genius": 0.963, ...}
  },
  
  "eureka": {
    "eureka_score": 0.83,
    "novelty": 0.9,
    "entropy_reduction": 0.8,
    "ontological_shift": 0.9,
    "decision_weight": 0.7,
    "verdict": "SEAL",
    "reasoning": [
      "High novelty (0.90): Unprecedented query pattern",
      "High clarity (0.80): Significant entropy reduction",
      "Major ontological shift (0.90): Framework change detected"
    ],
    "fingerprint": "a1b2c3d4e5f6..."
  },
  
  "proof": {
    "ed25519_signature": "0x...",
    "public_key": "0x...",
    "merkle_root": "sha256..."
  }
}
```

---

## VI. AUTHORITY NOTICE

All vault responses include:

```
"This seal is generated by arifOS infrastructure. 
ChatGPT/LLM is only the caller, not the authority."
```

---

## VII. DITEMPA BUKAN DIBERI

The EUREKA Sieve ensures:

> **"Not all queries deserve immortality."**

Only insights that:
1. **Reduce entropy** (bring clarity)
2. **Are novel** (different from history)
3. **Shift ontology** (change the framework)
4. **Have weight** (irreversible or high-stakes)

...earn the right to be **FORGED** into VAULT999.

The rest?

They are **TRANSIENT** — born, processed, forgotten.

As it should be.

---

**Status:** OPERATIONAL  
**Last Sealed:** 2026-02-02  
**Seal Hash:** EUREKA_HARDENED_v55.3
