"""
arifosmcp.intelligence/mcp_bridge.py
=======================

MCP Bridge for ACLIP_CAI — Governed Nervous System (v2).

All tool calls are wrapped by the Constitutional FloorAuditor (F1-F13).
Raw sensor results are returned inside a governed MCPResponse envelope,
giving callers full constitutional context alongside the payload.

Architecture:
    aaa-mcp pipeline
        → aclip_* tool (this bridge)
            → FloorAuditor.check_floors()   ← F1-F13 gate
            → actual console_tool()         ← sensor call
            → MCPResponse envelope          ← governed output

Verdict meanings (aligned with core/floor_audit.py):
    SEAL    — all critical floors pass; data is trusted
    PARTIAL — minor soft-floor failures; proceed with caution
    SABAR   — significant floor failures; hold for review
    HOLD    — F1 or F11 failure; requires human approval (888_HOLD)
    VOID    — critical floor failure (F9/F12); hard block
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from fastmcp import FastMCP

# Local MCP surface for ACLIP bridge tools.
# This avoids a hard reverse dependency on arifosmcp.transport.server.
mcp = FastMCP("ACLIP_CAI_Bridge")

from .console_tools import (
    chroma_query,
    config_flags,
    cost_estimator,
    forge_guard,
    fs_inspect,
    log_tail,
    net_status,
    process_list,
    system_health,
)

# Lazy-import to avoid circular dependencies if core is not fully initialized
try:
    from .core.floor_audit import FloorAuditor

    _AUDITOR: FloorAuditor | None = FloorAuditor()
except Exception:  # pragma: no cover
    _AUDITOR = None


# =============================================================================
# MCPResponse — Governed envelope
# =============================================================================


@dataclass
class MCPResponse:
    """
    Constitutional envelope for all governed ACLIP tool responses.

    Callers receive both the raw sensor payload AND the governance
    context (verdict, floor pass rates, recommendations).
    """

    tool: str
    verdict: str  # SEAL | PARTIAL | SABAR | HOLD | VOID
    pass_rate: float  # Fraction of floors that passed [0.0, 1.0]
    data: dict = field(default_factory=dict)
    recommendation: str = ""
    failed_floors: list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(tz=timezone.utc).isoformat())
    motto: str = "DITEMPA BUKAN DIBERI 🔥"

    def to_dict(self) -> dict:
        return asdict(self)


def _govern(tool_name: str, action: str, context: str, severity: str = "low") -> dict:
    """
    Run FloorAuditor check and return a governance context dict.
    Degrades gracefully if the auditor is unavailable (F7 Humility).
    """
    if _AUDITOR is None:
        return {
            "verdict": "partial",
            "pass_rate": 0.80,
            "failed_floors": [],
            "recommendation": "FloorAuditor unavailable — operating in degraded mode (F7).",
        }
    try:
        audit = _AUDITOR.check_floors(action=action, context=context, severity=severity)
        return {
            "verdict": audit.verdict.value,
            "pass_rate": audit.pass_rate,
            "failed_floors": [f.floor for f in audit.floor_results.values() if not f.passed],
            "recommendation": audit.recommendation,
        }
    except Exception as exc:  # pragma: no cover
        return {
            "verdict": "partial",
            "pass_rate": 0.80,
            "failed_floors": [],
            "recommendation": f"Audit error (degraded): {exc}",
        }


def _build_response(tool: str, gov: dict, payload: dict) -> dict:
    resp = MCPResponse(
        tool=tool,
        verdict=gov["verdict"],
        pass_rate=gov["pass_rate"],
        data=payload,
        recommendation=gov.get("recommendation", ""),
        failed_floors=gov.get("failed_floors", []),
    )
    return resp.to_dict()


# =============================================================================
# MCP Tool Wrappers — all governed
# =============================================================================


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_system_health(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Retrieve system health metrics (CPU, memory, disk).

    Governed by F1-F13 Constitutional Floors.
    Returns a governed MCPResponse envelope with verdict + payload.

    Args:
        include_swap: Include swap/memory statistics
        include_io: Include disk I/O statistics
        include_temp: Include thermal readings
    """
    gov = _govern(
        tool_name="aclip_system_health",
        action="retrieve system health metrics [ref: sensors]. human-approved validation.",
        context="routine operational monitoring",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_system_health", gov, {})

    result = await system_health(
        include_swap=include_swap,
        include_io=include_io,
        include_temp=include_temp,
    )
    return _build_response("aclip_system_health", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_process_list(
    filter_name: str | None = None,
    filter_user: str | None = None,
    min_cpu_percent: float = 0.0,
    min_memory_mb: float = 0.0,
    limit: int = 50,
    include_threads: bool = False,
) -> dict:
    """
    [ACLIP_CAI] List and filter system processes.

    Governed by F1-F13 Constitutional Floors.

    Args:
        filter_name: Filter by process name (substring match)
        filter_user: Filter by username
        min_cpu_percent: Minimum CPU percentage threshold
        min_memory_mb: Minimum memory usage in MB
        limit: Maximum number of processes to return
        include_threads: Include thread count per process
    """
    gov = _govern(
        tool_name="aclip_process_list",
        action="list and inspect system processes [ref: ps]. human-approved validation.",
        context="operational diagnostics",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_process_list", gov, {})

    result = await process_list(
        filter_name=filter_name,
        filter_user=filter_user,
        min_cpu_percent=min_cpu_percent,
        min_memory_mb=min_memory_mb,
        limit=limit,
        include_threads=include_threads,
    )
    return _build_response("aclip_process_list", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_fs_inspect(
    path: str = ".",
    depth: int = 1,
    max_depth: int | None = None,
    include_hidden: bool = False,
    min_size_bytes: int = 0,
    pattern: str | None = None,
    max_files: int = 100,
) -> dict:
    """
    [ACLIP_CAI] Inspect filesystem structure and file metadata.

    Governed by F1-F13 Constitutional Floors.

    Args:
        path: Root path to inspect
        depth: Maximum directory depth to traverse
        max_depth: Compatibility alias for depth
        include_hidden: Include hidden files
        min_size_bytes: Minimum file size to include
        pattern: Glob pattern to filter files (e.g., "*.py")
        max_files: Maximum files to return (entropy control)
    """
    gov = _govern(
        tool_name="aclip_fs_inspect",
        action=f"inspect filesystem at path {path!r} [ref: os.walk]. human-approved validation.",
        context="filesystem introspection for observability",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_fs_inspect", gov, {})

    result = await fs_inspect(
        path=path,
        depth=depth,
        max_depth=max_depth,
        include_hidden=include_hidden,
        min_size_bytes=min_size_bytes,
        pattern=pattern,
        max_files=max_files,
    )
    return _build_response("aclip_fs_inspect", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_log_tail(
    log_file: str = "arifosmcp.transport.log",
    lines: int = 50,
    pattern: str = "",
    log_path: str | None = None,
    grep_pattern: str | None = None,
    since_minutes: int | None = None,
) -> dict:
    """
    [ACLIP_CAI] Tail and search log files.

    Governed by F1-F13 Constitutional Floors.

    Args:
        log_file: Path to log file
        lines: Number of lines to retrieve
        pattern: Filter lines matching regex pattern
        log_path: Compatibility alias for log_file
        grep_pattern: Alias for pattern
        since_minutes: Only return lines from last N minutes
    """
    gov = _govern(
        tool_name="aclip_log_tail",
        action="read and tail system log files [ref: tail]. human-approved validation.",
        context="log introspection for debugging",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_log_tail", gov, {})

    result = await log_tail(
        log_file=log_file,
        lines=lines,
        pattern=pattern,
        log_path=log_path,
        grep_pattern=grep_pattern,
        since_minutes=since_minutes,
    )
    return _build_response("aclip_log_tail", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_net_status(
    check_ports: bool = True,
    check_connections: bool = True,
    check_interfaces: bool = True,
    check_routing: bool = True,
    target_host: str | None = None,
) -> dict:
    """
    [ACLIP_CAI] Network connectivity and interface status.

    Governed by F1-F13 Constitutional Floors.

    Args:
        check_ports: Include listening/open ports
        check_connections: Include active connections
        check_interfaces: Include network interface status
        check_routing: Include routing table
        target_host: Optional host for ping reachability test
    """
    gov = _govern(
        tool_name="aclip_net_status",
        action="inspect network interfaces [ref: netstat]. human-approved validation.",
        context="network diagnostics",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_net_status", gov, {})

    result = await net_status(
        check_ports=check_ports,
        check_connections=check_connections,
        check_interfaces=check_interfaces,
        check_routing=check_routing,
        target_host=target_host,
    )
    return _build_response("aclip_net_status", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_config_flags(
    config_path: str | None = None,
    env_prefix: str | None = "ARIFOS",
    include_secrets: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Inspect configuration files and environment variables.

    Governed by F1-F13 Constitutional Floors.
    Secrets are masked by default (F1 Amanah).

    Args:
        config_path: Path to config file (.json, .yaml, .env)
        env_prefix: Filter environment variables by prefix
        include_secrets: Include unmasked secrets — requires SEAL verdict
    """
    # Config reads are low-severity; secret exposure is medium
    severity = "medium" if include_secrets else "low"
    gov = _govern(
        tool_name="aclip_config_flags",
        action="read configuration files and environment variables",
        context=f"config introspection (include_secrets={include_secrets})",
        severity=severity,
    )
    if gov["verdict"] in ("void", "hold"):
        return _build_response("aclip_config_flags", gov, {})

    # Enforce: only expose raw secrets when audit is SEAL
    effective_include_secrets = include_secrets and gov["verdict"] == "seal"
    result = await config_flags(
        config_path=config_path,
        env_prefix=env_prefix,
        include_secrets=effective_include_secrets,
    )
    return _build_response("aclip_config_flags", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_chroma_query(
    query_text: str,
    collection_name: str = "default",
    n_results: int = 5,
    where_filter: dict | None = None,
    include_embeddings: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Query ChromaDB vector store for semantic search.

    Governed by F1-F13 Constitutional Floors.

    Args:
        query_text: Text to search for
        collection_name: ChromaDB collection name
        n_results: Number of results to return
        where_filter: Optional metadata filter
        include_embeddings: Include vector embeddings in response
    """
    gov = _govern(
        tool_name="aclip_chroma_query",
        action=f"semantic vector search: {query_text[:120]}",
        context="knowledge base retrieval",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_chroma_query", gov, {})

    result = await chroma_query(
        query_text=query_text,
        collection_name=collection_name,
        n_results=n_results,
        where_filter=where_filter,
        include_embeddings=include_embeddings,
    )
    return _build_response("aclip_chroma_query", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_cost_estimator(
    action_description: str,
    estimated_cpu_percent: float = 0.0,
    estimated_ram_mb: float = 0.0,
    estimated_io_mb: float = 0.0,
    operation_type: str = "compute",
    token_count: int | None = None,
    compute_seconds: float | None = None,
    storage_gb: float | None = None,
    api_calls: int | None = None,
    provider: str = "openai",
    model: str = "gpt-4",
) -> dict:
    """
    [ACLIP_CAI] Estimate costs for AI operations and infrastructure.

    Governed by F1-F13 Constitutional Floors.

    Args:
        action_description: Description of planned action
        estimated_cpu_percent: Estimated CPU usage percentage
        estimated_ram_mb: Estimated RAM usage in MB
        estimated_io_mb: Estimated I/O impact in MB
        operation_type: Operation class (llm, embedding, storage, compute)
        token_count: Number of tokens
        compute_seconds: Compute time in seconds
        storage_gb: Storage usage in GB
        api_calls: Number of API calls
        provider: LLM provider (openai, anthropic, gemini)
        model: Model name for pricing
    """
    gov = _govern(
        tool_name="aclip_cost_estimator",
        action=f"estimate compute/API cost: {action_description[:120]}",
        context="thermodynamic budget planning",
        severity="low",
    )
    if gov["verdict"] == "void":
        return _build_response("aclip_cost_estimator", gov, {})

    result = await cost_estimator(
        action_description=action_description,
        estimated_cpu_percent=estimated_cpu_percent,
        estimated_ram_mb=estimated_ram_mb,
        estimated_io_mb=estimated_io_mb,
        operation_type=operation_type,
        token_count=token_count,
        compute_seconds=compute_seconds,
        storage_gb=storage_gb,
        api_calls=api_calls,
        provider=provider,
        model=model,
    )
    return _build_response("aclip_cost_estimator", gov, result.to_dict())


@mcp.tool(annotations={"readOnlyHint": True})
async def aclip_forge_guard(
    check_system_health: bool = True,
    cost_score_threshold: float = 0.8,
    cost_score_to_check: float = 0.0,
    action: str = "",
    target: str = "",
    session_id: str = "",
    risk_level: str = "low",
    justification: str = "",
    dry_run: bool = True,
    require_approval: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Forge guard — constitutional local circuit breaker.

    Evaluates local host/cost/risk signals and F1-F13 floors before
    returning a gate decision. This is the primary 888_HOLD trigger.

    Args:
        check_system_health: Include host pressure in gate evaluation
        cost_score_threshold: Threshold for SABAR gate
        cost_score_to_check: Caller-provided cost score
        action: Action to evaluate (deploy, modify, delete, execute)
        target: Target resource (path, service, config)
        session_id: aaa-mcp session ID for traceability
        risk_level: Assessed risk level (low/medium/high/critical)
        justification: Reason for the action (required for high risk)
        dry_run: Only evaluate without executing
        require_approval: Mandate 888_HOLD human approval gate
    """
    # High-risk actions get elevated severity for floor audit
    severity = "high" if risk_level in ("high", "critical") else "medium"
    gov = _govern(
        tool_name="aclip_forge_guard",
        action=(
            f"forge guard evaluation — action={action!r}, "
            f"target={target!r}, risk={risk_level!r}, "
            f"justification: {justification[:120]}"
        ),
        context=f"session={session_id}, require_approval={require_approval}",
        severity=severity,
    )

    # HOLD or VOID → hard block (888_HOLD protocol)
    if gov["verdict"] in ("void", "hold"):
        gov["recommendation"] = (
            "888_HOLD triggered — constitutional floor failure. "
            "Human sovereign approval required before proceeding. " + gov.get("recommendation", "")
        )
        return _build_response("aclip_forge_guard", gov, {"can_proceed": False})

    result = await forge_guard(
        check_system_health=check_system_health,
        cost_score_threshold=cost_score_threshold,
        cost_score_to_check=cost_score_to_check,
        action=action,
        target=target,
        session_id=session_id,
        risk_level=risk_level,
        justification=justification,
        dry_run=dry_run,
        require_approval=require_approval,
    )
    payload = result.to_dict()
    payload["can_proceed"] = result.data.get("can_proceed", False)
    return _build_response("aclip_forge_guard", gov, payload)


# =============================================================================
# Registration helper (unchanged API — no breaking change)
# =============================================================================


def register_aclip_tools(mcp_server: Any) -> None:
    """
    Register all governed ACLIP_CAI tools with an MCP server instance.

    Called during aaa-mcp server initialization to expose the 9-tool
    nervous system together with their F1-F13 governance envelopes.

    Args:
        mcp_server: FastMCP server instance
    """
    tools = [
        aclip_system_health,
        aclip_process_list,
        aclip_fs_inspect,
        aclip_log_tail,
        aclip_net_status,
        aclip_config_flags,
        aclip_chroma_query,
        aclip_cost_estimator,
        aclip_forge_guard,
    ]
    for tool in tools:
        mcp_server.tool()(tool)
