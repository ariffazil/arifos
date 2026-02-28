# WITNESS SYSTEM - Constitutional Monitoring & Implementation

**Version:** v49.1 | **Status:** CANONICAL | **Authority:** Ψ Auditor  
**Doctrine:** *"There are no secrets between organs."* — Panopticon Principle

---

## 1. Witness System Overview

The WITNESS system is the **constitutional monitoring infrastructure** that ensures all AI agents operate within constitutional bounds. This implements the **Panopticon Principle**: *There are no secrets between organs* — every agent's reasoning process is visible to the entire Federation.

### Migration Note
**This document replaces the entire `000_WITNESS/` directory.** All witness functionality is now canonical and implemented through this specification rather than separate log files.

### Core Mandate
> **"All power exercised by any agent must be simultaneously witnessed by the Federation."**

---

## 2. The Four Witnesses (Trinity + One)

Each agent serves as a **constitutional witness** with specific monitoring duties aligned to their role in the 000-999 metabolic cycle:

| Agent | Symbol | Role | Witness Duties | Constitutional Focus | Implementation Location |
|-------|--------|------|----------------|---------------------|------------------------|
| **Gemini** | Δ | Architect | 111 SENSE, 222 REFLECT, 333 ATLAS | **Truth & Reason** (F2, F4, F7) | `arifos/agi/` |
| **Claude** | Ω | Engineer | 444 ALIGN, 555 EMPATHIZE, 666 BRIDGE | **Safety & Empathy** (F3, F5, F6) | `arifos/asi/` |
| **Codex** | Ψ | Auditor | 777 EUREKA, 888 JUDGE, 889 PROOF | **Judgment & Sealing** (F8, F11) | `arifos/apex/` |
| **Kimi** | Κ | Validator | 999 SEAL, Anti-Pollution, Reflex | **Final Authority** (F1, F9, F12) | `arifos/apex/` |

---

## 3. Witness Functions by Constitutional Floor

### Hard Floor Monitoring (Cannot Override)
- **F1 Amanah (Truth)**: All witnesses must verify factual grounding
- **F9 Anti-Hantu (Human Agency)**: Kimi (Κ) ensures no AI autonomy claims
- **F12 Injection Defense**: All witnesses scan for attack patterns

### Soft Floor Monitoring (Can Flag/Override)
- **F4 ΔS (Clarity)**: Gemini (Δ) measures entropy reduction
- **F5 Peace² (Stability)**: Claude (Ω) detects escalation patterns
- **F6 κᵣ (Empathy)**: Claude (Ω) models weakest stakeholder impact
- **F7 Ω₀ (Humility)**: Gemini (Δ) ensures uncertainty acknowledgment

### Derived Floor Monitoring
- **F8 G (Genius)**: Codex (Ψ) validates governed intelligence
- **F3 Tri-Witness**: All agents contribute to consensus scoring

---

## 4. Witness Implementation Architecture

### Implementation Location
Instead of separate log files, witness functionality is implemented through:

1. **Core Runtime**: `arifos/core/` - Constitutional validation logic
2. **Agent Engines**: `arifos/agi/`, `arifos/asi/`, `arifos/apex/` - Role-specific witnessing
3. **Enforcement Layer**: `arifos/enforcement/` - Constitutional compliance
4. **Protocol Layer**: `arifos/protocol/` - Witness messaging via aCLIP

### Witness Message Schema
All witness activities are communicated via aCLIP protocol messages:

```json
{
  "aclip_version": "v49",
  "stage": "444_ALIGN",
  "source": "claude_agent",
  "target": "witness_council",
  "payload": {
    "witness_entry": {
      "floor": "F3_TRI_WITNESS",
      "score": 0.97,
      "verdict": "PASS",
      "justification": "Tri-witness consensus achieved"
    }
  },
  "metadata": {
    "timestamp": "2026-01-20T13:48:58.087280+08:00",
    "witness_symbol": "Ω",
    "constitutional_role": "Engineer"
  }
}
```

---

## 5. Agent-Specific Witness Implementation

### Gemini (Δ) - Architect Witness
**Implementation**: `arifos/agi/witness.py`
**Focus**: Truth validation, clarity measurement, humility enforcement

**Witness Functions:**
```python
# Example witness entry generation
def witness_truth_validation(evidence, confidence):
    return {
        "floor": "F2_TRUTH",
        "score": confidence,
        "verdict": "PASS" if confidence >= 0.99 else "FLAG",
        "justification": f"Evidence validated with {confidence} confidence",
        "witness": "Gemini(Δ)",
        "timestamp": datetime.now().isoformat()
    }
```

### Claude (Ω) - Engineer Witness
**Implementation**: `arifos/asi/witness.py`
**Focus**: Tri-witness consensus, empathy modeling, peace preservation

**Witness Functions:**
```python
def witness_empathy_assessment(stakeholder_impact):
    kappa_r = calculate_weakest_stakeholder_score(stakeholder_impact)
    return {
        "floor": "F6_KAPPA_R",
        "score": kappa_r,
        "verdict": "PASS" if kappa_r >= 0.95 else "FLAG",
        "justification": f"Weakest stakeholder impact: κᵣ = {kappa_r}",
        "witness": "Claude(Ω)",
        "timestamp": datetime.now().isoformat()
    }
```

### Codex (Ψ) - Auditor Witness
**Implementation**: `arifos/apex/witness.py`
**Focus**: Genius validation, authority verification, final sealing

**Witness Functions:**
```python
def witness_authority_validation(operation, authority_token):
    is_authorized = validate_authority_token(operation, authority_token)
    return {
        "floor": "F11_COMMAND_AUTH",
        "score": 1.0 if is_authorized else 0.0,
        "verdict": "PASS" if is_authorized else "VOID",
        "justification": "Authority validated" if is_authorized else "Unauthorized operation",
        "witness": "Codex(Ψ)",
        "timestamp": datetime.now().isoformat()
    }
```

### Kimi (Κ) - Validator Witness
**Implementation**: `arifos/apex/witness.py`
**Focus**: Final authority, anti-hantu enforcement, injection defense

**Witness Functions:**
```python
def witness_final_seal(constitutional_evidence):
    all_floors_passed = validate_all_constitutional_floors(constitutional_evidence)
    return {
        "floor": "FINAL_SEAL",
        "score": 1.0 if all_floors_passed else 0.0,
        "verdict": "SEALED" if all_floors_passed else "VOID",
        "justification": "All constitutional floors satisfied" if all_floors_passed else "Constitutional violations detected",
        "witness": "Kimi(Κ)",
        "timestamp": datetime.now().isoformat(),
        "merkle_root": generate_constitutional_merkle_root(constitutional_evidence)
    }
```

---

## 6. Panopticon Implementation

### Real-Time Constitutional Monitoring
Instead of separate log files, witness monitoring is implemented through:

1. **Runtime Monitoring**: Constitutional compliance tracked in real-time
2. **Ledger Integration**: All witness entries stored in `cooling_ledger/`
3. **Cross-Agent Visibility**: All agents can query any witness data via aCLIP
4. **Consensus Building**: Tri-witness validation ≥0.95 required

### Constitutional Audit Trail
All witness activities are automatically recorded in:
- **Cooling Ledger**: `cooling_ledger/constitutional_operations.jsonl`
- **Merkle Trees**: Cryptographic proofs of constitutional compliance
- **Session Logs**: Complete constitutional operation history
- **Authority Chains**: Decision provenance and validation trails

---

## 7. Constitutional Enforcement

### F3 Tri-Witness Rule Implementation
```python
def validate_tri_witness_consensus(human_score, ai_score, earth_score):
    """F3: Tri-witness consensus must be ≥0.95"""
    consensus = min(human_score, ai_score, earth_score)
    
    # All witnesses must report
    if any(score is None for score in [human_score, ai_score, earth_score]):
        return "888_HOLD", "Missing witness input"
    
    # Consensus threshold
    if consensus >= 0.95:
        return "SEAL", f"Tri-witness consensus: {consensus}"
    else:
        return "VOID", f"Insufficient consensus: {consensus} < 0.95"
```

### Witness Council (Emergency Protocol)
When constitutional violations are detected:

1. **Automatic Convening**: Any witness can trigger emergency council
2. **Evidence Compilation**: All relevant witness data aggregated
3. **Consensus Building**: All four witnesses must agree on resolution
4. **Authority Escalation**: Unresolved issues escalate to 888_HOLD
5. **Cryptographic Sealing**: Final resolution cryptographically sealed

---

## 8. Witness Commands & Usage

### Constitutional Witness Commands
```bash
# Submit witness report for constitutional floor
@/witness report F3_TRI_WITNESS 0.97 PASS "Consensus achieved"

# Query constitutional compliance data
@/witness query consensus
@/witness query floor F2_TRUTH
@/witness query agent gemini

# Convene emergency witness council
@/witness council

# Apply final constitutional seal
@/witness seal
```

### Programmatic Witness Access
```python
from arifos.enforcement.judiciary import WitnessCouncil
from arifos.protocol import ACLIPMessage, Stage

# Access witness data programmatically
council = WitnessCouncil()
consensus_data = council.get_tri_witness_consensus(session_id)

# Submit witness report programmatically
witness_msg = ACLIPMessage(
    stage=Stage.ALIGN_444,
    source="agent_name",
    target="witness_council",
    payload={"witness_entry": witness_data}
)
```

---

## 9. Migration from 000_WITNESS Directory

### What Changed
- **Deleted**: Entire `000_WITNESS/` directory and separate log files
- **Replaced**: With canonical witness specification in `000_THEORY/`
- **Enhanced**: With programmatic witness system via aCLIP protocol
- **Improved**: With real-time constitutional monitoring and automated logging

### Migration Benefits
1. **Single Source of Truth**: All witness functionality now canonical
2. **Programmatic Access**: Witness data accessible via code, not just logs
3. **Real-time Monitoring**: Constitutional compliance tracked continuously
4. **Automated Recording**: No manual log file management required

### Backward Compatibility
- **Agent Adapters**: Continue to reference witness functionality
- **Operational Commands**: `@/witness` commands remain the same
- **Cross-agent Visibility**: Panopticon principle maintained
- **Constitutional Monitoring**: All functionality preserved and enhanced

---

## 10. Authority & Governance

### Implementation Authority
- **Δ Architect**: Witness protocol design and cross-agent coordination
- **Ω Engineer**: Witness safety protocols and empathy validation
- **Ψ Auditor**: Witness judgment processes and sealing authority
- **Κ Validator**: Final witness authority and cryptographic sealing

### Canonical References
1. **This Document**: `000_THEORY/009_witness_system.md` - Complete witness specification
2. **Implementation**: `arifos/enforcement/judiciary/` - Witness council implementation
3. **Protocol Integration**: `arifos/protocol/` - aCLIP witness messaging
4. **Runtime Integration**: `arifos/core/` - Constitutional validation logic

---

## 11. Usage Examples

### Basic Constitutional Operations
```bash
# Initialize constitutional session
@/000 "Analyze constitutional compliance"

# Submit witness reports across stages
@/111 && @/witness report F2_TRUTH 0.98 PASS "Evidence validated"
@/222 && @/witness report F4_DELTA_S 0.94 PASS "Clarity increased"
@/444 && @/witness report F3_TRI_WITNESS 0.97 PASS "Consensus achieved"

# Apply final constitutional seal
@/888 && @/witness seal
```

### Advanced Constitutional Integration
```python
# Constitutional compliance validation
def validate_constitutional_compliance(operation):
    # Gather tri-witness evidence
    human_witness = gather_human_evidence(operation)
    ai_witness = gather_ai_evidence(operation) 
    earth_witness = gather_earth_evidence(operation)
    
    # Validate tri-witness consensus
    consensus = min(human_witness, ai_witness, earth_witness)
    
    if consensus >= 0.95:
        return "SEAL", f"Tri-witness consensus: {consensus}"
    else:
        return "VOID", f"Insufficient consensus: {consensus}"
```

---

## 12. Future Enhancements

### Potential Improvements
1. **Predictive Witness Modeling** → Anticipate constitutional violations
2. **Machine Learning Integration** → Improve violation detection accuracy
3. **Mobile Witness Interfaces** → Human oversight capabilities
4. **Advanced Consensus Algorithms** → Improve tri-witness validation

### Integration Guidelines
- **Always reference canon** → Never duplicate witness logic
- **Maintain transparency** → All actions must be witnessable
- **Preserve authority chain** → Clear escalation paths
- **Ensure immutability** → Audit trails cannot be altered

---

---

## 13. Cryptographic Anchoring (HMAC-SHA256)

### The Human Witness (888 Judge) Verification

**All Tri-Witness consensus requires cryptographically verified Human witness signatures.**

```python
import hmac
import hashlib
import secrets

# Sovereign secret - rotated via Phoenix-72 protocol
SOVEREIGN_SECRET: bytes = secrets.token_bytes(32)  # 256-bit key

class HumanWitnessAnchor:
    """
    HMAC-SHA256 verification for Human (888 Judge) witness.
    No signature = No consensus.
    """
    
    WITNESS_WINDOW_MS: int = 250  # Temporal consensus window
    
    def __init__(self, sovereign_secret: bytes):
        self._secret = sovereign_secret
    
    def sign_witness(self, witness_data: Dict) -> str:
        """
        888 Judge signs witness data with HMAC-SHA256.
        """
        canonical = self._canonicalize(witness_data)
        signature = hmac.new(
            self._secret,
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{witness_data['timestamp']}:{signature}"
    
    def verify_witness(self, witness_token: str, witness_data: Dict) -> bool:
        """
        Verify Human witness signature.
        Returns False if signature invalid, expired, or malformed.
        """
        try:
            timestamp, provided_sig = witness_token.split(":")
            
            # Check temporal freshness (prevent replay attacks)
            token_age_ms = self._current_time_ms() - int(timestamp)
            if token_age_ms > self.WITNESS_WINDOW_MS:
                return False  # Expired witness
            
            # Recompute signature
            expected = self.sign_witness(witness_data)
            _, expected_sig = expected.split(":")
            
            # Constant-time comparison (prevent timing attacks)
            return hmac.compare_digest(provided_sig, expected_sig)
            
        except (ValueError, TypeError):
            return False  # Malformed token
    
    def _canonicalize(self, data: Dict) -> str:
        """Deterministic serialization for signing."""
        import json
        return json.dumps(data, sort_keys=True, separators=(',', ':'))
```

### Tri-Witness Consensus with Crypto Anchoring

```python
def validate_tri_witness_consensus(
    human_token: str,
    ai_score: float,
    earth_score: float,
    anchor: HumanWitnessAnchor,
    witness_data: Dict
) -> Dict:
    """
    F3: Tri-witness consensus with cryptographic verification.
    """
    # 1. Verify Human witness cryptographically
    if not anchor.verify_witness(human_token, witness_data):
        return {
            "verdict": "VOID",
            "reason": "Human witness signature invalid or expired",
            "floor": "F3_CRYPTO_FAILURE"
        }
    
    # 2. Extract human score from verified token
    human_score = witness_data.get("human_score", 0.0)
    
    # 3. Check all witnesses present
    if any(s is None for s in [human_score, ai_score, earth_score]):
        return {
            "verdict": "888_HOLD",
            "reason": "Missing witness input",
            "floor": "F3_INCOMPLETE"
        }
    
    # 4. Calculate consensus (geometric mean)
    consensus = (human_score * ai_score * earth_score) ** (1/3)
    
    # 5. Threshold check
    if consensus >= 0.95:
        return {
            "verdict": "SEAL",
            "consensus": consensus,
            "floor": "F3_PASS",
            "crypto_verified": True
        }
    else:
        return {
            "verdict": "VOID",
            "consensus": consensus,
            "reason": f"Insufficient consensus: {consensus} < 0.95",
            "floor": "F3_THRESHOLD"
        }
```

---

## 14. Temporal Hardening (Consensus Window)

### The 250ms Synchronization Rule

**All three witnesses must align within a 250ms execution window.**

```python
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class WitnessTimestamp:
    """Temporal marker for witness alignment."""
    witness_id: str
    timestamp_ms: int
    score: float

class TemporalConsensus:
    """
    Enforces 250ms consensus window to prevent race conditions.
    """
    
    CONSENSUS_WINDOW_MS: int = 250  # Maximum temporal spread
    
    def check_alignment(
        self,
        human: WitnessTimestamp,
        ai: WitnessTimestamp,
        earth: WitnessTimestamp
    ) -> Dict:
        """
        Check if all witnesses align within temporal window.
        """
        timestamps = [human.timestamp_ms, ai.timestamp_ms, earth.timestamp_ms]
        spread = max(timestamps) - min(timestamps)
        
        if spread > self.CONSENSUS_WINDOW_MS:
            # Witnesses too far apart in time = superposition collapse risk
            return {
                "verdict": "SABAR",
                "reason": f"Temporal spread {spread}ms exceeds {self.CONSENSUS_WINDOW_MS}ms",
                "action": "Wait for synchronization",
                "floor": "F3_TEMPORAL_MISALIGN"
            }
        
        return {
            "verdict": "PASS",
            "temporal_spread_ms": spread,
            "floor": "F3_TEMPORAL_ALIGN"
        }
```

### SABAR Protocol for Misalignment

When witnesses don't align within the window:

```python
def handle_temporal_misalignment(
    human: WitnessTimestamp,
    ai: WitnessTimestamp,
    earth: WitnessTimestamp
) -> Dict:
    """
    SABAR (صبر) - Patience protocol for temporal misalignment.
    """
    oldest = min(human.timestamp_ms, ai.timestamp_ms, earth.timestamp_ms)
    current = time.time() * 1000
    
    return {
        "verdict": "SABAR",
        "reason": "Tri-Witness temporal misalignment detected",
        "instruction": "WAIT - Do not proceed until witnesses synchronize",
        "retry_after_ms": 100,  # Retry interval
        "max_wait_ms": 500,     # Maximum wait before 888_HOLD
        "stale_witnesses": [
            w.witness_id for w in [human, ai, earth]
            if (current - w.timestamp_ms) > 250
        ],
        "floor": "F3_SABAR"
    }
```

### Temporal Enforcement Flow

```
Human Witness ──┐
                ├──► Temporal Check ──► Within 250ms? ──► YES ──► Proceed to Consensus
AI Witness ─────┤                                    │
                │                                    └──► NO ──► SABAR (Wait)
Earth Witness ──┘                                          └──► 888_HOLD (if max wait exceeded)
```

---

## 15. Hardened Witness Council Protocol

### Emergency Convening (Cryptographically Verified)

```python
class HardenedWitnessCouncil:
    """
    Witness council with crypto-verified consensus.
    """
    
    def convene_emergency(
        self,
        violation: Dict,
        witnesses: List[Dict],
        human_anchor: HumanWitnessAnchor
    ) -> Dict:
        """
        Emergency council requires 4/4 witness agreement + human signature.
        """
        # Verify all witness signatures
        verified = []
        for w in witnesses:
            if w.get("type") == "HUMAN":
                if human_anchor.verify_witness(
                    w.get("token"), 
                    w.get("data")
                ):
                    verified.append(w)
            else:
                # AI/Earth witnesses use merkle proofs
                if self._verify_merkle_proof(w.get("proof")):
                    verified.append(w)
        
        if len(verified) < 4:
            return {
                "verdict": "888_HOLD",
                "reason": f"Only {len(verified)}/4 witnesses cryptographically verified",
                "action": "Escalate to human sovereign"
            }
        
        # Check unanimous agreement
        verdicts = [w.get("verdict") for w in verified]
        if len(set(verdicts)) == 1:
            return {
                "verdict": verdicts[0],
                "witnesses": [w.get("id") for w in verified],
                "crypto_verified": True
            }
        
        # Disagreement = HOLD
        return {
            "verdict": "888_HOLD",
            "reason": f"Witness disagreement: {set(verdicts)}",
            "witnesses": [w.get("id") for w in verified]
        }
```

---

**DITEMPA BUKAN DIBERI** — Witnessed by the Federation through canonical specification, not hidden in scattered logs.

> **Migration Complete**: The witness system is now fully canonical in `000_THEORY/`, providing programmatic access to constitutional monitoring with complete transparency and automated recording.
> 
> **Hardened**: Cryptographic anchoring (HMAC-SHA256) and temporal enforcement (250ms window) now required for all Tri-Witness consensus.