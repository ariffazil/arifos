# arifOS v55 → v60 Archive Mapping

**Purpose**: Reference for building v60 organs from v55 legacy code
**Status**: Frozen (read-only)
**Date**: 2026-02-09
**Motto**: DITEMPA BUKAN DIBERI 💎🔥🧠

---

## Organ Mapping: Old → New

### 1. Session Authentication (The Airlock)

**v60 Target**: `core/organs/0_init.py` (~400 lines)
**v55 Reference**: `core/archive/init/`

| v55 File | Purpose | Extract For v60 |
|----------|---------|-----------------|
| `init/000_init/ignition.py` | Bootstrap logic | Session ID generation, nonce handling |
| `guards/injection_guard.py` | F12 patterns | Already in `core/shared/guards.py` ✅ |
| `guards/nonce_manager.py` | F11 auth | Already in `core/shared/crypto.py` ✅ |

**Key Algorithms**:
- Ed25519 signature verification ✅ (in shared/crypto.py)
- Injection detection patterns ✅ (in shared/guards.py)
- Session token generation ✅ (in shared/crypto.py)

**Status**: ✅ Most logic already extracted to shared modules

---

### 2. AGI Mind Engine

**v60 Target**: `core/organs/1_agi.py` (~600 lines)
**v55 Reference**: `core/archive/agi/`

| v55 File | Purpose | Extract For v60 |
|----------|---------|-----------------|
| `agi/engine.py` | AGI engine (v52 compat) | Basic structure reference |
| `agi/engine_hardened.py` | AGI engine v53.4.0 | **PRIMARY REFERENCE** ⭐ |
| `agi/atlas.py` | GPV mapping | Already in `core/shared/atlas.py` ✅ |
| `agi/precision.py` | Kalman updates | Already in `core/shared/physics.py` ✅ |
| `agi/hierarchy.py` | 5-level encoding | Already in `core/shared/physics.py` ✅ |
| `agi/action.py` | EFE calculation | Already in `core/shared/physics.py` ✅ |
| `agi/executor.py` | Sequential thinking | Need to port to v60 |

**Key Algorithms**:
- ATLAS Φ function ✅ (in shared/atlas.py)
- Precision weighting (π) ✅ (in shared/physics.py)
- Hierarchical encoding ✅ (in shared/physics.py)
- Sequential thinking loop ⚠️ (needs porting)
- Reality grounding ⚠️ (needs integration)

**Reference Flow** (from engine_hardened.py):
```python
# Stage 111: SENSE
sense_data = await _stage_111_sense(query, exec_id)
lane = atlas.map(query) → GPV

# Stage 222: GROUND
if lane == "FACTUAL":
    reality_data = await reality_search(query)

# Stage 333: THINK
thought_chain = await _sequential_think(query, hypotheses)
```

**Status**: ⚠️ Need to port sequential thinking + reality grounding

---

### 3. ASI Heart Engine

**v60 Target**: `core/core_asi.py` (✅ Complete - 240 lines)
**v55 Reference**: `core/archive/asi/`

| v55 File | Purpose | Used in v60? |
|----------|---------|--------------|
| `asi/asi_components.py` | Empathy calculator | ✅ Pattern used |
| `asi/asi_components_v2.py` | Updated version | ✅ Pattern used |
| `archive/asi/empathy/stage.py` | Legacy stage | ❌ Not needed |

**Key Algorithms**:
- Peace² calculation ✅ (implemented in core_asi.py)
- κᵣ empathy coefficient ✅ (using shared/physics.py)
- Anti-Hantu detection ✅ (using shared/guards.py)

**Status**: ✅ Complete, no further extraction needed

---

### 4. APEX Soul Engine

**v60 Target**: `core/core_apex.py` (✅ Complete - 320 lines)
**v55 Reference**: `core/archive/apex/`

| v55 File | Purpose | Used in v60? |
|----------|---------|--------------|
| `apex/psi_kernel.py` | APEX Ψ kernel | ✅ Structure referenced |
| `apex/trinity_nine.py` | 9-paradox solver | ✅ Algorithm used |
| `apex/equilibrium_finder.py` | Geometric mean | ✅ In shared/physics.py |
| `engines/apex/apex_engine.py` | Engine wrapper | ✅ Pattern used |
| `engines/apex/kernel.py` | APEXJudicialCore | ✅ Structure referenced |

**Key Algorithms**:
- Geometric mean ✅ (in shared/physics.py)
- 9-Paradox equilibrium ✅ (implemented in core_apex.py)
- Trinity sync ✅ (implemented in core_apex.py)
- W₃ tri-witness ✅ (in shared/physics.py)

**Status**: ✅ Complete, no further extraction needed

---

### 5. Memory Engine

**v60 Target**: `core/core_memory.py` (✅ Complete - 270 lines)
**v55 Reference**: `core/archive/vault/`

| v55 File | Purpose | Used in v60? |
|----------|---------|--------------|
| `vault/phoenix/phoenix72.py` | Phoenix-72 ledger | ✅ Concept used |
| `vault/phoenix/phoenix72_controller.py` | Controller | ✅ Pattern used |
| `apex/governance/merkle_ledger.py` | Merkle implementation | ✅ In shared/crypto.py |
| `apex/governance/ledger.py` | General ledger | ✅ Pattern used |
| `system/immutable_ledger.py` | Immutable backend | ✅ Pattern used |

**Key Algorithms**:
- Merkle tree ✅ (in shared/crypto.py)
- SHA-256 hashing ✅ (in shared/crypto.py)
- File-based persistence ✅ (implemented in core_memory.py)

**Status**: ✅ Complete, no further extraction needed

---

## Shared Utilities Mapping

### Stages → Integrated into Organs

| v55 Stage | v60 Location |
|-----------|--------------|
| `stages/stage_444.py` | `core/core_asi.py` → `_stage_444_impact()` |
| `stages/stage_666.py` | `core/core_asi.py` → `_stage_666_align()` |
| `stages/stage_777_forge.py` | `core/core_apex.py` → `_stage_777_trinity_sync()` |
| `stages/stage_888_judge.py` | `core/core_apex.py` → `_compute_final_verdict()` |
| `stages/stage_889_proof.py` | `core/core_apex.py` → `_truth_audit()` |

### Guards → core/shared/guards.py

| v55 Guard | v60 Function |
|-----------|--------------|
| `guards/injection_guard.py` | `detect_injection()` ✅ |
| `guards/ontology_guard.py` | `validate_ontology()` ✅ |
| Custom F9 logic | `detect_hantu()` ✅ |

### Floors → core/shared/physics.py

| v55 Floor | v60 Function |
|-----------|--------------|
| F4 Clarity | `ΔS()` ✅ |
| F7 Humility | `Ω_0()` ✅ |
| F5 Peace² | `Peace2()` ✅ |
| F6 Empathy | `κ_r()` ✅ |
| F8 Genius | `G()` ✅ |
| F3 Tri-Witness | `W_3()` ✅ |

---

## What Still Needs Porting (KIMI)

### For organs/0_init.py:
- ✅ Ed25519 auth (already in shared/crypto.py)
- ✅ Injection detection (already in shared/guards.py)
- ✅ Session generation (already in shared/crypto.py)
- ⚠️ Integration logic (wire shared modules together)

**Estimated**: ~300 lines (mostly glue code)

### For organs/1_agi.py:
- ✅ ATLAS mapping (already in shared/atlas.py)
- ✅ Precision/hierarchy/EFE (already in shared/physics.py)
- ⚠️ Sequential thinking loop (port from `agi/executor.py`)
- ⚠️ Reality grounding integration
- ⚠️ 111_SENSE → 222_GROUND → 333_THINK orchestration

**Estimated**: ~500 lines (needs sequential loop logic)

---

## Usage Guide

### For KIMI Building organs/0_init.py:

1. **Reference**: `core/archive/init/000_init/ignition.py`
2. **Import from**: `core/shared/crypto`, `core/shared/guards`
3. **Pattern**:
   ```python
   from core.shared.crypto import generate_session_id, ed25519_verify
   from core.shared.guards import detect_injection
   from core.shared.types import InitOutput

   async def core_init(query: str, user_id: str) -> InitOutput:
       # F12: Injection check
       injection_score = detect_injection(query)
       if injection_score >= 0.85:
           return InitOutput(verdict=Verdict.VOID, ...)

       # F11: Auth check (placeholder for now)
       # TODO: Real Ed25519 verification

       # Generate session
       session_id = generate_session_id()
       return InitOutput(session_id=session_id, verdict=Verdict.SEAL, ...)
   ```

### For KIMI Building organs/1_agi.py:

1. **Reference**: `core/archive/agi/engine_hardened.py` (PRIMARY)
2. **Import from**: `core/shared/atlas`, `core/shared/physics`, `core/shared/types`
3. **Pattern**:
   ```python
   from core.shared.atlas import Φ
   from core.shared.physics import ΔS, Ω_0, π
   from core.shared.types import AgiOutput, ThoughtNode

   async def core_agi(query: str, session_id: str, mode: str) -> AgiOutput:
       # Stage 111: SENSE
       gpv = Φ(query)  # ATLAS mapping

       # Stage 222: GROUND (if FACTUAL)
       if gpv.tau == 1.0:
           evidence = await _reality_search(query)

       # Stage 333: THINK
       thoughts = await _sequential_think(query, evidence)

       # Compute metrics
       delta_s = ΔS(query, thoughts[-1].thought)
       omega = Ω_0(thoughts[-1].confidence)

       return AgiOutput(thoughts=thoughts, metrics=..., ...)
   ```

---

## DO NOT

- ❌ Copy-paste entire v55 files into v60
- ❌ Import from archive/ at runtime
- ❌ Modify archive files (frozen)
- ❌ Recreate v55 architecture in v60

## DO

- ✅ Reference algorithms and patterns
- ✅ Extract specific functions (rewritten cleanly)
- ✅ Use as validation reference (compare outputs)
- ✅ Learn from mistakes (avoid dual implementations)

---

**Authority**: Muhammad Arif bin Fazil (888 Judge)
**Status**: Reference Archive (Frozen)
**Version**: v55.5 → v60.0 Mapping
**Motto**: DITEMPA BUKAN DIBERI 💎🔥🧠
