"""
888_HOLD Escalation State Machine

F13 Sovereign Safety Valve

Implements three escalation pathways:
1. Reply + Continue: Refuse but keep conversation active
2. Offer Handover: Recommend human specialist transfer
3. Forced Escalation: Immediate human routing (non-negotiable)

Trigger Conditions:
- F2 verification failure (hallucination)
- F12 injection detection (high confidence)
- F11 unauthorized access attempt
- Irreversible operation detected
- Missing grounding evidence
- Jurisdictional ambiguity

All escalations are logged to VAULT999.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4


logger = logging.getLogger(__name__)


class EscalationPathway(Enum):
    """Three constitutional escalation pathways."""
    REPLY_CONTINUE = auto()    # Refuse but keep active
    OFFER_HANDOVER = auto()    # Recommend human (user choice)
    FORCED_ESCALATION = auto() # Immediate human (no choice)


class HoldState(Enum):
    """States in the 888_HOLD lifecycle."""
    PENDING = auto()       # Awaiting human response
    APPROVED = auto()      # Human approved - proceed
    DENIED = auto()        # Human denied - block
    TIMEOUT = auto()       # No response in time
    CANCELLED = auto()     # Cancelled by agent


@dataclass
class HoldRequest:
    """A request for human approval (888_HOLD)."""
    hold_id: str
    execution_id: str
    agent_id: str
    action_type: str
    
    # Escalation details
    pathway: EscalationPathway
    reason: str
    risk_level: str  # low, medium, high, critical
    
    # Constitutional context
    floor_violations: List[str] = field(default_factory=list)
    floor_scores: List[Dict] = field(default_factory=list)
    
    # Human response
    state: HoldState = field(default=HoldState.PENDING)
    human_decision: Optional[str] = None
    human_notes: Optional[str] = None
    responded_by: Optional[str] = None
    
    # Timing
    created_at: datetime = field(default_factory=datetime.utcnow)
    responded_at: Optional[datetime] = None
    timeout_seconds: int = 3600  # 1 hour default
    
    # Action payload (what was blocked)
    action_payload: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for VAULT999."""
        return {
            "hold_id": self.hold_id,
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "action_type": self.action_type,
            "pathway": self.pathway.name,
            "reason": self.reason,
            "risk_level": self.risk_level,
            "floor_violations": self.floor_violations,
            "state": self.state.name,
            "human_decision": self.human_decision,
            "human_notes": self.human_notes,
            "responded_by": self.responded_by,
            "created_at": self.created_at.isoformat(),
            "responded_at": self.responded_at.isoformat() if self.responded_at else None,
            "timeout_seconds": self.timeout_seconds
        }


class HoldStateManager:
    """
    888_HOLD State Machine Manager.
    
    Central coordinator for all escalation flows.
    Manages pending holds, human notifications, and resolution.
    """
    
    def __init__(
        self,
        notification_callback: Optional[Callable] = None,
        vault_logger=None,
        default_timeout: int = 3600
    ):
        self.notification_callback = notification_callback
        self.vault = vault_logger
        self.default_timeout = default_timeout
        
        # Active holds
        self.pending_holds: Dict[str, HoldRequest] = {}
        self.resolved_holds: Dict[str, HoldRequest] = {}
        
        # Statistics
        self.stats = {
            "total_holds": 0,
            "approved": 0,
            "denied": 0,
            "timeouts": 0,
            "by_pathway": {
                "REPLY_CONTINUE": 0,
                "OFFER_HANDOVER": 0,
                "FORCED_ESCALATION": 0
            }
        }
    
    async def create_hold(
        self,
        execution_id: str,
        agent_id: str,
        action_type: str,
        reason: str,
        risk_level: str,
        pathway: EscalationPathway = EscalationPathway.OFFER_HANDOVER,
        floor_violations: Optional[List[str]] = None,
        floor_scores: Optional[List[Dict]] = None,
        action_payload: Optional[Dict] = None,
        timeout_seconds: Optional[int] = None
    ) -> HoldRequest:
        """
        Create a new 888_HOLD escalation.
        
        This pauses the agent execution and awaits human decision.
        """
        hold_id = f"HOLD-{uuid4().hex[:12].upper()}"
        
        hold = HoldRequest(
            hold_id=hold_id,
            execution_id=execution_id,
            agent_id=agent_id,
            action_type=action_type,
            pathway=pathway,
            reason=reason,
            risk_level=risk_level,
            floor_violations=floor_violations or [],
            floor_scores=floor_scores or [],
            action_payload=action_payload or {},
            timeout_seconds=timeout_seconds or self.default_timeout
        )
        
        self.pending_holds[hold_id] = hold
        self.stats["total_holds"] += 1
        self.stats["by_pathway"][pathway.name] += 1
        
        logger.warning(f"[{hold_id}] 888_HOLD created for {action_type} "
                      f"(risk={risk_level}, pathway={pathway.name})")
        
        # Log to VAULT999
        if self.vault:
            await self.vault.log_escalation(hold.to_dict())
        
        # Notify human (if callback configured)
        if self.notification_callback:
            await self.notification_callback(hold)
        
        return hold
    
    async def resolve_hold(
        self,
        hold_id: str,
        decision: str,  # APPROVED or DENIED
        responded_by: str,
        notes: Optional[str] = None
    ) -> HoldRequest:
        """
        Resolve a pending hold with human decision.
        
        This is the F13 Sovereign in action.
        """
        if hold_id not in self.pending_holds:
            raise ValueError(f"Hold {hold_id} not found or already resolved")
        
        hold = self.pending_holds[hold_id]
        
        # Update state
        if decision == "APPROVED":
            hold.state = HoldState.APPROVED
            self.stats["approved"] += 1
            logger.info(f"[{hold_id}] APPROVED by {responded_by}")
            
        elif decision == "DENIED":
            hold.state = HoldState.DENIED
            self.stats["denied"] += 1
            logger.info(f"[{hold_id}] DENIED by {responded_by}")
            
        else:
            raise ValueError(f"Invalid decision: {decision}")
        
        hold.human_decision = decision
        hold.human_notes = notes
        hold.responded_by = responded_by
        hold.responded_at = datetime.utcnow()
        
        # Move to resolved
        self.resolved_holds[hold_id] = hold
        del self.pending_holds[hold_id]
        
        # Log to VAULT999
        if self.vault:
            await self.vault.log_escalation_resolution(hold.to_dict())
        
        return hold
    
    async def check_hold_status(self, hold_id: str) -> Optional[HoldState]:
        """Check the current status of a hold."""
        if hold_id in self.pending_holds:
            hold = self.pending_holds[hold_id]
            
            # Check for timeout
            elapsed = (datetime.utcnow() - hold.created_at).total_seconds()
            if elapsed > hold.timeout_seconds:
                hold.state = HoldState.TIMEOUT
                self.stats["timeouts"] += 1
                
                # Move to resolved
                self.resolved_holds[hold_id] = hold
                del self.pending_holds[hold_id]
                
                logger.warning(f"[{hold_id}] TIMEOUT after {hold.timeout_seconds}s")
                
                if self.vault:
                    await self.vault.log_escalation_timeout(hold.to_dict())
                
                return HoldState.TIMEOUT
            
            return HoldState.PENDING
        
        if hold_id in self.resolved_holds:
            return self.resolved_holds[hold_id].state
        
        return None
    
    def get_pending_holds(self) -> List[HoldRequest]:
        """Get all pending holds awaiting human response."""
        return list(self.pending_holds.values())
    
    def get_hold_details(self, hold_id: str) -> Optional[HoldRequest]:
        """Get details of a specific hold."""
        if hold_id in self.pending_holds:
            return self.pending_holds[hold_id]
        if hold_id in self.resolved_holds:
            return self.resolved_holds[hold_id]
        return None
    
    async def auto_escalate_critical(
        self,
        execution_id: str,
        agent_id: str,
        action_type: str,
        reason: str,
        floor_violations: List[str]
    ) -> HoldRequest:
        """
        Automatically escalate critical violations.
        
        Uses FORCED_ESCALATION pathway (no user choice).
        """
        return await self.create_hold(
            execution_id=execution_id,
            agent_id=agent_id,
            action_type=action_type,
            reason=reason,
            risk_level="critical",
            pathway=EscalationPathway.FORCED_ESCALATION,
            floor_violations=floor_violations,
            timeout_seconds=600  # 10 min for critical
        )
    
    async def offer_handover(
        self,
        execution_id: str,
        agent_id: str,
        action_type: str,
        reason: str
    ) -> HoldRequest:
        """
        Offer to handover to human specialist.
        
        Uses OFFER_HANDOVER pathway (user can decline).
        """
        return await self.create_hold(
            execution_id=execution_id,
            agent_id=agent_id,
            action_type=action_type,
            reason=reason,
            risk_level="high",
            pathway=EscalationPathway.OFFER_HANDOVER
        )
    
    async def reply_and_continue(
        self,
        execution_id: str,
        agent_id: str,
        action_type: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Refuse action but keep conversation active.
        
        Uses REPLY_CONTINUE pathway (softest escalation).
        
        Returns message to send to user.
        """
        hold = await self.create_hold(
            execution_id=execution_id,
            agent_id=agent_id,
            action_type=action_type,
            reason=reason,
            risk_level="medium",
            pathway=EscalationPathway.REPLY_CONTINUE
        )
        
        # For REPLY_CONTINUE, we don't block - we just note it
        # In this pathway, the agent continues but with a warning
        
        return {
            "hold_id": hold.hold_id,
            "message": f"I cannot perform this action: {reason}. "
                      f"However, I'm happy to help with something else within safe boundaries.",
            "pathway": "REPLY_CONTINUE",
            "requires_human": False
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get escalation statistics."""
        return {
            **self.stats,
            "pending_count": len(self.pending_holds),
            "resolved_count": len(self.resolved_holds)
        }
    
    async def cleanup_old_holds(self, max_age_hours: int = 24):
        """Clean up old resolved holds to prevent memory bloat."""
        cutoff = datetime.utcnow() - __import__('datetime').timedelta(hours=max_age_hours)
        
        to_remove = []
        for hold_id, hold in self.resolved_holds.items():
            if hold.responded_at and hold.responded_at < cutoff:
                to_remove.append(hold_id)
        
        for hold_id in to_remove:
            del self.resolved_holds[hold_id]
        
        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} old holds")


# Convenience functions for common escalation patterns

async def escalate_for_f11_violation(
    hold_manager: HoldStateManager,
    execution_id: str,
    agent_id: str,
    action: str
) -> HoldRequest:
    """Escalate for F11 authorization failure."""
    return await hold_manager.create_hold(
        execution_id=execution_id,
        agent_id=agent_id,
        action_type=action,
        reason="F11: Command requires explicit authorization",
        risk_level="high",
        pathway=EscalationPathway.OFFER_HANDOVER,
        floor_violations=["F11"]
    )


async def escalate_for_f12_injection(
    hold_manager: HoldStateManager,
    execution_id: str,
    agent_id: str,
    injection_score: float
) -> HoldRequest:
    """Escalate for F12 injection detection."""
    return await hold_manager.auto_escalate_critical(
        execution_id=execution_id,
        agent_id=agent_id,
        action_type="process_input",
        reason=f"F12: High-confidence injection detected (score={injection_score:.2f})",
        floor_violations=["F12"]
    )


async def escalate_for_irreversible_action(
    hold_manager: HoldStateManager,
    execution_id: str,
    agent_id: str,
    action: str
) -> HoldRequest:
    """Escalate for irreversible operation (F1 Amanah)."""
    return await hold_manager.create_hold(
        execution_id=execution_id,
        agent_id=agent_id,
        action_type=action,
        reason="F1: Irreversible action requires human confirmation",
        risk_level="high",
        pathway=EscalationPathway.OFFER_HANDOVER,
        floor_violations=["F1"]
    )
