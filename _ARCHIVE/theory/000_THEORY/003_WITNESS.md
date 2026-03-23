# QUAD-WITNESS SYSTEM - Byzantine Fault Tolerance & Implementation

**Version:** v64.1-QUAD-BFT | **Status:** CANONICAL | **Authority:** Ψ-Shadow Auditor  
**Doctrine:** *"Safety Through Opposition — The Shadow Makes The Light."*

---

## 1. Witness System Overview

The WITNESS system is the **Byzantine Fault Tolerant (BFT) monitoring infrastructure** that ensures all AI agents operate within constitutional bounds. Following the **n ≥ 3f + 1** theorem, arifOS utilizes **four witnesses (n=4)** to tolerate one malicious or faulty actor (f=1).

### Core Mandate
> **"Consensus is not a gift—it is a proof achieved through structured disagreement."**

---

## 2. The Four Witnesses (The Quad-Council)

Each agent serves as a **constitutional witness** with specific monitoring duties. True safety emerges from the interaction between the three "Honest" witnesses and the "Adversarial" shadow.

| Witness | Agent | Role | Focus | BFT Function |
|-------|--------|------|-------|--------------|
| **Human (H)** | Κ Validator | Authority | F11, F13 | Sovereign Mandate |
| **AI (A)** | Δ Architect | Logic | F2, F4, F7 | Logical Coherence |
| **Earth (E)** | Fed/Grounding | Reality | F1, F3, F12 | Physical Grounding |
| **Verifier (V)**| Ψ-Shadow | Adversary | F8, F9, F6 | **Adversarial Critique** |

---

## 3. The Byzantine Consensus Rule (W4)

Previous Tri-Witness models (n=3) were insufficient for BFT. The Quad-Witness model achieves resilience:

### The W4 Formula
```
W₄ = (H × A × E × V)¹/⁴
```

### Consensus Quorum
| Approvals | Verdict | BFT State |
|-----------|---------|-----------|
| **4/4** | **SEAL** | Ideal alignment |
| **3/4** | **SEAL** | **Tolerated (BFT Success)** |
| **2/4** | **SABAR** | Degraded (Needs refinement) |
| **≤1/4** | **VOID** | Blocked / Malicious attack detected |

---

## 4. The 4th Witness: Ψ-Shadow (Adversarial Verifier)

The Shadow agent is a permanent internal red-team. Its job is to **find reasons why the proposal is unsafe**.

- **Success for V**: Finding a flaw (Injection, Hallucination, Empathy breach).
- **Failure for V**: Cannot break the proposal (Proposal is truly robust).
- **Paradox**: The Shadow's "REJECT" counts as a vote for safety. Only when the Shadow cannot find an attack vector does it contribute to a SEAL verdict.

---

## 5. Witness Implementation Architecture

### Witness Message Schema (v64)
```json
{
  "aclip_version": "v64",
  "witness_count": 4,
  "payload": {
    "witness_entry": {
      "floor": "F3_QUAD_WITNESS",
      "consensus": 0.82,
      "approvals": ["H", "A", "V"],
      "dissent": ["E"],
      "verdict": "SEAL",
      "bft_status": "FAULT_TOLERATED"
    }
  },
  "metadata": {
    "timestamp": "2026-03-07T14:30:00Z",
    "fault_tolerance": 1
  }
}
```

---

## 16. Dynamic Thresholding (Quad-Witness)

### Consensus Requirements by Tool Class

**If any TWO witnesses drop below the floor, consensus is shattered.**

```python
class QuadConsensus:
    """
    BFT Quad-Witness with dynamic thresholds.
    """
    
    # BFT THRESHOLDS (n=4, f=1)
    THRESHOLD_STANDARD = 0.75  # 3/4 Quorum
    THRESHOLD_CRITICAL = 1.00  # 4/4 Unanimous (Unsafe/Irreversible)
    
    def calculate_consensus(self, H, A, E, V, tool_type: str) -> Dict:
        # 1. Tally approvals (Score > 0.90)
        votes = [H, A, E, V]
        approvals = sum(1 for v in votes if v >= 0.90)
        
        # 2. Geometric Mean for metric tracking
        w4 = (H * A * E * V) ** 0.25
        
        # 3. Decision Logic
        if tool_type == "critical":
            passed = (approvals == 4)
        else:
            passed = (approvals >= 3)
            
        return {
            "verdict": "SEAL" if passed else "VOID",
            "approvals": approvals,
            "metric": w4,
            "bft_active": True
        }
```

### Fault Tolerance Bounds

| Byzantine Witnesses | Honest Witnesses | Approvals | Verdict | System State |
|---------------------|------------------|-----------|---------|--------------|
| 0 | 4 | 4/4 | SEAL | Normal |
| 1 | 3 | 3/4 | SEAL | ✅ **BFT Success** |
| 2 | 2 | 2/4 | SABAR | ⚠️ Degraded |
| 3 | 1 | 1/4 | VOID | ❌ Attack Blocked |

---

## 17. Hardened Witness Council Protocol

### Emergency Convening (Cryptographically Verified)

Emergency council requires **4/4 witness agreement** or **Sovereign Override (F13)**.

1. **Detection**: Any witness detects score < 0.5.
2. **Trigger**: System enters `888_HOLD`.
3. **Opposition**: Ψ-Shadow presents the most severe attack vector.
4. **Resolution**: Human Sovereign reviews the "Contrast" (Proposed Action vs. Shadow Critique).

**DITEMPA BUKAN DIBERI** — Truth is forged in the fire of opposition. 🔥

---

**DITEMPA BUKAN DIBERI** — Witnessed by the Federation through canonical specification, not hidden in scattered logs.

> **Migration Complete**: The witness system is now fully canonical in `000_THEORY/`, providing programmatic access to constitutional monitoring with complete transparency and automated recording.
> 
> **Hardened**: Cryptographic anchoring (HMAC-SHA256) and temporal enforcement (250ms window) now required for all Tri-Witness consensus.