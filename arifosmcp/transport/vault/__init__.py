"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""
Vault hardened modules.
"""

from .hardened import (
    EUREKA_THRESHOLD,
    SABAR_THRESHOLD,
    EUREKAScore,
    HardenedAnomalousContrastEngine,
    HardenedEUREKASieve,
    create_hardened_sieve,
    should_seal_to_vault_hardened,
)

__all__ = [
    "HardenedAnomalousContrastEngine",
    "HardenedEUREKASieve",
    "EUREKAScore",
    "EUREKA_THRESHOLD",
    "SABAR_THRESHOLD",
    "create_hardened_sieve",
    "should_seal_to_vault_hardened",
]
