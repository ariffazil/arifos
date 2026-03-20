
import asyncio
import uuid
import json
from arifosmcp.runtime.tools import init_anchor, arifOS_kernel
from arifosmcp.runtime.models import Verdict, ClaimStatus

async def test_closure():
    print("🧪 Starting Full Pipeline Closure Test (Operator-Grade)")
    
    session_id = f"test-closure-{uuid.uuid4().hex[:6]}"
    actor_id = "operator" # Recognized but non-sovereign
    
    # 1. 000 INIT
    print(f"\n[INIT] Anchoring session: {session_id} for {actor_id}")
    init_res = await init_anchor(
        actor_id=actor_id,
        intent={"query": "Test end-to-end closure", "task_type": "audit"},
        session_id=session_id,
        human_approval=True
    )
    
    print(f"Init Record: ok={init_res.ok}, status={init_res.status}, verdict={init_res.verdict}")
    print(f"Identity: claimed={init_res.payload.get('claimed_actor_id')}, resolved={init_res.payload.get('resolved_actor_id')}, status={init_res.payload.get('claim_status')}")
    
    if not init_res.ok or init_res.payload.get('claim_status') not in ["accepted", "verified", "anchored"]:
        print("❌ Init failed or identity not accepted correctly.")
        return

    # 2. 444 ROUTER -> 777 FORGE -> 888 JUDGE -> 999 VAULT
    print("\n[KERNEL] Executing governed task...")
    kernel_res = await arifOS_kernel(
        query="Analyze the consistency of F1-F13 floors and seal the audit trace in the vault.",
        intent={
            "query": "Analyze the consistency of F1-F13 floors and seal the audit trace in the vault.",
            "task_type": "audit",
            "domain": "governance"
        },
        session_id=session_id,
        risk_tier="low",
        allow_execution=True,
        dry_run=False
    )
    
    print(f"Kernel Result: ok={kernel_res.ok}, verdict={kernel_res.verdict}")
    print(f"Stage Trace: {json.dumps(kernel_res.trace, indent=2)}")
    
    # Check for 888-JUDGE and 999-VAULT in the trace
    stages = list(kernel_res.trace.keys())
    print(f"Stages reached: {stages}")
    
    if "888_JUDGE" in stages:
        print("✅ 888_JUDGE reached!")
    else:
        print("❌ 888_JUDGE NOT reached.")
        
    if "999_VAULT" in stages:
        print("✅ 999_VAULT reached!")
    else:
        print("❌ 999_VAULT NOT reached (expected if not sovereign or needs more steps).")

    if kernel_res.verdict == Verdict.SEAL:
        print("🔥 SUCCESS: Pipeline sealed end-to-end!")
    else:
        print(f"⚠️ Partial Success: Verdict is {kernel_res.verdict}")

if __name__ == "__main__":
    asyncio.run(test_closure())
