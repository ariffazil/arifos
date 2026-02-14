#!/usr/bin/env python3
"""
arifos-router — Canonical MCP Face of arifOS (v65.0-ROUTER)

Minimal gateway that:
1. Spawns AAA-MCP (constitutional) + ACLIP-CAI (sensory) backends
2. Routes tool calls: aclip_* → ACLIP, others → AAA
3. Presents unified tool surface to clients

Usage:
    arifos-router              # stdio mode (default)
    arifos-router --sse        # SSE mode for Railway

Backends:
    - AAA-MCP: constitutional pipeline (5-Core)
    - ACLIP-CAI: sensory console (10-Sense), localhost only

DITEMPA BUKAN DIBERI
"""

import asyncio
import os
import sys
from typing import Optional, Any

# Force local source priority
sys.path.insert(0, os.getcwd())

from fastmcp import FastMCP
from mcp import Client, StdioServerParameters

# Router configuration
AAA_CMD = [sys.executable, "-m", "aaa_mcp"]
ACLIP_CMD = [sys.executable, "-m", "aclip_cai.server"]

# Router MCP server
mcp = FastMCP(
    "arifos-router",
    instructions="""
arifos-router — Canonical MCP Face of arifOS

Unified gateway exposing:
  CONSTITUTIONAL (AAA-MCP): init_session, agi_cognition, asi_empathy, apex_verdict, vault_seal
  SENSORY (ACLIP-CAI): aclip_system_health, aclip_fs_inspect, aclip_log_tail, etc.

Routing:
  - Tools with 'aclip_' prefix → ACLIP-CAI backend (localhost)
  - All other tools → AAA-MCP backend (constitutional)

Security:
  - ACLIP backend binds to localhost only
  - Router mediates all sensory access
  - Constitutional floors enforced by AAA-MCP

This is the canonical entry point for arifOS MCP ecosystem.
""",
)

# Backend clients
aaa_client: Optional[Client] = None
aclip_client: Optional[Client] = None


async def ensure_backends():
    """Ensure both backends are connected."""
    global aaa_client, aclip_client
    
    if aaa_client is None:
        aaa_params = StdioServerParameters(
            command=AAA_CMD[0],
            args=AAA_CMD[1:],
            env=os.environ.copy(),
        )
        aaa_client = Client(aaa_params)
        await aaa_client.__aenter__()
    
    if aclip_client is None:
        aclip_params = StdioServerParameters(
            command=ACLIP_CMD[0],
            args=ACLIP_CMD[1:],
            env=os.environ.copy(),
        )
        aclip_client = Client(aclip_params)
        await aclip_client.__aenter__()


async def route_tool(tool_name: str, arguments: dict) -> Any:
    """Route tool call to appropriate backend."""
    await ensure_backends()
    
    if tool_name.startswith("aclip_"):
        # Route to ACLIP-CAI (sensory)
        if aclip_client is None:
            raise RuntimeError("ACLIP-CAI backend not available")
        return await aclip_client.call_tool(tool_name, arguments)
    else:
        # Route to AAA-MCP (constitutional)
        if aaa_client is None:
            raise RuntimeError("AAA-MCP backend not available")
        return await aaa_client.call_tool(tool_name, arguments)


# =============================================================================
# CONSTITUTIONAL TOOLS (Proxy to AAA-MCP)
# =============================================================================

@mcp.tool()
async def init_session(
    session_id: str = "",
    query: str = "",
    authority_context: str = "standard",
    grounding_required: bool = False,
) -> dict:
    """000_INIT — Session ignition with F11/F12 authority checks."""
    return await route_tool("init_session", {
        "session_id": session_id,
        "query": query,
        "authority_context": authority_context,
        "grounding_required": grounding_required,
    })


@mcp.tool()
async def agi_cognition(
    query: str,
    session_id: str = "",
    context: str = "",
    evidence_required: bool = True,
) -> dict:
    """111-333_AGI — Mind (Δ): Sense, Think, Reason."""
    return await route_tool("agi_cognition", {
        "query": query,
        "session_id": session_id,
        "context": context,
        "evidence_required": evidence_required,
    })


@mcp.tool()
async def asi_empathy(
    query: str,
    session_id: str = "",
    stakeholders: list = None,
) -> dict:
    """555-666_ASI — Heart (Ω): Empathize, Align."""
    args = {
        "query": query,
        "session_id": session_id,
    }
    if stakeholders:
        args["stakeholders"] = stakeholders
    return await route_tool("asi_empathy", args)


@mcp.tool()
async def apex_verdict(
    session_id: str,
    query_summary: str = "",
    risk_level: str = "medium",
) -> dict:
    """888_APEX — Soul (Ψ): Final constitutional judgment."""
    return await route_tool("apex_verdict", {
        "session_id": session_id,
        "query_summary": query_summary,
        "risk_level": risk_level,
    })


@mcp.tool()
async def vault_seal(
    session_id: str,
    verdict: str,
    query_summary: str = "",
    risk_level: str = "low",
    category: str = "general",
    floors_checked: list = None,
) -> dict:
    """999_VAULT — Seal (🔒): Immutable audit record."""
    args = {
        "session_id": session_id,
        "verdict": verdict,
        "query_summary": query_summary,
        "risk_level": risk_level,
        "category": category,
    }
    if floors_checked:
        args["floors_checked"] = floors_checked
    return await route_tool("vault_seal", args)


@mcp.tool()
async def human_approve(
    session_id: str,
    approved: bool,
    actor: str = "888",
    reason: str = "",
) -> dict:
    """L8 Human Sovereign — Approve AWAITING_888 state."""
    return await route_tool("human_approve", {
        "session_id": session_id,
        "approved": approved,
        "actor": actor,
        "reason": reason,
    })


# =============================================================================
# SENSORY TOOLS (Proxy to ACLIP-CAI)
# =============================================================================

@mcp.tool()
async def aclip_system_health(
    mode: str = "full",
    filter_process: str = "",
    top_n: int = 15,
) -> dict:
    """[ACLIP C0] System health — CPU, RAM, disk, processes."""
    return await route_tool("system_health", {
        "mode": mode,
        "filter_process": filter_process,
        "top_n": top_n,
    })


@mcp.tool()
async def aclip_fs_inspect(
    path: str = ".",
    depth: int = 1,
    include_hidden: bool = False,
) -> dict:
    """[ACLIP C2] Filesystem inspection — read-only directory traversal."""
    return await route_tool("fs_inspect", {
        "path": path,
        "depth": depth,
        "include_hidden": include_hidden,
    })


@mcp.tool()
async def aclip_log_tail(
    log_file: str = "aaa_mcp.log",
    lines: int = 50,
    pattern: str = "",
) -> dict:
    """[ACLIP C3] Log tail — recent entries with optional grep."""
    return await route_tool("log_tail", {
        "log_file": log_file,
        "lines": lines,
        "pattern": pattern,
    })


@mcp.tool()
async def aclip_net_status(
    check_ports: bool = True,
    check_connections: bool = True,
) -> dict:
    """[ACLIP C4] Network posture — ports, connections, routing."""
    return await route_tool("net_status", {
        "check_ports": check_ports,
        "check_connections": check_connections,
    })


@mcp.tool()
async def aclip_config_flags() -> dict:
    """[ACLIP C5] Environment and feature flags."""
    return await route_tool("config_flags", {})


@mcp.tool()
async def aclip_chroma_query(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    list_only: bool = False,
) -> dict:
    """[ACLIP C6] Vector memory semantic search."""
    return await route_tool("chroma_query", {
        "query": query,
        "collection": collection,
        "top_k": top_k,
        "list_only": list_only,
    })


@mcp.tool()
async def aclip_cost_estimator(
    action_description: str,
    estimated_cpu_percent: float = 0,
    estimated_ram_mb: float = 0,
    estimated_io_mb: float = 0,
) -> dict:
    """[ACLIP C7] Thermodynamic cost estimation."""
    return await route_tool("cost_estimator", {
        "action_description": action_description,
        "estimated_cpu_percent": estimated_cpu_percent,
        "estimated_ram_mb": estimated_ram_mb,
        "estimated_io_mb": estimated_io_mb,
    })


@mcp.tool()
async def aclip_financial_cost(
    service: str,
    action: str,
    resource_id: str = "",
    period_days: int = 1,
) -> dict:
    """[ACLIP C9] Financial cost estimation."""
    return await route_tool("financial_cost", {
        "service": service,
        "action": action,
        "resource_id": resource_id,
        "period_days": period_days,
    })


@mcp.tool()
async def aclip_forge_guard(
    check_system_health: bool = True,
    cost_score_threshold: float = 0.8,
    cost_score_to_check: float = 0.0,
) -> dict:
    """[ACLIP C8] Local safety circuit breaker."""
    return await route_tool("forge_guard", {
        "check_system_health": check_system_health,
        "cost_score_threshold": cost_score_threshold,
        "cost_score_to_check": cost_score_to_check,
    })


# =============================================================================
# Entry Point
# =============================================================================

def main():
    """Start the arifos-router."""
    import argparse
    
    parser = argparse.ArgumentParser(description="arifos-router — Canonical MCP Face of arifOS")
    parser.add_argument("--sse", action="store_true", help="Use SSE transport")
    parser.add_argument("--port", type=int, default=8080, help="Port for SSE mode")
    parser.add_argument("--host", default="0.0.0.0", help="Host for SSE mode")
    
    args = parser.parse_args()
    
    print("[router] arifos-router Starting", file=sys.stderr)
    print("[router] Canonical MCP Face of arifOS", file=sys.stderr)
    print(f"[router] Mode: {'SSE' if args.sse else 'stdio'}", file=sys.stderr)
    
    if args.sse:
        mcp.run_sse(host=args.host, port=args.port)
    else:
        mcp.run_stdio()


if __name__ == "__main__":
    main()
