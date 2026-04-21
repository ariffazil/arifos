"""
arifOS MCP Server v2.0 - Critical Fixes Implementation
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
from fastmcp import FastMCP, Context
from .identity import get_identity, set_identity
from .contract import ExecutionGovernanceContract, ExecutionStatus, GovernanceVerdict, ArtifactState
from .kernel import kernel_route
from .vault import vault_seal
from .mind import mind_reason

mcp = FastMCP("arifOS-v2 🔥", version="2.0.0-CRITICAL-FIXES")

@mcp.tool()
async def arifos_init(declared_name: str = "anonymous", session_id: str = "global"):
    identity = get_identity(session_id).declare(declared_name)
    set_identity(session_id, identity)
    return {"identity": identity.to_contract(), "status": "initialized"}

@mcp.tool()
async def arifos_kernel(query: str, session_id: str = "global"):
    identity = get_identity(session_id)
    result = await kernel_route(query=query, identity=identity)
    return result.to_dict()

@mcp.tool()
async def arifos_mind(query: str, session_id: str = "global"):
    identity = get_identity(session_id)
    result = await mind_reason(query=query, identity=identity)
    return result.to_dict()

if __name__ == "__main__":
    mcp.run()
