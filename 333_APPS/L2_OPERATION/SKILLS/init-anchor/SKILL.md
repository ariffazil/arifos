---
name: init-anchor
description: 000_INIT + anchor verb — Session ignition, injection defense, and authority verification
---

# init-anchor

## Scope
Organ 000_INIT + Verb anchor — Session initialization, F12 injection defense, and F11 authority verification.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F4 | Clarity | ΔS ≤ 0 |
| F11 | CommandAuth | LOCKED |
| F12 | Injection | Risk < 0.85 |

## Backend Path
- `aclip_cai/triad/psi/anchor.py`
- `core/organs/_0_init.py`
- `aaa_mcp/server.py:arifos_aaa_anchor_session`

## Operational Rules

**Trigger When:**
- New session needs to be established
- Query requires injection scanning (F12)
- Authority verification required (F11)
- User token needs validation

**Allowed Operations:**
- Initialize session with UUID generation
- Establish **Thermodynamic Boundary** (Metadata Summary) on session start
- Initialize **Context Governor** for pattern-based file filtering (GitIngest pattern)
- Scan for prompt injection, jailbreak attempts, delimiter attacks
- Verify authority level (SOVEREIGN | ADMIN | USER | PUBLIC)
- Set session grounding parameters
- Create governance token for downstream stages

**888_HOLD Required:**
- Bypassing F12 injection defense
- Elevating authority without verification
- Initializing session with known malicious context

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos-aaa_anchor_session", {
    "query": "user request",
    "session_id": None,  # Will be generated
    "grounding_required": True
})

# Direct backend
from aclip_cai.triad.psi import anchor
result = await anchor.anchor_session(query, session_id, actor_id)
```

## Verification
```bash
python -c "from aaa_mcp.server import create_aaa_mcp_server; print('Anchor session tool ready')"
```
