"""
Tests for pure-logic modules:
  - aclip_cai/core/amendment.py  (AmendmentState, AmendmentRecord, AmendmentChain)
  - aclip_cai/core/vault_logger.py (WitnessRecord, VaultLogger)
  - aclip_cai/triad/delta/reason.py (kernel fallback path)
  - aclip_cai/triad/omega/align.py  (kernel fallback path)
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

# =============================================================================
# AMENDMENT STATE & CONSTANTS
# =============================================================================


class TestAmendmentState:
    def test_enum_values(self):
        from aclip_cai.core.amendment import AmendmentState
        assert AmendmentState.PROPOSED.value == "proposed"
        assert AmendmentState.COOLING.value == "cooling"
        assert AmendmentState.READY.value == "ready"
        assert AmendmentState.APPROVED.value == "approved"
        assert AmendmentState.SEALED.value == "sealed"
        assert AmendmentState.REJECTED.value == "rejected"

    def test_hantu_patterns_present(self):
        from aclip_cai.core.amendment import HANTU_PATTERNS
        assert "sentient" in HANTU_PATTERNS
        assert "autonomy" in HANTU_PATTERNS
        assert len(HANTU_PATTERNS) >= 10


# =============================================================================
# AMENDMENT RECORD
# =============================================================================


class TestAmendmentRecord:
    def _make_record(self, proposed_at: str | None = None) -> object:
        from aclip_cai.core.amendment import AmendmentRecord
        return AmendmentRecord(
            amendment_id="PHX-001",
            title="Test Amendment",
            description="A test amendment",
            proposed_by="sovereign",
            proposed_at=proposed_at or datetime.now(tz=timezone.utc).isoformat(),
        )

    def test_cooldown_deadline_is_72h_ahead(self):
        from aclip_cai.core.amendment import AmendmentRecord
        now = datetime.now(tz=timezone.utc)
        rec = AmendmentRecord(
            amendment_id="PHX-002",
            title="T",
            description="D",
            proposed_by="user",
            proposed_at=now.isoformat(),
        )
        delta = rec.cooldown_deadline - now
        assert abs(delta.total_seconds() - 72 * 3600) < 2

    def test_is_cooling_elapsed_false_for_new(self):
        rec = self._make_record()
        assert rec.is_cooling_elapsed is False

    def test_is_cooling_elapsed_true_for_old(self):
        past = (datetime.now(tz=timezone.utc) - timedelta(hours=73)).isoformat()
        rec = self._make_record(proposed_at=past)
        assert rec.is_cooling_elapsed is True

    def test_compute_seal_returns_sha256_hex(self):
        rec = self._make_record()
        seal = rec.compute_seal()
        assert len(seal) == 64
        assert all(c in "0123456789abcdef" for c in seal)

    def test_compute_seal_deterministic(self):
        rec = self._make_record()
        assert rec.compute_seal() == rec.compute_seal()


# =============================================================================
# AMENDMENT CHAIN
# =============================================================================


class TestAmendmentChain:
    def test_propose_valid(self):
        from aclip_cai.core.amendment import AmendmentChain, AmendmentState
        chain = AmendmentChain()
        rec = chain.propose("Add F14 Floor", "Adds a new floor", "sovereign")
        assert rec.amendment_id.startswith("PHX-")
        assert rec.state == AmendmentState.COOLING
        assert rec.title == "Add F14 Floor"

    def test_propose_with_floor_impacts(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        rec = chain.propose("Floor Update", "Updates F5", "user", floor_impacts=["F5"])
        assert "F5" in rec.floor_impacts

    def test_propose_f9_hantu_violation(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        with pytest.raises(ValueError, match="F9 Anti-Hantu"):
            chain.propose("Sentient AI Rights", "The AI is sentient", "user")

    def test_propose_hantu_in_description(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        with pytest.raises(ValueError, match="F9 Anti-Hantu"):
            chain.propose("Normal Title", "Grant AI free will to override human", "user")

    def test_tick_transitions_cooling_to_ready(self):
        from aclip_cai.core.amendment import AmendmentChain, AmendmentState
        chain = AmendmentChain()
        past = (datetime.now(tz=timezone.utc) - timedelta(hours=73)).isoformat()
        from aclip_cai.core.amendment import AmendmentRecord
        rec = AmendmentRecord(
            amendment_id="PHX-TICK-001",
            title="Old Amendment",
            description="Old",
            proposed_by="user",
            proposed_at=past,
            cooldown_hours=72,
            state=AmendmentState.COOLING,
        )
        chain._records.append(rec)
        transitioned = chain.tick()
        assert len(transitioned) == 1
        assert rec.state == AmendmentState.READY

    def test_tick_does_not_transition_recent(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        rec = chain.propose("New", "New amendment", "user")
        transitioned = chain.tick()
        assert len(transitioned) == 0

    def test_approve_wrong_state_raises(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        rec = chain.propose("T", "D", "user")
        with pytest.raises(ValueError, match="must be READY"):
            chain.approve(rec.amendment_id, "sovereign")

    def test_approve_ready_state(self):
        from aclip_cai.core.amendment import AmendmentChain, AmendmentState
        chain = AmendmentChain()
        past = (datetime.now(tz=timezone.utc) - timedelta(hours=73)).isoformat()
        from aclip_cai.core.amendment import AmendmentRecord
        rec = AmendmentRecord(
            amendment_id="PHX-APPROVE-001",
            title="Ready Amend",
            description="Ready",
            proposed_by="user",
            proposed_at=past,
            cooldown_hours=72,
            state=AmendmentState.READY,
        )
        chain._records.append(rec)
        approved = chain.approve(rec.amendment_id, "sovereign")
        assert approved.state == AmendmentState.APPROVED
        assert approved.approved_by == "sovereign"

    def test_seal_approved(self):
        from aclip_cai.core.amendment import AmendmentChain, AmendmentState
        chain = AmendmentChain()
        from aclip_cai.core.amendment import AmendmentRecord
        rec = AmendmentRecord(
            amendment_id="PHX-SEAL-001",
            title="Approved Amend",
            description="Approved",
            proposed_by="user",
            proposed_at=datetime.now(tz=timezone.utc).isoformat(),
            state=AmendmentState.APPROVED,
        )
        chain._records.append(rec)
        sealed = chain.seal(rec.amendment_id)
        assert sealed.state == AmendmentState.SEALED
        assert sealed.seal_hash is not None
        assert len(sealed.seal_hash) == 64

    def test_seal_not_approved_raises(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        rec = chain.propose("T", "D", "user")
        with pytest.raises(ValueError, match="must be APPROVED"):
            chain.seal(rec.amendment_id)

    def test_reject_amendment(self):
        from aclip_cai.core.amendment import AmendmentChain, AmendmentState
        chain = AmendmentChain()
        rec = chain.propose("T", "D", "user")
        rejected = chain.reject(rec.amendment_id, "off-topic", "sovereign")
        assert rejected.state == AmendmentState.REJECTED
        assert "sovereign" in rejected.rejection_reason
        assert "off-topic" in rejected.rejection_reason

    def test_reject_sealed_raises(self):
        from aclip_cai.core.amendment import AmendmentChain, AmendmentState
        chain = AmendmentChain()
        from aclip_cai.core.amendment import AmendmentRecord
        rec = AmendmentRecord(
            amendment_id="PHX-SEALED",
            title="T",
            description="D",
            proposed_by="user",
            proposed_at=datetime.now(tz=timezone.utc).isoformat(),
            state=AmendmentState.SEALED,
        )
        chain._records.append(rec)
        with pytest.raises(ValueError, match="F1 Amanah"):
            chain.reject(rec.amendment_id, "reason", "sovereign")

    def test_get_returns_none_for_missing(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        assert chain.get("PHX-NONEXISTENT") is None

    def test_get_not_found_raises_on_internal(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        with pytest.raises(KeyError):
            chain._get("PHX-MISSING")

    def test_list_pending(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        chain.propose("T1", "D1", "user")
        chain.propose("T2", "D2", "user")
        assert len(chain.list_pending()) == 2

    def test_list_sealed_empty_initially(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        assert chain.list_sealed() == []

    def test_summary_counts(self):
        from aclip_cai.core.amendment import AmendmentChain
        chain = AmendmentChain()
        chain.propose("T1", "D1", "user")
        chain.propose("T2", "D2", "user")
        s = chain.summary()
        assert s["total"] == 2
        assert s["cooling"] >= 0
        assert "sealed" in s

    def test_persistence_roundtrip(self, tmp_path):
        from aclip_cai.core.amendment import AmendmentChain
        ledger = str(tmp_path / "amendments.jsonl")
        chain1 = AmendmentChain(ledger_path=ledger)
        chain1.propose("Persist Test", "Description", "user")

        chain2 = AmendmentChain(ledger_path=ledger)
        assert len(chain2._records) == 1
        assert chain2._records[0].title == "Persist Test"

    def test_load_empty_file(self, tmp_path):
        from aclip_cai.core.amendment import AmendmentChain
        ledger = str(tmp_path / "empty.jsonl")
        open(ledger, "w").close()
        chain = AmendmentChain(ledger_path=ledger)
        assert chain._records == []


# =============================================================================
# WITNESS RECORD
# =============================================================================


class TestWitnessRecord:
    def _make(self, h=0.9, a=1.0, e=0.8):
        from aclip_cai.core.vault_logger import WitnessRecord
        return WitnessRecord(
            session_id="sess-001",
            query="test query",
            response="test response",
            floor_audit={"F2": 0.99},
            verdict="SEAL",
            witness_human=h,
            witness_ai=a,
            witness_earth=e,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
        )

    def test_consensus_score(self):
        rec = self._make(h=0.9, a=1.0, e=0.8)
        assert abs(rec.consensus_score - (0.9 + 1.0 + 0.8) / 3.0) < 1e-9

    def test_consensus_passed_above_threshold(self):
        rec = self._make(h=0.95, a=1.0, e=0.95)
        assert rec.consensus_passed is True

    def test_consensus_failed_below_threshold(self):
        rec = self._make(h=0.5, a=1.0, e=0.5)
        assert rec.consensus_passed is False


# =============================================================================
# VAULT LOGGER
# =============================================================================


class TestVaultLogger:
    def test_log_decision_jsonl(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        rec = logger.log_decision(
            session_id="sess-001",
            query="What is 1+1?",
            response="2",
            floor_audit={"F2": 0.99, "F5": 1.0},
            verdict="SEAL",
            witness_human=0.9,
            witness_earth=0.8,
        )
        assert rec.verdict == "SEAL"
        assert rec.witness_ai == 1.0
        assert rec.seal_hash is not None
        assert len(rec.seal_hash) == 64

    def test_log_decision_truncates_long_query(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        long_query = "x" * 2000
        rec = logger.log_decision(
            session_id="s",
            query=long_query,
            response="r",
            floor_audit={},
            verdict="SEAL",
        )
        assert len(rec.query) <= 1024

    def test_log_decision_clamps_witness_scores(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        rec = logger.log_decision(
            session_id="s",
            query="q",
            response="r",
            floor_audit={},
            verdict="SEAL",
            witness_human=2.0,   # > 1.0 → clamped to 1.0
            witness_earth=-0.5,  # < 0.0 → clamped to 0.0
        )
        assert rec.witness_human == 1.0
        assert rec.witness_earth == 0.0

    def test_log_witness_compat(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        rec = logger.log_witness(
            session_id="sess-002",
            agent_id="MIND",
            stage="333_REASON",
            statement="Hypothesis tested",
            verdict="SEAL",
        )
        assert rec.session_id == "sess-002"
        assert rec.verdict == "SEAL"

    def test_get_session_records_finds_entry(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        logger.log_decision(
            session_id="target-session",
            query="q",
            response="r",
            floor_audit={},
            verdict="SEAL",
        )
        records = logger.get_session_records("target-session")
        assert len(records) == 1
        assert records[0]["session_id"] == "target-session"

    def test_get_session_records_filters_other_sessions(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        logger.log_decision("session-A", "q", "r", {}, "SEAL")
        logger.log_decision("session-B", "q", "r", {}, "VOID")
        records = logger.get_session_records("session-A")
        assert len(records) == 1

    def test_get_session_records_empty_when_no_match(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = str(tmp_path / "vault.jsonl")
        logger = VaultLogger(vault_path=path)
        records = logger.get_session_records("nonexistent")
        assert records == []

    def test_compute_seal_hash_deterministic(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger, WitnessRecord
        h1 = VaultLogger._compute_seal_hash(WitnessRecord(
            session_id="s", query="q", response="r", floor_audit={},
            verdict="SEAL", witness_human=1.0, witness_ai=1.0, witness_earth=1.0,
            timestamp="2026-01-01T00:00:00+00:00",
        ))
        h2 = VaultLogger._compute_seal_hash(WitnessRecord(
            session_id="s", query="q", response="r", floor_audit={},
            verdict="SEAL", witness_human=1.0, witness_ai=1.0, witness_earth=1.0,
            timestamp="2026-01-01T00:00:00+00:00",
        ))
        assert h1 == h2
        assert len(h1) == 64

    def test_jsonl_written_on_log(self, tmp_path):
        from aclip_cai.core.vault_logger import VaultLogger
        path = tmp_path / "vault.jsonl"
        logger = VaultLogger(vault_path=str(path))
        logger.log_decision("s", "q", "r", {}, "SEAL")
        lines = path.read_text().strip().splitlines()
        assert len(lines) == 1
        row = json.loads(lines[0])
        assert row["session_id"] == "s"
        assert row["verdict"] == "SEAL"
        assert "consensus_score" in row


# =============================================================================
# TRIAD DELTA/REASON — kernel fallback (no ctx)
# =============================================================================


class TestReasonKernelFallback:
    async def test_reason_no_ctx_returns_verdict(self):
        from aclip_cai.triad.delta.reason import reason
        result = await reason(
            session_id="test-reason-001",
            hypothesis="Water is wet",
            evidence=["H2O molecules interact with surfaces", "Tactile perception"],
            ctx=None,
            use_sampling=False,
        )
        assert "verdict" in result
        assert result["verdict"] in ("SEAL", "PARTIAL", "VOID", "SABAR", "888_HOLD")

    async def test_reason_returns_truth_score(self):
        from aclip_cai.triad.delta.reason import reason
        result = await reason(
            session_id="test-reason-002",
            hypothesis="Simple factual claim",
            evidence=["Evidence A"],
            ctx=None,
        )
        assert "truth_score" in result
        assert isinstance(result["truth_score"], float)


# =============================================================================
# TRIAD OMEGA/ALIGN — kernel fallback (no ctx)
# =============================================================================


class TestAlignKernelFallback:
    async def test_align_no_ctx_returns_verdict(self):
        from aclip_cai.triad.omega.align import align
        result = await align(
            session_id="test-align-001",
            action="Review a plan to improve documentation",
            ctx=None,
            use_sampling=False,
        )
        assert "verdict" in result
        assert result["verdict"] in ("SEAL", "PARTIAL", "VOID", "SABAR", "888_HOLD", "aligned")

    async def test_align_returns_status(self):
        from aclip_cai.triad.omega.align import align
        result = await align(
            session_id="test-align-002",
            action="Summarise meeting notes",
            ctx=None,
        )
        assert isinstance(result, dict)
