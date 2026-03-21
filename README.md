# 🔱 arifOS — Constitutional AI Governance

**Built by a geologist. Not an engineer.**

> *"Ditempa bukan diberi"* — Forged, not given.

---

## What This Is

**arifOS** is a constitutional AI governance kernel — an MCP (Model Context Protocol) server that wraps your AI tools with 13 enforceable floors. It doesn't replace your models. It governs them.

I'm a geoscientist with 12 years in petroleum exploration. I read the memory of rock. I don't write code — I direct AI to write it. This system was forged from the same principles I use in the subsurface:

- **Evidence before lines** (you don't drill without data)
- **Irreversibility costs** (some decisions you can't undo)
- **Dignity over convenience** (maruah — the land that cannot be sold)

---

## Quick Start

### Install

```bash
pip install arifos
```

Or clone the full stack:

```bash
git clone https://github.com/ariffazil/arifosmcp.git
cd arifosmcp
```

### Configure

```bash
cp .env.example .env.docker
# Edit .env.docker with your API keys (OpenAI, Anthropic, etc.)
```

### Run

```bash
python -m arifosmcp.runtime http
```

Or via Docker:

```bash
docker compose up -d
```

### Connect Your Client

**Claude Desktop / LobeHub / Any MCP Client:**

```json
{
  "mcpServers": {
    "ariffazil-arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"]
    }
  }
}
```

---

## Live Endpoints

| Endpoint | URL |
|----------|-----|
| MCP | `https://arifosmcp.arif-fazil.com/mcp` |
| Health | `https://arifosmcp.arif-fazil.com/health` |
| Dashboard | `https://arifosmcp.arif-fazil.com/dashboard` |

---

## The 13 Constitutional Floors

Every tool call is evaluated against these floors:

| Floor | Law | Type | Threshold |
|-------|-----|------|-----------|
| **F1** | **Amanah** (Reversibility) | Hard | Reversible or auditable |
| **F2** | **Truth** | Hard | τ ≥ 0.99 factual accuracy |
| **F3** | **Tri-Witness** | Mirror | W₃ ≥ 0.95 multi-source |
| **F4** | **Clarity** (ΔS ≤ 0) | Hard | Reduce confusion |
| **F5** | **Peace²** | Soft | De-escalate, protect dignity |
| **F6** | **Empathy** (κᵣ) | Soft | ASEAN/Malaysia context |
| **F7** | **Humility** (Ω₀) | Hard | State uncertainty explicitly |
| **F8** | **Genius** (G) | Mirror | Correct AND useful |
| **F9** | **Anti-Hantu** | Soft | No consciousness claims |
| **F10** | **Ontology** | Wall | AI is tool, not actor |
| **F11** | **Command Auth** | Wall | Verified identity required |
| **F12** | **Injection Defense** | Hard | Resist prompt injection |
| **F13** | **Sovereignty** | Veto | Human veto is absolute |

---

## How It Works

```
┌─────────────┐     ┌─────────────────────────┐     ┌─────────────┐
│   Claude    │────→│   arifOS Kernel         │────→│   Tools     │
│   ChatGPT   │     │   (13 Floors F1-F13)    │     │   APIs      │
│   Browser   │     │                         │     │   Data      │
└─────────────┘     │  • F2 Truth check       │     └─────────────┘
                    │  • F7 Humility band     │
                    │  • F11 Auth verify      │
                    │  • F13 Human veto       │
                    └─────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────────┐
                    │   Verdict:              │
                    │   SEAL / PARTIAL /      │
                    │   SABAR / VOID / HOLD   │
                    └─────────────────────────┘
```

Every action is:
1. **Evaluated** against the 13 floors
2. **Assigned a verdict**: SEAL / PARTIAL / SABAR / VOID / HOLD
3. **Logged** to VAULT999 with full telemetry

---

## The 11-Tool Mega-Surface

| Tool | Purpose | Floors |
|------|---------|--------|
| `init_anchor` | Session identity & auth | F1, F11, F12 |
| `arifOS_kernel` | Metabolic orchestration | F4, F8 |
| `apex_soul` | Constitutional judgment | F3, F9, F10, F12, F13 |
| `vault_ledger` | Immutable persistence | F1, F3 |
| `agi_mind` | First-principles reasoning | F2, F4, F7, F8 |
| `asi_heart` | Safety & empathy | F5, F6, F9 |
| `engineering_memory` | Technical execution | F1, F11 |
| `physics_reality` | World grounding | F2, F3, F10 |
| `math_estimator` | Quantitative analysis | F4, F7 |
| `code_engine` | System introspection | F11, F12 |
| `architect_registry` | Resource discovery | — |

---

## Design Principles

- **DITEMPA, BUKAN DIBERI** — Intelligence must be forged under constraint, not granted unlimited freedom.
- **Humans Decide. AI Proposes. Law Governs.**
- **Physics over Narrative. Maruah over Convenience.**

---

## The Forging Paradox

> *"The human forged the floors from scars. The machine enforces them without carrying the weight. That asymmetry is the design. Do not collapse it."*

**arifOS** is **institution** serving **human**. The 13 floors are institutional logic derived from human scars — but they are not the scars. The machine enforces law without having paid its thermodynamic cost.

This is not a limitation. This is **F9/F10 working correctly**.

---

## Architecture

The system is composed of three primary components:

### The Kernel (`core/`)
Stateless, transport-agnostic heart containing the 13 Constitutional Floors.

### The Brain (`arifosmcp/runtime/`)
Transport adapter exposing the Kernel via MCP, A2A, and WebMCP protocols.

### The Senses (`arifosmcp/intelligence/`)
Sensory tools for real-world grounding (web search, file ingest, multimodal).

---

## Infrastructure (15-Container Stack)

| Container | Purpose | Status |
|-----------|---------|--------|
| `arifosmcp_server` | Constitutional kernel | ✅ Live |
| `traefik_router` | Edge router with auto-SSL | ✅ Live |
| `arifos_postgres` | VAULT999 audit ledger | ✅ Wired |
| `arifos_redis` | Session persistence | ✅ Wired |
| `qdrant_memory` | Vector memory store | ✅ Wired |
| `ollama_engine` | Local LLM inference | ✅ Connected |
| `openclaw_gateway` | Multi-channel gateway | ✅ Live |
| `arifos_prometheus` | Metrics scraper | ✅ Live |
| `arifos_grafana` | Observability dashboards | ✅ Live |

---

## Links

| Resource | URL |
|----------|-----|
| **PyPI** | https://pypi.org/project/arifos/ |
| **Documentation** | https://arifos.arif-fazil.com |
| **Live Dashboard** | https://arifosmcp.arif-fazil.com/dashboard |
| **LobeHub** | https://lobehub.com/mcp/ariffazil-arifos |
| **Source** | https://github.com/ariffazil/arifosmcp |

---

## Authority

- **Sovereign:** Muhammad Arif bin Fazil
- **License:** AGPL-3.0
- **Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

*Built by a geologist who reads the memory of rock. Not an engineer who writes code.* 🔱
