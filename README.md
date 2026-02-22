# arifOS — DITEMPA BUKAN DIBERI
<!-- mcp-name: io.github.ariffazil/arifos-mcp -->

arifOS is a Python governance kernel for AI systems.

It does one core job: decide whether an AI output is allowed to proceed.

It does this through:
- a 5-organ kernel (INIT, AGI, ASI, APEX, VAULT),
- a 13-floor constitutional policy layer,
- a governed MCP server interface for tools and clients.

If you are non-technical, read this page top to bottom and you will have the complete repo picture.

## What arifOS Is
- It is not a hardware operating system.
- It is an intelligence governance kernel for AI cognition.
- It can block unsafe actions (`VOID`), pause for human ratification (`HOLD` / `SABAR`), or approve (`SEAL`).

## What Problem It Solves
Without governance, AI systems can:
- produce high-confidence wrong answers,
- suggest irreversible operations without explicit authorization,
- blur uncertainty and authority boundaries.

arifOS enforces explicit guardrails before output is accepted.

## Core Concepts
1. `5 organs`:
- `init_session` (INIT)
- `agi_cognition` (AGI)
- `asi_empathy` (ASI)
- `apex_verdict` (APEX)
- `vault_seal` (VAULT)

2. `13 constitutional floors`:
- F1 to F13 are evaluated for every governed decision path.
- Critical floor failures can force `VOID` or `HOLD`.

3. `000 → 999 pipeline`:
- Decisions move through a staged governance flow and end in an auditable verdict.

## Repo Reality (Ground Truth as of 2026-02-22)
- Package version: `2026.2.22` (`pyproject.toml`)
- Python baseline: `>=3.12` (`pyproject.toml`)
- FastMCP runtime pinned: `fastmcp==3.0.1`
- Registry server identity: `io.github.ariffazil/arifos-mcp` (`server.json`)
- Registry package entry: PyPI `arifos` + OCI image metadata (`server.json`)
- Deployment workflow: `.github/workflows/deploy.yml` (VPS/Coolify path)
- Legacy Railway deploy workflow removed from active workflows

Live endpoint configured in repo:
- `https://arifosmcp.arif-fazil.com`
- Health check path: `/health`

Observed from this environment on 2026-02-22:
- `GET https://arifosmcp.arif-fazil.com/health` returned `503 Service Unavailable` at check time.

## Exposed MCP Surface (Current)
From local `fastmcp inspect fastmcp.json --format mcp`, current server exposes:

Canonical kernel tools:
- `init_session`
- `agi_cognition`
- `asi_empathy`
- `apex_verdict`
- `vault_seal`

Utility tools:
- `search`
- `fetch`
- `analyze`
- `system_audit`

Container/ops tools:
- `container_list`
- `container_restart`
- `container_logs`
- `container_exec`
- `sovereign_health`

Resource exposed:
- `capability://modules`

Note:
- Legacy 9-verb naming exists as compatibility aliases at REST/adapter level.
- Canonical runtime is the 5-organ kernel toolset above.

## Quick Start (Non-Coder Friendly)
If you only want to run it locally:

1. Install Python 3.12+.
2. Open terminal in this repo.
3. Run:

```bash
pip install -e .
python -m aaa_mcp
```

This starts MCP in `stdio` mode (local client mode).

Alternative transports:

```bash
python -m aaa_mcp sse
python -m aaa_mcp http
```

Script entry points (also valid after install):
- `arifos`
- `aaa-mcp`
- `arifos-mcp`

## FastMCP Profiles
Config files in repo:
- `fastmcp.json` (default HTTP profile at `/mcp/` on `0.0.0.0:8080`)
- `dev.fastmcp.json`
- `prod.fastmcp.json`

Run examples:

```bash
fastmcp run dev.fastmcp.json
fastmcp run prod.fastmcp.json
fastmcp run fastmcp.json
```

Smoke checks:

```bash
fastmcp inspect fastmcp.json --format mcp
fastmcp list aaa_mcp/server.py:mcp --json
```

## Deployment (Current Path)
Primary deployment target is VPS/Coolify.

Active GitHub workflow:
- `.github/workflows/deploy.yml`

Required GitHub Actions secrets:
- `VPS_HOST`
- `VPS_USERNAME`
- `VPS_SSH_KEY`

Domain configured for MCP:
- `arifosmcp.arif-fazil.com`

## Status and Humility
This repo contains production, experimental, and research layers.

What is stable:
- Core governance/kernel structure.
- MCP runtime entrypoints.
- FastMCP pinning and conformance workflow structure.

What is still moving:
- CI reliability and housekeeping debt across legacy docs.
- Some historical documents still reference old Railway-era context (non-runtime docs).

## For Zero-Context Readers
If you remember only one thing:

arifOS is a constitutional gate in front of AI output.
It decides if a response is allowed, delayed, or blocked, and records that decision.

## Links
- Repository: `https://github.com/ariffazil/arifOS`
- Docs site: `https://arifos.arif-fazil.com`
- MCP endpoint domain: `https://arifosmcp.arif-fazil.com`
- Registry namespace: `io.github.ariffazil/arifos-mcp`

## License
AGPL-3.0-only (`LICENSE`).

---

DITEMPA BUKAN DIBERI — Forged, Not Given.
