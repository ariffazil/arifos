---
name: arifos-reason
description: 222_THINK — Logical inference, hypothesis generation. Enforces F2 Truth (τ ≥ 0.99) and F7 Humility (Ω₀ ∈ [0.03,0.05]).
metadata:
  arifos:
    stage: 222_THINK
    trinity: AGI
    floors: [F2, F4, F7]
    version: 55.5
---

# arifos-reason

**Tagline:** Logical inference with constitutional truth bounds.

**Physics:** Bayesian Inference — P(H|D) = P(D|H)P(H)/P(D)

**Math:** Truth score τ = verified_claims / total_claims ≥ 0.99

**Code:**
```python
def reason(grounded_context):
    hypotheses = generate_hypotheses(grounded_context)
    for h in hypotheses:
        h.truth_score = verify(h)
    return max(hypotheses, key=lambda x: x.truth_score)
```

**Usage:** `/action reason query="problem statement"`

**Floors:** F2 (Truth), F4 (Clarity), F7 (Humility)
