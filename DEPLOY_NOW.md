# arifOS MCP - Deploy Fixes to Railway
**Critical: One-line fix unblocks entire pipeline**

---

## Status

| Component | Status |
|-----------|--------|
| Server | ✅ Online (Railway) |
| 19 Tools | ✅ Reachable |
| Governance Gates | ✅ Working (correctly blocking) |
| **Login Flow** | ❌ **Broken (fixed in source, needs deploy)** |

---

## The Fix

**Root Cause:** `init_anchor` sets `claim_status = "accepted"` but deployed server only knows:
- `anonymous`, `claimed`, `anchored`, `verified`

**One-line fix in source:**
```python
# arifosmcp/runtime/models.py
class ClaimStatus(str, Enum):
    ANONYMOUS = "anonymous"
    CLAIMED = "claimed" 
    ANCHORED = "anchored"
    VERIFIED = "verified"
    ACCEPTED = "accepted"              # ← ADDED
    REJECTED = "rejected"              # ← ADDED
    DEMOTED = "demoted"                # ← ADDED
    REJECTED_PROTECTED_ID = "rejected_protected_id"  # ← ADDED
```

---

## Deploy Steps (Railway)

```bash
# 1. Push to main branch
git add .
git commit -m "Fix: ClaimStatus enum for init_anchor"
git push origin main

# 2. Railway auto-deploys
# Or manually: railway up

# 3. Verify deployment
curl https://arifosmcp-production.up.railway.app/health
```

---

## Post-Deploy Verification

Run these checks in order:

### 1. Badge in (should work now)
```json
{
  "tool": "init_anchor",
  "args": {
    "actor_id": "operator-test",
    "intent": {"query": "Test", "task_type": "audit"}
  }
}
```
**Expected:** `verdict: "SEAL"`, `claim_status: "accepted"`

### 2. Access downstream tools
```json
{
  "tool": "arifOS_kernel", 
  "args": {
    "query": "Complete 000-999 pipeline",
    "session_id": "<from_step_1>"
  }
}
```
**Expected:** Pipeline completes without `BRIDGE_FAILURE`

### 3. Reality check
```json
{
  "tool": "physics_reality",
  "args": {"mode": "search", "input": "test query"}
}
```
**Expected:** Returns envelope with `tool: "physics_reality"`

### 4. Vault seal
```json
{
  "tool": "vault_ledger",
  "args": {"mode": "verify"}
}
```
**Expected:** Finds VAULT999/vault999.jsonl

---

## What Changes

| Before | After |
|--------|-------|
| Login → Internal error → Stuck in lobby | Login → SEAL → Full access |
| All tools blocked (correctly, but frustratingly) | Tools unlock after proper anchor |
| "accepted" not recognized | "accepted" valid claim status |

---

## Risk Assessment

**Low Risk.** This is:
- Adding enum values (not removing)
- Backward compatible
- Only affects claim status strings
- No logic changes

**Rollback:** Revert commit, redeploy.

---

## One-Line Truth

> Fix the front door, and the whole building opens.

Deploy when ready.

---

*Ditempa Bukan Diberi* 🔨💎
