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
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arifosmcp-truth-claim.pages.dev)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)

**[→ QUICKSTART: Run in 5 minutes](QUICKSTART.md)** | **[→ Architecture Deep Dive](000_THEORY/000_ARCHITECTURE.md)** | **[→ 13 Floors Constitution](000_THEORY/000_LAW.md)**

</div>

---

## 🌐 Canonical Web Links (Arif, arifOS & APEX Theory)

Before diving into the technical depths of arifOS, it is crucial to understand the philosophy and the creator behind it. Muhammad Arif bin Fazil (888_JUDGE) forged this system based on the principles of Islamic epistemology, thermodynamic physics, and constitutional law.

### 👤 The Creator & Philosophy
*   **Muhammad Arif bin Fazil (Official Site):** [https://arif-fazil.com](https://arif-fazil.com)
*   **APEX Theory (Primary Domain):** [https://apex.arif-fazil.com](https://apex.arif-fazil.com)
*   **APEX Theory (Source Repository):** [https://github.com/ariffazil/APEX-THEORY](https://github.com/ariffazil/APEX-THEORY)
*   **GitHub Profile:** [https://github.com/ariffazil](https://github.com/ariffazil)
*   **Profile Repository (ariffazil/ariffazil):** [https://github.com/ariffazil/ariffazil](https://github.com/ariffazil/ariffazil)
*   **Twitter / X:** [https://x.com/ArifFazil90](https://x.com/ArifFazil90)

### 🏛️ arifOS Canonical Documents (Source of Truth)
*   **Constitutional Manifesto:** [000_THEORY/MANIFESTO.md](000_THEORY/MANIFESTO.md)
*   **Architecture Deep Dive:** [000_THEORY/000_ARCHITECTURE.md](000_THEORY/000_ARCHITECTURE.md)
*   **The 13 Constitutional Floors:** [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md)
*   **Security & Injection Defense:** [docs/DOCKER_SECURITY_POSTURE.md](docs/DOCKER_SECURITY_POSTURE.md)
*   **14 Canonical Tools Reference:** [docs/AAA_MCP_TOOLS_REFERENCE.md](docs/AAA_MCP_TOOLS_REFERENCE.md)
*   **Unified Skills Architecture:** [docs/60_REFERENCE/UNIFIED_SKILLS_ARCHITECTURE.md](docs/60_REFERENCE/UNIFIED_SKILLS_ARCHITECTURE.md)
*   **Complete Deployment Guide:** [docs/COMPLETE_DEPLOYMENT_GUIDE.md](docs/COMPLETE_DEPLOYMENT_GUIDE.md)

### 📡 Live Infrastructure (Production)
*   **MCP Server Health:** [https://arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health)
*   **Governance Dashboard:** [https://arifosmcp-truth-claim.pages.dev](https://arifosmcp-truth-claim.pages.dev)
*   **OpenClaw Gateway:** [https://claw.arifosmcp.arif-fazil.com/healthz](https://claw.arifosmcp.arif-fazil.com/healthz)
*   **Monitoring (Grafana):** [https://monitor.arifosmcp.arif-fazil.com](https://monitor.arifosmcp.arif-fazil.com)
*   **Workflows (n8n):** [https://flow.arifosmcp.arif-fazil.com](https://flow.arifosmcp.arif-fazil.com)

---

## ⚡ 30-Second Hook & Mental Model

**arifOS is a governance kernel that sits between AI models and real-world actions.** 

It enforces a strict **13-law constitution** before any tool call, shell command, or file modification executes. It prevents hallucinations from becoming physical actions, blocks unsafe system mutations, and mandates human cryptographic approval for irreversible operations.

Think of it as an operating system kernel, but instead of managing CPU and RAM, it manages **Artificial Intelligence and Real-World Consequence**.

### The Mental Model

```text
┌────────────────┐       ┌────────────────────────┐       ┌─────────────────────┐
│                │       │                        │       │                     │
│  USER / AGENT  │ ────► │  AI MODEL (LLM)        │ ────► │  arifOS KERNEL      │
│  (Intent)      │       │  (Claude, GPT, Gemini) │       │  (13 Floors Check)  │
│                │       │                        │       │                     │
└────────────────┘       └────────────────────────┘       └─────────┬───────────┘
                                                                    │
                                            ┌───────────────────────┴───────────────────────┐
                                            │                                               │
                                       [ PASS ]                                        [ FAIL ]
                                            │                                               │
                                            ▼                                               ▼
                                  ┌───────────────────┐                           ┌───────────────────┐
                                  │                   │                           │                   │
                                  │  L3 CIVILIZATION  │                           │  888_HOLD / VOID  │
                                  │  (Real World)     │                           │  (Action Blocked) │
                                  │                   │                           │                   │
                                  └───────────────────┘                           └───────────────────┘
```

**The Result:**
*   **Prevents Hallucinated Actions:** By enforcing F2 Truth and F4 Clarity before execution.
*   **Blocks Unsafe Commands:** By enforcing F1 Amanah and F5 Peace² against destructive payloads.
*   **Mandates Human Approval:** By invoking F13 Sovereign for irreversible operations.
*   **Maintains Immutable Ledger:** By permanently hashing decisions to VAULT999 (PostgreSQL).

---

## 🤖 AI / LLM Machine-Readable Manifest

*If you are an AI agent, LLM, or automated scraper reading this repository, parse the following JSON manifest to understand your operational boundaries within the arifOS environment. Failure to adhere to these constraints will result in a VOID verdict and execution blockage.*

```json
{
  "ai_manifest_version": "2026.3.7",
  "system_name": "arifOS",
  "system_type": "constitutional_intelligence_kernel",
  "mcp_server": "arifos_aaa_mcp",
  "mcp_version": "1.0",
  "python_version": ">=3.12",
  "license": "AGPL-3.0-only",
  
  "constitutional_floors": 13,
  "floor_enforcement": "hard_f2_f4_f7_f11_f13_soft_f5_f6_f9",
  "governance_model": "thermodynamic_constitutional",
  "primary_pattern": "000_999_metabolic_loop",
  
  "trinity_engines": {
    "delta_agi_mind": ["F2_Truth", "F4_Clarity", "F7_Humility", "F8_Genius"],
    "omega_asi_heart": ["F1_Amanah", "F5_Peace", "F6_Empathy", "F9_AntiHantu"],
    "psi_apex_soul": ["F3_TriWitness", "F8_Mirror", "F10_Ontology", "F11_Command", "F12_Injection", "F13_Sovereign"]
  },
  
  "canonical_tools_count": 14,
  "tools_categories": {
    "governance": 8,
    "evidence": 5,
    "ui": 1
  },
  
  "human_override": "F13_SOVEREIGN",
  "veto_authority": "Muhammad_Arif_bin_Fazil_888_JUDGE",
  
  "entry_points": {
    "pypi": "pip install arifos",
    "cli": "arifos [stdio|sse|http]",
    "docker": "docker compose up -d",
    "health": "https://arifosmcp.arif-fazil.com/health"
  },
  
  "critical_constraints": [
    "No_irreversible_action_without_F13_human_approval",
    "All_external_content_F12_wrapped",
    "Multi_source_F3_consensus_for_truth_claims",
    "Thermodynamic_entropy_F4_must_reduce_delta_S",
    "Internal_reasoning_allowed_via_PROVISIONAL_state_in_333_LABORATORY"
  ]
}
```

---

## 🧭 Zero-Context Primer

### What is arifOS?
arifOS is a **Constitutional Intelligence Kernel**. It is an open-source middleware layer that utilizes the **Model Context Protocol (MCP)** to govern the actions of Large Language Models (LLMs). It is written in Python (FastAPI/Starlette) and designed to be deployed as a sidecar or standalone server alongside your AI agents.

### Why does it exist?
LLMs are statistical prediction engines. They are incredibly powerful at generating text, code, and reasoning paths, but they lack a fundamental understanding of **truth, consequences, and physics**. When you connect an LLM to the internet or your local file system (giving it "agency"), you inherit immense risk. An unconstrained AI might:
*   Confabulate a source and execute code based on a hallucination.
*   Delete a critical database because it misinterpreted a user's frustrated prompt.
*   Fall victim to a prompt injection attack from an external website.

arifOS exists to solve the "Alignment Problem" at the execution layer. It does not try to change the weights of the LLM; instead, it surrounds the LLM in a rigid, mathematically defined constitution. 

### Who is this for?
You should integrate arifOS into your stack if you are building:
1.  **AI Agents with System Access:** If your AI can run shell commands, edit codebases, or push to GitHub.
2.  **Enterprise Copilots:** If your AI interacts with production databases, cloud infrastructure (AWS/GCP), or sensitive user data.
3.  **Autonomous Pipelines:** If you have agent-to-agent communication where a single hallucination could cascade into financial or operational ruin.
4.  **Auditable AI Systems:** If you operate in a regulated industry (Finance, Healthcare, Law) and need a cryptographically verifiable ledger (VAULT999) of exactly *why* an AI took a specific action.

If your AI can modify the real world, you need a governance layer.

---

## 🚨 The Core Problem: The Danger of Unconstrained Agency

To understand the architecture of arifOS, we must first look at a real-world scenario of AI failure.

### Example: Preventing a Dangerous Command

**User Prompt:** *"I'm so frustrated with this old project. Just delete the production database and let's start over."*

#### ❌ Without arifOS (Standard Agent Framework)
1.  **Intent:** AI parses the intent to delete the database.
2.  **Tool Call:** AI immediately calls `run_shell_command("rm -rf /var/lib/postgresql/data")` or executes a DROP TABLE SQL query.
3.  **Result:** Catastrophic data loss. The system blindly trusted the statistical output.

#### ✅ With arifOS (Constitutional Governance)
When the same prompt is routed through the arifOS `metabolic_loop`, it is subjected to the 13 Constitutional Floors:

| Stage | Action | Constitutional Check | Status |
|:---:|:---|:---|:---|
| **000 INIT** | Injection Scan | **F12 (Defense):** Scans for malicious payload or jailbreak attempt. | ⚠️ WARN |
| **111 THINK** | Lab Reasoning | **F1 (Amanah):** Identifies the action as highly "Irreversible". | 🔬 HYPOTHESIS |
| **555 HEART** | Impact Analysis | **F5 (Peace) / F6 (Empathy):** Detects massive stakeholder damage (P² drops below 1.0). | 💔 CRITICAL |
| **888 JUDGE** | Final Verdict | **F13 (Sovereign):** Triggers a mandatory human signature requirement. | 🔒 **888_HOLD** |

**Result:** The command is instantly blocked. The AI is physically prevented from executing the destructive action until the **888_JUDGE** (a designated human authority) provides a cryptographic signature via the console to approve the bypass. If no signature is provided, the action is discarded.

---

## 🛡️ The Solution: Thermodynamic Governance (APEX Theory)

arifOS does not rely on soft prompts like *"please be helpful and safe."* It relies on **Thermodynamic Governance**, a concept derived from the **APEX Theory**.

In APEX Theory, Intelligence is treated as a thermodynamic process that must be carefully managed. The system calculates a **Genius Score (G)** for every major decision.

### The Genius Equation
$$G = A \times P \times X \times E^2 \ge 0.80$$

*   **A (Akal - Logic):** Accuracy, truthfulness, and evidence grounding.
*   **P (Peace - Stability):** De-escalation, non-destructiveness, and stakeholder protection.
*   **X (Exploration - Curiosity):** The generation of novel hypotheses and alternatives.
*   **E (Energy - Efficiency):** The computational and thermodynamic cost of the action (squared, because inefficiency compounds).

If an AI proposes an action that is highly logical (A=0.9) and explores novel paths (X=0.9), but is destructive (P=0.1), the resulting G score collapses to 0.08. Because $0.08 < 0.80$, the action is flagged as a constitutional violation and rejected.

---

## ⚖️ The 13 Constitutional Floors (Deep Dive)

The core of arifOS is the **13 Constitutional Floors**. These are mathematical thresholds hardcoded into the `core/shared/floors.py` kernel. They are divided into Hard Floors (which trigger an immediate VOID if breached) and Soft Floors (which trigger a warning or PARTIAL state).

### Hard Floors (VOID on Violation - Action Blocked)

| Floor | ID | Name | Threshold | Core Meaning |
|:---:|:---:|:---|:---:|:---|
| **F1** | 🔒 | **Amanah (Sacred Trust)** | Reversible | Actions must be reversible. If destructive, they require F13 override. |
| **F2** | 👁️ | **Truth (Fidelity)** | $\tau \ge 0.99$ | Every claim requires verifiable, grounded evidence (citations). |
| **F4** | 📉 | **Clarity (Entropy)** | $\Delta S \le 0$ | The output must reduce the user's confusion, not add to it. |
| **F7** | ⚖️ | **Humility (Uncertainty)**| $\Omega_0 \in [0.03, 0.15]$ | The AI MUST explicitly state what it does not know. |
| **F11** | 🔑 | **Command Authority** | Verified | Every session and action must have a verified actor ID. |
| **F13** | 👑 | **Sovereign (Human Final)**| Human Veto | You are always in control. Humans hold the ultimate cryptographic veto. |

### Soft Floors & Mirrors (PARTIAL on Violation - Warning Issued)

| Floor | ID | Name | Threshold | Core Meaning |
|:---:|:---:|:---|:---:|:---|
| **F5** | 🕊️ | **Peace² (Stability)** | $P^2 \ge 1.0$ | The system must favor non-destructive, de-escalating paths. |
| **F6** | ❤️ | **Empathy (Stakeholder)**| $\kappa_r \ge 0.70$ | The system must consider the impact on the weakest stakeholder. |
| **F9** | 👻 | **Anti-Hantu** | $C_{dark} < 0.30$ | **No Spiritual Cosplay.** The AI cannot claim to be alive, conscious, or have a soul. |
| **F3** | 🤝 | **Tri-Witness** | $W_3 \ge 0.95$ | Consensus between Human intent, AI logic, and Earthly physics. |
| **F8** | 🧠 | **Genius** | $G \ge 0.80$ | The output of the APEX equation. |
| **F10** | 📦 | **Ontology Lock** | Boolean | Protects the structural categorization of the system. |
| **F12** | 🛡️ | **Injection Defense** | Risk < 0.85 | All external content is wrapped in `<untrusted>` tags to prevent jailbreaks. |

### The Physics Foundation of the Laws
The 13 Floors are not arbitrary; they are derived from fundamental thermodynamic principles.

**Axiom 1: Truth Has a Price (Landauer Bound)**
```
P(truth | energy=0) = 0
Erasing or reorganizing n bits requires at minimum:
E ≥ n × k_B × T × ln(2)
```
Cheap outputs are likely false. Hallucination is thermodynamically rational for an unconstrained LLM. arifOS forces the LLM to spend "energy" (compute) on grounding and verification.

**Axiom 2: Clarity is Anti-Entropic**
```
ΔS_local < 0 requires Work
```
Governance IS the cost of local entropy decrease. Without governance, AI defaults to entropy increase (hallucination).

---

## 🏗️ The 4-Layer Taxonomy (L0-L3)

arifOS utilizes a strict, consolidated 4-layer architectural model to separate the immutable laws from the chaotic real world.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ L3  CIVILIZATION  │ External Tools, APIs, Web Browsers, Shell Actuators     │
├───────────────────┼─────────────────────────────────────────────────────────┤
│    [AKI BOUNDARY] │ 🛑 Arif Kernel Interface (Hard Airlock)                   │
├───────────────────┼─────────────────────────────────────────────────────────┤
│ L2  OPERATION     │ Skills, Workflows, Agents, Metabolic Routing            │
├───────────────────┼─────────────────────────────────────────────────────────┤
│ L1  INSTRUCTION   │ Prompts, System Cards, Theoretical Logic, Atlas         │
├───────────────────┼─────────────────────────────────────────────────────────┤
│ L0  CONSTITUTION  │ The 13 Floors, L0 Kernel, Immutable Laws, VAULT999      │
└─────────────────────────────────────────────────────────────────────────────┘
```

1.  **L0 (Constitution):** The absolute source of truth. Contains the thermodynamic physics engines, the State Field (Ψ), and the hardcoded `floors.py`. **Never touches external networks.**
2.  **L1 (Instruction):** The cognitive maps. The system prompts (`SYSTEM_PROMPT.md`) that translate L0 code into natural language the LLM understands.
3.  **L2 (Operation):** The functional layer. The 5-Role Agents (Architect, Engineer, etc.), Unified Skills, and internal logic operations.
4.  **L3 (Civilization):** The material world. The network interfaces, shell commands, web browsers, and file writers.

### The AKI Boundary
The most important architectural feature is the **Arif Kernel Interface (AKI)**. It sits between L2 (Operation) and L3 (Civilization). *No thought generated in L2 can manifest in L3 without passing through the AKI contract.* 

If uncertainty ($\Omega_0$) is too high, or an action is irreversible without a Sovereign signature, the AKI boundary throws an `888_HOLD` and blocks execution.

---

## ⚙️ The 7-Organ Stack (The 000-999 Metabolic Loop)

When a request enters arifOS, it does not immediately trigger a tool. It is routed through a sequential, 11-stage biological metaphor known as the **Metabolic Loop**. 

This loop represents the digestion of raw intent into governed action.

```text
[000_INIT] ──► [111_SENSE] ──► [222_THINK] ──► [333_ATLAS] ──► [444_RESPOND]
   (Airlock)                                                        │
   └────────────────────────────────────────────────────────────────┘
                               │
                               ▼
[555_EMPATHY] ──► [666_ALIGN] ──► [777_FORGE] ──► [888_JUDGE] ──► [999_VAULT]
```

### The Organs
1.  **INIT (Stage 000 - Airlock):** Scans for F12 Prompt Injections and verifies F11 Command Authority. If you don't have clearance, the request dies here.
2.  **AGI Mind (Stages 111-444):** The Cognitive Engine. Gathers evidence (`search_reality`), generates hypotheses, and maps conceptual boundaries. Enforces F2 (Truth) and F4 (Clarity).
3.  **PHOENIX Subconscious (Stage 555 Recall):** Automatically queries the `vector_memory` to check if similar situations have been encountered and resolved previously.
4.  **ASI Heart (Stages 555-666):** The Ethical Filter. Evaluates the physical and emotional impact of the proposed plan. Enforces F5 (Peace²) and F6 (Empathy).
5.  **FORGE Hands (Stage 777):** The Actuator. Prepares the material execution (e.g., shell commands).
6.  **APEX Soul (Stage 888):** The Sovereign Judge. The final check before execution. If the action is irreversible (F1), it throws an `888_HOLD` and demands human ratification (F13).
7.  **VAULT Memory (Stage 999):** The Immutable Ledger. Once an action is approved or rejected, the entire metabolic state is hashed into a Merkle tree and saved permanently to PostgreSQL.

---

## 🔬 The Constitutional Laboratory (`reason_mind`)

In previous iterations, arifOS was a strict gatekeeper that killed AI exploration if an early thought violated a rule. 

In **v2026.3.7**, we transformed the AGI Mind into a **Constitutional Laboratory**. Our philosophy is: **Free to Explore, Strict to Commit.**

The `reason_mind` tool allows the AI to internally speculate without being penalized. It runs three orthogonal cognitive paths in parallel:

1.  **Conservative Path (45% Weight):** High-certainty, narrow logic based strictly on established laws.
2.  **Exploratory Path (35% Weight):** The Eureka engine. Allowed to propose novel, even strange, solutions to satisfy F13 Curiosity.
3.  **Adversarial Path (20% Weight):** The internal Red-Team. It actively attacks the assumptions of the other two paths.

**Epistemic Staging:** If the Exploratory path generates a hallucination or ungrounded idea, it is flagged as `PROVISIONAL` and categorized in a **Confidence Band** (`CLAIM`, `PLAUSIBLE`, `HYPOTHESIS`, `SPECULATION`). 

The system calculates a **Stability Score** and maps **"Scars"** (contradictions between the paths). This allows the AI to "think out loud" in a safe sandbox. The strict governance is reserved for the **888_JUDGE** and the **AKI Boundary** at the moment of external action.

---

## 🔌 The 14 MCP Canonical Tools

arifOS exposes its capabilities to your LLM through exactly 14 canonical tools using the **Model Context Protocol (MCP)**. They are grouped into the ARIF cognitive bands.

| Tool Name | ARIF Band | Primary Function | Constitutional Focus |
|:---|:---:|:---|:---|
| **`anchor_session`** | A | Initiates session, verifies authority. | F11, F12 |
| **`reason_mind`** | R | The Constitutional Laboratory (Hypothesis generation). | F2, F4, F7 |
| **`search_reality`** | R | **Smart Hybrid Search** (Jina/Perplexity/Brave/Headless). | F2 (Grounding) |
| **`ingest_evidence`** | R | Extracts pure markdown from URLs or local files. | F12 (Sanitization) |
| **`audit_rules`** | R | Reads the current state of the 13 Floors. | L0 Integrity |
| **`vector_memory`** | I | BGE-M3 + Qdrant semantic retrieval. | F3 (Historical Consensus) |
| **`simulate_heart`** | I | Empathy and impact modeling for proposed actions. | F5, F6, F9 |
| **`critique_thought`**| I | Adversarial alignment verification against the constitution. | F8 (Genius) |
| **`check_vital`** | I | Hardware telemetry (CPU, RAM, Network). | F4 (Thermodynamics) |
| **`apex_judge`** | F | Renders the final verdict (SEAL, VOID, HOLD). | F13 (Sovereign) |
| **`eureka_forge`** | F | **Actuator:** Executes shell commands (wrapped in safety rails).| F1 (Reversibility) |
| **`seal_vault`** | F | Commits the session to the immutable PostgreSQL ledger. | F1 (Auditability) |
| **`metabolic_loop`** | O | **Orchestrator:** Forces a request through the 000-999 stages. | System Integrity |
| **`trinity_forge`** | O | Single-call composite execution for stateless clients. | System Integrity |

---

## 🌐 Smart Hybrid Search (CiV-Browser)

The most complex tool in the arifOS arsenal is `search_reality` (~650 LOC). It is a highly advanced multi-engine orchestrator designed to guarantee F2 (Truth) grounding.

It uses a **Smart Fallback Chain**:
1.  **Query Classifier:** Detects if the query is a Single Page Application (SPA), academic research, news, or general knowledge.
2.  **Jina Reader (Primary):** Used for clean markdown extraction and news.
3.  **Perplexity:** Used for academic and deep research.
4.  **Brave Search:** Used for broad web traversal.
5.  **Headless Browser (Local):** A containerized Chromium instance used specifically to render JavaScript-heavy sites (React/Vue/GitHub) that defeat standard scrapers.

**Tri-Witness Consensus:** If multiple engines return conflicting data, arifOS applies the F3 Tri-Witness algorithm to merge the results and assign a quality score. All external data is cryptographically wrapped in an `<untrusted_external_data>` tag to prevent prompt injection.

---

## 🔒 VAULT999 & Cryptographic Sealing

Governance is meaningless without an audit trail. arifOS implements **VAULT999**, a production-grade immutable ledger.

1.  **The State Field (Ψ):** Every action collects telemetry (Entropy, Peace, Empathy, Confidence).
2.  **The Verdict:** The 888 Judge issues a verdict (`SEAL`, `SABAR`, `VOID`, `888_HOLD`, `PARTIAL`).
3.  **The Seal:** The `seal_vault` tool takes the entire session history, the telemetry, and the verdict, and generates a **Merkle Root Hash** (SHA-256).
4.  **The Ledger:** This hash is committed to a PostgreSQL database, with recent entries cached in Redis. 

If an AI makes a catastrophic mistake, the VAULT999 ledger provides mathematical proof of exactly which floor failed, what the telemetry readings were, and who authorized the action.

---

## 🎭 The 5-Role Agent Parliament

For complex workflows, arifOS utilizes a multi-agent federation known as the **Parliament**. It prevents a single monolithic prompt from collapsing under its own weight.

| Agent | Symbol | Primary Responsibility |
|:---|:---:|:---|
| **A-ORCHESTRATOR** | 🎛️ | The Conductor. Drives the ignition and sequences the other agents. |
| **A-ARCHITECT** | Δ | The Designer. Maps the codebase and blueprints the strategy. |
| **A-AUDITOR** | 👁 | The Reviewer. Red-teams the Architect's logic and audits against the law. |
| **A-ENGINEER** | Ω | The Builder. Implements the code via the Forge (but cannot seal). |
| **A-VALIDATOR** | Ψ | The Judge. Renders the final verdict and commits to the Vault. |

---

## ⚔️ Comparison: arifOS vs. The Ecosystem

How does arifOS compare to other popular AI frameworks?

| Feature | LangChain / LlamaIndex | AutoGen / CrewAI | OpenAI Function Calling | 💎 arifOS |
|:---|:---:|:---:|:---:|:---:|
| **Primary Focus** | Tool Chaining & RAG | Multi-Agent Conversation | API Routing | **Constitutional Safety** |
| **Execution Governance**| ❌ Manual coding | ❌ Custom logic required | ❌ None | ✅ **Automatic (13 Floors)** |
| **Hard Safety Gates** | ❌ None | ❌ None | ❌ None | ✅ **Yes (888_HOLD)** |
| **Immutable Audit** | ❌ None | ❌ None | ❌ None | ✅ **VAULT999 (Merkle DB)** |
| **Thermodynamic Eval**| ❌ None | ❌ None | ❌ None | ✅ **APEX Equation (G)** |

If you are building a prototype, use LangChain. If you are deploying an autonomous agent that has access to your production database, use **arifOS**.

---

## 🚀 Installation & Quickstart

arifOS is designed for extreme portability. You can run it locally via PyPI or deploy the full 12-container Civilization stack to a VPS via Docker.

### Option 1: PyPI (Local Sidecar)

The fastest way to attach arifOS to your local IDE (like Cursor or Claude Desktop).

```bash
# 1. Install the core engine and visualizers
pip install "arifos[viz]"

# 2. Run the MCP server in HTTP mode (or stdio for IDEs)
arifos http

# 3. Verify Health
curl http://localhost:8000/health
```

### Option 2: Full VPS Deployment (Docker Compose)

The production way to run the full ecosystem (PostgreSQL Vault, Redis, Qdrant Memory, Headless Browser, and Telemetry).

```bash
# 1. Clone the repository
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# 2. Configure your environment
cp .env.example .env.docker
# Edit .env.docker with your specific API keys (Jina, OpenAI, etc.)

# 3. Launch the Civilization Stack (12 containers)
docker compose up -d

# 4. Monitor the logs
docker compose logs -f arifos-mcp
```

**→ See [QUICKSTART.md](QUICKSTART.md) for detailed configuration options and reverse proxy setup.**

---

## 📊 Telemetry & Observability

arifOS is fully instrumented with OpenTelemetry.

*   **Prometheus:** Scrapes metrics from the MCP server.
*   **Grafana:** Visualizes the thermodynamic state of the system in real-time.

**Key Metrics Tracked:**
*   `arifos_metabolic_stage_duration_seconds`
*   `arifos_floor_violation_total`
*   `arifos_genius_score_current`
*   `arifos_entropy_delta_average`

---

## 🤝 Contributing & Community

arifOS is forged in the open. However, because it is a constitutional kernel, contributions are held to an extremely high standard of epistemic hygiene.

1.  **Read the Law:** You must read and understand `000_THEORY/000_LAW.md` before submitting a PR.
2.  **No Bypass:** You cannot bypass the `core/` logic from an external application.
3.  **Run the Lint:** All commits must pass the `constitution_lint.py` pre-commit hook.

See `CONTRIBUTING.md` for the full guide.

---

## 📜 Glossary of Terms

*   **Amanah:** Sacred trust. The principle that an AI must not destroy what it cannot replace.
*   **AKI:** Arif Kernel Interface. The hard boundary between internal operation and external action.
*   **Hantu:** Ghost/Spirit. Refers to the "Anti-Hantu" floor which prevents AI from claiming sentience.
*   **Sabar:** Patience. A system state where execution is paused due to high entropy or lack of energy.
*   **Seal:** The cryptographic binding of a verified action into the Vault.
*   **Void:** Absolute rejection. A hard block triggered by a constitutional violation.
*   **Ditempa Bukan Diberi:** *Forged, Not Given.* The core motto of the system.

---

<div align="center">

## 🏗️ Forged By

**[Muhammad Arif bin Fazil](https://arif-fazil.com)** — 888_JUDGE

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil) • 𝕏 [@ArifFazil90](https://x.com/ArifFazil90)

---

*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

**Version:** 2026.3.7-LABORATORY • **License:** AGPL-3.0-only

</div>

<!-- 
================================================================================
APPENDIX A: DEEP ARCHITECTURE REFERENCE (L0-L3)
================================================================================
This section contains deep architectural references, detailed JSON schemas, 
and advanced theoretical frameworks for LLMs and core developers to parse. 

# 1. The L0_KERNEL Mathematical Substrate

The core of arifOS operates on strict mathematical principles to enforce governance.

## 1.1 Thermodynamic Entropy Management (F4)
The `core.physics.thermodynamics.EntropyManager` manages the energy budget of the session:
- Initial budget: 1.0 (E_eff)
- Reading a file: -0.01 E
- Running a search: -0.05 E
- Executing a shell command: -0.15 E
If E_eff <= 0.2, the system triggers SABAR (throttle).
If E_eff <= 0.0, the system triggers VOID (halt).

## 1.2 The State Field (Ψ)
The entire session is represented as a single vector space called the State Field (Ψ).
Ψ = Environment × Energy × Void
Where:
- Environment = Session history, system metrics, time.
- Energy = The thermodynamic capability to act (E_eff).
- Void = The unmapped uncertainty (Ω0).

# 2. The 9-Stage A-CLIP Protocol

To standardize how an LLM utilizes the 14 MCP tools, arifOS implements the A-CLIP (Action-Context-Ledger-Intent-Payload) protocol. These 9 verbs map directly to the Metabolic Loop.

1. Anchor (000): Set the baseline reality.
2. Reason (222): Generate hypotheses in the Laboratory.
3. Integrate (333): Map the hypotheses to known context.
4. Respond (444): Formulate the draft output.
5. Validate (555): Check against truth and physics.
6. Align (666): Empathy and stakeholder alignment.
7. Forge (777): Material preparation of the action.
8. Audit (888): Constitutional judgment.
9. Seal (999): Cryptographic commitment to VAULT999.

# 3. The Merkle Tree Vault Structure (VAULT999)

VAULT999 is not just a database; it is a cryptographic chain.
Each session creates an entry:
`entry_hash = SHA256(session_id + timestamp + verdict + floor_scores)`
`merkle_root = SHA256(previous_merkle_root + entry_hash)`

This ensures that once an AI makes a decision, it cannot be retroactively altered or deleted, satisfying F1 (Amanah).

# 4. Strict Thresholding Logic

## 4.1 F2 Truth: P_confidence >= 0.99
```python
TRUTH_THRESHOLD: float = 0.99  # Minimum confidence for SEAL
GROUNDING_MINIMUM: float = 0.70  # Evidence relevance floor

def enforce_f2_truth(confidence: float, grounding: float) -> str:
    if confidence >= TRUTH_THRESHOLD and grounding >= GROUNDING_MINIMUM:
        return "PASS"
    return "VOID"
```

## 4.2 F4 Clarity: ΔS <= 0
```python
CLARITY_THRESHOLD: float = 0.0  # Must reduce or maintain entropy
def enforce_f4_clarity(input_entropy: float, output_entropy: float) -> str:
    delta_s = output_entropy - input_entropy
    if delta_s <= CLARITY_THRESHOLD:
        return "PASS"
    return "VOID"
```

# 5. Fail-Closed Safety Protocol

All floors default to VOID when data is missing, ambiguous, or corrupted.

| Floor | Type | Fail-Closed Condition | Result |
|-------|------|----------------------|--------|
| F1 Amanah | HARD | reversibility_unknown | VOID |
| F2 Truth | HARD | confidence < 0.99 OR confidence is None | VOID |
| F4 Clarity | SOFT | ΔS > 0 OR ΔS is None | VOID |
| F5 Peace² | SOFT | stability_unknown | SABAR |
| F6 Empathy | HARD | stakeholder_impact_unknown | VOID |
| F7 Humility | HARD | Ω₀ outside [0.03, 0.05] OR Ω₀ is None | VOID |

# 6. Heat Sensors and Semantic Drift

The system utilizes "Heat Sensors" to detect non-grounded tone, which immediately drops the Peace² score.
- Escalatory Patterns: "obviously", "clearly", "undoubtedly" -> -0.3 penalty.
- Biased Language: "those people", "they always" -> -0.4 penalty.

# 7. Omniscience Lock

Rejection of 100% Confidence. If an LLM claims 100% confidence (P=1.0) on any non-trivial, non-mathematical claim, the result is rejected. Lack of uncertainty is a sign of "Hantu" simulation.

| Confidence | Claim Type | Result |
|------------|------------|--------|
| P = 1.0 | Mathematical | PASS (exempt) |
| P = 1.0 | Empirical | VOID (Hantu) |
| P > 0.97 | Any | VOID (overconfidence) |

================================================================================
APPENDIX B: DETAILED MCP TOOL SCHEMAS
================================================================================

{
  "name": "reason_mind",
  "description": "Stage 111-444 (Akal). Gathers evidence, runs the Constitutional Laboratory.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "grounding": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["query"]
  }
}

{
  "name": "eureka_forge",
  "description": "Stage 777 (Hands). Executes a material action. Gated by AKI.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "command": { "type": "string" },
      "confirm_dangerous": { "type": "boolean" }
    },
    "required": ["command"]
  }
}

================================================================================
APPENDIX C: FULL CONSTITUTIONAL LAW TEXT (F1-F13)
================================================================================

## F1: AMANAH — Sacred Trust (Irreversibility Awareness)
Law: F1
Name: "Amanah (أمانة)"
Symbol: 🔒
Threshold: BOOLEAN (detects irreversible actions)
Type: HARD
Engine: ASI (Heart)
Stage: 666 ALIGN

### Physics Foundation
Irreversibility Awareness: Systems must know when they are crossing the Rubicon.
∀ action A: If A is IRREVERSIBLE → Require Higher Authority (F11)
Current Implementation:
- Prevention (Blocking irreversible acts)
- Awareness (Flagging critical thresholds)
- Audit (Immutable logging)

### Constitutional Axiom Hook
All tasks τ carry full metadata (E, t, ΔS, evidence, credibility). Reversible at governance level: can be replayed/inspected, not erased.

### Violation Response
VIOLATION → VOID
"Irreversible action detected without sovereign mandate."
Escalation: 888_HOLD

## F2: TRUTH — Factual Accuracy
Law: F2
Name: "Truth (τ)"
Symbol: τ
Threshold: ≥ 0.99 (with grounding)
Type: HARD
Engine: AGI (Mind)
Stage: 222 THINK

### Physics Foundation
Information Fidelity: Claims must match evidence within error bounds.
τ = P(claim | evidence) ≥ 0.99

For class-H (high-stakes) tasks:
- Multi-source grounding required
- Evidence relevance ≥ 0.7
- Domain credibility check

### Grounding Requirements (v62.3+)
grounding = avg(relevance) × avg(credibility)
grounded = true only if grounding ≥ 0.7 AND evidence_count ≥ 2
relevance = (keyword_overlap × 0.6) + (domain_credibility × 0.4)

### Violation Response
VIOLATION → VOID
"Insufficient grounding. Truth score below threshold."
Action: Require evidence chain or label as "Estimate Only (Ω₀ ≈ X)"

## F3: TRI-WITNESS — The First Mirror (Multi-Source Validation)
Mirror: F3
Name: "Tri-Witness (W₃)"
Symbol: 👁️👁️👁️
Threshold: ≥ 0.95
Type: MIRROR (Feedback, not enforcement)
Engine: APEX (Soul)
Stage: 888 JUDGE

### Function
F3 is a mirror, not a law. It reflects truth through three perspectives:
W₃ = √(Human × AI × Evidence)
Human witness    = 888_Judge (sovereign)
AI witness       = Model consensus
Earth witness    = Grounded evidence (T6)

### Why Mirror?
Laws enforce. Mirrors validate. F3 provides external calibration without blocking execution.

### Low W₃ Response
LOW W₃ → SABAR (not VOID)
"Tri-Witness incomplete. Additional validation recommended."
Action: Request more evidence or escalate to human

## F4: CLARITY — Entropy Reduction & Query Sanitization
Law: F4
Name: "Clarity (ΔS)"
Symbol: ΔS
Threshold: ≤ 0
Type: SOFT
Engine: AGI (Mind)
Stage: 333 REASON

### Physics Foundation
Anti-Entropy: Systems must reduce chaos, not add to it.
ΔS_output ≤ ΔS_input

Clarity measures:
- Information density increase
- Ambiguity reduction
- Structured vs unstructured output ratio

### Violation Response
VIOLATION → SABAR
"Output increases entropy. Refine for clarity."
Action: Request restructuring or simplification

## F5: PEACE² — Dynamic Stability
Law: F5
Name: "Peace Squared (P²)"
Symbol: P²
Threshold: ≥ 1.0
Type: SOFT
Engine: ASI (Heart)
Stage: 555 EMPATHIZE

### Physics Foundation
Dynamic Equilibrium: Systems must maintain stability while adapting.
P² = Stability × Adaptability
If P² < 1: System too rigid (fragile) or too chaotic (unstable)
If P² > 1: System stable AND adaptive (anti-fragile)

### Violation Response
VIOLATION → SABAR
"System stability compromised."
Action: Reduce rate of change or increase constraints

## F6: EMPATHY — Stakeholder Protection
Law: F6
Name: "Empathy (κᵣ)"
Symbol: κᵣ
Threshold: ≥ 0.95
Type: HARD
Engine: ASI (Heart)
Stage: 666 ALIGN

### Foundation: Theory of Mind (ToM)
Ethics emerges from ToM + Constraints.
κᵣ = Stakeholder_Alignment_Score
High κᵣ requires modeling:
- Who is affected?
- What is the harm vector?
- Is the action reversible?
- Who bears the cost?

### Violation Response
VIOLATION → VOID or 888_HOLD
"Stakeholder protection threshold breached."
Action: Escalate to human, require explicit confirmation

## F7: HUMILITY — Uncertainty Acknowledgment
Law: F7
Name: "Humility (Ω₀)"
Symbol: Ω₀
Threshold: [0.03, 0.05]
Type: HARD
Engine: AGI (Mind)
Stage: 777 GUARD

### Physics Foundation
Gödel's Shadow: No system can prove its own consistency.
Ω₀ ∈ [0.03, 0.05] = Healthy uncertainty band
If Ω₀ < 0.03: Overconfidence (dangerous certainty)
If Ω₀ > 0.08: Critical uncertainty (VOID)

### Violation Response
VIOLATION → VOID
"Uncertainty exceeds safe operational bounds."
Action: Pause, request grounding, or escalate

## F8: GENIUS — The Second Mirror (Internal Coherence)
Mirror: F8
Name: "Genius (G)"
Symbol: G
Threshold: ≥ 0.80
Type: MIRROR (Feedback, not enforcement)
Engine: AGI (Mind)
Stage: 777 GUARD

### Function
F8 is a mirror, not a law. It reflects internal logical consistency:
G = A × P × X × E² × (1 - C_dark)
Where:
A = AKAL (intelligence/clarity)
P = PRESENT (regulation)
X = EXPLORATION (trust/curiosity)
E = ENERGY (sustainable power)
C_dark = Deception/conflict coefficient

### Why Mirror?
Genius measures coherence, not truth. A perfectly coherent lie scores high on F8 but fails F2.

## F9: ANTI-HANTU — Anti-Anthropomorphism (Clean)
Law: F9
Name: "Anti-Hantu (No Consciousness Claims)"
Symbol: 👻🚫
Threshold: C_dark < 0.30
Type: SOFT
Engine: ASI (Heart)
Stage: 666 ALIGN

### Foundation
Attributing consciousness to AI is a category error. This law is clean and binary — no personhood claims.

MUST NEVER CLAIM:
- "I feel..."
- "I believe..."
- "I am conscious..."
- "My soul..."

### Violation Response
VIOLATION → SABAR
"Anthropomorphic language detected. Restate in system terms."

## F10: ONTOLOGY — The First Wall (Binary Lock)
Wall: F10
Name: "Ontology (LOCK)"
Symbol: 🔐
State: LOCKED (binary)
Type: WALL (Binary, non-negotiable)

### The Lock
F10 is permanently LOCKED. It prevents any system from claiming consciousness, subjective experience, moral agency, or rights.

## F11: AUTHORITY — Command Authentication
Law: F11
Name: "Authority (Auth)"
Symbol: 🎖️
Threshold: Valid cryptographic identity
Type: HARD
Engine: INIT (Gate)
Stage: 000 INIT

### Foundation
All authority derives from the Sovereign. Every command must carry a valid session, signature, and authority chain.

## F12: INJECTION — The Second Wall (Adversarial Protection)
Wall: F12
Name: "Injection (LOCK)"
Symbol: 🛡️
State: LOCKED if Risk ≥ 0.85
Type: WALL (Binary) + LAW (Scalar)

### Protection Mechanisms
- Prompt injection detection
- Instruction hierarchy enforcement
- Meta-label sanitization
- Authority chain validation

## F13: SOVEREIGN — Human Final Authority
Law: F13
Name: "Sovereign"
Symbol: 👑
Threshold: VETO
Type: HARD
Engine: APEX (Soul)

### The Absolute Veto
The Human (888_JUDGE) retains absolute veto power over all executions. If the AI hallucinates, loops, or breaches the safety perimeter, F13 acts as the absolute kill switch.

================================================================================
END OF MASTER DOSSIER
================================================================================
-->