"""
constitutional-check skill handler
F3 Tri-Witness consensus evaluation.
"""

from typing import Any, Dict
from core.intelligence import compute_w3


class ConstitutionalCheckSkill:
    """Skill for constitutional verification with F3."""
    
    NAME = "constitutional-check"
    FLOOR = "F3"
    
    async def evaluate_proposal(
        self,
        human_score: float,
        ai_score: float,
        earth_score: float
    ) -> Dict[str, Any]:
        """Evaluate proposal with Tri-Witness."""
        w3 = compute_w3(human_score, ai_score, earth_score)
        
        verdicts = {
            (True, True, True): "SEAL",
            (True, True, False): "SABAR",
            (True, False, True): "HOLD",
            (False, True, True): "PARTIAL",
        }
        
        key = (w3 >= 0.95, ai_score >= 0.9, earth_score >= 0.9)
        verdict = verdicts.get(key, "VOID")
        
        return {
            "verdict": verdict,
            "w3_score": w3,
            "witnesses": {
                "human": human_score,
                "ai": ai_score,
                "earth": earth_score
            },
            "threshold": 0.95,
            "passed": w3 >= 0.95
        }


async def execute(action: str, params: Dict[str, Any], session_id: str, dry_run: bool = True):
    """Main entry point."""
    skill = ConstitutionalCheckSkill()
    
    if action == "evaluate_proposal":
        return await skill.evaluate_proposal(
            params.get("human_score", 0),
            params.get("ai_score", 0),
            params.get("earth_score", 0)
        )
    
    return {"verdict": "VOID", "reason": f"Unknown action: {action}"}
