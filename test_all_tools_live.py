#!/usr/bin/env python3
"""
test_all_tools_live.py — Live verbatim test of all arifOS MCP tools (v2).
This module provides a convenient CLI wrapper around the pytest suite.
"""

import argparse
import sys
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="arifOS MCP — Constitutional Test Runner")
    parser.add_argument("--block", type=str, help="Specific block to run (e.g. governance, triad, edge_cases, sensory, pipeline_full)")
    parser.add_argument("--only", type=str, help="Comma-separated test names to run specifically.")
    parser.add_argument("--ci", action="store_true", help="Run in CI mode (outputs JSON and hides console noise)")
    
    args = parser.parse_args()
    
    # Path to tests/mcp_live
    tests_dir = Path(__file__).parent / "tests" / "mcp_live"
    
    pytest_args = [sys.executable, "-m", "pytest"]
    
    if args.block:
        # e.g., --block governance -> tests/mcp_live/test_governance.py
        pytest_args.append(str(tests_dir / f"test_{args.block}.py"))
    else:
        # run all
        pytest_args.append(str(tests_dir))

    if args.only:
        # Use pytest -k expression
        keywords = " or ".join(args.only.split(","))
        pytest_args.extend(["-k", keywords])
        
    if args.ci:
        # JSON output (if pytest-json-report is installed)
        # Using pytest-reportlog as built-in fallback since it generates JSON-lines
        pytest_args.extend(["--report-log=test-results.json", "-q"])
    else:
        pytest_args.append("-v")
    
    print(f"Running: {' '.join(pytest_args)}")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
