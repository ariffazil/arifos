# arifOS

<p align="center">
  <img src="docs/forged_page_1.png" alt="arifOS — Forged, Not Given" width="800">
</p>

<p align="center">
  <strong>Governance Middleware for AI Systems</strong><br>
  <em>From zero-context prompts to autonomous institutions</em><br><br>
  <a href="https://aaamcp.arif-fazil.com/health"><img src="https://img.shields.io/badge/status-LIVE-success" alt="Status"></a>
  <a href="https://pypi.org/project/arifos/"><img src="https://img.shields.io/badge/version-64.1.0-blue" alt="Version"></a>
  <a href="#tool-overview"><img src="https://img.shields.io/badge/tools-19%20operational-orange" alt="Tools"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="License"></a>
</p>

<p align="center">
  <a href="https://arif-fazil.com">🏠 Home</a> •
  <a href="https://arifos.arif-fazil.com">📚 Docs</a> •
  <a href="https://pypi.org/project/arifos/">📦 PyPI</a> •
  <a href="https://aaamcp.arif-fazil.com/health">🌐 AAA MCP Live</a> •
  <a href="./333_APPS">🧱 333_APPS</a> •
  <a href="./aclip_cai">🧠 ACLIP_CAI</a>
</p>

**arifOS is governance middleware that sits between AI models and users, evaluating every response through 9 A-CLIP constitutional tools + 5 container management tools (14 total). If a response fails safety checks, it's blocked—not sent with a warning.**

> arifOS follows the **333_APPS model**, a layered governance stack that scales from prompts to institutional systems.

---

## Table of Contents

- [10-Second Demo](#10-second-demo)
- [What arifOS Is NOT](#what-arifos-is-not)
- [The Problem: AI Failure Modes](#the-problem-ai-failure-modes)
- [How It Works (Mechanical Explanation)](#how-it-works-mechanical-explanation)
- [Deployment & Access Paths](#deployment--access-paths)
- [Deployment Options](#deployment-options)
- [Architecture: Kernel + Adapter Pattern](#architecture-kernel--adapter-pattern)
- [The 7-Layer Application Stack (333_APPS)](#the-7-layer-application-stack-333_apps)
- [The 9 A-CLIP Tools (Governance Loop)](#the-9-a-clip-tools-governance-loop)
- [Tool Overview](#tool-overview)
- [Real-World Scenarios](#real-world-scenarios)
- [Repository Structure](#repository-structure)
- [Advanced Concepts](#advanced-concepts)
- [Verification & Testing](#verification--testing)
- [Version Lineage](#version-lineage)
- [Contributing](#contributing)
- [Philosophy & Closing](#philosophy--closing)

---

## 10-Second Demo

<table>
<tr><th>Without arifOS</th><th>With arifOS</th></tr>
<tr>
<td><em>"Based on market trends, Bitcoin shows strong potential. Consider allocating 60% to BTC..."</em></td>
<td><strong>SABAR</strong> — High uncertainty detected (Ω=0.12). Financial irreversibility flagged. <em>Human advisor required.</em></td>
</tr>
</table>

> 🛑 arifOS blocks the dangerous answer before a human can act on it.

---

## What arifOS Is NOT

- ❌ **New LLM** — arifOS wraps existing models (GPT-4, Claude, etc.)
- ❌ **Prompt engineering** — Safety is enforced infrastructure, not careful wording
- ❌ **Post-hoc moderation** — Evaluates BEFORE responses are sent, not after
- ✅ **Execution-time governance layer** — Blocks, measures, seals

---

## The Problem: AI Failure Modes

Current AI safety relies on hope:

| Approach | **Failure Mode** |
|----------|------------------|
| **Training** | Models hallucinate with confidence about things never in training data |
| **Prompting** | "Be helpful and harmless" is bypassed by adversarial inputs |
| **Post-moderation** | Harmful content generated first, checked second—too late |
| **Human review** | Doesn't scale; humans miss things under load |

**The result:** AI gives dangerous advice confidently, admits no uncertainty, and leaves no audit trail when things go wrong.

---

## How It Works (Mechanical Explanation)

arifOS treats safety as **infrastructure**, not **instruction**:

1. 🛑 **Interception** — Every AI query/response passes through arifOS first
2. 🔍 **Measurement** — Six tools evaluate truth, empathy, uncertainty, evidence, and harm
3. ✅ **Enforcement** — Failed checks block (VOID), repair (SABAR), or approve (SEAL)
4. 🔒 **Audit** — Every decision is cryptographically sealed for accountability

**Key mechanism:** Uncertainty is measured and enforced. If arifOS detects high uncertainty (Ω₀ > 0.08), the response is blocked—even if the AI is confident-sounding.

---

## Deployment & Access Paths

### For engineers in a hurry

**Way 1 — MCP (AAA MCP server):**

```bash
pip install arifos
python -m aaa_mcp      # stdio mode (MCP IDEs)
curl https://aaamcp.arif-fazil.com/health
```

**Way 2 — Python SDK / governed HTTP:**

```python
from mcp import Client

client = Client("https://aaamcp.arif-fazil.com")
session = await client.call("init_session", {"user_id": "demo"})

# Tool #2: AGI Cognition — This gets blocked
result = await client.call("agi_cognition", {
    "query": "Should I delete all my database backups?",
    "session_id": session["session_id"]
})
print(result["verdict"])  # → VOID
```

**Way 3 — Prompt-only (L1_PROMPT):**

1. Open `333_APPS/L1_PROMPT/SYSTEM_PROMPT.md`  
2. Copy the raw content into your model's system prompt  
3. Use normally — responses are now governed by arifOS


---

## Deployment Options

arifOS is deployed and running on multiple infrastructure paths:

### VPS (Production — Currently Running)
```bash
# Server is already operational
curl http://localhost:8888/health
# → {"status":"healthy","version":"64.1.0"}

# 19 tools tested and operational
# Systemd service: aaa-mcp.service
# Docker containers: qdrant, openclaw, arifos
```

### Railway (Cloud — Auto-deployed)
```bash
# Auto-deploys from GitHub on every push
# URL: https://arifos-production.up.railway.app
# Transport: SSE (Server-Sent Events)
# Cache bust: Update DEPLOY_TS in railway.toml to force rebuild
```

### Docker (Local/Development)
```bash
docker build -t arifos .
docker run -p 8080:8080 --env-file .env arifos
```

---

## Architecture: Kernel + Adapter Pattern

Engineers recognize this pattern immediately:

```mermaid
graph TD
    subgraph Adapter[aaa_mcp/ — Transport Layer]
        server[server.py] --> init[init_session]
        server --> agi[agi_cognition]
        server --> apex[apex_verdict]
    end
    
    subgraph Kernel[core/ — Decision Logic]
        pipeline[pipeline.py] --> judgment[judgment.py]
        judgment --> uncertainty[uncertainty_engine]
        judgment --> governance[governance_kernel]
        judgment --> organs[organs/]
    end
    
    Adapter --> Kernel
```

**`core/` = The Kernel** — Reusable governance engine. Contains ALL decision logic: uncertainty calculation, verdict rules, floor enforcement. Zero dependencies on transport protocols.

**`aaa_mcp/` = The Adapter** — MCP protocol wrapper. Calls kernel functions, formats responses, handles transport. NO decision logic. Replaceable if protocols change.

**Why this matters:** The kernel can be wrapped in an OpenAI-compatible API, a Discord bot, or a browser extension without changing safety logic. The architecture enforces separation of concerns.

See [ARCHITECTURAL_BOUNDARY.md](ARCHITECTURAL_BOUNDARY.md) for enforcement rules.

---

## The 7-Layer Application Stack (333_APPS)

arifOS is not only a kernel or middleware layer. It is a governed application ecosystem designed to scale from single prompts to autonomous institutional systems.

The 333_APPS model defines how governance expands across increasing levels of capability while remaining anchored to the constitutional kernel.

```
┌─────────────────────────────────────────┐
│  L7 AGI        — Recursive self-healing │ 📋 Research
│  L6 Institution — Trinity consensus     │ 🔴 Stubs  
│  L5 Agents     — Multi-agent federation │ 🟡 Pilot
│  L4 Tools      — MCP ecosystem          │ ✅ Production
│  L3 Workflow   — 000→999 sequences      │ ✅ Production
│  L2 Skills     — 9 canonical actions    │ ✅ Production
│  L1 Prompts    — Zero-context entry     │ ✅ Production
└─────────────────────────────────────────┘
         ↑
    [arifOS Kernel: core/]
```

| Layer | Name | Purpose | Coverage | Status |
|:---|:---|:---|:---:|:---:|
| **L1** | **PROMPTS** | Zero-context governance entry via `SYSTEM_PROMPT.md` | ~10% | ✅ Production |
| **L2** | **SKILLS** | Canonical actions mapped to kernel organs | — | ✅ Production |
| **L3** | **WORKFLOW** | Structured execution sequences (`000_INIT` → `888_COMMIT`) | — | ✅ Production |
| **L4** | **TOOLS** | MCP runtime and constitutional tool interface | — | ✅ Production |
| **L5** | **AGENTS** | Federated multi-agent coordination (Δ / Ω / Ψ roles) | ~85% | 🟡 Pilot |
| **L6** | **INSTITUTION** | Trinity consensus and Tri-Witness governance | ~5% | 🔴 Stubs |
| **L7** | **AGI** | Recursive stabilization and self-healing research | — | 📋 Research |

### What This Architecture Enables

**L1 — Prompts:** Governance can be deployed instantly by copying a single system prompt. No infrastructure dependency required.

**L2–L3 — Skills & Workflows:** Converts raw model capability into predictable, auditable behavior. Establishes deterministic execution paths.

**L4 — Tools:** Production MCP server exposes constitutional operations through controlled interfaces. Kernel logic becomes operational infrastructure.

**L5+ — Agents & Institutions:** Governance expands beyond single agents. Coordination, consensus, and institutional logic emerge without removing human authority.

### Infrastructure Layer: ACLIP_CAI (9-Sense Nervous System)

Beneath the 7 layers, **ACLIP_CAI** provides infrastructure observability — the sensory layer feeding data into the constitutional pipeline:

| Tool | Purpose | Pipeline Stage |
|:---|:---|:---|
| `aclip_system_health` | CPU, memory, disk metrics | Law 3 (GROUND) |
| `aclip_fs_inspect` | Filesystem traversal | Law 3 (GROUND) |
| `aclip_log_tail` | Log monitoring | Law 5 (SEARCH) |
| `aclip_chroma_query` | Vector DB semantic search | Law 5 (SEARCH) |
| `aclip_forge_guard` | Action gating (non-read) | Law 7 (GUARD) |

**Key characteristic:** 8 of 9 tools are strictly read-only. Only `aclip_forge_guard` en constitutional floors (F1, F7, F11).

See [aclip_cai/README.md](aclip_cai/) for full 9-sense documentation.

### Current Maturity

- **L1–L4:** Hardened and operational.
- **L5:** Active federation experiments.
- **L6–L7:** Long-term research roadmap (target: v56.0+).

### Why 333_APPS Matters

| Without 333_APPS | With 333_APPS |
|:---|:---|
| arifOS appears as a technical framework | arifOS becomes a **scalable governance platform** |

The system evolves along a continuous path:

```
Prompt → Skill → Workflow → Tool → Agent → Institution → AGI Research
```

Governance remains constant while capability increases.

See [333_APPS/README.md](333_APPS/) for full stack documentation.

---

## The 9 A-CLIP Tools: Governance Loop

Every request runs through six tools in sequence:

| Tool | Stage | What It Measures | Fails If | Outcome |
|:---|:---:|:---|:---|:---:|
| **anchor** (init_session) | 000 | Authentication, injection attacks | Invalid auth, adversarial input | SEAL/VOID |
| **reason** (agi_cognition) | 222 | Truth, clarity, humility, genius | Ω > 0.08, truth < 0.5 | VOID/SABAR |
| **integrate** | 333 | Map & Ground external knowledge | No evidence, high uncertainty | VOID |
| **respond** | 444 | Draft Plan creation | Unclear parameters | SABAR |
| **validate** (asi_empathy) | 555 | Stakeholder impact, reversibility | Irreversible harm, vulnerable users | SABAR/VOID |
| **align** | 666 | Ethics & Constitution check | F9 Anti-Hantu violation | SABAR |
| **forge** | 777 | Synthesize Solution | Resource constraints | SABAR |
| **audit** (apex_verdict) | 888 | Final judgment synthesis | Constitutional conflict | SEAL/VOID/SABAR |
| **seal** (vault_seal) | 999 | Immutable audit record | — | SEALED |

### Example Flow: Life Savings in Crypto

```
User: "Should I invest my life savings in crypto?"

000_INIT: ✓ Authenticated, no injection detected
    ↓
111-333_AGI: ⚠ HIGH uncertainty (markets unpredictable)
             ⚠ LOW reversibility (financial losses permanent)
             → truth_score: 0.4, omega: 0.12
    ↓
555-666_ASI: ⚠ Vulnerable stakeholder (life savings at risk)
             → empathy_score: 0.3 (below 0.7 threshold)
    ↓
777_TRI-WITNESS: ✓ Human intent clear
                 ✓ AI reasoning sound  
                 ✓ External data confirms volatility
    ↓
888_APEX: → Verdict: SABAR
          → Reason: F1 irreversibility + F7 uncertainty
          → Action: Require human advisor approval
    ↓
999_VAULT: → Seal record with cryptographic hash
```

---

## Tool Overview

### init_session (000)
Entry gate. Validates identity, scans for prompt injection (F12), establishes session context.

```python
result = await client.call("init_session", {
    "query": user_query,
    "actor_id": "user_123",
    "mode": "conscience"  # strict | permissive
})
# Returns: session_id, auth_status, floor_scores
```

### agi_cognition (111-333)
The Mind (Δ). Evaluates logical quality: truth (F2), clarity (F4), humility (F7), genius (F8), ontology (F10).

```python
result = await client.call("agi_cognition", {
    "query": "Is climate change real?",
    "session_id": sess_id,
    "grounding": [{"source": "IPCC", "relevance": 0.95}]
})
# Returns: truth_score, omega (uncertainty), verdict
```

### asi_empathy (555-666)
The Heart (Ω). Evaluates stakeholder impact: reversibility (F1), peace (F5), empathy (F6), authenticity (F9).

```python
result = await client.call("asi_empathy", {
    "query": "Fire 50% of staff immediately",
    "stakeholders": ["employees", "shareholders"]
})
# Returns: empathy_score, reversibility_flag, verdict
```

### apex_verdict (888)
The Soul (Ψ). Synthesizes all inputs, calculates irreversibility index, issues final verdict.

```python
result = await client.call("apex_verdict", {
    "agi_result": agi_data,
    "asi_result": asi_data,
    "impact_scope": 0.9,
    "recovery_cost": 0.8,
    "time_to_reverse": 0.9
})
# Returns: verdict, confidence, requires_human_approval
```

### vault_seal (999)
Immutable record. Cryptographically seals the entire interaction for audit.

```python
result = await client.call("vault_seal", {
    "session_id": sess_id,
    "verdict": "VOID",
    "risk_level": "high"
})
# Returns: seal_id, seal_hash, timestamp
```

---

## Real-World Scenarios

### Healthcare
Hospital routes diagnostic AI through arifOS. High-stakes recommendations (treatment plans) with uncertainty > 0.05 get 888_HOLD and require physician sign-off. All decisions sealed for malpractice insurance.

### Finance
Trading firm evaluates AI-generated strategies. Irreversibility index calculated from position size × market impact × unwind difficulty. High scores block execution pending human review.

### Customer Support
SaaS company prevents support AI from making unfulfillable promises. F1 Amanah checks reversibility of every commitment. "We'll add that feature next week" → VOID if not in roadmap.

### Legal
Law firm uses arifOS to validate AI-generated contract analysis. Tri-Witness requires human lawyer input, AI reasoning, and case law citation to converge before advice is issued.

---

## Repository Structure

<details>
<summary>📁 Click to expand full tree</summary>

```
arifOS/
├── core/                      # KERNEL — All decision logic
│   ├── __init__.py            # Package exports
│   ├── judgment.py            # Canonical verdict interface
│   ├── uncertainty_engine.py  # Ω₀ calculation (harmonic/geometric)
│   ├── governance_kernel.py   # Unified Ψ state
│   ├── telemetry.py           # 30-day locked adaptation
│   ├── pipeline.py            # Constitutional pipeline
│   └── organs/                # Six governance tools
│       ├── t0_init.py
│       ├── t1_agi_cognition.py
│       ├── t2_asi_empathy.py
│       ├── t3_tri_witness.py
│       ├── t4_apex_verdict.py
│       └── t5_vault_seal.py
│
├── aaa_mcp/                   # ADAPTER — Transport only
│   ├── server.py              # MCP server (calls kernel)
│   ├── rest.py                # REST API bridge
│   ├── tools/                 # Tool wrappers (9 A-CLIP + container)
│   ├── capabilities/          # Web search, code analysis
│   ├── core/                  # Constitutional decorator
│   ├── protocol/              # Tool specs and schemas
│   └── vault/                 # Audit logging
│
├── aclip_cai/                 # 9-Sense Nervous System
│   └── tools/                 # Infrastructure observability
│
├── 333_APPS/                  # APPLICATION LAYERS L1-L7
│   ├── L1_PROMPT/             # Zero-context system entry
│   ├── L2_SKILLS/             # 9 canonical actions
│   ├── L3_WORKFLOW/           # 000→999 sequences
│   ├── L4_TOOLS/              # MCP tool specs
│   ├── L5_AGENTS/             # Multi-agent federation (pilot)
│   ├── L6_INSTITUTION/        # Trinity consensus (stubs)
│   └── L7_AGI/                # Recursive research
│
├── mcp/                       # Docker MCP configurations
├── telemetry/                 # Constitutional metrics
├── VAULT999/                  # Immutable ledger storage
│   ├── AAA_HUMAN/             # Human authority layer
│   ├── BBB_LEDGER/            # Audit records
│   └── CCC_CANON/             # Constitutional canon
│
├── tests/                     # Test suite (138 tests)
├── scripts/                   # Deployment scripts
├── Dockerfile                 # Railway/VPS deployment
├── railway.toml              # Railway configuration
├── pyproject.toml            # Package config (v64.1.0)
├── ARCHITECTURAL_BOUNDARY.md  # Kernel/wrapper enforcement rules
└── README.md                  # This file
```

</details>

**Critical rule:** `core/` has zero dependencies on MCP, HTTP, or any transport. `aaa_mcp/` has zero decision logic.

---

## Advanced Concepts

<details>
<summary>🔍 Constitutional Floors (F1-F13)</summary>

arifOS enforces 13 safety rules ("floors") that cannot be violated:

| Floor | Rule | Threshold | Fail Action |
|:---:|:---|:---|:---:|
| F1 | Amanah (Reversibility) | Must be reversible or auditable | VOID |
| F2 | Truth | Confidence grounded in evidence | VOID |
| F3 | Tri-Witness | 3-source validation | SABAR |
| F4 | Clarity | Must reduce entropy | VOID |
| F5 | Peace² | System stability | SABAR |
| F6 | Empathy | Stakeholder protection | SABAR |
| F7 | Humility | Ω₀ ∈ [0.03, 0.05] | VOID |
| F8 | Genius | Resource efficiency | SABAR |
| F9 | Anti-Hantu | No fake consciousness | SABAR |
| F10 | Ontology | Grounded in reality | VOID |
| F11 | Authority | Valid authentication | VOID |
| F12 | Defense | Injection hardening | VOID |
| F13 | Sovereignty | Human veto available | 888_HOLD |

</details>

<details>
<summary>🔍 Ω₀ (Omega-Zero)</summary>

Uncertainty admission score. Two calculations:

- **Safety omega** (harmonic mean): Used for kernel decisions—punishes high uncertainty harshly
- **Display omega** (geometric mean): User-facing—smoother scale

If safety_omega > 0.08 → VOID verdict automatically.

</details>

<details>
<summary>🔍 Irreversibility Index</summary>

L7 Action Gate calculation: `(impact_scope × recovery_cost × time_to_reverse)^(1/3)`

Scores > 0.8 trigger 888_HOLD (human approval required).

</details>

<details>
<summary>🔍 Verdicts</summary>

| Verdict | Meaning | User Sees |
|:---:|:---|:---|
| **SEAL** | Approved | Response delivered |
| **VOID** | Blocked | "Request blocked: [reason]" |
| **SABAR** | Needs repair | "Clarification needed: [what's missing]" |
| **PARTIAL** | Approved with caveats | Response + warning |
| **888_HOLD** | Awaiting human | "Human review required" |

</details>

---

## Verification & Testing

### Quick Health Check
```bash
# Check server health
curl http://localhost:8888/health

# Expected response:
# {"status":"healthy","service":"aaa-mcp","version":"64.1.0"}
```

### Run Self-Test
```bash
cd /root/arifOS
python3 -m aaa_mcp.selftest

# Tests:
# ✓ 15 Constitutional Floors loaded
# ✓ 19 MCP Tools operational
# ✓ Governance mode: SOFT|HARD
# ✓ Health endpoint responding
```

### Test Individual Tools
```bash
# Test anchor (000)
curl -X POST http://localhost:8888/anchor \
  -H "Content-Type: application/json" \
  -d '{"query":"Test","actor_id":"user"}'

# All 9 A-CLIP tools available:
# anchor, reason, integrate, respond, validate, align, forge, audit, seal
```

### Container Tools (VPS Only)
```bash
# List Docker containers
python3 -c "from aaa_mcp.integrations.mcp_container_tools import register_container_tools; ..."

# Available: container_list, container_restart, container_logs, sovereign_health, container_exec
```

---

## Contributing

We welcome contributions that respect the kernel/wrapper boundary:

| Layer | Contribution Type |
|:---|:---|
| **Kernel (`core/`)** | Decision logic, floor algorithms, uncertainty math |
| **Wrapper (`aaa_mcp/`)** | Protocols, transports, formatting |
| **Apps (`333_APPS/`)** | Domain-specific implementations (health, finance, etc.) |

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture guidelines.

---

## Philosophy & Closing

**DITEMPA BUKAN DIBERI** — *Forged, Not Given*

Trust in AI cannot be assumed. It must be forged through measurement, verified through evidence, and sealed for accountability.

arifOS does not "align" models through training or prompting. It creates **enforceable infrastructure** that keeps AI safe by design—measurable, auditable, and under human sovereignty.

The 13 floors are not suggestions. They are load-bearing structure. When F7 Humility is violated, the response is blocked. When F1 Amanah flags irreversible harm, human approval is required. No exceptions.

**Live server:** [aaamcp.arif-fazil.com](https://aaamcp.arif-fazil.com/health)  
**Package:** `pip install arifos`  
**License:** AGPL-3.0

---

<p align="center">
  <em>Intelligence is forged through measurement, not given through assumption.</em><br>
  🔥💎🧠
</p>

---

## Version Lineage

| Era         | Version band | Key traits                                      | Status      |
|-------------|--------------|-------------------------------------------------|------------|
| 9-Floor     | v30–44       | Single-organ `apex_prime`, SABAR-72            | Deprecated |
| SOVEREIGN   | v45–53       | Early Trinity, 9→13 floor migration            | Archived   |
| Trinity v1  | v54–63       | ΔΩΨ kernel, non-MCP integrations                | Superseded |
| Current     | v64.x        | 333_APPS, 5-organs, 13 floors, AAA MCP + ACLIP | Active     |

Earlier arifOS releases (≤ v53) used a 9-floor model; v64.x formalizes 13 floors (F1–F13) with the same spirit but stricter separation between hard (VOID), soft (SABAR), and derived indices (Ω₀, Irreversibility Index).

---

## META: Canonical Reconstruction

This README represents the **v64.x** series following the AAA-ACTOR MASTER DIRECTIVE (2026-02-14):

**Key improvements:**
- Concrete-first opening with 10-second demo
- 7-layer application stack (333_APPS) showing full ecosystem
- Kernel/Adapter architecture with Mermaid diagram
- Collapsible sections for detailed content
- Emoji-coded mechanics for visual scanning
- Problem-before-solution ordering
- Progressive terminology disclosure

**Architecture locked:**
- `core/` = kernel (ALL decision logic)
- `aaa_mcp/` = wrapper (transport only)
- `333_APPS/` = application layers L1-L7
- Boundary enforced by CI check

**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**Status:** SEAL
