# L3_WORKFLOW — Documented Sequences (v55.5-HARDENED)

**Level 3 | 70% Coverage | Medium Complexity**

> *"Workflows are compositions of actions — multi-step recipes with state persistence."*

---

## 🎯 Purpose

L3_WORKFLOW combines atomic **Actions** (from L2) into **multi-step sequences** that implement the full arifOS Metabolic Loop. Each workflow spans one or more stages of the 000→999 cycle.

---

## 📈 Effectiveness Spectrum

```
Coverage:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░ 70%
Cost:      $1.00-2.00 per workflow
Setup:     15 minutes
Autonomy:  Medium (human triggers, AI sequences)
```

---

## 📁 Directory Structure (v55.5-HARDENED)

```
L3_WORKFLOW/
├── README.md                    # This file
│
└── WORKFLOWS/                   # 🔥 6 CANONICAL WORKFLOWS
    ├── 000_SESSION_INIT.md      # Ignition (init_gate)
    ├── 111_INTENT.md            # Sense (anchor)
    ├── 333_CONTEXT.md           # Think + Atlas (reason, integrate)
    ├── 555_SAFETY.md            # Empathy + Align (validate, align)
    ├── 777_IMPLEMENT.md         # Forge (forge, respond)
    └── 888_COMMIT.md            # Judge + Seal (audit, seal)
```

---

## 🔄 The Metabolic Loop (6 Workflows)

| # | Workflow | Stage | Actions Used (L2) | Trinity |
|---|----------|-------|-------------------|---------|
| 1 | **000_SESSION_INIT** | `000` | `init_gate` | Gate |
| 2 | **111_INTENT** | `111` | `anchor` | Δ Mind |
| 3 | **333_CONTEXT** | `222-333` | `reason`, `integrate` | Δ Mind |
| 4 | **555_SAFETY** | `444-666` | `respond`, `validate`, `align` | Ω Heart |
| 5 | **777_IMPLEMENT** | `777` | `forge` | Δ Mind |
| 6 | **888_COMMIT** | `888-999` | `audit`, `seal` | Ψ Soul |

### Workflow Flow

```
000_SESSION_INIT → 111_INTENT → 333_CONTEXT → 555_SAFETY → 777_IMPLEMENT → 888_COMMIT
       ↓                                                                        ↓
       └────────────────────── Strange Loop (999→000) ──────────────────────────┘
```

---

## 🔗 Relationship to Actions (L2)

Workflows **compose** atomic Actions:

| Abstraction | Layer | Example | Scope |
|-------------|-------|---------|-------|
| **Action** | L2 | `anchor` | Single stage operation |
| **Workflow** | L3 | `333_CONTEXT` | Multi-stage sequence |
| **Agent** | L5 | `ASI_Guardian` | Full autonomy |

```
Workflow = Action₁ + Action₂ + ... + Actionₙ + State Management
```

---

## 📋 Workflow Anatomy

Each workflow file follows this structure:

```markdown
# Workflow: [STAGE]_[NAME]

**Stage:** [Number] ([Name])
**Purpose:** [Description]
**Trigger:** [When to use]
**Output:** [What it produces]

---

## When to Use
[Conditions for invocation]

## Workflow Steps
### Step 1: [Name]
[Details]

### Step 2: [Name]
[Details]
...

## Output Specification
[YAML/JSON schema]

## Constitutional Compliance
| Floor | Verification | Status |
[Table of floors checked]

## Next Stage
[What workflow follows this one]

---
**DITEMPA BUKAN DIBERI**
```

---

## 🛡️ Constitutional Floors Per Workflow

| Workflow | Primary Floors | Enforcement |
|----------|----------------|-------------|
| **000_SESSION_INIT** | F11, F12, F13 | Authority, Injection, Sovereign |
| **111_INTENT** | F4, F12 | Clarity, Injection |
| **333_CONTEXT** | F2, F4, F7 | Truth, Clarity, Humility |
| **555_SAFETY** | F5, F6, F9 | Peace, Empathy, Anti-Hantu |
| **777_IMPLEMENT** | F1, F4, F8 | Amanah, Clarity, Genius |
| **888_COMMIT** | ALL F1-F13 | Full constitutional check |

---

## 🔧 Platform Integration

These workflows are **model-agnostic**. Platform-specific bindings:

| Platform | Integration |
|----------|-------------|
| **Gemini/Antigravity** | `.agent/workflows/` references these |
| **Claude** | Import directly or use MCP tools |
| **ChatGPT** | Use via MCP HTTP transport |

---

## 🚀 Deployment History

### v53.x — Platform-Specific (Archived)
- Workflows in `.claude/workflows/` only
- No Gemini integration
- Platform-locked

### v55.5-HARDENED — Current ✅
- **Unified to `L3_WORKFLOW/WORKFLOWS/`**
- Model-agnostic canonical location
- Cross-references to L2 Actions
- All 6 metabolic workflows present

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v55.5-HARDENED  
**Last Updated:** 2026-02-06  
**Creed:** DITEMPA BUKAN DIBERI

---

## ✅ Reality Check

| Component | Status | Evidence |
|-----------|--------|----------|
| 000_SESSION_INIT | ✅ Complete | 163 lines |
| 111_INTENT | ✅ Complete | 5KB |
| 333_CONTEXT | ✅ Complete | 6KB |
| 555_SAFETY | ✅ Complete | 7KB |
| 777_IMPLEMENT | ✅ Complete | 6KB |
| 888_COMMIT | ✅ Complete | 323 lines |
| **Coverage** | **70%** | **As designed** |

> This layer is **production-ready** for workflow-based orchestration.

---

## 🔗 Related Documents

- [../L2_SKILLS/ACTIONS/](../L2_SKILLS/ACTIONS/) — The 11 Canonical Actions
- [../L4_TOOLS/](../L4_TOOLS/) — MCP Tool bindings
- [../../.agent/workflows/](../../.agent/workflows/) — Gemini-specific workflows
