# GEOX Forwarding Shim — VPS Server
# DITEMPA BUKAN DIBERI
#
# This file is a backward-compatibility shim.
# The canonical server is now at: execution_plane.vps.server

from execution_plane.vps.server import mcp, create_app, main

__all__ = ["mcp", "create_app", "main"]

if __name__ == "__main__":
    main()
