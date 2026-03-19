"""Compatibility tests for the deprecated `python -m aclip_cai` transport alias."""

from __future__ import annotations

import sys
from typing import Any


def test_aclip_transport_alias_delegates_to_aaa_main(monkeypatch) -> None:
    import aclip_cai.__main__ as cli

    called: dict[str, Any] = {}

    def _fake_main() -> None:
        called["argv"] = list(sys.argv)

    monkeypatch.setattr("aaa_mcp.__main__.main", _fake_main)
    monkeypatch.setattr(sys, "argv", ["aclip_cai", "sse", "--port", "9090"])

    cli.main()

    assert called["argv"] == ["aaa_mcp", "sse", "--port", "9090"]


def test_aclip_help_alias_delegates_without_inventing_a_mode(monkeypatch) -> None:
    import aclip_cai.__main__ as cli

    called: dict[str, Any] = {}

    def _fake_main() -> None:
        called["argv"] = list(sys.argv)

    monkeypatch.setattr("aaa_mcp.__main__.main", _fake_main)
    monkeypatch.setattr(sys, "argv", ["aclip_cai", "--help"])

    cli.main()

    assert called["argv"] == ["aaa_mcp", "--help"]
