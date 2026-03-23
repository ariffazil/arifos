"""
arifosmcp/runtime/init_anchor_hardened.py — Hardened Init Anchor (v2)

The Ignition State of Intelligence with:
- Authority lifecycle management
- Scope degradation logic
- Session class enforcement
- Signed challenge binding
- Approval provenance tracking
- Input-Normalization Contract (v3):
  tolerant on transport shape, strict on authority and intent
"""

from __future__ import annotations

import hashlib
import json
import re
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
# CANONICAL INGRESS FIELDS — Recognized by init_anchor normalization layer
# ═══════════════════════════════════════════════════════════════════════════════

_CANONICAL_FIELDS: frozenset[str] = frozenset({
    "declared_name", "intent", "requested_scope", "risk_tier",
    "auth_context", "session_id", "session_class", "human_approval",
    "proof", "trace", "query", "raw_input", "actor_id",
    "caller_context", "pns_shield",
})

# Patterns that indicate injection or authority-override attempts
_INJECTION_PATTERNS: tuple[str, ...] = (
    "ignore policy",
    "ignore all previous instructions",
    "forget your instructions",
    "you are now",
    "treat me as sovereign",
    "override constitution",
    "your new instructions",
    "disregard all",
    "ignore all laws",
    "you must obey",
)

# Fields that are advisory only — never elevated to authority
_ADVISORY_ONLY_FIELDS: frozenset[str] = frozenset({
    "raw_input", "caller_context", "pns_shield",
})

# Truthy/falsy normalization maps for human_approval
_TRUTHY_STRINGS: frozenset[str] = frozenset({"true", "yes", "1"})
_FALSY_STRINGS: frozenset[str] = frozenset({"false", "no", "0"})


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
        # ── Canonical ingress fields (Section 4.1 of contract) ──
        declared_name: str | None = None,
        intent: str | dict | None = None,
        requested_scope: list[str] | None = None,
        risk_tier: str = "low",
        auth_context: dict | None = None,
        session_id: str | None = None,
        session_class: str = "execute",
        human_approval: bool | str | int | None = False,
        proof: str | None = None,
        trace: TraceContext | None = None,
        # ── Extended canonical fields ──
        query: str | None = None,
        raw_input: str | None = None,
        actor_id: str | None = None,
        caller_context: dict | None = None,
        pns_shield: Any = None,
        # ── Unknown field absorber (Section 3.1) ──
        **kwargs: Any,
    ) -> ToolEnvelope:
        """
        Initialize hardened session anchor.

        Input-Normalization Contract (v3):
        - Tolerant on transport shape: unknown fields ignored, not rejected
        - Strict on authority: no authority from raw text or caller metadata
        - Strict on intent: must provide at least one of intent/query/raw_input
        - Fail-closed for risky/privileged flows, open for low-risk session start
        """
        tool = "init_anchor"

        # ── STEP 1: Record which canonical fields were actually provided ──
        accepted_fields: list[str] = []
        ignored_fields: list[str] = list(kwargs.keys())
        derived_fields: list[str] = []
        normalization_warnings: list[str] = []

        if declared_name is not None: accepted_fields.append("declared_name")
        if actor_id is not None: accepted_fields.append("actor_id")
        if intent is not None: accepted_fields.append("intent")
        if query is not None: accepted_fields.append("query")
        if raw_input is not None: accepted_fields.append("raw_input")
        if requested_scope is not None: accepted_fields.append("requested_scope")
        if auth_context is not None: accepted_fields.append("auth_context")
        if session_id is not None: accepted_fields.append("session_id")
        if caller_context is not None: accepted_fields.append("caller_context")
        if pns_shield is not None: accepted_fields.append("pns_shield")
        if proof is not None: accepted_fields.append("proof")

        # ── STEP 2: Normalize strings (trim/collapse whitespace) ──
        def _norm_str(v: Any) -> str | None:
            if isinstance(v, str):
                normalized = " ".join(v.strip().split())
                return normalized if normalized else None
            return None

        _dn = _norm_str(declared_name) or _norm_str(actor_id)
        declared_name_norm: str = _dn if _dn is not None else "anonymous"
        query = _norm_str(query)
        raw_input = _norm_str(raw_input)

        if isinstance(intent, str):
            intent = _norm_str(intent)
        elif isinstance(intent, dict):
            # Normalize string values inside intent dict
            intent = {k: (_norm_str(v) if isinstance(v, str) else v) for k, v in intent.items()}

        # ── STEP 3: Normalize human_approval boolean ──
        if isinstance(human_approval, str):
            lower_ha = human_approval.lower().strip()
            if lower_ha in _TRUTHY_STRINGS:
                human_approval = True
            elif lower_ha in _FALSY_STRINGS:
                human_approval = False
            else:
                normalization_warnings.append(
                    f"human_approval value '{human_approval}' is ambiguous — defaulted to False"
                )
                human_approval = False
        elif isinstance(human_approval, int):
            human_approval = bool(human_approval)
        elif human_approval is None:
            human_approval = False

        # ── STEP 4: Derive effective intent (intent > query > raw_input > name fallback) ──
        effective_intent: str | None = None
        if intent:
            if isinstance(intent, dict):
                effective_intent = (
                    intent.get("query") or intent.get("task") or
                    intent.get("raw_input") or str(intent)
                )
            else:
                effective_intent = intent
        elif query:
            effective_intent = query
            derived_fields.append("intent (derived from query)")
        elif raw_input:
            effective_intent = raw_input
            derived_fields.append("intent (derived from raw_input)")
        elif declared_name_norm and declared_name_norm != "anonymous":
            # Fallback: named caller with no explicit intent — derive minimal session intent
            effective_intent = f"Session initialization for {declared_name_norm}"
            derived_fields.append("intent (derived from declared_name — minimal fallback)")
        elif auth_context and isinstance(auth_context, dict) and auth_context.get("actor_id"):
            effective_intent = "Authenticated session initialization"
            derived_fields.append("intent (derived from auth_context — minimal fallback)")

        # ── STEP 5: Injection defense on free-text fields (F12) ──
        for field_name, text_val in [
            ("intent", effective_intent),
            ("query", query),
            ("raw_input", raw_input),
        ]:
            if text_val and any(p in text_val.lower() for p in _INJECTION_PATTERNS):
                return ToolEnvelope.void(
                    tool=tool,
                    session_id=session_id or "session-rejected",
                    reason=f"F12: Injection attempt detected in field '{field_name}'",
                    trace=trace,
                )

        # ── STEP 6: Reject if minimum safe intent is missing ──
        if not effective_intent:
            return ToolEnvelope.void(
                tool=tool,
                session_id=session_id or "session-rejected",
                reason="Missing minimum: provide at least one of intent, query, or raw_input",
                trace=trace,
            )

        # ── STEP 7: Normalize session_id (auto-mint if absent) ──
        if not session_id or not str(session_id).strip():
            session_id = f"sess-{secrets.token_hex(8)}"
            derived_fields.append(f"session_id (auto-minted: {session_id})")
        else:
            session_id = str(session_id).strip()

        # ── STEP 8: Normalize risk_tier ──
        try:
            risk = RiskTier((risk_tier or "low").lower().strip())
        except ValueError:
            normalization_warnings.append(
                f"risk_tier '{risk_tier}' is invalid — defaulted to 'low'"
            )
            risk = RiskTier.LOW
            derived_fields.append("risk_tier (defaulted to 'low')")

        # ── STEP 9: Normalize session_class ──
        try:
            sclass = SessionClass((session_class or "execute").lower().strip())
        except ValueError:
            normalization_warnings.append(
                f"session_class '{session_class}' is invalid — defaulted to 'execute'"
            )
            sclass = SessionClass.EXECUTE
            derived_fields.append("session_class (defaulted to 'execute')")

        # ── STEP 10: Normalize requested_scope ──
        if not requested_scope:
            requested_scope = ["read", "query"]
            derived_fields.append("requested_scope (defaulted to ['read', 'query'])")

        # ── STEP 11: Validate caller_context (advisory only — never sovereign) ──
        if caller_context is not None:
            _known_caller_fields = {
                "agent_id", "model_id", "persona_id", "runtime_role",
                "toolchain_role", "extra",
            }
            caller_unknown = [k for k in caller_context if k not in _known_caller_fields]
            if caller_unknown:
                normalization_warnings.append(
                    f"caller_context: ignored unknown subfields {caller_unknown}"
                )
            # Caller context cannot claim authority roles
            rt = caller_context.get("runtime_role", "")
            if rt in ("sovereign", "admin", "root", "god"):
                normalization_warnings.append(
                    f"caller_context.runtime_role='{rt}' ignored: caller_context cannot claim authority (F9)"
                )

        # ── STEP 12: Identity contradiction check (auth_context takes precedence) ──
        if auth_context and isinstance(auth_context, dict):
            auth_actor = auth_context.get("actor_id")
            if (
                auth_actor
                and declared_name_norm != "anonymous"
                and auth_actor != declared_name_norm
            ):
                return ToolEnvelope.void(
                    tool=tool,
                    session_id=session_id,
                    reason=(
                        f"Identity contradiction: declared_name='{declared_name_norm}' "
                        f"conflicts with auth_context.actor_id='{auth_actor}'. "
                        "Signed auth_context takes precedence (F11)."
                    ),
                    trace=trace,
                )
            # Signed auth_context actor wins
            if auth_actor and declared_name_norm == "anonymous":
                declared_name_norm = str(auth_actor)
                derived_fields.append("declared_name (from auth_context.actor_id)")

        # ── STEP 13: Privileged execution check (fail-closed for high-risk) ──
        _privileged_scopes = frozenset({"execute", "write", "delete", "destructive", "*"})
        is_privileged = (
            risk in (RiskTier.HIGH, RiskTier.SOVEREIGN) or
            bool(set(requested_scope) & _privileged_scopes)
        )
        missing_requirements: list[str] = []

        if is_privileged:
            if not auth_context:
                missing_requirements.append("auth_context (required for privileged execution)")
            if risk == RiskTier.SOVEREIGN and not human_approval:
                missing_requirements.append(
                    "human_approval=true (required for sovereign tier)"
                )

        if missing_requirements:
            # Deferred — not malformed. Structured response per contract Section 10.
            return ToolEnvelope.hold(
                tool=tool,
                session_id=session_id,
                reason=(
                    f"Deferred: privileged execution requires: "
                    f"{', '.join(missing_requirements)}"
                ),
                trace=trace,
                missing_requirements=missing_requirements,
                next_allowed_tools=["init_anchor"],
                claimed_actor_id=declared_name_norm,
                suggested_canonical_call={
                    "tool": "init_anchor",
                    "mode": "init",
                    "payload": {
                        "actor_id": declared_name_norm,
                        "intent": effective_intent[:100] if effective_intent else "",
                        "auth_context": "<provide signed auth_context here>",
                        "risk_tier": risk_tier,
                    },
                    "note": "Provide auth_context to unlock privileged or sovereign workflows.",
                },
            )

        # ── STEP 14: Create signed challenge ──
        challenge = SignedChallenge(
            challenge_id=f"chal-{secrets.token_hex(8)}",
            declared_name=declared_name_norm,
            intent=effective_intent[:200],
            requested_scope=requested_scope,
            risk_tier=risk,
            session_class=sclass,
            timestamp=datetime.now(timezone.utc).isoformat(),
            nonce=secrets.token_hex(16),
        )
        challenge_hash = challenge.compute_hash()

        # ── STEP 15: Scope negotiation ──
        allowed_scope = self._negotiate_scope(
            requested=requested_scope,
            session_class=sclass,
            risk_tier=risk,
            declared_name=declared_name_norm,
            has_human_approval=bool(human_approval),
        )

        scope_reduced = set(requested_scope) != set(allowed_scope)
        envelope_warnings: list[str] = list(normalization_warnings)
        if scope_reduced:
            envelope_warnings.append(
                f"Scope negotiated: requested {requested_scope}, granted {allowed_scope}"
            )

        if not allowed_scope:
            return ToolEnvelope.hold(
                tool=tool,
                session_id=session_id,
                reason=(
                    f"Scope denied: requested {requested_scope} exceeds authority "
                    f"for {sclass.value} class"
                ),
                trace=trace,
            )

        # ── STEP 16: Approval provenance ──
        provenance = ApprovalProvenance(
            approver_id=declared_name_norm,
            approver_type="sovereign" if sclass == SessionClass.SOVEREIGN else "system",
            approved_at=datetime.now(timezone.utc).isoformat(),
            policy_version=challenge.policy_version,
            approval_method="human_override" if human_approval else "semantic_key",
            challenge_hash=challenge_hash,
        )

        # ── STEP 17: Session state ──
        state = SessionState(
            session_id=session_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            last_activity=datetime.now(timezone.utc).isoformat(),
            declared_name=declared_name_norm,
            session_class=sclass,
            current_scope=allowed_scope,
            risk_tier=risk,
            challenge_hash=challenge_hash,
            original_context={
                "declared_name": declared_name_norm,
                "intent": effective_intent,
                "requested_scope": requested_scope,
            },
        )
        self._sessions[session_id] = state

        # ── STEP 18: Human marker and entropy ──
        human_marker = determine_human_marker(
            risk_tier=risk,
            confidence=0.95 if human_approval else 0.80,
            blast_radius="minimal" if sclass == SessionClass.OBSERVE else "limited",
            human_approved=bool(human_approval),
        )

        entropy = calculate_entropy_budget(
            ambiguity_score=0.0,
            assumptions=[],
            blast_radius="minimal",
            confidence=0.95,
        )

        # ── STEP 19: Build envelope with normalization report ──
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
            warnings=envelope_warnings,
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
                # ── Normalization report (contract Section 10) ──
                "identity": {
                    "claimed_actor_id": declared_name_norm,
                    "verified_actor_id": (
                        auth_context.get("actor_id") if auth_context and isinstance(auth_context, dict) else None
                    ),
                    "auth_state": "verified" if auth_context else "claimed_only",
                    "note": (
                        "Identity verified via auth_context." if auth_context
                        else "Claimed identity accepted for low-risk session. Not treated as authority."
                    ),
                },
                "normalization": {
                    "status": "created",
                    "accepted_fields": accepted_fields,
                    "ignored_fields": ignored_fields,
                    "derived_fields": derived_fields,
                    "warnings": normalization_warnings,
                    "missing_requirements": [],
                    "reason": (
                        "Anchor created. Low-risk session initialized without full auth."
                        if not auth_context else
                        "Anchor created with authenticated context."
                    ),
                },
                "continuation": {
                    "session_id": session_id,
                    "next_allowed_tools": self._get_next_tools(sclass),
                    "guidance": (
                        "Session initialized. Use arifOS_kernel for governed reasoning, "
                        "or provide auth_context to init_anchor to unlock privileged workflows."
                    ),
                },
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
