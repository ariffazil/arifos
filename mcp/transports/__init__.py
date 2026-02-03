"""
arifOS MCP Transports — Glocal AAA Consolidation (v55.3)

Global + Local = Glocal: One transport layer that works everywhere.

Exports:
    StdioTransport: Local stdio for Claude Desktop, Cursor (BBB Bridge)
    SSETransport: Streamable HTTP for production/cloud (AAA Authority)
    main_auto: Auto-detect transport mode from environment
    main_stdio: Explicit stdio entry point
    main_sse: Explicit SSE entry point

Entry Points:
    python -m mcp.transports [stdio|sse|auto]
    
    aaa-mcp          → main_auto (auto-detect)
    aaa-mcp-sse      → main_sse (production)
    aaa-mcp-stdio    → main_stdio (local dev)

DITEMPA BUKAN DIBERI
"""

from .stdio import StdioTransport
from .sse import SSETransport
from .base import BaseTransport

# Glocal entry points
from .__main__ import main_auto, main_stdio, main_sse

__all__ = [
    # Transports
    "StdioTransport", 
    "SSETransport", 
    "BaseTransport",
    # Entry points
    "main_auto",
    "main_stdio", 
    "main_sse",
]
