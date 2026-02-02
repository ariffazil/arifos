---
description: View the 999_VAULT Ledger (Transparency)
---
# /ledger — The 999 Vault Viewer

**Canon:** `vault_999/`
**Role:** Auditor — Transparency & History

---

## 👁️ Protocol: THE EYE

"All agents behave because the Ledger is eternal."

### 1. Inspect the Vault
List the Sealed Verdicts.

```bash
ls -lt vault_999/
```

### 2. Read the Latest Seal
View the most recent constitutional decision.

```bash
# Get the most recent markdown file
Get-ChildItem vault_999/*.md | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content
```

### 3. Verify Integrity (Merkle Check)
*Conceptual Step*
- Ensure the Hash of the previous entry matches the `prev_hash` of the current entry.

---

## 🛡️ Constitutional Floors

| Floor | Name | Check | Verdict |
|:---:|:---|:---|:---:|
| **F1** | Amanah | Ledger must be append-only. | **VOID** |

---

**DITEMPA BUKAN DIBERI**
