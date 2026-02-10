# L2_SKILLS — Parameterized Templates (v55.5-HARDENED)

**Level 2 | 50% Coverage | Low Complexity**

> *DITEMPA BUKAN DIBERI — Skills forged, not given.*

---

## Directory Structure

```
L2_SKILLS/
├── README.md                 # This file
├── skill_templates.yaml      # 10 canonical stage templates
├── mcp_tool_templates.py     # Python tool wrappers
├── ACTIONS/                  # 9 canonical atomic actions
│   ├── anchor/               # 111_SENSE — Ground reality
│   ├── reason/               # 222_THINK — Logical inference
│   ├── integrate/            # 333_ATLAS — Cross-domain synthesis
│   ├── respond/              # 444_EVIDENCE — Compassionate output
│   ├── validate/             # 555_EMPATHY — Stakeholder impact
│   ├── align/                # 666_ALIGN — Ethical alignment
│   ├── forge/                # 777_FORGE — Reduce entropy
│   ├── audit/                # 888_JUDGE — Constitutional verdict
│   └── seal/                 # 999_SEAL — Immutable commitment
└── UTILITIES/                # Auxiliary skills
    ├── visual-law/           # Trinity design system
    ├── capture-terminal/     # Terminal output capture
    └── route-tasks/          # Policy-based task routing
```

---

## The 9 Canonical Actions

| # | Action | Stage | Trinity | MCP Tool | Primary Floors |
|---|--------|-------|---------|----------|----------------|
| 1 | **anchor** | 111 | Δ Mind | `agi_sense` | F4, F7, F12 |
| 2 | **reason** | 222 | Δ Mind | `agi_reason` | F2, F4, F7 |
| 3 | **integrate** | 333 | Δ Mind | `agi_reason` | F2, F7, F8 |
| 4 | **respond** | 444 | Ω Heart | `asi_act` | F4, F5, F6 |
| 5 | **validate** | 555 | Ω Heart | `asi_empathize` | F1, F5, F6 |
| 6 | **align** | 666 | Ω Heart | `asi_align` | F5, F6, F9 |
| 7 | **forge** | 777 | Ψ Soul | `reality_search` | F2, F4, F7 |
| 8 | **audit** | 888 | Ψ Soul | `apex_verdict` | F1-F13 |
| 9 | **seal** | 999 | Ψ Soul | `vault_seal` | F1, F3, F11 |

---

## Quick Start

```python
# Load skill templates
import yaml
with open("skill_templates.yaml") as f:
    skills = yaml.safe_load(f)

# Use a skill
template = skills["777_FORGE"]["template"]
```

```python
# MCP tool wrapper
from mcp_tool_templates import _ignite_, _logic_, _decree_

# Initialize session
session = await _ignite_(query="Your query")

# Execute reasoning
result = await _logic_(query="Your query", session_id=session["session_id"])
```

---

## Deployment

```bash
# Local development
pip install -e ".[dev]"

# Environment
export ARIFOS_MODE=PROD
export ARIFOS_SKILLS_PATH=333_APPS/L2_SKILLS

# Test
pytest L2_SKILLS/tests/ -v
```

---

## Constitutional Floors

| Floor | Status | Mechanism |
|-------|--------|-----------|
| F1 Amanah | ✅ | Reversibility checks |
| F2 Truth | ✅ | τ ≥ 0.99 verification |
| F3 Tri-Witness | ✅ | W₃ ≥ 0.95 consensus |
| F4 Clarity | ✅ | ΔS ≤ 0 enforcement |
| F5 Peace² | ✅ | P² ≥ 1.0 validation |
| F6 Empathy | ✅ | κᵣ ≥ 0.95 protection |
| F7 Humility | ✅ | Ω₀ ∈ [0.03,0.05] |
| F8 Genius | ✅ | G ≥ 0.80 scoring |
| F9 Anti-Hantu | ✅ | C_dark < 0.30 |
| F10 Ontology | ✅ | Symbol validation |
| F11 Command Auth | ✅ | Token verification |
| F12 Injection | ✅ | Risk < 0.85 |
| F13 Sovereign | ✅ | Human override |

---

## Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v55.5-HARDENED  
**Creed:** DITEMPA BUKAN DIBERI
