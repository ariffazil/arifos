"""
GEOX MCP Server — SSE Transport Bridge for A2A Ecosystem
═══════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI

SSE (Server-Sent Events) transport enabling:
- Web Browser clients (React UI) 
- External AI Agents (Claude, Kimi, etc.)
- Multi-agent swarm intelligence over HTTPS

Uses FastMCP 3.x with HTTP/SSE transport + Starlette for custom routes.
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

# Starlette for HTTP handling
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

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
    CANON_9_KEYS,
)

# Import base GEOX tools
from geox.core.ac_risk import compute_ac_risk
from geox.core.tool_registry import ToolRegistry

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("geox.sse_bridge")

# ═══════════════════════════════════════════════════════════════════════════════
# Server Configuration
# ═══════════════════════════════════════════════════════════════════════════════

GEOX_VERSION = "v2026.04.11-SSE"
GEOX_SEAL = "DITEMPA BUKAN DIBERI"
GEOX_CODENAME = "Earth Intelligence Core + SSE Bridge"

# EARTH.CANON_9 — Thermodynamic State Vector Basis
EARTH_CANON_9 = {
    "rho": "density (kg/m3)",
    "vp": "compressional velocity (m/s)",
    "vs": "shear velocity (m/s)",
    "res": "electrical resistivity (ohm.m)",
    "chi": "magnetic susceptibility (SI)",
    "k": "thermal conductivity (W/mK)",
    "p": "pore pressure (Pa)",
    "t": "temperature (K)",
    "phi": "porosity (0-1)",
}

# ═══════════════════════════════════════════════════════════════════════════════
# FastMCP Initialization
# ═══════════════════════════════════════════════════════════════════════════════

mcp = FastMCP(
    name="geox-earth-intelligence-core",
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
# Tool Definitions
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def geox_acp_register_agent(
    agent_id: str,
    role: str,
    name: str,
    resources: Optional[list] = None,
    tools: Optional[list] = None
) -> dict:
    """Register an agent with the Agent Control Plane."""
    return await acp_register_agent(agent_id, role, name, resources, tools)


@mcp.tool()
async def geox_acp_submit_proposal(agent_id: str, proposal: dict) -> dict:
    """Submit a proposal for 888_JUDGE evaluation."""
    return await acp_submit_proposal(agent_id, proposal)


@mcp.tool()
async def geox_acp_check_convergence(resource: str) -> dict:
    """Check agent convergence on a resource."""
    return await acp_check_convergence(resource)


@mcp.tool()
async def geox_acp_grant_seal(proposal_id: str, human_auth_token: str) -> dict:
    """Grant 999_SEAL (sovereign human authority)."""
    return acp_grant_seal(proposal_id, human_auth_token)


@mcp.tool()
async def geox_acp_get_status() -> dict:
    """Get ACP system status."""
    return await acp_get_status()


@mcp.tool()
async def geox_metabolize(
    state_vector: dict,
    propagation_mode: str = "1d_to_3d",
    uncertainty_floor: float = 0.04
) -> dict:
    """
    Metabolize a state vector through CANON_9 basis with F7 humility bounds.
    """
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


@mcp.tool()
async def geox_compute_ac_risk(
    area_km2: float,
    min_depth: float,
    max_depth: float,
    depth_unit: str = "m"
) -> dict:
    """
    Compute Anomalous Contrast (AC) Risk for a geological area.
    Theory of Anomalous Contrast (ToAC) core calculation.
    """
    try:
        result = compute_ac_risk(area_km2, min_depth, max_depth, depth_unit)
        return {
            "ac_risk_score": result.risk_score,
            "ac_category": result.category,
            "confidence": result.confidence,
            "theory": "ToAC",
            "verdict": "888_PROCEED" if result.risk_score < 0.7 else "888_HOLD",
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "verdict": "888_HOLD",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Resources
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.resource("geox://canon9/state")
def get_canon9_state() -> str:
    return json.dumps(EARTH_CANON_9, indent=2)


@mcp.resource("geox://acp/status")
async def get_acp_status_resource() -> str:
    status = await acp_get_status()
    return json.dumps(status, indent=2)


@mcp.resource("geox://capabilities")
def get_capabilities() -> str:
    caps = ToolRegistry.get_capabilities()
    return json.dumps(caps, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP Routes (Health, Status, etc.)
# ═══════════════════════════════════════════════════════════════════════════════

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
        "transport": "SSE/HTTP",
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


# ═══════════════════════════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    host = os.getenv("GEOX_HOST", "0.0.0.0")
    port = int(os.getenv("GEOX_PORT", "8000"))
    
    logger.info(f"🔥 GEOX SSE Bridge Starting")
    logger.info(f"   Version: {GEOX_VERSION}")
    logger.info(f"   Seal: {GEOX_SEAL}")
    logger.info(f"   Transport: HTTP/SSE on http://{host}:{port}")
    logger.info(f"   MCP Endpoint: /mcp")
    logger.info(f"   Health: /health")
    logger.info(f"   ACP: Agent Control Plane Enabled")
    
    # FastMCP 3.x uses HTTP transport with SSE under the hood
    mcp.run(transport="http", host=host, port=port)
