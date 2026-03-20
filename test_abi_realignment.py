
import asyncio
import json
from arifosmcp.runtime.tools import init_anchor, get_caller_status

async def test_realigned_abi():
    print("--- Testing Structured Intent & Human Approval ---")
    intent_obj = {
        "query": "Validate the 11 functional quadrants",
        "domain": "engineering",
        "task_type": "audit",
        "desired_output": "system_health_report"
    }
    
    # This call previously failed on schema or didn't persist flags
    envelope = await init_anchor(
        actor_id="verifier-agent-01",
        intent=intent_obj,
        human_approval=True,
        session_id="realigned-session-001"
    )
    
    print(f"Status: {envelope.status}")
    print(f"Verdict: {envelope.verdict}")
    print(f"Human Approval Persisted: {envelope.payload.get('human_approval_persisted')}")
    print(f"Authority Human Required: {envelope.authority.human_required}")
    
    if envelope.philosophy:
        print("\n--- Philosophical Anchor (Emergence Check) ---")
        agi = envelope.philosophy.get('agi', {})
        print(f"Quote: \"{agi.get('quote')}\"")
        print(f"Author: {agi.get('author')}")
        print(f"Contrast Category: {agi.get('category')}")
    else:
        print("\nERROR: Philosophy is still NULL!")

    print("\n--- Testing Protected ID Hard Fail with Philosophy ---")
    protected_env = await init_anchor(
        actor_id="arif",
        intent="Sovereign Access",
        human_approval=False,
        session_id="protected-fail-001"
    )
    print(f"Protected Verdict: {protected_env.verdict}")
    if protected_env.philosophy:
        agi = protected_env.philosophy.get('agi', {})
        print(f"Humility Quote (F7): \"{agi.get('quote')}\" - {agi.get('author')}")

if __name__ == "__main__":
    asyncio.run(test_realigned_abi())
