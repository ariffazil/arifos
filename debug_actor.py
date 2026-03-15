
import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

from arifosmcp.runtime.tools import init_anchor_state, arifos_kernel

async def test():
    # Set OPEN MODE for testing
    os.environ["ARIFOS_GOVERNANCE_OPEN_MODE"] = "true"
    
    print("Testing init_anchor_state with chat-operator...")
    env = await init_anchor_state(declared_name="chat-operator", query="I am chat-operator")
    
    print(f"Init OK: {env.ok}")
    if env.auth_context:
        print(f"Init Auth Context Actor ID: {env.auth_context.get('actor_id')}")
    print(f"Init Authority Actor ID: {env.authority.actor_id}")

    if not env.auth_context:
        print("Failed to get auth_context from init")
        return

    # Promote to declared
    env.auth_context["authority_level"] = "declared"
    env.auth_context["authority"] = {"level": "declared", "actor_id": "chat-operator"}
    
    print("\nTesting arifos_kernel with continuity...")
    # Simulate the nesting done in the test
    nested_ctx = {
        "continuity": {
            "actor_id": "chat-operator",
            "method": "minted_auth_context",
        }
    }
    
    env2 = await arifos_kernel(
        query="Explain the runtime continuity posture.",
        actor_id="chat-operator",
        auth_context=nested_ctx,
        risk_tier="low",
        dry_run=True,
        session_id="test-session"
    )
    
    print(f"Kernel OK: {env2.ok}")
    if env2.auth_context:
        print(f"Kernel Auth Context Actor ID: {env2.auth_context.get('actor_id')}")
    print(f"Kernel Authority Actor ID: {env2.authority.actor_id}")

if __name__ == "__main__":
    asyncio.run(test())
