"""Pipeline gate helpers for no-bypass enforcement."""

from __future__ import annotations


def should_halt_on_auditor(auditor_verdict: str) -> bool:
    return str(auditor_verdict).upper() != "SEAL"
