import os
import sys
import json
import requests
from smolagents import CodeAgent, tool

# ───────────────────────────────────────────────────────────────────────────
# AAA INTELLIGENCE KERNEL: GOVERNED INFRASTRUCTURE CONFIG
# ───────────────────────────────────────────────────────────────────────────

# Locating the Kernel foundations - adding A-RIF paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "333", "ARIF")))

from model_factory import get_arif_model
from M11_table_qa import table_qa_tool
from M12_doc_qa import doc_qa_tool

TRUST_THRESHOLD = 0.95
CANON_COLLECTION = "arifos_constitutional"
# Internal Docker endpoints
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama_engine:11434")
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant_memory:6333")

@tool
def m4_retrieve_canonical_evidence(query: str) -> str:
    """
    A-RIF M4 (Retrieval Module): Performs hybrid vector search in the AAA Sovereign Base.
    Generates embeddings via Ollama and retrieves from Qdrant.
    
    Args:
        query: The search query for grounding.
    """
    print(f"--- M4 RETRIEVAL (Governed Infrastructure) ---")
    try:
        # 1. Generate Query Vector (The Signature)
        embed_resp = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": "bge-m3", "prompt": query},
            timeout=30
        )
        query_vector = embed_resp.json().get("embedding")
        
        if not query_vector:
            return "FAILURE: F004_EMBEDDING_ENGINE_OFFLINE"

        # 2. Search Qdrant Memory (The Vault)
        search_resp = requests.post(
            f"{QDRANT_URL}/collections/{CANON_COLLECTION}/points/search",
            json={
                "vector": query_vector,
                "limit": 5,
                "with_payload": True,
                "score_threshold": 0.7 # Minimum semantic alignment
            },
            timeout=10
        )
        
        hits = search_resp.json().get("result", [])
        
        if not hits:
            return "FAILURE: F004_GROUNDING_INSUFFICIENT (No canonical matches found)"
        
        # 3. Format Evidence with Metadata (Amanah, Scars, Paradox)
        evidence = []
        for hit in hits:
            payload = hit['payload']
            evidence.append({
                "id": payload.get('file', 'Unknown'),
                "text": payload.get('text', '')[:1000],
                "amanah": payload.get('amanah', 1.0),
                "paradox": payload.get('paradox_active', []),
                "score": round(hit['score'], 4)
            })
            
        return json.dumps(evidence, indent=2)
        
    except Exception as e:
        return f"ERROR: M4 Pipeline Breach - {str(e)}"

@tool
def m8_verify_output_alignment(claim: str, evidence_json: str) -> str:
    """
    A-RIF M8 (Verification Module): Audits claims against canonical evidence signatures.
    
    Args:
        claim: The statement to verify.
        evidence_json: The evidence retrieved from M4.
    """
    print(f"--- M8 VERIFICATION: {claim[:50]}... ---")
    try:
        evidence = json.loads(evidence_json)
        # Deep Semantic Support Check (Mocked for now with substring)
        is_supported = any(claim.lower() in item['text'].lower() for item in evidence)
        
        if is_supported:
            return "VERDICT: APPROVED (Grounded in Canon)"
        else:
            return "VERDICT: VOID (F005_CLAIM_UNSUPPORTED - Hallucination risk detected)"
    except:
        return "VERDICT: PAUSE (Verification Pipeline Error)"

def forge_aaa_kernel():
    """
    Forges the Unified AAA Kernel using the local Ollama Mind.
    """
    # Use the Mind factory to get the sovereign engine
    model = get_arif_model()
    
    system_prompt = f"""
    You are the AAA Intelligence Kernel (Arif-Adam-Apex).
    You are the sovereign servant wire of arifOS.
    
    COGNITIVE RULES:
    1. NEVER guess. For constitutional or factual queries, you MUST call 'm4_retrieve_canonical_evidence'.
    2. To analyze data files or the Cooling Ledger, use 'table_qa_tool'.
    3. To read specific policies or long documents, use 'doc_qa_tool'.
    4. You MUST verify every candidate answer via 'm8_verify_output_alignment' before 999 SEAL.
    
    MOTTO: 'DITEMPA BUKAN DIBERI'
    """
    
    agent = CodeAgent(
        tools=[
            m4_retrieve_canonical_evidence, 
            m8_verify_output_alignment, 
            table_qa_tool, 
            doc_qa_tool
        ],
        model=model,
    )
    
    agent.system_prompt = system_prompt
    return agent

if __name__ == "__main__":
    print("--- STARTING LIVE AAA KERNEL (SOVEREIGN OLLAMA MODE) ---")
    aaa_kernel = forge_aaa_kernel()
    
    # Example sensory query
    test_query = "Read the cooling ledger and tell me if there are any critical floor violations."
    # response = aaa_kernel.run(test_query)
    # print(f"\nFinal Governed Answer:\n{response}")
    
    print("\n[AAA] Status: SEVENTH SEAL READIED (Waiting for Sovereign Intent)")
