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
> Version: `2026.03.10-SEAL`

If you're wondering what an "MCP Server" is: **It's the bridge that connects an AI (like Claude or Cursor) to arifOS.** 

The Model Context Protocol (MCP) is a standard that lets AI models securely use external tools. arifOS runs its own MCP server so that any AI can connect to it and instantly be bound by the 13 constitutional floors.

## Runtime Architecture

- **Primary Entrypoint:** `python -m arifosmcp.runtime`
- **Session Registry:** `arifosmcp.runtime.sessions` (Centralized state)
- **Tool Surface:** Layered (`chatgpt` public interface + `full` APEX-G internal stack)
- **Production transport:** Streamable HTTP (`/mcp`) — Current MCP standard
- **Local transport:** stdio — For Claude Desktop, Cursor IDE
- **Constitutional envelope:** 333 axioms + 13 laws + APEX-G 5-layer stack
- **Port:** 8080 (default)

## Launch commands (How to run it)

Depending on where you are running the AI, you start the server differently:

```bash
# Local stdio (for Claude Desktop, Cursor)
python -m arifosmcp.runtime stdio

# Streamable HTTP (production - recommended)
HOST=0.0.0.0 PORT=8080 python -m arifosmcp.runtime http
```

## Public Interface (`ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt`)

| Tool | Role |
|------|------|
| `arifOS_kernel` | One-call governed constitutional execution entrypoint. |
| `search_reality` | External grounding and source discovery. |
| `ingest_evidence` | Read-only evidence fetch/intake. |
| `session_memory` | Session context and reasoning artifact memory. |
| `audit_rules` | Read-only constitutional rule audit. |
| `check_vital` | Read-only system health snapshot. |
| `open_apex_dashboard` | Opens the APEX dashboard iframe in MCP-compatible clients. |

Legacy aliases: `arifOS.kernel` and `metabolic_loop_router` refer to `arifOS_kernel`.

`arifOS_kernel` accepts a claimed `actor_id` for routing intent, but continuity is established by `auth_context`. Run `init_anchor_state` for the first anchored call, then pass the returned `auth_context` into subsequent governed kernel calls.

## Canonical 10-Tool APEX-G Stack (`full` profile)

The core constitutional assembly line. Every tool returns a `RuntimeEnvelope`.

| Stage | Tool | Role |
|-------|------|------|
| 000 | `init_anchor_state` | Governed session bootstrap. Mints auth chain. |
| 111 | `integrate_analyze_reflect` | Problem framing and integrative analysis. |
| 333 | `reason_mind_synthesis` | Multi-step reasoning with Eureka synthesis slot. |
| 444 | `metabolic_loop_router` | Full 000→999 pipeline orchestrator (internal legacy alias for `arifOS_kernel`). |
| 555 | `vector_memory_store` | BBB associative vector memory (store/recall/search/forget). |
| 666A | `assess_heart_impact` | Empathy and ethical safety engine. |
| 666B | `critique_thought_audit` | Adversarial internal thought audit. |
| 777 | `quantum_eureka_forge` | Sandboxed discovery actuator. Proposes, never executes. |
| 888 | `apex_judge_verdict` | Constitutional judgment. Produces governance token. |
| 999 | `seal_vault_commit` | Immutable VAULT999 ledger sealing. Append-only. |

### Stage 222 (Reality Verification)

The kernel path now contains a `222_REALITY` verification stage between `333_MIND` and `666_HEART`. Grounding status/score are included in judge synthesis and sealed telemetry for replay.

### Contrast Analytics Status

The runtime currently returns per-call deltas and telemetry, but not a dedicated turn-to-turn contrast score. Historical analysis is available in `full` profile through `trace_replay` over sealed vault telemetry; explicit semantic contrast fields are a future enhancement.

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
| `ui://apex/dashboard-v2.html` | APEX Sovereign Dashboard HTML template (MCP App) |

## APEX Sovereign Dashboard

The APEX Sovereign Dashboard visualises the **APEX Theorem** (`G^dagger = A * P * X * E^2 * (Delta S / C)`) in real time.

**Live:** [arifosmcp.arif-fazil.com/dashboard/](https://arifosmcp.arif-fazil.com/dashboard/)

URL mapping:
- **Widget domain / app origin**: `https://arifosmcp.arif-fazil.com`
- **MCP endpoint**: `https://arifosmcp.arif-fazil.com/mcp`
- **Dashboard page**: `https://arifosmcp.arif-fazil.com/dashboard/`
- **Dashboard telemetry API**: `https://arifosmcp.arif-fazil.com/api/governance-status`

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
