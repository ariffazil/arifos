import asyncio
import json
from arifos_aaa_mcp.server import apex_judge

async def run_audit():
    # Simulate the APEX Judgment for the refactoring task
    result = await apex_judge(
        session_id="sess_20260306_refactor",
        query="Refactor AAA MCP metabolic loop to 11-stage canonical workflow and re-align migration docs.",
        agi_result={"verdict": "SEAL", "telemetry": {"dS": -1.34}},
        asi_result={"verdict": "SEAL", "telemetry": {"peace2": 1.20, "kappa_r": 0.99}},
        proposed_verdict="SEAL",
        debug=True
    )
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(run_audit())
