"""
core/pipeline.py — Unified 000-999 Constitutional Pipeline

Canonical entrypoints:
- forge(): full 000→999 execution with stage-specific mottos
- quick(): fast 000→333 execution

Uses core.organs as the single source of truth.
Stage mottos: 000=DITEMPA, 111=DIKAJI, 222=DIJELAJAH, ..., 999=DITEMPA
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

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
    
    # NEW: Diagnostic information for user feedback
    query_type: str = "UNKNOWN"  # PROCEDURAL, OPINION, COMPARATIVE, FACTUAL
    f2_threshold: float = 0.99
    floors_failed: list = None
    remediation: str = ""  # Actionable fix suggestion
    motto_summary: str = ""  # 9 mottos from all stages
    
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
            return "✅ Constitutional verification passed."
        
        elif self.verdict == "PARTIAL":
            return f"⚠️ Limited approval with constraints. {self.remediation}"
        
        elif self.verdict == "VOID":
            msg = "❌ Blocked by constitutional floors."
            if self.floors_failed:
                msg += f" Failed: {', '.join(self.floors_failed)}."
            if self.remediation:
                msg += f" {self.remediation}"
            return msg
        
        elif self.verdict == "888_HOLD":
            return "🛑 Requires human sovereign review."
        
        return "Unknown verdict."


async def quick(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
) -> dict[str, Any]:
    """
    Fast path: 000 → 333

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
    Full pipeline: 000 → 999 with adaptive F2 governance.
    
    Now with:
    - P0.1: Query type classification (TEST, CONVERSATIONAL, PROCEDURAL, OPINION, FACTUAL)
    - P0.2: Adaptive F2 thresholds (0.50 - 0.99 based on query type)
    - P0.3: Circuit breaker for early VOID + fast path for TEST/CONVERSATIONAL
    - Better error messages with remediation steps
    
    Returns a ForgeResult with all stage outputs and diagnostics.
    """
    import time
    start_time = time.perf_counter()
    
    # 000_INIT: Ignite with DITEMPA, BUKAN DIBERI
    token = await init(
        query,
        actor_id,
        auth_token,
        require_sovereign_for_high_stakes=require_sovereign,
    )
    
    # P0.2: Use adaptive F2 threshold from SessionToken
    f2_threshold = token.f2_threshold
    query_type = token.query_type
    
    # Stage motto for logging/debugging
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

    # P0.3: Fast path for TEST/CONVERSATIONAL queries (skip heavy stages)
    if query_type in [QueryType.TEST, QueryType.CONVERSATIONAL]:
        # Minimal pipeline: init → agi (fast path) → direct SEAL
        # AGI will detect fast path via GPV.can_use_fast_path()
        agi_out = await agi(query, token.session_id, action="full")
        
        # Skip ASI and APEX for low-stakes queries - go straight to SEAL
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
            seal=None,  # Skip vault for fast path
            processing_time_ms=elapsed,
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            floors_failed=[],
            remediation="Fast path: TEST/CONVERSATIONAL query processed with minimal stages.",
        )

    # 111-333: AGI with stage mottos
    # 111_SENSE: DIKAJI, BUKAN DISUAPI (Examined, not assumed)
    # 222_THINK: DIJELAJAH, BUKAN DISEKATI (Explored, not restricted)
    # 333_REASON: DIJELASKAN, BUKAN DIKABURKAN (Clarified, not obscured)
    stage_motto_111 = get_motto_for_stage("111_SENSE")
    stage_motto_222 = get_motto_for_stage("222_THINK")
    stage_motto_333 = get_motto_for_stage("333_REASON")
    
    agi_out = await agi(query, token.session_id, action="full")
    agi_tensor = agi_out.get("tensor")
    
    # P0.3: Circuit breaker - check AGI floors before continuing
    floors_violated = []
    
    # Check F2 (Truth)
    truth_score = getattr(agi_tensor, 'truth_score', 0.5)
    if truth_score < f2_threshold:
        floors_violated.append("F2")
    
    # Check F4 (Entropy) - skip if query type allows
    entropy_delta = getattr(agi_tensor, 'entropy_delta', 0.0)
    if not token.skip_f4 and entropy_delta > 0:
        floors_violated.append("F4")
    
    # Check F7 (Humility)
    humility = getattr(agi_tensor, 'humility', None)
    if humility and not humility.is_locked():
        floors_violated.append("F7")
    
    # Check F8 (Genius)
    genius = getattr(agi_tensor, 'genius', None)
    if genius and genius.G() < 0.80:
        floors_violated.append("F8")
    
    # Circuit breaker: if any floors violated, stop here
    if floors_violated:
        elapsed = (time.perf_counter() - start_time) * 1000
        
        # Build remediation message
        remediation_parts = [f"Query: {query_type.value} (F2 threshold: {f2_threshold})"]
        
        if "F2" in floors_violated:
            if query_type.value == "FACTUAL":
                remediation_parts.append("Add specific facts or citations.")
            elif query_type.value in ["PROCEDURAL", "TEST"]:
                remediation_parts.append("Try rephrasing or use mode='fast'.")
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

    # 444_SYNC: DIHADAPI, BUKAN DITANGGUHI (Faced, not postponed)
    # 555_EMPATHY: DIDAMAIKAN, BUKAN DIPANASKAN (Calmed, not inflamed)
    # 666_ALIGN: DIJAGA, BUKAN DIABAIKAN (Guarded, not neglected)
    stage_motto_444 = get_motto_for_stage("444_SYNC")
    stage_motto_555 = get_motto_for_stage("555_EMPATHY")
    stage_motto_666 = get_motto_for_stage("666_ALIGN")
    
    # 555-666: ASI (only if AGI passed all floors)
    asi_out = await asi(query, agi_tensor, token.session_id, action="full")

    # 777_FORGE: DIUSAHAKAN, BUKAN DIHARAPI (Worked, not hoped)
    # 888_JUDGE: DISEDARKAN, BUKAN DIYAKINKAN (Aware, not over-assured)
    stage_motto_777 = get_motto_for_stage("777_FORGE")
    stage_motto_888 = get_motto_for_stage("888_JUDGE")
    
    # 444-888: APEX
    apex_out = await apex(agi_tensor, asi_out, token.session_id, action="full")

    # 999_SEAL: DITEMPA, BUKAN DIBERI (same as 000 - immutable foundation)
    stage_motto_999 = get_motto_for_stage("999_SEAL")
    
    # 999: VAULT
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

    # Compile motto output from all stages
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


__all__ = ["ForgeResult", "forge", "quick", "quick_check"]

# Async version that returns just the verdict string
async def quick_check(query: str, actor_id: str = "user") -> str:
    """Quick check - returns verdict string only."""
    result = await quick(query, actor_id)
    return result.get("verdict", "VOID")
