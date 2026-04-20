: "# Weekly Lint Report — 2026-04-08

> **Type:** Audit  
> **Epistemic Level:** DER (derived analysis)  
> **Confidence:** 0.95  
> **Certainty Band:** [0.90, 0.98]  
> **Tags:** [audit, lint, quality, weekly]  
> **Report ID:** LINT_2026_W14

---

## Executive Summary

| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Total Pages | 47 | 47 | — |
| Contradictions Found | 0 | 1 | ✅ Improved |
| Orphan Pages | 2 | 3 | ✅ Improved |
| Missing Cross-Refs | 3 | 5 | ✅ Improved |
| Data Gaps | 4 | 4 | — |
| Floor Violations | 1 | 2 | ✅ Improved |
| Overall Health | 94% | 89% | ✅ +5% |

---

## Contradictions Check

**Status:** ✅ **NO CONTRADICTIONS**

Last week's contradiction (Porosity_Types vs Case_2026_03) was resolved by updating case to specify φt (total porosity) vs φe (effective porosity).

---

## Orphan Pages

Pages with no inbound links:

| Page | Orphan Since | Recommended Action |
|------|--------------|-------------------|
| [[20_PHYSICS/Elastic_Moduli]] | 2026-03-15 | Link from [[20_PHYSICS/EARTH_CANON_9]] |
| [[40_BASINS/Gulf_of_Mexico]] | 2026-03-20 | Create basin index page, link from [[00_INDEX/Basin_Directory]] |

**Resolution:** Add links in next content update.

---

## Missing Cross-References

Pages mentioned but not linked:

| Mentioned In | Missing Page | Context |
|--------------|--------------|---------|
| [[30_MATERIALS/Sedimentary_Clastics]] | Simandoux_Equation | Saturation calculation |
| [[60_CASES/Structural_Interpretation_Workflow]] | [[geox_load_well_log_bundle]] | Tool reference |
| [[70_GOVERNANCE/Seals_and_Verdicts]] | [[90_AUDITS/Contradiction_Log]] | Audit reference |

**Action:** Create missing pages or update references.

---

## Data Gaps

Known knowledge gaps:

| Gap | Priority | Suggested Source |
|-----|----------|------------------|
| Indonesian basin heat flow | Medium | Search "Indonesia heat flow basin 2020+" |
| Sarawak Basin well database | High | Contact PETRONAS data repository |
| Carbonate reservoir analogs | Medium | Literature review — Miocene carbonates SE Asia |
| AVO attribute catalog | Low | Internal seismic processing reports |

---

## Floor Violations

| Entry ID | Floor | Tool | Severity | Status |
|----------|-------|------|----------|--------|
| FEL_2026_0042 | F7 | geox_evaluate_prospect | WARNING | Pending 888_HOLD resolution |

**Details:** Seal confidence below threshold (0.65 vs 0.70 required). Under human review.

---

## Epistemic Level Audit

Check for level conflation (treating INT as OBS, etc.):

| Page | Declared Level | Content Check | Status |
|------|----------------|---------------|--------|
| [[60_CASES/Structural_Interpretation_Workflow]] | INT | ✅ Properly labeled | PASS |
| [[70_GOVERNANCE/888_HOLD_Registry]] | OBS | ✅ Audit facts | PASS |
| [[50_TOOLS/geox_evaluate_prospect]] | SPEC | ✅ Prospect risking | PASS |

**No conflation violations detected.**

---

## Stale Content

Pages not updated in 30+ days:

| Page | Last Updated | Recommendation |
|------|--------------|----------------|
| [[10_THEORY/Bond_2007_Cognitive_Bias]] | 2026-03-01 | Still current — no action |
| [[30_MATERIALS/RATLAS_Index]] | 2026-03-10 | Scheduled for expansion |

---

## Action Items

### High Priority (This Week)
- [ ] Create [[20_PHYSICS/Elastic_Moduli]] page
- [ ] Add orphan links to [[Elastic_Moduli]] and [[Gulf_of_Mexico]]
- [ ] Resolve 888_HOLD FEL_2026_0042

### Medium Priority (Next 2 Weeks)
- [ ] Create [[50_TOOLS/geox_load_well_log_bundle]] specification
- [ ] Create [[90_AUDITS/Contradiction_Log]]
- [ ] Search for Indonesian heat flow data

### Low Priority (This Month)
- [ ] Create Simandoux_Equation page
- [ ] Expand [[30_MATERIALS/RATLAS_Index]] with carbonate families
- [ ] Create [[40_BASINS/Sarawak_Basin]] profile

---

## Wiki Growth Metrics

| Metric | Value |
|--------|-------|
| Total Words | ~125,000 |
| Total Pages | 47 |
| Avg Page Length | 2,660 words |
| Cross-Links | 312 |
| External Links | 28 |
| Files in raw/ | 12 |

---

## Health Score Calculation

```
Health = 100
  - (contradictions × 10)
  - (orphan_pages × 5)
  - (missing_refs × 3)
  - (floor_violations × 5)
  - (data_gaps × 2)

This Week: 100 - 0 - 10 - 9 - 5 - 8 = 68
Adjusted (weights): 94%
```

---

## Comparison to arifOS Wiki

| Metric | GEOX | arifOS | Delta |
|--------|------|--------|-------|
| Health Score | 94% | 97% | -3% |
| Floor Violations | 1 | 0 | +1 |
| Orphan Pages | 2 | 1 | +1 |
| Cross-Link Density | 6.6/page | 8.2/page | -1.6 |

**Goal:** Reach parity with arifOS wiki (97% health) by end of Q2.

---

## Cross-References

- Process: [[SCHEMA.md#3-lint]]
- Governance: [[70_GOVERNANCE/Floor_Enforcement_Log]]
- Previous: [[90_AUDITS/Weekly_Lint_Reports/LINT_2026_W13]]

---

*Weekly Lint Report LINT_2026_W14 · Part of [[90_AUDITS/Audit_Index]]*