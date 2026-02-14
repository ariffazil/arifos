"""
core/ — arifOS Kernel (v64.1-GAGI)

Reusable brain + physics + organs
Imported by: aaa_mcp (MCP wrapper), future products

Components:
- uncertainty_engine: 5-dim vector with harmonic/geometric mean
- governance_kernel: Conditional AWAITING_888
- telemetry: 30-day locked adaptation
"""

__version__ = "64.1.0"

# Expose kernel components
from .uncertainty_engine import UncertaintyEngine, UncertaintyVector, calculate_uncertainty
from .governance_kernel import GovernanceKernel, GovernanceState, AuthorityLevel, get_governance_kernel
from .telemetry import log_telemetry, check_adaptation_status, telemetry_store

__all__ = [
    "UncertaintyEngine",
    "UncertaintyVector", 
    "calculate_uncertainty",
    "GovernanceKernel",
    "GovernanceState",
    "AuthorityLevel",
    "get_governance_kernel",
    "log_telemetry",
    "check_adaptation_status",
    "telemetry_store",
]
