"""
maintenance.py - System Health & Maintenance (v55)

Provides health check endpoints and system status reporting.
Used by L4 tools and external monitoring dashboards.
"""

import sys
import platform
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def health_check() -> Dict[str, Any]:
    """
    Perform a comprehensive system health check.
    Returns a dictionary with component-level status (green/yellow/red).
    """
    timestamp = time.time()
    components = {}
    overall_status = "GREEN"

    # 1. Core System Info
    status = {
        "status": overall_status,
        "timestamp": timestamp,
        "version": "v55.0-FEDERATION",
        "system": {
            "platform": platform.system(),
            "python": sys.version.split()[0],
            "api_version": "v1",
        },
        "components": components,
    }

    # 2. Validators Check
    try:
        from mcp_server.core.validators import ConstitutionValidator
        components["validators"] = {"status": "green", "detail": "active"}
    except ImportError as e:
        components["validators"] = {"status": "red", "detail": f"failed: {e}"}
        overall_status = "RED"

    # 3. Kernel Manager Check (AGI/ASI/APEX cores)
    try:
        from codebase.kernel import get_kernel_manager
        km = get_kernel_manager()
        
        # Check AGI
        try:
            agi = km.get_agi()
            agi_status = "green"
        except Exception as e:
            agi_status = "red"
            overall_status = "RED" if overall_status == "GREEN" else overall_status
        
        # Check ASI
        try:
            asi = km.get_asi()
            asi_status = "green"
        except Exception as e:
            asi_status = "red"
            overall_status = "RED" if overall_status == "GREEN" else overall_status
        
        # Check APEX
        try:
            apex = km.get_apex()
            apex_status = "green"
        except Exception as e:
            apex_status = "red"
            overall_status = "RED" if overall_status == "GREEN" else overall_status
        
        components["kernel_manager"] = {
            "status": overall_status if overall_status != "GREEN" else "green",
            "detail": {
                "agi": agi_status,
                "asi": asi_status,
                "apex": apex_status,
            }
        }
    except ImportError as e:
        components["kernel_manager"] = {"status": "red", "detail": f"failed: {e}"}
        overall_status = "RED"

    # 4. Session Store Check
    try:
        from codebase.state import SessionStore
        store = SessionStore()
        components["session_store"] = {"status": "green", "detail": "active"}
    except ImportError as e:
        components["session_store"] = {"status": "red", "detail": f"failed: {e}"}
        overall_status = "RED"

    # 5. Floor Validators Check (F1-F13)
    try:
        from codebase.floors import FloorRegistry
        floor_count = len(FloorRegistry.list_floors()) if hasattr(FloorRegistry, 'list_floors') else 13
        components["floor_validators"] = {
            "status": "green",
            "detail": f"{floor_count} floors registered"
        }
    except ImportError as e:
        components["floor_validators"] = {"status": "yellow", "detail": f"warning: {e}"}
        if overall_status == "GREEN":
            overall_status = "YELLOW"

    # 6. Tool Registry Check
    try:
        from mcp_server.core.tool_registry import ToolRegistry
        registry = ToolRegistry()
        tool_count = len(registry.list_tools())
        components["tool_registry"] = {
            "status": "green",
            "detail": f"{tool_count} tools registered"
        }
    except ImportError as e:
        components["tool_registry"] = {"status": "red", "detail": f"failed: {e}"}
        overall_status = "RED"

    # 7. Bridge Check
    try:
        from mcp_server.bridge import BridgeRouter
        components["bridge"] = {"status": "green", "detail": "functional"}
    except ImportError as e:
        components["bridge"] = {"status": "yellow", "detail": f"warning: {e}"}
        if overall_status == "GREEN":
            overall_status = "YELLOW"

    status["status"] = overall_status
    return status


def bridge_check() -> bool:
    """
    Verify the bridge shim is functional.
    """
    try:
        from mcp_server.bridge import BridgeRouter
        return True
    except ImportError:
        return False


def get_component_status(component_name: str) -> Dict[str, Any]:
    """
    Get status of a specific component.
    """
    full_health = health_check()
    return full_health.get("components", {}).get(component_name, {
        "status": "unknown",
        "detail": "Component not found"
    })
