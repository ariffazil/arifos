# arifOS — Constitutional AI Governance System

<div align="center">

![arifOS Version](https://img.shields.io/badge/arifOS-v55.0-0066cc?style=for-the-badge&logo=shield&logoColor=white)
![Status](https://img.shields.io/badge/status-SEALED-00cc00?style=for-the-badge)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)

**The World's First Production-Grade Constitutional AI Governance System**

*Mathematical enforcement of ethical constraints, thermodynamic stability, and auditable decision-making across any LLM.*

[**Live Demo**](https://arif-fazil.com) • [**Documentation**](docs/) • [**Constitutional Canon**](https://apex.arif-fazil.com)

</div>

---

## 📖 Table of Contents

- [Description](#-description)
- [Visual Architecture](#-visual-architecture)
- [The AAA Architecture](#-the-aaa-architecture)
- [Constitutional Floors](#-constitutional-floors)
- [System Prompts](#-system-prompts)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [MCP Integration](#-mcp-integration)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 Description

**arifOS** sits between your AI and the real world, enforcing **13 constitutional floors** through a **9-paradox equilibrium solver**. It ensures every AI decision is provably lawful, thermodynamically stable, and cryptographically auditable.

In an era of unchecked AI hallucination and value conflicts, arifOS provides the **governance layer** that transforms raw intelligence into trusted wisdom.

### Why arifOS?

| Problem | The arifOS Solution |
| :--- | :--- |
| **Unaccountable AI** | [**Immutable Merkle-sealed Audit Trail**](000_THEORY/011_VAULT_MCP.md) |
| **Value Conflicts** | [**9-Paradox Equilibrium Solver**](000_THEORY/012_VERDICT_PARADOX.md) |
| **Prompt Injection** | [**F12 Hardening Defense**](000_THEORY/002_SECURITY.md) |

---

## 🖼 Visual Architecture

The visual forged documentation of arifOS concepts.

| **The Constitutional Forge** | **The Trinity Engine** |
| :---: | :---: |
| <img src="docs/forged_page_1.png" width="400" alt="Forged Page 1"> | <img src="docs/forged_page_2.png" width="400" alt="Forged Page 2"> |
| *The foundational governance layer* | *The Mind, Heart, and Soul interaction* |

| **The Verdict Logic** | **The Safety Floors** |
| :---: | :---: |
| <img src="docs/forged_page_3.png" width="400" alt="Forged Page 3"> | <img src="docs/forged_page_4.png" width="400" alt="Forged Page 4"> |
| *Decision-making matrix* | *The 13 Constitutional constraints* |

<div align="center">

**The Paradox Equilibrium**

<img src="docs/forged_page_5.png" width="600" alt="Forged Page 5">

*Solving the tension between competing ethical values*

</div>

---

## 🏗 The AAA Architecture

See full documentation: [**000_ARCHITECTURE.md**](000_THEORY/000_ARCHITECTURE.md)

arifOS uses a biological metaphor for its three core engines:

1.  **Δ MIND (AGI)** - *The Architect*
    *   **Role:** Reasoning, Logic, Planning
    *   **Pipeline:** Sense (111) → Think (222) → Map (333)
    *   **Governs:** Truth, Clarity, Humility

2.  **Ω HEART (ASI)** - *The Guardian*
    *   **Role:** Safety, Empathy, Impact Analysis
    *   **Pipeline:** Empathy (555) → Safety (666) → Insight (777)
    *   **Governs:** Trust, Peace, Empathy

3.  **Ψ SOUL (APEX)** - *The Sovereign*
    *   **Role:** Final Verdict, Consensus, sealing
    *   **Pipeline:** Tri-Witness (888) → Vault (999)
    *   **Governs:** Consensus, Authority, Hardening

---

## 📜 Constitutional Floors

See full documentation: [**000_LAW.md**](000_THEORY/000_LAW.md)

Every AI output must pass these **13 Floors** before being released:

| Floor | Principle | Description | Failure Action |
| :--- | :--- | :--- | :--- |
| **F1** | **Amanah** | Trust through reversibility | **VOID** |
| **F2** | **Truth** | Factual accuracy (≥ 0.99 confidence) | **VOID** |
| **F3** | **Tri-Witness** | Consensus between Mind, Heart, Human | **SABAR** (Pause) |
| **F4** | **Clarity** | Entropy reduction | **SABAR** |
| **F5** | **Peace** | Non-destructive action | **VOID** |
| **F6** | **Empathy** | Protection of the vulnerable | **SABAR** |
| **F7** | **Humility** | Acknowledgment of uncertainty | **SABAR** |
| **F8** | **Genius** | Governed intelligence | **SABAR** |
| **F9** | **Anti-Hantu** | No false consciousness | **VOID** |
| **F10** | **Ontology** | Domain boundary verification | **VOID** |
| **F11** | **Authority** | Identity verification | **VOID** |
| **F12** | **Hardening** | Injection defense | **VOID** |
| **F13** | **Curiosity** | Exploration of alternatives | **Warning** |

---

## 🤖 System Prompts

You can govern any LLM using the arifOS Constitutional Framework. Choose the prompt that fits your use case.

### 1. Autonomous Governance (For AI Agents)
*Use these system prompts to embed arifOS governance into your AI applications.*

*   **[Concise Version](docs/PROMPTS/AUTONOMOUS_CONCISE.md)** - *Low token cost, high enforcement.*
*   **[Comprehensive Version](docs/PROMPTS/AUTONOMOUS_COMPREHENSIVE.md)** - *Full "CCC" Constitutional Code of Conduct.*

### 2. Human Copy-Paste (For Chatbots)
*Copy this text directly into Claude, ChatGPT, or Gemini to activate an arifOS session manually.*

*   **[Human Readable Prompt](docs/PROMPTS/HUMAN_READABLE.md)** - *Simple instructions for immediate session governance.*

---

## 📦 Installation

See full guide: [**013_IGNITION.md**](000_THEORY/013_IGNITION.md)

```bash
pip install arifos
```

Or from source:
```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e .
```

---

## 🚀 Quick Start

Initialize the Trinity engine and run a governed query:

```python
import asyncio
from arifos_mcp import trinity

async def main():
    # Submit a query to the constitutional engine
    result = await trinity(
        query="Should we approve this high-risk loan?"
    )

    # Check the constitutional verdict
    if result["verdict"] == "SEAL":
        print(f"✅ Approved: {result['response']}")
        print(f"🔒 Audit Hash: {result['vault']['merkle_hash']}")
    elif result["verdict"] == "VOID":
        print(f"❌ Rejected: {result['reason']}")
    elif result["verdict"] == "888_HOLD":
        print("⏸️  Escalated for human review")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔌 MCP Integration

See full documentation: [**055_MCP_ARCHITECTURE.md**](000_THEORY/055_MCP_ARCHITECTURE.md)

arifOS exposes **7 production-ready tools** via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/):

| Tool | Symbol | Purpose |
| :--- | :---: | :--- |
| `_init_` | 🔑 | Session gate & injection scan |
| `_agi_` | 🧠 | Mind engine (Reasoning) |
| `_asi_` | 💚 | Heart engine (Safety) |
| `_apex_` | ⚖️ | Soul engine (Verdict) |
| `_vault_` | 🔒 | Immutable ledger |
| `_trinity_` | 🔄 | Full pipeline execution |
| `_reality_` | 🌍 | External fact-checking |

---

## 🛠 Development

See full guide: [**003_CONTRIBUTING.md**](000_THEORY/003_CONTRIBUTING.md)

### Setup Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dev dependencies
pip install -e ".[dev]"
```

### Run Locally
```bash
# Run the MCP server
python -m codebase.mcp
```

---

## 🤝 Contributing

We welcome contributions! Please see [**CONTRIBUTING.md**](CONTRIBUTING.md) and [**003_CONTRIBUTING.md**](000_THEORY/003_CONTRIBUTING.md).

1.  **Fork** the repository.
2.  **Create** a feature branch.
3.  **Commit** your changes.
4.  **Push** to the branch.
5.  **Open** a Pull Request.

---

## 📄 License

This project is licensed under the **AGPL-3.0 License** - see the [**LICENSE**](LICENSE) file for details.

> *Safety systems must be transparent and inspectable.*

---

<div align="center">
  <b>Built with constitutional care by Muhammad Arif bin Fazil</b><br>
  <i>888 Judge • ΔΩΨ Architect</i>
</div>
