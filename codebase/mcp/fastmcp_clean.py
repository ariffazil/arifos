"""
codebase/mcp/fastmcp_clean.py — Legacy Adapter

Redirects to the canonical aaa_mcp package.
"""

import runpy
import sys

print("Redirecting to aaa_mcp (v55.5)...")
# Execute the aaa_mcp module as a script
try:
    # This is equivalent to `python -m aaa_mcp stdio` if arguments were passed
    # But since the workflow runs this script directly, we might need to invoke run() manually.
    # However, aaa_mcp.__main__ handles the CLI.
    # Let's import aaa_mcp.asi_gateway and run it.

    from aaa_mcp.server import mcp

    # Check arguments
    if len(sys.argv) > 1 and sys.argv[1] == "sse":
        mcp.run(transport="sse", port=6277)
    else:
        mcp.run(transport="stdio")

except Exception as e:
    print(f"Failed to launch aaa_mcp: {e}")
    sys.exit(1)
