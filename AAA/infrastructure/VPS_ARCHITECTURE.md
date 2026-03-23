# arifOS VPS — Unified Architecture Snapshot

**Last verified:** 2026-03-14 by Codex (GPT-5)  
**Repo HEAD:** `0fe45827`  
**Public MCP version:** `2026.03.12-FORGED`  
**Status:** 12 containers running, `arifosmcp` healthy, OpenClaw forged and healthy, GitHub `main` aligned

> Production dossier for the live VPS. This file describes the actual runtime topology, not the intended one.

---

## 1. Host Facts

| Item | Value |
|------|-------|
| Hostname | `srv1325122` |
| OS / Kernel | Linux `6.17.0-14-generic` |
| Deploy path | `/srv/arifosmcp/` |
| Repo alias | `/srv/arifOS` -> `/srv/arifosmcp` |
| Compose files | `/srv/arifosmcp/docker-compose.yml`, `/srv/arifosmcp/docker-compose.override.yml` |
| Persistent data root | `/opt/arifos/data` |
| Persistent secret root | `/opt/arifos/secrets` |
| Public ingress | Traefik on `80/443` only |

---

## 2. Git Reality

| Item | Value |
|------|-------|
| Branch | `main` |
| Local HEAD | `0fe45827` |
| Alignment vs `origin/main` | aligned at verification |
| Worktree intent | production source of truth |
| Deployment state | latest pushed forged state is live |

Operational note:
- the VPS repo and GitHub `main` were previously drifted
- that drift has now been reconciled and pushed
- current production docs should assume `/srv/arifosmcp` is the only live code source of truth

---

## 3. Live Runtime Topology

### 3.1 Containers Running Now

| Container | Image | State | Exposure |
|-----------|-------|-------|----------|
| `arifosmcp_server` | `arifos/arifosmcp:latest` | healthy | `127.0.0.1:8080` via Traefik |
| `traefik_router` | `traefik:v3.6.9` | up | public `80/443` |
| `arifos_postgres` | `postgres:16-alpine` | healthy | loopback only |
| `arifos_redis` | `redis:7-alpine` | healthy | loopback only |
| `qdrant_memory` | `qdrant/qdrant:latest` | up | internal only |
| `ollama_engine` | `ollama/ollama:latest` | healthy | internal only |
| `openclaw_gateway` | `arifos/openclaw-forged:2026.03.14` | healthy | `127.0.0.1:18789` |
| `headless_browser` | `ghcr.io/browserless/chromium:latest` | healthy | internal only |
| `arifos_prometheus` | `prom/prometheus:latest` | up | internal only |
| `arifos_grafana` | `grafana/grafana:latest` | healthy | routed internally/publicly by Traefik rules |
| `arifos_n8n` | `n8nio/n8n:latest` | up | routed internally/publicly by Traefik rules |
| `agent_zero_reasoner` | `agent0ai/agent-zero:latest` | up | internal only, intended Traefik route exists |

### 3.2 Agent and Service State

| Agent / Service | Current state | What is proven |
|-----------------|---------------|----------------|
| `arifosmcp_server` | healthy | `/health`, `/status`, `/tools`, discovery doc and MCP endpoint respond |
| `openclaw_gateway` | healthy | forged image deployed; `kimi` and `opencode` work; preflight passes |
| `agent_zero_reasoner` | running | service is alive internally; real user traffic still not proven |
| `arifos_n8n` | running | container is up; workflow usage not verified in this pass |
| `ollama_engine` | healthy | local model and embedding runtime reachable |
| `qdrant_memory` | up | vector memory backend available |
| `headless_browser` | healthy | Browserless available for agents |

---

## 4. Network and Exposure

### 4.1 Public Surface

Public host ports:
- `80`
- `443`

Core stateful services remain private or loopback-bound:
- Postgres: loopback only
- Redis: loopback only
- arifosmcp app port: loopback only, fronted by Traefik
- OpenClaw: loopback only
- Ollama / Qdrant / Browserless / n8n internals: Docker network only

### 4.2 External URLs

| Layer | URL | State |
|------|-----|-------|
| arifosmcp health | `https://arifosmcp.arif-fazil.com/health` | live |
| arifosmcp status | `https://arifosmcp.arif-fazil.com/status` | live |
| arifosmcp MCP | `https://arifosmcp.arif-fazil.com/mcp` | live |
| arifosmcp tools | `https://arifosmcp.arif-fazil.com/tools` | live |
| arifosmcp discovery | `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json` | live |
| arifOS docs | `https://arifos.arif-fazil.com` | expected live |
| APEX Theory | `https://apex.arif-fazil.com` | expected live |
| Grafana | `https://monitor.arifosmcp.arif-fazil.com` | expected live |
| Agent Zero intended route | `https://brain.arifosmcp.arif-fazil.com` | not proven healthy |

---

## 5. arifosmcp Server Snapshot

Live health response on 2026-03-14:

| Field | Value |
|------|-------|
| Service | `arifos-aaa-mcp` |
| Version | `2026.03.12-FORGED` |
| Status | `healthy` |
| Transport | `streamable-http` |
| Tools loaded | `10` |
| Continuity signing | `configured` |
| Governed continuity | `enabled` |
| ML floors | disabled |
| ML method | `heuristic` |
| API bearer auth | `not_configured` |

### 5.1 Public Tool Surface

| Tool | Role |
|------|------|
| `arifOS_kernel` | main governed orchestrator |
| `search_reality` | external grounding |
| `ingest_evidence` | evidence ingestion |
| `session_memory` | continuity memory |
| `audit_rules` | floor and governance inspection |
| `check_vital` | system vitality and capability map |
| `init_anchor_state` | onboarding + continuity anchor |
| `verify_vault_ledger` | immutable ledger verification |
| `open_apex_dashboard` | APEX UI entry point |

### 5.2 Runtime Capability Highlights

The live `/health` capability map reports:

- `continuity_signing: configured`
- `governed_continuity: enabled`
- `vault_persistence: enabled`
- `vector_memory: enabled`
- `external_grounding: enabled`
- `model_provider_access: enabled`
- `local_model_runtime: enabled`
- `auto_deploy: enabled`

Persistent continuity is now backed by:
- `/opt/arifos/secrets/governance.secret`

---

## 6. OpenClaw Runtime

### 6.1 Proven Runtime State

| Item | Value |
|------|-------|
| Image | `arifos/openclaw-forged:2026.03.14` |
| Health | `{"ok":true,"status":"live"}` |
| Agent model in live log | `kimi/kimi-k2-5` |
| Native tools | `kimi 1.18.0`, `opencode 1.2.24` |
| Telegram provider | starts for `@arifOS_bot` |
| Browser control | `127.0.0.1:18791` with token auth |
| MCP bridge to arifosmcp | healthy |

### 6.2 OpenClaw Capability Wiring

Confirmed reachable from inside OpenClaw:
- Docker socket
- `/mnt/arifos`
- `/mnt/apex`
- arifosmcp MCP bridge
- Browserless
- mounted workspace and skills
- internal Docker network services

Operational note:
- Venice remains present for future provider use
- the main runtime path is no longer blocked by Venice credit failure

---

## 7. Memory and Intelligence Subsystems

| Component | State | Notes |
|-----------|-------|-------|
| PostgreSQL 16 | healthy | vault and ledger persistence |
| Redis 7 | healthy | cache and session support |
| Qdrant | up | vector memory backend |
| Ollama | healthy | local runtime and embeddings |
| `qwen2.5:3b` | available | local fallback model |
| `bge-m3` | available | embedding model |
| `nomic-embed-text` | available | secondary embedding option |

Live arifosmcp health/discovery reports:
- `vault999: postgresql+redis+merkle`
- `vector_memory: qdrant+bge-m3-1024dim`

---

## 8. Observability

| Component | State |
|-----------|-------|
| Prometheus | up |
| Grafana | healthy |
| arifosmcp `/health` | healthy |
| arifosmcp `/status` | healthy |
| OpenClaw `/healthz` | healthy |
| Traefik metrics port `8082` | still not treated as a sealed fix |

---

## 9. Key Paths

| Path | Purpose |
|------|---------|
| `/srv/arifosmcp/` | production repo |
| `/srv/arifosmcp/docker-compose.yml` | declared topology |
| `/srv/arifosmcp/docker-compose.override.yml` | local overrides and mounts |
| `/srv/arifosmcp/.env` | runtime secrets and live deploy env |
| `/srv/arifosmcp/.env.docker` | Docker-injected env for containers |
| `/srv/arifosmcp/DEPLOY.md` | deploy procedure |
| `/srv/arifosmcp/infrastructure/VPS_ARCHITECTURE.md` | architecture dossier |
| `/srv/arifosmcp/infrastructure/VPS_CAPABILITIES_MAP.md` | live capability matrix |
| `/opt/arifos/data/openclaw/` | OpenClaw persistent data |
| `/opt/arifos/secrets/governance.secret` | persistent continuity signing secret |

