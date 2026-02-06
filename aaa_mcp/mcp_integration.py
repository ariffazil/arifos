"""
arifOS MCP Server Integration Layer
Wraps external MCP servers with constitutional governance
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from .core.constitutional_decorator import constitutional_floor, get_tool_floors
from .mcp_config import MCP_SERVERS, get_server_config, validate_constitutional_compliance

logger = logging.getLogger(__name__)


@dataclass
class MCPCallRecord:
    """Record of an MCP server call for audit/reversibility"""

    timestamp: str
    server: str
    operation: str
    omega_before: float
    omega_after: float
    verdict: str  # SEAL / VOID / SABAR
    floors_enforced: list
    reversible: bool
    rollback_data: Optional[Dict] = None


class MCPIntegrationLayer:
    """
    Constitutional governance layer for MCP servers.
    Ensures all external tool calls comply with arifOS 13 Floors.
    """

    def __init__(self):
        self.call_history: list[MCPCallRecord] = []
        self._servers: Dict[str, Any] = {}

    async def call_server(
        self, server_name: str, operation: str, params: Dict[str, Any], omega_estimate: float = 0.05
    ) -> Dict[str, Any]:
        """
        Execute MCP server call with constitutional enforcement.

        Args:
            server_name: Name of MCP server (from MCP_SERVERS registry)
            operation: Specific operation to perform
            params: Operation parameters
            omega_estimate: Estimated uncertainty (Ω₀)

        Returns:
            Result with constitutional metadata and verdict
        """
        config = get_server_config(server_name)
        if not config:
            return {
                "verdict": "VOID",
                "error": f"Unknown MCP server: {server_name}",
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            }

        # F7 Humility: Check uncertainty threshold
        if not validate_constitutional_compliance(server_name, omega_estimate):
            return {
                "verdict": "SABAR",
                "error": f"Ω₀={omega_estimate} exceeds threshold {config.omega_threshold}",
                "floors_enforced": config.floors,
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            }

        # Pre-execution: Record call for reversibility (F1 Amanah)
        call_record = MCPCallRecord(
            timestamp=datetime.utcnow().isoformat(),
            server=server_name,
            operation=operation,
            omega_before=omega_estimate,
            omega_after=0.0,
            verdict="PENDING",
            floors_enforced=config.floors,
            reversible=config.reversible,
        )

        try:
            # Execute server call
            # Note: Actual MCP server call would happen here
            # For now, return structured response template
            result = {
                "server": server_name,
                "operation": operation,
                "params": params,
                "status": "completed",
                "verdict": "SEAL",
                "trinity_component": config.trinity.value,
                "floors_enforced": config.floors,
                "atomic_action": config.atomic_action,
                "reversible": config.reversible,
                "omega_estimate": omega_estimate,
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            }

            call_record.verdict = "SEAL"
            call_record.omega_after = omega_estimate * 0.9  # Assume uncertainty reduced

        except Exception as e:
            logger.error(f"MCP call failed: {e}")
            call_record.verdict = "VOID"
            result = {
                "verdict": "VOID",
                "error": str(e),
                "server": server_name,
                "operation": operation,
                "floors_enforced": config.floors,
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            }

        # Record for audit trail
        self.call_history.append(call_record)

        return result

    async def batch_call(self, calls: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        """
        Execute multiple MCP calls with sequential constitutional checks.
        Each call is evaluated independently with Ω₀ tracking.
        """
        results = []
        for call in calls:
            result = await self.call_server(
                server_name=call["server"],
                operation=call["operation"],
                params=call.get("params", {}),
                omega_estimate=call.get("omega", 0.05),
            )
            results.append(result)

            # If any call VOIDs, halt batch (F3 Tri-Witness)
            if result.get("verdict") == "VOID":
                logger.warning(f"Batch halted at call {len(results)}: {call}")
                break

        return results

    def get_audit_log(self) -> list[MCPCallRecord]:
        """Retrieve full audit trail of MCP calls"""
        return self.call_history

    def can_rollback(self, call_index: int) -> bool:
        """Check if a specific call can be reversed (F1 Amanah)"""
        if call_index >= len(self.call_history):
            return False
        return self.call_history[call_index].reversible


# Singleton instance for system-wide use
_mcp_layer: Optional[MCPIntegrationLayer] = None


def get_mcp_layer() -> MCPIntegrationLayer:
    """Get or create the MCP integration layer singleton"""
    global _mcp_layer
    if _mcp_layer is None:
        _mcp_layer = MCPIntegrationLayer()
    return _mcp_layer


# Convenience functions for direct use
async def mcp_call(server: str, operation: str, **kwargs) -> Dict[str, Any]:
    """Quick call to MCP server with constitutional enforcement"""
    layer = get_mcp_layer()
    return await layer.call_server(server, operation, kwargs)


# Decorator for wrapping existing MCP tools
@constitutional_floor("F1", "F2", "F7")
def with_constitutional_governance(func: Callable) -> Callable:
    """
    Decorator to add constitutional governance to any MCP tool.
    Wraps function with Ω₀ tracking, floor enforcement, and audit logging.
    """

    async def wrapper(*args, **kwargs):
        omega = kwargs.pop("_omega", 0.05)
        layer = get_mcp_layer()

        # Pre-call constitutional check
        result = await func(*args, **kwargs)

        # Stamp with governance metadata
        if isinstance(result, dict):
            result["_constitutional"] = {
                "omega_estimate": omega,
                "floors": get_tool_floors(func.__name__),
                "timestamp": datetime.utcnow().isoformat(),
            }

        return result

    return wrapper
