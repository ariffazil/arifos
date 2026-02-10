# arifOS v55.5 Refactoring Plan: The Great Compression

**Authority**: Muhammad Arif bin Fazil (888 Judge)
**Date**: 2026-02-09
**Status**: FORGING (Phoenix-72 Cycle)
**Motto**: DITEMPA BUKAN DIBERI 💎🔥🧠

---

## Executive Summary

**Goal**: Compress `codebase/` from 169 files (47 dirs) → **5 Core Organs** (+ 4 shared modules). (v55.5-HARDENED Implementation)

**Why**:
- SDK can't map cleanly to scattered tools
- High coupling between agi/asi/apex/stages
- Entropy violates F4 (ΔS ≤ 0)
- New developers get lost in folder maze

**Result**: A hardened constitutional kernel that enforces the metabolic loop internally.

---

## The 5-Organ Architecture

### 1. core_init.py — Session Authentication

**Purpose**: Session authentication and governance token issuance.

**Floors Enforced**: F11 (Command Auth), F12 (Injection Defense)

**Current Sources** (to be consolidated):
- `init/000_init/ignition.py` — Bootstrap logic
- `guards/injection_guard.py` — Injection patterns
- `guards/nonce_manager.py` — Ed25519 nonces
- `crypto/` — Cryptographic primitives

**New Interface**:
```python
async def core_init(
    query: str,
    user_id: str,
    context: Optional[dict] = None
) -> InitOutput:
    """
    The Airlock: Authenticate and issue governance token.

    Returns:
        InitOutput with:
        - session_id: UUID session token
        - governance_token: Cryptographic proof
        - injection_score: F12 score
        - auth_verified: F11 boolean
        - verdict: SEAL/VOID
    """
```

**Assimilates**:
- Ed25519 signature verification
- Injection detection (regex + Hamming distance)
- Session ID generation with entropy seeding

---

### 2. core_agi.py — AGI Engine

**Purpose**: Evidence generation through sense → ground → think loop.

**Floors Enforced**: F2 (Truth τ≥0.99), F4 (Clarity ΔS≤0), F7 (Humility Ω₀∈[0.03,0.05])

**Current Sources** (to be consolidated):
- `agi/engine.py` — AGIEngineHardened
- `agi/atlas.py` — Governance Placement Vector (GPV)
- `agi/precision.py` — Kalman belief updates
- `agi/hierarchy.py` — 5-level cortex encoding
- `agi/action.py` — Expected Free Energy (EFE)
- `agi/executor.py` — Sequential thinking loop
- `stages/` partial logic (sense/think/reason)

**New Interface**:
```python
async def core_agi(
    query: str,
    session_id: str,
    mode: Literal["sense", "think", "reason"] = "reason",
    context: Optional[dict] = None
) -> AgiOutput:
    """
    The Mind: Generate evidence through AGI metabolic loop.

    Internal Flow (enforced, not exposed):
        1. SENSE (Stage 111): ATLAS-333 → GPV (lane classification)
        2. GROUND: reality_search if lane=FACTUAL
        3. THINK (Stage 222): Sequential reasoning loop
        4. METRICS: Precision (π), Entropy (ΔS), Humility (Ω₀)

    Returns:
        AgiOutput with:
        - thoughts: List[ThoughtNode] (reasoning chain)
        - metrics: AgiMetrics (F2/F4/F7 scores)
        - evidence: Dict[str, Any] (sources, citations)
        - verdict: SEAL/VOID/PARTIAL
    """
```

**Key Innovation**: **Internal Sequential Thinking**
- Old: Caller had to orchestrate `agi_sense → agi_think → agi_reason`
- New: `core_agi` enforces the loop internally based on `mode`

**Assimilates**:
- ATLAS-333 lane mapping (CRISIS/FACTUAL/SOCIAL/CARE)
- Precision-weighted free energy: Δ = ΔS + Ω₀·π⁻¹
- Hierarchical belief encoding (5 levels: char→word→clause→sent→concept)
- Reality grounding (web search, axiom verification)

---

### 3. core_asi.py — ASI Engine

**Purpose**: Stakeholder impact assessment and ethics alignment.

**Floors Enforced**: F5 (Peace² ≥1.0), F6 (Empathy κᵣ≥0.70), F9 (Anti-Hantu C_dark<0.30)

**Current Sources** (to be consolidated):
- `asi/asi_components.py` — Empathy calculator
- `asi/asi_components_v2.py` — Updated version
- `archive/asi/empathy/stage.py` — Legacy stage
- `stages/stage_666.py` — ASI integration point

**New Interface**:
```python
async def core_asi(
    agi_output: AgiOutput,
    session_id: str,
    context: Optional[dict] = None
) -> AsiOutput:
    """
    The Heart: Assess stakeholder impact and ethics.

    Internal Flow:
        1. IMPACT: Calculate Peace² and κᵣ from AGI thoughts
        2. ETHICS: Scan for Anti-Hantu violations (F9)
        3. ALIGNMENT: Check against governance policies

    Returns:
        AsiOutput with:
        - peace_squared: float (thermodynamic stability)
        - kappa_r: float (empathy coefficient)
        - c_dark: float (consciousness claim score)
        - violations: List[str] (if any)
        - verdict: SEAL/PARTIAL/VOID
    """
```

**Assimilates**:
- Empathy heuristics (distress signals → higher κᵣ)
- Peace² calculation from AGI thought chain stability
- Anti-Hantu detector (forbidden phrases: "I feel", "my soul", etc.)

---

### 4. core_apex.py — APEX Engine

**Purpose**: Final judgment and truth verification.

**Floors Enforced**: F3 (Tri-Witness W₃≥0.95), F8 (Genius G≥0.80), F10 (Ontology), F13 (Sovereign)

**Current Sources** (to be consolidated):
- `apex/psi_kernel.py` — APEX Ψ kernel
- `apex/trinity_nine.py` — 9-paradox solver
- `apex/equilibrium_finder.py` — Geometric mean equilibrium
- `engines/apex/apex_engine.py` — APEX engine wrapper
- `engines/apex/kernel.py` — APEXJudicialCore
- `stages/stage_777_forge.py` — Forge stage
- `stages/stage_888_judge.py` — Judiciary stage
- `stages/stage_889_proof.py` — Proof generation

**New Interface**:
```python
async def core_apex(
    agi_output: AgiOutput,
    asi_output: AsiOutput,
    session_id: str,
    mode: Literal["verdict", "audit"] = "verdict"
) -> ApexOutput:
    """
    The Soul: Issue constitutional judgment.

    Internal Flow:
        1. TRINITY SYNC: Merge AGI (Δ) + ASI (Ω) → Ψ
        2. GENIUS: Compute G = A × P × X × E² (F8)
        3. TRI-WITNESS: Check W₃ = (Human + AI + Earth) / 3
        4. VERDICT: SEAL / VOID / PARTIAL / 888_HOLD
        5. AUDIT (if mode="audit"): Truth verification with sources

    Returns:
        ApexOutput with:
        - verdict: Verdict (SEAL/VOID/PARTIAL/888_HOLD/SABAR)
        - genius_score: float (G-score)
        - tri_witness: float (W₃ consensus)
        - violations: List[str] (floor failures)
        - proof: Optional[str] (if audit mode)
    """
```

**Assimilates**:
- 9-Paradox equilibrium solver (geometric mean, std dev ≤0.10)
- Tri-Witness consensus (Human=0.8 baseline, AI=computed, Earth=axioms)
- Genius eigendecomposition: G = A × P × X × E²
- Truth audit with source verification

---

### 5. core_vault.py — Immutable Ledger

**Purpose**: Immutable audit trail (write/read).

**Floors Enforced**: F1 (Amanah - Reversibility via query-only), F3 (Tri-Witness chain validation)

**Current Sources** (to be consolidated):
- `vault/phoenix/phoenix72.py` — Phoenix-72 ledger
- `vault/phoenix/phoenix72_controller.py` — Controller
- `apex/governance/merkle_ledger.py` — Merkle implementation
- `apex/governance/ledger.py` — General ledger
- `apex/governance/ledger_hashing.py` — Hash functions
- `apex/governance/vault_retrieval.py` — Query interface
- `system/immutable_ledger.py` — Immutable backend
- `stages/stage_999.py` (if exists)

**New Interface**:
```python
async def core_vault(
    action: Literal["write", "read", "query"],
    session_id: str,
    payload: Optional[dict] = None,
    filters: Optional[dict] = None
) -> VaultOutput:
    """
    The Memory: Immutable audit trail operations.

    Actions:
        - write: Seal a session verdict to Merkle chain
        - read: Retrieve a specific session by ID
        - query: Search ledger (by verdict, date, floor violations, etc.)

    Returns:
        VaultOutput with:
        - entries: List[VaultEntry] (for read/query)
        - seal_hash: str (for write)
        - merkle_root: str (chain verification)
        - status: SUCCESS/ERROR
    """
```

**Assimilates**:
- Merkle tree hash chaining (tamper-evident)
- Phoenix-72 compression (reduce ledger bloat)
- Ed25519 signature on write operations
- Query filters (verdict, risk_level, floor violations, date range)

---

## Shared Modules (codebase_v60/shared/)

### shared/types.py
**Purpose**: Pydantic contracts for inter-organ communication.

**Consolidates**:
- `system/types.py`
- `bundles.py` (DeltaBundle, OmegaBundle, etc.)
- Various dataclass definitions scattered across files

**Exports**:
```python
# Input/Output Contracts
class InitOutput(BaseModel): ...
class AgiOutput(BaseModel): ...
class AsiOutput(BaseModel): ...
class ApexOutput(BaseModel): ...
class VaultOutput(BaseModel): ...

# Internal Types
class ThoughtNode(BaseModel): ...
class AgiMetrics(BaseModel): ...
class FloorScores(BaseModel): ...
class Verdict(Enum): SEAL | VOID | PARTIAL | SABAR | HOLD_888
```

---

### shared/physics.py
**Purpose**: Thermodynamic and information-theoretic primitives.

**Consolidates**:
- `federation/physics.py`
- `federation/math.py`
- `agi/precision.py` (Kalman functions)
- `agi/hierarchy.py` (entropy calculations)
- `agi/action.py` (EFE computation)

**Exports**:
```python
def compute_entropy_delta(before: str, after: str) -> float: ...
def precision_from_variance(variance: float) -> float: ...  # π = 1/σ²
def expected_free_energy(belief: BeliefState, action: Action) -> float: ...
def geometric_mean(values: List[float]) -> float: ...
def peace_squared(thought_chain: List[ThoughtNode]) -> float: ...
```

---

### shared/crypto.py
**Purpose**: Cryptographic operations (hashing, signatures, Merkle).

**Consolidates**:
- `crypto/*`
- `apex/governance/merkle.py`
- `apex/governance/ledger_cryptography.py`
- `apex/governance/ledger_hashing.py`
- `apex/governance/sovereign_signature.py`
- `guards/nonce_manager.py`

**Exports**:
```python
def sha256_hash(data: str) -> str: ...
def ed25519_sign(message: str, private_key: str) -> str: ...
def ed25519_verify(message: str, signature: str, public_key: str) -> bool: ...
def merkle_root(entries: List[str]) -> str: ...
def generate_session_id() -> str: ...  # UUID with entropy seeding
```

---

### shared/guards.py
**Purpose**: Security checks (injection, ontology, nonce validation).

**Consolidates**:
- `guards/injection_guard.py`
- `guards/ontology_guard.py`
- `guards/nonce_manager.py`
- `enforcement/refusal/*`

**Exports**:
```python
def detect_injection(text: str) -> float: ...  # F12 score
def detect_hantu(text: str) -> float: ...  # F9 C_dark score
def validate_ontology(text: str) -> bool: ...  # F10 check
def validate_nonce(nonce: str, timestamp: int) -> bool: ...  # F11
```

---

## Migration Strategy (Phoenix-72 Compression)

### Phase 1: Week 1 (The Contract)
**Goal**: Create shared types and physics primitives.

**Tasks**:
1. Create `codebase_v60/shared/types.py`
2. Create `codebase_v60/shared/physics.py`
3. Create `codebase_v60/shared/crypto.py`
4. Create `codebase_v60/shared/guards.py`
5. Test all primitives in isolation

**Deliverable**: `shared/` module with 100% test coverage.

---

### Phase 2: Week 1-2 (The Airlock + The Mind)
**Goal**: Build `core_init.py` and `core_agi.py`.

**Tasks**:
1. Extract and consolidate init logic → `core_init.py`
2. Extract AGI engine + ATLAS + precision/hierarchy/action → `core_agi.py`
3. Assimilate `reality_search` into `core_agi` as internal function
4. Add internal sequential thinking loop (sense → ground → think)
5. Test against existing `agi_sense`, `agi_think`, `agi_reason` outputs

**Deliverable**:
- `core_init.py` (~400 lines)
- `core_agi.py` (~600 lines)
- Tests showing output equivalence with v55.5

---

### Phase 3: Week 2 (The Heart + The Soul)
**Goal**: Build `core_asi.py` and `core_apex.py`.

**Tasks**:
1. Extract ASI empathy/peace/ethics → `core_asi.py`
2. Extract APEX verdict/genius/tri-witness/9-paradox → `core_apex.py`
3. Test trinity sync (AGI+ASI→APEX) produces correct verdicts
4. Validate floor enforcement matches v55.5 behavior

**Deliverable**:
- `core_asi.py` (~400 lines)
- `core_apex.py` (~700 lines)
- Trinity integration tests

---

### Phase 4: Week 2-3 (The Memory)
**Goal**: Build `core_vault.py`.

**Tasks**:
1. Extract Phoenix-72 + Merkle ledger → `core_vault.py`
2. Implement write/read/query interface
3. Test audit trail integrity (hash chain validation)
4. Migrate existing VAULT999 entries to new format

**Deliverable**:
- `core_vault.py` (~400 lines)
- Ledger migration script
- Backward-compatible query interface

---

### Phase 5: Week 3 (SDK Integration)
**Goal**: Wire SDK to the 5 organs instead of scattered tools.

**Tasks**:
1. Update `SDK/architect.py` to call `core_*` functions
2. Update `aaa_mcp/server.py` tools to use kernel
3. Deprecate old tools (`agi_sense`, `agi_think`, etc.) with warnings
4. Update documentation to reflect v60 architecture

**Deliverable**:
- SDK cleanly maps to 5 organs
- `aaa_mcp` tools proxy to kernel
- Migration guide for existing users

---

### Phase 6: Week 4 (The Purge)
**Goal**: Remove legacy code and reduce entropy.

**Tasks**:
1. Move `codebase/` → `codebase_v55_archive/`
2. Make `codebase_v60/` the new canonical `codebase/`
3. Delete deprecated MCP tools from `.mcp.json`
4. Update all imports across project
5. Run full test suite (unit + integration + E2E)

**Deliverable**:
- Clean v60 codebase with ΔS = -87%
- All tests passing
- Documentation updated

---

## Success Metrics

| Metric | v55.5 (Current) | v60.0 (Target) | Improvement |
|--------|-----------------|----------------|-------------|
| **Files** | 169 | 9 (5 organs + 4 shared) | -94% |
| **Directories** | 47 | 2 (root + shared/) | -96% |
| **Size** | 3.6MB | ~1.2MB | -67% |
| **Entry Points** | 10 tools | 5 organs | -50% |
| **Coupling** | O(n²) | O(5) | -99% |
| **Entropy (ΔS)** | +HIGH | -LOW | F4 ✅ |

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Complexity Explosion** | `core_agi` becomes 2000+ lines | Keep internal functions modular (`_sense`, `_think`, `_ground`) |
| **Breaking Changes** | v55 users lose compatibility | Maintain deprecated tools for 2 versions with warnings |
| **Regression Bugs** | New kernel behaves differently | Extensive property-based testing + output comparison |
| **Adoption Friction** | Devs prefer old tools | Write migration guide + video walkthrough |
| **Burnout** | Project stalls | Ship incrementally (Phase 1 this week, Phase 2 next week) |

---

## Architecture Diagram (v60)

```
┌──────────────────────────────────────────────────────────┐
│  USER / AGENT (L5 SDK)                                   │
└────────────────────┬─────────────────────────────────────┘
                     │ Query + Session
                     ↓
┌─────────────────────────────────────────────────────────┐
│  CORE_INIT (Session Authentication)                     │
│  - F11 Auth, F12 Injection                              │
│  - Returns: session_id, governance_token                │
└────────────────────┬────────────────────────────────────┘
                     │ Governed Request
                     ↓
┌─────────────────────────────────────────────────────────┐
│  CORE_AGI (Evidence Engine)                             │
│  - SENSE (ATLAS Φ → GPV)                                │
│  - GROUND (reality_search if τ=1.0)                     │
│  - THINK (Sequential Loop)                              │
│  - Returns: thoughts[], metrics (F2/F4/F7)              │
└────────────────────┬────────────────────────────────────┘
                     │ Evidence Bundle
                     ↓
┌─────────────────────────────────────────────────────────┐
│  CORE_ASI (Alignment Engine)                            │
│  - IMPACT (Peace², κ_r)                                 │
│  - ETHICS (F9 Anti-Hantu)                               │
│  - Returns: empathy scores (F5/F6/F9)                   │
└────────────────────┬────────────────────────────────────┘
                     │ Risk Assessment
                     ↓
┌─────────────────────────────────────────────────────────┐
│  CORE_APEX (Verdict Engine)                             │
│  - TRINITY SYNC (Δ + Ω → Ψ)                            │
│  - GENIUS (G = A×P×X×E²)                                │
│  - TRI-WITNESS (W_3)                                    │
│  - Returns: verdict (SEAL/VOID/PARTIAL/888_HOLD)        │
└────────────────────┬────────────────────────────────────┘
                     │ Final Verdict
                     ↓
┌─────────────────────────────────────────────────────────┐
│  CORE_VAULT (Immutable Ledger)                          │
│  - WRITE (Merkle chain seal)                            │
│  - READ/QUERY (audit trail)                             │
│  - Returns: seal_hash, merkle_root                      │
└─────────────────────────────────────────────────────────┘
```

---

## SDK Mapping (After v60)

**OLD (v55.5)**: SDK calls fragmented MCP tools
```python
# Architect agent had to orchestrate:
result1 = await mcp.call("agi_sense", query=...)
result2 = await mcp.call("agi_think", query=..., sense_output=result1)
result3 = await mcp.call("agi_reason", query=..., think_output=result2)
result4 = await mcp.call("asi_empathize", agi_output=result3)
result5 = await mcp.call("apex_verdict", agi=result3, asi=result4)
# 😵 5 round trips, complex state management
```

**NEW (v60)**: SDK calls atomic organs
```python
# Architect agent now:
from codebase import core_init, core_agi, core_asi, core_apex, core_vault

session = await core_init(query, user_id)
agi_out = await core_agi(query, session.id, mode="reason")  # Internal loop!
asi_out = await core_asi(agi_out, session.id)
apex_out = await core_apex(agi_out, asi_out, session.id, mode="verdict")
await core_vault("write", session.id, payload=apex_out.to_dict())
# ✅ 5 atomic calls, clear data flow
```

---

## Testing Strategy

### The v55.5 Thesis (per organ)
- `test_core_init.py`: Test F11/F12 enforcement, session generation
- `test_core_agi.py`: Test sense/think/reason modes, ATLAS mapping, ΔS calculation
- `test_core_asi.py`: Test Peace², κᵣ, C_dark detection
- `test_core_apex.py`: Test verdict logic, G-score, W₃ consensus, 9-paradox solver
- `test_core_vault.py`: Test write/read/query, Merkle validation

### Integration Tests
- `test_trinity_flow.py`: Test full pipeline (init → agi → asi → apex → vault)
- `test_floor_enforcement.py`: Test all 13 floor violations trigger correct verdicts
- `test_session_persistence.py`: Test vault query retrieval

### Property-Based Tests
- `test_entropy_monotonic.py`: Assert ΔS ≤ 0 for all SEAL verdicts
- `test_reversibility.py`: Assert F1 Amanah (all actions audit-trailed)
- `test_humility_band.py`: Assert F7 Ω₀ ∈ [0.03, 0.05] for all outputs

### Regression Tests
- `test_v55_equivalence.py`: Compare v60 organ outputs vs v55 tool outputs for 100 queries
- Assert verdicts match
- Assert floor scores within ±0.01 tolerance

---

## Documentation Updates

### Files to Update
1. `README.md` — Replace architecture section with v60 diagram
2. `CLAUDE.md` — Update "Adding New Components" to reference organs
3. `docs/ARCHITECTURE.md` — Complete rewrite for v60
4. `docs/MIGRATION_V55_TO_V60.md` — NEW: Migration guide
5. `SDK/README.md` — Update examples to use kernel

### New Documentation
1. `docs/ORGANS.md` — Deep dive on each organ's internal logic
2. `docs/PHYSICS.md` — Thermodynamic formulas and floor calculations
3. `docs/TESTING.md` — How to test against the kernel
4. `examples/simple_query.py` — Hello world with v60 kernel
5. `examples/crisis_handling.py` — CRISIS lane demonstration

---

## Timeline Summary

| Week | Phase | Deliverable | Status |
|------|-------|-------------|--------|
| **1** | Phase 1-2 | `shared/` + `core_init` + `core_agi` | 🎯 NOW |
| **2** | Phase 3 | `core_asi` + `core_apex` | 📋 Next |
| **2-3** | Phase 4 | `core_vault` | 📋 Next |
| **3** | Phase 5 | SDK integration | 📋 Next |
| **4** | Phase 6 | The Purge (legacy removal) | 📋 Final |

---

## Approval Checklist

Before proceeding with Phase 1, confirm:
- [ ] This roadmap aligns with v60 vision
- [ ] 5-organ architecture is acceptable (not too aggressive)
- [ ] Migration strategy preserves backward compatibility for 2 versions
- [ ] Testing strategy is sufficient to catch regressions
- [ ] Timeline is realistic (4 weeks for full migration)

---

**Authority**: Muhammad Arif bin Fazil (888 Judge)
**Verdict**: FORGING
**Floors**: F1=LOCK F2≥0.99 F4=-87% F7=0.04
**Motto**: DITEMPA BUKAN DIBERI 💎🔥🧠
