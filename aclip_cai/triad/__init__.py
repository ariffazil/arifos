"""
aclip_cai/triad/__init__.py — The 3 Triads of arifOS
"""
from .delta.anchor import anchor
from .delta.reason import reason
from .delta.integrate import integrate

from .omega.respond import respond
from .omega.validate import validate
from .omega.align import align

from .psi.forge import forge
from .psi.audit import audit
from .psi.seal import seal

__all__ = [
    "anchor", "reason", "integrate",
    "respond", "validate", "align",
    "forge", "audit", "seal"
]
