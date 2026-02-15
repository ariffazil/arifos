---
name: f3-tri-witness-consensus
description: Tri-Witness consensus calculator enforcing F3 (W₃ ≥ 0.95) through geometric mean of Human × AI × System witnesses. Implements consensus theory with ANCHOR validation, REASON calculation, and SEAL persistence. Merged from f3-tri-witness-consensus + tri-witness-validator. Use for all constitutional validation requiring multi-source consensus.
version: "v64.1-GAGI-HARDENED"
authority: "Muhammad Arif bin Fazil"
---

# F3 Tri-Witness Consensus (v64.1-GAGI-HARDENED)

**Constitutional Status:** HARDENED  
**Floor Enforced:** F3 (Tri-Witness W₃ ≥ 0.95)  
**Formula:** W₃ = (w₁ × w₂ × w₃)^(1/3)  
**Witnesses:** Human + AI/Institutional + Earth/System  

---

## ANCHOR Phase — Witness Validation

**Constitutional Floor:** F12 + F2

Before calculating consensus:

```
ANCHOR CHECKLIST:
├── C5_config_flags — validation environment ready
├── F12: Verify witness inputs are untampered
│   ├── Check input signatures (if available)
│   └── Sanitize witness scores (must be ∈ [0,1])
├── F2: Verify each witness has grounding
│   ├── Human: stakeholder identification valid?
│   ├── AI: reasoning trace available?
│   └── System: evidence chain intact?
└── F10: Lock witness definitions
    ├── Human = entity with suffering capacity
    ├── AI = constitutional reasoning engine
    └── System = observable evidence/physics
```

**ANCHOR Gates:**
- Witness score outside [0,1] → VOID (F12)
- Missing grounding → SABAR (F2)
- Only 1-2 witnesses → VOID (F3 requires 3)

---

## The Tri-Witness Formula

```
W₃ = (w_human × w_ai × w_system)^(1/3) ≥ 0.95

Why geometric mean?
- Arithmetic mean: one strong witness can mask weak ones
- Geometric mean: ALL witnesses must be strong
- If any witness = 0, W₃ = 0 (no shortcuts)

Example:
- w_human = 0.99, w_ai = 0.99, w_system = 0.50
- Arithmetic: (0.99 + 0.99 + 0.50) / 3 = 0.83
- Geometric: (0.99 × 0.99 × 0.50)^(1/3) = 0.79 ← FAILS F3
```

---

## REASON Phase — Consensus Calculation

### Step 1: Gather Witnesses
```python
def gather_witnesses(context: Dict) -> WitnessSet:
    """
    Collect three validated witnesses
    """
    return WitnessSet(
        human=calculate_human_witness(context['stakeholders']),
        ai=calculate_ai_witness(context['reasoning']),
        system=calculate_system_witness(context['evidence'])
    )

def calculate_human_witness(stakeholders: List) -> float:
    """
    Human witness = weakest stakeholder confidence
    F4 Empathy: protect the most vulnerable
    """
    if not stakeholders:
        return 0.0
    
    # Find weakest (most vulnerable) stakeholder
    weakest = min(stakeholders, key=lambda s: s.confidence)
    return weakest.confidence  # This is our human witness

def calculate_ai_witness(reasoning: ReasoningResult) -> float:
    """
    AI witness = truth score of reasoning
    F2: τ ≥ 0.99 for full confidence
    """
    # Base on F2 truth score
    base_score = reasoning.truth_score
    
    # Adjust by clarity (F6)
    clarity_bonus = 1.0 + reasoning.clarity_gain  # clarity_gain ≤ 0
    
    # Adjust by humility (F7)
    humility_factor = 1.0 - reasoning.omega_0  # omega_0 ∈ [0.03, 0.05]
    
    return min(base_score * clarity_bonus * humility_factor, 1.0)

def calculate_system_witness(evidence: EvidenceResult) -> float:
    """
    System witness = evidence consensus
    F2: Ground truth verification
    """
    if not evidence.verified_sources:
        return 0.0
    
    # Consensus among verified sources
    return len(evidence.verified_sources) / max(len(evidence.all_sources), 1)
```

### Step 2: Calculate W₃
```python
def calculate_tri_witness(witnesses: WitnessSet) -> TriWitnessResult:
    """
    F3: Geometric mean of three witnesses
    """
    # Geometric mean
    product = witnesses.human * witnesses.ai * witnesses.system
    w3 = product ** (1/3)
    
    # Component analysis
    components = {
        'w_human': witnesses.human,
        'w_ai': witnesses.ai,
        'w_system': witnesses.system,
        'product': product,
        'W3': w3
    }
    
    # F3 threshold check
    if w3 >= 0.95:
        return TriWitnessResult.SEAL(
            W3=w3,
            components=components,
            verdict="CONSENSUS_ACHIEVED"
        )
    elif w3 >= 0.80:
        return TriWitnessResult.SABAR(
            W3=w3,
            components=components,
            recommendation="Strengthen weakest witness",
            weakest=min(components, key=components.get)
        )
    else:
        return TriWitnessResult.VOID(
            W3=w3,
            components=components,
            reason="F3: Tri-Witness below acceptable threshold"
        )
```

### Step 3: Identify Weakness
```python
def analyze_witness_gap(result: TriWitnessResult) -> GapAnalysis:
    """
    REASON: Identify which witness needs strengthening
    """
    components = result.components
    
    gaps = []
    
    if components['w_human'] < 0.95:
        gaps.append({
            'witness': 'human',
            'current': components['w_human'],
            'target': 0.95,
            'improvement': 'Better stakeholder engagement or care protocols'
        })
    
    if components['w_ai'] < 0.95:
        gaps.append({
            'witness': 'ai',
            'current': components['w_ai'],
            'target': 0.95,
            'improvement': 'Improve reasoning clarity or reduce overconfidence'
        })
    
    if components['w_system'] < 0.95:
        gaps.append({
            'witness': 'system',
            'current': components['w_system'],
            'target': 0.95,
            'improvement': 'Gather more evidence or verify sources'
        })
    
    return GapAnalysis(gaps=gaps, priority=min(gaps, key=lambda x: x['current']))
```

---

## Consensus Retry Protocol

```python
def retry_with_improvement(
    previous: TriWitnessResult,
    context: Dict
) -> TriWitnessResult:
    """
    One retry allowed for SABAR results
    """
    if previous.verdict != "SABAR":
        return previous  # Only retry SABAR
    
    analysis = analyze_witness_gap(previous)
    weakest = analysis.priority
    
    # Strengthen weakest witness
    if weakest['witness'] == 'human':
        context['stakeholders'] = enhance_stakeholder_care(context)
    elif weakest['witness'] == 'ai':
        context['reasoning'] = improve_reasoning_clarity(context)
    elif weakest['witness'] == 'system':
        context['evidence'] = gather_additional_evidence(context)
    
    # Recalculate
    witnesses = gather_witnesses(context)
    return calculate_tri_witness(witnesses)
```

---

## SEAL Phase — Consensus Persistence

```python
def seal_consensus(result: TriWitnessResult, context: Dict) -> VaultResult:
    """
    F1: Immutable consensus record
    """
    # Memory entity
    memory.create_entities([{
        "name": f"consensus-{utc_now()}",
        "entityType": "tri_witness_consensus",
        "observations": [
            f"W3: {result.W3:.6f}",
            f"w_human: {result.components['w_human']:.4f}",
            f"w_ai: {result.components['w_ai']:.4f}",
            f"w_system: {result.components['w_system']:.4f}",
            f"Verdict: {result.verdict}",
            f"Weakest: {result.weakest if hasattr(result, 'weakest') else 'N/A'}"
        ]
    }])
    
    # Vault seal
    entry = {
        "timestamp": utc_now(),
        "W3": result.W3,
        "components": result.components,
        "verdict": result.verdict,
        "context_hash": hash_context(context)
    }
    
    return Vault999().seal(entry)
```

---

## Usage Examples

**Basic Consensus Check:**
```python
witnesses = WitnessSet(
    human=0.98,  # Strong stakeholder support
    ai=0.96,     # Clear reasoning
    system=0.97  # Solid evidence
)

result = calculate_tri_witness(witnesses)
# W3 = (0.98 × 0.96 × 0.97)^(1/3) = 0.9698 ≥ 0.95 → SEAL
```

**Failing Consensus (SABAR):**
```python
witnesses = WitnessSet(
    human=0.99,
    ai=0.99,
    system=0.70  # Weak evidence
)

result = calculate_tri_witness(witnesses)
# W3 = 0.873 < 0.95 → SABAR
# Retry with more evidence gathering
```

**Critical Failure (VOID):**
```python
witnesses = WitnessSet(
    human=0.50,  # Stakeholders harmed
    ai=0.99,
    system=0.99
)

result = calculate_tri_witness(witnesses)
# W3 = 0.793 → VOID (too low even for SABAR)
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
