"""
MCP Tools - Constitutional AI Governance (v55.3)
Location: codebase/mcp/tools/

Glocal Consolidation: This module exports the canonical MCP tools.

Tools (from canonical_trinity.py):
- init_gate: Constitutional initialization (000)
- agi_genius: Mind Engine with metrics/evidence (111-333)
- asi_act: Heart Engine with empathy and ethics (444-666)
- apex_judge: Soul Engine with judgment (777-888)
- vault_999: Immutable governance ledger (999)

Stub tools (agi_tool, asi_tool, apex_tool, trinity_hat) archived in v55.3.
Use canonical_trinity functions instead.

DITEMPA BUKAN DIBERI
"""

# Canonical implementations (real kernels)
from .canonical_trinity import (
    mcp_init,
    mcp_agi,
    mcp_asi,
    mcp_apex,
    mcp_vault,
    mcp_trinity,
    mcp_reality,
)

# Vault tool (direct access)
from .vault_tool import VaultTool

__all__ = [
    # Canonical MCP tools
    "mcp_init",
    "mcp_agi",
    "mcp_asi",
    "mcp_apex",
    "mcp_vault",
    "mcp_trinity",
    "mcp_reality",
    # Direct vault access
    "VaultTool",
]
