# L2_SKILLS/UTILITIES — Auxiliary Skills

**Level 2 | Utility Functions | Model-Agnostic**

> *"Tools that serve the 9 Canonical Actions — auxiliary, not core."*

---

## 🎯 Purpose

UTILITIES contains **auxiliary skills** that support the 9 canonical arifOS actions but are not part of the core metabolic loop. These are helper functions, visual systems, and operational tools.

---

## 📁 Utility Skills

| Skill | Purpose | Primary Use |
|-------|---------|-------------|
| **visual-law** | v55.5 Trinity visual design system | Site theming & UI components |
| **capture-terminal** | Terminal output capture & logging | Debug traces & audit logs |
| **route-tasks** | Task routing by constitutional policy | Workflow orchestration |

---

## 🎨 visual-law (v55.5)

The Trinity visual design system with unified color palette:

| Site | Color | Hex | Symbol |
|------|-------|-----|--------|
| **HUMAN** | Crimson | `#FF2D2D` | Body |
| **THEORY** | Gold | `#FFD700` | Soul |
| **APPS** | Cyan | `#06B6D4` | Mind |

**Contains:**
- HTML templates (`assets/`)
- Color token references
- TrinityLogo SVG components
- WCAG AA compliant contrasts

---

## 📺 capture-terminal

PowerShell script for capturing terminal output with timestamps.

**Contains:**
- `capture.ps1` — Main capture script
- `scripts/` — Helper utilities

**Usage:**
```powershell
.\capture.ps1 -Command "your-command" -OutputFile "trace.log"
```

---

## 🔀 route-tasks

Policy-based task routing for constitutional workflows.

**Contains:**
- `SKILL.md` — Routing instructions
- `scripts/` — Routing logic

**Usage:**
```bash
/skill route-tasks task="user request" policy="F5-safety"
```

---

## 🔗 Relationship to Core Actions

```
UTILITIES (Auxiliary)                 ACTIONS (Core)
├── visual-law ──────────────────────┬── anchor (111_SENSE)
├── capture-terminal ────────────────┼── reason (222_THINK)
└── route-tasks ─────────────────────┼── integrate (333_ATLAS)
                                     ├── respond (444_EVIDENCE)
                                     ├── validate (555_EMPATHY)
                                     ├── align (666_ALIGN)
                                     ├── forge (777_FORGE)
                                     ├── audit (888_JUDGE)
                                     └── seal (999_SEAL)
```

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v55.5-HARDENED  
**Last Updated:** 2026-02-06  
**Creed:** DITEMPA BUKAN DIBERI

---

## 📚 Related Documents

- [../ACTIONS/README.md](../ACTIONS/README.md) — The 9 Canonical Actions
- [../README.md](../README.md) — L2_SKILLS overview
- [../../STATUS.md](../../STATUS.md) — 333_APPS status tracker
