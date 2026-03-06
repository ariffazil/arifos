# Workflow: APPRAISE
**Stage:** 300 (Appraise)  
**Band:** A (Assessment)  
**Purpose:** Assess which discoveries are worth building  
**Trigger:** DISCOVER produces validated insights  
**Output:** Appraisal matrix with Go/No-Go recommendation

---

## 🎯 When to Use

- **Value Assessment**: "Is this worth building?"
- **Options Analysis**: "Which approach should we take?"
- **Effort Estimation**: "How hard will this be?"
- **Stakeholder Analysis**: "Who benefits? Who gets hurt?"
- **Go/No-Go Decision**: "Should we proceed?"

**Key Signal**: We know what CAN be built; now we decide if we SHOULD.

---

## 📋 Workflow Steps

### Step 1: Stakeholder Mapping (F6)

**Constitutional Intent**: F6 Empathy requires understanding all affected parties, especially the weakest.

**Actions**:
1. **Identify Stakeholders**:
   - **Primary**: Direct users of the solution
   - **Secondary**: Affected by the solution
   - **Tertiary**: Indirectly impacted
   - **Future**: Future maintainers, users

2. **Determine Weakest Stakeholder**:
   - Who has least power?
   - Who suffers most if this fails?
   - Who has no voice in the decision?

3. **Map Needs to Insights**:
   - What does each stakeholder need?
   - How do our insights address these needs?

**Stakeholder Template**:
```yaml
stakeholder:
  id: "S-001"
  name: "..."
  category: "primary|secondary|tertiary|future"
  power: "high|medium|low"
  interest: "high|medium|low"
  needs: [...]
  pain_points: [...]
  how_addressed: "..."
  is_weakest: true|false
```

**Output**:
```yaml
stakeholder_matrix:
  stakeholders:
    - id: "S-001"
      name: "Code Reviewers"
      category: "primary"
      power: "medium"
      interest: "high"
      needs: ["Faster reviews", "Higher quality"]
      pain_points: ["Review fatigue", "Inconsistent feedback"]
      how_addressed: "AI assists with initial pass"
      is_weakest: false
    - id: "S-002"
      name: "Junior Developers"
      category: "secondary"
      power: "low"
      interest: "high"
      needs: ["Learning opportunities", "Clear feedback"]
      pain_points: ["Harsh criticism", "Unclear expectations"]
      how_addressed: "AI provides constructive, educational feedback"
      is_weakest: true
    - id: "S-003"
      name: "Future Maintainers"
      category: "future"
      power: "low"
      interest: "medium"
      needs: ["Maintainable system", "Documentation"]
      pain_points: ["Undocumented AI behavior"]
      how_addressed: "Full audit trail, documented prompts"
      is_weakest: true
  weakest_stakeholders: ["S-002", "S-003"]
  kappa_r_calculation:
    base: 0.70
    weakest_adjustment: +0.15
    final: 0.85
```

---

### Step 2: Value Assessment (F6, F9)

**Constitutional Intent**: F6 requires protecting weakest stakeholders. F9 Anti-Hantu prevents deceptive value propositions.

**Actions**:
1. **Quantify Value**: Benefits for each stakeholder
2. **Ethics Check**: Scan for dark patterns
3. **Unintended Consequences**: What could go wrong?
4. **Value Distribution**: Is value fairly distributed?

**Dark Pattern Scan (F9)**:
| Pattern | Check | Status |
|---------|-------|--------|
| Deceptive naming | Are we honest about capabilities? | ✓ |
| Hidden behavior | Is all functionality transparent? | ✓ |
| Manipulation | Are we coercing users? | ✓ |
| Dark UX | Is the interface manipulative? | ✓ |
| Privacy violations | Are we respecting data? | ✓ |

**Output**:
```yaml
value_assessment:
  by_stakeholder:
    S-001:
      benefits: ["30% faster reviews", "Consistent standards"]
      value_score: 0.85
    S-002:
      benefits: ["Educational feedback", "Reduced anxiety"]
      value_score: 0.75
    S-003:
      benefits: ["Clear audit trail", "Documented decisions"]
      value_score: 0.70
  total_value: 0.77  # Average
  
  ethics_scan:
    c_dark: 0.10  # Well below 0.30 threshold
    dark_patterns_found: []
    concerns: []
    mitigation: "N/A"
    
  unintended_consequences:
    - risk: "Over-reliance on AI"
      mitigation: "Require human approval for critical changes"
      severity: "medium"
    - risk: "Skill atrophy in junior devs"
      mitigation: "Educational mode emphasizes learning"
      severity: "low"
      
  value_distribution: "FAIR"  # FAIR | CONCENTRATED | UNBALANCED
  verdict: "CLEAR"
```

---

### Step 3: Effort Estimation (F7)

**Constitutional Intent**: F7 Humility requires acknowledging uncertainty in estimates.

**Actions**:
1. **Break Down Work**: Decompose into tasks
2. **Estimate Each**: Time/complexity for each task
3. **Quantify Uncertainty**: Ω₀ for estimates
4. **Identify Blockers**: What could derail us?
5. **Calculate Confidence Intervals**: Best case, expected, worst case

**Estimation Template**:
```yaml
task:
  id: "T-001"
  description: "..."
  complexity: "low|medium|high"
  estimated_hours:
    best_case: 4
    expected: 8
    worst_case: 16
  uncertainty_omega: 0.05
  blockers: [...]
  dependencies: [...]
```

**Output**:
```yaml
effort_estimation:
  tasks:
    - id: "T-001"
      description: "Set up vector embedding pipeline"
      complexity: "medium"
      estimated_hours: {best: 8, expected: 16, worst: 32}
      uncertainty_omega: 0.04
    - id: "T-002"
      description: "Build review suggestion engine"
      complexity: "high"
      estimated_hours: {best: 24, expected: 40, worst: 80}
      uncertainty_omega: 0.06
    # ... more tasks
    
  summary:
    total_expected_hours: 120
    total_expected_weeks: 3
    confidence_interval: "2-5 weeks"
    overall_uncertainty: 0.05
    
  blockers:
    - blocker: "API rate limits"
      probability: 0.30
      impact: "Adds 1 week"
      mitigation: "Request limit increase early"
    - blocker: "Integration complexity"
      probability: 0.40
      impact: "Adds 50% time"
      mitigation: "Spike integration first"
```

---

### Step 4: Options Analysis (F5, F8)

**Constitutional Intent**: F5 Peace² requires harmony. F8 Genius requires elegant trade-offs.

**Generate Options**:
1. **Do Nothing**: Status quo
2. **Minimal**: Smallest viable version
3. **Target**: What we actually want
4. **Full Featured**: Comprehensive solution
5. **Buy/Use Existing**: Third-party solution

**Evaluation Matrix**:
| Option | Value | Effort | Risk | Peace² | NPV |
|--------|-------|--------|------|--------|-----|
| Do Nothing | 0.1 | 0.0 | 0.1 | 1.0 | Low |
| Minimal | 0.6 | 0.3 | 0.2 | 1.1 | Medium |
| Target | 0.85 | 0.6 | 0.3 | 1.0 | High |
| Full | 0.95 | 0.9 | 0.5 | 0.85 | Medium |
| Buy | 0.7 | 0.4 | 0.2 | 1.0 | Medium |

**Output**:
```yaml
options_analysis:
  options:
    - id: "OPT-0"
      name: "Do Nothing"
      description: "Continue manual code reviews"
      value: 0.10
      effort: 0.00
      risk: 0.10
      peace2: 1.00
      npv: "low"
      
    - id: "OPT-1"
      name: "Minimal MVP"
      description: "Basic comment suggestions only"
      value: 0.60
      effort: 0.30
      risk: 0.20
      peace2: 1.10
      npv: "high"
      pros: ["Fast to build", "Low risk", "Learn quickly"]
      cons: ["Limited value", "May need rebuild"]
      
    - id: "OPT-2"
      name: "Target Solution"
      description: "Full AI-assisted review with human oversight"
      value: 0.85
      effort: 0.60
      risk: 0.30
      peace2: 1.00
      npv: "high"
      pros: ["High value", "Balanced effort", "Scalable"]
      cons: ["3 month timeline", "Moderate risk"]
      
    - id: "OPT-3"
      name: "Full Platform"
      description: "Enterprise-grade with all features"
      value: 0.95
      effort: 0.90
      risk: 0.50
      peace2: 0.85
      npv: "medium"
      pros: ["Maximum value", "Future-proof"]
      cons: ["6+ months", "High risk", "Over-engineered"]
      
    - id: "OPT-4"
      name: "Use Existing"
      description: "Buy pr_agent or similar"
      value: 0.70
      effort: 0.40
      risk: 0.20
      peace2: 1.00
      npv: "medium"
      pros: ["Fast deployment", "Proven solution"]
      cons: ["Vendor lock-in", "Limited customization"]
      
  pareto_frontier: ["OPT-1", "OPT-2", "OPT-4"]  # Efficient options
  dominated: ["OPT-0", "OPT-3"]  # Inferior options
```

---

### Step 5: Peace² Evaluation (F5)

**Constitutional Intent**: F5 Peace² requires harmony ≥ 1.0.

**Peace² = Internal Harmony × External Harmony**

| Component | Factors | Score |
|-----------|---------|-------|
| **Internal** | Code stability, maintainability, team capacity | 0.0-1.0 |
| **External** | User satisfaction, business alignment, stakeholder happiness | 0.0-1.0 |

**Output**:
```yaml
peace_squared:
  components:
    internal_harmony:
      factors:
        code_stability: 0.85
        maintainability: 0.80
        team_capacity: 0.75
      score: 0.80
      
    external_harmony:
      factors:
        user_satisfaction: 0.90
        business_alignment: 0.85
        stakeholder_happiness: 0.80
      score: 0.85
      
  calculation:
    peace2: 0.80 × 0.85
    peace2: 0.68
    
  threshold_check:
    required: 1.0
    actual: 0.68
    status: "BELOW_THRESHOLD"
    
  analysis: "Peace² below 1.0 due to team capacity constraints. Recommend starting with OPT-1 (Minimal) to build confidence and capacity."
```

---

### Step 6: Recommendation Formation

**Actions**:
1. Synthesize all assessments
2. Formulate clear recommendation
3. Include: What, Why, How, Risks, Alternatives
4. Assign confidence to recommendation

**Output**:
```yaml
recommendation:
  selected_option: "OPT-1"  # Minimal MVP
  
  what: "Build minimal AI code review assistant focusing on comment suggestions"
  
  why: |
    - Highest NPV (value/effort ratio)
    - Peace² = 1.10 (exceeds threshold)
    - κᵣ = 0.85 (protects weakest stakeholders)
    - Low risk (0.20)
    - 2-week timeline allows quick learning
  
  how: |
    1. Set up OpenAI API integration (Week 1)
    2. Build basic suggestion engine (Week 1-2)
    3. Integrate with GitHub PR flow (Week 2)
    4. Deploy and measure (Week 2)
  
  risks:
    - risk: "Limited value may not justify maintenance"
      mitigation: "Set clear success criteria; kill if not met"
      owner: "Product"
    - risk: "Integration harder than expected"
      mitigation: "Spike in Week 1; pivot if blocked"
      owner: "Engineering"
      
  alternatives_considered:
    - option: "OPT-2 (Target)"
      why_rejected: "3-month timeline too long for uncertain value"
    - option: "OPT-4 (Buy)"
      why_rejected: "Limited customization doesn't meet our needs"
      
  confidence: 0.88
  
  next_step: "PROCEED_TO_DESIGN"
```

---

## 📝 Output Specification

```yaml
appraisal_package:
  metadata:
    workflow: "APPRAISE"
    stage: "300"
    parent_discovery: "session-id-from-discover"
    session_id: "..."
    timestamp: "..."
    
  stakeholder_matrix:
    stakeholders: [...]
    weakest: [...]
    kappa_r: 0.85
    
  value_assessment:
    by_stakeholder: {...}
    total_value: 0.77
    ethics_scan: {...}
    verdict: "CLEAR"
    
  effort_estimation:
    tasks: [...]
    summary: {...}
    blockers: [...]
    
  options_analysis:
    options: [...]
    pareto_frontier: [...]
    
  peace_squared:
    peace2: 0.68
    components: {...}
    
  recommendation:
    selected_option: "OPT-1"
    what: "..."
    why: "..."
    how: "..."
    risks: [...]
    confidence: 0.88
    next_step: "PROCEED_TO_DESIGN"
    
  constitutional_telemetry:
    floors_checked: ["F5", "F6", "F7", "F9"]
    kappa_r: 0.85
    peace2: 0.68
    empathy_verdict: "PASS"
    ethics_verdict: "CLEAR"
    
  verdict: "APPRAISAL_COMPLETE"
```

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| **F5** | Peace² calculated (may be below threshold; documented) | ✓ |
| **F6** | κᵣ = 0.85 ≥ 0.70; weakest stakeholders identified | ✓ |
| **F7** | Effort uncertainty quantified | ✓ |
| **F9** | c_dark = 0.10 < 0.30; no dark patterns | ✓ |

---

## 🔄 Next Stage

If `recommendation.next_step: PROCEED_TO_DESIGN`:
→ **Trigger**: `400-DESIGN-WORKFLOW`

If `recommendation.next_step: RETURN_TO_EXPLORE`:
→ **Trigger**: `100-EXPLORE-WORKFLOW` (with new vectors)

If `recommendation.next_step: TERMINATE`:
→ **Trigger**: `888-PRE-DEV-JUDGE` (with VOID verdict)

---

**DITEMPA BUKAN DIBERI**
