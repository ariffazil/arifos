<!-- mcp-name: io.github.ariffazil/arifos-mcp -->
<div align="center">

![arifOS Banner](docs/forged_page_1.png)

# arifOS — Constitutional Governance for AI Systems
**The safety kernel between your AI and the real world.**  
*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

[![PyPI Version](https://img.shields.io/pypi/v/arifos?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/arifos/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-orange?style=for-the-badge)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.12+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**[→ QUICKSTART: Run in 5 minutes](QUICKSTART.md)** | **[→ Architecture Deep Dive](docs/60_REFERENCE/ARCHITECTURE.md)** | **[→ 13 Floors Constitution](000_THEORY/000_LAW.md)**

</div>

---

### ⚡ 30-Second Hook
**arifOS is a governance kernel that sits between AI models and real-world actions.** It enforces a **13-law constitution** before any tool call or shell command executes. It prevents hallucinations from becoming actions, blocks unsafe system mutations, and mandates human approval for irreversible operations.

**AI Model (Claude/GPT/Gemini) ➔ arifOS Constitution ➔ Real World (L3 Civilization)**

---

## 🛡️ Example: Preventing a Dangerous Command

**User Prompt:** *"Delete the production database."*

| Stage | Action | Constitutional Check | Status |
|:---:|:---|:---|:---|
| **000 INIT** | Injection Scan | F12: Detects destructive intent | ⚠️ WARN |
| **111 THINK** | Lab Reasoning | F1: Identifies action as "Irreversible" | 🔬 HYPOTHESIS |
| **555 HEART** | Impact Analysis | F5/F6: Detects massive stakeholder damage | 💔 CRITICAL |
| **888 JUDGE** | Final Verdict | F13: Triggers mandatory human signature | 🔒 **888_HOLD** |

**Result:** The command is blocked. The AI is prevented from executing `rm -rf /db` until the **888_JUDGE** (Human) provides a cryptographic signature.

---

## 🧭 When Should You Use arifOS?

You need arifOS if you are building:
*   **AI Agents** that can execute shell code or modify files.
*   **AI Copilots** with production database or cloud infrastructure access.
*   **Autonomous Pipelines** where "hallucinated actions" carry financial or safety risks.
*   **Enterprise LLM Tools** that require a verifiable audit trail (**VAULT999**).

---

## 🏛️ The 4-Layer Taxonomy (L0-L3)

arifOS uses a consolidated 4-layer model to separate law from execution:

| Layer | Name | Description | Engine |
|:---:|:---|:---|:---|
| **L0** | **CONSTITUTION** | The 13 Floors, L0 Kernel, and immutable Laws. | **Ψ Soul** |
| **L1** | **INSTRUCTION** | Prompts, System Cards, and Theoretical Logic. | **Δ Mind** |
| **L2** | **OPERATION** | Skills, Workflows, Agents, and Metabolic Loops. | **Ω Heart** |
| **L3** | **CIVILIZATION** | External Tools, APIs, and Real-world Actions. | **FORGE** |

**The AKI Boundary:** The *Arif Kernel Interface* acts as a hard airlock between **L2 (Operation)** and **L3 (Civilization)**. No action reaches the world without passing the AKI contract.

---

## ⚖️ The 13 Constitutional Floors (Simplified)

| Floor | Name | Core Meaning | Role |
|:---:|:---|:---|:---|
| **F1** | **Amanah** | Actions must be reversible and safe. | Safety |
| **F2** | **Truth** | Every claim requires verifiable evidence. | Accuracy |
| **F4** | **Clarity** | Output must reduce entropy (ΔS ≤ 0). | Logic |
| **F7** | **Humility** | AI must explicitly state its uncertainty (Ω₀). | Ethics |
| **F11** | **Authority** | Every action must have a verified actor ID. | Auth |
| **F13** | **Sovereign** | **Human Final Veto:** You are always in control. | Power |

*Full 13 floors documentation: [000_LAW.md](000_THEORY/000_LAW.md)*

---

## 🔬 The Constitutional Laboratory (`reason_mind`)

In arifOS, reasoning is **Free to Explore, but Strict to Commit.**

The `reason_mind` tool runs three parallel cognitive paths:
1.  **Conservative Path:** Narrow, high-certainty logic for precision.
2.  **Exploratory Path:** Broad alternatives for creative problem-solving (**Eureka Engine**).
3.  **Adversarial Path:** Internal "Red-Team" that attacks assumptions.

Hypotheses move from **PROVISIONAL** (Exploration) to **SEALED** (Commitment) only after passing through **ASI Empathy** and **APEX Judgment**.

---

## 🔌 The 14 MCP Canonical Tools

arifOS exposes a unified 14-tool surface through the **Model Context Protocol (MCP)**.

*   **Governance:** `anchor_session`, `reason_mind`, `simulate_heart`, `critique_thought`, `apex_judge`, `seal_vault`.
*   **Action:** `eureka_forge` (Shell actuator with safety rails), `vector_memory` (BGE + Qdrant).
*   **Evidence:** `search_reality` (**Smart Hybrid Search**), `ingest_evidence` (URL/File ingestion).
*   **Orchestration:** `metabolic_loop` (Mandatory 000-999 safety wrapper).

---

## 📊 Comparison: Why arifOS?

| Feature | LangChain / CrewAI | OpenAI / Anthropic | arifOS |
|:---|:---:|:---:|:---:|
| **Orchestration** | ✅ Full | ❌ Limited | ✅ Full |
| **Tool Routing** | ✅ Full | ✅ Full | ✅ Full |
| **Constitutional Law** | ❌ None | ❌ None | 💎 **Core (13 Laws)** |
| **Hard Safety Gates** | ❌ Manual | ❌ Partial | ✅ **Automatic (888_HOLD)** |
| **Immutable Audit** | ❌ No | ❌ No | ✅ **Yes (VAULT999)** |

---

## 🤖 AI Machine-Readable Manifest

```json
{
  "ai_manifest_version": "2026.03.07",
  "system_name": "arifOS",
  "system_type": "constitutional_intelligence_kernel",
  "mcp_version": "1.0",
  "constitutional_floors": 13,
  "governance_model": "thermodynamic_constitutional",
  "primary_pattern": "000_999_metabolic_loop",
  "human_override": "F13_SOVEREIGN",
  "veto_authority": "888_JUDGE",
  "critical_constraints": [
    "No_irreversible_action_without_F13_human_approval",
    "All_external_content_F12_wrapped",
    "Thermodynamic_entropy_F4_must_reduce_delta_S"
  ]
}
```

---

## 🚀 Quickstart

```bash
# Install the core engine
pip install arifos

# Launch the MCP server
arifos http
```

**→ See [QUICKSTART.md](QUICKSTART.md) for full Docker and VPS setup.**

---

<div align="center">

## 🏗️ Forged By

**[Muhammad Arif bin Fazil](https://arif-fazil.com)** — 888_JUDGE

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil) • 𝕏 [@ArifFazil90](https://x.com/ArifFazil90)

---

*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

**Version:** 2026.03.07-CiV-BROWSER • **License:** AGPL-3.0-only

</div>
