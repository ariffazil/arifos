import asyncio
import json
from arifosmcp.runtime.server import anchor_session, vector_memory, seal_vault, apex_judge


async def audit_amanah():
    print("🛡️ Starting Amanah Continuity Audit...")

    # 1. Start Session
    print("Step 1: Anchor Session")
    anch = await anchor_session(query="Amanah Audit", actor_id="auditor")
    session_token = anch.get("session_id")
    print(f"Session Token: {session_token}")

    # 2. Link a simulated thought
    print("\nStep 2: Vector Memory (Phoenix Organ)")
    vm = await vector_memory(query="Amanah audit trace", session_id=session_token)
    print(f"VM Tool session_id: {vm.get('session_id')}")
    assert vm.get("session_id") == session_token

    # 3. Apex Judge (Soul Organ)
    print("\nStep 3: Apex Judge (Soul Organ)")
    aj = await apex_judge(session_id=session_token, query="Audit complete", human_approve=True)
    print(f"Full Apex Judge Response: {json.dumps(aj, indent=2)}")
    gov_token = aj.get("governance_token")

    if aj.get("verdict") == "VOID":
        print(
            f"❌ AUDIT BLOCKED: Apex Judge returned VOID. Reason: {aj.get('laws_13', {}).get('failed_required')}"
        )
        return

    # 4. Seal Vault (Memory Organ)
    print("\nStep 4: Seal Vault (Final Seal)")
    sv = await seal_vault(
        session_id=session_token, summary="Audit sealed", governance_token=gov_token
    )
    print(f"Vault Status: {sv.get('verdict')}")
    assert sv.get("verdict") in {"SEAL", "PARTIAL"}

    print("\n✅ AMANAH AUDIT PASSED: Session continuity preserved across all organs.")


if __name__ == "__main__":
    asyncio.run(audit_amanah())
