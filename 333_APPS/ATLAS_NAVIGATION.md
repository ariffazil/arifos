# 333_APPS — ATLAS MAP for Internal Navigation

> **Agent Navigation Protocol | Constitutional Stack Topology**  
> **Version:** v64.1.1-GAGI  
> **Updated:** 2026-02-14

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

### How 333_APPS Layers Map to 000-999 Stages (9 A-CLIP Tools)

```
333_APPS Layer          000-999 Stage          Tool (A-CLIP)          Kernel Organ
───────────────────────────────────────────────────────────────────────────────────
L1_PROMPT               000_INIT               anchor                 _0_init.py (Gate)

L2_SKILLS               222_REASON             reason                 _1_agi.py (Mind)
L2_SKILLS               333_INTEGRATE          integrate              _1_agi.py (Mind)
L2_SKILLS               444_RESPOND            respond                _1_agi.py (Mind)

L3_WORKFLOW             555_VALIDATE           validate               _2_asi.py (Heart)
L3_WORKFLOW             666_ALIGN              align                  _2_asi.py (Heart)
L3_WORKFLOW             777_FORGE              forge                  _2_asi.py (Heart)

L4_TOOLS                888_AUDIT              audit                  _3_apex.py (Soul)
L4_TOOLS                999_SEAL               seal                   _4_vault.py (Memory)

(Experimental)
L5_AGENTS               Multi-Agent Federation —                        _3_apex.py (Soul)

L6-L7                   Institution → AGI      —                        _3_apex.py + _4_vault.py
```

**Container Tools (VPS Operations):**
- `container_list`, `container_restart`, `container_logs`
- `sovereign_health`, `container_exec`
- Located in: `aaa_mcp/integrations/`

---

## 🎭 Agent-Specific Navigation (v64.1.1 GAGI)

### For ARCHITECT (Δ) — Stages 000-444
**Domain:** L1_PROMPT → L2_SKILLS → L3_WORKFLOW
**Tools:** `anchor` → `reason` → `integrate` → `respond`
**Kernel Core:** `core/organs/_1_agi.py`
**Physics:** `core/shared/physics.py`

### For ENGINEER (Ω) — Stages 555-777
**Domain:** L4_TOOLS → L5_AGENTS
**Tools:** `validate` → `align` → `forge`
**Kernel Core:** `core/organs/_2_asi.py`
**Physics:** `core/shared/physics.py`

### For VALIDATOR (Ψ) — Stages 888-999
**Domain:** L6_INSTITUTION → L7_AGI
**Tools:** `audit` → `seal`
**Kernel Core:** `core/organs/_3_apex.py` + `core/organs/_4_vault.py`
**Ledger:** `vault_999/`

### For OPERATOR — Container Tools
**Domain:** VPS Infrastructure Management
**Tools:** `container_list`, `container_restart`, `container_logs`, `sovereign_health`, `container_exec`
**Location:** `aaa_mcp/integrations/container_controller.py`

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
│   └── ACTIONS/            # 9 A-CLIP Canonical Skills
│       ├── anchor/         # 000_INIT
│       ├── reason/         # 222_REASON
│       ├── integrate/      # 333_INTEGRATE
│       ├── respond/        # 444_RESPOND
│       ├── validate/       # 555_VALIDATE
│       ├── align/          # 666_ALIGN
│       ├── forge/          # 777_FORGE
│       ├── audit/          # 888_AUDIT
│       └── seal/           # 999_SEAL
├── L3_WORKFLOW/            # Documented Sequences
├── L4_TOOLS/               # MCP Tool Documentation
└── L5-L7/                  # Experimental (Pilots)
```

---

## 🔄 The Metabolic Loop Integration

The transition from `v55` to `v64.1.1-GAGI` involves moving implementation logic from the application folders into the **5-Organ Kernel** (`core/`). 

1.  **Request** enters via **L1_PROMPT** (`anchor`).
2.  **Logic** is executed by **L2_SKILLS** via 9 A-CLIP tools (`reason`, `integrate`, `respond`).
3.  **Safety** is verified by **L3_WORKFLOW** tools (`validate`, `align`, `forge`).
4.  **Verdict** is issued by **L4_TOOLS** (`audit`) and sealed into **vault_999/** by `seal`.

**Performance Optimizations (v64.1.1):**
- Config caching: 13,725x faster
- Container caching: 16,022x faster
- Constants centralized in `aaa_mcp/config/constants.py`

---

## Version History

**v64.1.1-GAGI (2026-02-14):**
- Updated 9 A-CLIP tool names (anchor, reason, integrate, respond, validate, align, forge, audit, seal)
- Added Container Tools to navigation
- Performance improvements documented
- Aligned with `aaa_mcp/server.py` implementation

**v55.5-HARDENED (Legacy):**
- Original 5-tool model (init_session, agi_cognition, etc.)

---

**DITEMPA BUKAN DIBERI**
