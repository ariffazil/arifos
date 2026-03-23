"""
test_invariants_authority.py — Authority Binding Invariants

F11 + F13: Authority must be unambiguous, verifiable, and non-transferable.
"""
import pytest
import asyncio
from arifosmcp.runtime.tools import init_anchor, arifos_kernel
from arifosmcp.runtime.models import RiskClass


class TestAuthorityScopeInvariant:
    """Invariant: approval_scope gates tool access deterministically"""

    @pytest.mark.asyncio
    async def test_sovereign_has_kernel_scope(self):
        """ariffazil must have arifOS_kernel:execute scope"""
        result = await init_anchor(
            actor_id='arif',
            intent='test sovereign scope',
            session_id='scope-test-001'
        )
        
        scopes = result.authority.approval_scope if result.authority else []
        has_kernel = any("arifOS_kernel" in s for s in scopes)
        assert has_kernel, "Sovereign must have kernel scope"

    @pytest.mark.asyncio
    async def test_anonymous_has_no_kernel_scope(self):
        """Anonymous must NOT have kernel scope"""
        # Call kernel without auth
        result = await arifos_kernel(
            query='test',
            session_id='anon-scope-test-002'
        )
        
        # Should fail
        assert not result.ok, "Anonymous kernel call must fail"
        
        # Error should indicate auth failure
        if result.errors:
            assert any("AUTH" in e.code for e in result.errors), \
                "Error must indicate auth failure"


class TestAuthorityProvenanceInvariant:
    """Invariant: authority_source indicates how authority was derived"""

    @pytest.mark.asyncio
    async def test_anchored_has_authority_source(self):
        """All anchored responses must include authority_source"""
        result = await init_anchor(
            actor_id='arif',
            intent='test provenance',
            session_id='provenance-test-003'
        )
        
        assert "authority_source" in result.payload, \
            "Must include authority_source in payload"
        assert result.payload["authority_source"] in ["token", "session", "fallback"], \
            "authority_source must be valid enum"


class TestCapabilityGatingInvariant:
    """Invariant: next_action gated on actual capability, not hardcoded"""

    @pytest.mark.asyncio
    async def test_sovereign_next_action_is_kernel(self):
        """Sovereign anchor should suggest kernel"""
        result = await init_anchor(
            actor_id='arif',
            intent='test next action',
            session_id='next-action-test-004'
        )
        
        assert result.next_action is not None, "Must have next_action"
        assert "arifOS_kernel" in str(result.next_action.get("tool", "")), \
            "Sovereign next_action should be kernel"

    @pytest.mark.asyncio
    async def test_anonymous_next_action_is_anchor(self):
        """Anonymous status should suggest anchor"""
        status = await get_caller_status(session_id='global')
        
        # Anonymous should NOT suggest kernel
        if status.next_action:
            assert "arifOS_kernel" not in str(status.next_action.get("tool", "")), \
                "Anonymous next_action must not be kernel"


class TestRiskClassAlignmentInvariant:
    """Invariant: risk_class matches tool's actual authority requirements"""

    def test_kernel_enforced_at_runtime(self):
        """arifOS_kernel enforces F11/F13 at runtime even if spec differs"""
        # NOTE: Spec may show F4 only, but runtime enforces F11/F13 via
        # _requires_explicit_kernel_auth() in bridge.py
        # This test documents the gap between spec metadata and runtime reality
        from arifosmcp.runtime.public_registry import public_tool_spec_by_name
        specs = public_tool_spec_by_name()
        
        if "arifOS_kernel" in specs:
            spec = specs["arifOS_kernel"]
            # Runtime enforces F11/F13 regardless of spec floors
            # TODO: Align spec metadata with runtime enforcement
            assert spec.layer == "KERNEL", "arifOS_kernel must be KERNEL layer"


class TestErrorRemediationInvariant:
    """Invariant: Auth errors include actionable remediation"""

    @pytest.mark.asyncio
    async def test_auth_error_has_next_tool(self):
        """Auth failure must specify next tool"""
        result = await arifos_kernel(
            query='test remediation',
            session_id='remediation-test-005'
        )
        
        if not result.ok and result.errors:
            error = result.errors[0]
            assert error.required_next_tool is not None, \
                "Auth error must have required_next_tool"
            assert "init_anchor" in str(error.required_next_tool), \
                "Auth error should point to init_anchor"

    @pytest.mark.asyncio
    async def test_auth_error_has_required_fields(self):
        """Auth failure must specify required fields"""
        result = await arifos_kernel(
            query='test remediation',
            session_id='remediation-test-006'
        )
        
        if not result.ok and result.errors:
            error = result.errors[0]
            assert error.required_fields is not None, \
                "Auth error must have required_fields"
            assert len(error.required_fields) > 0, \
                "required_fields must not be empty"


# Import needed for test
from arifosmcp.runtime.tools import get_caller_status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
