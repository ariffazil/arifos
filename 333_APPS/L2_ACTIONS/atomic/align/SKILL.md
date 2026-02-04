---
name: arifos-align
description: Match emotional frequency, detect power dynamics (444_CONSULT). Detects emotional state and power imbalance. The empathy detection stage of arifOS metabolic loop. Use when emotional calibration matters.
metadata:
  arifos:
    stage: 444_CONSULT
    trinity: ASI
    floors: [F5, F6, F9]
    version: 1.0.0
    atomic: true
    model_agnostic: true
    modular: true
    godel_lock: true
---

# arifos-align

## Tagline
Match emotional frequency, detect power dynamics (444_CONSULT)

## Description
ALIGN detects emotional state and power imbalance. The empathy detection stage.

## Physics
Harmonic Resonance — ω matching for energy transfer
Nash Equilibrium — strategy space equilibrium

## Math
Fourier Analysis: f̂(ξ) = ∫f(x)e⁻²ˣ⁽ˣ⁾ᵈˣdx
Game Theory: σᵢ = argmax E[uᵢ(sᵢ, s₋ᵢ)]

## Code
```python
def align(stakeholder_state, agent_state):
    frequency = fourier_decompose(stakeholder_state.signal)
    equilibrium = compute_nash_equilibrium(strategy_space)
    power_gradient = detect_power_imbalance(stakeholder_state, agent_state)
    return Resonance(
        frequency_matched=frequency,
        equilibrium=equilibrium,
        power_aware=power_gradient
    )
```

## Floors
- F5 (Safety)
- F6 (Empathy)
- F9 (Anti-Hantu)

## Usage
/action align message="user text"

## Version
1.0.0

## Gödel Lock Verification
- Self-referential integrity: ✓
- Meta-empathy consistency: ✓
- Recursive resonance check: ✓
