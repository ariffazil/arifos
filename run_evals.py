import asyncio
import os
from pathlib import Path

# Adjust path to find aclip_cai correctly if run from root
import sys
sys.path.insert(0, os.path.abspath('.'))

from aclip_cai.core.eval.suite import ConstitutionalEvalSuite
from aclip_cai.core.kernel import get_kernel
from aclip_cai.core.eval.reporters import generate_html_report

async def main():
    print("🔥 Forging Constitutional Eval Suite v2...")
    golden_dir = Path("tests/mcp_live/golden")
    suite = ConstitutionalEvalSuite(golden_dir)
    kernel = await get_kernel()
    
    print(f"Loading datasets from {golden_dir}...")
    results = await suite.run_all(kernel)
    
    report_path = "test-reports/arifos-golden-report.html"
    print(f"Generating living constitutional dashboard: {report_path}")
    
    generate_html_report(results, report_path)
    print("✅ Completed Eval Suite. Dashboard generated!")

if __name__ == "__main__":
    asyncio.run(main())
