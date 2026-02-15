"""
Legally Defensible Refusal System for arifOS v55.5

R1-R5 taxonomy with 4-layer refusal messages, appeal system, and audit trail.

DITEMPA BUKAN DIBERI — Forged, not given; refusal is integrity under pressure.
"""

from .types import RefusalType, RiskDomain, RefusalResponse
from .builder import generate_refusal_response, load_refusal_config
from .appeal import AppealSystem, Appeal
from .templates import DOMAIN_TEMPLATES, SKIN_TEMPLATES

__all__ = [
    "RefusalType",
    "RiskDomain", 
    "RefusalResponse",
    "generate_refusal_response",
    "load_refusal_config",
    "AppealSystem",
    "Appeal",
    "DOMAIN_TEMPLATES",
    "SKIN_TEMPLATES",
]
