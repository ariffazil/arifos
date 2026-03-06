---
name: constitution-canon
description: arifOS 13 Constitutional Floors (F1-F13) — canonical thresholds and law enforcement
---

# Constitution Canon

## Scope
F1-F13 floor definitions, thresholds, enforcement order, and constitutional law governance.

## Constitutional Alignment
| Floor | Name | Type | Threshold |
|-------|------|------|-----------|
| F1 | Amanah | HARD | LOCKED |
| F2 | Truth | HARD | τ ≥ 0.99 |
| F3 | Tri-Witness | MIRROR | W³ ≥ 0.95 |
| F4 | Clarity | HARD | ΔS ≤ 0 |
| F5 | Peace² | SOFT | P² ≥ 1.0 |
| F6 | Empathy | SOFT | κᵣ ≥ 0.70 |
| F7 | Humility | HARD | Ω₀ ∈ [0.03, 0.05] |
| F8 | Genius | MIRROR | G ≥ 0.80 |
| F9 | Anti-Hantu | SOFT | C_dark < 0.30 |
| F10 | Ontology | WALL | BOOLEAN |
| F11 | CommandAuth | WALL | LOCKED |
| F12 | Injection | HARD | Risk < 0.85 |
| F13 | Sovereign | VETO | HUMAN |

## Key Components
- `core/shared/floors.py` — Canonical THRESHOLDS dictionary
- `000_THEORY/000_LAW.md` — Constitutional law specification
- `core/kernel/constitutional_decorator.py` — Floor enforcement decorator
- `core/organs/` — 5-organ enforcement pipeline

## Execution Order
F12→F11 (Walls) → AGI Floors (F1,F2,F4,F7) → ASI Floors (F5,F6,F9) → Mirrors (F3,F8) → Ledger

## Operational Rules
**Trigger When:**
- Evaluating if an action passes constitutional muster
- Setting floor thresholds for enforcement decisions
- Auditing decisions against canonical law

**Allowed Operations:**
- Reference floor thresholds for any decision
- Check floor compliance via decorator
- Log floor pass/fail telemetry

**888_HOLD Required:**
- Modifying any floor threshold
- Bypassing floor enforcement (emergency only)
- Changing execution order

## Quick Reference
```python
from core.shared.floors import THRESHOLDS

# Check specific floor
F2_threshold = THRESHOLDS["F2"]["value"]  # 0.99

# All floor types
HARD_FLOORS = ["F1", "F2", "F4", "F7", "F12"]
SOFT_FLOORS = ["F5", "F6", "F9"]
MIRROR_FLOORS = ["F3", "F8"]
WALL_FLOORS = ["F10", "F11"]
VETO_FLOOR = ["F13"]
```

## Verification
```bash
python -c "from core.shared.floors import THRESHOLDS; print(f'F1-F13 loaded: {len(THRESHOLDS)} floors')"
```
