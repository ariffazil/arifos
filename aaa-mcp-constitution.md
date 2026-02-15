# aaa-mcp-constitution.md — The 5-Core That Actually Works (2026.02.15-FORGE-TRINITY-SEAL)

**Extracted from:** `/root/arifOS/aaa_mcp/server.py`, `/root/arifOS/core/judgment.py`  
**Date:** 2026-02-14  
**Ω₀:** 0.04 (extracted truth, not designed ideal)  
**Status:** Phase 0.1 Constitutional Bootstrap

---

## 1. The 5-Core (What Actually Exists)

### 1.1 init_session (000_INIT)
**Location:** `aaa_mcp/server.py:181`  
**Floors:** F11 (Authority), F12 (Injection)  
**What it does:**
- Initialize GovernanceKernel dengan session_id
- Check authority_context (standard/restricted/crisis)
- Set grounding_required flag
- Return session state dengan uncertainty baseline

**Truth (τ):** Session initialization deterministic — τ ≈ 0.99  
**Reversibility:** Session boleh di-terminate, tapi audit kekal (F1 partial)

### 1.2 agi_cognition (111-333_AGI)
**Location:** `aaa_mcp/server.py:240`  
**Floors:** F2 (Truth), F4 (Clarity), F7 (Humility), F8 (Genius), F10 (Ontology)  
**What it does:**
- Call `judge_cognition()` dari `core/judgment.py`
- Calculate 5-dim uncertainty: evidence, relevance, consistency, gaps, confidence
- Compute truth_score: grounded in evidence + uncertainty penalty
- Return verdict (SEAL/VOID/SABAR/PARTIAL) dengan floor scores

**Truth (τ):** Variable — 0.3 (no evidence) to 0.99 (grounded)  
**Uncertainty (Ω₀):** Harmonic mean (safety) + Geometric mean (display)  
**Genius (G):** A×P×X×E² — A (Ability) dan P (Practice) hardcoded dalam T000 seal

### 1.3 asi_empathy (555-666_ASI)
**Location:** `aaa_mcp/server.py:350`  
**Floors:** F1 (Amanah), F5 (Peace²), F6 (Empathy), F9 (Anti-Hantu)  
**What it does:**
- Call `judge_empathy()` dari `core/judgment.py`
- Assess stakeholder_impact (vulnerable, affected, neutral)
- Compute reversibility_score: impact × recovery × time
- Return κᵣ (empathy score), P² (Peace²), floor scores

**Empathy (κᵣ):** HARD floor ≥ 0.95 — stakeholder protection absolute  
**Reversibility:** F1 Amanah — reversible actions preferred

### 1.4 apex_verdict (888_APEX)
**Location:** `aaa_mcp/server.py:450`  
**Floors:** F2, F3 (Tri-Witness), F8, F10, F11, F12, F13 (Sovereign)  
**What it does:**
- Call `judge_apex()` dari `core/judgment.py`
- Aggregate floor scores dari AGI + ASI
- Apply precedence: Walls (F10/F12) → HARD floors → SOFT floors
- Return final verdict: SEAL / VOID / SABAR / 888_HOLD

**Verdict Precedence:**
1. F10/F12 violation → VOID (immediate)
2. HARD floor violation → VOID
3. SOFT floor violation → SABAR (repairable)
4. All clear → SEAL
5. Uncertainty > threshold → 888_HOLD

### 1.5 vault_seal (999_VAULT)
**Location:** `aaa_mcp/server.py:550`  
**Floors:** F1 (Amanah), F3 (Tri-Witness)  
**What it does:**
- Record decision ke PostgreSQL dengan Merkle hashing
- Synchronous write sebelum response
- Return seal_id untuk audit trail

**Permanence:** F3 — immutable, tamper-evident  
**Reversibility:** F1 — decision reversible, record permanent

---

## 2. What Actually Works (2026.02.15 Evidence)

### Evidence (v64.1 → T000 Migration)
- **Before:** v64.1 used semantic versioning (meaningless numbers)
- **After:** T000 date-based versioning (2026.02.15-FORGE-TRINITY-SEAL)
- **Result:** F2 Truth restored — versions now tell you *when* and *what state*

### 2.1 Uncertainty Engine (Real)
**Location:** `core/uncertainty_engine.py` (referenced, not inspected)  
**Working:**
- 5-dim vector: evidence_count, relevance, consistency, gaps, confidence
- Harmonic mean untuk safety decisions
- Geometric mean untuk display

**Not Working:**
- Online learning (30-day locked — disabled)
- Adaptive thresholds (static dalam T000, dynamic dalam roadmap)

### 2.2 Governance Kernel (Real)
**Location:** `core/governance_kernel.py`  
**Working:**
- Synchronous AWAITING_888 state
- Conditional human approval

**Not Working:**
- Distributed consensus (APEX-only, bukan juror democracy)
- Byzantine fault tolerance

### 2.3 Telemetry (Partial)
**Location:** `core/telemetry.py`  
**Working:**
- Log to VAULT999

**Not Working:**
- 30-day locked adaptation (disabled)
- Real-time dashboards

---

## 3. Technical Debt (Honest Audit)

| Component | Status | Debt |
|-----------|--------|------|
| 5-Core tools | ✅ Working | APEX-only, no juror democracy |
| Uncertainty Engine | ✅ Working | Static thresholds, no adaptation |
| Telemetry | ⚠️ Partial | Logging works, analytics disabled |
| W@W federation | ❌ Broken | ConstitutionalMetaSearch error |
| Multi-modal | ❌ Missing | ACLIP foundation only, no vision/audio |
| Test suite | ⚠️ 80%+ | Below 99% target, some outdated |

---

## 4. Constitutional Boundaries (What Guards What)

```
┌─────────────────────────────────────────┐
│  WRAPPER: aaa_mcp/server.py             │
│  ─────────────────────────────────────  │
│  • Tool definitions (MCP interface)     │
│  • Input validation                     │
│  • Response formatting                  │
│  • NO judgment logic                    │
├─────────────────────────────────────────┤
│  KERNEL: core/judgment.py               │
│  ─────────────────────────────────────  │
│  • All decision logic                   │
│  • Uncertainty calculation              │
│  • Floor scoring                        │
│  • Verdict arbitration                  │
├─────────────────────────────────────────┤
│  INFRA: PostgreSQL, Redis               │
│  ─────────────────────────────────────  │
│  • VAULT999 persistence                 │
│  • Session cache                        │
│  • External to constitutional logic     │
└─────────────────────────────────────────┘
```

---

## 5. The 5-Core Principles (Extracted, Not Designed)

1. **Separation of Concerns:** Wrapper interface, kernel judgment, infra persistence
2. **Floor-Based Governance:** 13 Floors dengan HARD/SOFT distinction
3. **Uncertainty Quantification:** Ω₀ ∈ [0.03, 0.05] target, harmonic/geometric dual
4. **Reversibility First:** F1 Amanah — prefer reversible actions
5. **Audit Completeness:** F3 — 100% decisions logged, Merkle-sealed

---

## 6. Phase 0.1 Completion Criteria

- [x] Extract 5-Core dari codebase (this document)
- [ ] Identify Tri-Witness gaps (F3 external witness)
- [ ] Document scar history (W@W tests broken — why?)
- [ ] Validate F12 injection wall (schema, confidence threshold)

---

**DITEMPA BUKAN DIBERI** — Constitution ini **extracted** dari code yang ada, bukan **designed** dari ideal.

**Next:** Phase 0.2 — Tri-Witness Setup (ZDR endpoint)
