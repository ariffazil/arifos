"""
aclip_cai/mcp_bridge.py
=======================

MCP Bridge for ACLIP_CAI 9-Tool Nervous System.

This module registers ACLIP_CAI tools as MCP tools that can be called
by the aaa-mcp 9-law pipeline. All tools are exposed with the `aclip_`
prefix to distinguish them from constitutional tools.

Integration Pattern:
--------------------
aaa-mcp pipeline -> detects infrastructure query -> calls aclip_* tool ->
data returned to pipeline -> constitutional evaluation (if needed)

The 9-Law Pipeline uses ACLIP_CAI tools at specific stages:
- Law 3 (Ground): system_health, fs_inspect, config_flags
- Law 5 (Search): chroma_query, log_tail
- Law 7 (Guard): forge_guard gating decisions
"""

from typing import Optional, Any
import json

from aaa_mcp.server import mcp
from aaa_mcp.core.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.services.constitutional_metrics import ConflictStatus

from .console_tools import (
    system_health,
    process_list,
    fs_inspect,
    log_tail,
    net_status,
    config_flags,
    chroma_query,
    cost_estimator,
    forge_guard,
)


# =============================================================================
# MCP Tool Wrappers
# =============================================================================

@mcp.tool()
async def aclip_system_health(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Retrieve system health metrics (CPU, memory, disk).
    
    Console-only tool. No constitutional floors. Fast system introspection.
    
    Args:
        include_swap: Include swap/memory statistics
        include_io: Include disk I/O statistics
        include_temp: Include thermal readings
    
    Returns:
        System metrics with latency and timestamp
    """
    result = await system_health(
        include_swap=include_swap,
        include_io=include_io,
        include_temp=include_temp,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_process_list(
    filter_name: Optional[str] = None,
    filter_user: Optional[str] = None,
    min_cpu_percent: float = 0.0,
    min_memory_mb: float = 0.0,
    limit: int = 50,
    include_threads: bool = False,
) -> dict:
    """
    [ACLIP_CAI] List and filter system processes.
    
    Console-only tool. No constitutional floors. Process introspection.
    
    Args:
        filter_name: Filter by process name (substring match)
        filter_user: Filter by username
        min_cpu_percent: Minimum CPU percentage threshold
        min_memory_mb: Minimum memory usage in MB
        limit: Maximum number of processes to return
        include_threads: Include thread count per process
    
    Returns:
        Filtered process list with resource usage
    """
    result = await process_list(
        filter_name=filter_name,
        filter_user=filter_user,
        min_cpu_percent=min_cpu_percent,
        min_memory_mb=min_memory_mb,
        limit=limit,
        include_threads=include_threads,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_fs_inspect(
    path: str = "/root/arifOS",
    max_depth: int = 2,
    include_hidden: bool = False,
    min_size_bytes: int = 0,
    pattern: Optional[str] = None,
    max_files: int = 100,
) -> dict:
    """
    [ACLIP_CAI] Inspect filesystem structure and file metadata.
    
    Console-only tool. No constitutional floors. Filesystem introspection.
    
    Args:
        path: Root path to inspect
        max_depth: Maximum directory depth to traverse
        include_hidden: Include hidden files
        min_size_bytes: Minimum file size to include
        pattern: Glob pattern to filter files (e.g., "*.py")
        max_files: Maximum files to return
    
    Returns:
        File tree with metadata
    """
    result = await fs_inspect(
        path=path,
        max_depth=max_depth,
        include_hidden=include_hidden,
        min_size_bytes=min_size_bytes,
        pattern=pattern,
        max_files=max_files,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_log_tail(
    log_path: str,
    lines: int = 50,
    grep_pattern: Optional[str] = None,
    since_minutes: Optional[int] = None,
) -> dict:
    """
    [ACLIP_CAI] Tail and search log files.
    
    Console-only tool. No constitutional floors. Log introspection.
    
    Args:
        log_path: Path to log file
        lines: Number of lines to retrieve
        grep_pattern: Filter lines matching regex pattern
        since_minutes: Only return lines from last N minutes
    
    Returns:
        Log entries with parsed metadata
    """
    result = await log_tail(
        log_path=log_path,
        lines=lines,
        grep_pattern=grep_pattern,
        since_minutes=since_minutes,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_net_status(
    check_interfaces: bool = True,
    check_connections: bool = True,
    check_routing: bool = True,
    target_host: Optional[str] = None,
) -> dict:
    """
    [ACLIP_CAI] Network connectivity and interface status.
    
    Console-only tool. No constitutional floors. Network introspection.
    
    Args:
        check_interfaces: Include network interface status
        check_connections: Include active connections
        check_routing: Include routing table
        target_host: Optional host to ping test
    
    Returns:
        Network status and diagnostics
    """
    result = await net_status(
        check_interfaces=check_interfaces,
        check_connections=check_connections,
        check_routing=check_routing,
        target_host=target_host,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_config_flags(
    config_path: Optional[str] = None,
    env_prefix: Optional[str] = "ARIFOS",
    include_secrets: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Inspect configuration files and environment variables.
    
    Console-only tool. No constitutional floors. Config introspection.
    Secrets are masked by default.
    
    Args:
        config_path: Path to config file (.json, .yaml, .env)
        env_prefix: Filter environment variables by prefix
        include_secrets: Include unmasked secrets (use with caution)
    
    Returns:
        Configuration data with safe defaults
    """
    result = await config_flags(
        config_path=config_path,
        env_prefix=env_prefix,
        include_secrets=include_secrets,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_chroma_query(
    query_text: str,
    collection_name: str = "default",
    n_results: int = 5,
    where_filter: Optional[dict] = None,
    include_embeddings: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Query ChromaDB vector store for semantic search.
    
    Console-only tool. No constitutional floors. Vector DB introspection.
    
    Args:
        query_text: Text to search for
        collection_name: ChromaDB collection name
        n_results: Number of results to return
        where_filter: Optional metadata filter
        include_embeddings: Include vector embeddings
    
    Returns:
        Semantic search results with distances
    """
    result = await chroma_query(
        query_text=query_text,
        collection_name=collection_name,
        n_results=n_results,
        where_filter=where_filter,
        include_embeddings=include_embeddings,
    )
    return result.to_dict()


@mcp.tool()
async def aclip_cost_estimator(
    operation_type: str,
    token_count: Optional[int] = None,
    compute_seconds: Optional[float] = None,
    storage_gb: Optional[float] = None,
    api_calls: Optional[int] = None,
    provider: str = "openai",
    model: str = "gpt-4",
) -> dict:
    """
    [ACLIP_CAI] Estimate costs for AI operations and infrastructure.
    
    Console-only tool. No constitutional floors. Cost projection.
    
    Args:
        operation_type: Type of operation (llm, embedding, storage, compute)
        token_count: Number of tokens
        compute_seconds: Compute time in seconds
        storage_gb: Storage usage in GB
        api_calls: Number of API calls
        provider: LLM provider (openai, anthropic, gemini)
        model: Model name for pricing
    
    Returns:
        Cost breakdown in USD
    """
    result = await cost_estimator(
        operation_type=operation_type,
        token_count=token_count,
        compute_seconds=compute_seconds,
        storage_gb=storage_gb,
        api_calls=api_calls,
        provider=provider,
        model=model,
    )
    return result.to_dict()


@mcp.tool()
@constitutional_floor("F1", "F7", "F11")  # Forge guard needs constitutional oversight
async def aclip_forge_guard(
    action: str,
    target: str,
    session_id: str,
    risk_level: str = "low",
    justification: str = "",
    dry_run: bool = True,
    require_approval: bool = False,
) -> dict:
    """
    [ACLIP_CAI] Forge guard — gating decisions for system modifications.
    
    The ONLY ACLIP_CAI tool with constitutional floors (F1, F7, F11).
    Evaluates and gates actions that modify system state.
    
    Args:
        action: Action to evaluate (deploy, modify, delete, execute)
        target: Target resource (path, service, config)
        session_id: aaa-mcp session ID
        risk_level: Assessed risk level (low/medium/high/critical)
        justification: Reason for the action
        dry_run: Only evaluate without executing
        require_approval: Mandate human approval
    
    Returns:
        Verdict (SEAL/VOID/PARTIAL/SABAR/888_HOLD) with recommendations
    """
    result = await forge_guard(
        action=action,
        target=target,
        session_id=session_id,
        risk_level=risk_level,
        justification=justification,
        dry_run=dry_run,
        require_approval=require_approval,
    )
    
    # Wrap in constitutional envelope
    response = result.to_dict()
    response["motto"] = "DITEMPA BUKAN DIBERI 🔥"
    response["floors_enforced"] = get_tool_floors("aclip_forge_guard")
    response["pass"] = "forward" if result.data.get("can_proceed") else "hold"
    
    return response


# =============================================================================
# Registration Function
# =============================================================================

def register_aclip_tools(mcp_server: Any) -> None:
    """
    Register all ACLIP_CAI tools with an MCP server instance.
    
    This is called during aaa-mcp server initialization to expose
    the 9-tool nervous system to the 9-law pipeline.
    
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
    
    return None
