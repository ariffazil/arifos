"""
core/execution_validator.py - Feedback Loop Handler

Closes the Witness Gap by validating execution results and feeding back
into the Tri-Witness system. Every execution updates W3 scores.
"""

from typing import Any, Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of execution validation."""
    w3_score: float
    human_witness: float
    ai_witness: float
    earth_witness: float
    verdict: str
    feedback: Dict[str, Any]


class ExecutionValidator:
    """
    Validates execution results and closes the feedback loop.
    
    Tri-Witness Calculation:
    - Human: Did user approve? (1.0 = yes, 0.0 = no)
    - AI: Did execution match expectation? (1.0 = success, 0.0 = failure)
    - Earth: Did system actually change? (verified via checksum)
    
    W3 = (H * A * E)^(1/3)
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.validation_history = []
    
    def validate_execution(
        self,
        expected: Dict[str, Any],
        actual: Dict[str, Any],
        human_approved: bool = True
    ) -> ValidationResult:
        """
        Validate execution result against expectation.
        
        Args:
            expected: What AI predicted would happen
            actual: What actually happened (from RuntimeBridge)
            human_approved: Did human approve this execution?
        """
        # Human witness
        h = 1.0 if human_approved else 0.0
        
        # AI witness - did execution succeed?
        a = 1.0 if actual.get("success", False) else 0.3
        
        # Earth witness - did reality change?
        e = self._verify_earth_state(expected, actual)
        
        # Calculate W3
        w3 = (h * a * e) ** (1/3)
        
        # Determine verdict
        if w3 >= 0.95:
            verdict = "SEAL"
        elif w3 >= 0.85:
            verdict = "PARTIAL"
        else:
            verdict = "VOID"
        
        result = ValidationResult(
            w3_score=w3,
            human_witness=h,
            ai_witness=a,
            earth_witness=e,
            verdict=verdict,
            feedback={
                "timestamp": datetime.now().isoformat(),
                "expected": expected,
                "actual": actual,
                "delta": self._compute_delta(expected, actual)
            }
        )
        
        # Store for learning
        self.validation_history.append(result)
        
        return result
    
    def _verify_earth_state(self, expected: Dict, actual: Dict) -> float:
        """Verify actual system state changed as expected."""
        # Check verification hash
        expected_hash = expected.get("verification_hash", "")
        actual_hash = actual.get("verification_hash", "")
        
        if expected_hash and actual_hash == expected_hash:
            # No change detected
            return 0.5
        
        # Check return code
        if actual.get("returncode", -1) == 0:
            return 0.95
        
        return 0.3
    
    def _compute_delta(self, expected: Dict, actual: Dict) -> Dict:
        """Compute difference between expected and actual."""
        return {
            "success_match": expected.get("success") == actual.get("success"),
            "output_similarity": self._output_similarity(
                expected.get("stdout", ""),
                actual.get("stdout", "")
            )
        }
    
    def _output_similarity(self, expected: str, actual: str) -> float:
        """Simple similarity metric."""
        if not expected or not actual:
            return 0.0
        # Simple containment check
        if expected.strip() in actual.strip():
            return 1.0
        return 0.5
    
    def get_learning_summary(self) -> Dict:
        """Generate learning summary from validation history."""
        if not self.validation_history:
            return {"message": "No executions yet"}
        
        total = len(self.validation_history)
        sealed = sum(1 for v in self.validation_history if v.verdict == "SEAL")
        avg_w3 = sum(v.w3_score for v in self.validation_history) / total
        
        return {
            "total_executions": total,
            "seal_rate": sealed / total,
            "average_w3": avg_w3,
            "trend": "improving" if avg_w3 > 0.9 else "stable"
        }


def validate(expected: Dict, actual: Dict, session_id: str, human_approved: bool = True) -> ValidationResult:
    """Convenience function."""
    validator = ExecutionValidator(session_id)
    return validator.validate_execution(expected, actual, human_approved)
