"""
aclip_cai/core/floor_audit.py — Forwarding Stub

This file has been deprecated as a standalone module. The LIVE floor
auditor has been moved to its canonical location in core.shared.floor_audit.
It is imported here intact to preserve backwards compatibility for existing
aclip_cai agents and triad functions.
"""

from core.shared.floor_audit import (
    AuditResult,
    FloorAuditor,
    FloorResult,
    Verdict,
)

__all__ = ["Verdict", "FloorResult", "AuditResult", "FloorAuditor"]
