"""
arifOS core — Constitutional Kernel (RUKUN AGI)
================================================

The 5-Organ Kernel + 4 Shared Modules.

Organs:
- airlock (init): Session Authentication (F11/F12)
- mind (agi): AGI Evidence Engine (F2/F4/F7/F8)
- heart (asi): ASI Alignment Engine (F1/F5/F6)
- soul (apex): APEX Verdict Engine (F3/F8/F9/F10/F13)
- memory (vault): Constitutional Memory (F1/F13)

Version: v55.5.0-RUKUN
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
DITEMPA BUKAN DIBERI
"""

__version__ = "60.0.0-RUKUN"

from . import organs, shared

# Convenience exports (public surface)
from .organs import (
    agi,
    align,
    anchor,
    apex,
    asi,
    empathize,
    feel,
    forge,
    heart,
    init,
    judge,
    memory,
    mind,
    reason,
    seal,
    sense,
    soul,
    sync,
    think,
    vault,
)
from .pipeline import ForgeResult, quick
from .pipeline import forge as forge_pipeline

__all__ = [
    "organs",
    "shared",
    "init",
    "sense",
    "think",
    "reason",
    "sync",
    "empathize",
    "align",
    "forge",
    "judge",
    "seal",
    "anchor",
    "feel",
    "forge_pipeline",
    "quick",
    "ForgeResult",
]
