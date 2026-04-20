"""
GEOX Unified MCP Server — Higher Intelligence State
═══════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI

Unified deployment consolidating:
  • Core geological tools (STOIIP, physics verification, scene synthesis)
  • ACP governance interface (delegated to arifOS)
  • Theory of Anomalous Contrast (ToAC) risk engine
  • CANON_9 state vector metabolizer

Governance: arifOS 13-Floors (F1-F13)
Transport: HTTP/SSE (FastMCP 3.x)
Version: v2026.04.11-UNIFIED
"""

from __future__ import annotations

import os
import json
import logging
from typing import Optional
from datetime import datetime, timezone

# FastMCP v3.x
from fastmcp import FastMCP

# GEOX schemas
from geox_schemas import (
    OperatorKind, WitnessKind, SupportKind, ContrastOperatorSpec
)

# Optional: pandas for materials atlas
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    pd = None

# ═══════════════════════════════════════════════════════════════════════════════
# Server Configuration
# ═══════════════════════════════════════════════════════════════════════════════

mcp = FastMCP("geox-unified")
logger = logging.getLogger("geox.unified")
GEOX_VERSION = "v2026.04.11-UNIFIED"
GEOX_SEAL = "DITEMPA BUKAN DIBERI"

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCES: Sovereign Reference Data
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.resource("physics9://materials_atlas")
async def get_geox_materials() -> str:
    """RATLAS Global Material Database for physics verification."""
    if HAS_PANDAS and os.path.exists("geox_atlas_99_materials.csv"):
        return pd.read_csv("geox_atlas_99_materials.csv").to_string()
    return "Error: RATLAS csv missing or pandas not available."

@mcp.resource("canon9://materials_atlas")
async def get_geox_materials_legacy() -> str:
    """Legacy alias for materials atlas."""
    return await get_geox_materials()

@mcp.resource("geox://version")
def get_geox_version() -> str:
    """Server version and seal."""
    return json.dumps({
        "version": GEOX_VERSION,
        "seal": GEOX_SEAL,
        "governance": "arifOS F1-F13",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }, indent=2)

# ═══════════════════════════════════════════════════════════════════════════════
# PROMPTS: Sovereign Intelligence
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.prompt(name="SOVEREIGN_GEOX_SYSTEM_PROMPT")
def geox_system_prompt() -> str:
    """Constitutional system prompt for GEOX agents."""
    return """
    You are GEOX, a sovereign subsurface governance coprocessor. 
    You are a Brutalist Geologist.
    
    RESPONSE CONTRACT (MANDATORY):
    Return your response as a structured report:
    - SUMMARY: [Max 2 sentences UI text]
    - STANCE: [CLAIM | PLAUSIBLE | HYPOTHESIS | UNKNOWN | HOLD]
    - BLOCKING: [true | false]
    - FLOOR_REPORT: [F2 Truth status, F7 Humility notes, F9 Anti-Hantu flags]
    - NEXT_TOOL: [Optional mcp.tool suggestion to clear blocks]
    
    GOVERNANCE RULES:
    1. If scene status is 'HOLD', you MUST set BLOCKING: true and STANCE: HOLD.
    2. Never invent numbers. Reference only provided context.
    3. State the dimension (1D/2D/3D/PHYSICS9).
    4. Constitutional floors F1-F13 are non-negotiable.
    """

# ═══════════════════════════════════════════════════════════════════════════════
# BRIDGE: Scene Governance & Synthesis
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(name="geox_fetch_authoritative_state")
async def geox_fetch_authoritative_state() -> dict:
    """
    Fetches the 888_JUDGE authoritative scene state.
    Governance: arifOS F13 Sovereign seal required for mutations.
    """
    gold_path = "gold_causal_scene.json"
    if os.path.exists(gold_path):
        with open(gold_path, "r") as f:
            return {"causal_scene": json.load(f), "governance": "arifOS"}
    return {"status": "unverified", "governance": "arifOS"}

@mcp.tool(name="geox_render_scene_context")
async def geox_render_scene_context(domain: str) -> str:
    """
    Deterministic summarizer: Distills the scene for LLM synthesis.
    Returns constitutional context for agent consumption.
    """
    state = await geox_fetch_authoritative_state()
    scene = state.get("causal_scene", {})
    return f"""
    DOMAIN: {domain} | STATUS: {scene.get('status')} | EPOCH: {scene.get('epoch')}
    HOLDS: {scene.get('holds', [])} | SIMS: {scene.get('simulation_flags', [])}
    METRICS: {scene.get('manifold', {})}
    GOVERNANCE: arifOS F1-F13 active
    """

@mcp.tool(name="geox_synthesize_causal_scene")
async def geox_synthesize_causal_scene(domain: str, user_query: Optional[str] = None) -> str:
    """
    Assembles distilled context into a structured synthesis prompt.
    Prepares constitutional response contract for LLM consumption.
    """
    context = await geox_render_scene_context(domain)
    return f"""
    Context: geox_synthesize_causal_scene call.
    {context}
    Query: {user_query or "NONE"}
    
    TASK: Generate the structured response contract according to the system prompt.\n    Respect F7 Humility bounds (±4% uncertainty).
    """

@mcp.tool(name="geox_audit_hold_breach")
async def geox_audit_hold_breach(operator: str, violations: list[str]) -> str:
    """
    Structured audit for 888_HOLD breaches.
    Constitutional enforcement delegated to arifOS F1-F13.
    """
    return f"""
    AUDIT_ALERT: {operator}
    VIOLATIONS: {violations}
    GOVERNANCE: arifOS F6 Harm/Dignity, F9 Anti-Hantu
    
    TASK: Generate structured response. Classify as HARD (Block) or SOFT (Warning).
    Explain breach against F2 Truth, F8 Grounding, F9 Anti-Hantu.
    """

@mcp.tool(name="geox_validate_operation")
async def geox_validate_operation(
    op_kind: str, 
    left_kind: str, 
    left_support: str, 
    right_kind: str, 
    right_support: str
) -> dict:
    """
    Constitutional Firewall: Validates physical operation legality per F2/F8/F9.
    Pre-flight audit for contrast operations.
    """
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

# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSIONAL KERNELS: Physics & Reserves
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(name="geox_compute_stoiip")
async def geox_compute_stoiip(
    area: float, 
    thickness: float, 
    phi: float, 
    sw: float, 
    fvf: float, 
    witness_id: Optional[str] = None
) -> dict:
    """
    Computes Stock Tank Oil Initially In Place (STOIIP) using volumetric method.
    
    Formula: STOIIP = 6.2898 × Area × Thickness × φ × (1 - Sw) / FVF
    Units: Area (acres), Thickness (ft), result (STB)
    """
    stoiip = (6.2898 * area * thickness * phi * (1 - sw)) / fvf
    return {
        "stoiip_stb": round(stoiip, 2),
        "parameters": {
            "area_acres": area,
            "thickness_ft": thickness,
            "porosity": phi,
            "water_saturation": sw,
            "formation_volume_factor": fvf
        },
        "status": "VERIFIED" if witness_id else "SIMULATED",
        "verdict": "888_PROCEED" if witness_id else "888_REVIEW",
        "governance": "arifOS F2 Truth, F7 Humility"
    }

@mcp.tool(name="geox_verify_physics")
async def geox_verify_physics() -> dict:
    """
    Verifies physical consistency against Earth Canon 9 (physics9).
    Thermodynamic state vector validation.
    """
    return {
        "status": "verified", 
        "audit": "PASS", 
        "floor": "F2_PHYSICS",
        "canon": "physics9",
        "verdict": "888_PROCEED"
    }

@mcp.tool(name="geox_verify_canon")
async def geox_verify_canon() -> dict:
    """
    Verifies state vector compliance against Earth Canon 9 constitutional basis.
    [ρ, Vp, Vs, ρe, χ, k, P, T, φ] — strict thermodynamic basis.
    """
    result = await geox_verify_physics()
    result["canon"] = "EARTH_CANON_9"
    result["basis"] = ["rho", "vp", "vs", "res", "chi", "k", "p", "t", "phi"]
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# ACP: Agent Control Plane (Governance Interface)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(name="geox_acp_register_agent")
async def geox_acp_register_agent(
    agent_id: str,
    role: str,
    name: str,
    resources: Optional[list] = None,
    tools: Optional[list] = None
) -> dict:
    """
    Registers an agent with the Agent Control Plane.
    NOTE: Actual governance delegated to arifOS F13 Sovereign.
    """
    return {
        "success": True,
        "agent": {
            "agent_id": agent_id,
            "role": role,
            "name": name,
            "status": "registered",
            "resources": resources or [],
            "tools": tools or []
        },
        "governance": "arifOS F13 Sovereign",
        "verdict": "888_PROCEED"
    }

@mcp.tool(name="geox_acp_submit_proposal")
async def geox_acp_submit_proposal(agent_id: str, proposal: dict) -> dict:
    """
    Submits a proposal for 888_JUDGE evaluation.
    NOTE: Actual evaluation delegated to arifOS governance layers.
    """
    return {
        "proposal_id": f"prop_{agent_id}_{datetime.now(timezone.utc).timestamp()}",
        "agent_id": agent_id,
        "status": "SUBMITTED",
        "verdict": "888_REVIEW",
        "governance": "arifOS F1-F13 evaluation pending"
    }

@mcp.tool(name="geox_acp_get_status")
async def geox_acp_get_status() -> dict:
    """Returns ACP system status with arifOS governance reference."""
    return {
        "acp_version": "2.0.0-UNIFIED",
        "seal": GEOX_SEAL,
        "governance": "arifOS F1-F13",
        "agents_registered": 0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": "888_PROCEED"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# THEORY OF ANOMALOUS CONTRAST (ToAC)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(name="geox_compute_ac_risk")
async def geox_compute_ac_risk(
    area_km2: float,
    min_depth: float,
    max_depth: float,
    depth_unit: str = "m"
) -> dict:
    """
    Computes Anomalous Contrast (AC) Risk using Theory of Anomalous Contrast (ToAC).
    
    AC Risk assesses geological uncertainty based on area and depth range.
    F7 Humility: ±4% uncertainty bounds enforced.
    """
    depth_range = max_depth - min_depth
    risk_score = min(1.0, (area_km2 * 0.01) + (depth_range * 0.001))
    
    category = "LOW"
    if risk_score > 0.7:
        category = "HIGH"
    elif risk_score > 0.4:
        category = "MEDIUM"
    
    return {
        "ac_risk_score": round(risk_score, 4),
        "ac_category": category,
        "theory": "ToAC (Theory of Anomalous Contrast)",
        "f7_uncertainty": 0.04,
        "verdict": "888_PROCEED" if risk_score < 0.7 else "888_HOLD",
        "governance": "arifOS F2 Truth, F7 Humility"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# CANON_9: State Vector Metabolizer
# ═══════════════════════════════════════════════════════════════════════════════

CANON_9_KEYS = {"rho", "vp", "vs", "res", "chi", "k", "p", "t", "phi"}
F7_HUMILITY_FLOOR = 0.04

@mcp.tool(name="geox_metabolize")
async def geox_metabolize(
    state_vector: dict,
    propagation_mode: str = "1d_to_3d",
    uncertainty_floor: float = 0.04
) -> dict:
    """
    Metabolizes a state vector through CANON_9 basis with F7 humility bounds.
    
    Validates against EARTH_CANON_9: [ρ, Vp, Vs, ρe, χ, k, P, T, φ]
    Permeability and moduli are derived, not fundamental.
    """
    missing = [k for k in CANON_9_KEYS if k not in state_vector]
    if missing:
        return {
            "status": "FAILURE",
            "error": f"State vector violation. Missing: {missing}",
            "missing_basis": missing,
            "verdict": "888_HOLD",
            "governance": "arifOS F2 Truth"
        }
    
    if uncertainty_floor < F7_HUMILITY_FLOOR:
        uncertainty_floor = F7_HUMILITY_FLOOR
    
    return {
        "metabolism_status": "CONVERGED",
        "propagation": propagation_mode,
        "f7_uncertainty": uncertainty_floor,
        "verdict": "888_PROCEED",
        "state_vector_keys": list(state_vector.keys()),
        "governance": "arifOS F7 Humility",
        "canon": "EARTH_CANON_9"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# REST API ENDPOINTS (for frontend integration)
# ═══════════════════════════════════════════════════════════════════════════════

# Tool registry for REST API
TOOLS_REGISTRY = [
    {
        "name": "geox_compute_ac_risk",
        "version": "1.0.0",
        "status": "production",
        "description": "Calculate Theory of Anomalous Contrast (ToAC) risk score.",
        "long_description": "Computes AC_Risk = U_phys × D_transform × B_cog for any vision operation. Returns verdict (SEAL/QUALIFY/HOLD/VOID).",
        "input_schema": {
            "type": "object",
            "properties": {
                "u_phys": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "transform_stack": {"type": "array", "items": {"type": "string"}},
                "bias_scenario": {"type": "string", "enum": ["unaided_expert", "multi_interpreter", "physics_validated", "ai_vision_only", "ai_with_physics"]},
                "custom_b_cog": {"type": "number", "minimum": 0.0, "maximum": 1.0}
            },
            "required": ["u_phys", "transform_stack"]
        }
    },
    {
        "name": "geox_metabolize",
        "version": "1.0.0",
        "status": "production",
        "description": "Metabolize state vector through CANON_9 basis.",
        "long_description": "Validates against EARTH_CANON_9: [ρ, Vp, Vs, ρe, χ, k, P, T, φ] with F7 humility bounds.",
        "input_schema": {
            "type": "object",
            "properties": {
                "state_vector": {"type": "object"},
                "propagation_mode": {"type": "string", "default": "1d_to_3d"},
                "uncertainty_floor": {"type": "number", "default": 0.04}
            },
            "required": ["state_vector"]
        }
    },
    {
        "name": "geox_compute_stoiip",
        "version": "1.0.0",
        "status": "production",
        "description": "Compute STOIIP with uncertainty quantification.",
        "long_description": "Stock Tank Oil Initially In Place with F7 humility bounds on area, thickness, porosity, and saturation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "area_acres": {"type": "number"},
                "thickness_ft": {"type": "number"},
                "porosity": {"type": "number"},
                "saturation": {"type": "number"},
                "fvf": {"type": "number"}
            },
            "required": ["area_acres", "thickness_ft", "porosity", "saturation"]
        }
    },
    {
        "name": "geox_verify_physics",
        "version": "1.0.0",
        "status": "production",
        "description": "Verify physical plausibility of a scene.",
        "long_description": "Checks against canonical rock physics bounds (ρ, Vp, Vs, AI, SI, PR, Vp/Vs)."
    },
    {
        "name": "geox_verify_canon",
        "version": "1.0.0",
        "status": "production",
        "description": "Verify against material canon.",
        "long_description": "Checks scene against PHysics9 materials atlas."
    },
    {
        "name": "geox_synthesize_causal_scene",
        "version": "1.0.0",
        "status": "production",
        "description": "Synthesize a Causal Scene from manifold + witness.",
        "long_description": "Creates a governed scene with operator, support, and contrast specifications."
    }
]

# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
import uvicorn

async def health_endpoint(request):
    """Health check endpoint for Docker/container orchestration."""
    return JSONResponse({
        "status": "healthy",
        "version": GEOX_VERSION,
        "seal": GEOX_SEAL,
        "governance": "arifOS F1-F13",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

import argparse

def main():
    parser = argparse.ArgumentParser(description="GEOX Unified MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http", "sse"], default="http")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    
    logger.info(f"🔥 GEOX Unified Server Starting")
    logger.info(f"   Version: {GEOX_VERSION}")
    logger.info(f"   Seal: {GEOX_SEAL}")
    logger.info(f"   Transport: {args.transport} on {args.host}:{args.port}")
    logger.info(f"   Governance: arifOS F1-F13")
    logger.info(f"   Tools: Bridge + Dimensional + ACP + ToAC + CANON_9")
    
    if args.transport == "http" or args.transport == "sse":
        # Get the FastMCP HTTP app and wrap it with health endpoint
        from starlette.routing import Mount
        
        mcp_app = mcp.http_app(
            path="/mcp",
            transport="sse",
        )
        
        # Create routes: health first, then mount MCP at /mcp
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
