---
id: api
title: MCP API Reference (L4 Tools)
sidebar_position: 3
description: JSON-RPC contracts, protocol negotiation, and canonical arifOS AAA MCP tool surface.
---

# MCP API Reference (L4 Tools)

arifOS exposes a governed MCP surface through `arifos_aaa_mcp`. Every `tools/call` is evaluated through constitutional gates before execution.

## Protocol versioning

- Current protocol: `2025-11-25`
- Supported versions: `2025-11-25`, `2025-03-26`
- Negotiated during `initialize`; one session must use one agreed version.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {"name": "client", "version": "1.0"}
  }
}
```

## JSON-RPC call shape

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "reason_mind",
    "arguments": {
      "query": "Is this deployment ready?",
      "session_id": "sess_abc"
    }
  }
}
```

## Canonical 13 tools

| Tool | Description |
|:--|:--|
| `anchor_session` | 000 INIT: ignite constitutional session and continuity token. |
| `reason_mind` | 333 REASON: run AGI cognition with grounding and budget controls. |
| `recall_memory` | 444 EVIDENCE: retrieve associative memory traces for current thought. |
| `simulate_heart` | 555 EMPATHY: evaluate stakeholder impact and care constraints. |
| `critique_thought` | 666 ALIGN: run 7-model critique (inversion, framing, non-linearity, etc.). |
| `apex_judge` | 888 APEX: sovereign constitutional verdict synthesis. |
| `eureka_forge` | 777 FORGE: execute action payload behind sovereign control gates. |
| `seal_vault` | 999 SEAL: commit immutable session decision record. |
| `search_reality` | External evidence discovery (read-only). |
| `fetch_content` | Fetch raw evidence content (read-only). |
| `inspect_file` | Inspect local filesystem structure and metadata (read-only). |
| `audit_rules` | Run constitutional/system rule audit checks (read-only). |
| `check_vital` | Read system health telemetry (CPU, memory, IO/thermal optional). |

## Resources and prompt

- Resource: `arifos://aaa/schemas`
- Resource: `arifos://aaa/full-context-pack`
- Prompt: `arifos.prompt.aaa_chain`

## Response envelope

Tool responses include governed fields:

- `verdict`
- `tool`
- `axioms_333`
- `laws_13`
- `telemetry`
- `apex_dials`
- `contrast_engine`
- `motto`
- `data`

Verdict behavior:

- `SEAL` -> continue
- `PARTIAL` -> continue with caution
- `SABAR` -> refine/retry
- `VOID` -> blocked
- `888_HOLD` -> human ratification required
