# 333_APPS — ATLAS MAP for Internal Navigation

> **Agent Navigation Protocol | Constitutional Stack Topology**  
> **Version:** v55.5-HARDENED  
> **Updated:** 2026-02-10

---

## 🧭 ATLAS Overview

This ATLAS is the **internal navigation map** for agents operating within the arifOS ecosystem. It maps the high-level application layers to the low-level kernel implementation.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT POSITIONING                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  YOU ARE HERE → 333_APPS/ (7-Layer Application Stack)                   │
│                                                                         │
│  The Kernel runs on: core/ (Canonical Hardened Implementation)           │
│                                                                         │
│  The Constitution lives in: 000_LAW.md (The 13 Floors)                   │
│                                                                         │
│  The Memory persists in: vault_999/ (Immutable Ledger)                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ The 4-Layer Mapping Matrix

### How 333_APPS Layers Map to 000-999 Stages

```
333_APPS Layer          000-999 Stage          Kernel Organ
─────────────────────────────────────────────────────────────
L1_PROMPT               000_INIT               _0_init.py (Gate)
                        111_SENSE              

L2_SKILLS               222_THINK              _1_agi.py (Mind)

L3_WORKFLOW             333_ATLAS              _1_agi.py (Mind)
                        444_EVIDENCE           _3_apex.py (Trinity)

L4_TOOLS                555_EMPATHY            _2_asi.py (Heart)
                        666_ALIGN              _2_asi.py (Heart)
                        
(Experimental)
L5_AGENTS               777_FORGE              _3_apex.py (Soul)

L6-L7                   888_JUDGE → 999_SEAL   _3_apex.py + _4_vault.py
```

---

## 🎭 Agent-Specific Navigation (v55.5 Hardened)

### For ARCHITECT (Δ) — Stages 111-333
**Domain:** L1_PROMPT → L2_SKILLS → L3_WORKFLOW
**Kernel Core:** `core/organs/_1_agi.py`
**Physics:** `core/shared/physics.py`

### For ENGINEER (Ω) — Stages 555-777
**Domain:** L4_TOOLS → L5_AGENTS
**Kernel Core:** `core/organs/_2_asi.py`
**Physics:** `core/shared/physics.py`

### For VALIDATOR (Ψ) — Stages 888-999
**Domain:** L6_INSTITUTION → L7_AGI
**Kernel Core:** `core/organs/_3_apex.py` + `core/organs/_4_vault.py`
**Ledger:** `vault_999/`

---

## 📂 Repository Topology Map

### Canonical Hardened Kernel (core/)
```
core/
├── organs/                 # The 5 Vital Organs
│   ├── _0_init.py          # Stage 000 — 🔐 Gatekeeper
│   ├── _1_agi.py           # Stage 111-333 — 🧠 Mind
│   ├── _2_asi.py           # Stage 555-666 — ❤️ Heart
│   ├── _3_apex.py          # Stage 444, 777-888 — ⚖️ Soul
│   └── _4_vault.py         # Stage 999 — 🔒 Memory
└── shared/                 # Common Substrate
    ├── physics.py          # Thermodynamics & Metrics
    └── types.py            # Pydantic Contracts
```

### Application Stack (333_APPS/)
```
333_APPS/
├── L1_PROMPT/              # System Instructions
├── L2_SKILLS/              # Functional Templates
│   └── ACTIONS/            # Canonical Skillset
├── L3_WORKFLOW/            # Documented Sequences
└── L4_TOOLS/               # MCP Tool Documentation
```

---

## 🔄 The Metabolic Loop Integration

The transition from `v55` to `v55.5-HARDENED` involves moving implementation logic from the application folders into the **5-Organ Kernel** (`core/`). 

1.  **Request** enters via **L1_PROMPT**.
2.  **Logic** is executed by **L2_SKILLS** pointing to `core/organs/_1_agi.py`.
3.  **Safety** is verified by **L4_TOOLS** pointing to `core/organs/_2_asi.py`.
4.  **Verdict** is sealed into **vault_999/** by `core/organs/_4_vault.py`.

---

**DITEMPA BUKAN DIBERI**
