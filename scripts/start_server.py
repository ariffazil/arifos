"""
arifOS MCP Server — Railway Production Entry Point

Starts the constitutional MCP server with all 9 tools on SSE transport.
Health endpoint at /health for Railway healthchecks.
Tool list at / for service discovery.

DITEMPA BUKAN DIBERI
"""

import os

# Railway provides PORT and HOST via environment
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")

from aaa_mcp.server import mcp  # noqa: E402 — env must be set before import

# SSE transport for remote MCP clients
# Serves: /sse (events), /messages (POST), /health (GET), / (GET)
mcp.run(transport="sse", host=host, port=port)
