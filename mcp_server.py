"""
mcp_server.py — arifOS Unified Entry Point
Imports the thin transport layer which in turn utilizes aclip_cai.
"""
import sys
import os

# Ensure package discovery
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aaa_mcp.server import mcp

if __name__ == "__main__":
    # Start the unified MCP server
    mcp.run()
