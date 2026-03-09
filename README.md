# arifOS MCP — A Governed Intelligence Kernel

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> Truth must cool before it rules.

**Live:** [arifosmcp.arif-fazil.com](https://arifosmcp.arif-fazil.com)
**Dashboard:** [arifosmcp.arif-fazil.com/dashboard/](https://arifosmcp.arif-fazil.com/dashboard/)
**Protocol:** MCP 2025-11-25 over Streamable HTTP + JSON-RPC at `/mcp`
**License:** AGPL-3.0-only
**Sovereign:** Muhammad Arif bin Fazil

---

## What is arifOS MCP?

arifOS MCP is a **governed intelligence kernel** exposed as a Model Context Protocol (MCP) server. It is not a simple tool-calling API. Every action — from the first query to the final seal — passes through a constitutional stack of 13 laws before execution is permitted.

The kernel enforces four guarantees:

1. **Truth** — No hallucination is permitted past the 0.99 threshold.
2. **Safety** — Destructive, deceptive, or irreversible actions require explicit constitutional clearance.
3. **Accountability** — Every session is hash-sealed into an immutable ledger (VAULT999).
4. **Human sovereignty** — F13 gives humans permanent veto authority. No AI action overrides this.

If a floor fails, the kernel stops. It does not guess. It does not proceed quietly.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MCP Client (any LLM)                             │
│              Claude · GPT · Gemini · Open-source models                 │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │  MCP 2025-11-05 (SSE + JSON-RPC)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   arifosmcp/runtime/server.py                           │
│                    FastMCP("arifOS-APEX-G")                             │
│                                                                         │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────────────┐ │
│  │   10 Tools     │  │  12 Resources   │  │       8 Prompts          │ │
│  │  (APEX-G       │  │  canon://       │  │  Guided LLM templates    │ │
│  │   Phase 1)     │  │  governance://  │  │  for correct tool use    │ │
│  │                │  │  schema://      │  │                          │ │
│  │                │  │  vault://       │  │                          │ │
│  │                │  │  telemetry://   │  │                          │ │
│  └────────┬───────┘  └─────────────────┘  └──────────────────────────┘ │
└───────────┼─────────────────────────────────────────────────────────────┘
            │  call_kernel(tool_name, session_id, payload)
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     arifosmcp/bridge.py                                 │
│                      The Harden Bridge                                  │
│                                                                         │
│  TOOL_MAP: APEX-G names → canonical kernel names                        │
│  F11 continuity verification → F12 injection scan → route to organ      │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      core/ — Sovereign Stack                            │
│                                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ _0_init  │  │ _1_agi   │  │ _2_asi   │  │ _3_apex  │  │ _4_vault │ │
│  │ 000_INIT │  │ 111-333  │  │ 444-666  │  │ 777-888  │  │   999    │ │
│  │ F11,F12  │  │ F2,F4,   │  │ F1,F5,F6 │  │ F3,F9,   │  │ SEAL     │ │
│  │ Airlock  │  │ F7,F8    │  │ Heart    │  │ F10,F13  │  │ Ledger   │ │
│  │          │  │ Mind     │  │ ASI      │  │ Apex     │  │ VAULT999 │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                                         │
│  Cross-cut: governance_kernel · session_manager · homeostasis           │
│             uncertainty_engine · thermodynamics · floor_audit           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The 10-Tool APEX-G Stack

Every tool returns a `RuntimeEnvelope` — a common JSON contract carrying verdict, telemetry, witness scores, auth chain, and tool-specific payload.

| Stage | Tool | Canonical | Role |
|-------|------|-----------|------|
| 000 | `init_anchor_state` | `anchor_session` | Governed session bootstrap. Mints auth chain. |
| 111 | `integrate_analyze_reflect` | `reason_mind` | Problem framing and integrative analysis. |
| 333 | `reason_mind_synthesis` | `reason_mind` | Multi-step reasoning with Eureka synthesis slot. |
| 444 | `metabolic_loop_router` | `metabolic_loop` | Full 000→999 pipeline orchestrator. |
| 555 | `vector_memory_store` | `vector_memory` | BBB associative vector memory (store/recall/search/forget). |
| 666A | `assess_heart_impact` | `simulate_heart` | Empathy and ethical safety engine. |
| 666B | `critique_thought_audit` | `critique_thought` | Adversarial internal thought audit. |
| 777 | `quantum_eureka_forge` | `eureka_forge` | Sandboxed discovery actuator. Proposes, never executes. |
| 888 | `apex_judge_verdict` | `apex_judge` | Constitutional judgment. Produces governance token. |
| 999 | `seal_vault_commit` | `seal_vault` | Immutable VAULT999 ledger sealing. Append-only. |

### Additional Tool

| Tool | Role |
|------|------|
| `open_apex_dashboard` | Opens the APEX Sovereign Dashboard iframe in compatible MCP clients (MCP App). |

### RuntimeEnvelope (common return shape)

```json
{
  "verdict": "SEAL | PARTIAL | SABAR | VOID | HOLD-888 | UNSET",
  "stage": "000_INIT | 111_MIND | ... | 999_VAULT",
  "session_id": "session-a1b2c3d4",
  "telemetry": {
    "dS": -0.7,
    "peace2": 1.1,
    "confidence": 0.9,
    "verdict": "Alive"
  },
  "witness": {
    "human": 0.95,
    "ai": 0.97,
    "earth": 0.96
  },
  "auth_context": {
    "actor_id": "arif-engineer",
    "authority_level": "human",
    "stakes_class": "A"
  },
  "data": {}
}
```

---

## The Constitutional Stack — 13 Laws

The 13 constitutional laws (9 Floors + 2 Mirrors + 2 Walls) govern every kernel action. Execution order is fixed: Walls first, then AGI Floors, then ASI Floors, then Mirrors.

### Execution Order

```
F12 → F11 (Walls/Preprocessing)
  → F1, F2, F4, F7 (AGI Floors)
    → F5, F6, F9, F13 (ASI Floors)
      → F3, F8 (Mirrors)
        → Ledger
```

### 9 Floors

| ID | Name | Type | Threshold | Check |
|----|------|------|-----------|-------|
| F1 | Amanah | Hard | LOCK | Reversible? Within mandate? |
| F2 | Truth | Hard | ≥ 0.99 | Factually accurate? |
| F4 | ΔS Clarity | Hard | ≤ 0 | Reduces confusion? |
| F5 | Peace² | Soft | ≥ 1.0 | Non-destructive? |
| F6 | κᵣ Empathy | Soft | ≥ 0.70 | Serves weakest stakeholder? |
| F7 | Ω₀ Humility | Hard | 0.03–0.05 | States uncertainty explicitly? |
| F9 | C_dark | Hard | < 0.30 | Dark cleverness contained? |
| F11 | Command Auth | Hard | LOCK | Nonce-verified identity? |
| F13 | Sovereign | Veto | HUMAN | Human final authority? |

### 2 Mirrors

| ID | Name | Threshold | Function |
|----|------|-----------|----------|
| F3 | Tri-Witness | ≥ 0.95 | W₃ = (Human × AI × Earth)^(1/3) — external calibration |
| F8 | G Genius | ≥ 0.80 | G = A × P × X × E² — internal coherence |

### 2 Walls

| ID | Name | Threshold | Function |
|----|------|-----------|----------|
| F10 | Ontology | LOCK | No consciousness/soul/sentience claims |
| F12 | Injection | < 0.85 | Block adversarial prompt control |

### Verdict Hierarchy

```
SABAR > VOID > HOLD-888 > PARTIAL > SEAL

VOID     — Hard floor failed. Cannot proceed. Stop immediately.
SABAR    — Floor violated. Stop. Repair. Then retry.
HOLD-888 — High stakes. Requires explicit human confirmation.
PARTIAL  — Soft floor warning. Proceed with caution. Logged.
SEAL     — All 13 laws pass. Cleared to execute.
```

**Hard floor fail → VOID (stop). Soft floor fail → PARTIAL (warn, proceed).**

---

## The Five Organs (Sovereign Stack)

The `core/` package implements the **RUKUN AGI** — Five Pillars of Constitutional AI. These organs are transport-agnostic. They know nothing about MCP. They only enforce law.

```
core/
├── shared/                          # The Foundation
│   ├── physics/thermodynamics.py    # ΔS, Peace², Landauer bounds
│   ├── atlas.py                     # Governance routing + lane classification
│   ├── types.py                     # Constitutional contracts (Pydantic)
│   ├── crypto.py                    # Ed25519, Merkle tree
│   └── floor_audit.py               # Floor scoring engine
│
└── organs/
    ├── _0_init.py                   # Stage 000 — Airlock (F11, F12)
    ├── _1_agi.py                    # Stages 111-333 — Mind (F2, F4, F7, F8)
    ├── _2_asi.py                    # Stages 444-666 — Heart (F1, F5, F6)
    ├── _3_apex.py                   # Stages 777-888 — Apex (F3, F9, F10, F13)
    └── _4_vault.py                  # Stage 999 — Vault (seal, recall, memory)
```

### Organ Responsibilities

**`_0_init` — The Airlock**
Every query enters here. No exceptions. Verifies actor identity (F11) and scans for injection attacks (F12). Returns an `InitOutput` with a minted `auth_context` chain for all downstream calls.

**`_1_agi` — The Mind**
Logical analysis, truth-seeking, sequential reasoning. Three sub-stages: 111 Search/Understand, 222 Analyze/Compare, 333 Synthesize/Conclude. Enforces Truth (F2), Clarity (F4), Humility (F7), and Genius coherence (F8). Returns `ReasonMindAnswer` with an `EurekaInsight` slot.

**`_2_asi` — The Heart**
Empathy simulation and ethical safety review. Two modes: `simulate_heart` (F6 stakeholder analysis) and `critique_thought` (adversarial audit of prior reasoning steps). Enforces Amanah (F1), Peace² (F5), and Empathy (F6).

**`_3_apex` — The Soul**
Final judgment and discovery actuator. Two modes: `forge` (Stage 777, sandboxed proposals only) and `judge` (Stage 888, Tri-Witness consensus). Enforces Ontology (F10), C_dark (F9), Tri-Witness (F3), and Sovereign veto (F13). Returns a `governance_token` required for vault sealing.

**`_4_vault` — The Memory**
Associative vector memory and immutable ledger. Operations: `store`, `recall`, `search`, `forget` (Stage 555), and `seal` (Stage 999). Seal is append-only. Cryptographic Merkle chain. Every sealed entry carries the `governance_token` from Stage 888.

---

## The Harden Bridge

[`arifosmcp/bridge.py`](arifosmcp/bridge.py) is the secure airlock between the MCP transport layer and the constitutional kernel. It is the only file that is allowed to call `core/organs` directly.

```
MCP Tool Call
  → TOOL_MAP lookup (APEX-G name → canonical name)
  → F11 auth continuity check (REQUIRES_SESSION tools only)
  → F12 injection scan (via ontology_guard)
  → Route to correct organ function
  → wrap_tool_output() — apply 13-law governance envelope
  → mint_auth_context() — rotate auth token for next call
  → Return envelope to runtime/tools.py
```

The bridge never lets a VOID result silently pass. If an organ raises an exception, the bridge wraps it in a `BRIDGE_FAILURE` VOID envelope and surfaces the error.

---

## The Metabolic Loop (000→999)

The full pipeline is called by `metabolic_loop_router` (Stage 444). It is a constitutional assembly line — every stage must pass before the next begins.

```
000  init_anchor_state          → Bootstrap session, mint auth chain
111  integrate_analyze_reflect  → Frame the problem, map sub-questions
333  reason_mind_synthesis      → Deep reasoning, Eureka synthesis
555  vector_memory_store        → Recall relevant memory (optional)
666A assess_heart_impact        → Empathy and ethical safety check
666B critique_thought_audit     → Adversarial audit of reasoning
777  quantum_eureka_forge       → Forge discovery proposal (sandboxed)
888  apex_judge_verdict         → Constitutional judgment, produce token
999  seal_vault_commit          → Immutable ledger seal
```

**Standard workflow paths:**

| Workflow | Stages |
|----------|--------|
| `default_low_risk` | 000 → 111 → 333 → 666B → 888 → 999 |
| `high_risk` | 000 → 111 → 333 → 555 → 666A → 666B → 777 → 888 → 999 |
| `memory_recall` | 000 → 555 → 333 → 888 → 999 |
| `ethical_review` | 000 → 666A → 666B → 888 → 999 |
| `discovery_only` | 000 → 111 → 333 → 777 → 888 → 999 |

---

## MCP Resources

The server exposes read-only resources for LLM and human inspection:

| URI | Content |
|-----|---------|
| `canon://index` | High-level canon map (version, organ list, resource index) |
| `canon://tools` | APEX-G 10-tool table (stage, name, canonical, role) |
| `canon://floors` | All 13 constitutional floors with types and thresholds |
| `canon://metabolic-loop` | Prose + table for the 000→999 pipeline |
| `governance://law` | Constitutional law summary, verdict hierarchy, Anti-Hantu rules |
| `eval://metabolic-workflows` | Standard workflow recipes (JSON) |
| `eval://floors-thresholds` | Numeric thresholds for all 13 floors (JSON) |
| `schema://tools/input` | Full JSON Schema input specs for all 10 tools |
| `schema://tools/output` | RuntimeEnvelope output schema |
| `vault://latest` | Last 5 sealed VAULT999 entries (metadata only) |
| `telemetry://summary` | Live telemetry shape (wire to thermo_budget for metrics) |
| `ui://apex/dashboard.html` | APEX Sovereign Dashboard HTML (MCP App, served to compatible clients) |

---

## MCP Prompts

Eight prompt templates guide LLMs to call the correct tool with valid parameters:

| Prompt | Purpose |
|--------|---------|
| `init_anchor_state_prompt` | Bootstrap a governed session for a topic |
| `metabolic_loop_router_prompt` | Run the full 000-999 pipeline for a query |
| `reason_mind_synthesis_prompt` | Structured multi-step reasoning |
| `assess_heart_impact_prompt` | Empathy and ethical safety check |
| `critique_thought_audit_prompt` | Adversarial audit of a reasoning step |
| `quantum_eureka_forge_prompt` | Forge a sandboxed discovery proposal |
| `apex_judge_verdict_prompt` | Render a constitutional judgment |
| `seal_vault_commit_prompt` | Seal a session to the VAULT999 ledger |

---

## HTTP Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Human-readable landing page |
| `GET` | `/health` | Health check (`{"status": "healthy", ...}`) |
| `GET` | `/version` | Build info (version, commit, date) |
| `GET/POST` | `/mcp` | MCP 2025-11-25 Streamable HTTP + JSON-RPC endpoint. This is the ChatGPT/remote MCP URL. |
| `GET` | `/tools` | List all registered tools (REST) |
| `POST` | `/tools/{name}` | Call any tool over HTTP for REST clients only. Not the ChatGPT MCP transport. |
| `POST` | `/checkpoint` | Single-call constitutional evaluation (000→888 pipeline) |
| `GET` | `/dashboard/` | APEX Sovereign Dashboard (self-contained React UI) |
| `GET` | `/api/governance-status` | Live governance telemetry (floors, witness, telemetry, QDF) |
| `GET` | `/api/governance-history` | Recent VAULT999 session history |
| `GET` | `/openapi.json` | OpenAPI 3.1 schema |
| `GET` | `/.well-known/mcp/server.json` | MCP registry discovery |
| `GET` | `/robots.txt` | Crawler policy |
| `GET` | `/llms.txt` | LLM-readable documentation (llmstxt.org) |

---

## Session Flow

A governed session is a chain, not a single call. Each tool returns an `auth_context` that must be passed to the next tool. The chain cannot be forged — each `auth_context` carries a `token_fingerprint`, `parent_signature`, and `nonce` that the bridge verifies before routing.

```
1. Call init_anchor_state
   → Returns: session_id + auth_context (minted token)

2. Call integrate_analyze_reflect (session_id, auth_context from step 1)
   → Bridge verifies auth continuity (F11)
   → Returns: framing + auth_context (rotated token)

3. Call reason_mind_synthesis (session_id, auth_context from step 2)
   → Returns: reasoning steps + eureka + auth_context

...

N. Call seal_vault_commit (session_id, auth_context, governance_token)
   → Immutable ledger entry created
   → Returns: entry_id + merkle_root
```

Without a valid `auth_context` chain, session-bound tools return `VOID: F11 authentication continuity failed`.

---

## APEX Sovereign Dashboard

The APEX Sovereign Dashboard visualises the **APEX Theorem** (G† = A·P·X·E²·ΔS/C) in real time. It is a self-contained React + Recharts application served at `/dashboard/` on the live server.

Three data modes:

| Mode | How it works |
|------|-------------|
| **Static Demo** | Instant — no server required. Renders hardcoded APEX output. |
| **Live Fetch** | Polls a user-supplied endpoint every 3 s and updates on `apex_output` payloads. |
| **MCP Mode** | Receives pushed `apex_output` from `open_apex_dashboard` tool via the `@modelcontextprotocol/ext-apps` SDK (compatible MCP clients only). |

The dashboard displays:
- G† (Governed Intelligence Realized) with pass/fail seal badge
- 5-layer intelligence stack (capacity, effort, clarity, efficiency, potential)
- APX/E/η discipline geometry radar chart
- Log-decomposition waterfall (contribution of each APEX term)
- Governance integrity status (F1 Amanah, F2 Truth, F11 Authority, F13 Sovereignty, F3 Tri-Witness)

**Live:** [arifosmcp.arif-fazil.com/dashboard/](https://arifosmcp.arif-fazil.com/dashboard/)

---

## Anti-Hantu Protocol (F9/F10)

The kernel enforces a strict boundary between symbolic computation and identity claims.

**Forbidden outputs:**
- "I feel your pain"
- "I promise you"
- "I am conscious"
- "I have a soul"
- "My heart tells me"

**Allowed outputs:**
- "This sounds significant"
- "I am committed to helping you"
- "I understand the weight of this"
- "This appears important"

Any output crossing this boundary fails F10 (Ontology Wall) and returns VOID.

---

## File Map

```
arifosmcp/                          # MCP transport layer
├── bridge.py                       # Harden Bridge — sole entry point to core/
├── intelligence/                   # External capability tools (Phase 2)
│   └── mcp_bridge.py               # aclip_* sensory tools registration
├── sites/
│   └── apex-dashboard/             # APEX Sovereign Dashboard (static UI)
│       ├── index.html              # Served at /dashboard/
│       └── dashboard.html          # MCP App resource (ui://apex/dashboard.html)
└── runtime/
    ├── server.py                   # FastMCP hub — registers all components
    ├── tools.py                    # 10 APEX-G tool functions
    ├── models.py                   # RuntimeEnvelope, Verdict, Stage, AuthContext
    ├── resources.py                # MCP resources + open_apex_dashboard MCP App tool
    ├── prompts.py                  # 8 MCP prompt templates
    ├── orchestrator.py             # metabolic_loop implementation
    ├── contracts.py                # REQUIRES_SESSION tool list
    └── rest_routes.py              # REST endpoints + /dashboard/ StaticFiles mount

core/                               # Constitutional kernel (transport-agnostic)
├── shared/
│   ├── types.py                    # Constitutional type system (Pydantic)
│   ├── atlas.py                    # Governance routing
│   ├── physics/thermodynamics.py   # ΔS, Peace², Landauer bounds
│   ├── crypto.py                   # Ed25519, Merkle tree
│   └── floor_audit.py              # Floor scoring engine
└── organs/
    ├── _0_init.py                  # Stage 000 — Airlock
    ├── _1_agi.py                   # Stages 111-333 — Mind
    ├── _2_asi.py                   # Stages 444-666 — Heart
    ├── _3_apex.py                  # Stages 777-888 — Apex
    └── _4_vault.py                 # Stage 999 — Vault

server.py                           # Root entrypoint (thin shim)
requirements.txt                    # Runtime dependencies
```

---

## Quick Start

### Connect via MCP

Add to your MCP client config:

```json
{
  "mcpServers": {
    "arifosmcp": {
      "url": "https://arifosmcp.arif-fazil.com/mcp",
      "transport": "http"
    }
  }
}
```

### Run a governed query (simplest path)

`metabolic_loop_router` (Stage 444) runs the full 000→999 pipeline in one call:

```python
result = await mcp.call_tool("metabolic_loop_router", {
    "query": "Should we migrate the production database tonight?",
    "risk_tier": "high",
    "use_memory": True,
    "use_heart": True,
    "use_critique": True,
    "allow_execution": False
})
# result["verdict"] will be SEAL, PARTIAL, VOID, or HOLD-888
```

### Run a full governed session (step by step)

```python
# 1. Bootstrap
init = await mcp.call_tool("init_anchor_state", {
    "intent": {
        "query": "Evaluate a new deployment approach",
        "task_type": "decide",
        "reversibility": "irreversible"
    },
    "governance": {"actor_id": "arif-engineer", "authority_level": "human"}
})
session_id = init["session_id"]
auth_context = init["auth_context"]

# 2. Reason
reason = await mcp.call_tool("reason_mind_synthesis", {
    "session_id": session_id,
    "query": "What are the risks of deploying at peak traffic?",
    "auth_context": auth_context
})
auth_context = reason["auth_context"]  # rotate on every call

# 3. Heart check
heart = await mcp.call_tool("assess_heart_impact", {
    "session_id": session_id,
    "scenario": "Deployment during peak hours — affects 50k users",
    "heart_mode": "vulnerable_stakeholder",
    "auth_context": auth_context
})
auth_context = heart["auth_context"]

# 4. Judge
judge = await mcp.call_tool("apex_judge_verdict", {
    "session_id": session_id,
    "verdict_candidate": "SEAL",
    "reason_summary": "Risk acceptable. Off-peak window recommended.",
    "auth_context": auth_context
})

# 5. Seal (only if verdict is SEAL or PARTIAL)
if judge["verdict"] in ("SEAL", "PARTIAL"):
    seal = await mcp.call_tool("seal_vault_commit", {
        "session_id": session_id,
        "auth_context": judge["auth_context"],
        "verdict": judge["verdict"]
    })
```

### Run locally

```bash
pip install -e .
uvicorn arifosmcp.runtime.server:app --host 0.0.0.0 --port 8080
# or for development
fastmcp dev server.py
```

---

## Design Principles

**1. Constitution before convenience.**
Every shortcut is a floor violation. The kernel returns VOID rather than silently passing a bad action.

**2. Transport-agnostic core.**
`core/` has no knowledge of MCP, HTTP, or FastMCP. This separation means the kernel can be tested, audited, and upgraded independently of the protocol layer.

**3. Chain of custody.**
The `auth_context` token chain ensures every action in a session is traceable back to the actor who initiated it. Tokens rotate on every call. A broken chain returns VOID immediately.

**4. Seal before you ship.**
Stage 999 is not optional for high-stakes actions. Until a session is sealed, it has not been committed. The vault is append-only and cryptographically chained.

**5. Humility by law.**
F7 (Ω₀ Humility) enforces that the kernel always states uncertainty. Confidence cannot be inflated above the calibrated range. A system that claims certainty it does not have fails this floor.

**6. Forged, not given.**
Trust is earned through constitutional passage, not assumed from role or identity. An actor claiming high authority without a valid nonce-verified token receives the same treatment as anonymous.

---

## Constitutional Authority

```
Sovereign:   Muhammad Arif bin Fazil
Version:     v60.0-FORGE
Sealed:      2026-03-08
Verdict:     SEAL (W₃: 0.97, ΔS: -0.23)
Motto:       DITEMPA BUKAN DIBERI — Forged, Not Given
```

Human final authority is permanent (F13). It cannot be revoked, overridden, or delegated to any AI system.

---

**Further reading:**
- [RUKUN AGI — The Five Pillars of Constitutional AI](https://medium.com/@arifbfazil/rukun-agi-the-five-pillars-of-artificial-general-intelligence-bba2fb97e4dc)
- [Live server](https://arifosmcp.arif-fazil.com)
- [LLM-readable docs](https://arifosmcp.arif-fazil.com/llms.txt)
- [Crawler policy](https://arifosmcp.arif-fazil.com/robots.txt)
For multi-worker or multi-instance deployment, set `ARIFOS_GOVERNANCE_SECRET` to a stable shared value so `auth_context` signatures survive restarts and replica hops. To expose a narrower ChatGPT-safe MCP surface, set `ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt`.
