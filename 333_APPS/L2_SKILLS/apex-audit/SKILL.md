---
name: apex-audit
description: 777-888_APEX + audit verb — Judge all floors, constitutional rule audit, final verdict
---

# apex-audit

## Scope
Organ 777-888_APEX (Soul/Ψ) + Verb audit — Complete constitutional audit of all F1-F13 floors, final judgment, verdict synthesis.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F1-F13 | ALL | Per floor spec |
| F3 | Tri-Witness | W³ ≥ 0.95 |
| F9 | Anti-Hantu | C_dark < 0.30 |
| F13 | Sovereign | HUMAN veto |

## Backend Path
- `aclip_cai/triad/psi/audit.py`
- `core/organs/_3_soul.py`
- `aaa_mcp/server.py:arifos_aaa_apex_judge`

## Operational Rules

**Trigger When:**
- Final verdict synthesis required
- All-floor constitutional audit needed
- F3 Tri-Witness consensus calculation
- Governance token generation for seal_vault
- Human approval checkpoint (F13)

**Allowed Operations:**
- Audit all 13 constitutional floors
- Calculate F3 Tri-Witness consensus (W³)
- Synthesize verdict from AGI + ASI results
- Generate governance token (Amanah handshake)
- Propose verdict: SEAL | PARTIAL | SABAR | VOID | 888_HOLD

**888_HOLD Required:**
- **F13 Sovereign**: Human final authority
- **HIGH IMPACT**: Any irreversible action
- **CONFLICTING**: AGI vs ASI disagreement
- **F3 FAILURE**: W³ < 0.95 consensus

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos_aaa_apex_judge", {
    "query": "decision context",
    "session_id": "sess-xxx",
    "agi_result": {...},
    "asi_result": {...},
    "critique_result": {...}
})

# Direct backend
from aclip_cai.triad.psi import audit
result = await audit.audit_all_floors(session_id, agi_result, asi_result)
```

## Verification
```bash
python -c "from aclip_cai.triad.psi.audit import audit_all_floors; print('Audit module ready')"
```
