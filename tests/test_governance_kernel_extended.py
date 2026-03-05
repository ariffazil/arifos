"""
Extended GovernanceKernel tests.

Covers: AuthorityLevel, GovernanceState, GovernanceKernel (all methods),
        get_governance_kernel, clear_governance_kernel.
"""
from __future__ import annotations

import pytest


# =============================================================================
# ENUMS
# =============================================================================


class TestAuthorityLevel:
    def test_values_exist(self):
        from core.governance_kernel import AuthorityLevel
        assert AuthorityLevel.ANALYSIS.value == "analysis"
        assert AuthorityLevel.SUGGESTION.value == "suggestion"
        assert AuthorityLevel.REQUIRES_HUMAN.value == "requires_human"
        assert AuthorityLevel.UNSAFE_TO_AUTOMATE.value == "unsafe"


class TestGovernanceStateEnum:
    def test_values_exist(self):
        from core.governance_kernel import GovernanceState
        assert GovernanceState.ACTIVE.value == "active"
        assert GovernanceState.AWAITING_888.value == "awaiting_888"
        assert GovernanceState.CONDITIONAL.value == "conditional"
        assert GovernanceState.VOID.value == "void"


# =============================================================================
# GOVERNANCE KERNEL INIT & DEFAULTS
# =============================================================================


class TestGovernanceKernelDefaults:
    def setup_method(self):
        from core.governance_kernel import GovernanceKernel
        self.kernel = GovernanceKernel(session_id="test-session")

    def test_default_authority_level(self):
        from core.governance_kernel import AuthorityLevel
        assert self.kernel.authority_level == AuthorityLevel.ANALYSIS

    def test_default_governance_state(self):
        from core.governance_kernel import GovernanceState
        assert self.kernel.governance_state == GovernanceState.ACTIVE

    def test_default_can_proceed(self):
        assert self.kernel.can_proceed() is True

    def test_default_escalation_not_required(self):
        assert self.kernel.escalation_required is False

    def test_default_human_approval_not_required(self):
        assert self.kernel.human_approval_status == "not_required"

    def test_session_id_stored(self):
        assert self.kernel.session_id == "test-session"


# =============================================================================
# UPDATE UNCERTAINTY → GOVERNANCE STATE TRANSITIONS
# =============================================================================


class TestUpdateUncertainty:
    def setup_method(self):
        from core.governance_kernel import GovernanceKernel
        self.kernel = GovernanceKernel()

    def test_low_uncertainty_stays_active(self):
        from core.governance_kernel import GovernanceState
        self.kernel.update_uncertainty(0.02, 0.02, {"grounding": 0.02})
        assert self.kernel.governance_state == GovernanceState.ACTIVE

    def test_medium_uncertainty_becomes_conditional(self):
        from core.governance_kernel import GovernanceState
        self.kernel.update_uncertainty(0.04, 0.04, {"grounding": 0.04})
        assert self.kernel.governance_state == GovernanceState.CONDITIONAL

    def test_high_uncertainty_triggers_888(self):
        from core.governance_kernel import GovernanceState
        self.kernel.update_uncertainty(0.07, 0.07, {"grounding": 0.07})
        assert self.kernel.governance_state == GovernanceState.AWAITING_888
        assert self.kernel.escalation_required is True
        assert self.kernel.human_approval_status == "pending"

    def test_uncertainty_components_stored(self):
        components = {"grounding": 0.03, "reasoning": 0.02}
        self.kernel.update_uncertainty(0.03, 0.03, components)
        assert self.kernel.uncertainty_components == components


# =============================================================================
# UPDATE IRREVERSIBILITY
# =============================================================================


class TestUpdateIrreversibility:
    def setup_method(self):
        from core.governance_kernel import GovernanceKernel
        self.kernel = GovernanceKernel()

    def test_low_irreversibility_stays_active(self):
        from core.governance_kernel import GovernanceState
        self.kernel.update_irreversibility(0.1, 0.1, 0.1)
        assert self.kernel.governance_state == GovernanceState.ACTIVE

    def test_high_irreversibility_triggers_888(self):
        from core.governance_kernel import GovernanceState
        # 0.9 × 0.9 × 0.9 = 0.729 > 0.6
        self.kernel.update_irreversibility(0.9, 0.9, 0.9)
        assert self.kernel.governance_state == GovernanceState.AWAITING_888

    def test_irreversibility_index_calculated(self):
        self.kernel.update_irreversibility(0.5, 0.4, 0.3)
        expected = 0.5 * 0.4 * 0.3
        assert abs(self.kernel.irreversibility_index - expected) < 0.001

    def test_reversibility_score_complement(self):
        self.kernel.update_irreversibility(0.5, 0.5, 0.4)
        # reversibility_score = 1 - irreversibility_index
        assert abs(self.kernel.reversibility_score - (1.0 - self.kernel.irreversibility_index)) < 0.001


# =============================================================================
# APPROVE HUMAN
# =============================================================================


class TestApproveHuman:
    def setup_method(self):
        from core.governance_kernel import GovernanceKernel
        self.kernel = GovernanceKernel()
        self.kernel.update_uncertainty(0.07, 0.07, {})  # trigger AWAITING_888

    def test_approve_true_becomes_conditional(self):
        from core.governance_kernel import GovernanceState
        self.kernel.approve_human(True, actor="888_sovereign")
        assert self.kernel.governance_state == GovernanceState.CONDITIONAL
        assert self.kernel.escalation_required is False
        assert self.kernel.human_approval_status == "approved"
        assert self.kernel.decision_owner == "888_sovereign"

    def test_approve_false_becomes_void(self):
        from core.governance_kernel import GovernanceState
        self.kernel.approve_human(False)
        assert self.kernel.governance_state == GovernanceState.VOID
        assert self.kernel.human_approval_status == "denied"
        assert self.kernel.decision_owner == "system"

    def test_approve_sets_timestamp(self):
        self.kernel.approve_human(True)
        assert self.kernel.human_override_timestamp is not None


# =============================================================================
# CAN PROCEED
# =============================================================================


class TestCanProceed:
    def test_active_can_proceed(self):
        from core.governance_kernel import GovernanceKernel, GovernanceState
        kernel = GovernanceKernel()
        assert kernel.can_proceed() is True

    def test_conditional_can_proceed(self):
        from core.governance_kernel import GovernanceKernel, GovernanceState
        kernel = GovernanceKernel()
        kernel.update_uncertainty(0.04, 0.04, {})  # → CONDITIONAL
        assert kernel.can_proceed() is True

    def test_awaiting_888_cannot_proceed(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        kernel.update_uncertainty(0.07, 0.07, {})  # → AWAITING_888
        assert kernel.can_proceed() is False

    def test_void_cannot_proceed(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        kernel.approve_human(False)
        assert kernel.can_proceed() is False


# =============================================================================
# OUTPUT TAGS
# =============================================================================


class TestGetOutputTags:
    def test_analysis_tag(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        tags = kernel.get_output_tags()
        assert "[ANALYSIS]" in tags

    def test_suggestion_tag(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        kernel.update_uncertainty(0.04, 0.04, {})
        tags = kernel.get_output_tags()
        assert "[SUGGESTION]" in tags

    def test_requires_human_tag(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        kernel.update_uncertainty(0.07, 0.07, {})
        tags = kernel.get_output_tags()
        assert "[REQUIRES_HUMAN_JUDGMENT]" in tags
        assert "[PENDING_888_APPROVAL]" in tags

    def test_unsafe_tag(self):
        from core.governance_kernel import GovernanceKernel, AuthorityLevel
        kernel = GovernanceKernel()
        kernel.authority_level = AuthorityLevel.UNSAFE_TO_AUTOMATE
        tags = kernel.get_output_tags()
        assert "[UNSAFE_TO_AUTOMATE]" in tags


# =============================================================================
# TO_DICT
# =============================================================================


class TestToDict:
    def test_to_dict_has_all_keys(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel(session_id="dict-test")
        d = kernel.to_dict()
        for key in ("authority_level", "decision_owner", "safety_omega",
                    "governance_state", "can_proceed", "output_tags",
                    "session_id", "timestamp"):
            assert key in d

    def test_to_dict_can_proceed_reflected(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        kernel.update_uncertainty(0.07, 0.07, {})
        d = kernel.to_dict()
        assert d["can_proceed"] is False

    def test_to_dict_thresholds_present(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        d = kernel.to_dict()
        assert "thresholds" in d
        assert "irreversibility" in d["thresholds"]


# =============================================================================
# REGISTRY FUNCTIONS
# =============================================================================


class TestGovernanceRegistry:
    def test_get_creates_new_kernel(self):
        from core.governance_kernel import get_governance_kernel, clear_governance_kernel
        sid = "registry-test-session"
        clear_governance_kernel(sid)
        kernel = get_governance_kernel(sid)
        assert kernel is not None
        assert kernel.session_id == sid
        clear_governance_kernel(sid)

    def test_get_returns_same_kernel(self):
        from core.governance_kernel import get_governance_kernel, clear_governance_kernel
        sid = "same-kernel-session"
        clear_governance_kernel(sid)
        k1 = get_governance_kernel(sid)
        k2 = get_governance_kernel(sid)
        assert k1 is k2
        clear_governance_kernel(sid)

    def test_clear_removes_kernel(self):
        from core.governance_kernel import get_governance_kernel, clear_governance_kernel, _governance_kernels
        sid = "clear-test"
        get_governance_kernel(sid)
        assert sid in _governance_kernels
        clear_governance_kernel(sid)
        assert sid not in _governance_kernels

    def test_clear_nonexistent_is_safe(self):
        from core.governance_kernel import clear_governance_kernel
        # Should not raise
        clear_governance_kernel("nonexistent-session-xyz")


# =============================================================================
# THERMODYNAMIC CHECK
# =============================================================================


class TestThermodynamicConstraints:
    def test_check_returns_or_none(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        # Either returns ThermodynamicState or None (if THERMODYNAMICS_AVAILABLE=False)
        result = kernel.check_thermodynamic_constraints()
        # Just verify it doesn't raise and returns something useful
        assert result is None or hasattr(result, "verdict")

    def test_no_entropy_manager_returns_none(self):
        from core.governance_kernel import GovernanceKernel
        kernel = GovernanceKernel()
        kernel.entropy_manager = None
        result = kernel.check_thermodynamic_constraints()
        assert result is None
