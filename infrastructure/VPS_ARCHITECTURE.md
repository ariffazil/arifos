# arifOS VPS — Unified Architecture Snapshot

**Last verified:** 2026-03-12 by Claude Code (claude-sonnet-4-6)
**Git HEAD:** `1af6d53b` — fix(deploy): add scripts/run_evals.py [2026.03.12-SEAL]
**Server version:** `2026.03.10-FORGED`
**Status:** ✅ ALL 12 CONTAINERS RUNNING — VPS = GitHub = Live

> Single source of truth for VPS state. All agents update this file after significant changes.

---

## 1. Server Facts

| Item | Value |
|------|-------|
| Hostname | `srv1325122` |
| Public IPv6 | `2a02:4780:5e:dbf6::1` |
| OS | Linux 6.17.0-14-generic |
| Disk | 85GB / 193GB used (44%) |
| RAM | 3.5GB / 15GB used |
| Load avg | ~0.1–0.4 (idle) |
| Deploy path | `/srv/arifosmcp/` (symlinked from `/srv/arifOS/`) |
| Compose file | `/srv/arifosmcp/docker-compose.yml` |

---

## 2. Git Sync State

| Location | Commit | Status |
|----------|--------|--------|
| VPS `/srv/arifosmcp` | `1af6d53b` | ✅ |
| GitHub `ariffazil/arifosmcp` main | `1af6d53b` | ✅ |
| **Alignment** | **Identical** | ✅ **SEALED** |

Remote URL uses HTTPS + token (no SSH key on VPS):
```bash
GITHUB_TOKEN=$(grep GITHUB_TOKEN .env | head -1 | cut -d= -f2)
git pull "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main
git push "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main
```

---

## 3. Containers — Live State

| Container | Image | Status | Memory | Port Binding |
|-----------|-------|--------|--------|--------------|
| `arifosmcp_server` | `arifos/arifosmcp:latest` | ✅ healthy | 93MB / 3GB | `127.0.0.1:8080` |
| `traefik_router` | `traefik:v3.6.9` | ✅ up | 85MB / 128MB | `0.0.0.0:80,443` |
| `arifos_postgres` | `postgres:16-alpine` | ✅ healthy | 18MB / 1GB | `127.0.0.1:5432` |
| `arifos_redis` | `redis:7-alpine` | ✅ healthy | 4MB / 128MB | `127.0.0.1:6379` |
| `arifos_grafana` | `grafana/grafana:latest` | ✅ healthy | 91MB / 1GB | internal only |
| `arifos_prometheus` | `prom/prometheus:latest` | ✅ up | 35MB / 1GB | internal only |
| `openclaw_gateway` | `ghcr.io/openclaw/openclaw:latest` | ✅ healthy | 563MB / 2GB | `127.0.0.1:18789` |
| `qdrant_memory` | `qdrant/qdrant:latest` | ✅ up | 159MB / 1GB | internal only |
| `ollama_engine` | `ollama/ollama:latest` | ✅ up | 296MB / 1.5GB | internal only |
| `headless_browser` | `ghcr.io/browserless/chromium:latest` | ✅ healthy | 91MB / 1GB | internal only |
| `agent_zero_reasoner` | `agent0ai/agent-zero:latest` | ✅ up | 784MB / 1GB | internal only |
| `arifos_n8n` | `n8nio/n8n:latest` | ✅ up | 317MB / 1GB | internal only |

**Network:** `arifos_arifos_trinity` bridge — `10.0.10.0/24`

**Security posture:**
- Postgres (`5432`) and Redis (`6379`) bound to `127.0.0.1` only ✅
- MCP server (`8080`) bound to `127.0.0.1` only — exposed via Traefik ✅
- Only ports 80 and 443 are public-facing ✅

---

## 4. Public URLs

| Layer | Name | URL | Hosting |
|-------|------|-----|---------|
| Brain | MCP server | https://arifosmcp.arif-fazil.com/mcp | VPS (Traefik) |
| Brain | Health | https://arifosmcp.arif-fazil.com/health | VPS |
| Brain | Tools | https://arifosmcp.arif-fazil.com/tools | VPS |
| Brain | Discovery | https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json | VPS |
| Law | arifOS docs | https://arifos.arif-fazil.com | GitHub Pages |
| Soul | APEX Theory | https://apex.arif-fazil.com | Cloudflare Pages |
| Soul | APEX Dashboard | https://arifosmcp-truth-claim.pages.dev | Cloudflare Pages (⚠️ 404) |
| Eye | Monitoring | https://monitor.arifosmcp.arif-fazil.com | Grafana on VPS |

---

## 5. arifosmcp Server — Intelligence Kernel

**Version:** `2026.03.10-FORGED`
**Transport:** `streamable-http` (MCP 2025-11-25 spec)
**Auth:** Open — `api_bearer_auth: not_configured` (zero friction for adoption)
**ML floors:** `ml_floors_enabled: false` — heuristic mode (SBERT not loaded)

### 8 Public Tools

| Tool | Stage | Role |
|------|-------|------|
| `arifOS_kernel` | 444_ROUTER | Main metabolic orchestrator (000→999 pipeline) |
| `search_reality` | 111_SENSE | Web grounding via Perplexity/Brave/Jina |
| `ingest_evidence` | 222_REALITY | Extract and load evidence from URLs |
| `session_memory` | — | Governed session continuity (Qdrant-backed) |
| `audit_rules` | 333_MIND | Inspect all 13 constitutional floors |
| `check_vital` | 000_INIT | System vitality, thermo-budget, capability map |
| `bootstrap_identity` | 000_INIT | Declare user identity — onboarding entry point (new) |
| `open_apex_dashboard` | — | Open live governed metrics dashboard |

### Discovery Doc
```
GET /.well-known/mcp/server.json
transports: [http, stdio]   ← SSE removed (was advertised but 404)
auth: none
tools: 8
```

### Metabolic Loop (000 → 999)
```
000 INIT    — Airlock, injection shield (F12), identity grounding
111–333     — MIND: truth (F2), clarity (F4), humility (F7), genius (F8)
444         — ROUTER: constitutional routing via arifOS_kernel
555–666     — HEART: peace (F5), empathy (F6), anti-hantu (F9)
777–888     — APEX: discipline, Quad-Witness BFT, verdict
999 VAULT   — Merkle-hash seal to PostgreSQL+Redis ledger
```

---

## 6. Ollama — Local LLMs

| Model | Size | Purpose |
|-------|------|---------|
| `bge-m3:latest` | 1.2GB | Embeddings (768-dim) for Qdrant vector memory |
| `nomic-embed-text:latest` | 274MB | Lightweight embeddings |
| `qwen2.5:3b` | 1.9GB | Local reasoning / fallback LLM |

---

## 7. Observability

### Prometheus Scrape Targets
| Job | Status | Notes |
|-----|--------|-------|
| `arifos-mcp` | ✅ up | Scrapes `/metrics` — constitutional metrics live |
| `prometheus` | ✅ up | Self-monitoring |
| `qdrant` | ✅ up | Vector DB metrics |
| `traefik` | ❌ down | Port 8082 not enabled (low priority) |

### Key Prometheus Metrics
- `arifos_genius_score` — G† per session/tool
- `arifos_entropy_delta` — ΔS clarity metric
- `arifos_humility_band` — Ω₀ uncertainty band
- `arifos_verdicts_total` — SEAL/VOID/HOLD_888/PARTIAL counts
- `arifos_metabolic_loop_seconds` — pipeline latency histogram
- `arifos_requests_total` — request counter

---

## 8. Request Flow

```
Internet → Cloudflare (CDN + DDoS) → VPS :443
  → Traefik v3.6.9 (TLS termination, routing)
    → arifosmcp_server :8080 (FastMCP + FastAPI)
      → Constitutional floors F1–F13
        → Trinity engines (Δ Mind / Ω Heart / Ψ APEX)
          → Tool execution
            → VAULT999 (Postgres + Redis, Merkle-hashed)
```

---

## 9. Key File Paths

| Path | Purpose |
|------|---------|
| `/srv/arifosmcp/` | Main repo (symlinked from `/srv/arifOS/`) |
| `/srv/arifosmcp/docker-compose.yml` | Container orchestration |
| `/srv/arifosmcp/.env` | Runtime secrets (never commit) |
| `/srv/arifosmcp/.env.docker` | Docker-injected env (never commit) |
| `/srv/arifosmcp/arifosmcp/runtime/` | FastMCP server, routes, tools, registry |
| `/srv/arifosmcp/core/` | Trinity engines, floors, physics, vault |
| `/srv/arifosmcp/scripts/run_evals.py` | Constitutional Dashboard eval generator |
| `/opt/arifos/data/core/` | Persistent data volume (mounted into container) |
| `/root/CONTEXT.md` | Shared agent context — read first |
| `/root/CLAUDE.md` | Claude Code instructions |
| `/root/AGENTS.md` | All AI agents guide |

---

## 10. Critical Environment Variables

| Variable | Purpose | Set? |
|----------|---------|------|
| `ARIFOS_GOVERNANCE_SECRET` | Core auth secret | ✅ |
| `DATABASE_URL` | PostgreSQL connection | ✅ |
| `REDIS_URL` | Cache connection | ✅ |
| `GITHUB_TOKEN` | GitHub API + push | ✅ |
| `OPENCLAW_GATEWAY_TOKEN` | OpenClaw auth | ✅ |
| `ARIFOS_888_JUDGE_KEY` | Sovereign human veto | ✅ |
| `ARIFOS_API_KEY` | Bearer auth for MCP | ❌ not set = open access (intentional) |
| `COPILOT_API_KEY` | Copilot Studio X-API-Key | ❌ not set (optional) |
| `ARIFOS_PUBLIC_TOOL_PROFILE` | Tool surface profile | `chatgpt` |

---

## 11. Common Commands

```bash
cd /srv/arifosmcp

# Sync with GitHub
GITHUB_TOKEN=$(grep GITHUB_TOKEN .env | head -1 | cut -d= -f2)
git pull "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main

# Restart MCP server (picks up code from mounted volume instantly)
docker restart arifosmcp_server

# Restart any service
docker compose up -d --no-deps <service>

# Tail logs
docker logs -f arifosmcp_server

# Full status
docker ps && docker stats --no-stream

# Health check
curl -s https://arifosmcp.arif-fazil.com/health | python3 -m json.tool
```

---

## 12. Known Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| Traefik metrics port 8082 unreachable | ⚠️ Low | App unaffected |
| APEX Dashboard 404 | ⚠️ Low | Cloudflare Pages deploy broken |
| ML floors disabled | ℹ️ Info | Set `ARIFOS_ML_FLOORS=1` to enable SBERT |
| Grafana dashboards not wired | ℹ️ Info | Prometheus scraping works; dashboards need setup |
| OpenClaw image models 404 | ⚠️ Low | claude-opus-4-5/4-6 model IDs changed |
| arifOS LICENSE = CC0 vs AGPL docs | ⚠️ Medium | Needs reconciliation |

---

## 13. Session Changes Log (2026-03-11/12)

| Change | Status |
|--------|--------|
| Grafana restarted (was DOWN) | ✅ Done |
| Postgres + Redis locked to 127.0.0.1 | ✅ Done |
| GitHub MCP server installed (`github-mcp-server` v0.32.0) | ✅ Done |
| OpenClaw qmd fixed (`@tobilu/qmd` v2.0.1) | ✅ Done |
| OpenClaw auth-profiles.json restored | ✅ Done |
| SSE removed from discovery doc | ✅ Done |
| `/metrics` Prometheus scraping fixed | ✅ Done |
| PR #268 merged (Copilot Studio + `bootstrap_identity` tool) | ✅ Done |
| VPS and GitHub main aligned at `1af6d53b` | ✅ SEALED |

*Last verified: 2026-03-12 by Claude Code (claude-sonnet-4-6)*
