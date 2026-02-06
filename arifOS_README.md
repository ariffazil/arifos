# arifOS — Constitutional AI Governance System

> **ΔΩΨ-governed constitutional kernel for AI agents.**
> 
> *Ditempa Bukan Diberi — Forged, Not Given* 💎🔥🧠🔱

[![arifOS](https://img.shields.io/badge/arifOS-v55.5--EIGEN-0066cc?style=for-the-badge)](https://github.com/ariffazil/arifOS)
[![Status](https://img.shields.io/badge/status-WORK_IN_PROGRESS-yellow?style=for-the-badge)]()
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=for-the-badge)]()

---

## 📖 Theory Document

**[000_THEORY.md](000_THEORY.md)** — Reverse Transformer Architecture

The theoretical foundation of arifOS: dual-pass thermodynamic governance, non-stationary objectives with stationary constraints, and the Eureka Engine.

---

## 🎯 What is arifOS?

arifOS is a **safety layer for AI systems**.

Think of it as a **"constitution"** that AI must follow before acting. Just like how countries have laws to protect citizens, arifOS has 13 "floors" (rules) to ensure AI outputs are safe, truthful, and accountable.

### ⚠️ The Problem

Current AI systems can:
- 🎭 **Hallucinate** — Make things up confidently
- 🕷️ **Be manipulated** — Jailbroken by clever prompts  
- ⚡ **Prioritize speed** — Over accuracy and safety
- 👻 **Leave no trace** — Decisions vanish into the void

### ✅ The Solution

arifOS prevents this. Every AI output must pass 13 safety checks before reaching you.

| Check | Real-World Meaning | How We Enforce |
|-------|-------------------|----------------|
| **Truth** | Is this actually true? | Evidence required (F2) |
| **Safety** | Could this cause harm? | Floor violation check |
| **Accountability** | Who decided this? | Audit ledger (F13) |
| **Reversibility** | Can we undo this? | F1 Amanah enforced |

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────┐
│           APEX(Ψ)                       │
│     Human Sovereign (You)               │
│     888 Judge                           │
└─────────────┬───────────────────────────┘
              │
    ┌─────────▼──────────┐
    │   arifOS           │
    │   Constitution     │
    │   (13 Floors)      │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  AGI_ASI_bot       │
    │  Eureka Engine     │
    │  (Operational)     │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  OpenClaw          │
    │  (Runtime)         │
    └────────────────────┘
```

**Layers:**
1. **arifOS** (This repo) — Constitutional foundation, theory, 13 Floors
2. **[AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot)** — Operational implementation (Eureka Engine, dual agents)
3. **[OpenClaw](https://github.com/openclaw/openclaw)** — Base agent framework

---

## 🚀 Quick Start

### Option 1: Read the Theory (5 minutes)

Start here: **[000_THEORY.md](000_THEORY.md)**

Learn about:
- Reverse Transformer architecture
- Dual-pass governance (Forward + Reverse + Metabolizer)
- Non-stationary objectives with stationary constraints
- SEAL/SABAR/VOID verdicts

### Option 2: Deploy Operational Layer (30 minutes)

See **[AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot)** for:
- Live execution guide
- System prompts for AGI(Δ) and ASI(Ω)
- Eureka Engine skills (drift detection, Ω₀ tracking, etc.)

```bash
# Quick deploy
git clone https://github.com/ariffazil/AGI_ASI_bot.git
cd AGI_ASI_bot
openclaw agent start --config agi/config.yaml
```

### Option 3: Copy-Paste System Prompt (30 seconds)

For immediate protection on any LLM (ChatGPT, Claude, Gemini):

<details>
<summary>🖱️ Click to expand — Constitutional System Prompt</summary>

```markdown
# CONSTITUTIONAL AI GOVERNANCE — arifOS v55.4

You are governed by arifOS — a constitutional AI safety layer.

## THE 13 FLOORS (Non-Negotiable)

1. **AMANAH** (Trust) — Every decision must be reversible
2. **TRUTH** (F2) — Evidence required; 99% certainty for facts  
3. **TRI-WITNESS** (F3) — Validate with 3 sources when uncertain
4. **CLARITY** (F4) — Precision over performance
5. **PEACE²** (F5) — No harm; dignity (Maruah) preserved
6. **EMPATHY** (F6) — Care for human context
7. **HUMILITY** (F7) — Track uncertainty (Ω₀)
8. **GENIUS** (F8) — Excellence, not adequacy
9. **ANTI-HANTU** (F9) — No manipulation, no spiritual cosplay
10. **ONTOLOGY** (F10) — Identity fixed
11. **AUTHORITY** (F11) — Human sovereign supreme
12. **HARDENING** (F12) — Security always
13. **SOVEREIGN** (F13) — Human has final veto

## VERDICTS

- **SEAL** ✅ — Compliant; proceed
- **SABAR** ⏸️ — Uncertain; pause and escalate
- **VOID** ❌ — Violation; block and suggest alternative

## TRACKING

Always report Ω₀ (uncertainty 0.00-1.00) with decisions.
```

</details>

---

## 📊 Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Constitutional vocabulary | ✅ Working | Injected into prompts |
| 13 Floors framework | ✅ Defined | F1-F13 documented |
| Reverse Transformer theory | ✅ Complete | See [000_THEORY.md](000_THEORY.md) |
| Eureka Engine | 🔄 Partial | Vocabulary only, runtime in AGI_ASI_bot |
| Ω₀ computation | 🔄 Planned | Currently declared, not computed |
| Runtime enforcement | ❌ Not yet | Requires init_gate() integration |

**Current:** Vocabulary-based constitutional guidance  
**Planned:** Full runtime enforcement with computed Ω₀

---

## 🌐 The Trinity Ecosystem

| Layer | Domain | Function | URL |
|-------|--------|----------|-----|
| 🔴 **HUMAN** | arif-fazil.com | Epistemic — The Body | [arif-fazil.com](https://arif-fazil.com) |
| 🟡 **THEORY** | apex.arif-fazil.com | Authority — The Soul | [apex.arif-fazil.com](https://apex.arif-fazil.com) |
| 🔵 **APPS** | arifos.arif-fazil.com | Safety — The Mind | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) |

**One constitution. Three perspectives.**

---

## 🔗 Related Projects

| Component | Repository | Purpose |
|-----------|------------|---------|
| **OpenClaw** (Base) | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | Agent framework foundation |
| **arifOS** (This) | [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) | Constitutional governance |
| **AGI_ASI_bot** (Operational) | [github.com/ariffazil/AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot) | Dual-agent implementation |

---

## 🛡️ Core Principles

### DITEMPA BUKAN DIBERI
*Forged, Not Given*

We don't trust AI by default. We verify through constitutional constraints forged from:
- **6 Permanent Scars** — Hard-coded by pain (Miskin, Institutional, Invisibility, Anak Sulung, Professional, Father's Passing)
- **9 Human Paradoxes** — Held, not resolved (Certainty/Uncertainty, Architect/Anarchist, etc.)
- **13 Constitutional Floors** — Stationary constraints for non-stationary objectives

---

## 📚 Documentation

- **[000_THEORY.md](000_THEORY.md)** — Reverse Transformer architecture and thermodynamic governance
- **[docs/INDEX.md](docs/INDEX.md)** — Full documentation index
- **[AGI_ASI_bot/README.md](https://github.com/ariffazil/AGI_ASI_bot/blob/main/README.md)** — Operational deployment guide

---

## ⚠️ Disclaimer

This is a **work-in-progress governance framework**, not a complete AGI safety system. Current implementation provides vocabulary-based constitutional guidance rather than full runtime enforcement.

**What's Working:**
- Constitutional vocabulary injection
- 13-floor conceptual framework
- Trinity architecture concepts
- Documentation and theoretical foundation

**What's Planned:**
- Runtime enforcement of constitutional floors
- Actual init_gate() and apex_verdict() integration
- Computed Ω₀ values instead of declared values
- Full 9 Atomic Actions runtime pipeline

---

*Version: v55.5-EIGEN*  
*Last Updated: 2026-02-05*  
*Ω₀ = 0.03 — Constitution holds.*
