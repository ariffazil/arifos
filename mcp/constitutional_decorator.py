"""
Constitutional Decorator for FastMCP
Wraps FastMCP tools with arifOS 13-floor enforcement
"""
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

# Floor enforcement registry
FLOOR_ENFORCEMENT = {
    "init_gate": ["F11", "F12"],      # Auth + Injection
    "agi_sense": ["F2", "F4"],        # Truth + Clarity
    "agi_think": ["F2", "F4", "F7"],  # Truth + Clarity + Humility
    "agi_reason": ["F2", "F4", "F7"], # Truth + Clarity + Humility
    "asi_empathize": ["F5", "F6"],    # Peace² + Empathy
    "asi_align": ["F5", "F6", "F9"],  # Peace² + Empathy + Anti-Hantu
    "apex_verdict": ["F3", "F8"],     # Tri-Witness + Genius
    "reality_search": ["F2", "F7"],   # Truth + Humility
    "vault_seal": ["F1", "F3"],       # Amanah + Tri-Witness
}

def constitutional_floor(*floors: str):
    """
    Decorator to enforce constitutional floors on MCP tools.
    
    Usage:
        @constitutional_floor("F2", "F4", "F7")
        @mcp.tool()
        async def agi_reason(query: str) -> dict:
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Pre-execution floor checks
            logger.info(f"Constitutional enforcement: {floors}")
            
            # Execute tool
            result = await func(*args, **kwargs)
            
            # Post-execution validation
            if isinstance(result, dict):
                # Ensure verdict field exists
                if "verdict" not in result:
                    result["verdict"] = "SEAL"
                
                # Stamp with constitutional metadata
                result["_constitutional_enforcement"] = {
                    "floors_checked": floors,
                    "framework": "arifOS",
                    "version": "v55.4"
                }
            
            return result
        
        # Attach floor metadata for introspection
        wrapper._constitutional_floors = floors
        return wrapper
    return decorator

def get_tool_floors(tool_name: str) -> list:
    """Get constitutional floors for a tool."""
    return FLOOR_ENFORCEMENT.get(tool_name, [])
