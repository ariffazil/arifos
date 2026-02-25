# L2_SKILLS — 11 Canonical VERBS (v60.0-FORGE)

**Level 2 | 9 Actions Only | ΔS ≤ 0**

> *DITEMPA BUKAN DIBERI — Actions forged, not scattered.*

---

## The 11 Canonical VERBS

| # | VERB | Stage | Trinity | MCP Tool | Primary Floors | Action |
|---|------|-------|---------|----------|----------------|--------|
| 1 | **anchor** | 111 | Δ Mind | `init_gate` + `agi_sense` | F2, F4, F12 | 🔱 PERCEIVE |
| 2 | **reason** | 222 | Δ Mind | `agi_think` | F2, F4, F7, F8 | 🧠 THINK |
| 3 | **integrate** | 333 | Δ Mind | `agi_reason` | F2, F7, F8 | 🗺️ MAP |
| 4 | **respond** | 444 | Ω Heart | `asi_respond` | F4, F5, F6 | ❤️ CARE |
| 5 | **validate** | 555 | Ω Heart | `asi_empathize` | F1, F5, F6 | 🛡️ DEFEND |
| 6 | **align** | 666 | Ω Heart | `asi_align` | F5, F6, F9 | ⚖️ HARMONIZE |
| 7 | **forge** | 777 | Ψ Soul | `trinity_forge` | F2, F4, F7 | 🔥 CRYSTALLIZE |
| 8 | **audit** | 888 | Ψ Soul | `apex_judge` | F1-F13 | 👁️ JUDGE |
| 9 | **seal** | 999 | Ψ Soul | `vault_seal` | F1, F3, F11 | 🔒 COMMIT |

---

## Consolidation (18 → 9)

Old scattered skills → New unified VERBS:
- `f1-amanah`, `f2-truth`, `f6-*`, `f7-*`, `f8-*`, `f9-*`, `f13-*` → **9 VERBS**
- `trinity-*-pipeline`, `apex-*`, `phoenix-*` → **forge**, **audit**, **seal**

See: [CONSOLIDATION_v60.md](CONSOLIDATION_v60.md)

---

## Directory Structure

```
L2_SKILLS/
├── README.md                 # This file
├── CONSOLIDATION_v60.md      # 18→9 mapping
├── 333_AXIOMS.md             # Root glossary (symlink)
├── skill_templates.yaml      # 9 verb templates
├── mcp_tool_templates.py     # Python wrappers
└── ACTIONS/                  # 11 canonical VERBS
    ├── anchor/
    ├── reason/
    ├── integrate/
    ├── respond/
    ├── validate/
    ├── align/
    ├── forge/
    ├── audit/
    └── seal/
```

---

## Quick Start

```python
# Use VERB directly
from arifos.skills import anchor, reason, validate, seal

# 111: Anchor reality
session = await anchor(query="Your query")

# 222: Reason through
analysis = await reason(query="Your query", session_id=session.id)

# 555: Validate stakeholders
impact = await validate(query="Your query", session_id=session.id)

# 999: Seal decision
commitment = await seal(verdict="SEAL", session_id=session.id)
```

---

## Constitutional Floors (All 13)

| Floor | Status | Enforced By |
|-------|--------|-------------|
| F1 Amanah | ✅ | validate, audit, seal |
| F2 Truth | ✅ | anchor, reason, forge |
| F3 Tri-Witness | ✅ | audit, seal |
| F4 Clarity | ✅ | anchor, reason, forge |
| F5 Peace² | ✅ | respond, validate, align |
| F6 Empathy | ✅ | validate, align |
| F7 Humility | ✅ | reason, integrate, forge |
| F8 Genius | ✅ | reason, integrate |
| F9 Anti-Hantu | ✅ | align |
| F10 Ontology | ✅ | anchor |
| F11 Command | ✅ | seal |
| F12 Injection | ✅ | anchor |
| F13 Sovereign | ✅ | audit |

---

## Axioms Reference

See: [333_AXIOMS.md](/333_AXIOMS.md)

Key axioms:
- **ΔS ≤ 0** — Cooling is primary duty
- **P(Truth|E=0) = 0** — No free truth
- **W₃ ≥ 0.95** — Tri-witness consensus
- **κᵣ ≥ 0.95** — Weakest stakeholder protected
- **Ω₀ ∈ [0.03,0.05]** — Healthy uncertainty

---

## Deployment

```bash
# Install
pip install -e ".[dev]"

# Test
pytest L2_SKILLS/ACTIONS/ -v

# Run
python -m arifos.skills.anchor "Your query"
```

---

## Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v60.0-FORGE  
**Creed:** DITEMPA BUKAN DIBERI  
**Entropy:** ΔS = -50% (18→9)
