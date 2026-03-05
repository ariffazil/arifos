# arifOS VPS — Deployment Status

**Last Updated:** 2026-03-05
**Version:** v2026.3.1
**Phase:** 2B Complete — Phase 3 Next

---

## Live Services

| Service | Status | URL / Access |
|---------|--------|--------------|
| arifOS MCP Server | HEALTHY | `https://arifosmcp.arif-fazil.com/mcp` |
| Traefik Router | UP | `:80` → `:443` (auto-redirect) |
| PostgreSQL 16 | HEALTHY | `localhost:5432` |
| Redis 7 | HEALTHY | `localhost:6379` |
| Qdrant | UP | `http://qdrant:6333` (internal) |
| Webhook CI/CD | UP | `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos` |

---

## arifOS MCP — Tool Status

**Endpoint:** `https://arifosmcp.arif-fazil.com/mcp`
**Transport:** Streamable HTTP
**Tools loaded:** 13

| Tool | Status | Notes |
|------|--------|-------|
| `anchor_session` | LIVE | |
| `reason_mind` | LIVE | |
| `recall_memory` | LIVE | Qdrant backend active (Phase 2A) |
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

---

## Constitutional Governance

All 13 tools protected by F1-F13 constitutional floors.

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

## CI/CD Pipeline

- **GitHub → VPS:** Push to `main` triggers webhook at `hook.arifosmcp.arif-fazil.com`
- **Auth:** HMAC-SHA256 verified
- **Deploy:** `git pull` → rebuild arifosmcp image → restart → health check
- **Fallback:** GitHub Actions via Tailscale SSH (`.github/workflows/deploy-vps.yml`)

---

## Not Yet Deployed

| Service | Phase | Reason |
|---------|-------|--------|
| Ollama (local LLM) | 3 | Image not pulled |
| Prometheus + Grafana | 3 | Configs ready, not in compose yet |
| n8n (workflow automation) | 3 | Not in compose yet |
| Agent Zero | 4 | Image not pulled, APEX-THEORY dir missing |
| OpenClaw | 4 | Image needs source build |

---

## Phase Log

| Phase | Scope | Status | Date |
|-------|-------|--------|------|
| 1 | PostgreSQL, Redis, Traefik, arifOS MCP | COMPLETE | — |
| 2A | Qdrant vector memory | COMPLETE | 2026-03-05 |
| 2B | Webhook CI/CD listener | COMPLETE | 2026-03-05 |
| 3 | Ollama, Prometheus, Grafana, n8n | NEXT | — |
| 4 | Agent Zero, OpenClaw | PLANNED | — |
| 5 | Production hardening, monitoring alerts | PLANNED | — |

---

**DITEMPA BUKAN DIBERI**
