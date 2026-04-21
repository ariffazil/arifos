#!/usr/bin/env python3
"""Sovereign Probe - ANTI-HANTU Layer 2 health check
Tests connectivity to all critical services FROM the orchestrator's perspective.
Uses only stdlib to avoid missing binary dependencies.
"""
import urllib.request
import urllib.error
import sys
import socket

services = {
    "geox-organ:8000": "http://geox-organ:8000/health",
    "vault999:8100": "http://vault999:8100/health",
    "ollama:11434": "http://ollama-engine-prod:11434/",
}

all_ok = True
for name, url in services.items():
    try:
        r = urllib.request.urlopen(url, timeout=5)
        status = r.status
        if status == 200:
            print(f"OK {name}")
        else:
            print(f"FAIL {name} status={status}")
            all_ok = False
    except Exception as e:
        print(f"FAIL {name} {e}")
        all_ok = False

# redis uses RESP protocol - just check port is open
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect(("redis", 6379))
    s.close()
    print("OK redis:6379")
except Exception as e:
    print(f"FAIL redis:6379 {e}")
    all_ok = False

sys.exit(0 if all_ok else 1)
