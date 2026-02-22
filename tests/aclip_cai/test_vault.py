"""
tests/aclip_cai/test_vault.py
================================

Unit tests for aclip_cai.core.vault_logger — Tri-Witness VAULT999.
"""

import os
import json
import tempfile
import pytest
from aclip_cai.core.vault_logger import VaultLogger, WitnessRecord


@pytest.fixture
def tmp_vault(tmp_path):
    """VaultLogger backed by a temporary JSONL file."""
    ledger = str(tmp_path / "vault.jsonl")
    return VaultLogger(jsonl_path=ledger), ledger


def test_seal_writes_record(tmp_vault):
    """seal() should write a record to the JSONL ledger."""
    logger, ledger_path = tmp_vault
    record = logger.seal(
        session_id="v-001",
        action="system health check",
        verdict="seal",
        agent_id="antigravity",
        witness_human=0.95,
        witness_ai=0.97,
        witness_earth=0.90,
    )
    assert os.path.exists(ledger_path)
    with open(ledger_path) as f:
        lines = [json.loads(l) for l in f if l.strip()]
    assert len(lines) == 1
    assert lines[0]["session_id"] == "v-001"


def test_seal_hash_computed(tmp_vault):
    """seal() should compute and attach a SHA-256 hash."""
    logger, _ = tmp_vault
    record = logger.seal(
        session_id="v-002",
        action="audit log review",
        verdict="seal",
        agent_id="antigravity",
        witness_human=0.99,
        witness_ai=0.98,
        witness_earth=0.95,
    )
    assert record.seal_hash is not None
    assert len(record.seal_hash) == 64  # SHA-256 hex


def test_consensus_score(tmp_vault):
    """W₃ = mean(H, A, E) — tri-witness consensus."""
    logger, _ = tmp_vault
    record = logger.seal(
        session_id="v-003",
        action="check floors",
        verdict="seal",
        agent_id="test",
        witness_human=0.80,
        witness_ai=0.90,
        witness_earth=0.70,
    )
    expected = (0.80 + 0.90 + 0.70) / 3
    assert record.consensus_score == pytest.approx(expected, abs=1e-6)


def test_consensus_below_threshold_is_noted(tmp_vault):
    """Records with low W₃ (< 0.95) should be flaggable."""
    logger, _ = tmp_vault
    record = logger.seal(
        session_id="v-004",
        action="risky op",
        verdict="hold",
        agent_id="test",
        witness_human=0.50,
        witness_ai=0.60,
        witness_earth=0.40,
    )
    assert record.consensus_score < 0.95


def test_multiple_records_appended(tmp_vault):
    """Multiple seal() calls should append lines, not overwrite."""
    logger, ledger_path = tmp_vault
    for i in range(3):
        logger.seal(
            session_id=f"v-{i:03d}",
            action="step",
            verdict="seal",
            agent_id="test",
            witness_human=0.95,
            witness_ai=0.95,
            witness_earth=0.95,
        )
    with open(ledger_path) as f:
        lines = [l for l in f if l.strip()]
    assert len(lines) == 3
