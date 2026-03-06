---
name: asi-respond
description: 555-666_ASI + respond verb — Compassionate output generation and stakeholder communication
---

# asi-respond

## Scope
Organ 555-666_ASI (Heart/Ω) + Verb respond — Compassionate response generation, F4 clarity, F5 peace, F6 empathy in output.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F4 | Clarity | ΔS ≤ 0 |
| F5 | Peace² | P² ≥ 1.0 |
| F6 | Empathy | κᵣ ≥ 0.70 |

## Backend Path
- `aclip_cai/triad/omega/respond.py`
- `core/organs/_2_heart.py`
- `aaa_mcp/server.py:arifos_aaa_simulate_heart`

## Operational Rules

**Trigger When:**
- Response needs stakeholder-aware generation
- Compassionate framing required (F6)
- Output peace verification needed (F5)
- Clarifying ambiguous results

**Allowed Operations:**
- Generate stakeholder-aware responses
- Ensure F5 Peace² ≥ 1.0 in output
- Apply F6 Empathy (κᵣ ≥ 0.70)
- Reduce entropy in communication (F4)
- Format output with constitutional tone

**888_HOLD Required:**
- Bypassing empathy requirements (F6)
- Generating harmful/destabilizing output (F5)
- Intentional obfuscation (F4 violation)

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos-aaa_simulate_heart", {
    "query": "stakeholder impact assessment",
    "session_id": "sess-xxx",
    "stakeholders": ["user", "system", "data"]
})

# Direct backend
from aclip_cai.triad.omega import respond
result = await respond.generate_response(plan, stakeholders)
```

## Verification
```bash
python -c "from aclip_cai.triad.omega.respond import generate_response; print('Respond module ready')"
```
