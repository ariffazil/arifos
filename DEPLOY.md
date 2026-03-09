# arifOS Deployment Guide

This is the canonical operator guide for deploying `arifosmcp` on a VPS and connecting it to ChatGPT.

## 1) Canonical Architecture

Production in this repo is:

- `docker-compose.yml` as the canonical VPS stack
- Traefik as the edge router and TLS terminator
- `arifosmcp.runtime.server:app` as the canonical MCP ASGI app
- Streamable HTTP on `/mcp`
- Health and operator routes on the same host:
  - `/health`
  - `/.well-known/mcp/server.json`
  - `/dashboard/`

The canonical public surfaces are:

- MCP endpoint: `https://arifosmcp.arif-fazil.com/mcp`
- Health: `https://arifosmcp.arif-fazil.com/health`
- Discovery manifest: `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json`
- Dashboard: `https://arifosmcp.arif-fazil.com/dashboard/`
- Docs: `https://arifos.arif-fazil.com`

## 2) Blessed Runtime Path

Use one of these two paths only:

### VPS production

```bash
docker compose pull
docker compose up -d --build
```

This starts Traefik, Postgres, Redis, Qdrant, Ollama, OpenClaw, monitoring, and the public `arifosmcp` service.

### Direct runtime without Docker

```bash
python -m arifosmcp.runtime http
```

Legacy compatibility entrypoints under `arifosmcp.transport` still exist, but they are not the recommended public ChatGPT deployment path.

## 3) Required Environment

Start from `.env.docker.example` and create `.env.docker`.

Minimum production values:

```env
PORT=8080
HOST=0.0.0.0
AAA_MCP_TRANSPORT=http
ARIFOS_MCP_PATH=/mcp
ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt
ARIFOS_PUBLIC_BASE_URL=https://arifosmcp.arif-fazil.com
ARIFOS_WIDGET_DOMAIN=https://arifosmcp.arif-fazil.com
ARIFOS_GOVERNANCE_SECRET=CHANGE_ME_TO_A_LONG_RANDOM_SECRET
POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD
GRAFANA_PASSWORD=CHANGE_ME_GRAFANA_PASSWORD
WEBHOOK_SECRET=CHANGE_ME_WEBHOOK_SECRET
OPENCLAW_RESTART_TOKEN=CHANGE_ME_OPENCLAW_RESTART_TOKEN
OPENCLAW_GATEWAY_TOKEN=CHANGE_ME_OPENCLAW_GATEWAY_TOKEN
```

Notes:

- `ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt` is the intended public surface.
- `ARIFOS_PUBLIC_BASE_URL` and `ARIFOS_WIDGET_DOMAIN` should be the root origin only, not `/mcp` and not `/dashboard/`.
- Provider API keys are optional unless your workload actually uses them.

## 4) VPS Deployment

### Prerequisites

- Ubuntu VPS with Docker Engine and Docker Compose
- DNS for `arifosmcp.arif-fazil.com`
- Ports `80` and `443` open
- Repository cloned on VPS

### Deploy

```bash
git pull --ff-only origin main
cp .env.docker.example .env.docker
docker compose pull
docker compose up -d --build
```

### Check containers

```bash
docker compose ps
docker compose logs --tail=100 arifosmcp
docker compose logs --tail=100 traefik
```

### Local verification on VPS

```bash
curl -fsS http://127.0.0.1:8080/health
curl -i http://127.0.0.1:8080/.well-known/mcp/server.json
curl -i -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## 5) Traefik and DNS

`docker-compose.yml` already contains the public router for:

- `Host(\`arifosmcp.arif-fazil.com\`)`

This repo’s canonical public deployment uses Traefik labels in Compose, not a separate production Coolify compose file.

Cloudflare:

- `Proxied` can work for the public host.
- If you are debugging SSE or transport behavior, temporarily switch to DNS-only to remove Cloudflare from the path.
- A `406 Not Acceptable` from `/mcp` is an application-layer issue, not a TLS or DNS issue.

## 6) ChatGPT Connector Setup

Official OpenAI guidance for ChatGPT Apps and Developer Mode is:

- Create the connector with the HTTPS URL plus `/mcp`
- ChatGPT supports either Streamable HTTP or HTTP/SSE transports

For this repo, use:

- Connector URL: `https://arifosmcp.arif-fazil.com/mcp`

Do not use:

- `https://arifosmcp.arif-fazil.com`
- `https://arifosmcp.arif-fazil.com/dashboard/`
- `https://arifosmcp.arif-fazil.com/mcp/extra`

Widget domain for app resources is the root origin:

- `https://arifosmcp.arif-fazil.com`

## 7) Accept Header Compatibility

The public runtime uses:

```python
mcp.http_app(
    path="/mcp",
    json_response=True,
    stateless_http=True,
)
```

That means the upstream MCP SDK is in JSON-only Streamable HTTP mode, which requires `application/json` in the request `Accept` header.

Important:

- If the client sends `Accept: application/json`, `/mcp` works.
- If the client omits `Accept`, the compatibility middleware now injects `application/json`.
- If the client sends a wildcard like `Accept: */*`, the compatibility middleware now appends `application/json`.

This closes the 406 gap that still appeared on the live VPS when the client did not explicitly advertise JSON.

### Live diagnostic

If you see this:

```bash
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

and receive `406 Not Acceptable`, then one of these is true:

1. The VPS is still running an older image that predates the Accept compatibility fix.
2. The reverse proxy is not forwarding to the current runtime.
3. The client is sending an incompatible `Accept` header and the new build is not yet deployed.

## 8) Tool Surface and Health Output

`/health` intentionally reports the canonical public tool registry, not every internal or legacy registration point.

With:

```env
ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt
```

the expected public surface is the stable 7-tool operator set:

- `arifOS.kernel`
- `search_reality`
- `ingest_evidence`
- `session_memory`
- `audit_rules`
- `check_vital`
- `open_apex_dashboard`

So this is expected:

- `/health` reports `tools_loaded: 7`

If you switch to the internal `full` profile, additional compatibility and ACLIP tools may be registered, but that is not the intended public ChatGPT surface.

## 8.5) Wisdom Quotes System

arifOS includes a dual-layer wisdom injection system:

### 33-Quote Deterministic Registry (Primary)
- Floor F2 failure → Carl Sagan: "Extraordinary claims require extraordinary evidence."
- Floor F7 failure → Socrates: "The only true wisdom is in knowing you know nothing."
- Stage 999 SEAL → "DITEMPA, BUKAN DIBERI."

### 99-Quote Semantic Corpus (Secondary)
- Collection: `arifos_wisdom_quotes` (Qdrant)
- Model: BAAI/bge-m3 (1024-dim, multilingual)
- Categories: scar(20), triumph(20), paradox(20), wisdom(15), power(10), love(10), seal(4)
- Access: `retrieve_wisdom(query, category, n_results)`
- Embed script: `python scripts/embed_wisdom_quotes.py`

### Integration
Every `arifOS.kernel` response includes:
```json
"philosophy": {
  "quote_id": "W8",
  "quote": "Extraordinary claims require extraordinary evidence.",
  "author": "Carl Sagan",
  "category": "wisdom"
}
```

To re-embed wisdom corpus after updates:
```bash
docker exec arifosmcp_server python3 scripts/embed_wisdom_quotes.py
```

## 9) Answers To Deployment Blockers

### Q1: What is the intended MCP transport architecture?

Use `arifosmcp.runtime.server:app` and `python -m arifosmcp.runtime http`.

- `FastMCP` is the canonical transport layer.
- `/mcp` is the canonical public protocol endpoint.
- `arifosmcp.transport.*` contains compatibility and older transport surfaces, not the preferred public deployment target.

### Q2: How to disable SDK-level Accept validation?

Do not bypass the SDK by monkey-patching it first.

The correct first-line configuration is already:

- `json_response=True`

That maps through FastMCP into the SDK’s JSON-only mode. The remaining operational issue is making sure the request `Accept` header includes `application/json`. This repo now handles missing and wildcard Accept values before the SDK validates them.

### Q3: What is the canonical deployment method?

For production:

- `docker-compose.yml`
- Traefik
- `uvicorn arifosmcp.runtime.server:app`

For local/manual use:

- `python -m arifosmcp.runtime http`

### Q4: How to properly expose the MCP endpoint for ChatGPT?

Expose:

- `https://arifosmcp.arif-fazil.com/mcp`

ChatGPT connector setup should point exactly there. Keep `/health`, discovery, and `/dashboard/` on the same origin.

### Q5: Does `json_response=True` actually configure the underlying SDK transport?

Yes.

In the installed FastMCP codepath, `FastMCP.http_app(..., json_response=True)` flows into `create_streamable_http_app(..., json_response=True)`, which configures the underlying session manager and SDK transport for JSON-only mode.

The remaining 406 problem was not that `json_response=True` was ignored; it was that the incoming request still needed to advertise JSON in `Accept`.

## 10) Validation Checklist

Run these after every deploy:

```bash
curl -fsS https://arifosmcp.arif-fazil.com/health
curl -fsS https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json
curl -i https://arifosmcp.arif-fazil.com/dashboard/
curl -i -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Expected:

- `/health` returns `200`
- discovery manifest returns `200`
- `/dashboard/` returns `200`
- `POST /mcp` returns `200`

`GET /mcp` may return `405` in stateless HTTP mode. That alone is not a deployment failure.

## 11) Targeted Local Checks

```bash
ruff check arifosmcp/runtime/fastmcp_ext/transports.py arifosmcp/runtime/server.py
pytest tests/test_http_accept_compat.py::test_appends_json_accept_to_wildcard -q
pytest tests/test_dockerfile_runtime.py::test_canonical_vps_env_template_declares_public_profile_and_governance_secret -q
```

## 12) Sources

- OpenAI Apps SDK quickstart: add your connector with HTTPS + `/mcp`
- OpenAI Apps SDK build guide: MCP server must be publicly reachable over HTTPS
- OpenAI MCP/connectors guide: remote MCP servers work with Streamable HTTP or HTTP/SSE

Forged, not given.
