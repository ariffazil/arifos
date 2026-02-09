"""
core/pipeline.py - Unified 000-999 Constitutional Pipeline

Canonical entrypoints:
- forge(): full 000->999 execution with stage-specific mottos
- quick(): fast 000->333 execution
- forge_with_nudge(): add a little push for emergence

Uses core.organs as the single source of truth.
Stage mottos: 000=DITEMPA, 111=DIKAJI, 222=DIJELAJAH, ..., 999=DITEMPA
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Dict

from core.organs import init, agi, asi, apex, vault
from core.organs._0_init import QueryType
from core.shared.mottos import (
    get_motto_for_stage,
    format_stage_output,
    get_full_pipeline_chant,
)
from core.shared.formatter import (
    OutputMode,
    OutputFormatter,
    format_for_user,
    format_for_debug,
)


@dataclass
class ForgeResult:
    """Result of full constitutional pipeline with diagnostics."""
    verdict: str
    session_id: str
    token_status: str
    agi: dict[str, Any]
    asi: dict[str, Any]
    apex: dict[str, Any]
    seal: Any
    processing_time_ms: float = 0.0
    
    # Diagnostic information for user feedback
    query_type: str = "UNKNOWN"
    f2_threshold: float = 0.99
    floors_failed: list = None
    remediation: str = ""
    motto_summary: str = ""
    
    def __post_init__(self):
        if self.floors_failed is None:
            self.floors_failed = []
    
    def is_success(self) -> bool:
        """Check if result was successful (SEAL or PARTIAL)."""
        return self.verdict in ("SEAL", "PARTIAL")
    
    def is_blocked(self) -> bool:
        """Check if result was blocked (VOID)."""
        return self.verdict == "VOID"
    
    def needs_human(self) -> bool:
        """Check if result needs human review (888_HOLD)."""
        return self.verdict == "888_HOLD"
    
    def to_user_message(self) -> str:
        """Generate user-friendly result message with remediation."""
        if self.verdict == "SEAL":
            return "Constitutional verification passed."
        
        elif self.verdict == "PARTIAL":
            return f"Limited approval with constraints. {self.remediation}"
        
        elif self.verdict == "VOID":
            msg = "Blocked by constitutional floors."
            if self.floors_failed:
                msg += f" Failed: {', '.join(self.floors_failed)}."
            if self.remediation:
                msg += f" {self.remediation}"
            return msg
        
        elif self.verdict == "888_HOLD":
            return "Requires human sovereign review."
        
        return "Unknown verdict."


async def quick(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
) -> dict[str, Any]:
    """
    Fast path: 000 -> 333

    Returns AGI output if init passes; otherwise returns VOID/HOLD token info.
    """
    token = await init(query, actor_id, auth_token)
    if token.is_void or token.requires_human:
        return {
            "verdict": "VOID" if token.is_void else "888_HOLD",
            "session_id": token.session_id,
            "token_status": token.status,
            "reason": token.reason,
        }

    agi_out = await agi(query, token.session_id, action="full")
    return {
        "verdict": "SEAL",
        "session_id": token.session_id,
        "token_status": token.status,
        "agi": agi_out,
    }


async def forge(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    require_sovereign: bool = False,
) -> ForgeResult:
    """
    Full pipeline: 000 -> 999 with adaptive F2 governance.
    
    Now with:
    - P0.1: Query type classification
    - P0.2: Adaptive F2 thresholds
    - P0.3: Circuit breaker for early VOID + fast path
    - Better error messages with remediation steps
    """
    import time
    start_time = time.perf_counter()
    
    # 000_INIT
    token = await init(
        query,
        actor_id,
        auth_token,
        require_sovereign_for_high_stakes=require_sovereign,
    )
    
    f2_threshold = token.f2_threshold
    query_type = token.query_type
    stage_motto_000 = get_motto_for_stage("000_INIT")

    if token.is_void or token.requires_human:
        verdict = "VOID" if token.is_void else "888_HOLD"
        elapsed = (time.perf_counter() - start_time) * 1000
        remediation = "Check authentication (F11) or injection patterns (F12)."
        return ForgeResult(
            verdict=verdict,
            session_id=token.session_id,
            token_status=token.status,
            agi={},
            asi={},
            apex={},
            seal=None,
            processing_time_ms=elapsed,
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            floors_failed=token.floors_failed if hasattr(token, 'floors_failed') else [],
            remediation=remediation,
        )

    # Fast path for TEST/CONVERSATIONAL
    if query_type in [QueryType.TEST, QueryType.CONVERSATIONAL]:
        agi_out = await agi(query, token.session_id, action="full")
        asi_out = {"verdict": "SEAL", "empathy": 0.8, "fast_path": True}
        apex_out = {"verdict": "SEAL", "fast_path": True}
        elapsed = (time.perf_counter() - start_time) * 1000
        
        return ForgeResult(
            verdict="SEAL",
            session_id=token.session_id,
            token_status=token.status,
            agi=agi_out,
            asi=asi_out,
            apex=apex_out,
            seal=None,
            processing_time_ms=elapsed,
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            floors_failed=[],
            remediation="Fast path: TEST/CONVERSATIONAL query processed with minimal stages.",
        )

    # 111-333: AGI
    stage_motto_111 = get_motto_for_stage("111_SENSE")
    stage_motto_222 = get_motto_for_stage("222_THINK")
    stage_motto_333 = get_motto_for_stage("333_REASON")
    
    agi_out = await agi(query, token.session_id, action="full")
    agi_tensor = agi_out.get("tensor")
    
    # Circuit breaker
    floors_violated = []
    
    truth_score = getattr(agi_tensor, 'truth_score', 0.5)
    if truth_score < f2_threshold:
        floors_violated.append("F2")
    
    entropy_delta = getattr(agi_tensor, 'entropy_delta', 0.0)
    if not token.skip_f4 and entropy_delta > 0:
        floors_violated.append("F4")
    
    humility = getattr(agi_tensor, 'humility', None)
    if humility and not humility.is_locked():
        floors_violated.append("F7")
    
    genius = getattr(agi_tensor, 'genius', None)
    if genius and genius.G() < 0.80:
        floors_violated.append("F8")
    
    if floors_violated:
        elapsed = (time.perf_counter() - start_time) * 1000
        remediation_parts = [f"Query: {query_type.value} (F2 threshold: {f2_threshold})"]
        
        if "F2" in floors_violated:
            if query_type.value == "FACTUAL":
                remediation_parts.append("Add specific facts or citations.")
            else:
                remediation_parts.append("Rephrase with more specific language.")
        
        if "F4" in floors_violated:
            remediation_parts.append("F4 Clarity: Query increases uncertainty. Be more specific.")
        
        if "F7" in floors_violated:
            remediation_parts.append("F7 Humility: Add uncertainty ('I think', 'perhaps').")
        
        if "F8" in floors_violated:
            remediation_parts.append("F8 Genius: Simplify or add more context.")
        
        return ForgeResult(
            verdict="VOID",
            session_id=token.session_id,
            token_status=token.status,
            agi=agi_out,
            asi={},
            apex={},
            seal=None,
            processing_time_ms=elapsed,
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            floors_failed=floors_violated,
            remediation=" ".join(remediation_parts),
        )

    # 444-666: ASI
    stage_motto_444 = get_motto_for_stage("444_SYNC")
    stage_motto_555 = get_motto_for_stage("555_EMPATHY")
    stage_motto_666 = get_motto_for_stage("666_ALIGN")
    
    asi_out = await asi(query, agi_tensor, token.session_id, action="full")

    # 777-888: APEX
    stage_motto_777 = get_motto_for_stage("777_FORGE")
    stage_motto_888 = get_motto_for_stage("888_JUDGE")
    
    apex_out = await apex(agi_tensor, asi_out, token.session_id, action="full")

    # 999: VAULT
    stage_motto_999 = get_motto_for_stage("999_SEAL")
    
    seal_out = await vault(
        "seal",
        judge_output=apex_out.get("judge", apex_out),
        agi_tensor=agi_tensor,
        asi_output=asi_out,
        session_id=token.session_id,
        query=query,
    )

    verdict = apex_out.get("verdict") or apex_out.get("judge", {}).get("verdict", "SEAL")
    elapsed = (time.perf_counter() - start_time) * 1000

    motto_summary = " | ".join([
        f"000: {token.motto}",
        f"111: {agi_out.get('motto_111', 'DIKAJI, BUKAN DISUAPI')}",
        f"222: {agi_out.get('motto_222', 'DIJELAJAH, BUKAN DISEKATI')}",
        f"333: {agi_out.get('motto_333', 'DIJELASKAN, BUKAN DIKABURKAN')}",
        f"444: {apex_out.get('motto_444', 'DIHADAPI, BUKAN DITANGGUHI')}",
        f"555: {asi_out.get('motto_555', 'DIDAMAIKAN, BUKAN DIPANASKAN')}",
        f"666: {asi_out.get('motto_666', 'DIJAGA, BUKAN DIABAIKAN')}",
        f"777: {apex_out.get('motto_777', 'DIUSAHAKAN, BUKAN DIHARAPI')}",
        f"888: {apex_out.get('motto_888', 'DISEDARKAN, BUKAN DIYAKINKAN')}",
        f"999: {seal_out.motto if seal_out else 'DITEMPA, BUKAN DIBERI'}",
    ])
    
    return ForgeResult(
        verdict=verdict,
        session_id=token.session_id,
        token_status=token.status,
        agi=agi_out,
        asi=asi_out,
        apex=apex_out,
        seal=seal_out,
        processing_time_ms=elapsed,
        query_type=query_type.value,
        f2_threshold=f2_threshold,
        floors_failed=apex_out.get("floors_failed", []),
        remediation="" if verdict == "SEAL" else "Review floor violations above.",
        motto_summary=motto_summary,
    )


# =============================================================================
# EUREKA NUDGE - Just a little push for emergence
# =============================================================================

async def forge_with_nudge(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    nudge_type: Optional[str] = None,
    output_mode: OutputMode = OutputMode.USER,
) -> Dict[str, Any]:
    """
    Forge with a nudge - just a little push for cognitive emergence.
    
    Args:
        query: User query
        actor_id: Identity
        auth_token: Optional token
        nudge_type: 'reframe', 'invert', 'zoom_out', 'zoom_in', 
                    'connect', 'simplify', 'extreme', 'first', or None for random
        output_mode: USER, DEBUG, or JSON
        
    Returns:
        Formatted result with nudge used
    """
    from core.shared.nudge import get_nudge, apply_nudge, NudgeType
    
    # Get nudge (random if not specified)
    if nudge_type:
        nudge = get_nudge(NudgeType(nudge_type))
    else:
        nudge = get_nudge()
    
    # Apply nudge to query
    nudged_query = apply_nudge(query, nudge)
    
    # Run pipeline with nudged query
    result = await forge(nudged_query, actor_id, auth_token)
    
    # Format result
    result_dict = {
        "verdict": result.verdict,
        "session_id": result.session_id,
        "agi": result.agi,
        "asi": result.asi,
        "apex": result.apex,
        "seal": result.seal,
        "query_type": result.query_type,
        "motto_summary": result.motto_summary,
        "nudge": {
            "type": nudge.type.value,
            "description": nudge.description,
        },
    }
    
    # Format based on mode
    formatter = OutputFormatter(mode=output_mode)
    formatted = formatter.format(result_dict, template_name=None)
    
    if output_mode == OutputMode.DEBUG:
        formatted["_raw"] = result_dict
        formatted["_nudged_query"] = nudged_query
    
    return formatted


# =============================================================================
# FORMATTED FORGE - With user/debug/schema modes
# =============================================================================

async def forge_formatted(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    output_mode: OutputMode = OutputMode.USER,
    schema_template: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Formatted forge with output mode selection.
    
    Args:
        query: User query
        actor_id: Identity
        auth_token: Optional token
        output_mode: USER, DEBUG, or JSON
        schema_template: Template name for SCHEMA mode
        
    Returns:
        Formatted result based on output_mode
    """
    result = await forge(query, actor_id, auth_token)
    
    result_dict = {
        "verdict": result.verdict,
        "session_id": result.session_id,
        "agi": result.agi,
        "asi": result.asi,
        "apex": result.apex,
        "seal": result.seal,
        "query_type": result.query_type,
        "f2_threshold": result.f2_threshold,
        "floors_failed": result.floors_failed,
        "remediation": result.remediation,
        "motto_summary": result.motto_summary,
    }
    
    formatter = OutputFormatter(mode=output_mode)
    formatted = formatter.format(result_dict, template_name=schema_template)
    
    if output_mode == OutputMode.DEBUG:
        formatted["_raw"] = result_dict
    
    return formatted


__all__ = [
    "ForgeResult",
    "forge",
    "quick",
    "forge_with_nudge",
    "forge_formatted",
    "OutputMode",
]
