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
    
    Metrics for tuning equilibrium:
    - refusal_overturned_rate: Indicates thresholds may be too strict
    - appeal_rate_by_domain: Shows where social survivability is breaking
    
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
        
        # Get metrics for threshold tuning
        metrics = appeal_system.get_appeal_metrics()
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
    
    def get_appeal_metrics(self) -> Dict[str, Any]:
        """
        Get metrics for tuning equilibrium thresholds.
        
        Returns:
            Dict with:
            - total_appeals: Total number of appeals submitted
            - total_reviewed: Total number reviewed by humans
            - overturned_count: Number of OVERTURN decisions
            - uphold_count: Number of UPHOLD decisions
            - refusal_overturned_rate: Percentage of appeals that were overturned
            - appeal_rate_by_domain: Count of appeals per risk domain
            - pending_count: Current pending appeals
        
        These metrics enable data-driven threshold adjustment:
        - High overturn rate → thresholds too strict
        - High appeal rate in specific domain → tune that domain
        """
        if not self.appeal_log_path.exists():
            return {
                "total_appeals": 0,
                "total_reviewed": 0,
                "overturned_count": 0,
                "uphold_count": 0,
                "refusal_overturned_rate": 0.0,
                "appeal_rate_by_domain": {},
                "pending_count": 0
            }
        
        total_appeals = 0
        overturned = 0
        uphold = 0
        by_domain = {}
        reviewed_ids = set()
        
        with open(self.appeal_log_path) as f:
            for line in f:
                data = json.loads(line)
                
                # Count submissions
                if data.get("status") == "PENDING":
                    total_appeals += 1
                    
                    # Track domain if available
                    domain = data.get("risk_domain", "unknown")
                    by_domain[domain] = by_domain.get(domain, 0) + 1
                
                # Count reviews
                elif data.get("action") == "human_review":
                    reviewed_ids.add(data["trace_id"])
                    
                    if data.get("status") == "OVERTURN":
                        overturned += 1
                    elif data.get("status") == "UPHOLD":
                        uphold += 1
        
        total_reviewed = overturned + uphold
        overturn_rate = (overturned / total_reviewed * 100) if total_reviewed > 0 else 0.0
        pending = total_appeals - len(reviewed_ids)
        
        return {
            "total_appeals": total_appeals,
            "total_reviewed": total_reviewed,
            "overturned_count": overturned,
            "uphold_count": uphold,
            "refusal_overturned_rate": round(overturn_rate, 2),
            "appeal_rate_by_domain": by_domain,
            "pending_count": pending
        }
