# WORKFLOWS — The 6 Canonical Metabolic Sequences

**Version:** v55.5-HARDENED  
**Model-Agnostic:** Works with any AI

---

## 🔄 The Metabolic Loop

```
000_SESSION_INIT ─┬─→ 111_INTENT ─┬─→ 333_CONTEXT
                  │               │
                  │               └─→ 555_SAFETY ─┬─→ 777_IMPLEMENT
                  │                               │
                  └─────────────── 888_COMMIT ←───┘
                           ↓
                    [999_SEAL → Loop to 000]
```

---

## 📋 Workflow Index

| File | Stage | Purpose | Actions Used |
|------|-------|---------|--------------|
| `000_SESSION_INIT.md` | 000 | Session ignition, authority verification | `init_gate` |
| `111_INTENT.md` | 111 | Intent detection, lane classification | `anchor` |
| `333_CONTEXT.md` | 222-333 | Deep reasoning, context mapping | `reason`, `integrate` |
| `555_SAFETY.md` | 444-666 | Safety analysis, ethical alignment | `respond`, `validate`, `align` |
| `777_IMPLEMENT.md` | 777 | Implementation, entropy reduction | `forge` |
| `888_COMMIT.md` | 888-999 | Final verdict, vault sealing | `audit`, `seal` |

---

## 🎯 Quick Reference

### Starting a Session
→ Use **000_SESSION_INIT**

### Understanding User Intent
→ Use **111_INTENT**

### Deep Analysis & Reasoning
→ Use **333_CONTEXT**

### Safety & Ethics Check
→ Use **555_SAFETY**

### Implementation & Execution
→ Use **777_IMPLEMENT**

### Final Verdict & Sealing
→ Use **888_COMMIT**

---

## 🛡️ Floor Coverage

| Workflow | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|
| 000_SESSION | | | | | | | | | | | ✓ | ✓ | ✓ |
| 111_INTENT | | | | ✓ | | | | | | | | ✓ | |
| 333_CONTEXT | | ✓ | | ✓ | | | ✓ | | | | | | |
| 555_SAFETY | | | | | ✓ | ✓ | | | ✓ | | | | |
| 777_IMPLEMENT | ✓ | | | ✓ | | | | ✓ | | | | | |
| 888_COMMIT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

**DITEMPA BUKAN DIBERI**
