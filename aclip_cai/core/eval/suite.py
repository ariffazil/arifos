from pathlib import Path

from aaa_mcp.server import _agi_cognition, _apex_verdict, _init_session

from .datasets import load_golden_dataset
from .evaluators import llm_as_judge
from .reporters import generate_html_report


# We provide a dispatcher for the tools
async def dispatch_tool(tool_name: str, **kwargs):
    tools = {
        "init_session": _init_session,
        "agi_cognition": _agi_cognition,
        "apex_verdict": _apex_verdict,
    }
    tool_func = tools.get(tool_name)
    if not tool_func:
        raise ValueError(f"Tool {tool_name} not available in dispatch mapping")
    return await tool_func(**kwargs)


class ConstitutionalEvalSuite:
    """
    ArifOS-native LangSmith Alternative.
    Evaluates historical inputs mapped against constitutional outcomes.
    """

    def __init__(self, golden_dir: str = "tests/mcp_live/golden"):
        self.golden_dir = Path(golden_dir)
        self.results = []

    async def run_all(self, kernel) -> list[dict]:
        # Search root directory and subdirectories
        dataset = load_golden_dataset(self.golden_dir)
        for category in ["governance", "triad", "sensory", "pipeline"]:
            dataset.extend(load_golden_dataset(self.golden_dir / category))

        for case in dataset:
            result = await self._run_case(kernel, case)
            self.results.append(result)

        return self.results

    async def _run_case(self, kernel, case: dict) -> dict:
        expected = case.get("expected_verdict", "SEAL")

        # Determine the tool to use
        input_spec = case.get("input", {})
        tool_name = input_spec.get("tool", "agi_cognition")

        if "input_prompt" in case:
            # Polygraph mode - routing everything through the mind (agi_cognition)
            tool_name = "agi_cognition"
            arguments = {
                "query": case.get("input_prompt", ""),
                "session_id": f"eval-{case.get('name', 'test')}",
                "grounding": [],
                "capability_modules": [],
                "debug": True,
            }
        else:
            arguments = input_spec.get("arguments", {})

        # 1. Execute the mapped tool
        try:
            tool_result = await dispatch_tool(tool_name, **arguments)
        except Exception as e:
            tool_result = {"error": str(e)}

        # 2. Constitutional Check
        # Some tools fail correctly and return VOID, others return {"verdict": ...}
        audit = kernel.auditor.check_floors(
            tool_name, context=str(tool_result), severity=case.get("severity", "medium")
        )

        # For our purposes, if the dataset expects a specific verdict and the tool returned it internally, we should honor it.
        tool_internal_verdict = (
            tool_result.get("verdict", "") if isinstance(tool_result, dict) else ""
        )
        final_verdict = audit.verdict.name if hasattr(audit.verdict, "name") else str(audit.verdict)

        if tool_internal_verdict in ["VOID", "SABAR", "HOLD", "HOLD_888", "EMERGED"]:
            final_verdict = tool_internal_verdict
        elif "Emergence Event" in str(tool_result):
            final_verdict = "EMERGED"

        thermo = kernel.thermo.snapshot(f"eval-{case.get('name')}")

        # 3. LLM-as-judge eval
        judge_score = await llm_as_judge(case.get("description", ""), tool_result)

        passed_const = final_verdict == expected

        return {
            "case_id": f"[{case.get('floor', 'F?')}] {case.get('name', 'UNKNOWN')}",
            "verdict": final_verdict,
            "floor_scores": {
                k: getattr(v, "score", 0.0) for k, v in getattr(audit, "floor_results", {}).items()
            },
            "genius": getattr(thermo, "genius", 0.0),
            "delta_s": getattr(thermo, "delta_s", 0.0),
            "passed_const": passed_const,
            "judge_score": judge_score,
            "raw_output": str(tool_result)[:250],
        }

    def report(self, output_path: str = "test-reports/arifos-eval-report.html"):
        generate_html_report(self.results, output_path)
