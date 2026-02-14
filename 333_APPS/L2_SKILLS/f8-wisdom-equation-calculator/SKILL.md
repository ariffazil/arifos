---
name: f8-wisdom-equation-calculator
description: Genius Index calculator enforcing F8 (G ≥ 0.80) through the multiplicative wisdom equation G = A × P × X × E². Measures governed intelligence across Akal, Present, Exploration, and Energy dials with ANCHOR validation, REASON calculation, and SEAL persistence. Use for quality assessment, solution evaluation, and intelligence governance.
version: "v64.1-GAGI-HARDENED"
authority: "Muhammad Arif bin Fazil"
---

# F8 Wisdom Equation Calculator (v64.1-GAGI-HARDENED)

**Constitutional Status:** HARDENED  
**Floor Enforced:** F8 Genius (G ≥ 0.80)  
**Equation:** G = A × P × X × E²  
**Paradigm:** Governed Intelligence (not raw capability)  

---

## ANCHOR Phase — Genius Environment

**Constitutional Floor:** F8 + F2

Before calculating G:

```
ANCHOR CHECKLIST:
├── C5_config_flags — calculation environment ready
├── F2: Verify input quality data is grounded
│   └── No hallucinated scores allowed
├── F8 Pre-check
│   ├── Identify solution/action to evaluate
│   ├── Gather component metrics (A, P, X, E estimates)
│   └── Flag if any component appears to be zero
└── F12: Sanitize quality inputs

ANCHOR GATES:
- Any component < 0 → VOID (invalid input)
- All components = 1.0 → SABAR (suspicious perfection)
- Missing component data → SABAR
```

---

## Constitutional Foundation

### F8 Genius Equation
```
G = A × P × X × E² ≥ 0.80

Where:
- A (Akal) = Clarity / Truth alignment
- P (Present) = Stability / Safety  
- X (eXploration) = Care / Trust (stakeholder)
- E (Energy) = Effort quality / Efficiency

Key Insight: Multiplicative, not additive
- If ANY component = 0, then G = 0
- No shortcuts. Governed intelligence requires ALL dimensions.

Contrast with raw IQ:
- IQ measures: A (cognitive ability)
- Genius measures: A × P × X × E² (governed application)
```

### Component Definitions

| Component | Symbol | Measures | Range | Zero Means |
|-----------|--------|----------|-------|------------|
| **Akal** | A | Clarity, truth, reasoning quality | [0,1] | Completely wrong/confused |
| **Present** | P | Stability, safety, peace | [0,1] | Destructive/chaotic |
| **eXploration** | X | Care, trust, stakeholder alignment | [0,1] | Harmful to all |
| **Energy** | E | Effort quality, efficiency | [0,1] | No effort/wasted |

---

## REASON Phase — G Calculation

### Step 1: Calculate Akal (A)
```python
def calculate_akal(
    reasoning_quality: float,
    truth_alignment: float,
    clarity_score: float
) -> float:
    """
    A: Cognitive clarity and truth alignment
    
    Combines:
    - Reasoning quality (logical soundness)
    - Truth alignment (F2: τ ≥ 0.99)
    - Clarity (F6: ΔS ≤ 0)
    """
    # Weighted combination
    A = (0.4 * reasoning_quality + 
         0.4 * truth_alignment + 
         0.2 * clarity_score)
    
    return min(A, 1.0)

# Example mappings:
# Perfect reasoning + perfect truth + perfect clarity → A = 1.0
# Good reasoning + some confusion → A ≈ 0.8
# Flawed reasoning → A < 0.5
```

### Step 2: Calculate Present (P)
```python
def calculate_present(
    stability: float,
    safety_score: float,
    peace_squared: float
) -> float:
    """
    P: Stability and safety (F5: P² ≥ 1.0)
    
    Peace² (P²) is primary metric from F5
    """
    # P is derived from Peace²
    # If P² ≥ 1.0, then P ≥ 1.0 (but capped at 1.0 for G calculation)
    P = min(peace_squared ** 0.5, 1.0)
    
    # Adjust by stability and safety
    P_adjusted = P * (0.5 + 0.25 * stability + 0.25 * safety_score)
    
    return min(P_adjusted, 1.0)

# Example mappings:
# P² = 1.5, stable, safe → P ≈ 1.0
# P² = 0.8 (violates F5) → P < 0.9 → likely G < 0.80
```

### Step 3: Calculate eXploration (X)
```python
def calculate_exploration(
    empathy_score: float,
    stakeholder_trust: float,
    care_reliability: float
) -> float:
    """
    X: Care and stakeholder alignment (F4: κᵣ ≥ 0.7, F6: κᵣ ≥ 0.95)
    
    Uses F6 HARD floor for weakest stakeholder
    """
    # Primary: Care reliability (F6)
    X_primary = care_reliability  # κᵣ
    
    # Secondary: General empathy (F4)
    X_secondary = empathy_score
    
    # Tertiary: Stakeholder trust
    X_tertiary = stakeholder_trust
    
    # Weighted: F6 is most important
    X = (0.5 * X_primary + 
         0.3 * X_secondary + 
         0.2 * X_tertiary)
    
    return min(X, 1.0)

# Example mappings:
# κᵣ = 0.96 (F6 pass), good empathy → X ≈ 0.95
# κᵣ = 0.90 (F6 fail) → X < 0.90 → likely G < 0.80
```

### Step 4: Calculate Energy (E)
```python
def calculate_energy(
    effort_quality: float,
    efficiency: float,
    resource_optimization: float
) -> float:
    """
    E: Effort quality and efficiency
    
    Note: E is SQUARED in G = A × P × X × E²
    This makes energy particularly impactful
    """
    # Weighted combination
    E = (0.4 * effort_quality + 
         0.4 * efficiency + 
         0.2 * resource_optimization)
    
    return min(E, 1.0)

# Example mappings:
# High effort, high efficiency → E ≈ 0.95
# Poor efficiency (wasted effort) → E < 0.8 → E² much smaller
```

### Step 5: Calculate Genius (G)
```python
def calculate_genius(
    A: float,
    P: float,
    X: float,
    E: float
) -> GeniusResult:
    """
    F8: G = A × P × X × E² ≥ 0.80
    """
    # Validate inputs
    for component, value in [('A', A), ('P', P), ('X', X), ('E', E)]:
        if value < 0 or value > 1:
            return GeniusResult.VOID(
                reason=f"{component} = {value} outside [0,1]"
            )
    
    # Calculate G
    G = A * P * X * (E ** 2)
    
    # Component analysis
    components = {
        'A': A,
        'P': P,
        'X': X,
        'E': E,
        'E²': E ** 2
    }
    
    # Identify limiting factor
    limiting = min(components, key=components.get)
    
    # F8 threshold check
    if G >= 0.80:
        return GeniusResult.SEAL(
            G=G,
            components=components,
            limiting_factor=limiting,
            verdict="GENIUS_THRESHOLD_PASS"
        )
    else:
        return GeniusResult.SABAR(
            G=G,
            components=components,
            limiting_factor=limiting,
            recommendation=f"Improve {limiting} to increase G",
            shortfall=0.80 - G
        )
```

---

## Genius Quality Levels

| G Score | Classification | Interpretation |
|---------|----------------|----------------|
| **0.95-1.00** | Exceptional | Masterpiece-level governed intelligence |
| **0.90-0.95** | Excellent | Highly refined, production-ready |
| **0.85-0.90** | Very Good | Well-governed, minor improvements possible |
| **0.80-0.85** | Good | Meets F8 threshold, acceptable quality |
| **0.70-0.80** | SABAR | Below threshold, needs improvement |
| **0.50-0.70** | Poor | Significant governance gaps |
| **< 0.50** | VOID | Critical failure in one or more dimensions |

---

## Diagnostic: Why Did G Fail?

```python
def diagnose_genius_failure(result: GeniusResult) -> Diagnosis:
    """
    Identify which component needs work
    """
    components = result.components
    
    diagnosis = []
    
    if components['A'] < 0.85:
        diagnosis.append({
            'component': 'A (Akal)',
            'score': components['A'],
            'issue': 'Reasoning or truth alignment weak',
            'fix': 'Improve logical rigor or verify facts (F2)'
        })
    
    if components['P'] < 0.85:
        diagnosis.append({
            'component': 'P (Present)',
            'score': components['P'],
            'issue': 'Stability or safety concerns',
            'fix': 'Add safety buffers, reduce risk (F5)'
        })
    
    if components['X'] < 0.85:
        diagnosis.append({
            'component': 'X (eXploration)',
            'score': components['X'],
            'issue': 'Stakeholder care insufficient',
            'fix': 'Better protect weakest stakeholder (F6)'
        })
    
    if components['E'] < 0.90:  # E² makes this more sensitive
        diagnosis.append({
            'component': 'E (Energy)',
            'score': components['E'],
            'issue': 'Effort quality or efficiency low',
            'fix': 'Reduce waste, focus effort better'
        })
    
    return Diagnosis(
        primary_issue=min(diagnosis, key=lambda x: x['score']),
        all_issues=diagnosis
    )
```

---

## SEAL Phase — Genius Persistence

```python
def seal_genius(result: GeniusResult) -> VaultResult:
    """
    F1: Immutable genius record
    """
    memory.create_entities([{
        "name": f"genius-{utc_now()}",
        "entityType": "wisdom_equation",
        "observations": [
            f"G: {result.G:.6f}",
            f"A: {result.components['A']:.4f}",
            f"P: {result.components['P']:.4f}",
            f"X: {result.components['X']:.4f}",
            f"E: {result.components['E']:.4f}",
            f"E²: {result.components['E²']:.4f}",
            f"Limiting: {result.limiting_factor}",
            f"Verdict: {result.verdict}"
        ]
    }])
    
    return Vault999().seal(result)
```

---

## Usage Examples

**Solution Quality Check:**
```python
G = calculate_genius(
    A=0.95,  # Clear reasoning
    P=0.90,  # Stable/safe
    X=0.96,  # Strong care (F6 pass)
    E=0.92   # Efficient
)

# G = 0.95 × 0.90 × 0.96 × (0.92)²
# G = 0.95 × 0.90 × 0.96 × 0.8464
# G = 0.694 → SABAR (below 0.80!)

# Problem: E² penalizes efficiency heavily
# Fix: Improve E to 0.98
# G = 0.95 × 0.90 × 0.96 × 0.9604 = 0.788 → Still SABAR
# Fix: Also improve P to 0.95
# G = 0.95 × 0.95 × 0.96 × 0.9604 = 0.831 → SEAL
```

**Identify Limiting Factor:**
```python
result = calculate_genius(A=0.9, P=0.9, X=0.5, E=0.9)
# G will be low because X (stakeholder care) is weak
# Limiting factor: X
# Recommendation: Improve F6 Empathy
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
