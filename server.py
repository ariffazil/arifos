import os
import sys

from arifosmcp.runtime import create_aaa_mcp_server
from arifosmcp.runtime.fastmcp_ext.transports import run_server

mcp = create_aaa_mcp_server()

if __name__ == "__main__":
    # Standard entrypoint for local execution and deployment platforms
    mode = (sys.argv[1] if len(sys.argv) > 1 else os.getenv("AAA_MCP_TRANSPORT", "stdio")).lower()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))

    try:
        run_server(mcp, mode=mode, host=host, port=port)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)
        sys.exit(1)
