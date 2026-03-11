# arifosmcp VPS Deploy Guide

This document is the current deployment reference for the production VPS layout as of March 10, 2026.

Production deploys are High-stakes - apply `888_HOLD` gate before sealing changes to live infrastructure.

## Current Topology

The live architecture is a single VPS running a 13-service Docker Compose stack behind Traefik.

Canonical source of truth:

| Layer | Canonical path / endpoint | Notes |
| --- | --- | --- |
| Git working tree | `/srv/arifosmcp` | Main active repository on VPS |
| Persistent data root | `/opt/arifos/data` | Postgres, Redis, Qdrant, Grafana, n8n, OpenClaw, Agent Zero |
| TLS state | `/opt/arifos/traefik/acme.json` | Traefik certificate store |
| Public base URL | `https://arifosmcp.arif-fazil.com` | Main public MCP domain |
| MCP endpoint | `https://arifosmcp.arif-fazil.com/mcp` | Streamable HTTP MCP |
| SSE endpoint | `https://arifosmcp.arif-fazil.com/sse` | SSE transport |
| Public discovery | `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json` | Generated from runtime registry |

Known drift:

- The active codebase on VPS is `/srv/arifosmcp`.
- Some Compose mounts and helper scripts still reference legacy `/srv/arifOS`.
- Treat `/srv/arifosmcp` as the code source of truth and normalize legacy path references before sealing major infra changes.

## 13-Service Stack

The current Docker Compose architecture contains these services:

| Service | Role | Persistence | Exposure |
| --- | --- | --- | --- |
| `traefik` | Reverse proxy, TLS, routing | `/opt/arifos/traefik/acme.json` | Public `:80`, `:443` |
| `postgres` | Primary relational store | `/opt/arifos/data/postgres` | Internal |
| `redis` | Cache / broker | `/opt/arifos/data/redis` | Internal |
| `qdrant` | Vector memory | `/opt/arifos/data/qdrant` | Internal |
| `ollama` | Local model runtime | `/opt/arifos/data/ollama` | Internal |
| `openclaw` | External agent gateway | `/opt/arifos/data/openclaw` plus legacy code mount | Internal |
| `agent-zero` | Local reasoning sidecar | `/opt/arifos/data/agent-zero` plus legacy code mount | Internal |
| `arifosmcp` | Main FastMCP runtime | Repo bind mount plus env file | Routed via Traefik |
| `prometheus` | Metrics collector | `/opt/arifos/data/prometheus` plus config mount | Internal |
| `grafana` | Dashboards | `/opt/arifos/data/grafana` | Public via Traefik |
| `n8n` | Automation workflows | `/opt/arifos/data/n8n` | Public via Traefik |
| `webhook` | Controlled HTTP trigger service | Legacy code mount | Internal |
| `headless_browser` | Browser automation / rendering | Container-local | Internal |

## Runtime Contract

The public MCP surface is registry-driven from `arifosmcp.runtime.public_registry`.

Current public profile:

- Version: `2026.03.10`
- Public tool profile: `chatgpt`
- Public tool count: `7`
- Discovery documents:
  - `spec/server.json`
  - `spec/mcp-manifest.json`
- Deploy validation source:
  - `scripts/deploy_production.py`

Do not hand-edit public tool lists in multiple places. Update the registry and regenerate specs.

## Required Production Environment

Create `.env.docker` from `.env.docker.example` and set production values explicitly.

Minimum required variables:

| Variable | Required value / guidance |
| --- | --- |
| `PORT` | `8080` |
| `HOST` | `0.0.0.0` |
| `AAA_MCP_TRANSPORT` | `http` |
| `ARIFOS_VERSION` | `2026.03.10` |
| `ARIFOS_PUBLIC_TOOL_PROFILE` | `chatgpt` |
| `ARIFOS_MCP_PATH` | `/mcp` |
| `ARIFOS_PUBLIC_BASE_URL` | Public HTTPS domain, currently `https://arifosmcp.arif-fazil.com` |
| `ARIFOS_WIDGET_DOMAIN` | Same public origin unless intentionally split |
| `ARIFOS_GOVERNANCE_SECRET_FILE` | **Preferred:** Path to persistent secret file (see below) |
| `ARIFOS_GOVERNANCE_SECRET` | Fallback: Long random secret (not recommended for production) |
| `POSTGRES_PASSWORD` | Strong secret |
| `OPENCLAW_ACCESS_TOKEN` | Strong secret |
| `N8N_BASIC_AUTH_PASSWORD` | Strong secret |
| `WEBHOOK_SECRET` | Strong secret |
| `GF_SECURITY_ADMIN_PASSWORD` | Strong secret |

Operational note:

- **F11 CRITICAL:** `ARIFOS_GOVERNANCE_SECRET` MUST be persistent across restarts. Ephemeral secrets invalidate all auth_context tokens on restart, breaking session continuity.
- **Recommended:** Use `ARIFOS_GOVERNANCE_SECRET_FILE` pointing to a stable file path (e.g., `/opt/arifos/secrets/governance.secret`)
- See [DEPLOY_SECRETS.md](DEPLOY_SECRETS.md) for Docker Secrets, file-based secrets, and rotation procedures.

## Canonical VPS Layout

Use this directory shape on the VPS:

```text
/srv/arifosmcp
├── docker-compose.yml
├── .env.docker
├── arifosmcp/
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
└── traefik/
    └── acme.json
```

Avoid duplicate live working trees under home directories. They increase entropy and make rollback analysis harder.

## Deploy Procedure

### 1. Prepare host

```bash
mkdir -p /srv/arifosmcp
mkdir -p /opt/arifos/data/{agent-zero,grafana,n8n,ollama,openclaw,postgres,prometheus,qdrant,redis}
mkdir -p /opt/arifos/traefik
touch /opt/arifos/traefik/acme.json
chmod 600 /opt/arifos/traefik/acme.json
```

### 2. Sync repository

```bash
cd /srv/arifosmcp
git pull --ff-only
cp .env.docker.example .env.docker
```

Edit `.env.docker` and replace all placeholder secrets before continuing.

### 3. Regenerate public specs

Run this whenever public tools, prompts, resources, or version change:

```bash
cd /srv/arifosmcp
python scripts/generate_public_specs.py
```

### 4. Build and launch stack

```bash
cd /srv/arifosmcp
docker compose --env-file .env.docker up -d --build
```

If you need a targeted restart for the MCP runtime only:

```bash
cd /srv/arifosmcp
docker compose --env-file .env.docker up -d --build arifosmcp
```

### 5. Inspect runtime health

```bash
docker compose ps
docker compose logs --tail=200 arifosmcp
docker compose logs --tail=200 traefik
```

## Overlay Deploy Path

There is also a scripted VPS overlay deploy path:

```bash
cd /srv/arifosmcp
python scripts/deploy_production.py \
  --platform vps-overlay \
  --host root@YOUR_VPS_IP \
  --app-dir /srv/arifosmcp \
  --public-base-url https://YOUR_DOMAIN
```

Important:

- The deploy script now validates public tools against `arifosmcp.runtime.public_registry`.
- Some script defaults still carry legacy path assumptions such as `/root/arifOS`.
- Override `--app-dir` explicitly to `/srv/arifosmcp` until those legacy defaults are fully removed.

## Verification

After deployment, verify the public contract and runtime:

```bash
curl -fsS https://YOUR_DOMAIN/health
curl -fsS https://YOUR_DOMAIN/.well-known/mcp/server.json
curl -fsS https://YOUR_DOMAIN/tools
curl -fsS https://YOUR_DOMAIN/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}'
```

Expected checks:

- `health` returns success.
- `server.json` and `mcp-manifest.json` match the current registry version.
- `tools/list` reflects the `chatgpt` public profile.
- Public tool count is `7`.
- `arifosmcp` is reachable through Traefik, not by direct public port exposure.

## Observability

Supporting observability stack:

- Prometheus scrapes service metrics.
- Grafana provides dashboards.
- Traefik logs ingress behavior.
- `docker compose logs` remains the fastest first-pass incident surface on the VPS.

For incidents:

```bash
cd /srv/arifosmcp
docker compose ps
docker compose logs --tail=200 arifosmcp
docker compose logs --tail=200 postgres
docker compose logs --tail=200 redis
docker compose logs --tail=200 qdrant
```

## Chaos Watch

Current entropy risks to reduce before a hard production seal:

| Risk | Impact | Action |
| --- | --- | --- |
| Duplicate repo roots on VPS | Unclear live code path | Keep `/srv/arifosmcp` as sole active repo |
| Legacy `/srv/arifOS` mounts in Compose | Broken binds or stale code | Normalize mounts to `/srv/arifosmcp` |
| Placeholder governance secret | Session continuity breaks across restart | Use `ARIFOS_GOVERNANCE_SECRET_FILE` with stable path. See [DEPLOY_SECRETS.md](DEPLOY_SECRETS.md) |
| Manual spec drift | Discovery/docs/runtime mismatch | Regenerate specs from registry before deploy |
| Production deploy without contract check | Silent public surface regression | Run deploy validation and post-deploy `tools/list` |

## Deploy Standard

For this repo, a production-ready VPS deploy means:

1. Code runs from `/srv/arifosmcp`.
2. Persistent state lives under `/opt/arifos/data`.
3. Traefik owns public ingress and TLS.
4. Public MCP specs are generated from the runtime registry.
5. The public `chatgpt` profile exposes exactly the intended 7 tools.
6. Secrets are fixed, non-placeholder, and not process-ephemeral.
7. High-stakes deploys are treated as `888_HOLD` until human approval is explicit.
