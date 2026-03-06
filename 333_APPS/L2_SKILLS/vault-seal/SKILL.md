---
name: vault-seal
description: 999_VAULT + seal verb — Immutable ledger commit, cryptographic seal, memory band assignment
---

# vault-seal

## Scope
Organ 999_VAULT + Verb seal — Immutable decision commitment, cryptographic sealing, audit trail, memory band assignment.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F1 | Amanah | LOCKED (token verification) |
| F3 | Tri-Witness | W³ ≥ 0.95 |
| F11 | CommandAuth | LOCKED (governance token) |

## Backend Path
- `aclip_cai/triad/psi/seal.py`
- `core/organs/_4_vault.py`
- `aaa_mcp/server.py:arifos_aaa_seal_vault`
- Ledger: `VAULT999/`

## Operational Rules

**Trigger When:**
- Decision needs immutable commitment
- Audit trail requires cryptographic seal
- Session needs final termination
- Memory band assignment required

**Allowed Operations:**
- Verify governance token from apex_judge (Amanah handshake)
- Commit decision to VAULT999 ledger
- Generate Merkle root and SHA-256 seal
- Assign memory band (L0-L5)
- Store thermodynamic telemetry

**888_HOLD Required:**
- **TOKEN INVALID**: Governance token verification failure
- **VERDICT MISMATCH**: Tampered token or verdict
- **LEDGER CORRUPTION**: Database/VAULT999 integrity issues

## Amanah Handshake
```python
# In apex_judge: signs token
governance_token = _build_governance_token(session_id, verdict)

# In seal_vault: verifies token
token_valid, verified_verdict = _verify_governance_token(session_id, governance_token)
if not token_valid:
    return {"verdict": "VOID", "reason": "Token verification failed"}
```

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos_aaa_seal_vault", {
    "session_id": "sess-xxx",
    "summary": "Decision summary",
    "verdict": "SEAL",
    "governance_token": "token-from-apex"
})

# Direct backend
from aclip_cai.triad.psi import seal
result = await seal.seal_decision(session_id, summary, verdict, telemetry)
```

## Verification
```bash
python -c "from aclip_cai.triad.psi.seal import seal_decision; print('Seal module ready')"
```
