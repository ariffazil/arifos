"""
core/ — arifOS Kernel (2026.03.10-METABOLIC-ROUTER-SEAL)

Reusable governance engine containing ALL decision logic.
Imported by: aaa_mcp (wrapper), future products

Components:
- uncertainty_engine: 5-dim vector with harmonic/geometric mean
- governance_kernel: Conditional AWAITING_888
- telemetry: 30-day locked adaptation
- judgment: Canonical verdict interface
- organs: Six constitutional tools

Architecture: Kernel/Wrapper pattern
core/ = decision logic (this package)
aaa_mcp/ = transport only (no decisions)
"""

__version__ = "2026.03.10"

# Expose kernel components for import
from . import enforcement, governance_kernel, judgment, organs, telemetry, uncertainty_engine

__all__ = [
    "enforcement",
    "uncertainty_engine",
    "governance_kernel",
    "telemetry",
    "judgment",
    "organs",
]
