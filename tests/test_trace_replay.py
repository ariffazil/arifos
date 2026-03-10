from __future__ import annotations

import json

import pytest

from arifosmcp import bridge


@pytest.mark.asyncio
async def test_trace_replay_reads_trace_from_vault_telemetry(tmp_path, monkeypatch):
    vault_path = tmp_path / "vault999.jsonl"
    monkeypatch.setattr(bridge, "DEFAULT_VAULT_PATH", vault_path)

    vault_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "session_id": "s-1",
                        "summary": "test summary",
                        "verdict": "SEAL",
                        "timestamp": "2026-03-10T00:00:00Z",
                        "seal_hash": "abc123",
                        "telemetry": {
                            "trace": {"111_MIND": "SEAL", "222_REALITY": {"score": 0.88}},
                            "reality": {"score": 0.88, "status": "OK"},
                        },
                    }
                ),
                json.dumps(
                    {
                        "session_id": "s-2",
                        "summary": "other session",
                        "verdict": "SEAL",
                        "timestamp": "2026-03-10T00:00:01Z",
                        "telemetry": {"trace": {"111_MIND": "PARTIAL"}},
                    }
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
