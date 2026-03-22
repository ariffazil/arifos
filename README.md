# arifOS MCP — The Body

**Production execution kernel of the arifOS Constitutional AI Governance System.**

> The Mind defines the law. The Body executes it.

[![Health](https://img.shields.io/badge/dynamic/json?url=https://arifosmcp.arif-fazil.com/health&query=status&label=Server&color=00b894)](https://arifosmcp.arif-fazil.com/health)
[![Tools](https://img.shields.io/badge/Mega--Tools-11_(37_modes)-blue)](https://arifosmcp.arif-fazil.com/tools)
[![Transport](https://img.shields.io/badge/Transport-Streamable_HTTP-purple)](https://arifosmcp.arif-fazil.com/mcp)
[![Containers](https://img.shields.io/badge/Containers-16_running-success)](https://monitor.arifosmcp.arif-fazil.com)

| Repo | Purpose |
|---|---|
| [ariffazil/arifOS](https://github.com/ariffazil/arifOS) | **The Mind** — theory, constitution, governance docs |
| [ariffazil/arifosmcp](https://github.com/ariffazil/arifosmcp) | **The Body** — this repo, FastMCP server, Docker stack |

---

## Live Endpoints

| Endpoint | URL |
|---|---|
| MCP Gateway (agents connect here) | https://arifosmcp.arif-fazil.com/mcp |
| Health + Capability Map | https://arifosmcp.arif-fazil.com/health |
| Tool Explorer | https://arifosmcp.arif-fazil.com/tools |
| Developer Portal | https://arifosmcp.arif-fazil.com/ |
| Grafana Monitoring | https://monitor.arifosmcp.arif-fazil.com |

---

## What This Is

A **FastMCP streamable-http server** that exposes 11 mega-tools (37 modes) to AI agents. Every tool call passes through a constitutional metabolic pipeline — three organs judge each request before it executes:

| Organ | Symbol | Role | Constitutional Floors |
|---|---|---|---|
| `agi_mind` | Δ Mind | First-principles logic and truth verification | F2, F4, F7, F8 |
| `asi_heart` | Ω Heart | Safety check, empathy, red-team veto | F1, F5, F6, F9 |
| `apex_soul` | Ψ Soul | Final judgment, sovereign override | F3, F11, F13 |

All three organs must pass before a `vault_ledger` seal is issued. APEX score threshold: **G† ≥ 0.80**

```
G† = (A × P × X × E²) × |ΔS| / C
```

---

## The 11 Mega-Tools

| Tool | Constitutional Floor | Function |
|---|---|---|
| `init_anchor` | F11 Authority | Forge sovereign session tokens, bind identity |
| `arifOS_kernel` | F13 Sovereign | Main orchestrator — routes requests through organs |
| `agi_mind` | F8 Genius | First-principles reasoning, truth analysis, G-Index scoring |
| `asi_heart` | F6 Empathy | Human-impact check, safety veto, constraint alignment |
| `apex_soul` | F7 Humility | Constitutional score, Gödel boundary check |
| `physics_reality` | F2 Truth | Ground claims via Qdrant RAG + Brave Search |
| `engineering_memory` | F10 Ontology | Long-term vector memory (write, recall, graph) |
| `vault_ledger` | F13 Finality | Cryptographic ZKPC action sealing and audit |
| `math_estimator` | F4 Clarity | Thermodynamic variance, entropy budget calculation |
| `code_engine` | — | AST parsing, code execution, auto-formatting |
| `architect_registry` | — | Dependency graphs, system topology mapping |

---

## Connect an MCP Client

Add to Claude Desktop, Cursor, or any MCP-compatible client:

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "http",
      "url": "https://arifosmcp.arif-fazil.com/mcp"
    }
  }
}
```

---

## 16-Container Stack

```
traefik_router        — TLS reverse proxy (Cloudflare, ports 80/443)
arifosmcp_server      — FastMCP server, port 8080
openclaw_gateway      — Sandboxed agent execution, port 18789
agent_zero_reasoner   — AGI reasoning layer, port 18001
qdrant_memory         — Vector DB, 1024-dim embeddings, port 6333
ollama_engine         — Local LLM generation, port 11434
arifos_postgres       — Vault audit log (asyncpg), port 5432
arifos_redis          — Session storage, vault backend, port 6379
arifos_prometheus     — Metrics scraper, port 9090
arifos_grafana        — Monitoring dashboards
arifos_n8n            — Workflow automation
arifos_webhook        — Incoming webhook processor
headless_browser      — Chromium browser automation
civ08_code_server     — VS Code in browser
civ01_stirling_pdf    — PDF processing
civ03_evolution_api   — WhatsApp API bridge
```

---

## Deployment (VPS — you are already on it)

```bash
cd /srv/arifosmcp

# Status and health
make status
make health

# Reload after code changes — instant (volume-mounted)
docker restart arifosmcp_server

# Deploy code changes (2–3 min, uses layer cache)
make fast-deploy

# Full rebuild — only if Dockerfile or dependencies changed (10–15 min)
make reforge

# Tail logs
make logs

# Pull latest from GitHub
GITHUB_TOKEN=$(grep GITHUB_TOKEN .env | head -1 | cut -d= -f2)
git pull "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main

# Push to GitHub
git push "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main
```

---

## Environment Setup

Copy `.env.example` → `.env` and `.env.docker.example` → `.env.docker`, then fill in secrets.

Key variables:

| Variable | Purpose |
|---|---|
| `ARIFOS_PUBLIC_BASE_URL` | Public URL (https://arifosmcp.arif-fazil.com) |
| `POSTGRES_*` | Vault audit database (host: `arifos_postgres`) |
| `REDIS_*` | Session storage (host: `arifos_redis`) |
| `QDRANT_*` | Vector memory (host: `qdrant_memory:6333`) |
| `ANTHROPIC_API_KEY` | Claude API — organ reasoning |
| `OPENAI_API_KEY` | GPT fallback provider |
| `BRAVE_API_KEY` | Real-time web search (F2 grounding) |
| `ARIFOS_ML_FLOORS` | Set to `1` to enable SBERT ML floor scoring |

---

## Codebase Structure

```
arifosmcp/core/
  governance_kernel.py     Main orchestrator — metabolic pipeline (000→999 stages)
  pipeline.py              Stage execution engine
  organs/
    _1_agi.py              Δ Mind — logic, truth (F2, F4, F7, F8)
    _2_asi.py              Ω Heart — safety, empathy (F1, F5, F6, F9)
    _3_apex.py             Ψ Soul — judgment, sovereign override (F3, F11, F13)
  shared/physics.py        APEX formula: G† = (A×P×X×E²)×|ΔS|/C
  enforcement/             Constitutional floor enforcement (F1–F13)
  vault/                   ZKPC sealing, asyncpg audit writes
  state/                   Session and vault state management

aaa_mcp/                   Public MCP tool surface (FastMCP definitions)
infrastructure/            VPS config, Traefik, Prometheus, Grafana
scripts/                   deploy, backup, diagnostic, embed scripts
sites/                     Developer portal static HTML
Dockerfile                 Server image
docker-compose.yml         16-container orchestration
Makefile                   Deployment shortcuts
```

---

## Known Issues

| Issue | Priority |
|---|---|
| Traefik metrics port 8082 — Prometheus scrape fails | Low |
| APEX Dashboard (apex.arif-fazil.com) — Cloudflare Pages 404 | Medium |
| Prometheus counters not fully wired to all tool handlers | Medium |
| LICENSE: CC0 declared but code is AGPL-3.0 | Pending reconciliation |

---

*DITEMPA BUKAN DIBERI — Forged through thermodynamic work, not given through computation.*
*Authority: Muhammad Arif bin Fazil — Sovereign Architect*
