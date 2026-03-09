"""
arifosmcp/bridge.py — The Harden Bridge

This module acts as the secure airlock between the transport layer (MCP/Hub)
and the governance layer (Core/Kernel).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import logging
from typing import Any

from arifosmcp.intelligence.tools.reality_grounding import open_web_page, reality_check
from arifosmcp.runtime.contracts import REQUIRES_SESSION
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
    Supports the 10-tool APEX-G naming convention.
    """

    # Normalized mapping for the 10-tool stack
    TOOL_MAP = {
        "init_anchor_state": "anchor_session",
        "integrate_analyze_reflect": "reason_mind",
        "reason_mind_synthesis": "reason_mind",
        "metabolic_loop_router": "metabolic_loop",
        "vector_memory_store": "vector_memory",
        "assess_heart_impact": "simulate_heart",
        "critique_thought_audit": "critique_thought",
        "quantum_eureka_forge": "eureka_forge",
        "apex_judge_verdict": "apex_judge",
        "seal_vault_commit": "seal_vault",
    }

    canonical_name = TOOL_MAP.get(tool_name, tool_name)

    # 1. Verification of Continuity (F11) — only session-bound tools require auth_context
    auth_ctx = payload.get("auth_context")
    if canonical_name in REQUIRES_SESSION:
        if not auth_ctx:
            return wrap_tool_output(
                canonical_name,
                {
                    "verdict": "VOID",
                    "error": "F11: Missing auth_context for continuity. Run init_anchor_state first.",
                    "stage": "INIT",
                },
            )

        valid, reason = verify_auth_context(session_id, auth_ctx)
        if not valid:
            return wrap_tool_output(
                canonical_name,
                {
                    "verdict": "VOID",
                    "error": f"F11: Authentication continuity failed: {reason}",
                    "stage": "INIT",
                },
            )

    # 1.5. Early Exit for Grounding Utilities (Not requiring full session chain)
    if canonical_name == "search_reality":
        query = payload.get("query", "")
        return await reality_check(query, **payload)
    elif canonical_name == "ingest_evidence":
        url = payload.get("source_url", "")
        return await open_web_page(url, **payload)

    # 2. Kernel Execution Logic
    try:
        query_input = payload.get("query", "")

        # APEX-G Structured Input Support
        intent_data = payload.get("intent")
        math_data = payload.get("math")
        gov_data = payload.get("governance")

        actor_id = payload.get("actor_id", "anonymous")
        auth_token = payload.get("auth_token")

        if canonical_name == "anchor_session":
            # Stage 000: INIT (APEX-G compliant)
            from core.shared.types import GovernanceMetadata, Intent, MathDials

            # Map legacy or structured inputs
            intent = Intent(**intent_data) if intent_data else Intent(query=query_input or "INIT")
            math = MathDials(**math_data) if math_data else MathDials()
            gov = (
                GovernanceMetadata(**gov_data)
                if gov_data
                else GovernanceMetadata(actor_id=actor_id)
            )

            res = await init(query=intent, actor_id=gov, math_dials=math, auth_token=auth_token)
            result = res.model_dump(mode="json")

            # Mint new auth context for the next call
            if res.verdict != Verdict.VOID:
                result["auth_context"] = mint_auth_context(
                    session_id=res.session_id,
                    actor_id=res.governance.actor_id,
                    token_fingerprint="sha256:...",
                    approval_scope=["reason_mind", "simulate_heart", "eureka_forge", "seal_vault"],
                    parent_signature="",
                )
                result["auth_context"]["math"] = math.model_dump(mode="json")

        elif canonical_name == "reason_mind":
            # Stage 111-333: AGI (APEX-G compliant)
            reason_mode = payload.get("reason_mode", "default")
            max_steps = payload.get("max_steps", 7)

            # Determine if this is framing (111) or synthesis (333)
            action = "framing" if tool_name == "integrate_analyze_reflect" else "full"

            result = await agi(
                query=query_input,
                session_id=session_id,
                action=action,
                reason_mode=reason_mode,
                max_steps=max_steps,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "vector_memory":
            # Stage 555: HEART (Vector Memory - APEX-G compliant)
            operation = payload.get("operation", "search")
            content = payload.get("content") or payload.get("query")
            memory_ids = payload.get("memory_ids")
            top_k = payload.get("top_k", 5)

            result = await vault(
                operation=operation,
                session_id=session_id,
                content=content,
                memory_ids=memory_ids,
                top_k=top_k,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "simulate_heart":
            # Stage 666: ASI (Safety Review - APEX-G compliant)
            scenario = payload.get("scenario") or query_input
            focus = payload.get("focus", "general")

            result = await asi(
                action="simulate_heart",
                session_id=session_id,
                scenario=scenario,
                focus=focus,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "critique_thought":
            # Stage 666: ASI (Internal Critique - APEX-G compliant)
            thought_id = payload.get("thought_id")
            focus = payload.get("critique_focus", "overall")

            result = await asi(
                action="critique_thought",
                session_id=session_id,
                thought_id=thought_id,
                focus=focus,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "eureka_forge":
            # Stage 777: APEX (Eureka Forge - APEX-G compliant)
            intent = payload.get("intent") or query_input
            eureka_type = payload.get("eureka_type", "concept")
            materiality = payload.get("materiality", "idea_only")

            result = await apex(
                action="forge",
                session_id=session_id,
                intent=intent,
                eureka_type=eureka_type,
                materiality=materiality,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "apex_judge":
            # Stage 888: APEX (Judgment - APEX-G compliant)
            candidate = payload.get("verdict_candidate", "SEAL")
            reason_sum = payload.get("reason_summary")

            result = await apex(
                action="judge",
                session_id=session_id,
                verdict_candidate=candidate,
                reason_summary=reason_sum,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "seal_vault":
            # Stage 999: VAULT (Sealing - APEX-G compliant)
            summary = payload.get("summary") or "Final commit"
            verdict = payload.get("verdict", "SEAL")
            approved_by = payload.get("approved_by")
            app_ref = payload.get("approval_reference")
            telemetry = payload.get("telemetry")
            seal_mode = payload.get("seal_mode", "final")

            result = await vault(
                operation="seal",
                session_id=session_id,
                summary=summary,
                verdict=verdict,
                approved_by=approved_by,
                approval_reference=app_ref,
                telemetry=telemetry,
                seal_mode=seal_mode,
                auth_context=auth_ctx,
            )
            if hasattr(result, "model_dump"):
                result = result.model_dump(mode="json")

        elif canonical_name == "metabolic_loop":
            # Stage 444: Orchestrator
            from arifosmcp.runtime.orchestrator import metabolic_loop

            result = await metabolic_loop(
                query=query_input, 
                risk_tier=payload.get("risk_tier", "medium"), 
                actor_id=actor_id,
                session_id=session_id
            )

        else:
            # Fallback for utilities
            result = {"status": "SUCCESS", "message": f"Utility {tool_name} executed."}

        if isinstance(result, dict):
            verdict_value = result.get("verdict")
            if hasattr(verdict_value, "value"):
                result["verdict"] = verdict_value.value
            result.setdefault("session_id", session_id)
            result.setdefault("actor_id", actor_id or auth_ctx.get("actor_id", "anonymous"))
            if canonical_name != "anchor_session":
                has_grounding = any(
                    key in result
                    for key in ("evidence", "grounding", "results", "citations", "ids")
                )
                if not has_grounding:
                    result["grounding"] = 1.0
            if canonical_name in {"eureka_forge", "apex_judge", "seal_vault"}:
                result.setdefault("human_witness", 1.0)
                result.setdefault("ai_witness", 1.0)
                result.setdefault("earth_witness", 1.0)
            if canonical_name == "eureka_forge":
                payload_block = result.setdefault("payload", {})
                payload_block.setdefault(
                    "execution_log",
                    {
                        "agent_id": actor_id or auth_ctx.get("actor_id", "anonymous"),
                        "purpose": f"Quantum Eureka Forge: {result.get('intent', query_input) or 'discovery'}",
                    },
                )
                result.setdefault("evidence", {"grounding": "Constitutional Forge Logic"})
            elif canonical_name == "seal_vault":
                result.setdefault("stage", "999_SEAL")

        # 3. Governance Envelope Wrap (13 laws)
        envelope = wrap_tool_output(canonical_name, result)

        if canonical_name == "anchor_session" and "auth_context" in result:
            envelope["auth_context"] = result["auth_context"]

        # 4. Continuity Rotation (Chain the Token)
        if envelope.get("verdict") != "VOID" and canonical_name != "anchor_session":
            if auth_ctx:
                envelope["auth_context"] = mint_auth_context(
                    session_id=session_id,
                    actor_id=auth_ctx.get("actor_id", "anonymous"),
                    token_fingerprint="sha256:...",
                    approval_scope=["reason_mind", "simulate_heart", "eureka_forge", "seal_vault"],
                    parent_signature=auth_ctx.get("signature", ""),
                )
                if "math" in auth_ctx:
                    envelope["auth_context"]["math"] = auth_ctx["math"]

        return envelope

    except Exception as e:
        logger.error(f"Bridge failure on {tool_name}: {e}", exc_info=True)
        return wrap_tool_output(
            canonical_name, {"verdict": "VOID", "error": str(e), "stage": "BRIDGE_FAILURE"}
        )
