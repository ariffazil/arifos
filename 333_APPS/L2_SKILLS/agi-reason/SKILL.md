---
name: agi-reason
description: 111-444_AGI + reason verb — AGI cognition, thinking, causal tracing, and truth evaluation
---

# agi-reason

## Scope
Organ 111-444_AGI (Mind/Δ) + Verb reason — AGI reasoning, thinking, causal analysis, and truth evaluation (F2, F4, F7, F8).

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F2 | Truth | τ ≥ 0.99 |
| F4 | Clarity | ΔS ≤ 0 |
| F7 | Humility | Ω₀ ∈ [0.03, 0.05] |
| F8 | Genius | G ≥ 0.80 |

## Backend Path
- `aclip_cai/triad/delta/reason.py`
- `core/organs/_1_mind.py`
- `aaa_mcp/server.py:arifos_aaa_reason_mind`

## Operational Rules

**Trigger When:**
- Complex reasoning required on query
- Truth verification needed (F2)
- Causal chain analysis required
- Solution approaches need evaluation

**Allowed Operations:**
- Parse intent and reduce entropy (F4)
- Execute **Hierarchical Reasoning**: Summary -> Tree -> Atomic Content
- Consolidate logic into **Atomic Context Units** (canonical path + delimiters)
- Perform causal tracing and logic chains
- Calculate uncertainty bounds (F7)
- Evaluate genius score for approaches (F8)
- Ground reasoning with external evidence

**888_HOLD Required:**
- Reasoning bypass of F2 truth requirements
- Uncertainty override outside Ω₀ bounds
- Genius score manipulation

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos_aaa_reason_mind", {
    "query": "reasoning task",
    "session_id": "sess-xxx",
    "capability_modules": ["causal", "truth", "genius"]
})

# Direct backend
from aclip_cai.triad.delta import reason
result = await reason.reason_mind(query, session_id)
```

## Verification
```bash
python -c "from aclip_cai.triad.delta.reason import reason_mind; print('Reason module ready')"
```
