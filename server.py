"""
server.py — arifOS MCP Server Entry Point
==========================================

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from arifos.adapters.mcp.server import app, mcp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)