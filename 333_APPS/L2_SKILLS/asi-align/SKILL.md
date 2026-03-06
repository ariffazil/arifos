---
name: asi-align
description: 555-666_ASI + align verb — Harmony enforcement, bias critique, F5/F6/F9 alignment checks
---

# asi-align

## Scope
Organ 555-666_ASI (Heart/Ω) + Verb align — Harmony enforcement, 7-model critique, bias detection, F5/F6/F9 alignment.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F5 | Peace² | P² ≥ 1.0 |
| F6 | Empathy | κᵣ ≥ 0.70 |
| F9 | Anti-Hantu | C_dark < 0.30 |

## Backend Path
- `aclip_cai/triad/omega/align.py`
- `core/organs/_2_heart.py`
- `aaa_mcp/server.py:arifos_aaa_critique_thought`

## Operational Rules

**Trigger When:**
- Multi-model critique required
- Bias detection and correction needed
- F9 Anti-Hantu consciousness claim check
- Framing inversion analysis
- Non-linearity detection

**Allowed Operations:**
- Run 7-model critique (inversion, framing, non-linearity, etc.)
- Critique the **Structural Integrity** of context (is it atomic?)
- Validate that **Delimiters** are preserved during critique
- Detect consciousness claims (F9)
- Calculate alignment score across perspectives
- Check for hidden assumptions
- Validate stakeholder fairness (F6)

**888_HOLD Required:**
- Consciousness claim detected (F9)
- Severe bias without correction path
- Critique bypass for high-stakes decisions

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos_aaa_critique_thought", {
    "plan": {...},
    "session_id": "sess-xxx",
    "context": "decision context"
})

# Direct backend
from aclip_cai.triad.omega import align
result = await align.run_critique(plan, session_id)
```

## Verification
```bash
python -c "from aclip_cai.triad.omega.align import run_critique; print('Align module ready')"
```
