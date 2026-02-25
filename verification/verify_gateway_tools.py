import asyncio

from aaa_mcp.server import (
    mcp,
)

# Import original functions for logic verification
# Import original functions for logic verification
from aaa_mcp.tools.mcp_gateway import gateway_list_tools, gateway_route_tool
from aaa_mcp.wrappers.k8s_wrapper import k8s_constitutional_apply


async def verify_gateway_tools():
    print("=" * 60)
    print("VERIFICATION: MCP Gateway Tools")
    print("=" * 60)

    # 1. Inspect Registered Tools via Server Object (Proof of Exposure)
    print("\n[1] Inspecting Registered Tools in 'mcp' object...")
    if hasattr(mcp, "_tool_manager") and hasattr(mcp._tool_manager, "_tools"):
        tool_names = list(mcp._tool_manager._tools.keys())
        print(f"Server Tool Names: {tool_names}")

        expected = [
            "_gateway_route_tool_wrapper",
            "_gateway_list_tools_wrapper",
            "_k8s_constitutional_apply_wrapper",
        ]
        for t in expected:
            if t in tool_names:
                print(f"  [OK] Found {t}")
            else:
                print(f"  [FAIL] Missing {t}")
    else:
        print("  [WARN] Could not access mcp._tool_manager")

    # 2. Verify gateway_list_tools (Logic)
    print("\n[2] Verifying gateway_list_tools logic...")
    try:
        tools = await gateway_list_tools()  # Call original function
        print(f"  Tools returned: {len(tools.get('servers', {}))}")
        print(f"  Gateway Version: {tools.get('version')}")
        if "gateway" in tools:
            print("  [OK] Gateway list structure valid")
        else:
            print("  [FAIL] Invalid gateway list structure")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

    # 3. Verify gateway_route_tool (Mocked Logic)
    print("\n[3] Verifying gateway_route_tool (Mock Payload)...")
    payload = {
        "manifest": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod",
        "namespace": "default",
    }

    try:
        # Call original function
        result = await gateway_route_tool(
            tool_name="k8s_apply",
            payload=payload,
            session_id="test-session-123",
            actor_id="verifier",
        )
        print("  Result Keys:", result.keys())
        if "gateway_decision" in result or "verdict" in result:
            verdict = result.get("verdict")
            print(f"  Gateway Verdict: {verdict}")
            if verdict in ["SEAL", "SABAR", "VOID", "888_HOLD"]:
                print("  [OK] Constitutional evaluation ran")
            else:
                print(f"  [FAIL] Unexpected verdict: {verdict}")
        else:
            print("  [FAIL] No verdict in response")

    except Exception as e:
        print(f"  [FAIL] Execution error: {e}")

    # 4. Verify k8s_constitutional_apply (Evaluation Mode Logic)
    print("\n[4] Verifying k8s_constitutional_apply (Evaluation)...")
    try:
        # Call original function
        k8s_result = await k8s_constitutional_apply(
            manifest="apiVersion: v1\nkind: Service\nmetadata:\n  name: test-svc",
            namespace="prod",
            session_id="test-session-456",
            dry_run=True,  # Should return evaluation without side effects
        )
        print("  Result Keys:", k8s_result.keys())

        if k8s_result.get("verdict") == "888_HOLD":
            print("  [OK] Correctly flagged PROD operation as 888_HOLD")
        elif k8s_result.get("verdict") == "SEAL":
            print("  [OK] Sealed")
        else:
            print(f"  Verdict: {k8s_result.get('verdict')}")

    except Exception as e:
        print(f"  [FAIL] Execution error: {e}")


if __name__ == "__main__":
    asyncio.run(verify_gateway_tools())
