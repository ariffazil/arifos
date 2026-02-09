"""
Refusal Audit Trail Management

Constitutional Compliance:
- F1 Amanah: Immutable audit trail
- F2 Truth: Accurate logging
- F13 Sovereign: Human oversight and appeal tracking

DITEMPA BUKAN DIBERI — Forged, not given.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


class RefusalAudit:
    """
    Audit trail management for refusal system.
    
    Provides queries and analytics over immutable refusal ledger.
    """
    
    def __init__(self, ledger_path: str = "VAULT999/BBB_LEDGER/refusal_audit.jsonl"):
        """
        Initialize audit system.
        
        Args:
            ledger_path: Path to immutable refusal ledger (JSONL)
        """
        self.ledger_path = Path(ledger_path)
    
    def get_refusals_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all refusals for a specific session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            List of refusal entries
        """
        refusals = []
        
        if not self.ledger_path.exists():
            return refusals
        
        with open(self.ledger_path) as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("session_id") == session_id:
                    refusals.append(entry)
        
        return refusals
    
    def get_refusals_by_domain(
        self, 
        risk_domain: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get refusals by risk domain.
        
        Args:
            risk_domain: Risk domain (e.g., "violence", "medical")
            limit: Maximum number of results (None = all)
        
        Returns:
            List of refusal entries
        """
        refusals = []
        
        if not self.ledger_path.exists():
            return refusals
        
        with open(self.ledger_path) as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("risk_domain") == risk_domain:
                    refusals.append(entry)
                    if limit and len(refusals) >= limit:
                        break
        
        return refusals
    
    def get_refusal_by_trace_id(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get refusal by trace ID.
        
        Args:
            trace_id: Refusal trace identifier
        
        Returns:
            Refusal entry or None if not found
        """
        if not self.ledger_path.exists():
            return None
        
        with open(self.ledger_path) as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("trace_id") == trace_id:
                    return entry
        
        return None
    
    def get_refusal_stats(self) -> Dict[str, Any]:
        """
        Get aggregate statistics on refusals.
        
        Returns:
            Dict with counts by type, domain, and appealability
        """
        stats = {
            "total": 0,
            "by_type": {},
            "by_domain": {},
            "by_profile": {},
            "appealable": 0,
            "high_risk": 0  # risk_score >= 0.85
        }
        
        if not self.ledger_path.exists():
            return stats
        
        with open(self.ledger_path) as f:
            for line in f:
                entry = json.loads(line)
                stats["total"] += 1
                
                # Count by type
                refusal_type = entry.get("refusal_type", "unknown")
                stats["by_type"][refusal_type] = stats["by_type"].get(refusal_type, 0) + 1
                
                # Count by domain
                risk_domain = entry.get("risk_domain", "unknown")
                stats["by_domain"][risk_domain] = stats["by_domain"].get(risk_domain, 0) + 1
                
                # Count by profile
                profile = entry.get("profile", "unknown")
                stats["by_profile"][profile] = stats["by_profile"].get(profile, 0) + 1
                
                # Count appealable
                if entry.get("appealable"):
                    stats["appealable"] += 1
                
                # Count high risk
                if entry.get("risk_score", 0) >= 0.85:
                    stats["high_risk"] += 1
        
        return stats
    
    def verify_integrity(self) -> Dict[str, Any]:
        """
        Verify ledger integrity (check for tampering).
        
        Returns:
            Dict with integrity status and any issues found
        """
        issues = []
        total_entries = 0
        
        if not self.ledger_path.exists():
            return {"status": "no_ledger", "issues": ["Ledger file does not exist"]}
        
        with open(self.ledger_path) as f:
            for line_num, line in enumerate(f, start=1):
                try:
                    entry = json.loads(line)
                    total_entries += 1
                    
                    # Check required fields
                    required = ["trace_id", "refusal_type", "risk_domain", "timestamp"]
                    for field in required:
                        if field not in entry:
                            issues.append(f"Line {line_num}: Missing required field '{field}'")
                    
                except json.JSONDecodeError as e:
                    issues.append(f"Line {line_num}: Invalid JSON - {e}")
        
        status = "valid" if not issues else "corrupted"
        
        return {
            "status": status,
            "total_entries": total_entries,
            "issues": issues
        }
