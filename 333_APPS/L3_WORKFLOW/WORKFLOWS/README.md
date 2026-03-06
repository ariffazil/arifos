# WORKFLOWS — The 9 Metabolic Sequences (v60.1-ARIF)

Level 3 | 9 Recipes | ΔS ≤ 0

> *Ditempa Bukan Diberi* — Forged, Not Given

---

## 🆕 NEW: Exploration-First Architecture (v2026.3.6)

### Two-Phase Workflow System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRE-DEVELOPMENT (Laptop/Kimi)                             │
│                         EXPLORATION → DECISION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   000_INIT → 100_EXPLORE → 200_DISCOVER → 300_APPRAISE → 400_DESIGN        │
│       ↓                                                                      │
│   [Session]   [Broad]      [Deep]        [Evaluate]     [Plan]             │
│       ↓                                                                      │
│       └──────────────────────┬────────────────────────────────┘             │
│                              ↓                                               │
│                        888_PRE_DEV_JUDGE                                     │
│                              ↓                                               │
│                    [Go/No-Go Decision]                                       │
│                              ↓                                               │
│                    SEAL / SABAR / VOID / 888_HOLD                           │
│                              ↓                                               │
└──────────────────────────────┼─────────────────────────────────────────────┘
                               │
                               ↓ HANDOFF
┌──────────────────────────────┼─────────────────────────────────────────────┐
│                    PRODUCTION (VPS Agents)                                   │
│                      IMPLEMENTATION → DEPLOYMENT                             │
├──────────────────────────────┼─────────────────────────────────────────────┤
│                              ↓                                               │
│   000_RE_INIT → 111_SENSE → 222_THINK → 333_ATLAS → 777_FORGE              │
│       ↓           ↓           ↓           ↓           ↓                     │
│   [Context]    [Gather]   [Analyze]   [Map]      [Build]                   │
│       ↓           ↓           ↓           ↓           ↓                     │
│       └───────────┴───────────┴───────────┴───────────┘                     │
│                       ↓                                                      │
│                  888_JUDGE → 999_VAULT                                      │
│                       ↓           ↓                                          │
│                  [Verify]    [Commit]                                       │
│                       ↓                                                      │
└───────────────────────┴──────────────────────────────────────────────────────┘
```

---

## 📁 Workflow Inventory

### Pre-Development Workflows (Exploration Phase)

| Workflow | Stage | Band | Purpose | Floors |
|----------|-------|------|---------|--------|
| **[100-EXPLORE](100-EXPLORE-WORKFLOW.md)** | 100 | E | Domain reconnaissance, broad exploration | F2, F4, F7, F8 |
| **[200-DISCOVER](200-DISCOVER-WORKFLOW.md)** | 200 | D | Deep pattern recognition, hypothesis testing | F2, F3, F4, F7, F8 |
| **[300-APPRAISE](300-APPRAISE-WORKFLOW.md)** | 300 | A | Value/effort assessment, Go/No-Go input | F5, F6, F7, F9 |
| **[400-DESIGN](400-DESIGN-WORKFLOW.md)** | 400 | D | Architecture blueprint, implementation plan | F2, F4, F5, F6, F7, F8, F10 |
| **[888-PRE-DEV-JUDGE](888-PRE-DEV-JUDGE-WORKFLOW.md)** | 888 | Ψ | Final verdict, production handoff | ALL |

### Production Workflows (Implementation Phase)

| Workflow | Stage | Band | Purpose | Floors |
|----------|-------|------|---------|--------|
| **[anchor](anchor-WORKFLOW.md)** | 000 | A | Session ignition | F11, F12, F13 |
| **[reason](reason-WORKFLOW.md)** | 222 | R | Logical inference | F2, F4, F7, F8 |
| **[integrate](integrate-WORKFLOW.md)** | 333 | I | Context atlas | F2, F4, F7, F10 |
| **[respond](respond-WORKFLOW.md)** | 444 | R | Draft response | F4, F5, F6 |
| **[validate](validate-WORKFLOW.md)** | 555 | R | Safety validation | F5, F6, F1 |
| **[align](align-WORKFLOW.md)** | 666 | R | Ethical alignment | F5, F6, F9 |
| **[forge](forge-WORKFLOW.md)** | 777 | F | Implementation | F1, F2, F4, F8 |
| **[audit](audit-WORKFLOW.md)** | 888 | I | Full F1-F13 review | ALL |
| **[seal](seal-WORKFLOW.md)** | 999 | F | Vault commitment | F1, F3 |

### Architecture Documentation

| Document | Purpose |
|----------|---------|
| **[EXPLORATION-APPRAISAL-ARCHITECTURE](EXPLORATION-APPRAISAL-ARCHITECTURE.md)** | Complete architecture guide for exploration-first development |

---

## 🔄 The Dual-Loop Architecture

### Why Two Phases?

| Aspect | Pre-Development | Production |
|--------|----------------|------------|
| **Agent** | You + Kimi (Laptop) | VPS Agents |
| **Focus** | Exploration, creativity, judgment | Implementation, precision, consistency |
| **Cost** | Lower (local compute) | Higher (VPS resources) |
| **Iteration** | Fast, exploratory | Measured, deliberate |
| **Uncertainty** | High (discovering) | Low (executing known plan) |
| **Reversibility** | Easy (ideas are cheap) | Hard (code is committed) |

### Separation of Concerns

**Pre-Development (You Decide)**:
- Should we build this?
- What should we build?
- How should it work?
- What's the architecture?

**Production (Agents Execute)**:
- Write the code
- Run the tests
- Deploy the service
- Monitor the system

---

## 📋 When to Use Which Workflow

### Starting a New Project
```
100-EXPLORE → 200-DISCOVER → 300-APPRAISE → 400-DESIGN → 888-PRE-DEV-JUDGE
     ↓
["I have an idea"] → ["Let's verify it"] → ["Should we build?"] → 
     ↓
["How exactly?"] → ["Your decision, Arif"]
```

### Evaluating Technology
```
100-EXPLORE → 200-DISCOVER → 300-APPRAISE → 888-PRE-DEV-JUDGE
     ↓
["Should we use X or Y?"] → ["Test both"] → ["Compare"] → 
     ↓
["Recommend: Use X"]
```

### Ready-to-Implement Feature
```
400-DESIGN → 888-PRE-DEV-JUDGE → [Handoff] → 111_SENSE → 777_FORGE
     ↓
["Architecture ready"] → ["Approve"] → ["VPS takes over"] → 
     ↓
["Implement"] → ["Ship"]
```

---

## 🛡️ Floor Coverage by Phase

### Pre-Development Floors

| Workflow | F2 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 100-EXPLORE | ✓ | ✓ | | | ✓ | ✓ | | | | | |
| 200-DISCOVER | ✓ | ✓ | | | ✓ | ✓ | | | | | |
| 300-APPRAISE | | | ✓ | ✓ | ✓ | | ✓ | | | | |
| 400-DESIGN | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | | | |
| 888-PRE-DEV-JUDGE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### Production Floors

| Workflow | F1 | F2 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| anchor | | | | | | | | | | ✓ | ✓ | ✓ |
| reason | | ✓ | ✓ | | | ✓ | ✓ | | | | | |
| integrate | | ✓ | ✓ | | | ✓ | | | ✓ | | | |
| respond | | | ✓ | ✓ | ✓ | | | | | | | |
| validate | ✓ | | | ✓ | ✓ | | | | | | | |
| align | | | | ✓ | ✓ | | | ✓ | | | | |
| forge | ✓ | ✓ | ✓ | | | | ✓ | | ✓ | | | |
| audit | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| seal | ✓ | | | | | | | | | | | ✓ |

---

## 📊 Workflow Relationship Matrix

### Pre-Development Chain

```
EXPLORE ──(if PROCEED)──→ DISCOVER ──(if VALIDATED)──→ APPRAISE ──(if GO)──→ DESIGN ──→ JUDGE
   ↓                          ↓                          ↓                      ↓
CONTINUE                  REJECT                  NO-GO               SABAR/VOID
(explore more)         (hypothesis false)      (not worth it)        (revise)
```

### Production Chain

```
anchor ──→ reason ──→ integrate ──→ respond ──→ validate ──→ align ──→ forge ──→ audit ──→ seal
  ↓          ↓           ↓                                    ↓         ↓         ↓
000        222         333                                  555       666       777       888   999
```

---

## 🎯 Workflow vs Skill vs Tool

| Layer | What | Example | State | Constitutional |
|-------|------|---------|-------|----------------|
| **Tool** | Atomic capability | `reason_mind()` | Stateless | Floor-enforced |
| **Skill** | Behavioral prompt | "You are a refactoring agent..." | Stateless | Guidance-only |
| **Workflow** | Multi-step recipe | `EXPLORE → DISCOVER → APPRAISE` | Stateful | Loop-governed |

**Key Insight**: 
- Tools are **called**; they execute and return
- Skills **guide**; they shape behavior  
- Workflows **orchestrate**; they maintain state across stages

---

## 🚀 Quick Start

### For Exploration (Laptop)
```bash
# Start with exploration
kimi skill use arifos-agi-plan

# Follow 100-EXPLORE workflow
> "I want to explore building an AI code review tool"

# Continue through the chain
[EXPLORE] → [DISCOVER] → [APPRAISE] → [DESIGN] → [JUDGE]
```

### For Production (VPS)
```bash
# After SEAL verdict, VPS agents take over
ssh root@srv1325122.hstgr.cloud
./scripts/vps_production_workflow.sh

# Follow production workflows
[anchor] → [reason] → [integrate] → [forge] → [audit] → [seal]
```

---

## 📚 Related Documentation

| Document | Purpose |
|----------|---------|
| [EXPLORATION-APPRAISAL-ARCHITECTURE](EXPLORATION-APPRAISAL-ARCHITECTURE.md) | Complete architecture guide |
| [SKILLS_ALIGNMENT_REPORT](../../SKILLS_ALIGNMENT_REPORT.md) | Skills inventory and sync status |
| [UNIFIED_SKILLS_ARCHITECTURE](../../docs/60_REFERENCE/UNIFIED_SKILLS_ARCHITECTURE.md) | L1-L3 stack architecture |
| [AGENTS.md](../../AGENTS.md) | Canonical agent guidance |

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v60.1-FORGE-ARIF + v2026.3.6-EXPLORATION  
**Entropy:** ΔS = -0.65

---

**DITEMPA BUKAN DIBERI** — Forged through exploration, validated through judgment, executed with precision. 🔥
