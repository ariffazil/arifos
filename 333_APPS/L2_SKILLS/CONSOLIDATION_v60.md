# Skill Consolidation v60-FORGE: 18 → 9 VERBS

> *From scattered nouns to forged actions.*

---

## Before (18 Skills - Entropy Chaos)

```
~/.config/agents/skills/
├── apex-888-judgment-engine
├── constitutional-skill-template
├── f1-amanah-file-guardian
├── f13-sovereign-kinetic-brake
├── f2-truth-document-guardian
├── f3-tri-witness-consensus
├── f6-empathy-hard-floor
├── f6-thermodynamic-clarity
├── f7-godel-uncertainty-guard
├── f8-wisdom-equation-calculator
├── f9-shadow-cleverness-guard
├── phoenix-cooling-schedule
├── tri-witness-validator
├── trinity-000-999-pipeline
└── trinity-governance-core
```

---

## After (9 Skills - Forged Actions)

```
333_APPS/L2_SKILLS/ACTIONS/
├── anchor/      ← 111_SENSE (PERCEIVE)
├── reason/      ← 222_THINK (THINK)
├── integrate/   ← 333_REASON (MAP)
├── respond/     ← 444_EVIDENCE (CARE)
├── validate/    ← 555_EMPATHY (DEFEND)
├── align/       ← 666_ALIGN (HARMONIZE)
├── forge/       ← 777_FORGE (CRYSTALLIZE)
├── audit/       ← 888_JUDGE (DECIDE)
└── seal/        ← 999_SEAL (COMMIT)
```

---

## Consolidation Mapping

| New VERB | Consolidates | Floors | Trinity |
|----------|--------------|--------|---------|
| **anchor** | `agi_sense` + reality grounding | F2, F4, F12 | Δ |
| **reason** | `agi_think` + `agi_reason` + `f8-wisdom` | F2, F4, F7, F8 | Δ |
| **integrate** | `agi_reason` (deep) + atlas nav | F2, F7, F8 | Δ |
| **respond** | Compassionate output | F4, F5, F6 | Ω |
| **validate** | `asi_empathize` + `f6-empathy` + `f6-clarity` | F1, F5, F6 | Ω |
| **align** | `asi_align` + `f9-anti-hantu` | F5, F6, F9 | Ω |
| **forge** | `trinity-forge` + `reality-search` | F2, F4, F7 | Ψ |
| **audit** | `apex-verdict` + `f3-tri-witness` + `f13-sovereign` | ALL | Ψ |
| **seal** | `vault-seal` + `phoenix-cooling` | F1, F3, F11 | Ψ |

---

## Deleted Skills (Moved to Archive)

| Skill | Reason |
|-------|--------|
| `apex-888-judgment-engine` | → merged into **audit** |
| `f1-amanah-file-guardian` | → merged into **validate** (F1 check) |
| `f2-truth-document-guardian` | → merged into **anchor** |
| `f3-tri-witness-consensus` | → merged into **audit** |
| `f6-*` (both) | → merged into **validate** |
| `f7-godel-uncertainty-guard` | → merged into **reason** |
| `f8-wisdom-equation-calculator` | → merged into **reason** |
| `f9-shadow-cleverness-guard` | → merged into **align** |
| `phoenix-cooling-schedule` | → merged into **seal** |
| `tri-witness-validator` | → merged into **audit** |
| `trinity-000-999-pipeline` | → merged into **forge** |
| `trinity-governance-core` | → merged into **audit** |

---

## Entropy Reduction

```
Before: 18 skills × ~50 lines each = 900 lines of cognitive load
After:   9 skills × ~50 lines each = 450 lines of cognitive load

REDUCTION: 50% entropy removed ✅
```

---

## Usage

```python
# Old way (scattered)
from f1_amanah_file_guardian import check_reversibility
from f2_truth_document_guardian import verify_pdf
from f6_empathy_hard_floor import check_stakeholders

# New way (unified VERBS)
from arifos.skills import validate  # Contains F1, F2, F6 checks

# Use
result = await validate(query, session_id)
# Returns: {verdict, next_action: "align"}
```

---

**DITEMPA BUKAN DIBERI — Actions forged, not scattered.**
