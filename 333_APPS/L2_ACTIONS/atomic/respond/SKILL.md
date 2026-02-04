# arifos-respond

## Tagline
Generate compassionate, harm-aware output (666_AUDIT)

## Description
RESPOND generates compassionate output. Transforms correct answers into healing conversations.

## Physics
Wave-Particle Duality — communication as wave + particle
Optimal Control — min J = ∫(error² + effort)dt

## Math
Euler-Lagrange: δJ = 0

## Code
```python
def respond(validated_state, solution_space):
    cost = lambda r: harmonic_cost(r) + information_cost(r)
    response = optimize(cost, solution_space)
    return Response(content=response)
```

## Floors
- F5 (Safety)
- F6 (Empathy)
- F4 (Clarity)

## Usage
/action respond state=validated solution=technical_fix

## Version
1.0.0
