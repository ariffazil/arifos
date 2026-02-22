---
id: mcp-server
title: MCP Server
sidebar_position: 2
description: Install, configure, and connect to the arifOS MCP server via stdio, SSE, or HTTP.
---

# MCP Server

> Source: [`README.md`](https://github.com/ariffazil/arifOS/blob/main/README.md) · [`aaa_mcp/server.py`](https://github.com/ariffazil/arifOS/blob/main/aaa_mcp/server.py) · [`server.py`](https://github.com/ariffazil/arifOS/blob/main/server.py)  
> PyPI: [`pip install arifos`](https://pypi.org/project/arifos/)

arifOS speaks the **Model Context Protocol (MCP)** — the open standard for LLM tool use. Any MCP-compatible client (Claude Desktop, Cursor, OpenClaw, ChatGPT developer mode) can connect to it.

---

## Installation

### Option A — PyPI (fastest)

```bash
pip install arifos
```

### Option B — From source (recommended for contributors)

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

The `server.py` at repo root runs **22 tools** in one process — 9 AAA-MCP governance tools + 10 ACLIP-CAI sensory tools + ChatGPT search/fetch tools.

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

## The 9 Canonical Governance Tools

All tools chain via `session_id`. Each enforces specific constitutional floors.

| # | Tool | Verb | Stages | Floors Checked |
|:--|:--|:--|:--|:--|
| 1 | `_init_` / `ANCHOR` | Init & authorise | 000 | F11, F12 |
| 2 | `_agi_` / `REASON` | Think & hypothesise | 222 | F2, F8 |
| 3 | `INTEGRATE` | Map & ground | 333 | F7, F10 |
| 4 | `RESPOND` | Draft & plan | 444 | F4, F6 |
| 5 | `VALIDATE` | Impact check | 555 | F5, F6 |
| 6 | `ALIGN` | Ethics check | 666 | F9 |
| 7 | `FORGE` | Synthesise code | 777 | F2, F4 |
| 8 | `_apex_` / `AUDIT` | Verdict & consensus | 888 | F3, F11 |
| 9 | `_vault_` / `SEAL` | Commit to vault | 999 | F1, F3 |

Additional tools in the unified server:

- **`reality_search`** — Web search via Brave API (F7, F10 grounding)
- **ACLIP-CAI C0–C9** — Sensory/observability tools

---

## Environment Variables

| Variable | Required | Default | Description |
|:--|:--|:--|:--|
| `ARIF_SECRET` | Recommended | `""` | Authentication header for SSE/HTTP transports |
| `BRAVE_API_KEY` | Optional | `""` | Enables `reality_search` web grounding |
| `OPENAI_API_KEY` | Optional | `""` | ChatGPT search/fetch tools in unified server |
| `DATABASE_URL` | Optional | SQLite | VAULT999 PostgreSQL connection string |
| `REDIS_URL` | Optional | In-memory | Session state Redis URL |
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

# Response:
# {"status":"healthy","version":"2026.2.19","reality_index":0.94,"floors_passing":13}

# Governance metrics
curl https://arifosmcp.arif-fazil.com/metrics.json
```

---

## Verify with Self-Test

```bash
python -m aaa_mcp.selftest
```

A passing self-test confirms all 9 tools are reachable, at least one tool produces `SEAL`, and F12 injection scanning is active.

---

## Zero-Install: System Prompt Only

If you cannot run a server, copy `333_APPS/L1_PROMPT/SYSTEM_PROMPT.md` into any LLM's system settings. This gives L1 governance (prompting only — no cryptographic sealing, no VAULT999, no tool calls).

```bash
cat 333_APPS/L1_PROMPT/SYSTEM_PROMPT.md | pbcopy   # macOS
cat 333_APPS/L1_PROMPT/SYSTEM_PROMPT.md | xclip    # Linux
```
