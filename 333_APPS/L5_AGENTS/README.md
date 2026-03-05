# L5_AGENTS — The 5-Role Constitutional Hypervisor (v60.1-ARIF)

> *"Emergence is no longer random; it is patterned into 5 disciplined civil servants sitting under the constitution."*

Level 5 | 7-Organ Sovereign Stack | High Complexity | Governance

---

## 🎯 Purpose

**L5_AGENTS** is strictly the **5-role hypervisor layer** sitting under the arifOS constitution. This layer completely isolates constitutional intelligence across five distinct officers, deliberately injecting friction to eradicate single points of failure.

It does **not** contain independent environmental physics, arbitrary knowledge (theory), or unmapped tools. L5 only routes the 000-999 metabolic loops into structured, accountable responsibilities.

---

## 🏛️ The Constitutional Parliament (ARIF Mapping)

Each role is bound to specific ARIF cognitive bands to ensure clear separation of concerns:

| Agent | Symbol | ARIF Bands | Primary Responsibility |
|:---:|:---:|:---:|:---|
| **A‑ORCHESTRATOR** | 🎛️ | **A** | Conductor: Drives Band A ignition & sequences R/I/F. |
| **A‑ARCHITECT** | Δ | **R + I** | Designer: Blueprints plans (Reflect) & Maps Context (Integrate). |
| **A‑AUDITOR** | 👁 | **R + I** | Reviewer: Red-Teams logic (Reflect) & Audits Law (Integrate). |
| **A‑ENGINEER** | Ω | **R + F** | Builder: Implements via Forge; never seals directly. |
| **A‑VALIDATOR** | Ψ | **F Apex** | Judge: Final verdict renderer (Apex) & Vault sealer (Seal). |

---

## 🧬 Architecture: 3 Planes of Enforcement

L5 enforces lowest entropy by dividing all structure into **Three One-Way Planes**:

```text
ROLE (md)  ─┐
            ├──> POWER (py)  ───> runtime
ENV (json) ─┘
```

1. **ROLE (`ROLE/`)**: Human-readable intent and constraints. Job descriptions, virtues, scars.
2. **CONTRACT / ENV (`CONTRACT/`)**: Machine-readable tuning dials. Thresholds, permissions, risk ratings.
3. **POWER (`POWER/`)**: The physical execution. The only layer that interacts with tools, reality, or the file system.

*Rules:*
- **POWER may read CONTRACT**, but **never reads ROLE md**.
- **ROLE never contains numbers/thresholds/tool names**.
- **CONTRACT never contains executable code** (schema-validated).
- **Only POWER can touch reality** (MCP/tools/fs/net/vault).

---

## 📂 Canonical Directory Structure

```text
L5_AGENTS/
├── README.md               # This index
├── ROLE/                   # The Human Meaning (Markdown)
│   ├── A-ARCHITECT.md      ├── A-ENGINEER.md       ├── A-AUDITOR.md        
│   ├── A-VALIDATOR.md      ├── A-ORCHESTRATOR.md   
│   └── FLOORS.md           # The Constitution's human translation
│
├── CONTRACT/               # The Machine Dials (JSON)
│   ├── role_profiles.json  ├── env.dev.json        ├── env.prod.json
│   └── schemas/            # JSON Schemas
│
└── POWER/                  # The Execution Machinery (Python)
    ├── orchestrator.py     ├── base_agent.py       
    ├── roles/              # architect.py, engineer.py, etc.
    ├── enforcement/        # gates.py, policy.py, preflight.py
    └── io/                 # tools.py, vault.py
```

---

## 💼 Connecting L5 to External CLIs (OpenCode)

External CLIs (such as Cursor or **OpenCode**) never access the `POWER` plane directly. They strictly project the roles using simple constraints mapping to the internal constitution.

---

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v60.1-FORGE-ARIF  
**Architecture:** 7-Organ Stack `[A-R-I-F]`  
**Status:** SEALED  
**Creed:** DITEMPA BUKAN DIBERI

