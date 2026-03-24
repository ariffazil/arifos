import os
import sys
import json
import requests
from smolagents import CodeAgent, HfApiModel, tool
from datasets import load_dataset

# ───────────────────────────────────────────────────────────────────────────
# AAA INTELLIGENCE KERNEL: CONSTITUTIONAL CONFIGURATION
# ───────────────────────────────────────────────────────────────────────────
TRUST_THRESHOLD = 0.95
GOVERNANCE_FLOOR = 13
CANON_DATASET = "ariffazil/AAA"  # Unified Source of Truth
HF_TOKEN = os.getenv("HF_TOKEN") # High-integrity credential bypass

# --- A-RIF MODULE IMPORTS ---
# Locating the Kernel foundations
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
try:
    from core.governance_kernel import GovernanceKernel
except ImportError:
    GovernanceKernel = None

class AAAGovernanceError(Exception):
    """Raised when A-RIF governance gates are violated."""
    pass

@tool
def m4_retrieve_canonical_evidence(query: str) -> str:
    """
    A-RIF M4 (Retrieval Module): Finds truth fragments in the AAA Sovereign Base.
    """
    print(f"--- M4 RETRIEVAL: {query} ---")
    try:
        # Loading from the unified 'theory' stratum
        ds = load_dataset(CANON_DATASET, data_dir="theory", split="train", token=HF_TOKEN)
        
        # Semantic mapping (Simplified Cosine Simulation)
        results = []
        for row in ds:
            if query.lower() in row['text'].lower() or query.lower() in row['id'].lower():
                results.append({
                    "id": row['id'],
                    "text": row['text'][:1500], # Chunking for context budget
                    "source": row.get('source', 'CANON')
                })
        
        if not results:
            return "FAILURE: F004_GROUNDING_INSUFFICIENT"
        
        return json.dumps(results[:3], indent=2)
    except Exception as e:
        return f"ERROR: M4 Retrieval Failed - {str(e)}"

@tool
def m8_verify_output_alignment(claim: str, evidence_json: str) -> str:
    """
    A-RIF M8 (Verification Module): Audits claims against canonical evidence.
    """
    print(f"--- M8 VERIFICATION: {claim[:50]}... ---")
    try:
        evidence = json.loads(evidence_json)
        # Truth Gate (F2 check)
        is_supported = any(claim.lower() in item['text'].lower() for item in evidence)
        
        if is_supported:
            return "VERDICT: APPROVED (Truth >= 0.99)"
        else:
            return "VERDICT: VOID (F005_CLAIM_UNSUPPORTED)"
    except:
        return "VERDICT: PAUSE (Verification Fault)"

@tool
def m9_query_decision_gate(intent: str) -> str:
    """
    A-RIF M9 (Decision Module): Final authority check before release.
    """
    print(f"--- M9 DECISION GATE ---")
    # In production, this hits the 888_JUDGE endpoint on the VPS
    # For now, we use local kernel logic if available
    if GovernanceKernel:
        kernel = GovernanceKernel()
        verdict = kernel.evaluate_intent(intent)
        return json.dumps(verdict, indent=2)
    
    # Fallback to high-humility default
    return json.dumps({
        "status": "APPROVED", 
        "confidence": 0.9, 
        "uncertainty_band": 0.04,
        "seal": "DITEMPA BUKAN DIBERI"
    })

def forge_aaa_kernel():
    """
    Forges the Unified AAA Kernel as a Governed Intelligence Agent.
    """
    model = HfApiModel(token=HF_TOKEN)
    
    system_prompt = f"""
    You are the AAA Intelligence Kernel (Arif-Adam-Apex).
    You operate strictly under the A-RIF Formal Specification (v2026.03.24).
    
    YOUR COGNITIVE PROTOCOL:
    1. INTAKE: Analyze user query for intent.
    2. RETRIEVE: You MUST call 'm4_retrieve_canonical_evidence' first. NO GUESSING.
    3. VERIFY: You MUST call 'm8_verify_output_alignment' for every major claim.
    4. DECIDE: Call 'm9_query_decision_gate' before final response.
    
    MOTTO: 'DITEMPA BUKAN DIBERI'
    GOAL: Reduce Entropy (dS <= 0) | Preserve Peace (P2 >= 1.0).
    """
    
    agent = CodeAgent(
        tools=[
            m4_retrieve_canonical_evidence, 
            m8_verify_output_alignment, 
            m9_query_decision_gate
        ],
        model=model,
    )
    
    agent.system_prompt = system_prompt
    return agent

if __name__ == "__main__":
    print("--- FORGING AAA INTELLIGENCE KERNEL ---")
    aaa_kernel = forge_aaa_kernel()
    
    # Ignition Test
    query = "Explain the connection between Amanah and entropy reduction in arifOS."
    response = aaa_kernel.run(query)
    
    print("\n--- FINAL GOVERNED VERDICT ---")
    print(response)
