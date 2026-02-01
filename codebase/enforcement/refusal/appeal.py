"""
Appeal System — Human-in-the-Loop Review

Constitutional Compliance:
- F1 Amanah: Reversible decisions (appeals allowed)
- F13 Sovereign: Human authority can overturn AI decisions
- F6 Empathy: Users can contest misunderstandings

DITEMPA BUKAN DIBERI — Forged, not given.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class Appeal:
    """Appeal record for contested refusal."""
    session_id: str
    trace_id: str
    user_context: str
    status: str  # PENDING, REVIEWED, OVERTURN, UPHOLD
    submitted_at: str
    reviewed_at: Optional[str] = None
    reviewer: Optional[str] = None
    decision_reason: Optional[str] = None


class AppealSystem:
    """
    Human-in-the-loop review for refusals.
    
    Usage:
        appeal_system = AppealSystem()
        
        # User submits appeal
        result = appeal_system.submit_appeal(
            session_id="sess_123",
            trace_id="abc123def",
            user_context="I was trying to learn about security, not hack"
        )
        
        # Human reviews appeal
        decision = appeal_system.human_review(
            trace_id="abc123def",
            decision="OVERTURN",
            reason="User intent was educational, not malicious",
            reviewer="human_operator"
        )
    """
    
    def __init__(self, appeal_log_path: str = "VAULT999/BBB_LEDGER/appeals.jsonl"):
        """
        Initialize appeal system.
        
        Args:
            appeal_log_path: Path to immutable appeal ledger (JSONL)
        """
        self.appeal_log_path = Path(appeal_log_path)
        self.appeal_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def submit_appeal(self, session_id: str, trace_id: str, user_context: str) -> Dict[str, str]:
        """
        User triggers 'REVIEW' or 'ESCALATE'.
        
        Args:
            session_id: Session identifier
            trace_id: Refusal trace ID (from RefusalResponse)
            user_context: User's explanation of why refusal was incorrect
        
        Returns:
            Dict with appeal_id, status, and message
        """
        appeal = Appeal(
            session_id=session_id,
            trace_id=trace_id,
            user_context=user_context,
            status="PENDING",
            submitted_at=datetime.now(timezone.utc).isoformat()
        )
        
        # Log to immutable ledger
        with open(self.appeal_log_path, "a") as f:
            f.write(json.dumps(asdict(appeal)) + "\n")
        
        return {
            "message": "Appeal recorded. If review is enabled for this deployment, it will be queued.",
            "appeal_id": trace_id,
            "status": "PENDING"
        }
    
    def human_review(
        self, 
        trace_id: str, 
        decision: str, 
        reason: str, 
        reviewer: str = "human_operator"
    ) -> Dict[str, str]:
        """
        Human overturns or upholds refusal.
        
        Args:
            trace_id: Refusal trace ID
            decision: "OVERTURN" (approve original request) or "UPHOLD" (maintain refusal)
            reason: Human's explanation for decision
            reviewer: Human reviewer identifier
        
        Returns:
            Dict with decision details
        """
        if decision not in ["OVERTURN", "UPHOLD"]:
            raise ValueError(f"Invalid decision: {decision}. Must be 'OVERTURN' or 'UPHOLD'.")
        
        # Create review record
        review = {
            "trace_id": trace_id,
            "status": decision,
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
            "reviewer": reviewer,
            "decision_reason": reason,
            "action": "human_review"
        }
        
        # Log decision to immutable ledger
        with open(self.appeal_log_path, "a") as f:
            f.write(json.dumps(review) + "\n")
        
        return {
            "appeal_id": trace_id,
            "decision": decision,
            "reason": reason,
            "reviewed_by": reviewer,
            "reviewed_at": review["reviewed_at"]
        }
    
    def get_pending_appeals(self) -> List[Appeal]:
        """
        Get all pending appeals (not yet reviewed).
        
        Returns:
            List of Appeal objects with status="PENDING"
        """
        appeals = []
        
        if not self.appeal_log_path.exists():
            return appeals
        
        # Track which appeals have been reviewed
        reviewed_ids = set()
        pending_by_id = {}
        
        with open(self.appeal_log_path) as f:
            for line in f:
                data = json.loads(line)
                
                # Track reviewed appeals (they have "action" field)
                if data.get("action") == "human_review":
                    reviewed_ids.add(data["trace_id"])
                
                # Collect pending appeals
                elif data.get("status") == "PENDING":
                    pending_by_id[data["trace_id"]] = Appeal(**data)
        
        # Return only appeals that haven't been reviewed
        for trace_id, appeal in pending_by_id.items():
            if trace_id not in reviewed_ids:
                appeals.append(appeal)
        
        return appeals
    
    def get_appeal_history(self, trace_id: str) -> List[Dict[str, Any]]:
        """
        Get full history for a specific appeal.
        
        Args:
            trace_id: Refusal trace ID
        
        Returns:
            List of all events (submission, reviews) for this trace_id
        """
        history = []
        
        if not self.appeal_log_path.exists():
            return history
        
        with open(self.appeal_log_path) as f:
            for line in f:
                data = json.loads(line)
                if data.get("trace_id") == trace_id:
                    history.append(data)
        
        return history
