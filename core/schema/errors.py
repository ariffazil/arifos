"""
core/schema/errors.py — Normalized Error Schema

Runtime errors go here.  Never bury errors inside payload or data.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SchemaError(BaseModel):
    """
    A single normalized runtime error entry.

    All tool errors must be surfaced here, not buried in payload.
    """

    code: str = Field(description="Machine-readable error code (e.g. IMPORT_ERROR, AUTH_FAIL)")
    message: str = Field(description="Human-readable error description")
    stage: str | None = Field(
        default=None, description="Stage where the error occurred (e.g. 777_FORGE)"
    )
    recoverable: bool = Field(
        default=True,
        description="Whether the error is recoverable without aborting the session",
    )
