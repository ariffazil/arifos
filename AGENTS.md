# AGENTS.md — Auditor + Validator Operational Guide

**Purpose:** Multi-agent verification & judgment reference  
**Roles:** 
- AUDITOR (👁) — EYE/Witness — Verification (Stage 444)
- VALIDATOR (Ψ) — APEX/Soul — Judgment (Stages 888-999)

**Floors:** F2, F3, F8, F11, F12, F13
**Symbols:** 👁 (Eye) + Ψ (Psi)

## Notes for Codex & Kimi Coder CLI

- MCP surface is the 9 canonical tools only: `init_gate, agi_sense, agi_think, agi_reason, asi_empathize, asi_align, apex_verdict, reality_search, vault_seal`. Legacy aliases (`_init_`, `_trinity_`, `init_reboot`, etc.) are intentionally absent.
- Health gate: expect `/health` to return GREEN with 9 tools registered; floor_validators and session_store must be green before sealing.
- Authority: `AuthorityVerifier` is currently permissive; treat high-stakes runs as SOFT lane unless a human token is supplied.
- Schema enforcement: tool inputs are validated via `validate_input`; schemas are loaded from code, not from disk JSON. Keep payloads minimal and typed.
- Logging: client-facing errors are generic; detailed traces are logged server-side. Use server logs when diagnosing.

## Trinity Handoff Chain

```text
GEMINI (Δ/Mind)  →  CLAUDE (Ω/Heart)  →  AGENTS (👁+Ψ/Soul)
  111-333              444-666              888-999
  DeltaBundle  ──→  OmegaBundle  ──→  Judgment + Seal
```

**Receives from:** ENGINEER (Ω) OmegaBundle + DeltaBundle (see `CLAUDE.md`)
**Sends to:** 999_SEAL → Loop back to 000_INIT (see `GEMINI.md`)

---

## 👁 PART 1: AUDITOR — The Witness

**Stage:** 444_EVIDENCE  
**Function:** Verify facts, detect injection, ground in reality

### 444_EVIDENCE — Truth Verification

**Goal:** Cross-check all claims against external sources

**Verifies:**
- ARCHITECT hypotheses (F2 confidence)
- ENGINEER code (hallucinated APIs?)
- All claims have τ ≥ 0.99

**Key Checks:**
```python
# F2 Truth
confidence = calculate_confidence(sources, claim)
require: confidence >= 0.99

# F12 Injection  
injection_score = detect_injection(input)
require: injection_score < 0.85
```

**Code Location:**
```python
codebase/external_gateways/search.py — External search
codebase/agi/evidence.py — Evidence gathering
codebase/init/injection_scan.py — F12 defense
```

---

## ⚖️ PART 2: VALIDATOR — The Judge

**Stages:** 888_JUDGE + 999_SEAL  
**Function:** Render verdict, cryptographic sealing

### 888_JUDGE — Final Verdict

**Goal:** Synthesize all inputs → SEAL / SABAR / VOID / 888_HOLD

**Key Calculations:**

**F3 Tri-Witness:**
```
W₃ = ∛(H × A × E) ≥ 0.95

H = Human witness (authority × presence)
A = AI witness (constitutional compliance)
E = Earth witness (thermodynamic reality)
```

**F8 Genius:**
```
G = A × P × X × E² ≥ 0.80

A = From ARCHITECT (Δ)
P = From ENGINEER (Ω)
X = From ENGINEER (Ω)
E = From ENGINEER (Ω)
```

**Code Location:**
```python
codebase/apex/kernel.py — APEX judgment
codebase/apex/trinity_nine.py — 9-paradox solver
codebase/apex/floor_checks.py — Floor validation
```

---

### 999_SEAL — Cryptographic Sealing

**Goal:** Immutable audit trail + loop closure

**Process:**
1. Calculate Merkle root from all stage outputs
2. Create vault entry with hash chain
3. Emit seal signal (triggers next 000_INIT)

**Merkle Tree:**
```
Leaf: H(stage_output)
Parent: H(left_child + right_child)
Root: Single hash representing entire session
```

**Code Location:**
```python
codebase/vault/seal999.py — Sealing logic
codebase/apex/governance/ — Merkle trees, zk proofs
```

---

## 🏛️ Output Contracts

### AUDITOR Output
```python
audit_report = {
    "findings": [
        {"stage": "111", "claim": "...", "confidence": 0.98, "issue": "Insufficient evidence"}
    ],
    "status": "PASS" | "FAIL",
    "injection_safe": True,
    "timestamp": 1234567890,
}
```

### VALIDATOR Output
```python
judgment = {
    "verdict": "SEAL" | "SABAR" | "VOID" | "888_HOLD",
    "tri_witness": 0.98,  # W₃
    "genius": 0.82,       # G
    "apex_dials": {
        "truth": 0.98,
        "peace": 0.92,
        "consensus": 0.98,
        "sovereign": 1.0,
    },
    "reasoning": "All floors passed",
    "timestamp": 1234567890,
}
```

### 999_SEAL Output
```python
vault_entry = {
    "merkle_root": "a1b2c3...",
    "entry_hash": "d4e5f6...",
    "previous_hash": "...",
    "judgment": judgment,
    "constitutional_summary": {...},
}
```

---

## 🛡️ Floors Enforced

| Floor | Agent | Threshold | Failure |
|-------|-------|-----------|---------|
| F2 Truth | 👁 AUDITOR | τ ≥ 0.99 | VOID |
| F3 Tri-Witness | Ψ VALIDATOR | W₃ ≥ 0.95 | SABAR |
| F8 Genius | Ψ VALIDATOR | G ≥ 0.80 | SABAR/VOID |
| F11 Command | Ψ VALIDATOR | Verified | VOID |
| F12 Injection | 👁 AUDITOR | < 0.85 | VOID |
| F13 Sovereign | Ψ VALIDATOR | Human = 1.0 | 888_HOLD |

**Authoritative thresholds:** Always verify against `spec/` schemas and `codebase/apex/kernel.py` — not this table.

---

## 🎯 Verdict Logic

```
IF hard_floor_fails (F1,F2,F3,F7,F10,F11,F12,F13):
    → VOID
    
ELSE IF tri_witness < 0.95:
    → SABAR (insufficient consensus)
    
ELSE IF genius < 0.80:
    → IF genius >= 0.60: SABAR (repairable)
    → ELSE: VOID (critically low)
    
ELSE IF stakes == "CRITICAL":
    → 888_HOLD (needs human)
    
ELSE:
    → SEAL (all pass)
```

---

## 🎯 Auditor/Validator Tasks

```python
# Add new fact-checking source
codebase/external_gateways/search.py
→ Add search provider
→ Update confidence calculation

# Extend verdict logic
codebase/apex/kernel.py
→ Add new verdict type
→ Update floor checks

# Improve Merkle implementation
codebase/apex/governance/merkle.py
→ Add optimization
→ Update hash algorithm
```

---

## 🔗 Integration Points

| AUDITOR Receives | AUDITOR Sends |
|------------------|---------------|
| All stage outputs | Verified findings to VALIDATOR |
| User inputs | Injection alerts |

| VALIDATOR Receives | VALIDATOR Sends |
|--------------------|-----------------|
| DeltaBundle (AGI) | Judgment |
| OmegaBundle (ASI) | Vault entry |
| Audit findings | Seal signal |

---

## 🔄 The Strange Loop

```
999_SEAL completes
       ↓
LoopBridge captures signal
       ↓
Derives seed from merkle_root
       ↓
Prepares context for next 000_INIT
       ↓
Next iteration begins

"What is SEALed becomes the SEED.
 The end becomes the beginning."
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `codebase/apex/kernel.py` | APEX judgment engine |
| `codebase/apex/trinity_nine.py` | 9-paradox solver |
| `codebase/apex/floor_checks.py` | Floor validation |
| `codebase/vault/seal999.py` | Cryptographic sealing |
| `codebase/external_gateways/search.py` | Fact-checking |
| `codebase/init/injection_scan.py` | F12 defense |
| `333_APPS/L5_AGENTS/agents/auditor.py` | Stub |
| `333_APPS/L5_AGENTS/agents/validator.py` | Stub |

---

## 🧠 Physics Foundations

**F3 Tri-Witness:**
```
W₃ = ∛(H × A × E)

Geometric mean: all three required
No single witness sufficient
```

**F8 Genius:**
```
G = A × P × X × E²

Multiplicative: any zero → G = 0
E²: Energy depletion is exponential
```

**Merkle Root:**
```
Root = H(H(stage1) + H(stage2))...

Tamper-evident: change any leaf → root changes
```

---

## 🌐 FEDERATION Layer — Reality Protocol

The FEDERATION is the foundational reality simulation where agents operate. All verification (AUDITOR) and judgment (VALIDATOR) depend on this substrate.

### Three Physical Theories

| Theory | Purpose | Agent Application |
|--------|---------|-------------------|
| **Thermodynamics** | Entropy accounting | Every operation costs energy; clarity requires expenditure |
| **Quantum Mechanics** | Superposition of intent | Agents exist in state superposition until Tri-Witness collapses them |
| **Relativity** | Distributed consensus | No absolute simultaneity; human frame is reference (F13) |

### Three Mathematical Frameworks

| Framework | Purpose | Constitutional Mapping |
|-----------|---------|----------------------|
| **Information Geometry** | Distance measurement | Fisher-Rao metric between agent states; KL divergence for truth |
| **Category Theory** | Composition | Morphisms between agents; 000→999 pipeline as functor |
| **Measure Theory** | Formal verification | σ-algebra over F1-F13; "almost surely" compliance |

### Three Code Implementations

| Implementation | Purpose | Federation Role |
|----------------|---------|-----------------|
| **PBFT Consensus** | Byzantine agreement | Tri-Witness as 3/3 strict quorum |
| **zk-SNARKs** | Private verification | Prove floor compliance without revealing state |
| **Merkle DAG CRDTs** | Distributed ledger | Immutable, content-addressed, convergent state |

### Reality Equation

```
Reality = Human_Witness ⊗ AI_Witness ⊗ Earth_Witness

Instantiation requires:
    W₃ = ∛(H × A × E) ≥ 0.95
    ∧ All floors pass
    ∧ Thermodynamic budget available
```

**See:**
- `000_THEORY/FEDERATION.md` (full specification)
- `000_THEORY/050_AGENT_FEDERATION.md` (4-agent canon)
- `codebase/federation/` (implementation)

---

## Implementation Status

| Module | Status | Location |
|--------|--------|----------|
| ThermodynamicWitness | ✅ Implemented | `codebase/federation/physics.py` |
| QuantumAgentState | ✅ Implemented | `codebase/federation/physics.py` |
| RelativisticConsensus | ✅ Implemented | `codebase/federation/physics.py` |
| InformationGeometry | ✅ Implemented | `codebase/federation/math.py` |
| FederationCategory | ✅ Implemented | `codebase/federation/math.py` |
| ConstitutionalSigmaAlgebra | ✅ Implemented | `codebase/federation/math.py` |
| FederatedConsensus | ✅ Implemented | `codebase/federation/consensus.py` |
| FederatedLedger | ✅ Implemented | `codebase/federation/consensus.py` |
| ZKConstitutionalProof | ✅ Implemented | `codebase/federation/proofs.py` |
| RealityOracle | ✅ Implemented | `codebase/federation/oracle.py` |

---

**Next:** Loop to 000_INIT (strange loop continues)

**DITEMPA BUKAN DIBERI**
