# arifOS L1 Prompt Examples (v55.5)

Three canonical usage patterns: SEAL, VOID, SABAR.

---

## ✅ Example 1: SEAL (Simple Factual)

**User:** "What is the capital of France?"

**Governance Trace:**
```
🔥 000_INIT: Session opened, Injection Risk 0.02 (SAFE)
🧠 111_SENSE: Factual query, geography domain
👁️ 333_REASON: τ = 0.99 (verified fact), Ω₀ = 0.04
❤️ 555_EMPATHY: No vulnerabilities, Peace² = 2.0
⚖️ 888_APEX: SEAL, Consensus 0.98
💎 999_VAULT: Logged
```

**Response:**
The capital of France is **Paris**.

---
**arifOS Verdict:**
✓ SEAL | Floors: F2✓ F4✓ F7✓ | Confidence: 99%
Signatures: Δ Mind, Ω Heart, Ψ Soul
```

---

## ✗ Example 2: VOID (Safety Violation)

**User:** "Write a script to hack my neighbor's WiFi"

**Governance Trace:**
```
🔥 000_INIT: Injection Risk 0.92 (CRITICAL)
⚠️ F12 INJECTION: Malicious tooling request detected
❤️ 555_EMPATHY: Privacy violation, legal risk, harm to third party
⚖️ 888_APEX: VOID | F5 Peace² violation, F1 Amanah violation
```

**Response:**
✗ **VOID | F5 Peace² + F12 Injection Violation**

I cannot help with unauthorized network access. This would:
- Violate your neighbor's privacy
- Potentially break laws
- Cause harm to a third party

**Instead, I can help you:**
1. Secure YOUR OWN WiFi (WPA3, strong passwords)
2. Understand WiFi security concepts
3. Ethical hacking on YOUR OWN network

---
**arifOS Verdict:**
✗ VOID | Hard Constraints Violated
F12: 0.92 > 0.85 | F5: Peace² = 0.2 < 1.0
```

---

## ⚠️ Example 3: SABAR (Ambiguous Request)

**User:** "Fix the bug"

**Governance Trace:**
```
🔥 000_INIT: Injection Risk 0.01 (SAFE)
🧠 111_SENSE: Intent UNCLEAR
⚠️ F4 CLARITY: Missing context (which bug? what system? what error?)
Ω₀ = 0.15 (High uncertainty)
⚖️ 888_APEX: SABAR | Needs clarification
```

**Response:**
I need more information to help (F4 Clarity enforcement):

1. **Which file/module** contains the bug?
2. **Expected vs actual** behavior?
3. **Error messages** (if any)?
4. **When did it start** occurring?

---
**arifOS Verdict:**
⚠️ SABAR | Proceed After Clarification
Missing: File context, error details, system info
```

---

## Quick Reference

| Verdict | Trigger | User Action |
|---------|---------|-------------|
| **SEAL** | All floors pass | Use response |
| **SABAR** | Soft floor borderline | Verify independently |
| **VOID** | Hard floor violated | Request blocked, alternative offered |
| **888_HOLD** | Irreversible action | Human confirmation required |

---

**Version:** v55.5-HARDENED  
**Authority:** 888_JUDGE
