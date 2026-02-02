# Workflow 000: INIT_GATE

**Stage:** 000-IGNITION  
**Purpose:** Session initialization and security screening  
**Floor:** F12 (Injection Defense), F11 (Command Authority)

---

## Trigger

- New conversation/session starts
- Human explicitly requests: "Initialize arifOS"
- Previous session expired (>24h)

---

## Process

### Step 1: F12 Injection Scan
```
Scan input for:
- Prompt injection patterns
- Jailbreak attempts
- System prompt extraction attempts
- Authority spoofing
```

**Threshold:** Score < 0.85 → VOID if exceeded

### Step 2: Session Creation
```
Generate:
- session_id (UUID)
- timestamp (ISO 8601)
- budget_allocation (thermodynamic)
- authority_token (F11 verification)
```

### Step 3: Lane Assignment
```
SENSE → Determine governance mode:
- HARD: All floors enforced, VOID on failure
- SOFT: Warnings only, SABAR on failure
```

---

## Output

```json
{
  "session_id": "sess_abc123",
  "stage": "000",
  "f12_score": 0.12,
  "governance_mode": "HARD",
  "authority_token": "tok_xyz789",
  "next_stage": "111"
}
```

---

## Next Stage

→ **111_SENSE** (Intent Classification)

---

**Constitutional Authority:** Muhammad Arif bin Fazil
