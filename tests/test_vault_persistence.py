import json
import threading
from pathlib import Path

import pytest

from aaa_mcp.session_ledger import SessionLedger


def _dummy_payload(idx: int):
    return {
        "session_id": f"sess-{idx}",
        "verdict": "SEAL" if idx % 2 == 0 else "VOID",
        "init": {"k": idx},
        "agi": {"x": idx},
        "asi": {"y": idx},
        "judge": {"verdict": "SEAL"},
        "telemetry": {"p_truth": 0.9},
    }


def test_append_three_and_verify(tmp_path):
    ledger = SessionLedger(base_path=tmp_path)
    for i in range(3):
        p = _dummy_payload(i)
        ledger.seal_session(
            session_id=p["session_id"],
            verdict=p["verdict"],
            init_result=p["init"],
            genius_result=p["agi"],
            act_result=p["asi"],
            judge_result=p["judge"],
            telemetry=p["telemetry"],
            key_insights=["k"],
            authority="test",
        )

    ok, root = ledger.verify_chain()
    assert ok
    assert root


def test_restart_and_verify_chain(tmp_path):
    ledger = SessionLedger(base_path=tmp_path)
    for i in range(2):
        p = _dummy_payload(i)
        ledger.seal_session(
            session_id=p["session_id"],
            verdict=p["verdict"],
            init_result=p["init"],
            genius_result=p["agi"],
            act_result=p["asi"],
            judge_result=p["judge"],
            telemetry=p["telemetry"],
            authority="test",
        )

    # Simulate restart by creating a new instance
    fresh = SessionLedger(base_path=tmp_path)
    ok, _ = fresh.verify_chain()
    assert ok


def test_tamper_detection(tmp_path):
    ledger = SessionLedger(base_path=tmp_path)
    p = _dummy_payload(1)
    ledger.seal_session(
        session_id=p["session_id"],
        verdict=p["verdict"],
        init_result=p["init"],
        genius_result=p["agi"],
        act_result=p["asi"],
        judge_result=p["judge"],
        telemetry=p["telemetry"],
        authority="test",
    )

    # Tamper: modify verdict in stored JSON
    stored = next(tmp_path.joinpath("sessions").glob("*.json"))
    data = json.loads(stored.read_text())
    data["verdict"] = "SEAL"  # flip verdict
    stored.write_text(json.dumps(data, indent=2))

    ok, reason = ledger.verify_chain()
    assert not ok
    assert "hash-mismatch" in reason


def test_concurrent_seals_ordered(tmp_path):
    ledger = SessionLedger(base_path=tmp_path)

    def do_seal(idx):
        p = _dummy_payload(idx)
        ledger.seal_session(
            session_id=p["session_id"],
            verdict=p["verdict"],
            init_result=p["init"],
            genius_result=p["agi"],
            act_result=p["asi"],
            judge_result=p["judge"],
            telemetry=p["telemetry"],
            authority="test",
        )

    t1 = threading.Thread(target=do_seal, args=(1,))
    t2 = threading.Thread(target=do_seal, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    ok, _ = ledger.verify_chain()
    assert ok

    entries = ledger._walk_chain()
    sequences = [e.sequence for e in entries]
    assert sequences == sorted(sequences)
    assert sequences[0] == 1
