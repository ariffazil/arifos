<div align="center">

<img src="https://raw.githubusercontent.com/ariffazil/arifOS/main/sites/library/static/img/banner_sovereign.png" width="100%" alt="arifOS Banner">

# arifosmcp
### AI Governance System — Tame the Chaos, Keep Human Control

**[Website](https://arifosmcp.arif-fazil.com)** • **[Live Dashboard](https://arifosmcp.arif-fazil.com/dashboard)** • **[Documentation](https://arifos.arif-fazil.com)**

*Ditempa Bukan Diberi — Forged, Not Given*

[![Status](https://img.shields.io/badge/Status-Production%20Ready-00b894.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/health)
[![Release](https://img.shields.io/badge/Version-2026.03.13--FORGED-blue.svg?style=flat-square)](https://github.com/ariffazil/arifosmcp/releases)
[![Tools](https://img.shields.io/badge/Public%20Tools-12-success.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/tools)
[![License](https://img.shields.io/badge/License-AGPL%203.0-lightgrey.svg?style=flat-square)](./LICENSE)

</div>

## What is arifOS?

**The Short Version:**
arifOS is like a " constitution + immune system" for AI. It wraps around any AI model (GPT, Claude, local models) and forces it to follow rules before answering.

**The Problem It Solves:**
Raw AI models hallucinate, forget context, and have no memory of what they said yesterday. They're like smart interns with amnesia who confidently make things up. arifOS adds:
- ✅ **Memory** — remembers facts across sessions
- ✅ **Truth-checking** — verifies claims before speaking  
- ✅ **Safety limits** — stops dangerous actions
- ✅ **Human veto** — you have final say on irreversible decisions

**Real-World Analogy:**
> Think of a Transformer (GPT/Claude) as a powerful engine. arifOS is the chassis, brakes, and steering wheel. The engine provides horsepower, but arifOS decides if it's safe to drive.

---

## Quick Start (5 Minutes)

### 1. Connect to the Live Server

```bash
# Check if it's running
curl https://arifosmcp.arif-fazil.com/health

# View available tools
curl https://arifosmcp.arif-fazil.com/tools
```

### 2. Start a Session

```bash
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "init_anchor_state",
      "arguments": {
        "declared_name": "MyFirstSession"
      }
    }
  }'
```

**Response:**
```json
{
  "verdict": "SEAL",
  "session_id": "sess-abc123",
  "message": "Session established"
}
```

### 3. Ask It to Research Something

```bash
# Search the web with constitutional safeguards
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "reality_compass",
      "arguments": {
        "query": "latest renewable energy statistics 2026"
      }
    }
  }'
```

**What makes this special?** Instead of just giving you an answer, it returns:
- Where it found the info (source URLs)
- How confident it is (uncertainty score)
- Whether facts conflict between sources
- A verdict: SEAL (proceed), HOLD (needs your approval), or VOID (unsafe)

---

## The Four Horizons (Roadmap)

We built arifOS in phases. Here's where we are:

### ✅ Horizon 1: Zero-Entropy Kernel (LIVE NOW)
**Goal:** Make the system stable and honest
- **VOID Eradication:** Mechanical errors now return "HOLD" or "SABAR" (wait) instead of crashing with "VOID"
- **MGI Envelope:** Every response has 3 layers: Machine status → Governance verdict → Intelligence analysis
- **Entropy Score (ΔS):** System measures if it's adding confusion (bad) or reducing it (good)
- **3E Telemetry:** Exploration → Entropy → Eureka cycle enforced on all outputs
- **Tri-Witness (W3):** Consensus metric requiring Human × AI × Earth sources
- **HMAC Governance Tokens:** F11-compliant authentication (NOT JWT)
- **F12 Injection Scanner:** 14-regex pattern protection against prompt injection

**ΔS Status:** 0.37 → 0.05 (near-crystalline order)

**📊 Live Metrics:**
- `W3_SCORE` — Tri-Witness consensus histogram
- `HOLD_QUEUE_DEPTH` — Pending sovereign decisions
- `VOID_EVENTS` — Constitutional collapse counter (should be zero)

### 🔭 Horizon 2: Tri-Witness Reality Engine (Q2 2026)
**Goal:** Build permanent, verified memory
- **Qdrant Integration:** Automatically saves every verified fact to vector database
- **Cross-Session Memory:** Ask a question today, reference the answer in 6 months
- **Reality Dossier:** Shows you conflicting sources side-by-side

### 👑 Horizon 3: Sovereign Command Center (Q3 2026)
**Goal:** Visual control panel for governance
- **Real-time Dashboard:** See Ω₀ (uncertainty), ΔS (entropy), and G (genius) gauges
- **888_HOLD Pager:** Get phone alerts when AI hits ethical boundaries
- **1-Click Ratification:** Approve/deny waiting decisions from your phone

### 🌌 Horizon 4: Trinity Swarms (Q4 2026+)
**Goal:** Multiple AI agents working safely in parallel
- **Role-Bound Agents:** Architect (designs), Engineer (builds), Auditor (checks risks), Validator (verifies), Orchestrator (coordinates)
- **Agent-to-Agent Handoffs:** They pass verified evidence bundles, not rumors

---

## Key Concepts (In Plain English)

### The 13 Floors (F1-F13)
Think of these as "safety checks" that run before any AI action:

| Floor | Plain English | What It Does |
|-------|---------------|--------------|
| **F1 Amanah** | Trust | Can we undo this? If not, needs human approval |
| **F2 Truth** | Accuracy | Must be 99% confident before claiming facts |
| **F3 Witness** | Consensus | Needs 3 sources: Human + AI + Earth (external data) |
| **F4 Clarity** | Reduce Confusion | Output must be clearer than input (ΔS ≤ 0) |
| **F5 Peace²** | Safety | Safety margin must exceed risk |
| **F6 Empathy** | Care | Protect the weakest stakeholder |
| **F7 Humility** | Admit Uncertainty | Always leave 3-5% room for "I might be wrong" |
| **F8 Genius** | Smart Balance | Intelligence = Accuracy × Stability × Curiosity × Energy² |
| **F9 Anti-Hantu** | No Ghosts | AI cannot claim to have feelings/soul |
| **F10 Ontology** | Know Thyself | AI is a tool, not a person |
| **F11 Continuity** | Verify Identity | Must prove who you are before acting |
| **F12 Injection** | Anti-Hacking | Blocks attempts to trick the AI |
| **F13 Sovereign** | Human Wins | You can override any AI decision |

### The 3E Cycle (How AI Thinks Here)

Instead of "ask → answer," arifOS forces:

1. **Exploration** — Map what we don't know
2. **Entropy** — List uncertainties and conflicts honestly  
3. **Eureka** — Only then synthesize an answer

**Result:** The AI must show its work and admit confusion *before* sounding confident.

### The Metabolic Loop (000-999)

Every request flows through 11 stages:

```
000 INIT → 111 SENSE → 222 THINK → 333 REASON → 444 ALIGN 
→ 555 EMPATHY → 666 BRIDGE → 777 EUREKA → 888 JUDGE → 889 PROOF → 999 VAULT
```

- **000:** Check identity (F11)
- **111-333:** Think and research (AGI Mind)
- **555-666:** Check safety and ethics (ASI Heart)
- **888:** Final decision (APEX Soul)
- **999:** Save to immutable ledger

---

## What You Can Do With This

### For Developers
```python
# Connect from Python
from mcp import ClientSession

async with ClientSession("https://arifosmcp.arif-fazil.com/mcp") as session:
    # Initialize with constitutional safeguards
    result = await session.call_tool("init_anchor_state", {
        "declared_name": "MyApp"
    })
    
    # Search with automatic fact-checking
    evidence = await session.call_tool("reality_compass", {
        "query": "climate data 2026"
    })
```

### For Researchers
- **Verify Sources:** Every claim comes with URLs and confidence scores
- **Track Changes:** See how AI certainty evolves as it learns more
- **Conflict Detection:** Automatically flags when sources disagree

### For System Administrators
- **Health Monitoring:** `check_vital` gives real-time system status
- **Audit Trails:** Every decision is logged with cryptographic signatures
- **Emergency Stop:** `888_HOLD` pauses any operation for human review

---

## 🆕 What's New in FORGED-2026.03 (Grand Unified Technical Specification)

### VOID Memanjang Elimination
**Before:** Any error → VOID (even network timeouts!)  
**After:** Typed fault codes with proper verdicts

```python
# Mechanical faults → 888_HOLD (retryable)
classify_exception(httpx.TimeoutException())
# → FaultClassification(fault_code="TIMEOUT_EXCEEDED", verdict="888_HOLD")

# Constitutional faults only → VOID (terminal)
classify_exception(InjectionAttackDetected())
# → FaultClassification(fault_code="F12_INJECTION", verdict="VOID")
```

### 3E Intelligence Telemetry
Every tool response now includes:
- **Exploration**: What sources were consulted
- **Entropy**: What uncertainties remain  
- **Eureka**: What insights were synthesized

```json
{
  "three_e": {
    "exploration": {"sources_consulted": 5, "depth_level": 3},
    "entropy": {"uncertainty_index": 0.12, "contradiction_count": 1},
    "eureka": {"novelty_score": 0.85, "crystallisation_flag": true}
  }
}
```

### Tri-Witness Consensus (W3)
**Formula:** `W3 = (Human × AI × Earth)^(1/3)`

| W3 Score | Verdict | Meaning |
|----------|---------|---------|
| ≥ 0.95 | SEAL | All 3 witnesses agree |
| 0.75-0.94 | PARTIAL | 2/3 witnesses agree |
| 0.50-0.74 | SABAR | Wait for more evidence |
| < 0.50 | 888_HOLD | No consensus |

### Security Hardening
- **HMAC-SHA256 Tokens**: `header.claims.signature` (not JWT)
- **F12 Scanner**: 14 patterns block injection attacks
- **Merkle Vault**: RFC 6962 append-only audit ledger

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                         │
└───────────────────────┬─────────────────────────────────────┘
                        │ JSON-RPC / SSE
┌───────────────────────▼─────────────────────────────────────┐
│                  arifosmcp Server                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Machine   │  │  Governance  │  │  Intelligence    │   │
│  │  (Can it    │  │  (Should it  │  │  (3E Cycle)      │   │
│  │   run?)     │  │   proceed?)  │  │                  │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐    ┌──────────┐
   │ Qdrant  │    │  Brave   │    │ Browser- │
   │ (Memory)│    │  Search  │    │ less     │
   └─────────┘    └──────────┘    └──────────┘
```

---

## Live Tool Registry (12 Tools)

| Tool | What It Does |
|------|--------------|
| `arifOS_kernel` | Main reasoning engine with constitutional checks |
| `reality_compass` | Search web + verify facts |
| `reality_atlas` | Build knowledge graphs |
| `reality_dossier` | Show conflicts between sources |
| `init_anchor_state` | Start a governed session |
| `revoke_anchor_state` | End session securely |
| `check_vital` | System health check |
| `audit_rules` | View all 13 floors status |
| `session_memory` | Store/retrieve context |
| `verify_vault_ledger` | Check audit trail integrity |
| `open_apex_dashboard` | Launch visual dashboard |
| `search_reality` / `ingest_evidence` | Research aliases |

---

## Safety & Governance

**arifOS is built on three hard rules:**

1. **The AI admits when it's confused** (F7 Humility)
   - Every response includes `uncertainty_score` (0.03-0.05)
   - Cannot say "I'm certain" without evidence

2. **Dangerous actions pause for human approval** (F1 Amanah)
   - Delete operations, irreversible changes → `888_HOLD`
   - You get Telegram/email notification to approve/deny

3. **The system remembers and verifies** (F3 Tri-Witness)
   - Claims need 3 witnesses: Human + AI + External source
   - Disagreements are surfaced, not hidden

---

## Production Deployment

```bash
# Docker (recommended)
docker run -d \
  --name arifosmcp \
  -p 3000:3000 \
  -e ARIFOS_ENV=production \
  ariffazil/arifosmcp:latest

# Or run directly
python -m arifosmcp.runtime http
```

**Health Check:**
```bash
curl http://localhost:3000/health
# Expected: {"status": "SEALED", "verdict": "HEALTHY"}
```

---

## Documentation & Support

- **[Full Documentation](https://arifos.arif-fazil.com)** — Deep dive into theory
- **[API Reference](https://arifosmcp.arif-fazil.com/docs)** — Technical specs
- **[Dashboard](https://arifosmcp.arif-fazil.com/dashboard)** — Live metrics
- **[GitHub Issues](https://github.com/ariffazil/arifosmcp/issues)** — Bug reports

---

## Philosophy

> *"Raw intelligence is cheap, entropic, and dangerous. Governance physics makes it lawful."*

arifOS doesn't replace AI models. It **tames** them. It forces them to:
- Show their work
- Admit uncertainty  
- Verify facts
- Respect human sovereignty

**DITEMPA BUKAN DIBERI — Forged, Not Given.**

This system wasn't bought or copied. It was built line-by-line with constitutional intent.

---

## License

AGPL 3.0 — If you modify this, you must share your changes. Constitutional governance should be transparent.

---

**Last Updated:** 2026-03-13 | **Version:** 2026.03.13-FORGED | **Entropy (ΔS):** 0.05
