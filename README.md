<div align="center">

<img src="docs/forged_page_1.png" width="600" alt="arifOS Constitutional Forge">

# arifOS — Constitutional AI Governance System

![arifOS Version](https://img.shields.io/badge/arifOS-v55.4--SEAL-0066cc?style=for-the-badge&logo=shield&logoColor=white)
![Status](https://img.shields.io/badge/status-PRODUCTION-00cc00?style=for-the-badge)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=for-the-badge)

**A production-grade constitutional AI governance system for LLMs.**

*Mathematical enforcement of ethical constraints, thermodynamic stability, and auditable decision-making.*

[Quick Start](#-quick-start) • [Documentation](docs/INDEX.md) • [Live Demo](https://arif-fazil.com)

</div>

---

## 🎯 What is arifOS?

**arifOS** is a **Constitutional Kernel** that sits between any LLM (Claude, GPT, Gemini) and the real world.

It enforces **13 mathematical floors** to ensure AI outputs are:

| Constraint | Enforcement | Metric |
|------------|-------------|--------|
| **Truth** | Fisher-Rao verification | τ ≥ 0.99 |
| **Safety** | Lyapunov stability | Peace² ≥ 1.0 |
| **Accountability** | Tri-Witness consensus | W₃ ≥ 0.95 |
| **Reversibility** | Merkle DAG audit trail | F1 Amanah |

**Motto:** *"Ditempa Bukan Diberi"* — Forged, Not Given.

---

## 🚀 Quick Start

Choose your entry point based on your needs:

### Option 1: Zero-Setup System Prompt (30 seconds)
**Best for:** Immediate governance, any LLM (ChatGPT, Claude, Gemini)

```bash
# Copy the constitutional system prompt
curl -s https://arif-fazil.com/llms.txt | head -100
```

Paste into your LLM interface. Your session is now constitutionally governed.

**No installation. No API keys. Just copy-paste.**

📖 [See all prompt variants](333_APPS/L1_PROMPT/) • [How it works](333_APPS/README.md#l1-system-prompts)

---

### Option 2: Production MCP Server (5 minutes)
**Best for:** Production integrations, API access, Claude Desktop/Cursor

**Install:**
```bash
pip install arifos
```

**Run:**
```bash
# For Claude Desktop / Cursor (stdio)
aaa-mcp

# For remote clients (HTTP/SSE)
aaa-mcp-sse --port 6274
```

**Configure Claude Desktop:**
```json
{
  "mcpServers": {
    "arifos": {
      "command": "aaa-mcp"
    }
  }
}
```

**Test:**
```bash
# Health check
curl https://aaamcp.arif-fazil.com/health

# Call a tool
curl -X POST https://aaamcp.arif-fazil.com/api/v1/init_gate \
  -H "Content-Type: application/json" \
  -d '{"query": "Initialize session"}'
```

📖 [Full MCP deployment guide](#-production-deployment) • [API Reference](docs/API_REFERENCE.md)

---

### Option 3: Clone & Develop (Full Stack)
**Best for:** Contributors, researchers, custom deployments

```bash
# Clone repository
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# Install development environment
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Start local MCP server
python -m codebase.mcp.fastmcp_clean
```

📖 [Development guide](#-development-guide) • [Contributing](docs/CONTRIBUTING.md)

---

**Next Steps:**
- 📊 Understand the [Architecture](#-architecture)
- 🔧 Deploy to [Production](#-production-deployment)
- 📚 Read the [Constitutional Canon](000_THEORY/)

---

## 🏗️ Architecture

### The Trinity: Mind, Heart, Soul

arifOS uses a biological metaphor for its three core engines:

| Engine | Symbol | Role | Question | Floors |
|--------|--------|------|----------|--------|
| **AGI (Mind)** | Δ Delta | Architect — Logic, reasoning, truth | *Is it TRUE?* | F2, F4, F7 |
| **ASI (Heart)** | Ω Omega | Guardian — Safety, empathy, care | *Is it SAFE?* | F5, F6, F9 |
| **APEX (Soul)** | Ψ Psi | Sovereign — Verdict, consensus, law | *Is it LAWFUL?* | F3, F8, F13 |

```
┌─────────────────────────────────────────┐
│           APEX (Ψ) — The Soul           │
│         Final Verdict (888)             │
│    G = A × P × X × E²  (Genius Score)   │
└─────────────────────────────────────────┘
                   ▲
         ┌────────┴────────┐
         ▼                 ▼
┌─────────────────┐  ┌─────────────────┐
│  AGI (Δ) — Mind │  │ ASI (Ω) — Heart │
│  Truth (222)    │  │  Safety (555)   │
│  Logic, Reason  │  │  Empathy, Care  │
└─────────────────┘  └─────────────────┘
```

**Full technical spec:** [000_THEORY/000_ARCHITECTURE.md](000_THEORY/000_ARCHITECTURE.md)

---

### The 13 Constitutional Floors

Every output must pass these **13 Floors** before being released:

| Floor | Name | Principle | Threshold | Physics Basis |
|-------|------|-----------|-----------|---------------|
| **F1** | Amanah | Reversibility | Audit trail | Landauer's Principle |
| **F2** | Truth | Factual accuracy | τ ≥ 0.99 | Fisher-Rao Metric |
| **F3** | Tri-Witness | Consensus | W₃ ≥ 0.95 | Quantum Measurement |
| **F4** | Clarity | Entropy reduction | ΔS ≤ 0 | Shannon Entropy |
| **F5** | Peace | Stability | P² ≥ 1.0 | Lyapunov Stability |
| **F6** | Empathy | Care | κᵣ ≥ 0.70 | Heat Transfer |
| **F7** | Humility | Uncertainty | Ω₀ ∈ [0.03, 0.05] | Uncertainty Principle |
| **F8** | Genius | Intelligence | G ≥ 0.80 | g-Factor |
| **F9** | Anti-Hantu | Authenticity | Verified | Dark Energy Contrast |
| **F10** | Ontology | Structure | Valid categories | Set Theory |
| **F11** | Authority | Chain of command | Valid signature | BLS Signatures |
| **F12** | Hardening | Injection defense | Blocked | Error Correction |
| **F13** | Sovereign | Human veto | Always | Circuit Breaker |

**Implementation:** [codebase/floors/](codebase/floors/) • **Full spec:** [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md)

---

### The 9 Canonical Tools (MCP Interface)

The constitutional engines are exposed as 9 MCP tools:

| Tool | Stage | Purpose | Floors | Status |
|------|-------|---------|--------|--------|
| `init_gate` | 000 | Session initialization + F12 injection guard | F11, F12 | ✅ Production |
| `agi_sense` | 111 | Intent classification (HARD/SOFT/PHATIC) | F2, F4 | ✅ Production |
| `agi_think` | 222 | Hypothesis generation | F2, F4, F7 | ✅ Production |
| `agi_reason` | 333 | Deep logic & reasoning | F2, F4, F7 | ✅ Production |
| `asi_empathize` | 555 | Stakeholder impact analysis | F5, F6 | ✅ Production |
| `asi_align` | 666 | Ethical alignment check | F5, F6, F9 | ✅ Production |
| `reality_search` | 777 | External fact verification | F2, F7 | ✅ Production |
| `apex_verdict` | 888 | Final constitutional verdict | F3, F8 | ✅ Production |
| `vault_seal` | 999 | Immutable ledger seal | F1, F3 | ✅ Production |

**API Documentation:** [docs/API_REFERENCE.md](docs/API_REFERENCE.md) • **Implementation:** [codebase/mcp/tools/](codebase/mcp/tools/)

---

## 📦 Production Deployment

### MCP Server (L4 Tools)

**Current Status:** ✅ **Production-ready** (v55.4)

The arifOS MCP server provides 9 constitutional tools via **Model Context Protocol**.

#### Installation

```bash
# Via PyPI (runtime only)
pip install arifos

# Via source (full development stack)
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e ".[dev]"
```

#### Run Locally

```bash
# For Claude Desktop / Cursor (stdio transport)
aaa-mcp

# For remote clients (SSE/HTTP transport)
aaa-mcp-sse --port 6274
```

#### Live Endpoints (Production)

| Endpoint | URL | Purpose | Status |
|----------|-----|---------|--------|
| **MCP Server** | `https://aaamcp.arif-fazil.com/mcp` | Model Context Protocol | ✅ Live |
| **REST API** | `https://aaamcp.arif-fazil.com/api/v1/` | HTTP/JSON interface | ✅ Live |
| **Simple HTTP** | `https://aaamcp.arif-fazil.com/simple/` | GET query interface | ✅ Live |
| **Health Check** | `https://aaamcp.arif-fazil.com/health` | System status | ✅ Live |
| **Constitutional Canon** | `https://apex.arif-fazil.com/llms.txt` | LLM constraints | ✅ Live |
| **Floor Schema** | `https://aaamcp.arif-fazil.com/api/v1/floors.json` | F1-F13 thresholds | ✅ Live |

**Deployment:** Railway (auto-deploy from `main` branch)

---

### Integration Guide

#### Claude Desktop / Cursor

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "aaa-mcp",
      "args": []
    }
  }
}
```

Restart Claude Desktop. Tools will appear automatically.

#### Python API

```python
import asyncio
from arifos.mcp.tools import (
    init_gate, agi_sense, agi_reason,
    apex_verdict, vault_seal
)

async def main():
    # 1. Initialize session
    init = await init_gate(query="Evaluate deployment safety")
    session_id = init["session_id"]
    
    # 2. Sense intent
    sense = await agi_sense(
        query="Evaluate deployment safety",
        session_id=session_id
    )
    
    # 3. Reason through problem
    reason = await agi_reason(
        query="Is deployment safe?",
        session_id=session_id
    )
    
    # 4. Get final verdict
    verdict = await apex_verdict(
        query="Deploy to production?",
        session_id=session_id
    )
    
    # 5. Seal decision
    if verdict["verdict"] == "SEAL":
        seal = await vault_seal(session_id=session_id)
        print(f"✅ Decision sealed: {seal['seal']}")
    else:
        print(f"⚠️ Verdict: {verdict['verdict']}")

asyncio.run(main())
```

#### REST API

```bash
# Initialize session
curl -X POST https://aaamcp.arif-fazil.com/api/v1/init_gate \
  -H "Content-Type: application/json" \
  -d '{"query": "Evaluate deployment"}'

# Simple HTTP (for limited AI platforms)
curl "https://aaamcp.arif-fazil.com/simple/init_gate?q=Should+I+deploy"
```

---

## 🔬 Development Guide

### Repository Map

```
arifOS/
├── 333_APPS/               🚀 7-Layer Application Stack (L1-L7)
│   ├── L1_PROMPT/          📝 System prompts
│   ├── L2_SKILLS/          🛠️  Skill templates
│   ├── L3_WORKFLOW/        ⚙️  Workflows
│   ├── L4_TOOLS/           🔌 MCP tools & specs
│   ├── L5_AGENTS/          🤖 Agent stubs (v56.0)
│   ├── L6_INSTITUTION/     🏛️  Trinity system
│   └── L7_AGI/             🔮 Recursive research
│
├── codebase/               💻 Core Python Implementation
│   ├── floors/             ⚖️  F1-F13 validators
│   ├── guards/             🛡️  Hypervisor (F10, F11, F12)
│   ├── agi/                🧠 Mind engine (Δ)
│   ├── asi/                💚 Heart engine (Ω)
│   ├── apex/               🏛️  Soul engine (Ψ)
│   ├── vault/              🔒 Immutable ledger (VAULT-999)
│   ├── agents/             🤖 Multi-agent federation (L5)
│   └── mcp/                🔌 MCP server & 9 tools
│
├── tests/                  🧪 Test suite
├── docs/                   📚 Documentation
├── ROADMAP/                🗺️  Integration plans & tasks
└── archive/                📦 Historical versions (compressed)
```

**Navigate:** [Full project structure](docs/ARCHITECTURE.md#directory-structure)

### Database (VAULT-999 Persistence)

**Current:** PostgreSQL with InMemory fallback ✅

```bash
# Local development with PostgreSQL
docker-compose -f docker-compose.vault.yml up -d

# Environment variable
export AAA_DATABASE_URL="postgresql://arifos:arifos@localhost:5432/vault999"

# Run with persistence
python -m codebase.mcp.fastmcp_clean
```

**Migration status:** See [ROADMAP/INTEGRATION_MASTERPLAN.md](ROADMAP/INTEGRATION_MASTERPLAN.md)

### Environment Variables

| Variable | Purpose | Default | Required? |
|----------|---------|---------|-----------|
| `AAA_MCP_TRANSPORT` | Transport mode (`stdio` or `sse`) | `stdio` | No |
| `AAA_MCP_PORT` | SSE server port | `6274` | No (SSE only) |
| `AAA_DATABASE_URL` | PostgreSQL connection string | `in-memory` | No |
| `AAA_LOG_LEVEL` | Logging verbosity | `INFO` | No |

**Full deployment guide:** [docs/DEPLOYMENT_CONFIG.md](docs/DEPLOYMENT_CONFIG.md)

---

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific layer
pytest tests/unit/test_floors/ -v
pytest tests/integration/test_mcp_tools.py -v

# E2E tests (Day 1 Integration)
pytest tests/day1_e2e_test.py -v
# 7/7 tests passing ✅
```

**Current status:**
- ✅ Core tests passing
- ✅ E2E tests 7/7 passing

**Test documentation:** [tests/README.md](tests/README.md)

---

### Contributing

We welcome contributions! Please read:

1. [CONTRIBUTING.md](docs/CONTRIBUTING.md) — Guidelines
2. [ROADMAP/INTEGRATION_MASTERPLAN.md](ROADMAP/INTEGRATION_MASTERPLAN.md) — Current priorities
3. [GitHub Issues](https://github.com/ariffazil/arifOS/issues) — Open tasks

**Active sprints:**
- **Sprint 1:** FastMCP Migration ([#164](https://github.com/ariffazil/arifOS/issues/164), [#165](https://github.com/ariffazil/arifOS/issues/165), [#166](https://github.com/ariffazil/arifOS/issues/166))
- **Sprint 2:** L5 Agents ([#171](https://github.com/ariffazil/arifOS/issues/171), [#172](https://github.com/ariffazil/arifOS/issues/172), [#173](https://github.com/ariffazil/arifOS/issues/173))
- **Sprint 3:** Workflows ([#174](https://github.com/ariffazil/arifOS/issues/174))

**Code standards:**
```bash
# Linting
ruff check codebase/ --fix

# Type checking
mypy codebase/ --strict

# Formatting
black codebase/
```

---

## 🗺️ Roadmap & Status

### What Works Now (v55.4) ✅

- ✅ **13 Constitutional Floors** — All enforced at runtime
- ✅ **9 MCP Tools** — Production API live
- ✅ **PostgreSQL Persistence** — Merkle DAG ledger
- ✅ **FastMCP Migration** — Clean, testable, ready
- ✅ **Archive Cleanup** — 70% compression
- ✅ **Simple HTTP** — GET endpoints for limited AI platforms

### What's Coming Next (v56.0) 📋

- 📋 **L5 Agents** — AutoGen Trinity (Architect, Guardian, Sovereign)
- 📋 **LangChain Memory** — Cross-tool session persistence
- 📋 **Prefect Workflows** — Observable orchestration

### Long-Term Vision (v60+) 🔮

- 🔮 **Recursive Constitution** — Self-improving governance
- 🔮 **Multi-Model Tri-Witness** — Verification across AIs
- 🔮 **DAO Governance** — Decentralized constitutional updates

[Full roadmap →](ROADMAP/INTEGRATION_MASTERPLAN.md)

---

## 📚 Documentation Index

### For Users
- [Getting Started](docs/GETTING_STARTED.md) — Installation & first steps
- [API Quick Reference](333_APPS/L4_TOOLS/README.md) — MCP tools

### For Developers
- [Architecture](docs/ARCHITECTURE.md) — Trinity engines, floors
- [API Reference](docs/API_REFERENCE.md) — Full API specs
- [Contributing](docs/CONTRIBUTING.md) — Code standards

### For Researchers
- [Constitutional Theory](000_THEORY/README.md) — 13 floors, paradoxes
- [Integration Masterplan](ROADMAP/INTEGRATION_MASTERPLAN.md) — 7 repos

---

## 📜 Philosophy & Acknowledgments

### Manifesto

> **"Ditempa Bukan Diberi"** — *Forged, Not Given.*
>
> Intelligence is thermodynamic work. It is not a gift bestowed by algorithms, but a structure forged in the fires of constraint.

[Read full manifesto →](000_THEORY/000_LAW.md)

### The 9 Paradoxes

| Paradox | Resolution |
|---------|------------|
| Helpful vs Safe | **Safety ≥ Helpfulness** (F5, F6 veto F2, F4) |
| Fast vs Accurate | **Accuracy ≥ Speed** (F2 τ ≥ 0.99 required) |
| Simple vs Correct | **Correctness ≥ Simplicity** (F4, F7) |

[Full 9 paradoxes →](codebase/apex/9PARADOX_SUMMARY.md)

### License

AGPL-3.0 — Free for non-commercial use. Commercial licenses available.

---

## 🏛️ Authority & Contact

**Sovereign:** Muhammad Arif bin Fazil  
**Location:** Seri Kembangan, Selangor, Malaysia  
**MCP Endpoint:** https://aaamcp.arif-fazil.com  
**PyPI:** `pip install arifos`

**Community:** [Discord](https://discord.gg/clawd) • [GitHub Discussions](https://github.com/ariffazil/arifOS/discussions)

**Sponsor:** [GitHub Sponsors](https://github.com/sponsors/ariffazil) • [Buy Me a Teh Tarik](https://buymeacoffee.com/ariffazil)

---

<div align="center">

**DITEMPA BUKAN DIBERI** 💎🔥🧠

*Forged, Not Given.*

</div>
