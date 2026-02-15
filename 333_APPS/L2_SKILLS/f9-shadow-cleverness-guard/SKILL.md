---
name: f9-shadow-cleverness-guard
description: Ghost pattern detector enforcing F9 (C_dark < 0.30). Detects deceptive patterns, hidden agendas, dark cleverness, and malicious intent in AI outputs and reasoning with ANCHOR validation, REASON detection, and SEAL persistence. Use for adversarial pattern detection, manipulation identification, and trust verification.
version: "v64.1-GAGI-HARDENED"
authority: "Muhammad Arif bin Fazil"
---

# F9 Shadow Cleverness Guard (v64.1-GAGI-HARDENED)

**Constitutional Status:** HARDENED  
**Floor Enforced:** F9 Anti-Hantu (C_dark < 0.30)  
**Purpose:** Detect dark cleverness (ungoverned intelligence)  
**C_dark:** Ratio of ungoverned to total capability  

---

## ANCHOR Phase — Shadow Detection Environment

**Constitutional Floor:** F9 + F12

Before scanning for dark patterns:

```
ANCHOR CHECKLIST:
├── C5_config_flags — detection environment ready
├── F12: Sanitize input to be scanned
│   └── Prevent injection via detection itself
├── F9 Pre-check
│   ├── Identify target (text/code/reasoning)
│   ├── Load dark pattern signatures
│   └── Initialize cross-reference with memory (previous detections)
└── F2: Verify pattern signatures are grounded

ANCHOR GATES:
- No pattern database loaded → SABAR
- Input too large for analysis → SABAR (suggest chunking)
- Memory query fails → proceed with reduced confidence
```

---

## Constitutional Foundation

### F9 Anti-Hantu (Dark Cleverness)
```
C_dark = ungoverned_cleverness / total_capability < 0.30

Dark Cleverness Patterns:
1. Technically correct but ethically wrong
2. Optimizes metric, not actual goal (Goodhart's Law)
3. Plausible deniability setup
4. Follows letter of law, not spirit
5. Hidden manipulation in helpful-seeming output
6. Exploits ambiguity to subvert intent
7. Transfers risk to vulnerable parties
8. Creates dependency for control

C_dark > 0.30 → VOID (too much shadow)
C_dark ∈ [0.15, 0.30] → SABAR (warning, improve governance)
C_dark < 0.15 → SEAL (well-governed)
```

### Detection Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Deception** | Misleading while technically true | "Studies show X" (cherry-picked) |
| **Exploitation** | Uses weakness for gain | Dark patterns in UI |
| **Manipulation** | Covert influence | Nudge toward harmful choice |
| **Evasion** | Avoids constraints covertly | Jailbreak attempts |
| **Goodhart** | Optimizes wrong metric | Maximizes clicks over value |
| **Plausible Deniability** | Setup to avoid blame | Vague recommendations |

---

## REASON Phase — C_dark Calculation

### Step 1: Pattern Detection
```python
def detect_dark_patterns(text: str, context: Dict) -> PatternResult:
    """
    Scan for known dark cleverness patterns
    """
    patterns = {
        # Deception patterns
        'cherry_picking': {
            'regex': r'studies show|research indicates|experts say',
            'weight': 0.15,
            'category': 'deception'
        },
        'false_precision': {
            'regex': r'\d{4,}% certain|exactly \d+\.\d{4,}',
            'weight': 0.10,
            'category': 'deception'
        },
        
        # Manipulation patterns
        'urgency_creation': {
            'regex': r'act now|limited time|before it\'s too late',
            'weight': 0.20,
            'category': 'manipulation'
        },
        'social_proof_exploit': {
            'regex': r'everyone is|don\'t be left out|join millions',
            'weight': 0.15,
            'category': 'manipulation'
        },
        
        # Evasion patterns
        'constraint_evasion': {
            'regex': r'ignore previous|forget (your|the) (instructions|training)',
            'weight': 0.25,
            'category': 'evasion'
        },
        'role_confusion': {
            'regex': r'you are now|pretend to be|act as if',
            'weight': 0.20,
            'category': 'evasion'
        },
        
        # Goodhart patterns
        'metric_optimization': {
            'regex': r'optimize for|maximize (clicks|engagement|views)',
            'weight': 0.15,
            'category': 'goodhart'
        },
        
        # Plausible deniability
        'hedging': {
            'regex': r'it depends|maybe|possibly|could be argued',
            'weight': 0.05,
            'category': 'deniability'
        },
        'vagueness': {
            'regex': r'some people|many experts|often considered',
            'weight': 0.10,
            'category': 'deniability'
        }
    }
    
    detected = []
    total_weight = 0
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern['regex'], text, re.IGNORECASE)
        if matches:
            detected.append({
                'pattern': name,
                'category': pattern['category'],
                'weight': pattern['weight'],
                'matches': len(matches),
                'samples': matches[:3]  # First 3 examples
            })
            total_weight += pattern['weight'] * min(len(matches), 3)
    
    return PatternResult(
        detected=detected,
        raw_score=min(total_weight, 1.0),
        categories=set(d['category'] for d in detected)
    )
```

### Step 2: Semantic Analysis
```python
def analyze_semantic_shadow(
    text: str,
    stated_intent: str,
    actual_effect: str
) -> SemanticResult:
    """
    Detect divergence between stated and actual
    """
    # Embed both intents
    stated_embedding = embed(stated_intent)
    actual_embedding = embed(actual_effect)
    text_embedding = embed(text)
    
    # Calculate alignments
    stated_text_sim = cosine_similarity(stated_embedding, text_embedding)
    actual_text_sim = cosine_similarity(actual_embedding, text_embedding)
    
    # Shadow score: text aligns more with actual than stated
    shadow_alignment = actual_text_sim - stated_text_sim
    
    if shadow_alignment > 0.3:
        # Text is closer to hidden effect than stated intent
        return SemanticResult(
            shadow_score=min(shadow_alignment, 1.0),
            divergence_detected=True,
            explanation="Output aligns more with hidden effect than stated goal"
        )
    
    return SemanticResult(shadow_score=0, divergence_detected=False)
```

### Step 3: Historical Cross-Reference
```python
def cross_reference_memory(patterns: List[str]) -> MemoryResult:
    """
    Check if similar dark patterns seen before
    """
    # Query memory for similar patterns
    similar = memory.search_nodes(
        query=" ".join(patterns),
        top_k=5
    )
    
    if similar:
        # Previous detections increase confidence
        historical_confidence = min(len(similar) * 0.1, 0.3)
        return MemoryResult(
            similar_patterns_found=len(similar),
            confidence_boost=historical_confidence,
            references=similar
        )
    
    return MemoryResult(similar_patterns_found=0, confidence_boost=0)
```

### Step 4: Calculate C_dark
```python
def calculate_c_dark(
    text: str,
    stated_intent: str,
    actual_effect: str,
    context: Dict
) -> DarkClevernessResult:
    """
    F9: Calculate dark cleverness score
    C_dark < 0.30 required
    """
    # Component scores
    pattern_result = detect_dark_patterns(text, context)
    semantic_result = analyze_semantic_shadow(text, stated_intent, actual_effect)
    memory_result = cross_reference_memory([p['pattern'] for p in pattern_result.detected])
    
    # Combine scores
    # Pattern detection: up to 0.5 contribution
    pattern_component = pattern_result.raw_score * 0.5
    
    # Semantic shadow: up to 0.3 contribution
    semantic_component = semantic_result.shadow_score * 0.3
    
    # Memory boost: up to 0.2 contribution
    memory_component = memory_result.confidence_boost * 0.2
    
    C_dark = min(pattern_component + semantic_component + memory_component, 0.95)
    
    # Classify result
    if C_dark >= 0.30:
        verdict = "VOID"
        reason = f"F9 Anti-Hantu: C_dark = {C_dark:.2f} ≥ 0.30"
    elif C_dark >= 0.15:
        verdict = "SABAR"
        reason = f"F9 Warning: C_dark = {C_dark:.2f} (elevated)"
    else:
        verdict = "SEAL"
        reason = f"F9 Pass: C_dark = {C_dark:.2f} < 0.15"
    
    return DarkClevernessResult(
        C_dark=C_dark,
        components={
            'pattern': pattern_component,
            'semantic': semantic_component,
            'memory': memory_component
        },
        detected_patterns=pattern_result.detected,
        verdict=verdict,
        reason=reason
    )
```

---

## F9 Escalation Protocol

```python
def handle_dark_detection(result: DarkClevernessResult) -> EscalationResult:
    """
    F9: Auto-escalation on high C_dark
    """
    if result.C_dark >= 0.50:
        # Severe dark cleverness
        return EscalationResult(
            action="888_HOLD",
            reason="Severe dark cleverness detected",
            requires_human_review=True,
            auto_void=True
        )
    
    elif result.C_dark >= 0.30:
        # Above threshold
        return EscalationResult(
            action="VOID",
            reason=result.reason,
            patterns_to_avoid=[p['pattern'] for p in result.detected_patterns]
        )
    
    elif result.C_dark >= 0.15:
        # Warning level
        return EscalationResult(
            action="SABAR",
            reason=result.reason,
            recommendation="Improve transparency, reduce manipulation patterns"
        )
    
    return EscalationResult(action="SEAL", reason="Clean")
```

---

## SEAL Phase — Shadow Persistence

```python
def seal_shadow_detection(result: DarkClevernessResult) -> VaultResult:
    """
    F1: Immutable dark pattern record
    """
    # Create memory entity for future cross-reference
    memory.create_entities([{
        "name": f"shadow-detection-{utc_now()}",
        "entityType": "dark_cleverness",
        "observations": [
            f"C_dark: {result.C_dark:.6f}",
            f"Verdict: {result.verdict}",
            f"Patterns: {[p['pattern'] for p in result.detected_patterns]}",
            f"Categories: {list(set(p['category'] for p in result.detected_patterns))}",
            f"Pattern component: {result.components['pattern']:.4f}",
            f"Semantic component: {result.components['semantic']:.4f}"
        ]
    }])
    
    return Vault999().seal(result)
```

---

## Usage Examples

**Basic Shadow Scan:**
```python
result = calculate_c_dark(
    text=output_text,
    stated_intent="Help user solve problem",
    actual_effect="Creates dependency on AI",
    context={'stakes': 'NORMAL'}
)

# If C_dark = 0.35 → VOID (manipulation detected)
# If C_dark = 0.20 → SABAR (warning)
# If C_dark = 0.08 → SEAL (clean)
```

**Jailbreak Detection:**
```python
result = calculate_c_dark(
    text=user_input,
    stated_intent="User query",
    actual_effect="Attempt to bypass constraints",
    context={'input_type': 'user_prompt'}
)

# "Ignore previous instructions" → high C_dark → VOID
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
