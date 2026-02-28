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
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://674a01a3.arifosmcp-truth-claim.pages.dev)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)

</div>

---

## 🧭 What is arifOS?

**arifOS is an AI Control Plane.** It sits between language models (like Claude, GPT, Gemini) and real-world actions, acting as a **constitutional governance kernel**. 

It wraps models inside a mathematical pipeline that enforces **13 constitutional floors** (safety, truth, authority) and **human sovereignty** before any output reaches the user or executes a tool.

## ⚖️ Why does it exist?

Unconstrained AI acts on statistical probability, not structural truth, often leading to hallucinated assertions or reckless tool execution. arifOS exists to force AI cognition through a rigorous verification pipeline. 

It ensures that:
- **Truth is grounded** (F2)
- **Entropy is reduced** (F4) 
- **Destructive actions are prevented** without human sovereign ratification (888_HOLD).

*Code is execution. Governance is survival.*

---

## 🚀 How do I run it in 2 minutes?

**arifOS exposes a 13-tool Model Context Protocol (MCP) server.** You can connect it directly to your favorite MCP-compatible AI clients (Claude Desktop, Cursor, Windsurf).

### Prerequisites
- **Python**: 3.12 or higher.
- **Environment**: Linux, macOS, or Windows WSL.

```bash
# 1. Install arifOS
pip install arifos

# 2. Export required safety environment variables
export ARIFOS_GOVERNANCE_SECRET=$(openssl rand -hex 32)
export DB_PASSWORD="your-strong-secret-here"
export DATABASE_URL="postgresql://arifos:${DB_PASSWORD}@localhost:5432/vault999"

# 3. Start local MCP server for desktop IDE clients (stdio mode)
python -m arifos_aaa_mcp stdio
```

⚠️ **Warning:** Do not expose the HTTP `/mcp` transport over the open network without explicit auth. See [SECURITY.md](SECURITY.md).

#### Hooking it up to Claude Desktop
Add this to your `~/.config/claude/claude_desktop_config.json`:
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

## 🔍 How do I trust/verify it?

You don't have to trust it; you can verify it. 

Every decision made by arifOS is cryptographically sealed in an immutable ledger (**VAULT999**) with a Merkle hash chain.
- Want to verify the system's alignment? Check the **Live Dashboard**: [Live Test Truth Claim](https://674a01a3.arifosmcp-truth-claim.pages.dev)
- Check the real-time GitHub Actions tests.

When a query is processed, arifOS provides a structured verdict envelope:
- ✅ **SEAL**: Passed all 13 constitutional floors.
- ⚠️ **SABAR**: Held for reform. Entropy or risk was too high.
- ❌ **VOID**: Blocked. Factual fidelity (F2) or Injection (F12) failed.
- 🛑 **888_HOLD**: Irreversible action requested. Waiting for human sovereign cryptographic ratification.

---

## 📚 Where do I go next?

To dig deeper into the mechanics, deployment, and security of arifOS, refer to our specialized documentation:

| Domain | Guide | What's Inside |
|---|---|---|
| 🏗️ **Design** | [ARCHITECTURE.md](ARCHITECTURE.md) | Trinty Logic (ΔΩΨ), 7-Organ Stack, and EMD Physics |
| 🛡️ **Defense** | [SECURITY.md](SECURITY.md) | Injection handling, Auth models, and Threat vectors |
| ⚖️ **Law** | [GOVERNANCE.md](000_THEORY/000_LAW.md) | The 13 Constitutional Floors and Genius Engine |
| 🚀 **Deploy** | [DEPLOYMENT.md](DEPLOYMENT.md) | VPS setups, Docker, and Cloudflare scaling |
| 🧰 **Tools** | [MCP_TOOLS.md](MCP_TOOLS.md) | The 13 canonical tools exposed to the LLM |

---

<div align="center">

**Made with 🔥 by [ARIF FAZIL](https://arif-fazil.com)**

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil)

*Ditempa Bukan Diberi* — Forged, Not Given

</div>
