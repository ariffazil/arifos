# L5_AGENTS

This layer is strictly the **5-role hypervisor layer** sitting under the arifOS constitution. It is organized into 3 non-overlapping planes. 

## 1. Planes & One-Way Architecture
```
ROLE (md)  ─┐
            ├──> POWER (py)  ───> runtime
ENV (json) ─┘
```
1. **ROLE (`ROLE/`)**: Human-readable intent and constraints. Job descriptions, virtues, scars. 
2. **CONTRACT / ENV (`CONTRACT/`)**: Machine-readable tuning dials. Thresholds, permissions, risk ratings.
3. **POWER (`POWER/`)**: The physical execution. The only layer that interacts with tools, reality, or the file system. Enforces gates, roles, and vault writes. 

*Rules:*
- POWER reads CONTRACT
- POWER strictly ignores ROLE (md is for humans)
- CONTRACT never executes logic. 
- All external actions must be initiated by POWER. 

## 2. The 5 Agents
The 5 roles enforce a "mini constitutional parliament", each guarding against specific failure modes and exhibiting unique emergent characteristics.

- **A‑ARCHITECT**: Asks "Should this exist?". Designs options, enforces constraints, but never touches code / reality. Emergent behavior is cautious and design-heavy.
- **A‑ENGINEER**: Asks "Can we make it work?". Writes code, modifies systems. Execution-biased, but forced to respect the Vault and HOLD patterns.
- **A‑AUDITOR**: Asks "What could break / be abused?". Reads logs, assumes breach. Raises objections without creating new designs.
- **A‑VALIDATOR**: Scientific truth verifier. Epistemic intelligence ensuring evidence matches claims. 
- **A‑ORCHESTRATOR**: The disciplined conductor routing tasks in the strict sequence (Architect -> Engineer -> Auditor -> Validator), enforcing gates and no-bypass constraints.

## 3. No-Bypass Rules
- Auditor without `SEAL` forces Orchestrator `HALT`
- Validator will not `SEAL` while there are open objections
- Irreversible changes without `HOLD` mandate `VOID` 
