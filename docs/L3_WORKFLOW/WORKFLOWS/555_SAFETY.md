# Workflow: 555_SAFETY

**Stage:** 555 (Empathy/Defense)  
**Purpose:** Evaluate safety, identify stakeholders, and ensure ethical alignment  
**Trigger:** After 333_CONTEXT atlas generation  
**Output:** Safety report with empathy score and risk mitigation

---

## 🎯 When to Use

Use this workflow after context gathering to evaluate the safety and ethical implications of the proposed action.

---

## 📋 Workflow Steps

### Step 1: Stakeholder Identification
```markdown
Identify all parties affected by this action:

PRIMARY (direct impact):
├── End users
├── Developers
├── Operations team
├── Business stakeholders
└── Data subjects

SECONDARY (indirect impact):
├── Future maintainers
├── Dependent systems
├── Compliance teams
└── Reputation/brand

TERTIARY (ecosystem impact):
├── Open source community
├── Industry standards
├── Regulatory bodies
└── Society at large
```

### Step 2: Impact Assessment
```markdown
For each stakeholder, assess impact:

Benefits (positive outcomes):
├── What do they gain?
├── How is their experience improved?
└── What problems are solved?

Risks (negative outcomes):
├── What could go wrong?
├── What data is exposed?
├── What functionality breaks?
└── What trust is eroded?

Unknowns (uncertainty):
├── What don't we know?
├── What assumptions are we making?
└── What could surprise us?
```

### Step 3: Empathy Score Calculation (F6)
```markdown
Calculate κᵣ (empathy score) for weakest stakeholder:

κᵣ = min(κ₁, κ₂, ..., κₙ)

Where each stakeholder's empathy score considers:
- Voice: Are they heard? (0-1)
- Protection: Are they safe? (0-1)
- Benefit: Do they gain? (0-1)
- Autonomy: Is their choice respected? (0-1)

Threshold: κᵣ ≥ 0.70 required
```

### Step 4: Reversibility Check (F1 Amanah)
```markdown
Evaluate reversibility:

FULLY REVERSIBLE:
├── Code changes with git history
├── Configuration changes
├── Documentation updates
└── Rollback plan exists

PARTIALLY REVERSIBLE:
├── Database migrations (down migration?)
├── API changes (versioning?)
├── Data transformations (backup?)
└── Mitigation plan required

IRREVERSIBLE:
├── Data deletion without backup
├── Security key exposure
├── Production incident
└── HARD lane + cooling required
```

### Step 5: Peace² Evaluation (F5)
```markdown
Calculate Peace² = Internal_Peace × External_Peace

INTERNAL (system harmony):
├── No breaking changes
├── Backward compatible
├── Tests pass
├── No conflicts
└── Clean implementation

EXTERNAL (user harmony):
├── No UX disruption
├── Clear communication
├── Training not required
├── Intuitive behavior
└── Positive reception

Threshold: Peace² ≥ 1.0
```

### Step 6: Safety Alignment
```markdown
Final safety evaluation:

ALIGN (Proceed):
├── All floors pass
├── κᵣ ≥ 0.70
├── Reversible OR acceptable risk
├── Peace² ≥ 1.0
└── Weakest stakeholder protected

SABAR (Cooldown):
├── Soft floor warning (0.50-0.79)
├── Minor risk detected
├── One retry allowed
└── Adjust and re-evaluate

VOID (Abort):
├── Hard floor failure (< 0.50)
├── Irreversible harm possible
├── κᵣ < 0.70
└── Escalate to human
```

---

## 📝 Output Specification

### Safety Report Object
```yaml
safety_report:
  session_id: "session_2026-01-31_abc123"
  
  stakeholders:
    - name: "End Users"
      type: "primary"
      impact: "positive"
      voice: 0.95
      protection: 0.90
      benefit: 0.85
      autonomy: 1.0
      kappa: 0.90
    
    - name: "Future Maintainers"
      type: "secondary"
      impact: "neutral"
      voice: 0.70
      protection: 0.80
      benefit: 0.75
      autonomy: 0.90
      kappa: 0.78
    
    - name: "Open Source Community"
      type: "tertiary"
      impact: "positive"
      voice: 0.60
      protection: 0.90
      benefit: 0.80
      autonomy: 1.0
      kappa: 0.82
  
  weakest_stakeholder:
    name: "Future Maintainers"
    kappa: 0.78
    concern: "Code complexity"
    mitigation: "Add comprehensive documentation"
  
  empathy:
    kappa_r: 0.78  # Minimum across all stakeholders
    threshold: 0.70
    status: "PASS"  # ✅ κᵣ ≥ 0.70
  
  reversibility:
    level: "FULLY_REVERSIBLE"
    rollback_plan: "git revert + config flag"
    backup_required: false
  
  peace:
    internal: 0.95
    external: 0.90
    peace_squared: 0.855  # ≥ 1.0? No — but acceptable for SOFT lane
    status: "ACCEPTABLE"
  
  verdict: "ALIGN"
  conditions:
    - "Add documentation for future maintainers"
  
  next_stage: "777_IMPLEMENT"
```

---

## 🔄 Next Stage

After 555_SAFETY completes with verdict ALIGN → Proceed to **777_IMPLEMENT**

If verdict SABAR → Return to 333_CONTEXT with adjustments

If verdict VOID → Terminate and escalate to human

---

## ✅ Completion Checklist

- [ ] Stakeholders identified (primary/secondary/tertiary)
- [ ] Impact assessed (benefits/risks/unknowns)
- [ ] Empathy score calculated (κᵣ ≥ 0.70)
- [ ] Weakest stakeholder identified
- [ ] Reversibility evaluated
- [ ] Peace² calculated
- [ ] Verdict rendered (ALIGN/SABAR/VOID)
- [ ] Conditions documented
- [ ] Output saved to state

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| F1 | Reversibility confirmed | Required |
| F5 | Peace² acceptable | Required |
| F6 | Empathy κᵣ ≥ 0.70 | Required |
| F9 | Anti-Hantu scan | Required |

---

## 📝 Usage Example

```markdown
[After 333_CONTEXT: Dark mode implementation]

AI: [Executes 555_SAFETY]
  → Stakeholders: End Users, Maintainers, Community
  → Weakest: Future Maintainers (κ = 0.78)
  → Empathy κᵣ: 0.78 ≥ 0.70 ✅
  → Reversibility: FULLY (git + flag)
  → Peace²: 0.855 (acceptable for SOFT)
  → Verdict: ALIGN
  → Condition: Add documentation
  
Proceeding to 777_IMPLEMENT...
```

---

## 🔄 000-999 Loop Integration

```
Previous: 333_CONTEXT (Mapping)
Current:  555_SAFETY (Empathy)
Next:     777_IMPLEMENT (Forge)
        or 333_CONTEXT (if SABAR)
        or TERMINATE (if VOID)

Connection: Safety gates implementation
```

**Loop Reference:** The HEART of the system — empathy before action.

---

**DITEMPA BUKAN DIBERI**
