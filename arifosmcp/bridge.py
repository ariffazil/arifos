"""
arifosmcp/bridge.py — The Harden Bridge

This module acts as the secure airlock between the transport layer (MCP/Hub)
and the governance layer (Core/Kernel).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import logging
from typing import Any

from arifosmcp.intelligence.tools.reality_grounding import open_web_page, reality_check
from core.enforcement.auth_continuity import mint_auth_context, verify_auth_context
from core.enforcement.governance_engine import wrap_tool_output
from core.organs import Verdict, agi, apex, asi, init, vault

logger = logging.getLogger(__name__)


async def call_kernel(
    tool_name: str,
    session_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    Route a tool call through the 7-Organ Sovereign Stack.
    """

    # 1. Verification of Continuity (F11)
    auth_ctx = payload.get("auth_context")
    if tool_name != "anchor_session":
        if not auth_ctx:
            return wrap_tool_output(
                tool_name,
                {
                    "verdict": "VOID",
                    "error": "F11: Missing auth_context for continuity. Run anchor_session first.",
                    "stage": "INIT",
                },
            )

        valid, reason = verify_auth_context(session_id, auth_ctx)
        if not valid:
            return wrap_tool_output(
                tool_name,
                {
                    "verdict": "VOID",
                    "error": f"F11: Authentication continuity failed: {reason}",
                    "stage": "INIT",
                },
            )

    # 1.5. Early Exit for Grounding Utilities (Not requiring full session chain)
    if tool_name == "search_reality":
        query = payload.get("query", "")
        return await reality_check(query, **payload)
    elif tool_name == "ingest_evidence":
        url = payload.get("source_url", "")
        return await open_web_page(url, **payload)

    # 2. Kernel Execution Logic
    try:
        query = payload.get("query", "")
        actor_id = payload.get("actor_id", "anonymous")
        auth_token = payload.get("auth_token")

        if tool_name == "anchor_session":
            # Stage 000: INIT
            res = await init(query=query or "INIT", actor_id=actor_id, auth_token=auth_token)
            result = res.model_dump(mode="json")

            # Mint new auth context for the next call
            if res.verdict != Verdict.VOID:
                result["auth_context"] = mint_auth_context(
                    session_id=res.session_id,
                    actor_id=res.actor_id,
                    token_fingerprint="sha256:...",
                    approval_scope=["reason_mind", "simulate_heart", "eureka_forge", "seal_vault"],
                    parent_signature="",
                )

        elif tool_name == "reason_mind":
            # Stage 111-333: AGI
            result = await agi(query=query, session_id=session_id, action="full")
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif tool_name == "simulate_heart" or tool_name == "critique_thought":
            # Stage 555-666: ASI
            # AGI is prerequisite for ASI (needs tensor)
            agi_out = await agi(query=query, session_id=session_id, action="full")
            result = await asi(
                action="full", agi_tensor=agi_out.tensor, session_id=session_id, query=query
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif tool_name == "apex_judge" or tool_name == "eureka_forge":
            # Stage 777-888: APEX
            agi_out = await agi(query=query, session_id=session_id, action="full")
            asi_out = await asi(
                action="full", agi_tensor=agi_out.tensor, session_id=session_id, query=query
            )

            mode = "forge" if tool_name == "eureka_forge" else "judge"
            result = await apex(
                action=mode,
                agi_tensor=agi_out.tensor,
                asi_output=asi_out.model_dump() if hasattr(asi_out, "model_dump") else asi_out,
                session_id=session_id,
                query=query,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif tool_name == "seal_vault":
            # Stage 999: VAULT
            # Needs previous stage outputs
            agi_out = await agi(query=query, session_id=session_id, action="full")
            asi_out = await asi(
                action="full", agi_tensor=agi_out.tensor, session_id=session_id, query=query
            )
            apex_out = await apex(
                action="judge",
                agi_tensor=agi_out.tensor,
                asi_output=asi_out,
                session_id=session_id,
                query=query,
            )

            result = await vault(
                action="seal",
                judge_output=apex_out.model_dump() if hasattr(apex_out, "model_dump") else apex_out,
                agi_tensor=agi_out.tensor,
                asi_output=asi_out.model_dump() if hasattr(asi_out, "model_dump") else asi_out,
                session_id=session_id,
                query=query,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        else:
            # Fallback for utilities using AGI sense/think
            result = await agi(query=query, session_id=session_id, action="sense")
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        # 3. Governance Envelope Wrap (13 laws)
        envelope = wrap_tool_output(tool_name, result)

        # 4. Continuity Rotation (Chain the Token)
        if envelope.get("verdict") != "VOID" and tool_name != "anchor_session":
            if auth_ctx:
                envelope["auth_context"] = mint_auth_context(
                    session_id=session_id,
                    actor_id=auth_ctx.get("actor_id", "anonymous"),
                    token_fingerprint=auth_ctx.get("token_fingerprint", ""),
                    approval_scope=auth_ctx.get("approval_scope", []),
                    parent_signature=auth_ctx.get("signature", ""),
                )

        return envelope

    except Exception as e:
        logger.error(f"Bridge failure on {tool_name}: {e}", exc_info=True)
        return wrap_tool_output(
            tool_name, {"verdict": "VOID", "error": str(e), "stage": "BRIDGE_FAILURE"}
        )
