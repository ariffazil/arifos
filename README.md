# arifOS — Constitutional AI Governance System

> **ΔΩΨ-governed constitutional kernel for AI agents.**
> 
> *Ditempa Bukan Diberi — Forged, Not Given* 💎🔥🧠🔱

[![arifOS](https://img.shields.io/badge/arifOS-v55.4--SEAL-0066cc?style=for-the-badge)](https://github.com/ariffazil/arifOS)
[![Status](https://img.shields.io/badge/status-WORK_IN_PROGRESS-yellow?style=for-the-badge)]()
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=for-the-badge)]()

---

## 📋 Table of Contents

- [What is arifOS?](#what-is-arifos)
- [Quick Start](#quick-start)
- [AAA MCP Server](#aaa-mcp-server)
- [Architecture](#architecture)
- [Theory](#theory)
- [Deployment](#deployment)
- [Trinity Ecosystem](#trinity-ecosystem)

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

### Tools Available

#### Constitutional Tools

| Tool | Floor | Description |
|------|-------|-------------|
| `init_gate` | F1-F13 | Initialize constitutional check |
| `apex_verdict` | F11/F13 | Sovereign judgment |
| `omega_track` | F7 | Uncertainty measurement |
| `drift_detect` | F7/F8 | Objective shift detection |

#### Trinity Tools

| Tool | Domain | Description |
|------|--------|-------------|
| `canonical_trinity` | ΔΩΨ | Core Trinity functions |
| `mcp_000_init` | F3 | Initialize with tri-witness |
| `seal_verdict` | F1 | Apply SEAL verdict |
| `void_action` | F1/F9 | Block violation |

### Example Usage

```python
import requests

# Check constitution
response = requests.post("http://localhost:8080/mcp", json={
    "tool": "init_gate",
    "params": {
        "action": "deploy_to_production",
        "context": "user_request"
    }
})

# Returns: {"verdict": "SEAL|SABAR|VOID", "omega": 0.03}
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

### Repository Structure

```
arifOS/
├── 000_THEORY.md           # Reverse Transformer theory
├── README.md               # This file
├── start_server.py         # MCP server entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image
├── railway.toml            # Railway deployment config
├── pyproject.toml          # Package config
│
├── mcp_server/             # MCP implementation
│   ├── tools/              # Constitutional tools
│   │   ├── canonical_trinity.py
│   │   ├── init_gate.py
│   │   └── apex_verdict.py
│   └── server.py           # Server logic
│
├── codebase/               # Core implementation
│   ├── init.py             # Initialization
│   └── floors/             # F1-F13 implementations
│
└── docs/                   # Documentation
    ├── INDEX.md
    └── architecture/
```

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

See **[000_THEORY.md](000_THEORY.md)** for full theory.

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

---

## 🌐 The Trinity Ecosystem

arifOS is part of a three-layer system:

| Layer | Symbol | Domain | Function | URL |
|-------|--------|--------|----------|-----|
| **HUMAN** | Δ | arif-fazil.com | Epistemic — The Body | [arif-fazil.com](https://arif-fazil.com) |
| **THEORY** | Ψ | apex.arif-fazil.com | Authority — The Soul | [apex.arif-fazil.com](https://apex.arif-fazil.com) |
| **APPS** | Ω | arifos.arif-fazil.com | Safety — The Mind | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) |

### Symbol Mapping

| Context | Δ (Delta) | Ω (Omega) | Ψ (Psi) |
|---------|-----------|-----------|---------|
| Trinity Sites | HUMAN/Body | APPS/Mind | THEORY/Soul |
| AGI_ASI_bot | AGI/Logic | ASI/Care | APEX/Sovereign |

**One constitution. Three perspectives.**

---

## 🔗 Related Projects

| Component | Repository | Purpose |
|-----------|------------|---------|
| **OpenClaw** (Base) | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | Agent framework foundation |
| **arifOS** (This) | [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) | Constitutional governance + AAA MCP |
| **AGI_ASI_bot** (Operational) | [github.com/ariffazil/AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot) | Dual-agent implementation |
| **arif-fazil-sites** (Frontend) | [github.com/ariffazil/arif-fazil-sites](https://github.com/ariffazil/arif-fazil-sites) | Trinity static sites |

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

## 📚 Documentation

- **[000_THEORY.md](000_THEORY.md)** — Reverse Transformer architecture
- **[docs/INDEX.md](docs/INDEX.md)** — Full documentation index
- **[AGI_ASI_bot/README.md](https://github.com/ariffazil/AGI_ASI_bot/blob/main/README.md)** — Operational deployment

---

## ⚠️ Disclaimer

This is a **work-in-progress governance framework**, not a complete AGI safety system. Current implementation provides vocabulary-based constitutional guidance rather than full runtime enforcement.

---

*Version: v55.4-SEAL*  
*Last Updated: 2026-02-05*  
*Ω₀ = 0.03 — Constitution holds.*
