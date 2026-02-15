# arifOS MCP Bridge Server

Wraps the existing arifOS REST API into a proper MCP protocol server (SSE transport) so Claude.ai can discover and call tools.

## The Problem

Your current server at `aaamcp.arif-fazil.com` is a **REST API** (FastAPI). Claude.ai's MCP connector expects the **MCP wire protocol** (SSE or Streamable HTTP). That's why tools don't show up — Claude connects, but can't do the MCP handshake.

## The Fix

This bridge server speaks MCP protocol and proxies tool calls to your existing REST API.

```
Claude.ai  →  MCP Bridge (SSE)  →  arifOS REST API
              (this server)        (aaamcp.arif-fazil.com)
```

## Deploy on Railway

### Option A: Replace current service

1. Add these 3 files to your arifOS repo (or a new repo)
2. Set Railway to build from this directory
3. Set env var: `ARIFOS_API_URL=https://aaamcp.arif-fazil.com` (or internal Railway URL)
4. Railway auto-sets `PORT`

### Option B: New Railway service alongside existing

1. Create new service in same Railway project
2. Point it to this repo/directory
3. Set env var: `ARIFOS_API_URL=http://arifos.railway.internal:PORT` (use internal networking)
4. Set custom domain or use Railway-provided URL

### After Deploy

1. Go to **claude.ai → Settings → Integrations**
2. Remove old AAA MCP connector
3. Add new connector: `https://YOUR-RAILWAY-URL/sse`
4. **Start a new chat** (tools load at chat start)

## Tools Exposed

| Tool | Stage | Description |
|------|-------|-------------|
| `forge` | 000→999 | Full constitutional pipeline with vault seal |
| `think` | 000→333 | AGI-only, no sealing |
| `init` | 000 | Initialize session |
| `search` | 111 | Reality grounding |
| `reason` | 222-333 | Mind processing |
| `empathy` | 555 | Heart processing |
| `align` | 444 | Constitutional alignment |
| `reflect` | 777 | APEX judgment |
| `seal` | 999 | Vault seal |
| `health` | — | Server health check |
| `vault_query` | — | Query audit ledger |
| `reality_search` | — | Axiom engine |

## Local Test

```bash
pip install -r requirements.txt
ARIFOS_API_URL=https://aaamcp.arif-fazil.com python server.py
# → Server runs on http://localhost:8000/sse
```

Then test with MCP Inspector:
```bash
npx @modelcontextprotocol/inspector
# Connect to http://localhost:8000/sse
```

## Important Notes

- The REST API endpoints (`/forge`, `/think`, etc.) must match your actual server routes
- If your API uses different endpoint names, update `server.py` accordingly
- The bridge adds ~10ms overhead per call (just proxying JSON)
