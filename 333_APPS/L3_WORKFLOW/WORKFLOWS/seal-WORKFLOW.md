# Workflow: seal
**Stage:** 999 (Commit)  
**Purpose:** Persist verdict/solution/session to VAULT999, apply Phoenix-72 cooling if needed.  
**Trigger:** After audit-WORKFLOW renders a SEAL verdict.  
**Output:** Immutable vault entry and Merkle proof.

---

## 📋 Workflow Steps

### Step 1: Merkle Proof Generation
1. Hash all stage outputs and implementation artifacts.
2. Link to the previous vault entry.

### Step 2: Vault Commitment
1. Append entry to `VAULT999/vault999.jsonl`.
2. Sync metadata to `metadata/floor_status.json`.

### Step 3: Cooling & Handoff (Phoenix)
1. Apply Phoenix-72 protocol if irreversible work was done.
2. Capture TODOs and pending impacts.

### Step 4: Loop Closure
1. Reset session state.
2. Prepare for the next 000_INIT.
3. Final Signal: "SEALED. DITEMPA BUKAN DIBERI."

---

## 📝 Output Specification
```yaml
commitment:
  seal_id: "..."
  merkle_root: "..."
  vault_status: "SUCCESS"
  timestamp: "..."
```

---

**DITEMPA BUKAN DIBERI**
