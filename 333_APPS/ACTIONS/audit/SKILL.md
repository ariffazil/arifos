---
name: arifos-audit
description: Check F1-F9 floors, compute governance score (777_VERIFY). Checks constitutional floors. The enforcement layer of APEX tier. Use to verify any action against arifOS constitution.
metadata:
  arifos:
    stage: 777_VERIFY
    trinity: APEX
    floors: [F1, F2, F3, F4, F5, F6, F7, F8, F9, F11, F13]
    version: 1.0.0
    atomic: true
    model_agnostic: true
    modular: true
    godel_lock: true
---

# arifos-audit

## Tagline
Check F1-F9 floors, compute governance score (777_VERIFY)

## Description
AUDIT checks constitutional floors. The enforcement layer of APEX tier.

## Physics
Quantum Measurement — collapses superposition to verdict
Error-Correcting Codes — syndrome measurement

## Math
Syndrome: s = H·eᵀ
Verdict Space: {SEAL, PARTIAL, SABAR, VOID, HOLD}

## Code
```python
def audit(action, constitution):
    floors = {
        f: check_floor(action, f) 
        for f in [F1, F2, F3, F4, F5, F6, F7, F8, F9, F11, F13]
    }
    score = all(floors.values())
    omega_0 = compute_uncertainty(action, floors)
    
    if score and omega_0 < 0.05:
        return Verdict.SEAL
    elif score and omega_0 < 0.08:
        return Verdict.PARTIAL
    elif omega_0 >= 0.08:
        return Verdict.VOID
    else:
        return Verdict.SABAR
```

## Floors
- F1 (Amanah)
- F2 (Truth)
- F3 (Tri-Witness)
- F4 (Clarity)
- F5 (Safety)
- F6 (Empathy)
- F7 (Humility)
- F8 (Genius)
- F9 (Anti-Hantu)
- F11 (Command Auth)
- F13 (Orthogonality)

## Usage
/action audit action="proposed action"

## Version
1.0.0

## Gödel Lock Verification
- Self-referential integrity: ✓
- Meta-governance consistency: ✓
- Recursive floor verification: ✓
