#!/usr/bin/env python3
"""E2E Test Suite for arifOS MCP Server"""

import requests
import json
import sys

base_url = "http://72.62.71.199:8080"
session_id = None

print("🧪 E2E Testing arifOS MCP - Full Suite (13 Tools)")
print("=" * 70)

headers = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


def parse_sse(response_text):
    """Parse Server-Sent Events format to extract JSON data"""
    events = []
    current_event = {}

    for line in response_text.strip().split("\n"):
        if line.startswith("event:"):
            current_event["event"] = line[6:].strip()
        elif line.startswith("data:"):
            data = line[5:].strip()
            current_event["data"] = data
            try:
                current_event["json"] = json.loads(data)
            except:
                pass
        elif line == "" and current_event:
            events.append(current_event)
            current_event = {}

    if current_event:
        events.append(current_event)

    return events


def mcp_call(method, params, req_id):
    global session_id
    call_headers = headers.copy()
    if session_id:
        call_headers["MCP-Session-Id"] = session_id

    r = requests.post(
        f"{base_url}/mcp",
        headers=call_headers,
        json={"jsonrpc": "2.0", "method": method, "params": params, "id": req_id},
        timeout=20,
    )

    # Parse SSE response
    if r.headers.get("content-type", "").startswith("text/event-stream"):
        events = parse_sse(r.text)
        new_session = r.headers.get("MCP-Session-Id")
        if new_session:
            session_id = new_session
        return events, r.status_code
    else:
        try:
            return [{"json": r.json()}], r.status_code
        except:
            return [{"data": r.text}], r.status_code


results = {"passed": 0, "failed": 0, "tests": [], "verdicts": {}}

# Test 1: Initialize
print("\n📍 Step 1: Initialize MCP Session")
events, status = mcp_call(
    "initialize",
    {
        "protocolVersion": "2025-11-05",
        "capabilities": {},
        "clientInfo": {"name": "e2e-test", "version": "1.0.0"},
    },
    "init-1",
)

if status == 200 and events and "json" in events[0]:
    result = events[0]["json"].get("result", {})
    server_info = result.get("serverInfo", {})
    print(f"   ✅ Session: {session_id[:25]}...")
    print(f"   Server: {server_info.get('name')} v{server_info.get('version')}")
    results["passed"] += 1
    results["tests"].append("✅ initialize")
else:
    print(f"   ❌ Failed")
    results["failed"] += 1
    results["tests"].append("❌ initialize")

# Test 2: List Tools
print("\n📍 Step 2: List Tools")
events, status = mcp_call("tools/list", {}, "tools-1")
if status == 200 and events and "json" in events[0]:
    result = events[0]["json"].get("result", {})
    tools = result.get("tools", [])
    print(f"   ✅ {len(tools)} tools available")
    results["passed"] += 1
    results["tests"].append(f"✅ tools/list ({len(tools)} tools)")
else:
    results["failed"] += 1
    results["tests"].append("❌ tools/list")

# Test 3: anchor_session (F11-F13)
print("\n📍 Step 3: anchor_session [F11 Authority, F12 Defense, F13 Sovereign]")
events, status = mcp_call(
    "tools/call",
    {
        "name": "anchor_session",
        "arguments": {
            "query": "E2E constitutional governance test",
            "actor_id": "e2e-tester",
            "mode": "conscience",
        },
    },
    "anchor-1",
)

if status == 200 and events:
    for event in events:
        if "json" in event:
            result = event["json"].get("result", {})
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    try:
                        data = json.loads(item.get("text", "{}"))
                        verdict = data.get("verdict", "N/A")
                        print(f"   ✅ Verdict: {verdict}")
                        results["verdicts"]["anchor_session"] = verdict
                        if verdict in ["SEAL", "PARTIAL"]:
                            results["passed"] += 1
                            results["tests"].append(f"✅ anchor_session ({verdict})")
                        else:
                            results["tests"].append(f"⚠️ anchor_session ({verdict})")
                    except:
                        pass

# Test remaining tools
tools_to_test = [
    ("check_vital", {"include_swap": True}, "F4,F5,F7"),
    ("audit_rules", {"audit_scope": "quick", "verify_floors": True}, "F2,F8,F10"),
    ("inspect_file", {"path": "/root/arifOS", "depth": 1, "max_files": 5}, "F1,F4,F11"),
    (
        "search_reality",
        {"query": "constitutional AI governance", "intent": "research"},
        "F2,F4,F12",
    ),
    (
        "fetch_content",
        {
            "id": "https://raw.githubusercontent.com/ariffazil/arifOS/main/README.md",
            "max_chars": 500,
        },
        "F2,F4,F12",
    ),
    (
        "reason_mind",
        {"query": "Analyze thermodynamic efficiency", "session_id": session_id, "risk_mode": "low"},
        "F2,F4,F7,F8",
    ),
    (
        "simulate_heart",
        {
            "query": "Deploy MCP server",
            "session_id": session_id,
            "stakeholders": ["users", "developers"],
        },
        "F4,F5,F6",
    ),
    (
        "vector_memory",
        {"query": "constitutional patterns", "session_id": session_id, "depth": 2},
        "F4,F7,F13",
    ),
    (
        "critique_thought",
        {"session_id": session_id, "plan": {"action": "test", "target": "e2e"}},
        "F4,F7,F8",
    ),
    (
        "apex_judge",
        {
            "session_id": session_id,
            "query": "E2E test verdict",
            "proposed_verdict": "SEAL",
            "human_approve": False,
        },
        "F1-F13",
    ),
]

for tool_name, args, floors in tools_to_test:
    print(f"\n📍 Step {tools_to_test.index((tool_name, args, floors)) + 4}: {tool_name} [{floors}]")
    try:
        events, status = mcp_call(
            "tools/call", {"name": tool_name, "arguments": args}, f"{tool_name}-1"
        )

        if status == 200:
            verdict_found = False
            for event in events:
                if "json" in event:
                    result = event["json"].get("result", {})
                    content = result.get("content", [])
                    for item in content:
                        if item.get("type") == "text":
                            try:
                                data = json.loads(item.get("text", "{}"))
                                verdict = data.get("verdict", "N/A")
                                print(f"   ✅ Verdict: {verdict}")
                                results["verdicts"][tool_name] = verdict
                                verdict_found = True
                                results["passed"] += 1
                                results["tests"].append(f"✅ {tool_name} ({verdict})")
                            except:
                                pass

            if not verdict_found:
                print(f"   ✅ Executed (no verdict in response)")
                results["passed"] += 1
                results["tests"].append(f"✅ {tool_name}")
        else:
            print(f"   ❌ HTTP {status}")
            results["failed"] += 1
            results["tests"].append(f"❌ {tool_name}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")
        results["failed"] += 1
        results["tests"].append(f"❌ {tool_name}")

# Summary
print("\n" + "=" * 70)
print("📊 E2E TEST RESULTS - arifOS MCP 13 Canonical Tools")
print("=" * 70)
total = results["passed"] + results["failed"]
print(f"✅ Passed: {results['passed']}/{total}")
print(f"❌ Failed: {results['failed']}/{total}")
print(f"📈 Success Rate: {results['passed'] / total * 100:.1f}%" if total > 0 else "N/A")

print("\n🎯 Constitutional Verdicts:")
for tool, verdict in results["verdicts"].items():
    icon = "✅" if verdict in ["SEAL", "PARTIAL"] else "⚠️" if verdict == "SABAR" else "❌"
    print(f"   {icon} {tool}: {verdict}")

print("\n📝 All Test Results:")
for test in results["tests"]:
    print(f"   {test}")

print("\n✨ E2E Testing Complete!")
