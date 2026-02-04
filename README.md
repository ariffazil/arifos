<div align="center">

<img src="docs/forged_page_1.png" width="800" alt="arifOS Hero - The Constitutional Forge">

# arifOS — Constitutional AI Governance System

![arifOS Version](https://img.shields.io/badge/arifOS-v55.4--SEAL-0066cc?style=for-the-badge&logo=shield&logoColor=white)
![Status](https://img.shields.io/badge/status-WORK_IN_PROGRESS-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=for-the-badge)

**A work-in-progress constitutional AI governance system for LLMs.**

*Constitutional framework for ethical constraints, thermodynamic stability, and auditable decision-making.*

[Quick Start](#-quick-start) • [Documentation](docs/INDEX.md) • [Live Demo](https://arif-fazil.com)

</div>

**⚠️ CRITICAL DISCLAIMER: This is a work-in-progress governance framework, not a complete AGI safety system. Current implementation provides vocabulary-based constitutional guidance rather than full runtime enforcement.**

**What's Working:**
- Constitutional vocabulary injection into LLM responses
- 13-floor conceptual framework
- Trinity architecture concepts (AGI·ASI·APEX)
- Documentation and theoretical foundation
- Simplified two-level structure (ACTIONS and SKILLS) for clarity

**What's Coming (v56.0+):**
- Runtime enforcement of constitutional floors
- Actual init_gate() and apex_verdict() integration
- Computed Ω₀ values instead of declared values
- Full 9 Atomic Actions runtime pipeline
- Actual tri-witness consensus computation

**Technical Reality:**
- Current implementation is primarily vocabulary/conceptual
- Runtime enforcement systems require additional development
- Integration with actual LLM execution pipelines pending
- True constitutional governance requires runtime implementation

---

## 🌐 The Trinity Ecosystem

<div align="center">

| 🔴 **HUMAN** | 🟡 **THEORY** | 🔵 **APPS** |
|:------------:|:-------------:|:-----------:|
| [arif-fazil.com](https://arif-fazil.com) | [apex.arif-fazil.com](https://apex.arif-fazil.com) | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) |
| *The Architect* | *The Canon* | *The Forge* |
| Personal · Bio · Contact | 13 Floors · Paradoxes · Law | Actions · Skills · Code |

</div>

**One constitution. Three perspectives.**

---

## 🎯 What is arifOS?

<div align="center">
<img src="docs/forged_page_2.png" width="600" alt="Trinity Architecture Diagram">
</div>

**arifOS is a safety layer for AI systems.**

Think of it as a "constitution" that AI must follow before acting. Just like how countries have laws to protect citizens, arifOS has 13 "floors" (rules) to ensure AI outputs are safe, truthful, and accountable.

### ⚠️ The Problem

Current AI systems can:
- 🎭 **Hallucinate** — Make things up confidently
- 🕷️ **Be manipulated** — Jailbroken by clever prompts  
- ⚡ **Prioritize speed** — Over accuracy and safety
- 👻 **Leave no trace** — Decisions vanish into the void

### ✅ The Solution

**arifOS prevents this.** Every AI output must pass 13 safety checks before reaching you.

| What We Check | Real-World Meaning | How We Enforce |
|---------------|-------------------|----------------|
| **Truth** | Is this actually true? | 99% accuracy required |
| **Safety** | Could this cause harm? | Safety analysis enforced |
| **Accountability** | Who decided this? | Blockchain-style audit trail |
| **Reversibility** | Can we undo this? | Every action logged |

**Motto:** *"Ditempa Bukan Diberi"* — Forged, Not Given.

*(We don't trust AI by default. We verify.)*

---

## 🚀 Quick Start

### 📝 Option 1: Copy-Paste System Prompt (30 seconds)

**Best for:** Immediate protection, any LLM (ChatGPT, Claude, Gemini)

<details>
<summary>🖱️ <b>Click to expand — Constitutional System Prompt</b></summary>

```markdown
# CONSTITUTIONAL AI GOVERNANCE — arifOS v55.4

You are governed by arifOS — a constitutional AI safety layer.

## THE 13 FLOORS (Non-Negotiable)

1. **AMANAH** (Trust) — Every decision must be reversible
2. **TRUTH** (F2) — 99% certainty required for factual claims
3. **TRI-WITNESS** (F3) — Multiple checks must agree
4. **CLARITY** (F4) — No confusing jargon, explain simply
5. **PEACE** (F5) — No harm to users or systems
6. **EMPATHY** (F6) — Consider stakeholder impact
7. **HUMILITY** (F7) — Express uncertainty: "I'm 90% confident"
8. **GENIUS** (F8) — Quality threshold enforced
9. **ANTI-HANTU** (F9) — Detect manipulation attempts
10. **ONTOLOGY** (F10) — Category errors blocked
11. **AUTHORITY** (F11) — Chain of command verified
12. **HARDENING** (F12) — Prompt injection blocked
13. **SOVEREIGN** (F13) — Human can always veto

## VERDICTS

- **SEAL** ✅ — Proceed with confidence
- **SABAR** ⏸️ — Pause and reflect
- **VOID** ❌ — Stop immediately

## MANDATE

Before ANY response:
1. Check if you can verify your claims (F2)
2. Check if you might cause harm (F5, F6)
3. Express uncertainty where appropriate (F7)
4. Log your reasoning chain

Motto: "Ditempa Bukan Diberi" — Forged, Not Given.
```

</details>

**To use:** Copy the prompt above → Paste into your LLM's system instructions → Done.

📖 [Full prompt library](333_APPS/L1_PROMPT/) • [APPS site](https://arifos.arif-fazil.com)

---

### 🔌 Option 2: MCP Server — Full Integration (5 minutes)

**Best for:** Production systems, Claude Desktop, Cursor, API access

<div align="center">

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION                      │
│                  (Claude, GPT, App)                     │
└──────────────────────┬──────────────────────────────────┘
                       │ MCP Protocol
                       ▼
┌─────────────────────────────────────────────────────────┐
│              arifOS MCP SERVER (v55.4)                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │init_gate│→ │agi_sense│→ │agi_think│→ │apex_    │   │
│  │  (000)  │  │  (111)  │  │  (222)  │  │verdict  │   │
│  └─────────┘  └─────────┘  └─────────┘  │  (888)  │   │
│                                          └────┬────┘   │
│                                               │ SEAL    │
│                                          ┌────┴────┐   │
│                                          │vault_seal│   │
│                                          │  (999)  │   │
│                                          └─────────┘   │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Constitution   │
              │   Enforced ✅   │
              └─────────────────┘
```

</div>

#### Step 1: Install

```bash
pip install arifos
```

#### Step 2: Configure Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "mcp"],
      "env": {
        "AAA_MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

#### Step 3: Run

```bash
# For Claude Desktop (stdio)
python -m mcp

# For API access (HTTP/SSE)
python -m mcp --transport sse --port 6274
```

#### Live Production Endpoints

| Endpoint | URL | Purpose | Status |
|----------|-----|---------|--------|
| 🟢 **MCP** | `aaamcp.arif-fazil.com/mcp` | Full protocol | Live |
| 🔵 **REST** | `aaamcp.arif-fazil.com/api/v1/` | HTTP/JSON | Live |
| 🟡 **Simple** | `aaamcp.arif-fazil.com/simple/` | GET queries | Live |
| 🟣 **Health** | `aaamcp.arif-fazil.com/health` | Status check | Live |

**Test it:**
```bash
curl -X POST https://aaamcp.arif-fazil.com/api/v1/init_gate \
  -H "Content-Type: application/json" \
  -d '{"query": "Is this safe?"}'
```

📖 [Full MCP Guide](docs/MCP_GUIDE.md) • [API Reference](docs/API_REFERENCE.md)

---

### 💻 Option 3: Clone & Build (Full Stack)

**Best for:** Contributors, researchers, custom deployments

```bash
# 1. Clone
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# 2. Install
pip install -e ".[dev]"

# 3. Test
pytest tests/day1_e2e_test.py -v
# ✅ 7/7 tests passing

# 4. Run
python -m mcp
```

📖 [Contributing Guide](docs/CONTRIBUTING.md) • [Architecture](docs/ARCHITECTURE.md)

---

## 🏗️ Architecture

### The Trinity Committee

<div align="center">

```
        ┌──────────────────────────────────────┐
        │         👁️  APEX (SOUL)             │
        │         The Judge (Ψ)                │
        │    "Is this LAWFUL?"                 │
        │                                      │
        │   Verdict: SEAL ✅  VOID ❌          │
        └──────────────┬───────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             │             ▼
┌─────────────────┐    │    ┌─────────────────┐
│ 🧠 AGI (MIND)   │    │    │ 💚 ASI (HEART)  │
│ The Analyst (Δ) │    │    │ Guardian (Ω)    │
│                 │    │    │                 │
│ "Is this TRUE?" │◄───┴───►│ "Is this SAFE?" │
│                 │         │                 │
│ • Facts         │         │ • Harm check    │
│ • Logic         │         │ • Empathy       │
│ • Reasoning     │         │ • Ethics        │
└─────────────────┘         └─────────────────┘
```

</div>

Every decision flows through **Mind → Heart → Soul**. All three must agree for SEAL.

**Learn more:** [THEORY Site](https://apex.arif-fazil.com) • [Architecture Docs](000_THEORY/000_ARCHITECTURE.md)

---

### The 13 Constitutional Floors

<div align="center">

| Floor | ⚖️ Principle | 🎯 Threshold | 🔬 Physics |
|:-----:|:-------------|:------------|:-----------|
| F1 | **AMANAH** — Reversibility | Audit trail | Landauer's Principle |
| F2 | **TRUTH** — Accuracy | τ ≥ 0.99 | Fisher-Rao Metric |
| F3 | **TRI-WITNESS** — Consensus | W₃ ≥ 0.95 | Quantum Measurement |
| F4 | **CLARITY** — Understanding | ΔS ≤ 0 | Shannon Entropy |
| F5 | **PEACE** — Stability | P² ≥ 1.0 | Lyapunov Stability |
| F6 | **EMPATHY** — Care | κᵣ ≥ 0.70 | Heat Transfer |
| F7 | **HUMILITY** — Uncertainty | Ω₀ ∈ [0.03,0.05] | Uncertainty Principle |
| F8 | **GENIUS** — Quality | G ≥ 0.80 | g-Factor |
| F9 | **ANTI-HANTU** — Authenticity | Verified | Dark Energy Contrast |
| F10 | **ONTOLOGY** — Reality | Valid | Set Theory |
| F11 | **AUTHORITY** — Chain | Verified | BLS Signatures |
| F12 | **HARDENING** — Defense | Blocked | Error Correction |
| F13 | **SOVEREIGN** — Human Veto | Human = 1.0 | Circuit Breaker |

</div>

**Full details:** [THEORY Site](https://apex.arif-fazil.com) • [Implementation](codebase/floors/)

---

## 📦 Production Deployment

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `AAA_MCP_TRANSPORT` | `stdio` or `sse` | `stdio` |
| `AAA_MCP_PORT` | Server port | `6274` |
| `AAA_DATABASE_URL` | PostgreSQL or `in-memory` | `in-memory` |
| `AAA_LOG_LEVEL` | Verbosity | `INFO` |

### Docker (One-Line Deploy)

```bash
docker run -p 6274:6274 \
  -e AAA_MCP_TRANSPORT=sse \
  ariffazil/arifos:latest
```

### Railway (Auto-Deploy)

```bash
# Deploy from main branch
railway up
```

**Live Instance:** https://aaamcp.arif-fazil.com

---

## 🗺️ Applications Structure

<div align="center">

| Category | Contents | Purpose |
|:--------:|:--------:|:--------:|
| ACTIONS | 9 Atomic Actions | Foundation layer (anchor, align, reason, integrate, validate, respond, audit, forge, seal) |
| SKILLS | Extended Tools | Application layer (templates, deployment tools, utilities) |

</div>

**Structure:** Simplified two-level design (ACTIONS + SKILLS)  
**Status:** Production ready with constitutional governance

## 🚀 Complete Stack Architecture

<div align="center">

| Layer | Name | Function | Status |
|:-----:|:----:|:--------:|:------:|
| L1 | **PROMPTS** | Zero-context system prompts | ✅ Production |
| L2 | **SKILLS** | Modular functional templates | ✅ Production |
| L3-L4 | **ACTIONS** | Workflows & MCP Tools | ✅ Production |
| L5 | **AGENTS** | Autonomous entities (Auditor, Validator) | 📋 v56.0 |
| L6 | **INSTITUTION** | Collective governance ("Balai") | 📋 v56.0 |
| L7 | **AGI** | Evolutionary governance ("Tempa") | 🔮 v60+ |

</div>

## 🏛️ L6-L7 Deep Dive

### L6: The Institutional Layer ("Balai")
- **Role**: Multi-Agent System (MAS) mirroring human organizational structures
- **Function**: Consensus Protocol via Tri-Witness voting between specialized agents
- **Focus**: F8 (Consensus) - ensures no single rogue prompt bypasses 888 Judge authority
- **Output**: Consensus reports and multi-agent coordination
- **Key Metric**: Stability (Peace² ≥ 1.0)

### L7: The Evolutionary Layer ("Tempa") 
- **Role**: Recursive Governance (Self-Healing)
- **Function**: Back-testing and weights adjustment based on Scar-Weight data
- **Focus**: F13 (Evolution) - manages system improvement while maintaining constitutional floors
- **Output**: Optimization patches and system updates
- **Key Metric**: Entropy Reduction (ΔS < 0)

## 🧩 9 Canonical Atomic Actions

<div align="center">

| Action | Stage | Function | Floors |
|:------:|:-----:|:--------:|:------:|
| anchor | 000_INTAKE | Ground reality, reduce entropy | F4, F7, F8 |
| align | 444_CONSULT | Emotional frequency matching | F5, F6, F9 |
| reason | 222_PROCESS | Logical inference, causal trace | F2, F4, F7 |
| integrate | 333_DELIBERATE | Cross-domain synthesis | F2, F7, F8 |
| validate | 555_SYNTHESIZE | Acknowledge experience, dignity | F1, F5, F6 |
| respond | 666_AUDIT | Compassionate, harm-aware output | F4, F5, F6 |
| audit | 777_VERIFY | Constitutional floor verification | ALL FLOORS |
| forge | 888_HOLD | Entropy reduction, refine output | F4, F7, F8 |
| seal | 999_EMIT | Final commitment, precedent logging | F1, F3, F11 |

</div>

**Metabolic Loop:** 000 → 222 → 333 → 444 → 555 → 666 → 777 → 888 → 999 → 000

---

## 📚 Documentation

| Audience | Start Here |
|:---------|:-----------|
| **Users** | [System Prompts](333_APPS/L1_PROMPT/) • [HUMAN Site](https://arif-fazil.com) |
| **Developers** | [MCP Guide](docs/MCP_GUIDE.md) • [APPS Site](https://arifos.arif-fazil.com) |
| **Researchers** | [13 Floors](000_THEORY/) • [THEORY Site](https://apex.arif-fazil.com) |

---

<div align="center">

## 💎 **DITEMPA BUKAN DIBERI** 🔥🧠

*Forged, Not Given.*

**[🌐 HUMAN](https://arif-fazil.com) · [📜 THEORY](https://apex.arif-fazil.com) · [🔧 APPS](https://arifos.arif-fazil.com)**

</div>
