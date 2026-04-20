"""
Backward-compatible GEOX MCP entrypoint.

Canonical public server: geox_unified_mcp_server.py
"""

from __future__ import annotations

try:
    import fastmcp

    FASTMCP_VERSION = tuple(map(int, fastmcp.__version__.split(".")[:2]))
    IS_FASTMCP_3 = FASTMCP_VERSION >= (3, 0)
except Exception:
    IS_FASTMCP_3 = False

from geox_unified_mcp_server import *  # noqa: F401,F403


if __name__ == "__main__":
    main()
