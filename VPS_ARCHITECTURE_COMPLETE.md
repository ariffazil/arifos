# VPS Architecture & Component Reference
## arifOS Constitutional AI Governance System

**Last Updated:** 2026-03-05
**VPS Host:** srv1325122.hstgr.cloud
**Public IP:** 72.62.71.199
**Owner:** Arif Fazil — *Ditempa Bukan Diberi*

---

## 1. Hardware

| Component | Specification |
|-----------|---------------|
| Provider | Hostinger KVM VPS |
| OS | Ubuntu 25.10 (non-LTS) |
| Kernel | Linux 6.17.0-14-generic x86_64 |
| CPU | 4 vCPU |
| Memory | 16 GB RAM |
| Disk | 193 GB SSD — 125G used / 69G free (65%) |

---

## 2. Network

### Public Access
| Port | Service |
|------|---------|
| 22 | SSH (key-only, Fail2Ban active) |
| 80 | Traefik → redirects to HTTPS |
| 443 | Traefik → routes to services |

### Tailscale Mesh (Private)
| Node | Tailscale IP | Status |
|------|-------------|--------|
| VPS (srv1325122) | 100.111.84.52 | Online |
| You (ARIFFAZIL) | 100.109.203.23 | Online |
| GHA deploy runners | 100.x.x.x (ephemeral) | Active on push |

### Domain Routing (via Traefik + Let's Encrypt)
| Domain | Backend | Status |
|--------|---------|--------|
| `arifosmcp.arif-fazil.com` | arifosmcp_server:8080 | LIVE |
| `brain.arifosmcp.arif-fazil.com` | agent-zero:80 | NOT DEPLOYED |
| `claw.arifosmcp.arif-fazil.com` | openclaw:3000 | NOT DEPLOYED |
| `hook.arifosmcp.arif-fazil.com` | arifos_webhook:9000 | LIVE |

### Docker Networks
| Network | Subnet | Used By |
|---------|--------|---------|
| `arifos_trinity` | 10.0.10.0/24 | All current services |
| `arifos-internal` | 172.18.x.x | Phase1 legacy (still attached) |

---

## 3. Services — Current State

### RUNNING (6 containers)

| Container | Image | Status | Port | Purpose |
|-----------|-------|--------|------|---------|
| `arifosmcp_server` | arifos/arifosmcp:latest | **HEALTHY** | :8080 | Constitutional AI kernel — 13 MCP tools |
| `traefik_router` | traefik:v3.0 | **UP** | :80/:443 | Edge router, TLS termination |
| `arifos-postgres` | postgres:16-alpine | **HEALTHY** | localhost:5432 | Vault state, audit logs |
| `arifos-redis` | redis:7-alpine | **HEALTHY** | localhost:6379 | Session cache, broker |
| `qdrant_memory` | qdrant/qdrant:latest | **UP** | (internal :6333) | Vector memory for recall_memory tool |
| `arifos_webhook` | almir/webhook:latest | **UP** | (internal :9000) | CI/CD auto-deploy on git push |

### NOT RUNNING (defined in docker-compose.yml)

| Container | Image | Blocker | Phase |
|-----------|-------|---------|-------|
| `ollama_engine` | ollama/ollama:latest | Image not pulled (~4GB) | 3 |
| `agent_zero_reasoner` | agent0ai/agent-zero:latest | Image not pulled + `/opt/arifos/APEX-THEORY` dir missing | 4 |
| `openclaw_gateway` | openclaw:local | No image — needs source build from `/root/openclaw` | 4 |

---

## 4. Agent Control Plane (Host-Level CLIs)

All installed at `/home/ariffazil/.local/bin/` and `/usr/local/bin/`:

| CLI | Version | AGI Wrapper | Purpose |
|-----|---------|-------------|---------|
| `claude` (Claude Code) | 2.1.69 | `agi-claude` | Primary dev + ops agent |
| `opencode` | 1.2.16 | `agi-opencode` | Alternative coding agent |
| `codex` | 0.107.0 | `agi-codex` | OpenAI Codex CLI |
| `gemini` | 0.31.0 | `agi-gemini` | Google Gemini CLI |
| `kimi` | 1.17.0 | `agi-kimi` | Moonshot Kimi CLI |

All 5 CLIs have `agi-*` and `ai-*` wrapper variants pre-configured with arifOS AGI context.

---

## 5. arifOS MCP Server — Tool Surface

**Transport:** Streamable HTTP at `https://arifosmcp.arif-fazil.com/mcp`
**Tools:** 13 canonical tools across 3 Trinity lanes

### Metabolic Chain (000→999)
| Tool | Stage | Lane | Floor(s) |
|------|-------|------|---------|
| `anchor_session` | 000 | Δ Delta | F11, F12 |
| `reason_mind` | 111-333 | Δ Delta | F2, F4, F7, F13 |
| `recall_memory` | 444 | Ψ Psi | F3, F7 → **Qdrant live** |
| `simulate_heart` | 555 | Ω Omega | F5, F6 |
| `critique_thought` | 666 | Ω Omega | F4, F7, F8 |
| `eureka_forge` | 777 | Ψ Psi | F1, F4 |
| `apex_judge` | 888 | Ψ Psi | F1-F13 |
| `seal_vault` | 999 | Ψ Psi | F1, F3, F10 |

### Evidence Tools (read-only)
| Tool | Purpose | Backend |
|------|---------|---------|
| `search_reality` | Web search | Perplexity / Brave (keys set) |
| `fetch_content` | Content extraction | Jina Reader (key set) |
| `inspect_file` | Filesystem read | Host-level |
| `audit_rules` | Constitutional audit | core/shared/floors.py |
| `check_vital` | System health | Docker + host |

---

## 6. Data Volumes & Paths

```
/srv/arifOS/                    # Git repo — canonical source of truth
/opt/arifos/
├── data/
│   ├── core/                   # arifOS runtime data
│   ├── qdrant/                 # Vector storage (LIVE)
│   ├── ollama/                 # LLM models (Phase 3, dir exists)
│   ├── postgres/               # (Phase 3 full-stack only)
│   ├── redis/                  # (Phase 3 full-stack only)
│   └── agent_zero/             # (Phase 4, not created yet)
├── traefik/
│   ├── acme.json               # Let's Encrypt certs
│   ├── dynamic.yml             # Static routing rules
│   └── traefik.yml             # Entry points config
└── APEX-THEORY/                # MISSING — needed for openclaw + agent-zero

/var/lib/docker/volumes/
├── arifos_postgres_data/       # PostgreSQL data (phase1 compose)
└── arifos_redis_data/          # Redis data (phase1 compose)
```

---

## 7. CI/CD Pipeline

### Webhook Auto-Deploy
- **Endpoint:** `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos`
- **Trigger:** GitHub push to `main`
- **Auth:** HMAC-SHA256 signature (secret set in GitHub webhook settings)
- **Script:** `/srv/arifOS/deployment/deploy_from_git.sh`
- **Action:** `git pull` → `docker compose --build arifosmcp` → health check

### GitHub Actions
- **Workflow:** `.github/workflows/deploy-vps.yml`
- **Tailscale VPN:** Connects GHA runner to VPS for SSH deploy
- **Symlink:** Creates `/root/arifOS → /srv/arifOS` if missing

---

## 8. API Reference

```bash
# Health
curl https://arifosmcp.arif-fazil.com/health

# MCP endpoint (Streamable HTTP)
POST https://arifosmcp.arif-fazil.com/mcp

# Webhook deploy trigger (GitHub handles this)
POST https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos

# Qdrant (internal only)
curl http://localhost:6333/healthz     # from VPS host
# or from any container:
curl http://qdrant:6333/healthz
```

---

## 9. Security

| Layer | Tool | Status |
|-------|------|--------|
| SSH hardening | Key-only auth, no root login | Active |
| Brute-force protection | Fail2Ban | Active |
| TLS termination | Traefik + Let's Encrypt | Active |
| VPN mesh | Tailscale | Active |
| Webhook auth | HMAC-SHA256 | Active |
| Constitutional floors | F1-F13 on all MCP tools | Active |

---

## 10. Phased Deployment Roadmap

### Phase 1 — Core Runtime ✅ COMPLETE
- PostgreSQL 16, Redis 7, Traefik v3, arifOS MCP (13 tools)

### Phase 2 — Memory & Automation ✅ COMPLETE (2026-03-05)
- **2A:** Qdrant vector DB — `recall_memory` tool now has live backend
- **2B:** Webhook CI/CD listener — auto-deploy on git push to main

### Phase 3 — Agent Workbench (NEXT)
- [ ] Ollama (local LLM engine) — `docker compose up -d ollama` + model pull
- [ ] Prometheus + Grafana monitoring — configs ready in `deployment/`, need compose services
- [ ] n8n workflow automation — needs compose service + domain (`flow.arifosmcp.arif-fazil.com`)

### Phase 4 — Multi-Agent Runtime
- [ ] Agent Zero — autonomous agent web UI at `brain.arifosmcp.arif-fazil.com`
  - Requires: create `/opt/arifos/APEX-THEORY`, pull image
- [ ] OpenClaw gateway — `claw.arifosmcp.arif-fazil.com`
  - Requires: clone source → build `openclaw:local` image

### Phase 5 — Production Hardening
- [ ] Verify SSL cert issuance via `acme.json` + test HTTPS end-to-end
- [ ] Consolidate Traefik routing (remove duplicate `dynamic.yml` file provider)
- [ ] Backup automation — Postgres dump cron + Vault999 archive
- [ ] Monitoring alerts — Grafana → Telegram (TELEGRAM_BOT_TOKEN set)
- [ ] `/opt/arifos/APEX-THEORY` — create shared theory volume

---

## 11. Full Stack Vision (When All Phases Complete)

```
Human
  ├── Claude Code / SSH (direct VPS control)
  ├── Agent Zero → brain.arifosmcp.arif-fazil.com  (autonomous agent UI)
  └── n8n → flow.arifosmcp.arif-fazil.com          (workflow automation)

AI Agents (via MCP)
  └── arifOS MCP → arifosmcp.arif-fazil.com
        ├── recall_memory    → Qdrant          (vector memory)     ← LIVE
        ├── search_reality   → Perplexity/Brave (web search)       ← LIVE
        ├── fetch_content    → Jina             (content extract)  ← LIVE
        └── eureka_forge     → Ollama           (local LLM)        ← Phase 3

Infrastructure
  ├── Traefik    (TLS + routing)                                   ← LIVE
  ├── PostgreSQL (constitutional vault + state)                    ← LIVE
  ├── Redis      (cache + message broker)                          ← LIVE
  ├── Qdrant     (semantic vector memory)                          ← LIVE
  ├── Webhook    (CI/CD auto-deploy)                               ← LIVE
  ├── Ollama     (local LLM, no API key needed)                    ← Phase 3
  ├── Prometheus + Grafana (monitoring + alerts)                   ← Phase 3
  └── n8n        (workflow orchestration)                          ← Phase 3
```

---

## 12. Key Files Reference

| File | Purpose |
|------|---------|
| `/srv/arifOS/docker-compose.yml` | Primary compose — all services |
| `/srv/arifOS/docker-compose.phase1.yml` | Legacy infra layer (postgres, redis via old network) |
| `/srv/arifOS/deployment/hooks.json` | Webhook trigger config |
| `/srv/arifOS/deployment/deploy_from_git.sh` | Auto-deploy script |
| `/srv/arifOS/deployment/prometheus/prometheus.yml` | Prometheus scrape config (ready) |
| `/srv/arifOS/deployment/grafana/` | Grafana datasource + dashboards (ready) |
| `/srv/arifOS/.env.docker` | API keys for MCP tools (20 keys set) |
| `/opt/arifos/traefik/acme.json` | Let's Encrypt certificate store |
| `/opt/arifos/traefik/dynamic.yml` | Static Traefik routing rules |

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
