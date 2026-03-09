"""
core/schema — Canonical Output Schema for arifOS MCP Tools

Single source of truth for all tool output envelopes.

Public surface::

    from core.schema import ArifOSOutput, Verdict, Status, Stage, Metrics
    from core.schema import Trace, Authority, Meta, SchemaError
    from core.schema import VerdictValidator

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from core.schema.authority import Authority, AuthorityLevel, AuthState
from core.schema.errors import SchemaError
from core.schema.meta import DebugBlock, Meta
from core.schema.metrics import Metrics
from core.schema.output import ArifOSOutput
from core.schema.stage import Stage, stage_weight
from core.schema.trace import Trace
from core.schema.validator import VerdictValidator
from core.schema.verdict import (
    COMMITMENT_TOOLS,
    EXPLORATORY_TOOLS,
    SAFETY_TOOLS,
    Status,
    Verdict,
)

__all__ = [
    # Core envelope
    "ArifOSOutput",
    # Enums
    "Verdict",
    "Status",
    "Stage",
    "AuthorityLevel",
    "AuthState",
    # Schema models
    "Metrics",
    "Trace",
    "Authority",
    "SchemaError",
    "Meta",
    "DebugBlock",
    # Validator
    "VerdictValidator",
    # Helpers
    "stage_weight",
    # Tool classifications
    "EXPLORATORY_TOOLS",
    "SAFETY_TOOLS",
    "COMMITMENT_TOOLS",
]
