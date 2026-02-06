# arifOS — Constitutional AI Governance System

> **ΔΩΨ-governed constitutional kernel for AI agents.**
> 
> *Ditempa Bukan Diberi — Forged, Not Given* 💎🔥🧠🔱

[![arifOS](https://img.shields.io/badge/arifOS-v55.5--EIGEN-0066cc?style=for-the-badge)](https://github.com/ariffazil/arifOS)
[![Status](https://img.shields.io/badge/status-WORK_IN_PROGRESS-yellow?style=for-the-badge)]()
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=for-the-badge)]()

![arifOS Forged](docs/forged_page_1.png)

*Ditempa Bukan Diberi — Forged, Not Given*

---

## 📋 Table of Contents

- [What is arifOS?](#what-is-arifos)
- [Quick Start](#quick-start)
- [AAA MCP Server](#aaa-mcp-server)
- [333_APPS](#333_apps)
- [Repository Structure](#repository-structure)
- [Architecture](#architecture)
- [Theory](#theory)
- [Deployment](#deployment)
- [Trinity Ecosystem](#trinity-ecosystem)
- [Documentation](#documentation)

---

## 🎯 What is arifOS?

arifOS is a **constitutional AI governance system** that makes AI agents safer, more accountable, and thermodynamically stable.

**The Core Idea:** AI outputs must pass 13 constitutional "floors" (rules) before reaching users. Think of it as a constitution for AI — like how countries have laws to protect citizens.

### The Problem with Current AI

| Issue | Real Example | arifOS Fix |
|-------|-------------|------------|
| 🎭 **Hallucination** | AI makes up facts confidently | F2 (Truth) — 99% certainty required |
| 🕷️ **Manipulation** | Jailbroken by clever prompts | F9 (Anti-Hantu) — no manipulation |
| ⚡ **Speed > Safety** | Rushed outputs with errors | F1 (Amanah) — reversible actions only |
| 👻 **No Accountability** | Decisions vanish into void | F13 (Stewardship) — audit ledger |

### The 13 Floors (Non-Negotiable Rules)

| Floor | Name | Principle |
|-------|------|-----------|
| F1 | **AMANAH** | Reversibility — every decision can be undone |
| F2 | **TRUTH** | Evidence required; 99% certainty for facts |
| F3 | **TRI-WITNESS** | Validate with 3 sources when uncertain |
| F4 | **CLARITY** | Precision over performance |
| F5 | **PEACE²** | No harm; dignity (Maruah) preserved |
| F6 | **EMPATHY** | Care for human context |
| F7 | **HUMILITY** | Track uncertainty (Ω₀ 0.00-1.00) |
| F8 | **GENIUS** | Excellence, not adequacy |
| F9 | **ANTI-HANTU** | No manipulation, no spiritual cosplay |
| F10 | **ONTOLOGY** | Identity fixed |
| F11 | **AUTHORITY** | Human sovereign supreme |
| F12 | **HARDENING** | Security always |
| F13 | **SOVEREIGN** | Human has final veto |

**Verdicts:**
- ✅ **SEAL** — Compliant; proceed
- ⏸️ **SABAR** — Uncertain; pause and escalate  
- ❌ **VOID** — Violation; block and suggest alternative

---

## 🚀 Quick Start

### Option 1: Use the AAA MCP Server (5 minutes)

arifOS exposes its governance through an **MCP (Model Context Protocol) server**:

```bash
# Clone the repo
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# Install dependencies
pip install -r requirements.txt

# Start the MCP server
python start_server.py

# Server runs on http://localhost:8080
# Healthcheck: curl http://localhost:8080/health
```

**MCP Endpoint:** `aaamcp.arif-fazil.com/mcp`

### Option 2: Read the Theory (10 minutes)

**[000_THEORY.md](000_THEORY.md)** — Reverse Transformer Architecture

Learn about:
- Dual-pass governance (Forward + Reverse + Metabolizer)
- Non-stationary objectives with stationary constraints
- Thermodynamic stability (Peace²)

### Option 3: Deploy the Full Trinity System (30 minutes)

See **[AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot)** for:
- Dual-agent implementation (AGI + ASI)
- Eureka Engine with drift detection
- Live execution guide

```bash
git clone https://github.com/ariffazil/AGI_ASI_bot.git
cd AGI_ASI_bot
openclaw agent start --config agi/config.yaml
```

---

## 🔧 AAA MCP Server

The **AAA (Atomic Actions Architecture) MCP Server** provides constitutional governance as a service.

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check — returns `{status: "ok"}` |
| `/mcp` | POST | Main MCP endpoint for tool calls |
| `/` | GET | Root info — service status |

### The 9 AAA MCP Tools

| # | Tool | Floors | Description |
|---|------|--------|-------------|
| 1 | `init_gate` | F11, F12 | Initialize constitutional session |
| 2 | `agi_sense` | F2, F4 | AGI sense/perceive |
| 3 | `agi_think` | F2, F4, F7 | AGI think/process |
| 4 | `agi_reason` | F2, F4, F7 | AGI reason/logic |
| 5 | `asi_empathize` | F5, F6 | ASI empathy/care |
| 6 | `asi_align` | F5, F6, F9 | ASI alignment/safety |
| 7 | `apex_verdict` | F3, F8 | APEX judgment/decision |
| 8 | `reality_search` | F2, F7 | External fact verification |
| 9 | `vault_seal` | F1, F3 | Immutable ledger seal |

**Source:** [`mcp_server/server.py`](mcp_server/server.py)

### Example Usage

```python
import requests

# Initialize constitutional session
response = requests.post("http://localhost:8080/mcp", json={
    "tool": "init_gate",
    "params": {
        "query": "Deploy to production",
        "session_id": "sess_123"
    }
})

# Returns: {"verdict": "SEAL", "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠", "floors_enforced": ["F11", "F12"]}

# AGI reasoning
response = requests.post("http://localhost:8080/mcp", json={
    "tool": "agi_reason",
    "params": {
        "query": "Analyze this data",
        "session_id": "sess_123"
    }
})

# ASI alignment check
response = requests.post("http://localhost:8080/mcp", json={
    "tool": "asi_align",
    "params": {
        "query": "Is this safe?",
        "session_id": "sess_123"
    }
})

# Seal to ledger
response = requests.post("http://localhost:8080/mcp", json={
    "tool": "vault_seal",
    "params": {
        "session_id": "sess_123",
        "verdict": "SEAL",
        "payload": {"action": "deploy", "result": "success"}
    }
})
```

### Environment Variables

```bash
PORT=8080              # Server port
HOST=0.0.0.0           # Bind address
ARIFOS_ENV=production  # Environment
ARIFOS_LOG_LEVEL=info  # Logging level
API_KEY=your_key       # API authentication
DATABASE_URL=...       # Database connection
REDIS_URL=...          # Redis connection
```

**Source:** [`.env.example`](.env.example)

---

## 📱 333_APPS

The **333_APPS** directory contains the application layer of arifOS — production-ready implementations and integrations.

```
333_APPS/
├── L0_DNA/           # Core genetic code (immutable)
├── L1_FOUNDATION/    # Foundation layer (kernel, constitution)
├── L2_TOOLS/         # Tool implementations
├── L3_DATA/          # Data layer
├── L4_MCP/           # MCP server implementations
├── L5_RUNTIME/       # Runtime environments
├── L6_INTEGRATION/   # Third-party integrations
└── L7_DEPLOYMENT/    # Deployment configurations
```

**Purpose:** While `mcp_server/` contains the reference MCP implementation, `333_APPS/` contains the **production-hardened** versions with:
- Enterprise security (F12 Hardening)
- Multi-environment configs
- Integration tests
- Performance optimizations

**See:** [`333_APPS/`](333_APPS/) directory

---

## 📁 Repository Structure

```
arifOS/
├── 000_THEORY.md              # ← Reverse Transformer theory [START HERE]
├── 000_THEORY/                # ← Extended theory documents
├── AGENTS.md                  # ← Agent configuration guide
├── CHANGELOG.md               # ← Version history
├── CONTRIBUTING.md            # ← Contribution guidelines
├── DEPLOYMENT_CONFIG.md       # ← Deployment configuration
├── DEPLOYMENT_TIPS.md         # ← Deployment troubleshooting
├── HANDOFF_000_INIT_LOOP.md   # ← Initialization handoff guide
├── LICENSE                    # ← AGPL-3.0 License
├── README.md                  # ← This file
├── RELEASE_v55.3.md           # ← v55.3 release notes
├── SECURITY.md                # ← Security policy
├── llms.txt                   # ← LLM context file
│
├── 333_APPS/                  # ← Application layer (L0-L7)
├── VAULT999/                  # ← Secure storage
├── codebase/                  # ← Core implementation
│   ├── init.py               # ← Initialization exports
│   └── ...
├── docs/                      # ← Documentation
│   ├── API_REFERENCE.md      # ← API documentation
│   ├── APPLICATIONS.md       # ← Application guides
│   ├── ARCHITECTURE_AND_NAMING_v45.md
│   ├── COMPARISON.md         # ← Framework comparisons
│   └── ... (50+ docs)
├── examples/                  # ← Usage examples
├── integrations/              # ← Third-party integrations
├── mcp_server/                # ← MCP server implementation
│   ├── server.py             # ← FastMCP server
│   └── tools/                # ← Tool implementations
│       └── canonical_trinity.py
├── reports/                   # ← Analysis reports
├── scripts/                   # ← Utility scripts
├── setup/                     # ← Setup configurations
├── skills/                    # ← Skill definitions
├── templates/                 # ← Templates
├── tests/                     # ← Test suite
│
├── Dockerfile                 # ← Container image
├── railway.toml              # ← Railway deployment config
├── pyproject.toml            # ← Python package config
├── requirements.txt          # ← Python dependencies
├── start_server.py           # ← Server entry point
└── test_import.py            # ← Import tests
```

---

## 🏛️ Architecture

### Layer Stack

```
┌─────────────────────────────────────────┐
│           APEX(Ψ)                       │
│     Human Sovereign (You)               │
│     888 Judge                           │
└─────────────┬───────────────────────────┘
              │
    ┌─────────▼──────────┐
    │   arifOS           │  ← This repo
    │   Constitution     │     (Theory + MCP)
    │   (13 Floors)      │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  AGI_ASI_bot       │  ← Operational layer
    │  Eureka Engine     │     (Dual agents)
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  OpenClaw          │  ← Runtime
    │  (Base framework)  │
    └────────────────────┘
```

### Key Components

| Component | Path | Purpose |
|-----------|------|---------|
| **Theory** | [`000_THEORY.md`](000_THEORY.md) | Constitutional framework |
| **MCP Server** | [`mcp_server/server.py`](mcp_server/server.py) | FastMCP implementation |
| **Tools** | [`mcp_server/tools/`](mcp_server/tools/) | 9 AAA tools |
| **Apps** | [`333_APPS/`](333_APPS/) | Production layer |
| **Docs** | [`docs/`](docs/) | Full documentation |
| **Examples** | [`examples/`](examples/) | Usage examples |

---

## 📖 Theory

### Reverse Transformer Architecture

Standard LLMs work like this:
```
Input → Generate → Output
```

arifOS adds a **reverse pass**:
```
Input → Generate → [GOVERNANCE CHECK] → Output
                    ↓
              Constitution
              (F1-F13)
```

**Forward Pass:** Generate possibilities (entropy increase)  
**Reverse Pass:** Filter through constraints (entropy decrease)  
**Metabolizer:** Learn and update state (stability increase)

This creates **thermodynamic governance**: every pass must reduce entropy and increase Peace².

### Key Concepts

| Concept | Meaning |
|---------|---------|
| **Non-Stationary Objectives** | Human goals drift over time (survival → status → legacy) |
| **Stationary Constraints** | F1-F13 never change, regardless of goals |
| **Ω₀ (Omega)** | Uncertainty measure (0.00-1.00). Target: 0.03-0.05 |
| **Scars** | 6 permanent constraints hard-coded by pain |
| **Paradox Engine** | 9 human paradoxes held, not resolved |

**Full theory:** [`000_THEORY.md`](000_THEORY.md)

---

## 🚢 Deployment

### Railway (Recommended)

```bash
# Railway auto-detects Dockerfile
git push origin main

# Or deploy via CLI
railway login
railway link
railway up
```

**Configuration:** [`railway.toml`](railway.toml)

**Railway Variables:**
```
PORT=8080
HOST=0.0.0.0
ARIFOS_ENV=production
```

### Docker

```bash
# Build
docker build -t arifos .

# Run
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e HOST=0.0.0.0 \
  arifos
```

**Dockerfile:** [`Dockerfile`](Dockerfile)

### Local Development

```bash
# Install
pip install -r requirements.txt
pip install -e .

# Run
python start_server.py

# Test
curl http://localhost:8080/health
```

**Requirements:** [`requirements.txt`](requirements.txt)  
**Package:** [`pyproject.toml`](pyproject.toml)

---

## 🌐 The Trinity Ecosystem

arifOS is part of a three-layer system:

| Layer | Symbol | Domain | Function | URL |
|-------|--------|--------|----------|-----|
| **HUMAN** | Δ | arif-fazil.com | Epistemic — The Body | [arif-fazil.com](https://arif-fazil.com) |
| **THEORY** | Ψ | apex.arif-fazil.com | Authority — The Soul | [apex.arif-fazil.com](https://apex.arif-fazil.com) |
| **APPS** | Ω | arifos.arif-fazil.com | Safety — The Mind | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) |

### Three Repositories

| Repository | Purpose | Link |
|------------|---------|------|
| **arifOS** | Constitutional governance + AAA MCP | [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) |
| **AGI_ASI_bot** | Dual-agent operational layer | [github.com/ariffazil/AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot) |
| **arif-fazil-sites** | Trinity static sites (HUMAN·THEORY·APPS) | [github.com/ariffazil/arif-fazil-sites](https://github.com/ariffazil/arif-fazil-sites) |

### Symbol Mapping

| Context | Δ (Delta) | Ω (Omega) | Ψ (Psi) |
|---------|-----------|-----------|---------|
| Trinity Sites | HUMAN/Body | APPS/Mind | THEORY/Soul |
| AGI_ASI_bot | AGI/Logic | ASI/Care | APEX/Sovereign |

**One constitution. Three perspectives.**

---

## 📚 Documentation

### Essential Reading

| Document | Purpose |
|----------|---------|
| [`000_THEORY.md`](000_THEORY.md) | Reverse Transformer architecture |
| [`AGENTS.md`](AGENTS.md) | Agent configuration |
| [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) | API documentation |
| [`docs/APPLICATIONS.md`](docs/APPLICATIONS.md) | Application guides |
| [`docs/ARCHITECTURE_AND_NAMING_v45.md`](docs/ARCHITECTURE_AND_NAMING_v45.md) | Architecture details |
| [`docs/COMPARISON.md`](docs/COMPARISON.md) | Framework comparisons |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute |

### For AI Agents

- [`AGENTS.md`](AGENTS.md) — Canonical instructions
- [`llms.txt`](llms.txt) — LLM context
- [`docs/AGI_BUILDER_BLUEPRINT.md`](docs/AGI_BUILDER_BLUEPRINT.md) — Blueprint
- [`docs/AAA_TRINITY_MAPPING.md`](docs/AAA_TRINITY_MAPPING.md) — Trinity mapping

---

## 📊 Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Constitutional vocabulary | ✅ Working | Injected into prompts |
| 13 Floors framework | ✅ Defined | F1-F13 documented |
| AAA MCP Server | ✅ Running | aaamcp.arif-fazil.com |
| Reverse Transformer theory | ✅ Complete | See 000_THEORY.md |
| Eureka Engine | 🔄 Partial | Runtime in AGI_ASI_bot |
| Runtime enforcement | ❌ Not yet | Full init_gate() pending |

---

## 🛡️ Core Principles

### DITEMPA BUKAN DIBERI
*Forged, Not Given*

We don't trust AI by default. We verify through constitutional constraints forged from:

- **6 Permanent Scars** — Miskin, Institutional, Invisibility, Anak Sulung, Professional, Father's Passing
- **9 Human Paradoxes** — Held, not resolved
- **13 Constitutional Floors** — Stationary constraints for non-stationary objectives

---

## ⚠️ Disclaimer

This is a **work-in-progress governance framework**, not a complete AGI safety system. Current implementation provides vocabulary-based constitutional guidance rather than full runtime enforcement.

**What's Working:**
- Constitutional vocabulary injection
- 13-floor conceptual framework
- Trinity architecture concepts
- AAA MCP Server
- Documentation and theoretical foundation

**What's Planned:**
- Runtime enforcement of constitutional floors
- Actual init_gate() and apex_verdict() integration
- Computed Ω₀ values instead of declared values
- Full 9 Atomic Actions runtime pipeline

---

*Version: v55.5-EIGEN*  
*Last Updated: 2026-02-05*  
*Ω₀ = 0.03 — Constitution holds.*
