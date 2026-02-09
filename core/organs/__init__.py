"""
core/organs/__init__.py — Organ Exports

RUKUN AGI 5-Organ Kernel:
    _0_init  → The Airlock (Stages 000-111)
    _1_agi   → The Mind (Stages 111-333)
    _2_asi   → The Heart (Stages 555-666)
    _3_apex  → The Soul (Stages 444-777-888)
    _4_vault → The Memory (Stage 999)

Usage:
    from core.organs import init, agi, asi, apex, vault
    
    # Or granular imports
    from core.organs import sense, empathize, sync, seal

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

# Import all organs
from core.organs import _0_init
from core.organs import _1_agi
from core.organs import _2_asi
from core.organs import _3_apex
from core.organs import _4_vault

# Re-export main functions (unified interfaces)
from core.organs._0_init import init
from core.organs._1_agi import agi
from core.organs._2_asi import asi
from core.organs._3_apex import apex
from core.organs._4_vault import vault

# Re-export actions for direct use
from core.organs._0_init import (
    init,
    scan_injection,
    verify_auth,
)

from core.organs._1_agi import (
    sense,
    think,
    reason,
)

from core.organs._2_asi import (
    empathize,
    align,
)

from core.organs._3_apex import (
    sync,
    forge,
    judge,
)

from core.organs._4_vault import (
    seal,
    query,
    verify,
)

__all__ = [
    # Organ modules
    "_0_init",
    "_1_agi",
    "_2_asi",
    "_3_apex",
    "_4_vault",
    
    # Unified interfaces
    "init",
    "agi",
    "asi",
    "apex",
    "vault",
    
    # Actions
    "scan_injection",  # F12
    "verify_auth",     # F11
    "sense",           # Stage 111
    "think",           # Stage 222
    "reason",          # Stage 333
    "empathize",       # Stage 555
    "align",           # Stage 666
    "sync",            # Stage 444
    "forge",           # Stage 777
    "judge",           # Stage 888
    "seal",            # Stage 999
    "query",           # Vault read
    "verify",          # Vault verify
]
