# L2_SKILLS — Parameterized Templates

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

## 📁 Files in This Directory

| File | Description | Status |
|------|-------------|--------|
| `skill_templates.yaml` | YAML skill definitions | ✅ Complete |
| `mcp_tool_templates.py` | Python tool wrappers | ✅ Complete |
| `DEPLOYMENT.md` | Deployment guide | ✅ Complete |

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
    - init_000
    - sense_111
    - think_222
    - judge_888
    - seal_999
```

---

## 🛡️ Constitutional Floors Enforced

| Floor | Enforcement | Mechanism | Status |
|-------|-------------|-----------|--------|
| F1 Amanah | ⚠️ Partial | Template instruction | Available |
| F2 Truth | ⚠️ Partial | Template parameter | Available |
| F3 Tri-Witness | ❌ None | Requires multi-agent | N/A |
| F4 Clarity | ✅ Full | Schema validation | **Active** |
| F5 Peace² | ⚠️ Partial | Template instruction | Available |
| F6 Empathy | ⚠️ Partial | Parameter injection | Available |
| F7 Humility | ⚠️ Partial | Bounds checking | Available |
| F8 Genius | ⚠️ Partial | Formula templates | Available |
| F9 Anti-Hantu | ⚠️ Partial | Pattern templates | Available |
| F10 Ontology | ⚠️ Partial | Type checking | Available |
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

### v55.5 — Current
- Updated version alignment with root README
- 50+ skill templates verified
- Full YAML validation active
- 50+ skill templates
- Full YAML validation
- MCP tool integration

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
**Version:** v55.5
**Last Updated:** 2026-02-02  
**Creed:** DITEMPA BUKAN DIBERI


---

## ✅ Reality Check

| Component | Status | Evidence |
|-----------|--------|----------|
| skill_templates.yaml | ✅ Complete | 50+ skill definitions |
| mcp_tool_templates.py | ✅ Complete | Python wrappers ready |
| DEPLOYMENT.md | ✅ Complete | Guide complete |
| **Coverage** | **50%** | **As designed** |

> This layer is **production-ready** for skill-based deployment.

---

## 🔗 Related Documents

- [333_APPS STATUS](../STATUS.md) — Master status tracker
- [ROADMAP/MASTER_TODO.md](../../ROADMAP/MASTER_TODO.md) — Implementation tasks
