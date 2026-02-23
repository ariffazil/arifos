---
id: api
title: API Reference
sidebar_position: 3
description: Truth-grounded tool surface, JSON-RPC transport, and governance semantics for the arifOS MCP server.
---

# API Reference

> Source: `aaa_mcp/server.py`, `server.py`, `aaa_mcp/protocol/schemas.py`, `aaa_mcp/protocol/tool_registry.py`
> Live endpoint: `https://arifosmcp.arif-fazil.com`
> Version: `2026.02.22-FORGE-VPS-SEAL` (T000)

arifOS speaks MCP (Model Context Protocol) using JSON-RPC 2.0. This page documents the tool surface that is
actually registered in `main` today.

:::info Public tool surface (F2 Truth)
The AAA-MCP server registers the following MCP tool names:

`anchor`, `reason`, `integrate`, `respond`, `validate`, `align`, `forge`, `audit`, `seal`, `trinity_forge`, `search`, `fetch`.

If you are looking for names like `init_gate` or `apex_verdict`: those exist as canonical identifiers in
`aaa_mcp/protocol/tool_registry.py`, but they are not currently the MCP tool names registered by `aaa_mcp/server.py`.
:::

---

## 1. Transports

| Transport | Connection | Best for |
|:--|:--|:--|
| stdio | `python -m aaa_mcp stdio` | Claude Desktop, Cursor IDE, local dev |
| SSE (primary) | `GET /sse` | remote clients, streaming |
| HTTP (fallback) | `POST /mcp` | direct JSON-RPC automation |

Authentication (SSE/HTTP):

```http
ARIF_SECRET: <your-secret>
Content-Type: application/json
```

---

## 2. JSON-RPC MCP call shape

Tool calls use `tools/call`:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "anchor",
    "arguments": {
      "query": "Should we deploy to production?",
      "actor_id": "operator"
    }
  },
  "id": 1
}
```

Tool responses are returned as text content containing JSON.

---

## 3. Governance semantics

### Verdicts

Tool outputs use these verdict strings:

`SEAL`, `PARTIAL`, `SABAR`, `VOID`, `888_HOLD`

Client handling:

| Verdict | Meaning | Client action |
|:--|:--|:--|
| `SEAL` | allowed | continue / record |
| `PARTIAL` | allowed with warnings | continue with caution |
| `SABAR` | retry/refine | add grounding, revise, or wait |
| `VOID` | blocked | do not proceed; fix violation |
| `888_HOLD` | human ratification required | stop and escalate |

### Governance mode (`GOVERNANCE_MODE`)

The repo currently uses `GOVERNANCE_MODE` values like `HARD` and `SOFT` in deployment configs.

- Documentation term: `STRICT` = maximum enforcement.
- Current config term: `HARD` = `STRICT` (legacy label).

If your environment only accepts `HARD`/`SOFT`, set `HARD` for production enforcement.

---

## 4. Tools

Below are the registered MCP tools and their current parameter surfaces (from function signatures).
Return payload fields may evolve; always key off `verdict` + `session_id`.

### `anchor` (stage 000)

Initialize a constitutional session.

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `actor_id` | string | no |
| `auth_token` | string | no |
| `platform` | string | no |

Floors: F11, F12

### `reason` (stage 222)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `session_id` | string | yes |
| `hypotheses` | number | no |

Floors: F2, F4, F8

### `integrate` (stage 333)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `session_id` | string | yes |
| `grounding` | array | no |

Floors: F7, F10

### `respond` (stage 444)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `session_id` | string | yes |
| `plan` | string | no |
| `scope` | string | no |

Floors: F4, F6

### `validate` (stage 555)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `session_id` | string | yes |
| `stakeholders` | array | no |
| `scope` | string | no |

Floors: F5, F6

### `align` (stage 666)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `session_id` | string | yes |
| `ethical_rules` | array | no |

Floors: F9

### `forge` (stage 777)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `session_id` | string | yes |
| `implementation_details` | object | yes |

Floors: F2, F4

### `audit` (stage 888)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `session_id` | string | yes |
| `verdict` | string | yes |
| `human_approve` | boolean | no |

Floors: F3, F11, F13

### `seal` (stage 999)

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `session_id` | string | yes |
| `summary` | string | yes |
| `verdict` | string | yes |

Floors: F1, F3

### `trinity_forge` (000->999)

Single-call pipeline orchestration.

Parameters:

| Field | Type | Required |
|:--|:--|:--|
| `query` | string | yes |
| `actor_id` | string | no |

### `search`, `fetch` (read-only hints)

These exist to support ChatGPT Deep Research style workflows.

- `search(query: string) -> { ids: string[] }`
- `fetch(id: string) -> record`

---

## 5. Infrastructure boundaries

- Python: `>= 3.10` (see `pyproject.toml`).
- Persistence:
  - PostgreSQL is used when `DATABASE_URL` is configured and Postgres dependencies are available.
  - Local fallbacks exist (memory and/or SQLite), so Postgres is recommended for high-load durability, not a universal runtime blocker.
- Cache:
  - Redis is recommended for high-load session state stability (F5 Peace^2), but local fallbacks exist.
