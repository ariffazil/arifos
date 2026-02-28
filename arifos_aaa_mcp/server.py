"""arifOS AAA MCP public 13-tool surface.

This package is the canonical external interface.
Legacy `aaa_mcp` and `aclip_cai` remain internal intelligence providers.
"""

from __future__ import annotations

import json
from typing import Any

from fastmcp import FastMCP

from aaa_mcp import server as legacy
from aaa_mcp.protocol.aaa_contract import MANIFEST_VERSION
from aaa_mcp.protocol.public_surface import (
    PUBLIC_CANONICAL_TOOLS,
    PUBLIC_PROMPT_NAMES,
    PUBLIC_RESOURCE_URIS,
)
from aaa_mcp.protocol.tool_registry import export_full_context_pack
from aclip_cai.triad import align
from aclip_cai.tools.fs_inspector import fs_inspect
from aclip_cai.tools.system_monitor import get_system_health

from .contracts import require_session, validate_input
from .fastmcp_ext.discovery import build_surface_discovery
from .governance import LAW_13_CATALOG, TOOL_DIALS_MAP, wrap_tool_output

mcp = FastMCP(
    "arifOS_AAA_MCP",
    instructions=(
        "Canonical 13-tool arifOS AAA MCP surface. "
        "Use 000->333->555->666->777_EUREKA_FORGE->888_APEX_JUDGE->999 governance spine."
    ),
)

AAA_TOOLS = list(PUBLIC_CANONICAL_TOOLS)
_SESSION_GOVERNANCE_TOKENS: dict[str, str] = {}


def _model_flags(plan: dict[str, Any], context: str = "") -> dict[str, Any]:
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
    auth_token: str | None = None,
    mode: str = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
) -> dict[str, Any]:
    """000 BOOTLOADER: initialize constitutional execution kernel and governance context."""
    blocked = validate_input("anchor_session", {"query": query, "actor_id": actor_id})
    if blocked:
        return wrap_tool_output("anchor_session", blocked)
    payload = await legacy.anchor_session.fn(
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
    grounding: list[dict[str, Any]] | None = None,
    capability_modules: list[str] | None = None,
    debug: bool = False,
) -> dict[str, Any]:
    """333 REASON: run AGI cognition with grounding and budget controls."""
    blocked = validate_input("reason_mind", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("reason_mind", blocked)
    missing = require_session("reason_mind", session_id)
    if missing:
        return wrap_tool_output("reason_mind", missing)
    payload = await legacy.reason_mind.fn(
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
) -> dict[str, Any]:
    """444 EVIDENCE: retrieve associative memory traces for current thought."""
    blocked = validate_input(
        "recall_memory",
        {"current_thought_vector": current_thought_vector, "session_id": session_id},
    )
    if blocked:
        return wrap_tool_output("recall_memory", blocked)
    missing = require_session("recall_memory", session_id)
    if missing:
        return wrap_tool_output("recall_memory", missing)
    payload = await legacy.recall_memory.fn(
        current_thought_vector=current_thought_vector,
        session_id=session_id,
        debug=debug,
    )
    return wrap_tool_output("recall_memory", payload)


@mcp.tool(name="simulate_heart")
async def simulate_heart(
    query: str,
    session_id: str,
    stakeholders: list[str] | None = None,
    capability_modules: list[str] | None = None,
    debug: bool = False,
) -> dict[str, Any]:
    """555 EMPATHY: evaluate stakeholder impact and care constraints."""
    blocked = validate_input("simulate_heart", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("simulate_heart", blocked)
    missing = require_session("simulate_heart", session_id)
    if missing:
        return wrap_tool_output("simulate_heart", missing)
    payload = await legacy.simulate_heart.fn(
        query=query,
        session_id=session_id,
        stakeholders=stakeholders,
        capability_modules=capability_modules,
        debug=debug,
    )
    return wrap_tool_output("simulate_heart", payload)


@mcp.tool(name="critique_thought")
async def critique_thought(
    plan: dict[str, Any], session_id: str, context: str = ""
) -> dict[str, Any]:
    """666 ALIGN: run 7-model critique (inversion, framing, non-linearity, etc.)."""
    blocked = validate_input("critique_thought", {"plan": plan, "session_id": session_id})
    if blocked:
        return wrap_tool_output("critique_thought", blocked)
    missing = require_session("critique_thought", session_id)
    if missing:
        return wrap_tool_output("critique_thought", missing)
    flags = _model_flags(plan, context=context)
    failed = [k for k, v in flags.items() if not v]
    critique_text = context.strip() or json.dumps(plan, ensure_ascii=True, sort_keys=True)
    payload: dict[str, Any] = {
        "verdict": "SEAL" if not failed else "SABAR",
        "session_id": session_id,
        "stage": "666_ALIGN",
        "mental_models": flags,
        "failed_models": failed,
        "critique_backend": "heuristic_fallback",
    }
    try:
        align_result = await align(session_id=session_id, action=critique_text)
        if isinstance(align_result, dict):
            payload.update(
                {
                    "verdict": str(align_result.get("verdict", payload["verdict"])),
                    "recommendation": align_result.get("recommendation"),
                    "alignment_status": align_result.get("status"),
                    "alignment_backend_result": align_result,
                    "critique_backend": "triad_align",
                }
            )
            if failed and payload["verdict"] == "SEAL":
                payload["verdict"] = "PARTIAL"
    except Exception as exc:
        payload["critique_backend_error"] = str(exc)
    return wrap_tool_output("critique_thought", payload)


@mcp.tool(name="apex_judge")
async def apex_judge(
    session_id: str,
    query: str,
    agi_result: dict[str, Any] | None = None,
    asi_result: dict[str, Any] | None = None,
    critique_result: dict[str, Any] | None = None,
    proposed_verdict: str = "SEAL",
    human_approve: bool = False,
    debug: bool = False,
) -> dict[str, Any]:
    """888 APEX JUDGE METABOLIC: sovereign constitutional verdict synthesis."""
    blocked = validate_input("apex_judge", {"session_id": session_id, "query": query})
    if blocked:
        return wrap_tool_output("apex_judge", blocked)
    missing = require_session("apex_judge", session_id)
    if missing:
        return wrap_tool_output("apex_judge", missing)
    payload = await legacy.apex_judge.fn(
        session_id=session_id,
        query=query,
        agi_result=agi_result,
        asi_result=asi_result,
        implementation_details={"critique": critique_result or {}},
        proposed_verdict=proposed_verdict,
        human_approve=human_approve,
        debug=debug,
    )
    if isinstance(payload, dict):
        token = payload.get("governance_token")
        if isinstance(token, str) and token.strip():
            _SESSION_GOVERNANCE_TOKENS[session_id] = token.strip()
        stage_value = str(payload.get("stage", "")).upper()
        if stage_value in {"", "777-888", "777-888_APEX", "888_AUDIT", "888_JUDGE"}:
            payload["stage"] = "888_APEX_JUDGE"
            if stage_value:
                payload["stage_legacy"] = stage_value
    return wrap_tool_output("apex_judge", payload)


@mcp.tool(name="eureka_forge")
async def eureka_forge(
    session_id: str,
    command: str,
    working_dir: str = "/root",
    timeout: int = 60,
    confirm_dangerous: bool = False,
    agent_id: str = "unknown",
    purpose: str = "",
) -> dict[str, Any]:
    """777 EUREKA FORGE: execute shell commands with audit logging and confirmation for dangerous operations.
    
    F5: Safe defaults (validates working_dir)
    F6: Comprehensive error handling
    F7: Risk classification (LOW/MODERATE/CRITICAL)
    F9: Transparent logging with agent_id and purpose
    
    Dangerous commands (rm -rf, mkfs, dd, etc.) require confirm_dangerous=True
    """
    blocked = validate_input(
        "eureka_forge",
        {"session_id": session_id, "command": command, "agent_id": agent_id},
    )
    if blocked:
        return wrap_tool_output("eureka_forge", blocked)
    missing = require_session("eureka_forge", session_id)
    if missing:
        return wrap_tool_output("eureka_forge", missing)
    payload = await legacy.eureka_forge.fn(
        session_id=session_id,
        command=command,
        working_dir=working_dir,
        timeout=timeout,
        confirm_dangerous=confirm_dangerous,
        agent_id=agent_id,
        purpose=purpose,
    )
    if isinstance(payload, dict):
        stage_value = str(payload.get("stage", "")).upper()
        if stage_value in {"", "888_FORGE", "777_FORGE", "777_EXECUTE"}:
            payload["stage"] = "777_EUREKA_FORGE"
            if stage_value:
                payload["stage_legacy"] = stage_value
    return wrap_tool_output("eureka_forge", payload)


@mcp.tool(name="seal_vault")
async def seal_vault(
    session_id: str,
    summary: str,
    verdict: str = "SEAL",
    governance_token: str | None = None,
) -> dict[str, Any]:
    """999 SEAL: commit immutable session decision record."""
    blocked = validate_input("seal_vault", {"session_id": session_id, "summary": summary})
    if blocked:
        return wrap_tool_output("seal_vault", blocked)
    missing = require_session("seal_vault", session_id)
    if missing:
        return wrap_tool_output("seal_vault", missing)

    resolved_token = ""
    if isinstance(governance_token, str) and governance_token.strip():
        resolved_token = governance_token.strip()
    elif session_id in _SESSION_GOVERNANCE_TOKENS:
        resolved_token = _SESSION_GOVERNANCE_TOKENS[session_id]
    else:
        # Backend convenience path: mint token from APEX so humans never copy opaque strings.
        auto_judge = await legacy.apex_judge.fn(
            session_id=session_id,
            query=summary,
            proposed_verdict=verdict,
            human_approve=False,
            implementation_details={"source": "seal_vault_auto_token"},
        )
        auto_token = auto_judge.get("governance_token") if isinstance(auto_judge, dict) else ""
        if isinstance(auto_token, str) and auto_token.strip():
            resolved_token = auto_token.strip()
            _SESSION_GOVERNANCE_TOKENS[session_id] = resolved_token

    if not resolved_token:
        return wrap_tool_output(
            "seal_vault",
            {
                "verdict": "VOID",
                "stage": "999_SEAL",
                "session_id": session_id,
                "error": "Missing governance_token for seal_vault",
                "remediation": "Call apex_judge first in this session, then retry seal_vault.",
            },
        )

    payload = await legacy.seal_vault.fn(
        session_id=session_id,
        summary=summary,
        governance_token=resolved_token,
    )
    return wrap_tool_output("seal_vault", payload)


@mcp.tool(name="search_reality")
async def search_reality(query: str, intent: str = "general") -> dict[str, Any]:
    """External evidence discovery (read-only)."""
    blocked = validate_input("search_reality", {"query": query})
    if blocked:
        return wrap_tool_output("search_reality", blocked)
    payload = await legacy.search_reality.fn(query=query, intent=intent)
    return wrap_tool_output("search_reality", payload)


@mcp.tool(name="fetch_content")
async def fetch_content(id: str, max_chars: int = 4000) -> dict[str, Any]:
    """Fetch raw evidence content (read-only)."""
    blocked = validate_input("fetch_content", {"id": id})
    if blocked:
        return wrap_tool_output("fetch_content", blocked)
    payload = await legacy.fetch_content.fn(id=id, max_chars=max_chars)
    return wrap_tool_output("fetch_content", payload)


@mcp.tool(name="inspect_file")
async def inspect_file(
    path: str = ".",
    depth: int = 1,
    include_hidden: bool = False,
    pattern: str = "*",
    min_size_bytes: int = 0,
    max_files: int = 100,
) -> dict[str, Any]:
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
async def audit_rules(audit_scope: str = "quick", verify_floors: bool = True) -> dict[str, Any]:
    """Run constitutional/system rule audit checks (read-only)."""
    blocked = validate_input("audit_rules", {"audit_scope": audit_scope})
    if blocked:
        return wrap_tool_output("audit_rules", blocked)
    payload = await legacy.audit_rules.fn(audit_scope=audit_scope, verify_floors=verify_floors)
    return wrap_tool_output("audit_rules", payload)


@mcp.tool(name="check_vital")
async def check_vital(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> dict[str, Any]:
    """Read system health telemetry (CPU, memory, IO/thermal optional)."""
    payload = get_system_health(
        include_swap=include_swap,
        include_io=include_io,
        include_temp=include_temp,
    )
    return wrap_tool_output("check_vital", payload)


def create_aaa_mcp_server() -> Any:
    # ABI version guard: prevent silent half-upgrades between transport and kernel layers.
    try:
        from aaa_mcp.server import MANIFEST_VERSION as inner_version  # type: ignore[attr-defined]

        if inner_version != MANIFEST_VERSION:
            import sys

            print(
                f"[arifOS] MANIFEST_VERSION MISMATCH: "
                f"aaa_mcp={inner_version} vs arifos_aaa_mcp={MANIFEST_VERSION}. "
                "Restart the server after updating both layers.",
                file=sys.stderr,
            )
    except ImportError:
        pass  # aaa_mcp not installed — ignore guard in test isolation
    return mcp


@mcp.resource(
    PUBLIC_RESOURCE_URIS["schemas"],
    name="arifos_aaa_tool_schemas",
    mime_type="application/json",
    description="Canonical AAA MCP 13-tool schema/contract overview.",
)
def aaa_tool_schemas() -> str:
    discovery = build_surface_discovery(AAA_TOOLS)
    payload = {
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
            "Psi": ["apex_judge", "eureka_forge", "seal_vault"],
        },
        "axioms": ["A1_TRUTH_COST", "A2_SCAR_WEIGHT", "A3_ENTROPY_WORK"],
        "technical_aliases": {
            "13_floors": "governance_rules",
            "333_axioms": "reasoning_constraints",
            "apex_dials": "decision_parameters",
            "eureka_forge": "action_actuator",
            "vault999": "immutable_ledger",
        },
        "laws_13": LAW_13_CATALOG,
        "apex_g_map": TOOL_DIALS_MAP,
        "discovery": discovery,
    }
    # FastMCP resources must return str/bytes or ResourceContent.
    return json.dumps(payload, ensure_ascii=True)


@mcp.resource(
    PUBLIC_RESOURCE_URIS["full_context_pack"],
    name="arifos_aaa_full_context_pack",
    mime_type="application/json",
    description="Full-context orchestration metadata (stage spine, prompts, resources).",
)
def aaa_full_context_pack() -> str:
    return json.dumps(export_full_context_pack(), ensure_ascii=True)


@mcp.prompt(name=PUBLIC_PROMPT_NAMES["aaa_chain"])
def aaa_chain_prompt(query: str, actor_id: str = "user") -> str:
    return (
        "Use AAA 13-tool chain with continuity: "
        "anchor_session -> reason_mind -> simulate_heart -> critique_thought -> "
        "apex_judge -> seal_vault (token is handled by backend). "
        f"query={query!r}; actor_id={actor_id!r}."
    )


# ── REST routes (custom HTTP endpoints alongside MCP at /mcp) ──────────
# Registered here so they're available when mcp.run(transport="http") creates
# the Starlette app.  Each route is added via mcp.custom_route() which appends
# to mcp._additional_http_routes — picked up by create_streamable_http_app().
from .rest_routes import register_rest_routes

_TOOL_REGISTRY = {
    "anchor_session": anchor_session,
    "reason_mind": reason_mind,
    "recall_memory": recall_memory,
    "simulate_heart": simulate_heart,
    "critique_thought": critique_thought,
    "apex_judge": apex_judge,
    "eureka_forge": eureka_forge,
    "seal_vault": seal_vault,
    "search_reality": search_reality,
    "fetch_content": fetch_content,
    "inspect_file": inspect_file,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
}

register_rest_routes(mcp, _TOOL_REGISTRY)


__all__ = [
    "mcp",
    "create_aaa_mcp_server",
    "aaa_tool_schemas",
    "aaa_full_context_pack",
    "aaa_chain_prompt",
]
