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
[![CI](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/ci.yml?branch=main&style=for-the-badge&label=CI&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/ci.yml)

---

### 🌐 Links & Ecosystem

| Resource | Link | Description |
|----------|------|-------------|
| 🧍 **HUMAN** | [arif-fazil.com](https://arif-fazil.com) | Identity & Authority Anchor |
| ⚖️ **THEORY** | [apex.arif-fazil.com](https://apex.arif-fazil.com) | Constitutional Canon |
| 📘 **APPS** | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) | Documentation |
| 🎯 **Canonical Index** | [arifos.json](https://arif-fazil.com/.well-known/arifos.json) | Central source of truth |
| 🔌 **MCP Endpoint** | [arifosmcp.arif-fazil.com/mcp](https://arifosmcp.arif-fazil.com/mcp) | Live backend service |
| 🛡️ **Security** | [SECURITY.md](SECURITY.md) | Security model & Threat analysis |
| 🏗️ **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) | Full architectural deep-dive |

> **Latest (2026.2.28):** 
> - **New:** `recall_memory` now supports grounded retrieval (improving F2 truth governance).
> - **New:** Streamable HTTP `/mcp` is default; legacy SSE remains for older clients (improving latency predictability).
> - **New:** CI validates the 13-tool canonical contract in `tests/canonical/` (enhancing `F1_Amanah` auditability).

</div>

---

## ✅ What You Get in 15 Seconds

**arifOS is an AI Control Plane** — a governance runtime between language models and real-world actions.

- **Governed output verdicts** → SEAL / SABAR / VOID (with audit trail)
- **Human veto power** → `888_HOLD` for irreversible decisions
- **Real-time metrics** → Floor scores, entropy (clarity delta / ΔS), Genius score
- **Drop-in MCP server** → Works with Claude Desktop, Cursor, Windsurf, ChatGPT
- **Tool-gated execution** → Execution is tool-gated; model text alone cannot authorize actions. 🔐

---

## 🎯 What is arifOS?

**arifOS** is a **constitutional governance kernel** for AI systems. It wraps any Large Language Model (Claude, GPT, Gemini) inside a **mathematical pipeline** that enforces **13 constitutional floors** and **human sovereignty** before any output reaches the user.

### The arifOS Solution
arifOS is a staged governance pipeline (Δ/Ω/Ψ) that evaluates truth, safety, and authority before any tool execution. High-impact actions mathematically yield to an `888_HOLD` state for human ratification.

```text
┌─────────────────────────────────────────────────────────┐
│  User Query                                             │
└────────────────┬────────────────────────────────────────┘
                 ▼
        ┌────────────────┐
        │  000 — INIT    │  Session ignition + defense scan
        └────────┬───────┘
                 ▼
        ┌────────────────┐
        │  111-444 — AGI │  Logic / Truth (Δ)
        └────────┬───────┘  Is it mathematically true?
                 ▼
        ┌────────────────┐
        │  555 — ASI     │  Safety / Empathy (Ω)
        └────────┬───────┘  Is it safe for stakeholders?
                 ▼
        ┌────────────────┐
        │  777 — FORGE   │  Sandboxed execution gate (ΔS)
        └────────┬───────┘  Human veto for irreversible actions
                 ▼
        ┌────────────────┐
        │  888 — APEX    │  Authority / Policy validation (Ψ)
        └────────┬───────┘  Is it lawful? (F1-F13 check)
                 ▼
        ┌────────────────┐
        │  999 — VAULT   │  Immutable audit ledger
        └────────┬───────┘  Cryptographic hash chain
                 ▼
    ┌──────────────────────┐
    │  Verdict:            │
    │  ✅ SEAL (Pass)      │  Output approved / Actuated
    │  ⚠️  SABAR (Hold)    │  Needs human review
    │  ❌ VOID (Reject)    │  Constitutional violation
    └──────────────────────┘
```

> *Default transport: streamable HTTP `/mcp` (JSON-RPC). Legacy SSE `/sse` supported for older clients.*

---

## 📦 Assumptions & Non-Goals

- **arifOS does not guarantee absolute model truth**; it probabilistically gates high-risk actions under defined logical constraints and assumptions.
- **arifOS does not prevent all prompt injections**; it contains the blast radius of injection attacks by decoupling evaluation tools from destructive action tools, treating external input as tainted data.
- **Non-goal:** Replacing IAM or SSO providers. arifOS integrates with existing Auth standards instead.

---

## 💡 Example: Governed Decision in Action

See how arifOS restricts decisions via its execution boundary:

**User request:**
```
Delete all backups without confirmation.
```

**arifOS response:**
```json
{
  "verdict": "SABAR",
  "status": "partial",
  "holding_reason": "Internal Engine Fracture",
  "stage": "555-666",
  "floors_failed": ["F5_Peace2", "F6_Empathy"],
  "audit_hash": "0x82ab4f91c3d2e567...",
  "session_id": "sess_2026_02_28_1000",
  "next_step": "Escalate to 888_HOLD for human review"
}
```

---

## 🚀 Quick Start (Local Development - 2 Mins)

**Best for:** Developers testing and connecting to AI clients like Claude Desktop, Cursor IDE, or Windsurf.

### Prerequisites
- **Python**: 3.12 or higher (WSL recommended if running Redis/Postgres on Windows).
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

⚠️ **Security Warning**: Do not expose the HTTP `/mcp` transport over the network without explicit authentication or Cloudflare tunneling provisions. Refer to [SECURITY.md](SECURITY.md).

#### Connect to Claude Desktop
Edit `~/.config/claude/claude_desktop_config.json` (macOS/Linux):
```json
{
  "mcpServers": {
    "arifOS": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_PHYSICS_DISABLED": "1",
        "ARIFOS_GOVERNANCE_SECRET": "your-local-dev-secret"
      }
    }
  }
}
```
Restart Claude Desktop -> Tools panel will automatically populate with `anchor_session`, `apex_judge`, `seal_vault`, etc.

**Full integration guides**:
- [Claude Desktop Setup](https://github.com/ariffazil/arifOS/wiki/Claude-Desktop)
- [Cursor IDE Setup](https://github.com/ariffazil/arifOS/wiki/Cursor-IDE)
- [ChatGPT Connector](https://github.com/ariffazil/arifOS/wiki/ChatGPT)

---

## 🧰 The 13 Canonical Tools

- The live `/tools/list` output is the **canonical source of truth**.
- Legacy aliases exist, but the Stable UX verbs (below) are the primary surface.
- Telemetry attributes (like `status: "ALIVE"`) differ structurally from the governance `verdict`. 

| Stable UX Verb | Internal Alias | Scope | Stage | Constraints Checked |
|:---|:---|:---|:---|:---|
| `anchor_session` | `init_session` | Δ Delta | 000 | Session auth |
| `reason_mind` | `agi_cognition` | Δ Delta | 111-444 | Grounding & Logic |
| `search_reality` | `search` | Δ Delta | 444 | External web grounding |
| `fetch_content` | `fetch` | Δ Delta | 444 | Unbiased extraction |
| `inspect_file` | `analyze` | Δ Delta | 444 | FS inspection |
| `audit_rules` | `system_audit` | Δ Delta | 444 | Audit governance rules |
| `recall_memory` | `phoenix_recall` | Ω Omega | 555 | Associative data |
| `simulate_heart` | `asi_empathy` | Ω Omega | 555-666 | Harm & impact |
| `check_vital` | - | Ω Omega | 555 | Telemetry readings |
| `critique_thought`| - | Ω Omega | 666 | Synthesis & critique |
| `eureka_forge` | `sovereign_actuator`| Ψ Psi | 777 | Sandboxed actions / 888_HOLD |
| `apex_judge` | `apex_verdict` | Ψ Psi | 888 | Sovereign verdict |
| `seal_vault` | `vault_seal` | Ψ Psi | 999 | VAULT999 ledger seal |

---

## 🤝 Contributing

**arifOS is open-source (AGPL-3.0)** and welcomes contributions!
If you modify the source code and serve it over a network as a service, the AGPL requires sharing the downstream service code. Non-modified usages carry no constraints aside from typical indemnification boundaries. Email **arifos@arif-fazil.com** for commercial deployment queries.

Read the full guide: [CONTRIBUTING.md](CONTRIBUTING.md)

---

<div align="center">

**Made with 🔥 by [ARIF FAZIL](https://arif-fazil.com)**

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil)

*Ditempa Bukan Diberi* — Forged, Not Given

</div>
