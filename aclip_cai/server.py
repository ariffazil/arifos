"""
ACLIP CAI — Console for AI on arifOS

The local ops surface for AI agents.
What a CLI is for humans, ACLIP is for the AI.

aaa-mcp  = The Constitution (governance, floors, Trinity pipeline)
aclip-cai = The Console    (system health, memory, platform ops)

Transport: MCP (implementation detail)
Identity:  ACLIP — arifOS Console for AI

Entry: python -m aclip_cai [stdio|sse|http]
"""

from fastmcp import FastMCP

mcp = FastMCP(
    "aclip-cai",
    instructions="""ACLIP — Console for AI on arifOS (9 Senses Forged)

The complete ops surface for AI agents on this machine.
Agents use this console to see and operate the local environment.

Console tools:
  C0 system_health  - Read RAM, CPU, disk, top processes
  C1 process_list   - (Alias for system_health mode=processes)
  C2 fs_inspect     - Inspect filesystem without modification
  C3 log_tail       - Read recent log entries
  C4 net_status     - Inspect network ports and connections
  C5 config_flags   - Read environment and feature flags
  C6 chroma_query   - Query persistent vector memory
  C7 cost_estimator - Predict the thermodynamic/resource cost of an action
  C8 forge_guard    - Local safety circuit breaker (OK/SABAR/VOID_LOCAL)

What a CLI is for humans, ACLIP is for the AI.
Constitutional governance remains in aaa-mcp.
""",
)


@mcp.tool()
async def system_health(
    mode: str = "full",
    filter_process: str = "",
    top_n: int = 15,
) -> dict:
    """Read system health from the ACLIP console (C0).

    The AI equivalent of opening Task Manager or running 'top'.

    Args:
        mode: "full" (health + processes + warnings) |
              "resources" (RAM/CPU/disk only) |
              "processes" (process list only) (C1)
        filter_process: Substring filter on process name (e.g. "python").
        top_n: Max processes to return (default 15).
    """
    from aclip_cai.tools.system_monitor import (
        get_resource_usage,
        get_system_health,
        list_processes,
    )

    if mode == "resources":
        return get_resource_usage()
    if mode == "processes":
        return list_processes(filter_name=filter_process, top_n=top_n)
    return get_system_health()


@mcp.tool()
async def fs_inspect(
    path: str = ".",
    depth: int = 1,
    include_hidden: bool = False,
) -> dict:
    """Inspect filesystem without modification (C2, F1 Amanah preview).

    Physical meaning: How much data exists where.
    Used for: IO cost estimation, rollback scope, vault impact.
    """
    from aclip_cai.tools.fs_inspector import fs_inspect as inspect_logic

    return inspect_logic(path=path, depth=depth, include_hidden=include_hidden)


@mcp.tool()
async def log_tail(
    log_file: str = "aaa_mcp.log",
    lines: int = 50,
    pattern: str = "",
) -> dict:
    """Read recent log entries (C3, F5/F6 scar weight).

    Physical meaning: Historical errors, incidents, warnings.
    Used for: W_scar computation → empathy calibration.
    """
    from aclip_cai.tools.log_reader import log_tail as tail_logic

    return tail_logic(log_file=log_file, lines=lines, pattern=pattern)


@mcp.tool()
async def net_status(
    check_ports: bool = True,
    check_connections: bool = True,
) -> dict:
    """Inspect network posture (C4, F10/F12 defense).

    Physical meaning: Attack surface, data exfil risk.
    Used for: Defense decisions before network-heavy actions.
    """
    from aclip_cai.tools.net_monitor import net_status as status_logic

    return status_logic(check_ports=check_ports, check_connections=check_connections)


@mcp.tool()
async def config_flags() -> dict:
    """Read environment and feature flags (C5, F11/F13 authority).

    Physical meaning: How the system is configured in reality.
    Used for: Threshold selection (LAB vs HARD mode).
    """
    from aclip_cai.tools.config_reader import config_flags as flags_logic

    return flags_logic()


@mcp.tool()
async def cost_estimator(
    action_description: str,
    estimated_cpu_percent: float = 0,
    estimated_ram_mb: float = 0,
    estimated_io_mb: float = 0,
) -> dict:
    """Predict resource cost (C7, F4 ΔS proxy).

    Physical meaning: Energy/heat/time consumption.
    Used for: Blast radius in thermodynamic terms.
    """
    from aclip_cai.tools.thermo_estimator import cost_estimator as estimator_logic

    return estimator_logic(
        action_description=action_description,
        estimated_cpu_percent=estimated_cpu_percent,
        estimated_ram_mb=estimated_ram_mb,
        estimated_io_mb=estimated_io_mb,
    )


@mcp.tool()
async def forge_guard(
    check_system_health: bool = True,
    cost_score_threshold: float = 0.8,
    cost_score_to_check: float = 0.0,
) -> dict:
    """Local safety relay (C8, All floors pre-check).

    Physical meaning: Circuit breaker at console level.
    Returns: OK / SABAR (delay) / VOID_LOCAL (don't try).
    """
    from aclip_cai.tools.safety_guard import forge_guard as guard_logic

    return guard_logic(
        check_system_health=check_system_health,
        cost_score_threshold=cost_score_threshold,
        cost_score_to_check=cost_score_to_check,
    )


@mcp.tool()
async def chroma_query(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    list_only: bool = False,
) -> dict:
    """Query the ACLIP memory console (Chroma vector store).

    The AI equivalent of 'grep' or 'search' over persistent memory.
    Reads from C:\\Users\\User\\chroma_memory.

    Args:
        query: Natural language search query.
        collection: Chroma collection name (default: "default").
        top_k: Number of results to return (default 5).
        list_only: If True, list available collections instead of searching.
    """
    from aclip_cai.tools.chroma_query import list_collections, query_memory

    if list_only:
        return list_collections()
    return query_memory(query=query, collection=collection, top_k=top_k)
