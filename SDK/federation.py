"""
arifOS L5: Agent Federation
===========================
Orchestrates the 4-agent constitutional federation.

Flow:
    User Query → Architect → Engineer → Auditor → Validator → Sealed Output
                 (plan)      (execute)  (audit)   (consensus)

Current Status (v55.3-L5-alpha):
- Architect: ✅ WORKING
- Engineer: 🔴 STUB
- Auditor: 🔴 STUB  
- Validator: 🔴 STUB

For full federation, use architect_only() method.
Full federation coming in v55.4.

Version: v55.3-L5-alpha
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
"""

from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .base_agent import Verdict, AgentOutput, FloorScores
from .architect import Architect, ArchitectPlan
from .engineer import Engineer
from .auditor import Auditor
from .validator import Validator


@dataclass
class FederationResult:
    """Result from federation execution."""
    query: str
    plan: Optional[ArchitectPlan]
    architect_output: Optional[AgentOutput]
    engineer_output: Optional[AgentOutput]
    auditor_output: Optional[AgentOutput]
    validator_output: Optional[AgentOutput]
    final_verdict: Verdict
    final_response: any
    execution_path: list[str]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "plan": self.plan.to_dict() if self.plan else None,
            "architect_output": self.architect_output.to_dict() if self.architect_output else None,
            "engineer_output": self.engineer_output.to_dict() if self.engineer_output else None,
            "auditor_output": self.auditor_output.to_dict() if self.auditor_output else None,
            "validator_output": self.validator_output.to_dict() if self.validator_output else None,
            "final_verdict": self.final_verdict.value,
            "final_response": str(self.final_response),
            "execution_path": self.execution_path,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentFederation:
    """
    4-Agent Constitutional Federation
    ==================================
    
    Orchestrates Architect → Engineer → Auditor → Validator pipeline.
    
    Current Status (v55.3):
    - Full federation: 🔴 NOT AVAILABLE (Engineer/Auditor/Validator are stubs)
    - Architect only: ✅ WORKING
    
    Usage:
        federation = AgentFederation()
        
        # Full federation (coming v55.4)
        # result = await federation.execute(query)
        
        # Architect only (working now)
        result = await federation.architect_only(query)
    
    The federation ensures:
    - Every step is constitutionally governed
    - Tri-Witness consensus before final output
    - Audit trail in VAULT-999
    - Human can override at any point (F13 Sovereign)
    """
    
    def __init__(self, tri_witness_threshold: float = 0.95):
        """
        Initialize the federation.
        
        Args:
            tri_witness_threshold: Minimum W₃ for consensus (default 0.95)
        """
        self.architect = Architect()
        self.engineer = Engineer()
        self.auditor = Auditor()
        self.validator = Validator()
        self.tri_witness_threshold = tri_witness_threshold
    
    async def architect_only(self, query: str, context: dict = None) -> FederationResult:
        """
        Execute only the Architect agent (working in v55.3).
        
        Returns a plan without full federation execution.
        
        Args:
            query: User query
            context: Optional additional context
            
        Returns:
            FederationResult with plan but no execution
        """
        input_data = {"query": query, "context": context or {}}
        
        # Run Architect
        architect_output = await self.architect.governed_process(input_data)
        
        # Extract plan if successful
        plan = None
        if architect_output.verdict in [Verdict.SEAL, Verdict.PARTIAL]:
            if isinstance(architect_output.response, dict):
                plan = architect_output.response.get("response")
            elif isinstance(architect_output.response, ArchitectPlan):
                plan = architect_output.response
        
        return FederationResult(
            query=query,
            plan=plan,
            architect_output=architect_output,
            engineer_output=None,
            auditor_output=None,
            validator_output=None,
            final_verdict=architect_output.verdict,
            final_response=plan,
            execution_path=["Architect"],
        )
    
    async def execute(
        self,
        query: str,
        context: dict = None,
        human_override: bool = False
    ) -> FederationResult:
        """
        Execute full 4-agent federation.
        
        ⚠️ NOT FULLY IMPLEMENTED IN v55.3
        
        Currently only Architect works.
        Engineer, Auditor, Validator will raise NotImplementedError.
        
        For v55.3, use architect_only() instead.
        
        Args:
            query: User query
            context: Optional additional context
            human_override: If True, skip to human review (F13)
            
        Returns:
            FederationResult with full execution trace
        """
        input_data = {"query": query, "context": context or {}}
        execution_path = []
        
        # Stage 1: Architect
        execution_path.append("Architect")
        architect_output = await self.architect.governed_process(input_data)
        
        if architect_output.verdict == Verdict.VOID:
            return FederationResult(
                query=query,
                plan=None,
                architect_output=architect_output,
                engineer_output=None,
                auditor_output=None,
                validator_output=None,
                final_verdict=Verdict.VOID,
                final_response=None,
                execution_path=execution_path,
            )
        
        # Extract plan
        plan = None
        if isinstance(architect_output.response, dict):
            plan = architect_output.response.get("response")
        
        # Check if human review required
        if plan and plan.requires_human_review and not human_override:
            return FederationResult(
                query=query,
                plan=plan,
                architect_output=architect_output,
                engineer_output=None,
                auditor_output=None,
                validator_output=None,
                final_verdict=Verdict.HOLD_888,
                final_response="F13 Sovereign: Human review required",
                execution_path=execution_path,
            )
        
        # Stage 2: Engineer (STUB - will raise)
        execution_path.append("Engineer")
        try:
            engineer_input = {
                "query": query,
                "plan": plan.to_dict() if plan else {},
                "context": context or {},
            }
            engineer_output = await self.engineer.governed_process(engineer_input)
        except NotImplementedError as e:
            # Return partial result with error
            return FederationResult(
                query=query,
                plan=plan,
                architect_output=architect_output,
                engineer_output=None,
                auditor_output=None,
                validator_output=None,
                final_verdict=Verdict.HOLD_888,
                final_response=f"Federation incomplete: {str(e)}",
                execution_path=execution_path,
            )
        
        # Stage 3: Auditor (STUB - will raise)
        execution_path.append("Auditor")
        try:
            auditor_input = {
                "query": query,
                "plan": plan.to_dict() if plan else {},
                "engineer_result": engineer_output.to_dict(),
            }
            auditor_output = await self.auditor.governed_process(auditor_input)
        except NotImplementedError as e:
            return FederationResult(
                query=query,
                plan=plan,
                architect_output=architect_output,
                engineer_output=engineer_output,
                auditor_output=None,
                validator_output=None,
                final_verdict=Verdict.HOLD_888,
                final_response=f"Federation incomplete: {str(e)}",
                execution_path=execution_path,
            )
        
        # Stage 4: Validator (STUB - will raise)
        execution_path.append("Validator")
        try:
            validator_input = {
                "query": query,
                "audit_report": auditor_output.to_dict(),
                "tri_witness_threshold": self.tri_witness_threshold,
            }
            validator_output = await self.validator.governed_process(validator_input)
        except NotImplementedError as e:
            return FederationResult(
                query=query,
                plan=plan,
                architect_output=architect_output,
                engineer_output=engineer_output,
                auditor_output=auditor_output,
                validator_output=None,
                final_verdict=Verdict.HOLD_888,
                final_response=f"Federation incomplete: {str(e)}",
                execution_path=execution_path,
            )
        
        # Full federation complete
        return FederationResult(
            query=query,
            plan=plan,
            architect_output=architect_output,
            engineer_output=engineer_output,
            auditor_output=auditor_output,
            validator_output=validator_output,
            final_verdict=validator_output.verdict,
            final_response=validator_output.response,
            execution_path=execution_path,
        )


__all__ = ["AgentFederation", "FederationResult"]
