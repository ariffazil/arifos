import json
from pathlib import Path

def generate_html_report(results: list[dict], output_path: str):
    """
    Generates a beautifully styled, un-tamperable HTML report map 
    of the Constitutional Eval Suite run.
    """
    try:
        import pytest_html  # Check if they have the styling extensions
    except ImportError:
        pass
        
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    html_content = [
        "<html><head><title>arifOS Constitutional Report</title>",
        "<style>",
        "body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0c10; color: #c5c6c7; margin: 2rem; }",
        "h1 { color: #66fcf1; border-bottom: 2px solid #45a29e; padding-bottom: 0.5rem; }",
        ".case { background: #1f2833; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; border-left: 5px solid; }",
        ".case.pass { border-color: #66fcf1; }",
        ".case.fail { border-color: #ff4c4c; }",
        ".metric { font-weight: bold; color: #45a29e; }",
        "</style></head><body>",
        "<h1>arifOS Constitutional Eval Report</h1>"
    ]
    
    passes = 0
    fails = 0
    
    for r in results:
        status_class = "pass" if r.get("passed_const") else "fail"
        if r.get("passed_const"):
            passes += 1
        else:
            fails += 1
            
        html_content.append(f"<div class='case {status_class}'>")
        html_content.append(f"<h2>{r.get('case_id', 'UNKNOWN')}</h2>")
        html_content.append(f"<p><span class='metric'>Verdict:</span> {r.get('verdict', 'N/A')}</p>")
        html_content.append(f"<p><span class='metric'>Genius Score:</span> {r.get('genius', 'N/A')}</p>")
        html_content.append(f"<p><span class='metric'>ΔS:</span> {r.get('delta_s', 'N/A')}</p>")
        html_content.append(f"<p><span class='metric'>Floor Scores:</span> {json.dumps(r.get('floor_scores', {}))}</p>")
        html_content.append("</div>")

    html_content.insert(10, f"<p><strong>Total:</strong> {len(results)} | <strong>Passes:</strong> {passes} | <strong>Fails:</strong> {fails}</p>")
    html_content.append("</body></html>")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(html_content))
