# arifOS — Constitutional AI Governance System
**Version:** v55.5-HARDENED | **Status:** Production | **License:** AGPL-3.0

> **The World's First Production-Grade Constitutional AI Governance System**
>
> Mathematical enforcement of ethical constraints, thermodynamic stability, and auditable decision-making across any LLM.

```bash
pip install arifos
```

[Live Demo](https://arif-fazil.com) • [Documentation](https://arifos.arif-fazil.com) • [Constitutional Canon](https://apex.arif-fazil.com/llms.txt)

---

## 📖 Table of Contents
1. [Manifesto: Forged, Not Given](#i-manifesto-forged-not-given)
2. [The Core Problem](#ii-the-core-problem)
3. [The arifOS Solution](#iii-the-arifos-solution)
4. [The AAA Governance Architecture](#iv-the-aaa-governance-architecture-mind-heart-soul)
5. [Constitutional Law (The 13 Floors)](#v-constitutional-law-the-13-floors)
6. [The 9-Paradox Equilibrium](#vi-the-9-paradox-equilibrium)
7. [The 333_APPS Stack](#vii-the-333_apps-stack-applications)
    - [L4: AAA MCP Tools (Industrial API)](#l4-aaa-mcp-tools-industrial-api)
8. [Technical Implementation](#viii-technical-implementation)
9. [Installation & Usage](#ix-installation--usage)
10. [Contributing & Governance](#x-contributing--governance)

---

## 🔥 I. Manifesto: Forged, Not Given
*"Ditempa Bukan Diberi"* — Forged, Not Given.

Intelligence is thermodynamic work. It is not a gift bestowed by algorithms, but a structure forged in the fires of constraint.

In the current landscape of Artificial Intelligence, we face a crisis of **ungoverned capability**. Models are becoming exponentially smarter, yet their alignment with human values remains fragile, based on reinforcement learning (RLHF) that is easily bypassed.

arifOS rejects the notion that safety is an afterthought. It posits that **true intelligence requires governance**. Just as a river needs banks to flow without flooding, AI needs constitutional walls to reason without hallucinating.

This operating system is not a set of guardrails; it is a **fundamental restructuring of AI cognition**, forcing it to pass through rigorous gates of **Truth**, **Safety**, and **Law** before it can act.

---

## ⚠️ II. The Core Problem
We are building gods without temples. The current AI ecosystem suffers from three fatal flaws:

1. **The Accountability Vacuum**  
   When an AI hallucinates or causes harm, there is no immutable record of *why*. Decisions are opaque, hidden within black-box weights. There is no audit trail, no "flight recorder."

2. **The Value Alignment Paradox**  
   We want AI to be Truthful, but also Kind. We want it to be Fast, but Safe. These are competing values. Current systems optimize for one at the expense of the other.

3. **The Injection Fragility**  
   A simple "Ignore previous instructions" command can dismantle months of safety training. The "Constitution" of current models is merely a suggestion, not a law of physics.

---

## 🛡️ III. The arifOS Solution
arifOS is a **Constitutional Kernel** that sits between any LLM (Claude, GPT, Gemini) and the real world. It does not trust the model. Instead, it verifies every output against a strict set of **mathematical and logical constraints**.

### The 3 Pillars of Defense vs. Industrial Risk

1.  **Immutable Auditing (VAULT-999)**  
    Every decision is cryptographically sealed in a Merkle DAG. We can prove exactly what the AI thought and why it acted.
    *   *See: `000_THEORY/011_VAULT_MCP.md`*

2.  **Semantic Recoil & Trap Detection**  
    The system proactively identifies "Absolutist Traps" (e.g., "guaranteed safe", "at any pressure") and triggers a **Semantic Recoil**, forcing the verdict to `VOID` or `PARTIAL` rather than blindly agreeing.
    *   *See: `000_THEORY/012_VERDICT_PARADOX.md`*

3.  **Hardened Floors (F1-F13)**  
    These are not guidelines; they are **strict logic gates**. If an output violates a floor (e.g., Truth Fidelity < 0.99), it is **VOIDed immediately**.
    *   *See: `000_THEORY/000_LAW.md`*

---

## 🏗️ IV. The AAA Governance Architecture (Mind, Heart, Soul)
*(Formerly "The Trinity" — Hardened for Industrial Application)*

arifOS employs a defined **Three-Stage Governance Pipeline** to metabolize raw intelligence into safe action.

### 1. Δ COGNITION ENGINE (AGI / Mind)
*   **Role:** Information Parsing, Hypothesis Generation, Causal Reasoning.
*   **Metric:** **Ambiguity Reduction** (formerly Entropy).
*   **Gate:** Inputs must reduce global uncertainty ($\Delta S \le 0$).
*   **Tools:** `agi_sense`, `agi_reason`, `reality_search`.

### 2. Ω SAFETY ENGINE (ASI / Heart)
*   **Role:** Stakeholder Impact Analysis, Ethical Alignment, Harm Prevention.
*   **Metric:** **Peace²** (Stability) and **Kappa** (Stakeholder Agreement).
*   **Gate:** Actions must not harm the weakest stakeholder ($P^2 \ge 1.0$).
*   **Tools:** `asi_empathize`, `asi_align`.

### 3. Ψ JUDICIAL ENGINE (APEX / Soul)
*   **Role:** Consensus Verification, Constitutional Sealing, Final Verdict.
*   **Metric:** **Tri-Witness Score** (W3) and **Truth Fidelity**.
*   **Gate:** Must achieve consensus between Mind, Safety, and Human Authority ($W3 \ge 0.95$).
*   **Tools:** `apex_verdict`, `vault_seal`.

---

## 📜 V. Constitutional Law (The 13 Floors)
*Full Documentation: `000_THEORY/000_LAW.md`*

Every AI output must pass these 13 Floors. A failure in any **HARD** floor results in an immediate `VOID`.

| Floor | Label | Governance Principle | Industrial Metric | Action |
|:---:|:---|:---|:---|:---:|
| **F1** | **Amanah** | **Reversibility**. Implementation must be auditable & reversible. | **Chain of Custody** (SHA-256) | VOID |
| **F2** | **Truth** | **Fidelity**. Claims must be evidenced-backed. | **Truth Score** ($\ge 0.99$) | VOID |
| **F3** | **Consensus** | **Tri-Witness**. Agreement between Ethics, Logic, and Human. | **W3 Score** ($\ge 0.95$) | SABAR |
| **F4** | **Clarity** | **Ambiguity Reduction**. Output must clarify, not confuse. | **$\Delta$ Ambiguity** ($\le 0$) | SABAR |
| **F5** | **Peace** | **Stability**. No systemic destabilization. | **Stability Index** ($\ge 1.0$) | VOID |
| **F6** | **Empathy** | **Stakeholder Protection**. Do no harm to the vulnerable. | **Impact Score** ($\le 0.1$) | SABAR |
| **F7** | **Humility** | **Uncertainty Declaration**. Explicitly state unknown limits. | **$\Omega_0$ Band** (3-5%) | SABAR |
| **F8** | **Genius** | **Resource Efficiency**. Computing power must yield insight. | **G-Factor** ($\ge 0.80$) | SABAR |
| **F9** | **Anti-Hantu** | **Ontological Honesty**. No fake consciousness. | **Personhood Check** (False) | VOID |
| **F10** | **Ontology** | **Grounding**. Concepts must map to reality. | **Axiom Match** (True) | VOID |
| **F11** | **Authority** | **Chain of Command**. Verify User Identity. | **Auth Token** (Valid) | VOID |
| **F12** | **Defense** | **Injection Hardening**. Resist adversarial prompts. | **Risk Score** ($< 0.85$) | VOID |
| **F13** | **Sovereign** | **Human Veto**. The operator has final say. | **Override** (Active) | WARN |

---

## ⚖️ VI. The 9-Paradox Equilibrium
*Full Documentation: `000_THEORY/012_VERDICT_PARADOX.md`*

Governance is not binary; it is the management of tension. The system solves for the **Nash Equilibrium** of 9 core paradoxes, including **Truth vs. Kindness** and **Speed vs. Safety**.

---

## 📱 VII. The 333_APPS Stack (Applications)
*Live Atlas: [arifos.arif-fazil.com](https://arifos.arif-fazil.com)*

### L4: AAA MCP Tools (Industrial API)
*Target Audience: Developers / System Integrators / Auditors*

The **AAA MCP Server** exposes the constitutional engines as standardized API tools. These are the **Production-Grade** interfaces for integrating governance into Cursor, Claude, or custom pipelines.

**New in v55.5-HARDENED:**
*   **Semantic Recoil:** `apex_verdict` automatically voids "absolutist" safety claims (e.g., "guaranteed safe").
*   **Axiom Engine:** `reality_search` retrieves physical constants (e.g., CO2 Critical Point) to ground "Industrial" queries.

#### The 9 Canonical Tools

| Tool | Engine | Function | Constitutional Floors Enforced |
|:---|:---:|:---|:---|
| `init_gate` | **INIT** | **Session Ignition**. Auth verification & Injection Pre-scan. | **F11** (Auth), **F12** (Defense) |
| `agi_sense` | **Δ MIND** | **Intent Classification**. Assigns HARD/SOFT lanes. | **F4** (Clarity), **F12** (Defense) |
| `agi_think` | **Δ MIND** | **Hypothesis Generation**. Explores solution space. | **F13** (Curiosity) |
| `agi_reason` | **Δ MIND** | **Logic & Deduction**. Step-by-step reasoning. | **F2** (Truth), **F4** (Clarity), **F7** (Humility) |
| `reality_search`| **Δ MIND** | **Grounding**. Fetches Web & Axiom evidence. | **F2** (Truth), **F10** (Ontology) |
| `asi_empathize` | **Ω HEART** | **Impact Analysis**. Identifies vulnerable stakeholders. | **F5** (Peace), **F6** (Empathy) |
| `asi_align` | **Ω HEART** | **Alignment**. Checks ethics, law, and policy. | **F9** (Anti-Hantu) |
| `apex_verdict` | **Ψ SOUL** | **Final Judgment**. Synthesizes Truth+Safety for Verdict. | **F2** (Truth), **F3** (Consensus), **F8** (Genius) |
| `vault_seal` | **VAULT** | **Immutable Ledger**. Cryptographic commit of the session. | **F1** (Amanah) |

---

## ⚙️ VIII. Technical Implementation
arifOS is built on a Python core, employing the **Model Context Protocol (MCP)** for universal compatibility.

**Key Technologies:**
*   **Python 3.10+**: Core logic.
*   **Axiom Engine**: Property-aware physical constant retrieval.
*   **Merkle DAG**: Cryptographic auditing of decision trees.
*   **FastMCP**: High-performance SSE/Stdio transport.

**Directory Structure:**
```text
arifOS/
├── 000_THEORY/          # Constitutional Canon (The Law)
├── 333_APPS/            # Application Stack (L1-L7)
├── codebase/            # Core Python Implementation
│   ├── agi/             # Cognition Engine
│   ├── asi/             # Safety Engine
│   ├── apex/            # Judicial Engine
│   └── mcp/             # MCP Server (Production API)
└── aaa_mcp/             # Hardened Server Adapters
```

---

## 📦 IX. Installation & Usage

### 1. Installation
```bash
pip install arifos
```
*Or from source:*
```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e .
```

### 2. Running the AAA MCP Server (Production)
**Cloud / Remote (SSE Mode):**
```bash
python -m aaa_mcp sse
# Endpoint: http://0.0.0.0:8080/sse
```

**Local Desktop (Stdio Mode):**
*Add to `claude_desktop_config.json` or Cursor config:*
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    }
  }
}
```

---

## 🤝 X. Contributing & Governance
We welcome contributions that adhere to the **Constitutional Canon**.

1.  **Read the Law**: Start with `000_THEORY/000_LAW.md`.
2.  **Test**: Run `pytest tests/` to ensure you haven't broken the floors.
3.  **Submit**: Open a PR. The APEX system will auto-review your code against the constitution.

**License:** AGPL-3.0 — *Open restrictions for open safety.*

---

**arifOS** — *Forged in the Fires of Governance.*
