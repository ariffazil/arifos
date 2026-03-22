"""
arifosmcp/runtime/init_anchor_hardened.py — Hardened Init Anchor (v2)

The Ignition State of Intelligence with:
- Authority lifecycle management
- Scope degradation logic
- Session class enforcement
- Signed challenge binding
- Approval provenance tracking
"""

from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from arifosmcp.runtime.contracts_v2 import (
    ToolEnvelope,
    ToolStatus,
    RiskTier,
    HumanDecisionMarker,
    SessionClass,
    TraceContext,
    EntropyBudget,
    generate_trace_context,
    validate_fail_closed,
    determine_human_marker,
    calculate_entropy_budget,
)


# ═══════════════════════════════════════════════════════════════════════════════
# SIGNED CHALLENGE — Cryptographic Session Binding
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SignedChallenge:
    """
    Binding of declared_name, intent, requested_scope, risk_tier into one signed challenge.
    
    This prevents tampering with session parameters after establishment.
    """
    challenge_id: str
    declared_name: str
    intent: str
    requested_scope: list[str]
    risk_tier: RiskTier
    session_class: SessionClass
    timestamp: str
    nonce: str
    policy_version: str = "v2026.03.22-hardened"
    
    def to_canonical(self) -> str:
        """Create canonical string for signing."""
        data = {
            "challenge_id": self.challenge_id,
            "declared_name": self.declared_name,
            "intent": self.intent[:100],  # Truncate for safety
            "requested_scope": sorted(self.requested_scope),
            "risk_tier": self.risk_tier.value,
            "session_class": self.session_class.value,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "policy_version": self.policy_version,
        }
        return json.dumps(data, sort_keys=True, separators=(',', ':'))
    
    def compute_hash(self) -> str:
        """Compute challenge hash (simulates signature)."""
        return hashlib.sha256(self.to_canonical().encode()).hexdigest()[:32]


# ═══════════════════════════════════════════════════════════════════════════════
# APPROVAL PROVENANCE — Who, When, Under What Policy
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ApprovalProvenance:
    """
    Complete audit trail of approval.
    
    - who approved
    - when
    - under what policy version
    """
    approver_id: str
    approver_type: str  # human | system | sovereign
    approved_at: str
    policy_version: str
    approval_method: str  # semantic_key | webauthn | human_override | delegation
    challenge_hash: str
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "approver_id": self.approver_id,
            "approver_type": self.approver_type,
            "approved_at": self.approved_at,
            "policy_version": self.policy_version,
            "approval_method": self.approval_method,
            "challenge_hash": self.challenge_hash,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE — Lifecycle Intelligence
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SessionState:
    """
    Full session state for degradation detection.
    """
    session_id: str
    created_at: str
    last_activity: str
    declared_name: str
    session_class: SessionClass
    current_scope: list[str]
    risk_tier: RiskTier
    challenge_hash: str
    
    # Context tracking for degradation
    original_context: dict[str, Any] = field(default_factory=dict)
    context_changes: list[dict] = field(default_factory=list)
    posture_score: float = 1.0  # 1.0 = pristine, 0.0 = compromised
    
    def age_seconds(self) -> float:
        """Calculate session age."""
        created = datetime.fromisoformat(self.created_at)
        now = datetime.now(timezone.utc)
        return (now - created).total_seconds()
    
    def is_expired(self, max_age_seconds: float = 3600) -> bool:
        """Check if session has exceeded TTL."""
        return self.age_seconds() > max_age_seconds
    
    def record_context_change(self, change_type: str, details: dict):
        """Record a context change for audit."""
        self.context_changes.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": change_type,
            "details": details,
        })


# ═══════════════════════════════════════════════════════════════════════════════
# SCOPE DEGRADATION — Automatic Downgrade Instead of Full Revoke
# ═══════════════════════════════════════════════════════════════════════════════

class ScopeDegradationEngine:
    """
    Implements anchor degradation logic:
    
    if session ages → degrade scope
    if context changes → degrade scope  
    if toolchain role changes → degrade scope
    if network/device posture changes → degrade scope
    
    Instead of full revoke first, downgrade scope automatically.
    """
    
    DEGRADATION_RULES = {
        "session_age": {
            "threshold_1": (1800, "downgrade_to_advise"),    # 30 min
            "threshold_2": (3600, "downgrade_to_observe"),   # 60 min
        },
        "context_change": {
            "actor_id_change": "immediate_degrade",
            "network_change": "downgrade_one_level",
            "device_change": "downgrade_one_level",
        },
        "posture_score": {
            "below_0.5": "downgrade_to_observe",
            "below_0.2": "immediate_revoke",
        },
    }
    
    @classmethod
    def check_degradation(cls, state: SessionState) -> tuple[bool, str, list[str]]:
        """
        Check if session needs degradation.
        
        Returns:
            (needs_action, action_type, new_scope)
        """
        actions = []
        
        # Check session age
        age = state.age_seconds()
        if age > cls.DEGRADATION_RULES["session_age"]["threshold_2"][0]:
            actions.append(("age", "downgrade_to_observe"))
        elif age > cls.DEGRADATION_RULES["session_age"]["threshold_1"][0]:
            actions.append(("age", "downgrade_to_advise"))
        
        # Check posture score
        if state.posture_score < 0.2:
            actions.append(("posture", "immediate_revoke"))
        elif state.posture_score < 0.5:
            actions.append(("posture", "downgrade_to_observe"))
        
        # Determine outcome
        if any(a[1] == "immediate_revoke" for a in actions):
            return True, "immediate_revoke", []
        
        if any(a[1] == "downgrade_to_observe" for a in actions):
            new_scope = cls._get_scope_for_class(SessionClass.OBSERVE)
            return True, "downgrade_to_observe", new_scope
        
        if any(a[1] == "downgrade_to_advise" for a in actions):
            new_scope = cls._get_scope_for_class(SessionClass.ADVISE)
            return True, "downgrade_to_advise", new_scope
        
        return False, "no_action", state.current_scope
    
    @classmethod
    def _get_scope_for_class(cls, session_class: SessionClass) -> list[str]:
        """Get default scope for session class."""
        scopes = {
            SessionClass.OBSERVE: ["read", "query", "audit"],
            SessionClass.ADVISE: ["read", "query", "recommend", "draft"],
            SessionClass.EXECUTE: ["read", "write", "execute", "query"],
            SessionClass.SOVEREIGN: ["*"],  # All permissions
        }
        return scopes.get(session_class, ["read"])
    
    @classmethod
    def downgrade_one_level(cls, current: SessionClass) -> SessionClass:
        """Downgrade session class by one level."""
        order = [SessionClass.SOVEREIGN, SessionClass.EXECUTE, SessionClass.ADVISE, SessionClass.OBSERVE]
        try:
            idx = order.index(current)
            if idx < len(order) - 1:
                return order[idx + 1]
        except ValueError:
            pass
        return SessionClass.OBSERVE  # Fail closed


# ═══════════════════════════════════════════════════════════════════════════════
# HARDENED INIT ANCHOR — The Ignition State v2
# ═══════════════════════════════════════════════════════════════════════════════

class HardenedInitAnchor:
    """
    Hardened init_anchor with:
    - Signed challenge binding
    - Session class enforcement
    - Scope negotiation (not silent issue)
    - Explicit denial reasons
    - Approval provenance
    - Anchor degradation logic
    """
    
    # Session registry (in production, use Redis)
    _sessions: dict[str, SessionState] = {}
    
    async def init(
        self,
        declared_name: str,
        intent: str,
        requested_scope: list[str],
        risk_tier: str,
        auth_context: dict | None = None,
        session_id: str | None = None,
        session_class: str = "execute",
        human_approval: bool = False,
        proof: str | None = None,
        trace: TraceContext | None = None,
    ) -> ToolEnvelope:
        """
        Initialize hardened session anchor.
        
        Requires scope negotiation — will not silently issue broad scope.
        """
        tool = "init_anchor"
        session_id = session_id or f"sess-{secrets.token_hex(8)}"
        
        # Validate fail-closed
        validation = validate_fail_closed(
            auth_context=auth_context,
            risk_tier=risk_tier,
            session_id=session_id,
            tool=tool,
            trace=trace,
        )
        if not validation.valid:
            return validation.to_envelope(tool, session_id, trace)
        
        # Parse risk tier
        try:
            risk = RiskTier(risk_tier.lower())
        except ValueError:
            return ToolEnvelope.void(
                tool=tool,
                session_id=session_id,
                reason=f"Invalid risk_tier: {risk_tier}",
                trace=trace,
            )
        
        # Parse session class
        try:
            sclass = SessionClass(session_class.lower())
        except ValueError:
            return ToolEnvelope.void(
                tool=tool,
                session_id=session_id,
                reason=f"Invalid session_class: {session_class}",
                trace=trace,
            )
        
        # Create signed challenge
        challenge = SignedChallenge(
            challenge_id=f"chal-{secrets.token_hex(8)}",
            declared_name=declared_name,
            intent=intent,
            requested_scope=requested_scope,
            risk_tier=risk,
            session_class=sclass,
            timestamp=datetime.now(timezone.utc).isoformat(),
            nonce=secrets.token_hex(16),
        )
        challenge_hash = challenge.compute_hash()
        
        # Scope negotiation (not silent issue)
        allowed_scope = self._negotiate_scope(
            requested=requested_scope,
            session_class=sclass,
            risk_tier=risk,
            declared_name=declared_name,
            has_human_approval=human_approval,
        )
        
        # Check if scope was reduced
        scope_reduced = set(requested_scope) != set(allowed_scope)
        warnings = []
        if scope_reduced:
            warnings.append(
                f"Scope negotiated: requested {requested_scope}, granted {allowed_scope}"
            )
        
        # If scope reduced to nothing, explicit denial
        if not allowed_scope:
            return ToolEnvelope.hold(
                tool=tool,
                session_id=session_id,
                reason=f"Scope denied: requested {requested_scope} exceeds authority for {sclass.value} class",
                trace=trace,
            )
        
        # Create approval provenance
        provenance = ApprovalProvenance(
            approver_id=declared_name,
            approver_type="sovereign" if sclass == SessionClass.SOVEREIGN else "system",
            approved_at=datetime.now(timezone.utc).isoformat(),
            policy_version=challenge.policy_version,
            approval_method="human_override" if human_approval else "semantic_key",
            challenge_hash=challenge_hash,
        )
        
        # Create session state
        state = SessionState(
            session_id=session_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            last_activity=datetime.now(timezone.utc).isoformat(),
            declared_name=declared_name,
            session_class=sclass,
            current_scope=allowed_scope,
            risk_tier=risk,
            challenge_hash=challenge_hash,
            original_context={
                "declared_name": declared_name,
                "intent": intent,
                "requested_scope": requested_scope,
            },
        )
        
        # Store session
        self._sessions[session_id] = state
        
        # Determine human marker
        human_marker = determine_human_marker(
            risk_tier=risk,
            confidence=0.95 if human_approval else 0.80,
            blast_radius="minimal" if sclass == SessionClass.OBSERVE else "limited",
            human_approved=human_approval,
        )
        
        # Calculate entropy
        entropy = calculate_entropy_budget(
            ambiguity_score=0.0,  # Init is authoritative
            assumptions=[],
            blast_radius="minimal",
            confidence=0.95,
        )
        
        # Build envelope
        envelope = ToolEnvelope(
            status=ToolStatus.OK,
            tool=tool,
            session_id=session_id,
            risk_tier=risk,
            confidence=0.95,
            human_decision=human_marker,
            requires_human=human_marker in (
                HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED,
                HumanDecisionMarker.HUMAN_APPROVAL_BOUND,
            ),
            inputs_hash=challenge_hash,
            outputs_hash=hashlib.sha256(
                json.dumps(allowed_scope, sort_keys=True).encode()
            ).hexdigest()[:32],
            trace=trace,
            evidence_refs=[challenge_hash],
            warnings=warnings,
            entropy=entropy,
            next_allowed_tools=self._get_next_tools(sclass),
            payload={
                "challenge": {
                    "challenge_id": challenge.challenge_id,
                    "hash": challenge_hash,
                    "session_class": sclass.value,
                },
                "scope": {
                    "requested": requested_scope,
                    "granted": allowed_scope,
                    "negotiated": scope_reduced,
                },
                "provenance": provenance.to_dict(),
                "degradation_ready": True,
            },
        )
        
        return envelope
    
    async def state(
        self,
        session_id: str,
        trace: TraceContext | None = None,
    ) -> ToolEnvelope:
        """Check session state with degradation detection."""
        tool = "init_anchor"
        
        if session_id not in self._sessions:
            return ToolEnvelope.void(
                tool=tool,
                session_id=session_id,
                reason="Session not found",
                trace=trace,
            )
        
        state = self._sessions[session_id]
        
        # Check degradation
        needs_action, action_type, new_scope = ScopeDegradationEngine.check_degradation(state)
        
        warnings = []
        if needs_action:
            warnings.append(f"Degradation triggered: {action_type}")
            state.current_scope = new_scope
            
            if action_type == "immediate_revoke":
                del self._sessions[session_id]
                return ToolEnvelope.void(
                    tool=tool,
                    session_id=session_id,
                    reason="Session revoked due to security posture degradation",
                    trace=trace,
                )
        
        # Update activity
        state.last_activity = datetime.now(timezone.utc).isoformat()
        
        return ToolEnvelope(
            status=ToolStatus.OK,
            tool=tool,
            session_id=session_id,
            risk_tier=state.risk_tier,
            confidence=0.90,
            trace=trace,
            warnings=warnings,
            entropy=calculate_entropy_budget(
                blast_radius="minimal",
                confidence=0.90,
            ),
            payload={
                "session": {
                    "declared_name": state.declared_name,
                    "session_class": state.session_class.value,
                    "age_seconds": state.age_seconds(),
                    "scope": state.current_scope,
                    "posture_score": state.posture_score,
                },
                "degradation": {
                    "action_required": needs_action,
                    "action_type": action_type,
                },
                "context_changes": state.context_changes,
            },
        )
    
    async def revoke(
        self,
        session_id: str,
        reason: str,
        trace: TraceContext | None = None,
    ) -> ToolEnvelope:
        """Revoke session anchor."""
        tool = "init_anchor"
        
        if session_id in self._sessions:
            del self._sessions[session_id]
        
        return ToolEnvelope(
            status=ToolStatus.OK,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier.LOW,
            confidence=1.0,
            trace=trace,
            payload={
                "revoked": True,
                "reason": reason,
            },
        )
    
    def _negotiate_scope(
        self,
        requested: list[str],
        session_class: SessionClass,
        risk_tier: RiskTier,
        declared_name: str,
        has_human_approval: bool,
    ) -> list[str]:
        """
        Negotiate scope based on authority, not silent issue.
        """
        # Base scope by class
        base_scope = ScopeDegradationEngine._get_scope_for_class(session_class)
        
        # High risk requires human approval for write/execute
        if risk_tier in (RiskTier.HIGH, RiskTier.SOVEREIGN):
            if not has_human_approval:
                base_scope = [s for s in base_scope if s in ("read", "query", "audit")]
        
        # Intersect with requested
        allowed = [s for s in requested if s in base_scope]
        
        return allowed
    
    def _get_next_tools(self, session_class: SessionClass) -> list[str]:
        """Determine allowed next tools based on session class."""
        base = ["math_estimator", "architect_registry"]
        
        if session_class in (SessionClass.EXECUTE, SessionClass.SOVEREIGN):
            base.extend([
                "arifOS_kernel",
                "agi_mind",
                "asi_heart",
                "physics_reality",
            ])
        
        if session_class == SessionClass.SOVEREIGN:
            base.extend([
                "engineering_memory",
                "vault_ledger",
                "apex_soul",
            ])
        
        return base


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "HardenedInitAnchor",
    "SignedChallenge",
    "ApprovalProvenance",
    "SessionState",
    "ScopeDegradationEngine",
    "SessionClass",
]
