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

__version__ = "55.5.0-RUKUN"

from . import shared
from . import organs

# Convenience exports (public surface)
from .organs import (
    mind,
    heart,
    soul,
    memory,
    init,
    agi,
    asi,
    apex,
    vault,
    sense,
    think,
    reason,
    empathize,
    align,
    sync,
    forge,
    judge,
    seal,
    anchor,
    feel,
)
from .pipeline import forge as forge_pipeline, quick, ForgeResult

__all__ = [
    "shared",
    "organs",
    "mind",
    "heart",
    "soul",
    "memory",
    "init",
    "agi",
    "asi",
    "apex",
    "vault",
    "sense",
    "think",
    "reason",
    "empathize",
    "align",
    "sync",
    "forge",
    "judge",
    "seal",
    "anchor",
    "feel",
    "forge_pipeline",
    "quick",
    "ForgeResult",
]
