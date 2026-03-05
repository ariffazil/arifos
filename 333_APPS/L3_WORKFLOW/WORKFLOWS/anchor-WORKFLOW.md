# Workflow: anchor
**Stage:** 000 (Ignition)  
**Purpose:** Session ignition + intent grounding + lane pre-classification.  
**Trigger:** Any new user interaction  
**Output:** Session context with verified authority and initial intent mapping.

---

## 🎯 When to Use
Use this workflow at the **start of every session** to ignite the arifOS mind and ground the user's intent.

---

## 📋 Workflow Steps

### Step 1: Session Creation & Ignition
1. Generate unique session ID.
2. Record timestamp (UTC).
3. Initialize constitutional state and load 13 Constitutional Floors (F1-F13).
4. Set thermodynamic budget (entropy limit).

### Step 2: Authority Verification (F11)
1. Verify sovereign token or actor identification.
2. Determine authority level (888_JUDGE, ADMIN, USER, GUEST).
3. Establish Tri-Witness Handshake (W₃ ≥ 0.95).

### Step 3: Injection Defense (F12)
1. Scan query for injection patterns or constitutional bypass attempts.
2. Verify environment integrity.

### Step 4: Intent Grounding
1. Extract key entities and domain (CODE, DOC, ARCH, etc.).
2. Basic lane pre-classification (HARD, SOFT, PHATIC).
3. Predicted needs analysis (Explicit vs Implicit).

---

## 📝 Output Specification
```yaml
anchor_state:
  session_id: "..."
  authority: "..."
  tri_witness: 0.97
  lane: "SOFT"
  entities: [...]
  status: "IGNITED"
```

---

**DITEMPA BUKAN DIBERI**
