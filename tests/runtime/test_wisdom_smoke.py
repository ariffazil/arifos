"""
arifOS Wisdom System — Smoke Test Harness
Tests arifos_wisdom tool, arifos://wisdom resources, audit logging,
fallback behavior, and deterministic selection.
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import pytest

# Ensure project root is on path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from arifosmcp.runtime.wisdom_quotes import (
    pick_quote,
    pick_quote_with_meta,
    quotes_for_surface,
    registry_stats,
    SURFACES,
    WISDOM_REGISTRY,
)
from arifosmcp.runtime.philosophy import select_wisdom_quote
from arifosmcp.runtime.tools import arifos_wisdom, arifos_wisdom_stats


class TestWisdomRegistry:
    def test_registry_has_quotes(self):
        stats = registry_stats()
        assert stats["total"] > 40
        assert stats["active"] > 40

    def test_all_surfaces_have_coverage(self):
        stats = registry_stats()
        for surface in SURFACES:
            # Some surfaces may legitimately have 0 quotes (e.g., empty)
            if surface == "empty":
                continue
            assert stats["by_surface"].get(surface, 0) > 0, f"surface {surface} has no quotes"

    def test_verdict_quotes_exist(self):
        void_q = pick_quote("void", tone="severe", shadow_profile="shadow")
        assert void_q is not None
        hold_q = pick_quote("hold", tone="severe", shadow_profile="restraint")
        assert hold_q is not None
        partial_q = pick_quote("partial", tone="reflective", shadow_profile="paradox")
        assert partial_q is not None
        sabar_q = pick_quote("sabar", tone="calm", shadow_profile="humility")
        assert sabar_q is not None

    def test_pick_quote_meta_includes_reason(self):
        meta = pick_quote_with_meta("judge", tone="firm", verdict="SEAL")
        assert meta["quote"]["id"]
        assert meta["selection_reason"] in {
            "exact_match",
            "language_relaxed",
            "tone_relaxed",
            "shadow_relaxed",
            "safe_default",
        }
        assert isinstance(meta["display_priority"], int)
        assert "fallback_step" in meta

    def test_select_wisdom_quote_returns_metadata(self):
        result = select_wisdom_quote("judge", tone="firm", verdict="SEAL")
        assert result["quote_id"]
        assert "selection_reason" in result
        assert "display_priority" in result
        assert "fallback_step" in result

    def test_contrast_pairs_exist(self):
        pairs = [q for q in WISDOM_REGISTRY if q.get("contrast_pair")]
        assert len(pairs) >= 3

    def test_shadow_index(self):
        high_scar = [q for q in WISDOM_REGISTRY if q["scar_weight"] >= 2]
        high_shadow = [q for q in WISDOM_REGISTRY if q["shadow_weight"] >= 2]
        high_paradox = [q for q in WISDOM_REGISTRY if q["paradox_weight"] >= 2]
        assert len(high_scar) >= 2
        assert len(high_shadow) >= 3
        assert len(high_paradox) >= 3


class TestWisdomTool:
    @pytest.mark.asyncio
    async def test_arifos_wisdom_returns_ok(self):
        result = await arifos_wisdom(surface="judge", tone="firm", verdict="SEAL")
        assert result["ok"] is True
        assert result["tool"] == "arifos_wisdom"
        assert result["quote"]["quote_id"]
        assert result["quote"]["selection_reason"]

    @pytest.mark.asyncio
    async def test_arifos_wisdom_stats_returns_shadow_index(self):
        result = await arifos_wisdom_stats()
        assert result["ok"] is True
        assert result["tool"] == "arifos_wisdom_stats"
        assert "shadow_index" in result
        assert "contrast_pairs" in result


class TestWisdomAudit:
    def test_audit_file_written(self, tmp_path, monkeypatch):
        audit_file = tmp_path / "wisdom_audit.jsonl"
        monkeypatch.setattr(
            "arifosmcp.runtime.wisdom_quotes._WISDOM_AUDIT_PATH", audit_file
        )
        from arifosmcp.runtime.wisdom_quotes import pick_quote_with_meta
        pick_quote_with_meta("judge", tone="firm", verdict="SEAL", session_id="sess-test")
        assert audit_file.exists()
        lines = audit_file.read_text().strip().split("\n")
        assert len(lines) >= 1
        entry = json.loads(lines[-1])
        assert entry["surface"] == "judge"
        assert entry["verdict"] == "SEAL"
        assert entry["session_id"] == "sess-test"


class TestWisdomDeterminism:
    def test_same_call_same_quote(self):
        q1 = pick_quote("judge", tone="firm", verdict="SEAL")
        q2 = pick_quote("judge", tone="firm", verdict="SEAL")
        assert q1["id"] == q2["id"]

    def test_different_verdict_different_quote(self):
        q_seal = pick_quote("judge", tone="firm", verdict="SEAL")
        q_void = pick_quote("void", tone="severe", verdict="VOID")
        assert q_seal["id"] != q_void["id"]
