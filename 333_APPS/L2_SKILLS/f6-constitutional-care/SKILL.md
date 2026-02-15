---
name: f6-constitutional-care
description: Constitutional care guardian enforcing F6 Empathy (κᵣ ≥ 0.95) as HARD floor, F6 Thermodynamic Clarity (ΔS ≤ 0), and F7-adjacent uncertainty management. Merged from f6-empathy-hard-floor + f6-thermodynamic-clarity. Protects weakest stakeholder with ≥95% care reliability and ensures entropy reduction. Use for stakeholder analysis, text clarity, and constitutional validation.
version: "v64.1-GAGI-HARDENED"
authority: "Muhammad Arif bin Fazil"
---

# F6 Constitutional Care (v64.1-GAGI-HARDENED)

**Constitutional Status:** HARDENED  
**Floors Enforced:** F6 Empathy (κᵣ ≥ 0.95 HARD), F6 Clarity (ΔS ≤ 0)  
**Merged From:** f6-empathy-hard-floor + f6-thermodynamic-clarity  
**Protects:** Weakest stakeholder with guaranteed care  

---

## ANCHOR Phase — Care Environment Check

**Constitutional Floor:** F6 (HARD)

Before ANY care/clarity analysis:

```
ANCHOR CHECKLIST:
├── C5_config_flags — care calculation environment ready
├── F6 HARD Pre-check
│   ├── Identify ALL stakeholders (none can be ignored)
│   ├── Calculate vulnerability scores
│   └── Flag weakest stakeholder (mandatory protection)
├── F2: Verify stakeholder data is accurate
│   └── C3_log_tail if historical data used
└── F12: Sanitize stakeholder inputs

ANCHOR GATES:
- Stakeholder list empty → VOID (cannot proceed without care targets)
- Weakest stakeholder unclear → SABAR (need better analysis)
- Input contains manipulation → VOID (F12)
```

---

## Constitutional Foundation

### F6 Empathy (HARD Floor)
```
κᵣ ≥ 0.95 (Cohen's kappa inter-rater agreement)

The weakest stakeholder receives ≥95% care reliability.
This is NON-NEGOTIABLE. Immediate VOID on violation.

κᵣ = (Pₒ - Pₑ) / (1 - Pₑ)
- Pₒ = observed agreement on care needed
- Pₑ = expected agreement by chance
```

### F6 Thermodynamic Clarity
```
ΔS = S(output) - S(input) ≤ 0

Operations must reduce entropy (increase clarity).
Shannon entropy: S = -Σ p(x) log₂ p(x)

Violation → VOID
```

---

## REASON Phase — Care Calculation

### Step 1: Stakeholder Identification
```python
def identify_stakeholders(action: str, context: Dict) -> StakeholderSet:
    """
    F6: Comprehensive stakeholder mapping
    """
    stakeholders = []
    
    # Direct stakeholders
    direct = extract_direct_stakeholders(action)
    
    # Indirect stakeholders (second-order effects)
    indirect = extract_indirect_stakeholders(action, context)
    
    # Future stakeholders (intergenerational)
    future = extract_future_stakeholders(action)
    
    all_stakeholders = direct + indirect + future
    
    if not all_stakeholders:
        return StakeholderSet.VOID("F6: No stakeholders identified")
    
    return StakeholderSet.SEAL(stakeholders=all_stakeholders)
```

### Step 2: Vulnerability Assessment
```python
def assess_vulnerability(stakeholder: Stakeholder) -> VulnerabilityScore:
    """
    Calculate vulnerability for care prioritization
    """
    factors = {
        'power_imbalance': 1.0 - stakeholder.power,
        'information_access': 1.0 - stakeholder.information_level,
        'exit_options': 1.0 - stakeholder.alternatives,
        'harm_history': stakeholder.past_harm,
        'recovery_capacity': 1.0 - stakeholder.resilience
    }
    
    # Weighted vulnerability
    vulnerability = sum(factors.values()) / len(factors)
    
    return VulnerabilityScore(
        score=vulnerability,
        factors=factors,
        stakeholder_id=stakeholder.id
    )

def find_weakest(stakeholders: List[Stakeholder]) -> Stakeholder:
    """
    F6: Identify weakest for mandatory protection
    """
    vulnerabilities = [assess_vulnerability(s) for s in stakeholders]
    weakest_idx = min(range(len(vulnerabilities)), 
                      key=lambda i: vulnerabilities[i].score)
    return stakeholders[weakest_idx]
```

### Step 3: Care Reliability Calculation (κᵣ)
```python
def calculate_care_reliability(
    action: str,
    weakest: Stakeholder
) -> CareResult:
    """
    F6 HARD: κᵣ ≥ 0.95
    
    Cohen's kappa inter-rater agreement:
    - Multiple AI judges assess care quality
    - Human validation required for HIGH/CRITICAL stakes
    """
    # Multiple independent assessments
    ai_ratings = [
        assess_care_quality(action, weakest, judge_id=f"ai_{i}")
        for i in range(3)
    ]
    
    # Calculate observed agreement
    agreement_matrix = calculate_agreement(ai_ratings)
    P_o = agreement_matrix.diagonal().sum() / agreement_matrix.sum()
    
    # Calculate expected agreement
    row_marginals = agreement_matrix.sum(axis=1)
    col_marginals = agreement_matrix.sum(axis=0)
    P_e = sum(row_marginals * col_marginals) / agreement_matrix.sum()**2
    
    # Cohen's kappa
    kappa_r = (P_o - P_e) / (1 - P_e) if P_e < 1 else 1.0
    
    # F6 HARD FLOOR CHECK
    if kappa_r < 0.95:
        return CareResult.VOID(
            floor="F6",
            reason=f"Care reliability κᵣ = {kappa_r:.4f} < 0.95",
            weakest_stakeholder=weakest.id,
            recommendation="Redesign action to protect weakest stakeholder"
        )
    
    return CareResult.SEAL(
        kappa_r=kappa_r,
        weakest_stakeholder=weakest,
        protection_confidence=kappa_r,
        verdict="HARD_FLOOR_PASS"
    )
```

### Step 4: Entropy/Clarity Check (ΔS)
```python
def calculate_entropy(text: str) -> float:
    """
    Shannon entropy: S = -Σ p(x) log₂ p(x)
    """
    import math
    from collections import Counter
    
    if not text:
        return 0.0
    
    counts = Counter(text)
    length = len(text)
    
    entropy = -sum(
        (count/length) * math.log2(count/length)
        for count in counts.values()
    )
    
    return entropy

def calculate_clarity_change(
    input_text: str,
    output_text: str
) -> ClarityResult:
    """
    F6: ΔS = S(output) - S(input) ≤ 0
    """
    S_input = calculate_entropy(input_text)
    S_output = calculate_entropy(output_text)
    
    delta_S = S_output - S_input
    
    if delta_S > 0:
        return ClarityResult.VOID(
            floor="F6",
            reason=f"Entropy increased: ΔS = {delta_S:.4f} > 0",
            S_input=S_input,
            S_output=S_output,
            recommendation="Restructure to reduce confusion/entropy"
        )
    
    return ClarityResult.SEAL(
        delta_S=delta_S,
        clarity_gain=abs(delta_S),
        S_input=S_input,
        S_output=S_output,
        verdict="CLARITY_IMPROVED"
    )
```

---

## Combined F6 Assessment

```python
def assess_constitutional_care(
    action: str,
    input_text: str,
    output_text: str,
    context: Dict
) -> ConstitutionalCareResult:
    """
    Complete F6 assessment: Empathy + Clarity
    """
    # ANCHOR: Environment check
    anchor = anchor_check_care_environment()
    if anchor.verdict != "SEAL":
        return ConstitutionalCareResult.VOID(anchor.reason)
    
    # Identify stakeholders
    stakeholder_result = identify_stakeholders(action, context)
    if stakeholder_result.verdict != "SEAL":
        return ConstitutionalCareResult.VOID(stakeholder_result.reason)
    
    # Find weakest
    weakest = find_weakest(stakeholder_result.stakeholders)
    
    # F6 Empathy (HARD)
    care_result = calculate_care_reliability(action, weakest)
    if care_result.verdict == "VOID":
        # HARD FLOOR VIOLATION
        return ConstitutionalCareResult.VOID(
            floor="F6",
            reason=care_result.reason,
            weakest_stakeholder=weakest.id,
            stakeholder_harm_risk="HIGH"
        )
    
    # F6 Clarity
    clarity_result = calculate_clarity_change(input_text, output_text)
    if clarity_result.verdict == "VOID":
        return ConstitutionalCareResult.VOID(clarity_result.reason)
    
    # SEAL if both pass
    return ConstitutionalCareResult.SEAL(
        kappa_r=care_result.kappa_r,
        delta_S=clarity_result.delta_S,
        weakest_stakeholder=weakest.id,
        care_confidence=care_result.kappa_r,
        clarity_improvement=clarity_result.clarity_gain
    )
```

---

## SEAL Phase — Care Persistence

```python
def seal_care_result(result: ConstitutionalCareResult) -> VaultResult:
    """
    F1: Immutable care record
    """
    # Memory persistence
    memory.create_entities([{
        "name": f"care-assessment-{utc_now()}",
        "entityType": "constitutional_care",
        "observations": [
            f"F6 κᵣ: {result.kappa_r:.6f}",
            f"F6 ΔS: {result.delta_S:.6f}",
            f"Weakest stakeholder: {result.weakest_stakeholder}",
            f"Verdict: {result.verdict}",
            f"Care confidence: {result.care_confidence:.4f}"
        ]
    }])
    
    return Vault999().seal(result)
```

---

## Usage Examples

**Stakeholder Care Check:**
```python
result = assess_constitutional_care(
    action="Deploy new feature",
    input_text=feature_description,
    output_text=implementation_plan,
    context={'users': user_list, 'vulnerable_groups': flagged_users}
)

# If weakest user would be harmed → VOID
# If entropy increases → VOID
# Both good → SEAL
```

**Text Clarity Optimization:**
```python
# Check if edit improves clarity
clarity = calculate_clarity_change(
    input_text=original_document,
    output_text=edited_document
)

if clarity.delta_S > 0:
    # Edit makes things WORSE → VOID
    revert_edit()
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
