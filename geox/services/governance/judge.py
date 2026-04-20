from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional
from geox.shared.contracts.schemas import (
    Verdict, VerdictStatus, RiskAssessment, RiskFactor, 
    EvidenceObject, EvidenceKind
)
from services.geo_fabric.engine import fabric

class SovereignJudge:
    """
    The 888_JUDGE Implementation.
    Evaluates physical evidence against constitutional floors.
    """

    def evaluate_well_prospect_fit(
        self, 
        intent_id: str, 
        well_obj: EvidenceObject, 
        prospect_obj: EvidenceObject
    ) -> Verdict:
        """
        Evaluate if a well correctly targets a prospect.
        This is a 'Causal Loop' verification tool.
        """
        
        # 1. Project Trajectory if needed
        # (Assuming payload has head and survey)
        head = well_obj.payload["head"]
        survey = well_obj.payload["survey"]
        
        traj_points = fabric.project_well_trajectory(
            head_xy=(head["x"], head["y"]),
            md_points=survey["md"],
            incl_points=survey["inc"],
            azim_points=survey["azi"]
        )
        
        # 2. Check Prospect Boundary
        # (Assuming payload has boundary)
        boundary = prospect_obj.payload["boundary"]
        
        # Check if the terminal point (TD) is inside the prospect
        td_point = (traj_points[-1][0], traj_points[-1][1])
        is_inside = fabric.validate_constraint(td_point, boundary)
        
        # 3. Formulate Verdict
        verdict_id = f"V-{uuid4().hex[:8]}"
        risk_factors = []
        
        if is_inside:
            status = VerdictStatus.SEAL
            confidence = 0.95
            rationale = f"Well {well_obj.ref.id} TD correctly penetrates {prospect_obj.ref.id} bounds."
        else:
            status = VerdictStatus.HOLD_888
            confidence = 0.60
            rationale = f"Well {well_obj.ref.id} misses prospect {prospect_obj.ref.id} boundary at TD."
            risk_factors.append(RiskFactor(
                key="GEOMETRIC_MISS",
                impact=0.8,
                reason="Terminal well position is outside interpreted closure."
            ))

        return Verdict(
            verdictId=verdict_id,
            intentId=intent_id,
            status=status,
            confidence=confidence,
            author="888_JUDGE_KERNEL",
            rationale=rationale,
            risk=RiskAssessment(score=0.2 if is_inside else 0.8, factors=risk_factors),
            auditTraceId=f"TRACE-{uuid4().hex[:12]}",
            timestamp=datetime.now()
        )

# Global Access Instance
judge = SovereignJudge()
