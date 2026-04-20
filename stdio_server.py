#!/usr/bin/env python3
"""
arifOS MCP — stdio transport entrypoint

Used by local MCP clients (Cursor, Claude, Gemini, Kimi) that speak
stdio JSON-RPC. This script runs inside the Docker container via:

    docker exec -i arifosmcp python /usr/src/app/stdio_server.py

DITEMPA BUKAN DIBERI
"""
from arifos.mcp_server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=False, log_level="CRITICAL")
