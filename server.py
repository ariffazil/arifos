"""
server.py — arifOS MCP Server Entry Point
==========================================

This file is the canonical entrypoint for:
  1. FastMCP Horizon (cloud deploy) — "server.py:mcp"
  2. Local development — "python server.py"

Single source of truth: this file re-exports the arifosmcp FastMCP instance.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_REPO_ROOT))

from arifosmcp.mcp_server import mcp

if __name__ == "__main__":
    mcp.run()
