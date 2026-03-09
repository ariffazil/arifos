"""
tests/schema/test_validator.py — Verdict Contract Enforcement Tests

Validates VerdictValidator enforces the stage-verdict contract:
- Exploratory tools cannot emit VOID
- Safety/alignment tools cannot emit VOID
- Only commitment tools (and 000_INIT) may emit VOID
- Stage-level rule: stage < 888_JUDGE and verdict == VOID → SABAR
- Combined validate() applies both rules
"""

from __future__ import annotations

import pytest

from core.schema import Stage, Verdict, VerdictValidator


class TestVerdictValidatorByStage:
    """Stage-level verdict contract enforcement."""

    def test_mind_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.MIND, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_sense_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.SENSE, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_reality_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.REALITY, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_heart_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.HEART, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_critique_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.CRITIQUE, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_forge_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.FORGE, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_router_stage_void_normalized_to_sabar(self):
        result = VerdictValidator.validate_by_stage(Stage.ROUTER, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_judge_stage_void_allowed(self):
        """888_JUDGE is the first stage where real rejection is legal."""
        result = VerdictValidator.validate_by_stage(Stage.JUDGE, Verdict.VOID)
        assert result == Verdict.VOID

    def test_vault_stage_void_allowed(self):
        result = VerdictValidator.validate_by_stage(Stage.VAULT, Verdict.VOID)
        assert result == Verdict.VOID

    def test_init_stage_void_allowed(self):
        """000_INIT may emit VOID for auth failures."""
        result = VerdictValidator.validate_by_stage(Stage.INIT, Verdict.VOID)
        assert result == Verdict.VOID

    @pytest.mark.parametrize(
        "verdict", [Verdict.SEAL, Verdict.PROVISIONAL, Verdict.PARTIAL, Verdict.SABAR, Verdict.HOLD]
    )
    def test_non_void_verdicts_pass_through(self, verdict):
        """Non-VOID verdicts are never normalized."""
        for stage in (Stage.MIND, Stage.SENSE, Stage.HEART, Stage.CRITIQUE):
            result = VerdictValidator.validate_by_stage(stage, verdict)
            assert result == verdict


class TestVerdictValidatorByTool:
    """Tool-classification verdict contract enforcement."""

    # Exploratory tools
    @pytest.mark.parametrize(
        "tool",
        ["reason_mind", "vector_memory", "search_reality", "ingest_evidence", "anchor_session"],
    )
    def test_exploratory_tools_void_normalized(self, tool):
        result = VerdictValidator.validate_by_tool(tool, Verdict.VOID)
        assert result == Verdict.SABAR

    # Safety tools
    @pytest.mark.parametrize("tool", ["simulate_heart", "critique_thought", "audit_rules"])
    def test_safety_tools_void_normalized(self, tool):
        result = VerdictValidator.validate_by_tool(tool, Verdict.VOID)
        assert result == Verdict.SABAR

    # Commitment tools — VOID is legal here
    @pytest.mark.parametrize("tool", ["apex_judge", "eureka_forge", "seal_vault"])
    def test_commitment_tools_void_allowed(self, tool):
        result = VerdictValidator.validate_by_tool(tool, Verdict.VOID)
        assert result == Verdict.VOID

    def test_non_void_passes_through_all_tools(self):
        for tool in ("reason_mind", "apex_judge", "audit_rules", "seal_vault"):
            for verdict in (Verdict.SEAL, Verdict.SABAR, Verdict.HOLD, Verdict.PARTIAL):
                result = VerdictValidator.validate_by_tool(tool, verdict)
                assert result == verdict


class TestVerdictValidatorCombined:
    """Combined validate() applies both tool and stage rules."""

    def test_combined_exploratory_tool_mind_stage_void(self):
        result = VerdictValidator.validate("reason_mind", Stage.MIND, Verdict.VOID)
        assert result == Verdict.SABAR

    def test_combined_commitment_tool_judge_stage_void(self):
        result = VerdictValidator.validate("apex_judge", Stage.JUDGE, Verdict.VOID)
        assert result == Verdict.VOID

    def test_combined_commitment_tool_forge_stage_void(self):
        # Even commitment tools cannot bypass stage rule for pre-888 stages
        result = VerdictValidator.validate("apex_judge", Stage.FORGE, Verdict.VOID)
        # apex_judge passes tool check, but FORGE stage normalizes VOID → SABAR
        assert result == Verdict.SABAR


class TestIsValidForStage:
    """is_valid_for_stage returns (bool, message) without mutation."""

    def test_invalid_void_at_mind(self):
        valid, msg = VerdictValidator.is_valid_for_stage(Stage.MIND, Verdict.VOID)
        assert valid is False
        assert "333_MIND" in msg

    def test_valid_seal_at_any_stage(self):
        valid, msg = VerdictValidator.is_valid_for_stage(Stage.MIND, Verdict.SEAL)
        assert valid is True
        assert msg == ""

    def test_valid_void_at_judge(self):
        valid, msg = VerdictValidator.is_valid_for_stage(Stage.JUDGE, Verdict.VOID)
        assert valid is True
