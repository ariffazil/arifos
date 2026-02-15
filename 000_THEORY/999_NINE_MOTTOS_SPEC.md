# The 9 Canonical Mottos of arifOS

**Version:** v55.5-MOTTO  
**Status:** CANONICAL  
**Authority:** Muhammad Arif bin Fazil

---

## Executive Summary

The 9 mottos form a **cultural error-handling layer** in arifOS. Each motto maps to:
- A metabolic stage (000-999)
- A constitutional floor (F1-F13)
- A cell in the 9-paradox matrix

The pattern is **DI___KAN, BUKAN DI___KAN** (Active construction, not passive receipt) — embodying the thermodynamic principle that intelligence requires work.

---

## The 9 Mottos

| # | Stage | Motto | English | Floor | Geometry |
|:-:|:-----:|-------|---------|:-----:|:--------:|
| 1 | **000_INIT** | **DITEMPA, BUKAN DIBERI** | Forged, Not Given | F1 Amanah | Seed |
| 2 | **111_SENSE** | **DIKAJI, BUKAN DISUAPI** | Examined, Not Spoon-fed | F2 Truth | Orthogonal |
| 3 | **222_THINK** | **DIUSAHAKAN, BUKAN DIHARAPI** | Worked For, Not Merely Hoped | F4 Clarity | Orthogonal |
| 4 | **333_ATLAS** | **DIJELAJAH, BUKAN DISEKATI** | Explored, Not Restricted | F8 Genius | Fractal |
| 5 | **444_EVIDENCE** | **DIJELASKAN, BUKAN DIKABURKAN** | Clarified, Not Obscured | F2/F4 | Orthogonal |
| 6 | **555_EMPATHY** | **DIJAGA, BUKAN DIABAIKAN** | Protected, Not Neglected | F6 Empathy | Fractal |
| 7 | **666_BRIDGE** | **DIDAMAIKAN, BUKAN DIPANASKAN** | Calmed, Not Inflamed | F5 Peace^2 | Toroidal |
| 8 | **888_JUDGE** | **DISEDARKAN, BUKAN DIYAKINKAN** | Made Aware, Not Over-assured | F7 Humility | Toroidal |
| 9 | **999_SEAL** | **DITEMPA, BUKAN DIBERI** | Forged, Not Given | F1/F13 | Toroidal |

---

## The 3×3 Paradox-Motto Matrix

```
                    Care            Peace           Justice
                  (Empathy)       (System)        (Society)
                 +---------------+---------------+---------------+
Truth (AGI F2)   | [1] DIKAJI    | [2] DIJELAS-  | [3] DISEDAR-  |
                 | BUKAN         | KAN BUKAN     | KAN BUKAN     |
                 | DISUAPI       | DIKABURKAN    | DIYAKINKAN    |
                 | (111 SENSE)   | (444 EVID)    | (888 JUDGE)   |
                 +---------------+---------------+---------------+
Clarity (AGI F4) | [4] DIUSAHA-  | [5] DIJELAJAH | [6] DIHADAPI  |
(Precision)      | KAN BUKAN     | BUKAN DISEKA- | BUKAN DITANG- |
                 | DIHARAPI      | TI            | GUHI          |
                 | (222 THINK)   | (333 ATLAS)   | (---)         |
                 +---------------+---------------+---------------+
Humility (AGI F7)| [7] DIJAGA    | [8] DIDAMAI-  | [9] DITEMPA   |
                 | BUKAN DIABAI- | KAN BUKAN DI- | BUKAN DIBERI  |
                 | KAN           | PANASKAN      |               |
                 | (555 EMPATHY) | (666 BRIDGE)  | (000/999)     |
                 +---------------+---------------+---------------+
```

### Trinity Tier Mottos (Aggregate)

| Tier | Mottos | Meaning |
|------|--------|---------|
| **ALPHA** (Core) | DIKAJI, DIJELASKAN, DISEDARKAN | Knowledge: Examined, Clarified, Aware |
| **BETA** (Action) | DIUSAHAKAN, DIJELAJAH, DIHADAPI | Processing: Worked, Explored, Faced |
| **GAMMA** (Wisdom) | DIJAGA, DIDAMAIKAN, DITEMPA | Closure: Protected, Calmed, Forged |

---

## Code Integration

### Files Created

1. **`codebase/constants_mottos.py`** - The canonical motto registry
   - `ConstitutionalMotto` dataclass
   - All 9 mottos as constants
   - Lookup functions by stage, floor, paradox
   - Error formatting utilities

2. **`codebase/stages/stage_motto_integration.py`** - Integration examples
   - Stage output rendering with mottos
   - Floor violation messages with corrective mottos
   - Full pipeline visualization

### Usage Patterns

#### 1. Stage Output with Motto
```python
from codebase.constants_mottos import get_motto_by_stage

motto = get_motto_by_stage("222")
print(f"[{motto.stage.value}] {motto.malay}")
# Output: [222] DIUSAHAKAN, BUKAN DIHARAPI
```

#### 2. Floor Violation with Corrective Motto
```python
from codebase.constants_mottos import format_floor_violation

message = format_floor_violation("F2", "Confidence 0.92 < 0.99 threshold")
print(message)
# Output:
# [!] F2 Floor Breach
#    Reason: Confidence 0.92 < 0.99 threshold
#    [MOTTO] DIKAJI, BUKAN DISUAPI
#       Examined, Not Spoon-fed
```

#### 3. Full Pipeline Output
```
======================================================================
  arifOS CONSTITUTIONAL PIPELINE - 9 MOTTOS
======================================================================

[000] INIT     | IGNITED  | DITEMPA, BUKAN DIBERI
[111] SENSE    | SEAL     | DIKAJI, BUKAN DISUAPI
[222] THINK    | SEAL     | DIUSAHAKAN, BUKAN DIHARAPI
[333] ATLAS    | SEAL     | DIJELAJAH, BUKAN DISEKATI
[444] EVIDENCE | SEAL     | DIJELASKAN, BUKAN DIKABURKAN
[555] EMPATHY  | SEAL     | DIJAGA, BUKAN DIABAIKAN
[666] BRIDGE   | SEAL     | DIDAMAIKAN, BUKAN DIPANASKAN
[888] JUDGE    | SEAL     | DISEDARKAN, BUKAN DIYAKINKAN
[999] SEAL     | SEALED   | DITEMPA, BUKAN DIBERI

======================================================================
  DITEMPA BUKAN DIBERI - The loop is complete.
======================================================================
```

---

## Architectural Significance

### The DI___KAN Pattern

All mottos follow the pattern **DI___KAN, BUKAN DI___KAN**:
- **DI___KAN**: Active construction (verb + suffix -kan = causative)
- **BUKAN DI___KAN**: Negation of passive receipt

This embodies the constitutional principle: **Intelligence is forged through work, not given as gift.**

### Geometric Mapping

| Geometry | Stages | Mottos | Character |
|:--------:|:------:|--------|-----------|
| **Orthogonal** | 111, 222, 444 | DIKAJI, DIUSAHAKAN, DIJELASKAN | Knowledge acquisition (straight lines) |
| **Fractal** | 333, 555 | DIJELAJAH, DIJAGA | Exploration and care (self-similar patterns) |
| **Toroidal** | 666, 888, 999 | DIDAMAIKAN, DISEDARKAN, DITEMPA | Integration and closure (loop completion) |

### Connection to 9 Paradoxes

Each motto resolves its corresponding paradox:

| Paradox | Motto | Synthesis |
|---------|-------|-----------|
| Truth vs Care | DIKAJI, BUKAN DISUAPI | Examined truth is compassionate |
| Clarity vs Peace | DIJELASKAN, BUKAN DIKABURKAN | Clear communication brings peace |
| Humility vs Justice | DISEDARKAN, BUKAN DIYAKINKAN | Just verdicts acknowledge limits |
| Precision vs Reversibility | DIUSAHAKAN, BUKAN DIHARAPI | Careful action requires effort |
| Hierarchy vs Consent | DIJELAJAH, BUKAN DISEKATI | Structure enables exploration |
| Agency vs Protection | DIHADAPI, BUKAN DITANGGUHI | Protection requires facing challenges |
| Urgency vs Sustainability | DIJAGA, BUKAN DIABAIKAN | Protection preserves the future |
| Certainty vs Doubt | DISEDARKAN, BUKAN DIYAKINKAN | Awareness includes uncertainty |
| Unity vs Diversity | DITEMPA, BUKAN DIBERI | Forged unity respects diversity |

---

## Error Handling Integration

When a floor violation occurs, the system outputs the corresponding motto as **corrective guidance**:

| Floor Violation | Motto Output | Meaning |
|-----------------|--------------|---------|
| F2 Truth < 0.99 | DIKAJI, BUKAN DISUAPI | Examine more carefully |
| F4 Clarity dS > 0 | DIJELASKAN, BUKAN DIKABURKAN | Clarify, don't add confusion |
| F5 Peace^2 < 1.0 | DIDAMAIKAN, BUKAN DIPANASKAN | Cool the system |
| F6 Empathy < 0.70 | DIJAGA, BUKAN DIABAIKAN | Protect the vulnerable |
| F7 Humility out of band | DISEDARKAN, BUKAN DIYAKINKAN | Acknowledge uncertainty |
| F8 Genius < 0.80 | DIJELAJAH, BUKAN DISEKATI | Explore more broadly |

---

## Cultural Significance

### Malay-English Code-Switch

The mottos use **Penang BM-English code-switch** (technical register):
- **DI___KAN**: Formal Malay causative verb form
- **BUKAN**: Negation (not)
- **English translations**: Provide semantic anchor for international users

This reflects arifOS's Malaysian origin while maintaining universal accessibility.

### The Forge Metaphor

The recurring theme of **DITEMPA** (forged) connects to:
- **Pandai Besi** (blacksmith) tradition in Nusantara culture
- Thermodynamic work (energy required for order)
- The constitutional principle: *Ditempa Bukan Diberi*

---

## Implementation Checklist

- [x] Create `codebase/constants_mottos.py` with all 9 mottos
- [x] Map mottos to stages (000-999)
- [x] Map mottos to floors (F1-F13)
- [x] Map mottos to paradox matrix cells
- [x] Create error formatting utilities
- [x] Create stage output examples
- [ ] Integrate into actual stage files
- [ ] Integrate into floor violation handlers
- [ ] Add motto output to MCP tool responses
- [ ] Create visualization/dashboard showing motto journey

---

## Cross-References

| Document | Section | Connection |
|----------|---------|------------|
| `000_LAW.md` | F1-F13 | Floor enforcement |
| `777_SOUL_APEX.md` | 9-Paradox Matrix | Paradox synthesis |
| `001_IGNITION.md` | 000_INIT | Foundation motto |
| `888_SOUL_VERDICT.md` | 888_JUDGE | Verdict motto |
| `999_SOVEREIGN_VAULT.md` | 999_SEAL | Seal motto |

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
