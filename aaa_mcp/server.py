"""
aaa_mcp/server.py — Unified FastMCP Tool Surface

Contract:
- 5 canonical governance tools:
  init_session, agi_cognition, asi_empathy, apex_verdict, vault_seal
- 4 read-only utilities:
  search, fetch, analyze, system_audit

This module exposes a FastMCP server instance via `create_unified_mcp_server()`.
All tools must be async and must not write to stdout (stdio transport safety).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import uuid

from aclip_cai.mcp_server import mcp
from aclip_cai.triad import align, anchor, audit, forge, integrate, reason, respond, seal, validate

from aaa_mcp.external_gateways.brave_client import BraveSearchClient
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


@mcp.tool(name="init_session", description="000_INIT — Session ignition + L0 Kernel injection + defense scan.")
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

init_session = ToolHandle(_init_session)

@mcp.tool(name="agi_cognition", description="111–444_AGI — Reason + integrate + draft response.")
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

agi_cognition = ToolHandle(_agi_cognition)

@mcp.tool(name="asi_empathy", description="555–666_ASI — Validate + align.")
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

asi_empathy = ToolHandle(_asi_empathy)

@mcp.tool(name="apex_verdict", description="777–888_APEX — Forge + audit final verdict.")
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

apex_verdict = ToolHandle(_apex_verdict)

@mcp.tool(name="vault_seal", description="999_VAULT — Commit decision to immutable vault.")
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

vault_seal = ToolHandle(_vault_seal)

# ═══════════════════════════════════════════════════════
# UTILITIES (Read-only)
# ═══════════════════════════════════════════════════════


@mcp.tool(name="search", description="Read-only web search (Brave API if configured).")
async def _search(query: str, intent: str = "general") -> Dict[str, Any]:
    try:
        client = BraveSearchClient()
        payload = await client.search(query=query, intent=intent)
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

search = ToolHandle(_search)

@mcp.tool(name="fetch", description="Read-only fetch by URL/id from `search` results.")
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

fetch = ToolHandle(_fetch)

@mcp.tool(name="analyze", description="Read-only analysis helper for structured data.")
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

analyze = ToolHandle(_analyze)

@mcp.tool(name="system_audit", description="Read-only system audit (health + basic invariants).")
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

system_audit = ToolHandle(_system_audit)

# ═══════════════════════════════════════════════════════
# MCP RESOURCES + PROMPTS (Full-context orchestration)
# ═══════════════════════════════════════════════════════


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
    "init_session",
    "agi_cognition",
    "asi_empathy",
    "apex_verdict",
    "vault_seal",
    "search",
    "fetch",
    "analyze",
    "system_audit",
    "_resource_full_context_template",
    "_resource_tool_schemas",
    "_prompt_trinity_forge",
    "_prompt_anchor_reason",
    "_prompt_audit_then_seal",
]
