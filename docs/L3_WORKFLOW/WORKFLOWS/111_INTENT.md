# Workflow: 111_INTENT

**Stage:** 111 (Intent)  
**Purpose:** Map user request to constitutional lanes and determine processing path  
**Trigger:** After 000_SESSION_INIT completes  
**Output:** Intent classification + lane assignment

---

## 🎯 When to Use

Use this workflow after session initialization to understand what the user wants and how to process it constitutionally.

---

## 📋 Workflow Steps

### Step 1: Entity Extraction
```markdown
1. Extract key entities from user query:
   - Nouns (people, places, things)
   - Verbs (actions)
   - Context references
   - Time constraints
   
2. Identify domain:
   - CODE (programming)
   - DOC (documentation)
   - CONFIG (configuration)
   - ARCH (architecture)
   - RESEARCH (exploration)
   - OTHER (miscellaneous)
```

### Step 2: Contrast Detection
```markdown
Identify tensions/oppositions in request:
- "old vs new"
- "fast vs safe"
- "cheap vs quality"
- "now vs later"
- "simple vs complete"

Document contrasts for 333_CONTEXT stage.
```

### Step 3: Intent Classification
```markdown
Classify primary intent:
├── EXPLAIN (information seeking)
├── BUILD (creation)
├── FIX (repair)
├── REFACTOR (improvement)
├── REVIEW (evaluation)
├── DEBUG (troubleshooting)
├── DEPLOY (release)
└── EXPLORE (discovery)
```

### Step 4: Lane Determination (Critical)
```markdown
Based on intent + domain + context, assign lane:

HARD Lane (High Stakes):
├── Modifies production code
├── Changes architecture
├── Affects security
├── Alters data structures
├── Requires 888_JUDGE oversight
└── Stakes: CRITICAL

SOFT Lane (Medium Stakes):
├── Documentation updates
├── Configuration changes
├── Test additions
├── Refactoring (reversible)
├── No production impact
└── Stakes: NORMAL

PHATIC Lane (Low Stakes):
├── Information queries
├── Explanation requests
├── Learning questions
├── Casual discussion
└── Stakes: LOW
```

### Step 5: Contrast Engine Analysis
```markdown
The Contrast Engine predicts user needs:

1. What do they THINK they want?
2. What do they ACTUALLY need?
3. What are they NOT asking for?
4. What could go WRONG?

Output: Contrast map for 333_CONTEXT
```

### Step 6: Energy Budget Allocation
```markdown
Based on lane assignment, allocate energy:

HARD Lane:
- Energy budget: HIGH
- Cooling required: YES (Tier 2-3)
- Tri-Witness: Mandatory
- Verdict: Requires APEX_888

SOFT Lane:
- Energy budget: MEDIUM
- Cooling required: MAYBE (Tier 1)
- Tri-Witness: Standard
- Verdict: Standard 777_FORGE

PHATIC Lane:
- Energy budget: LOW
- Cooling required: NO
- Tri-Witness: Relaxed
- Verdict: Fast-track
```

---

## 📝 Output Specification

### Intent Map Object
```yaml
intent_map:
  session_id: "session_2026-01-31_abc123"
  raw_query: "I need to refactor the authentication module"
  entities:
    domain: "CODE"
    action: "REFACTOR"
    target: "authentication module"
    constraints: []
  
  contrasts:
    - "old auth vs new auth"
    - "compatibility vs improvement"
  
  classification:
    primary: "REFACTOR"
    secondary: "ARCH"
    confidence: 0.92
  
  lane_assignment:
    lane: "SOFT"
    stakes: "NORMAL"
    rationale: "Refactoring is reversible if F1 Amanah maintained"
  
  energy_allocation:
    budget: "MEDIUM"
    cooling: "TIER_1"
    tri_witness_required: true
  
  predicted_needs:
    explicit: "Code refactoring"
    implicit: "Maintain compatibility"
    risks: "Breaking changes"
    missing: "Test coverage check"
  
  next_stage: "333_CONTEXT"
```

---

## 🔄 Next Stage

After 111_INTENT completes → Proceed to **333_CONTEXT**

---

## ✅ Completion Checklist

- [ ] Entities extracted
- [ ] Domain identified
- [ ] Contrasts documented
- [ ] Intent classified
- [ ] Lane assigned (HARD/SOFT/PHATIC)
- [ ] Energy budget allocated
- [ ] Predicted needs documented
- [ ] Output saved to state

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| F4 | Clarity of intent | Required |
| F6 | Empathy for user needs | Required |
| F7 | Humility in prediction | Required |

---

## 📝 Usage Example

```markdown
User: "Add dark mode to the settings page"

AI: [Executes 111_INTENT]
  → Domain: CODE
  → Intent: BUILD
  → Contrasts: "light vs dark", "UI vs backend"
  → Lane: SOFT (reversible UI change)
  → Stakes: NORMAL
  → Energy: MEDIUM
  → Predicted needs: CSS variables, theme toggle, persistence
  
Proceeding to 333_CONTEXT gathering...
```

---

## 🔄 000-999 Loop Integration

```
Previous: 000_SESSION_INIT (Ignition)
Current:  111_INTENT (Understanding)
Next:     333_CONTEXT (Mapping)
```

**Loop Reference:** This is Stage 2 of the metabolic loop. The intent becomes the seed for context gathering.

---

**DITEMPA BUKAN DIBERI**
