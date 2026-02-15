from __future__ import annotations

import os
from pathlib import Path

from aclip_cai.console_tools import config_flags, net_status


async def test_net_status_check_ports_alias() -> None:
    result = await net_status(
        check_ports=True,
        check_connections=False,
        check_interfaces=False,
        check_routing=False,
    )

    assert result.status == "ok"
    assert "summary" in result.data
    assert "ports_count" in result.data["summary"]


async def test_net_status_check_connections_path() -> None:
    result = await net_status(
        check_ports=False,
        check_connections=True,
        check_interfaces=False,
        check_routing=False,
    )

    assert result.status == "ok"
    assert "summary" in result.data
    assert "connections_count" in result.data["summary"]


async def test_config_flags_unsupported_file_type_no_raw(tmp_path: Path) -> None:
    cfg = tmp_path / "sample.conf"
    cfg.write_text("SECRET_TOKEN=abc123\n", encoding="utf-8")

    result = await config_flags(config_path=str(cfg), env_prefix=None, include_secrets=False)

    assert result.status == "ok"
    file_data = result.data["files"][str(cfg)]
    assert "raw" not in file_data
    assert file_data.get("note") == "unsupported file type"


async def test_config_flags_mode_and_feature_flags(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_MODE", "LAB")
    monkeypatch.setenv("ARIFOS_FEATURE_ALPHA", "enabled")
    monkeypatch.setenv("ARIFOS_API_SECRET", "hidden")

    result = await config_flags(env_prefix="ARIFOS", include_secrets=False)

    assert result.status == "ok"
    assert result.data["governance"]["mode"] == "LAB"
    assert result.data["governance"]["feature_flags"]["ARIFOS_FEATURE_ALPHA"] == "enabled"
    assert result.data["environment"]["ARIFOS_API_SECRET"] == "***masked***"
