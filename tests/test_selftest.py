from __future__ import annotations

from aaa_mcp.selftest import check_environment, check_floors


def test_selftest_environment_defaults_without_warnings(monkeypatch) -> None:
    for key in ("HOST", "PORT", "GOVERNANCE_MODE", "VAULT_PATH"):
        monkeypatch.delenv(key, raising=False)

    passed, issues = check_environment()

    assert passed is True
    assert issues == []


def test_selftest_floors_use_canonical_bindings() -> None:
    passed, issues = check_floors()

    assert passed is True
    assert issues == []
