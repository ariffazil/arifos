"""
arifOS v60: Constitutional Kernel
==================================

The 5-Organ Kernel + 4 Shared Modules.

Organs:
- core_init: Session Authentication (F11/F12)
- core_agi: AGI Evidence Engine (F2/F4/F7)
- core_asi: ASI Alignment Engine (F5/F6/F9)
- core_apex: APEX Verdict Engine (F3/F8/F10)
- core_memory: Constitutional Memory (F1/F13)

Version: v60.0-FORGE
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
DITEMPA BUKAN DIBERI 💎🔥🧠
"""

__version__ = "60.0.0-FORGE"

# Note: Actual organs will be imported once core_init and core_agi are built
# For now, we export shared modules

from . import shared

__all__ = [
    "shared",
]
