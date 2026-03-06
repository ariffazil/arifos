"""
Integration tests for 13-tool MCP compliance.

Validates:
- Exactly 13 public tools in AAA_CANONICAL_TOOLS
- No deprecated/archived tools exposed in the canonical surface
- CANONICAL_TOOL_COUNT == 13
- ingest_evidence is present and callable
- metabolic_loop is present in canonical surface
- fetch_content and inspect_file are NOT in canonical surface
"""

from __future__ import annotations

from aaa_mcp.protocol.aaa_contract import (
    AAA_CANONICAL_TOOLS,
    ARCHIVED_TOOLS,
    CANONICAL_TOOL_COUNT,
    L4_TOOLS,
    READ_ONLY_TOOLS,
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Tool Count
# ─────────────────────────────────────────────────────────────────────────────

class TestToolCount:
    """Verify CANONICAL_TOOL_COUNT is exactly 13."""

    def test_canonical_count_constant_is_13(self):
        assert CANONICAL_TOOL_COUNT == 13

    def test_aaa_canonical_tools_length_is_13(self):
        assert len(AAA_CANONICAL_TOOLS) == CANONICAL_TOOL_COUNT

    def test_l4_tools_frozenset_length_is_13(self):
        assert len(L4_TOOLS) == 13


# ─────────────────────────────────────────────────────────────────────────────
# 2. Exact Tool Names
# ─────────────────────────────────────────────────────────────────────────────

EXPECTED_13_TOOLS = {
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "eureka_forge",
    "apex_judge",
    "seal_vault",
    "search_reality",
    "ingest_evidence",
    "audit_rules",
    "check_vital",
    "metabolic_loop",
}


class TestExactToolNames:
    """Verify the exact 13 tool names are present — no more, no less."""

    def test_canonical_tools_matches_expected_set(self):
        assert set(AAA_CANONICAL_TOOLS) == EXPECTED_13_TOOLS

    def test_ingest_evidence_is_present(self):
        assert "ingest_evidence" in L4_TOOLS

    def test_metabolic_loop_is_present(self):
        assert "metabolic_loop" in L4_TOOLS

    def test_no_ghost_fetch_content(self):
        assert "fetch_content" not in L4_TOOLS, (
            "fetch_content must not appear in canonical surface — it is archived"
        )

    def test_no_ghost_inspect_file(self):
        assert "inspect_file" not in L4_TOOLS, (
            "inspect_file must not appear in canonical surface — it is archived"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 3. Archived Tools Isolation
# ─────────────────────────────────────────────────────────────────────────────

class TestArchivedToolsIsolation:
    """Verify archived tools are tracked but not exposed."""

    def test_archived_tools_set_exists(self):
        assert isinstance(ARCHIVED_TOOLS, frozenset)

    def test_fetch_content_is_archived(self):
        assert "fetch_content" in ARCHIVED_TOOLS

    def test_inspect_file_is_archived(self):
        assert "inspect_file" in ARCHIVED_TOOLS

    def test_archived_tools_disjoint_from_canonical(self):
        overlap = ARCHIVED_TOOLS & L4_TOOLS
        assert not overlap, (
            f"Archived tools must not appear in canonical surface: {overlap}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 4. Read-Only Tool Classification
# ─────────────────────────────────────────────────────────────────────────────

class TestReadOnlyTools:
    def test_ingest_evidence_is_read_only(self):
        assert "ingest_evidence" in READ_ONLY_TOOLS

    def test_fetch_content_not_in_read_only(self):
        assert "fetch_content" not in READ_ONLY_TOOLS

    def test_inspect_file_not_in_read_only(self):
        assert "inspect_file" not in READ_ONLY_TOOLS

    def test_read_only_tools_subset_of_canonical(self):
        assert READ_ONLY_TOOLS.issubset(L4_TOOLS), (
            f"All READ_ONLY_TOOLS must be in L4_TOOLS. Extras: {READ_ONLY_TOOLS - L4_TOOLS}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 5. Allowlist Parity
# ─────────────────────────────────────────────────────────────────────────────

class TestAllowlistParity:
    """Verify 333_APPS allowlist matches canonical 13."""

    def test_l5_agent_allowlist_matches_canonical(self):
        from importlib import import_module

        mod = import_module("333_APPS.L5_AGENTS.POWER.io.tools")
        allowed: frozenset[str] = getattr(mod, "_ALLOWED_TOOLS")
        assert allowed == EXPECTED_13_TOOLS, (
            f"Allowlist mismatch.\n  Extra: {allowed - EXPECTED_13_TOOLS}\n  Missing: {EXPECTED_13_TOOLS - allowed}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 6. ingest_evidence callable smoke test
# ─────────────────────────────────────────────────────────────────────────────

class TestIngestEvidenceCallable:
    """Verify ingest_evidence can be imported and called."""

    async def test_ingest_evidence_bad_source_type(self):
        from aaa_mcp.tools.ingest_evidence import ingest_evidence

        result = await ingest_evidence(source_type="ftp", target="ftp://test")
        assert result["status"] == "BAD_SOURCE_TYPE"

    async def test_ingest_evidence_url_bad_target(self):
        from aaa_mcp.tools.ingest_evidence import ingest_evidence

        result = await ingest_evidence(source_type="url", target="not-a-url")
        assert result["status"] == "BAD_TARGET"

    async def test_ingest_evidence_file_mode_nonexistent(self):
        from aaa_mcp.tools.ingest_evidence import ingest_evidence

        result = await ingest_evidence(
            source_type="file", target="/nonexistent_path_arifos_test"
        )
        # Should return an error envelope, not raise
        assert "status" in result
