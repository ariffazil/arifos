---
id: mcp-server
title: MCP Server
sidebar_position: 2
description: Technical reference for the canonical arifOS AAA MCP runtime.
---

# arifOS AAA MCP Server

> Registry ID: `io.github.ariffazil/arifos-mcp`
> Live base URL: `https://arifosmcp.arif-fazil.com`
> Runtime module: `arifos_aaa_mcp`
> Version: `2026.2.23`

## Runtime profile

- Primary transport: SSE (`/sse`)
- Fallback transport: Streamable HTTP (`/mcp`)
- Local transport: stdio
- Constitutional envelope: 333 axioms + 13 laws + APEX dials

## Launch commands

```bash
# stdio
python -m arifos_aaa_mcp stdio

# SSE
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp sse

# HTTP MCP
PORT=8089 python -m arifos_aaa_mcp http
```

## Canonical MCP surface

### Tools (13)

- `anchor_session`
- `reason_mind`
- `recall_memory`
- `simulate_heart`
- `critique_thought`
- `judge_soul`
- `forge_hand`
- `seal_vault`
- `search_reality`
- `fetch_content`
- `inspect_file`
- `audit_rules`
- `check_vital`

### Resources (2)

- `arifos://aaa/schemas`
- `arifos://aaa/full-context-pack`

### Prompt (1)

- `arifos.prompt.aaa_chain`

## Deployment files to keep aligned

- `Dockerfile`
- `start-trinity.sh`
- `docker-compose.yml`
- `deployment/docker-compose.vps.yml`
- `.github/workflows/deploy.yml`
- `server.json`

## Required secrets (minimum)

- `ARIF_SECRET` or `ARIF_JWT_SECRET`
- `DATABASE_URL`
- `REDIS_URL`

Optional web grounding:

- `PPLX_API_KEY` (preferred) or `PERPLEXITY_API_KEY`
- `PPLX_MODEL` (default `sonar-pro`)
- `BRAVE_API_KEY` (fallback)
