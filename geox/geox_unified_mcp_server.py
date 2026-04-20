# GEOX Forwarding Shim — FastMCP Server
# DITEMPA BUKAN DIBERI
#
# This file is a backward-compatibility shim.
# The canonical server is now at: control_plane.fastmcp.server

from control_plane.fastmcp.server import mcp, create_app, main

__all__ = ["mcp", "create_app", "main"]

if __name__ == "__main__":
    main()
