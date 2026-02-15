"""
arifOS MCP Deployment Tool
==========================

Deploys the constitutional MCP server to production networks.

Usage:
    # Local deployment (stdio)
    python scripts/deploy_mcp.py --mode local
    
    # Railway deployment (SSE/HTTP)
    python scripts/deploy_mcp.py --mode railway
    
    # Docker deployment
    python scripts/deploy_mcp.py --mode docker
    
    # Health check
    python scripts/deploy_mcp.py --health-check

DITEMPA BUKAN DIBERI
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


async def validate():
    """Validate deployment readiness."""
    print("[SCAN] MCP Deployment Validation")
    print("=" * 50)
    
    checks = []
    warnings = []
    errors = []
    
    # Check 1: Core imports
    try:
        from core.organs import init, agi, asi, apex, vault
        from core.pipeline import forge, quick_check
        checks.append("Core imports")
        print("  [OK] Core organs and pipeline accessible")
    except Exception as e:
        errors.append(f"Core imports: {e}")
        print(f"  [ERR] Core imports: {e}")
    
    # Check 2: Core pipeline execution
    try:
        from core.pipeline import forge
        result = await forge("Test query", actor_id="deploy_check")
        checks.append(f"Core pipeline ({result.verdict})")
        print(f"  [OK] Core pipeline executes ({result.verdict})")
    except Exception as e:
        errors.append(f"Core pipeline: {e}")
        print(f"  [ERR] Core pipeline: {e}")
    
    # Check 3: AAA MCP wiring
    try:
        from aaa_mcp.core.engine_adapters import CORE_AVAILABLE
        if CORE_AVAILABLE:
            checks.append("AAA MCP wired to Core")
            print("  [OK] AAA MCP using Core organs")
        else:
            warnings.append("AAA MCP in fallback mode")
            print("  [WARN] AAA MCP in fallback mode")
    except Exception as e:
        warnings.append(f"Wiring check: {e}")
        print(f"  [WARN] Wiring check: {e}")
    
    # Check 4: MCP tools
    try:
        from aaa_mcp.server import mcp
        tools = await mcp.list_tools()
        tool_names = [t.name for t in tools]
        checks.append(f"MCP tools ({len(tools)})")
        print(f"  [OK] MCP tools registered: {len(tools)}")
        for name in tool_names[:5]:
            print(f"       - {name}")
    except Exception as e:
        errors.append(f"MCP tools: {e}")
        print(f"  [ERR] MCP tools: {e}")
    
    # Check 5: Dockerfile
    dockerfile = Path(__file__).parent.parent / "Dockerfile"
    if dockerfile.exists():
        checks.append("Dockerfile")
        print("  [OK] Dockerfile present")
    else:
        errors.append("Dockerfile missing")
        print("  [ERR] Dockerfile missing")
    
    # Check 6: Railway config
    railway_toml = Path(__file__).parent.parent / "railway.toml"
    if railway_toml.exists():
        checks.append("Railway config")
        print("  [OK] railway.toml present")
    else:
        warnings.append("railway.toml missing")
        print("  [WARN] railway.toml missing")
    
    print()
    print("=" * 50)
    print(f"[OK] Checks passed: {len(checks)}")
    print(f"[WARN] Warnings: {len(warnings)}")
    print(f"[ERR] Errors: {len(errors)}")
    
    if errors:
        print("\n[FAIL] Validation failed - fix errors before deployment")
        return False
    
    print("\n[PASS] Validation passed - ready for civilization")
    return True


def deploy_local():
    """Deploy locally using stdio."""
    print("[DEPLOY] Local Deployment (stdio)")
    print("=" * 50)
    
    subprocess.run([sys.executable, "-m", "aaa_mcp"], 
                   cwd=str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Deploy arifOS MCP")
    parser.add_argument("--mode", choices=["local", "railway", "docker", "validate"],
                       default="validate")
    args = parser.parse_args()
    
    if args.mode == "validate":
        success = asyncio.run(validate())
        sys.exit(0 if success else 1)
    elif args.mode == "local":
        deploy_local()


if __name__ == "__main__":
    main()
