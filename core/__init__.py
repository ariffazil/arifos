"""
core/ — arifOS Kernel (v64.1-GAGI)

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

__version__ = "64.1.0"

# Expose kernel components for import
from . import uncertainty_engine
from . import governance_kernel
from . import telemetry
from . import judgment
from . import organs

__all__ = [
    "uncertainty_engine",
    "governance_kernel",
    "telemetry",
    "judgment",
    "organs",
]
