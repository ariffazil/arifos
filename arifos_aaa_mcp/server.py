"""arifOS AAA MCP public 13-tool surface.

This package is the canonical external interface.
Legacy `aaa_mcp` and `aclip_cai` remain internal intelligence providers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from aaa_mcp import server as legacy
from aclip_cai.tools.fs_inspector import fs_inspect
from aclip_cai.tools.system_monitor import get_system_health
from .governance import LAW_13_CATALOG, TOOL_DIALS_MAP, wrap_tool_output
from .contracts import require_session, validate_input
from .fastmcp_ext.discovery import build_surface_discovery

from aaa_mcp.protocol.tool_registry import export_full_context_pack


mcp = FastMCP(
    "arifOS_AAA_MCP",
    instructions=(
        "Canonical 13-tool arifOS AAA MCP surface. "
        "Use 000->333->555->666->777/888->999 governance spine."
    ),
)

AAA_TOOLS = [
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
]


def _model_flags(plan: Dict[str, Any], context: str = "") -> Dict[str, Any]:
    text = (context + " " + str(plan)).lower()
    return {
        "non_linearity": any(k in text for k in ["feedback", "cascade", "tipping"]),
        "gray_thinking": any(k in text for k in ["however", "trade-off", "depends"]),
        "occams_bias": len(plan.keys()) <= 20,
        "framing_bias": not any(k in text for k in ["obviously", "guaranteed", "always", "never"]),
        "anti_comfort": any(k in text for k in ["hard", "difficult", "mitigation", "review"]),
        "delayed_discomfort": any(k in text for k in ["future", "later", "debt", "drift"]),
        "inversion": any(k in text for k in ["failure", "risk", "worst-case", "break"]),
    }


@mcp.tool(name="anchor_session")
async def anchor_session(
    query: str,
    actor_id: str = "anonymous",
    auth_token: Optional[str] = None,
    mode: str = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
) -> Dict[str, Any]:
    """000 INIT: ignite constitutional session and continuity token."""
    blocked = validate_input("anchor_session", {"query": query, "actor_id": actor_id})
    if blocked:
        return wrap_tool_output("anchor_session", blocked)
    payload = await legacy.init_session.fn(
        query=query,
        actor_id=actor_id,
        auth_token=auth_token,
        mode=mode,
        grounding_required=grounding_required,
        debug=debug,
    )
    return wrap_tool_output("anchor_session", payload)


@mcp.tool(name="reason_mind")
async def reason_mind(
    query: str,
    session_id: str,
    grounding: Optional[List[Dict[str, Any]]] = None,
    capability_modules: Optional[List[str]] = None,
    debug: bool = False,
) -> Dict[str, Any]:
    """333 REASON: run AGI cognition with grounding and budget controls."""
    blocked = validate_input("reason_mind", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("reason_mind", blocked)
    missing = require_session("reason_mind", session_id)
    if missing:
        return wrap_tool_output("reason_mind", missing)
    payload = await legacy.agi_cognition.fn(
        query=query,
        session_id=session_id,
        grounding=grounding,
        capability_modules=capability_modules,
        debug=debug,
    )
    return wrap_tool_output("reason_mind", payload)


@mcp.tool(name="recall_memory")
async def recall_memory(
    current_thought_vector: str,
    session_id: str,
    debug: bool = False,
) -> Dict[str, Any]:
    """444 EVIDENCE: retrieve associative memory traces for current thought."""
    blocked = validate_input(
        "recall_memory", {"current_thought_vector": current_thought_vector, "session_id": session_id}
    )
    if blocked:
        return wrap_tool_output("recall_memory", blocked)
    missing = require_session("recall_memory", session_id)
    if missing:
        return wrap_tool_output("recall_memory", missing)
    payload = await legacy.phoenix_recall.fn(
        current_thought_vector=current_thought_vector,
        session_id=session_id,
        debug=debug,
    )
    return wrap_tool_output("recall_memory", payload)


@mcp.tool(name="simulate_heart")
async def simulate_heart(
    query: str,
    session_id: str,
    stakeholders: Optional[List[str]] = None,
    capability_modules: Optional[List[str]] = None,
    debug: bool = False,
) -> Dict[str, Any]:
    """555 EMPATHY: evaluate stakeholder impact and care constraints."""
    blocked = validate_input("simulate_heart", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("simulate_heart", blocked)
    missing = require_session("simulate_heart", session_id)
    if missing:
        return wrap_tool_output("simulate_heart", missing)
    payload = await legacy.asi_empathy.fn(
        query=query,
        session_id=session_id,
        stakeholders=stakeholders,
        capability_modules=capability_modules,
        debug=debug,
    )
    return wrap_tool_output("simulate_heart", payload)


@mcp.tool(name="critique_thought")
async def critique_thought(plan: Dict[str, Any], session_id: str, context: str = "") -> Dict[str, Any]:
    """666 ALIGN: run 7-model critique (inversion, framing, non-linearity, etc.)."""
    blocked = validate_input("critique_thought", {"plan": plan, "session_id": session_id})
    if blocked:
        return wrap_tool_output("critique_thought", blocked)
    missing = require_session("critique_thought", session_id)
    if missing:
        return wrap_tool_output("critique_thought", missing)
    flags = _model_flags(plan, context=context)
    failed = [k for k, v in flags.items() if not v]
    payload = {
        "verdict": "SEAL" if not failed else "SABAR",
        "session_id": session_id,
        "stage": "666_ALIGN",
        "mental_models": flags,
        "failed_models": failed,
    }
    return wrap_tool_output("critique_thought", payload)


@mcp.tool(name="judge_soul")
async def judge_soul(
    session_id: str,
    query: str,
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
    critique_result: Optional[Dict[str, Any]] = None,
    proposed_verdict: str = "SEAL",
    human_approve: bool = False,
    debug: bool = False,
) -> Dict[str, Any]:
    """777/888 APEX: sovereign constitutional verdict synthesis."""
    blocked = validate_input("judge_soul", {"session_id": session_id, "query": query})
    if blocked:
        return wrap_tool_output("judge_soul", blocked)
    missing = require_session("judge_soul", session_id)
    if missing:
        return wrap_tool_output("judge_soul", missing)
    payload = await legacy.apex_verdict.fn(
        session_id=session_id,
        query=query,
        agi_result=agi_result,
        asi_result=asi_result,
        implementation_details={"critique": critique_result or {}},
        proposed_verdict=proposed_verdict,
        human_approve=human_approve,
        debug=debug,
    )
    return wrap_tool_output("judge_soul", payload)


@mcp.tool(name="forge_hand")
async def forge_hand(
    action_payload: Dict[str, Any],
    session_id: str,
    signature: str,
    execution_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """888 FORGE: execute action payload behind sovereign control gates."""
    blocked = validate_input(
        "forge_hand",
        {"action_payload": action_payload, "session_id": session_id, "signature": signature},
    )
    if blocked:
        return wrap_tool_output("forge_hand", blocked)
    missing = require_session("forge_hand", session_id)
    if missing:
        return wrap_tool_output("forge_hand", missing)
    payload = await legacy.sovereign_actuator.fn(
        action_payload=action_payload,
        signed_tensor={},
        execution_context=execution_context or {},
        signature=signature,
        session_id=session_id,
        idempotency_key=f"forge-{session_id}",
    )
    return wrap_tool_output("forge_hand", payload)


@mcp.tool(name="seal_vault")
async def seal_vault(session_id: str, summary: str, verdict: str = "SEAL") -> Dict[str, Any]:
    """999 SEAL: commit immutable session decision record."""
    blocked = validate_input("seal_vault", {"session_id": session_id, "summary": summary})
    if blocked:
        return wrap_tool_output("seal_vault", blocked)
    missing = require_session("seal_vault", session_id)
    if missing:
        return wrap_tool_output("seal_vault", missing)
    payload = await legacy.vault_seal.fn(session_id=session_id, summary=summary, verdict=verdict)
    return wrap_tool_output("seal_vault", payload)


@mcp.tool(name="search_reality")
async def search_reality(query: str, intent: str = "general") -> Dict[str, Any]:
    """External evidence discovery (read-only)."""
    blocked = validate_input("search_reality", {"query": query})
    if blocked:
        return wrap_tool_output("search_reality", blocked)
    payload = await legacy.search.fn(query=query, intent=intent)
    return wrap_tool_output("search_reality", payload)


@mcp.tool(name="fetch_content")
async def fetch_content(id: str, max_chars: int = 4000) -> Dict[str, Any]:
    """Fetch raw evidence content (read-only)."""
    blocked = validate_input("fetch_content", {"id": id})
    if blocked:
        return wrap_tool_output("fetch_content", blocked)
    payload = await legacy.fetch.fn(id=id, max_chars=max_chars)
    return wrap_tool_output("fetch_content", payload)


@mcp.tool(name="inspect_file")
async def inspect_file(
    path: str = ".",
    depth: int = 1,
    include_hidden: bool = False,
    pattern: str = "*",
    min_size_bytes: int = 0,
    max_files: int = 100,
) -> Dict[str, Any]:
    """Inspect local filesystem structure and metadata (read-only)."""
    blocked = validate_input("inspect_file", {"path": path})
    if blocked:
        return wrap_tool_output("inspect_file", blocked)
    payload = fs_inspect(
        path=path,
        depth=depth,
        include_hidden=include_hidden,
        pattern=pattern,
        min_size_bytes=min_size_bytes,
        max_files=max_files,
    )
    return wrap_tool_output("inspect_file", payload)


@mcp.tool(name="audit_rules")
async def audit_rules(audit_scope: str = "quick", verify_floors: bool = True) -> Dict[str, Any]:
    """Run constitutional/system rule audit checks (read-only)."""
    blocked = validate_input("audit_rules", {"audit_scope": audit_scope})
    if blocked:
        return wrap_tool_output("audit_rules", blocked)
    payload = await legacy.system_audit.fn(audit_scope=audit_scope, verify_floors=verify_floors)
    return wrap_tool_output("audit_rules", payload)


@mcp.tool(name="check_vital")
async def check_vital(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> Dict[str, Any]:
    """Read system health telemetry (CPU, memory, IO/thermal optional)."""
    payload = get_system_health(
        include_swap=include_swap,
        include_io=include_io,
        include_temp=include_temp,
    )
    return wrap_tool_output("check_vital", payload)


def create_aaa_mcp_server() -> Any:
    return mcp


@mcp.resource(
    "arifos://aaa/schemas",
    name="arifos_aaa_tool_schemas",
    mime_type="application/json",
    description="Canonical AAA MCP 13-tool schema/contract overview.",
)
def aaa_tool_schemas() -> Dict[str, Any]:
    discovery = build_surface_discovery(AAA_TOOLS)
    return {
        "tool_count": 13,
        "surface": AAA_TOOLS,
        "trinity": {
            "Delta": [
                "anchor_session",
                "reason_mind",
                "search_reality",
                "fetch_content",
                "inspect_file",
                "audit_rules",
            ],
            "Omega": ["recall_memory", "simulate_heart", "critique_thought", "check_vital"],
            "Psi": ["judge_soul", "forge_hand", "seal_vault"],
        },
        "axioms": ["A1_TRUTH_COST", "A2_SCAR_WEIGHT", "A3_ENTROPY_WORK"],
        "laws_13": LAW_13_CATALOG,
        "apex_g_map": TOOL_DIALS_MAP,
        "discovery": discovery,
    }


@mcp.resource(
    "arifos://aaa/full-context-pack",
    name="arifos_aaa_full_context_pack",
    mime_type="application/json",
    description="Full-context orchestration metadata (stage spine, prompts, resources).",
)
def aaa_full_context_pack() -> Dict[str, Any]:
    return export_full_context_pack()


@mcp.prompt(name="arifos.prompt.aaa_chain")
def aaa_chain_prompt(query: str, actor_id: str = "user") -> str:
    return (
        "Use AAA 13-tool chain with continuity: "
        "anchor_session -> reason_mind -> simulate_heart -> critique_thought -> "
        "judge_soul -> seal_vault. "
        f"query={query!r}; actor_id={actor_id!r}."
    )


__all__ = [
    "mcp",
    "create_aaa_mcp_server",
    "aaa_tool_schemas",
    "aaa_full_context_pack",
    "aaa_chain_prompt",
]
