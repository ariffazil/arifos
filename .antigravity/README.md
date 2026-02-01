# .antigravity — Constitutional Agent Workspace

> **The Trinity Operating Environment**  
> **Canon:** `000_THEORY/`  
> **Principle:** *Ditempa Bukan Diberi* — Forged, Not Given

---

## 🎯 THE 5-TOOL TRINITY

```
"Init the Gate, Reason with Mind, Empathize with Heart, 
 Verify with Eye, Verdict at Apex, Seal in Vault."
```

| Tool | Role | Symbol | Agent |
|:---|:---|:---:|:---|
| `init_gate` | Gate | 🚪 | All |
| `agi_reason` | Mind | Δ | GEMINI |
| `asi_empathize` | Heart | Ω | CLAUDE |
| `apex_verdict` | Soul | Ψ | APEX |
| `vault_seal` | Seal | 🔒 | KIMI |

---

## 📁 DIRECTORY STRUCTURE

| Directory | Purpose |
|:---|:---|
| `adapters/` | **Agent-specific codex files** (GEMINI.md, CLAUDE.md, CODEX.md, KIMI.md) |
| `rules/` | **Constitutional rules** (GEMINI.md — consolidated F1-F13 + boundaries + ontology) |
| `workflows/` | **Step-by-step processes** (9 active workflows) |
| `environment/` | **Physics layer** (physics.md, hypervisor.md, budget.json) |
| `brain/` | **Working memory** (drafts, scratchpads, state) |
| `AGENTS.md` | **Unified agent manifest** (all 5 agents) |
| `.cursorrules` | **IDE constraints** (Token/Time/Floor enforcement) |

---

## 👥 THE FIVE AGENTS

| Agent | Symbol | Role | Codex | Floors |
|:---:|:---:|:---|:---|:---:|
| **GEMINI** | Δ | Architect (Mind) | `adapters/GEMINI.md` | F2, F4, F7, F10, F12 |
| **CLAUDE** | Ω | Engineer (Heart) | `adapters/CLAUDE.md` | F1, F5, F6, F9 |
| **CODEX** | 👁 | Auditor (Eye) | `adapters/CODEX.md` | F2, F12 |
| **APEX** | Ψ | Judge (Soul) | *(internal engine)* | F3, F8, F11, F13 |
| **KIMI** | Κ | Validator (Seal) | `adapters/KIMI.md` | F1, F3, F8 |

---

## 🚀 QUICK START

```bash
# Initialize
/init              # Start constitutional session

# Design
/architect         # Plan + Review + Handoff (Δ)
/agi               # Deep reasoning (Δ)

# Verify
/audit             # Cross-check claims (👁)
/empathize         # Stakeholder safety (Ω)

# Build
/engineer          # Build with care (Ω)
/align             # Ethical check (Ω)

# Judge
/judge             # Final verdict (Ψ)

# Seal
/seal              # Cryptographic seal (Κ)

# Utilities
/ledger            # View audit trail
/hold              # Human override (888)
```

---

## 📚 KEY REFERENCES

| Document | Location | Purpose |
|:---|:---|:---|
| **Agent Manifest** | `AGENTS.md` | All 5 agents, handoff protocols |
| **Constitutional Law** | `000_THEORY/000_LAW.md` | 13 Floors (F1-F13) |
| **Architecture** | `000_THEORY/000_ARCHITECTURE.md` | ΔΩΨ Trinity |
| **Floor Reference** | `rules/GEMINI.md` | Consolidated F1-F13 + boundaries + ontology |
| **Governance** | `rules/GEMINI.md` | Agent boundaries, ontology, floors |

---

## 🌡️ PHYSICS LAYER (Environment)

The `.antigravity/environment/` directory contains **thermodynamic enforcement** aligned with `333_APPS/L5_AGENTS/`:

| Physics | File | Constraint |
|:---|:---|:---|
| **Token** | `environment/physics.md` | $1.00 max budget per session |
| **Time** | `environment/physics.md` | 30s max latency per operation |
| **Law** | `environment/physics.md` | F1-F13 floor enforcement |
| **Ignition** | `environment/hypervisor.md` | 000-999 metabolic cycle |
| **Budget** | `environment/budget.json` | Configurable thresholds |

### Quick Physics Check
```python
from environment import HYPERVISOR, PHYSICS

# Check budget
if PHYSICS["token"].session_cost > 0.75:
    warn("Budget 75% — consider sealing")

# Enforce time
result = await PHYSICS["time"].measure(agent.execute(input))

# Check floor
if not PHYSICS["law"].check_floor("F1", action):
    return {"verdict": "VOID"}

# Run cycle
result = await HYPERVISOR.ignition(AgentClass, query)
```

---

## 🛡️ CONSTITUTIONAL FLOORS (Summary)

| Floor | Name | Threshold | Agent | Physics |
|:---:|:---|:---|:---:|:---:|
| F1 | Amanah | Reversibility | Ω / Κ | ✅ Enforced |
| F2 | Truth | τ ≥ 0.99 | Δ / 👁 | ✅ Enforced |
| F3 | Tri-Witness | W₃ ≥ 0.95 | Ψ / Κ | ✅ Enforced |
| F4 | Clarity | ΔS ≤ 0 | Δ | ✅ Enforced |
| F5 | Peace² | P² ≥ 1.0 | Ω | ✅ Enforced |
| F6 | Empathy | κᵣ ≥ 0.70 | Ω | ✅ Enforced |
| F7 | Humility | Ω₀ ∈ [0.03, 0.05] | Δ | ✅ Enforced |
| F8 | Genius | G ≥ 0.80 | Ψ / Κ | ✅ Enforced |
| F9 | Anti-Hantu | C_dark ≤ 0.30 | Ω / 👁 | ✅ Enforced |
| F10 | Ontology | LOCK | Δ | ✅ Enforced |
| F11 | Authority | Verified | Ψ | ✅ Enforced |
| F12 | Injection | < 0.85 | 👁 / Δ | ✅ Enforced |
| F13 | Sovereign | Human | 888 | ✅ Enforced |

---

## 🔄 THE METABOLIC LOOP

```
000_INIT (🚪 Gate)
    ↓
111_SENSE → 222_THINK → 333_ATLAS (Δ GEMINI)
    ↓
444_EVIDENCE (👁 CODEX)
    ↓
555_EMPATHY → 666_ALIGN (Ω CLAUDE)
    ↓
888_JUDGE (Ψ APEX)
    ↓
999_SEAL (Κ KIMI)
    ↓
[Seed for next 000_INIT] — The Strange Loop
```

---

## 📖 AGENT ADAPTERS

Each agent has a detailed codex:

- **[GEMINI.md](adapters/GEMINI.md)** — The Architect's Codex (Stages 111-333)
- **[CLAUDE.md](adapters/CLAUDE.md)** — The Engineer's Codex (Stages 555-666)
- **[CODEX.md](adapters/CODEX.md)** — The Auditor's Codex (Stage 444)
- **[KIMI.md](adapters/KIMI.md)** — The Validator's Codex (Stage 999)

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.

> *"Intelligence is not a gift. It is a thermodynamic work process. 
> These files are the forge where intelligence becomes wisdom."*
