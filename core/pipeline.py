"""
core/pipeline.py — Unified 000-999 Constitutional Pipeline

Canonical entrypoints:
- forge(): full 000→999 execution
- quick(): fast 000→333 execution

Uses core.organs as the single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from core.organs import init, agi, asi, apex, vault


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
    - Query type classification (PROCEDURAL, OPINION, COMPARATIVE, FACTUAL)
    - Adaptive F2 thresholds (0.60 - 0.99 based on query type)
    - Fast path for low-risk procedural/opinion queries
    - Better error messages with remediation steps
    
    Returns a ForgeResult with all stage outputs and diagnostics.
    """
    import time
    start_time = time.perf_counter()
    
    # 000: Init (includes P0.1 query classification)
    token = await init(
        query,
        actor_id,
        auth_token,
        require_sovereign_for_high_stakes=require_sovereign,
    )
    
    # P0.2: Use adaptive F2 threshold from SessionToken
    f2_threshold = token.f2_threshold
    query_type = token.query_type

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

    # 111-333: AGI (with adaptive F2 from SessionToken)
    agi_out = await agi(query, token.session_id, action="full")
    agi_tensor = agi_out.get("tensor")
    
    # Check if AGI passed adaptive F2
    truth_score = getattr(agi_tensor, 'truth_score', 0.5)
    if truth_score < f2_threshold:
        # F2 failure with remediation
        elapsed = (time.perf_counter() - start_time) * 1000
        remediation = (
            f"Query classified as {query_type.value} (F2 threshold: {f2_threshold}). "
        )
        if query_type.value == "FACTUAL":
            remediation += "Add specific facts or citations to increase truth score."
        elif query_type.value in ["PROCEDURAL", "TEST"]:
            remediation += "This command was blocked unexpectedly—try rephrasing or use mode='fast'."
        else:
            remediation += "Rephrase with more specific language."
        
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
            floors_failed=["F2"],
            remediation=remediation,
        )

    # 555-666: ASI
    asi_out = await asi(query, agi_tensor, token.session_id, action="full")

    # 444-888: APEX
    apex_out = await apex(agi_tensor, asi_out, token.session_id, action="full")

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
    )


__all__ = ["ForgeResult", "forge", "quick", "quick_check"]

# Async version that returns just the verdict string
async def quick_check(query: str, actor_id: str = "user") -> str:
    """Quick check - returns verdict string only."""
    result = await quick(query, actor_id)
    return result.get("verdict", "VOID")
