import asyncio
import os
import shutil

# Adjust path to find arifosmcp.intelligence correctly if run from root
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

from arifosmcp.intelligence.core.eval.reporters import generate_html_report
from arifosmcp.intelligence.core.eval.suite import ConstitutionalEvalSuite
from arifosmcp.intelligence.core.kernel import get_kernel


async def main():
    print("🔥 Forging Constitutional Eval Suite v2...")
    golden_dir = Path("tests/mcp_live/golden")
    suite = ConstitutionalEvalSuite(golden_dir)
    kernel = await get_kernel()

    print(f"Loading datasets from {golden_dir}...")
    results = await suite.run_all(kernel)

    report_path = "test-reports/index.html"
    print(f"Generating living constitutional dashboard: {report_path}")

    generate_html_report(results, report_path)
    
    # Copy the APEX Sovereign Dashboard
    apex_src = Path("arifosmcp/sites/apex-dashboard/dashboard.html")
    if apex_src.exists():
        apex_dest_dir = Path("test-reports/dashboard")
        apex_dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(apex_src, apex_dest_dir / "index.html")
        print(f"✅ APEX Sovereign Dashboard copied to {apex_dest_dir / 'index.html'}")

    print("✅ Completed Eval Suite. Dashboard generated!")


if __name__ == "__main__":
    asyncio.run(main())
