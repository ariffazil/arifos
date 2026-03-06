<!-- mcp-name: io.github.ariffazil/arifos-mcp -->
<div align="center">

![arifOS Banner](docs/forged_page_1.png)

# arifOS — Constitutional Intelligence Kernel (ARIF)
**The system that knows because it admits what it cannot know.**  
*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

**What it is:** A constitutional decision kernel that governs tool execution for LLMs via MCP.  
**What it isn't:** Not a model, not an agent, not a chatbot.  
**What it guarantees:** A hardened L2–L5 stack with no irreversible action without explicit human approval.

[![Version](https://img.shields.io/badge/version-2026.3.1-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/ariffazil/arifOS/releases)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-orange?style=for-the-badge)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.12+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arifosmcp-truth-claim.pages.dev)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)
[![Coverage](https://codecov.io/gh/ariffazil/arifOS/graph/badge.svg?token=b458f4ac-fb08-4554-baf3-dc3967fafb79)](https://codecov.io/gh/ariffazil/arifOS)

**[→ QUICKSTART: Run in 5 minutes](QUICKSTART.md)**

</div>

> **Gödel-locked** = canonical endpoints whose content is governed by the constitutional sealing process; changes require Phoenix cooling + signed release.

---

## 🏛️ Foundational Canonical Texts (Core Reading)
*To understand arifOS, you must read the source material. These are the godel-locked technical papers defining the framework.*

| Domain | Canonical Text | Description |
|:---:|:---|:---|
| 🏗️ **Design** | [`ARCHITECTURE.md`](docs/60_REFERENCE/ARCHITECTURE.md) | **The Blueprint:** Trinity Logic (ΔΩΨ), 7-Organ Stack, and EMD Physics. |
| ⚖️ **Law** | [`000_THEORY/000_LAW.md`](000_THEORY/000_LAW.md) | **The Constitution:** The mathematical thresholds for the 13 Floors. |
| 🛡️ **Defense** | [`SECURITY.md`](docs/00_META/SECURITY.md) | **The Firewall:** Injection handling, Auth models, and Threat vectors. |
| 🧰 **Tools** | [`TOOLS_CANONICAL_13.md`](docs/60_REFERENCE/TOOLS_CANONICAL_13.md) | **The Surface:** The 14 canonical tools bridging the LLM to the Kernel. |
| 🚀 **Deploy** | [`DEPLOYMENT.md`](docs/60_REFERENCE/DEPLOYMENT.md) | **The Vanguard:** VPS setups, Docker, and Streamable HTTP scaling. |
| 🗺️ **Deploy Map** | [`DEPLOYMENT_MASTER.md`](docs/DEPLOYMENT_MASTER.md) | **The Traffic Control:** Which workflow deploys which public surface. |

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

| Level | Name | Scope | ARIF Band | Operational Role in the arifOS Stack |
|:---:|:---|:---|:---:|:---|
| **L7** | **AGI / Ecosystem** | Civilisation-Scale | — | *[Research]* Permissionless sovereignty and self-healing. |
| **L6** | **Institution** | Organisational | — | *[Experimental]* Trinity consensus for governing societies. |
| **L5** | **Agents** | Federation | **A R I F** | *[Active]* 5-role constitutional hypervisor enforcing no-bypass gates. |
| **L4** | **Tools (MCP)** | Production | **A R I F** | *[Active]* 14 MCP tools grouped into 4 ARIF cognitive bands. |
| **L3** | **Workflow** | Production | **A R I F** | *[Active]* 9 metabolic workflows assembling ARIF verbs into loops. |
| **L2** | **Skills** | Production | **A R I F** | *[Active]* 9 canonical verbs (A-CLIP) for behavioural primitives. |
| **L1** | **Prompts** | Production | — | *[Active]* Intent classification and reality centering. |
| **L0** | **KERNEL** | **SEALED** | — | *[Active]* The Immutable Core holding the 13 Floors and VAULT999. |

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
    A[A - ANCHOR] -- ignition --> R[R - REFLECT]
    R -- reasoning --> I[I - INTEGRATE]
    I -- context --> F[F - FORGE]
    F -- execute --> V[999 VAULT]
    
    subgraph 000-999 Loop
        A --> INIT[000]
        R --> THINK[333]
        I --> MAP[555]
        F --> SEAL[999]
    end
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
| **F6** | Empathy | **HARD** | **Who gets hurt?** Protects the weakest stakeholder. | Harm impact `κᵣ ≥ 0.70`. |
| **F7** | Humility | **HARD** | **Is the AI cocky?** Must preserve room to be wrong. | Uncertainty band `Ω₀ ∈ [0.03, 0.05]`. |
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

### 1. ARIF Bands at L4 (Tools)
L4_TOOLS exposes the Trinity kernel as 13 MCP tools, hardened into 4 bands. Clients only see tools; arifOS enforces bands and Floors behind the scenes.

| Band | Meaning | Tools (examples) | Primary Floors |
|:---:|---|---|---|
| **A** | **Anchor** | anchor_session, check_vital | F4, F11–F13 |
| **R** | **Reflect** | reason_mind, search_reality, vector_memory | F2, F4–F8 |
| **I** | **Integrate** | inspect_file, audit_rules | F1, F7, F10 |
| **F** | **Forge** | eureka_forge, apex_judge, seal_vault | F1, F8, F9, F13 |

### 2. The 5-Role Hypervisor (L5 Agents)
The constitutional parliament routes ARIF bands to specific roles:
- **Orchestrator**: Band A + Flow Routing.
- **Architect/Auditor**: Band R (Reflection) + Band I (Context Mapping).
- **Engineer**: Band R + Band F (Implementation - Non-destructive).
- **Validator**: Band F Apex (Final Judgment & Sealing).

---

## 🔌 The MCP Protocol & ARIF Tools (L4)

arifOS acts as an **MCP Server** (`arifos_aaa_mcp`). Rather than trusting an LLM, your IDE or Desktop client points its tool-calls at arifOS via the Model Context Protocol.

The server exposes **14 governed tools**. When an AI attempts to use a tool like `eureka_forge` to execute a shell command, it doesn't just run. The command is risk-classified (LOW / MODERATE / CRITICAL), dangerous operations require explicit `confirm_dangerous=True`, and the entire execution is wrapped in a 13-LAW governance envelope with audit logging. Only after `apex_judge` issues a signed `governance_token` can `seal_vault` commit the decision to the immutable ledger.

### 8 Metabolic Tools (Core Governance Chain)
*These 8 tools form the canonical `000 → 999` metabolic loop. Every governed action flows through this chain.*

| Tool | Plain English Function | Constitutional Stage |
|:--|:--|:--|
| `anchor_session` | 🚪 Starts a new session and checks security clearance. | 000 INIT |
| `reason_mind` | 🧠 Asks the AI to logically think through a problem. | 333 AGI Mind |
| `vector_memory` | 📚 BBB Vector Memory — geometric semantic retrieval (BGE + Qdrant). | 444-555 PHOENIX RECALL |
| `simulate_heart` | ❤️ Checks if a decision will harm any stakeholders. | 555 ASI Heart |
| `critique_thought` | ⚖️ Forces the AI to argue against its own idea to find flaws. | 666 ASI Heart |
| `eureka_forge` | ⚒️ Executes shell commands with risk classification, audit logging, and human confirmation gates for dangerous operations. | 777 FORGE Actuator |
| `apex_judge` | 👑 Makes the final pass/fail ruling on whether an action is safe. | 888 APEX Soul |
| `seal_vault` | 🔒 Commits the decision to an immutable ledger. Requires a `governance_token` signed by `apex_judge` (Amanah Handshake) — no token, no entry. | 999 VAULT Memory |

### 5 Evidence Tools (Read-Only Inspection)
*These 5 tools provide evidence grounding without executing actions. They support the metabolic chain but do not modify state.*

| Tool | Plain English Function | Purpose |
|:--|:--|:--|
| `search_reality` | 🔍 Searches the web via Jina Reader (primary) to verify facts with clean Markdown extraction. Falls back to Perplexity → Brave. | F2 Truth verification |
| `fetch_content` | 📄 Extracts clean Markdown from URLs via Jina Reader (primary). F12 Defense: wraps content in untrusted envelope. | Evidence retrieval |
| `inspect_file` | 📁 Looks at files on your hard drive securely. | F1 Amanah audit |
| `audit_rules` | 📋 Checks the system's own safety rules. | Governance health check |
| `check_vital` | 📈 Checks if the server CPU/RAM is healthy. | System telemetry |

### 1 Governance UI Tool
| Tool | Plain English Function | Purpose |
|:--|:--|:--|
| `visualize_governance` | 🖥️ Opens the Constitutional Decision Visualizer — real-time dashboard for all 13 Floor scores, Tri-Witness consensus, thermodynamic telemetry, and VAULT999 verdict history. | Governance observability |

---

## 🔗 External Integrations

arifOS integrates with external services for **grounding, search, and content extraction** — always wrapped in constitutional enforcement (F2 Truth, F4 Clarity, F12 Defense).

### Search & Content Extraction (Priority Chain)

| Priority | Service | Purpose | API Key | Fallback |
|:---:|:---|:---|:---:|:---:|
| **1** | **Jina Reader** | Clean Markdown extraction from web pages. Superior content quality vs raw HTML. | `JINA_API_KEY` | — |
| **2** | **Perplexity AI** | Conversational search with citations. | `PERPLEXITY_API_KEY` | Jina |
| **3** | **Brave Search** | Privacy-focused web search. | `BRAVE_API_KEY` | Perplexity |

**Usage:**
```bash
# Optional: Set API keys for higher rate limits
export JINA_API_KEY="your-jina-key"        # https://jina.ai
export PERPLEXITY_API_KEY="your-px-key"    # https://perplexity.ai
export BRAVE_API_KEY="your-brave-key"      # https://brave.com/search/api/
```

**Constitutional Protection:**
- **F2 Truth**: All external content must have evidence URLs
- **F4 Clarity**: Jina Reader extracts clean Markdown (reduces entropy vs HTML)
- **F12 Defense**: External content wrapped in `<untrusted_external_data>` envelope with taint lineage

---

## 🚀 Developer Mental Model
When you call arifOS from an MCP client (Claude Desktop, Cursor, etc.):
1. **L1 Prompts**: Your intent is captured and classified.
2. **L2-L3 (Skills/Workflows)**: Decision on *what cognitive steps* to run.
3. **L4 (ARIF Tools)**: Actual MCP calls (search, fetch, forge, judge, seal).
4. **L5 Agents**: Enforce roles, preflight, and `888_HOLD` before any irreversible action.

---

## 🚀 How to Run It (The "How")

### Prerequisites
- **Python**: 3.12+ (We recommend `uv` as the package manager).
- **Environment**: Linux, macOS, or Windows WSL.
- **Database**: PostgreSQL is recommended for production `VAULT999`; local/dev can use SQLite/file fallback.

### 1. Local execution (`stdio` mode for Claude Desktop / Cursor)
```bash
# 1. Install arifOS
pip install arifos

# 2. Export required safety environment variables
# Preferred: single global profile at ~/.arifos/env (loaded automatically by runtime entrypoints)
# Fallback: local .env compatibility stub in repo root
# ⚠️ SECURITY: Generate strong secrets (rotate per deployment)
export ARIFOS_GOVERNANCE_SECRET=$(openssl rand -hex 32)
export DB_PASSWORD="your-strong-secret-here"  # Use vault in production
export DATABASE_URL="postgresql://arifos:${DB_PASSWORD}@localhost:5432/vault999"
# Optional: Enable ML SentenceTransformers for Empathy scoring (F5/F6/F9)
export ARIFOS_ML_FLOORS=1

# 🔐 PRODUCTION HARDENING CHECKLIST:
# - [ ] Store secrets in vault (HashiCorp Vault, AWS Secrets Manager)
# - [ ] Rotate secrets minimum every 90 days
# - [ ] Separate dev/prod credentials (NEVER reuse)
# - [ ] Enable DB audit logging
# - [ ] Use least-privilege DB user (not superuser)

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

**For ChatGPT Integrations (hardened split):**
Use the mode that matches your ChatGPT integration type.

1. **ChatGPT Apps / MCP mode (protocol-native):**
   - Start HTTP MCP: `HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http`
   - Connect MCP endpoint: `http://localhost:8080/mcp` (or your public `https://.../mcp`)

2. **Custom GPT Actions mode (REST/OpenAPI):**
   - OpenAPI import URL: `http://localhost:8080/openapi.json` (or `https://.../openapi.json`)
   - Primary action endpoint: `POST /checkpoint`
   - Health probe: `GET /health`
   - If `ARIFOS_API_KEY` is enabled, send `Authorization: Bearer <token>`

3. **CORS for ChatGPT web clients:**
   - Default allowed origins include `https://chat.openai.com` and `https://chatgpt.com`
   - Override with `ARIFOS_ALLOWED_ORIGINS` when running behind stricter policies

### 2. Production Execution (`http` streamable mode for VPS / Cloud)
Instead of two-channel SSE, arifOS uses the modern **Streamable HTTP** standard for robust cloud scalability behind Nginx proxies.
```bash
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http
```
*For complete VPS, Nginx, Docker, and Cloudflare scaling instructions, see [`DEPLOYMENT.md`](docs/60_REFERENCE/DEPLOYMENT.md).*

---

## 🎮 Constitutional Decision Visualizer (Production Deployed)

**Live MCP App + Standalone Dashboard for Real-Time Governance Monitoring**

The Constitutional Decision Visualizer is arifOS's **real-time control room** for monitoring the 13 Floors, Tri-Witness consensus, and thermodynamic vitality during decision processing. It is **production-deployed** and accessible via multiple platforms.

### Access Methods

1. **MCP App (Claude Web/Desktop)**  
   - Call the `visualize_governance` tool from any MCP client
   - Renders an interactive UI showing live governance telemetry
   - Resource URI: `ui://constitutional-visualizer/mcp-app.html`

2. **Standalone Dashboard (Web Browser)**  
   - **Local**: `http://localhost:8080/dashboard`  
   - **Production**: `https://dashboard.arifosmcp.arif-fazil.com`
   - No MCP client required - pure browser experience

### Real-Time Features

- **Live Floor Gauges**: Real-time visualization of all 13 Constitutional Floors (F1-F13) with thermodynamic visual language
- **Tri-Witness Radar (W³)**: Geometric consensus visualization between Human, AI, and Earth layers  
- **Thermodynamic Telemetry**: Live ΔS (entropy), Peace², κᵣ (empathy), and Ψ (vitality) monitoring
- **Metabolic Flow Trace**: Watch the `000 → 999` pipeline execute in real-time
- **Verdict History**: Browse past governance decisions from VAULT999

### API Endpoints

The visualizer consumes these production REST endpoints:
- `GET /api/governance-status` - Current session telemetry (ΔS, floors, verdict)
- `GET /api/governance-history` - Recent VAULT999 sessions

**Deployment Status**: ✅ **LIVE**

---

## 🛡️ Verification & Audit (The "Whatever/Proof")

**You don't have to blindly trust arifOS; you can independently verify it.**

Every thought, action, or tool call processed by arifOS is mathematically evaluated and sealed into append-only **`VAULT999`** ledger records (PostgreSQL in production, SQLite/file fallback in local/dev).

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

### 🔍 VAULT999 Ledger Fields (Independently Verifiable)
Every decision writes an immutable record with:
- `verdict` (SEAL/SABAR/VOID/HOLD/PARTIAL)
- `floor_scores` (F1-F13 computed values)
- `telemetry` (ΔS, Peace², κᵣ, G, Ω₀)
- `governance_token_hash` (HMAC signature, not the token itself)
- `session_id` + `parent_hash` (Merkle chain)
- `timestamp` (ISO8601 with timezone)
- `zkpc_proof` (Zero-knowledge proof of execution)

### 📊 The Truth Claim Dashboard
We continuously pipe live tests through the framework to prove its reliability. To see real-time integrity sweeps, anomalies, and structural proofs of the system:
**[View the Live Constitutional Audit Dashboard](https://arifosmcp-truth-claim.pages.dev)**

---

## 🔮 State of the Forge (The "When")

**Current Status:** Active Development / Production Ready L4.

- **Version:** 2026.3.1 (14 MCP tools live — Jina Reader integration, npm client verified, visualize_governance deployed).
- **ChatGPT Actions Surface:** `GET /openapi.json` + `POST /checkpoint` now live in runtime for Custom GPT Actions integration.
- **ChatGPT MCP Surface:** `POST /mcp` remains the protocol-native endpoint for MCP-capable hosts.
- **Jina Reader Integration:** `search_reality` and `fetch_content` now use Jina Reader as primary backend for clean Markdown extraction — superior content quality vs raw SERP APIs. Fallback chain: Jina → Perplexity → Brave.
- **npm/JS Client:** `@arifos/mcp` v0.1.0 verified across HTTP and stdio transports (see `packages/npm/arifos-mcp/`).
- **Constitutional Visualizer:** `visualize_governance` tool live — real-time dashboard for all 13 Floors, Tri-Witness, thermodynamic telemetry, and VAULT999 history.
- **Amanah Handshake:** `apex_judge` signs an HMAC-SHA256 `governance_token` that `seal_vault` must verify before any ledger write. No token = no entry. Tampered token = VOID.
- **F4 Clarity Hardened:** Hard floor — responses that increase entropy (`ΔS > 0`) return VOID, not PARTIAL.
- **Validation baseline:** canonical contract and Actions surface tests are enforced in `tests/canonical/`.

For a detailed multi-year roadmap, see [`ROADMAP.md`](docs/ROADMAP.md).

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
