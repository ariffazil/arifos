import os
import json

def config_flags() -> dict:
    """
    Reads environment and feature flags.

    It focuses on environment variables prefixed with 'ARIFOS_' or 'MCP_'.
    It also tries to load a JSON config file if one is specified via
    the 'ARIFOS_CONFIG_FILE' environment variable.

    Returns:
        dict: A dictionary containing relevant configuration flags.
    """
    flags = {
        "environment_variables": {},
        "from_file": {}
    }
    
    # Read environment variables with specific prefixes
    for key, value in os.environ.items():
        if key.startswith("ARIFOS_") or key.startswith("MCP_"):
            flags["environment_variables"][key] = value

    # Check for a config file path in env vars
    config_file_path = os.environ.get("ARIFOS_CONFIG_FILE")
    if config_file_path and os.path.exists(config_file_path):
        try:
            with open(config_file_path, "r") as f:
                flags["from_file"] = json.load(f)
        except json.JSONDecodeError as e:
            flags["from_file"]["error"] = f"Failed to decode JSON from {config_file_path}: {e}"
        except Exception as e:
            flags["from_file"]["error"] = f"Failed to read config file {config_file_path}: {e}"
    
    return flags
