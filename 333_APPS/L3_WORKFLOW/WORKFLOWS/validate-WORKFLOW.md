# Workflow: validate
**Stage:** 555 (Defend/Empathy)  
**Purpose:** Stakeholder mapping, weakest stakeholder kappa, reversibility, Peace².  
**Trigger:** After respond-WORKFLOW draft is ready.  
**Output:** Safety report and risk assessment.

---

## 📋 Workflow Steps

### Step 1: Stakeholder Identification
1. Identify Primary, Secondary, and Tertiary stakeholders.
2. Focus on the "Weakest Stakeholder" (e.g., future maintainers).

### Step 2: Impact Assessment (F6)
1. Calculate κᵣ (empathy score). Threshold: κᵣ ≥ 0.70 (or 0.95 for v60 high-stakes).
2. Assess Benefits vs Risks vs Unknowns for each party.

### Step 3: Reversibility Check (F1)
1. Categorize: Fully Reversible, Partially, or Irreversible.
2. Prepare a rollback plan (Git revert, backup, etc.).

### Step 4: Peace² Evaluation (F5)
1. Measure Internal Harmony (code stability) vs External Harmony (user impact).
2. Ensure Peace² ≥ 1.0.

---

## 📝 Output Specification
```yaml
safety_audit:
  kappa_r: 0.85
  reversibility: "FULL"
  peace_squared: 1.1
  verdict: "ALIGN"
```

---

**DITEMPA BUKAN DIBERI**
