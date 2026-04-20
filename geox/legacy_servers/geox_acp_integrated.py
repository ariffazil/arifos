"""
GEOX MCP Server with ACP Integration
═══════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI

Integrated server combining:
- Base GEOX tools (7 Essential Tools)
- Agent Control Plane (ACP) with A2A protocol
- Constitutional governance (F1-F13)
- 888_JUDGE verdict protocol
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

# FastMCP
from fastmcp import FastMCP

# Import ACP components
from geox_mcp_server_acp import (
    acp,
    acp_register_agent,
    acp_submit_proposal,
    acp_check_convergence,
    acp_grant_seal,
    acp_get_status,
    F7_HUMILITY_FLOOR,
    F7_MAX_UNCERTAINTY,
)

# Import base GEOX tools
from geox.core.ac_risk import compute_ac_risk, AC_RiskResult
from geox.core.tool_registry import ToolRegistry, ErrorCode, create_standardized_error

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("geox.eic_acp")

# ═══════════════════════════════════════════════════════════════════════════════
# Server Configuration
# ═══════════════════════════════════════════════════════════════════════════════

GEOX_VERSION = "v2026.04.11-ACP"
GEOX_SEAL = "DITEMPA BUKAN DIBERI"
GEOX_CODENAME = "Earth Intelligence Core + ACP"

mcp = FastMCP(
    name="GEOX Earth Intelligence Core",
    version=GEOX_VERSION,
    instructions=(
        "Earth Intelligence for subsurface governance with Agent Control Plane. "
        "Theory of Anomalous Contrast (ToAC) is the core. "
        "Constitutional floors F1-F13 are non-negotiable. "
        "ACP enables multi-agent swarm intelligence. "
        f"{GEOX_SEAL}"
    ),
)

# ═══════════════════════════════════════════════════════════════════════════════
# HTTP Routes
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from starlette.requests import Request
    from starlette.responses import JSONResponse, PlainTextResponse
    
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_: Request) -> PlainTextResponse:
        return PlainTextResponse("OK")
    
    @mcp.custom_route("/health/details", methods=["GET"])
    async def health_details(_: Request) -> JSONResponse:
        caps = ToolRegistry.get_capabilities()
        acp_status = await acp_get_status()
        return JSONResponse({
            "ok": True,
            "service": "geox-earth-intelligence-core",
            "version": GEOX_VERSION,
            "codename": GEOX_CODENAME,
            "seal": GEOX_SEAL,
            "capabilities": caps,
            "tools": [t.name for t in ToolRegistry.list_tools(include_scaffold=False)],
            "constitutional_floors": ["F1", "F2", "F4", "F7", "F9", "F11", "F13"],
            "acp": acp_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    
    @mcp.custom_route("/tools", methods=["GET"])
    async def list_tools_endpoint(_: Request) -> JSONResponse:
        tools = ToolRegistry.list_tools_dict(include_scaffold=False)
        return JSONResponse({"tools": tools, "count": len(tools), "seal": GEOX_SEAL})
    
    @mcp.custom_route("/acp/status", methods=["GET"])
    async def acp_status_endpoint(_: Request) -> JSONResponse:
        status = await acp_get_status()
        return JSONResponse(status)
    
except ImportError as e:
    logger.warning(f"Starlette routes disabled: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# ACP Tools
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(name="geox_acp_register_agent")
async def geox_acp_register_agent(
    agent_id: str,
    role: str,
    name: str,
    resources: Optional[list] = None,
    tools: Optional[list] = None
) -> dict:
    """Register an agent with the Agent Control Plane."""
    return await acp_register_agent(agent_id, role, name, resources, tools)


@mcp.tool(name="geox_acp_submit_proposal")
async def geox_acp_submit_proposal(agent_id: str, proposal: dict) -> dict:
    """Submit a proposal for 888_JUDGE evaluation."""
    return await acp_submit_proposal(agent_id, proposal)


@mcp.tool(name="geox_acp_check_convergence")
async def geox_acp_check_convergence(resource: str) -> dict:
    """Check agent convergence on a resource."""
    return await acp_check_convergence(resource)


@mcp.tool(name="geox_acp_grant_seal")
async def geox_acp_grant_seal(proposal_id: str, human_auth_token: str) -> dict:
    """Grant 999_SEAL (sovereign human authority)."""
    return acp_grant_seal(proposal_id, human_auth_token)


@mcp.tool(name="geox_acp_get_status")
async def geox_acp_get_status_tool() -> dict:
    """Get ACP system status."""
    return await acp_get_status()


@mcp.tool(name="geox_metabolize")
async def geox_metabolize(
    state_vector: dict,
    propagation_mode: str = "1d_to_3d",
    uncertainty_floor: float = 0.04
) -> dict:
    """
    Metabolize a state vector through CANON_9 basis with F7 humility bounds.
    """
    from geox_mcp_server_acp import CANON_9_KEYS
    
    missing = [k for k in CANON_9_KEYS if k not in state_vector]
    if missing:
        return {
            "status": "FAILURE",
            "error": f"State vector violation. Missing: {missing}",
            "missing_basis": missing,
            "verdict": "888_HOLD",
        }
    
    if uncertainty_floor < F7_HUMILITY_FLOOR:
        uncertainty_floor = F7_HUMILITY_FLOOR
    
    return {
        "metabolism_status": "CONVERGED",
        "propagation": propagation_mode,
        "f7_uncertainty": uncertainty_floor,
        "verdict": "888_PROCEED",
        "state_vector_keys": list(state_vector.keys()),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Resources
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.resource("geox://canon9/state")
def get_canon9_state() -> str:
    from geox_mcp_server_acp import EARTH_CANON_9
    return json.dumps(EARTH_CANON_9, indent=2)


@mcp.resource("geox://acp/status")
async def get_acp_status_resource() -> str:
    status = await acp_get_status()
    return json.dumps(status, indent=2)


