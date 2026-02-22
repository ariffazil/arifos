#!/usr/bin/env python3
"""
arifOS Unified Server — Master Entry Point (v65.0-FORGE)
Canonical "One Server" at the project root.

Combines:
  - 5-Organ Trinity (INIT, AGI, ASI, APEX, VAULT)
  - 10 Sensory Tools (aCLIP_CAI)
  - ChatGPT integration (Search/Fetch)
  - Container Ops & Self-Audit

Usage:
    python server.py                   # REST API (default)
    python server.py --mode rest       # Full HTTP + SSE endpoints
    python server.py --mode sse        # FastMCP SSE transport
    python server.py --mode stdio      # Stdio for local agents

DITEMPA BUKAN DIBERI
"""

import os
import sys

# Ensure local source priority
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aaa_mcp.__main__ import main

if __name__ == "__main__":
    main()
