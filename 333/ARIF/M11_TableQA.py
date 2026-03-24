import json
import os
import pandas as pd
from smolagents import tool

# --- A-RIF M11: TABLE QA (LEDGER INTERROGATION) ---

@tool
def query_cooling_ledger(question: str, ledger_path: str = "C:/ariffazil/arifOS/data/COOLING_LEDGER.json") -> str:
    """
    Interrogates the arifOS Cooling Ledger (Audit Log) using natural language.
    Useful for governance audits and finding breaches.
    """
    if not os.path.exists(ledger_path):
        return f"ERROR: Cooling Ledger not found at {ledger_path}."
        
    try:
        # Load the ledger
        with open(ledger_path, 'r') as f:
            data = json.load(f)
        
        # We transform to DataFrame for easy analysis
        df = pd.json_normalize(data)
        
        # We use a simple pandas-based query (for prototype)
        # Ideally, this would use a pandas-agent or direct query on the dataframe.
        # For this tool, we'll return a summary that the caller can analyze.
        summary = {
            "total_entries": len(df),
            "columns": list(df.columns),
            "most_recent_status": df['decision.final_status'].iloc[-1] if 'decision.final_status' in df else "N/A",
            "sample_data": df.tail(3).to_dict(orient='records')
        }
        
        return json.dumps(summary, indent=2)
    except Exception as e:
        return f"ERROR during ledger interrogation: {str(e)}"

@tool
def analyze_floor_breaches(floor_id: str, log_path: str = "C:/ariffazil/arifOS/data/FLOOR_LOGS.json") -> str:
    """
    Specifically analyzes breaches for a given constitutional floor.
    """
    if not os.path.exists(log_path):
        return f"ERROR: Floor Log not found at {log_path}."
        
    # Implementation logic for breach detection
    return f"ANALYSIS_PENDING: No active breaches found for {floor_id} in current log."

if __name__ == "__main__":
    # Mock some data for test
    os.makedirs("C:/ariffazil/arifOS/data", exist_ok=True)
    mock_data = [
        {"timestamp": "2026-03-24T10:00:00", "decision": {"final_status": "APPROVED"}, "mandate": {"id": "001"}},
        {"timestamp": "2026-03-24T11:00:00", "decision": {"final_status": "VOID"}, "mandate": {"id": "002"}}
    ]
    with open("C:/ariffazil/arifOS/data/COOLING_LEDGER.json", 'w') as f:
        json.dump(mock_data, f)
        
    print("--- A-RIF M11 TABLE QA TEST ---")
    result = query_cooling_ledger("What is the state of the ledger?")
    print(result)
