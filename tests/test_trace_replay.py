from __future__ import annotations

import hashlib
import json

import pytest

from arifosmcp.runtime import bridge
from core.organs._4_vault import _CHAIN_SEED, compute_vault_seal_hash


def _build_vault_entry(
    *,
    session_id: str,
    summary: str,
    timestamp: str,
    verdict: str = "SEAL",
    telemetry: dict[str, object] | None = None,
) -> dict[str, object]:
    entry = {
        "session_id": session_id,
        "ledger_id": f"LGR-{session_id.upper()}",
        "summary": summary,
        "verdict": verdict,
        "approved_by": "system",
        "approval_reference": None,
        "telemetry": telemetry or {},
        "timestamp": timestamp,
    }
    seal_hash = compute_vault_seal_hash(entry)
    return {
        **entry,
        "seal_hash": seal_hash,
        "chain": {
            "payload_hash": seal_hash,
            "entry_hash": hashlib.sha256((seal_hash + _CHAIN_SEED).encode()).hexdigest(),
            "prev_entry_hash": "0x" + "0" * 64,
        },
    }


@pytest.mark.asyncio
async def test_trace_replay_reads_trace_from_vault_telemetry(tmp_path, monkeypatch):
    vault_path = tmp_path / "vault999.jsonl"
    monkeypatch.setattr(bridge, "DEFAULT_VAULT_PATH", vault_path)

    vault_path.write_text(
        "\n".join(
            [
                json.dumps(
                    _build_vault_entry(
                        session_id="s-1",
                        summary="test summary",
                        timestamp="2026-03-10T00:00:00Z",
                        telemetry={
                            "trace": {"111_MIND": "SEAL", "222_REALITY": {"score": 0.88}},
                            "reality": {"score": 0.88, "status": "OK"},
                        },
                    )
                ),
                json.dumps(
                    _build_vault_entry(
                        session_id="s-2",
                        summary="other session",
                        timestamp="2026-03-10T00:00:01Z",
                        telemetry={"trace": {"111_MIND": "PARTIAL"}},
                    )
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = await bridge.call_kernel("trace_replay", "s-1", {"limit": 5})

    assert result["status"] == "SUCCESS"
    assert result["payload"]["replay_status"] == "SUCCESS"
    assert result["payload"]["trace_count"] == 1
    assert result["payload"]["entries"][0]["trace"]["111_MIND"] == "SEAL"
    assert result["payload"]["entries"][0]["reality"]["score"] == 0.88


@pytest.mark.asyncio
async def test_trace_replay_returns_no_data_when_vault_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(bridge, "DEFAULT_VAULT_PATH", tmp_path / "missing.jsonl")

    result = await bridge.call_kernel("trace_replay", "s-404", {"limit": 5})

    assert result["status"] == "SUCCESS"
    assert result["payload"]["replay_status"] == "NO_DATA"
    assert result["payload"]["trace_count"] == 0


@pytest.mark.asyncio
async def test_trace_replay_blocks_tampered_vault_entries(tmp_path, monkeypatch):
    vault_path = tmp_path / "vault999.jsonl"
    monkeypatch.setattr(bridge, "DEFAULT_VAULT_PATH", vault_path)

    entry = {
        "session_id": "s-bad",
        "summary": "tampered entry",
        "timestamp": "2026-03-10T00:00:00Z",
        "telemetry": {"trace": {"111_MIND": "SEAL"}},
    }
    signed_entry = _build_vault_entry(**entry)
    good_hash = signed_entry["seal_hash"]
    tampered = {
        **signed_entry,
        "summary": "tampered entry after seal",
        "seal_hash": good_hash,
        "chain": {
            "payload_hash": good_hash,
            "entry_hash": "not-a-real-entry-hash",
            "prev_entry_hash": "0x" + "0" * 64,
        },
    }
    vault_path.write_text(json.dumps(tampered), encoding="utf-8")

    result = await bridge.call_kernel("trace_replay", "s-bad", {"limit": 5})

    assert result["ok"] is False
    assert result["status"] == "ERROR"
    assert result["payload"]["replay_status"] == "TAMPERED"
    assert result["payload"]["trace_count"] == 0
    assert result["errors"][0]["code"] == "TRACE_REPLAY_TAMPER"
