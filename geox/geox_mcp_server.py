"""
Backward-compatible GEOX MCP entrypoint.

Canonical public server: geox_unified_mcp_server.py
"""

from __future__ import annotations

from geox_unified_mcp_server import *  # noqa: F401,F403


if __name__ == "__main__":
    main()
