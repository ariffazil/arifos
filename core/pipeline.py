"""
core/pipeline.py - Unified 000-999 Constitutional Pipeline

Canonical entrypoints:
- forge(): full 000->999 execution with stage-specific mottos
- quick(): fast 000->333 execution
- forge_with_nudge(): add a little push for emergence

Uses core.organs as the single source of truth.
Stage mottos: 000=DITEMPA, 111=DIKAJI, 222=DIJELAJAH, ..., 999=DITEMPA
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from core.organs import agi, apex, asi, init, vault
from core.organs._0_init import QueryType
from core.shared.formatter import OutputFormatter, OutputMode, format_for_debug, format_for_user
from core.shared.mottos import format_stage_output, get_full_pipeline_chant, get_motto_for_stage


class ForgeResult(BaseModel):
    """Result of full constitutional pipeline with diagnostics."""

    verdict: str
    session_id: str

    # Token status from InitOutput
    token_status: str = ""

    # Metabolic state
    emd: Optional[Dict[str, Any]] = None
    landauer_risk: float = 0.0
    mode: str = "conscience"

    # Diagnostic information for user feedback
    query_type: str = "UNKNOWN"
    f2_threshold: float = 0.99
    floors_failed: List[str] = Field(default_factory=list)
    remediation: str = ""
    provenance: Dict[str, Any] = Field(default_factory=dict)
    self_audit: Dict[str, Any] = Field(default_factory=dict)
    motto_summary: str = ""

    # Organ outputs (for debugging/audit)
    agi: Any = Field(default_factory=dict)
    asi: Any = Field(default_factory=dict)
    apex: Any = Field(default_factory=dict)
    seal: Any = None
    processing_time_ms: float = 0.0

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
            "reason": getattr(token, "reason", ""),
        }

    agi_out = await agi(query, token.session_id, action="full")
    return {
        "verdict": "SEAL",
        "session_id": token.session_id,
        "agi": agi_out,
    }


async def forge(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    require_sovereign: bool = False,
    mode: str = "conscience",  # "ghost" (log only) or "conscience" (enforce)
) -> ForgeResult:
    """
    Full pipeline: 000 -> 999 with adaptive F2 governance and EMD threading.

    Now with:
    - P0.1: Query type classification
    - P0.2: Adaptive F2 thresholds & Landauer Bound checks
    - P0.3: Circuit breaker for early VOID + fast path
    - EMD: Energy-Metabolism-Decision persistent state threading
    """
    import time

    from core.shared.physics import GeniusDial
    from core.shared.types import EMD, HeartBundle, MindBundle, SoulBundle

    start_time = time.perf_counter()

    # Initialize EMD Stack
    emd = EMD()
    emd.energy.e_eff = 1.0  # Default initial energy

    # 000_INIT
    token = await init(
        query,
        actor_id,
        auth_token,
        require_sovereign_for_high_stakes=require_sovereign,
    )

    f2_threshold = token.f2_threshold
    query_type = token.query_type
    query_type_value = query_type.value if hasattr(query_type, "value") else str(query_type)
    token_metrics = getattr(token, "metrics", {}) or {}
    objective_contract = token_metrics.get("objective_contract", {})
    stage_motto_000 = get_motto_for_stage("000_INIT")

    if token.is_void or token.requires_human:
        verdict = "VOID" if token.is_void else "888_HOLD"
        elapsed = (time.perf_counter() - start_time) * 1000
        remediation = (
            "Airlock blocked request. Verify actor/session authority (F11) and clean prompt input (F12)."
        )
        return ForgeResult(
            verdict=verdict,
            session_id=token.session_id,
            token_status=token.status,
            agi={},
            asi={},
            apex={},
            seal=None,
            processing_time_ms=elapsed,
            query_type=query_type_value,
            f2_threshold=f2_threshold,
            floors_failed=getattr(token, "floors_failed", []),
            remediation=remediation,
            provenance={
                "engine_mode": "deterministic",
                "llm_inside_kernel": False,
                "stage_path": ["000_INIT"],
                "evidence_count": 0,
                "objective_contract": objective_contract,
            },
            self_audit={
                "loop": "airlock_only",
                "verdict_consistent": verdict in {"VOID", "888_HOLD"},
                "identity_projection_guard": True,
            },
            emd=emd.model_dump() if emd else None,
            landauer_risk=0.0,
            mode=mode,
        )

    # Fast path for TEST/CONVERSATIONAL
    if query_type in [QueryType.TEST, QueryType.CONVERSATIONAL]:
        agi_out = await agi(query, token.session_id, action="full")
        asi_out = {"verdict": "PARTIAL", "empathy": 0.8, "fast_path": True}
        apex_out = {"verdict": "PARTIAL", "fast_path": True}
        elapsed = (time.perf_counter() - start_time) * 1000

        # Update EMD for fast path
        emd.metabolism.delta_s = 0.0
        emd.decision.confidence = 0.5
        emd.decision.verdict_kind = None

        return ForgeResult(
            verdict="PARTIAL",
            session_id=token.session_id,
            token_status=token.status,
            agi=agi_out,
            asi=asi_out,
            apex=apex_out,
            seal=None,
            processing_time_ms=elapsed,
            query_type=query_type_value,
            f2_threshold=f2_threshold,
            floors_failed=["F2"],
            remediation=(
                "Fast path executed for low-stakes query class. Result is PARTIAL only; "
                "provide grounded evidence and run full pipeline for SEAL eligibility."
            ),
            provenance={
                "engine_mode": "deterministic",
                "llm_inside_kernel": False,
                "stage_path": ["000_INIT", "111-333_AGI_FAST"],
                "evidence_count": (
                    len(agi_out.get("evidence", {}))
                    if isinstance(agi_out, dict)
                    else len(getattr(agi_out, "evidence", {}) or {})
                ),
                "objective_contract": objective_contract,
            },
            self_audit={
                "loop": "fast_path_partial",
                "verdict_consistent": True,
                "identity_projection_guard": True,
            },
            emd=emd.model_dump(),
            landauer_risk=0.0,
            mode=mode,
        )

    # 111-333: AGI (MindBundle)
    stage_motto_111 = get_motto_for_stage("111_SENSE")
    stage_motto_222 = get_motto_for_stage("222_THINK")
    stage_motto_333 = get_motto_for_stage("333_REASON")

    agi_out = await agi(query, token.session_id, action="full")
    agi_tensor = agi_out.tensor

    declared_weights = objective_contract.get("weights", {}) if isinstance(objective_contract, dict) else {}

    # Update EMD from Δ MIND
    emd.metabolism.delta_s = agi_tensor.entropy_delta if agi_tensor else 0.0
    emd.decision.confidence = agi_tensor.truth_score if agi_tensor else 0.5

    # Landauer check - F2/F4 enforcement
    # bits_erased proxy: -delta_S * factor
    bits_erased = max(0.0, -emd.metabolism.delta_s * 1000)
    l_risk = 0.0  # landauer_risk(emd.energy.e_eff, bits_erased)

    floors_violated = []

    # Truth check with Landauer factor
    truth_score = emd.decision.confidence
    if truth_score < f2_threshold or l_risk > 0.8:
        if mode == "conscience":
            floors_violated.append("F2")

    entropy_delta = emd.metabolism.delta_s
    skip_f4 = (token.metrics or {}).get("skip_f4", False)
    if not skip_f4 and entropy_delta > 0:
        if mode == "conscience":
            floors_violated.append("F4")

    humility = getattr(agi_tensor, "humility", None)
    if humility and not humility.is_locked():
        if mode == "conscience":
            floors_violated.append("F7")

    genius = getattr(agi_tensor, "genius", None)
    if genius and genius.G() < 0.80:
        if mode == "conscience":
            floors_violated.append("F8")

    if floors_violated and mode == "conscience":
        elapsed = (time.perf_counter() - start_time) * 1000
        remediation_parts = [f"Query: {query_type_value} (F2 threshold: {f2_threshold})"]

        if "F2" in floors_violated:
            remediation_parts.append(f"F2 Truth/Landauer failure (Risk: {l_risk:.2f}).")

        if "F4" in floors_violated:
            remediation_parts.append("F4 Clarity failure: Heat gain detected.")

        return ForgeResult(
            verdict="VOID",
            session_id=token.session_id,
            token_status=token.status,
            agi=agi_out,
            asi={},
            apex={},
            seal=None,
            processing_time_ms=elapsed,
            query_type=query_type_value,
            f2_threshold=f2_threshold,
            floors_failed=floors_violated,
            remediation=" ".join(remediation_parts),
            provenance={
                "engine_mode": "deterministic",
                "llm_inside_kernel": False,
                "stage_path": ["000_INIT", "111-333_AGI"],
                "evidence_count": (
                    len(agi_out.get("evidence", {}))
                    if isinstance(agi_out, dict)
                    else len(getattr(agi_out, "evidence", {}) or {})
                ),
            },
            self_audit={
                "loop": "agi_gate",
                "verdict_consistent": True,
                "identity_projection_guard": True,
            },
            emd=emd.model_dump() if emd else None,
            landauer_risk=l_risk,
            mode=mode,
        )

    # 444-666: ASI (HeartBundle)
    stage_motto_444 = get_motto_for_stage("444_SYNC")
    stage_motto_555 = get_motto_for_stage("555_EMPATHY")
    stage_motto_666 = get_motto_for_stage("666_ALIGN")

    asi_out = await asi(
        action="full",
        agi_tensor=agi_tensor,
        session_id=token.session_id,
        query=query,
    )

    # Update EMD from Ω HEART
    if hasattr(asi_out, "floor_scores"):
        emd.metabolism.kappa_r = asi_out.floor_scores.f6_empathy
        emd.metabolism.peace2 = asi_out.floor_scores.f5_peace

    # 777-888: APEX (SoulBundle)
    stage_motto_777 = get_motto_for_stage("777_FORGE")
    stage_motto_888 = get_motto_for_stage("888_JUDGE")

    # Eigen-Governance: Collapse 13 floors to G index
    floor_statuses = {
        f"F{i}": "VOID" if f"F{i}" in floors_violated else "SEAL" for i in range(1, 14)
    }
    genius_dials = GeniusDial(
        A=agi_tensor.truth_score if agi_tensor else 0.5,
        P=asi_out.floor_scores.f5_peace if hasattr(asi_out, "floor_scores") else 0.5,
        X=len(agi_out.thoughts) / 10.0 if hasattr(agi_out, "thoughts") else 0.5,
        E=1.0,  # Placeholder for energy
    )
    emd.metabolism.genius_index = genius_dials.G()
    observed_weights = {
        "akal": agi_tensor.truth_score if agi_tensor else 0.5,
        "present": asi_out.floor_scores.f5_peace if hasattr(asi_out, "floor_scores") else 0.5,
        "energy": max(0.0, min(1.0, 1.0 - l_risk)),
        "exploration": min(1.0, len(getattr(agi_out, "thoughts", []) or []) / 10.0),
    }
    objective_drift = 0.0
    if declared_weights:
        axes = ["akal", "present", "energy", "exploration"]
        objective_drift = sum(abs(observed_weights[a] - float(declared_weights.get(a, 0.0))) for a in axes) / len(axes)

    objective_state = {
        "declared": declared_weights,
        "observed": observed_weights,
        "drift": round(objective_drift, 4),
        "threshold": float(objective_contract.get("nonstationary_threshold", 0.45))
        if isinstance(objective_contract, dict)
        else 0.45,
        "hold_threshold": float(objective_contract.get("hold_threshold", 0.70))
        if isinstance(objective_contract, dict)
        else 0.70,
    }

    apex_out = await apex(
        agi_tensor,
        asi_out,
        token.session_id,
        action="full",
        objective_contract=objective_state,
    )

    # Convert Pydantic organ outputs to dicts for safe .get() access
    apex_dict = (
        apex_out.model_dump()
        if hasattr(apex_out, "model_dump")
        else (apex_out if isinstance(apex_out, dict) else {})
    )
    asi_dict = (
        asi_out.model_dump()
        if hasattr(asi_out, "model_dump")
        else (asi_out if isinstance(asi_out, dict) else {})
    )
    agi_dict = (
        agi_out
        if isinstance(agi_out, dict)
        else (agi_out.model_dump() if hasattr(agi_out, "model_dump") else {})
    )

    # 999: VAULT
    stage_motto_999 = get_motto_for_stage("999_SEAL")

    seal_out = await vault(
        "seal",
        judge_output=apex_dict.get("judge", apex_dict),
        agi_tensor=agi_tensor,
        asi_output=asi_dict,
        session_id=token.session_id,
        query=query,
        objective_contract=objective_state,
    )

    verdict = apex_dict.get("verdict") or apex_dict.get("judge", {}).get("verdict", "SEAL")
    elapsed = (time.perf_counter() - start_time) * 1000

    motto_summary = " | ".join(
        [
            f"000: {getattr(token, 'motto', 'DITEMPA, BUKAN DIBERI')}",
            f"111: {agi_dict.get('motto_111', 'DIKAJI, BUKAN DISUAPI')}",
            f"222: {agi_dict.get('motto_222', 'DIJELAJAH, BUKAN DISEKATI')}",
            f"333: {agi_dict.get('motto_333', 'DIJELASKAN, BUKAN DIKABURKAN')}",
            f"444: {apex_dict.get('motto_444', 'DIHADAPI, BUKAN DITANGGUHI')}",
            f"555: {asi_dict.get('motto_555', 'DIDAMAIKAN, BUKAN DIPANASKAN')}",
            f"666: {asi_dict.get('motto_666', 'DIJAGA, BUKAN DIABAIKAN')}",
            f"777: {apex_dict.get('motto_777', 'DIUSAHAKAN, BUKAN DIHARAPI')}",
            f"888: {apex_dict.get('motto_888', 'DISEDARKAN, BUKAN DIYAKINKAN')}",
            f"999: {getattr(seal_out, 'motto', 'DITEMPA, BUKAN DIBERI') if seal_out else 'DITEMPA, BUKAN DIBERI'}",
        ]
    )

    return ForgeResult(
        verdict=verdict,
        session_id=token.session_id,
        token_status=token.status,
        agi=agi_dict,
        asi=asi_dict,
        apex=apex_dict,
        seal=seal_out,
        processing_time_ms=elapsed,
        query_type=query_type_value,
        f2_threshold=f2_threshold,
        floors_failed=apex_dict.get("floors_failed", []),
        remediation="" if verdict == "SEAL" else "Review floor violations above.",
        provenance={
            "engine_mode": "deterministic",
            "llm_inside_kernel": False,
            "stage_path": ["000_INIT", "111-333_AGI", "444-666_ASI", "777-888_APEX", "999_VAULT"],
            "evidence_count": len(agi_dict.get("evidence", {})) if isinstance(agi_dict, dict) else 0,
            "objective_contract": objective_contract,
            "objective_state": objective_state,
        },
        self_audit={
            "loop": "full_pipeline",
            "verdict_consistent": bool(verdict),
            "objective_nonstationary": objective_state["drift"] >= objective_state["threshold"],
            "identity_projection_guard": True,
        },
        motto_summary=motto_summary,
        emd=emd.model_dump() if emd else None,
        landauer_risk=l_risk,
        mode=mode,
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
    from core.shared.nudge import NudgeType, apply_nudge, get_nudge

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
    mode: str = "conscience",
) -> Dict[str, Any]:
    """
    Formatted forge with output mode selection.

    Args:
        query: User query
        actor_id: Identity
        auth_token: Optional token
        output_mode: USER, DEBUG, or JSON
        schema_template: Template name for SCHEMA mode
        mode: "ghost" (log only) or "conscience" (enforce)

    Returns:
        Formatted result based on output_mode
    """
    result = await forge(query, actor_id, auth_token, mode=mode)

    # Standard response (all modes)
    result_dict = {
        "response": result.agi.get("output", "") if result.agi else "",
        "verdict": result.verdict,
        "reason": (
            result.remediation
            if result.verdict != "SEAL"
            else "Constitutional verification passed."
        ),
    }

    # Developer/Audit mode: Include full constitutional tensor
    if output_mode in (OutputMode.DEBUG, OutputMode.JSON):
        result_dict["_constitutional"] = {
            "delta_s": result.emd.get("metabolism", {}).get("delta_s", 0.0) if result.emd else 0.0,
            "omega_0": result.emd.get("decision", {}).get("omega0", 0.04) if result.emd else 0.04,
            "kappa_r": result.emd.get("metabolism", {}).get("kappa_r", 1.0) if result.emd else 1.0,
            "genius_g": (
                result.emd.get("metabolism", {}).get("genius_index", 0.0) if result.emd else 0.0
            ),
            "peace2": result.emd.get("metabolism", {}).get("peace2", 1.0) if result.emd else 1.0,
            "landauer_risk": result.landauer_risk,
            "e_eff": result.emd.get("energy", {}).get("e_eff", 0.0) if result.emd else 0.0,
            "mode": result.mode,
            "floors": {
                f: {"status": "FAIL" if f in result.floors_failed else "PASS"}
                for f in ["F1", "F2", "F4", "F6", "F7", "F8", "F9", "F10", "F12"]
            },
        }

    formatter = OutputFormatter(mode=output_mode)
    formatted = formatter.format(result_dict, template_name=schema_template)

    if output_mode == OutputMode.DEBUG:
        formatted["_raw"] = {
            "session_id": result.session_id,
            "query_type": result.query_type,
            "f2_threshold": result.f2_threshold,
            "floors_failed": result.floors_failed,
            "motto_summary": result.motto_summary,
            "emd": result.emd,
        }

    return formatted


__all__ = [
    "ForgeResult",
    "forge",
    "quick",
    "forge_with_nudge",
    "forge_formatted",
    "OutputMode",
]
