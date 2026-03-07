"""
L6_CIVILIZATION: Resource Governor
Canon: C:/Users/User/arifOS/333_APPS/L6_CIVILIZATION/resource_governor.py

Treats VPS RAM as the "thermodynamic budget" of the civilization.
Enforces limits so local Ollama limits and agent footprints don't cause OOM kills.
"""

import json
import psutil
from typing import Dict, Any

# Assuming 16GB total VPS RAM. Safety threshold at 20% free (around 3.2GB).
RAM_SAFETY_THRESHOLD_PERCENT = 20.0 

def _get_free_ram_percent() -> float:
    """Gets current free RAM percentage (mocked via psutil for now)."""
    mem = psutil.virtual_memory()
    return mem.available / mem.total * 100.0

def request_permit(task_id: str, estimated_cost_mb: int, estimated_tokens: int) -> Dict[str, Any]:
    """
    Called by an Agent or MCP tool before attempting heavy workloads 
    (like embedding generation or heavy LLM inference).
    
    Returns:
        {"verdict": "ALLOW"|"QUEUE"|"DENY", "reason": "...", "queue_id": ...}
    """
    free_ram_pct = _get_free_ram_percent()
    
    # Floor F12 Defense Mechanism: Prevent OOM
    if free_ram_pct < RAM_SAFETY_THRESHOLD_PERCENT:
        return {
            "verdict": "QUEUE",
            "reason": f"F12 Violation Prevented: Free RAM at {free_ram_pct:.1f}% (below {RAM_SAFETY_THRESHOLD_PERCENT}%).",
            "queue_id": f"queue_{task_id}"
        }
    
    # Token check logic could be inserted here
    if estimated_tokens > 8192: # Arbitrary high token context example
        return {
            "verdict": "DENY",
            "reason": "Token budget exceeded for single synchronous operation.",
            "queue_id": None
        }

    return {
        "verdict": "ALLOW",
        "reason": f"RAM healthy ({free_ram_pct:.1f}% free). Thermodynamics stable.",
        "queue_id": None
    }
