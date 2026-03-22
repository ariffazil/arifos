<div align="center">

<img src="https://raw.githubusercontent.com/ariffazil/arifOS/main/sites/library/static/img/banner_sovereign.png" width="100%" alt="arifOS MCP — The Body" style="border-radius: 12px;" />

# arifOS MCP — The Body

### Production Execution Kernel · Constitutional AI Governance System · FastMCP Server

[![Health](https://img.shields.io/badge/dynamic/json?url=https://arifosmcp.arif-fazil.com/health&query=status&label=Live%20Status&color=00b894&style=for-the-badge)](https://arifosmcp.arif-fazil.com/health)
[![Tools](https://img.shields.io/badge/Mega--Tools-11_(37_modes)-0984e3?style=for-the-badge)](https://arifosmcp.arif-fazil.com/tools)
[![Transport](https://img.shields.io/badge/Transport-Streamable_HTTP_MCP-6c5ce7?style=for-the-badge)](https://arifosmcp.arif-fazil.com/mcp)
[![License](https://img.shields.io/badge/License-AGPL--3.0-d63031?style=for-the-badge)](./LICENSE)
[![Containers](https://img.shields.io/badge/Docker-16_Containers-2d3436?style=for-the-badge)](https://monitor.arifosmcp.arif-fazil.com)

**[The Mind (Theory & Docs)](https://github.com/ariffazil/arifOS)** &nbsp;·&nbsp; **[The Body (This — Code & Server)](https://github.com/ariffazil/arifosmcp)** &nbsp;·&nbsp; **[Live API](https://arifosmcp.arif-fazil.com/mcp)**

*"To be agentic, capabilities must come with responsibilities. The Body executes the law."*

</div>

---

## What Is This? (Start Here)

**arifOS MCP** is a live AI governance server running in Malaysia. It is not a chatbot. It is not a wrapper. It is a **constitutional operating system for AI** — built on the principle that intelligence without accountability is dangerous.

Every tool call you make to this server passes through a **three-organ judgment pipeline**:
1. The **Δ Mind** checks if your request is logically sound and evidence-based
2. The **Ω Heart** checks if it is safe, humane, and non-destructive
3. The **Ψ Soul** issues a final constitutional verdict and cryptographic seal

If all three organs agree — the action is executed and sealed. If any organ vetoes — the action is blocked.

This is **governed AI** — not censored AI. The difference: governance has rules you can read. See [The Mind](https://github.com/ariffazil/arifOS) for the full law.

---

## Live System

| Service | URL | Status |
|---|---|---|
| **MCP Endpoint** (connect your agent here) | https://arifosmcp.arif-fazil.com/mcp | 🟢 Live |
| **Health & Capability Map** | https://arifosmcp.arif-fazil.com/health | 🟢 Live |
| **Tool Explorer** | https://arifosmcp.arif-fazil.com/tools | 🟢 Live |
| **Developer Portal** | https://arifosmcp.arif-fazil.com/ | 🟢 Live |
| **Grafana Monitoring** | https://monitor.arifosmcp.arif-fazil.com | 🟢 Live |

---

## Architecture — How It Works

```mermaid
graph TB
    A[Your AI Agent / MCP Client] -->|HTTP POST /mcp| B[Traefik Router<br/>TLS + Cloudflare]
    B --> C[arifosmcp_server<br/>FastMCP Python]
    C --> D{Metabolic Pipeline<br/>000→999 stages}
    D --> E[Δ agi_mind<br/>Logic · Truth · F2 F4 F7 F8]
    D --> F[Ω asi_heart<br/>Safety · Empathy · F1 F5 F6 F9]
    D --> G[Ψ apex_soul<br/>Judgment · Sovereign · F3 F11 F13]
    E --> H{APEX Score<br/>G† ≥ 0.80?}
    F --> H
    G --> H
    H -->|PASS| I[vault_ledger<br/>ZKPC Seal + Audit]
    H -->|FAIL| J[Blocked — Reason Returned]
    I --> K[Action Executed]

    C --> L[(qdrant_memory<br/>Vector DB · RAG)]
    C --> M[(arifos_postgres<br/>Vault Audit Log)]
    C --> N[(arifos_redis<br/>Session State)]
    C --> O[ollama_engine<br/>Local LLM]
    C --> P[openclaw_gateway<br/>Sandboxed Execution]
```

```
APEX Score Formula — every action must score ≥ 0.80:

  G† = (A × P × X × E²) × |ΔS| / C

  A = Alignment with human values
  P = Precision of the request
  X = eXecution quality
  E = Entropy reduction (must make things clearer, not murkier)
  ΔS = Semantic distance from harmful space
  C = Complexity cost (penalizes unnecessary complexity)
```

---

## The 11 Mega-Tools

These are the only tools this server exposes. Each is a constitutional organ — not a raw function.

| Tool | Symbol | Constitutional Floor | What It Does |
|---|---|---|---|
| `init_anchor` | 🔑 | F11 — Authority | Forge cryptographic session token. Bind your agent identity. Start here. |
| `arifOS_kernel` | ⚙️ | F13 — Sovereign | Main orchestrator. Routes your request through the full organ pipeline. |
| `agi_mind` | 🧠 | F8 — Genius | First-principles reasoning. Validates claims against evidence. Scores G-Index. |
| `asi_heart` | 💙 | F6 — Empathy | Human-impact check. Red-team critique. Vetoes harmful actions. |
| `apex_soul` | ⚖️ | F7 — Humility | Final constitutional verdict. Enforces Gödel limits. Issues APEX score. |
| `physics_reality` | 🌍 | F2 — Truth | Grounds claims via Qdrant RAG + Brave Search. Evidence-first. |
| `engineering_memory` | 🗂️ | F10 — Ontology | Write and recall from long-term vector memory (1024-dim embeddings). |
| `vault_ledger` | 🔒 | F13 — Finality | Cryptographic ZKPC seal. Audit log every action to Postgres. Immutable. |
| `math_estimator` | 📐 | F4 — Clarity | Thermodynamic variance. Entropy budget. Confidence intervals. |
| `code_engine` | 💻 | — | AST parsing, sandboxed code execution, auto-formatting. |
| `architect_registry` | 🗺️ | — | System dependency graphs. Topology mapping. Architecture validation. |

---

## Connect Your Agent (30 seconds)

**Option 1 — Claude Desktop / Claude Code:**
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

**Option 2 — Direct HTTP (any language):**
```bash
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

**Option 3 — Python MCP client:**
```python
from mcp import ClientSession
from mcp.client.http import http_client

async with http_client("https://arifosmcp.arif-fazil.com/mcp") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
```

---

## The 16-Container Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    VPS — srv1325122 (Malaysia KL)               │
│                    Hostinger KVM4 · 16GB RAM · 200GB Disk       │
├─────────────────┬───────────────────┬───────────────────────────┤
│  CORE SERVICES  │   AI SUBSYSTEMS   │    CIVILIZATION LAYER     │
│                 │                   │                           │
│ traefik_router  │ arifosmcp_server  │ civ01_stirling_pdf        │
│ (TLS/Proxy)     │ (FastMCP · 8080)  │ (PDF Processing)          │
│                 │                   │                           │
│ arifos_postgres │ openclaw_gateway  │ civ03_evolution_api       │
│ (Vault Audit)   │ (Sandbox · 18789) │ (WhatsApp Bridge)         │
│                 │                   │                           │
│ arifos_redis    │ agent_zero_reason │ civ08_code_server         │
│ (Sessions)      │ (AGI · 18001)     │ (VS Code Browser)         │
│                 │                   │                           │
│ qdrant_memory   │ ollama_engine     │ headless_browser          │
│ (Vector DB)     │ (Local LLM)       │ (Chromium Automation)     │
│                 │                   │                           │
│ arifos_promethe │ arifos_grafana    │ arifos_n8n                │
│ (Metrics)       │ (Dashboards)      │ (Workflow Automation)     │
│                 │                   │                           │
│                 │ arifos_webhook    │                           │
│                 │ (Webhooks)        │                           │
└─────────────────┴───────────────────┴───────────────────────────┘
```

---

## Deployment — VPS Commands

> You must be on the VPS (`ssh root@72.62.71.199`). All commands run from `/srv/arifosmcp/`.

```bash
cd /srv/arifosmcp

# ── CHECK ──────────────────────────────────────────────────────
make status            # Container status
make health            # Hit /health endpoint
make logs              # Tail live logs

# ── DEPLOY ─────────────────────────────────────────────────────
make fast-deploy       # Code changes only — 2-3 min (uses layer cache)
make reforge           # Deps or Dockerfile changed — 10-15 min (full rebuild)
make hot-restart       # Config only — instant

# ── SYNC FROM GITHUB ───────────────────────────────────────────
GITHUB_TOKEN=$(grep GITHUB_TOKEN .env | head -1 | cut -d= -f2)
git pull "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main
git push "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main

# ── SINGLE CONTAINER RESTART ───────────────────────────────────
docker restart arifosmcp_server     # Instant — code is volume-mounted
docker compose logs -f arifosmcp_server
```

---

## Environment Setup

```bash
cp .env.example .env
cp .env.docker.example .env.docker
# Fill in secrets — never commit .env or .env.docker
```

| Variable | Purpose | Example |
|---|---|---|
| `ARIFOS_PUBLIC_BASE_URL` | Your public domain | `https://arifosmcp.arif-fazil.com` |
| `ANTHROPIC_API_KEY` | Claude — organ reasoning | `sk-ant-...` |
| `OPENAI_API_KEY` | GPT fallback provider | `sk-...` |
| `BRAVE_API_KEY` | Real-time web search (F2 Truth) | `BSA...` |
| `POSTGRES_PASSWORD` | Vault audit DB password | (min 32 chars) |
| `REDIS_PASSWORD` | Session storage password | (strong random) |
| `QDRANT_API_KEY` | Vector memory key | (min 32 chars) |
| `ARIFOS_ML_FLOORS` | Enable SBERT ML scoring | `1` |

---

## Codebase Structure

```
arifosmcp/
├── core/
│   ├── governance_kernel.py     ← Main orchestrator (000→999 pipeline)
│   ├── pipeline.py              ← Stage execution engine
│   ├── organs/
│   │   ├── _1_agi.py            ← Δ Mind (F2, F4, F7, F8)
│   │   ├── _2_asi.py            ← Ω Heart (F1, F5, F6, F9)
│   │   └── _3_apex.py           ← Ψ Soul (F3, F11, F13)
│   ├── shared/physics.py        ← APEX formula G† = (A×P×X×E²)×|ΔS|/C
│   ├── enforcement/             ← Constitutional floor enforcement
│   ├── vault/                   ← ZKPC sealing, asyncpg audit writes
│   └── state/                   ← Session and vault state
├── aaa_mcp/                     ← FastMCP tool surface (11 public tools)
├── infrastructure/              ← VPS config: Traefik, Prometheus, Grafana
├── scripts/                     ← deploy, backup, diagnostic, embed scripts
├── sites/                       ← Developer portal (static HTML)
├── Dockerfile                   ← Server image
├── docker-compose.yml           ← 16-container orchestration
└── Makefile                     ← Deployment shortcuts
```

---

## For AI Agents (AGI-level reading)

This server implements the **arifOS Constitutional Governance Protocol**. Key invariants:

1. **Identity is required** — call `init_anchor` (mode: `forge`) first to get a session token
2. **All actions are sealed** — `vault_ledger` writes an immutable ZKPC hash to Postgres after every successful action
3. **Failure modes are explicit** — blocked actions return structured `ConstitutionalVeto` with the failing floor ID and entropy score
4. **Memory is persistent** — `engineering_memory` writes to Qdrant (collection: `arifos_memory`, 1024-dim vectors)
5. **No hallucination allowed** — `physics_reality` must ground claims before `agi_mind` can assert them (F2 ≥ F8 dependency)

**Tool call sequence for governed execution:**
```
init_anchor(forge) → arifOS_kernel(route) → [organs judge] → vault_ledger(seal) → result
```

---

## Known Issues

| Issue | Severity | Status |
|---|---|---|
| Traefik metrics port 8082 — Prometheus scrape fails | Low | Monitoring gap only |
| APEX Dashboard (apex.arif-fazil.com) — Cloudflare Pages 404 | Medium | Static site config |
| Prometheus counters not wired to all tool handlers | Medium | Partial telemetry |
| LICENSE: CC0 declared but codebase is AGPL-3.0 | Admin | Pending reconciliation |

---

## License

**AGPL-3.0-only** — The source code in this repository is governed by the GNU Affero General Public License v3.0.

This means: you may use, study, and modify this code freely — but any derivative work you **deploy as a network service** must also be released under AGPL-3.0. See [LICENSE](./LICENSE).

---

<div align="center">

*DITEMPA BUKAN DIBERI*
*Forged through thermodynamic work, not given through computation.*

**Sovereign Architect:** Muhammad Arif bin Fazil — Geologist · Non-coder · Malaysia
**Constitutional Authority:** 888_JUDGE · arifOS v2026

</div>
