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
- [Key Features](#-key-features)
- [The AAA Architecture](#-the-aaa-architecture)
- [Constitutional Floors](#-constitutional-floors)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [MCP Integration](#-mcp-integration)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 💡 Description

**arifOS** sits between your AI and the real world, enforcing **13 constitutional floors** through a **9-paradox equilibrium solver**. It ensures every AI decision is provably lawful, thermodynamically stable, and cryptographically auditable.

In an era of unchecked AI hallucination and value conflicts, arifOS provides the **governance layer** that transforms raw intelligence into trusted wisdom.

### Why arifOS?

| Problem | The arifOS Solution |
| :--- | :--- |
| **Unaccountable AI** | 100% immutable Merkle-sealed audit trail (VAULT-999) |
| **Value Conflicts** | Nash equilibrium solver for 9 fundamental ethical paradoxes |
| **Prompt Injection** | F12 Hardening with a 92% injection block rate |

---

## ✨ Key Features

- **Tri-Layer Governance**: The **AAA Framework** splits decision-making into Mind (Logic), Heart (Safety), and Soul (Verdict).
- **13 Enforceable Floors**: Hard constraints on Truth, Safety, Empathy, and Reality that cannot be bypassed.
- **Paradox Resolution**: Mathematically solves conflicts between competing values (e.g., Truth vs. Kindness).
- **Immutable Auditing**: Every decision is cryptographically sealed in **VAULT-999**.
- **Model Agnostic**: Works with Claude, GPT, Gemini, Llama, and more.
- **MCP Native**: Fully compatible with the **Model Context Protocol** for seamless tool integration.

---

## 🏗 The AAA Architecture

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

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- `pip`

### Install from PyPI
```bash
pip install arifos
```

### Install from Source
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

### Claude Desktop Configuration
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "codebase.mcp"],
      "env": {
        "PYTHONPATH": "/path/to/arifOS"
      }
    }
  }
}
```

---

## 🛠 Development

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

## 🧪 Testing

We maintain a high standard of reliability with >90% test coverage.

```bash
# Run full test suite
pytest tests/ -v

# Run only constitutional floor tests
pytest tests/test_hardened_v53.py

# Run equilibrium solver tests
pytest tests/test_nine_paradox.py
```

---

## 🤝 Contributing

We welcome contributions that align with our constitutional values!

1.  **Fork** the repository.
2.  **Create** a feature branch (`git checkout -b feature/amazing-feature`).
3.  **Commit** your changes (`git commit -m 'Add amazing feature'`).
4.  **Push** to the branch (`git push origin feature/amazing-feature`).
5.  **Open** a Pull Request.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

---

## 📄 License

This project is licensed under the **AGPL-3.0 License** - see the [LICENSE](LICENSE) file for details.

> *Safety systems must be transparent and inspectable.*

---

## 👏 Acknowledgments

**Theoretical Foundations:**
*   **Isaac Asimov** (Three Laws of Robotics)
*   **John Rawls** (Theory of Justice)
*   **Claude Shannon** (Information Theory)
*   **Rudolf Kalman** (Kalman Filter)
*   **John Nash** (Game Theory)

**Motto:** *"Ditempa Bukan Diberi"* — Forged, Not Given.

---

<div align="center">
  <b>Built with constitutional care by Muhammad Arif bin Fazil</b><br>
  <i>888 Judge • ΔΩΨ Architect</i>
</div>