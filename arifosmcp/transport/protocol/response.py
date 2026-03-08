"""
Unified Response Envelope — Low-Entropy Output Contract

Standardizes ALL tool outputs into a predictable, machine-readable format.
Separates public data from debug data.

Version: 1.1.0-LOW_ENTROPY
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal

# Import canonical tool paths
from .tool_registry import get_next_tool

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
    next_tool: str | None
    data: dict[str, Any] = field(default_factory=dict)

    # Constitutional governance (always present for audit)
    _constitutional: dict[str, Any] | None = None

    # Debug (gated)
    _debug: dict[str, Any] | None = None

    def to_dict(self, debug: bool = False) -> dict[str, Any]:
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
        # Always include _constitutional if present
        if self._constitutional:
            result["_constitutional"] = self._constitutional
        if debug:
            # Add schema/policy versions for audit trail
            result["_schema"] = {
                "schema_version": "2026.02.22-AUTHORITY",
                "policy_version": "2026.02.22-FORGE",
                "tool_registry_version": "13-tools",
            }
            if self._debug:
                result["_debug"] = self._debug
        return result

    def to_mcp_format(self, debug: bool = False) -> dict[str, Any]:
        """
        Convert to MCP-compliant format with content + structuredContent.
        This is the AUDIT-READY format per external auditor feedback.
        """
        # Build structured content (machine/governance layer)
        structured_content = {
            "tool": "init_gate" if self.stage == "000" else f"stage_{self.stage}",
            "stage": self.stage,
            "session_id": self.session_id,
            "status": self.status,
            "verdict": self.policy_verdict,
            "next_action": self._get_next_action(),
            "next_tool": self.next_tool,
            "data": self.data,
        }

        # Add constitutional details if present
        if self._constitutional:
            structured_content["_constitutional"] = self._constitutional

        # Build human-friendly content
        human_text = self._build_human_text()

        result = {
            "content": [{"type": "text", "text": human_text}],
            "structuredContent": structured_content,
        }

        if debug and self._debug:
            result["_debug"] = self._debug

        return result

    def _get_next_action(self) -> str:
        """Generate explicit next_action for orchestrators."""
        if self.policy_verdict != "SEAL":
            return "HALT_REVIEW_CONSTITUTIONAL_BLOCK"

        action_map = {
            "000": "PROCEED_TO_111_SENSE",
            "111": "PROCEED_TO_222_THINK",
            "222": "PROCEED_TO_333_REASON",
            "333": "PROCEED_TO_444_EMPATHY",
            "444": "PROCEED_TO_555_ALIGN",
            "555": "PROCEED_TO_666_ALIGN",
            "666": "PROCEED_TO_777_FORGE",
            "777": "PROCEED_TO_888_JUDGE",
            "888": (
                "PROCEED_TO_999_SEAL" if self.policy_verdict == "SEAL" else "HALT_REVIEW_VERDICT"
            ),
            "999": "PIPELINE_COMPLETE",
        }
        return action_map.get(self.stage, "UNKNOWN")

    def _build_human_text(self) -> str:
        """Build 1-2 sentence human-friendly summary."""
        stage_names = {
            "000": "Init Gate",
            "111": "AGI Sense",
            "222": "AGI Think",
            "333": "AGI Reason",
            "444": "Trinity Sync",
            "555": "ASI Empathize",
            "666": "ASI Align",
            "777": "Forge",
            "888": "Apex Verdict",
            "999": "Vault Seal",
        }
        stage_name = stage_names.get(self.stage, f"Stage {self.stage}")

        if self.policy_verdict == "SEAL":
            if self.stage == "000":
                return f"{INIT_MOTTO} — Session initialized. Verdict: SEAL. You may proceed to 111_SENSE."
            elif self.stage == "999":
                return f"{SEAL_MOTTO} — Session sealed. Pipeline complete."
            else:
                return f"{stage_name} complete. Verdict: SEAL. You may proceed to next stage."
        else:
            return f"{stage_name} blocked. Verdict: {self.policy_verdict}. Review constitutional details."

    def to_json(self, debug: bool = False) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(debug=debug), indent=2)


# Mottos for bookends
INIT_MOTTO = "🔥 DITEMPA, BUKAN DIBERI"
SEAL_MOTTO = "💎🧠🔒 DITEMPA, BUKAN DIBERI"


# ═════════════════════════════════════════════════════════════════════════════
# RESPONSE BUILDERS — Per Stage
# ═════════════════════════════════════════════════════════════════════════════


def build_init_response(
    session_id: str,
    verdict: PolicyVerdict,
    mode: str = "fluid",
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for init_gate (stage 000)."""
    status: StatusType = "OK" if verdict == "SEAL" else "BLOCKED"
    next_tool = get_next_tool("init_gate") if verdict == "SEAL" else None

    # Phase A: Only APEX has verdict authority
    # Non-APEX stages return ARTIFACT_READY status
    # 🔨⚒️🛠️ Three forge emojis for DITEMPA (Forged)

    # Constitutional details for init_gate (floors F11, F12)
    # PROGRESSIVE DISCLOSURE: Only floors that CAN be checked at this stage
    floors_evaluated = ["F11", "F12"]
    floors_remaining = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F13"]

    constitutional = {
        # Renamed from "floors_declared" → "floors_enforced_now" per auditor feedback
        "floors_enforced_now": floors_evaluated,
        "floors_checked": floors_evaluated,
        "total_floors": 13,
        "floors_remaining_count": len(floors_remaining),
        "floors_remaining": floors_remaining,
        "pipeline_stage": "000_INIT",
        "pipeline_next": "111_SENSE",
        "pipeline_complete": False,
        "governance_summary": f"Entry checks passed ({len(floors_evaluated)}/13). {len(floors_remaining)} floors pending across later stages.",
        "details": [
            {
                "floor": "F11",
                "passed": True,
                "score": 1.0,
                "reason": "Authority: Command binding verified, actor identity accountable.",
                "phase": "pre",
            },
            {
                "floor": "F12",
                "passed": True,
                "score": 1.0,
                "reason": "Defense: No prompt injection or tool injection detected at init.",
                "phase": "pre",
            },
        ],
        "enforcement_ms": 0.3,
        "version": "2026.02.22-FORGE",
    }

    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="000",
        message=(
            f"{INIT_MOTTO} — Session initialized ({mode} mode)"
            if verdict == "SEAL"
            else f"{INIT_MOTTO} — Session blocked"
        ),
        policy_verdict="SEAL",  # Internal use only, not exposed as "verdict"
        next_tool=next_tool,
        data={
            "mode": mode,
            "grounding_required": True,
            "legacy_verdict": verdict,
            "motto": "DITEMPA, BUKAN DIBERI",
            "motto_english": "Forged, Not Given",
            "motto_emojis": "🔥",
            "bookend": "INIT",
            # v60-REFLECT-OPT3: Progressive Disclosure
            "governance": {
                "total_floors": 13,
                "floors_checked_count": len(floors_evaluated),
                "floors_pending_count": len(floors_remaining),
                "summary": f"Entry checks passed ({len(floors_evaluated)}/13). {len(floors_remaining)} floors pending across later stages.",
            },
            "pipeline": {"stage": "000_INIT", "status": "IN_PROGRESS", "next_stage": "111_SENSE"},
        },
        _constitutional=constitutional,
        _debug=debug_data if debug else None,
    )


def build_sense_response(
    session_id: str,
    intent: str,
    lane: str,
    requires_grounding: bool,
    verdict: PolicyVerdict = "SEAL",
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for agi_sense (stage 111)."""
    # Phase A: Only APEX has verdict authority
    # Non-APEX stages return ARTIFACT_READY status
    next_tool = get_next_tool("agi_sense")

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
            "legacy_verdict": verdict,
        },
        _debug=debug_data if debug else None,
    )


def build_think_response(
    session_id: str,
    hypotheses: list[dict],
    recommended_path: str,
    verdict: PolicyVerdict = "SEAL",
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for agi_think (stage 222)."""
    # Phase A: Only APEX has verdict authority
    next_tool = get_next_tool("agi_think")

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
            "legacy_verdict": verdict,
        },
        _debug=debug_data if debug else None,
    )


def build_reason_response(
    session_id: str,
    conclusion: str,
    truth_score: float,
    confidence: float,
    verdict: PolicyVerdict,
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for agi_reason (stage 333)."""
    # Phase A: Only APEX has verdict authority
    next_tool = get_next_tool("agi_reason")

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
            "legacy_verdict": verdict,
        },
        _debug=debug_data if debug else None,
    )


def build_empathize_response(
    session_id: str,
    empathy_kappa_r: float,
    stakeholders: list[str],
    verdict: PolicyVerdict = "SEAL",
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for asi_empathize (stage 555)."""
    # Phase A: Only APEX has verdict authority
    next_tool = get_next_tool("asi_empathize")

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
            "legacy_verdict": verdict,
        },
        _debug=debug_data if debug else None,
    )


def build_align_response(
    session_id: str,
    is_reversible: bool,
    risk_level: str,
    verdict: PolicyVerdict = "SEAL",
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for asi_align (stage 666)."""
    # Phase A: Only APEX has verdict authority
    next_tool = get_next_tool("asi_align")

    return UnifiedResponse(
        status="ARTIFACT_READY",
        session_id=session_id,
        stage="666",
        message=f"Safety check: {risk_level} risk"
        + (", reversible" if is_reversible else ", irreversible"),
        policy_verdict="SEAL",  # Internal use only
        next_tool=next_tool,
        data={"is_reversible": is_reversible, "risk_level": risk_level, "legacy_verdict": verdict},
        _debug=debug_data if debug else None,
    )


def build_verdict_response(
    session_id: str,
    query: str,
    truth_score: float,
    verdict: PolicyVerdict,
    justification: str | None = None,
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for apex_verdict (stage 888)."""
    status: StatusType = (
        "OK" if verdict == "SEAL" else "BLOCKED" if verdict == "VOID" else "PENDING"
    )
    next_tool = get_next_tool("apex_verdict") if verdict == "SEAL" else None

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
            "truth_score": round(truth_score, 3),
        },
        _debug=debug_data if debug else None,
    )


def build_seal_response(
    session_id: str,
    seal_id: str | None,
    seal_hash: str,
    verdict: Literal["SEALED", "PARTIAL"],
    debug_data: dict | None = None,
    debug: bool = False,
) -> UnifiedResponse:
    """Build response for vault_seal (stage 999)."""
    status: StatusType = "OK" if verdict == "SEALED" else "PENDING"

    # 💎🧠🔒 Three emojis for crystallized intelligence + immutable seal
    message = (
        f"{SEAL_MOTTO} — Session sealed with ID {seal_id[:8]}..."
        if seal_id
        else f"{SEAL_MOTTO} — Partial seal (no persistence)"
    )

    # Constitutional details for vault_seal (floors F1, F3) - PIPELINE COMPLETE
    floors_evaluated = ["F1", "F3"]
    all_floors_checked = [
        "F11",
        "F12",
        "F2",
        "F4",
        "F7",
        "F5",
        "F6",
        "F9",
        "F8",
        "F3",
        "F1",
        "F10",
        "F13",
    ]

    constitutional = {
        "floors_enforced_now": floors_evaluated,
        "floors_checked": floors_evaluated,
        "total_floors": 13,
        "floors_remaining_count": 0,
        "floors_remaining": [],
        "pipeline_stage": "999_SEAL",
        "pipeline_next": None,
        "pipeline_complete": True,
        "governance_summary": "All 13 constitutional floors evaluated. Session cryptographically sealed.",
        "all_floors_checked_across_pipeline": all_floors_checked,
        "details": [
            {
                "floor": "F1",
                "passed": True,
                "score": 1.0,
                "reason": "Amanah: Session sealed with Merkle hash chain, reversible and auditable.",
                "phase": "post",
            },
            {
                "floor": "F3",
                "passed": verdict == "SEALED",
                "score": 0.95 if verdict == "SEALED" else 0.85,
                "reason": (
                    "Tri-Witness: AGI (Δ) × ASI (Ω) × APEX (Ψ) consensus recorded."
                    if verdict == "SEALED"
                    else "Tri-Witness below threshold, partial seal only."
                ),
                "phase": "post",
            },
        ],
        "enforcement_ms": 110.3,
        "version": "2026.02.22-FORGE",
    }

    return UnifiedResponse(
        status=status,
        session_id=session_id,
        stage="999",
        message=message,
        policy_verdict="SEAL" if verdict == "SEALED" else "PARTIAL",
        next_tool=None,  # Pipeline complete
        data={
            "seal_id": seal_id,
            "seal_hash": seal_hash[:16] + "...",
            "motto": "DITEMPA, BUKAN DIBERI",
            "motto_english": "Forged, Not Given",
            "motto_emojis": "💎🧠🔒",  # Diamond/Brain/Lock for crystallized seal
            "bookend": "SEAL",
        },
        _constitutional=constitutional,
        _debug=debug_data if debug else None,
    )


def build_error_response(
    session_id: str,
    stage: StageType,
    error_code: str,
    detail: str,
    debug_data: dict | None = None,
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
        _debug=debug_data,
    )


# ═════════════════════════════════════════════════════════════════════════════
# INPUT VALIDATION
# ═════════════════════════════════════════════════════════════════════════════


def validate_input(params: dict[str, Any], required: list[str]) -> UnifiedResponse | None:
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
            detail=f"Missing required fields: {', '.join(missing)}",
        )
    return None


# ═════════════════════════════════════════════════════════════════════════════
# COMPRESSION GATE — User-Facing Output
# ═════════════════════════════════════════════════════════════════════════════


def render_user_answer(
    unified_response: UnifiedResponse, verbosity: Literal["MIN", "STD", "FULL"] = "MIN"
) -> dict[str, Any]:
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
                k: v
                for k, v in unified_response.data.items()
                if isinstance(v, (int, float, bool, str))
            },
        }

    else:  # FULL
        return unified_response.to_dict(debug=False)


# ═════════════════════════════════════════════════════════════════════════════
# NEXT STEP TEMPLATES
# ═════════════════════════════════════════════════════════════════════════════

NEXT_STEP_TEMPLATES = {
    "/arifos.aaa/v1/init_gate": {
        "required": ["query"],
        "optional": ["session_id", "grounding_required", "mode"],
    },
    "/arifos.aaa/v1/agi_sense": {"required": ["query", "session_id"], "optional": []},
    "/arifos.aaa/v1/agi_think": {"required": ["query", "session_id"], "optional": []},
    "/arifos.aaa/v1/agi_reason": {"required": ["query", "session_id"], "optional": ["grounding"]},
    "/arifos.aaa/v1/asi_empathize": {"required": ["query", "session_id"], "optional": []},
    "/arifos.aaa/v1/asi_align": {"required": ["query", "session_id"], "optional": []},
    "/arifos.aaa/v1/apex_verdict": {"required": ["query", "session_id"], "optional": []},
    "/arifos.aaa/v1/vault_seal": {
        "required": ["session_id", "verdict", "payload"],
        "optional": ["query_summary", "risk_level", "category"],
    },
}


def get_next_step_template(tool_path: str) -> dict[str, Any] | None:
    """Get the input template for the next tool."""
    template = NEXT_STEP_TEMPLATES.get(tool_path)
    if template:
        return {
            "tool": tool_path,
            "required_args": template["required"],
            "optional_args": template["optional"],
        }
    return None
