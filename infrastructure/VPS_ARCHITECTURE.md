# arifOS VPS — Unified Architecture Snapshot

**Last verified:** 2026-03-13 by Codex (GPT-5)  
**Repo HEAD:** `06bbda10cf35d2cc24e584b17e041bb43cd0e58b`  
**Public MCP version:** `2026.03.12-FORGED`  
**Status:** 12 containers running, MCP healthy, OpenClaw healthy, Git not aligned with GitHub main

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
| Disk | `107G / 193G` used (`56%`), `87G` free |
| RAM | `4.7Gi / 15Gi` used, `10Gi` available |
| Swap | `1.1Gi / 4.0Gi` used |
| Load avg | `0.04 0.07 0.17` |
| Uptime at verification | ~`3h 06m` |

---

## 2. Git Reality

| Item | Value |
|------|-------|
| Branch | `main` |
| Local HEAD | `06bbda10cf35d2cc24e584b17e041bb43cd0e58b` |
| Divergence vs `origin/main` | `ahead 7`, `behind 2` |
| Worktree | dirty |
| Alignment | ❌ not aligned with GitHub main |

Modified files observed live:
- `arifosmcp/runtime/__init__.py`
- `core/judgment.py`
- `core/shared/crypto.py`
- `docker-compose.yml`
- `infrastructure/VPS_ARCHITECTURE.md`
- `spec/mcp-manifest.json`
- `spec/server.json`
- `tests/core/test_judgment.py`
- `uv.lock`

Implication:
- the VPS is not a clean deploy of current GitHub `main`
- any “latest GitHub main” claim is false until fetch/merge/redeploy is done explicitly

---

## 3. Live Runtime Topology

### 3.1 Containers Running Now

| Container | Image | State | Mem Usage | Exposure |
|-----------|-------|-------|-----------|----------|
| `arifosmcp_server` | `arifos/arifosmcp:latest` | ✅ healthy | `316.6MiB / 3GiB` | `127.0.0.1:8080` |
| `traefik_router` | `traefik:v3.6.9` | ✅ up | `84.87MiB / 128MiB` | public `80/443` |
| `arifos_postgres` | `postgres:16-alpine` | ✅ healthy | `29.07MiB / 1GiB` | `127.0.0.1:5432` |
| `arifos_redis` | `redis:7-alpine` | ✅ healthy | `5.08MiB / 128MiB` | `127.0.0.1:6379` |
| `qdrant_memory` | `qdrant/qdrant:latest` | ✅ up | `215.9MiB / 1GiB` | internal only |
| `ollama_engine` | `ollama/ollama:latest` | ✅ healthy | `1.989GiB / 2GiB` | internal only |
| `openclaw_gateway` | `arifos/openclaw-forged:2026.03.13` | ✅ healthy | `455.9MiB / 2GiB` | `127.0.0.1:18789` |
| `headless_browser` | `ghcr.io/browserless/chromium:latest` | ✅ healthy | `87.68MiB / 1GiB` | internal only |
| `arifos_prometheus` | `prom/prometheus:latest` | ✅ up | `34.03MiB / 1GiB` | internal only |
| `arifos_grafana` | `grafana/grafana:latest` | ✅ healthy | `94.81MiB / 1GiB` | internal only |
| `arifos_n8n` | `n8nio/n8n:latest` | ✅ up | `332MiB / 1GiB` | internal only |
| `agent_zero_reasoner` | `agent0ai/agent-zero:latest` | ✅ up | `1.02GiB / 2GiB` | internal only, routed by Traefik label |

### 3.2 Actual Agent State

| Agent / Service | Current state | What is proven |
|-----------------|---------------|----------------|
| `arifosmcp_server` | healthy | public `/health`, `/tools`, discovery doc all respond |
| `openclaw_gateway` | healthy | `http://127.0.0.1:18789/healthz` returns `ok`; Telegram provider starts |
| `agent_zero_reasoner` | running | booted and serving internally; no strong evidence of real user traffic |
| `arifos_n8n` | running | container is up; workflow usage not verified in this pass |
| `ollama_engine` | healthy but near memory ceiling | reachable and generation was previously proven from OpenClaw |
| `qdrant_memory` | up | reachable on internal network |
| `headless_browser` | healthy | Browserless available for agents |

### 3.3 Compose Drift

The runtime does not match the checked-in topology cleanly:
- `agent_zero_reasoner` is running with Compose labels from service `agent-zero`
- current `docker-compose.yml` does not cleanly reflect that live runtime as a first-class declared service
- `webhook` is declared in compose history, but no `arifos_webhook` container is running now
- OpenClaw name drift is now corrected; the live container is back to the stable name `openclaw_gateway`

This is operational drift, not just cosmetic drift.

---

## 4. Network and Exposure

### 4.1 Public Surface

Only these host ports are publicly bound:
- `80`
- `443`

All core stateful services remain private or loopback-bound:
- Postgres: loopback only
- Redis: loopback only
- arifosmcp app port: loopback only, fronted by Traefik
- OpenClaw: loopback only
- Ollama / Qdrant / Browserless / n8n: internal Docker network

### 4.2 External URLs

| Layer | URL | State |
|------|-----|-------|
| arifosmcp health | `https://arifosmcp.arif-fazil.com/health` | ✅ live |
| arifosmcp MCP | `https://arifosmcp.arif-fazil.com/mcp` | ✅ live |
| arifosmcp tools | `https://arifosmcp.arif-fazil.com/tools` | ✅ live |
| arifosmcp discovery | `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json` | ✅ live |
| arifOS docs | `https://arifos.arif-fazil.com` | expected live |
| APEX Theory | `https://apex.arif-fazil.com` | expected live |
| Grafana | `https://monitor.arifosmcp.arif-fazil.com` | expected live |
| Agent Zero intended route | `https://brain.arifosmcp.arif-fazil.com` | ⚠️ historical DNS/ACME failure evidence |

### 4.3 Agent Zero Exposure Reality

Traefik labels on the live container define:
- router rule: `Host(\`brain.arifosmcp.arif-fazil.com\`)`
- service port: `80`

But historical Traefik logs show repeated ACME failures because `brain.arifosmcp.arif-fazil.com` returned `NXDOMAIN`.

Implication:
- Agent Zero is running internally
- its public route has not been proven healthy
- no reliable evidence of real user traffic was found in this verification pass

---

## 5. arifosmcp Server Snapshot

Live health response on 2026-03-13:

| Field | Value |
|------|-------|
| Service | `arifos-aaa-mcp` |
| Version | `2026.03.12-FORGED` |
| Status | `healthy` |
| Transport | `streamable-http` |
| Tools loaded | `9` |
| ML floors | disabled |
| ML method | `heuristic` |
| API bearer auth | `not_configured` |

### 5.1 Public Tool Surface

| Tool | Stage | Role |
|------|-------|------|
| `arifOS_kernel` | `444_ROUTER` | Main orchestrator |
| `search_reality` | `111_SENSE` | Grounding |
| `ingest_evidence` | `222_REALITY` | Ingestion |
| `session_memory` | `555_MEMORY` | Continuity |
| `audit_rules` | `333_MIND` | Governance |
| `check_vital` | `000_INIT` | Telemetry |
| `bootstrap_identity` | `000_INIT` | Onboarding |
| `open_apex_dashboard` | `888_JUDGE` | Visualizer |
| `verify_vault_ledger` | `999_VAULT` | Auditor |

### 5.2 Discovery Doc Highlights

```json
{
  "name": "io.github.ariffazil/arifos-mcp",
  "version": "2026.03.12-FORGED",
  "protocolVersion": "2025-11-25",
  "tools": 9,
  "vector_memory": "qdrant+bge-m3-1024dim",
  "authentication": { "type": "none" }
}
```

---

## 6. OpenClaw Runtime

### 6.1 Proven Runtime State

| Item | Value |
|------|-------|
| Health | `{"ok":true,"status":"live"}` |
| Agent model in live log | `kimi/kimi-k2-5` |
| Telegram provider | starts for `@arifOS_bot` |
| Browser control | `127.0.0.1:18791` with token auth |
| MCP bridge to arifosmcp | healthy |
| `mcporter` | sees `arifos` with `9 tools` |

### 6.2 OpenClaw Capability Wiring

Confirmed reachable from inside the OpenClaw container:
- Docker socket
- `/mnt/arifos`
- `/mnt/apex`
- arifosmcp MCP bridge
- Browserless
- internal Docker network services
- mounted host CLIs and helper wrappers

### 6.3 OpenClaw Stability Notes

- OpenClaw is healthy now
- container naming is drifting because current recreate flow produces generated names
- gateway log still shows a Venice model catalog timeout during provider discovery, but runtime continues
- this is not the same as user-visible Venice credit failure

---

## 7. Memory and Intelligence Subsystems

| Component | State | Notes |
|-----------|-------|-------|
| PostgreSQL 16 | healthy | VAULT / ledger persistence |
| Redis 7 | healthy | cache / session support |
| Qdrant | up | vector memory backend for arifosmcp |
| Ollama | healthy but memory-heavy | local runtime and embeddings |
| `qwen2.5:3b` | available | local fallback model |
| `bge-m3` | available | embedding model |
| `nomic-embed-text` | available | secondary embedding option |

Live arifosmcp discovery reports:
- `vault999: postgresql+redis+merkle`
- `vector_memory: qdrant+bge-m3-1024dim`

---

## 8. Observability

| Component | State |
|-----------|-------|
| Prometheus | up |
| Grafana | healthy |
| arifosmcp health endpoint | healthy |
| OpenClaw health endpoint | healthy |
| Traefik metrics port `8082` | still treated as unresolved / not proven fixed |

---

## 9. Key Paths

| Path | Purpose |
|------|---------|
| `/srv/arifosmcp/` | production repo |
| `/srv/arifosmcp/docker-compose.yml` | declared topology |
| `/srv/arifosmcp/docker-compose.override.yml` | local overrides / mounts |
| `/srv/arifosmcp/.env` | runtime secrets |
| `/srv/arifosmcp/.env.docker` | Docker-injected env for containers |
| `/srv/arifosmcp/infrastructure/VPS_ARCHITECTURE.md` | architecture dossier |
| `/srv/arifosmcp/infrastructure/VPS_CAPABILITIES_MAP.md` | live capability matrix |
| `/opt/arifos/data/openclaw/` | OpenClaw persistent data |
| `/opt/arifos/data/openclaw/workspace/config/mcporter.json` | MCP config used by OpenClaw |
| `/root/CONTEXT.md` | owner / VPS context |
| `/root/AGENTS.md` | agent operating instructions |

---

## 10. Active Risks

| Risk | Severity | Current state |
|------|----------|---------------|
| Git divergence from `origin/main` | High | `ahead 7`, `behind 2`, dirty |
| Compose/runtime drift | High | running Agent Zero + generated OpenClaw name do not cleanly match desired compose state |
| Ollama near memory limit | Medium | `1.989GiB / 2GiB` |
| Agent Zero public route | Medium | historical DNS/ACME failures; usage unproven |
| API bearer auth disabled on public MCP | Medium | discovery still reports `authentication: none` |
| ML floors disabled | Info | heuristic mode active |
| Grafana constitutional dashboards | Info | still not fully proven in this pass |

---

## 11. Bottom Line

The VPS is operational and the main public brain surface is healthy:
- `arifosmcp` is live and serving `9` tools
- OpenClaw is healthy and wired to arifosmcp
- Agent Zero exists and runs, but it is not yet a proven public-facing production agent

The system is not fully “aligned” in the strict sense:
- Git is diverged
- runtime topology has drift
- some agent access paths are mounted but not uniformly stable
