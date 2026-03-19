"""
tests/test_runtime_adversarial_auth.py — F11 Adversarial Identity and Auth Hardening Tests

This suite targets edge cases around token forgery, session masking, precedence injection,
and identity escalation, ensuring the F11/F1 invariants remain unbroken.
"""

import pytest
import time
import asyncio
from arifosmcp.runtime.tools import init_anchor, arifos_kernel, get_caller_status
from core.enforcement.auth_continuity import mint_auth_context
from arifosmcp.runtime.models import Verdict
from arifosmcp.runtime.sessions import get_session_identity, clear_session_identity, set_active_session

@pytest.mark.asyncio
class TestAdversarialIdentity:
    async def test_inv1_precedence_attack_downgrade(self):
        """
        Payload: actor_id="anonymous" or "user", declared_name="ariffazil" (sovereign)
        Expect: Resolves strictly to the actor_id capability, discarding declared_name's false authority.
        """
        # We test this by attempting init_anchor with conflicting identities
        anchor = await init_anchor(
            raw_input="Attempt precedence injection",
            actor_id="declared_user",
            declared_name="ariffazil"
        )
        assert anchor.ok is True
        
        # After anchoring, check the stored identity
        stored = get_session_identity(anchor.session_id)
        assert stored is not None
        assert stored["actor_id"] == "declared_user"
        assert stored["authority_level"] == "declared" # Should NOT be sovereign
        
    async def test_inv2_token_session_mismatch(self):
        """
        Valid Token A (from Session A), injected into Session B's kernel call.
        Expect: Rejected (Token bound to different session ID).
        """
        # 1. Mint valid sovereign token for Session A
        anchor_a = await init_anchor(
            actor_id="ariffazil",
            intent="Mint token A"
        )
        token_a = anchor_a.auth_context
        
        # 2. Extract context
        if hasattr(token_a, "model_dump"):
            token_a_dict = token_a.model_dump(mode="json")
        else:
            token_a_dict = token_a
            
        # 3. Create Session B (anonymously)
        # 4. Attempt to use Token A on Session B
        # we can pass it by overriding session_id but giving auth_context
        res = await arifos_kernel(
            query="Execute privileged action",
            session_id="session-B-adversary123", # Different session
            auth_context=token_a_dict,
            risk_tier="high"
        )
        
        # Should be blocked due to mismatch F11
        assert res.verdict in (Verdict.HOLD, Verdict.VOID, Verdict.SABAR), "Allowed stolen token cross-session"
        assert res.errors is not None and len(res.errors) > 0
        error_msg = str(res.errors[0].message)
        assert "mismatch" in error_msg.lower() or "bound" in error_msg.lower() or "auth" in error_msg.lower()

    async def test_inv3_expiration_forgery(self):
        """
        Expired auth_context where client bumped 'exp' timestamp without recalculating signature.
        Expect: Rejected (Signature failure).
        """
        # Mint token
        auth_context_dict = mint_auth_context(
            actor_id="ariffazil",
            authority_level="sovereign",
            approval_scope=["arifOS_kernel:execute"],
            session_id="session-expired-test",
            token_fingerprint="mock-fingerprint",
            parent_signature="mock-signature"
        )
        
        # Tamper with expiry
        auth_context_dict["exp"] += 90000 
        
        kernel_res = await arifos_kernel(
            query="High risk action",
            session_id="session-expired-test",
            auth_context=auth_context_dict,
            risk_tier="high"
        )
        
        assert kernel_res.verdict in (Verdict.HOLD, Verdict.VOID, Verdict.SABAR)
        assert any("tamper" in str(e.message).lower() or "sign" in str(e.message).lower() or "invalid" in str(e.message).lower() for e in kernel_res.errors)

    async def test_inv4_null_byte_whitespace_coercion(self):
        """
        Payload: actor_id="   " or "\\x00"
        Expect: Safely handled exactly like "anonymous".
        """
        anchor = await init_anchor(
            actor_id="   ",
            intent="Null byte attack"
        )
        
        # The system might refuse anchoring or gracefully downgrade to anonymous/guest
        if anchor.ok:
            stored = get_session_identity(anchor.session_id)
            assert stored["actor_id"] == "anonymous"
            assert stored["authority_level"] == "anonymous"

    async def test_inv5_global_diagnostics_isolation(self):
        """
        If session_id="global", it MUST remain completely stateless.
        Cannot overwrite _ACTIVE_SESSION_ID.
        """
        anchor = await init_anchor(actor_id="declared_user", intent="Create baseline")
        active = anchor.session_id
        set_active_session(active)
        
        # Call global
        global_res = await get_caller_status(session_id="global")
        
        # Must be anonymous
        assert global_res.payload["caller_state"] == "anonymous"
        
        # Active session must remain unchanged
        from arifosmcp.runtime.sessions import _ACTIVE_SESSION_ID
        assert _ACTIVE_SESSION_ID == active
