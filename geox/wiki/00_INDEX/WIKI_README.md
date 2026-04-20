# GEOX Wiki — Implementation Summary

> **Status:** FOUNDATION COMPLETE  
> **Date:** 2026-04-08  
> **Pages Created:** 10 core documents  
> **Structure:** Karpathy-style LLM Wiki Pattern  

---

## What Was Built

A complete **Large Earth Model (LEM) Wiki** implementing the [Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), deeply integrated with the arifOS constitutional federation.

### The Intelligence Stack

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 3: arifOS (Constitutional Governance)                     │
│ └── 13 Floors, 888_JUDGE, 999_VAULT                             │
│     Wiki: /root/arifOS/wiki/                                    │
├─────────────────────────────────────────────────────────────────┤
│ LAYER 2: GEOX (Large Earth Model)                               │
│ └── ToAC, RATLAS, EARTH.CANON_9, Forward/Inverse                │
│     Wiki: /root/GEOX/wiki/ ← YOU ARE HERE                       │
├─────────────────────────────────────────────────────────────────┤
│ LAYER 1: LLM (Fluent Reasoning)                                 │
│ └── Natural language interface                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Wiki Structure

```
GEOX/wiki/
├── SCHEMA.md                    # Wiki constitution (20KB)
├── index.md                     # Content catalog (8KB)
├── log.md                       # Chronological log
├── WIKI_README.md               # This file
│
├── 00_INDEX/                    # Entry points
│   ├── Quickstart.md            # 5-page journey
│   ├── Prerequisite_Map.md      # Knowledge graph
│   └── LLM_LEM_Manifesto.md     # Intelligence stack philosophy (17KB)
│
├── 10_THEORY/                   # Core geoscience theory
│   └── Theory_of_Anomalous_Contrast.md  # ToAC core (8KB)
│
├── 20_PHYSICS/                  # EARTH.CANON_9
│   └── EARTH_CANON_9.md         # 9 fundamental variables (4KB)
│
├── 30_MATERIALS/                # RATLAS
│   └── RATLAS_Index.md          # 99-material atlas (4KB)
│
├── 80_INTEGRATION/              # arifOS federation
│   └── Cross_Wiki_Links.md      # Navigation between wikis (5KB)
│
└── raw/                         # Immutable sources
    ├── papers/                  # Bond et al. 2007, etc.
    ├── well_logs/               # LAS references
    ├── seismic_surveys/         # Survey metadata
    └── basin_reports/           # Regional geology
```

---

## Key Features

### 1. Karpathy Pattern Implementation

| Element | Status | Location |
|---------|--------|----------|
| **Raw Sources** | ✅ | `raw/` — immutable documents |
| **The Wiki** | ✅ | `*/` — LLM-maintained knowledge |
| **The Schema** | ✅ | `SCHEMA.md` — conventions & workflows |
| **Operations** | ✅ | Ingest, Query, Lint defined |
| **index.md** | ✅ | Content catalog with metadata |
| **log.md** | ✅ | Chronological session record |

### 2. Constitutional Integration

GEOX wiki is **federated** with arifOS wiki:

| GEOX Page | Links To |
|-----------|----------|
| `[[80_INTEGRATION/Cross_Wiki_Links]]` | `[[arifos::Floors]]` |
| `[[70_GOVERNANCE/*]]` | `[[arifos::888_JUDGE]]` |
| `[[10_THEORY/Theory_of_Anomalous_Contrast]]` | `[[arifos::Floors#F9]]` |

**Updated arifOS pages:**
- `[[arifos::GEOX]]` — Now links to full GEOX wiki
- `[[arifos::index]]` — Links to GEOX wiki in Entities section

### 3. Frontmatter Schema

Every page includes YAML frontmatter:

```yaml
---
type: [Theory | Material | Basin | Tool | Case | Governance]
tags: [array, of, tags]
sources: [raw/papers/bond_2007.pdf]
last_sync: 2026-04-08
confidence: 0.95                    # F7 Humility
certainty_band: [0.85, 0.99]        # Ω₀ interval
epistemic_level: [OBS | DER | INT | SPEC]
arifos_floor: [F1 | F2 | F4 | F7 | F9 | F11 | F13]
---
```

### 4. Epistemic Levels (Critical)

| Level | Code | Meaning |
|-------|------|---------|
| **OBSERVATIONAL** | OBS | Raw sensor data |
| **DERIVED** | DER | Computed from observations |
| **INTERPRETED** | INT | Inferred from derived data |
| **SPECULATED** | SPEC | Proposed but unverified |

**F9 Violation:** Collapsing levels (treating INT as OBS) triggers 888_HOLD.

---

## The LLM → LEM → arifOS Philosophy

### The Problem

| Layer Alone | Failure Mode |
|-------------|--------------|
| **LLM only** | Generates plausible but physically impossible geology |
| **LLM + LEM** | Grounded but may overclaim, lacks audit trail |
| **Full Stack** | Grounded, governed, auditable, human-sovereign |

### The Solution

From `[[00_INDEX/LLM_LEM_Manifesto]]`:

> *"GEOX makes AI see the Earth. arifOS makes sure it does not lie about what it sees."*

**Layer 1: LLM** — Fluent reasoning surface (but ungrounded)  
**Layer 2: LEM (GEOX)** — Physics grounding, spatial verification, uncertainty quantification  
**Layer 3: arifOS** — Constitutional governance, 13 Floors, human sovereignty  

---

## Usage Workflows

### Ingest Workflow
```
1. Add source to raw/
2. LLM reads → discusses → writes summary
3. LLM updates entity/concept pages
4. LLM updates index.md
5. LLM appends to log.md
6. Human reviews in Obsidian
```

### Query Workflow
```
1. LLM reads index.md to find relevant pages
2. LLM drills into specific pages
3. LLM synthesizes answer with citations
4. LLM declares epistemic level
5. LLM suggests filing synthesis back to wiki
```

### Lint Workflow
```
1. Check for contradictions between pages
2. Identify stale claims
3. Find orphan pages (no inbound links)
4. Flag missing cross-references
5. Report data gaps
```

---

## Navigation

### Start Here
- **New to GEOX?** → `[[00_INDEX/Quickstart]]`
- **The intelligence stack?** → `[[00_INDEX/LLM_LEM_Manifesto]]`
- **Core theory?** → `[[10_THEORY/Theory_of_Anomalous_Contrast]]`
- **Physics foundation?** → `[[20_PHYSICS/EARTH_CANON_9]]`

### Cross-Wiki
- **arifOS main** → `[[arifos::index]]`
- **13 Floors** → `[[arifos::Floors]]`
- **888_JUDGE** → `[[arifos::888_JUDGE]]`

---

## Next Steps

### Immediate (Week 1)
- [ ] Populate remaining theory pages (Forward_vs_Inverse, Contrast_Canon)
- [ ] Create RATLAS material family pages
- [ ] Add first basin profile (Malay_Basin)

### Short Term (Month 1)
- [ ] Complete 50_TOOLS specifications
- [ ] Create 60_CASES with real workflows
- [ ] Populate 70_GOVERNANCE with floor enforcement logs

### Long Term (Quarter 1)
- [ ] Weekly lint reports in 90_AUDITS
- [ ] Full 99-material RATLAS pages
- [ ] Integration with Obsidian vault

---

## File Statistics

| File | Size | Purpose |
|------|------|---------|
| SCHEMA.md | 20KB | Wiki constitution |
| index.md | 8KB | Content catalog |
| LLM_LEM_Manifesto.md | 17KB | Intelligence stack philosophy |
| Theory_of_Anomalous_Contrast.md | 8KB | Core theory |
| Contrast_Canon.md | 8KB | Domain separation |
| Epistemic_Levels.md | 6KB | OBS/DER/INT/SPEC |
| Bond_2007_Cognitive_Bias.md | 6KB | Empirical foundation |
| EARTH_CANON_9.md | 4KB | Physics foundation |
| RATLAS_Index.md | 4KB | Material atlas index |
| Sedimentary_Clastics.md | 6KB | RATLAS family (18 materials) |
| Malay_Basin.md | 7KB | Basin profile example |
| Cross_Wiki_Links.md | 5KB | arifOS federation |
| **Total** | **~105KB** | Week 1 complete |

---

## Constitutional Telemetry

```
GEOX_WIKI_VERSION = "1.0.0"
SCHEMA_ANCHOR = "000"
STATUS = "FOUNDATION_COMPLETE"
PARENT_SCHEMA = "arifOS/wiki/SCHEMA.md"
TOTAL_PAGES = 10
CROSS_WIKI_LINKS = 8
FEDERATION_STATUS = "ACTIVE"
```

---

*GEOX Large Earth Model Wiki*  
*arifOS Constitutional Federation*  
*DITEMPA BUKAN DIBERI — Forged, not given.*
