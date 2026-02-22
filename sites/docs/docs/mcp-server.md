---
id: mcp-server
title: MCP Server
sidebar_position: 2
description: Install, configure, and connect to the arifOS MCP server via stdio, SSE, or HTTP.
---

# MCP Server

> Source: [`README.md`](https://github.com/ariffazil/arifOS/blob/main/README.md) · [`aaa_mcp/server.py`](https://github.com/ariffazil/arifOS/blob/main/aaa_mcp/server.py) · [`server.py`](https://github.com/ariffazil/arifOS/blob/main/server.py)  
> PyPI: [`pip install arifos`](https://pypi.org/project/arifos/)

arifOS speaks the **Model Context Protocol (MCP)** - the open standard for LLM tool use. Any MCP-compatible client (Claude Desktop, Cursor, OpenClaw, ChatGPT developer mode) can connect to it.

---

## Installation

### Option A - PyPI (fastest)

```bash
pip install arifos
```

### Option B - From source (recommended for contributors)

```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e ".[dev]"          # editable install with dev deps
# or with uv:
pip install uv && uv pip install -e ".[dev]"
```

---

## Running the Server

### Unified server (recommended for production)

The `server.py` at repo root runs a **unified** FastMCP server that bundles:

- AAA-MCP governance pipeline tools (000->999)
- Additional read-only observability/sensory tools

Counts and non-governance tool names can change; treat the governance pipeline tools as the stable operator contract.

```bash
python server.py                  # default: REST mode
python server.py --mode rest      # REST API + SSE + all tools
python server.py --mode sse       # FastMCP SSE transport
python server.py --mode http      # FastMCP HTTP transport
python server.py --mode stdio     # stdio (local clients)
```

### Standalone AAA-MCP server (9 governance tools only)

```bash
python -m aaa_mcp                 # stdio
python -m aaa_mcp sse             # SSE on :8080
python -m aaa_mcp http            # HTTP on :8080
python -m aaa_mcp.selftest        # smoke test
```

---

## Public MCP Tools (Truth-Grounded)

The AAA-MCP transport currently exposes **legacy verb tool names** as the MCP tool surface.
These are public tool names today (call them via MCP). They also correspond to internal pipeline stages.

All tools chain via `session_id`.

| # | MCP tool name | Stage | Purpose | Floors |
|:--|:--|:--|:--|:--|
| 1 | `anchor` | 000 | Session ignition / airlock | F11, F12 |
| 2 | `reason` | 222 | Hypotheses / reasoning | F2, F4, F8 |
| 3 | `integrate` | 333 | Context + grounding merge | F7, F10 |
| 4 | `respond` | 444 | Draft / plan synthesis | F4, F6 |
| 5 | `validate` | 555 | Stakeholder impact | F5, F6 |
| 6 | `align` | 666 | Ethics/policy reconciliation | F9 |
| 7 | `forge` | 777 | Solution synthesis | F2, F4 |
| 8 | `audit` | 888 | Final judgment | F3, F11, F13 |
| 9 | `seal` | 999 | Commit to VAULT999 | F1, F3 |
| 10 | `trinity_forge` | 000->999 | Full pipeline shortcut | entry enforces F11/F12; internal stages enforce floors |

Additional tools may be present depending on which server you run:

- `search`, `fetch` - ChatGPT Deep Research integration (read-only hints)
- Additional read-only observability/sensory tools (unified server)

:::info Canonical IDs vs MCP tool names
You may also see canonical tool identifiers in `aaa_mcp/protocol/tool_registry.py` (e.g. `init_gate`, `agi_reason`).
These are routing/documentation identifiers, not the MCP tool names currently registered by `aaa_mcp/server.py`.
For MCP calls, use the tool names in the table above.
:::

---

## Environment Variables

| Variable | Required | Default | Description |
|:--|:--|:--|:--|
| `ARIF_SECRET` | Recommended | `""` | Authentication header for SSE/HTTP transports |
| `BRAVE_API_KEY` | Optional | `""` | Enables external web search grounding (where configured) |
| `OPENAI_API_KEY` | Optional | `""` | ChatGPT search/fetch tools in unified server |
| `DATABASE_URL` | Optional | SQLite/memory | VAULT999 persistence (PostgreSQL when configured; local fallbacks supported) |
| `REDIS_URL` | Optional | In-memory | Session state cache (Redis when configured; local fallbacks supported) |
| `PORT` | Optional | `8080` | Server port for SSE/HTTP modes |
| `HOST` | Optional | `0.0.0.0` | Server bind address |
| `AAA_MCP_TRANSPORT` | Optional | `stdio` | Override transport (`stdio`/`sse`/`http`) |
| `AAA_MCP_OUTPUT_MODE` | Optional | `user` | `user` or `debug` (verbose floor scores) |
| `ARIFOS_PHYSICS_DISABLED` | Optional | `0` | Set `1` to skip thermodynamic calculations (faster, for tests) |

Copy `.env.docker.example` to `.env.docker` and fill in your keys before deploying.

---

## Connecting MCP Clients

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"]
    }
  }
}
```

### Cursor IDE

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"]
    }
  }
}
```

### Remote SSE / HTTP client

```bash
# Test SSE endpoint (expects a hanging connection)
curl -H "ARIF_SECRET: your-secret" https://arifosmcp.arif-fazil.com/sse -m 2

# Test HTTP MCP endpoint
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "ARIF_SECRET: your-secret" \
  -d '{"jsonrpc":"2.0","method":"ping","id":1}'
```

### OpenClaw (WhatsApp gateway)

```json
{
  "agents": {
    "arif-actor": {
      "model": "claude-sonnet-4",
      "skills": ["AAA-ACTOR", "exec-skill"],
      "mcp": { "url": "https://arifosmcp.arif-fazil.com/sse" }
    }
  }
}
```

---

## Health & Metrics

```bash
# Live health check (returns JSON)
curl https://arifosmcp.arif-fazil.com/health

# Governance metrics (if enabled)
curl https://arifosmcp.arif-fazil.com/metrics.json
```

---

## Verify with Self-Test

```bash
python -m aaa_mcp.selftest
```

A passing self-test confirms the server loads, tools are registered, and baseline health contracts are intact.

---

## Zero-Install: System Prompt Only

If you cannot run a server, copy `333_APPS/L1_PROMPT/SYSTEM_PROMPT.md` into any LLM's system settings. This gives L1 governance (prompting only - no cryptographic sealing, no VAULT999, no tool calls).

```bash
cat 333_APPS/L1_PROMPT/SYSTEM_PROMPT.md | pbcopy   # macOS
cat 333_APPS/L1_PROMPT/SYSTEM_PROMPT.md | xclip    # Linux
```
