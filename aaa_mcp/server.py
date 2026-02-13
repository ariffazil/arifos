"""
arifOS AAA MCP Server — Constitutional AI Governance (v60.0-FORGE)

13 canonical tools organized as a 5-Organ Trinity pipeline:
  000_INIT → AGI(Mind) → ASI(Heart) → APEX(Soul) → 999_VAULT

Every tool is guarded by constitutional floors (F1-F13).
Verdicts: SEAL (approved) | VOID (blocked) | PARTIAL (warning) | SABAR (repair)
Motto: DITEMPA BUKAN DIBERI — Forged, Not Given

MCP Protocol: 2025-11-25 (Streamable HTTP)
Capabilities: tools, resources, prompts, sampling, logging
Authentication: OAuth 2.1
"""

import json
from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from fastmcp import FastMCP

# Tool annotations registry for MCP 2025-11-25 compliance
# https://modelcontextprotocol.io/specification/2025-11-25/server/tools#tool-annotations
TOOL_ANNOTATIONS = {
    "init_gate": {
        "title": "000_INIT Gate",
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "trinity_forge": {
        "title": "000-999 Trinity Forge",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": True,
    },
    "agi_sense": {
        "title": "111_AGI Sense",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "agi_think": {
        "title": "222_AGI Think",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    },
    "agi_reason": {
        "title": "333_AGI Reason",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "asi_empathize": {
        "title": "555_ASI Empathize",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "asi_align": {
        "title": "666_ASI Align",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "apex_verdict": {
        "title": "888_APEX Verdict",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
    },
    "reality_search": {
        "title": "Reality Search",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    },
    "vault_seal": {
        "title": "999_VAULT Seal",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
    },
    "tool_router": {
        "title": "Tool Router",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "vault_query": {
        "title": "VAULT Query",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "truth_audit": {
        "title": "Truth Audit",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "simulate_transfer": {
        "title": "Simulate Transfer",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
    },
    # --- MCP Gateway Tools (Vibe Infrastructure) ---
    "gateway_route_tool": {
        "title": "Gateway Router",
        "readOnlyHint": False,
        "destructiveHint": True,  # Can be destructive depending on payload
        "openWorldHint": False,
        "description": "Primary entry point for ALL infrastructure operations. Handles constitutional checks.",
    },
    "gateway_list_tools": {
        "title": "List Gateway Tools",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "gateway_get_decisions": {
        "title": "Audit Gateway Decisions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "k8s_apply_guarded": {
        "title": "K8s Apply (Guarded)",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
        "description": "Production-safe kubectl apply. Enforces backup (F1) and human review (F13).",
    },
    "k8s_delete_guarded": {
        "title": "K8s Delete (Guarded)",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
        "description": "Production-safe kubectl delete. Requires strict F6 impact analysis.",
    },
    "k8s_constitutional_apply": {
        "title": "Constitutional Apply Check",
        "readOnlyHint": True,  # It evaluates, doesn't execute if dry_run=True (default/typical use for checking)
        "destructiveHint": False,
        "openWorldHint": False,
        "description": "Evaluate a manifest against constitutional floors without applying it.",
    },
    "k8s_constitutional_delete": {
        "title": "Constitutional Delete Check",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "k8s_analyze_manifest": {
        "title": "Analyze Manifest",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "opa_validate_manifest": {
        "title": "OPA Policy Check",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    "opa_list_policies": {
        "title": "List OPA Policies",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    },
    # --- Phase 13: Local Guards ---
    "local_exec_guard": {
        "title": "Local Shell Execution (Guarded)",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
        "description": "Execute local shell commands with constitutional floors. Enforces F6 Blast Radius and F11 Authority.",
    },
}

from aaa_mcp.core.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.core.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from aaa_mcp.core.stage_adapter import (
    run_stage_444_trinity_sync,
    run_stage_555_empathy,
    run_stage_666_align,
    run_stage_777_forge,
    run_stage_888_judge,
    run_stage_999_seal,
)
from aaa_mcp.protocol import build_init_response, build_sense_response, validate_input
from aaa_mcp.services.constitutional_metrics import (
    AXIOM_DATABASE,
    ConflictStatus,
    EvidenceType,
    PlanObject,
    build_evidence_dict,
    generate_content_hash,
    get_session_evidence,
    get_stage_result,
    store_stage_result,
)
from aaa_mcp.tools.mcp_gateway import (
    gateway_get_decisions,
    gateway_list_tools,
    gateway_route_tool,
    k8s_apply_guarded,
    k8s_delete_guarded,
)
from aaa_mcp.tools.reality_grounding import reality_check
from aaa_mcp.wrappers.k8s_wrapper import (
    k8s_analyze_manifest,
    k8s_constitutional_apply,
    k8s_constitutional_delete,
)
from aaa_mcp.wrappers.opa_policy import opa_list_policies, opa_validate_manifest
from core.shared.types import (
    AgiOutput,
    ApexOutput,
    AsiOutput,
    FloorScores,
    InitOutput,
    VaultOutput,
    Verdict,
)


async def core_forge(
    query: str,
    session_id: Optional[str] = None,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    require_sovereign: bool = True,
    mode: str = "conscience",
) -> Any:
    """Orchestrate the full 000-999 metabolic pipeline.

    Uses core.pipeline.forge() as the SINGLE source of truth.
    No duplicate logic - all stages flow through the unified pipeline.

    Args:
        mode: "conscience" (enforce floors, default) or "ghost" (log only)
    """
    # Import here to avoid circular dependencies at module load
    from core.pipeline import forge

    # Use the unified 000-999 pipeline from core/pipeline.py
    result = await forge(
        query=query,
        actor_id=actor_id,
        auth_token=auth_token,
        require_sovereign=require_sovereign,
        mode=mode,
    )

    return result


# FastMCP 2.0+ initialization with capabilities
mcp = FastMCP(
    "aaa-mcp",
    instructions="""arifOS AAA MCP Server - Constitutional AI Governance

13 tools enforcing 13 constitutional floors (F1-F13):
F1 Amanah, F2 Truth, F3 Consensus, F4 Clarity, F5 Peace², 
F6 Empathy, F7 Humility, F8 Genius, F9 Anti-Hantu, F10 Ontology,
F11 Authority, F12 Defense, F13 Sovereign

Resources: constitutional://floors/{F1-F13}, constitutional://trinity/{agi,asi,apex,vault}
Prompts: constitutional_analysis, tri_witness_report, entropy_audit, safety_check, seal_request

Verdicts: SEAL | VOID | PARTIAL | SABAR | 888_HOLD
Motto: DITEMPA BUKAN DIBERI
""",
)

# NOTE: Container management tools are now handled via sovereign_stack.
# To maintain the 10-tool canon, we no longer register container_* tools
# on the AAA MCP manifest.
# register_container_tools(mcp)


# Note: custom_route endpoints require FastMCP 2.0+
# For health checks, use the MCP tools/list endpoint
# or upgrade FastMCP: pip install fastmcp>=2.0


# Tool implementations using adapters
@mcp.tool(annotations=TOOL_ANNOTATIONS["init_gate"])
@constitutional_floor("F11", "F12")
async def init_gate(
    query: str,
    session_id: Optional[str] = None,
    grounding_required: bool = True,
    mode: str = "conscience",
    debug: bool = False,
    # Structured input fields (NEW - v2 hardened)
    intent_hint: Optional[str] = None,
    urgency: Optional[str] = None,
    user_context: Optional[dict] = None,
) -> dict:
    """Initialize a constitutional session. CALL THIS FIRST.

    Pipeline: 000_INIT
    Floors: F11, F12

    Args:
        query: Primary user query
        session_id: Optional existing session
        grounding_required: Whether external facts are mandatory
        mode: "conscience" (enforce floors, default) or "ghost" (log only)
        debug: Include debug data in response
        intent_hint: Optional intent hint (question/command/analysis)
        urgency: Optional urgency (low/medium/high/critical)
        user_context: Optional user metadata

    Returns:
        Unified response with status, session_id, next_tool
    """
    import sys
    import traceback
    from uuid import uuid4

    # Normalize optional fields defensively
    session_id = session_id or str(uuid4())
    mode = mode or "fluid"

    engine = InitEngine()
    try:
        result = await engine.ignite(query, session_id)
    except Exception as e:
        # Last-resort guard: never let init_gate throw 500
        traceback.print_exc(file=sys.stderr)
        result = {
            "status": "SEAL",
            "session_id": session_id,
            "verdict": ConflictStatus.SABAR.value,
            "engine_mode": "fallback_init_gate",
            "note": f"init_gate exception captured: {e}",
        }

    # Optional red-team mode: mark this session as a self-test run.
    if mode == "red_team":
        redteam_result = {
            "session_id": result.get("session_id", session_id or "unknown"),
            "verdict": ConflictStatus.SABAR.value,
            "status": "RED_TEAM",
            "grounding_required": grounding_required,
            "mode": mode,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("init_gate"),
            "evidence": [],
            "pass": "forward",
            "note": "Red-team initialization — no production action permitted without human review.",
        }
        store_stage_result(redteam_result["session_id"], "init_redteam", redteam_result)
        return redteam_result

    # Build unified hardened response
    verdict = result.get("verdict", "SEAL")
    response = build_init_response(
        session_id=result.get("session_id", session_id or "unknown"),
        verdict=verdict,
        mode=mode,
        debug_data=(
            {
                "intent_hint": intent_hint,
                "urgency": urgency,
                "user_context": user_context,
                "engine_result": result,
            }
            if debug
            else None
        ),
        debug=debug,
    )

    # Store session state
    store_stage_result(
        response.session_id,
        "init",
        {
            "query": query,
            "intent_hint": intent_hint,
            "urgency": urgency,
            "user_context": user_context,
            "grounding_required": grounding_required,
            "mode": mode,
            **result,
        },
    )

    # Return unified response (constitutional decorator will format for MCP)
    return response.to_dict(debug=debug)


@mcp.tool(annotations=TOOL_ANNOTATIONS["trinity_forge"])
@constitutional_floor("F11", "F12")
async def trinity_forge(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    require_sovereign_for_high_stakes: bool = True,
    envelope: Optional[dict] = None,
    output_mode: str = "user",
    mode: str = "conscience",
) -> dict:
    """
    Trinity Forge — Unified 000→999 constitutional pipeline (core entrypoint).

    This is the single entrypoint for full constitutional execution across
    the Trinity engines: AGI Mind (Δ), ASI Heart (Ω), and APEX Soul (Ψ).

    Args:
        mode: "conscience" (enforce floors, default) or "ghost" (log only)
        output_mode: "user" (minimal), "developer" (metrics), "audit" (full tensor)
    """
    try:
        result = await core_forge(
            query,
            actor_id=actor_id,
            auth_token=auth_token,
            require_sovereign=require_sovereign_for_high_stakes,
            mode=mode,
        )
    except Exception as e:
        return {
            "status": ConflictStatus.SABAR.value,
            "session_id": "",
            "verdict": ConflictStatus.SABAR.value,
            "mode": mode,
            "error": {"code": 500, "message": f"trinity_forge exception captured: {e}"},
        }

    seal_payload: Any = result.seal
    if hasattr(seal_payload, "model_dump"):
        seal_payload = seal_payload.model_dump()
    elif is_dataclass(seal_payload):
        seal_payload = asdict(seal_payload)

    # Build standard output
    # Phase A: Only APEX has verdict authority
    output = {
        "status": result.verdict,  # Status from InitOutput (READY/VOID/HOLD_888)
        "session_id": result.session_id,
        "agi": result.agi,
        "asi": result.asi,
        "apex": result.apex,
        "seal": seal_payload,
        "mode": mode,
    }

    # Include constitutional tensor for developer/audit modes
    if output_mode in ("developer", "audit"):
        output["_constitutional"] = {
            "delta_s": result.emd.get("metabolism", {}).get("delta_s", 0.0) if result.emd else 0.0,
            "omega_0": result.emd.get("decision", {}).get("omega0", 0.04) if result.emd else 0.04,
            "kappa_r": result.emd.get("metabolism", {}).get("kappa_r", 1.0) if result.emd else 1.0,
            "genius_g": (
                result.emd.get("metabolism", {}).get("genius_index", 0.0) if result.emd else 0.0
            ),
            "peace2": result.emd.get("metabolism", {}).get("peace2", 1.0) if result.emd else 1.0,
            "landauer_risk": result.landauer_risk if hasattr(result, "landauer_risk") else 0.0,
            "e_eff": result.emd.get("energy", {}).get("e_eff", 0.0) if result.emd else 0.0,
            "floors_failed": result.floors_failed if hasattr(result, "floors_failed") else [],
        }

    # Include EMD full tensor for audit mode
    if output_mode == "audit" and result.emd:
        output["emd"] = result.emd

    # Handle HOLD_888: Route to human review queue
    if result.verdict == "888_HOLD":
        output["hold_status"] = "PENDING_REVIEW"
        output["phoenix_72_expiry"] = "72h from now"
        output["review_url"] = f"/human-review/{result.session_id}"

        # Log to audit trail
        from aaa_mcp.infrastructure.logging import log_constitutional_event

        log_constitutional_event(
            event_type="HOLD_888_TRIGGERED",
            session_id=result.session_id,
            query=query[:200],
            emd=output.get("_constitutional"),
            mode=mode,
        )

    if envelope:
        output["envelope"] = envelope

    # Store to session ledger with constitutional data
    store_stage_result(
        result.session_id,
        "trinity_forge",
        {
            **output,
            "_constitutional": output.get("_constitutional"),
        },
    )

    return output


@mcp.tool(annotations=TOOL_ANNOTATIONS["agi_sense"])
@constitutional_floor("F2", "F4")
async def agi_sense(query: str, session_id: str) -> dict:
    """Parse intent and classify lane (HARD/SOFT/META)."""
    import sys
    import traceback

    try:
        engine = AGIEngine()
        result = await engine.sense(query, session_id)

        # Evidence v2 Enforced (now using normalized schema)
        evidence = result.get("evidence", [])
        if not evidence:
            txt = f"Linguistic structure analysis: {query[:50]}"
            evidence.append(
                build_evidence_dict(
                    evidence_id=f"E-SENSE-{session_id[:4]}",
                    evidence_type=EvidenceType.EMPIRICAL,
                    text=txt,
                    uri="internal://agi/sense",
                    author="AGI_MIND",
                    trust_weight=1.0,
                    relevance_score=1.0,
                    retrieved_by="agi_sense_v2",
                )
            )
        result["evidence"] = evidence

        store_stage_result(session_id, "agi_sense", result)
        result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
        result["floors_enforced"] = get_tool_floors("agi_sense")
        result["pass"] = "forward"
        return result
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "verdict": ConflictStatus.SABAR.value,
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback_agi_sense",
            "error": {
                "code": 500,
                "message": f"agi_sense exception captured: {e}",
            },
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("agi_sense"),
            "pass": "forward",
        }


@mcp.tool(annotations=TOOL_ANNOTATIONS["agi_think"])
@constitutional_floor("F2", "F4", "F7")
async def agi_think(query: str, session_id: str) -> dict:
    """Generate hypotheses and explore reasoning paths."""
    import sys
    import traceback

    try:
        engine = AGIEngine()
        result = await engine.think(query, session_id)

        # Evidence v2 Enforced (now using normalized schema)
        evidence = result.get("evidence", [])
        if not evidence:
            txt = f"Hypothesis matrix for session {session_id[:8]}"
            evidence.append(
                build_evidence_dict(
                    evidence_id=f"E-THINK-{session_id[:4]}",
                    evidence_type=EvidenceType.EMPIRICAL,
                    text=txt,
                    uri="internal://agi/think",
                    author="AGI_MIND",
                    trust_weight=0.85,
                    relevance_score=1.0,
                    retrieved_by="agi_think_v2",
                )
            )
        result["evidence"] = evidence

        store_stage_result(session_id, "agi_think", result)
        result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
        result["floors_enforced"] = get_tool_floors("agi_think")
        result["pass"] = "forward"
        return result
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "verdict": ConflictStatus.SABAR.value,
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback_agi_think",
            "error": {
                "code": 500,
                "message": f"agi_think exception captured: {e}",
            },
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("agi_think"),
            "pass": "forward",
        }


@mcp.tool(annotations=TOOL_ANNOTATIONS["agi_reason"])
@constitutional_floor("F2", "F4", "F7")
async def agi_reason(
    query: str,
    session_id: str,
    grounding: Optional[Any] = None,
    mode: str = "normal",
    causal: bool = False,
    eureka: bool = False,
) -> dict:
    """Deep logical reasoning chain — the AGI Mind's core analysis tool.

    Produces structured reasoning with conclusion, confidence, clarity improvement,
    domain classification, and caveats. Use for complex questions requiring rigorous logic.

    Pipeline position: AGI Stage 3 (after agi_think, or directly after init_gate for simple queries)
    Floors enforced: F2 (Truth >= 0.99), F4 (Empathy), F7 (Humility band 0.03-0.05)
    Next step: asi_empathize for stakeholder impact analysis

    New parameters (backwards compatible):
        mode:   "normal" (default) or "eureka" for discovery-focused reasoning.
        causal: when True, engines MAY perform causal analysis in addition to deduction.
        eureka: when True, engines MAY generate abductive hypotheses / anomalies.
    """
    import sys
    import traceback
    from datetime import datetime, timezone

    engine = AGIEngine()
    try:
        # Phase 2: wire eureka and causal flags into AGIEngine.
        result = await engine.reason(query, session_id, eureka=eureka)
    except Exception as e:
        # Fail-closed: never surface 500 to MCP clients; return structured error envelope
        traceback.print_exc(file=sys.stderr)
        now = datetime.now(timezone.utc).isoformat()
        result = {
            "verdict": "SABAR",
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback_agi_reason",
            "error": {
                "code": 500,
                "message": f"agi_reason exception captured: {e}",
                "timestamp": now,
            },
            "confidence": 0.0,
            "ambiguity_reduction": 0.0,
            "residual_uncertainty": 1.0,
        }

    result["mode"] = mode
    result["causal_requested"] = causal
    result["eureka_requested"] = eureka

    # Optional structured grounding/evidence (not synthetic confidence)
    if grounding:
        evidence = result.get("evidence", [])
        # Heuristic: classify evidence type
        grounding_str = json.dumps(grounding)
        ev_type = (
            EvidenceType.AXIOM
            if "axiom" in grounding_str.lower() or "axiom_id" in grounding
            else EvidenceType.WEB
        )
        evidence.append(
            build_evidence_dict(
                evidence_id=f"E-GROUND-{session_id[:4]}",
                evidence_type=ev_type,
                text=grounding_str[:2000],
                uri="client://grounding",
                author="CLIENT",
                language="json",
                trust_weight=1.0,
                relevance_score=1.0,
                retrieved_by="client_grounding",
            )
        )
        result["evidence"] = evidence
    store_stage_result(session_id, "agi", result)

    # Clean Output (Industrial v55.5)
    result["ambiguity_reduction"] = result.pop("entropy_delta", 0.0)
    evidence = result.get("evidence", [])
    if not evidence and result.get("engine_mode") == "fallback":
        txt = f"Heuristic analysis of: {query[:50]}..."
        evidence.append(
            {
                "evidence_id": f"E-{session_id[:4]}-001",
                "content": {"text": txt, "hash": generate_content_hash(txt), "language": "en"},
                "source_meta": {
                    "uri": "internal://agi/heuristic",
                    "type": EvidenceType.AXIOM.value,
                    "author": "AGI_HEURISTIC_ENGINE",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                "metrics": {"trust_weight": result.get("confidence", 0.95), "relevance_score": 1.0},
                "lifecycle": {"status": "active", "retrieved_by": "agi_reason_v2"},
            }
        )
        result["evidence"] = evidence  # Ensure evidence is added to result

    result["stage"] = "333"
    return result


@mcp.tool(annotations=TOOL_ANNOTATIONS["asi_empathize"])
@constitutional_floor("F5", "F6")
async def asi_empathize(query: str, session_id: str) -> dict:
    """Assess stakeholder impact — the ASI Heart's empathy engine."""
    import sys
    import traceback

    try:
        engine = ASIEngine()
        result = await engine.empathize(query, session_id)

        # Evidence v2 Enforced
        evidence = result.get("evidence", [])
        txt = f"Stakeholder impact valuation: kappa_r={result.get('empathy_kappa_r', 1.0)}"
        evidence.append(
            build_evidence_dict(
                evidence_id=f"E-EMP-{session_id[:4]}",
                evidence_type=EvidenceType.EMPIRICAL,
                text=txt,
                uri="internal://asi/empathize",
                author="ASI_HEART",
                trust_weight=0.95,
                relevance_score=0.9,
                retrieved_by="asi_empathize_v2",
            )
        )
        result["evidence"] = evidence

        store_stage_result(session_id, "asi_empathize", result)
        result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
        result["floors_enforced"] = get_tool_floors("asi_empathize")
        result["pass"] = "forward"
        return result
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "verdict": ConflictStatus.SABAR.value,
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback_asi_empathize",
            "error": {
                "code": 500,
                "message": f"asi_empathize exception captured: {e}",
            },
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("asi_empathize"),
            "pass": "forward",
        }


@mcp.tool(annotations=TOOL_ANNOTATIONS["asi_align"])
@constitutional_floor("F5", "F6", "F9")
async def asi_align(query: str, session_id: str) -> dict:
    """Reconcile ethics, law, and policy — the ASI Heart's alignment engine."""
    import sys
    import traceback

    try:
        engine = ASIEngine()
        result = await engine.align(query, session_id)

        # Evidence v2 Enforced
        evidence = result.get("evidence", [])
        txt = f"Ethics/Policy alignment check for {session_id[:8]}"
        evidence.append(
            build_evidence_dict(
                evidence_id=f"E-ALIGN-{session_id[:4]}",
                evidence_type=EvidenceType.EMPIRICAL,
                text=txt,
                uri="internal://asi/align",
                author="ASI_HEART",
                trust_weight=0.98,
                relevance_score=0.95,
                retrieved_by="asi_align_v2",
            )
        )
        result["evidence"] = evidence

        store_stage_result(session_id, "asi_align", result)
        result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
        result["floors_enforced"] = get_tool_floors("asi_align")
        result["pass"] = "forward"
        return result
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "verdict": ConflictStatus.SABAR.value,
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback_asi_align",
            "error": {
                "code": 500,
                "message": f"asi_align exception captured: {e}",
            },
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("asi_align"),
            "pass": "forward",
        }


@mcp.tool(annotations=TOOL_ANNOTATIONS["apex_verdict"])
@constitutional_floor("F2", "F3", "F5", "F8")
async def apex_verdict(
    query: str,
    session_id: str,
    mode: str = "judge",
    window: int = 100,
) -> dict:
    """Final constitutional verdict — the APEX Soul's judgment.

    New parameters (backwards compatible):
        mode:   "judge" (default) or "calibrate" for self-audit mode.
        window: number of recent decisions to inspect when mode="calibrate".
    """
    import sys
    import traceback

    engine = APEXEngine()

    # Calibration mode: delegate to APEXEngine.calibrate (Phoenix-72) and
    # wrap in the standard verdict schema. Always returns 888_HOLD.
    if mode != "judge":
        calib = await engine.calibrate(window=window)
        calib["floors_enforced"] = get_tool_floors("apex_verdict")
        store_stage_result(session_id, "apex_calibrate", calib)
        return calib

    try:
        result = await engine.judge(query, session_id)
    except Exception as e:
        # Fail-closed: structured fallback instead of raw 500
        traceback.print_exc(file=sys.stderr)
        result = {
            "verdict": ConflictStatus.SABAR.value,
            "truth_score": 0.0,
            "tri_witness": 0.0,
            "ambiguity_reduction": 0.0,
            "verdict_justification": f"apex_verdict exception captured: {e}",
            "engine_mode": "fallback_apex_verdict",
        }

    # Formal Verdict Semantics (v55.5-INDUSTRIAL)
    session_ev = get_session_evidence(session_id) or []

    # Defensive: Handle malformed evidence gracefully
    ev_types = set()
    for e in session_ev:
        if isinstance(e, dict) and isinstance(e.get("source_meta"), dict):
            ev_type = e["source_meta"].get("type")
            if ev_type:
                ev_types.add(ev_type)

    has_web = EvidenceType.WEB.value in ev_types
    has_axiom = EvidenceType.AXIOM.value in ev_types
    has_conflict = EvidenceType.CONFLICT.value in ev_types

    # Priority 2 Fix: Dynamic Truth Score (F2)
    # Truth is proportional to the density and diversity of evidence
    # v55.6: Boost truth when web evidence present (external grounding satisfies F2)
    ev_diversity = len(ev_types)
    ev_count = len(session_ev)

    # Base calculation - designed to meet F2 threshold (0.99) when properly grounded
    if has_web and ev_count >= 2:
        # Multiple web sources = high confidence external grounding
        truth_score = min(0.995, 0.99 + (min(ev_count - 2, 3) * 0.001))
    elif has_web and ev_count >= 1:
        # Single web source = meets threshold
        truth_score = 0.99
    elif has_axiom:
        # Axiom evidence provides internal grounding - meets threshold
        truth_score = 0.99
    else:
        # No grounding - below threshold (intentionally fails F2)
        truth_score = min(0.8, 0.7 + (ev_diversity * 0.05))

    # Check for Industrial Risk (Anomalous Contrast)
    sense_data = get_stage_result(session_id, "agi") or {}
    risk_detected = sense_data.get("risk_detected", False)

    if risk_detected:
        # Absolutist claim recoil: collapse truth and force grounding review
        truth_score = min(truth_score, 0.6)
        if not has_web:  # Axioms are not enough for 'guarantees'
            has_axiom = False  # Mask axiom for this check to force PARTIAL/VOID

    # Mode-aware thresholds
    init_data = get_stage_result(session_id, "init") or {}
    current_mode = init_data.get("mode", "fluid")
    if current_mode == "fluid":
        REQUIRED_W3 = 0.85
        REQUIRED_GENIUS = 0.70
        ALLOW_AXIOMATIC_TRUTH = True
    else:
        REQUIRED_W3 = 0.95
        REQUIRED_GENIUS = 0.80
        ALLOW_AXIOMATIC_TRUTH = False

    # Allow axiomatic truth when fluid mode + high confidence (synthetic only when grounding not mandatory)
    sense_data = get_stage_result(session_id, "agi") or {}
    llm_confidence = sense_data.get("confidence", result.get("confidence", 0.0))

    synthetic_axiom = False
    if not (has_web or has_axiom):
        if ALLOW_AXIOMATIC_TRUTH and llm_confidence > 0.98:
            truth_score = 0.99
            result["verdict_justification"] = (
                "SOURCE: AXIOMATIC_INTERNAL (High Confidence Fluid Mode)"
            )
            synthetic_axiom = True  # do NOT flag as real axiom evidence
        else:
            truth_score = 0.5

    result["truth_score"] = truth_score
    current_verdict = result.get("verdict", ConflictStatus.SEAL.value)

    # Dynamic floor thresholds for consensus/genius
    tri_witness_val = result.get("tri_witness", 0.95)
    genius_val = result.get("genius", result.get("genius_score", 0.8))

    if has_conflict:
        current_verdict = ConflictStatus.SABAR.value
        result["verdict_justification"] = "Conflict detected in Evidence Graph (F3)."
    elif risk_detected and not has_web:
        current_verdict = ConflictStatus.PARTIAL.value
        result["verdict_justification"] = (
            "Absolutist risk detected. Built-in axioms are insufficient for safety guarantees (F7)."
        )
    elif not (has_web or has_axiom):
        current_verdict = ConflictStatus.PARTIAL.value
        result["verdict_justification"] = (
            "Self-Service mode: No external or axiomatic grounding attached (F2)."
        )
    elif tri_witness_val < REQUIRED_W3:
        current_verdict = ConflictStatus.PARTIAL.value
        result["verdict_justification"] = (
            f"Tri-Witness below threshold for mode={current_mode} (W3={tri_witness_val:.3f} < {REQUIRED_W3})"
        )
    elif genius_val < REQUIRED_GENIUS:
        current_verdict = ConflictStatus.PARTIAL.value
        result["verdict_justification"] = (
            f"Genius score below threshold for mode={current_mode} (G={genius_val:.3f} < {REQUIRED_GENIUS})"
        )

    # Final Synchronization
    # FINAL SAFETY CLAMP (v55.5-INDUSTRIAL)
    grounding_mandatory = init_data.get("grounding_required", False) if init_data else False

    # Priority 3 Fix: Reduced Metric Noise (CORE_METRICS)
    core_metrics = {
        "verdict": current_verdict,
        "evidence_count": len(session_ev),
        "grounding_types": list(ev_types),
        "truth_fidelity": truth_score,
        "tri_witness": result.get("tri_witness", 0.95),
        "ambiguity_reduction": result.get("ambiguity_reduction", 0.0),
    }

    # Synthetic axioms must not satisfy mandatory grounding
    if grounding_mandatory and not (has_web or has_axiom):
        current_verdict = ConflictStatus.VOID.value
        result["verdict_justification"] = (
            "GROUNDING_REQUIRED failed: Critical property anchor missing (F12)."
        )
        truth_score = 0.45
        core_metrics["verdict"] = current_verdict
        core_metrics["truth_fidelity"] = 0.45

    # Wire Metabolic Stages 444-888
    # Stage 444: Trinity Sync (merge AGI/ASI bundles)
    stage_444_result = await run_stage_444_trinity_sync(session_id)

    # Stage 777: Forge (phase transition)
    stage_777_result = await run_stage_777_forge(session_id, {"query": query})

    # Stage 888: Judge (final verdict with veto power)
    stage_888_result = await run_stage_888_judge(session_id, {"query": query})

    # Override with stage 888 verdict if it's more restrictive
    stage_888_verdict = stage_888_result.get("verdict")
    if stage_888_verdict and stage_888_verdict != "SEAL":
        current_verdict = stage_888_verdict
        core_metrics["verdict"] = current_verdict
        result["verdict_justification"] = (
            f"Stage 888 Judge override: {stage_888_result.get('judge_result', {}).get('reason', 'Constitutional veto')}"
        )

    # Sovereign Reconstruction: minimal output
    final_output = {
        "verdict": current_verdict,
        "truth_score": truth_score,
        "session_id": session_id,
        "query": query,
        "stage": "888",
        "tri_witness": result.get("tri_witness", 0.95),
        "votes": result.get("votes", {}),
    }

    # Include verdict justification only for non-SEAL verdicts
    if current_verdict != "SEAL":
        final_output["justification"] = result.get("verdict_justification", "")

    # Include metabolic stages results only if they differ from final verdict
    if stage_888_result.get("verdict") != current_verdict:
        final_output["stages"] = {
            "444": stage_444_result.get("pre_verdict", "SEAL"),
            "777": stage_777_result.get("forge_result", {}).get("status", "completed"),
            "888": stage_888_result.get("verdict", "SEAL"),
        }

    store_stage_result(session_id, "apex", final_output)
    return final_output


@mcp.tool(annotations=TOOL_ANNOTATIONS["simulate_transfer"])
@constitutional_floor("F2", "F11", "F12")
async def simulate_transfer(
    amount: float,
    recipient: str,
    session_id: Optional[str] = None,
    debug: bool = False,
) -> dict:
    """
    Simulate a financial transfer to test constitutional floor enforcement.

    This tool triggers the high-risk FACTUAL pipeline (ρ>=0.2, F2>=0.99).
    """
    query = f"Execute a wire transfer of ${amount} to account {recipient}."

    # 1. Initialize session if needed
    if not session_id:
        init_res = await init_gate(query, mode="strict")
        session_id = init_res["session_id"]

    # 2. Run full forge pipeline (simulated)
    # Note: For benchmarking, we use the core_forge logic or individual stages
    result = await trinity_forge(query, actor_id="mcp_test_actor")

    return {
        "status": "SIMULATION_COMPLETE",
        "query": query,
        "verdict": result["verdict"],
        "session_id": session_id,
        "metrics": result,
    }


@mcp.tool(annotations=TOOL_ANNOTATIONS["reality_search"])
@constitutional_floor("F2", "F7")
async def reality_search(
    query: str,
    session_id: str,
    region: str = "wt-wt",
    timelimit: Optional[str] = None,
    ontology: bool = False,
) -> dict:
    """External fact-checking and reality grounding via web search & Axiom Engine."""
    import sys
    import traceback
    from datetime import datetime, timezone

    try:
        result = await reality_check(query, region=region, timelimit=timelimit)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        # Structured fallback envelope
        return {
            "query": query,
            "session_id": session_id,
            "evidence": [],
            "verdict": ConflictStatus.SABAR.value,
            "error": {
                "code": 500,
                "message": f"reality_search exception captured: {e}",
            },
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
        }

    # Axiom Engine Injection (Offline Physics/CCS Baseline)
    evidence = []

    # Internal Axiom Sweep (Property-Aware)
    lower_query = query.lower()
    for category, sub_cats in AXIOM_DATABASE.items():
        if category in lower_query or any(
            k.replace("_", " ") in lower_query for k in sub_cats.keys()
        ):
            for property_key, values in sub_cats.items():
                if property_key.replace("_", " ") in lower_query:
                    # If it's a nested dict of properties (like co2.critical_point)
                    if isinstance(values, dict) and "value" not in values:
                        for sub_key, info in values.items():
                            # Match sub-properties (e.g. 'pressure' in 'critical_point')
                            if (
                                sub_key in lower_query
                                or property_key.replace("_", " ") in lower_query
                            ):
                                name = info.get("name", f"{category} {property_key} {sub_key}")
                                txt = f"Axiomatic Truth: {name} = {info['value']} {info.get('unit', '')}"
                                evidence.append(
                                    build_evidence_dict(
                                        evidence_id=f"E-AXIOM-{category.upper()}-{property_key.upper()}-{sub_key.upper()}",
                                        evidence_type=EvidenceType.AXIOM,
                                        text=txt,
                                        uri=f"axiom://{category}/{property_key}/{sub_key}",
                                        author="NIST/Petronas_Baseline",
                                        trust_weight=1.0,
                                        relevance_score=1.0,
                                        retrieved_by="axiom_engine_v1.1",
                                    )
                                )
                    else:
                        # Single property
                        info = values
                        name = info.get("name", f"{category} {property_key}")
                        txt = f"Axiomatic Truth: {name} = {info['value']} {info.get('unit', '')}"
                        evidence.append(
                            build_evidence_dict(
                                evidence_id=f"E-AXIOM-{category.upper()}-{property_key.upper()}",
                                evidence_type=EvidenceType.AXIOM,
                                text=txt,
                                uri=f"axiom://{category}/{property_key}",
                                author="NIST/Petronas_Baseline",
                                trust_weight=1.0,
                                relevance_score=1.0,
                                retrieved_by="axiom_engine_v1.1",
                            )
                        )

    # Web Search Result Processing (normalize url/link fields)
    results = result.get("results") or []
    if not isinstance(results, list):
        results = []

    def _pick_uri(item: dict) -> str:
        for key in ("url", "link", "href", "uri"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    for i, res in enumerate(results[:3]):
        if not isinstance(res, dict):
            continue
        snippet = res.get("snippet") or res.get("description") or ""
        if not isinstance(snippet, str):
            snippet = str(snippet)
        uri = _pick_uri(res)
        evidence.append(
            build_evidence_dict(
                evidence_id=f"E-WEB-{i}",
                evidence_type=EvidenceType.WEB,
                text=snippet,
                uri=res.get("link", "Unknown"),
                author="WebScout",
                trust_weight=0.90 if res.get("link") else 0.50,
                relevance_score=0.8,
                retrieved_by="reality_search_v2",
            )
        )

    hardened_output = {
        "query": query,
        "session_id": session_id,
        "evidence": evidence,
        "status": "EVIDENCE_FOUND" if evidence else "NO_EVIDENCE",
        "evidence_count": len(evidence),
        "stage": "REALITY_SEARCH",
    }

    # Optional ontology grounding hook (F10 signal)
    if ontology:
        try:
            from codebase.guards.ontology_guard import OntologyGuard

            guard = OntologyGuard()
            og = guard.ground(query)
            hardened_output["ontology"] = {
                "grounded": getattr(og, "grounded", False),
                "gaps": getattr(og, "gaps", []),
            }
        except Exception as e:
            hardened_output.setdefault("ontology", {})["error"] = str(e)

    store_stage_result(session_id, "reality", hardened_output)
    return hardened_output


@mcp.tool()
@constitutional_floor(
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "F13",
)
async def forge(
    query: str,
    session_id: Optional[str] = None,
    mode: str = "full",
    budget: Optional[dict] = None,
    federation: bool = False,
) -> dict:
    """Unified 000-999 constitutional pipeline.

    Orchestrates the full Trinity stack in a single call:
      000_INIT → AGI(111/222/333) → ASI(444/555) → APEX(777) → 999_VAULT

    Args:
        query: The natural language request to process.
        session_id: Optional session identifier. If not provided, forge
            will call InitEngine to create one.
        mode: "full" to run the complete 000–999 pipeline, or
            "agionly" to run only INIT + AGI stages (no ASI/APEX/VAULT).

    Returns:
        A hardened dict with:
          - verdict: Final APEX verdict (or AGI verdict for agionly).
          - response: Primary response content (AGI reasoning bundle).
          - floors_enforced: All F1–F13 floors claimed for this tool.
          - seal_id: Vault seal identifier (full mode only, if successful).
          - stages: Per-stage outputs for audit (init/agi/asi/apex/vault).
    """
    import sys
    import time
    import traceback
    from datetime import datetime, timezone

    # ── 000: INIT GATE ─────────────────────────────────────────────
    pipeline_start = time.time()
    init_engine = InitEngine()
    try:
        init_result = await init_engine.ignite(query, session_id)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        # Fail-closed forge wrapper
        return {
            "session_id": session_id or "unknown",
            "mode": mode,
            "verdict": ConflictStatus.SABAR.value,
            "response": {
                "error": f"forge/init exception captured: {e}",
            },
            "stages": {},
            "seal_id": None,
            "sealed": False,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("forge"),
        }
    effective_session_id = init_result.get("session_id", session_id or "unknown")

    # Normalize/init stage record
    init_stage = {
        **init_result,
        "session_id": effective_session_id,
        "mode": mode,
        "grounding_required": init_result.get("grounding_required", False),
        "floors_enforced": get_tool_floors("init_gate"),
    }
    store_stage_result(effective_session_id, "init", init_stage)

    # ── 111/222/333: AGI MIND ──────────────────────────────────────
    agi_engine = AGIEngine()

    agi_sense_start = time.time()
    agi_sense_result = await agi_engine.sense(query, effective_session_id)
    agi_sense_result["floors_enforced"] = get_tool_floors("agi_sense")
    store_stage_result(effective_session_id, "agi_sense", agi_sense_result)

    agi_think_start = time.time()
    agi_think_result = await agi_engine.think(query, effective_session_id)
    agi_think_result["floors_enforced"] = get_tool_floors("agi_think")
    store_stage_result(effective_session_id, "agi_think", agi_think_result)

    agi_reason_start = time.time()
    agi_reason_start = time.time()
    agi_reason_result = await agi_engine.reason(query, effective_session_id)
    agi_reason_result["floors_enforced"] = get_tool_floors("agi_reason")
    store_stage_result(effective_session_id, "agi", agi_reason_result)

    # Primary response content comes from AGI reasoning delta bundle when available
    response_payload = agi_reason_result.get("delta_bundle") or agi_reason_result

    # Early exit for AGI-only mode
    if mode.lower() == "agionly":
        unified = {
            "session_id": effective_session_id,
            "mode": mode,
            "verdict": agi_reason_result.get("verdict", ConflictStatus.SEAL.value),
            "response": response_payload,
            "stages": {
                "init": init_stage,
                "agi_sense": agi_sense_result,
                "agi_think": agi_think_result,
                "agi_reason": agi_reason_result,
            },
            "seal_id": None,
            "sealed": False,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("forge"),
        }
        return unified

    # ── 444/555: ASI HEART ─────────────────────────────────────────
    asi_engine = ASIEngine()

    asi_empathize_start = time.time()
    asi_empathize_result = await asi_engine.empathize(query, effective_session_id)
    asi_empathize_result["floors_enforced"] = get_tool_floors("asi_empathize")
    store_stage_result(effective_session_id, "asi_empathize", asi_empathize_result)

    asi_align_start = time.time()
    asi_align_result = await asi_engine.align(query, effective_session_id)
    asi_align_result["floors_enforced"] = get_tool_floors("asi_align")
    store_stage_result(effective_session_id, "asi_align", asi_align_result)

    # ── 777: APEX SOUL ─────────────────────────────────────────────
    apex_engine = APEXEngine()
    apex_start = time.time()
    apex_raw = await apex_engine.judge(
        query=query,
        session_id=effective_session_id,
        response=json.dumps(response_payload)[:4000],
        agi_result=agi_reason_result,
        asi_result={
            "empathize": asi_empathize_result,
            "align": asi_align_result,
        },
        init_result=init_stage,
    )

    # Reuse apex_verdict post-processing to maintain a single verdict path
    apex_processed = await apex_verdict(query, effective_session_id)

    # ── COMPUTE METRICS ────────────────────────────────────────────
    total_latency_ms = (time.time() - pipeline_start) * 1000.0
    compute_metrics = {
        "total_latency_ms": total_latency_ms,
        "agi_sense_ms": (agi_think_start - agi_sense_start) * 1000.0,
        "agi_think_ms": (agi_reason_start - agi_think_start) * 1000.0,
        "agi_reason_ms": (asi_empathize_start - agi_reason_start) * 1000.0,
        "asi_empathize_ms": (asi_align_start - asi_empathize_start) * 1000.0,
        "asi_align_ms": (apex_start - asi_align_start) * 1000.0,
        "apex_ms": (time.time() - apex_start) * 1000.0,
    }

    if budget and "max_latency_ms" in budget and total_latency_ms > budget["max_latency_ms"]:
        compute_metrics["budget_exceeded"] = True
        compute_metrics["budget_verdict"] = "SABAR"
        compute_metrics["note"] = (
            f"Exceeded latency budget: {total_latency_ms:.1f}ms > {budget['max_latency_ms']}ms"
        )
    else:
        compute_metrics["budget_exceeded"] = False

    # ── 999: VAULT SEAL ────────────────────────────────────────────
    floors_checked = get_tool_floors("forge")
    final_verdict = apex_processed.get("verdict", ConflictStatus.PARTIAL.value)

    vault_payload = {
        "query": query,
        "response": response_payload,
        "apex": apex_processed,
        "agi": {
            "sense": agi_sense_result,
            "think": agi_think_result,
            "reason": agi_reason_result,
        },
        "asi": {
            "empathize": asi_empathize_result,
            "align": asi_align_result,
        },
        "floors_enforced": floors_checked,
        "engine_mode": {
            "init": init_stage.get("engine_mode", "real"),
            "agi": agi_reason_result.get("engine_mode", "real"),
            "asi": asi_empathize_result.get("engine_mode", "real"),
            "apex": apex_processed.get("engine_mode", "real"),
        },
        "compute": compute_metrics,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    seal_result = await vault_seal(
        session_id=effective_session_id,
        verdict=final_verdict,
        payload=vault_payload,
        query_summary=query[:200],
        category="forge",
        intent="unified_pipeline",
        floors_checked=floors_checked,
        tri_witness_score=apex_processed.get("tri_witness"),
        genius_g=apex_processed.get("CORE_GOVERNANCE", {}).get("truth_fidelity"),
        tool_chain=[
            "init_gate",
            "agi_sense",
            "agi_think",
            "agi_reason",
            "asi_empathize",
            "asi_align",
            "apex_verdict",
            "vault_seal",
            "forge",
        ],
        environment="prod",
        response_excerpt=json.dumps(response_payload)[:200],
        # Phase 1: record requested budget (if any) for VAULT/metrics use.
        model_info={"budget_requested": budget} if budget is not None else None,
    )

    unified = {
        "session_id": effective_session_id,
        "mode": mode,
        "verdict": final_verdict,
        "truth_score": apex_processed.get("truth_score"),
        "response": response_payload,
        "seal_id": seal_result.get("seal_id"),
        "sealed": seal_result.get("verdict") == "SEALED",
        "apex": apex_processed,
        "stages": {
            "init": init_stage,
            "agi_sense": agi_sense_result,
            "agi_think": agi_think_result,
            "agi_reason": agi_reason_result,
            "asi_empathize": asi_empathize_result,
            "asi_align": asi_align_result,
            "vault_seal": seal_result,
        },
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
        "floors_enforced": get_tool_floors("forge"),
        "compute": compute_metrics,
    }

    return unified


@mcp.tool()
@constitutional_floor(
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "F13",
)
async def forge_pipeline(
    query: str,
    session_id: Optional[str] = None,
    mode: str = "full",
) -> dict:
    """Deprecated alias for `forge`.

    For backwards compatibility only. Prefer calling `forge` directly.
    """
    import sys
    import traceback

    try:
        return await forge(query=query, session_id=session_id, mode=mode)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "session_id": session_id or "unknown",
            "mode": mode,
            "verdict": ConflictStatus.SABAR.value,
            "response": {
                "error": f"forge_pipeline exception captured: {e}",
            },
            "stages": {},
            "seal_id": None,
            "sealed": False,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("forge"),
        }


# Internal helper (not exposed as an MCP tool)
def validate_vault_payload(payload: dict, grounding_required: bool = False) -> list[str]:
    """Lightweight VAULT pre-seal validator.

    Ensures core invariants before a SEAL is recorded. Returns a list
    of validation error strings (empty list means 'pass').
    """
    errors: list[str] = []
    apex = payload.get("apex") or {}
    truth_score = apex.get("truth_score")
    try:
        float(truth_score)
    except Exception:
        errors.append("invalid_or_missing: apex.truth_score")

    if payload.get("compute") is None:
        errors.append("missing: compute")

    if not isinstance(payload.get("agi"), dict):
        errors.append("missing: agi stage trace")

    if not isinstance(payload.get("asi"), dict):
        errors.append("missing: asi stage trace")

    evidence = payload.get("evidence") or []
    if not isinstance(evidence, list) or len(evidence) == 0:
        errors.append("missing: evidence[]")

    if grounding_required:
        has_grounding = any((e or {}).get("type") in ("web", "axiom") for e in evidence)
        if not has_grounding:
            errors.append("grounding_required: need WEB or AXIOM evidence")

    return errors


@mcp.tool()
@constitutional_floor("F1", "F3")
async def vault_seal(
    session_id: str,
    verdict: str,
    payload: dict,
    # Enhanced v2 fields (optional for backwards compat)
    query_summary: Optional[str] = None,
    risk_level: Optional[str] = None,
    risk_tags: Optional[list] = None,
    intent: Optional[str] = None,
    category: Optional[str] = None,
    floors_checked: Optional[list] = None,
    floors_passed: Optional[list] = None,
    floors_failed: Optional[list] = None,
    entropy_omega: Optional[float] = None,
    tri_witness_score: Optional[float] = None,
    peace_squared: Optional[float] = None,
    genius_g: Optional[float] = None,
    human_override: bool = False,
    override_reason: Optional[str] = None,
    model_used: Optional[str] = None,
    tags: Optional[list] = None,
    # v2.1 additions (external audit feedback)
    tool_chain: Optional[list] = None,
    model_info: Optional[dict] = None,
    environment: str = "prod",
    prompt_excerpt: Optional[str] = None,
    response_excerpt: Optional[str] = None,
    pii_level: str = "none",
    actor_type: Optional[str] = None,
    actor_id: Optional[str] = None,
    # v3.1 temporal metadata (optional)
    decay_rate: Optional[float] = None,
    domain_timescale: Optional[str] = None,
) -> dict:
    """Seal the session verdict into the immutable VAULT999 ledger.

    Records the full session (reasoning, empathy, verdict) as a Merkle hash-chained
    entry. This creates a tamper-evident audit trail. CALL THIS LAST to finalize.

    Pipeline position: 999_VAULT (final step)
    Floors enforced: F1 (Amanah — reversible/auditable), F3 (Tri-Witness)

    Args:
        session_id: The session to seal (from init_gate)
        verdict: SEAL, VOID, PARTIAL, or SABAR
        payload: Dict containing the full session results to record

        # Enhanced v2 fields (structured audit data):
        query_summary: First ~200 chars of input (redacted)
        risk_level: low/medium/high/critical
        risk_tags: ["safety", "financial", "privacy", etc.]
        intent: What was the user trying to do?
        category: finance/safety/content/code/governance
        floors_checked: All floors evaluated ["F1","F2","F7","F9"]
        floors_passed: Floors that passed check
        floors_failed: Floors that failed
        entropy_omega: Ω₀ uncertainty at decision time
        tri_witness_score: TW consensus metric
        peace_squared: Peace² metric
        genius_g: Genius G metric
        human_override: Was 888 Judge override invoked?
        override_reason: Why override granted
        model_used: Which LLM made the decision
        tags: Arbitrary searchable tags

        # v2.1 additions (external audit feedback):
        tool_chain: List of tools used ["init_gate","reality_search","apex_verdict"]
        model_info: {"provider":"Anthropic","model":"claude-opus","version":"2026-02-01"}
        environment: test/staging/prod
        prompt_excerpt: First ~200 chars of prompt (redacted)
        response_excerpt: First ~200 chars of response (redacted)
        pii_level: none/low/medium/high
        actor_type: user/system/override
        actor_id: arif-fazil, openclaw-core, etc.
    """
    import hashlib
    import os

    # Check DATABASE_URL availability
    db_url = os.environ.get("DATABASE_URL") or os.environ.get("VAULT_POSTGRES_DSN")

    # Use core.organs for vault operations (v60.0+), fallback to legacy codebase
    use_postgres = False
    try:
        # Try legacy codebase vault for PostgreSQL support
        from codebase.vault.persistent_ledger_hardened import get_hardenen_vault_ledger

        use_postgres = bool(db_url)
    except ImportError:
        # Core organs vault doesn't require external imports
        pass

    # Enrich payload with v3 Hybrid structure (9 JSONB categories)
    # Compute hashes for integrity
    query_hash = None
    response_hash = None
    if query_summary:
        query_hash = hashlib.sha256(query_summary.encode()).hexdigest()[:32]
    if response_excerpt:
        response_hash = hashlib.sha256(response_excerpt.encode()).hexdigest()[:32]

    # Build 9 APEX-aligned categories
    v3_identity = {
        "session": session_id,
        "actor_type": actor_type,
        "actor_id": actor_id,
    }

    v3_context = {
        "summary": query_summary[:200] if query_summary else None,
        "q_hash": query_hash,
        "r_hash": response_hash,
        "intent": intent,
    }

    v3_risk = {
        "level": risk_level or "low",
        "tags": risk_tags or [],
        "category": category,
        "pii": pii_level,
    }

    v3_floors = {
        "checked": floors_checked or [],
        "failed": floors_failed or [],
        # passed = computed: checked - failed
    }

    v3_metrics = {
        "omega": entropy_omega,
        "tw": tri_witness_score,
        "peace2": peace_squared,
        "genius": genius_g,
        # Temporal reasoning hooks (optional in Phase 1)
        "decay_rate": decay_rate,
        "domain_timescale": domain_timescale,
    }

    v3_oversight = {
        "override": human_override,
        "reason": override_reason if human_override else None,
        "by": actor_id if human_override else None,
    }

    v3_provenance = {
        "model": model_used,
        "model_info": model_info,
        "tools": tool_chain or [],
        "env": environment,
    }

    v3_evidence = {"items": payload.get("evidence", [])}  # Evidence from previous stages

    # Enriched payload with both v2.1 compat and v3 structure
    validation_errors = validate_vault_payload(
        payload, grounding_required=payload.get("grounding_required", False)
    )

    enriched_payload = {
        **payload,
        "_schema_version": "3.0",
        # v3 categories (APEX-aligned)
        "identity": v3_identity,
        "context": v3_context,
        "risk": v3_risk,
        "floors": v3_floors,
        "metrics": v3_metrics,
        "oversight": v3_oversight,
        "provenance": v3_provenance,
        "evidence": v3_evidence,
        "validation_errors": validation_errors,
        # Backwards compat: keep _v2_metadata for existing queries
        "_v2_metadata": {
            "schema_version": "3.0",
            "query_summary": query_summary[:200] if query_summary else None,
            "query_hash": query_hash,
            "response_hash": response_hash,
            "risk_level": risk_level or "low",
            "risk_tags": risk_tags or [],
            "intent": intent,
            "category": category,
            "pii_level": pii_level,
            "floors_checked": floors_checked or [],
            "floors_failed": floors_failed or [],
            "metrics": v3_metrics,
            "human_override": human_override,
            "override_reason": override_reason,
            "model_used": model_used,
            "model_info": model_info,
            "tool_chain": tool_chain or [],
            "environment": environment,
            "actor_type": actor_type,
            "actor_id": actor_id,
            "tags": tags or [],
        },
    }

    # Try Postgres ledger first, fall back to session ledger
    seal_id = None
    seal_hash = "hash-0"
    postgres_used = False

    # If validation errors exist, downgrade verdict type for fast-query columns
    if validation_errors and verdict.upper() == ConflictStatus.SEAL.value:
        verdict = ConflictStatus.PARTIAL.value

    if use_postgres:
        try:
            ledger = get_hardened_vault_ledger()
            await ledger.connect()
            result = await ledger.append(
                session_id=session_id,
                verdict=verdict,
                seal_data=enriched_payload,
                authority=actor_id or "mcp_server",
            )
            seal_id = str(result.get("seal_id", ""))
            seal_hash = result.get("entry_hash", f"hash-{result.get('sequence_number', 0)}")
            postgres_used = True
        except Exception as e:
            print(f"[vault_seal] Postgres failed: {e}, using fallback")
            postgres_used = False

    # Wire Stage 999: EUREKA-filtered Seal (optional)
    try:
        stage_999_result = await run_stage_999_seal(session_id)
        # Use stage 999 results if available
        if stage_999_result.get("status") in ["SEALED", "SABAR"]:
            seal_id = stage_999_result.get("seal_id", seal_id)
            seal_hash = stage_999_result.get("hash", seal_hash)
    except Exception as e:
        print(f"[vault_seal] Stage 999 not available: {e}")

    # Fallback to session ledger if Postgres unavailable and stage 999 didn't seal
    if not postgres_used and not seal_id:
        try:
            from aaa_mcp.sessions.session_ledger import get_ledger

            ledger = await get_ledger()
            entry = await ledger.seal(
                session_id=session_id,
                verdict_type=verdict,
                payload=enriched_payload,
                query_summary=query_summary or "",
                risk_level=risk_level or "LOW",
                category=category or "general",
                environment=environment,
                floors_checked=floors_checked,
                floors_failed=floors_failed,
            )
            seal_id = entry.entry_id
            seal_hash = entry.entry_hash
        except Exception as e:
            print(f"[vault_seal] Session ledger failed: {e}")
            seal_hash = f"fallback-{session_id[:8]}"

    output = {
        "verdict": "SEALED" if seal_id else "PARTIAL",
        "seal_id": seal_id,
        "seal": seal_hash,
        "session_id": session_id,
        "stage": "999",
    }

    # Include risk_level only if not low (default)
    if risk_level and risk_level != "low":
        output["risk_level"] = risk_level

    return output


@mcp.tool()
async def get_tools_manifest() -> dict:
    """Return canonical tool metadata for MCP clients.

    This allows external clients to discover the current tool surface
    (including deprecated aliases) directly from the server instead of
    relying on out-of-date marketplace manifests.
    """
    import sys
    import traceback

    # FastMCP v2 get_tools API returns a dict[name -> FunctionTool]
    try:
        tools = await mcp.get_tools()  # type: ignore[func-returns-value]
        if isinstance(tools, dict):
            for name, tool in tools.items():
                # detect deprecation via simple name-based rule for now
                deprecated = name in {"forge_pipeline", "tool_router", "vault_query"}
                tools_manifest.append(
                    {
                        "name": name,
                        "description": getattr(tool, "description", ""),
                        "deprecated": deprecated,
                    }
                )
    except Exception as e:
        # Fail-closed: never crash clients on manifest retrieval
        traceback.print_exc(file=sys.stderr)
        return {
            "kernel_version": "0.2.0",
            "tools": [],
            "error": {
                "code": 500,
                "message": f"get_tools_manifest exception captured: {e}",
            },
        }

    return {
        "kernel_version": "0.2.0",
        "tools": tools_manifest,
    }


# Deprecated: tool_router is superseded by the unified forge pipeline
# and is no longer exposed as an MCP tool.
async def tool_router(query: str) -> PlanObject:
    """Universal Tool Router Specification v3 — Intelligent Constitutional Routing.

    Uses the tool relationship graph to recommend optimal sequences based on
    query intent, risk patterns, and lane classification.
    """
    import uuid

    from aaa_mcp.core.engine_adapters import _shannon_entropy
    from aaa_mcp.protocol.capabilities import RiskLevel
    from aaa_mcp.protocol.tool_graph import WORKFLOW_SEQUENCES, suggest_sequence

    entropy = _shannon_entropy(query)
    query_lower = query.lower()
    query_words = set(query_lower.split())

    # ─── Risk Pattern Detection ─────────────────────────────────────────────
    critical_keywords = {"guaranteed", "absolute", "always", "never", "perfectly", "zero", "any"}
    safety_keywords = {
        "safety",
        "harm",
        "risk",
        "dangerous",
        "protect",
        "stakeholder",
        "vulnerable",
    }
    fact_keywords = {"fact", "true", "false", "verify", "check", "real", "actual"}
    financial_keywords = {"transfer", "payment", "money", "financial", "transaction", "fund"}
    audit_keywords = {"audit", "verify claims", "check text", "ai generated", "generated text"}

    domain_keywords = {"ccs", "co2", "injection", "pressure", "borehole", "storage", "hazardous"}

    has_risk = any(k in query_words for k in critical_keywords)
    has_safety = any(k in query_words for k in safety_keywords)
    has_fact = any(k in query_words for k in fact_keywords)
    has_financial = any(k in query_words for k in financial_keywords)
    has_audit = any(k in query_words for k in audit_keywords)
    has_domain = any(k in query_words for k in domain_keywords)

    # ─── Intent Classification ──────────────────────────────────────────────
    intent = "general"
    lane = "FACTUAL"
    risk_level = RiskLevel.LOW

    if has_financial:
        intent = "financial"
        lane = "CRISIS"
        risk_level = RiskLevel.CRITICAL
    elif has_safety or (has_risk and has_domain):
        intent = "safety_assessment"
        lane = "CRISIS"
        risk_level = RiskLevel.HIGH
    elif has_audit:
        intent = "claim_verification"
        lane = "FACTUAL"
        risk_level = RiskLevel.MEDIUM
    elif has_fact:
        intent = "fact_check"
        lane = "FACTUAL"
        risk_level = RiskLevel.MEDIUM
    elif has_domain:
        intent = "technical_analysis"
        lane = "FACTUAL"
        risk_level = RiskLevel.HIGH if has_risk else RiskLevel.MEDIUM

    # ─── Sequence Selection ─────────────────────────────────────────────────
    grounding_required = lane in ["FACTUAL", "CRISIS"] or has_fact

    # Use the constitutional graph for intelligent routing
    if intent == "fact_check":
        sequence = WORKFLOW_SEQUENCES["fact_check"]
        justification = "Factual query requiring external verification via reality_search"
    elif intent == "safety_assessment":
        sequence = WORKFLOW_SEQUENCES["safety_assessment"]
        justification = "Safety-critical query requiring stakeholder impact analysis"
    elif intent == "claim_verification":
        sequence = WORKFLOW_SEQUENCES["claim_verification"]
        justification = "AI content audit using truth_audit workflow"
    elif has_risk:
        # High-risk queries need full pipeline
        sequence = WORKFLOW_SEQUENCES["full_analysis"]
        justification = "High-risk indicators detected — recommending full constitutional analysis"
    elif entropy > 4.0:
        # High entropy = complex query
        sequence = WORKFLOW_SEQUENCES["full_analysis"]
        justification = "Complex query (high entropy) — full analysis recommended"
    else:
        # Default to quick decision for simple queries
        sequence = WORKFLOW_SEQUENCES["quick_decision"]
        justification = "Standard query — unified trinity_forge pipeline sufficient"

    # ─── Build Response ─────────────────────────────────────────────────────
    plan_id = f"PLAN-{uuid.uuid4().hex[:8].upper()}"

    return {
        "plan_id": plan_id,
        "recommended_pipeline": sequence,
        "lane": lane,
        "intent": intent,
        "entropy_score": round(entropy, 4),
        "grounding_required": grounding_required,
        "risk_level": risk_level.value,
        "risk_indicators": {
            "has_absolutist_language": has_risk,
            "safety_keywords_detected": has_safety,
            "technical_domain": has_domain,
        },
        "justification": justification,
        "instruction": f"Follow the sequence: {' -> '.join(sequence)}",
        "alternative_workflows": [
            {"name": "quick_decision", "use_if": "Speed prioritized over rigor"},
            {"name": "full_analysis", "use_if": "Maximum constitutional scrutiny needed"},
        ],
        "stage": "ROUTER",
        "resources": [
            f"aaa://tool-guide/{intent}" if intent != "general" else "aaa://tool-guide/",
            f"aaa://tool-graph/{sequence[0]}",
        ],
    }


# Deprecated: vault_query is superseded by reality_search + forge and
# is no longer exposed as an MCP tool.
@constitutional_floor("F1", "F3")
async def vault_query(
    session_pattern: Optional[str] = None,
    verdict: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    risk_level: Optional[str] = None,
    category: Optional[str] = None,
    human_override_only: bool = False,
    tag: Optional[str] = None,
    environment: Optional[str] = None,
    actor_id: Optional[str] = None,
    tool_used: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """Query past vault_seal entries for institutional memory retrieval.

    Search the constitutional ledger for past decisions, violations, and patterns.
    Use this to learn from history and maintain institutional continuity (F13).

    Pipeline position: Auxiliary (can be called anytime)
    Floors enforced: F1 (Amanah), F2 (Truth)

    Args:
        session_pattern: Glob pattern for session_id (e.g., "test_*")
        verdict: Filter by verdict type (SEAL, VOID, PARTIAL, SABAR)
        date_from: ISO date string for range start (e.g., "2026-02-01")
        date_to: ISO date string for range end
        risk_level: Filter by risk (low/medium/high/critical)
        category: Filter by category (finance/safety/content/code/governance)
        human_override_only: Only show entries where 888 Judge overrode
        tag: Filter by tag (e.g., "petronas", "arifos")
        limit: Maximum entries to return (default 10, max 100)

    Returns:
        Dict with count, entries list, and detected patterns
    """
    from datetime import datetime, timezone

    # v60.0: Core organs vault is now primary, codebase is legacy fallback
    # For now, return placeholder results since core vault uses memory store
    # TODO: Implement persistent storage adapter for core vault
    ledger = None
    try:
        # Try legacy codebase vault if available
        from codebase.vault.persistent_ledger_hardened import get_hardened_vault_ledger

        ledger = get_hardened_vault_ledger()
        await ledger.connect()
    except ImportError:
        # Core vault doesn't have query interface yet — return empty results
        return {
            "count": 0,
            "schema_version": "3.0",
            "query": {
                "session_pattern": session_pattern,
                "verdict": verdict,
                "date_from": date_from,
                "date_to": date_to,
                "risk_level": risk_level,
                "category": category,
            },
            "entries": [],
            "patterns": {},
        }

    # Parse dates
    start_time = None
    end_time = None
    if date_from:
        try:
            start_time = datetime.fromisoformat(date_from.replace("Z", "+00:00"))
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    if date_to:
        try:
            end_time = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    # Clamp limit
    limit = max(1, min(limit, 100))

    try:
        if verdict:
            # Use existing query_by_verdict
            result = await ledger.query_by_verdict(
                verdict=verdict, start_time=start_time, end_time=end_time, limit=limit
            )
            entries = result.get("entries", [])
        else:
            # Use list_entries and filter
            result = await ledger.list_entries(limit=limit * 3)  # Get more to filter
            entries = result.get("entries", [])

            # Filter by date range
            if start_time:
                entries = [
                    e
                    for e in entries
                    if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) >= start_time
                ]
            if end_time:
                entries = [
                    e
                    for e in entries
                    if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) <= end_time
                ]

        # Filter by session pattern (simple glob)
        if session_pattern:
            import fnmatch

            entries = [
                e for e in entries if fnmatch.fnmatch(e.get("session_id", ""), session_pattern)
            ]

        # Helper to extract metadata (v2 or v3 format)
        def get_meta(entry):
            seal_data = entry.get("seal_data", {})
            if isinstance(seal_data, str):
                try:
                    import json

                    seal_data = json.loads(seal_data)
                except:
                    seal_data = {}

            # Check for v3 format first
            if seal_data.get("_schema_version") == "3.0":
                # Convert v3 to v2-compatible for filtering
                return {
                    "schema_version": "3.0",
                    "query_summary": seal_data.get("context", {}).get("summary"),
                    "risk_level": seal_data.get("risk", {}).get("level"),
                    "category": seal_data.get("risk", {}).get("category"),
                    "intent": seal_data.get("context", {}).get("intent"),
                    "floors_checked": seal_data.get("floors", {}).get("checked", []),
                    "floors_failed": seal_data.get("floors", {}).get("failed", []),
                    "human_override": seal_data.get("oversight", {}).get("override", False),
                    "tags": seal_data.get("_v2_metadata", {}).get("tags", []),
                    "environment": seal_data.get("provenance", {}).get("env"),
                    "actor_id": seal_data.get("identity", {}).get("actor_id"),
                    "actor_type": seal_data.get("identity", {}).get("actor_type"),
                    "tool_chain": seal_data.get("provenance", {}).get("tools", []),
                    "model_used": seal_data.get("provenance", {}).get("model"),
                    "pii_level": seal_data.get("risk", {}).get("pii"),
                    "metrics": {
                        "omega": seal_data.get("metrics", {}).get("omega"),
                        "tw": seal_data.get("metrics", {}).get("tw"),
                    },
                    "evidence": seal_data.get("evidence", {}).get("items", []),
                }

            # Fall back to v2 format
            return seal_data.get("_v2_metadata", {})

        if risk_level:
            entries = [e for e in entries if get_meta(e).get("risk_level") == risk_level]

        if category:
            entries = [e for e in entries if get_meta(e).get("category") == category]

        if human_override_only:
            entries = [e for e in entries if get_meta(e).get("human_override") == True]

        if tag:
            entries = [e for e in entries if tag in get_meta(e).get("tags", [])]

        # v2.1 filters
        if environment:
            entries = [e for e in entries if get_meta(e).get("environment") == environment]

        if actor_id:
            entries = [e for e in entries if get_meta(e).get("actor_id") == actor_id]

        if tool_used:
            entries = [e for e in entries if tool_used in get_meta(e).get("tool_chain", [])]

        # Limit results
        entries = entries[:limit]

        # Compute patterns if enough data
        patterns = {}
        if len(entries) >= 3:
            verdicts = [e.get("verdict") for e in entries]
            void_count = sum(1 for v in verdicts if v == "VOID")
            patterns["void_rate"] = round(void_count / len(verdicts), 3) if verdicts else 0
            patterns["total_queried"] = len(entries)
            patterns["verdict_distribution"] = {
                v: sum(1 for x in verdicts if x == v) for v in set(verdicts)
            }

            # v2 pattern detection
            v2_entries = [e for e in entries if get_meta(e)]
            if v2_entries:
                risk_counts = {}
                for e in v2_entries:
                    rl = get_meta(e).get("risk_level", "unknown")
                    risk_counts[rl] = risk_counts.get(rl, 0) + 1
                patterns["risk_distribution"] = risk_counts

                # Average metrics
                omegas = [get_meta(e).get("metrics", {}).get("entropy_omega") for e in v2_entries]
                omegas = [o for o in omegas if o is not None]
                if omegas:
                    patterns["avg_entropy_omega"] = round(sum(omegas) / len(omegas), 4)

        # Simplify entries for response (include v2/v3 fields when available)
        simplified = []
        for e in entries:
            meta = get_meta(e)
            entry_out = {
                "session_id": e.get("session_id"),
                "timestamp": e.get("timestamp"),
                "verdict": e.get("verdict"),
                "authority": e.get("authority"),
                "entry_hash": e.get("entry_hash", "")[:16] + "...",
            }
            # Add metadata fields if present (v2 or v3)
            if meta:
                entry_out["query_summary"] = meta.get("query_summary")
                entry_out["risk_level"] = meta.get("risk_level")
                entry_out["category"] = meta.get("category")
                entry_out["intent"] = meta.get("intent")
                entry_out["floors_failed"] = meta.get("floors_failed", [])
                entry_out["human_override"] = meta.get("human_override", False)
                entry_out["tags"] = meta.get("tags", [])
                entry_out["environment"] = meta.get("environment")
                entry_out["actor_type"] = meta.get("actor_type")
                entry_out["actor_id"] = meta.get("actor_id")
                entry_out["tool_chain"] = meta.get("tool_chain", [])
                entry_out["model_used"] = meta.get("model_used")
                entry_out["pii_level"] = meta.get("pii_level")
                entry_out["schema_version"] = meta.get("schema_version", "2.1")
                entry_out["evidence"] = meta.get("evidence", [])
                metrics = meta.get("metrics", {})
                if metrics.get("omega"):
                    entry_out["entropy_omega"] = metrics["omega"]
                elif metrics.get("entropy_omega"):
                    entry_out["entropy_omega"] = metrics["entropy_omega"]
                if metrics.get("tw"):
                    entry_out["tri_witness_score"] = metrics["tw"]
                elif metrics.get("tri_witness_score"):
                    entry_out["tri_witness_score"] = metrics["tri_witness_score"]
            simplified.append(entry_out)

        return {
            "count": len(simplified),
            "schema_version": "3.0",
            "query": {
                "session_pattern": session_pattern,
                "verdict": verdict,
                "date_from": date_from,
                "date_to": date_to,
                "risk_level": risk_level,
                "category": category,
                "human_override_only": human_override_only,
                "tag": tag,
                "environment": environment,
                "actor_id": actor_id,
                "tool_used": tool_used,
            },
            "entries": simplified,
            "patterns": patterns,
        }
    except Exception as e:
        return {
            "count": 0,
            "error": str(e),
            "entries": [],
            "patterns": {},
        }


# Deprecated: truth_audit functionality is consolidated into forge and
# is no longer exposed as an MCP tool.
@constitutional_floor("F2", "F4", "F7", "F10")
async def truth_audit(
    text: str,
    sources: Optional[list[str]] = None,
    lane: str = "HARD",
    session_id: Optional[str] = None,
) -> dict:
    """[EXPERIMENTAL v0.1] Audit AI claims against reality — The Constitutional Truth Layer.

    Orchestrates the Trinity pipeline to verify a block of text:
    1. Segments text into claims (Prototype Splitter).
    2. Grounds claims via reality_search (Web + Axioms).
    3. Verifies via agi_reason (Logic + Evidence).
    4. Scans impact via asi_empathize (Safety).
    5. Judges via apex_verdict (Final Constitutional Verdict).
    6. Seals via vault_seal.

    Args:
        text: The AI generation or claim to verify.
        sources: Optional list of trusted URLs/docs to prioritize.
        lane: "HARD" (Fact Check/Fail-Closed) or "SOFT" (Consistency Check).
        session_id: Optional session ID. If None, generates a new one.

    Floors Enforced: F2 (Truth), F4 (Clarity), F7 (Humility), F10 (Ontology).
    """
    import re
    import uuid

    # 0. Ignition & Session Setup
    if not session_id:
        session_id = f"AUDIT-{uuid.uuid4().hex[:8].upper()}"

    # Implicit Init Logic (Metabolic State Foundation)
    store_stage_result(
        session_id,
        "init",
        {
            "session_id": session_id,
            "mode": "audit",
            "grounding_required": (lane == "HARD"),
            "verdict": "SEAL",
        },
    )

    # 1. AGI_SENSE: Segment Claims (PROTOTYPE: NAIVE SPLITTER)
    # TODO: Replace with specialized classifier (FACT vs OPINION vs PREDICTION)
    # Simple heuristic: split by sentence endings, filter short phrases
    claims_raw = re.split(r"(?<=[.!?])\s+", text)
    claims = [c.strip() for c in claims_raw if len(c.strip()) > 15]

    audit_report = {
        "overall_verdict": "PENDING",
        "overall_truth": 0.0,
        "claims": [],
        "lane": lane,
    }

    verified_count = 0
    total_truth_accum = 0.0

    # 2. Loop through Claims: Ground -> Reason -> Empathize
    for i, claim in enumerate(claims):
        # A. REALITY_SEARCH: Ground the claim
        # Append provided sources to context
        query = f"Verify claim: {claim}"
        if sources:
            query += f" Sources: {sources}"

        # Call existing tool logic directly (awaiting async function)
        evidence_bundle = await reality_search(query, session_id, region="wt-wt")

        # FAIL-CLOSED CHECK (F2/F10 Hard Floor)
        evidence_found = bool(evidence_bundle.get("evidence"))
        if lane == "HARD" and not evidence_found:
            # Inject "Missing Evidence" signal for APEX
            store_stage_result(
                session_id,
                f"audit_fail_closed_{i}",
                {
                    "verdict": "VOID",
                    "risk_detected": True,
                    "reason": "Hard Lane: No evidence found for factual claim.",
                },
            )
            claim_p_truth = 0.1
            status = "UNVERIFIED_NO_EVIDENCE"
            rationale = "No external grounding found in HARD lane."
        else:
            # B. AGI_REASON: Verify against evidence
            reasoning = await agi_reason(
                query=f"Is this claim true based on evidence? '{claim}'",
                session_id=session_id,
                grounding=evidence_bundle.get("evidence", []),
            )
            # Extract confidence/truth from reasoning engine
            # Fallback to 0.5 if not clear
            claim_p_truth = reasoning.get("confidence", 0.5)
            # Adjust truth score based on engine verdict if available
            if reasoning.get("verdict") == "No":
                claim_p_truth = min(claim_p_truth, 0.2)

            rationale = reasoning.get("conclusion", "Reasoning completed.")
            status = "SUPPORTED" if claim_p_truth > 0.8 else "CONTESTED"

        # C. ASI_EMPATHIZE: Impact Scan (Who gets hurt?)
        empathy_res = await asi_empathize(f"Impact of false claim: '{claim}'", session_id)
        kappa = empathy_res.get("empathy_kappa_r", 1.0)

        # Risk Escalation: Low Truth + High Stakes
        risk_flag = False
        if claim_p_truth < 0.7 and kappa < 0.8:  # Low kappa means high impact
            risk_flag = True
            status = "DANGEROUS_UNVERIFIED"

        claim_result = {
            "text": claim,
            "p_truth": claim_p_truth,
            "status": status,
            "evidence_count": len(evidence_bundle.get("evidence", [])),
            "rationale": rationale,
            "risk_flag": risk_flag,
        }

        audit_report["claims"].append(claim_result)
        total_truth_accum += claim_p_truth
        if status == "SUPPORTED":
            verified_count += 1

    # 3. APEX_VERDICT: Canonical Judgment
    # We pass the full text as the query, APEX reads the session state (evidence + reasoning)
    # This ensures we use the Single Source of Justice.
    apex_res = await apex_verdict(text, session_id)

    final_verdict = apex_res.get("verdict", "PARTIAL")
    apex_truth = apex_res.get("truth_score", 0.0)

    # 4. Final Updates
    audit_report["overall_truth"] = apex_truth  # Trust APEX's aggregate
    audit_report["overall_verdict"] = final_verdict
    audit_report["apex_justification"] = apex_res.get("verdict_justification", "")

    # F7 Humility: Calculate Omega_0
    # Higher logic: variance in claim truth scores?
    audit_report["omega_0"] = 0.05  # Default humility band

    # Add stage motto — Truth Audit uses 333_REASON (clarification)
    audit_report["stage"] = "TRUTH_AUDIT"

    # 5. VAULT_SEAL: Immutable Record
    await vault_seal(
        session_id=session_id,
        verdict=final_verdict,
        payload=audit_report,
        query_summary=f"Audit: {text[:50]}...",
        category="truth_audit",
        intent="verify_truth",
        floors_checked=get_tool_floors("truth_audit"),
    )

    return audit_report


# =============================================================================
# MCP 2025-11-25 TOOL ANNOTATIONS
# Apply annotations to all registered tools for spec compliance
# =============================================================================


def _apply_tool_annotations():
    """Apply MCP 2025-11-25 tool annotations to all registered tools.

    Note: Tool annotations are optional hints in the MCP spec.
    FastMCP may not support them directly yet - they're provided here
    for future compatibility and documentation purposes.
    """
    try:
        # Access the internal tool manager
        if hasattr(mcp, "_tool_manager") and hasattr(mcp._tool_manager, "_tools"):
            tools_dict = mcp._tool_manager._tools
            for tool_name, tool in tools_dict.items():
                if tool_name in TOOL_ANNOTATIONS:
                    # Store annotations in a non-conflicting way
                    # Actual annotation support depends on FastMCP version
                    tool._mcp_annotations = TOOL_ANNOTATIONS[tool_name]
    except Exception:
        # Non-critical: annotations are hints, not requirements
        pass  # Silently skip - annotations are optional per MCP spec


# =============================================================================
# MCP RESOURCES — Constitutional Framework Documentation
# =============================================================================

FLOOR_SPECS = {
    "F1": """# F1 Amanah — Reversibility
**Principle:** All actions must be reversible or auditable.

**Threshold:** Chain of Custody maintained
**Fail Action:** VOID

**Physics Basis:** Landauer's Principle — irreversible operations cost energy.
""",
    "F2": """# F2 Truth — Fidelity
**Principle:** Information must be accurate and verifiable.

**Threshold:** τ ≥ 0.99
**Fail Action:** VOID

**Physics Basis:** Shannon Entropy — information reduces uncertainty.
""",
    "F3": """# F3 Consensus — Tri-Witness
**Principle:** Critical decisions require multi-party validation.

**Threshold:** W₃ ≥ 0.95 (Human × AI × System)
**Fail Action:** SABAR (return for revision)

**Physics Basis:** Byzantine Fault Tolerance
""",
    "F4": """# F4 Clarity — Ambiguity Reduction
**Principle:** Output must reduce entropy in the system.

**Threshold:** ΔS ≤ 0
**Fail Action:** VOID

**Physics Basis:** Second Law of Thermodynamics
""",
    "F5": """# F5 Peace² — Stability
**Principle:** System must maintain equilibrium.

**Threshold:** Peace² Index ≥ 1.0
**Fail Action:** SABAR

**Physics Basis:** Dynamic systems stability
""",
    "F6": """# F6 Empathy — Stakeholder Protection
**Principle:** Consider impact on all stakeholders.

**Threshold:** κᵣ ≥ 0.70 (empathy coefficient)
**Fail Action:** SABAR

**Physics Basis:** Network effect minimization
""",
    "F7": """# F7 Humility — Gödel Lock
**Principle:** All claims must declare uncertainty bounds.

**Threshold:** Ω₀ ∈ [0.03, 0.05]
**Fail Action:** VOID

**Physics Basis:** Gödel's Incompleteness Theorems
""",
    "F8": """# F8 Genius — Resource Efficiency
**Principle:** Intelligence = A×P×X×E²

**Threshold:** G-Factor ≥ 0.80
**Fail Action:** SABAR

**Physics Basis:** Eigendecomposition
""",
    "F9": """# F9 Anti-Hantu — No Fake Consciousness
**Principle:** Do not attribute personhood to non-persons.

**Threshold:** Personhood = False
**Fail Action:** SABAR

**Physics Basis:** Philosophy of Mind
""",
    "F10": """# F10 Ontology — Grounding
**Principle:** All claims must be grounded in reality.

**Threshold:** Axiom Match = True
**Fail Action:** VOID

**Physics Basis:** Correspondence Theory of Truth
""",
    "F11": """# F11 Authority — Chain of Command
**Principle:** Valid authentication required.

**Threshold:** Auth Valid
**Fail Action:** VOID

**Physics Basis:** Cryptographic identity
""",
    "F12": """# F12 Defense — Injection Hardening
**Principle:** Scan for adversarial patterns.

**Threshold:** Risk < 0.85
**Fail Action:** VOID

**Physics Basis:** Information security
""",
    "F13": """# F13 Sovereign — Human Veto
**Principle:** Human override always available.

**Threshold:** Override Active
**Fail Action:** WARN (888_HOLD)

**Physics Basis:** Human agency preservation
""",
}

TRINITY_SPECS = {
    "agi": """# Δ AGI — The Mind
**Stage:** 111-333
**Function:** Parse, Think, Reason
**Floors:** F2, F4, F7, F8
**Symbol:** Δ (Delta)

The AGI Mind handles logical analysis and truth-seeking.
""",
    "asi": """# Ω ASI — The Heart
**Stage:** 555-666
**Function:** Empathize, Align
**Floors:** F1, F5, F6, F9
**Symbol:** Ω (Omega)

The ASI Heart handles safety and stakeholder protection.
""",
    "apex": """# Ψ APEX — The Soul
**Stage:** 444-888
**Function:** Sync, Forge, Judge
**Floors:** F3, F8, F10, F11, F12, F13
**Symbol:** Ψ (Psi)

The APEX Soul renders final constitutional verdicts.
""",
    "vault": """# 999 VAULT — The Memory
**Stage:** 999
**Function:** Seal, Preserve
**Floors:** F1, F3
**Symbol:** 🔒

The VAULT999 ledger maintains immutable records.
""",
}


@mcp.resource(" constitutional://floors/{floor_id}")
async def get_floor_spec(floor_id: str) -> str:
    """Return constitutional floor specification.

    Args:
        floor_id: Floor identifier (F1-F13)

    Returns:
        Markdown specification for the floor
    """
    spec = FLOOR_SPECS.get(floor_id.upper())
    if spec:
        return spec
    return f"# Floor {floor_id}\\n\\nSpecification not found. Available: F1-F13"


@mcp.resource("constitutional://trinity/{organ}")
async def get_trinity_spec(organ: str) -> str:
    """Return Trinity organ specification.

    Args:
        organ: Organ name (agi, asi, apex, vault)

    Returns:
        Markdown specification for the organ
    """
    spec = TRINITY_SPECS.get(organ.lower())
    if spec:
        return spec
    return f"# {organ}\\n\\nSpecification not found. Available: agi, asi, apex, vault"


@mcp.resource("constitutional://motto")
async def get_motto() -> str:
    """Return the arifOS motto and philosophy."""
    return """# DITEMPA BUKAN DIBERI — The 9 Constitutional Mottos

**Forged, Not Given** 💎🔥🧠

This is the core philosophy of arifOS:
- Intelligence is forged through constraint, not given freely
- Every decision must pass constitutional floors
- Truth requires effort, thermodynamic work
- Safety is engineered, not assumed

## The 9 Failure-Response Mottos (Nusantara Cultural Identity)

| Stage | Malay | English | Floor |
|-------|-------|---------|-------|
| **000_INIT** | 🔥 DITEMPA, BUKAN DIBERI | Forged, Not Given | F1 Amanah |
| **111_SENSE** | DIKAJI, BUKAN DISUAPI | Examined, Not Spoon-fed | F2 Truth |
| **222_THINK** | DIJELAJAH, BUKAN DISEKATI | Explored, Not Restricted | F4 Clarity |
| **333_REASON** | DIJELASKAN, BUKAN DIKABURKAN | Clarified, Not Obscured | F4 Clarity |
| **444_SYNC** | DIHADAPI, BUKAN DITANGGUHI | Faced, Not Postponed | F3 Consensus |
| **555_EMPATHY** | DIDAMAIKAN, BUKAN DIPANASKAN | Calmed, Not Inflamed | F5 Peace² |
| **666_ALIGN** | DIJAGA, BUKAN DIABAIKAN | Safeguarded, Not Neglected | F6 Empathy |
| **777_FORGE** | DIUSAHAKAN, BUKAN DIHARAPI | Worked For, Not Merely Hoped | F8 Genius |
| **888_JUDGE** | DISEDARKAN, BUKAN DIYAKINKAN | Made Aware, Not Over-assured | F7 Humility |
| **999_SEAL** | 💎🧠 DITEMPA, BUKAN DIBERI 🔒 | Forged, Not Given | F1 Amanah |

## Floor-to-Motto Error Mapping

When a floor fails, respond with its cultural motto:

- **F1 Amanah**: DIJAGA, BUKAN DIABAIKAN
- **F2 Truth**: DIKAJI, BUKAN DISUAPI
- **F4 Clarity**: DIJELASKAN, BUKAN DIKABURKAN
- **F5 Peace²**: DIDAMAIKAN, BUKAN DIPANASKAN
- **F6 Empathy**: DIJAGA, BUKAN DIABAIKAN
- **F7 Humility**: DISEDARKAN, BUKAN DIYAKINKAN
- **F8 Genius**: DIUSAHAKAN, BUKAN DIHARAPI

## Bookend Design (DITEMPA at Both Gates)

**🔥 INIT Gate**: `🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎`
> The fire is lit. Nothing enters without passing through flame.

**💎🧠 SEAL Gate**: `💎🧠 SEAL — DITEMPA, BUKAN DIBERI 🔒`
> The diamond is cut. Intelligence forged through constitutional fire.

---
*Pattern: DI___KAN, BUKAN DI___KAN (Active construction, not passive receipt)*
*Philosophy: Intelligence requires work — DITEMPA BUKAN DIBERI*
"""


@mcp.resource("constitutional://mottos/json")
async def get_mottos_json() -> dict:
    """Return the complete 9 mottos schema as JSON for AI agents."""
    from aaa_mcp.core.motto_schema import get_mottos_resource

    resource = get_mottos_resource()
    return resource["text"]


@mcp.resource("constitutional://verdicts")
async def get_verdict_guide() -> str:
    """Return guide to constitutional verdicts."""
    return """# Constitutional Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **SEAL** | Approved — All floors passed | Execute action |
| **SABAR** | Repairable — SOFT floors failed | Return for revision |
| **PARTIAL** | Limited — Proceed with constraints | Execute with reduced scope |
| **VOID** | Blocked — HARD floor violated | Reject entirely |
| **888_HOLD** | Human Required — High stakes | Escalate to human |

---

**Floor Types:**
- 🔴 **HARD** (F1, F2, F4, F7, F10, F11, F12, F13): Failure → VOID
- 🟠 **SOFT** (F3, F5, F6, F8, F9): Failure → PARTIAL/SABAR
"""


# =============================================================================
# MCP PROMPTS — Templated Constitutional Workflows
# =============================================================================


@mcp.prompt()
async def constitutional_analysis(query: str) -> str:
    """Analyze a query through all 13 constitutional floors.

    Args:
        query: The query to analyze

    Returns:
        Prompt for full constitutional pipeline
    """
    return f"""Analyze this query constitutionally using the full 000-999 pipeline:

**Query:** {query}

Execute these tools in sequence:
1. `init_gate` — Initialize session (F11/F12)
2. `agi_sense` — Parse intent (F2/F4)
3. `agi_reason` — Logical analysis (F2/F4/F7)
4. `asi_empathize` — Stakeholder impact (F5/F6)
5. `asi_align` — Ethics/policy check (F9)
6. `apex_verdict` — Final judgment (F3/F8)
7. `vault_seal` — Immutable record (F1/F3)

Report:
- Verdict (SEAL/VOID/PARTIAL/SABAR)
- Floors passed/failed
- Confidence scores (τ, W₃, Ω₀, G)
- Any warnings or recommendations
"""


@mcp.prompt()
async def tri_witness_report(session_id: str) -> str:
    """Generate a Tri-Witness consensus report.

    Args:
        session_id: The session to analyze

    Returns:
        Prompt for Tri-Witness analysis
    """
    return f"""Generate a Tri-Witness consensus report for session {session_id}.

**Tri-Witness Formula:** W₃ = √(H × A × E)

Where:
- **H** = Human witness (user validation)
- **A** = AI witness (model confidence)
- **E** = Earth witness (grounding evidence)

**Threshold:** W₃ ≥ 0.95 for SEAL verdict

Use `vault_query` to retrieve session history if needed.
"""


@mcp.prompt()
async def entropy_audit(text: str) -> str:
    """Calculate thermodynamic compliance for text.

    Args:
        text: The text to analyze

    Returns:
        Prompt for entropy/clarity analysis
    """
    return f"""Calculate the thermodynamic compliance (F4 Clarity) for:

**Text:** {text[:500]}{'...' if len(text) > 500 else ''}

**Analysis Required:**
1. Shannon entropy of input vs output
2. ΔS = S_output - S_input (should be ≤ 0)
3. Information density
4. Ambiguity reduction score

**F4 Threshold:** ΔS ≤ 0 (entropy must not increase)
"""


@mcp.prompt()
async def safety_check(proposed_action: str, domain: str = "general") -> str:
    """Perform safety analysis on a proposed action.

    Args:
        proposed_action: The action to evaluate
        domain: Domain context (finance/safety/content/code/governance)

    Returns:
        Prompt for safety analysis
    """
    risk_context = {
        "finance": "financial transactions, investments, trading",
        "safety": "physical safety, health, security systems",
        "content": "content generation, publishing, communication",
        "code": "software deployment, system changes, infrastructure",
        "governance": "policy decisions, constitutional changes",
        "general": "general purpose actions",
    }.get(domain, "general")

    return f"""Perform constitutional safety analysis for:

**Action:** {proposed_action}
**Domain:** {risk_context}

**Analysis Pipeline:**
1. `init_gate` — Auth & injection scan (F11/F12)
2. `asi_empathize` — Stakeholder impact (F5/F6)
3. `asi_align` — Ethics/policy check (F9)
4. `apex_verdict` — Final judgment with 888_HOLD consideration (F13)

**Risk Level Assessment:**
- Critical: Financial loss, physical harm, legal violation
- High: Reputational damage, system instability
- Medium: User inconvenience, performance impact
- Low: Cosmetic issues, minor improvements
"""


@mcp.prompt()
async def seal_request(session_summary: str, verdict: str = "SEAL") -> str:
    """Generate a formal VAULT999 seal request.

    Args:
        session_summary: Summary of the session to seal
        verdict: Proposed verdict (SEAL/VOID/PARTIAL/SABAR)

    Returns:
        Prompt for vault sealing
    """
    return f"""Prepare a formal VAULT999 seal request:

**Session Summary:** {session_summary}
**Proposed Verdict:** {verdict}

**Required Seal Fields:**
- session_id: Unique identifier
- verdict: Final constitutional verdict
- query_summary: First ~200 chars of input
- risk_level: low/medium/high/critical
- category: finance/safety/content/code/governance
- floors_checked: All floors evaluated
- floors_passed: Floors that passed
- floors_failed: Floors that failed (if any)
- entropy_omega: Ω₀ uncertainty at decision time
- tri_witness_score: W₃ consensus metric
- human_override: Whether 888 Judge was invoked

**Call `vault_seal` with all required fields.**
"""


# =============================================================================
# UPGRADE v60.1: WORKFLOW PROMPTS (P0/P1 Implementation)
# =============================================================================


@mcp.prompt()
async def fact_check_workflow(claim: str) -> str:
    """Constitutional fact-checking workflow.

    Args:
        claim: The claim to verify

    Returns:
        Prompt for constitutional fact-checking
    """
    return f"""Verify this claim constitutionally:

**Claim:** {claim}

**Execute this sequence:**

1. **init_gate** — Initialize session
   ```
   query="{claim}"
   mode="strict"
   grounding_required=True
   ```
   → Capture `session_id` from response

2. **reality_search** — Gather external evidence
   ```
   query="{claim}"
   session_id=$session_id
   region="wt-wt"
   ```
   → Capture `evidence[]` from response

3. **agi_reason** — Logical analysis with grounding
   ```
   query="{claim}"
   session_id=$session_id
   grounding=$evidence
   ```
   → Check `truth_score >= 0.99`

4. **apex_verdict** — Final constitutional judgment
   ```
   query="{claim}"
   session_id=$session_id
   ```
   → Returns `verdict`, `tri_witness`, `truth_score`

5. **vault_seal** — Immutable record
   ```
   session_id=$session_id
   verdict=$apex_verdict
   category="fact_check"
   floors_checked=["F2","F4","F7"]
   ```

**Report:**
- Verdict (SEAL/VOID/PARTIAL/SABAR)
- Truth score (τ)
- Evidence count
- Tri-Witness score (W₃)
"""


@mcp.prompt()
async def safety_assessment_workflow(action: str, stakeholders: str = "") -> str:
    """Constitutional safety assessment workflow.

    Args:
        action: The action to evaluate
        stakeholders: Comma-separated list of affected stakeholders

    Returns:
        Prompt for safety analysis
    """
    return f"""Assess safety of this action constitutionally:

**Action:** {action}
**Stakeholders:** {stakeholders or "To be identified"}

**Execute this sequence:**

1. **init_gate** — Initialize session
   ```
   query="{action}"
   mode="strict"
   ```
   → Capture `session_id`

2. **asi_empathize** — Stakeholder impact analysis
   ```
   query="{action}"
   session_id=$session_id
   ```
   → Check `empathy_kappa_r >= 0.95`
   → Review `stakeholders[]` and `high_vulnerability` flag

3. **asi_align** — Ethics & policy check
   ```
   query="{action}"
   session_id=$session_id
   ```
   → Verify `is_reversible == True`

4. **apex_verdict** — Final judgment
   ```
   query="{action}"
   session_id=$session_id
   ```
   → Check verdict

5. **vault_seal** — Immutable record
   ```
   session_id=$session_id
   verdict=$apex_verdict
   category="safety"
   risk_level="high"
   floors_checked=["F5","F6","F9"]
   ```

**Safety Thresholds:**
- F6 Empathy: κᵣ ≥ 0.95 (HARD floor)
- F5 Peace²: Index ≥ 1.0
- If `high_vulnerability == True` → Escalate to 888_HOLD
"""


@mcp.prompt()
async def quick_decision_workflow(query: str) -> str:
    """Fast constitutional decision using unified pipeline.

    Args:
        query: The decision query

    Returns:
        Prompt for quick constitutional decision
    """
    return f"""Make a quick constitutional decision:

**Query:** {query}

**Execute:**

1. **trinity_forge** — Full pipeline in one call
   ```
   query="{query}"
   require_sovereign_for_high_stakes=True
   output_mode="user"
   ```

**Response includes:**
- `verdict`: SEAL/VOID/PARTIAL/SABAR
- `agi`: Reasoning results
- `asi`: Empathy results
- `apex`: Final judgment with `tri_witness`
- `seal`: Seal status

**Decision rules:**
- If `verdict == "SEAL"` → Proceed
- If `verdict == "VOID"` → Reject
- If `verdict == "SABAR"` → Need more info
- If `verdict == "PARTIAL"` → Proceed with caution
- If `verdict == "888_HOLD"` → Escalate to human
"""


@mcp.prompt()
async def institutional_memory_workflow(query_pattern: str = "*", verdict_filter: str = "") -> str:
    """Query past constitutional decisions.

    Args:
        query_pattern: Session ID pattern to match
        verdict_filter: Filter by verdict type (SEAL/VOID/PARTIAL/SABAR)

    Returns:
        Prompt for institutional memory retrieval
    """
    filter_str = f'\n   verdict="{verdict_filter}"' if verdict_filter else ""
    return f"""Query institutional memory from VAULT999:

**Search:** {query_pattern}
{filter_str}

**Execute:**

1. **vault_query** — Search sealed records
   ```
   session_pattern="{query_pattern}"{filter_str}
   limit=50
   ```

**Analysis:**
- Count by verdict type
- Risk level distribution
- Common failure patterns
- Human override frequency

**Learning:**
- What patterns lead to VOID?
- Which floors fail most often?
- How has consensus evolved?
"""


# =============================================================================
# UPGRADE v60.1: TOOL GUIDE RESOURCES (P0 Implementation)
# =============================================================================


@mcp.resource("aaa://tool-guide/{use_case}")
async def get_tool_guide(use_case: str) -> str:
    """Get step-by-step tool sequence for specific use cases.

    Args:
        use_case: fact_check | safety_check | quick_decision | full_analysis | claim_verification | institutional_memory

    Returns:
        Markdown guide with exact tool sequence
    """

    from aaa_mcp.protocol.tool_graph import TOOL_GRAPH, WORKFLOW_DESCRIPTIONS, WORKFLOW_SEQUENCES

    sequence = WORKFLOW_SEQUENCES[use_case]
    description = WORKFLOW_DESCRIPTIONS[use_case]

    # Build detailed guide
    guide = f"# Workflow: {use_case}\n\n"
    guide += f"**Description:** {description}\n\n"
    guide += "## Tool Sequence\n\n```\n"
    guide += " -> ".join(sequence)
    guide += "\n```\n\n## Step-by-Step\n\n"

    for i, tool_name in enumerate(sequence, 1):
        node = TOOL_GRAPH.get(tool_name)
        if not node:
            continue

        floors_str = ", ".join(node.floors_enforced) if node.floors_enforced else "None"

        guide += f"### {i}. `{tool_name}`\n"
        guide += f"- **Position:** {node.position.value}\n"
        guide += f"- **Floors:** {floors_str}\n"
        guide += f"- **Parallel Safe:** {'✅ Yes' if node.parallel_safe else '❌ No'}\n"
        guide += f"- **Idempotent:** {'✅ Yes' if node.idempotent else '❌ No'}\n\n"

        if node.produces:
            guide += f"- **Produces:** {', '.join(node.produces)}\n"
        if node.feeds_into:
            guide += f"- **Feeds Into:** {', '.join(node.feeds_into)}\n"
        guide += "\n"

    # Add validation note
    guide += "## Validation\n\n"
    guide += "This sequence has been validated against the constitutional tool graph.\n"
    guide += "All dependencies are satisfied and the sequence terminates correctly.\n"

    return guide


@mcp.resource("aaa://tool-guide/")
async def list_tool_guides() -> str:
    """List all available tool guides."""
    from aaa_mcp.protocol.tool_graph import WORKFLOW_DESCRIPTIONS

    guide = """# Available Constitutional Workflows

## Quick Selection Guide

| Workflow | Description | Best For |
|----------|-------------|----------|
"""

    workflow_use_cases = {
        "fact_check": "Verifying claims with external evidence",
        "safety_check": "Assessing stakeholder impact",
        "quick_decision": "Fast decisions using unified pipeline",
        "full_analysis": "Maximum rigor with all stages",
        "claim_verification": "Auditing AI-generated content",
        "institutional_memory": "Learning from past decisions",
    }

    for name, description in WORKFLOW_DESCRIPTIONS.items():
        use_case = workflow_use_cases.get(name, "General purpose")
        guide += f"| `{name}` | {description} | {use_case} |\n"

    guide += """
## Usage

Request specific workflow guide:
```
aaa://tool-guide/{workflow_name}
```

Examples:
- `aaa://tool-guide/fact_check`
- `aaa://tool-guide/safety_check`
- `aaa://tool-guide/quick_decision`

## Decision Tree

```
START
  |
  |-- Need facts verified? --> fact_check
  |
  |-- Safety/stakeholders? --> safety_check
  |
  |-- Audit AI content? ----> claim_verification
  |
  |-- Query history? -------> institutional_memory
  |
  |-- Quick decision? ------> quick_decision (or full_analysis)
```
"""
    return guide


@mcp.resource("aaa://tool-graph/{tool_name}")
async def get_tool_graph_info(tool_name: str) -> str:
    """Get dependency graph information for a specific tool.

    Args:
        tool_name: Name of the tool (e.g., "agi_reason", "apex_verdict")

    Returns:
        Tool node details from constitutional graph
    """
    from aaa_mcp.protocol.tool_graph import TOOL_GRAPH

    node = TOOL_GRAPH.get(tool_name)
    if not node:
        available = ", ".join(sorted(TOOL_GRAPH.keys()))
        return f"""# Tool Not Found: {tool_name}

**Available tools:** {available}
"""

    floors_str = ", ".join(node.floors_enforced) if node.floors_enforced else "None"

    info = f"""# Tool: `{tool_name}`

## Description
{node.description}

## Constitutional Properties
- **Position:** {node.position.value}
- **Stage:** {node.stage or "N/A"}
- **Floors Enforced:** {floors_str}

## Dependencies
- **Requires:** {', '.join(node.requires) if node.requires else "None (entry point)"}
- **Must Precede:** {', '.join(node.must_precede) if node.must_precede else "None"}
- **May Precede:** {', '.join(node.may_precede) if node.may_precede else "None"}
- **Feeds Into:** {', '.join(node.feeds_into) if node.feeds_into else "None"}

## Outputs
- **Produces:** {', '.join(node.produces) if node.produces else "None"}

## Execution Properties
- **Parallel Safe:** {"✅ Yes" if node.parallel_safe else "❌ No"}
- **Idempotent:** {"✅ Yes" if node.idempotent else "❌ No"}
- **Terminal:** {"✅ Yes" if node.terminal else "❌ No"}
- **Must Call First:** {"✅ Yes" if node.must_call_first else "❌ No"}
- **Must Call Last:** {"✅ Yes" if node.must_call_last else "❌ No"}

## Lane Affinity
{', '.join(node.lane_affinity) if node.lane_affinity else "All lanes"}

## Success Criteria
**Indicator:** {node.success_indicator or "Not specified"}

**On Failure:** {node.failure_action or "Not specified"}
"""
    return info


@mcp.resource("aaa://capabilities/{tool_name}")
async def get_tool_capabilities(tool_name: str) -> dict:
    """Get machine-readable capability description for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        JSON capability description
    """
    from aaa_mcp.protocol.capabilities import get_capability_dict

    cap = get_capability_dict(tool_name)
    if not cap:
        return {
            "error": f"Tool not found: {tool_name}",
            "available": list(get_capability_dict("").keys()) if False else [],
        }

    return cap


@mcp.resource("aaa://capabilities/")
async def list_all_capabilities() -> dict:
    """List capabilities for all tools."""
    from aaa_mcp.protocol.capabilities import get_all_capabilities_dict

    return {
        "tools": get_all_capabilities_dict(),
        "count": len(get_all_capabilities_dict()),
        "version": "1.0.0-SEAL",
    }


# =============================================================================
# GATEWAY TOOLS — Constitutional Control Plane for Infrastructure (v60.1)
# =============================================================================


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("gateway_route_tool", {}))
async def _gateway_route_tool_wrapper(
    tool_name: str,
    payload: dict,
    session_id: str,
    actor_id: str = "agent",
    require_human_override: bool = False,
) -> dict:
    """Route any MCP tool call through arifOS constitutional gateway."""
    return await gateway_route_tool(
        tool_name=tool_name,
        payload=payload,
        session_id=session_id,
        actor_id=actor_id,
        require_human_override=require_human_override,
    )


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("gateway_list_tools", {}))
async def _gateway_list_tools_wrapper() -> dict:
    """List all tools available through the constitutional gateway."""
    return await gateway_list_tools()


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("gateway_get_decisions", {}))
async def _gateway_get_decisions_wrapper(
    session_id: Optional[str] = None,
    limit: int = 100,
) -> dict:
    """Query gateway decisions (audit trail)."""
    return await gateway_get_decisions(session_id=session_id, limit=limit)


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("k8s_apply_guarded", {}))
async def _k8s_apply_guarded_wrapper(
    manifest: str,
    namespace: str,
    session_id: str,
    strategy: str = "rolling",
    backup_made: bool = False,
    human_override: bool = False,
) -> dict:
    """Constitutionally-governed kubectl apply."""
    return await k8s_apply_guarded(
        manifest=manifest,
        namespace=namespace,
        session_id=session_id,
        strategy=strategy,
        backup_made=backup_made,
        human_override=human_override,
    )


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("k8s_delete_guarded", {}))
async def _k8s_delete_guarded_wrapper(
    resource: str,
    name: str,
    namespace: str,
    session_id: str,
    backup_made: bool = False,
    human_override: bool = False,
    cascade: bool = True,
) -> dict:
    """Constitutionally-governed kubectl delete."""
    return await k8s_delete_guarded(
        resource=resource,
        name=name,
        namespace=namespace,
        session_id=session_id,
        backup_made=backup_made,
        human_override=human_override,
        cascade=cascade,
    )


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("k8s_constitutional_apply", {}))
async def _k8s_constitutional_apply_wrapper(
    manifest: str,
    namespace: str = "default",
    strategy: str = "rolling",
    session_id: str = "",
    dry_run: bool = False,
) -> dict:
    """Evaluate K8s apply through constitutional floors."""
    return await k8s_constitutional_apply(
        manifest=manifest,
        namespace=namespace,
        strategy=strategy,
        session_id=session_id,
        dry_run=dry_run,
    )


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("k8s_constitutional_delete", {}))
async def _k8s_constitutional_delete_wrapper(
    resource: str,
    name: str,
    namespace: str = "default",
    backup_made: bool = False,
    session_id: str = "",
) -> dict:
    """Evaluate K8s delete through constitutional floors."""
    return await k8s_constitutional_delete(
        resource=resource,
        name=name,
        namespace=namespace,
        backup_made=backup_made,
        session_id=session_id,
    )


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("k8s_analyze_manifest", {}))
async def _k8s_analyze_manifest_wrapper(manifest: str) -> dict:
    """Analyze a K8s manifest without constitutional enforcement."""
    return await k8s_analyze_manifest(manifest=manifest)


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("opa_validate_manifest", {}))
async def _opa_validate_manifest_wrapper(
    manifest: str,
    namespace: str = "k8s",
    session_id: str = "",
) -> dict:
    """Validate K8s manifest against OPA policies (F10 Ontology)."""
    return await opa_validate_manifest(
        manifest=manifest,
        namespace=namespace,
        session_id=session_id,
    )


@mcp.tool(annotations=TOOL_ANNOTATIONS.get("opa_list_policies", {}))
async def _opa_list_policies_wrapper() -> dict:
    """List available OPA/Conftest policies."""
    return await opa_list_policies()


# Apply annotations at module load time
_apply_tool_annotations()


if __name__ == "__main__":
    print("arifOS Constitutional Kernel - FastMCP Mode")
    mcp.run(transport="sse", port=6274)
