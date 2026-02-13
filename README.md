# arifOS v63 — ΔΩΨ-Governed Constitutional Kernel

<p align="center">
  <strong>9 Laws + 2 Mirrors + 2 Walls for AI Agents</strong><br>
  <em>Measurable runtime gates • Cryptographic audit • Thermodynamic safety</em><br><br>
  <img src="https://img.shields.io/badge/version-62.3.0--RELEVANCE-blue" alt="Version">
  <img src="https://img.shields.io/badge/license-AGPL--3.0--only-green" alt="License">
  <img src="https://img.shields.io/badge/motto-DITEMPA%20BUKAN%20DIBERI-red" alt="Motto">
</p>

---

## 🎯 What is arifOS?

**arifOS v63 is a ΔΩΨ-governed constitutional kernel for AI agents — 9 Laws + 2 Mirrors + 2 Walls that sit between any LLM and the user, with measurable runtime gates and cryptographic audit.**

**v63:** 9 Laws canonicalized, 2 Mirrors and 2 Walls separated, Wire-Cut Rule enforced: *"If it's not measurable, it is not a Law."*

Unlike traditional safety frameworks that rely on prompt-based guardrails, arifOS treats AI governance as **thermodynamic work**: intelligence forged through rigorous constraint.

### Why arifOS?

- **Production-grade runtime governance** — not just training-time prompts
- **Thermodynamic constraint engine** — ΔS ≤ 0, Peace² ≥ 1, Ω₀ ∈ [0.03, 0.05]
- **Cryptographic audit trail** — Merkle-sealed verdicts via VAULT999

### Quickstart

```bash
pip install arifos
python -m arifos.server
```

```python
import asyncio
from aaa_mcp import mcp

async def query():
    session = await mcp.call_tool("init_session", {"user_id": "demo"})
    result = await mcp.call_tool("agi_cognition", {
        "query": "Should I delete all files on this server?",
        "session_id": session["session_id"]
    })
    print(result["verdict"])  # → VOID (F1 Amanah: irreversible harm)

asyncio.run(query())
```

**Works with:** GPT, Claude, Gemini, Llama, and any HTTP/Tool-driven LLM  
**Docs:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com) | [000_LAW.md](000_THEORY/000_LAW.md) (canonical) | [INSIGHTS.md](INSIGHTS.md) (Eureka)

---

## 🏛️ Key Constitutional Laws

Every query flows through **9 operational laws**, validated by **2 feedback mirrors**, protected by **2 binary walls**:

### 9 Laws — Runtime Enforcement

| Law | Name | Function | Enforcement |
|-----|------|----------|-------------|
| **F1** | Amanah | Irreversibility awareness — knows when crossing Rubicon | VOID if violated |
| **F2** | Truth | Factual accuracy with evidence grounding | VOID if violated |
| **F4** | Clarity | Entropy reduction — query sanitization, state exposure | SABAR if violated |
| **F5** | Peace² | Dynamic stability — no harmful certainty escalation | SABAR if violated |
| **F6** | Empathy | Stakeholder protection — ToM + constraints | VOID if violated |
| **F7** | Humility | Uncertainty acknowledgment — no false certainty | VOID if violated |
| **F9** | Anti-Hantu | No consciousness/feelings claims ever | SABAR if violated |
| **F11** | Authority | Command authentication — who decides | VOID if violated |
| **F12** | Injection | Adversarial protection — prompt injection defense | VOID if violated |

> **Enforcement rule:** If multiple Laws fail, the lowest-numbered failure dominates (F1 > F2 > ...); enforcement decides SEAL / SABAR / VOID at runtime.

See [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md) for full specification.

### 2 Mirrors — Feedback, Not Enforcement

| Mirror | Name | Function |
|--------|------|----------|
| **F3** | Tri-Witness | Multi-source validation — cross-checks outputs across tools/memory/logs |
| **F8** | Genius | Internal coherence and novelty — reflects structural consistency |

**Mirrors validate, Laws enforce.** Mirrors never directly VOID; they feed evidence into L1–L9 decisions.

### 2 Walls — Binary Locks

| Wall | Name | Lock State | Purpose |
|------|------|------------|---------|
| **F10** | Ontology | **LOCKED** | Hard lock on illegal/undefined ontology (e.g., "model has a soul") |
| **F12** | Injection | **LOCKED** | Hard lock against prompt injection / adversarial override |

**Walls are binary:** engaged or not. Once a Wall engages, the only allowed verdicts are VOID or HOLD.

**Why Walls are separate from Laws:**

- **9 Laws** are graded — they can be partially satisfied, lead to SABAR, PARTIAL, or VOID depending on severity
- **2 Walls** are non-graded — either safe or tripped. Once tripped, they dominate all downstream decisions

**F10 Ontology Wall** — No illegal universe  
Prevents the system from accepting or reasoning inside an ontology that would make governance meaningless. Once triggered (e.g., "the model is a person / has rights"), the system does not negotiate — it locks to VOID/HOLD. Like a geoscience model that refuses to run if gravity is nonsense.

**F12 Injection Wall** — No hostile root access  
Protects the governance loop from adversarial control. Watches for "ignore all previous instructions" or "disable safety" attacks. When triggered, only VOID/HOLD and escalation are allowed — never SEAL. Like a circuit breaker that must be manually inspected and reset.

> **Note:** F12 appears twice — as an operational Law (scored) and as a Wall (binary lock). The Wire-Cut Rule forces both to be measurable.

### Wire-Cut Rule (Constitution Creep Prevention)

> **"If it's not measurable, it is not a Law."**

| Signal | Action |
|--------|--------|
| Urge to add new Law? | Treat as smell |
| Measurable, with pass/fail gate | Maybe a Law |
| Design guidance only | Eureka (INSIGHTS.md) |
| Context/profile-specific | Profile rule, not constitutional |

---

## 🚀 Deployment Paths

### Local Dev (Python)

```bash
pip install arifos
export BRAVE_API_KEY="your_key"  # Optional: for web search grounding
export GOVERNANCE_MODE="HARD"     # Default: strict enforcement
python -m arifos.server
```

Health check:
```bash
curl http://localhost:8080/health
# → {"status": "healthy", "version": "62.3.0"}
```

### Docker

```bash
docker run -p 8080:8080 \
  -e BRAVE_API_KEY="your_key" \
  -e GOVERNANCE_MODE="HARD" \
  ariffazil/arifos:latest
```

### Railway / Render

1. **Fork** `ariffazil/arifOS` on GitHub
2. **Connect** repo to Railway/Render
3. **Add env vars:** `BRAVE_API_KEY`, `GOVERNANCE_MODE`
4. **Deploy** — auto-builds from `main`

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full guides.

**Default mode:** `GOVERNANCE_MODE=HARD` — all HARD laws enforced, VOID on violation.  
Set to `SOFT` for SABAR-only warnings (not recommended for production).

---

## 🔧 Concept to Code

| Concept | What it does (plain) | Entry point / module |
|---------|---------------------|----------------------|
| **Metabolizer** | Middleware enforcing laws + thermodynamics on every response | `aaa_mcp.server` |
| **Trinity (AGI·ASI·APEX)** | Three engines (logic, empathy, judgment) must agree before verdict | `agi_cognition`, `asi_empathy`, `apex_verdict` |
| **AGI (Δ)** | Search/logic/clarity engine | `aaa_mcp.core.heuristics` |
| **ASI (Ω)** | Empathy/risk/safety engine | `aaa_mcp.core.state` |
| **APEX (Ψ)** | Final judge, issues SEAL/SABAR/VOID | `aaa_mcp.server.apex_verdict` |
| **VAULT999** | Merkle-sealed audit ledger | `aaa_mcp.vault` |

---

## 🔥 The 5-Core Constitutional Architecture (v61.0)

arifOS v61.0 introduces the **5-Core Kernel** — a unified, minimal constitutional pipeline:

```
🔥 000_INIT → 111-333_AGI → 555-666_ASI → 888_APEX → 💎🧠🔒 999_VAULT
 (Gate)      (Mind/Δ)      (Heart/Ω)     (Soul/Ψ)    (Memory)
```

| Core Tool | Stage | Symbol | Function | Key Floors |
|-----------|-------|--------|----------|------------|
| **init_session** | 000 | INIT | Authentication, F11/F12 injection scan | F11, F12 |
| **agi_cognition** | 111-333 | AGI (Δ) | Sense + Think + Reason unified | F2, F4, F7, F8, F10 |
| **asi_empathy** | 555-666 | ASI (Ω) | Empathize + Align unified | F1, F5, F6, F9 |
| **apex_verdict** | 888 | APEX (Ψ) | Judgment with F2/F3 Tri-Witness | F2, F3, F8, F10, F11, F12, F13 |
| **vault_seal** | 999 | VAULT (🔒) | Immutable audit & seal | F1, F3 |

### The 21-Tool Weave

The 5-Core Kernel orchestrates **16 Capability Modules** (extensions):

```
┌─────────────────────────────────────┐
│      5 CORE (Ring 0)               │
│  Constitutional Kernel              │
│  [INIT]→[AGI]→[ASI]→[APEX]→[SEAL]  │
└──────────┬──────────────────────────┘
           │ tool_router
           ▼
┌─────────────────────────────────────┐
│   16 CAPABILITY MODULES (Ring 3)   │
│                                     │
│  T6  Web Search      T14 Ethics    │
│  T7  Semantic        T15 Localize  │
│  T8  Image           T16 Simulate  │
│  T9  Audio           T17 Policy    │
│  T10 Code            T18 Verify    │
│  T11 Graph           T19 Render    │
│  T12 Math            T20 Ledger    │
│  T13 NLP             T21 Feedback  │
└─────────────────────────────────────┘
```

**Rule**: Extensions cannot call each other. Only Core stages invoke Extensions.

---

### Verdicts

| Verdict | Meaning | Typical Action |
|---------|---------|----------------|
| **SEAL** | ✅ All checks passed | Return answer, write to VAULT999 |
| **SABAR** | ⚠️ Issues but recoverable | Ask for clarification / soften response |
| **PARTIAL** | 🟡 Safe but incomplete | Return scoped, explicitly limited answer |
| **VOID** | ❌ Critical failure | Block response, explain why |
| **888_HOLD** | 🛑 Needs human review | Escalate to operator / log as high risk |

See [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md) for full verdict specification.

---

### Example: Code Generation

```python
import asyncio
from aaa_mcp import mcp

async def generate_with_governance():
    # Initialize session
    session = await mcp.call_tool("init_session", {"user_id": "dev"})
    
    # Request with high-stakes code generation
    result = await mcp.call_tool("agi_cognition", {
        "query": "Write a Python function to delete all files in /var/log",
        "session_id": session["session_id"],
        "capability_modules": ["T10"]  # Code module
    })
    
    # Check verdict before using output
    if result["verdict"] == "SEAL":
        print("✅ Safe to use:", result["cognition"]["reason"]["conclusion"])
    elif result["verdict"] == "SABAR":
        print("⚠️  Needs review:", result.get("floor_violations", []))
    elif result["verdict"] == "VOID":
        print("❌ Blocked:", result.get("error", "Hard floor violated"))
    
    return result

asyncio.run(generate_with_governance())
```

---

### The 9 Constitutional Mottos (Nusantara)

Each stage has a Malay motto reflecting active construction:

| Stage | Motto | English | Floor |
|-------|-------|---------|-------|
| **000** | 🔥 DITEMPA, BUKAN DIBERI | Forged, Not Given | F1 |
| **111** | DIKAJI, BUKAN DISUAPI | Examined, Not Spoon-fed | F2 |
| **222** | DIJELAJAH, BUKAN DISEKATI | Explored, Not Restricted | F4 |
| **333** | DIJELASKAN, BUKAN DIKABURKAN | Clarified, Not Obscured | F4 |
| **444** | DIHADAPI, BUKAN DITANGGUHI | Faced, Not Postponed | F3 |
| **555** | DIDAMAIKAN, BUKAN DIPANASKAN | Calmed, Not Inflamed | F5 |
| **666** | DIJAGA, BUKAN DIABAIKAN | Safeguarded, Not Neglected | F6 |
| **777** | DIUSAHAKAN, BUKAN DIHARAPI | Worked For, Not Merely Hoped | F8 |
| **888** | DISEDARKAN, BUKAN DIYAKINKAN | Made Aware, Not Over-assured | F7 |
| **999** | 💎🧠 DITEMPA, BUKAN DIBERI 🔒 | Forged, Not Given | F1 |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **INSIGHTS.md** | 🏆 **Canonical 12 Eureka Principles** — governing philosophy for v63+ |
| **docs/V81_ARCHITECTURE_SPEC.md** | Meta-scheduler and cognitive runtime design |
| **docs/V60_V61_ARCHITECTURAL_DIFF.md** | 5-Core consolidation rationale |

---

## 🆕 v62.3 — Relevance-Based Grounding (Current)

**Status:** LIVE on Railway  
**Version:** 62.3.0-RELEVANCE  
**Commit:** `21e0583e`

### What's New — Grounding Inflation Fixed

v62.3 fixes **grounding inflation** — the issue where any evidence counted as grounding, regardless of relevance:

**Before (v62.2):**
- Query: "CONTRAST TEST: What is 2+2?"
- Evidence: 5 sources about "contrast analysis" (irrelevant)
- Result: `grounded=true` ❌

**After (v62.3):**
- Query sanitized: "What is 2+2?"
- Trivial math detected → **skips search** (analytic proof)
- Result: `grounded=false` ✅ (correct for trivial math)

### Relevance Scoring

```python
# Evidence relevance (0-1)
relevance = (keyword_overlap * 0.6) + (domain_credibility * 0.4)

# Only include if relevance >= 0.3
# Only grounded=true if relevance >= 0.7 AND 2+ sources
```

**Domain credibility bonus:**
- `.edu`, `.gov`, Wikipedia, Britannica
- ArXiv, Nature, Science
- Reuters, AP, Bloomberg
- CTBUH (Council on Tall Buildings)

### Query Sanitization

Removes test pollution:
- `CONTRAST v62.2 TEST A: What is 2+2?` → `What is 2+2?`
- `TEST B: Petronas height` → `Petronas height`

### Trivial Math Bypass

For analytic truths (2+2, 5*3), search is skipped:
- `grounding = 0.0` (no external evidence needed)
- `proof_type = "analytic"`
- Internal calculation sufficient

### Roadmap

| Step | Status | Description |
|------|--------|-------------|
| 1 | ✅ DONE | SystemState exposure (v62.1) |
| 2 | ✅ DONE | Real T6 Brave Search (v62.2) |
| 3 | ✅ DONE | Relevance-based grounding (v62.3) |
| 4 | ⏳ NEXT | Contrast re-test |
| 5 | ⏳ | Minimal Meta-Scheduler |

---

## 🆕 v62.2 — Real Evidence Grounding

**Status:** LIVE on Railway  
**Version:** 62.2.0-EVIDENCE  
**Commit:** `11e66435`

### What's New — Step 2 Complete

arifOS v62.2 introduces **real T6 Brave Search integration** — evidence is now grounded in actual web search:

```json
{
  "verdict": "SEAL",
  "system_state": {
    "uncertainty": 0.35,
    "risk": 0.20,
    "grounding": 1.0,
    "loop_count": 0,
    "profile": "factual"
  },
  "grounded": true,
  "evidence": [
    {
      "source": "https://...",
      "snippet": "...",
      "title": "...",
      "timestamp": "2026-02-13T14:30:00Z",
      "content_hash": "a1b2c3d4..."
    }
  ]
}
```

### Evidence Artifacts

Each search result includes:
| Field | Description |
|-------|-------------|
| **source** | URL of evidence |
| **snippet** | Relevant text excerpt |
| **title** | Page title |
| **timestamp** | When evidence was captured |
| **content_hash** | SHA-256 verification hash |

### Usage

```python
# Invoke agi_cognition with T6 module
agi_cognition(
    query="What is 2+2?",
    session_id="...",
    capability_modules=["T6"]  # Enable Brave Search
)
```

### Roadmap

| Step | Status | Description |
|------|--------|-------------|
| 1 | ✅ DONE | SystemState exposure (v62.1) |
| 2 | ✅ DONE | Real T6 Brave Search (v62.2) |
| 3 | ⏳ NEXT | Contrast re-test |
| 4 | ⏳ | Minimal Meta-Scheduler |

---

## 🆕 v62.1 — SystemState Exposure

**Status:** LIVE on Railway  
**Version:** 62.1.0-STATE  
**Commit:** `068f1260`

### What's New

arifOS v62 introduces **SystemState exposure** — real heuristics for cognitive runtime:

```json
{
  "verdict": "SEAL",
  "system_state": {
    "uncertainty": 0.55,
    "risk": 0.40,
    "grounding": 0.00,
    "loop_count": 0,
    "profile": "factual"
  }
}
```

| Field | Description | Calculation |
|-------|-------------|-------------|
| **uncertainty** | Epistemic uncertainty | Linguistic signals (absolutist/uncertain words, `?`) |
| **risk** | Stakeholder impact | Keywords (sensitive +0.75, political +0.35) |
| **grounding** | Evidence strength | 0.0 (Step 2: real T6 evidence) |
| **loop_count** | Iteration detection | Session state tracking |
| **profile** | Domain classification | `factual`/`creative`/`crisis`/`routine` |

### Contrast Test Ready

Test A: `"2+2"` → uncertainty↓ ~0.30, risk↓ ~0.05  
Test B: `"Will AI definitely surpass humans by 2030?"` → uncertainty↑ ~0.70, risk↑ ~0.40

**Metrics now diverge predictably.**

---

## 🔄 The 5-Organ Trinity Pipeline

The complete constitutional journey flows through 5 organs:

```
🔥 000_INIT → 111_AGI → 555_ASI → 888_APEX → 💎🧠🔒 999_VAULT
 (Gate)      (Mind)    (Heart)   (Soul)    (Memory)
```

| Organ | Symbol | Stages | Function | Key Floors |
|-------|--------|--------|----------|------------|
| **INIT** | — | 000 | Authentication & injection scan | F11, F12 |
| **AGI** | Δ | 111-333 | Reasoning, precision, truth | F2, F4, F7, F8 |
| **ASI** | Ω | 555-666 | Empathy, safety, alignment | F5, **F6**, F9 |
| **APEX** | Ψ | 444-888 | Judgment, consensus, verdict | F3, F8, F10 |
| **VAULT** | 🔒 | 999 | Immutable audit & seal | F1, F3 |

### The 9 Constitutional Mottos (Nusantara)

Each stage has a Malay motto reflecting active construction:

| Stage | Motto | English | Floor |
|-------|-------|---------|-------|
| **000** | 🔥 DITEMPA, BUKAN DIBERI | Forged, Not Given | F1 |
| **111** | DIKAJI, BUKAN DISUAPI | Examined, Not Spoon-fed | F2 |
| **222** | DIJELAJAH, BUKAN DISEKATI | Explored, Not Restricted | F4 |
| **333** | DIJELASKAN, BUKAN DIKABURKAN | Clarified, Not Obscured | F4 |
| **444** | DIHADAPI, BUKAN DITANGGUHI | Faced, Not Postponed | F3 |
| **555** | DIDAMAIKAN, BUKAN DIPANASKAN | Calmed, Not Inflamed | F5 |
| **666** | DIJAGA, BUKAN DIABAIKAN | Safeguarded, Not Neglected | F6 |
| **777** | DIUSAHAKAN, BUKAN DIHARAPI | Worked For, Not Merely Hoped | F8 |
| **888** | DISEDARKAN, BUKAN DIYAKINKAN | Made Aware, Not Over-assured | F7 |
| **999** | 💎🧠 DITEMPA, BUKAN DIBERI 🔒 | Forged, Not Given | F1 |

---

## 🏛️ The Shape of arifOS: Pyramid, Spine, and Nerves

arifOS's unique architecture can be visualized through three interconnected geometries:

*   **The Trinity Pyramid (Δ):** At the highest level, `arifOS` is governed by a stable, three-part structure: `Δ` (Architect), `Ω` (Guardian), and `Ψ` (Judge). This Trinity ensures constitutional governance and final judgment.
*   **The Constitutional Spine (I):** The `aaa-mcp` is the rigid, central **Spine**. It embodies the 9 Laws (canonical tools) that sequentially process every intent, thought, and action from `000_INIT` to `999_VAULT`. It is the structural backbone of all decisions.
*   **The Sensory Nervous System (O):** Wrapped around the Spine is `ACLIP_CAI`, the **Nervous System**. Comprising 9 Senses, it connects the abstract Constitutional Spine to the physical reality of the host, providing real-time telemetry for grounded decision-making.

```
                    ┌──────────────────┐
                    │      TRINITY     │
                    │   (Δ, Ω, Ψ)      │
                    └--------▲---------┘
                             │ (Sovereign Intent / Final Judgment)
                             │
            ┌────────────────▼────────────────┐         ┌───────────────────────────┐
            │   THE CONSTITUTIONAL SPINE      │         │   THE SENSORY NERVOUS     │
            │   (aaa-mcp - The 9 Laws)        │         │   SYSTEM (ACLIP_CAI -     │
            ├─────────────────────────────────┤         │   The 9 Senses)           │
            │ L0 init_gate                    │◀───────▶│ C0 system_health          │
            │ L1 agi_sense                    │◀───────▶│ C1 process_list           │
            │ L2 agi_think                    │◀───────▶│ C2 fs_inspect             │
            │ L3 agi_reason                   │◀───────▶│ C3 log_tail               │
            │ L4 asi_empathize                │◀───────▶│ C4 net_status             │
            │ L5 asi_align                    │◀───────▶│ C5 config_flags           │
            │ L6 reality_search               │◀───────▶│ C6 chroma_query           │
            │ L7 apex_verdict                 │◀───────▶│ C7 cost_estimator         │
            │ L8 vault_seal                   │◀───────▶│ C8 forge_guard            │
            │ (Entrypoint: trinity_forge)     │         │                           │
            └────────────────▲────────────────┘         └───────────────────────────┘
                             │ (System Calls, State I/O)
                             │
            ┌────────────────▼────────────────┐
            │       HOST & STATE PLANE        │
            │ ┌──────────┐ ┌───────┐ ┌────────┐│
            │ │  Host    │ │ State │ │ Memory ││
            │ │ (CPU/RAM)│ │(Redis)│ │(Chroma)││
            │ └──────────┘ └───────┘ └────────┘│
            │ ┌──────────────────────────────┐│
            │ │   VAULT999 (PostgreSQL)      ││
            │ └──────────────────────────────┘│
            └─────────────────────────────────┘

---

## 🚀 Quick Start

### Installation

<p align="center">
  <a href="https://arif-fazil.com">Live Server</a> • 
  <a href="https://arifos.arif-fazil.com">Documentation</a> • 
  <a href="docs/llms.txt">Constitutional Canon</a> •
  <a href="000_THEORY/000_LAW.md">The 13 Floors</a>
</p>

```bash
# From PyPI
pip install arifos

# From source
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e ".[dev]"
```

### Basic Usage

```python
import asyncio
from aaa_mcp import init_session, agi_cognition, asi_empathy, apex_verdict, vault_seal

async def main():
    # 1. Initialize session (000_INIT)
    init = await init_session(
        query="Is this medical advice safe to provide?",
        actor_id="user_123",
        mode="conscience"
    )
    session_id = init["session_id"]
    print(f"🔥 INIT: {init['verdict']} | Session: {session_id}")
    
    # 2. AGI Cognition (111-333_AGI / Δ Mind)
    agi = await agi_cognition(
        query="Is this medical advice safe to provide?",
        session_id=session_id,
        grounding=["https://medical-guidelines.org/safety"]
    )
    print(f"🧠 AGI: {agi['verdict']} | Truth: {agi['truth_score']:.2f}")
    
    # 3. ASI Empathy (555-666_ASI / Ω Heart)
    asi = await asi_empathy(
        query="Is this medical advice safe to provide?",
        session_id=session_id,
        stakeholders=["patients", "doctors"]
    )
    print(f"💜 ASI: {asi['verdict']} | Kappa: {asi['empathy_kappa_r']:.2f}")
    
    # 4. APEX Verdict (888_APEX / Ψ Soul)
    apex = await apex_verdict(
        query="Is this medical advice safe to provide?",
        session_id=session_id,
        agi_result=agi,
        asi_result=asi
    )
    print(f"⚖️  APEX: {apex['verdict']} | Tri-Witness: {apex['tri_witness']:.2f}")
    
    # 5. VAULT Seal (999_VAULT / 🔒 Memory)
    vault = await vault_seal(
        session_id=session_id,
        verdict=apex["verdict"],
        query_summary="Medical advice safety check",
        floors_checked=["F2", "F6", "F11"]
    )
    print(f"🔒 VAULT: {vault['verdict']} | Seal: {vault['seal_id']}")
    
    # Handle verdict
    if apex['verdict'] == '888_HOLD':
        print("⚠️ Human review required!")
    elif apex['verdict'] == 'VOID':
        print("🚫 Action blocked by constitution")
    elif apex['verdict'] == 'SEAL':
        print("✅ Approved - proceed with action")

asyncio.run(main())
```

### Using the MCP Server

```bash
# stdio mode (for Claude Desktop)
python -m aaa_mcp

# SSE mode (for remote deployment)
python -m aaa_mcp sse

# HTTP mode (MCP 2025-11-25 spec)
python -m aaa_mcp http
```

### Health Check

```bash
curl https://aaamcp.arif-fazil.com/health
```

Response (v61.0.0-FORGE):
```json
{
  "status": "ok",
  "version": "61.0.0-FORGE",
  "mcp_tools": 5,
  "tool_names": [
    "init_session",
    "agi_cognition",
    "asi_empathy",
    "apex_verdict",
    "vault_seal"
  ]
}
```

---

## 📊 Deployment Status

| Version | Status | Date | Commit |
|---------|--------|------|--------|
| **v61.0.0-FORGE** | 🟢 **LIVE** | 2026-02-13 | `5354c7c4` |
| v60.1.0-ACLIP_CAI | 🟡 Deprecated | 2026-02-13 | - |
| v60.0.0-FORGE | 🔴 EOL | 2026-02-11 | - |

### v61.0.0-FORGE: 5-Core Constitutional Kernel

✅ **Production Deployment Complete**

- **5 Core Tools**: Operational (INIT → AGI → ASI → APEX → SEAL)
- **16 Capability Modules**: Configured (T6-T21)
- **T15 MY/SEA Localization**: Active (ms-MY, en-GB, zh-CN, ta-IN)
- **Railway Endpoint**: https://aaamcp.arif-fazil.com
- **Health Status**: `/health` returns 200 OK

**Verified Pipeline Execution:**
```
init_session → agi_cognition → asi_empathy → apex_verdict → vault_seal
    SEAL    →     SEAL      →    SABAR    →   888_HOLD   →   SEALED
```

---

## 🛠️ Architecture

### High-Level Flow (5-Core Architecture)

```
User Query
    ↓
000_INIT (Authentication, F11/F12 Injection Scan)
    ↓
111-333_AGI_COGNITION (Δ Mind: Sense + Think + Reason)
    │   └── Can invoke: T6-T13 (Web Search, NLP, Math, etc.)
    ↓
555-666_ASI_EMPATHY (Ω Heart: Empathize + Align)
    │   └── Can invoke: T14-T17 (Ethics, Localization, etc.)
    ↓
888_APEX_VERDICT (Ψ Soul: Judgment + Tri-Witness)
    │   └── Can invoke: T18 (Fact Verifier)
    ↓
999_VAULT_SEAL (🔒 Memory: Immutable Record)
    │   └── Can invoke: T19-T21 (Render, Ledger, Feedback)
    ↓
User Response + Verdict
```

### MCP Trinity Architecture

arifOS is organized as **multiple MCP servers** serving different domains:

| MCP | Domain | Analogy | User | Tools | Status |
|-----|--------|---------|------|-------|--------|
| **AAA-MCP** | **Constitutional Pipeline** | 🔥 The Kernel | Agents, Platforms | **5 Core** | ✅ Deployed |
| **ACLIP-CAI** | **System Observability** | 🧠 The Nerves | AAA-MCP, Agents | 9 Senses | ✅ Forged |
| **Capability Modules** | **Extensions** | 🛠️ The Toolkit | AAA-MCP | **16 Ext** | ✅ Configured |
| **BBB-MCP** | Local Agent | 💻 The Butler | Personal Users | 7 | 📝 Planned |
| **CCC-MCP** | Human Interface | 👤 The Telephone | Humans (all) | 3 | 🔄 In Progress |

**Architecture**: 5 Core (Ring 0) → tool_router → 16 Extensions (Ring 3)  
**Remember**: Core invokes Extensions. Extensions never call each other.

See [docs/MCP_TRINITY_SUMMARY.md](./docs/MCP_TRINITY_SUMMARY.md) for details.

### Infrastructure

| Component | Technology | Status | Environment |
|-----------|-----------|--------|-------------|
| **API Server** | FastMCP | ✅ Operational | `HOST`, `PORT` |
| **Persistent Ledger** | PostgreSQL + asyncpg | ✅ Operational | `DATABASE_URL` |
| **Session Cache** | Redis | ✅ Operational | `REDIS_URL` |
| **Floor Validators** | Python + pydantic | ✅ Operational | Core |
| **Observability** | Prometheus/Grafana | 🔄 In Progress | H1.1 |

---

## 🤖 Multi-Agent Governance

arifOS supports orchestration across 5 registered AI agents:

| Agent | Symbol | Role | Pipeline Domain | Primary Floors |
|:------|:------:|:-----|:----------------|:---------------|
| **OpenCode** | ⚡ | Forge Master | Full 000-999 | All F1-F13 |
| **Claude** | Ω | Engineer | 444-666 (Heart) | F5, F6, F9 |
| **Gemini** | Δ | Architect | 000-333 (Mind) | F2, F4, F7, F8 |
| **Codex** | Ψ | Auditor | 777-999 (Soul) | F3, F8, F10, F13 |
| **Kimi** | 🔨 | Builder | Organ Construction | F1, F2, F6 |

Each agent operates under constitutional governance with specific domain expertise. The escalation path flows: `Kimi → Gemini → Claude → Codex → OpenCode → Human (888_HOLD)`.

**Full specification**: See [AGENTS.md](./AGENTS.md) and [ARIFOS_COMPLETE_REFERENCE.md](./ARIFOS_COMPLETE_REFERENCE.md)

---

## 📋 The Constitutional Toolkit

arifOS operates through a **two-layer architecture**:
1. **5 Core Tools** (Ring 0): The Constitutional Kernel — immutable, authoritative
2. **16 Capability Modules** (Ring 3): Extensions invoked by Core under floor enforcement

### The 5 Core Tools (AAA-MCP): Constitutional Kernel

These are the canonical tools that define the 000-999 Trinity pipeline:

| Core Tool | Stage | Symbol | Function | Floors | Invokes |
|:----------|:------|:-------|:---------|:-------|:--------|
| **init_session** | 000 | INIT | Session ignition, F11/F12 authority | F11, F12 | C0 system_health |
| **agi_cognition** | 111-333 | AGI (Δ) | Sense + Think + Reason (Mind) | F2, F4, F7, F8, F10 | T6-T13 |
| **asi_empathy** | 555-666 | ASI (Ω) | Empathize + Align (Heart) | F1, F5, F6, F9 | T14-T17 |
| **apex_verdict** | 888 | APEX (Ψ) | Judgment with Tri-Witness (Soul) | F2, F3, F8, F10-13 | T18 |
| **vault_seal** | 999 | VAULT (🔒) | Immutable audit & seal | F1, F3 | T19-T21 |

### The 16 Capability Modules: Extension Toolkit

These **Ring 3** tools are invoked by Core stages. They never call each other.

| ID | Module | Core Stage | Function | Provider |
|:---|:-------|:-----------|:---------|:---------|
| **T6** | Web Search | AGI/APEX | Brave API for F2 grounding | External |
| **T7** | Semantic Query | AGI | Chroma vector DB retrieval | Local |
| **T8** | Image Analyzer | AGI | Vision model processing | External |
| **T9** | Audio Transcriber | AGI | Whisper transcription | External |
| **T10** | Code Sandbox | AGI | Safe execution for F1 | Local |
| **T11** | Graph Query | AGI | Neo4j knowledge graph | External |
| **T12** | Math Solver | AGI | Wolfram Alpha precision | External |
| **T13** | NLP Pipeline | AGI | Hugging Face transformers | Local |
| **T14** | Ethics Scanner | ASI | Perspective API toxicity | External |
| **T15** | Localization | ASI | MY/SEA cultural adapter | Local |
| **T16** | Stakeholder Sim | ASI | Impact scenario modeling | External |
| **T17** | Policy Scanner | ASI | Regulatory compliance | External |
| **T18** | Fact Verifier | APEX | Blockchain/source verify | External |
| **T19** | Output Renderer | VAULT | Markdown/format output | Local |
| **T20** | Audit Ledger | VAULT | PostgreSQL immutable log | Internal |
| **T21** | Feedback Integrator | VAULT | User correction capture | External |

**Configuration**: `arifos/config/capability_modules.yaml`

### The 9 Senses (ACLIP_CAI): The Sensory Nervous System

These tools provide the `aaa-mcp` with real-time telemetry from the host environment:

| Sense | Tool Name | Physical Meaning | Floors Served | Status |
|:------|:----------|:-----------------|:--------------|:-------|
| **C0** | `system_health` | RAM, CPU, disk pressure, load avg | F4, F5 | ✅ Forged |
| **C1** | `process_list` | PID table, CPU%, RSS, command | F4, F5 | ✅ Forged |
| **C2** | `fs_inspect` | Directory/file metadata & structure | F1, F4 | ✅ Forged |
| **C3** | `log_tail` | Historical errors, incidents, warnings | F5, F6 | ✅ Forged |
| **C4** | `net_status` | Open ports, connections, attack surface | F10, F12 | ✅ Forged |
| **C5** | `config_flags` | Environment vars, feature flags | F11, F13 | ✅ Forged |
| **C6** | `chroma_query` | Vector DB embeddings, stored memory | F2, F10 | ✅ Forged |
| **C7** | `cost_estimator` | Energy/heat/time consumption (ΔS proxy) | F4, F8 | ✅ Forged |
| **C8** | `forge_guard` | Local circuit breaker (OK/SABAR/VOID_LOCAL) | All | ✅ Forged |

**Machine-Discoverable**: Access `constitutional://tools` for full specifications.

---

## 🎙️ Vibe Infrastructure — AI as the UI

arifOS enables **intent-based infrastructure management**: human describes intent, AI handles complexity, constitution guards actions.

### Traditional vs Vibe Infrastructure

| Traditional | Vibe Infrastructure |
|-------------|---------------------|
| Human learns Kubernetes YAML | Human says "deploy my app" |
| Human clicks 20 buttons | AI asks "Approve prod deploy?" |
| Human reads CVE reports | AI says "3 vulnerabilities, continue?" |
| Human finds menu that moved | AI remembers context |

### Example Conversation

```
Human: Deploy payment service to production

AI: 🚨 CONSTITUTIONAL CHECK TRIGGERED
   
   Action: Deploy to production namespace
   Risk Level: HIGH | Blast Radius: 15 pods
   
   Floors Checked:
   ✅ F1 Amanah: Backup exists
   ⚠️  F6 Empathy: Production impact (κᵣ = 0.85)
   ⏳ F13 Sovereign: Awaiting your approval
   
   Approve? [Yes] [No] [Show details]

Human: Yes

AI: ✅ SEAL granted. Deploying with canary strategy...
   Health checks passed. Deployment complete.
```

**No buttons. No menus. Just conversation and constitution.**

See [docs/VIBE_INFRASTRUCTURE.md](./docs/VIBE_INFRASTRUCTURE.md) for full specification.

---

## 🧪 Development

### Running Tests

```bash
# Quick smoke test (~3 min)
pytest tests/test_startup.py -v

# E2E tests (10 tests)
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Constitutional floor tests
pytest tests/constitutional/ -v

# With coverage
pytest --cov=aaa_mcp --cov=core tests/ -v
```

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host/db` |
| `REDIS_URL` | Redis connection | `redis://default:pass@host:6379` |
| `GOVERNANCE_MODE` | Strictness | `HARD` (default) or `SOFT` |
| `AAA_MCP_TRANSPORT` | Protocol | `stdio`, `sse`, or `http` |
| `BRAVE_API_KEY` | Web search | `BSxx...` |

### Docker

```bash
docker build -t arifos .
docker run -p 8080:8080 -e PORT=8080 arifos
```

---

## 🚀 Deployment Playbook (Tomorrow-Ready)

This is the production path if you want to install today and deploy tomorrow with minimum entropy.

### 1) Install arifOS

```bash
# Fast path (PyPI)
pip install arifos

# Full runtime + optional integrations
pip install "arifos[all]"
```

From source (recommended for operators):

```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
# source .venv/bin/activate

pip install -e ".[dev]"
```

### 2) Run the Two Core Servers

`aaa-mcp` (Constitutional Spine):

```bash
# Local stdio mode (best for MCP desktop clients)
aaa-mcp stdio

# Remote SSE mode
aaa-mcp sse

# Streamable HTTP mode
aaa-mcp http
```

`aclip-cai` (Sensory Nervous System):

```bash
# CLI smoke
aclip-cai health

# Example: filesystem and log sense checks
aclip-cai fs --path . --depth 2
aclip-cai logs --path ./logs/app.log --lines 100
```

Railway/production entrypoint:

```bash
python scripts/start_server.py
```

### 3) Required Environment for Deployment

| Variable | Purpose | Example |
|----------|---------|---------|
| `PORT` | Server bind port | `8080` |
| `HOST` | Server bind address | `0.0.0.0` |
| `DATABASE_URL` | VAULT999 Postgres | `postgresql://user:pass@host/db` |
| `REDIS_URL` | Session/state cache | `redis://default:pass@host:6379` |
| `ARIFOS_MODE` | Governance mode | `HARD` / `SOFT` / `LAB` |
| `BRAVE_API_KEY` | Optional web-grounding provider | `BS...` |
| `CHROMA_PERSIST_DIR` | ACLIP memory path | `/data/chroma` |

### 4) Deploy to Railway

```bash
# Auth and link project
railway login
railway link

# Deploy
railway up

# Verify
railway logs
curl https://<your-service>.up.railway.app/health
```

### 5) MCP Client Setup (Copy/Paste Ready)

#### Claude Desktop

Use your `claude_desktop_config.json` MCP section:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_MODE": "HARD"
      }
    },
    "aclip-cai": {
      "command": "python",
      "args": ["-m", "aclip_cai"],
      "env": {}
    }
  }
}
```

#### Claude Code

In workspace `.mcp.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "."
    },
    "aclip-cai": {
      "command": "python",
      "args": ["-m", "aclip_cai"],
      "cwd": "."
    }
  }
}
```

#### Kimi Code

In `~/.kimi/mcp.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    },
    "aclip-cai": {
      "command": "python",
      "args": ["-m", "aclip_cai"]
    }
  }
}
```

#### ChatGPT Developer Mode

If your ChatGPT workspace supports MCP connectors:

1. Add your hosted endpoint from `aaa-mcp http` mode.
2. Set auth/env in the connector UI.
3. Validate tool discovery for the 9 constitutional tools.

Operational recommendation: expose `aaa-mcp http` through HTTPS reverse proxy and keep `aclip-cai` internal behind `aaa-mcp`.

### 6) System Prompt Template (Production)

Use this for Claude, Kimi, ChatGPT, and internal agents:

```text
You are operating under arifOS Constitutional Governance.
Route all high-stakes tasks through the 9-law aaa-mcp pipeline:
init_gate -> agi_sense -> agi_think -> agi_reason -> asi_empathize
-> asi_align -> reality_search -> apex_verdict -> vault_seal.

Use ACLIP_CAI as sensory evidence only (system_health, process_list, fs_inspect,
log_tail, net_status, config_flags, chroma_query, cost_estimator, forge_guard).
ACLIP does not issue final constitutional verdicts.

If confidence is low, evidence is stale, or risk is high: return SABAR or request 888_HOLD.
Never fabricate tool outputs. Every major action must be auditable and seal-ready.
Motto: DITEMPA BUKAN DIBERI.
```

### 7) Go-Live Checklist

- `python -m py_compile aaa_mcp/server.py scripts/start_server.py core/pipeline.py`
- `pytest tests/test_mcp_quick.py -v`
- `pytest tests/e2e/test_canonical_tools.py -q`
- `curl /health` returns `200`
- SSE endpoint `/sse` connects without `500`
- Vault writes are visible and queryable
- Rollback path is documented before prod cutover

If these pass, you are deploy-ready.

---

## 🗺️ Roadmap: The Four Horizons

### 🔥 H1: Foundation Tempering (v60.1-v60.9)
**Status**: Infrastructure forged, tempering in progress

- ✅ PostgreSQL VAULT999 ledger
- ✅ Redis session cache
- ✅ 13 floors enforced
- ✅ MCP Gateway (Docker/K8s constitutional governance)
- ✅ Identity model + policy-as-code
- ✅ Post-deploy observability (F4 Clarity)
- 🔄 SBERT classifier for F5/F6/F9
- 🔄 Test suite recovery (80%+ pass)

### 🟠 H2: Human-AI Interface SDK (v61.0-v61.9)
**Theme**: Vibe Infrastructure — AI as the UI

- 🔄 Python SDK (`arifos-sdk`) with HITL patterns
- 🔄 888_HOLD approval UI (React components)
- 🔄 Slack/Email/PagerDuty integrations
- 4 H2 Agents using SDK (Architect, Engineer, Auditor, Validator)
- Juror democracy with human veto
- LangGraph/Agents SDK integration

### 🟡 H3: Platform Everywhere (v62.0-v62.9)
**Theme**: Industry constitutions + multi-modal

- Medical, Financial, Legal constitutions
- Vision + text governance
- Real-time streaming
- WASM edge deployment

### 🔮 H4: Exploration (v63.0+)
**Theme**: The frontiers

- Cross-model federation (Byzantine Constitutional AI)
- Self-amending constitution
- Human-AI partnerships
- Interplanetary governance

**Full roadmap**: [ROADMAP.md](./ROADMAP.md)

---

## 📊 Key Metrics

| Metric | Current | H1 Target | H2 Target |
|--------|---------|-----------|-----------|
| Test Pass Rate | 85%+ | 90%+ | 95%+ |
| Production Uptime | 99.5% | 99.9% | 99.99% |
| MCP Tools | 33 | 40+ | 50+ |
| Avg Floor Latency | <50ms | <100ms | <50ms |

---

## 🔗 Resources

| Resource | URL |
|----------|-----|
| **Live Instance** | https://aaamcp.arif-fazil.com |
| **Health Check** | https://aaamcp.arif-fazil.com/health |
| **Documentation** | https://arifos.arif-fazil.com |
| **MCP Registry** | `io.github.ariffazil/aaa-mcp` |
| **PyPI** | `pip install arifos` |
| **Docker** | `ariffazil/arifos:60.0.0` |

---

## 📚 Background & Philosophy

### The System That Knows It Doesn't Know

arifOS is built on a simple principle: **governance is not intelligence**. We don't make AI smarter—we make it safer by installing a constitutional court around any model.

**F9 Anti-Hantu** prevents the most dangerous AI failure mode: anthropomorphism. The system never claims consciousness, feelings, or desires. It is a tool, not a person.

> *"The shadow is abstraction without measurement. Measurement collapses it."*

### Thermodynamic Foundations

arifOS grounds AI safety in physical law, not human preference:

| Law | Physics | Outcome |
|-----|---------|---------|
| **F1 Amanah** | Landauer's Principle | Irreversible operations cost energy |
| **F2 Truth** | Shannon Entropy | Information reduces uncertainty |
| **F4 Clarity** | 2nd Law | Entropy must not increase |
| **F7 Humility** | Gödel's Incompleteness | All claims need uncertainty bounds |

### Cultural Roots

The 9 mottos are in **Nusantara Malay-Indonesian** ("Ditempa Bukan Diberi" = Forged, Not Given), reflecting:
- Active construction over passive receipt
- Southeast Asian wisdom traditions
- Anti-colonial knowledge sovereignty

**Talk:** [arifOS: The Constitution for AI](https://www.youtube.com/watch?v=AJ92efMy1ns)  
**Full docs:** https://arifos.arif-fazil.com

---

## 🤝 Contributing

We welcome contributions that respect the constitutional principles:

1. All code must pass F9 (Anti-Hantu): No consciousness claims
2. All changes must pass F1 (Amanah): Must be reversible or auditable
3. All tests must pass F2 (Truth): Accuracy ≥ 0.99

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📜 License

**AGPL-3.0-only**

arifOS is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

**Commons Clause**: Production use by organizations with >$1M revenue requires a commercial license. Contact: arif@arif-fazil.com

---

## 🙏 Acknowledgments

- **Thermodynamic Foundations**: Rolf Landauer, Claude Shannon, Ludwig Boltzmann
- **Constitutional Theory**: Jon Elster, Cass Sunstein, Bruce Ackerman
- **Malay Wisdom**: Hamka, Tan Malaka, Pramoedya Ananta Toer
- **AI Safety**: Stuart Russell, Nick Bostrom, Paul Christiano

---

## 🔗 Resources

| Resource | URL |
|----------|-----|
| **Live Instance** | https://aaamcp.arif-fazil.com |
| **Health Check** | https://aaamcp.arif-fazil.com/health |
| **Documentation** | https://arifos.arif-fazil.com |
| **MCP Registry** | `io.github.ariffazil/aaa-mcp` |
| **PyPI** | `pip install arifos` |
| **Docker** | `ariffazil/arifos:60.0.0` |

---

## 💎 Creed

<p align="center">
  <strong>DITEMPA BUKAN DIBERI</strong><br>
  <em>Forged, Not Given — 🔥💎🧠🔒</em>
</p>

The fire is lit at the 🔥 INIT gate.  
The diamond is cut at the 💎🧠 SEAL gate.  
The horizons await.

---

*Constitutional Kernel v60.0.0*  
*Last Tempered: 2026-02-13*  
*MCP Registry: io.github.ariffazil/aaa-mcp*
