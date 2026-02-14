# arifOS v64.1-GAGI

<p align="center">
  <strong>Governance Middleware for AI Systems</strong><br>
  <em>From zero-context prompts to autonomous institutions</em><br><br>
  <a href="https://aaamcp.arif-fazil.com/health"><img src="https://img.shields.io/badge/status-LIVE-success" alt="Status"></a>
  <a href="https://pypi.org/project/arifos/"><img src="https://img.shields.io/badge/version-64.1--GAGI-blue" alt="Version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="License"></a>
</p>

**arifOS is governance middleware that sits between AI models and users, evaluating every response before it reaches a human. If a response fails safety checks, it's blocked—not sent with a warning.**

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

## Quickstart

```bash
# Install
pip install arifos

# Run local server
python -m aaa_mcp

# Or connect to live server
curl https://aaamcp.arif-fazil.com/health
```

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

arifOS scales from simple prompts to autonomous institutions:

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

| Layer | What It Does | Status |
|:---|:---|:---:|
| **L1 PROMPTS** | Copy `SYSTEM_PROMPT.md` to any AI → instant governance | ✅ |
| **L2 SKILLS** | 9 canonical actions mapped to kernel organs | ✅ |
| **L3 WORKFLOW** | Sequences: `000_INIT` → `888_COMMIT` → `999_SEAL` | ✅ |
| **L4 TOOLS** | Production MCP server with 6 constitutional tools | ✅ |
| **L5 AGENTS** | Multi-agent federation (Δ Architect, Ω Engineer, Ψ Auditor) | 🟡 |
| **L6 INSTITUTION** | Trinity consensus, Tri-Witness governance | 🔴 |
| **L7 AGI** | Recursive self-healing, F13 exploration | 📋 |

**Current:** L1-L4 hardened and live. L5-L7 roadmap for v56.0.

See [333_APPS/README.md](333_APPS/) for full stack details.

---

## The 6 Tools: Governance Loop

Every request runs through six tools in sequence:

| Tool | Stage | What It Measures | Fails If | Outcome |
|:---|:---:|:---|:---|:---:|
| **init_session** | 000 | Authentication, injection attacks | Invalid auth, adversarial input | SEAL/VOID |
| **agi_cognition** | 111-333 | Truth, clarity, humility, genius | Ω > 0.08, truth < 0.5 | VOID/SABAR |
| **asi_empathy** | 555-666 | Stakeholder impact, reversibility | Irreversible harm, vulnerable users | SABAR/VOID |
| **tri_witness** | 777 | Evidence from 3 sources | Human/AI/external disagree | SABAR |
| **apex_verdict** | 888 | Final judgment synthesis | Constitutional conflict | SEAL/VOID/SABAR |
| **vault_seal** | 999 | Immutable audit record | — | SEAL |

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
│   ├── tools/                 # Tool wrappers
│   ├── capabilities/          # Optional: web search, code analysis
│   └── vault/                 # Audit logging
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
├── tests/                     # Test suite
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

## META: Canonical Reconstruction

This README represents the **v64.1-GAGI** release following the AAA-ACTOR MASTER DIRECTIVE (2026-02-14):

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
