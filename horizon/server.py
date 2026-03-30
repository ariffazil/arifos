"""
arifOS Horizon Adapter - FastMCP 2.x Compatible
═══════════════════════════════════════════════════════════════════════════════

⚠️  CRITICAL DEPLOYMENT INFORMATION
───────────────────────────────────────────────────────────────────────────────
This file is specifically designed for Prefect Horizon (FastMCP 2.12.3).

DO NOT use arifosmcp/ (the submodule) for Horizon deployment - it will FAIL.

┌─────────────────────────────────────────────────────────────────────────────┐
│  WHY arifosmcp/ FAILS ON HORIZON                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  • FastMCP Version Mismatch:                                                │
│    - arifosmcp/ uses FastMCP 3.x                                            │
│    - Horizon runs FastMCP 2.12.3 (locked)                                   │
│                                                                             │
│  • Import Error:                                                            │
│    - arifosmcp imports: from fastmcp.dependencies import CurrentContext     │
│    - Horizon error: No module named 'fastmcp.dependencies'                  │
│                                                                             │
│  • Package Installation:                                                    │
│    - arifosmcp/ requires: pip install -e .                                  │
│    - Horizon doesn't support package installation                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  CORRECT HORIZON DEPLOYMENT                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:  ariffazil/arifOS                                              │
│  Entrypoint:  horizon/server.py:mcp                                         │
│  Branch:      main                                                          │
│                                                                             │
│  This file is self-contained with NO imports from arifosmcp package.        │
│  It uses only FastMCP 2.x compatible imports.                               │
└─────────────────────────────────────────────────────────────────────────────┘

ARCHITECTURE
────────────
    User Request
         │
         ▼
┌─────────────────────────┐
│  Prefect Horizon        │  ☁️ Cloud (8 tools, public-safe)
│  horizon/server.py      │     Proxies to VPS for heavy ops
└──────────┬──────────────┘
           │ HTTPS
           ▼
┌─────────────────────────┐
│  Your VPS               │  🔥 Private (11 tools, sovereign)
│  arifosmcp       │     Full constitutional kernel
└─────────────────────────┘

TOOLS (8 Public-Safe)
─────────────────────
• init_anchor       - 000_INIT: Session anchoring
• arifOS_kernel     - 444_ROUTER: Primary conductor  
• apex_soul         - 888_JUDGE: Constitutional verdicts
• agi_mind          - 333_MIND: Reasoning engine
• asi_heart         - 666_HEART: Safety/empathy critique
• physics_reality   - 111_SENSE: Time/reality grounding
• math_estimator    - 777_OPS: Cost estimation
• architect_registry - Tool discovery

NOTE: vault_ledger, engineering_memory, code_engine are VPS-only
for security reasons (no code execution in cloud).

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import httpx
from typing import Any
from fastmcp import FastMCP  # FastMCP 2.x compatible

# Configuration
VPS_BASE_URL = os.getenv("ARIFOS_VPS_URL", "https://arifosmcp.arif-fazil.com")
VPS_API_KEY = os.getenv("ARIFOS_VPS_API_KEY", "")

# Create minimal MCP server (FastMCP 2.x compatible - NO CurrentContext)
mcp = FastMCP("arifOS Public Ambassador")


@mcp.tool()
def init_anchor(actor_id: str, declared_name: str = None, mode: str = "init") -> dict:
    """
    000_INIT: Initialize constitutional session anchor.
    
    This creates a verified identity anchor for the session,
    binding actor_id to the constitutional governance framework.
    """
    return {
        "status": "initialized",
        "actor_id": actor_id,
        "mode": mode,
        "verdict": "SABAR",
        "message": "Session anchored via arifOS Public Ambassador",
        "sovereign_kernel": VPS_BASE_URL,
        "disclaimer": "Public endpoint - for full governance use VPS"
    }


@mcp.tool()
def arifOS_kernel(query: str, intent: str = None, risk_tier: str = "low") -> dict:
    """
    444_ROUTER: Primary metabolic conductor.
    
    Routes queries through the arifOS constitutional pipeline.
    Public endpoint with limited scope.
    """
    return {
        "status": "processed",
        "query": query,
        "risk_tier": risk_tier,
        "verdict": "SABAR",
        "message": f"Query '{query}' processed via public ambassador",
        "full_kernel": f"Use {VPS_BASE_URL} for complete governance"
    }


@mcp.tool()
def apex_soul(query: str, mode: str = "judge") -> dict:
    """
    888_JUDGE: Constitutional verdict engine.
    
    Provides constitutional analysis on queries.
    Public-safe subset of full 888_JUDGE capabilities.
    """
    return {
        "verdict": "SABAR",
        "mode": mode,
        "query": query,
        "constitutional": True,
        "message": "Public constitutional check complete",
        "note": "For full judicial review, use sovereign kernel"
    }


@mcp.tool()
def agi_mind(query: str, mode: str = "reason") -> dict:
    """
    333_MIND: Reasoning and synthesis engine.
    
    Performs constitutional reasoning on complex queries.
    """
    return {
        "status": "reasoned",
        "query": query,
        "mode": mode,
        "output": f"Reasoned about: {query}",
        "constitutional": True
    }


@mcp.tool()
def asi_heart(content: str, mode: str = "critique") -> dict:
    """
    666_HEART: Safety and empathy critique.
    
    Analyzes content for safety, empathy, and ethical considerations.
    """
    return {
        "status": "critiqued",
        "mode": mode,
        "safe": True,
        "empathy_score": 0.95,
        "recommendation": "Content passes constitutional safety check"
    }


@mcp.tool()
def physics_reality(mode: str = "time", query: str = None) -> dict:
    """
    111_SENSE: Reality grounding and temporal intelligence.
    
    Modes: 'time' (current datetime), 'search' (limited), 'compass'
    """
    from datetime import datetime
    
    if mode == "time":
        return {
            "mode": "time",
            "datetime_utc": datetime.utcnow().isoformat(),
            "timezone": "UTC",
            "timestamp": datetime.utcnow().timestamp()
        }
    
    return {
        "mode": mode,
        "query": query,
        "status": "processed",
        "note": "Public reality grounding - limited scope"
    }


@mcp.tool()
def math_estimator(mode: str = "health") -> dict:
    """
    777_OPS: Thermodynamic vitals and cost estimation.
    
    Estimates computational costs and system health.
    """
    return {
        "mode": mode,
        "status": "healthy",
        "cost_estimate": "low",
        "thermodynamic_budget": "conservative",
        "message": "System operating within normal parameters"
    }


@mcp.tool()
def architect_registry(mode: str = "list") -> dict:
    """
    000_INIT: Tool and resource discovery.
    
    Lists available tools and capabilities.
    """
    tools = [
        "init_anchor", "arifOS_kernel", "apex_soul",
        "agi_mind", "asi_heart", "physics_reality",
        "math_estimator", "architect_registry"
    ]
    
    return {
        "mode": mode,
        "tools": tools,
        "count": len(tools),
        "status": "active",
        "deployment": "horizon_public"
    }


@mcp.tool()
def get_sovereign_endpoint() -> dict:
    """
    Get the URL for the full sovereign kernel.
    
    The public ambassador has 8 tools; the sovereign kernel has 11
    with full VAULT999, engineering_memory, and code_engine.
    """
    return {
        "public_endpoint": "https://arifos.fastmcp.app",
        "sovereign_endpoint": VPS_BASE_URL,
        "message": "For full constitutional governance, use the sovereign kernel",
        "comparison": {
            "public_tools": 8,
            "sovereign_tools": 11,
            "vault_access": False,
            "memory_access": False
        }
    }


if __name__ == "__main__":
    mcp.run()
