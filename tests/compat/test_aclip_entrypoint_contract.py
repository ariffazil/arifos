"""Compatibility tests for the deprecated `python -m arifosmcp.intelligence` transport alias."""

from __future__ import annotations

import sys
from typing import Any


def test_aclip_transport_alias_delegates_to_aaa_main(monkeypatch) -> None:
    import arifosmcp.intelligence.__main__ as cli

    called: dict[str, Any] = {}

    def _fake_main() -> None:
        called["argv"] = list(sys.argv)

    monkeypatch.setattr("arifosmcp.transport.__main__.main", _fake_main)
    monkeypatch.setattr(sys, "argv", ["arifosmcp.intelligence", "sse", "--port", "9090"])

    cli.main()

    assert called["argv"] == ["arifosmcp.transport", "sse", "--port", "9090"]


def test_aclip_help_alias_delegates_without_inventing_a_mode(monkeypatch) -> None:
    import arifosmcp.intelligence.__main__ as cli

    called: dict[str, Any] = {}

    def _fake_main() -> None:
        called["argv"] = list(sys.argv)

    monkeypatch.setattr("arifosmcp.transport.__main__.main", _fake_main)
    monkeypatch.setattr(sys, "argv", ["arifosmcp.intelligence", "--help"])

    cli.main()

    assert called["argv"] == ["arifosmcp.transport", "--help"]
