# Workflow: 777_IMPLEMENT

**Stage:** 777 (Forge/Implementation)  
**Purpose:** Execute the implementation with constitutional checkpoints  
**Trigger:** After 555_SAFETY ALIGN verdict  
**Output:** Implementation results with verification

---

## 🎯 When to Use

Use this workflow after safety approval to execute the task with continuous constitutional monitoring.

---

## 📋 Workflow Steps

### Step 1: Pre-Implementation Check
```markdown
Verify prerequisites:
├── 555_SAFETY verdict was ALIGN
├── Context map is current
├── Stakeholder conditions documented
├── Rollback plan ready (if needed)
└── Workspace is clean
```

### Step 2: Implementation Strategy
```markdown
Based on lane assignment:

HARD Lane Strategy:
├── Implement in feature branch
├── Add comprehensive tests
├── Document every change
├── Request code review
├── Deploy to staging first
└── 888_JUDGE approval required

SOFT Lane Strategy:
├── Implement with tests
├── Document key changes
├── Self-review
├── Deploy when ready
└── Standard 888 verification

PHATIC Lane Strategy:
├── Quick implementation
├── Basic verification
└── Fast-track to 888
```

### Step 3: Constitutional Checkpoint 1 (F2 Truth)
```markdown
During implementation, verify:
├── Code is factually correct
├── No hallucinated APIs
├── Documentation matches implementation
├── Comments are accurate
└── τ ≥ 0.99 maintained
```

### Step 4: Constitutional Checkpoint 2 (F4 Clarity)
```markdown
Verify clarity:
├── Code is readable
├── Functions are focused
├── Naming is clear
├── Complexity is managed
└── ΔS ≤ 0 (confusion not increased)
```

### Step 5: Constitutional Checkpoint 3 (F8 Genius)
```markdown
Calculate Genius Score G = A × P × X × E²:

A (AKAL/Intelligence): Is it well-designed?
P (PRESENT/Regulation): Is it safe?
X (EXPLORATION/Trust): Is it innovative?
E (ENERGY/Sustainability): Is it efficient?

Threshold: G ≥ 0.80 for HARD lane
Threshold: G ≥ 0.70 for SOFT lane
```

### Step 6: Implementation Execution
```markdown
Execute the work:

CODE changes:
├── Write/modify files
├── Add tests
├── Update documentation
├── Verify imports
└── Check formatting

CONFIG changes:
├── Update settings
├── Verify environment
├── Test locally
└── Document changes

DOC changes:
├── Update README
├── Add examples
├── Update changelogs
└── Verify accuracy
```

### Step 7: Post-Implementation Verification
```markdown
Verify the implementation:

FUNCTIONAL:
├── Tests pass
├── Feature works as intended
├── No regressions
└── Edge cases handled

CONSTITUTIONAL:
├── F1: Can be reversed
├── F2: Truth maintained
├── F4: Clarity preserved
├── F5: Peace maintained
├── F6: Stakeholders still protected
├── F7: Humility acknowledged
└── F9: No dark patterns introduced
```

---

## 📝 Output Specification

### Implementation Result Object
```yaml
implementation:
  session_id: "session_2026-01-31_abc123"
  
  status: "COMPLETED"
  
  changes:
    files_modified:
      - path: "src/auth/settings.tsx"
        lines_added: 45
        lines_removed: 12
        description: "Added dark mode toggle and CSS variables"
      
      - path: "src/auth/theme.ts"
        lines_added: 23
        lines_removed: 0
        description: "Added dark mode color palette"
      
      - path: "tests/auth/settings.test.tsx"
        lines_added: 67
        lines_removed: 0
        description: "Added dark mode tests"
    
    files_created:
      - path: "docs/dark-mode-implementation.md"
        description: "Implementation guide for maintainers"
  
  verification:
    tests:
      total: 12
      passed: 12
      failed: 0
      coverage: 94%
    
    constitutional:
      f2_truth: 0.98  # ✅
      f4_clarity: -0.15  # ΔS < 0 ✅
      f5_peace: 0.92  # ✅
      f6_empathy: 0.85  # ✅
      f8_genius: 0.82  # ✅
      f9_antihantu: 0.05  # ✅
  
  genius_score:
    A: 0.90  # Well-designed
    P: 0.88  # Safe
    X: 0.85  # Good innovation
    E: 0.92  # Efficient
    G: 0.82  # ≥ 0.80 ✅
  
  stakeholder_impact:
    - name: "End Users"
      impact: "Positive — dark mode available"
    - name: "Future Maintainers"
      impact: "Positive — comprehensive docs added"
  
  rollback_instructions:
    - "git revert <commit_hash>"
    - "Or: Set DARK_MODE_ENABLED=false in config"
  
  next_stage: "888_COMMIT"
```

---

## 🔄 Next Stage

After 777_IMPLEMENT completes → Proceed to **888_COMMIT**

---

## ✅ Completion Checklist

- [ ] Pre-implementation checks passed
- [ ] Strategy aligned with lane
- [ ] F2 Truth verified
- [ ] F4 Clarity verified
- [ ] F8 Genius calculated (G ≥ 0.80/0.70)
- [ ] Changes implemented
- [ ] Tests pass
- [ ] Constitutional checkpoints passed
- [ ] Rollback instructions documented
- [ ] Output saved to state

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| F2 | Truth τ ≥ 0.99 | Required |
| F4 | Clarity ΔS ≤ 0 | Required |
| F7 | Humility Ω₀ ∈ [0.03,0.05] | Required |
| F8 | Genius G ≥ 0.80/0.70 | Required |
| F9 | Anti-Hantu < 0.30 | Required |
| F10 | Ontology maintained | Required |

---

## 📝 Usage Example

```markdown
[After 555_SAFETY: ALIGN verdict]

AI: [Executes 777_IMPLEMENT]
  → Modified: settings.tsx (+45/-12)
  → Modified: theme.ts (+23)
  → Created: tests (+67)
  → Created: docs
  → Tests: 12/12 passed
  → Genius G: 0.82 ✅
  → All constitutional floors passed
  
Proceeding to 888_COMMIT...
```

---

## 🔄 000-999 Loop Integration

```
Previous: 555_SAFETY (Empathy)
Current:  777_IMPLEMENT (Forge)
Next:     888_COMMIT (Decree)

Connection: Safe implementation → Final judgment
```

**Loop Reference:** The forge where ideas become reality.

---

**DITEMPA BUKAN DIBERI**
