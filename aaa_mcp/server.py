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


# ═══════════════════════════════════════════════════════
# GOVERNANCE TOOLS (5-Organ Trinity)
# ═══════════════════════════════════════════════════════


@mcp.tool(name="init_session", description="000_INIT — Session ignition + defense scan.")
async def _init_session(
    query: str,
    actor_id: str = "anonymous",
    auth_token: Optional[str] = None,
    mode: str = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
) -> Dict[str, Any]:
    try:
        session_id = f"{actor_id}-{uuid.uuid4().hex[:8]}"
        anch = await anchor(session_id=session_id, user_id=actor_id, context=query)
        verdict = str(anch.get("verdict", "SEAL"))
        return {
            "verdict": verdict,
            "session_id": anch.get("session_id", session_id),
            "stage": "000_INIT",
            "mode": mode,
            "grounding_required": grounding_required,
            "auth": {"present": bool(auth_token)},
            "debug": debug,
            "data": {"anchor": anch} if debug else {},
        }
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
) -> Dict[str, Any]:
    try:
        evidence = [str(x) for x in (grounding or [])]
        r = await reason(session_id=session_id, hypothesis=query, evidence=evidence)
        i = await integrate(session_id=session_id, context_bundle={"query": query, "grounding": grounding or {}})
        d = await respond(session_id=session_id, draft_response=f"Draft response for: {query}")
        verdict = _fold_verdict([str(r.get("verdict", "")), str(i.get("verdict", "")), str(d.get("verdict", ""))])
        return {
            "verdict": verdict,
            "session_id": session_id,
            "stage": "111-444",
            "capability_modules": capability_modules or [],
            "debug": debug,
            "data": {"reason": r, "integrate": i, "respond": d} if debug else {},
        }
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
) -> Dict[str, Any]:
    try:
        v = await validate(session_id=session_id, action=query)
        a = await align(session_id=session_id, action=query)
        verdict = _fold_verdict([str(v.get("verdict", "")), str(a.get("verdict", ""))])
        return {
            "verdict": verdict,
            "session_id": session_id,
            "stage": "555-666",
            "stakeholders": stakeholders or [],
            "capability_modules": capability_modules or [],
            "debug": debug,
            "data": {"validate": v, "align": a} if debug else {},
        }
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
) -> Dict[str, Any]:
    try:
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
        return {
            "verdict": verdict,
            "session_id": session_id,
            "stage": "777-888",
            "authority": {"human_approve": human_approve},
            "capability_modules": capability_modules or [],
            "debug": debug,
            "data": {"forge": forged, "audit": judged} if debug else {},
        }
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
        res = await seal(session_id=session_id, task_summary=summary, was_modified=True)
        return {"verdict": verdict, "stage": "999_VAULT", "session_id": session_id, "data": res}
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
]
