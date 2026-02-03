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

## 🚀 Quick Start (5 Minutes)

### Option 1: Use the System Prompt (Copy-Paste)

Add arifOS governance to any LLM:

```bash
curl -s https://arif-fazil.com/llms.txt | head -100
```

Copy into your LLM's system prompt. [Full prompt →](333_APPS/L1_PROMPT/SYSTEM_PROMPT.md)

### Option 2: Run MCP Server (Production API)

```bash
pip install fastmcp
python -m arifos.mcp
# Server running on http://localhost:6274
```

**Test it:**
```bash
curl -X POST http://localhost:6274/mcp \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"init_gate","arguments":{"query":"Should I deploy?"}},"id":1}'
```

### Option 3: Clone & Develop (Full Stack)

```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e .
pytest tests/ -v
```

---

## 🏗️ Architecture

### The Trinity (AGI / ASI / APEX)

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

### The 13 Constitutional Floors

| Floor | Principle | Physics | Enforcement |
|-------|-----------|---------|-------------|
| F1 | Amanah | Landauer's Principle | Reversible operations |
| F2 | Truth | Fisher-Rao Metric | τ ≥ 0.99 |
| F3 | Tri-Witness | Quantum Measurement | W₃ ≥ 0.95 |
| F4 | Clarity | Shannon Entropy | ΔS ≤ 0 |
| F5 | Peace | Lyapunov Stability | Peace² ≥ 1.0 |
| F6 | Empathy | Heat Transfer | κᵣ ≥ 0.70 |
| F7 | Humility | Uncertainty Principle | Ω₀ ∈ [0.03, 0.05] |
| F8 | Genius | g-Factor | G ≥ 0.80 |
| F9 | Anti-Hantu | Dark Energy Contrast | Authenticity check |
| F10 | Ontology | Set Theory | Category verification |
| F11 | Authority | BLS Signatures | Command chain |
| F12 | Hardening | Error Correction | Injection defense |
| F13 | Sovereign | Circuit Breaker | Human veto |

[Full floors →](codebase/floors/canonical.py)

### The 9 MCP Tools

| Tool | Stage | Floors | Purpose |
|------|-------|--------|---------|
| `init_gate` | 000 | F11, F12 | Initialize constitutional session |
| `agi_sense` | 111 | F2, F4 | Intent classification |
| `agi_think` | 222 | F2, F4, F7 | Hypothesis generation |
| `agi_reason` | 333 | F2, F4, F7 | Deep reasoning |
| `asi_empathize` | 555 | F5, F6 | Stakeholder analysis |
| `asi_align` | 666 | F5, F6, F9 | Ethical alignment |
| `apex_verdict` | 888 | F3, F8 | Final judgment |
| `reality_search` | 777 | F2, F7 | Fact verification |
| `vault_seal` | 999 | F1, F3 | Immutable audit trail |

---

## 📦 Production Deployment

### MCP Server (L4 Tools)

**Live Endpoint:** `https://aaamcp.arif-fazil.com`

**Transports:**
- **MCP Protocol:** `/mcp` (SSE + JSON-RPC)
- **REST API:** `/api/v1/*` (POST + auth)
- **Simple HTTP:** `/simple/*` (GET + query params)

### Integration Guides

**Claude Desktop:**
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "arifos.mcp"],
      "transport": "sse"
    }
  }
}
```

**Cursor:**
Add to `.cursor/mcp.json` with same config.

**Direct API:**
```bash
curl -X POST https://aaamcp.arif-fazil.com/simple/init_gate \
  -d "q=Should I implement neural voting?"
```

---

## 🔬 Development Guide

### Project Structure

```
arifOS/
├── mcp/                    ← MCP Server (FastMCP)
│   ├── server.py           ← Entry point
│   ├── tools/              ← 9 canonical tools
│   └── constitutional_decorator.py
│
├── codebase/               ← Core Engines
│   ├── agi/                ← AGI Mind (Δ)
│   ├── asi/                ← ASI Heart (Ω)
│   ├── apex/               ← APEX Soul (Ψ)
│   ├── floors/             ← F1-F13 validators
│   └── vault/              ← VAULT-999 ledger
│
├── 333_APPS/               ← Application Layers
│   ├── L1_PROMPT/          ← System prompts
│   ├── L4_TOOLS/           ← MCP specs
│   └── L5_AGENTS/          ← Agent stubs (v56.0)
│
├── docs/                   ← Documentation
├── tests/                  ← Test suite
└── archive/                ← Compressed history
```

### Running Tests

```bash
pytest tests/day1_e2e_test.py -v
# 7/7 tests passing
```

### Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

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
