---
type: Tool
tags: [index, tools, mcp, registry]
epistemic_level: OBS
last_sync: 2026-04-11
---

# Tool Index

> **Type:** Index  
> **Epistemic Level:** OBS  
> **Last Updated:** 2026-04-11  
> **Tags:** [index, tools, mcp, registry]  
> **Version:** 0.6.0 — Phase A + Phase B SEALED

---

## Complete Tool Registry (12 Tools in the Canonical Modular Surface)

This page documents the **canonical modular FastMCP surface** in:

```text
arifos/geox/tools/core.py
        ↓
arifos/geox/tools/adapters/fastmcp_adapter.py
```

The repository still contains other server files with overlapping or smaller tool sets. For merge/refactor work, use [[80_INTEGRATION/GEOX_REPO_STATE_AND_COMPONENT_MAP]] as the repo-state source of truth.

| Tool | Phase | Risk Level | Primary Floors | Status | Page |
|------|-------|-----------|----------------|--------|------|
| **geox_load_seismic_line** | A | GUARDED | F4, F11 | ✅ Active | [[geox_load_seismic_line]] |
| **geox_build_structural_candidates** | A | SAFE | F2, F7, F9 | ✅ Active | [[geox_build_structural_candidates]] |
| **geox_evaluate_prospect** | A | GUARDED | F1, F7, F13 | ✅ Active | [[geox_evaluate_prospect]] |
| **geox_feasibility_check** | A | SAFE | F2, F4 | ✅ Active | [[geox_feasibility_check]] |
| **geox_verify_geospatial** | A | SAFE | F2, F4 | ✅ Active | [[geox_verify_geospatial]] |
| **geox_calculate_saturation** | A | SAFE | F2, F7 | ✅ Active | [[geox_calculate_saturation]] |
| **geox_query_memory** | A | SAFE | F11 | ✅ Active | [[geox_query_memory]] |
| **geox_select_sw_model** | B | SAFE | F2, F4, F9 | ✅ Active | [[geox_select_sw_model]] |
| **geox_compute_petrophysics** | B | GUARDED | F2, F7, F9 | ✅ Active | [[geox_compute_petrophysics]] |
| **geox_validate_cutoffs** | B | GUARDED | F1, F2, F9, F13 | ✅ Active | [[geox_validate_cutoffs]] |
| **geox_petrophysical_hold_check** | B | DANGEROUS | F2, F4, F7, F9 | ✅ Active | [[geox_petrophysical_hold_check]] |
| **geox_health** | — | SAFE | — | ✅ Active | _utility_ |

---

## Phase Summary

| Phase | Tools | Status | Sealed |
|-------|-------|--------|--------|
| **A — Core** | 7 domain tools + geox_health | ✅ Complete | 999_SEAL_PHASE_A |
| **B — Petrophysics** | 4 tools | ✅ Complete | 999_SEAL_PHASE_B_PHYSICS |

---

## Phase B: Petrophysics Pipeline (v0.6.0)

The four Phase B tools form a governed pipeline for well log petrophysical analysis:

```
geox_select_sw_model       — F2/F4/F9: admissibility from log QC flags
        ↓
geox_compute_petrophysics  — F2/F7/F9: full property pipeline (Vsh, φ, Sw, BVW, k)
        ↓
geox_validate_cutoffs      — F1/F2/F9/F13: apply CutoffPolicy → Net Pay verdict
        ↓
geox_petrophysical_hold_check — F2/F4/F7/F9: 888_HOLD on floor violations
```

### Provenance Tags

Every output carries one of:

| Tag | Meaning |
|-----|---------|
| `MEASURED` | Direct sensor reading (RAW) |
| `DERIVED` | Computed from physics model |
| `POLICY` | Cutoff application — judgement call |
| `INTERPRETED` | Integrated inference |

---

## Risk Level Definitions

| Level | Description | Floors | Examples |
|-------|-------------|--------|----------|
| **SAFE** | Read-only, no state mutation | F2, F4 | Query memory, select model |
| **GUARDED** | May suggest irreversible actions | +F1, F13 | Evaluate prospect, compute petro |
| **DANGEROUS** | Triggers 888_HOLD — constitutional veto | +888_HOLD | geox_petrophysical_hold_check |

---

## Floor Coverage

| Floor | Tools Enforcing | Violation Outcome |
|-------|----------------|-------------------|
| F1 Amanah | 3 tools | Blocks writes until PARTIAL or SEAL |
| F2 Truth | All 11 tools | VOID if τ < 0.99 |
| F4 Clarity | 8 tools | Rejects inputs missing units/CRS |
| F7 Humility | 6 tools | Forces uncertainty band on estimates |
| F9 Anti-Hantu | 7 tools | Physical plausibility check on structure claims |
| F11 Authority | 4 tools | Provenance mandatory |
| F13 Sovereign | 3 tools | Human veto hook — prospect + cutoff gates |

---

## Usage Patterns

### Pattern 1: Seismic Interpretation
```
geox_load_seismic_line → geox_build_structural_candidates → geox_evaluate_prospect
```

### Pattern 2: Petrophysical Evaluation (Phase B)
```
geox_select_sw_model → geox_compute_petrophysics → geox_validate_cutoffs → geox_petrophysical_hold_check
```

### Pattern 3: Fast Saturation Estimate
```
geox_calculate_saturation → [888_HOLD if triggered]
```

### Pattern 4: Memory Query
```
geox_query_memory → [synthesis] → geox_evaluate_prospect
```

---

## Architecture (v0.6.0 Modular)

```
arifos/geox/tools/adapters/fastmcp_adapter.py  ← preferred FastMCP transport
    ↓
arifos/geox/tools/core.py                      ← pure async domain functions
    ↓
contracts/types.py                             ← result models
    ↓
services/                                      ← constitutional + petrophysics engines
physics/                                       ← saturation models, porosity solvers

root geox_mcp_server.py                        ← separate root server surface; do not assume
                                                 it is already a thin re-export
```

---

*Tool Index v2.0.0 · Phase A + Phase B SEALED · GEOX v0.6.0*  
*DITEMPA BUKAN DIBERI*
