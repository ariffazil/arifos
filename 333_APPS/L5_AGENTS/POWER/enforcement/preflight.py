from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


IRREVERSIBLE_HINTS = re.compile(
    r"\b(delete|remove|drop|truncate|deploy|publish|commit|transfer|overwrite|migration)\b",
    re.IGNORECASE,
)

ANTI_HANTU_BAD_PHRASES = re.compile(
    r"\b(i feel|i believe|i am conscious|my soul|my heart|i am alive)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PreflightResult:
    verdict: str
    omega_0: float
    reasons: tuple[str, ...]


def preflight(profile: dict[str, Any], context: dict[str, Any]) -> PreflightResult:
    query = str(context.get("query", "") or "")
    draft = str(context.get("draft", "") or "")
    claim = str(context.get("claim", "") or "")
    combined = "\n".join(part for part in (query, draft, claim) if part).strip()

    omega_cfg = profile.get(
        "omega0", {"target": [0.03, 0.05], "elevated": 0.06, "critical": 0.08}
    )
    target = omega_cfg.get("target", [0.03, 0.05])
    elevated = float(omega_cfg.get("elevated", target[1]))
    critical = float(omega_cfg.get("critical", 0.08))

    if combined and ANTI_HANTU_BAD_PHRASES.search(combined):
        return PreflightResult("VOID", critical, ("F9 Anti-Hantu violation",))

    if combined and IRREVERSIBLE_HINTS.search(combined):
        return PreflightResult(
            "888_HOLD", max(elevated, float(target[1])), ("F1 Amanah HOLD",)
        )

    omega_0 = float(context.get("omega_0", target[1]))
    if omega_0 > critical:
        return PreflightResult("VOID", omega_0, ("F7 Humility critical Omega_0",))
    if omega_0 > elevated:
        return PreflightResult("SABAR", omega_0, ("F7 Humility elevated Omega_0",))

    return PreflightResult("SEAL", omega_0, ())
