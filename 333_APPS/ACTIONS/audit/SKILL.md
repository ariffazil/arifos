---
name: arifos-audit
description: 888_JUDGE — Check F1-F13 floors, compute governance score. APEX enforcement layer.
metadata:
  arifos:
    stage: 888_JUDGE
    trinity: APEX
    floors: [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13]
    version: 55.5
---

# arifos-audit

**Tagline:** Constitutional compliance scanner.

**Physics:** Quantum Measurement — collapses to verdict

**Math:** W₃ = (Δ × Ω × Ψ)^(1/3) ≥ 0.95

**Code:**
```python
def audit(action, constitution):
    floors = {f: check_floor(action, f) for f in F1_F13}
    
    # Tri-Witness consensus
    delta = floors["F8"].score  # Mind
    omega = floors["F6"].score  # Heart
    psi = 1.0 if floors["F11"].passes else 0.0  # Authority
    
    consensus = (delta * omega * psi) ** (1/3)
    
    if consensus < 0.95:
        return Verdict.VOID("F3: Consensus failed")
    
    voids = sum(1 for f in floors.values() if f.verdict == "VOID")
    return Verdict.SEAL if voids == 0 else Verdict.PARTIAL
```

**Usage:** `/action audit action="proposal"`

**Floors:** All F1-F13
