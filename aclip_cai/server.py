"""
ACLIP-CAI MCP Server — Sensory Backend (v1.0-LOCAL)

Standalone MCP server exposing the 10-sense nervous system.
DEFAULT: localhost only (127.0.0.1) — internal to arifOS ecosystem.

Usage:
    python -m aclip_cai.server          # stdio mode (default)
    python -m aclip_cai.server --sse    # SSE mode (localhost only)

DITEMPA BUKAN DIBERI
"""

import os
import sys

# Force local source priority
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP

from aclip_cai.tools.chroma_query import list_collections, query_memory
from aclip_cai.tools.config_reader import config_flags as config_reader
from aclip_cai.tools.financial_monitor import financial_cost as estimate_financial_cost
from aclip_cai.tools.fs_inspector import fs_inspect as fs_inspector
from aclip_cai.tools.log_reader import log_tail as log_reader
from aclip_cai.tools.net_monitor import net_status as net_monitor
from aclip_cai.tools.safety_guard import forge_guard as safety_guard

# Import all sensory tools
from aclip_cai.tools.system_monitor import get_resource_usage, get_system_health, list_processes
from aclip_cai.tools.thermo_estimator import cost_estimator as thermo_cost

# Create MCP server
mcp = FastMCP(
    "aclip-cai",
    instructions="""
ACLIP-CAI — Console Intelligence & Perception (10 Senses)

Sensory tools for system observability:
  C0: system_health      — CPU, RAM, disk, processes
  C2: fs_inspect         — Filesystem traversal (read-only)
  C3: log_tail           — Log monitoring
  C4: net_status         — Network diagnostics
  C5: config_flags       — Environment inspection
  C6: chroma_query       — Vector memory search
  C7: cost_estimator     — Thermodynamic cost
  C8: forge_guard        — Safety circuit breaker (gated)
  C9: financial_cost     — Monetary cost

Security:
  - All tools read-only except forge_guard
  - forge_guard is local gating only (no remote execution)
  - DEFAULT: localhost only (127.0.0.1) — not exposed to internet

This is the SENSORY backend — it observes, it does not govern.
Constitutional governance lives in AAA-MCP.
""",
)


# =============================================================================
# SENSORY TOOLS (10 Senses)
# =============================================================================


@mcp.tool()
async def system_health(
    mode: str = "full",
    filter_process: str = "",
    top_n: int = 15,
) -> dict:
    """
    [C0] System health — CPU, RAM, disk, processes.

    The AI equivalent of 'top' or Task Manager.
    """
    if mode == "resources":
        return get_resource_usage()
    elif mode == "processes":
        return list_processes(filter_name=filter_process, top_n=top_n)
    else:
        return get_system_health()


@mcp.tool()
async def fs_inspect(
    path: str = ".",
    depth: int = 1,
    include_hidden: bool = False,
) -> dict:
    """
    [C2] Filesystem inspection — read-only directory traversal.

    Physical meaning: How much data exists where.
    """
    return fs_inspector(path=path, depth=depth, include_hidden=include_hidden)


@mcp.tool()
async def log_tail(
    log_file: str = "aaa_mcp.log",
    lines: int = 50,
    pattern: str = "",
) -> dict:
    """
    [C3] Log tail — recent entries with optional grep.

    Physical meaning: Historical errors, incidents, warnings.
    """
    return log_reader(log_file=log_file, lines=lines, pattern=pattern)


@mcp.tool()
async def net_status(
    check_ports: bool = True,
    check_connections: bool = True,
) -> dict:
    """
    [C4] Network posture — ports, connections, routing.

    Physical meaning: Attack surface, data exfil risk.
    """
    return net_monitor(check_ports=check_ports, check_connections=check_connections)


@mcp.tool()
async def config_flags() -> dict:
    """
    [C5] Environment and feature flags.

    Physical meaning: How the system is configured in reality.
    """
    return config_reader()


@mcp.tool()
async def chroma_query(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    list_only: bool = False,
) -> dict:
    """
    [C6] Vector memory semantic search.

    The AI equivalent of 'grep' over persistent memory.
    """
    if list_only:
        return list_collections()
    return query_memory(query=query, collection=collection, top_k=top_k)


@mcp.tool()
async def cost_estimator(
    action_description: str,
    estimated_cpu_percent: float = 0,
    estimated_ram_mb: float = 0,
    estimated_io_mb: float = 0,
) -> dict:
    """
    [C7] Thermodynamic cost estimation.

    Physical meaning: Energy/heat/time consumption.
    """
    return thermo_cost(
        action_description=action_description,
        estimated_cpu_percent=estimated_cpu_percent,
        estimated_ram_mb=estimated_ram_mb,
        estimated_io_mb=estimated_io_mb,
    )


@mcp.tool()
async def financial_cost(
    service: str,
    action: str,
    resource_id: str = "",
    period_days: int = 1,
) -> dict:
    """
    [C9] Financial cost estimation.

    Physical meaning: Monetary cost of operations.
    """
    return estimate_financial_cost(
        service=service,
        action=action,
        resource_id=resource_id,
        period_days=period_days,
    )


@mcp.tool()
async def forge_guard(
    check_system_health: bool = True,
    cost_score_threshold: float = 0.8,
    cost_score_to_check: float = 0.0,
) -> dict:
    """
    [C8] Local safety circuit breaker.

    Physical meaning: Console-level circuit breaker.
    Returns: OK / SABAR (delay) / VOID_LOCAL (don't try).

    NOTE: This is the ONLY tool with write/gate potential.
    It only gates local actions, never executes remotely.
    """
    return safety_guard(
        check_system_health=check_system_health,
        cost_score_threshold=cost_score_threshold,
        cost_score_to_check=cost_score_to_check,
    )


# =============================================================================
# Entry Point
# =============================================================================


def main():
    """Start the ACLIP-CAI server."""
    import argparse

    parser = argparse.ArgumentParser(description="ACLIP-CAI MCP Server")
    parser.add_argument("--sse", action="store_true", help="Use SSE transport (localhost only)")
    parser.add_argument("--port", type=int, default=50080, help="Port for SSE mode")
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host for SSE mode (default: localhost)"
    )

    args = parser.parse_args()

    print("[aclip] ACLIP-CAI Server Starting", file=sys.stderr)
    print(f"[aclip] Mode: {'SSE' if args.sse else 'stdio'}", file=sys.stderr)

    if args.sse:
        # FORCE localhost only for security
        if args.host not in ("127.0.0.1", "localhost"):
            print("[aclip] WARNING: Overriding host to 127.0.0.1 (localhost only)", file=sys.stderr)
            args.host = "127.0.0.1"
        print(f"[aclip] Binding to {args.host}:{args.port}", file=sys.stderr)
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
