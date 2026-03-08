"""
arifosmcp/bridge.py — The Harden Bridge

This module acts as the secure airlock between the transport layer (MCP/Hub)
and the governance layer (Core/Kernel).

It enforces:
1.  All logic resides in `core`.
2.  `arifosmcp` is transport-only.
3.  13 Canonical tool contracts are respected.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import logging
from typing import Any, Dict, Optional
from core.organs import (
    init,
    agi,
    asi,
    apex,
    vault,
    InitOutput,
    SealReceipt,
)
from core.enforcement.governance_engine import wrap_tool_output
from core.governance_kernel import get_governance_kernel

logger = logging.getLogger(__name__)

async def call_kernel(
    tool_name: str,
    session_id: str,
    payload: Dict[str, Any],
    actor_id: Optional[str] = None
) -> Dict[str, Any]:
    \"\"\"
    Route a tool call through the 7-Organ Sovereign Stack.
    
    1. INIT (000) - Gate & Defense
    2. AGI (111-333) - Logic & Truth
    3. ASI (555-666) - Empathy & Safety
    4. APEX (777-888) - Judgment & Forge
    5. VAULT (999) - Memory & Seal
    \"\"\"
    
    # Get current kernel state for telemetry
    kernel = get_governance_kernel(session_id)
    
    # ─── 000 INIT ───────────────────────────────────────────────────────────
    # All calls pass through init for session validation
    init_res = await init(
        session_id=session_id,
        actor_id=actor_id or payload.get("actor_id", "anonymous"),
        auth_context=payload.get("auth_context")
    )
    
    if init_res.verdict == "VOID":
        return wrap_tool_output(tool_name, init_res.to_dict())

    # ─── Organ Routing ──────────────────────────────────────────────────────
    try:
        if tool_name == "anchor_session":
            # Already handled by init call above, but we return its full state
            result = init_res.to_dict()
        
        elif tool_name == "reason_mind":
            result = await agi(session_id=session_id, payload=payload)
            
        elif tool_name == "simulate_heart":
            result = await asi(session_id=session_id, payload=payload)
            
        elif tool_name == "critique_thought":
            # ASI + APEX alignment
            result = await asi(session_id=session_id, payload=payload, mode="critique")
            
        elif tool_name == "eureka_forge":
            result = await apex(session_id=session_id, payload=payload, mode="forge")
            
        elif tool_name == "apex_judge":
            result = await apex(session_id=session_id, payload=payload, mode="judge")
            
        elif tool_name == "seal_vault":
            result = await vault(session_id=session_id, payload=payload)
            
        elif tool_name in ["search_reality", "ingest_evidence"]:
            # Utility tools also pass through AGI for grounding check
            result = await agi(session_id=session_id, payload=payload, mode="grounding")
            
        else:
            # Generic tool execution (Stage 222 Transition)
            result = await agi(session_id=session_id, payload=payload)

        # ─── 888 Governance Wrap ────────────────────────────────────────────
        # Every output is wrapped in the 13-law envelope
        envelope = wrap_tool_output(tool_name, result)
        
        # Attach telemetry from kernel
        envelope["psi_telemetry"] = kernel.to_dict()
        
        return envelope

    except Exception as e:
        logger.error(f"Bridge failure on {tool_name}: {e}", exc_info=True)
        return wrap_tool_output(tool_name, {
            "verdict": "VOID",
            "error": str(e),
            "stage": "BRIDGE_FAILURE"
        })
