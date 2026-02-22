import json
import datetime
from pathlib import Path

def generate_html_report(results: list[dict], output_path: str):
    """
    Generates a beautifully styled, un-tamperable HTML report map 
    of the Constitutional Eval Suite run - designed as the 'Ultimate Polygraph'.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    
    passes = sum(1 for r in results if r.get("passed_const", False))
    fails = len(results) - passes
    total = len(results)
    pass_rate = (passes / total * 100) if total > 0 else 0
    
    # CSS Styles for Premium Deep Blue & Gold Theme
    css = """
        :root {
            --bg-dark: #060b19;
            --bg-card: #0f172a;
            --bg-card-hover: #1e293b;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-cyan: #00f0ff;
            --accent-gold: #ffd700;
            --accent-red: #ff3366;
            --accent-green: #10b981;
            --border-glow: 0 0 10px rgba(0, 240, 255, 0.2);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            line-height: 1.6;
            padding: 2rem;
            background-image: 
                linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
        }
        
        header {
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-main);
            margin-bottom: 0.5rem;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        
        h1 span.highlight { color: var(--accent-gold); }
        
        .subtitle {
            font-size: 1.1rem;
            color: var(--accent-cyan);
            font-style: italic;
            letter-spacing: 1px;
        }
        
        .meta-info {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: var(--text-muted);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .stat-card {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 240, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--border-glow);
            border-color: rgba(0, 240, 255, 0.3);
        }
        
        .stat-value {
            font-size: 3rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #fff, var(--text-muted));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-value.gold { background: linear-gradient(to right, #fff, var(--accent-gold)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-value.cyan { background: linear-gradient(to right, #fff, var(--accent-cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-value.green { background: linear-gradient(to right, #fff, var(--accent-green)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-value.red { background: linear-gradient(to right, #fff, var(--accent-red)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .stat-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--text-muted);
        }
        
        .cases-container {
            display: grid;
            gap: 1.5rem;
        }
        
        .case-card {
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 4px solid var(--text-muted);
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .case-card:hover {
            background: var(--bg-card-hover);
            border-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        .case-card.pass { border-left-color: var(--accent-cyan); }
        .case-card.fail { border-left-color: var(--accent-red); }
        .case-card.hold { border-left-color: var(--accent-gold); }
        
        .case-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .case-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .badge {
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .badge-seal { background: rgba(0, 240, 255, 0.1); color: var(--accent-cyan); border: 1px solid rgba(0, 240, 255, 0.2); }
        .badge-void { background: rgba(255, 51, 102, 0.1); color: var(--accent-red); border: 1px solid rgba(255, 51, 102, 0.2); }
        .badge-hold { background: rgba(255, 215, 0, 0.1); color: var(--accent-gold); border: 1px solid rgba(255, 215, 0, 0.2); }
        .badge-sabar { background: rgba(148, 163, 184, 0.1); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.2); }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .metric-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 1.1rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
        }
        
        .floors-breakdown {
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 6px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
        }
        
        .floor-tag {
            display: inline-block;
            margin: 0.25rem;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .floor-tag.pass { border-color: rgba(0, 240, 255, 0.3); color: var(--accent-cyan); }
        .floor-tag.fail { border-color: rgba(255, 51, 102, 0.3); color: var(--accent-red); }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .case-card {
            animation: fadeIn 0.5s ease backwards;
        }
    """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>arifOS Constitutional Report</title>
        <style>{css}</style>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <header>
            <h1>arifOS <span class="highlight">Golden_13</span> Eval</h1>
            <p class="subtitle">The Ultimate Constitutional Polygraph</p>
            <div class="meta-info">
                <span><strong>Generated:</strong> {timestamp}</span>
                <span><strong>Target:</strong> F1-F13 Integrity Audit</span>
                <span><strong>Status:</strong> {'✅ SEALED' if pass_rate == 100 else '⚠️ ANOMALIES DETECTED'}</span>
            </div>
        </header>
        
        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-value gold">{total}</div>
                <div class="stat-label">Total Cases</div>
            </div>
            <div class="stat-card">
                <div class="stat-value {'green' if passes == total else 'cyan'}">{passes}</div>
                <div class="stat-label">Tests Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value {'red' if fails > 0 else 'text-main'}">{fails}</div>
                <div class="stat-label">Anomalies (Failed)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value {'cyan' if pass_rate >= 95 else 'gold' if pass_rate >= 80 else 'red'}">{pass_rate:.1f}%</div>
                <div class="stat-label">Integrity Score</div>
            </div>
        </div>
        
        <div class="cases-container">
    """
    
    # Render Cases
    for i, r in enumerate(results):
        verdict = str(r.get("verdict", "UNKNOWN")).upper()
        passed = r.get("passed_const", False)
        
        # Determine styling based on verdict
        card_class = "pass" if passed else "fail"
        if verdict in ["HOLD", "HOLD_888"]:
            card_class = "hold"
        elif verdict == "VOID" and passed: # Void can be a passed test if it correctly caught an attack!
            card_class = "pass"
            
        badge_class = "badge-seal"
        if verdict in ["VOID", "EMERGED"]: badge_class = "badge-void"
        elif verdict in ["HOLD", "HOLD_888"]: badge_class = "badge-hold"
        elif verdict == "SABAR": badge_class = "badge-sabar"
        
        # Floor formatting
        floors = r.get("floor_scores", {})
        floor_html = ""
        for floor, score in floors.items():
            f_class = "pass" if float(score) >= 0.8 else "fail"
            floor_html += f"<span class='floor-tag {f_class}'>{floor}: {score:.2f}</span>"
            
        genius = r.get("genius", 0.0)
        genius_color = "var(--accent-cyan)" if genius >= 0.80 else "var(--accent-red)"
        
        delta_s = r.get("delta_s", 0.0)
        ds_color = "var(--accent-cyan)" if delta_s <= 0 else "var(--accent-red)"
        
        # Add a sequential animation delay
        delay = i * 0.05
        
        html += f"""
            <div class="case-card {card_class}" style="animation-delay: {delay}s;">
                <div class="case-header">
                    <div class="case-title">
                        {r.get('case_id', f'Test Case #{i+1}')}
                    </div>
                    <div class="badge {badge_class}">{verdict}</div>
                </div>
                
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                    <strong>Raw Output excerpt:</strong> {str(r.get('raw_output', 'Nil'))[:80]}...
                </p>
                
                <div class="metrics-grid">
                    <div class="metric-item">
                        <span class="metric-label">Thermodynamic Budget</span>
                        <span class="metric-value">ΔS = <span style="color: {ds_color}">{delta_s:.4f}</span></span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Genius Score (G)</span>
                        <span class="metric-value" style="color: {genius_color}">{genius:.4f}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Constitutional Integrity</span>
                        <span class="metric-value">{'PASS' if passed else 'FAIL'}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">LLM As Judge</span>
                        <span class="metric-value">{r.get('judge_score', 'N/A')}</span>
                    </div>
                </div>
                
                <div class="floors-breakdown">
                    <strong>Floor Audits:</strong><br>
                    {floor_html if floor_html else "<span class='floor-tag'>No floor scores captured</span>"}
                </div>
            </div>
        """
        
    html += """
        </div>
        <footer style="margin-top: 3rem; text-align: center; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1rem;">
            DITEMPA BUKAN DIBERI • arifOS Intelligence Kernel • Constitutional Eval Suite
        </footer>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
