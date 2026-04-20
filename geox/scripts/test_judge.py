import sys
import os
import asyncio

# Path Hack
sys.path.append(os.path.abspath("."))

from services.evidence_store.store import store
from services.governance.judge import judge

async def test():
    print("Testing 888_JUDGE Loop...")
    
    well_id = "W-101"
    prospect_id = "PROSPECT_ALPHA"
    
    well = store.get_evidence(well_id)
    prospect = store.get_evidence(prospect_id)
    
    if not well or not prospect:
        print("Error: Seed data missing. Run seed_evidence.py first.")
        return

    print(f"Evaluating Well {well_id} vs Prospect {prospect_id}...")
    verdict = judge.evaluate_well_prospect_fit("INTENT-001", well, prospect)
    
    print(f"Verdict Status: {verdict.status}")
    print(f"Verdict Rationale: {verdict.rationale}")
    print(f"Verdict Confidence: {verdict.confidence}")
    print(f"Risk Score: {verdict.risk.score}")

if __name__ == "__main__":
    asyncio.run(test())
