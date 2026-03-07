# EXPLORATION & APPRAISAL WORKFLOWS — Pre-Development Architecture

**Level 3 | Pre-Development Focus | Exploration-First Design**  
**Version:** v2026.3.6-EXPLORATION  
**Authority:** Muhammad Arif bin Fazil  
**Status:** CANONICAL — FORGED, NOT GIVEN

---

## 1. CONCEPTUAL FRAMEWORK: Workflows vs Skills vs Tools

### The Three-Layer Abstraction Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         L5: AGENTS (Autonomous Systems)                      │
│              Autonomous entities with persistent state and goals             │
│                    Example: ASI_Guardian, Trinity_Agent                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                         L4: TOOLS (MCP Interface)                            │
│          Executable capabilities exposed via Model Context Protocol          │
│    Example: anchor_session, reason_mind, vps_git_ingest, container_exec      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ★ HERE →    L3: WORKFLOWS (Multi-Step Sequences)              ★ HERE →     │
│            Compositions of tools into constitutional metabolic loops         │
│           Example: EXPLORATION_WORKFLOW, APPRAISAL_WORKFLOW,                 │
│                    DESIGN_WORKFLOW, PROOF_OF_CONCEPT_WORKFLOW                │
├─────────────────────────────────────────────────────────────────────────────┤
│                         L2: SKILLS (Agent Prompts)                           │
│              Kimi/Claude skill definitions — behavioral prompts              │
│     Example: arifos-trinity-refactor, vps-repo-ingest, arifos-agi-plan       │
├─────────────────────────────────────────────────────────────────────────────┤
│                         L1: PRIMITIVES (VPS/Foundation)                      │
│              GitIngest, file system, shell execution, Docker                 │
│                 Example: git clone, docker ps, file read                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Distinctions

| Layer | What It Is | State | Constitutional | Example |
|-------|-----------|-------|----------------|---------|
| **Tools** | Atomic capabilities | Stateless | Floor-enforced | `reason_mind()` |
| **Skills** | Behavioral prompts | Stateless | Guidance-only | "You are a refactoring agent..." |
| **Workflows** | Multi-step recipes | Stateful | Loop-governed | `anchor → reason → integrate → audit` |

**The Critical Difference:**
- **Tools** are called; they execute and return
- **Skills** guide; they shape behavior
- **Workflows** orchestrate; they maintain state across stages

---

## 2. METABOLIC LOOP 000-999: Pre-Development Mapping

### Traditional vs Exploration-First Loop

**TRADITIONAL (Production-Focused):**
```
000_INIT → 111_SENSE → 222_THINK → 333_ATLAS → 444_RESPOND → 555_EMPATHY → 666_ALIGN → 777_FORGE → 888_JUDGE → 999_VAULT
   ↓                                                                                                          ↓
   └────────────────────────────────────────── SEALED ────────────────────────────────────────────────────────┘
```

**EXPLORATION-FIRST (Pre-Development):**
```
000_INIT → 100_EXPLORE → 200_DISCOVER → 300_APPRAISE → 400_DESIGN → 888_JUDGE → 999_VAULT
   ↓                                                                        ↓
   └────────────────────────────── DECISION PACKAGE ────────────────────────┘
                                        ↓
                              Handoff to Production Agents
                              (VPS agents take over)
```

### Pre-Development Stage Mapping

| Stage | Name | Purpose | Output | Floors |
|-------|------|---------|--------|--------|
| **000** | INIT | Session ignition, authority | Session context | F11, F12, F13 |
| **100** | EXPLORE | Broad domain exploration | Discovery log | F2, F4, F7 |
| **200** | DISCOVER | Deep pattern recognition | Insight repository | F2, F4, F8 |
| **300** | APPRAISE | Value/effort assessment | Appraisal matrix | F5, F6, F7, F9 |
| **400** | DESIGN | Architecture blueprint | Design document | F2, F4, F8, F10 |
| **888** | JUDGE | Go/No-Go verdict | Decision package | ALL |
| **999** | VAULT | Immutable record | Project genesis entry | F1, F3 |

---

## 3. THE FOUR EXPLORATION WORKFLOWS

### Workflow 1: EXPLORE — Domain Reconnaissance

**Stage:** 100 (Explore)  
**Purpose:** Broad-spectrum domain exploration before narrowing  
**Trigger:** New project idea, technology evaluation, market research  
**Output:** Discovery log with mapped territory

#### Constitutional Intent
EXPLORE operates with **F7 Humility** at maximum — we acknowledge vast unknowns. This stage is explicitly divergent; entropy temporarily increases (F4 suspended) to enable creativity.

#### Workflow Steps

**Step 1: Territory Mapping (F2, F4)**
- Define exploration boundaries (what's in/out of scope)
- Identify 5-7 key exploration vectors
- Set exploration budget (time, compute, tokens)
- Output: Territory map with bounded uncertainty

**Step 2: Multi-Source Ingestion (F2)**
- Ingest relevant repositories (GitIngest)
- Search web sources (Brave Search)
- Query documentation (Context7)
- Read research papers if applicable
- Output: Raw knowledge corpus

**Step 3: Pattern Synthesis (F8)**
- Identify recurring patterns across sources
- Map solution approaches to problem types
- Create pattern library
- Output: Pattern taxonomy

**Step 4: Uncertainty Quantification (F7)**
- Catalog known knowns, known unknowns, unknown unknowns
- Assign confidence intervals to findings
- Flag areas requiring deeper exploration
- Output: Uncertainty map with Ω₀ scores

**Step 5: Checkpoint — Continue or Narrow?**
- Assess exploration saturation
- Decide: Continue exploring, or proceed to DISCOVER?
- If continue: Loop back to Step 2 with refined vectors
- If narrow: Handoff to DISCOVER workflow

#### Output Specification
```yaml
exploration_package:
  territory_map:
    boundaries: [...]
    vectors: [...]
    budget_consumed: "..."
  knowledge_corpus:
    sources: [...]
    patterns_identified: [...]
    key_insights: [...]
  uncertainty:
    known_knowns: [...]
    known_unknowns: [...]
    unknown_unknowns: [...]
    omega_0: 0.04
  recommendation: "PROCEED_TO_DISCOVER" | "CONTINUE_EXPLORATION"
  verdict: "EXPLORATION_COMPLETE"
```

---

### Workflow 2: DISCOVER — Deep Pattern Recognition

**Stage:** 200 (Discover)  
**Purpose:** Deep analysis of promising directions from EXPLORE  
**Trigger:** EXPLORE recommends PROCEED_TO_DISCOVER  
**Output:** Insight repository with validated patterns

#### Constitutional Intent
DISCOVER shifts from breadth to depth. F2 Truth becomes paramount — we verify hypotheses generated during exploration. F8 Genius measures pattern recognition quality.

#### Workflow Steps

**Step 1: Hypothesis Selection (F2, F8)**
- Select top 3 patterns from EXPLORE for deep analysis
- Formulate falsifiable hypotheses about each
- Design verification experiments
- Output: Hypothesis test plan

**Step 2: Experimental Verification (F2, F4)**
- Build minimal test cases for each hypothesis
- Run verification experiments
- Document results with confidence scores
- Output: Experimental results

**Step 3: Cross-Validation (F3, F8)**
- Validate findings against multiple sources
- Check for confirmation bias
- Seek disconfirming evidence
- Output: Validated insights

**Step 4: Insight Crystallization (F4, F8)**
- Distill findings into actionable insights
- Create insight cards (one per validated pattern)
- Link insights to evidence
- Output: Insight repository

**Step 5: Genius Calculation (F8)**
- Calculate G = A × P × X × E²
- A (Akal): Depth of understanding
- P (Present): Relevance to current context
- X (Exploration): Novelty of insight
- E (Energy): Confidence in findings
- Output: Genius score with breakdown

#### Output Specification
```yaml
discovery_package:
  hypotheses_tested: [...]
  experimental_results: [...]
  insight_repository:
    - id: "..."
      pattern: "..."
      evidence: [...]
      confidence: 0.95
      applicability: "..."
  genius_calculation:
    G: 0.87
    breakdown:
      A: 0.90
      P: 0.95
      X: 0.85
      E: 0.92
  validated_insights: [...]
  verdict: "DISCOVERY_COMPLETE"
```

---

### Workflow 3: APPRAISE — Value/Effort Assessment

**Stage:** 300 (Appraise)  
**Purpose:** Assess which discoveries are worth building  
**Trigger:** DISCOVER produces validated insights  
**Output:** Appraisal matrix with recommendations

#### Constitutional Intent
APPRAISE is where Ω (Heart) engages fully. F5 Peace² ensures alignment with existing systems. F6 Empathy considers all stakeholders. F9 Anti-Hantu prevents deceptive value propositions.

#### Workflow Steps

**Step 1: Stakeholder Mapping (F6)**
- Identify all stakeholders (users, maintainers, business, future-you)
- Determine weakest stakeholder (who gets hurt if this fails?)
- Map stakeholder needs to discovery insights
- Output: Stakeholder matrix

**Step 2: Value Assessment (F6, F9)**
- Quantify value for each stakeholder
- Check for dark patterns (F9: C_dark < 0.30)
- Assess ethical implications
- Output: Value assessment with ethics check

**Step 3: Effort Estimation (F7)**
- Estimate development effort (time, complexity, risk)
- Quantify uncertainty in estimates (Ω₀)
- Identify blockers and dependencies
- Output: Effort matrix with confidence intervals

**Step 4: Options Analysis (F5, F8)**
- Generate 3+ implementation options
- Compare: Do Nothing, Minimal, Full Build, Buy/Use Existing
- Score each on value/effort/risk
- Output: Options matrix

**Step 5: Peace² Evaluation (F5)**
- Assess internal harmony (system stability)
- Assess external harmony (user impact)
- Calculate Peace² = Internal × External
- Threshold: Peace² ≥ 1.0

**Step 6: Recommendation Formation**
- Formulate clear recommendation
- Include: What, Why, How, Risks, Alternatives
- Output: Appraisal document

#### Output Specification
```yaml
appraisal_package:
  stakeholder_matrix:
    stakeholders: [...]
    weakest: "..."
    kappa_r: 0.85
  value_assessment:
    value_by_stakeholder: {...}
    c_dark: 0.15
    ethics_verdict: "CLEAR"
  effort_estimation:
    options:
      - name: "Minimal"
        effort: "2 weeks"
        confidence: 0.70
        uncertainty: 0.04
      - name: "Full Build"
        effort: "3 months"
        confidence: 0.50
        uncertainty: 0.05
  options_matrix:
    - option: "Do Nothing"
      value: 0.1
      effort: 0.0
      risk: 0.1
      peace2: 1.0
    - option: "Minimal"
      value: 0.7
      effort: 0.3
      risk: 0.2
      peace2: 1.1
    - option: "Full Build"
      value: 0.9
      effort: 0.8
      risk: 0.5
      peace2: 0.9
  recommendation:
    option: "Minimal"
    reasoning: "..."
    confidence: 0.85
  verdict: "APPRAISAL_COMPLETE"
```

---

### Workflow 4: DESIGN — Architecture Blueprint

**Stage:** 400 (Design)  
**Purpose:** Create implementation-ready architecture  
**Trigger:** APPRAISE recommends proceeding  
**Output:** Design document ready for production

#### Constitutional Intent
DESIGN brings together Δ (Mind) for technical correctness and Ω (Heart) for maintainability. F10 Ontology ensures proper categorization. F8 Genius ensures elegant solutions.

#### Workflow Steps

**Step 1: Requirements Extraction (F2, F10)**
- Extract functional requirements from appraisal
- Define non-functional requirements (performance, security)
- Categorize requirements (MUST, SHOULD, COULD)
- Output: Requirements specification

**Step 2: Component Architecture (F8, F10)**
- Design high-level components
- Define interfaces between components
- Map to existing codebase if applicable
- Output: Component diagram

**Step 3: Data Flow Design (F4, F8)**
- Design data flows between components
- Identify state management approach
- Plan for data persistence
- Output: Data flow diagrams

**Step 4: Interface Design (F6, F8)**
- Design user interfaces (CLI, API, UI)
- Consider weakest stakeholder experience
- Ensure reversibility (F1) in design
- Output: Interface specifications

**Step 5: Risk Analysis (F5, F7)**
- Identify technical risks
- Assess mitigation strategies
- Quantify residual uncertainty
- Output: Risk register

**Step 6: Implementation Roadmap (F8)**
- Create phased implementation plan
- Define milestones and deliverables
- Estimate timeline with uncertainty
- Output: Roadmap document

#### Output Specification
```yaml
design_package:
  requirements:
    functional: [...]
    non_functional: [...]
    categorized:
      must: [...]
      should: [...]
      could: [...]
  architecture:
    components: [...]
    interfaces: [...]
    data_flows: [...]
  interfaces:
    user_interfaces: [...]
    api_specs: [...]
    cli_design: "..."
  risks:
    technical: [...]
    mitigations: [...]
    residual_uncertainty: 0.04
  roadmap:
    phases: [...]
    milestones: [...]
    timeline: "..."
    confidence: 0.80
  verdict: "DESIGN_COMPLETE"
```

---

## 4. THE JUDGMENT WORKFLOW

### Workflow 5: PRE-DEV-JUDGE — Go/No-Go Decision

**Stage:** 888 (Judge)  
**Purpose:** Final verdict on pre-development package  
**Trigger:** DESIGN workflow complete  
**Output:** Decision package for production handoff

#### Constitutional Intent
This is the Ψ (Soul) moment. All Floors F1-F13 are checked. Tri-Witness consensus determines if we proceed.

#### Workflow Steps

**Step 1: Package Assembly**
- Collect outputs from all previous workflows
- Assemble complete pre-development package
- Index all evidence and decisions
- Output: Complete package

**Step 2: Floor-by-Floor Review (F1-F13)**
| Floor | Check | Status |
|-------|-------|--------|
| F1 | Reversibility ensured in design? | ✓ |
| F2 | All claims evidence-backed? | ✓ |
| F3 | Tri-Witness ≥ 0.95? | ✓ |
| F4 | Design reduces entropy? | ✓ |
| F5 | Peace² ≥ 1.0? | ✓ |
| F6 | Weakest stakeholder protected? | ✓ |
| F7 | Uncertainty properly bounded? | ✓ |
| F8 | Genius G ≥ 0.80? | ✓ |
| F9 | No dark patterns? | ✓ |
| F10 | Proper categorization? | ✓ |
| F11 | Authority verified? | ✓ |
| F12 | No injection vectors? | ✓ |
| F13 | Sovereign approval ready? | ✓ |

**Step 3: Tri-Witness Consensus (F3)**
- Human Witness: Your review and approval
- AI Witness: arifOS assessment
- Earth Witness: Evidence from reality (code, data, tests)
- Calculate W₃ = geometric_mean(H, A, E)

**Step 4: Verdict Rendering**
Options:
- **SEAL**: Proceed to production
- **SABAR**: Needs revision (specify what)
- **VOID**: Do not proceed (explain why)
- **888_HOLD**: Pause for human decision

**Step 5: Production Handoff Preparation**
- Create handoff document for VPS agents
- Include: Design package, decisions, context
- Prepare session for production phase
- Output: Handoff package

#### Output Specification
```yaml
decision_package:
  exploration: {...}  # From EXPLORE
  discovery: {...}    # From DISCOVER
  appraisal: {...}    # From APPRAISE
  design: {...}       # From DESIGN
  
  floor_review:
    f1_amanah: {status: "PASS", notes: "..."}
    f2_truth: {status: "PASS", notes: "..."}
    # ... all floors
    
  tri_witness:
    human: 0.95
    ai: 0.97
    earth: 0.94
    w3_final: 0.953
    
  verdict: "SEAL" | "SABAR" | "VOID" | "888_HOLD"
  
  handoff:
    production_ready: true
    vps_context: "..."
    estimated_effort: "..."
    
  governance_token: "..."
  vault_id: "..."
  timestamp: "..."
```

---

## 5. RELATIONSHIP TO METABOLIC LOOP

### Mapping to Canonical Stages

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PRE-DEVELOPMENT vs PRODUCTION                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   PRE-DEV (Laptop/Kimi)                    PRODUCTION (VPS/Agents)          │
│   ─────────────────────                    ───────────────────────          │
│                                                                              │
│   000_INIT ──────────────────────────────→ 000_INIT (re-ignite)             │
│       ↓                                                                      │
│   100_EXPLORE ──(divergent)──┐                                              │
│       ↓                      │                                              │
│   200_DISCOVER ──(converge)──┤                                              │
│       ↓                      ├──→ DECISION PACKAGE ──→ Handoff              │
│   300_APPRAISE ──(evaluate)──┤                                              │
│       ↓                      │                                              │
│   400_DESIGN ────(plan)──────┘                                              │
│       ↓                                                                      │
│   888_JUDGE ─────────────────────────────→ 888_JUDGE (re-assess)            │
│       ↓                                                                      │
│   999_VAULT ─────────────────────────────→ 999_VAULT (continue log)         │
│       ↓                                                                      │
│   Handoff to VPS ───────────────────────→ 111_SENSE (begin implementation)  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Why This Separation?

**Pre-Development (You + Kimi):**
- Exploration requires creativity and judgment
- High uncertainty, need for human intuition
- Research, design, decision-making
- Lower cost, faster iteration

**Production (VPS Agents):**
- Implementation requires precision and consistency
- Well-defined scope from pre-dev package
- Execution, testing, deployment
- Higher cost, requires infrastructure

---

## 6. IMPLEMENTATION NOTES

### For Laptop (Kimi) Usage

These workflows are **skill-based** for Kimi:
- Each workflow maps to a Kimi skill prompt
- Skills call arifOS MCP tools
- Human (you) is the sovereign at each stage

### For VPS Agents

VPS agents receive:
- Completed decision package
- Specific implementation instructions
- Context from pre-development phase
- Clear scope and boundaries

They execute:
- `111_SENSE` → `222_THINK` → `333_ATLAS` → `777_FORGE` → `888_JUDGE` → `999_VAULT`

---

## 7. CONSTANTS & THRESHOLDS

```python
EXPLORATION_CONSTANTS = {
    # Floors
    "F2_TRUTH_THRESHOLD": 0.95,        # Slightly lower for exploration
    "F3_TRI_WITNESS_THRESHOLD": 0.95,  # Same
    "F4_CLARITY_TARGET": -0.20,        # Allow some entropy in exploration
    "F5_PEACE_SQUARED_MIN": 1.0,       # Same
    "F6_EMPATHY_THRESHOLD": 0.70,      # Same
    "F7_HUMILITY_BAND": [0.03, 0.08],  # Wider band for exploration
    "F8_GENIUS_THRESHOLD": 0.80,       # Same
    "F9_C_DARK_MAX": 0.30,             # Same
    
    # Exploration-specific
    "EXPLORATION_VECTORS_MIN": 3,
    "EXPLORATION_VECTORS_MAX": 7,
    "HYPOTHESES_TO_TEST": 3,
    "OPTIONS_TO_GENERATE": 3,
    
    # Verdicts
    "VERDICT_HIERARCHY": ["VOID", "888_HOLD", "SABAR", "SEAL"]
}
```

---

**DITEMPA BUKAN DIBERI** — Forged through exploration, not given as instruction. 🔥
