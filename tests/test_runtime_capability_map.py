from __future__ import annotations

from arifosmcp.runtime.capability_map import build_runtime_capability_map


def test_capability_map_reports_file_backed_governance_secret(monkeypatch, tmp_path):
    secret_file = tmp_path / "governance.secret"
    secret_file.write_text("file-backed-secret", encoding="utf-8")

    monkeypatch.delenv("ARIFOS_GOVERNANCE_OPEN_MODE", raising=False)
    monkeypatch.delenv("ARIFOS_GOVERNANCE_SECRET", raising=False)
    monkeypatch.delenv("ARIFOS_GOVERNANCE_TOKEN_SECRET", raising=False)
    monkeypatch.setenv("ARIFOS_GOVERNANCE_SECRET_FILE", str(secret_file))

    capability_map = build_runtime_capability_map()

    assert capability_map["server_identity"]["continuity_signing"] == "configured"
    assert capability_map["capabilities"]["governed_continuity"] == "enabled"
