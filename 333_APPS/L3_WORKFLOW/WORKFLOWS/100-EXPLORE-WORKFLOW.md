# Workflow: EXPLORE
**Stage:** 100 (Explore)  
**Band:** E (Exploration)  
**Purpose:** Broad-spectrum domain exploration before narrowing  
**Trigger:** New project idea, technology evaluation, market research, "should we build this?"  
**Output:** Discovery log with mapped territory and exploration verdict

---

## 🎯 When to Use

- **New Project Genesis**: "I have an idea for..."
- **Technology Evaluation**: "Should we use X or Y?"
- **Market Research**: "What's the landscape for...?"
- **Feasibility Study**: "Can this even be built?"
- **Paradigm Exploration**: "How do others solve this?"

**Key Signal**: You don't yet know what you don't know.

---

## 📋 Workflow Steps

### Step 1: Territory Mapping (F2, F4, F7)

**Constitutional Intent**: Establish bounded exploration space. F7 Humility is at maximum — we explicitly acknowledge the unknown.

**Actions**:
1. Define the central question or problem
2. Identify 5-7 exploration vectors (dimensions to investigate)
3. Set exploration budget (time, compute, tokens)
4. Define boundaries (what's explicitly out of scope)
5. Record initial uncertainty estimate (Ω₀ ∈ [0.05, 0.08] for exploration)

**Vector Examples**:
- Technical feasibility
- Existing solutions/competitors
- User needs and pain points
- Integration complexity
- Maintenance burden
- Cost considerations
- Timeline constraints

**Output**:
```yaml
territory_map:
  central_question: "..."
  exploration_vectors:
    - name: "..."
      description: "..."
      priority: 1-5
  boundaries:
    in_scope: [...]
    out_of_scope: [...]
  budget:
    time: "..."
    compute: "..."
    tokens: "..."
  initial_uncertainty:
    omega_0: 0.06
    confidence: 0.30
```

---

### Step 2: Multi-Source Ingestion (F2)

**Constitutional Intent**: Ground exploration in reality. F2 Truth requires evidence from multiple sources.

**Actions**:
1. **Repository Ingestion**: Use `vps_git_ingest` to analyze relevant repos
2. **Web Search**: Use `brave_search` for landscape analysis
3. **Documentation**: Use `context7` for library/framework docs
4. **Research**: Search papers/blogs for deep dives
5. **Expert Knowledge**: Query `memory` for past learnings

**For Each Source**:
- Record source URL/reference
- Extract key insights
- Assign confidence score (τ)
- Tag with relevant exploration vectors

**Output**:
```yaml
knowledge_corpus:
  sources:
    - type: "repository"
      url: "..."
      ingested_via: "vps_git_ingest"
      insights: [...]
      confidence: 0.90
      tags: ["vector-1", "vector-3"]
    - type: "web_search"
      query: "..."
      results: [...]
      synthesized_insights: [...]
      confidence: 0.75
  raw_findings:
    - finding: "..."
      evidence: [...]
      confidence: 0.85
```

---

### Step 3: Pattern Synthesis (F8)

**Constitutional Intent**: Transform raw data into structured understanding. F8 Genius measures pattern recognition quality.

**Actions**:
1. **Pattern Identification**: What solutions appear repeatedly?
2. **Anti-Pattern Detection**: What approaches consistently fail?
3. **Emergent Themes**: What underlying principles emerge?
4. **Solution Taxonomy**: Categorize approaches by type
5. **Maturity Assessment**: How mature are various solutions?

**Pattern Categories**:
- Architectural patterns
- Implementation patterns
- Integration patterns
- Failure patterns
- Success patterns

**Output**:
```yaml
pattern_library:
  patterns:
    - id: "pattern-001"
      name: "..."
      description: "..."
      evidence: [...]
      prevalence: "common|uncommon|rare"
      maturity: "proven|emerging|experimental"
      applicability: "..."
  anti_patterns:
    - id: "anti-001"
      name: "..."
      why_it_fails: "..."
      evidence: [...]
  emergent_themes:
    - theme: "..."
      description: "..."
      supporting_evidence: [...]
  taxonomy:
    category_a: [...]
    category_b: [...]
```

---

### Step 4: Uncertainty Quantification (F7)

**Constitutional Intent**: Explicitly catalog what we don't know. F7 mandates uncertainty acknowledgment.

**Actions**:
1. **Known Knowns**: What are we confident about?
2. **Known Unknowns**: What questions do we know we need answered?
3. **Unknown Unknowns**: What blind spots might exist?
4. **Confidence Intervals**: Assign uncertainty to each finding
5. **Risk Areas**: Where could exploration be misleading?

**Output**:
```yaml
uncertainty_map:
  known_knowns:
    - statement: "..."
      confidence: 0.95
      evidence: [...]
  known_unknowns:
    - question: "..."
      importance: "high|medium|low"
      approach_to_answer: "..."
  unknown_unknowns:
    - risk_area: "..."
      mitigation: "..."
  confidence_distribution:
    high_confidence: [...]  # τ >= 0.90
    medium_confidence: [...]  # τ 0.70-0.89
    low_confidence: [...]  # τ < 0.70
  overall_uncertainty:
    omega_0: 0.05
    assessment: "Exploration has reduced major unknowns"
```

---

### Step 5: Checkpoint — Continue or Narrow?

**Constitutional Intent**: F4 Clarity begins to re-assert. Decision point based on exploration saturation.

**Decision Criteria**:

| Condition | Action |
|-----------|--------|
| New vectors discovered | Continue exploration |
| High uncertainty remains | Continue exploration |
| Budget exhausted | Proceed to DISCOVER |
| Patterns are clear | Proceed to DISCOVER |
| User requests pivot | Re-run territory mapping |

**Checkpoint Questions**:
1. Have we mapped the full territory?
2. Are the patterns stable and repeatable?
3. Do we have sufficient confidence to narrow?
4. Is the user satisfied with exploration breadth?

**Output**:
```yaml
checkpoint_decision:
  exploration_saturation: "saturated|partial|minimal"
  recommendation: "PROCEED_TO_DISCOVER" | "CONTINUE_EXPLORATION"
  reasoning: "..."
  next_steps: [...]
```

---

## 📝 Output Specification

```yaml
exploration_package:
  metadata:
    workflow: "EXPLORE"
    stage: "100"
    session_id: "..."
    timestamp: "..."
    version: "v2026.3.6"
    
  territory_map:
    central_question: "..."
    exploration_vectors: [...]
    boundaries: {...}
    budget: {...}
    
  knowledge_corpus:
    sources: [...]
    raw_findings: [...]
    
  pattern_library:
    patterns: [...]
    anti_patterns: [...]
    emergent_themes: [...]
    taxonomy: {...}
    
  uncertainty_map:
    known_knowns: [...]
    known_unknowns: [...]
    unknown_unknowns: [...]
    overall_uncertainty:
      omega_0: 0.05
      
  checkpoint:
    recommendation: "PROCEED_TO_DISCOVER"
    reasoning: "..."
    
  constitutional_telemetry:
    floors_checked: ["F2", "F4", "F7", "F8"]
    truth_scores: [...]
    genius_indicators:
      pattern_recognition: 0.85
      synthesis_quality: 0.82
    
  verdict: "EXPLORATION_COMPLETE"
```

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| **F2** | All findings evidence-backed with τ scores | ✓ |
| **F4** | Entropy increase is bounded and justified | ✓ |
| **F7** | Ω₀ ∈ [0.05, 0.08] documented | ✓ |
| **F8** | Pattern library demonstrates synthesis | ✓ |

---

## 🔄 Next Stage

If `recommendation: PROCEED_TO_DISCOVER`:
→ **Trigger**: `200-DISCOVER-WORKFLOW`

If `recommendation: CONTINUE_EXPLORATION`:
→ **Trigger**: Loop to Step 2 with refined vectors

---

## 💡 Usage Example

```markdown
User: "I want to build an AI-powered code review tool. What should I know?"

[EXPLORE WORKFLOW TRIGGERED]

1. Territory Mapping:
   - Central question: "How to build AI code review tool?"
   - Vectors: existing tools, AI models, integration methods, 
              user workflows, accuracy benchmarks, costs

2. Multi-Source Ingestion:
   - Ingest: pr_agent, codeball, reviewpad repos
   - Search: "AI code review tools comparison 2024"
   - Query: OpenAI API docs, anthropic docs

3. Pattern Synthesis:
   - Pattern: "Line-by-line comments" (common)
   - Pattern: "Summary + action items" (emerging)
   - Anti-pattern: "Blocking CI without human review" (fails often)

4. Uncertainty Quantification:
   - Known knowns: OpenAI API reliable, GitHub webhooks mature
   - Known unknowns: Accuracy on our specific codebase, user adoption
   - Ω₀ = 0.06

5. Checkpoint Decision:
   - Recommendation: PROCEED_TO_DISCOVER
   - Reasoning: Landscape mapped, clear patterns identified

→ Handoff to DISCOVER workflow
```

---

**DITEMPA BUKAN DIBERI**
