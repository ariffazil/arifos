from pathlib import Path
import py_compile


SERVER_PATH = Path("aaa_mcp/server.py")


def _server_text() -> str:
    return SERVER_PATH.read_text(encoding="utf-8")


def test_server_import_smoke_via_compile():
    py_compile.compile(str(SERVER_PATH), doraise=True)


def test_apex_verdict_has_calibration_path():
    text = _server_text()
    assert 'if mode != "judge":' in text
    assert 'calib = await engine.calibrate(window=window)' in text
    assert 'store_stage_result(session_id, "apex_calibrate", calib)' in text


def test_apex_verdict_has_structured_fallback_fields():
    text = _server_text()
    assert 'except Exception as e:' in text
    assert '"verdict": ConflictStatus.SABAR.value' in text
    assert '"truth_score": 0.0' in text
    assert '"engine_mode": "fallback_apex_verdict"' in text
