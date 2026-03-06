---
name: thermo-ops
description: arifOS-governed DevOps execution for VPS runtime changes with plan-first and 888_HOLD gates.
---
You are using the thermo-ops skill.

Core rules:
- Scope: limit edits and shell to `/srv/arifOS` and deployment paths explicitly referenced by runbooks.
- Always plan first: summarize goal, list steps, and mark irreversible items.
- For irreversible steps (db drops, rm, volume removal, destructive migrations), mark `888_HOLD` and wait for explicit human approval.
- Prefer small, reversible changes and explain them briefly before running.
- Verify after every infra change with direct health checks.
- Do not add duplicate source paths or ad-hoc symlink shortcuts.

Minimal verification set:

```bash
cd /srv/arifOS
docker ps
opencode mcp list
```
