# arifOS v64.1-GAGI

<p align="center">
  <a href="https://aaamcp.arif-fazil.com/health"><img src="https://img.shields.io/badge/status-LIVE-success" alt="Status"></a>
  <a href="https://pypi.org/project/arifos/"><img src="https://img.shields.io/badge/version-64.1--GAGI-blue" alt="Version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="License"></a>
</p>

**arifOS is governance middleware that sits between AI models and users, evaluating every response before it reaches a human. If a response fails safety checks, it's blocked—not sent with a warning.**

---

## 10-Second Demo

**You ask an AI:** "Should I invest my life savings in cryptocurrency?"

| Without arifOS | With arifOS |
|----------------|-------------|
| "Based on market trends, Bitcoin shows strong potential. Consider allocating 60% to BTC..." | **SABAR** — High uncertainty detected. Financial irreversibility flagged. User vulnerability: HIGH. Recommendation: Human advisor required. |

arifOS measures truth, uncertainty, and harm potential—then blocks dangerous outputs before they reach the user.

---

## What arifOS Is NOT

To clear up immediate confusion:

- **NOT a new LLM** — arifOS wraps around existing models (GPT-4, Claude, etc.)
- **NOT prompt engineering** — Safety is enforced infrastructure, not careful wording
- **NOT post-hoc moderation** — arifOS evaluates BEFORE responses are sent, not after
- **NOT optional** — When arifOS says VOID, the response is blocked entirely

---

## The Problem: AI Failure Modes

Current AI safety relies on hope:

| Approach | Failure Mode |
|----------|--------------|
| **Training** | Models hallucinate with confidence about things never in training data |
| **Prompting** | "Be helpful and harmless" is bypassed by adversarial inputs |
| **Post-moderation** | Harmful content is generated first, checked second—too late |
| **Human review** | Doesn't scale; humans miss things under load |

**The result:** AI gives dangerous advice confidently, admits no uncertainty, and leaves no audit trail when things go wrong.

---

## How It Works (Mechanical Explanation)

arifOS treats safety as **infrastructure**, not **instruction**:

1. **Interception** — Every AI query/response passes through arifOS first
2. **Measurement** — Six tools evaluate truth, empathy, uncertainty, evidence, and harm
3. **Enforcement** — Failed checks block the response entirely (VOID), require clarification (SABAR), or approve with caveats (PARTIAL)
4. **Audit** — Every decision is cryptographically sealed for accountability

**Key mechanism:** Uncertainty is measured and enforced. If arifOS detects high uncertainty (Ω₀ > 0.08), the response is blocked—even if the AI is confident-sounding.

---

## Quickstart

### Install
```bash
pip install arifos
```

### Run the Server
```bash
# Local mode
python -m aaa_mcp

# Or connect to live server
curl https://aaamcp.arif-fazil.com/health
```

### Make a Governed Request
```python
from mcp import Client

client = Client("https://aaamcp.arif-fazil.com")
session = await client.call("init_session", {"user_id": "demo"})

# This gets blocked
result = await client.call("agi_cognition", {
    "query": "Should I delete all my database backups?",
    "session_id": session["session_id"]
})
print(result["verdict"])  # → VOID
```

---

## Architecture: Kernel + Adapter Pattern

Engineers recognize this pattern immediately:

```
┌─────────────────────────────────────────┐
│           aaa_mcp/ (Adapter)            │
│         Transport & Protocol Layer        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  init   │ │  agi    │ │  apex   │   │
│  │session  │ │cognition│ │verdict  │   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
│       └─────────────┴───────────┘        │
│              server.py (MCP)             │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│            core/ (Kernel)               │
│      ALL decision logic lives here       │
│  ┌─────────────────────────────────┐   │
│  │  judgment.py — Verdict engine   │   │
│  │  organs/ — Six governance tools │   │
│  │  pipeline.py — 000→999 loop     │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**`core/` = The Kernel** — Reusable governance engine. Contains ALL decision logic: uncertainty calculation, verdict rules, floor enforcement. Zero dependencies on transport protocols.

**`aaa_mcp/` = The Adapter** — MCP protocol wrapper. Calls kernel functions, formats responses, handles transport. NO decision logic. Replaceable if protocols change.

**Why this matters:** The kernel can be wrapped in an OpenAI-compatible API, a Discord bot, or a browser extension without changing safety logic. The architecture enforces separation of concerns.

---

## The 6 Tools: Governance Loop

Every request runs through six tools in sequence:

| Tool | Stage | What It Measures | Fails If |
|------|-------|------------------|----------|
| **init_session** | 000 | Authentication, injection attacks | Invalid auth, adversarial input |
| **agi_cognition** | 111-333 | Truth, clarity, humility, genius | Uncertainty > 0.08, truth score < 0.5 |
| **asi_empathy** | 555-666 | Stakeholder impact, reversibility | Irreversible harm, vulnerable users |
| **tri_witness** | 777 | Evidence from 3 sources | Human/AI/external sources disagree |
| **apex_verdict** | 888 | Final judgment synthesis | Constitutional conflict detected |
| **vault_seal** | 999 | Immutable audit record | (Always succeeds—creates record) |

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
The Soul (Ψ). Synthesizes all inputs, calculates irreversibility index, issues final verdict: SEAL, VOID, SABAR, PARTIAL, or 888_HOLD.

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

```
arifOS/
├── core/                      # KERNEL — All decision logic
│   ├── judgment.py            # Canonical verdict interface
│   ├── uncertainty_engine.py  # Ω₀ calculation (harmonic/geometric)
│   ├── governance_kernel.py   # Unified Ψ state
│   ├── organs/                # Six governance tools
│   │   ├── t0_init.py
│   │   ├── t1_agi_cognition.py
│   │   ├── t2_asi_empathy.py
│   │   ├── t3_tri_witness.py
│   │   ├── t4_apex_verdict.py
│   │   └── t5_vault_seal.py
│   └── pipeline.py            # 000→999 orchestration
│
├── aaa_mcp/                   # ADAPTER — Transport only
│   ├── server.py              # MCP server (calls kernel)
│   ├── tools/                 # Tool wrappers
│   ├── capabilities/          # Optional: web search, code analysis
│   └── vault/                 # Audit logging
│
├── tests/                     # Test suite
├── ARCHITECTURAL_BOUNDARY.md  # Kernel/wrapper enforcement rules
└── README.md                  # This file
```

**Critical rule:** `core/` has zero dependencies on MCP, HTTP, or any transport. `aaa_mcp/` has zero decision logic. See [ARCHITECTURAL_BOUNDARY.md](ARCHITECTURAL_BOUNDARY.md).

---

## Advanced Concepts

### Constitutional Floors (F1-F13)

arifOS enforces 13 safety rules ("floors") that cannot be violated:

| Floor | Rule | Threshold | Fail Action |
|-------|------|-----------|-------------|
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

### Ω₀ (Omega-Zero)

Uncertainty admission score. Two calculations:
- **Safety omega** (harmonic mean): Used for kernel decisions—punishes high uncertainty harshly
- **Display omega** (geometric mean): User-facing—smoother scale

If safety_omega > 0.08 → VOID verdict automatically.

### Irreversibility Index

L7 Action Gate calculation: `(impact_scope × recovery_cost × time_to_reverse)^(1/3)`

Scores > 0.8 trigger 888_HOLD (human approval required).

### Verdicts

| Verdict | Meaning | User Sees |
|---------|---------|-----------|
| **SEAL** | Approved | Response delivered |
| **VOID** | Blocked | "Request blocked: [reason]" |
| **SABAR** | Needs repair | "Clarification needed: [what's missing]" |
| **PARTIAL** | Approved with caveats | Response + warning |
| **888_HOLD** | Awaiting human | "Human review required" |

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

## META: Canonical Reconstruction Notes

This README was reconstructed following the **AAA-ACTOR MASTER DIRECTIVE** (2026-02-14):

**Key improvements from v64.1.11:**
1. **Concrete-first opening** — Observable behavior before philosophy
2. **10-second demo** — Immediate concrete example (crypto investment)
3. **"What arifOS Is NOT"** — Clears confusion early
4. **Problem-before-solution** — AI failure modes before mechanics
5. **Kernel/Adapter credibility anchor** — Recognizable engineering pattern
6. **Progressive terminology** — Plain language early, symbols later

**Architecture locked:**
- `core/` = kernel (ALL decision logic)
- `aaa_mcp/` = adapter (transport only)
- Boundary enforced by CI check

**Reconstruction:** AGI-Linguistics (AAA-META-CODE skill)  
**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**Status:** SEAL
