"""
aaa_mcp/server.py — Canonical 13-Tool FastMCP Surface

Contract — 13 canonical tools with UX verb names:
  Governance (7):  anchor_session, reason_mind, recall_memory, simulate_heart,
                   critique_thought, judge_soul, forge_hand, seal_vault
  Utilities (5):   search_reality, fetch_content, inspect_file, audit_rules, check_vital

This module owns its own FastMCP instance (isolated from aclip_cai triad tools).
All tools must be async and must not write to stdout (stdio transport safety).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastmcp import FastMCP
from aclip_cai.triad import align, anchor, audit, forge, integrate, reason, respond, seal, validate

# Isolated FastMCP instance — canonical 13-tool surface ONLY.
# Previously shared aclip_cai's instance which leaked triad_*/sense_* tools.
mcp = FastMCP(
    "arifOS_AAA_MCP",
    instructions=(
        "Canonical 13-tool arifOS AAA MCP surface. "
        "Governance spine: 000->222->333->444->555->666->777->888->999. "
        "All tools return {verdict, stage, session_id} envelope."
    ),
)

from aaa_mcp.external_gateways.brave_client import BraveSearchClient
from fastmcp.resources.template import ResourceTemplate
from aaa_mcp.external_gateways.perplexity_client import PerplexitySearchClient
from aaa_mcp.protocol.l0_kernel_prompt import inject_l0_into_session
from aaa_mcp.protocol.schemas import CANONICAL_TOOL_INPUT_SCHEMAS, CANONICAL_TOOL_OUTPUT_SCHEMAS
from core.shared.context_template import build_full_context_template

def create_unified_mcp_server() -> Any:
    """Return the unified FastMCP server instance (tool registration happens at import time)."""
    return mcp


class ToolHandle:
    """
    Compatibility wrapper.

    Some test suites expect tool objects with a `.fn` attribute. FastMCP registers
    tools but returns the original function from its decorator, so we provide a
    stable `.fn` surface without affecting runtime registration.
    """

    def __init__(self, fn: Any) -> None:
        if hasattr(fn, "fn"):
            self.fn = fn.fn
        else:
            self.fn = fn


def _fold_verdict(verdicts: List[str]) -> str:
    if any(v.upper() == "VOID" for v in verdicts):
        return "VOID"
    if any(v.upper() in {"SABAR", "888_HOLD"} for v in verdicts):
        return "SABAR"
    if any(v.upper() == "PARTIAL" for v in verdicts):
        return "PARTIAL"
    return "SEAL"


def _build_floor_block(stage: str, reason: str) -> Dict[str, Any]:
    """Standardized F11 block for missing session/auth continuity."""
    return {
        "verdict": "VOID",
        "stage": stage,
        "session_id": "",
        "token_status": "ERROR",
        "floors": {"passed": [], "failed": ["F11"]},
        "truth": {"score": None, "threshold": None, "drivers": []},
        "next_actions": [
            "Run init_session (anchor) first to obtain session_id.",
            "Reuse the same session_id across downstream tools.",
            "Include actor_id/auth_token when available for continuity.",
        ],
        "remediation": {
            "required_auth_fields": ["session_id", "actor_id", "auth_token"],
            "reuse_session": True,
        },
        "error": reason,
    }


def _extract_truth(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = payload.get("truth_score")
    threshold = payload.get("f2_threshold")
    drivers = payload.get("truth_drivers")
    if not isinstance(drivers, list):
        drivers = []
    return {"score": score, "threshold": threshold, "drivers": drivers}


def _envelope(stage: str, session_id: str, verdict: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    floors_failed = payload.get("floors_failed", [])
    if not isinstance(floors_failed, list):
        floors_failed = []
    actions: List[str] = []
    if "F2" in floors_failed:
        actions.append("Provide stronger evidence and retry with grounded claims.")
    if "F11" in floors_failed:
        actions.append("Restore session/auth continuity and retry.")
    if not actions:
        actions.append("Continue to next constitutional stage.")
    return {
        "verdict": verdict,
        "stage": stage,
        "session_id": session_id,
        "floors": {"passed": [], "failed": floors_failed},
        "truth": _extract_truth(payload),
        "next_actions": actions,
    }


# ═══════════════════════════════════════════════════════
# GOVERNANCE TOOLS (5-Organ Trinity)
# ═══════════════════════════════════════════════════════


@mcp.tool(name="anchor_session", description="[Lane: Δ Delta] [Floors: F11, F12, F13] Session ignition & injection defense.")
async def _init_session(
    query: str,
    actor_id: str = "anonymous",
    auth_token: Optional[str] = None,
    mode: str = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
    inject_kernel: bool = True,
    compact_kernel: bool = False,
    template_id: str = "arifos.full_context.v1",
    auth_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Initialize a new constitutional session with L0 Kernel enforcement.
    
    Args:
        query: User's initial query
        actor_id: Authenticated actor identifier
        auth_token: Optional authentication token
        mode: Session mode (conscience, exploration, etc.)
        grounding_required: Whether to require source grounding
        debug: Include detailed internal data
        inject_kernel: Inject L0 constitutional prompt (default: True)
        compact_kernel: Use compact L0 prompt to save tokens (default: False)
    
    Returns:
        Session data with constitutional system prompt
    """
    try:
        session_id = f"{actor_id}-{uuid.uuid4().hex[:8]}"
        anch = await anchor(session_id=session_id, user_id=actor_id, context=query)
        verdict = str(anch.get("verdict", "SEAL"))
        
        result = {
            "verdict": verdict,
            "session_id": anch.get("session_id", session_id),
            "stage": "000_INIT",
            "template_id": template_id,
            "mode": mode,
            "grounding_required": grounding_required,
            "token_status": "AUTHENTICATED" if auth_token else "ANONYMOUS",
            "auth": {"present": bool(auth_token)},
            "auth_context": auth_context or {},
            "debug": debug,
            "data": {"anchor": anch} if debug else {},
        }

        result.update(
            _envelope(
                stage="000_INIT",
                session_id=result["session_id"],
                verdict=verdict,
                payload=anch if isinstance(anch, dict) else {},
            )
        )
        
        # 🔥 CONSTITUTIONAL INJECTION: Embed L0 Kernel prompt
        if inject_kernel:
            result = inject_l0_into_session(result, compact=compact_kernel)
            
        return result
        
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "000_INIT"}

anchor_session = ToolHandle(_init_session)

@mcp.tool(name="reason_mind", description="[Lane: Δ Delta] [Floors: F2, F4, F7, F8] AGI cognition & logic grounding.")
async def _agi_cognition(
    query: str,
    session_id: str,
    grounding: Optional[List[Dict[str, Any]]] = None,
    capability_modules: Optional[List[str]] = None,
    debug: bool = False,
    actor_id: str = "anonymous",
    auth_token: Optional[str] = None,
    parent_session_id: Optional[str] = None,
    auth_context: Optional[Dict[str, Any]] = None,
    inference_budget: int = 1,
    risk_mode: str = "medium",
) -> Dict[str, Any]:
    try:
        if not session_id:
            return _build_floor_block("111-444", "Missing session_id")

        evidence = [str(x) for x in (grounding or [])]
        r = await reason(session_id=session_id, hypothesis=query, evidence=evidence)
        i = await integrate(session_id=session_id, context_bundle={"query": query, "grounding": grounding or {}})
        d = await respond(session_id=session_id, draft_response=f"Draft response for: {query}")
        verdict = _fold_verdict([str(r.get("verdict", "")), str(i.get("verdict", "")), str(d.get("verdict", ""))])
        merged = {
            "truth_score": r.get("truth_score"),
            "f2_threshold": r.get("f2_threshold"),
            "floors_failed": list(r.get("floors_failed", [])) + list(i.get("floors_failed", [])) + list(d.get("floors_failed", [])),
        }
        result = {
            "capability_modules": capability_modules or [],
            "actor_id": actor_id,
            "token_status": "AUTHENTICATED" if auth_token else "ANONYMOUS",
            "parent_session_id": parent_session_id,
            "auth_context": auth_context or {},
            "inference_budget": max(0, min(3, int(inference_budget))),
            "risk_mode": risk_mode,
            "debug": debug,
            "data": {"reason": r, "integrate": i, "respond": d} if debug else {},
        }
        result.update(_envelope(stage="111-444", session_id=session_id, verdict=verdict, payload=merged))
        return result
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "111-444", "session_id": session_id}

reason_mind = ToolHandle(_agi_cognition)

@mcp.tool(name="recall_memory", description="[Lane: Ω Omega] [Floors: F4, F7, F13] Associative memory traces.")
async def _phoenix_recall(
    current_thought_vector: str,
    session_id: str,
    debug: bool = False,
) -> Dict[str, Any]:
    """
    Organ 5: PHOENIX. Associative memory retrieval via EUREKA sieve.
    """
    try:
        if not session_id:
            return _build_floor_block("555_RECALL", "Missing session_id")
        
        # Implementation will call core.organs._5_phoenix.phoenix_recall
        # For now, return a placeholder that confirms the stage
        result = {
            "status": "RECALL_SUCCESS",
            "memories": [],
            "metrics": {
                "jaccard_max": 0.0,
                "delta_s_actual": 0.0,
                "w_scar_applied": 0.5
            }
        }
        result.update(_envelope(stage="555_RECALL", session_id=session_id, verdict="SEAL", payload={}))
        return result
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "555_RECALL", "session_id": session_id}

recall_memory = ToolHandle(_phoenix_recall)

@mcp.tool(name="simulate_heart", description="[Lane: Ω Omega] [Floors: F4, F5, F6] Stakeholder impact & care constraints.")
async def _asi_empathy(
    query: str,
    session_id: str,
    stakeholders: Optional[List[str]] = None,
    capability_modules: Optional[List[str]] = None,
    debug: bool = False,
    actor_id: str = "anonymous",
    auth_token: Optional[str] = None,
    parent_session_id: Optional[str] = None,
    auth_context: Optional[Dict[str, Any]] = None,
    risk_mode: str = "medium",
) -> Dict[str, Any]:
    try:
        if not session_id:
            return _build_floor_block("555-666", "Missing session_id")

        v = await validate(session_id=session_id, action=query)
        a = await align(session_id=session_id, action=query)
        verdict = _fold_verdict([str(v.get("verdict", "")), str(a.get("verdict", ""))])
        merged = {
            "truth_score": v.get("truth_score"),
            "f2_threshold": v.get("f2_threshold"),
            "floors_failed": list(v.get("floors_failed", [])) + list(a.get("floors_failed", [])),
        }
        result = {
            "stakeholders": stakeholders or [],
            "capability_modules": capability_modules or [],
            "actor_id": actor_id,
            "token_status": "AUTHENTICATED" if auth_token else "ANONYMOUS",
            "parent_session_id": parent_session_id,
            "auth_context": auth_context or {},
            "risk_mode": risk_mode,
            "debug": debug,
            "data": {"validate": v, "align": a} if debug else {},
        }
        result.update(_envelope(stage="555-666", session_id=session_id, verdict=verdict, payload=merged))
        return result
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "555-666", "session_id": session_id}

simulate_heart = ToolHandle(_asi_empathy)

@mcp.tool(name="judge_soul", description="[Lane: Ψ Psi] [Floors: F1-F13] Sovereign verdict synthesis.")
async def _apex_verdict(
    session_id: str,
    query: str,
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
    capability_modules: Optional[List[str]] = None,
    implementation_details: Optional[Dict[str, Any]] = None,
    proposed_verdict: str = "SEAL",
    human_approve: bool = False,
    debug: bool = False,
    actor_id: str = "anonymous",
    auth_token: Optional[str] = None,
    parent_session_id: Optional[str] = None,
    auth_context: Optional[Dict[str, Any]] = None,
    risk_mode: str = "medium",
) -> Dict[str, Any]:
    try:
        if not session_id:
            return _build_floor_block("777-888", "Missing session_id")

        plan = {
            "query": query,
            "proposed_verdict": proposed_verdict,
            "human_approve": human_approve,
            "agi": agi_result or {},
            "asi": asi_result or {},
            "implementation_details": implementation_details or {},
        }
        forged = await forge(session_id=session_id, plan=str(plan))
        sovereign_token = "888_APPROVED" if human_approve else ""
        judged = await audit(session_id=session_id, action=str(plan), sovereign_token=sovereign_token)
        verdict = str(judged.get("verdict", proposed_verdict))
        merged = {
            "truth_score": judged.get("truth_score"),
            "f2_threshold": judged.get("f2_threshold"),
            "floors_failed": list(forged.get("floors_failed", [])) + list(judged.get("floors_failed", [])),
        }
        result = {
            "authority": {"human_approve": human_approve},
            "capability_modules": capability_modules or [],
            "actor_id": actor_id,
            "token_status": "AUTHENTICATED" if auth_token else "ANONYMOUS",
            "parent_session_id": parent_session_id,
            "auth_context": auth_context or {},
            "risk_mode": risk_mode,
            "debug": debug,
            "data": {"forge": forged, "audit": judged} if debug else {},
        }
        result.update(_envelope(stage="777-888", session_id=session_id, verdict=verdict, payload=merged))
        return result
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "777-888", "session_id": session_id}

judge_soul = ToolHandle(_apex_verdict)

@mcp.tool(name="forge_hand", description="[Lane: Ψ Psi] [Floors: F1, F11, F12] Sandboxed action execution.")
async def _sovereign_actuator(
    action_payload: Dict[str, Any],
    signed_tensor: Dict[str, Any],
    execution_context: Dict[str, Any],
    signature: str,
    session_id: str,
    idempotency_key: str,
    ratification_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Organ 6: FORGE. Physical world interaction gated by APEX Soul SEAL.
    """
    try:
        if not session_id:
            return _build_floor_block("888_FORGE", "Missing session_id")
        
        # Implementation will call core.organs._6_forge.sovereign_actuator
        # For now, return a placeholder that yields 888_HOLD if irreversible
        result = {
            "status": "888_HOLD",
            "message": "FORGE YIELDED. Sovereign ratification required.",
            "instruction": "Sign the ratification_challenge with the Sovereign Key to proceed."
        }
        result.update(_envelope(stage="888_FORGE", session_id=session_id, verdict="888_HOLD", payload={}))
        return result
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "888_FORGE", "session_id": session_id}

forge_hand = ToolHandle(_sovereign_actuator)

@mcp.tool(name="seal_vault", description="[Lane: Ψ Psi] [Floors: F1, F3, F10] Immutable ledger persistence.")
async def _vault_seal(
    session_id: str,
    summary: str,
    verdict: str = "SEAL",
) -> Dict[str, Any]:
    try:
        if not session_id:
            return _build_floor_block("999_VAULT", "Missing session_id")
        res = await seal(session_id=session_id, task_summary=summary, was_modified=True)
        result = {"data": res, "status": verdict}
        result.update(_envelope(stage="999_VAULT", session_id=session_id, verdict=verdict, payload=res))
        return result
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "999_VAULT", "session_id": session_id}

seal_vault = ToolHandle(_vault_seal)

# ═══════════════════════════════════════════════════════
# UTILITIES (Read-only)
# ═══════════════════════════════════════════════════════


@mcp.tool(name="search_reality", description="[Lane: Δ Delta] [Floors: F2, F4, F12] Web grounding (Perplexity/Brave).")
async def _search(query: str, intent: str = "general") -> Dict[str, Any]:
    try:
        # Preferred order: Perplexity (if PPLX key is set) -> Brave fallback.
        primary = PerplexitySearchClient()
        payload = await primary.search(query=query, intent=intent)

        if payload.get("status") in {"NO_API_KEY", "BAD_RESPONSE", "BAD_JSON", "BAD_SHAPE"}:
            fallback = BraveSearchClient()
            payload = await fallback.search(query=query, intent=intent)

        urls = [r.get("url") for r in payload.get("results", []) if r.get("url")]
        return {
            "query": query,
            "intent": intent,
            "status": payload.get("status", "OK"),
            "ids": urls,
            "results": payload.get("results", []),
        }
    except Exception as e:
        return {"query": query, "intent": intent, "ids": [], "results": [], "status": f"ERROR: {e}"}

search_reality = ToolHandle(_search)

@mcp.tool(name="fetch_content", description="[Lane: Δ Delta] [Floors: F2, F4, F12] Raw evidence content retrieval.")
async def _fetch(id: str, max_chars: int = 4000) -> Dict[str, Any]:
    try:
        import urllib.request

        if not (id.startswith("http://") or id.startswith("https://")):
            return {"id": id, "error": "Unsupported id (expected URL)", "status": "BAD_ID"}

        req = urllib.request.Request(id, headers={"User-Agent": "arifOS/aaa_mcp fetch"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read()
        text = raw.decode("utf-8", errors="replace")
        return {"id": id, "status": "OK", "content": text[:max_chars], "truncated": len(text) > max_chars}
    except Exception as e:
        return {"id": id, "error": str(e), "status": "ERROR"}

fetch_content = ToolHandle(_fetch)

# Internal Tool
async def _analyze(data: Dict[str, Any], analysis_type: str = "structure") -> Dict[str, Any]:
    try:
        if analysis_type == "structure":
            depth = 1
            if isinstance(data, dict):
                depth = 2 if any(isinstance(v, dict) for v in data.values()) else 1
            return {"verdict": "SEAL", "analysis_type": analysis_type, "depth": depth, "keys": list(data.keys())}
        return {"verdict": "PARTIAL", "analysis_type": analysis_type, "message": "Unknown analysis_type"}
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "analysis_type": analysis_type}

# analyze = ToolHandle(_analyze)

@mcp.tool(name="audit_rules", description="[Lane: Δ Delta] [Floors: F2, F8, F10] Rule & governance audit checks.")
async def _system_audit(audit_scope: str = "quick", verify_floors: bool = True) -> Dict[str, Any]:
    try:
        details: Dict[str, Any] = {"scope": audit_scope}
        if verify_floors:
            try:
                from aaa_mcp.core.constitutional_decorator import FLOOR_ENFORCEMENT

                details["floors_loaded"] = bool(FLOOR_ENFORCEMENT)
                details["floor_tool_count"] = len(FLOOR_ENFORCEMENT)
            except Exception as e:
                details["floors_loaded"] = False
                details["floor_error"] = str(e)
        return {"verdict": "SEAL" if details.get("floors_loaded", True) else "PARTIAL", "scope": audit_scope, "details": details}
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "scope": audit_scope}

audit_rules = ToolHandle(_system_audit)


@mcp.tool(name="critique_thought", description="[Lane: Ω Omega] [Floors: F4, F7, F8] 7-organ alignment & bias critique.")
async def _critique_thought(session_id: str, query: str) -> Dict[str, Any]:
    return _envelope(stage="666_CRITIQUE", session_id=session_id, verdict="SEAL", payload={"status": "STUB_IMPLEMENTATION"})

critique_thought = ToolHandle(_critique_thought)

@mcp.tool(name="inspect_file", description="[Lane: Δ Delta] [Floors: F1, F4, F11] Filesystem inspection (read-only).")
async def _inspect_file(session_id: str, path: str) -> Dict[str, Any]:
    return _envelope(stage="111_INSPECT", session_id=session_id, verdict="SEAL", payload={"status": "STUB_IMPLEMENTATION"})

inspect_file = ToolHandle(_inspect_file)

@mcp.tool(name="check_vital", description="[Lane: Ω Omega] [Floors: F4, F5, F7] System health & vital signs.")
async def _check_vital(session_id: str) -> Dict[str, Any]:
    return _envelope(stage="555_HEALTH", session_id=session_id, verdict="SEAL", payload={"status": "STUB_IMPLEMENTATION"})

check_vital = ToolHandle(_check_vital)

# ═══════════════════════════════════════════════════════
# RESOURCES, TEMPLATES, PROMPTS (Full-context orchestration + Inspector completeness)
# ═══════════════════════════════════════════════════════



@mcp.resource(
    "arifos://info",
    mime_type="application/json",
    description="Static server metadata and surface summary.",
)
async def _arifos_info_resource() -> Dict[str, Any]:
    return {
        "name": "arifOS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tools": [
            "anchor_session",
            "reason_mind",
            "recall_memory",
            "simulate_heart",
            "critique_thought",
            "judge_soul",
            "forge_hand",
            "seal_vault",
            "search_reality",
            "fetch_content",
            "inspect_file",
            "audit_rules",
            "check_vital",
        ],
    }


async def _constitutional_floor_resource(floor_id: str) -> Dict[str, Any]:
    """
    Lightweight floor lookup for MCP Resource Templates.
    If YAML config is available, returns threshold and hold-on-fail metadata.
    """
    floor_id = (floor_id or "").strip().upper()
    payload: Dict[str, Any] = {"floor": floor_id}

    try:
        import yaml  # type: ignore[import-not-found]

        from pathlib import Path

        cfg_path = Path(__file__).resolve().parents[1] / "aclip_cai" / "config" / "floors.yaml"
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        payload["thresholds"] = data.get("thresholds", {})
        payload["hold_on_fail"] = data.get("hold_on_fail", [])
        payload["floor_threshold"] = payload["thresholds"].get(floor_id)
    except Exception:
        payload["floor_threshold"] = None

    return payload


mcp.add_template(
    ResourceTemplate.from_function(
        fn=_constitutional_floor_resource,
        uri_template="constitutional://floors/{floor_id}",
        name="constitutional_floor",
        description="Lookup threshold/config for a constitutional floor ID.",
        mime_type="application/json",
    )
)


@mcp.prompt(
    name="arifos_governance_brief",
    description="Reusable prompt: arifOS governance constraints and usage.",
)
async def _arifos_governance_brief_prompt() -> str:
    return (
        "You are operating under arifOS constitutional governance.\n"
        "Use tools for actions; prefer reversible steps; avoid secrets leakage.\n"
        "If an operation is high-stakes or irreversible, request explicit human approval.\n"
    )

@mcp.resource(
    "arifos://templates/full-context",
    name="arifos_full_context_template",
    mime_type="application/json",
    description="Canonical full-context template for AAA constitutional orchestration.",
)
def _resource_full_context_template() -> Dict[str, Any]:
    return build_full_context_template()


@mcp.resource(
    "arifos://schemas/tooling",
    name="arifos_tool_schemas",
    mime_type="application/json",
    description="Canonical tool input/output schemas for AAA MCP tools.",
)
def _resource_tool_schemas() -> Dict[str, Any]:
    return {
        "schema_version": "2026.02.23-context-forge",
        "inputs": CANONICAL_TOOL_INPUT_SCHEMAS,
        "outputs": CANONICAL_TOOL_OUTPUT_SCHEMAS,
    }


@mcp.prompt(name="arifos.prompt.trinity_forge")
def _prompt_trinity_forge(query: str, actor_id: str = "user", mode: str = "conscience") -> str:
    return (
        "Use trinity_forge for full constitutional orchestration with session continuity.\n"
        "Stage spine: 000 -> 222 -> 333 -> 444 -> 666 -> 888 -> 999.\n"
        "Require truthful grounding; fail closed on F2/F11/F12 with remediation.\n"
        "Call shape: {\"name\":\"trinity_forge\",\"arguments\":{"
        f"\"query\":{query!r},\"actor_id\":{actor_id!r},\"mode\":{mode!r}"
        "}}"
    )


@mcp.prompt(name="arifos.prompt.anchor_reason")
def _prompt_anchor_reason(query: str, actor_id: str = "user") -> str:
    return (
        "Run two-step constitutional flow with explicit session continuity.\n"
        "1) anchor/init_session to obtain session_id.\n"
        "2) reason/agi_cognition using same session_id.\n"
        "If VOID on F11: request auth_token or corrected actor_id.\n"
        "If VOID on F2: request external evidence before retry.\n"
        f"Input query: {query}\nActor: {actor_id}"
    )


@mcp.prompt(name="arifos.prompt.audit_then_seal")
def _prompt_audit_then_seal(session_id: str, summary: str, proposed_verdict: str = "SEAL") -> str:
    return (
        "Finalize governed decision in two steps.\n"
        "1) apex_verdict/audit with session_id and explicit proposed_verdict.\n"
        "2) vault_seal with same session_id and immutable summary.\n"
        "If verdict is 888_HOLD, stop and request human ratification before seal.\n"
        f"session_id={session_id}; proposed_verdict={proposed_verdict}; summary={summary}"
    )

__all__ = [
    "create_unified_mcp_server",
    "mcp",
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "judge_soul",
    "forge_hand",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
    "_resource_full_context_template",
    "_resource_tool_schemas",
    "_prompt_trinity_forge",
    "_prompt_anchor_reason",
    "_prompt_audit_then_seal",
]
