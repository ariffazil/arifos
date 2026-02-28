<!-- mcp-name: io.github.ariffazil/arifos-mcp -->
<div align="center">

![arifOS Banner](docs/forged_page_1.png)

# arifOS — Constitutional Intelligence Kernel

**The system that knows because it admits what it cannot know.**  
*Ditempa Bukan Diberi* — Forged, Not Given

[![Version](https://img.shields.io/badge/version-2026.2.28-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/ariffazil/arifOS/releases)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange?style=for-the-badge)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.12+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arifosmcp-truth-claim.pages.dev)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)

</div>

---

## 🧭 What is arifOS?

**arifOS is a Constitutional Intelligence Kernel and AI Control Plane.** It sits locally or hosted in the cloud between language models (like Claude, GPT, Gemini) and real-world actions. 

By running an AI through its rigorous 000-999 mathematical "metabolic loop", it acts as a **lie detector and safety firewall**. It forces every interaction, code execution, or response to adhere to **13 strict constitutional rules (Floors)** before it hits the internet or ends up on your screen.

---

## ⚖️ Why does it exist?

Unconstrained AI models calculate statistical probability, not truth. Left unchecked, they will hallucinate facts, write dangerous code, and act without considering human consequences. **arifOS solves this.**

Code is execution. Governance is survival. arifOS ensures that:
- **Truth is grounded (F2 Truth):** The AI must physically back its claims with verifiable evidence, or explicitly admit `UNKNOWN`.
- **Entropy is reduced (F4 Clarity):** Outputs must reduce confusion, not add noise.
- **Destruction is prevented (F1 Amanah & F13 Sovereignty):** Irreversible actions are blocked and require cryptographically signed human ratification (`888_HOLD`).

---

## 🧠 The 8-Layer Architecture (`333_APPS`)

arifOS is not just a prompt; it is an entire **Intelligence Stack (Level 0 to Level 7)**. Swapping an AI model never bypasses the core governance kernel.

| Level | Name | Scope | Role in arifOS |
|:---:|:---|:---|:---|
| **L7** | **AGI / Ecosystem** | Civilisation-Scale | Permissionless sovereignty and recursive self-healing research. |
| **L6** | **Institution** | Organisational | Trinity consensus frameworks and organizational governance (Stubs/Pilots). |
| **L5** | **Agents** | Federation | Multi-agent coordination (the Hypervisor managing diverse AI actors). |
| **L4** | **Tools (MCP)** | Production | The Model Context Protocol (MCP) surface. 13 canonical tools bridging the AI to the Kernel. |
| **L3** | **Workflow** | Production | The `000 -> 999` stage constitutional metabolic sequences (Ignition to Commit). |
| **L2** | **Skills** | Production | Sensory systems (A-CLIP primitives) measuring environment, health, and network telemetry. |
| **L1** | **Prompts** | Production | The zero-context user entry layer where intents are caught and parsed. |
| **L0** | **KERNEL** | **SEALED** | **The Immutable Core.** 3 Engines (Mind, Heart, Soul), 13 Floors, and `VAULT999` ledger. No transport logic exists here. |

---

## 🚀 How do I run it in 2 minutes?

**arifOS exposes a 13-tool Model Context Protocol (MCP) server.** You can connect it directly to your favorite MCP-compatible AI clients (Claude Desktop, Cursor, ChatGPT).

### Prerequisites
- **Python**: 3.12+ 
- **Environment**: Linux, macOS, or Windows WSL.

```bash
# 1. Install arifOS
pip install arifos

# 2. Export required safety environment variables (Use a .env file for production!)
export ARIFOS_GOVERNANCE_SECRET=$(openssl rand -hex 32)
export DB_PASSWORD="your-strong-secret-here"
export DATABASE_URL="postgresql://arifos:${DB_PASSWORD}@localhost:5432/vault999"

# 3. Start local MCP server for desktop IDE clients (stdio mode)
python -m arifos_aaa_mcp stdio
```

*For production Cloud/VPS deployment with Streamable HTTP, see [`DEPLOYMENT.md`](DEPLOYMENT.md).*

⚠️ **Warning:** Do not expose the HTTP `/mcp` transport over the open network without explicit auth. See [`SECURITY.md`](SECURITY.md).

#### Hooking it up to Claude Desktop
Simply add this to your `~/.config/claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "arifOS_AAA": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_GOVERNANCE_SECRET": "your-local-dev-secret",
        "DATABASE_URL": "postgresql://arifos:dev@localhost:5432/vault999"
      }
    }
  }
}
```

---

## 🔍 How do I verify and trust it?

You don't have to blindly trust arifOS; you can verify its work. Every decision made by the AI is cryptographically sealed in an immutable ledger (**VAULT999**) with a Merkle hash chain.

When a query is processed, arifOS provides a structured verdict envelope:
- ✅ **SEAL**: Passed all 13 constitutional floors. The action is authorized and logged.
- 🟡 **PARTIAL**: Approved with warnings.
- ⚠️ **SABAR**: Refine and retry. Entropy or risk was too high; the AI was hallucinating or unsafe. *(Sabar = Patience)*
- ❌ **VOID**: Blocked. A hard rule (Truth or Security) was violated.
- 🛑 **888_HOLD**: Irreversible action requested. The system stops and waits for human sovereign cryptographic ratification.

**See it in action:** Check out the **[Live Constitutional Audit Dashboard](https://arifosmcp-truth-claim.pages.dev)** to see real-time integrity sweeps of the framework.

---

## 📚 Where do I go next?

To dig deeper into the mechanics, deployment, and security of arifOS, refer to our specialized documentation sites.

- **[arifOS Documentation Site](https://arifos.arif-fazil.com/)**
- **[Constitutional Audit Dashboard](https://arifosmcp-truth-claim.pages.dev/)**
- **[Live Status Page](https://arifosmcp.arif-fazil.com/health)**

| Domain | Guide | What's Inside |
|---|---|---|
| 🏗️ **Design** | [`ARCHITECTURE.md`](ARCHITECTURE.md) | Trinity Logic (ΔΩΨ), 7-Organ Stack, and EMD Physics |
| 🛡️ **Defense** | [`SECURITY.md`](SECURITY.md) | Injection handling, Auth models, and Threat vectors |
| ⚖️ **Law** | [`000_THEORY/000_LAW.md`](000_THEORY/000_LAW.md) | The 13 Constitutional Floors and Genius Engine |
| 🚀 **Deploy** | [`DEPLOYMENT.md`](DEPLOYMENT.md) | VPS setups, Docker, and Cloudflare scaling |
| 🧰 **Tools** | [`MCP_TOOLS.md`](MCP_TOOLS.md) | The 13 canonical tools exposed to the LLM |

---

## 🤝 Contributing & License
We welcome contributions! Have ideas on improving AI empathy scoring using Machine Learning? Find a bug in the injection defenses? Fork, code, and submit a PR. See `CONTRIBUTING.md` for guidelines.

- **License:** AGPL-3.0 (Free to use, modify, and distribute, but modifications must be shared under the same license).

---

<div align="center">

**Made with 🔥 by [ARIF FAZIL](https://arif-fazil.com)**

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil) • 𝕏 [@ArifFazil90](https://x.com/ArifFazil90)

*Ditempa Bukan Diberi* — Forged, Not Given

</div>
