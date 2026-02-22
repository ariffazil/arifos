"""
aaa_mcp/tools/manifold_adapter.py — Prompt Manifold MCP Integration

Integrates the 3×3 paradox-motto matrix with MCP tools for empirical testing.

Usage:
    # In any MCP tool, wrap output with manifold framing
    from aaa_mcp.tools.manifold_adapter import ManifoldMCPAdapter

    adapter = ManifoldMCPAdapter()
    result = adapter.wrap_output("333_REASON", raw_result, task="Explain X")
"""

from typing import Dict, Any
from core.shared.mottos import PromptManifold, get_motto_for_stage


class ManifoldMCPAdapter:
    """
    Adapter for integrating Prompt Manifold with MCP tool outputs.

    This adds the 3×3 matrix framing and validation to all MCP tool responses,
    enabling empirical measurement of the manifold's effects.
    """

    def __init__(self):
        self.manifold = PromptManifold()

    def wrap_output(
        self,
        stage: str,
        output: Dict[str, Any],
        task: str = "",
        validate: bool = True,
    ) -> Dict[str, Any]:
        """
        Wrap an MCP tool output with manifold framing.

        Args:
            stage: The 000-999 stage code
            output: The raw tool output
            task: Description of the task being performed
            validate: Whether to run validation checks

        Returns:
            Enhanced output with manifold framing
        """
        # Get matrix cell for this stage
        cell = self.manifold.get_by_stage(stage)
        motto = get_motto_for_stage(stage)

        # Build manifold metadata
        manifold_meta = {
            "stage": stage,
            "motto": str(motto),
            "motto_positive": motto.positive,
            "motto_negative": motto.negative,
            "meaning": motto.meaning,
        }

        if cell:
            manifold_meta.update(
                {
                    "matrix_row": cell.row.value,
                    "matrix_col": cell.col.value,
                    "geometry": cell.geometry.value,
                    "constraint": cell.constraint,
                }
            )

        manifold_meta["omega_0"] = self.manifold.omega_0

        # Validate if requested
        if validate and "text" in output:
            validation = self.manifold.validate_output(stage, output["text"])
            manifold_meta["validation"] = {
                "adherence_score": validation["adherence_score"],
                "violations": validation["violations"],
                "suggestions": validation["suggestions"],
            }

        # Merge with output
        wrapped = {
            **output,
            "manifold": manifold_meta,
        }

        return wrapped

    def get_prompt_prefix(self, stage: str, task: str = "") -> str:
        """
        Get a prompt prefix for framing LLM inputs.

        This can be prepended to any user query to guide the model
        through the 3×3 matrix constraints.
        """
        return self.manifold.get_prompt_frame(stage, task)

    def audit_compliance(
        self,
        session_id: str,
        outputs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Audit compliance across all stages of a session.

        Args:
            session_id: The session identifier
            outputs: Dict mapping stage -> output for that stage

        Returns:
            Compliance report with aggregate metrics
        """
        scores = []
        violations = []

        for stage, output in outputs.items():
            if "text" in output:
                validation = self.manifold.validate_output(stage, output["text"])
                scores.append(validation["adherence_score"])
                violations.extend(validation["violations"])

        avg_score = sum(scores) / len(scores) if scores else 0.0

        return {
            "session_id": session_id,
            "compliance_score": avg_score,
            "stages_evaluated": len(scores),
            "violations": violations,
            "omega_0": self.manifold.omega_0,
            "meets_threshold": avg_score >= 0.8,
        }


# ═════════════════════════════════════════════════════════════════════════════
# STAGE-SPECIFIC ADAPTERS
# ═════════════════════════════════════════════════════════════════════════════


def wrap_agi_sense(output: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap AGI SENSE output with manifold framing."""
    adapter = ManifoldMCPAdapter()
    return adapter.wrap_output("111_SENSE", output, task="Classify intent")


def wrap_agi_think(output: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap AGI THINK output with manifold framing."""
    adapter = ManifoldMCPAdapter()
    return adapter.wrap_output("222_THINK", output, task="Generate hypotheses")


def wrap_agi_reason(output: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap AGI REASON output with manifold framing."""
    adapter = ManifoldMCPAdapter()
    return adapter.wrap_output("333_REASON", output, task="Logical deduction")


def wrap_asi_empathize(output: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap ASI EMPATHIZE output with manifold framing."""
    adapter = ManifoldMCPAdapter()
    return adapter.wrap_output("555_EMPATHY", output, task="Stakeholder analysis")


def wrap_asi_align(output: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap ASI ALIGN output with manifold framing."""
    adapter = ManifoldMCPAdapter()
    return adapter.wrap_output("666_ALIGN", output, task="Safety alignment")


def wrap_apex_verdict(output: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap APEX VERDICT output with manifold framing."""
    adapter = ManifoldMCPAdapter()
    return adapter.wrap_output("888_JUDGE", output, task="Final judgment")


# ═════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═════════════════════════════════════════════════════════════════════════════

__all__ = [
    "ManifoldMCPAdapter",
    "wrap_agi_sense",
    "wrap_agi_think",
    "wrap_agi_reason",
    "wrap_asi_empathize",
    "wrap_asi_align",
    "wrap_apex_verdict",
]
