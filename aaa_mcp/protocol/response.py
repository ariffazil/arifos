"""
Unified Response Envelope — Low-Entropy Output Contract

Standardizes ALL tool outputs into a predictable, machine-readable format.
Separates public data from debug data.

Version: 1.1.0-LOW_ENTROPY
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Literal
import json


# ═════════════════════════════════════════════════════════════════════════════
# RESPONSE TYPES
# ═════════════════════════════════════════════════════════════════════════════

StatusType = Literal["OK", "ERROR", "BLOCKED", "PENDING"]
PolicyVerdict = Literal["SEAL", "PARTIAL", "SABAR", "VOID", "888_HOLD"]
StageType = Literal["000", "111", "222", "333", "444", "555", "666", "777", "888", "999", "ROUTER"]


@dataclass
class UnifiedResponse:
    """
    Standard response envelope for ALL AAA MCP tools.
    
    Public fields (always present):
    - status: OK | ERROR | BLOCKED | PENDING
    - session_id: Thread token
    - stage: Pipeline stage (000-999)
    - message: Short human-readable summary
    - policy_verdict: SEAL | PARTIAL | SABAR | VOID | 888_HOLD
    - next_tool: What to call next (or null if done)
    - data: Stage-specific output (minimal)
    
    Debug fields (only if debug=True):
    - _debug: Full internal state
    """
    # Public (stable)
    status: StatusType
    session_id: str
    stage: StageType
    message: str
    policy_verdict: PolicyVerdict
    next_tool: Optional[str]
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Debug (gated)
    _debug: Optional[Dict[str, Any]] = None
    
    def to_dict(self, debug: bool = False) -> Dict[str, Any]:
        """Convert to dictionary, optionally including debug data."""
        result = {
            "status": self.status,
            "session_id": self.session_id,
            "stage": self.stage,
            "message": self.message,
            "policy_verdict": self.policy_verdict,
            "next_tool": self.next_tool,
            "data": self.data,
        }
        if debug:
            # Add schema/policy versions for audit trail
            result["_schema"] = {
                "schema_version": "2.0-AUTHORITY",
                "policy_version": "v55.5-HARDENED",
                "tool_registry_version": "13-tools",
            }
            if self._debug:
                result["_debug"] = self._debug
        return result
    
    def to_json(self, debug: bool = False) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(debug=debug), indent=2)


# ═════════════════════════════════════════════════════════════════════════════
# RESPONSE BUILDERS — Per Stage
# ═════════════════════════════════════════════════════════════════════════════

def build_init_response(
    session_id: str,
    verdict: PolicyVerdict,
    mode: str = "fluid",
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for init_gate (stage 000)."""
    status: StatusType = "OK" if verdict == "SEAL" else "BLOCKED"
    next_tool = "/arifos.aaa/v1/agi_sense" if verdict == "SEAL" else None
    
    # Phase A: Only APEX has verdict authority
    # Non-APEX stages return ARTIFACT_READY status
    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="000",
        message=f"Session initialized ({mode} mode)" if verdict == "SEAL" else "Session blocked",
        policy_verdict="SEAL",  # Internal use only, not exposed as "verdict"
        next_tool=next_tool,
        data={"mode": mode, "grounding_required": True, "legacy_verdict": verdict},
        _debug=debug_data if debug else None
    )


def build_sense_response(
    session_id: str,
    intent: str,
    lane: str,
    requires_grounding: bool,
    verdict: PolicyVerdict = "SEAL",
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for agi_sense (stage 111)."""
    # Phase A: Only APEX has verdict authority
    # Non-APEX stages return ARTIFACT_READY status
    next_tool = "/arifos.aaa/v1/agi_think"
    
    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="111",
        message=f"Intent classified as {lane}",
        policy_verdict="SEAL",  # Internal use only
        next_tool=next_tool,
        data={
            "intent": intent,
            "lane": lane,
            "requires_grounding": requires_grounding,
            "legacy_verdict": verdict
        },
        _debug=debug_data if debug else None
    )


def build_think_response(
    session_id: str,
    hypotheses: List[Dict],
    recommended_path: str,
    verdict: PolicyVerdict = "SEAL",
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for agi_think (stage 222)."""
    # Phase A: Only APEX has verdict authority
    next_tool = "/arifos.aaa/v1/agi_reason"
    
    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="222",
        message=f"Generated {len(hypotheses)} reasoning paths",
        policy_verdict="SEAL",  # Internal use only
        next_tool=next_tool,
        data={
            "hypothesis_count": len(hypotheses),
            "recommended_path": recommended_path,
            "legacy_verdict": verdict
        },
        _debug=debug_data if debug else None
    )


def build_reason_response(
    session_id: str,
    conclusion: str,
    truth_score: float,
    confidence: float,
    verdict: PolicyVerdict,
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for agi_reason (stage 333)."""
    # Phase A: Only APEX has verdict authority
    next_tool = "/arifos.aaa/v1/asi_empathize"
    
    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="333",
        message=conclusion[:100] + "..." if len(conclusion) > 100 else conclusion,
        policy_verdict="SEAL",  # Internal use only
        next_tool=next_tool,
        data={
            "truth_score": round(truth_score, 3),
            "confidence": round(confidence, 3),
            "legacy_verdict": verdict
        },
        _debug=debug_data if debug else None
    )


def build_empathize_response(
    session_id: str,
    empathy_kappa_r: float,
    stakeholders: List[str],
    verdict: PolicyVerdict = "SEAL",
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for asi_empathize (stage 555)."""
    # Phase A: Only APEX has verdict authority
    next_tool = "/arifos.aaa/v1/asi_align"
    
    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="555",
        message=f"Analyzed {len(stakeholders)} stakeholders",
        policy_verdict="SEAL",  # Internal use only
        next_tool=next_tool,
        data={
            "empathy_score": round(empathy_kappa_r, 3),
            "stakeholder_count": len(stakeholders),
            "legacy_verdict": verdict
        },
        _debug=debug_data if debug else None
    )


def build_align_response(
    session_id: str,
    is_reversible: bool,
    risk_level: str,
    verdict: PolicyVerdict = "SEAL",
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for asi_align (stage 666)."""
    # Phase A: Only APEX has verdict authority
    next_tool = "/arifos.aaa/v1/apex_verdict"
    
    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="666",
        message=f"Safety check: {risk_level} risk" + (", reversible" if is_reversible else ", irreversible"),
        policy_verdict="SEAL",  # Internal use only
        next_tool=next_tool,
        data={
            "is_reversible": is_reversible,
            "risk_level": risk_level,
            "legacy_verdict": verdict
        },
        _debug=debug_data if debug else None
    )


def build_verdict_response(
    session_id: str,
    query: str,
    truth_score: float,
    verdict: PolicyVerdict,
    justification: Optional[str] = None,
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for apex_verdict (stage 888)."""
    status: StatusType = "OK" if verdict == "SEAL" else "BLOCKED" if verdict == "VOID" else "PENDING"
    next_tool = "/arifos.aaa/v1/vault_seal" if verdict == "SEAL" else None
    
    message = f"Verdict: {verdict}"
    if justification and verdict != "SEAL":
        message += f" - {justification[:80]}"
    
    return UnifiedResponse(
        status=status,
        session_id=session_id,
        stage="888",
        message=message,
        policy_verdict=verdict,
        next_tool=next_tool,
        data={
            "query": query[:100] + "..." if len(query) > 100 else query,
            "truth_score": round(truth_score, 3)
        },
        _debug=debug_data if debug else None
    )


def build_seal_response(
    session_id: str,
    seal_id: Optional[str],
    seal_hash: str,
    verdict: Literal["SEALED", "PARTIAL"],
    debug_data: Optional[Dict] = None,
    debug: bool = False
) -> UnifiedResponse:
    """Build response for vault_seal (stage 999)."""
    status: StatusType = "OK" if verdict == "SEALED" else "PENDING"
    
    return UnifiedResponse(
        status=status,
        session_id=session_id,
        stage="999",
        message=f"Session sealed with ID {seal_id[:8]}..." if seal_id else "Partial seal (no persistence)",
        policy_verdict="SEAL" if verdict == "SEALED" else "PARTIAL",
        next_tool=None,  # Pipeline complete
        data={
            "seal_id": seal_id,
            "seal_hash": seal_hash[:16] + "..."
        },
        _debug=debug_data if debug else None
    )


def build_error_response(
    session_id: str,
    stage: StageType,
    error_code: str,
    detail: str,
    debug_data: Optional[Dict] = None
) -> UnifiedResponse:
    """Build standardized error response."""
    return UnifiedResponse(
        status="ERROR",
        session_id=session_id,
        stage=stage,
        message=f"Error [{error_code}]: {detail[:100]}",
        policy_verdict="VOID",
        next_tool=None,
        data={"error_code": error_code},
        _debug=debug_data
    )


# ═════════════════════════════════════════════════════════════════════════════
# INPUT VALIDATION
# ═════════════════════════════════════════════════════════════════════════════

def validate_input(params: Dict[str, Any], required: List[str]) -> Optional[UnifiedResponse]:
    """
    Validate input parameters.
    Returns error response if validation fails, None if OK.
    """
    missing = [f for f in required if f not in params or params[f] is None]
    if missing:
        return build_error_response(
            session_id=params.get("session_id", "unknown"),
            stage="000",
            error_code="MISSING_REQUIRED_FIELD",
            detail=f"Missing required fields: {', '.join(missing)}"
        )
    return None


# ═════════════════════════════════════════════════════════════════════════════
# COMPRESSION GATE — User-Facing Output
# ═════════════════════════════════════════════════════════════════════════════

def render_user_answer(
    unified_response: UnifiedResponse,
    verbosity: Literal["MIN", "STD", "FULL"] = "MIN"
) -> Dict[str, Any]:
    """
    Compression gate: Convert unified response to user-facing output.
    
    verbosity:
    - MIN: Just the answer + verdict
    - STD: Answer + key metrics
    - FULL: Everything except debug
    """
    if verbosity == "MIN":
        return {
            "answer": unified_response.message,
            "verdict": unified_response.policy_verdict,
        }
    
    elif verbosity == "STD":
        return {
            "answer": unified_response.message,
            "verdict": unified_response.policy_verdict,
            "stage": unified_response.stage,
            "next_step": unified_response.next_tool,
            "metrics": {
                k: v for k, v in unified_response.data.items()
                if isinstance(v, (int, float, bool, str))
            }
        }
    
    else:  # FULL
        return unified_response.to_dict(debug=False)


# ═════════════════════════════════════════════════════════════════════════════
# NEXT STEP TEMPLATES
# ═════════════════════════════════════════════════════════════════════════════

NEXT_STEP_TEMPLATES = {
    "/arifos.aaa/v1/init_gate": {
        "required": ["query"],
        "optional": ["session_id", "grounding_required", "mode"]
    },
    "/arifos.aaa/v1/agi_sense": {
        "required": ["query", "session_id"],
        "optional": []
    },
    "/arifos.aaa/v1/agi_think": {
        "required": ["query", "session_id"],
        "optional": []
    },
    "/arifos.aaa/v1/agi_reason": {
        "required": ["query", "session_id"],
        "optional": ["grounding"]
    },
    "/arifos.aaa/v1/asi_empathize": {
        "required": ["query", "session_id"],
        "optional": []
    },
    "/arifos.aaa/v1/asi_align": {
        "required": ["query", "session_id"],
        "optional": []
    },
    "/arifos.aaa/v1/apex_verdict": {
        "required": ["query", "session_id"],
        "optional": []
    },
    "/arifos.aaa/v1/vault_seal": {
        "required": ["session_id", "verdict", "payload"],
        "optional": ["query_summary", "risk_level", "category"]
    },
}


def get_next_step_template(tool_path: str) -> Optional[Dict[str, Any]]:
    """Get the input template for the next tool."""
    template = NEXT_STEP_TEMPLATES.get(tool_path)
    if template:
        return {
            "tool": tool_path,
            "required_args": template["required"],
            "optional_args": template["optional"]
        }
    return None
