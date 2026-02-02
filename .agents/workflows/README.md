# arifOS Agent Workflows (000-999)

**Location:** `.agents/workflows/`  
**Purpose:** Standard operating procedures for the 000-999 metabolic loop

---

## The 10 Canonical Workflows

| Stage | File | Purpose | Engine |
|-------|------|---------|--------|
| 000 | `000_init.md` | Session ignition, F12 injection scan | — |
| 111 | `111_sense.md` | Intent classification, lane routing | AGI (Δ) |
| 222 | `222_think.md` | Hypothesis generation, exploration | AGI (Δ) |
| 333 | `333_reason.md` | Deep logical reasoning | AGI (Δ) |
| 444 | `444_evidence.md` | Evidence gathering, tri-witness | AGI (Δ) |
| 555 | `555_empathy.md` | Stakeholder impact analysis | ASI (Ω) |
| 666 | `666_align.md` | Ethics/law/policy reconciliation | ASI (Ω) |
| 777 | `777_forge.md` | Synthesis, solution crafting | ASI (Ω) |
| 888 | `888_judge.md` | Final constitutional verdict | APEX (Ψ) |
| 999 | `999_seal.md` | Cryptographic sealing, audit | VAULT |

---

## Usage

Each workflow file contains:
1. **Trigger conditions** — When to invoke this stage
2. **Required inputs** — What data the stage needs
3. **Process steps** — The metabolic operations
4. **Outputs** — What the stage produces
5. **Next stages** — Where to route after completion

---

## 000-999 Loop Flow

```
000_INIT (Session Start)
    ↓
111_SENSE (Intent Detection)
    ↓
222_THINK (Exploration) ←→ 333_REASON (Analysis)
    ↓                         ↓
    └────────→ 444_EVIDENCE ←─┘
                   ↓
555_EMPATHY (Impact Analysis)
    ↓
666_ALIGN (Ethics Check)
    ↓
777_FORGE (Synthesis)
    ↓
888_JUDGE (Constitutional Verdict)
    ↓
999_SEAL (Cryptographic Commit)
    ↓
000<->999 (Loop Complete)
```

---

**DITEMPA BUKAN DIBERI — Forged, Not Given**
