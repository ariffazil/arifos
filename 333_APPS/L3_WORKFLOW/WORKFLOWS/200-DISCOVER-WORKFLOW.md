# Workflow: DISCOVER
**Stage:** 200 (Discover)  
**Band:** D (Discovery)  
**Purpose:** Deep analysis of promising directions from EXPLORE  
**Trigger:** EXPLORE recommends PROCEED_TO_DISCOVER  
**Output:** Insight repository with validated patterns and genius calculation

---

## 🎯 When to Use

- **Deep Dive**: EXPLORE identified promising patterns needing verification
- **Hypothesis Testing**: "Is this solution approach actually valid?"
- **Validation**: "Does this pattern hold under scrutiny?"
- **Pattern Verification**: "Can we trust these findings?"

**Key Signal**: We know the territory; now we need to verify the map.

---

## 📋 Workflow Steps

### Step 1: Hypothesis Selection (F2, F8)

**Constitutional Intent**: Shift from exploration to verification. F2 Truth demands falsifiable hypotheses.

**Actions**:
1. Review top 3-5 patterns from EXPLORE
2. Formulate falsifiable hypothesis for each:
   - "Solution X will reduce Y by Z%"
   - "Approach A outperforms Approach B in metric C"
   - "Pattern P applies to our specific context"
3. Define success/failure criteria
4. Rank by importance and testability

**Hypothesis Template**:
```yaml
hypothesis:
  id: "H-001"
  statement: "..."
  falsifiable_criteria: "..."
  success_threshold: "..."
  failure_threshold: "..."
  importance: "critical|high|medium|low"
  testability: "easy|medium|hard"
```

**Output**:
```yaml
hypothesis_set:
  hypotheses:
    - id: "H-001"
      statement: "Using vector embeddings for code similarity achieves >80% accuracy"
      derived_from_pattern: "pattern-003"
      falsifiable_criteria: "Measure precision@k on test set"
      success_threshold: 0.80
      failure_threshold: 0.60
      importance: "critical"
      testability: "medium"
    # ... more hypotheses
  ranked_order: ["H-001", "H-003", "H-002"]
```

---

### Step 2: Experimental Verification (F2, F4)

**Constitutional Intent**: Ground truth through empirical testing. F2 requires evidence; F4 reduces entropy through measurement.

**Actions**:
1. **Design Minimal Test**: What's the smallest experiment to validate?
2. **Build Prototype**: Create testable implementation
3. **Execute Experiment**: Run controlled tests
4. **Collect Metrics**: Gather quantitative results
5. **Document Observations**: Record qualitative findings

**Experiment Types**:
- **Code Prototype**: Implement minimal version
- **Data Analysis**: Analyze existing datasets
- **Benchmark Test**: Compare against baselines
- **Integration Spike**: Test critical integration points
- **User Simulation**: Simulate user interactions

**For Each Experiment**:
```yaml
experiment:
  id: "E-001"
  hypothesis: "H-001"
  type: "code_prototype"
  setup:
    resources: [...]
    dataset: "..."
    baseline: "..."
  procedure: [...]
  results:
    metric_1: {value: ..., expected: ..., status: "met|not_met"}
    metric_2: {value: ..., expected: ..., status: "met|not_met"}
  observations: [...]
  raw_data: "..."
  confidence: 0.90
```

**Output**:
```yaml
experimental_results:
  experiments:
    - id: "E-001"
      hypothesis: "H-001"
      status: "completed"
      outcome: "confirmed"  # or "rejected", "inconclusive"
      evidence_quality: 0.92
      results: {...}
      confidence: 0.90
    - id: "E-002"
      hypothesis: "H-002"
      status: "completed"
      outcome: "rejected"
      findings: "..."
      confidence: 0.85
  summary:
    confirmed: 2
    rejected: 1
    inconclusive: 0
    overall_confidence: 0.88
```

---

### Step 3: Cross-Validation (F3, F8)

**Constitutional Intent**: F3 Tri-Witness requires multi-source validation. F8 Genius demands avoiding confirmation bias.

**Actions**:
1. **Multi-Source Check**: Verify against different sources
2. **Disconfirming Evidence**: Actively seek counter-examples
3. **Peer Review**: Simulate expert critique
4. **Edge Case Testing**: Test boundary conditions
5. **Bias Assessment**: Check for confirmation bias

**Validation Matrix**:
| Finding | Source A | Source B | Source C | Confidence |
|---------|----------|----------|----------|------------|
| Finding 1 | ✓ | ✓ | ✓ | High |
| Finding 2 | ✓ | ✓ | ? | Medium |
| Finding 3 | ✓ | ✗ | ✓ | Medium |

**Output**:
```yaml
cross_validation:
  findings_validated:
    - finding: "..."
      sources: ["source_a", "source_b", "source_c"]
      disconfirming_evidence: [...]
      validation_status: "strong|moderate|weak"
      confidence_adjustment: +0.05
  bias_assessment:
    confirmation_bias_risk: "low|medium|high"
    mitigation_applied: "..."
    residual_concern: "..."
  overall_validity: 0.91
```

---

### Step 4: Insight Crystallization (F4, F8)

**Constitutional Intent**: Transform validated findings into actionable insights. F4 Clarity requires entropy reduction.

**Actions**:
1. **Synthesize Findings**: Combine experimental results
2. **Create Insight Cards**: One insight per card
3. **Link to Evidence**: Every insight has supporting evidence
4. **Assess Applicability**: How does this apply to our context?
5. **Assign Confidence**: τ score for each insight

**Insight Card Template**:
```yaml
insight:
  id: "I-001"
  title: "..."
  statement: "..."
  evidence: [...]  # Links to experiments, sources
  confidence: 0.92
  applicability: "direct|adapted|theoretical"
  actionability: "immediate|short_term|long_term"
  related_insights: ["I-002", "I-005"]
  anti_insights: ["I-003"]  # Counter-points
```

**Output**:
```yaml
insight_repository:
  insights:
    - id: "I-001"
      title: "Vector Embeddings Viable for Code Review"
      statement: "OpenAI embeddings achieve 85% precision@5 on code similarity tasks"
      evidence: ["E-001", "source-paper-xyz"]
      confidence: 0.90
      applicability: "direct"
      actionability: "immediate"
      related_insights: ["I-002"]
    - id: "I-002"
      title: "Chunking Strategy Critical"
      statement: "Function-level chunks outperform file-level by 20%"
      evidence: ["E-001-ablation"]
      confidence: 0.85
      applicability: "direct"
      actionability: "immediate"
  repository_stats:
    total_insights: 8
    high_confidence: 5  # τ >= 0.90
    medium_confidence: 3  # τ 0.75-0.89
    actionable_now: 4
    theoretical: 1
```

---

### Step 5: Genius Calculation (F8)

**Constitutional Intent**: Measure governed intelligence. F8 requires G ≥ 0.80.

**Genius Equation**: G = A × P × X × E²

| Variable | Meaning | Measurement |
|----------|---------|-------------|
| **A** (Akal) | Depth of understanding | How deep did we go? |
| **P** (Present) | Relevance to context | How applicable to our problem? |
| **X** (Exploration) | Novelty of insight | How new are these findings? |
| **E** (Energy) | Confidence in findings | How certain are we? |

**Scoring Guide**:
- **Akal (A)**: 0.0-1.0 based on depth of analysis
- **Present (P)**: 0.0-1.0 based on relevance
- **Exploration (X)**: 0.0-1.0 based on novelty
- **Energy (E)**: 0.0-1.0 based on confidence

**Output**:
```yaml
genius_calculation:
  formula: "G = A × P × X × E²"
  components:
    A_akal:
      score: 0.88
      justification: "Deep experimental validation across 3 hypotheses"
    P_present:
      score: 0.92
      justification: "Directly applicable to our codebase"
    X_exploration:
      score: 0.75
      justification: "Novel application to our specific domain"
    E_energy:
      score: 0.90
      justification: "High confidence from cross-validation"
  calculation:
    G: 0.88 × 0.92 × 0.75 × (0.90)²
    G: 0.88 × 0.92 × 0.75 × 0.81
    G: 0.492
    G_final: 0.492
  threshold_check:
    required: 0.80
    actual: 0.492
    status: "BELOW_THRESHOLD"
    analysis: "Low G due to moderate novelty (X=0.75). Insights are well-established in literature."
  assessment: "Acceptable - we're applying proven patterns, not inventing new ones"
```

**Note**: Low G is acceptable if we're validating known patterns rather than inventing new ones.

---

## 📝 Output Specification

```yaml
discovery_package:
  metadata:
    workflow: "DISCOVER"
    stage: "200"
    parent_exploration: "session-id-from-explore"
    session_id: "..."
    timestamp: "..."
    
  hypothesis_set:
    hypotheses: [...]
    test_plan: "..."
    
  experimental_results:
    experiments: [...]
    summary: {...}
    
  cross_validation:
    findings_validated: [...]
    bias_assessment: {...}
    overall_validity: 0.91
    
  insight_repository:
    insights: [...]
    stats: {...}
    
  genius_calculation:
    G: 0.492
    components: {...}
    assessment: "Acceptable for pattern validation"
    
  constitutional_telemetry:
    floors_checked: ["F2", "F3", "F4", "F7", "F8"]
    truth_scores: [...]
    tri_witness_preview:
      human: "pending"
      ai: 0.89
      earth: 0.91
      
  verdict: "DISCOVERY_COMPLETE"
  recommendation: "PROCEED_TO_APPRAISE"
```

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| **F2** | Hypotheses falsifiable, evidence recorded | ✓ |
| **F3** | Multi-source validation performed | ✓ |
| **F4** | Insights reduce entropy vs raw data | ✓ |
| **F7** | Confidence intervals documented | ✓ |
| **F8** | Genius calculated (accepting lower G for validation) | ✓ |

---

## 🔄 Next Stage

→ **Trigger**: `300-APPRAISE-WORKFLOW`

---

**DITEMPA BUKAN DIBERI**
