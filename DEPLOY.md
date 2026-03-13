# arifosmcp VPS Deploy Guide

This document is the current deployment reference for the production VPS layout as of `2026-03-13`.

Production deploys are high-stakes. Apply `888_HOLD` discipline before sealing changes to live infrastructure.

## Current Topology

The live architecture is a single VPS running a `12`-container Docker Compose stack behind Traefik.

Canonical source of truth:

| Layer | Canonical path / endpoint | Notes |
| --- | --- | --- |
| Git working tree | `/srv/arifosmcp` | sole active repository on VPS |
| Persistent data root | `/opt/arifos/data` | Postgres, Redis, Qdrant, Grafana, n8n, OpenClaw, Agent Zero |
| Persistent secret root | `/opt/arifos/secrets` | file-backed continuity secret lives here |
| TLS state | `/opt/arifos/traefik/acme.json` | Traefik certificate store |
| Public base URL | `https://arifosmcp.arif-fazil.com` | main public MCP domain |
| MCP endpoint | `https://arifosmcp.arif-fazil.com/mcp` | streamable HTTP MCP |
| Health endpoint | `https://arifosmcp.arif-fazil.com/health` | capability map and runtime health |
| Status endpoint | `https://arifosmcp.arif-fazil.com/status` | no-JS ops truth page |
| Public discovery | `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json` | generated from runtime registry |

## Runtime Contract

The public MCP surface is registry-driven from `arifosmcp.runtime.public_registry`.

Current public profile:

- Version: `2026.03.12-FORGED`
- Public tool count: `10`
- Public endpoints:
  - `/mcp`
  - `/health`
  - `/status`
  - `/tools`
  - `/.well-known/mcp/server.json`
- Deploy validation sources:
  - `scripts/generate_public_specs.py`
  - targeted pytest contract checks

Current public tools:

1. `arifOS_kernel`
2. `search_reality`
3. `ingest_evidence`
4. `session_memory`
5. `audit_rules`
6. `check_vital`
7. `init_anchor_state`
8. `verify_vault_ledger`
9. `open_apex_dashboard`

Do not hand-edit public tool lists in multiple places. Update the registry and regenerate specs.

## Required Production Environment

Production is currently using the live `.env` plus Docker Compose mounts on the VPS. If you bootstrap a fresh host, create `.env.docker` from `.env.docker.example` and set production values explicitly.

Minimum required variables:

| Variable | Required value / guidance |
| --- | --- |
| `PORT` | `8080` |
| `HOST` | `0.0.0.0` |
| `AAA_MCP_TRANSPORT` | `http` |
| `ARIFOS_VERSION` | `2026.03.12-FORGED` |
| `ARIFOS_MCP_PATH` | `/mcp` |
| `ARIFOS_PUBLIC_BASE_URL` | `https://arifosmcp.arif-fazil.com` |
| `ARIFOS_WIDGET_DOMAIN` | same public origin unless intentionally split |
| `ARIFOS_GOVERNANCE_SECRET_FILE` | `/opt/arifos/secrets/governance.secret` |
| `ARIFOS_GOVERNANCE_SECRET_PREVIOUS` | previous value kept temporarily for rollover safety |
| `POSTGRES_PASSWORD` | configured |
| `OPENCLAW_ACCESS_TOKEN` | configured |
| `N8N_BASIC_AUTH_PASSWORD` | configured |
| `WEBHOOK_SECRET` | configured |
| `GF_SECURITY_ADMIN_PASSWORD` | configured |

Critical continuity note:

- `ARIFOS_GOVERNANCE_SECRET_FILE` is now the canonical production path
- do not rely on ephemeral `ARIFOS_GOVERNANCE_SECRET`
- current live secret is file-backed and readable by the `arifos` container user

## Canonical VPS Layout

Use this directory shape on the VPS:

```text
/srv/arifosmcp
├── docker-compose.yml
├── docker-compose.override.yml
├── .env
├── .env.docker
├── arifosmcp/
├── core/
├── scripts/
├── spec/
└── infrastructure/

/opt/arifos
├── data/
│   ├── agent-zero/
│   ├── grafana/
│   ├── n8n/
│   ├── ollama/
│   ├── openclaw/
│   ├── postgres/
│   ├── prometheus/
│   ├── qdrant/
│   └── redis/
├── secrets/
│   └── governance.secret
└── traefik/
    └── acme.json
```

Avoid duplicate live working trees under home directories. They increase entropy and make rollback analysis harder.

## Deploy Procedure

### 1. Prepare host

```bash
mkdir -p /srv/arifosmcp
mkdir -p /opt/arifos/data/{agent-zero,grafana,n8n,ollama,openclaw,postgres,prometheus,qdrant,redis}
mkdir -p /opt/arifos/secrets
mkdir -p /opt/arifos/traefik
touch /opt/arifos/traefik/acme.json
chmod 600 /opt/arifos/traefik/acme.json
openssl rand -hex 32 > /opt/arifos/secrets/governance.secret
chmod 600 /opt/arifos/secrets/governance.secret
chown 1000:1000 /opt/arifos/secrets/governance.secret
```

### 2. Sync repository

```bash
cd /srv/arifosmcp
git pull --ff-only
```

If bootstrapping a fresh environment:

```bash
cp .env.docker.example .env.docker
```

At minimum, confirm:

- `ARIFOS_GOVERNANCE_SECRET_FILE=/opt/arifos/secrets/governance.secret`
- `/opt/arifos/secrets` is mounted read-only into the `arifosmcp` container
- the secret file is readable by UID `1000`

### 3. Regenerate public specs

Run this whenever public tools, prompts, resources, or version change:

```bash
cd /srv/arifosmcp
python scripts/generate_public_specs.py
```

### 4. Build and launch stack

Full stack:

```bash
cd /srv/arifosmcp
docker compose up -d --build
```

Targeted MCP runtime redeploy:

```bash
cd /srv/arifosmcp
docker compose up -d --build arifosmcp
```

Targeted OpenClaw redeploy:

```bash
cd /srv/arifosmcp
docker compose up -d --build openclaw
```

### 5. Inspect runtime health

```bash
cd /srv/arifosmcp
docker compose ps
docker compose logs --tail=200 arifosmcp
docker compose logs --tail=200 openclaw
docker compose logs --tail=200 traefik
```

## Verification

After deployment, verify the public contract and runtime:

```bash
curl -fsS https://arifosmcp.arif-fazil.com/health
curl -fsS https://arifosmcp.arif-fazil.com/status?format=json
curl -fsS https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json
curl -fsS https://arifosmcp.arif-fazil.com/tools
curl -fsS https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}'
```

Expected checks:

- `/health` returns `healthy`
- `tools_loaded` is `10`
- `continuity_signing` is `configured`
- `governed_continuity` is `enabled`
- `/status` renders in plain HTML and returns JSON with `?format=json`
- `tools/list` includes `init_anchor_state`
- `arifosmcp` is reachable through Traefik, not by direct public port exposure

## Observability

Supporting observability stack:

- Prometheus scrapes service metrics
- Grafana provides dashboards
- Traefik logs ingress behavior
- `/status` is the fastest human-readable ops truth page
- `docker compose logs` remains the fastest first-pass incident surface on the VPS

For incidents:

```bash
cd /srv/arifosmcp
docker compose ps
docker compose logs --tail=200 arifosmcp
docker compose logs --tail=200 openclaw
docker compose logs --tail=200 postgres
docker compose logs --tail=200 redis
docker compose logs --tail=200 qdrant
```

## Chaos Watch

Current entropy risks still worth tracking:

| Risk | Impact | Action |
| --- | --- | --- |
| Agent Zero public route not proven | external access may still fail | verify DNS and Traefik route for `brain.arifosmcp.arif-fazil.com` |
| Traefik metrics port `8082` unresolved | observability gap | fix only if you actually need that scrape target |
| Manual runtime/spec drift | discovery/docs/runtime mismatch | regenerate specs from registry before deploy |
| OpenClaw provider catalog noise | warning confusion | keep Venice non-primary and watch startup logs |

## Deploy Standard

- make changes in `/srv/arifosmcp`
- regenerate specs if the public surface changes
- run targeted tests before restart
- redeploy only the necessary service when possible
- verify `/health`, `/status`, `/tools`, and MCP `tools/list` after every production change
