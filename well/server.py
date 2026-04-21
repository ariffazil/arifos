import sys
import os

# Add parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arifos.well.api.mcp_tools import mcp

if __name__ == "__main__":
    # In production, this would be the entrypoint
    mcp.run()
