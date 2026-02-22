"""
tests/aclip_cai/test_vault.py
================================

Unit tests for aclip_cai.core.vault_logger — Tri-Witness VAULT999.
"""

import json
import os
import pytest
from aclip_cai.core.vault_logger import VaultLogger, WitnessRecord


@pytest.fixture
def tmp_vault(tmp_path):
    """VaultLogger backed by a temporary JSONL file."""
    ledger = str(tmp_path / "vault.jsonl")
    return VaultLogger(vault_path=ledger), ledger


def test_log_decision_writes_record(tmp_vault):
    """log_decision() should write a record to the JSONL ledger."""
    logger, ledger_path = tmp_vault
    record = logger.log_decision(
        session_id="v-001",
        query="system health check",
        response="CPU: 20% RAM: 45%",
        floor_audit={"F2": 0.99, "F12": 1.0},
        verdict="seal",
        witness_human=0.95,
        witness_earth=0.90,
    )
    assert os.path.exists(ledger_path)
    with open(ledger_path) as f:
        lines = [json.loads(l) for l in f if l.strip()]
    assert len(lines) == 1
    assert lines[0]["session_id"] == "v-001"


def test_seal_hash_computed(tmp_vault):
    """log_decision() should compute and attach a SHA-256 hash."""
    logger, _ = tmp_vault
    record = logger.log_decision(
        session_id="v-002",
        query="audit log review",
        response="log entries OK",
        floor_audit={"F1": 1.0},
        verdict="seal",
        witness_human=0.99,
        witness_earth=0.95,
    )
    assert record.seal_hash is not None
    assert len(record.seal_hash) == 64  # SHA-256 hex


def test_consensus_score(tmp_vault):
    """W₃ = mean(H, A, E) — tri-witness consensus."""
    logger, _ = tmp_vault
    record = logger.log_decision(
        session_id="v-003",
        query="check floors",
        response="all pass",
        floor_audit={},
        verdict="seal",
        witness_human=0.80,
        witness_earth=0.70,
    )
    # AI witness is always 1.0
    expected = (0.80 + 1.0 + 0.70) / 3
    assert record.consensus_score == pytest.approx(expected, abs=1e-6)


def test_consensus_below_threshold_is_detectable(tmp_vault):
    """Records with low W₃ (< 0.95) should be identifiable."""
    logger, _ = tmp_vault
    record = logger.log_decision(
        session_id="v-004",
        query="risky op",
        response="held",
        floor_audit={},
        verdict="hold",
        witness_human=0.50,
        witness_earth=0.40,
    )
    assert record.consensus_score < 0.95
    assert not record.consensus_passed


def test_multiple_records_appended(tmp_vault):
    """Multiple log_decision() calls should append lines, not overwrite."""
    logger, ledger_path = tmp_vault
    for i in range(3):
        logger.log_decision(
            session_id=f"v-{i:03d}",
            query="step",
            response="ok",
            floor_audit={},
            verdict="seal",
            witness_human=0.95,
            witness_earth=0.95,
        )
    with open(ledger_path) as f:
        lines = [l for l in f if l.strip()]
    assert len(lines) == 3
