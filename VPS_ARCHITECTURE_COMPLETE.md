# VPS Architecture & Component Reference
## arifOS Constitutional AI Governance System

**Last Updated:** 2026-03-05
**Version:** v2026.3.2
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
| Disk | 193 GB SSD — 51G used / 143G free (27%) |
| Swap | vm.swappiness=10 (persisted via `/etc/sysctl.d/99-arifos.conf`) |

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

### Domain Routing (via Traefik v3.6.9 + Let's Encrypt)
| Domain | Backend | Status |
|--------|---------|--------|
| `arifosmcp.arif-fazil.com` | arifosmcp_server:8080 | LIVE |
| `claw.arifosmcp.arif-fazil.com` | openclaw_gateway:18789 | LIVE |
| `monitor.arifosmcp.arif-fazil.com` | arifos_grafana:3000 | LIVE |
| `flow.arifosmcp.arif-fazil.com` | arifos_n8n:5678 | LIVE |
| `hook.arifosmcp.arif-fazil.com` | arifos_webhook:9000 | LIVE |
| `brain.arifosmcp.arif-fazil.com` | agent-zero:80 | NOT DEPLOYED (Phase 4B) |

### Docker Networks
| Network | Subnet | Used By |
|---------|--------|---------|
| `arifos_arifos_trinity` | 10.0.10.0/24 | All current services (compose-prefixed) |
| `arifos_trinity` | alias | Referenced in compose labels |
| `arifos-internal` | 172.18.x.x | Phase1 legacy (postgres, redis, traefik) |

---

## 3. Services — Current State

### RUNNING (11 containers)

| Container | Image | Status | Port | Purpose |
|-----------|-------|--------|------|---------|
| `arifosmcp_server` | arifos/arifosmcp:latest (4.0GB) | **HEALTHY** | :8080 | Constitutional AI kernel — 14 MCP tools |
| `traefik_router` | traefik:v3.6.9 | **UP** | :80/:443 | Edge router, TLS termination |
| `arifos-postgres` | postgres:16-alpine | **HEALTHY** | localhost:5432 | Vault state, audit logs |
| `arifos-redis` | redis:7-alpine | **HEALTHY** | localhost:6379 | Session cache, broker |
| `qdrant_memory` | qdrant/qdrant:latest | **UP** | internal :6333 | Vector memory for recall_memory |
| `arifos_webhook` | almir/webhook:latest | **UP** | internal :9000 | CI/CD auto-deploy on git push |
| `ollama_engine` | ollama/ollama:latest | **UP** | internal :11434 | Local LLM — qwen2.5:3b loaded |
| `arifos_prometheus` | prom/prometheus:latest | **UP** | internal :9090 | Metrics collection |
| `arifos_grafana` | grafana/grafana:latest | **UP** | internal :3000 | Monitoring dashboards |
| `arifos_n8n` | n8nio/n8n:latest | **UP** | internal :5678 | Workflow automation |
| `openclaw_gateway` | openclaw/openclaw:latest | **HEALTHY** | internal :18789 | AI gateway — `claw.arifosmcp.arif-fazil.com` |

### NOT RUNNING (defined in docker-compose.yml)

| Container | Image | Blocker | Phase |
|-----------|-------|---------|-------|
| `agent_zero_reasoner` | agent0ai/agent-zero:latest | Image not pulled; `brain.arifosmcp.arif-fazil.com` DNS needed | 4B |

---

## 4. Three-Repo Architecture

| Repo | Role | Local Path |
|------|------|------------|
| `ariffazil/arifOS` | Kernel, MCP server, Docker infra, VAULT999 | `/srv/arifOS` |
| `ariffazil/openclaw-workspace` | OpenClaw agent OS — AGENTS/SOUL/TOOLS/skills | `/opt/arifos/git/openclaw-workspace` |
| `ariffazil/AGI_ASI_bot` | Client personas, MCP configs, governance hooks | `/opt/arifos/git/AGI_ASI_bot` |

**Rule:** Client MCP configs live in `AGI_ASI_bot`. Server-side changes go in `arifOS`. OpenClaw agent identity/skills go in `openclaw-workspace`.

---

## 5. Agent Control Plane (Host-Level CLIs)

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

## 6. arifOS MCP Server — Tool Surface

**Transport:** Streamable HTTP at `https://arifosmcp.arif-fazil.com/mcp`
**Tools:** 14 live + 1 pending (after next rebuild)

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
| `visualize_governance` | Constitutional Visualizer UI | 333_APPS/constitutional-visualizer |

### Extra Tool (post-rebuild)
| Tool | Purpose | Status |
|------|---------|--------|
| `query_openclaw` | OpenClaw gateway diagnostics (health + status) | PENDING — activates after `docker compose up --build arifosmcp` |

---

## 7. OpenClaw Gateway

**URL:** `https://claw.arifosmcp.arif-fazil.com`
**Internal:** `http://openclaw_gateway:18789`
**Default Model:** `moonshot/kimi-k2` (fallback: `anthropic/claude-sonnet-4-6`)
**API mode:** WebSocket (custom protocol) — HTTP endpoints serve SPA UI only

### Config
| File | Path |
|------|------|
| Runtime config | `/opt/arifos/data/openclaw/openclaw.json` |
| Workspace (git) | `/opt/arifos/git/openclaw-workspace/` |
| Workspace (symlink) | `/opt/arifos/data/openclaw/workspace/` |
| Memory | `/opt/arifos/data/openclaw/memory/` (gitignored) |
| Logs | `/opt/arifos/data/openclaw/logs/` (gitignored) |

### Key config fields
```json
{
  "agents.defaults.model.primary": "moonshot/kimi-k2",
  "agents.defaults.model.fallbacks": ["anthropic/claude-sonnet-4-6"],
  "gateway.bind": "lan",
  "gateway.port": 18789,
  "gateway.auth.mode": "token"
}
```

### openclaw-cli Skill
Two-layer diagnostic integration:
- **Layer 1 (MCP):** `query_openclaw` in `aaa_mcp/server.py` — HTTP probe + config read from `arifosmcp_server` container
- **Layer 2 (OpenClaw workspace):** `skills/openclaw-cli/openclaw_cli_skill.py` — full CLI (`health`, `status`, `models`, `channels`, `memory search`) runs inside `openclaw_gateway` container
- **Skill doc:** `/srv/arifOS/333_APPS/L2_SKILLS/openclaw-cli/SKILL.md`

---

## 8. Data Volumes & Paths

```
/srv/arifOS/                    # Git repo — canonical source of truth
/opt/arifos/
├── data/
│   ├── core/                   # arifOS runtime data
│   ├── qdrant/                 # Vector storage (LIVE)
│   ├── ollama/                 # LLM models — qwen2.5:3b (LIVE)
│   ├── openclaw/               # OpenClaw runtime data
│   │   ├── openclaw.json       # Runtime config (bind: lan, model: kimi-k2)
│   │   ├── workspace/          # Symlink → /opt/arifos/git/openclaw-workspace
│   │   ├── memory/             # Agent memory (gitignored)
│   │   └── logs/               # Gateway logs (gitignored)
│   └── n8n/                    # n8n workflow data
├── git/
│   ├── openclaw-workspace/     # ariffazil/openclaw-workspace (private)
│   └── AGI_ASI_bot/            # ariffazil/AGI_ASI_bot (private)
├── traefik/
│   ├── acme.json               # Let's Encrypt certs
│   ├── dynamic.yml             # Static routing rules
│   └── traefik.yml             # Entry points config
└── APEX-THEORY/                # ariffazil/APEX-THEORY — theory reference volume

/var/lib/docker/volumes/
├── arifos_postgres_data/       # PostgreSQL data
└── arifos_redis_data/          # Redis data
```

---

## 9. CI/CD Pipeline

### Webhook Auto-Deploy
- **Endpoint:** `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos`
- **Trigger:** GitHub push to `main`
- **Auth:** HMAC-SHA256 signature
- **Script:** `/srv/arifOS/deployment/deploy_from_git.sh`
- **Action:** `git pull` → `docker compose up --build arifosmcp` → health check

### GitHub Actions
- **Workflow:** `.github/workflows/deploy-vps.yml`
- **Tailscale VPN:** Connects GHA runner to VPS for SSH deploy
- **Symlink:** Creates `/root/arifOS → /srv/arifOS` if missing

---

## 10. API Reference

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
curl http://qdrant_memory:6333/healthz

# OpenClaw (HTTP serves SPA; management is WebSocket)
curl https://claw.arifosmcp.arif-fazil.com/healthz
```

---

## 11. Security

| Layer | Tool | Status |
|-------|------|--------|
| SSH hardening | Key-only auth, no root login | Active |
| Brute-force protection | Fail2Ban | Active |
| TLS termination | Traefik v3.6.9 + Let's Encrypt | Active |
| VPN mesh | Tailscale | Active |
| Webhook auth | HMAC-SHA256 | Active |
| Constitutional floors | F1-F13 on all MCP tools | Active |
| OpenClaw auth | Token-based (`gateway.auth.mode: token`) | Active |

---

## 12. Phased Deployment Roadmap

### Phase 1 — Core Runtime ✅ COMPLETE
- PostgreSQL 16, Redis 7, Traefik v3, arifOS MCP (13 tools)

### Phase 2 — Memory & Automation ✅ COMPLETE (2026-03-05)
- **2A:** Qdrant vector DB — `recall_memory` tool has live backend
- **2B:** Webhook CI/CD listener — auto-deploy on git push to main

### Phase 3 — Agent Workbench ✅ COMPLETE (2026-03-05)
- Ollama — local LLM engine, `qwen2.5:3b` loaded
- Prometheus + Grafana — monitoring live at `monitor.arifosmcp.arif-fazil.com`
- n8n — workflow automation live at `flow.arifosmcp.arif-fazil.com`

### Phase 4A — OpenClaw Gateway ✅ COMPLETE (2026-03-05)
- OpenClaw live at `claw.arifosmcp.arif-fazil.com`
- `bind: lan` wired in openclaw.json + Traefik labels in docker-compose.yml
- Kimi-k2 as default model; KIMI/ANTHROPIC/OPENAI API keys wired
- openclaw-workspace versioned at `ariffazil/openclaw-workspace`
- openclaw-cli skill: two-layer diagnostic integration
- `query_openclaw` MCP tool added (active after next `--build`)

### Phase 4B — Agent Zero (NEXT)
- [ ] Pull `agent0ai/agent-zero:latest` image
- [ ] Add `brain.arifosmcp.arif-fazil.com` DNS record → 72.62.71.199
- [ ] Uncomment/activate agent_zero_reasoner service in docker-compose.yml

### Phase 5 — Production Hardening (PLANNED)
- [ ] Grafana alerts → Telegram (TELEGRAM_BOT_TOKEN set)
- [ ] Backup automation — Postgres dump cron + Vault999 archive
- [ ] SSL cert audit — verify acme.json rotation
- [ ] BGE embeddings service (Phase 5 — high-quality vector embeddings)
- [ ] Consolidate Traefik routing (remove duplicate `dynamic.yml` file provider)

---

## 13. Full Stack (Current State)

```
Human
  ├── Claude Code / SSH (direct VPS control)
  ├── OpenClaw → claw.arifosmcp.arif-fazil.com     (AI gateway, kimi-k2) ← LIVE
  ├── n8n       → flow.arifosmcp.arif-fazil.com    (workflow automation)  ← LIVE
  ├── Grafana   → monitor.arifosmcp.arif-fazil.com (monitoring)           ← LIVE
  └── Agent Zero → brain.arifosmcp.arif-fazil.com  (autonomous agent UI)  ← Phase 4B

AI Agents (via MCP)
  └── arifOS MCP → arifosmcp.arif-fazil.com
        ├── recall_memory         → Qdrant          (vector memory)        ← LIVE
        ├── search_reality        → Perplexity/Brave (web search)           ← LIVE
        ├── fetch_content         → Jina             (content extract)      ← LIVE
        ├── visualize_governance  → 333_APPS         (constitutional UI)    ← LIVE
        ├── query_openclaw        → openclaw_gateway (diagnostics)          ← pending rebuild
        └── eureka_forge          → Ollama           (local LLM)            ← LIVE (qwen2.5:3b)

Infrastructure
  ├── Traefik    (TLS + routing, v3.6.9)                                   ← LIVE
  ├── PostgreSQL (constitutional vault + state)                             ← LIVE
  ├── Redis      (cache + message broker)                                   ← LIVE
  ├── Qdrant     (semantic vector memory)                                   ← LIVE
  ├── Webhook    (CI/CD auto-deploy)                                        ← LIVE
  ├── Ollama     (local LLM, qwen2.5:3b)                                   ← LIVE
  ├── Prometheus (metrics)                                                  ← LIVE
  ├── Grafana    (dashboards)                                               ← LIVE
  ├── n8n        (workflow orchestration)                                   ← LIVE
  └── OpenClaw   (AI gateway, kimi-k2)                                     ← LIVE
```

---

## 14. Key Files Reference

| File | Purpose |
|------|---------|
| `/srv/arifOS/docker-compose.yml` | Primary compose — all services |
| `/srv/arifOS/docker-compose.phase1.yml` | Legacy infra layer (postgres, redis via old network) |
| `/srv/arifOS/aaa_mcp/server.py` | 14+1 MCP tool definitions |
| `/srv/arifOS/aaa_mcp/integrations/openclaw_gateway_client.py` | OpenClaw HTTP probe + config reader |
| `/srv/arifOS/333_APPS/L2_SKILLS/openclaw-cli/SKILL.md` | openclaw-cli skill documentation |
| `/srv/arifOS/deployment/hooks.json` | Webhook trigger config |
| `/srv/arifOS/deployment/deploy_from_git.sh` | Auto-deploy script |
| `/srv/arifOS/.env` | API keys for MCP tools |
| `/opt/arifos/data/openclaw/openclaw.json` | OpenClaw runtime config (bind, model, auth) |
| `/opt/arifos/git/openclaw-workspace/` | OpenClaw agent identity + skills repo |
| `/opt/arifos/git/AGI_ASI_bot/` | Client MCP configs + persona repo |
| `/opt/arifos/traefik/acme.json` | Let's Encrypt certificate store |
| `/opt/arifos/traefik/dynamic.yml` | Static Traefik routing rules |

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
