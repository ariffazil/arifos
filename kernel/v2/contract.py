"""
Critical Fix 2: Execution/Governance Contract Separation
═══════════════════════════════════════════════════════════════════════════════

Every tool response must expose four top-level statuses:
1. execution_status: SUCCESS | ERROR | TIMEOUT
2. governance_verdict: SEAL | SABAR | HOLD | VOID
3. artifact_state: USABLE | PARTIAL | STAGED | REJECTED
4. continue_allowed: true | false
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    DRY_RUN = "DRY_RUN"

class GovernanceVerdict(str, Enum):
    SEAL = "SEAL"
    SABAR = "SABAR"
    HOLD = "HOLD"
    VOID = "VOID"
    PROVISIONAL = "PROVISIONAL"

class ArtifactState(str, Enum):
    USABLE = "USABLE"
    PARTIAL = "PARTIAL"
    STAGED = "STAGED"
    REJECTED = "REJECTED"
    EMPTY = "EMPTY"

@dataclass
class ExecutionGovernanceContract:
    execution_status: ExecutionStatus
    governance_verdict: GovernanceVerdict
    artifact_state: ArtifactState
    continue_allowed: bool
    message: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_status": self.execution_status.value,
            "governance_verdict": self.governance_verdict.value,
            "artifact_state": self.artifact_state.value,
            "continue_allowed": self.continue_allowed,
            "message": self.message,
        }

    @classmethod
    def success_seal(cls, message: str = "Approved") -> "ExecutionGovernanceContract":
        return cls(ExecutionStatus.SUCCESS, GovernanceVerdict.SEAL, ArtifactState.USABLE, True, message)
