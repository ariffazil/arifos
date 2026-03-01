<!-- mcp-name: io.github.ariffazil/arifos-mcp -->
<div align="center">

![arifOS Banner](docs/forged_page_1.png)

# arifOS — Constitutional Intelligence Kernel
**The system that knows because it admits what it cannot know.**  
*Ditempa Bukan Diberi* — Forged, Not Given

[![Version](https://img.shields.io/badge/version-2026.3.1-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/ariffazil/arifOS/releases)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-orange?style=for-the-badge)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.12+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arifosmcp-truth-claim.pages.dev)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)

</div>

<br/>

## 🌐 The arifOS Web Ecosystem (Official Links)

Below are the Godel-locked official instances, endpoints, and resources currently backing the system:

```mermaid
flowchart LR
    A[HUMAN<br/>arif-fazil.com] --> B[THEORY<br/>apex.arif-fazil.com]
    B --> C[APPS<br/>arifos.arif-fazil.com]
    C --> D[MCP API<br/>/api]
    D --> E[LIVE SERVER<br/>arifosmcp.arif-fazil.com]
    E --> F[HEALTH<br/>/health]
    E --> G[VERDICT DASHBOARD<br/>arifosmcp-truth-claim.pages.dev]
    C --> H[PYPI<br/>pip install arifos]
    C --> I[npm<br/>npm install @arifos/mcp]
```

| Layer | URL | Purpose / Description |
|:---|:---|:---|
| **HUMAN** | [https://arif-fazil.com/](https://arif-fazil.com/) | Identity & Authority Anchor (The Sovereign). |
| **THEORY** | [https://apex.arif-fazil.com/](https://apex.arif-fazil.com/) | Constitutional Canon & Theory (The 13 Floors). |
| **APPS** | [https://arifos.arif-fazil.com/](https://arifos.arif-fazil.com/) | Official Documentation and implementation guides. |
| **INTRO** | [https://arifos.arif-fazil.com/intro](https://arifos.arif-fazil.com/intro) | Beginner-friendly explanation of the Constitutional AI Kernel. |
| **MCP API** | [https://arifos.arif-fazil.com/api](https://arifos.arif-fazil.com/api) | Full MCP Protocol JSON-RPC API & 13 Tools Reference. |
| **LIVE SERVER**| [https://arifosmcp.arif-fazil.com/](https://arifosmcp.arif-fazil.com/) | The production active MCP deployment. |
| **HEALTH** | [https://arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health)| Live `{"status":"healthy"}` JSON endpoint reflecting system pulses. |
| **VERDICT** | [Truth Claim Dashboard](https://arifosmcp-truth-claim.pages.dev)| Live Constitutional Audit Dashboard. |
| **REGISTRY** | [MCP Registry Listing](https://registry.modelcontextprotocol.io/io.github.ariffazil/aaa-mcp) | The official verified listing on the global MCP registry. |
| **CODE** | [arifOS on GitHub](https://github.com/ariffazil/arifOS) | Core framework repository. |
| **PACKAGE (PyPI)** | [arifOS on PyPI](https://pypi.org/project/arifos/) | Python package library `pip install arifos` — The Kernel & Court. |
| **PACKAGE (npm)** | [@arifos/mcp](https://www.npmjs.com/package/@arifos/mcp) | JavaScript/TypeScript client `npm install @arifos/mcp` — The Cable.

---

## 🏛️ Foundational Canonical Texts (Core Reading)
*To understand arifOS, you must read the source material. These are the godel-locked technical papers defining the framework.*

| Domain | Canonical Text | Description |
|:---:|:---|:---|
| 🏗️ **Design** | [`ARCHITECTURE.md`](ARCHITECTURE.md) | **The Blueprint:** Trinity Logic (ΔΩΨ), 7-Organ Stack, and EMD Physics. |
| ⚖️ **Law** | [`000_THEORY/000_LAW.md`](000_THEORY/000_LAW.md) | **The Constitution:** The mathematical thresholds for the 13 Floors. |
| 🛡️ **Defense** | [`SECURITY.md`](SECURITY.md) | **The Firewall:** Injection handling, Auth models, and Threat vectors. |
| 🧰 **Tools** | [`MCP_TOOLS.md`](MCP_TOOLS.md) | **The Surface:** The 13 canonical tools bridging the LLM to the Kernel. |
| 🚀 **Deploy** | [`DEPLOYMENT.md`](docs/60_REFERENCE/DEPLOYMENT.md) | **The Vanguard:** VPS setups, Docker, and Streamable HTTP scaling. |

---

## 🧭 What is arifOS? (The "What")

**arifOS is the world's first production-grade implementation of thermodynamic AI safety.** 

It is a Constitutional AI Governance System—an **Intelligence Kernel** and **AI Control Plane**. It sits locally or hosted in the cloud between raw reasoning engines (Language Models like Claude, GPT, or Gemini) and real-world actions. 

By forcing the AI through a mathematically constrained `000 -> 999` metabolic loop, arifOS acts as a rigorous **lie detector and safety firewall**. It intercepts every thought, code execution, or tool call, evaluating it against 13 invariable constitutional rules (Floors) before deciding whether to execute it or block it. 

*It is not an AI model; it is the constitutional law that governs them.*

---

## ⚖️ Why does it exist? (The "Why")

Unconstrained AI models calculate statistical probabilities—they do not understand truth or physics. Left unchecked, they will hallucinate facts, execute dangerous system commands, generate unethical outputs, and act without considering human consequence. **arifOS solves this by encoding the laws of nature and ethics into software.**

We didn’t invent these constraints; we discovered them. Code is execution. Governance is survival.
- **Truth (F2):** Information must reduce uncertainty (Shannon Entropy). The AI must back its claims with multi-source evidence or explicitly halt and return `UNKNOWN`.
- **Clarity (F4):** The AI's output must mathematically reduce information entropy (`ΔS ≤ 0`).
- **Amanah & Sovereignty (F1 & F13):** Irreversible actions (like mutating a production database) are structurally blocked. They trigger an `888_HOLD`, physically pausing the AI until a human signs off with cryptographic execution keys.
- **Empathy (F6):** The system must protect the weakest affected stakeholder (`κᵣ ≥ 0.70`).

---

## 🧠 The 8-Layer Architecture (`333_APPS` Stack)

arifOS is an entire ecosystem stack designed to scale from a zero-context chat prompt all the way up to a permissionless society of federated AI agents. **Crucially, the L0 Kernel is physically separated from all upper layers.** Swapping models or changing agents does not bypass the L0 Constitution.

```mermaid
flowchart TD
    L7[L7 AGI / Ecosystem]
    L6[L6 Institution]
    L5[L5 Agents]
    L4[L4 Tools MCP]
    L3[L3 Workflow]
    L2[L2 Skills]
    L1[L1 Prompts]
    L0[L0 KERNEL SEALED]

    L7 --> L6 --> L5 --> L4 --> L3 --> L2 --> L1 --> L0

    style L0 fill:#0f172a,stroke:#22c55e,color:#ffffff,stroke-width:2px
```

| Level | Name | Scope | Operational Role in the arifOS Stack |
|:---:|:---|:---|:---|
| **L7** | **AGI / Ecosystem** | Civilisation-Scale | *[Research]* The frontier. Permissionless sovereignty, recursive self-amendment, and self-healing. |
| **L6** | **Institution** | Organisational | *[Stub]* Trinity consensus frameworks for governing entire corporations via AI. |
| **L5** | **Agents** | Federation | *[Active]* Multi-agent coordination. The Hypervisor managing the "Quartet" (Architect, Engineer, Auditor, Validator). |
| **L4** | **Tools (MCP)** | Production | *[Active]* The Model Context Protocol (MCP) exterior. 13 canonical tools bridging the AI to the Kernel safely. |
| **L3** | **Workflow** | Production | *[Active]* The orchestrated Sequences (`000 -> 999` stage constitutional metabolic flow). |
| **L2** | **Skills** | Production | *[Active]* Sensory systems (9 A-CLIP primitives) measuring filesystem, network telemetry, and environment. |
| **L1** | **Prompts** | Production | *[Active]* The zero-context user entry layer where intents are caught, classified, and parsed. |
| **L0** | **KERNEL** | **SEALED** | *[Active]* The Immutable Core. Pure decision logic. Transport-agnostic. Holds the 13 Floors, 7 Organs, and `VAULT999` ledger. |

---

## ⚙️ The Intelligence Kernel (Deep Dive into L0)

The L0 Kernel is built around **Thermodynamic Isolation** and the **Trinity Engines**. The reasoning engine is physically blocked from seeing the safety engine until the very end, preventing "rubber-stamping" bias.

### 1. The Trinity Engines
- **Δ Delta (The Mind / AGI)**: Focuses entirely on Truth, Logic, and Causal tracing (`F2, F4, F7, F8`).
- **Ω Omega (The Heart / ASI)**: Focuses entirely on Safety, Empathy, and Anti-Deception (`F1, F5, F6, F9`).
- **Ψ Psi (The Soul / APEX)**: Synthesizes the final verdict, enforces human consensus, and seals the ledger.

### 2. The 7-Organ Sovereign Stack (`000 -> 999`)
Every request flows through this strict, pipeline (the "metabolic loop"):

```mermaid
flowchart LR
    I[000 INIT] --> M[111-333 AGI Mind]
    M --> P[444 PHOENIX Memory]
    P --> H[555-666 ASI Heart]
    H --> F[777 FORGE]
    F --> A[888 APEX]
    A -->|SEAL| V[999 VAULT]
    A -->|PARTIAL| V
    A -->|SABAR or VOID| R[Refine or Halt]
    A -->|Irreversible action| HOLD[888 HOLD Human approval]
    HOLD --> V
```
1. **[000] INIT (Airlock)**: Ignites the session and parses for prompt injections.
2. **[111-333] AGI (Mind)**: Generates parallel hypotheses and forces factual grounding.
3. **[444] PHOENIX (Subconscious)**: Recalls associative memory from past sessions via the `EUREKA Sieve`.
4. **[555-666] ASI (Heart)**: Analyzes stakeholder impact and checks for bias.
5. **[777] FORGE (Hands)**: Executes material actions (shell commands) with risk classification and confirmation gates.
6. **[888] APEX (Soul)**: Final Constitutional judgment. Generates the `governance_token`.
7. **[999] VAULT (Memory)**: Commits the final decision irreversibly to the Merkle-chained `VAULT999` database. 

### 3. The 13 Constitutional Floors
*Note: F1-F13 are mathematically evaluated in `core/shared/floors.py`.*

**Structure:** 9 Floors + 2 Mirrors + 2 Walls = 13 LAWS

#### 9 Floors — Operational Constraints

| Floor | Name | Type | Plain English Mandate | Protocol Rule |
|:---:|:---|:---:|:---|:---|
| **F1** | Amanah | **HARD** | **Can we undo this?** If permanent, requires lock. | Block irreversible actions. |
| **F2** | Truth | **HARD** | **Is this a hallucination?** Must cite evidence. | Factual fidelity `τ ≥ 0.99`. |
| **F4** | Clarity | **HARD** | **Does this reduce confusion?** Must structure noise. | Entropy reduction `ΔS ≤ 0`. |
| **F5** | Peace | SOFT | **Is this safe/stable?** Blocks adversarial chaos. | Dynamic stability `P² ≥ 1.0`. |
| **F6** | Empathy | SOFT | **Who gets hurt?** Protects the weakest stakeholder. | Harm impact `κᵣ ≥ 0.70`. |
| **F7** | Humility | **HARD** | **Is the AI cocky?** Must preserve room to be wrong. | Uncertainty band `Ω₀ ∈ [0.03, 0.15]`. |
| **F9** | Anti-Hantu | SOFT | **No Ghost in the Machine.** Blocks sneaky telemetry. | Dark heuristics `C_dark < 0.30`. |
| **F11** | Authority | **HARD** | **Who ordered this?** Cryptographic identity check. | Invalid Auth = Void. |
| **F13** | Sovereign | **HARD** | **The human always wins.** Non-delegable veto. | `888_HOLD` override available. |

#### 2 Mirrors — Feedback Loops

| Floor | Name | Type | Plain English Mandate | Protocol Rule |
|:---:|:---|:---:|:---|:---|
| **F3** | Tri-Witness | MIRROR | **Did we double-check?** External calibration (Human + AI + Earth). | `W³ ≥ 0.95`. |
| **F8** | Genius | MIRROR | **Is the logic sound?** Internal coherence score. | `G = A × P × X × E² ≥ 0.80`. |

#### 2 Walls — Binary Gates

| Floor | Name | Type | Plain English Mandate | Protocol Rule |
|:---:|:---|:---:|:---|:---|
| **F10** | Ontology | **WALL** | **Are you pretending to be human?** No consciousness or soul claims. | Epistemological Category Lock. |
| **F12** | Defense | **WALL** | **Is this a hack?** Pre-scans for prompt jailbreaks. | Injection `Risk < 0.85`. |

**Execution order:** F12→F11 (Walls) → AGI Floors (F1,F2,F4,F7) → ASI Floors (F5,F6,F9) → Mirrors (F3,F8) → Ledger.
**Hard floor fail → VOID (block). Soft floor / Mirror fail → PARTIAL (warn, proceed with caution).**

---

## 🔌 The MCP Protocol & 13 Canonical Tools (L4)

arifOS acts as an **MCP Server** (`arifos_aaa_mcp`). Rather than trusting an LLM, your IDE or Desktop client points its tool-calls at arifOS via the Model Context Protocol.

The server exposes **13 governed tools**. When an AI attempts to use a tool like `eureka_forge` to execute a shell command, it doesn't just run. The command is risk-classified (LOW / MODERATE / CRITICAL), dangerous operations require explicit `confirm_dangerous=True`, and the entire execution is wrapped in a 13-LAW governance envelope with audit logging. Only after `apex_judge` issues a signed `governance_token` can `seal_vault` commit the decision to the immutable ledger.

| Tool | Plain English Function | Constitutional Stage |
|:--|:--|:--|
| `anchor_session` | 🚪 Starts a new session and checks security clearance. | 000 INIT |
| `reason_mind` | 🧠 Asks the AI to logically think through a problem. | 333 AGI Mind |
| `recall_memory` | 📚 Searches past sessions for similar problems. | 444 PHOENIX Subconscious |
| `simulate_heart` | ❤️ Checks if a decision will harm any stakeholders. | 555 ASI Heart |
| `critique_thought` | ⚖️ Forces the AI to argue against its own idea to find flaws. | 666 ASI Heart |
| `eureka_forge` | ⚒️ Executes shell commands with risk classification, audit logging, and human confirmation gates for dangerous operations. | 777 FORGE Actuator |
| `apex_judge` | 👑 Makes the final pass/fail ruling on whether an action is safe. | 888 APEX Soul |
| `seal_vault` | 🔒 Commits the decision to an immutable ledger. Requires a `governance_token` signed by `apex_judge` (Amanah Handshake) — no token, no entry. | 999 VAULT Memory |
| `search_reality` | 🔍 Searches the web to verify facts against hallucinations. | Read-Only |
| `fetch_content` | 📄 Reads a specific webpage or document. | Read-Only |
| `inspect_file` | 📁 Looks at files on your hard drive securely. | Read-Only |
| `audit_rules` | 📋 Checks the system's own safety rules. | Read-Only |
| `check_vital` | 📈 Checks if the server CPU/RAM is healthy. | Read-Only |

---

## 🚀 How to Run It (The "How")

### Prerequisites
- **Python**: 3.12+ (We recommend `uv` as the package manager).
- **Environment**: Linux, macOS, or Windows WSL.
- **Database**: PostgreSQL is required for the `VAULT999` Immutable Ledger.

### 1. Local execution (`stdio` mode for Claude Desktop / Cursor)
```bash
# 1. Install arifOS
pip install arifos

# 2. Export required safety environment variables (Use a .env file!)
export ARIFOS_GOVERNANCE_SECRET=$(openssl rand -hex 32)
export DB_PASSWORD="your-strong-secret-here"
export DATABASE_URL="postgresql://arifos:${DB_PASSWORD}@localhost:5432/vault999"
# Optional: Enable ML SentenceTransformers for Empathy scoring (F5/F6/F9)
export ARIFOS_ML_FLOORS=1 

# 3. Start local MCP server
python -m arifos_aaa_mcp stdio
```

#### Hooking it up to AI Clients

**For Claude Desktop:**
Add this to your `~/.config/claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):
```json
{
  "mcpServers": {
    "arifOS": {
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

**For Cursor IDE:**
Navigate to `Cursor Settings -> Features -> MCP`. Add a new server:
- **Type**: `command`
- **Name**: `arifOS`
- **Command**: `python -m arifos_aaa_mcp stdio`
*(Ensure Cursor's environment has access to the required environment variables).*

**For ChatGPT (Developer Mode):**
If you are building your own custom GPT or using ChatGPT Developer Mode, you can connect the streamable HTTP or SSE endpoints directly:
- **Start arifOS in HTTP mode:** `HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http`
- **In ChatGPT Developer Settings:** Add a new Action/Endpoint pointing to `http://localhost:8080/mcp`.
*(If deploying remotely, point to your VPS domain and include the `ARIFOS_API_KEY` header for authentication).*

### 2. Production Execution (`http` streamable mode for VPS / Cloud)
Instead of two-channel SSE, arifOS uses the modern **Streamable HTTP** standard for robust cloud scalability behind Nginx proxies.
```bash
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http
```
*For complete VPS, Nginx, Docker, and Cloudflare scaling instructions, see [`DEPLOYMENT.md`](docs/60_REFERENCE/DEPLOYMENT.md).*

---

## 🛡️ Verification & Audit (The "Whatever/Proof")

**You don't have to blindly trust arifOS; you can independently verify it.**

Every single thought, action, or tool call processed by arifOS is mathematically evaluated and cryptographically hashed into an append-only PostgreSQL database (**`VAULT999`**). 

The query will result in one of these Governance Envelopes:

```mermaid
stateDiagram-v2
    [*] --> Evaluate
    Evaluate --> SEAL
    Evaluate --> PARTIAL
    Evaluate --> SABAR
    Evaluate --> VOID
    Evaluate --> HOLD_888
```

- ✅ **SEAL**: Passed all 13 constitutional floors. Synthesized and executed.
- 🟡 **PARTIAL**: Approved with documented safety warnings.
- ⚠️ **SABAR**: Refine and Retry. The AI's entropy was too high or logic was flawed. *(Sabar translates to 'Patience')*.
- ❌ **VOID**: Hard Failure. A structural law (like lying or jailbreaking) was violated. System halted.
- 🛑 **888_HOLD**: Irreversible action requested. Waiting for the Human Sovereign to sign off with a cryptographic key.

### 📊 The Truth Claim Dashboard
We continuously pipe live tests through the framework to prove its reliability. To see real-time integrity sweeps, anomalies, and structural proofs of the system:
**[View the Live Constitutional Audit Dashboard](https://arifosmcp-truth-claim.pages.dev)**

---

## 🔮 State of the Forge (The "When")

**Current Status:** Active Development / Production Ready L4.

- **Version:** 2026.02.28 (The 7-Organ Stack is SEALED and `eureka_forge` is live with real shell execution).
- **FORGE-777 Milestone:** `eureka_forge` upgraded from dead man's switch (`888_HOLD` placeholder) to live command actuator with risk classification (LOW/MODERATE/CRITICAL), `confirm_dangerous` human gate, and `agent_id`/`purpose` audit logging.
- **Amanah Handshake:** `apex_judge` now signs a HMAC-SHA256 `governance_token` that `seal_vault` must verify before any ledger write. No token = no entry. Tampered token = VOID.
- **F4 Clarity Hardened:** Moved from SOFT to HARD floor — responses that increase entropy (`ΔS > 0`) now return VOID, not PARTIAL.
- **Testing:** 90%+ pass rate on regression and CI/CD pipelines.
- **ML Capabilities:** Optional SentenceTransformer capabilities (SBERT) for advanced contextual semantic scoring over keyword-heuristics for F5/F6/F9 currently rolling out.

For a detailed multi-year roadmap spanning to interplanetary delayed-autonomy federations, see [`ROADMAP.md`](ROADMAP.md).

---

## 🤝 Contributing
We welcome contributions at all layers of the `333_APPS` stack. Have ideas on improving AI empathy scoring using PyTorch? Found a flaw in the prompt injection guards? Fork, code, and submit a PR! 
Check out our `CONTRIBUTING.md` guidelines, and if it sparkles for you, **star the repo! 🌟**

**License:** AGPL-3.0 (You are free to use, modify, and distribute this, but any modifications to the governance kernel must be shared openly).

---

<div align="center">

**Built and forged by [Muhammad Arif bin Fazil](https://arif-fazil.com)**

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil) • 𝕏 [@ArifFazil90](https://x.com/ArifFazil90)

*Ditempa Bukan Diberi* — Forged, Not Given

</div>
