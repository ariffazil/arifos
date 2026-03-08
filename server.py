"""
server.py — arifOS AAA MCP root entrypoint

Thin shim so deployment platforms (Railway, Render, Fly.io)
and `fastmcp dev server.py` can discover the server without
knowing the internal package structure.

Real implementation: arifosmcp/runtime/server.py
"""

from arifosmcp.runtime import create_aaa_mcp_server

mcp = create_aaa_mcp_server()

if __name__ == "__main__":
    mcp.run()
