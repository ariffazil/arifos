"""
aclip_cai/console_tools.py
==========================

The 9-Sense Nervous System — Console Intelligence Implementation.

All tools are:
- Console-only (no ethics/ASI layer)
- Read-only (except forge_guard gating decisions)
- Fast (< 100ms response time target)
- Structured JSON output
- Fail-closed with explicit error envelopes

Design Principles:
------------------
1. No constitutional floors (these are infrastructure tools)
2. No emotional/empathy processing
3. Pure data retrieval and system inspection
4. Forge_guard is the only exception: it makes gating decisions
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

import aclip_cai.tools as internal_tools

# =============================================================================
# Shared Types and Utilities
# =============================================================================


@dataclass
class ToolResponse:
    """Standard response envelope for all ACLIP_CAI tools."""

    tool: str
    status: str  # "ok" | "error" | "warning"
    timestamp: str
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    latency_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _now() -> str:
    """ISO 8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


def _wrap_tool(tool_name: str, start_time: float, result: dict[str, Any]) -> ToolResponse:
    """Consistently maps internal aclip_base results to ToolResponse."""
    status_map = {"SEAL": "ok", "PARTIAL": "ok", "VOID": "error"}

    # Extract status and error/warning
    gate_status = result.get("status", "VOID")
    status = status_map.get(gate_status, "error")

    # Error message logic
    error_msg = result.get("error")
    if gate_status == "PARTIAL" and not error_msg:
        error_msg = result.get("warning")

    # Data is everything except metadata keys
    meta_keys = {"status", "error", "warning", "hint", "timestamp"}
    data = {k: v for k, v in result.items() if k not in meta_keys}

    return ToolResponse(
        tool=tool_name,
        status=status,
        timestamp=_now(),
        data=data,
        error=error_msg,
        latency_ms=round((time.perf_counter() - start_time) * 1000, 2),
    )


def _run_cmd(cmd: list[str], timeout: float = 5.0) -> tuple[str, str, int]:
    # ... (keeping it for legacy if needed, but tools should ideally use internal ones)

    """Execute shell command with timeout. Returns (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout}s", 124
    except Exception as e:
        return "", str(e), 1


def _parse_size(size_str: str) -> int:
    """Parse human-readable size to bytes."""
    units = {"B": 1, "K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}
    size_str = size_str.strip().upper()
    for suffix, multiplier in units.items():
        if size_str.endswith(suffix):
            try:
                return int(float(size_str[:-1]) * multiplier)
            except ValueError:
                return 0
    try:
        return int(size_str)
    except ValueError:
        return 0


# =============================================================================
# Tool 1: system_health — System Resource Metrics
# =============================================================================


async def system_health(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> ToolResponse:
    """Retrieve comprehensive system health metrics using psutil."""
    start = time.perf_counter()
    res = internal_tools.system_health(
        include_swap=include_swap,
        include_io=include_io,
        include_temp=include_temp,
    )
    return _wrap_tool("system_health", start, res)



# =============================================================================
# Tool 2: process_list — Process Inspection
# =============================================================================


async def process_list(
    filter_name: str | None = None,
    filter_user: str | None = None,
    min_cpu_percent: float = 0.0,
    min_memory_mb: float = 0.0,
    limit: int = 50,
    include_threads: bool = False,
) -> ToolResponse:
    """List and filter system processes using psutil."""
    start = time.perf_counter()
    res = internal_tools.process_list(
        filter_name=filter_name,
        filter_user=filter_user,
        min_cpu_percent=min_cpu_percent,
        min_memory_mb=min_memory_mb,
        limit=limit,
        include_threads=include_threads,
    )
    return _wrap_tool("process_list", start, res)

# =============================================================================
# Tool 3: fs_inspect — Filesystem Inspection
# =============================================================================


async def fs_inspect(
    path: str = ".",
    depth: int = 1,
    max_depth: int | None = None,
    include_hidden: bool = False,
    min_size_bytes: int = 0,
    pattern: str | None = None,
    max_files: int = 100,
) -> ToolResponse:
    """Inspect filesystem structure and file metadata."""
    start = time.perf_counter()
    res = internal_tools.fs_inspect(
        path=path,
        depth=depth,
        max_depth=max_depth,
        include_hidden=include_hidden,
        min_size_bytes=min_size_bytes,
        pattern=pattern,
        max_files=max_files,
    )
    # Post-process for backward compatibility (split tree into directories/files)
    if "tree" in res:
        tree = res.get("tree", [])
        flat_files = []
        flat_dirs = []
        
        def _collect_recursive(nodes):
            for node in nodes:
                if node.get("type") == "dir":
                    flat_dirs.append(node.get("path") or node.get("name"))
                    if "children" in node:
                        _collect_recursive(node["children"])
                else:
                    flat_files.append(node.get("path") or node.get("name"))
        
        _collect_recursive(tree)
        res["directories"] = flat_dirs
        res["files"] = flat_files

    return _wrap_tool("fs_inspect", start, res)

# =============================================================================
# Tool 4: log_tail — Log File Monitoring
# =============================================================================


async def log_tail(
    log_file: str = "aaa_mcp.log",
    lines: int = 50,
    pattern: str = "",
    log_path: str | None = None,
    follow: bool = False,
    grep_pattern: str | None = None,
    since_minutes: int | None = None,
) -> ToolResponse:
    """Tail and search log files."""
    start = time.perf_counter()
    res = internal_tools.log_tail(
        log_file=log_file,
        lines=lines,
        pattern=pattern,
        log_path=log_path,
        follow=follow,
        grep_pattern=grep_pattern,
        since_minutes=since_minutes,
    )
    return _wrap_tool("log_tail", start, res)


# =============================================================================
# Tool 5: net_status — Network Diagnostics
# =============================================================================


async def net_status(
    check_ports: bool = True,
    check_connections: bool = True,
    check_interfaces: bool = True,
    check_routing: bool = True,
    target_host: str | None = None,
) -> ToolResponse:
    """Network connectivity and interface status."""
    start = time.perf_counter()
    res = internal_tools.net_status(
        check_ports=check_ports,
        check_connections=check_connections,
        check_interfaces=check_interfaces,
        check_routing=check_routing,
        target_host=target_host,
    )
    return _wrap_tool("net_status", start, res)


# =============================================================================
# Tool 6: config_flags — Configuration Inspection
# =============================================================================


async def config_flags(
    config_path: str | None = None,
    env_prefix: str | None = "ARIFOS",
    include_secrets: bool = False,
) -> ToolResponse:
    """Inspect configuration files and environment variables."""
    start = time.perf_counter()
    res = internal_tools.config_flags(
        config_path=config_path,
        env_prefix=env_prefix,
        include_secrets=include_secrets,
    )
    return _wrap_tool("config_flags", start, res)



# =============================================================================
# Tool 7: chroma_query — Vector Database Search
# =============================================================================


async def chroma_query(
    query_text: str,
    collection_name: str = "default",
    n_results: int = 5,
    where_filter: dict | None = None,
    include_embeddings: bool = False,
) -> ToolResponse:
    """Query ChromaDB vector store for semantic search."""
    start = time.perf_counter()
    res = internal_tools.chroma_query(
        query=query_text,
        collection=collection_name,
        n_results=n_results,
        where=where_filter,
        include_embeddings=include_embeddings,
    )
    return _wrap_tool("chroma_query", start, res)


# =============================================================================
# Tool 8: cost_estimator — Resource Cost Projection
# =============================================================================


async def cost_estimator(
    action_description: str = "",
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
) -> ToolResponse:
    """Estimate costs for AI operations and infrastructure usage."""
    start = time.perf_counter()
    res = internal_tools.cost_estimator(
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
    return _wrap_tool("cost_estimator", start, res)


# =============================================================================
# Tool 9: forge_guard — Gating Decisions (Write-Enabled)
# =============================================================================


async def forge_guard(
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
) -> ToolResponse:
    """Forge guard — evaluates gating decisions for actions."""
    start = time.perf_counter()
    res = internal_tools.forge_guard(
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
    return _wrap_tool("forge_guard", start, res)
