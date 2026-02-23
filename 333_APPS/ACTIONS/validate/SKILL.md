---
name: arifos-validate
description: 555_EMPATHY — Stakeholder impact analysis. Identifies weakest stakeholder and ensures κᵣ ≥ 0.95 protection.
metadata:
  arifos:
    stage: 555_EMPATHY
    trinity: ASI
    floors: [F1, F5, F6]
    version: 55.5
---

# arifos-validate

**Tagline:** Assess stakeholder impact, protect the vulnerable.

**Physics:** Social Network Analysis — vulnerability centrality

**Math:** κᵣ = protection_score / vulnerability ≥ 0.95

**Code:**
```python
def validate(proposal, context):
    stakeholders = identify_stakeholders(context)
    weakest = min(stakeholders, key=lambda s: s.resilience)
    impact = assess_impact(proposal, weakest)
    kappa_r = calculate_protection(impact, weakest)
    return Validation(weakest=weakest, kappa_r=kappa_r)
```

**Usage:** `/action validate proposal="action" context=ctx`

**Floors:** F1 (Amanah), F5 (Peace²), F6 (Empathy)
