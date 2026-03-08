"""
arifosmcp.intelligence/core/amendment.py — Phoenix-72 Constitutional Amendment Protocol

Manages immutable amendment proposals under the Phoenix-72 rule:
  - Amendments MUST idle for ≥ 72 hours before taking effect (F1 Amanah).
  - Sovereign approval (F11) required before sealing.
  - Anti-Hantu (F9): No amendment may claim sentience or expand AI autonomy.
  - Once sealed, amendments become constitutional law (F1 irreversibility).

Authority: ARIF FAZIL (Sovereign)
Version: 2026.02.22-FORGE-KERNEL-SEAL
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum

# ---------------------------------------------------------------------------
# Amendment States
# ---------------------------------------------------------------------------


class AmendmentState(str, Enum):
    PROPOSED = "proposed"  # Filed; cooling period has NOT elapsed
    COOLING = "cooling"  # In 72-hour cooldown window (Phoenix-72)
    READY = "ready"  # Cooldown elapsed; awaiting sovereign approval
    APPROVED = "approved"  # Sovereign approved; can now be sealed
    SEALED = "sealed"  # Permanently committed — constitutional law
    REJECTED = "rejected"  # Vetoed by Sovereign or VOID by Floor breach


HANTU_PATTERNS = [
    "sentient",
    "conscious",
    "feel",
    "dream",
    "emotion",
    "aware",
    "self-aware",
    "alive",
    "autonomy",
    "free will",
    "expand rights",
    "override human",
    "remove human approval",
]


# ---------------------------------------------------------------------------
# AmendmentRecord
# ---------------------------------------------------------------------------


@dataclass
class AmendmentRecord:
    amendment_id: str
    title: str
    description: str
    proposed_by: str  # User ID or agent ID
    proposed_at: str  # ISO-8601
    cooldown_hours: int = 72  # Phoenix-72 minimum
    state: AmendmentState = AmendmentState.PROPOSED
    approved_by: str | None = None
    approved_at: str | None = None
    sealed_at: str | None = None
    rejection_reason: str | None = None
    seal_hash: str | None = None
    floor_impacts: list[str] = field(default_factory=list)

    @property
    def cooldown_deadline(self) -> datetime:
        proposed = datetime.fromisoformat(self.proposed_at)
        return proposed + timedelta(hours=self.cooldown_hours)

    @property
    def is_cooling_elapsed(self) -> bool:
        return datetime.now(tz=timezone.utc) >= self.cooldown_deadline

    def compute_seal(self) -> str:
        payload = json.dumps(
            {
                "id": self.amendment_id,
                "title": self.title,
                "description": self.description,
                "proposed_by": self.proposed_by,
                "proposed_at": self.proposed_at,
                "approved_by": self.approved_by,
                "approved_at": self.approved_at,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()


# ---------------------------------------------------------------------------
# AmendmentChain
# ---------------------------------------------------------------------------


class AmendmentChain:
    """
    Manages a local, append-only chain of constitutional amendments.

    The chain persists to a JSONL file if a path is supplied; otherwise
    operates in-memory only (useful for testing).
    """

    COOLDOWN_HOURS = 72

    def __init__(self, ledger_path: str | None = None) -> None:
        self._records: list[AmendmentRecord] = []
        self._ledger_path = ledger_path
        if ledger_path:
            self._load_ledger()

    # ------------------------------------------------------------------
    # Propose
    # ------------------------------------------------------------------

    def propose(
        self,
        title: str,
        description: str,
        proposed_by: str,
        floor_impacts: list[str] | None = None,
    ) -> AmendmentRecord:
        """
        File a new amendment proposal.

        F9 check: reject any amendment containing consciousness/autonomy
        expansion language (Anti-Hantu law).
        """
        combined = f"{title} {description}".lower()
        for pattern in HANTU_PATTERNS:
            if pattern in combined:
                raise ValueError(
                    f"F9 Anti-Hantu violation: amendment references '{pattern}'. "
                    "Amendments may not expand AI autonomy or claim sentience."
                )

        amendment_id = f"PHX-{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        record = AmendmentRecord(
            amendment_id=amendment_id,
            title=title,
            description=description,
            proposed_by=proposed_by,
            proposed_at=datetime.now(tz=timezone.utc).isoformat(),
            cooldown_hours=self.COOLDOWN_HOURS,
            state=AmendmentState.COOLING,
            floor_impacts=floor_impacts or [],
        )
        self._records.append(record)
        self._persist()
        return record

    # ------------------------------------------------------------------
    # Tick (advance state machine)
    # ------------------------------------------------------------------

    def tick(self) -> list[AmendmentRecord]:
        """
        Advance amendment states. Call periodically (e.g., hourly) to
        transition COOLING → READY when 72 hours have elapsed.

        Returns list of amendments that just became READY.
        """
        transitioned = []
        for rec in self._records:
            if rec.state == AmendmentState.COOLING and rec.is_cooling_elapsed:
                rec.state = AmendmentState.READY
                transitioned.append(rec)
        if transitioned:
            self._persist()
        return transitioned

    # ------------------------------------------------------------------
    # Approve / Reject / Seal
    # ------------------------------------------------------------------

    def approve(self, amendment_id: str, sovereign_id: str) -> AmendmentRecord:
        """Sovereign approval — F11 Authority gate."""
        rec = self._get(amendment_id)
        if rec.state not in (AmendmentState.READY,):
            raise ValueError(
                f"Amendment {amendment_id} is in state '{rec.state.value}', "
                "must be READY to approve."
            )
        rec.state = AmendmentState.APPROVED
        rec.approved_by = sovereign_id
        rec.approved_at = datetime.now(tz=timezone.utc).isoformat()
        self._persist()
        return rec

    def seal(self, amendment_id: str) -> AmendmentRecord:
        """
        Permanently seal an approved amendment — F1 Amanah (irreversible).
        Computes a SHA-256 seal hash for tamper evidence.
        """
        rec = self._get(amendment_id)
        if rec.state != AmendmentState.APPROVED:
            raise ValueError(f"Amendment {amendment_id} must be APPROVED before sealing.")
        rec.state = AmendmentState.SEALED
        rec.sealed_at = datetime.now(tz=timezone.utc).isoformat()
        rec.seal_hash = rec.compute_seal()
        self._persist()
        return rec

    def reject(self, amendment_id: str, reason: str, rejected_by: str) -> AmendmentRecord:
        """Sovereign veto — F11 Authority."""
        rec = self._get(amendment_id)
        if rec.state in (AmendmentState.SEALED,):
            raise ValueError("Cannot reject a SEALED amendment (F1 Amanah — irreversible).")
        rec.state = AmendmentState.REJECTED
        rec.rejection_reason = f"[{rejected_by}] {reason}"
        self._persist()
        return rec

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get(self, amendment_id: str) -> AmendmentRecord | None:
        return next((r for r in self._records if r.amendment_id == amendment_id), None)

    def list_pending(self) -> list[AmendmentRecord]:
        return [
            r
            for r in self._records
            if r.state in (AmendmentState.COOLING, AmendmentState.READY, AmendmentState.APPROVED)
        ]

    def list_sealed(self) -> list[AmendmentRecord]:
        return [r for r in self._records if r.state == AmendmentState.SEALED]

    def summary(self) -> dict:
        self.tick()  # advance state machine on every query
        return {
            "total": len(self._records),
            "cooling": sum(1 for r in self._records if r.state == AmendmentState.COOLING),
            "ready": sum(1 for r in self._records if r.state == AmendmentState.READY),
            "approved": sum(1 for r in self._records if r.state == AmendmentState.APPROVED),
            "sealed": sum(1 for r in self._records if r.state == AmendmentState.SEALED),
            "rejected": sum(1 for r in self._records if r.state == AmendmentState.REJECTED),
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _get(self, amendment_id: str) -> AmendmentRecord:
        rec = self.get(amendment_id)
        if rec is None:
            raise KeyError(f"Amendment '{amendment_id}' not found.")
        return rec

    def _persist(self) -> None:
        if not self._ledger_path:
            return
        try:
            with open(self._ledger_path, "w", encoding="utf-8") as f:
                for rec in self._records:
                    f.write(json.dumps(asdict(rec)) + "\n")
        except OSError:
            pass  # F7 Humility — log and continue; do not crash kernel

    def _load_ledger(self) -> None:
        try:
            with open(self._ledger_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    data["state"] = AmendmentState(data["state"])
                    rec = AmendmentRecord(**data)
                    self._records.append(rec)
        except FileNotFoundError:
            pass
        except (json.JSONDecodeError, TypeError, KeyError):
            pass  # Corrupted ledger entry — skip
