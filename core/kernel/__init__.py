"""
core.kernel — Intelligence Kernel Singleton
"""

from core.governance_kernel import get_governance_kernel

# Expose global kernel singleton for legacy and internal callers
kernel = get_governance_kernel("global")

__all__ = ["kernel", "get_governance_kernel"]
