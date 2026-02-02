#!/usr/bin/env python3
"""Debug API key authentication"""
import httpx

API_KEY = "Pmsx7POVlMg2aAKJ-G93uGwtAApUFcLEEcr7YtzFgyjuUPeOhBaIfC3OUNcLRCLh"
BASE_URL = "https://aaamcp.arif-fazil.com"

print("=== Debug: Testing API Key ===")
print(f"Key being used: {API_KEY}")
print(f"Key length: {len(API_KEY)}")
print()

try:
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    print(f"Request headers: {headers}")
    print()
    
    r = httpx.get(
        f"{BASE_URL}/api/tools",
        headers=headers,
        timeout=10
    )
    print(f"Response status: {r.status_code}")
    print(f"Response headers: {dict(r.headers)}")
    print(f"Response body: {r.text}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
