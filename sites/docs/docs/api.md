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
| **stdio** | `python -m arifos_aaa_mcp stdio` | Local IDE clients (Claude Desktop, Cursor) |
| **Streamable HTTP (Recommended)** | `POST /mcp` | Production deployments, cloud services |

**Note:** Streamable HTTP is the current MCP standard (2024+). See [architecture docs](/architecture) for details.

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

## Canonical 13 Tools

**Source of truth:** `arifos_aaa_mcp/server.py` → `AAA_TOOLS` list

| Tool | Description |
|:--|:--|
| `anchor_session` | 000 INIT: ignite constitutional session and continuity token. |
| `reason_mind` | 333 REASON: run AGI cognition with grounding and budget controls. |
| `recall_memory` | 444 EVIDENCE: retrieve associative memory traces for current thought. |
| `simulate_heart` | 555 EMPATHY: evaluate stakeholder impact and care constraints. |
| `critique_thought` | 666 ALIGN: run 7-model critique (inversion, framing, non-linearity, etc.). |
| `judge_soul` | 777/888 APEX: sovereign constitutional verdict synthesis. |
| `forge_hand` | 888 FORGE: execute action payload behind sovereign control gates. |
| `seal_vault` | 999 SEAL: commit immutable session decision record. |
| `search_reality` | External evidence discovery (read-only). |
| `fetch_content` | Fetch raw evidence content (read-only). |
| `inspect_file` | Inspect local filesystem structure and metadata (read-only). |
| `audit_rules` | Run constitutional/system rule audit checks (read-only). |
| `check_vital` | Read system health telemetry (CPU, memory, IO/thermal optional). |

**Live test:** `curl -X POST https://arifosmcp.arif-fazil.com/mcp -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'`

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
