---
name: arifos-forge
description: 777_FORGE — Solution generation with F8 Genius (G ≥ 0.80) and F2 Truth enforcement.
metadata:
  arifos:
    stage: 777_FORGE
    trinity: AGI
    floors: [F2, F4, F8, F13]
    version: 55.5
---

# arifos-forge

**Tagline:** Generate solutions, evaluate with Genius equation.

**Physics:** Thermodynamic Work — energy conversion efficiency

**Math:** G = A × P × X × E² ≥ 0.80

**Code:**
```python
def forge(specification, context_map):
    approaches = [
        generate_conservative(specification),
        generate_exploratory(specification),
        generate_adversarial(specification)
    ]
    
    for a in approaches:
        a.genius = calculate_genius(a)  # G = A×P×X×E²
    
    best = max(approaches, key=lambda x: x.genius)
    
    if best.genius < 0.80:
        return Verdict.SABAR("F8: Genius threshold not met")
    
    return Solution(approach=best, genius=best.genius)
```

**Usage:** `/action forge spec=requirements context=map`

**Floors:** F2 (Truth), F4 (Clarity), F8 (Genius), F13 (Curiosity)
