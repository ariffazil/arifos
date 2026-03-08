from __future__ import annotations

from aaa_mcp.build_info import get_build_info


def test_build_info_prefers_environment(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_VERSION", "2026.02.28")
    monkeypatch.setenv("GIT_SHA", "abc12345")
    monkeypatch.setenv("BUILD_TIME", "2026-02-28T06:02:00+00:00")

    info = get_build_info()

    assert info["version"] == "2026.02.28"
    assert info["schema_version"] == "2026.02.28"
    assert info["git_sha"] == "abc12345"
    assert info["build_time"] == "2026-02-28T06:02:00+00:00"


def test_build_info_falls_back_to_installed_package(monkeypatch) -> None:
    monkeypatch.delenv("ARIFOS_VERSION", raising=False)
    monkeypatch.delenv("GIT_SHA", raising=False)
    monkeypatch.delenv("BUILD_TIME", raising=False)

    info = get_build_info()

    assert info["version"] != "unknown"
    assert info["schema_version"] == info["version"]
