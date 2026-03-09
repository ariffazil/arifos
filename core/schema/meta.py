"""
core/schema/meta.py — Response Metadata Schema

Schema/admin metadata block — timestamps, versioning, debug flags.
This is the ONLY place for schema/admin metadata.

debug must never appear as True in production responses unless
explicitly requested by the caller.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

# Increment this when the canonical schema changes in a breaking way.
CURRENT_SCHEMA_VERSION = "1.0.0"


class Meta(BaseModel):
    """
    Response metadata block.

    Contains schema versioning, timestamp, and debug/dry-run flags.
    Never put domain logic here — only admin/observability fields.
    """

    schema_version: str = Field(
        default=CURRENT_SCHEMA_VERSION, description="Canonical schema version"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp of response generation",
    )
    debug: bool = Field(
        default=False,
        description="Whether debug fields are included in this response",
    )
    dry_run: bool = Field(
        default=False,
        description="Whether this was a dry-run (no side effects committed)",
    )


class DebugBlock(BaseModel):
    """
    Optional debug appendix — only present when meta.debug == True.

    Must NEVER appear in production responses unless explicitly requested.
    """

    reasoning: dict[str, Any] | None = None
    witness: dict[str, Any] | None = None
    raw_engine: dict[str, Any] | None = None
    contradictions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
