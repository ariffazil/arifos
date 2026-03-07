---
name: asi-validate
description: 555-666_ASI + validate verb — Defense validation, F1 Amanah reversibility, F5/F6 safety checks
---

# asi-validate

## Scope
Organ 555-666_ASI (Heart/Ω) + Verb validate — Defense validation, F1 reversibility check, F5 peace, F6 empathy validation.

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F1 | Amanah | LOCKED (reversibility) |
| F5 | Peace² | P² ≥ 1.0 |
| F6 | Empathy | κᵣ ≥ 0.70 |

## Backend Path
- `aclip_cai/triad/omega/validate.py`
- `core/organs/_2_heart.py`
- Safety: `core/shared/guards.py`

## Operational Rules

**Trigger When:**
- Safety validation required before execution
- F1 Amanah reversibility check needed
- Stakeholder impact assessment (F6)
- Risk classification (LOW/MODERATE/CRITICAL)

**Allowed Operations:**
- Check reversibility of proposed actions (F1)
- Verify that all file reads used the **Context Governor** filters
- Audit the **Token Density** (Signal-to-Noise ratio) of context
- Calculate risk tier and classify operations
- Verify weakest stakeholder protection (F6)
- Ensure peace metrics (F5)
- Flag 888_HOLD for irreversible high-impact actions

**888_HOLD Required:**
- All irreversible operations (F1 Amanah)
- High-impact modifications without rollback
- Risk tier CRITICAL without explicit confirmation
- Bypassing validation gates

## Quick Reference
```python
# Validation check
from aclip_cai.triad.omega import validate
result = await validate.check_safety(plan, context)

# Risk classification
from core.shared.guards import classify_risk
tier = classify_risk(operation_type, scope)
```

## Verification
```bash
python -c "from core.shared.guards import classify_risk; print('Validate: Guards ready')"
```
