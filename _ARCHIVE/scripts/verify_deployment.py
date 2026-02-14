#!/usr/bin/env python
"""
Deployment Verification Script for arifOS MCP Server (v55.5)
Checks all deployment files before pushing to Railway.
"""

import os
import sys
from pathlib import Path

def check_file_exists(path, required=True):
    """Check if a file exists."""
    exists = os.path.exists(path)
    status = "OK" if exists else ("FAIL REQUIRED" if required else "WARN optional")
    print(f"  [{status}] {path}")
    return exists

def verify_deployment():
    """Verify all deployment files are correctly configured."""
    print("=" * 70)
    print("arifOS MCP Deployment Verification (v55.5)")
    print("=" * 70)
    
    all_ok = True
    
    # Check Railway configuration at root (CRITICAL)
    print("\n[1] Railway Configuration (CRITICAL)")
    print("  Railway requires railway.toml at PROJECT ROOT")
    all_ok &= check_file_exists("railway.toml", required=True)
    
    # Check Docker configuration
    print("\n[2] Docker Configuration")
    all_ok &= check_file_exists("Dockerfile", required=True)
    all_ok &= check_file_exists(".dockerignore", required=True)
    
    # Check supporting files
    print("\n[3] Supporting Files")
    check_file_exists("railway.toml", required=False)
    
    # Check Python project files
    print("\n[4] Python Project Files")
    all_ok &= check_file_exists("pyproject.toml", required=True)
    all_ok &= check_file_exists("requirements.txt", required=True)
    
    # Verify railway.toml content
    print("\n[5] Railway.toml Validation")
    if os.path.exists("railway.toml"):
        with open("railway.toml", "r") as f:
            content = f.read()
            checks = [
                ("builder = \"DOCKERFILE\"", "Builder type"),
                ("dockerfilePath = \"Dockerfile\"", "Dockerfile path"),
                ("startCommand = \"python scripts/start_server.py\"", "Start command"),
                ("healthcheckPath = \"/health\"", "Health check"),
            ]
            for check, desc in checks:
                if check in content:
                    print(f"  [OK] {desc}")
                else:
                    print(f"  [FAIL] {desc} - MISSING: {check}")
                    all_ok = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok:
        print("ALL CHECKS PASSED - Ready for Railway deployment!")
        print("\nNext steps:")
        print("  1. git add railway.toml Dockerfile .dockerignore")
        print("  2. git commit -m 'Fix Railway deployment config'")
        print("  3. git push")
        print("  4. railway up")
        return 0
    else:
        print("SOME CHECKS FAILED - Please fix issues above")
        return 1

if __name__ == "__main__":
    sys.exit(verify_deployment())
