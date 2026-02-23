"""FastMCP extension layer for arifOS AAA MCP.

This package isolates FastMCP-specific integration concerns outside `core/`.
"""

from .discovery import build_surface_discovery
from .server_surface import build_server
from .telemetry import TelemetryStore
from .transports import run_server

__all__ = [
    "build_server",
    "run_server",
    "TelemetryStore",
    "build_surface_discovery",
]
