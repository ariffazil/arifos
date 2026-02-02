#!/usr/bin/env python3
"""Test API key authentication"""
import httpx

API_KEY = "Pmsx7POVlMg2aAKJ-G93uGwtAApUFcLEEcr7YtzFgyjuUPeOhBaIfC3OUNcLRCLh"
BASE_URL = "https://aaamcp.arif-fazil.com"

print("=== Test 1: Without API key (should fail with 401) ===")
try:
    r = httpx.get(f"{BASE_URL}/api/tools", timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Test 2: With API key (should succeed) ===")
try:
    r = httpx.get(
        f"{BASE_URL}/api/tools",
        headers={"x-api-key": API_KEY},
        timeout=10
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"ok: {data.get('ok')}")
    print(f"tools: {data.get('count')}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Test 3: Vault read with API key ===")
try:
    r = httpx.post(
        f"{BASE_URL}/api/vault/read",
        headers={"x-api-key": API_KEY, "Content-Type": "application/json"},
        json={"sequence": 12},
        timeout=10
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"ok: {data.get('ok')}")
    print(f"tool: {data.get('tool')}")
    print(f"operation: {data.get('operation')}")
except Exception as e:
    print(f"Error: {e}")
