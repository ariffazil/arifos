# WORKFLOWS — Unified Metabolic Loop (v2026.3.6-CANON)

**Level 3 | 11 Stages | 000→999 | ΔS ≤ 0**

> *Ditempa Bukan Diberi* — Forged, Not Given

---

## 🔄 Unified 11-Stage Metabolic Loop

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRE-DEVELOPMENT (Exploration & Design)                    │
│                        000 → 100 → 200 → 300 → 400                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   000_INIT ──→ 100_EXPLORE ──→ 200_DISCOVER ──→ 300_APPRAISE ──→ 400_DESIGN │
│      [Φ]           [E]              [D]              [A]             [D]     │
│       │              │                │                │               │     │
│       │          Broad            Deep          Evaluate          Plan       │
│       │          Domain           Pattern       Value/Effort      Architecture│
│       │                                                              │       │
│       └──────────────────────────────┬───────────────────────────────┘       │
│                                      ↓                                       │
│                            500_PLAN (Execution Strategy)                     │
│                                      [Σ]                                     │
│                               Safety Validation                              │
└──────────────────────────────────────┼───────────────────────────────────────┘
                                       ↓
┌──────────────────────────────────────┼───────────────────────────────────────┐
│                  PRODUCTION (Implementation & Deployment)                    │
│                    600 → 700 → 800 → 888 → 999                              │
├──────────────────────────────────────┼───────────────────────────────────────┤
│                                      ↓                                       │
│   600_PREPARE ──→ 700_PROTOTYPE ──→ 800_VERIFY ──→ 888_JUDGE ──→ 999_VAULT  │
│       [Ρ]             [Φ]               [Υ]            [Ψ]           [Ω]     │
│        │               │                 │              │             │      │
│    Environment      Build/            Final        Final        Commit       │
│    Setup            Implement       Testing      Verdict        to Vault     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 The 11 Canonical Workflows

### Pre-Development Phase (Exploration → Decision)

| # | Workflow | Stage | Band | Purpose | Floors |
|---|----------|-------|------|---------|--------|
| 1 | **[000-INIT](000-INIT-WORKFLOW.md)** | 000 | Φ | Session ignition, authority, intent | F11, F12, F13 |
| 2 | **[100-EXPLORE](100-EXPLORE-WORKFLOW.md)** | 100 | E | Domain reconnaissance, broad exploration | F2, F4, F7, F8 |
| 3 | **[200-DISCOVER](200-DISCOVER-WORKFLOW.md)** | 200 | D | Deep pattern recognition, hypothesis testing | F2, F3, F4, F7, F8 |
| 4 | **[300-APPRAISE](300-APPRAISE-WORKFLOW.md)** | 300 | A | Value/effort assessment, Go/No-Go input | F5, F6, F7, F9 |
| 5 | **[400-DESIGN](400-DESIGN-WORKFLOW.md)** | 400 | D | Architecture blueprint, implementation plan | F2, F4, F5, F6, F7, F8, F10 |

### Transition Phase (Strategy & Validation)

| # | Workflow | Stage | Band | Purpose | Floors |
|---|----------|-------|------|---------|--------|
| 6 | **[500-PLAN](500-PLAN-WORKFLOW.md)** | 500 | Σ | Execution planning, safety validation | F1, F5, F6, F9 |

### Production Phase (Implementation → Deployment)

| # | Workflow | Stage | Band | Purpose | Floors |
|---|----------|-------|------|---------|--------|
| 7 | **[600-PREPARE](600-PREPARE-WORKFLOW.md)** | 600 | Ρ | Environment setup, access provisioning | F11, F12 |
| 8 | **[700-PROTOTYPE](700-PROTOTYPE-WORKFLOW.md)** | 700 | Φ | Implementation execution, building | F1, F2, F4, F8 |
| 9 | **[800-VERIFY](800-VERIFY-WORKFLOW.md)** | 800 | Υ | Final testing, quality assurance | F2, F4, F6 |
| 10 | **[888-JUDGE](888-JUDGE-WORKFLOW.md)** | 888 | Ψ | Final verdict, Go/No-Go decision | **ALL F1-F13** |
| 11 | **[999-VAULT](999-VAULT-WORKFLOW.md)** | 999 | Ω | Immutable commitment, loop closure | F1, F3 |

---

## 🗺️ Workflow Navigation Guide

### When to Use Each Workflow

| Situation | Starting Workflow | Path |
|-----------|-------------------|------|
| **New project idea** | 000-INIT → 100-EXPLORE | 000 → 100 → 200 → 300 → 400 → 500 → [handoff] |
| **Known domain, new feature** | 000-INIT → 200-DISCOVER | 000 → 200 → 300 → 400 → 500 → [handoff] |
| **Architecture approved, build now** | 500-PLAN | 500 → 600 → 700 → 800 → 888 → 999 |
| **Production bug fix** | 000-INIT → 700-PROTOTYPE | 000 → 700 → 800 → 888 → 999 (expedited) |
| **Emergency deployment** | 000-INIT → 600-PREPARE | 000 → 600 → 700 → 888 → 999 (hotfix) |
| **Read-only inquiry** | 000-INIT → 100-EXPLORE | 000 → 100 → [report] |

### Decision Points

```
100-EXPLORE
     ↓
[Continue exploration?] ──NO──→ Terminate
     ↓ YES
200-DISCOVER
     ↓
[Patterns validated?] ──NO──→ Return to EXPLORE
     ↓ YES
300-APPRAISE
     ↓
[Proceed with build?] ──NO──→ Terminate or redesign
     ↓ YES
400-DESIGN
     ↓
[Design approved?] ──NO──→ Return to APPRAISE
     ↓ YES
500-PLAN
     ↓
[Plan validated?] ──NO──→ Return to DESIGN
     ↓ YES
[Handoff to Production]
     ↓
600-PREPARE → 700-PROTOTYPE → 800-VERIFY
     ↓
888-JUDGE
     ↓
[SEAL?] ──YES──→ 999-VAULT
     ↓ NO
[SABAR?] ──YES──→ Return to indicated stage
     ↓ NO
[VOID?] ──YES──→ Archive and terminate
     ↓ NO
[888_HOLD] ──→ Pause and review
```

---

## 🛡️ Floor Coverage Matrix

### Pre-Development (000-500)

| Workflow | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|
| 000-INIT | | | | | | | | | | | ✓ | ✓ | ✓ |
| 100-EXPLORE | | ✓ | | ✓ | | | ✓ | ✓ | | | | | |
| 200-DISCOVER | | ✓ | ✓ | ✓ | | | ✓ | ✓ | | | | | |
| 300-APPRAISE | | | | | ✓ | ✓ | ✓ | | ✓ | | | | |
| 400-DESIGN | | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | | | |
| 500-PLAN | ✓ | | | | ✓ | ✓ | | | ✓ | | | | |

### Production (600-999)

| Workflow | F1 | F2 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|
| 600-PREPARE | | | | | | | | | | ✓ | ✓ | |
| 700-PROTOTYPE | ✓ | ✓ | ✓ | | | | ✓ | | | | | |
| 800-VERIFY | | ✓ | ✓ | | ✓ | | | | | | | |
| 888-JUDGE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 999-VAULT | ✓ | | | | | | | | | | | ✓ |

---

## 📊 Stage Summary

| Stage | Name | Greek | Focus | Key Output |
|-------|------|-------|-------|------------|
| 000 | INIT | Φ (Phi) | Foundation | Ignited session |
| 100 | EXPLORE | E (Eta) | Expansion | Territory map |
| 200 | DISCOVER | D (Delta) | Depth | Validated insights |
| 300 | APPRAISE | A (Alpha) | Assessment | Value matrix |
| 400 | DESIGN | D (Delta) | Definition | Architecture blueprint |
| 500 | PLAN | Σ (Sigma) | Strategy | Execution plan |
| 600 | PREPARE | Ρ (Rho) | Readiness | Ready environment |
| 700 | PROTOTYPE | Φ (Phi) | Forge | Working implementation |
| 800 | VERIFY | Υ (Upsilon) | Validation | Verified system |
| 888 | JUDGE | Ψ (Psi) | Soul | Final verdict |
| 999 | VAULT | Ω (Omega) | Completion | Immutable record |

---

## 🎯 Workflow vs Skill vs Tool

| Layer | Abstraction | Example | State |
|-------|-------------|---------|-------|
| **L1** | Primitives | `git clone`, `docker ps` | Stateless |
| **L2** | Tools | `reason_mind()`, `vps_git_ingest()` | Stateless |
| **L3** | Skills | "You are a refactoring agent..." | Stateless |
| **L4** | **Workflows** | `000-INIT → 100-EXPLORE → ...` | **Stateful** |
| **L5** | Agents | Autonomous systems | Persistent |

**Key Insight**: Workflows maintain state across stages; tools and skills do not.

---

## 📁 File Organization

```
333_APPS/L3_WORKFLOW/WORKFLOWS/
├── README.md                                    (This file)
├── EXPLORATION-APPRAISAL-ARCHITECTURE.md       (Architecture guide)
│
├── 000-INIT-WORKFLOW.md                         (Foundation)
├── 100-EXPLORE-WORKFLOW.md                      (Expansion)
├── 200-DISCOVER-WORKFLOW.md                     (Depth)
├── 300-APPRAISE-WORKFLOW.md                     (Assessment)
├── 400-DESIGN-WORKFLOW.md                       (Definition)
├── 500-PLAN-WORKFLOW.md                         (Strategy)
├── 600-PREPARE-WORKFLOW.md                      (Readiness)
├── 700-PROTOTYPE-WORKFLOW.md                    (Forge)
├── 800-VERIFY-WORKFLOW.md                       (Validation)
├── 888-JUDGE-WORKFLOW.md                        (Soul)
└── 999-VAULT-WORKFLOW.md                        (Omega)

_ARCHIVE/                                        (Old workflows archived)
```

---

## 🚀 Quick Start

### For Exploration (Laptop)
```bash
kimi skill use arifos-agi-plan

# "I want to explore building X"

[000-INIT] → [100-EXPLORE] → [200-DISCOVER] → [300-APPRAISE] → [400-DESIGN]
     ↓
[Your decision at 500-PLAN]
```

### For Production (VPS)
```bash
# After SEAL verdict
ssh root@srv1325122.hstgr.cloud

[600-PREPARE] → [700-PROTOTYPE] → [800-VERIFY] → [888-JUDGE] → [999-VAULT]
```

---

## 📚 Related Documentation

| Document | Purpose |
|----------|---------|
| [EXPLORATION-APPRAISAL-ARCHITECTURE](EXPLORATION-APPRAISAL-ARCHITECTURE.md) | Complete architecture guide |
| [AGENTS.md](../../../AGENTS.md) | Canonical agent guidance |
| [UNIFIED_SKILLS_ARCHITECTURE](../../../docs/60_REFERENCE/UNIFIED_SKILLS_ARCHITECTURE.md) | L1-L3 stack |

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v2026.3.6-CANON  
**Status:** UNIFIED — CHAOS REDUCED  
**Entropy:** ΔS = -0.72

---

**11 Stages. 13 Floors. 1 Constitution.**

**DITEMPA BUKAN DIBERI** — Unified, canonical, forged. 🔥
