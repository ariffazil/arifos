import os
import json
from typing import Optional


def config_flags(
    config_path: Optional[str] = None,
    env_prefix: Optional[str] = "ARIFOS",
    include_secrets: bool = False,
) -> dict:
    """
    Reads environment and feature flags with mandatory secret masking (V2).

    Args:
        config_path (str): Optional path to a config file.
        env_prefix (str): Prefix to filter env vars (default: ARIFOS).
        include_secrets (bool): If True, returns raw secrets.
                                WARNING: F1 Violation if used without valid 888 Auth.

    Returns:
        dict: A dictionary containing safely masked flags.
    """
    flags = {"environment_variables": {}, "from_file": {}}

    # F1 Amanah: Define patterns that trigger masking
    SECRET_PATTERNS = ["KEY", "TOKEN", "SECRET", "PASS", "PWD", "AUTH", "CREDENTIAL", "SIGNATURE"]

    def _mask_value(key: str, value: str) -> str:
        """Masks the value if the key is a secret and include_secrets is False."""
        if include_secrets:
            return value

        # Check if key contains any secret pattern
        upper_key = key.upper()
        if any(p in upper_key for p in SECRET_PATTERNS):
            if len(value) > 8:
                return f"{value[:3]}...{value[-3:]} (REDACTED)"
            return "******** (REDACTED)"
        return value

    # 1. Read Environment Variables
    # We look for ARIFOS_*, MCP_*, or the custom prefix
    prefixes = ["ARIFOS_", "MCP_"]
    if env_prefix and env_prefix not in prefixes:
        prefixes.append(env_prefix)

    for key, value in os.environ.items():
        if any(key.startswith(p) for p in prefixes):
            flags["environment_variables"][key] = _mask_value(key, value)

    # 2. Read Config File
    path_to_read = config_path or os.environ.get("ARIFOS_CONFIG_FILE")

    if path_to_read and os.path.exists(path_to_read):
        try:
            with open(path_to_read, "r") as f:
                data = json.load(f)
                # Recursively mask file data (simplified flat masking for now)
                masked_data = {}
                for k, v in data.items():
                    if isinstance(v, str):
                        masked_data[k] = _mask_value(k, v)
                    else:
                        masked_data[k] = v  # Pass through non-string structures
                flags["from_file"] = masked_data
                flags["config_source"] = path_to_read
        except Exception as e:
            flags["from_file"]["error"] = f"Failed to read config: {str(e)}"

    return flags
