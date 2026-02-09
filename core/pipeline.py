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
    """Result of full constitutional pipeline."""
    verdict: str
    session_id: str
    token_status: str
    agi: dict[str, Any]
    asi: dict[str, Any]
    apex: dict[str, Any]
    seal: Any
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
    Full pipeline: 000 → 999

    Returns a ForgeResult with all stage outputs and vault receipt.
    """
    import time
    start_time = time.perf_counter()
    
    # 000: Init
    token = await init(
        query,
        actor_id,
        auth_token,
        require_sovereign_for_high_stakes=require_sovereign,
    )

    if token.is_void or token.requires_human:
        verdict = "VOID" if token.is_void else "888_HOLD"
        elapsed = (time.perf_counter() - start_time) * 1000
        return ForgeResult(
            verdict=verdict,
            session_id=token.session_id,
            token_status=token.status,
            agi={},
            asi={},
            apex={},
            seal=None,
            processing_time_ms=elapsed,
        )

    # 111-333: AGI
    agi_out = await agi(query, token.session_id, action="full")
    agi_tensor = agi_out.get("tensor")

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
    )


__all__ = ["ForgeResult", "forge", "quick", "quick_check"]

# Async version that returns just the verdict string
async def quick_check(query: str, actor_id: str = "user") -> str:
    """Quick check - returns verdict string only."""
    result = await quick(query, actor_id)
    return result.get("verdict", "VOID")
