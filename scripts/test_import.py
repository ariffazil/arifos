import sys
import os
sys.path.insert(0, os.getcwd())

# Try installing mcp package first
try:
    import mcp
    print("MCP package already available")
except ImportError:
    print("MCP package not available, attempting install...")
    import subprocess
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "mcp", "--break-system-packages"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("MCP package installed successfully")
        else:
            print(f"Failed to install mcp: {result.stderr}")
            # Continue anyway to test other imports
    except Exception as e:
        print(f"Exception during pip install: {e}")

# Try importing the server module
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("server", "./333_APPS/L4_TOOLS/mcp/server.py")
    server_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server_module)
    print("SUCCESS: Server module imports successfully")
except Exception as e:
    print(f"ERROR: Failed to import server module: {e}")
    import traceback
    traceback.print_exc()