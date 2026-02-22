"""Import smoke tests for arifOS MCP package integrity."""

from __future__ import annotations


def test_import_aaa_mcp_package() -> None:
    import aaa_mcp

    assert aaa_mcp is not None
    assert hasattr(aaa_mcp, "mcp")


def test_import_canonical_tools_from_package() -> None:
    from aaa_mcp import (
        agi_cognition,
        analyze,
        apex_verdict,
        asi_empathy,
        fetch,
        init_session,
        search,
        system_audit,
        vault_seal,
    )

    assert callable(init_session.fn)
    assert callable(agi_cognition.fn)
    assert callable(asi_empathy.fn)
    assert callable(apex_verdict.fn)
    assert callable(vault_seal.fn)
    assert callable(search.fn)
    assert callable(fetch.fn)
    assert callable(analyze.fn)
    assert callable(system_audit.fn)
