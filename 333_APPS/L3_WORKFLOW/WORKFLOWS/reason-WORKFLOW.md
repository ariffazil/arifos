# Workflow: reason
**Stage:** 222 (Think)  
**Purpose:** Pure logical inference on the anchored query, hypotheses, truth scoring.  
**Trigger:** After anchor-WORKFLOW completes.  
**Output:** Logical derivation and hypothesis set.

---

## 🎯 When to Use
Use this to analyze the anchored intent using deep logical inference before gathering heavy external context.

---

## 📋 Workflow Steps

### Step 1: Contrast Detection
1. Identify tensions/oppositions in the request (e.g., "fast vs safe").
2. Predict user goals vs explicit requests.

### Step 2: Hypothesis Generation
1. Generate 3 hypotheses:
   - Conservative (minimal change)
   - Optimistic (full feature/fix)
   - Novel (alternative perspective)

### Step 3: Truth Scoring (F2)
1. Assign initial truth confidence (τ) to hypotheses.
2. Identify dependencies that require external integration (Atlas).

### Step 4: Humility Audit (F7)
1. Bound uncertainty. Ω₀ ∈ [0.03, 0.05].
2. Identify what is NOT known at this stage.

---

## 📝 Output Specification
```yaml
reasoning:
  primary_hypothesis: "..."
  truth_score: 0.99
  uncertainty_bounds: [0.03, 0.05]
  contrasts: [...]
```

---

**DITEMPA BUKAN DIBERI**
