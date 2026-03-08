"""
FastMCP Server Entrypoint for arifOS Constitutional Kernel (Trinity Body).

This module is the canonical entrypoint referenced by fastmcp.json.
It exposes the FastMCP ``mcp`` instance backed by the full 13-tool
arifOS AAA MCP surface with thermodynamic governance.

Runtime architecture::

    core/server.py          ← FastMCP entrypoint (this file)
    core/governance.py      ← Constitutional governance engine
    core/contracts.py       ← Tool input contracts (F3/F11)
    core/rest_routes.py     ← HTTP REST endpoints
    core/transport/         ← stdio / SSE / HTTP adapters
    core/l0_constitution/   ← L0: 13-Floor kernel (re-exports)
    core/l1_cognition/      ← L1: Intelligence layer (re-exports)
    core/l2_tools/          ← L2: Canonical tool implementations

Usage::

    # FastMCP (stdio / HTTP / SSE)
    fastmcp run

    # Direct Python
    python -m core.server

    # Module import
    from core.server import mcp
"""

from __future__ import annotations

# Re-export the canonical FastMCP instance and helpers from the full server.
# arifos_aaa_mcp.server holds the 3 500-line implementation including all 13
# tools, governance token logic, physics enforcement, and REST routes.
from arifos_aaa_mcp.server import (  # noqa: F401
    MetabolicResult,
    MetabolicStage,
    AGIMindResult,
    ASIHeartResult,
    APEXSoulResult,
    aaa_full_context_pack,
    aaa_tool_schemas,
    agi_mind_loop,
    apex_soul_loop,
    asi_heart_loop,
    chatgpt_connector_bootstrap_prompt,
    create_aaa_mcp_server,
    governance_gate_profile_resource,
    mcp,
    mcp_transport_bootstrap_prompt,
    mcp_transport_profile_resource,
    metabolic_loop,
    metabolic_loop_prompt,
    tool_operating_manual_resource,
    tool_routing_policy_prompt,
)

__all__ = [
    "mcp",
    "create_aaa_mcp_server",
    "aaa_tool_schemas",
    "aaa_full_context_pack",
    "mcp_transport_profile_resource",
    "tool_operating_manual_resource",
    "governance_gate_profile_resource",
    "aaa_chain_prompt",
    "mcp_transport_bootstrap_prompt",
    "tool_routing_policy_prompt",
    "chatgpt_connector_bootstrap_prompt",
    "metabolic_loop",
    "metabolic_loop_prompt",
    "agi_mind_loop",
    "asi_heart_loop",
    "apex_soul_loop",
    "MetabolicResult",
    "MetabolicStage",
    "AGIMindResult",
    "ASIHeartResult",
    "APEXSoulResult",
]


def main() -> None:
    """Run the arifOS MCP server via FastMCP transport."""
    from core.transport.transports import run_server

    server = create_aaa_mcp_server()
    run_server(server)


if __name__ == "__main__":
    main()
