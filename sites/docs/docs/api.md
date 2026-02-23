---
id: api
title: API Reference
sidebar_position: 3
description: JSON-RPC and canonical tool contracts for arifOS AAA MCP.
---

# API Reference

Source of truth:

- `arifos_aaa_mcp/server.py`
- `arifos_aaa_mcp/contracts.py`
- `arifos_aaa_mcp/governance.py`

## Transports

| Transport | Connection | Use case |
|:--|:--|:--|
| stdio | `python -m arifos_aaa_mcp stdio` | Local IDE clients |
| SSE | `GET /sse` | Streaming remote clients |
| HTTP MCP | `POST /mcp` | Stateless automation |

## JSON-RPC call shape

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "anchor_session",
    "arguments": {
      "query": "Should we ship this release?",
      "actor_id": "ops"
    }
  },
  "id": 1
}
```

## Canonical tool list

| Tool | Stage |
|:--|:--|
| `anchor_session` | `000_INIT` |
| `reason_mind` | `333_REASON` |
| `recall_memory` | `444_SYNC` |
| `simulate_heart` | `555_EMPATHY` |
| `critique_thought` | `666_ALIGN` |
| `judge_soul` | `888_JUDGE` |
| `forge_hand` | `777_FORGE` |
| `seal_vault` | `999_SEAL` |
| `search_reality` | `111_SENSE` |
| `fetch_content` | `444_SYNC` |
| `inspect_file` | `111_SENSE` |
| `audit_rules` | `333_REASON` |
| `check_vital` | `555_EMPATHY` |

## Resources and prompt

- Resource: `arifos://aaa/schemas`
- Resource: `arifos://aaa/full-context-pack`
- Prompt: `arifos.prompt.aaa_chain`

## Response semantics

Tool responses include governed envelope fields such as:

- `verdict`
- `tool`
- `axioms_333`
- `laws_13`
- `apex_dials`
- `telemetry`
- `motto`
- `data`

Verdict handling:

- `SEAL` -> continue
- `PARTIAL` -> continue with caution
- `SABAR` -> refine/retry
- `VOID` -> blocked
- `888_HOLD` -> human ratification required
