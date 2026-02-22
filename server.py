"""
arifOS AAA MCP Server - Decoupled Transport Layer (v63.0-FORGE)
Motto: DITEMPA BUKAN DIBERI
"""

import json
import logging
import os
from typing import Any, Dict, List, Literal, Optional

from fastmcp import FastMCP

# arifOS Kernel Imports (Pure Decoupling)
try:
    from codebase.init.000_init.init_000 import init_session as kernel_init_session
    from codebase.agi.engine import agi_cognition as kernel_agi_cognition
    from codebase.asi.engine import asi_empathy as kernel_asi_empathy
    from codebase.shared.stages.stage_888_judge import apex_verdict as kernel_apex_verdict
    from codebase.shared.stages.stage_999_seal import vault_seal as kernel_vault_seal
except ImportError as e:
    logging.error(f"Kernel decoupling failure: {str(e)}")

# Tool annotations for MCP compliance
TOOL_ANNOTATIONS = {
    "init_session": {
        "title": "000_INIT - Session Ignition",
        "description": "Initialize constitutional session with F11/F12 authority checks",
    },
    "agi_cognition": {
        "title": "111-333_AGI - Mind (\u0394)",
        "description": "Sense, Think, Reason - Logical cognition pipeline",
    },
    "asi_empathy": {
        "title": "555-666_ASI - Heart (\u03a9)",
        "description": "Empathize, Align - Stakeholder protection and ethics",
    },
    "apex_verdict": {
        "title": "888_APEX - Soul (\u03a8)",
        "description": "Final constitutional judgment with F2/F3 verification",
    },
    "vault_seal": {
        "title": "999_VAULT - Seal (\ud83d\udd12)",
        "description": "Immutable audit record with F1/F3 permanence",
    },
}

def constitutional_floor(*floors: str):
    def decorator(func):
        func._constitutional_floors = floors
        return func
    return decorator

mcp = FastMCP("aaa-mcp")

@mcp.tool(annotations=TOOL_ANNOTATIONS["init_session"])
@constitutional_floor("F11", "F12")
async def init_session(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    mode: Literal["conscience", "ghost"] = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
) -> dict:
    return await kernel_init_session(query, actor_id, auth_token, mode, grounding_required, debug)

@mcp.tool(annotations=TOOL_ANNOTATIONS["agi_cognition"])
@constitutional_floor("F2", "F4", "F7", "F8", "F10")
async def agi_cognition(
    query: str,
    session_id: str,
    grounding: Optional[list] = None,
    capability_modules: Optional[list] = None,
    debug: bool = False,
) -> dict:
    return await kernel_agi_cognition(query, session_id, grounding, capability_modules, debug)

@mcp.tool(annotations=TOOL_ANNOTATIONS["asi_empathy"])
@constitutional_floor("F1", "F5", "F6", "F9")
async def asi_empathy(
    query: str,
    session_id: str,
    stakeholders: Optional[list] = None,
    capability_modules: Optional[list] = None,
    debug: bool = False,
) -> dict:
    return await kernel_asi_empathy(query, session_id, stakeholders, capability_modules, debug)

@mcp.tool(annotations=TOOL_ANNOTATIONS["apex_verdict"])
@constitutional_floor("F2", "F3", "F8", "F10", "F11", "F12", "F13")
async def apex_verdict(
    query: str,
    session_id: str,
    agi_result: Optional[dict] = None,
    asi_result: Optional[dict] = None,
    capability_modules: Optional[list] = None,
    debug: bool = False,
) -> dict:
    return await kernel_apex_verdict(query, session_id, agi_result, asi_result, capability_modules, debug)

@mcp.tool(annotations=TOOL_ANNOTATIONS["vault_seal"])
@constitutional_floor("F1", "F3")
async def vault_seal(
    session_id: str,
    verdict: str,
    output: str,
    evidence: Optional[list] = None,
    merkle_hash: Optional[str] = None,
) -> dict:
    return await kernel_vault_seal(session_id, verdict, output, evidence, merkle_hash)

if __name__ == "__main__":
    mcp.run()
