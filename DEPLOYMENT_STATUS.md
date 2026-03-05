# arifOS VPS — Deployment Status

**Last Updated:** 2026-03-05
**Version:** v2026.3.2
**Phase:** 4 Partial — OpenClaw live, Agent Zero pending

---

## Live Services

| Service | Status | URL / Access |
|---------|--------|--------------|
| arifOS MCP Server | HEALTHY | `https://arifosmcp.arif-fazil.com/mcp` |
| Traefik Router | UP | `:80` → `:443` (auto-redirect) |
| PostgreSQL 16 | HEALTHY | `localhost:5432` (arifos-internal) |
| Redis 7 | HEALTHY | `localhost:6379` (arifos-internal) |
| Qdrant | UP | `http://qdrant_memory:6333` (internal) |
| Ollama | UP | `http://ollama_engine:11434` (internal) — qwen2.5:3b loaded |
| OpenClaw | HEALTHY | `https://claw.arifosmcp.arif-fazil.com` |
| Prometheus | UP | `http://arifos_prometheus:9090` (internal) |
| Grafana | UP | `https://monitor.arifosmcp.arif-fazil.com` |
| n8n | UP | `https://flow.arifosmcp.arif-fazil.com` |
| Webhook CI/CD | UP | `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos` |

---

## arifOS MCP — Tool Status

**Endpoint:** `https://arifosmcp.arif-fazil.com/mcp`
**Transport:** Streamable HTTP
**Tools loaded:** 14 (15 after next rebuild — `query_openclaw` pending image bake)

| Tool | Status | Notes |
|------|--------|-------|
| `anchor_session` | LIVE | |
| `reason_mind` | LIVE | |
| `recall_memory` | LIVE | Qdrant backend active |
| `simulate_heart` | LIVE | |
| `critique_thought` | LIVE | |
| `eureka_forge` | LIVE | |
| `apex_judge` | LIVE | |
| `seal_vault` | LIVE | Token-locked |
| `search_reality` | LIVE | Perplexity + Brave keys set |
| `fetch_content` | LIVE | Jina key set |
| `inspect_file` | LIVE | |
| `audit_rules` | LIVE | |
| `check_vital` | LIVE | |
| `visualize_governance` | LIVE | Constitutional Visualizer UI |
| `query_openclaw` | PENDING | In server.py; active after next `docker compose up --build arifosmcp` |

---

## Constitutional Governance

All tools protected by F1-F13 constitutional floors.

| Floor | Name | Status |
|-------|------|--------|
| F1 | Amanah (Reversibility) | Active |
| F2 | Truth (τ ≥ 0.99) | Active |
| F3 | Tri-Witness | Active |
| F4 | Clarity (ΔS ≤ 0) | Active |
| F5 | Peace² | Active |
| F6 | Empathy (κᵣ ≥ 0.70) | Active |
| F7 | Humility (Ω₀ = 0.04) | Active |
| F8 | Genius (G ≥ 0.80) | Active |
| F9 | Anti-Hantu | Active |
| F10 | Ontology | Active |
| F11 | Command Auth | Active |
| F12 | Injection Defense | Active |
| F13 | Sovereign | Active — human veto always preserved |

---

## Three-Repo Architecture

| Repo | Role | Location |
|------|------|----------|
| `ariffazil/arifOS` | Kernel, MCP server, Docker infra, VAULT999 | `/srv/arifOS` |
| `ariffazil/openclaw-workspace` | OpenClaw agent OS — AGENTS/SOUL/TOOLS/skills | `/opt/arifos/git/openclaw-workspace` |
| `ariffazil/AGI_ASI_bot` | Client personas, governance files, hooks | `/opt/arifos/git/AGI_ASI_bot` |

---

## CI/CD Pipeline

- **GitHub → VPS:** Push to `main` triggers webhook at `hook.arifosmcp.arif-fazil.com`
- **Auth:** HMAC-SHA256 verified
- **Deploy:** `git pull` (via alpine container with SSH keys) → rebuild arifosmcp image → restart → health check
- **Fallback:** GitHub Actions via Tailscale SSH (`.github/workflows/deploy-vps.yml`)

---

## Not Yet Deployed

| Service | Phase | Notes |
|---------|-------|-------|
| Agent Zero | 4 | Image not pulled — `agent0ai/agent-zero:latest`; needs `brain.arifosmcp.arif-fazil.com` DNS |

---

## Phase Log

| Phase | Scope | Status | Date |
|-------|-------|--------|------|
| 1 | PostgreSQL, Redis, Traefik, arifOS MCP | COMPLETE | — |
| 2A | Qdrant vector memory | COMPLETE | 2026-03-05 |
| 2B | Webhook CI/CD listener | COMPLETE | 2026-03-05 |
| 3 | Ollama, Prometheus, Grafana, n8n | COMPLETE | 2026-03-05 |
| 4A | OpenClaw gateway — LAN bind, Traefik TLS, model keys wired | COMPLETE | 2026-03-05 |
| 4B | Agent Zero | NEXT | — |
| 5 | Production hardening: alerts, backups, SSL audit | PLANNED | — |

---

**DITEMPA BUKAN DIBERI**
