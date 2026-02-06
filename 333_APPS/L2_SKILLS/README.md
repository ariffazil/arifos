# L2_SKILLS — Parameterized Templates (v55.5-HARDENED)

**Level 2 | 50% Coverage | Low Complexity**

> *"Skills are prompts with parameters — reusable, composable, invocable."*

---

## 🎯 Purpose

L2_SKILLS wraps the constitutional prompts from L1 into **parameterized templates** that can be instantiated with variables, composed into chains, and invoked programmatically.

This layer enables **reusable capabilities** that maintain constitutional governance while adapting to specific contexts.

---

## 📈 Effectiveness Spectrum

```
Coverage:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░ 50%
Cost:      $0.20-0.50 per 1K operations
Setup:     5 minutes
Autonomy:  Very Low (human triggers)
```

---

## 📁 Directory Structure (v55.5-HARDENED)

```
L2_SKILLS/
├── README.md                    # This file
├── DEPLOYMENT.md                # Deployment guide
├── skill_templates.yaml         # YAML skill definitions
├── mcp_tool_templates.py        # Python tool wrappers
│
├── ACTIONS/                     # 🔥 9 CANONICAL ATOMIC ACTIONS
│   ├── README.md                # Actions overview
│   ├── anchor/SKILL.md          # 111_SENSE — Ground reality
│   ├── reason/SKILL.md          # 222_THINK — Logical inference
│   ├── integrate/SKILL.md       # 333_ATLAS — Cross-domain synthesis
│   ├── respond/SKILL.md         # 444_EVIDENCE — Compassionate output
│   ├── validate/SKILL.md        # 555_EMPATHY — Stakeholder impact
│   ├── align/SKILL.md           # 666_ALIGN — Ethical alignment
│   ├── forge/SKILL.md           # 777_FORGE — Reduce entropy
│   ├── audit/SKILL.md           # 888_JUDGE — Constitutional verdict
│   └── seal/SKILL.md            # 999_SEAL — Immutable commitment
│
└── UTILITIES/                   # 🛠️ AUXILIARY SKILLS
    ├── README.md                # Utilities overview
    ├── visual-law/              # v55.5 Trinity design system
    ├── capture-terminal/        # Terminal output capture
    └── route-tasks/             # Policy-based task routing
```

---

## 🔥 The 9 Canonical Actions (Metabolic Loop)

| # | Action | Stage | MCP Tool | Trinity | Primary Floors |
|---|--------|-------|----------|---------|----------------|
| 1 | **anchor** | `111_SENSE` | `agi_sense` | Δ Mind | F4, F7, F12 |
| 2 | **reason** | `222_THINK` | `agi_reason` | Δ Mind | F2, F4, F7 |
| 3 | **integrate** | `333_ATLAS` | `agi_reason` | Δ Mind | F2, F7, F8 |
| 4 | **respond** | `444_EVIDENCE` | `asi_act` | Ω Heart | F4, F5, F6 |
| 5 | **validate** | `555_EMPATHY` | `asi_empathize` | Ω Heart | F1, F5, F6 |
| 6 | **align** | `666_ALIGN` | `asi_align` | Ω Heart | F5, F6, F9 |
| 7 | **forge** | `777_FORGE` | `reality_search` | Δ Mind | F2, F4, F7 |
| 8 | **audit** | `888_JUDGE` | `apex_verdict` | Ψ Soul | ALL F1-F13 |
| 9 | **seal** | `999_SEAL` | `vault_seal` | Ψ Soul | F1, F3, F11 |

### Metabolic Loop Flow

```
000_INIT → anchor → reason → integrate → respond → validate → align → forge → audit → seal → 999
    ↓                                                                                        ↓
    └─────────────────────────────── Strange Loop (Seed for next cycle) ─────────────────────┘
```

---

## 🛠️ Skill Types

### 1. Constitutional Skills (F1-F13)
```yaml
skill:
  name: "f2_truth_verification"
  floor: "F2"
  parameters:
    claim: string
    confidence_threshold: 0.99
  invocation: |
    Verify the following claim against available evidence:
    Claim: {{ claim }}
    Required confidence: {{ confidence_threshold }}
    Apply F2 Truth floor (τ ≥ 0.99)
```

### 2. Task Skills
```yaml
skill:
  name: "code_review"
  category: "engineering"
  parameters:
    code: string
    language: string
  invocation: |
    Review this {{ language }} code for:
    1. F1 Amanah (reversible operations)
    2. F9 Anti-Hantu (no dark patterns)
    3. F4 Clarity (readable code)
```

### 3. Workflow Skills
```yaml
skill:
  name: "000_999_cycle"
  category: "orchestration"
  parameters:
    query: string
    user_token: string
  steps:
    - anchor   # 111_SENSE
    - reason   # 222_THINK
    - integrate # 333_ATLAS
    - respond  # 444_EVIDENCE
    - validate # 555_EMPATHY
    - align    # 666_ALIGN
    - forge    # 777_FORGE
    - audit    # 888_JUDGE
    - seal     # 999_SEAL
```

---

## 🛡️ Constitutional Floors Enforced

| Floor | Enforcement | Mechanism | Status |
|-------|-------------|-----------|--------|
| F1 Amanah | ⚠️ Partial | Template instruction | Available |
| F2 Truth | ⚠️ Partial | Template parameter | Available |
| F3 Tri-Witness | ✅ Active | Via `apex_verdict` (Human+AI+Earth) | **Active** |
| F4 Clarity | ✅ Full | Schema validation | **Active** |
| F5 Peace² | ⚠️ Partial | Template instruction | Available |
| F6 Empathy | ⚠️ Partial | Parameter injection | Available |
| F7 Humility | ✅ Active | Omega_0 interval check | **Active** |
| F8 Genius | ⚠️ Partial | Formula templates | Available |
| F9 Anti-Hantu | ✅ Active | Identity enforcement templates | **Active** |
| F10 Ontology | ✅ Active | Type checking & Entity lock | **Active** |
| F11 Command Auth | ✅ Full | Token validation | **Active** |
| F12 Injection | ✅ Full | Input sanitization | **Active** |
| F13 Sovereign | ✅ Full | Human approval gate | **Active** |

---

## 🚀 Deployment History

### v51.0 — Early Templates (Archived)
- Basic Jinja2 templates
- 5 initial skills
- Manual invocation only

### v52.0 — Standardization (Archived)
- YAML schema defined
- 25+ skills library
- CLI invocation added

### v53.0 — MCP Integration (Archived)
- Python wrappers created
- Tool template system
- Auto-discovery

### v55.5-HARDENED — Current ✅
- **9 Canonical Actions** consolidated in `ACTIONS/`
- **3 Utility Skills** moved to `UTILITIES/`
- Duplicate skills removed from root `skills/` folder
- Full YAML frontmatter on all SKILL.md files
- Gödel Lock verification on all actions
- 50+ skill templates verified

---

## 📊 Use Cases

| Scenario | Skill Type | Example |
|----------|-----------|---------|
| Safety check | Constitutional | `f5_peace_evaluation` |
| Code review | Task | `code_review` |
| Full audit | Workflow | `000_999_cycle` |
| Document analysis | Task | `document_entropy_check` |

---

## 🔗 Next Steps

- **L3_WORKFLOW/** — Documented sequences with file persistence
- **L4_TOOLS/** — Programmatic MCP tool enforcement

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
| ACTIONS/ | ✅ Complete | 9 canonical actions with SKILL.md |
| UTILITIES/ | ✅ Complete | 3 utility skills relocated |
| skill_templates.yaml | ✅ Complete | 50+ skill definitions |
| mcp_tool_templates.py | ✅ Complete | Python wrappers ready |
| DEPLOYMENT.md | ✅ Complete | Guide complete |
| **Coverage** | **50%** | **As designed** |

> This layer is **production-ready** for skill-based deployment.

---

## 🔗 Related Documents

- [ACTIONS/README.md](./ACTIONS/README.md) — The 9 Canonical Actions
- [UTILITIES/README.md](./UTILITIES/README.md) — Auxiliary Skills
- [333_APPS STATUS](../STATUS.md) — Master status tracker
- [ROADMAP/MASTER_TODO.md](../../ROADMAP/MASTER_TODO.md) — Implementation tasks
