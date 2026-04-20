"""
GEOX Unified MCP Server — HONEST VERSION
═══════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI

FIX: Removed hardcoded demo data. Tools now either:
  1. Compute from real user-provided parameters
  2. Return explicit "NO ACTIVE SCENE" if no data
  3. Validate inputs against physics, not return fake constants
"""

from __future__ import annotations

import os
import json
import logging
from typing import Optional
from datetime import datetime, timezone

from fastmcp import FastMCP
from geox_schemas import (
    OperatorKind, WitnessKind, SupportKind, ContrastOperatorSpec
)

mcp = FastMCP("geox-unified")
logger = logging.getLogger("geox.unified")
GEOX_VERSION = "v2026.04.11-HONEST"
GEOX_SEAL = "DITEMPA BUKAN DIBERI"

# ═══════════════════════════════════════════════════════════════════════════════
# STATE MANAGEMENT: No fake defaults
# ═══════════════════════════════════════════════════════════════════════════════

# In-memory scene store (empty until user provides data)
_active_scene: dict | None = None

def get_scene_or_none() -> dict | None:
    """Returns active scene or None. NO FAKE DEFAULTS."""
    global _active_scene
    return _active_scene

def set_active_scene(scene_data: dict):
    """Set a real scene from user input."""
    global _active_scene
    _active_scene = scene_data
    logger.info(f"[GEOX] Active scene set: {scene_data.get('name', 'unnamed')}")

# ═══════════════════════════════════════════════════════════════════════════════
# TOOLS: Honest implementations
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(name="geox_fetch_authoritative_state")
async def geox_fetch_authoritative_state() -> dict:
    """
    Fetches the 888_JUDGE authoritative scene state.
    
    HONEST: Returns real scene if set, else explicit 'NO_ACTIVE_SCENE'
    """
    scene = get_scene_or_none()
    if scene is None:
        return {
            "status": "NO_ACTIVE_SCENE",
            "message": "No geological scene has been established. Use geox_set_scene() with real parameters.",
            "governance": "arifOS F2 Truth — Cannot fabricate data",
            "hint": "Provide real well logs, seismic picks, or reservoir parameters"
        }
    
    return {
        "causal_scene": scene,
        "status": "ACTIVE_SCENE_LOADED",
        "governance": "arifOS F1-F13",
        "provenance": scene.get("provenance", "unknown")
    }

@mcp.tool(name="geox_set_scene")
async def geox_set_scene(
    name: str,
    crs: str,
    area_m2: float,
    gross_thickness_m: float,
    porosity: float,
    provenance: str = "user_specified"
) -> dict:
    """
    Establish a REAL geological scene with user-provided parameters.
    
    All values must come from actual data — well logs, seismic, core analysis.
    """
    # Validate physics
    if porosity < 0 or porosity > 1:
        return {
            "status": "HOLD",
            "verdict": "888_HOLD",
            "error": f"Porosity {porosity} outside physical bounds [0,1]",
            "governance": "arifOS F2 Truth — Physics violation"
        }
    
    if area_m2 <= 0:
        return {
            "status": "HOLD", 
            "verdict": "888_HOLD",
            "error": "Area must be positive",
            "governance": "arifOS F2 Truth"
        }
    
    scene = {
        "name": name,
        "crs": crs,
        "area_m2": area_m2,
        "gross_thickness_m": gross_thickness_m,
        "porosity": porosity,
        "provenance": provenance,
        "set_at": datetime.now(timezone.utc).isoformat(),
        "status": "user_verified"
    }
    
    set_active_scene(scene)
    
    return {
        "status": "SCENE_ESTABLISHED",
        "scene": scene,
        "verdict": "888_PROCEED",
        "governance": "arifOS F2 Truth — User attested data",
        "next": "Call geox_compute_stoiip() with this scene"
    }

@mcp.tool(name="geox_render_scene_context")
async def geox_render_scene_context(domain: str) -> str:
    """
    Render scene context — HONEST version.
    """
    state = await geox_fetch_authoritative_state()
    
    if state["status"] == "NO_ACTIVE_SCENE":
        return f"""
DOMAIN: {domain}
STATUS: NO_ACTIVE_SCENE
MESSAGE: No geological data loaded. 
ACTION REQUIRED: Call geox_set_scene() with real parameters from:
  - Well log analysis
  - Seismic interpretation  
  - Core measurements
  - Production data
GOVERNANCE: arifOS F2 Truth — No fabrication permitted
"""
    
    scene = state["causal_scene"]
    return f"""
DOMAIN: {domain}
STATUS: ACTIVE_SCENE_LOADED
SCENE: {scene.get('name')}
CRS: {scene.get('crs')}
AREA: {scene.get('area_m2'):,.0f} m²
THICKNESS: {scene.get('gross_thickness_m')} m
POROSITY: {scene.get('porosity')} (user-provided)
PROVENANCE: {scene.get('provenance')}
SET_AT: {scene.get('set_at')}
GOVERNANCE: arifOS F1-F13 active
"""

@mcp.tool(name="geox_compute_stoiip")
async def geox_compute_stoiip(
    area_acres: float,
    thickness_ft: float,
    porosity: float,
    sw: float,
    fvf: float,
    witness_id: Optional[str] = None
) -> dict:
    """
    Compute STOIIP from REAL parameters provided by user.
    
    Formula: 7758 × area × thickness × porosity × (1 - sw) / fvf
    All inputs must come from actual reservoir characterization.
    """
    # Validate all inputs
    errors = []
    if porosity < 0 or porosity > 1:
        errors.append(f"Porosity {porosity} outside [0,1]")
    if sw < 0 or sw > 1:
        errors.append(f"Water saturation {sw} outside [0,1]")
    if area_acres <= 0:
        errors.append("Area must be positive")
    if thickness_ft <= 0:
        errors.append("Thickness must be positive")
    if fvf <= 0:
        errors.append("FVF must be positive")
    
    if errors:
        return {
            "status": "HOLD",
            "verdict": "888_HOLD",
            "errors": errors,
            "governance": "arifOS F2 Truth — Input validation failed"
        }
    
    # Compute STOIIP
    stoiip = (7758 * area_acres * thickness_ft * porosity * (1 - sw)) / fvf
    
    # F7 Humility: quantify uncertainty
    # Typical volumetric uncertainty: ±15-30%
    uncertainty = 0.20  # 20% base uncertainty
    
    return {
        "stoiip_stb": round(stoiip, 1),
        "status": "COMPUTED_FROM_INPUTS",
        "inputs": {
            "area_acres": area_acres,
            "thickness_ft": thickness_ft,
            "porosity": porosity,
            "sw": sw,
            "fvf": fvf
        },
        "f7_uncertainty": uncertainty,
        "verdict": "888_PROCEED" if witness_id else "888_QUALIFY",
        "governance": "arifOS F2 Truth — Computed from attested inputs",
        "warning": "All inputs must come from actual well logs/seismic/core data. Do not invent numbers."
    }

@mcp.tool(name="geox_validate_operation")
async def geox_validate_operation(
    op_kind: str, 
    left_kind: str, 
    left_support: str, 
    right_kind: str, 
    right_support: str
) -> dict:
    """Constitutional validation for contrast operations."""
    try:
        spec = ContrastOperatorSpec(
            op_kind=OperatorKind(op_kind),
            left_kind=WitnessKind(left_kind),
            left_support=SupportKind(left_support),
            right_kind=WitnessKind(right_kind),
            right_support=SupportKind(right_support),
            rationale="Pre-flight constitutional audit."
        )
        return {
            "status": "LEGAL", 
            "spec": spec.model_dump(),
            "verdict": "888_PROCEED",
            "governance": "arifOS F2/F8/F9"
        }
    except Exception as e:
        return {
            "status": "HOLD", 
            "holds": [str(e)], 
            "blocking": True,
            "verdict": "888_HOLD",
            "governance": "arifOS F2/F8/F9"
        }

@mcp.tool(name="geox_audit_hold_breach")
async def geox_audit_hold_breach(operator: str, violations: list[str]) -> str:
    """Structured audit for 888_HOLD breaches."""
    return f"""
AUDIT_ALERT: {operator}
VIOLATIONS: {violations}
GOVERNANCE: arifOS F6 Harm/Dignity, F9 Anti-Hantu

TASK: Generate structured response. Classify as HARD (Block) or SOFT (Warning).
Explain breach against F2 Truth, F8 Grounding, F9 Anti-Hantu.
"""

@mcp.tool(name="geox_synthesize_causal_scene")
async def geox_synthesize_causal_scene(domain: str, user_query: Optional[str] = None) -> str:
    """HONEST: Only synthesize if scene exists."""
    state = await geox_fetch_authoritative_state()
    
    if state["status"] == "NO_ACTIVE_SCENE":
        return f"""
CANNOT SYNTHESIZE: No active geological scene.

User asked: {user_query or "N/A"}

To establish a scene, call:
  geox_set_scene(
    name="your_reservoir_name",
    crs="WGS84_UTM50N",
    area_m2=450000,
    gross_thickness_m=250,
    porosity=0.18,
    provenance="well_log_interpretation"
  )

GOVERNANCE: arifOS F2 Truth — No fabrication of geological context
"""
    
    context = await geox_render_scene_context(domain)
    return f"""
CAUSAL SYNTHESIS REQUEST
{context}
Query: {user_query or "NONE"}

Generate structured response respecting F7 Humility bounds (±4% uncertainty).
All claims must reference the scene parameters above.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

import argparse

def main():
    parser = argparse.ArgumentParser(description="GEOX Unified MCP Server (HONEST)")
    parser.add_argument("--transport", choices=["stdio", "http", "sse"], default="http")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    
    logger.info(f"🔥 GEOX Unified Server Starting (HONEST VERSION)")
    logger.info(f"   Version: {GEOX_VERSION}")
    logger.info(f"   Seal: {GEOX_SEAL}")
    logger.info(f"   Transport: {args.transport} on {args.host}:{args.port}")
    logger.info(f"   Governance: arifOS F1-F13")
    logger.info(f"   Policy: NO FABRICATION — Real data or explicit NO_ACTIVE_SCENE")
    
    if args.transport == "http" or args.transport == "sse":
        mcp_app = mcp.http_app(
            path="/mcp",
            transport="sse",
        )
        
        from starlette.applications import Starlette
        from starlette.routing import Route, Mount
        from starlette.responses import JSONResponse
        import uvicorn
        
        async def health_endpoint(request):
            return JSONResponse({
                "status": "healthy",
                "version": GEOX_VERSION,
                "seal": GEOX_SEAL,
                "policy": "NO_FAKE_DATA",
                "scene_loaded": get_scene_or_none() is not None
            })
        
        routes = [
            Route("/health", health_endpoint),
            Mount("/mcp", app=mcp_app),
        ]
        
        app = Starlette(routes=routes)
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        mcp.run(transport=args.transport, port=args.port, host=args.host)

if __name__ == "__main__":
    main()
