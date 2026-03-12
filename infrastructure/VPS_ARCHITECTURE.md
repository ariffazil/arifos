# arifOS VPS — Unified Architecture Snapshot

**Last verified:** 2026-03-11 by Claude Code (claude-sonnet-4-6)
**Version:** 2026.3.10-METABOLIC-ROUTER-SEAL
**Status:** ✅ ALL 12 CONTAINERS RUNNING

> This is the single source of truth for the VPS state.
> Do not maintain multiple architecture docs — update this one file.

---

## 1. Server Facts

| Item | Value |
|------|-------|
| Hostname | `srv1325122` |
| Public IP | `2a02:4780:5e:dbf6::1` |
| Disk | 193GB total — 84GB used (44%) — 110GB free |
| Swap | 4GB swapfile |
| Deploy path | `/srv/arifOS/` |
| Docker network | `arifos_arifos_trinity` (bridge, `10.0.10.0/24`) |

---

## 2. Live Container State

All 12 containers running as of 2026-03-11.

| Container | Image | Status | Exposed Port |
|-----------|-------|--------|-------------|
| `traefik_router` | `traefik:v3.6.9` | ✅ Up | 80, 443 (public) |
| `arifosmcp_server` | `arifos/arifosmcp:latest` | ✅ Up (healthy) | 127.0.0.1:8080 |
| `arifos_postgres` | `postgres:16-alpine` | ✅ Up (healthy) | 0.0.0.0:5432 ⚠️ |
| `arifos_redis` | `redis:7-alpine` | ✅ Up (healthy) | 0.0.0.0:6379 ⚠️ |
| `qdrant_memory` | `qdrant/qdrant:latest` | ✅ Up | internal only |
| `ollama_engine` | `ollama/ollama:latest` | ✅ Up | internal only |
| `openclaw_gateway` | `ghcr.io/openclaw/openclaw:latest` | ✅ Up (healthy) | 127.0.0.1:18789 |
| `headless_browser` | `ghcr.io/browserless/chromium:latest` | ✅ Up (healthy) | internal only |
| `agent_zero_reasoner` | `agent0ai/agent-zero:latest` | ✅ Up | internal only |
| `arifos_n8n` | `n8nio/n8n:latest` | ✅ Up | internal only |
| `arifos_prometheus` | `prom/prometheus:latest` | ✅ Up | internal only |
| `arifos_grafana` | `grafana/grafana:latest` | ✅ Up (healthy) | internal only |

> ⚠️ Postgres (5432) and Redis (6379) are bound to 0.0.0.0 — reachable from outside Docker. Should be restricted to 127.0.0.1.

---

## 3. Public URLs

| URL | Service |
|-----|---------|
| https://arifosmcp.arif-fazil.com/mcp | Live MCP endpoint |
| https://arifos.arif-fazil.com | Constitutional docs (GitHub Pages) |
| https://apex.arif-fazil.com | APEX Theory (GitHub Pages) |
| https://arif-fazil.com | Owner profile |
| https://monitor.arifosmcp.arif-fazil.com | Grafana monitoring |

---

## 4. Three-Tier Sovereign Architecture

```
LAW     arifos.arif-fazil.com   GitHub Pages  — immutable constitutional docs
BRAIN   arifosmcp.arif-fazil.com  VPS         — live MCP server, Trinity engine
SOUL    apex.arif-fazil.com     GitHub Pages  — APEX Theory, G† >= 0.80
```

---

## 5. Request Flow (Metabolic Loop 000-999)

```
MCP Client (Claude / GPT / Telegram)
        |
        v
  Traefik (TLS, routing)
        |
        v
  arifosmcp_server :8080
        |
   000  INIT      — F12 injection shield
   111  MIND      — Truth, Clarity, Humility
   444  MIND      — Genius scoring
   555  HEART     — Peace, Empathy, Anti-Hantu
   777  APEX      — G†=(AxPxXxE2)x|dS|/C >= 0.80
   999  VAULT     — Merkle-hash -> PostgreSQL
        |
   Verdict: SEAL | PARTIAL | SABAR | VOID | 888_HOLD
```

---

## 6. Service Dependencies

```
arifosmcp_server
  ├── qdrant_memory       (vector search, BGE-M3 768-dim)
  ├── ollama_engine       (local LLMs: qwen2.5, bge-m3)
  ├── arifos_postgres     (VAULT999 ledger)
  ├── arifos_redis        (session cache)
  ├── headless_browser    (JS page fetching)
  └── arifos_prometheus   -> arifos_grafana

openclaw_gateway
  ├── Telegram bot @arifOS_bot
  ├── kimi API (auth fixed 2026-03-11)
  └── qmd v2.0.1 (vector memory, fixed 2026-03-11)
```

---

## 7. Docker Volumes

| Volume | Purpose |
|--------|---------|
| `arifos_postgres_data` | VAULT999 ledger (permanent) |
| `arifos_redis_data` | Session cache |
| `arifosmcp_arifosmcp_vault` | Vault storage |
| `arifosmcp_arifosmcp_memory` | Agent memory |
| `arifosmcp_arifosmcp_telemetry` | Telemetry |
| `arifosmcp_arifosmcp_static` | Static files |
| `arifos_openclaw_config` | OpenClaw config |
| `openclaw_gateway` | OpenClaw runtime |

---

## 8. Key Files

| File | Purpose |
|------|---------|
| `/srv/arifOS/docker-compose.yml` | Main stack |
| `/srv/arifOS/docker-compose.override.yml` | Dev overrides (code mounts) |
| `/srv/arifOS/.env` | Compose-level env vars |
| `/srv/arifOS/.env.docker` | Full env for arifosmcp container |
| `/srv/arifOS/infrastructure/traefik.yml` | Traefik static config |
| `/srv/arifOS/infrastructure/dynamic.yml` | Traefik dynamic routing |
| `/root/CONTEXT.md` | Shared agent context (owner + project brief) |
| `/root/CLAUDE.md` | Claude Code agent instructions |
| `/root/AGENTS.md` | All-agent instructions |

---

## 9. Security Posture

| Control | Status |
|---------|--------|
| Non-root containers | ✅ arifosmcp runs as arifos:1000 |
| NoNewPrivileges | ✅ All services |
| Resource limits | ✅ CPU + memory on all |
| TLS termination | ✅ Traefik |
| Postgres exposed on 0.0.0.0:5432 | ⚠️ Should be 127.0.0.1 |
| Redis exposed on 0.0.0.0:6379 | ⚠️ Should be 127.0.0.1 |
| ARIFOS_888_JUDGE_KEY | ⚠️ Should go offline/HSM |
| OpenClaw sandbox | ⚠️ Needs hardening review |

---

## 10. OpenClaw State

| Item | Value |
|------|-------|
| Telegram bot | @arifOS_bot (running) |
| qmd binary | @tobilu/qmd v2.0.1 (fixed 2026-03-11) |
| Kimi auth | Restored (fixed 2026-03-11) |
| Auth profiles | `/root/.openclaw/agents/main/agent/auth-profiles.json` |

---

## 11. AI Agents on This Server

| Tool | Version | Command |
|------|---------|---------|
| Claude Code | current | `claude` |
| kimi-cli | 1.18.0 | `kimi` |
| opencode | 1.2.24 | `opencode` |
| gemini CLI | 0.33.0 | `gemini` |
| codex CLI | 0.114.0 | `codex` |
| aider | 0.86.2 | `aider` |
| GitHub Copilot CLI | 0.1.36 | `github-copilot-cli` |
| GitHub MCP Server | v0.32.0 | `github-mcp-server stdio` |

---

## 12. Common Commands

```bash
# Update stack
cd /srv/arifOS && git pull origin main && docker compose up -d

# Restart one service
docker restart <container_name>

# Tail logs
docker logs -f <container_name>

# Check all health
docker ps --format 'table {{.Names}}\t{{.Status}}'

# Disk check
df -h / && docker system df

# Free unused image space
docker image prune -f
```

---

## 13. Open Issues

| Priority | Issue |
|----------|-------|
| HIGH | Postgres + Redis exposed on 0.0.0.0 — restrict to 127.0.0.1 |
| MEDIUM | ARIFOS_888_JUDGE_KEY should move to offline/HSM |
| MEDIUM | OpenClaw sandbox needs hardening |
| LOW | Grafana dashboards not wired to G†/ΔS metrics yet |
| LOW | Prometheus metrics not yet exported from arifosmcp_server |

---

## 14. Retired / Replaced Docs

The following old docs are superseded by this file:
- `infrastructure/VPS_STATE_UPDATE_20260310.md`
- Any previous `VPS_ARCHITECTURE.md` versions

*Update this file after every significant VPS change. One doc, one truth.*
