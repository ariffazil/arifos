---
id: mcp-server
title: MCP Server
sidebar_position: 2
description: Technical reference for the canonical arifOS AAA MCP runtime.
---

# arifOS AAA MCP Server

> Registry ID: `io.github.ariffazil/arifos-mcp`
> Live base URL: `https://arifosmcp.arif-fazil.com`
> Runtime module: `arifosmcp.runtime`
> Version: `2026.03.08`

If you're wondering what an "MCP Server" is: **It's the bridge that connects an AI (like Claude or Cursor) to arifOS.** 

The Model Context Protocol (MCP) is a standard that lets AI models securely use external tools. arifOS runs its own MCP server so that any AI can connect to it and instantly be bound by the 13 constitutional floors.

## Runtime profile

- **Production transport:** Streamable HTTP (`/mcp`) — Current MCP standard
- **Local transport:** stdio — For Claude Desktop, Cursor IDE
- **Constitutional envelope:** 333 axioms + 13 laws + APEX-G 5-layer stack
- **Port:** 8080 (default)
- **Current protocol version:** `2025-11-25`
- **Supported protocol versions:** `2025-11-25`, `2025-03-26`

## Version negotiation

Protocol version is negotiated during `initialize` and fixed per session.
If a client sends an unsupported version, the server returns a JSON-RPC error and no session is created.

## Launch commands (How to run it)

Depending on where you are running the AI, you start the server differently:

```bash
# Local stdio (for Claude Desktop, Cursor)
python -m arifosmcp.runtime stdio

# Streamable HTTP (production - recommended)
HOST=0.0.0.0 PORT=8080 python -m arifosmcp.runtime http
```

## Canonical 10-Tool APEX-G Stack

The core constitutional assembly line. Every tool returns a `RuntimeEnvelope`.

| Stage | Tool | Role |
|-------|------|------|
| 000 | `init_anchor_state` | Governed session bootstrap. Mints auth chain. |
| 111 | `integrate_analyze_reflect` | Problem framing and integrative analysis. |
| 333 | `reason_mind_synthesis` | Multi-step reasoning with Eureka synthesis slot. |
| 444 | `metabolic_loop_router` | Full 000→999 pipeline orchestrator. |
| 555 | `vector_memory_store` | BBB associative vector memory (store/recall/search/forget). |
| 666A | `assess_heart_impact` | Empathy and ethical safety engine. |
| 666B | `critique_thought_audit` | Adversarial internal thought audit. |
| 777 | `quantum_eureka_forge` | Sandboxed discovery actuator. Proposes, never executes. |
| 888 | `apex_judge_verdict` | Constitutional judgment. Produces governance token. |
| 999 | `seal_vault_commit` | Immutable VAULT999 ledger sealing. Append-only. |

### Additional Tool

| Tool | Role |
|------|------|
| `open_apex_dashboard` | Opens the APEX Sovereign Dashboard iframe in compatible MCP clients (MCP App). |

## Interactive Resources

The server exposes read-only resources for LLM and human inspection:

| URI | Content |
|-----|---------|
| `canon://index` | High-level canon map |
| `canon://tools` | APEX-G 10-tool table |
| `canon://floors` | All 13 constitutional floors |
| `governance://law` | Constitutional law summary |
| `schema://tools/output` | RuntimeEnvelope output schema |
| `vault://latest` | Last 5 sealed VAULT999 entries |
| `telemetry://summary` | Live telemetry shape |
| `ui://apex-dashboard/view.html` | APEX Sovereign Dashboard HTML (MCP App) |

## APEX Sovereign Dashboard

The APEX Sovereign Dashboard visualises the **APEX Theorem** ($G^\dagger = A \cdot P \cdot X \cdot E^2 \cdot \frac{\Delta S}{C}$) in real time.

**Live:** [arifosmcp.arif-fazil.com/dashboard/](https://arifosmcp.arif-fazil.com/dashboard/)

## Deployment files to keep aligned

- `Dockerfile`
- `docker-compose.yml`
- `.github/workflows/deploy-cloudflare.yml`
- `server.json`

## Required secrets (minimum)

- `ARIF_SECRET` (For auth chain signing)
- `DATABASE_URL` (For VAULT999 ledger)
- `REDIS_URL` (For session persistence)

Optional web grounding:

- `PPLX_API_KEY` (Perplexity)
- `BRAVE_API_KEY` (Brave Search)
- `JINA_API_KEY` (Jina Reader)
