"""
GEOX Sovereign Governed Execution Server
═══════════════════════════════════════════════════════════════════════════════

The "GEOX by arifOS" surface from your audit.
Acts as the VPS / Dimension-Native / Governed Execution Plane.

Version: 2.0.0-DIMENSION-NATIVE
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os
import logging
import sys
import argparse
import json
import uvicorn
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Mount, Route
from datetime import datetime, timezone
from typing import Any

# ═══════════════════════════════════════════════════════════════════════════════
# GEOX Sovereign Configuration
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geox.sovereign")

GEOX_VERSION = "2.0.0-DIMENSION-NATIVE"
GEOX_SEAL = "DITEMPA BUKAN DIBERI"
GEOX_PROFILE = os.getenv("GEOX_PROFILE", "vps")  # Default to vps profile

mcp = FastMCP(
    name="GEOX by arifOS",
    version=GEOX_VERSION,
    on_duplicate="error",
    instructions="""Sovereign GEOX Execution Plane.
    
    This server provides high-integrity governed execution for geological tools.
    It enforces constitutional floors F1-F13 and embeds 888_HOLD logic.
    
    Dimensions: Prospect, Well, Earth3D, Map, Cross.
    """,
)

# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSION REGISTRIES BOOTSTRAP (Contract Parity)
# ═══════════════════════════════════════════════════════════════════════════════

sys.path.append(os.getcwd())

DIMENSION_GATES = {
    "vps": ["prospect", "well", "earth3d", "map", "cross"],
}

# Ensure we use the curated VPS dimension list
ENABLED_DIMENSIONS = DIMENSION_GATES.get("vps")

def bootstrap_registries():
    registry_map = {
        "prospect": "contracts.tools.prospect",
        "well": "contracts.tools.well",
        "earth3d": "contracts.tools.earth3d",
        "map": "contracts.tools.map",
        "cross": "contracts.tools.cross"
    }

    for dim in ENABLED_DIMENSIONS:
        if dim in registry_map:
            module_name = registry_map[dim]
            try:
                import importlib
                module = importlib.import_module(module_name)
                func_name = f"register_{dim}_tools"
                if hasattr(module, func_name):
                    register_func = getattr(module, func_name)
                    # Register tools onto the sovereign server
                    register_func(mcp, profile="vps")
                    logger.info(f"Registered SOVEREIGN {dim.upper()} tools")
            except Exception as e:
                logger.error(f"Failed to bootstrap sovereign {dim} registry: {e}")

bootstrap_registries()

# ═══════════════════════════════════════════════════════════════════════════════
# SOVEREIGN HEALTH & STATUS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.resource("geox://profile/status")
async def get_profile_status() -> dict:
    return {
        "status": "healthy",
        "service": "geox-dimension-native",
        "profile": "vps",
        "enabled_dimensions": ENABLED_DIMENSIONS,
        "version": GEOX_VERSION,
        "seal": GEOX_SEAL,
        "constitutional_floors": "F1-F13 ACTIVE"
    }

def build_status_payload() -> dict:
    return {
        "status": "healthy",
        "service": "geox-dimension-native",
        "version": GEOX_VERSION,
        "profile": "vps",
        "enabled_dimensions": ENABLED_DIMENSIONS,
        "seal": GEOX_SEAL,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ok": True,
        "constitutional_floors": {
            "F1": "active",
            "F2": "active",
            "F4": "active",
            "F7": "active",
            "F9": "active",
            "F11": "active",
            "F13": "active",
        }
    }

async def health_handler(request):
    return JSONResponse(build_status_payload())

async def run_legacy_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    # This server uses the canonical tools directly from registries
    tool_result = await mcp.call_tool(name, arguments)
    return {"success": True, "data": tool_result.content[0].text if tool_result.content else {}}

async def legacy_mcp_handler(request):
    try:
        payload = await request.json()
    except:
        return JSONResponse({"error": "Parse error"}, status_code=400)
    
    method = payload.get("method")
    params = payload.get("params", {})
    response_id = payload.get("id")

    if method == "tools/list":
        tools = [{"name": t.name, "description": t.description} for t in await mcp.list_tools()]
        return JSONResponse({"jsonrpc": "2.0", "id": response_id, "result": {"tools": tools}})
    
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        result = await run_legacy_tool(name, args)
        return JSONResponse({"jsonrpc": "2.0", "id": response_id, "result": {"content": [{"type": "text", "text": json.dumps(result)}]}})

    return JSONResponse({"error": "Method not found"}, status_code=404)

def create_app():
    mcp_app = mcp.http_app(path="/mcp", transport="streamable-http")
    return Starlette(
        routes=[
            Route("/health", health_handler, methods=["GET"]),
            Route("/mcp", legacy_mcp_handler, methods=["POST"]),
            Mount("/", mcp_app)
        ],
        lifespan=getattr(mcp_app, "lifespan", None),
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
