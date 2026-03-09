# Deployment Guide

This is the canonical VPS deployment path for the current repo state.

## Canonical Files

- Compose: `docker-compose.yml`
- Production image: `Dockerfile`
- Env template: `.env.docker.example`
- Runtime entrypoint: `arifosmcp.runtime.server:app`
- Public MCP endpoint: `/mcp`

`docker-compose.override.yml` is for local development only. Do not use it for VPS agents.

## Public Runtime Contract

- Internal container port: `8080`
- Host bind in compose: `127.0.0.1:8080:8080`
- Reverse proxy target: `http://127.0.0.1:8080`
- MCP transport: Streamable HTTP on `/mcp`
- Health endpoint: `/health`
- Tool discovery: `/tools`
- Dashboard: `/dashboard/`

The public profile defaults to `ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt`, which exposes:

- `metabolic_loop_router`
- `search_reality`
- `ingest_evidence`
- `audit_rules`
- `check_vital`
- `open_apex_dashboard`

## VPS Agent Flow

1. Pull the repo to `/srv/arifOS`.
2. Copy `.env.docker.example` to `.env.docker` if no production env file exists.
3. Replace at minimum:
   - `ARIFOS_GOVERNANCE_SECRET`
   - `POSTGRES_PASSWORD`
   - `GRAFANA_PASSWORD`
   - `WEBHOOK_SECRET`
4. Start the stack:

```bash
docker compose up -d --build
```

5. Verify locally on the VPS:

```bash
curl -fsS http://127.0.0.1:8080/health
curl -fsS http://127.0.0.1:8080/tools
curl -fsS http://127.0.0.1:8080/.well-known/mcp/server.json
```

6. Verify through the public domain:

```bash
curl -i https://arifosmcp.arif-fazil.com/health
curl -i https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json
curl -sS https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"deploy-check","version":"1.0"}}}'
```

## Mounted Config Sources

The compose file expects these repo paths to exist on the VPS clone:

- `deployment/hooks.json`
- `infrastructure/deploy_from_git.sh`
- `infrastructure/prometheus/prometheus.yml`
- `infrastructure/grafana/datasources/prometheus.yml`

## Notes

- `prod.fastmcp.json` now matches `/mcp` without a trailing slash.
- `ARIFOS_GOVERNANCE_SECRET` is required in production for stable auth continuity across restarts and replicas.
- If you need the full internal tool surface, override `ARIFOS_PUBLIC_TOOL_PROFILE=full` in `.env.docker`.
