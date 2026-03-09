"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""
Self-Ops Module for arifOS MCP Bridge

Infrastructure health monitoring and auto-remediation.
Part of the adapter layer, not the constitutional kernel.
"""

from .diagnostics import (
    HealthCheckResult,
    SelfOpsDiagnostics,
    SelfOpsReport,
    get_self_ops,
    self_diagnose,
)

__all__ = [
    "HealthCheckResult",
    "SelfOpsDiagnostics",
    "SelfOpsReport",
    "get_self_ops",
    "self_diagnose",
]
