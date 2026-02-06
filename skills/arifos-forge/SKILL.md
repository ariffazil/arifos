# arifos-forge

## Tagline
Reduce entropy, refine output, cool structure (888_HOLD)

## Description
FORGE reduces entropy and refines output. The cooling process.

## Physics
Simulated Annealing — T → 0 for global minimum
Renormalization Group — coarse-graining fluctuations

## Math
Optimization: min f(x) s.t. g(x) ≤ 0

## Code
```python
def forge(draft_output, temperature_schedule):
    T = temperature_schedule.initial
    while T > T_final:
        neighbor = perturb(current_state, T)
        if delta_E < 0 or random() < exp(-delta_E / T):
            current_state = neighbor
        T = T * cooling_rate
    return RefinedOutput(content=current_state)
```

## Floors
- F4 (Clarity)
- F7 (Humility)
- F8 (Genius)

## Usage
/action forge draft="raw output"

## Version
1.0.0
