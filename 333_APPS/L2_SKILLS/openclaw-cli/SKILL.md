---
name: openclaw-cli
version: 0.1.0
summary: "Read-only OpenClaw gateway diagnostics exposed via arifOS MCP"
description: >
  Two-layer integration providing safe, read-only OpenClaw diagnostics:

  Layer 1 — arifOS MCP tool (`query_openclaw` in aaa_mcp/server.py):
    Uses HTTP probe + config file read. Works from inside arifosmcp_server container.
    Exposes action='health' and action='status'.

  Layer 2 — OpenClaw workspace skill (openclaw-workspace/skills/openclaw-cli/):
    Full openclaw CLI access (health, status, models, channels, memory search).
    Runs INSIDE the openclaw_gateway container where the binary is available.

floors:
  - F1   # read-only; no state mutation
  - F2   # report only what is directly observable
  - F4   # structured output
  - F7   # mark unknowns explicitly (e.g. WS-only endpoints)
  - F9   # not a being; this is a diagnostic tool
  - F11  # no unauthenticated execution
  - F12  # no shell injection
  - F13  # Arif retains veto on mutating actions

safety:
  irreversible: false
  calls_shell: true
  shell_scope: "openclaw * --json (read-only subcommands only)"

mcp_tool:
  name: query_openclaw
  file: aaa_mcp/server.py
  integration: aaa_mcp/integrations/openclaw_gateway_client.py
  actions:
    - health   # HTTP /healthz probe + container state
    - status   # health + config snapshot (model, bind, version)

openclaw_skill:
  repo: ariffazil/openclaw-workspace (private)
  path: skills/openclaw-cli/
  tools:
    - openclaw_get_health
    - openclaw_get_status
    - openclaw_list_models
    - openclaw_get_models_status
    - openclaw_channels_status
    - openclaw_memory_search
    - openclaw_gateway_status
---

# openclaw-cli Skill

## Architecture

```
Claude/OpenCode
     │
     │ MCP call: query_openclaw(action="health"|"status")
     ▼
arifOS MCP (arifosmcp_server container)
     │
     │ HTTP GET http://openclaw_gateway:18789/healthz
     │ Read /opt/arifos/data/openclaw/openclaw.json (config only)
     ▼
openclaw_gateway_client.py
     │
     └─ Returns: http_probe, container_state, config_snapshot

OpenClaw agent (inside openclaw_gateway container)
     │
     │ Loads skills/openclaw-cli/ from workspace
     │ Calls: openclaw health --json, openclaw models list --json, etc.
     ▼
openclaw_cli_skill.py → TOOL_DISPATCH
```

## Why two layers

The OpenClaw management API is a **custom WebSocket protocol** (not REST).
Implementing a full WS client in Python would require mirroring the TypeScript
`GatewayClient` handshake. Instead:

- **MCP layer**: Uses the HTTP subset that's observable without WS auth
  (health probe, config file read, container inspect)
- **OpenClaw skill layer**: The OpenClaw agent itself can run `openclaw` CLI
  natively inside its container — full CLI access, no WS client needed

## 888_HOLD boundary

OUT OF SCOPE (require human confirmation):
- `openclaw gateway restart / stop / uninstall`
- `openclaw config set`
- `openclaw cron add / edit / rm`
- `openclaw channels add / remove`
- `openclaw reset / uninstall`

## Usage (via arifOS MCP)

```json
{
  "tool": "query_openclaw",
  "args": {
    "session_id": "<from anchor_session>",
    "action": "health"
  }
}
```

```json
{
  "tool": "query_openclaw",
  "args": {
    "session_id": "<from anchor_session>",
    "action": "status"
  }
}
```
