<div align="center">

<img src="https://raw.githubusercontent.com/ariffazil/arifOS/main/sites/library/static/img/banner_sovereign.png" width="100%" alt="arifOS Ecosystem Banner">

# arifosmcp
### Production-grade constitutional MCP runtime for arifOS

**[Theory](https://github.com/ariffazil/arifOS)** • **[Live MCP](https://arifosmcp.arif-fazil.com/mcp)** • **[Health](https://arifosmcp.arif-fazil.com/health)** • **[Status](https://arifosmcp.arif-fazil.com/status)** • **[Tools](https://arifosmcp.arif-fazil.com/tools)**

*Ditempa Bukan Diberi*

[![Status](https://img.shields.io/badge/Status-Healthy-00b894.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/health)
[![Release](https://img.shields.io/badge/Release-2026.03.12--FORGED-blue.svg?style=flat-square)](https://github.com/ariffazil/arifosmcp/commits/main)
[![Public Tools](https://img.shields.io/badge/Public%20Tools-10-success.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/tools)
[![License](https://img.shields.io/badge/License-AGPL%203.0-lightgrey.svg?style=flat-square)](./LICENSE)

</div>

`arifosmcp` is the live execution engine of arifOS: a governed MCP server that exposes a public tool surface, applies the constitutional kernel, persists continuity and ledger state, and serves production telemetry for agents and operators.

This repository is the production deploy source for the VPS at `/srv/arifosmcp`.

## Live State

Last verified on `2026-03-13`.

| Item | Current state |
| --- | --- |
| GitHub `main` | `0fe45827` |
| Public MCP version | `2026.03.12-FORGED` |
| Public transport | `streamable-http` |
| Public tools | `10` |
| Runtime health | `healthy` |
| Continuity signing | `configured` |
| Governed continuity | `enabled` |
| OpenClaw | forged image live and healthy |

Public endpoints:

- `https://arifosmcp.arif-fazil.com/mcp`
- `https://arifosmcp.arif-fazil.com/health`
- `https://arifosmcp.arif-fazil.com/status`
- `https://arifosmcp.arif-fazil.com/tools`
- `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json`

## Public Tool Surface

The live public registry currently exposes these `10` tools:

1. `arifOS_kernel`
2. `search_reality`
3. `ingest_evidence`
4. `session_memory`
5. `audit_rules`
6. `check_vital`
7. `bootstrap_identity`
8. `init_anchor_state`
9. `verify_vault_ledger`
10. `open_apex_dashboard`

Do not manually maintain this list in multiple places. The source of truth is the runtime public registry and generated specs.

## What Is New In The Current Forged State

- `init_anchor_state` is now on the public tool surface.
- `/status` is live as a zero-JS ops truth page.
- `auth_context.actor_id` is normalized at the runtime boundary for kernel verification.
- production continuity is now backed by a persistent file secret, not ephemeral fallback.
- OpenClaw is running on the forged image with native `kimi` and `opencode`.

## Repository Topography

| Path | Purpose |
| --- | --- |
| `arifosmcp/runtime/` | FastAPI/FastMCP runtime surface, public registry, routes, resources |
| `core/` | constitutional kernel, floors, judgment, vault and continuity logic |
| `spec/` | generated public discovery documents |
| `infrastructure/` | VPS dossiers, Docker and OpenClaw forge assets |
| `tests/` | runtime, contract and integration validation |

## Local Development

Use the project virtualenv or `uv` workflow.

```bash
cd /srv/arifosmcp
uv sync --dev
. .venv/bin/activate
python -m arifosmcp.runtime stdio
```

Run targeted checks:

```bash
pytest -q tests/test_kernel_contract_alignment.py
pytest -q tests/test_runtime_capability_map.py
pytest -q tests/integration/test_health_metrics.py
```

## Production Deploy

The canonical production guide is [DEPLOY.md](/srv/arifosmcp/DEPLOY.md).

Fast path on the VPS:

```bash
cd /srv/arifosmcp
git pull --ff-only
python scripts/generate_public_specs.py
docker compose up -d --build arifosmcp
curl -fsS https://arifosmcp.arif-fazil.com/health
curl -fsS https://arifosmcp.arif-fazil.com/status?format=json
curl -fsS https://arifosmcp.arif-fazil.com/tools
```

For the full live topology and container map, see [infrastructure/VPS_ARCHITECTURE.md](/srv/arifosmcp/infrastructure/VPS_ARCHITECTURE.md).
