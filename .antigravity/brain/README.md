# Brain (Working Memory)

**Location:** `.antigravity/brain/`  
**Purpose:** Working memory workspace for all agents  
**Constraint:** All transient working files, scratchpads, and draft outputs

---

## Purpose

- **Drafting:** Intermediate steps before sealing
- **Reasoning:** Complex thought chains
- **State:** Session-specific context preservation
- **Scratchpad:** Temporary calculations and notes

---

## Subdirectories

```
brain/
├── drafts/           # Work in progress
├── scratchpads/      # Temporary calculations
├── states/           # Session state preservation
└── templates/        # Reusable templates
    ├── delta_bundle.json
    ├── omega_bundle.json
    └── seal_entry.json
```

---

## Usage

Agents may write to `brain/` freely during operation.
All content in `brain/` is:
- **Transient** — May be cleaned periodically
- **Local** — Not committed to git
- **Private** — Agent-specific working space

**Important:** Final outputs must be sealed via `vault_seal`, not left in `brain/`.

---

**DITEMPA BUKAN DIBERI**
