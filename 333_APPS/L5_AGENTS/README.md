# L5_AGENTS — The 5-Role Constitutional Hypervisor

> *"Emergence is no longer random; it is patterned into 5 disciplined civil servants sitting under the constitution."*

**Level 5 | 7-Organ Sovereign Stack | High Complexity | Governance**

---

## 🎯 Purpose

**L5_AGENTS** is strictly the **5-role hypervisor layer** sitting under the arifOS constitution. This layer completely isolates constitutional intelligence across five distinct officers, deliberately injecting friction to eradicate single points of failure. 

It does **not** contain independent environmental physics, arbitrary knowledge (theory), or unmapped tools. L5 only routes the 000-999 metabolic loops into structured, accountable responsibilities.

---

## 🧬 Architecture: 3 Planes of Enforcement

L5 enforces lowest entropy by dividing all structure into **Three One-Way Planes**:

```
ROLE (md)  ─┐
            ├──> POWER (py)  ───> runtime
ENV (json) ─┘
```
1. **ROLE (`ROLE/`)**: Human-readable intent and constraints. Job descriptions, virtues, scars. 
2. **CONTRACT / ENV (`CONTRACT/`)**: Machine-readable tuning dials. Thresholds, permissions, risk ratings.
3. **POWER (`POWER/`)**: The physical execution. The only layer that interacts with tools, reality, or the file system. Enforces gates, roles, and vault writes. 

*Rules:*
- **POWER may read CONTRACT**, but **never reads ROLE md**.
- **ROLE never contains numbers/thresholds/tool names**.
- **CONTRACT never contains executable code** (schema-validated).
- **Only POWER can touch reality** (MCP/tools/fs/net/vault).

---

## 🏛️ The 5 Agents (The Constitutional Parliament)

The 5 roles enforce emergence natively aligned with the **7-Organ Sovereign Stack**:

| Agent | Symbol | Emergence Focus | No-Bypass Brakes |
|:---:|:---:|:---|:---|
| **A‑ARCHITECT** | Δ | Design & Plan | Cannot execute code or edit reality |
| **A‑ENGINEER** | Ω | Build & Implement | Must respect `888_HOLD` and Vault gates |
| **A‑AUDITOR** | 👁 | Review & Red-Team | Assumes breach, blocks irreversible actions |
| **A‑VALIDATOR** | Ψ | Truth & Evidence | Cannot `SEAL` without zero open objections |
| **A‑ORCHESTRATOR** | 🎛️ | Flow & Conductor | Cannot proceed without consensus gates passed |

### Emergence Under Load
Under stress (incidents, ambiguous tasks), instead of emergent chaos, the system yields **emergent negotiation**.
- Architect slows scope
- Engineer proposes safe patches
- Auditor yanks the brake
- Validator won’t certify
- Orchestrator routes to `HOLD`.

---

## 📂 Canonical Directory Structure

```
L5_AGENTS/
├── README.md               # This thin index
├── AAA_MCP_L5_EUREKA_PLAN.md # L5 Runbook notes
│
├── SPEC/ROLE/              # The Human Meaning (Markdown)
│   ├── A-ARCHITECT.md      
│   ├── A-ENGINEER.md       
│   ├── A-AUDITOR.md        
│   ├── A-VALIDATOR.md      
│   ├── A-ORCHESTRATOR.md   
│   ├── FLOORS.md           # The Constitution's human translation
│   └── GLOSSARY.md         # Terms mapping (SABAR, VOID, OP-CODE)
│
├── SPEC/CONTRACT/          # The Machine Dials (JSON)
│   ├── role_profiles.schema.json
│   ├── role_profiles.json
│   ├── env.schema.json
│   └── env.*.json          # Dev/Prod thresholds mapping F3/F12 logic
│
└── power/                  # The Execution Machinery (Python)
    ├── __init__.py         
    ├── base_agent.py       
    ├── orchestrator.py     
    ├── roles/              # Agent logic mappings
    │   ├── architect.py    
    │   ├── engineer.py     
    │   ├── auditor.py      
    │   └── validator.py    
    ├── enforcement/        # Brakes
    │   ├── preflight.py    
    │   ├── gates.py        
    │   └── policy.py       
    └── io/                 # Reality contact 
        ├── vault.py        
        └── tools.py        
```

---

## 💼 Connecting L5 to External CLIs (OpenCode)

External CLIs (such as Cursor or **OpenCode**) never access the `power` plane directly. They strictly project the roles using simple constraints mapping to the internal constitution. 

*(e.g., OpenCode dynamically loads the markdown prompts without loading any Python environment, while tool calls route downwards into the MCP protocol enforcing `preflight` and `gates` before execution).*

---

## 👑 Authority & Status

**Sovereign:** Muhammad Arif bin Fazil
**Version:** 2026.02.28 (FORGE-777 Milestone)
**Architecture:** 7-Organ Stack `[INIT, AGI, PHOENIX, ASI, FORGE, APEX, VAULT]`
**Status:** SEALED
**Creed:** DITEMPA BUKAN DIBERI
