"""arifOS AAA MCP public 13-tool surface.

This package is the canonical external interface.
Legacy `aaa_mcp` and `aclip_cai` remain internal intelligence providers.

PHASE 1 WIRING: Thermodynamic Core Integration
- All tools routed through core/ constitutional cage
- Physics exceptions caught and converted to VOID envelopes
- Tri-Witness vectors mapped for Ω_ortho calculation
"""

from __future__ import annotations

import json
import time
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

# ═══════════════════════════════════════════════════════
# PHASE 1: Wire MCP Gateway to Thermodynamic Core
# ═══════════════════════════════════════════════════════

# Import core thermodynamic cage
try:
    from core.physics.thermodynamics import (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        check_landauer_bound,
        derive_orthogonality,
    )
    from core.homeostasis import (
        PeaceViolation,
        check_peace_squared,
    )
    from core.kernel.constitutional_decorator import (
        EntropyViolation,
        AmanahViolation,
        constitutional_floor,
    )
    from core.judgment import (
        get_judgment_kernel,
        JudgmentKernel,
    )

    CORE_AVAILABLE = True
except ImportError as e:
    CORE_AVAILABLE = False
    import logging

    logging.warning(f"Thermodynamic core not available: {e}")


# Physics exception to VOID envelope converter
def _convert_physics_exception_to_void(
    exception: Exception,
    tool_name: str,
    session_id: str,
) -> dict[str, Any]:
    """
    Convert thermodynamic exceptions to VOID envelopes.

    Fail-closed: Physics violations return VOID, not crash.
    """
    exception_type = type(exception).__name__

    # Map exception types to constitutional floors
    floor_map = {
        "EntropyViolation": "F4_CLARITY",
        "AmanahViolation": "F1_AMANAH",
        "ModeCollapseError": "F3_TRI_WITNESS",
        "CheapTruthError": "F2_TRUTH",
        "PeaceViolation": "F5_PEACE2",
        "ThermodynamicViolation": "PHYSICS",
    }

    floor = floor_map.get(exception_type, "UNKNOWN")

    return {
        "verdict": "VOID",
        "stage": f"{tool_name.upper()}_PHYSICS",
        "session_id": session_id,
        "blocked_by_floor": floor,
        "blocked_by_exception": exception_type,
        "reason": str(exception),
        "thermodynamic_rejection": True,
        "error_class": exception_type,
        "timestamp": time.time(),
        "remediation": {
            "action": "COOLING_REQUIRED",
            "message": f"{floor} violation detected. System requires cooling cycle.",
            "next_steps": [
                "Wait for entropy dissipation",
                "Provide additional grounding evidence",
                "Reduce query complexity",
                "Request human oversight (888_HOLD)",
            ],
        },
    }


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

    # PHASE 1: Thermodynamic core integration
    start_time = time.time()
    try:
        payload = await legacy.anchor_session.fn(
            query=query,
            actor_id=actor_id,
            auth_token=auth_token,
            mode=mode,
            grounding_required=grounding_required,
            debug=debug,
        )

        # Add compute telemetry for Landauer bound
        payload["compute_ms"] = (time.time() - start_time) * 1000
        payload["tokens"] = len(query.split())

        return wrap_tool_output("anchor_session", payload)

    except (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        PeaceViolation,
        EntropyViolation,
        AmanahViolation,
    ) as e:
        # Fail-closed: Physics violations return VOID
        return wrap_tool_output(
            "anchor_session", _convert_physics_exception_to_void(e, "anchor_session", "init")
        )


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

    # PHASE 1: Thermodynamic core integration with physics exception handling
    start_time = time.time()
    try:
        payload = await legacy.reason_mind.fn(
            query=query,
            session_id=session_id,
            grounding=grounding,
            capability_modules=capability_modules,
            debug=debug,
        )

        # Add compute telemetry for Landauer bound
        payload["compute_ms"] = (time.time() - start_time) * 1000
        payload["tokens"] = len(query.split()) + len(str(payload).split())

        # PHASE 1: Strict F4 entropy check (ΔS <= 0)
        delta_s = payload.get("dS", 0.0)
        if CORE_AVAILABLE and delta_s > 0:
            raise EntropyViolation(
                f"F4_CLARITY_VIOLATION: ΔS={delta_s:.4f} > 0 in reason_mind output"
            )

        return wrap_tool_output("reason_mind", payload)

    except (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        PeaceViolation,
        EntropyViolation,
        AmanahViolation,
    ) as e:
        # Fail-closed: Physics violations return VOID
        return wrap_tool_output(
            "reason_mind", _convert_physics_exception_to_void(e, "reason_mind", session_id)
        )


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

    # PHASE 1: Thermodynamic core integration - APEX judgment with Ψ, W₃, Φₚ
    start_time = time.time()
    try:
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

        # Add compute telemetry
        payload["compute_ms"] = (time.time() - start_time) * 1000

        # PHASE 1: Map AGI/ASI vectors for Tri-Witness (Ω_ortho calculation)
        if agi_result and asi_result:
            # Extract embedding vectors for orthogonality check
            agi_vector = agi_result.get("embedding_vector", [])
            asi_vector = asi_result.get("embedding_vector", [])
            if agi_vector and asi_vector and CORE_AVAILABLE:
                omega_ortho = derive_orthogonality(agi_vector, asi_vector)
                payload["omega_ortho"] = omega_ortho
                if omega_ortho < 0.95:
                    payload["mode_collapse_warning"] = True

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

    except (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        PeaceViolation,
        EntropyViolation,
        AmanahViolation,
    ) as e:
        # Fail-closed: Physics violations return VOID
        return wrap_tool_output(
            "apex_judge", _convert_physics_exception_to_void(e, "apex_judge", session_id)
        )


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
    # PHASE 2: Thermodynamic telemetry for ledger binding
    telemetry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """999 SEAL: commit immutable session decision record with thermodynamic telemetry."""
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

    # PHASE 2: Bind thermodynamic telemetry to ledger
    # Include Ψ, W₃, Landauer metrics in vault entry
    thermodynamic_statement = {
        "summary": summary,
        "verdict": verdict,
        "governance_token": resolved_token[:16] + "...",  # Truncated for security
        # Include telemetry if provided
        "vitality_index": telemetry.get("psi") if telemetry else None,
        "tri_witness": telemetry.get("w3") if telemetry else None,
        "paradox_conductance": telemetry.get("phi_p") if telemetry else None,
        "landauer_ratio": telemetry.get("landauer_ratio") if telemetry else None,
        "omega_ortho": telemetry.get("omega_ortho") if telemetry else None,
        "constitutional_cost": telemetry.get("constitutional_cost") if telemetry else "SEALED",
        "timestamp": time.time(),
    }

    try:
        payload = await legacy.seal_vault.fn(
            session_id=session_id,
            summary=summary,
            governance_token=resolved_token,
            thermodynamic_statement=thermodynamic_statement,  # PHASE 2: Bind telemetry
        )

        # Add thermodynamic binding confirmation
        payload["thermodynamic_seal"] = {
            "bound_to_ledger": True,
            "telemetry_included": bool(telemetry),
            "constitutional_signature": resolved_token[:8] + "...",
        }

        return wrap_tool_output("seal_vault", payload)

    except (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        PeaceViolation,
        EntropyViolation,
        AmanahViolation,
    ) as e:
        # Fail-closed: Physics violations return VOID
        return wrap_tool_output(
            "seal_vault", _convert_physics_exception_to_void(e, "seal_vault", session_id)
        )


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


@mcp.prompt(
    name="arifos_governance_brief",
    description="Reusable prompt: arifOS governance constraints and usage.",
)
async def arifos_governance_brief_prompt() -> str:
    return (
        "You are operating under arifOS constitutional governance.\n"
        "Use tools for actions; prefer reversible steps; avoid secrets leakage.\n"
        "If an operation is high-stakes or irreversible, request explicit human approval.\n"
    )


@mcp.prompt(name="arifos.prompt.trinity_forge")
def trinity_forge_prompt(query: str, actor_id: str = "user", mode: str = "conscience") -> str:
    return (
        "Use trinity_forge for full constitutional orchest with session continuity.\n"
        "Stage spine: 000 -> 222 -> 333 -> 444 -> 666 -> 888 -> 999.\n"
        "Require truthful grounding; fail closed on F2/F11/F12 with remediation.\n"
        'Call shape: {"name":"trinity_forge","arguments":{"query":%r,"actor_id":%r,"mode":%r}}'
        % (query, actor_id, mode)
    )


@mcp.prompt(name="arifos.prompt.anchor_reason")
def anchor_reason_prompt(query: str, actor_id: str = "user") -> str:
    return (
        "Run two-step constitutional flow with explicit session continuity.\n"
        "1) anchor/init_session to obtain session_id.\n"
        "2) reason/agi_cognition using same session_id.\n"
        "If VOID on F11: request auth_token or corrected actor_id.\n"
        "If VOID on F2: request external evidence before retry.\n"
        "Input query: %s\nActor: %s" % (query, actor_id)
    )


@mcp.prompt(name="arifos.prompt.audit_then_seal")
def audit_then_seal_prompt(session_id: str, summary: str, proposed_verdict: str = "SEAL") -> str:
    return (
        "Finalize governed decision in two steps.\n"
        "1) apex_verdict/audit with session_id and explicit proposed_verdict.\n"
        "2) vault_seal with same session_id and immutable summary.\n"
        "If verdict is 888_HOLD, stop and request human ratification before seal.\n"
        "session_id=%s; proposed_verdict=%s; summary=%s" % (session_id, proposed_verdict, summary)
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
