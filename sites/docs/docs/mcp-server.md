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

- **Production transport:** Streamable HTTP (`/mcp`) — Current MCP standard
- **Local transport:** stdio — For Claude Desktop, Cursor IDE
- **Constitutional envelope:** 333 axioms + 13 laws + APEX dials
- **Port:** 8080 (default)

## Launch commands

```bash
# Local stdio (for Claude Desktop, Cursor)
python -m arifos_aaa_mcp stdio

# Streamable HTTP (production - recommended)
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http
```

**Why streamable HTTP?**
- Single endpoint (vs legacy SSE two-channel model)
- Cloud-native scaling
- Better firewall/proxy compatibility
- Current MCP standard (2024+)

## Canonical MCP surface

### Tools (13)

| Tool | Purpose |
|:--|:--|
| `anchor_session` | 000 INIT: Start governed session |
| `reason_mind` | 333 REASON: AGI cognition |
| `recall_memory` | 444 EVIDENCE: Memory retrieval |
| `simulate_heart` | 555 EMPATHY: Impact analysis |
| `critique_thought` | 666 ALIGN: 7-model critique |
| `judge_soul` | 777/888 APEX: Constitutional verdict |
| `forge_hand` | 888 FORGE: Execute with gates |
| `seal_vault` | 999 SEAL: Commit to ledger |
| `search_reality` | Web evidence discovery |
| `fetch_content` | Fetch raw content |
| `inspect_file` | Filesystem inspection |
| `audit_rules` | Rule compliance check |
| `check_vital` | System health metrics |

**Test live:** `curl https://arifosmcp.arif-fazil.com/health`

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
