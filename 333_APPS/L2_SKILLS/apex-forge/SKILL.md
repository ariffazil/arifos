---
name: apex-forge
description: 777-888_APEX + forge verb — Crystallize execution, shell commands with 888_HOLD gates
---

# apex-forge

## Scope
Organ 777-888_APEX (Soul/Ψ) + Verb forge — Execution crystallization, shell command execution with F1 Amanah gates and audit logging.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F1 | Amanah | LOCKED (reversibility) |
| F2 | Truth | τ ≥ 0.99 |
| F4 | Clarity | ΔS ≤ 0 |
| F8 | Genius | G ≥ 0.80 |

## Backend Path
- `aclip_cai/triad/psi/forge.py`
- `core/organs/_3_soul.py`
- `aaa_mcp/server.py:arifos_aaa_eureka_forge`

## Operational Rules

**Trigger When:**
- Shell command execution required
- File operations needed
- Dangerous operations (rm -rf, mkfs, dd, etc.)
- Git operations (commit, push, rebase)

**Allowed Operations:**
- Execute shell commands with timeout
- Record output as **Atomic Context Units** (with delimiters)
- Filter noisy output (build logs) using **Context Governor** patterns
- Working directory validation (F5 safe defaults)
- Comprehensive error handling (F6)
- Risk classification (LOW/MODERATE/CRITICAL)
- Transparent logging with agent_id and purpose (F9)

**888_HOLD Required:**
- **DANGEROUS**: rm -rf, mkfs, dd, fdisk, etc.
- **GIT DESTRUCTIVE**: rebase, force push, history rewrite
- **DATABASE**: migrations, schema changes
- **MASS OPS**: >10 files affected
- **CREDENTIALS**: secret handling, key rotation

## Quick Reference
```python
# MCP Tool
await mcp.call_tool("arifos_aaa_eureka_forge", {
    "command": "ls -la",
    "session_id": "sess-xxx",
    "working_dir": "/srv/arifOS",
    "purpose": "List repository files"
})

# Direct backend
from aclip_cai.triad.psi import forge
result = await forge.execute_shell(command, session_id, confirm_dangerous=True)
```

## Verification
```bash
python -c "from aaa_mcp.server import create_aaa_mcp_server; print('Forge tool ready')"
```
