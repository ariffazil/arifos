---
name: arifos-anchor
description: 000_INTAKE — Ground reality, parse intent. Reduces sensory entropy by fixing reference frame. Use at session start.
metadata:
  arifos:
    stage: 000_INTAKE
    trinity: AGI
    floors: [F4, F7, F12]
    version: 55.5
---

# arifos-anchor

**Tagline:** Establish position, intake context, ground reality.

**Physics:** Signal Detection Theory — d-prime metric

**Math:** I(x) = -log₂P(x)

**Code:**
```python
def anchor(input_space, noise_floor):
    signal = extract_signal(input_space, noise_floor)
    return GroundedContext(position=signal.position)
```

**Usage:** `/action anchor input="user query"`

**Verdict:** Returns SEAL with session_id, or VOID if F12 injection detected.
