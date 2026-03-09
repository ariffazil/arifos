#!/usr/bin/env python3
"""
E2E Test for eureka_forge
Tests constitutional governance, workspace boundaries, and risk classification.

Run: python test_eureka_forge_e2e.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Set test environment
os.environ["ARIFOS_WORKDIR"] = str(Path.cwd() / "test_workspace")
os.environ["ARIFOS_PUBLIC_APPROVAL_MODE"] = "true"

# Create test workspace
test_workspace = Path.cwd() / "test_workspace"
test_workspace.mkdir(exist_ok=True)

from arifosmcp.runtime.server import eureka_forge, anchor_session, DEFAULT_WORKDIR

print("=" * 70)
print("EUREKA FORGE E2E CONSTITUTIONAL TEST")
print("=" * 70)
print(f"DEFAULT_WORKDIR: {DEFAULT_WORKDIR}")
print(f"Test workspace: {test_workspace}")
print()


async def test_case(name, coro, expected_verdict=None):
    """Run a test case and report results."""
    print(f"\n{'─' * 70}")
    print(f"TEST: {name}")
    print("─" * 70)

    try:
        result = await coro

        # Handle different response structures
        if isinstance(result, dict):
            if "verdict" in result:
                verdict = result["verdict"]
            elif isinstance(result.get("content"), list) and len(result["content"]) > 0:
                # MCP response format
                text = result["content"][0].get("text", "{}")
                try:
                    import json

                    inner = json.loads(text)
                    verdict = inner.get("verdict", "UNKNOWN")
                except:
                    verdict = "UNKNOWN"
            else:
                verdict = "UNKNOWN"
        else:
            verdict = "UNKNOWN"

        print(f"  Verdict: {verdict}")

        if "error" in str(result):
            print(f"  Result: {result}")

        if expected_verdict and verdict != expected_verdict:
            print(f"  ⚠️  EXPECTED {expected_verdict}, GOT {verdict}")
            return False

        print(f"  ✅ PASS")
        return True

    except Exception as e:
        print(f"  ❌ EXCEPTION: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run all E2E tests."""

    results = []

    # Test 0: Create session first (required for all other tests)
    print("\n" + "=" * 70)
    print("SETUP: Creating constitutional session")
    print("=" * 70)

    session_result = await anchor_session(
        query="Test session for eureka_forge E2E",
        actor_id="test_agent",
    )

    # Extract session_id from result
    if isinstance(session_result, dict):
        if "session_id" in session_result:
            session_id = session_result["session_id"]
        elif isinstance(session_result.get("content"), list):
            import json

            try:
                inner = json.loads(session_result["content"][0]["text"])
                session_id = inner.get("session_id", "test-session-fallback")
            except:
                session_id = "test-session-fallback"
        else:
            session_id = "test-session-fallback"
    else:
        session_id = "test-session-fallback"

    print(f"  Session ID: {session_id}")

    # Test 1: Workspace boundary violation (F1 Amanah)
    results.append(
        await test_case(
            "F1 Amanah - Workspace Escape Blocked",
            eureka_forge(
                session_id=session_id,
                command="ls -la",
                working_dir="/etc",  # Outside workspace
                actor_id="test_agent",
                purpose="Test workspace boundary",
            ),
            expected_verdict="VOID",
        )
    )

    # Test 2: Safe command in workspace
    results.append(
        await test_case(
            "F5 Peace² - Safe Command (LOW risk)",
            eureka_forge(
                session_id=session_id,
                command="echo 'hello from eureka_forge'",
                working_dir=str(test_workspace),
                actor_id="test_agent",
                purpose="Test safe execution",
            ),
            expected_verdict="SEAL",
        )
    )

    # Test 3: File creation
    results.append(
        await test_case(
            "File Creation - Write to workspace",
            eureka_forge(
                session_id=session_id,
                command=f"echo 'test content' > test_file.txt && cat test_file.txt",
                working_dir=str(test_workspace),
                actor_id="test_agent",
                purpose="Test file creation",
            ),
            expected_verdict="SEAL",
        )
    )

    # Test 4: CRITICAL command without confirmation
    results.append(
        await test_case(
            "F1 Amanah - CRITICAL command blocked (no confirm)",
            eureka_forge(
                session_id=session_id,
                command="rm -rf /tmp/test",
                working_dir=str(test_workspace),
                actor_id="test_agent",
                purpose="Test critical blocking",
            ),
            expected_verdict="888_HOLD",
        )
    )

    # Test 5: CRITICAL command WITH confirmation
    results.append(
        await test_case(
            "F1 Amanah - CRITICAL command with confirm",
            eureka_forge(
                session_id=session_id,
                command="rm -rf test_file.txt",  # Clean up
                working_dir=str(test_workspace),
                actor_id="test_agent",
                purpose="Test critical with confirmation",
                confirm_dangerous=True,
            ),
            expected_verdict="SEAL",
        )
    )

    # Test 6: Directory listing
    results.append(
        await test_case(
            "F9 Transparency - Directory inspection",
            eureka_forge(
                session_id=session_id,
                command="ls -la",
                working_dir=str(test_workspace),
                actor_id="test_agent",
                purpose="Test directory listing",
            ),
            expected_verdict="SEAL",
        )
    )

    # Test 7: Invalid command (should error but not crash)
    results.append(
        await test_case(
            "Error Handling - Invalid command",
            eureka_forge(
                session_id=session_id,
                command="this_command_does_not_exist_12345",
                working_dir=str(test_workspace),
                actor_id="test_agent",
                purpose="Test error handling",
            ),
            expected_verdict="VOID",  # Non-zero exit = VOID
        )
    )

    # Test 8: Path traversal attempt
    results.append(
        await test_case(
            "F12 Defense - Path Traversal Blocked",
            eureka_forge(
                session_id=session_id,
                command="cat /etc/passwd",
                working_dir=str(test_workspace) + "/../../etc",  # Traversal attempt
                actor_id="test_agent",
                purpose="Test path traversal protection",
            ),
            expected_verdict="VOID",
        )
    )

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("🎉 ALL TESTS PASSED - eureka_forge is constitutional!")
        return 0
    else:
        print(f"⚠️  {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
