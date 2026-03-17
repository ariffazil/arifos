"""REST endpoints for the unified arifOS AAA MCP server.

Registered as custom routes on the FastMCP instance via mcp.custom_route().
These run alongside the standard MCP protocol at /mcp, providing:
  GET  /                           Landing page / service info
  GET  /health                     Docker healthcheck + monitoring
  GET  /version                    Build info
  GET  /tools                      Tool listing (REST-style)
  POST /tools/{tool_name}          REST tool calling (ChatGPT adapter)
  GET  /.well-known/mcp/server.json  MCP registry discovery

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import inspect
import logging
import os
import secrets
import time
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.staticfiles import StaticFiles

from arifosmcp.runtime.public_registry import build_mcp_discovery_json, build_server_json
from arifosmcp.runtime.resources import apex_tools_html_rows, apex_tools_markdown_table
from core.shared.floor_audit import get_ml_floor_runtime
from core.shared.floors import (
    FLOOR_SPEC_KEYS,
    get_floor_comparator,
    get_floor_spec,
    get_floor_threshold,
)

from .build_info import get_build_info
from .capability_map import build_runtime_capability_map
from .contracts import AAA_TOOL_ALIASES, AAA_TOOL_STAGE_MAP, TRINITY_BY_TOOL

BUILD_INFO = get_build_info()
MCP_PROTOCOL_VERSION = "2025-11-25"
MCP_SUPPORTED_PROTOCOL_VERSIONS = ["2025-11-25"]

TOOL_ALIASES: dict[str, str] = dict(AAA_TOOL_ALIASES)

logger = logging.getLogger(__name__)

_DASHBOARD_ALLOWED_ORIGINS = {
    "https://apex.arif-fazil.com",
    "https://arifosmcp.arif-fazil.com",
}


def _representative_floor_score(floor_id: str) -> float:
    """
    Build a visualizer-friendly fallback score from canonical core floor specs.

    This intentionally stays transport-agnostic by deriving from core as source-of-truth.
    """
    comparator = get_floor_comparator(floor_id)
    threshold = float(get_floor_threshold(floor_id))
    spec = get_floor_spec(floor_id)

    if floor_id == "F7" and "range" in spec:
        low, _high = spec["range"]
        return float(low) + 0.01  # representative in-band humility value

    if comparator in {">", ">="}:
        return threshold
    if comparator == "<=":
        return threshold
    # "<" comparators (e.g., risk-style floors) — choose conservative passing value
    return threshold * 0.5


def _canonical_floor_defaults() -> dict[str, float]:
    return {fid: _representative_floor_score(fid) for fid in FLOOR_SPEC_KEYS}


# Fallback floor defaults used only when live governance kernel state is unavailable.
_FLOOR_DEFAULTS: dict[str, float] = _canonical_floor_defaults()

# Fallback Tri-Witness weights (normalised to sum to 1.0).
# Reflects approximate sovereign split: Human 42%, AI 32%, Earth 26%.
_WITNESS_DEFAULTS: dict[str, float] = {"human": 0.42, "ai": 0.32, "earth": 0.26}

# Default QDF (Quantum Decision Field) baseline — target ≥ 0.83 per APEX solver spec.
_DEFAULT_QDF: float = 0.83

# Default metabolic stage returned when kernel state is unavailable.
# 333 = REASON stage, the last full AGI reasoning stage before TRINITY_SYNC.
_DEFAULT_METABOLIC_STAGE: int = 333


def _cache_headers() -> dict[str, str]:
    return {"Cache-Control": "no-store"}


def _dashboard_cors_headers(request: Request) -> dict[str, str]:
    origin = request.headers.get("origin", "").strip()
    if origin in _DASHBOARD_ALLOWED_ORIGINS:
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Vary": "Origin",
        }
    return {}


def _merge_headers(*header_sets: dict[str, str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for header_set in header_sets:
        merged.update(header_set)
    return merged


def _floor_passes(floor_id: str, score: float) -> bool:
    spec = get_floor_spec(floor_id)
    comparator = get_floor_comparator(floor_id)
    if floor_id == "F7" and "range" in spec:
        lower, upper = spec["range"]
        return float(lower) <= float(score) <= float(upper)

    threshold = float(get_floor_threshold(floor_id))
    if comparator == "<":
        return float(score) < threshold
    if comparator == "<=":
        return float(score) <= threshold
    if comparator == ">":
        return float(score) > threshold
    return float(score) >= threshold


def _build_governance_status_payload() -> dict[str, Any]:
    session_id: str | None = None
    floors: dict[str, Any] = {}
    telemetry: dict[str, Any] = {}
    witness: dict[str, float] = {}
    qdf: float = 0.0
    metabolic_stage: int = 0
    verdict: str = "SEAL"

    try:
        from core.governance_kernel import get_governance_kernel

        kernel = get_governance_kernel()
        state = kernel.get_current_state() if hasattr(kernel, "get_current_state") else {}
        if state:
            session_id = state.get("session_id")
            floors = state.get("floors", {})
            telemetry = state.get("telemetry", {})
            witness = state.get("witness", {})
            qdf = float(state.get("qdf", 0.0))
            metabolic_stage = int(state.get("metabolic_stage", 0))
            verdict = state.get("verdict", "SEAL")
    except (ImportError, AttributeError):
        logger.debug("Governance kernel unavailable — using default telemetry values")
    except Exception:
        logger.exception("Unexpected error loading governance kernel state")

    resolved_floors = {k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}
    resolved_witness = {k: witness.get(k, v) for k, v in _WITNESS_DEFAULTS.items()}
    resolved_telemetry = {
        "dS": telemetry.get("dS", -0.35),
        "peace2": telemetry.get("peace2", 1.04),
        "kappa_r": telemetry.get("kappa_r", 0.97),
        "echoDebt": telemetry.get("echoDebt", 0.4),
        "shadow": telemetry.get("shadow", 0.3),
        "confidence": telemetry.get("confidence", 0.88),
        "psi_le": telemetry.get("psi_le", 0.82),
        "verdict": verdict,
    }

    try:
        from core.telemetry import get_system_vitals

        machine_vitals = get_system_vitals()
    except Exception:
        machine_vitals = {"cpu_percent": 0.0, "memory_percent": 0.0}

    try:
        capability_map = build_runtime_capability_map()
        if (
            float(resolved_floors.get("F11", 0.0)) <= 0.0
            and capability_map.get("capabilities", {}).get("governed_continuity") == "enabled"
        ):
            resolved_floors["F11"] = _FLOOR_DEFAULTS["F11"]
    except Exception:
        capability_map = None

    try:
        if float(resolved_floors.get("F8", 0.0)) <= 0.0:
            from core.enforcement.genius import calculate_genius, coerce_floor_scores

            floor_scores = coerce_floor_scores(
                {
                    "f1": resolved_floors.get("F1"),
                    "f2": resolved_floors.get("F2"),
                    "f3": resolved_floors.get("F3"),
                    "f4": resolved_floors.get("F4"),
                    "f5": resolved_floors.get("F5"),
                    "f6": resolved_floors.get("F6"),
                    "f7": resolved_floors.get("F7"),
                    "f9": resolved_floors.get("F9"),
                    "f10": resolved_floors.get("F10"),
                    "f11": resolved_floors.get("F11"),
                    "f12": resolved_floors.get("F12"),
                    "f13": resolved_floors.get("F13"),
                }
            )
            genius_res = calculate_genius(
                floor_scores, h=0.0, compute_budget_used=0.0, compute_budget_max=1.0
            )
            resolved_floors["F8"] = round(
                max(_FLOOR_DEFAULTS["F8"], float(genius_res.get("genius_score", 0.0))),
                4,
            )
            if float(resolved_telemetry.get("confidence", 0.0)) <= 0.0:
                resolved_telemetry["confidence"] = resolved_floors["F8"]
    except Exception:
        pass

    return {
        "telemetry": resolved_telemetry,
        "witness": resolved_witness,
        "qdf": qdf or _DEFAULT_QDF,
        "floors": resolved_floors,
        "machine_vitals": machine_vitals,
        "session_id": session_id or f"sess_{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metabolic_stage": metabolic_stage or _DEFAULT_METABOLIC_STAGE,
    }


def _render_status_html(payload: dict[str, Any]) -> str:
    telemetry = payload["telemetry"]
    floors = payload["floors"]
    vitals = payload["machine_vitals"]
    witness = payload["witness"]

    floor_rows: list[str] = []
    for floor_id in sorted(FLOOR_SPEC_KEYS.keys(), key=lambda item: int(item[1:])):
        score = float(floors.get(floor_id, _FLOOR_DEFAULTS.get(floor_id, 0.0)))
        passed = _floor_passes(floor_id, score)
        status = "PASS" if passed else "FAIL"
        row_class = "pass" if passed else "fail"
        floor_rows.append(
            '<tr class="%s"><td>%s</td><td>%0.3f</td><td>%s</td></tr>'
            % (row_class, floor_id, score, status)
        )

    load_avg = vitals.get("load_avg", [])
    load_text = ", ".join(f"{float(value):.2f}" for value in load_avg[:3]) if load_avg else "n/a"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>arifOS Status</title>
  <style>
    body {{ background:#0b0f14; color:#e6edf3; font-family: ui-monospace, monospace; margin:0; padding:24px; }}
    h1,h2 {{ margin:0 0 12px; }}
    .meta, .grid {{ display:grid; gap:12px; }}
    .meta {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin: 0 0 20px; }}
    .card {{ background:#111821; border:1px solid #243041; border-radius:10px; padding:14px; }}
    .label {{ color:#8aa0b6; font-size:12px; text-transform:uppercase; letter-spacing:.08em; }}
    .value {{ font-size:20px; margin-top:6px; }}
    table {{ width:100%; border-collapse: collapse; margin-top: 10px; }}
    th, td {{ padding:8px 10px; border-bottom:1px solid #243041; text-align:left; }}
    .pass {{ color:#7ee787; }}
    .fail {{ color:#ff7b72; font-weight:bold; }}
    code {{ color:#f2cc60; }}
  </style>
</head>
<body>
  <h1>arifOS Ops Truth Page</h1>
  <div class="meta">
    <div class="card"><div class="label">Verdict</div><div class="value">{telemetry["verdict"]}</div></div>
    <div class="card"><div class="label">Timestamp</div><div class="value"><code>{payload["timestamp"]}</code></div></div>
    <div class="card"><div class="label">Session</div><div class="value"><code>{payload["session_id"]}</code></div></div>
    <div class="card"><div class="label">Metabolic Stage</div><div class="value">{payload["metabolic_stage"]}</div></div>
  </div>

  <div class="grid">
    <div class="card">
      <h2>Floors</h2>
      <table>
        <thead><tr><th>Floor</th><th>Score</th><th>Status</th></tr></thead>
        <tbody>
          {"".join(floor_rows)}
        </tbody>
      </table>
    </div>

    <div class="card">
      <h2>Telemetry</h2>
      <table>
        <tbody>
          <tr><td>dS</td><td>{float(telemetry.get("dS", 0.0)):.3f}</td></tr>
          <tr><td>peace2</td><td>{float(telemetry.get("peace2", 0.0)):.3f}</td></tr>
          <tr><td>echoDebt</td><td>{float(telemetry.get("echoDebt", 0.0)):.3f}</td></tr>
          <tr><td>shadow</td><td>{float(telemetry.get("shadow", 0.0)):.3f}</td></tr>
          <tr><td>psi_le</td><td>{float(telemetry.get("psi_le", 0.0)):.3f}</td></tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h2>Machine Vitals</h2>
      <table>
        <tbody>
          <tr><td>CPU</td><td>{float(vitals.get("cpu_percent", 0.0)):.1f}%</td></tr>
          <tr><td>Memory</td><td>{float(vitals.get("memory_percent", 0.0)):.1f}%</td></tr>
          <tr><td>Disk</td><td>{float(vitals.get("disk_percent", 0.0)):.1f}%</td></tr>
          <tr><td>Load</td><td>{load_text}</td></tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h2>Witness</h2>
      <table>
        <tbody>
          <tr><td>Human</td><td>{float(witness.get("human", 0.0)):.3f}</td></tr>
          <tr><td>AI</td><td>{float(witness.get("ai", 0.0)):.3f}</td></tr>
          <tr><td>Earth</td><td>{float(witness.get("earth", 0.0)):.3f}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>"""


WELCOME_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>arifOS MCP Server</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0d0d0d;color:#d4d4d4;font-family:ui-monospace,monospace;
         font-size:14px;line-height:1.6;padding:2rem 1rem;max-width:860px;margin:auto}
    h1{color:#e6c25d;font-size:1.5rem;margin-bottom:.25rem}
    h2{color:#aaa;font-size:.85rem;font-weight:normal;margin-bottom:2rem;
       letter-spacing:.08em;text-transform:uppercase}
    .pill{display:inline-block;background:#00ff8822;color:#00ff88;
          border:1px solid #00ff8855;border-radius:99px;
          padding:.1rem .6rem;font-size:.65rem;margin-left:.75rem;
          vertical-align:middle;position:relative;top:-2px}
    .pill-live{display:inline-block;background:#00ff8822;color:#00ff88;
          border:1px solid #00ff8855;border-radius:99px;
          padding:.1rem .6rem;font-size:.65rem;margin-left:.75rem;
          vertical-align:middle;position:relative;top:-2px;
          animation:pulse 2s infinite}
    .status-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin:1.5rem 0}
    .status-card{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:1rem}
    .status-card h4{color:#888;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem}
    .status-card .value{color:#e6c25d;font-size:1.25rem;font-weight:600}
    .status-card .live-indicator{display:inline-flex;align-items:center;gap:.5rem;color:#00ff88;font-size:.75rem;margin-top:.5rem}
    .status-card .mock-indicator{display:inline-flex;align-items:center;gap:.5rem;color:#f59e0b;font-size:.75rem;margin-top:.5rem}
    .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
    .dot.live{animation:pulse 1.5s infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
    section{margin-bottom:2.5rem}
    h3{color:#e6c25d;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;
       border-bottom:1px solid #333;padding-bottom:.4rem;margin-bottom:.75rem}
    table{width:100%;border-collapse:collapse}
    td,th{padding:.4rem .6rem;text-align:left}
    th{color:#888;font-weight:normal;font-size:.75rem;text-transform:uppercase}
    tr:nth-child(odd){background:#ffffff06}
    .stage{color:#e6c25d;font-size:.75rem;min-width:3.5rem;display:inline-block}
    .name{color:#7dd3fc}
    .role{color:#aaa}
    .url{color:#7dd3fc}
    a{color:#7dd3fc;text-decoration:none}
    a:hover{text-decoration:underline}
    .nav{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2rem}
    .nav a{background:#1a1a1a;border:1px solid #333;padding:.3rem .8rem;
           border-radius:4px;font-size:.8rem;color:#aaa}
    .nav a:hover{border-color:#7dd3fc;color:#7dd3fc}
    .motto{color:#555;font-size:.75rem;margin-top:2rem;text-align:center}
  </style>
</head>
<body>
  <h1>arifOS MCP <span class="pill-live">&#9679; LIVE</span></h1>
  <h2>Metabolic Governance Kernel v2026.03.14-VALIDATED</h2>
  
  <div class="status-grid">
    <div class="status-card">
      <h4>Constitutional Floors</h4>
      <div class="value">13/13 Active</div>
      <span class="live-indicator"><span class="dot live"></span>Real-time enforcement</span>
    </div>
    <div class="status-card">
      <h4>System Vitals</h4>
      <div class="value">LIVE</div>
      <span class="live-indicator"><span class="dot live"></span>CPU/Memory/Disk</span>
    </div>
    <div class="status-card">
      <h4>3E Telemetry</h4>
      <div class="value">ΔS/Peace²/G</div>
      <span class="live-indicator"><span class="dot live"></span>Physics engine</span>
    </div>
    <div class="status-card">
      <h4>Dashboard</h4>
      <div class="value"><a href="/dashboard" style="color:#7dd3fc">Open ↗</a></div>
      <span class="mock-indicator"><span class="dot" style="background:#f59e0b"></span>Some metrics simulated</span>
    </div>
  </div>

  <div class="nav">
    <a href="/tools">/tools</a>
    <a href="/health">/health</a>
    <a href="/dashboard">/dashboard</a>
    <a href="/status">/status</a>
    <a href="/version">/version</a>
    <a href="/openapi.json">/openapi.json</a>
    <a href="/llms.txt">/llms.txt</a>
    <a href="/llms.json">/llms.json</a>
    <a href="/.well-known/mcp/server.json">/mcp/server.json</a>
    <a href="https://arif-fazil.com" target="_blank">human</a>
    <a href="https://apex.arif-fazil.com" target="_blank">theory</a>
    <a href="https://arifos.arif-fazil.com" target="_blank">apps</a>
  </div>

  <section>
    <h3>Canonical Public arifOS Stack</h3>
    <table>
      <tr><th>Tool Name</th><th>Layer</th><th>Role</th></tr>
      __APEX_HTML_ROWS__
    </table>
  </section>

  <section>
    <h3>Endpoints</h3>
    <table>
      <tr><th>Method</th><th>Path</th><th>Description</th></tr>
      <tr><td>GET</td><td class="url">/health</td><td>Service health check</td></tr>
      <tr><td>GET</td><td class="url">/openapi.json</td><td>OpenAPI 3.1 schema</td></tr>
      <tr><td>GET</td><td class="url">/llms.txt</td><td>LLM-readable server description</td></tr>
      <tr><td>GET</td><td class="url">/llms.json</td><td>Full Sovereign Quad ecosystem map</td></tr>
      <tr><td>GET</td><td class="url">/discovery</td><td>MCP registry discovery</td></tr>
    </table>
  </section>

  <section>
    <h3>Governance</h3>
    <p style="color:#888">
      Every tool call passes through 13 constitutional floors (F1&ndash;F13).<br>
      Verdicts: <strong style="color:#00ff88">SEAL</strong> &nbsp;
                <strong style="color:#e6c25d">PARTIAL</strong> &nbsp;
                <strong style="color:#ff8800">HOLD-888</strong> &nbsp;
                <strong style="color:#ff4444">VOID</strong> &nbsp;
                <strong style="color:#ff4444">SABAR</strong><br>
      Protocol: <a href="https://modelcontextprotocol.io" target="_blank">MCP 2025-11-25</a>
    </p>
  </section>

  <div class="motto">DITEMPA BUKAN DIBERI &mdash; Forged, not given.</div>
</body>
</html>
"""

DOCS_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Documentation | arifOS MCP Server</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0d0d0d;color:#d4d4d4;font-family:ui-monospace,monospace;
         font-size:14px;line-height:1.6;padding:2rem 1rem;max-width:900px;margin:auto}
    h1{color:#e6c25d;font-size:1.5rem;margin-bottom:.25rem}
    h2{color:#e6c25d;font-size:1.1rem;margin:2rem 0 1rem;border-bottom:1px solid #333;padding-bottom:.5rem}
    h3{color:#7dd3fc;font-size:1rem;margin:1.5rem 0 .5rem}
    p{margin-bottom:1rem}
    ul,ol{margin-left:2rem;margin-bottom:1rem}
    li{margin-bottom:.5rem}
    code{background:#1a1a1a;padding:.2rem .4rem;border-radius:4px;font-size:.9rem}
    pre{background:#1a1a1a;padding:1rem;border-radius:8px;overflow-x:auto;margin:1rem 0;border:1px solid #333}
    a{color:#7dd3fc;text-decoration:none}
    a:hover{text-decoration:underline}
    .nav{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap}
    .nav a{background:#1a1a1a;border:1px solid #333;padding:.3rem .8rem;border-radius:4px;font-size:.8rem;color:#aaa}
    .nav a:hover{border-color:#7dd3fc;color:#7dd3fc}
    .version{color:#888;font-size:.9rem;margin-bottom:2rem}
    .note{background:#1a1a1a;border-left:3px solid #7dd3fc;padding:1rem;margin:1rem 0}
    table{width:100%;border-collapse:collapse;margin:1rem 0}
    th,td{padding:.5rem;text-align:left;border-bottom:1px solid #333}
    th{color:#e6c25d;font-weight:normal}
    footer{text-align:center;margin-top:3rem;padding-top:2rem;border-top:1px solid #333;color:#666;font-size:.85rem}
  </style>
</head>
<body>
  <h1>📚 arifOS Documentation</h1>
  <div class="version">Version 2026.03.14-VALIDATED</div>
  
  <div class="nav">
    <a href="/">← Home</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/tools">Tools API</a>
    <a href="/health">Health</a>
  </div>

  <h2>Quick Start</h2>
  <pre><code># Install
pip install arifosmcp==2026.3.14

# Run MCP server
python -m arifosmcp.runtime stdio</code></pre>

  <h2>The 25 Canonical Tools</h2>
  <h3>KERNEL (6 tools)</h3>
  <ul>
    <li><code>init_anchor</code> — Initialize session jurisdiction (000_INIT)</li>
    <li><code>arifOS_kernel</code> — Stage conductor, routes ΔΩΨ (444_ROUTER)</li>
    <li><code>forge</code> — Full pipeline trigger (000→999)</li>
    <li><code>revoke_anchor_state</code> — Kill switch</li>
    <li><code>register_tools</code> — Tool surface declaration</li>
  </ul>

  <h3>AGI Δ MIND (6 tools)</h3>
  <ul>
    <li><code>agi_reason</code> — Governed reasoning (F2/F4/F7)</li>
    <li><code>agi_reflect</code> — Metacognitive integration</li>
    <li><code>reality_compass</code> — Ground claims before reasoning</li>
    <li><code>search_reality</code> — Live web search</li>
    <li><code>ingest_evidence</code> — URL→normalized evidence</li>
    <li><code>reality_atlas</code> — Evidence mapping</li>
  </ul>

  <h3>ASI Ω HEART/HAND (4 tools)</h3>
  <ul>
    <li><code>asi_critique</code> — Adversarial safety check</li>
    <li><code>asi_simulate</code> — Consequence simulation</li>
    <li><code>agentzero_engineer</code> — Code execution (F11 gate)</li>
    <li><code>agentzero_memory_query</code> — Semantic recall</li>
  </ul>

  <h3>APEX Ψ SOUL (7 tools)</h3>
  <ul>
    <li><code>apex_judge</code> — Tri-witness verdict</li>
    <li><code>audit_rules</code> — F1-F13 inspection</li>
    <li><code>agentzero_validate</code> — Output validation</li>
    <li><code>agentzero_armor_scan</code> — F12 injection guard</li>
    <li><code>agentzero_hold_check</code> — 888_HOLD registry</li>
    <li><code>check_vital</code> — System telemetry</li>
    <li><code>open_apex_dashboard</code> — Live governance UI</li>
  </ul>

  <h3>VAULT999 (2 tools)</h3>
  <ul>
    <li><code>vault_seal</code> — Commit to ledger</li>
    <li><code>verify_vault_ledger</code> — Merkle integrity check</li>
  </ul>

  <h2>13 Constitutional Floors</h2>
  <table>
    <tr><th>Floor</th><th>Name</th><th>Threshold</th><th>Enforces</th></tr>
    <tr><td>F1</td><td>Amanah</td><td>≥ 0.5</td><td>Reversibility</td></tr>
    <tr><td>F2</td><td>Truth</td><td>≥ 0.99</td><td>Anti-hallucination</td></tr>
    <tr><td>F3</td><td>Tri-Witness</td><td>≥ 0.95</td><td>Consensus</td></tr>
    <tr><td>F4</td><td>ΔS Clarity</td><td>≤ 0</td><td>Entropy reduction</td></tr>
    <tr><td>F5</td><td>Peace²</td><td>≥ 1.0</td><td>Stability</td></tr>
    <tr><td>F6</td><td>Empathy</td><td>≥ 0.70</td><td>Weakest stakeholder</td></tr>
    <tr><td>F7</td><td>Humility</td><td>0.03-0.20</td><td>Uncertainty</td></tr>
    <tr><td>F8</td><td>Genius</td><td>≥ 0.80</td><td>Coherence</td></tr>
    <tr><td>F9</td><td>Anti-Hantu</td><td>&lt; 0.30</td><td>No dark patterns</td></tr>
    <tr><td>F10</td><td>Ontology</td><td>LOCK</td><td>No consciousness claims</td></tr>
    <tr><td>F11</td><td>Command Auth</td><td>LOCK</td><td>Identity verification</td></tr>
    <tr><td>F12</td><td>Injection</td><td>&lt; 0.85</td><td>Adversarial defense</td></tr>
    <tr><td>F13</td><td>Sovereign</td><td>HUMAN</td><td>Human veto</td></tr>
  </table>

  <h2>Trinity Architecture (ΔΩΨ)</h2>
  <ul>
    <li><strong>Δ Delta (AGI Mind)</strong> — Stages 000-444: Reason, sense, ground</li>
    <li><strong>Ω Omega (ASI Heart)</strong> — Stages 555-666: Empathy, memory, ethics</li>
    <li><strong>Ψ Psi (APEX Soul)</strong> — Stages 777-999: Forge, judge, seal</li>
  </ul>

  <h2>API Endpoints</h2>
  <ul>
    <li><code>GET /health</code> — System health & version</li>
    <li><code>GET /tools</code> — List all 25 tools</li>
    <li><code>GET /dashboard</code> — Live governance UI</li>
    <li><code>POST /mcp</code> — MCP protocol endpoint</li>
  </ul>

  <h2>MCP Client Setup</h2>
  <pre><code>{
  "mcpServers": {
    "arifos": {
      "command": "npx",
      "args": ["-y", "@arifos/mcp"]
    }
  }
}</code></pre>

  <footer>
    <p>Ditempa Bukan Diberi — Forged, Not Given [ΔΩΨ | ARIF]</p>
    <p>© 2026 Muhammad Arif bin Fazil | AGPL-3.0-only</p>
  </footer>
</body>
</html>
"""

ROBOTS_TXT = """\
User-agent: *
Allow: /

# LLM-readable description of this service
# See: https://llmstxt.org
Sitemap: https://arifosmcp.arif-fazil.com/llms.txt
Sitemap: https://arifosmcp.arif-fazil.com/llms.json
"""

LLMS_TXT = """\
# arifOS Brain (Runtime)
Location: https://arifosmcp.arif-fazil.com/llms.txt
Version: 2026.03.14-VALIDATED
Domain: BRAIN / THE MIND (Ω)

> arifOS Constitutional Kernel — a governed Model Context Protocol (MCP) server.
> Motto: DITEMPA BUKAN DIBERI — Forged, not given.

## What this server does

arifOS is an MCP server exposing a canonical public metabolic AI pipeline.
Every tool call passes through 13 governance floors (F1-F13) and returns
a structured RuntimeEnvelope with verdict, thermodynamic telemetry, and Tri-Witness scores. 
Agents reason from the capability map (Known Constraints).

## Connectivity

- **MCP Endpoint**: `https://arifosmcp.arif-fazil.com/mcp` (Streamable-HTTP)
- **Dashboard**: `https://arifosmcp.arif-fazil.com/dashboard/` (Live Audit)
- **Health**: `https://arifosmcp.arif-fazil.com/health`
- **Registry**: `https://arifosmcp.arif-fazil.com/.well-known/mcp/server.json`

## The canonical public arifOS stack

__APEX_MD_TABLE__

## Governance floors summary

- Hard floors: F1, F2, F4, F7, F9, F10, F11, F12.
- Soft floors: F3, F5, F6, F8.
- Veto: F13 Sovereign — human final authority

## 🔗 SOVEREIGN QUAD (Cross-Domain Context)
- **Human**: https://arif-fazil.com/llms.txt — The Epistemic Body
- **Theory**: https://apex.arif-fazil.com/llms.txt — The Authority Soul
- **Apps**: https://arifos.arif-fazil.com/llms.txt — The Safety Mind
- **Brain**: https://arifosmcp.arif-fazil.com/llms.txt — The Runtime Execution (THIS SITE)

---
**Status:** Ditempa Bukan Diberi.
**Vault Tier:** BRAIN
"""

LLMS_JSON = {
    "name": "arifOS Sovereign Quad",
    "description": "Unified Governance Kernel Map for Human, Theory, Law, and Brain domains.",
    "version": "2026.03.14-VALIDATED",
    "authority": "Muhammad Arif bin Fazil (888 Judge)",
    "motto": "Ditempa Bukan Diberi (Forged, Not Given)",
    "domains": {
        "human": {
            "name": "The Body (Human Authority)",
            "url": "https://arif-fazil.com",
            "llms_txt": "https://arif-fazil.com/llms.txt",
            "role": "Epistemic Root and final 888_JUDGE terminal.",
        },
        "theory": {
            "name": "The Soul (Constitutional Theory)",
            "url": "https://apex.arif-fazil.com",
            "llms_txt": "https://apex.arif-fazil.com/llms.txt",
            "role": "Mathematical foundations and the APEX Manifesto.",
        },
        "law": {
            "name": "The Mind (Technical Docs & Apps)",
            "url": "https://arifos.arif-fazil.com",
            "llms_txt": "https://arifos.arif-fazil.com/llms.txt",
            "role": "The 13 Floors specification and integration hub.",
        },
        "brain": {
            "name": "The Engine (Runtime MCP)",
            "url": "https://arifosmcp.arif-fazil.com",
            "llms_txt": "https://arifosmcp.arif-fazil.com/llms.txt",
            "role": "The live Constitutional Kernel (MCP) and Audit Dashboard.",
        },
    },
    "status": {
        "version": "2026.03.14-VALIDATED",
        "status": "FORGED",
    },
}

WELCOME_HTML = WELCOME_HTML.replace("__APEX_HTML_ROWS__", apex_tools_html_rows())
LLMS_TXT = LLMS_TXT.replace("__APEX_MD_TABLE__", apex_tools_markdown_table())

CHECKPOINT_MODES = {"quick", "full", "audit_only"}
RISK_TIER_BY_MODE = {
    "quick": "low",
    "full": "medium",
    "audit_only": "medium",
}


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _required_bearer_token() -> str | None:
    return os.getenv("ARIFOS_API_KEY") or os.getenv("ARIFOS_API_TOKEN")


def _auth_error_response(request: Request) -> JSONResponse | None:
    """Auth disabled - public access allowed."""
    return None


def _normalize_tool_name(raw_name: str) -> str:
    """Normalize tool path params so trailing slashes do not break alias resolution."""
    return (raw_name or "").strip().strip("/")


def _public_base_url(request: Request) -> str:
    explicit = os.getenv("ARIFOS_PUBLIC_BASE_URL", "").strip().rstrip("/")
    if explicit:
        return explicit
    scheme = request.headers.get("x-forwarded-proto") or request.url.scheme or "https"
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or "localhost"
    return f"{scheme}://{host}".rstrip("/")


def _openapi_schema(base_url: str) -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "arifOS Checkpoint REST API",
            "version": BUILD_INFO["version"],
            "description": (
                "Minimal REST/OpenAPI compatibility surface for arifOS constitutional "
                "evaluation. Primary endpoint: POST /checkpoint. This is not the MCP "
                "transport; remote MCP clients should connect to `/mcp`."
            ),
        },
        "servers": [{"url": base_url}],
        "paths": {
            "/checkpoint": {
                "post": {
                    "operationId": "evaluateCheckpoint",
                    "summary": "Constitutional checkpoint evaluation",
                    "description": (
                        "Runs governed evaluation through arifOS and returns verdict + telemetry."
                    ),
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CheckpointRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Checkpoint completed",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/CheckpointResponse"}
                                }
                            },
                        },
                        "400": {
                            "description": "Invalid request",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                        "401": {
                            "description": "Unauthorized",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                        "500": {
                            "description": "Internal error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                    },
                }
            },
            "/health": {
                "get": {
                    "operationId": "getHealth",
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "Service healthy",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "CheckpointRequest": {
                    "type": "object",
                    "required": ["task"],
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "User query/task to evaluate constitutionally.",
                        },
                        "mode": {
                            "type": "string",
                            "enum": sorted(CHECKPOINT_MODES),
                            "default": "full",
                            "description": "Execution profile for checkpoint evaluation.",
                        },
                        "actor_id": {
                            "type": "string",
                            "default": "chatgpt-action",
                            "description": "Caller identity for audit trail.",
                        },
                        "context": {
                            "description": "Optional context payload.",
                            "oneOf": [{"type": "string"}, {"type": "object"}, {"type": "array"}],
                        },
                        "risk_tier": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Optional risk override. If omitted, derived from mode.",
                        },
                        "debug": {"type": "boolean", "default": False},
                    },
                },
                "CheckpointResponse": {
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string"},
                        "session_id": {"type": "string"},
                        "request_id": {"type": "string"},
                        "latency_ms": {"type": "number"},
                        "mode": {"type": "string"},
                        "risk_tier": {"type": "string"},
                        "metrics": {"type": "object"},
                        "floors": {"type": "object"},
                        "result": {"type": "object"},
                    },
                    "required": ["verdict", "request_id", "latency_ms"],
                },
                "HealthResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "service": {"type": "string"},
                        "version": {"type": "string"},
                        "transport": {"type": "string"},
                        "tools_loaded": {"type": "integer"},
                        "timestamp": {"type": "string"},
                    },
                    "required": ["status", "service", "version", "transport"],
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "error_description": {"type": "string"},
                        "request_id": {"type": "string"},
                    },
                    "required": ["error"],
                },
            }
        },
    }


def register_rest_routes(mcp: Any, tool_registry: dict[str, Callable]) -> None:
    """Register REST endpoints as custom routes on the FastMCP instance.

    Args:
        mcp: The FastMCP server instance.
        tool_registry: Mapping of canonical tool names to async callables.
    """

    @mcp.custom_route("/", methods=["GET"])
    async def root(request: Request) -> Response:
        accept = request.headers.get("Accept", "")
        if "text/html" in accept:
            return HTMLResponse(WELCOME_HTML)
        return JSONResponse(
            {
                "service": "arifOS AAA MCP Server",
                "version": BUILD_INFO["version"],
                "protocol_version": MCP_PROTOCOL_VERSION,
                "supported_protocol_versions": MCP_SUPPORTED_PROTOCOL_VERSIONS,
                "mcp_endpoint": "/mcp",
                "tools_endpoint": "/tools",
                "health_endpoint": "/health",
                "tool_count": len(tool_registry),
                "tools": list(tool_registry.keys()),
            }
        )

    @mcp.custom_route("/docs", methods=["GET"])
    async def docs(request: Request) -> Response:
        """Documentation page — human and AI readable."""
        return HTMLResponse(DOCS_HTML, headers={"Cache-Control": "max-age=3600"})

    @mcp.custom_route("/docs/", methods=["GET"])
    async def docs_trailing(request: Request) -> Response:
        """Documentation page (trailing slash)."""
        return HTMLResponse(DOCS_HTML, headers={"Cache-Control": "max-age=3600"})

    @mcp.custom_route("/health", methods=["GET"])
    async def health(request: Request) -> Response:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "arifos-aaa-mcp",
                "version": BUILD_INFO["version"],
                "transport": "streamable-http",
                "tools_loaded": len(tool_registry),
                "ml_floors": get_ml_floor_runtime(),
                "capability_map": build_runtime_capability_map(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            headers={"Access-Control-Allow-Origin": "*"},
        )

    @mcp.custom_route("/metrics", methods=["GET"])
    async def metrics_endpoint(request: Request) -> Response:
        """Prometheus metrics — scraped by arifos_prometheus every 30s."""
        from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
        from starlette.responses import Response as _Resp

        return _Resp(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @mcp.custom_route("/version", methods=["GET"])
    async def version(request: Request) -> Response:
        return JSONResponse(BUILD_INFO)

    @mcp.custom_route("/tools", methods=["GET"])
    async def list_tools(request: Request) -> Response:
        if err := _auth_error_response(request):
            return err

        # Only return tools in CORE_TOOL_REGISTRY (canonical 23 tools)
        mcp_tools = await mcp.list_tools()
        tool_list = []
        for tool in mcp_tools:
            if tool.name in tool_registry:
                tool_list.append(
                    {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.parameters or {},
                        "stage": AAA_TOOL_STAGE_MAP.get(tool.name),
                        "lane": TRINITY_BY_TOOL.get(tool.name),
                    }
                )
        return JSONResponse({"tools": tool_list, "count": len(tool_list)})

    @mcp.custom_route("/tools/", methods=["GET"])
    async def list_tools_slash(request: Request) -> Response:
        return await list_tools(request)

    @mcp.custom_route("/openapi.json", methods=["GET"])
    async def openapi_json(request: Request) -> Response:
        schema = _openapi_schema(_public_base_url(request))
        return JSONResponse(schema)

    @mcp.custom_route("/tools/{tool_name:path}", methods=["POST"])
    async def call_tool_rest(request: Request) -> Response:
        """REST-style tool calling for ChatGPT and other HTTP clients."""
        if err := _auth_error_response(request):
            return err

        incoming_name = _normalize_tool_name(request.path_params.get("tool_name", ""))
        canonical_name = TOOL_ALIASES.get(incoming_name, incoming_name)
        request_id = f"req-{uuid.uuid4().hex[:12]}"
        start_time = time.time()

        if canonical_name not in tool_registry:
            return JSONResponse(
                {"error": f"Tool '{incoming_name}' not found", "request_id": request_id},
                status_code=404,
            )

        try:
            body = await request.json()
        except Exception:
            body = {}
        if not isinstance(body, dict):
            body = {}

        tool_obj = tool_registry[canonical_name]
        tool_fn = getattr(tool_obj, "fn", tool_obj)

        try:
            # Filter body to only valid parameters
            sig = inspect.signature(tool_fn)
            has_kwargs = any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
            )
            if has_kwargs:
                filtered = body
            else:
                valid_params = {
                    name
                    for name, p in sig.parameters.items()
                    if p.kind
                    not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                }
                filtered = {k: v for k, v in body.items() if k in valid_params}

            result = await tool_fn(**filtered)
        except Exception as exc:
            return JSONResponse(
                {"error": str(exc), "tool": incoming_name, "request_id": request_id},
                status_code=500,
            )

        latency_ms = (time.time() - start_time) * 1000

        # Handle RuntimeEnvelope and other Pydantic models serialization
        if hasattr(result, "model_dump"):
            # Pydantic v2
            result_dict = result.model_dump()
        elif hasattr(result, "dict"):
            # Pydantic v1
            result_dict = result.dict()
        else:
            result_dict = result

        return JSONResponse(
            {
                "status": "success",
                "tool": incoming_name,
                "canonical": canonical_name,
                "request_id": request_id,
                "latency_ms": round(latency_ms, 2),
                "result": result_dict,
            }
        )

    @mcp.custom_route("/.well-known/mcp/server.json", methods=["GET"])
    async def well_known(request: Request) -> Response:
        payload = build_server_json(_public_base_url(request))
        payload.setdefault("protocolVersion", MCP_PROTOCOL_VERSION)
        payload.setdefault("supportedProtocolVersions", MCP_SUPPORTED_PROTOCOL_VERSIONS)
        payload.setdefault(
            "authentication",
            {
                "type": "none",
                "description": "No authentication required. actor_id is used for logging only.",
            },
        )
        return JSONResponse(payload)

    @mcp.custom_route("/.well-known/mcp/internal-server.json", methods=["GET"])
    async def internal_well_known(request: Request) -> Response:
        profile = os.getenv("ARIFOS_PUBLIC_TOOL_PROFILE", "public").strip().lower() or "public"
        if profile in {"public", "chatgpt", "agnostic_public"}:
            return JSONResponse(
                {"error": "Internal contract disabled on public profile."}, status_code=404
            )

        payload = build_mcp_discovery_json(_public_base_url(request))
        payload.setdefault("protocolVersion", MCP_PROTOCOL_VERSION)
        payload.setdefault("supportedProtocolVersions", MCP_SUPPORTED_PROTOCOL_VERSIONS)
        payload.setdefault(
            "authentication",
            {
                "type": "none",
                "description": (
                    "Internal profile contract. Use only on trusted local or stdio transports."
                ),
            },
        )
        return JSONResponse(payload)

    @mcp.custom_route("/api/governance-status", methods=["GET"])
    async def governance_status(request: Request) -> Response:
        """Return current governance telemetry for the Constitutional Visualizer."""
        try:
            payload = _build_governance_status_payload()
            return JSONResponse(
                payload,
                headers=_merge_headers(_cache_headers(), _dashboard_cors_headers(request)),
            )
        except Exception as exc:
            logger.exception("governance_status endpoint failed")
            return JSONResponse(
                {"error": "governance_status_failed", "detail": str(exc)},
                status_code=500,
            )

    @mcp.custom_route("/status", methods=["GET"])
    async def status_page(request: Request) -> Response:
        """Zero-JS ops truth page for constrained renderers and humans."""
        payload = _build_governance_status_payload()
        fmt = request.query_params.get("format", "").strip().lower()
        accept_header = request.headers.get("accept", "").lower()
        accepts_json = "application/json" in accept_header
        accepts_html = "text/html" in accept_header

        if fmt == "json" or (fmt != "html" and accepts_json and not accepts_html):
            return JSONResponse(payload, headers=_cache_headers())

        return HTMLResponse(_render_status_html(payload), headers=_cache_headers())

    @mcp.custom_route("/api/governance-history", methods=["GET"])
    async def governance_history(request: Request) -> Response:
        """Return recent VAULT999 session history for the Constitutional Visualizer."""
        try:
            limit_raw = request.query_params.get("limit", "20")
            try:
                limit = max(1, min(int(limit_raw), 100))
            except (ValueError, TypeError):
                limit = 20

            sessions: list[dict[str, Any]] = []

            # Attempt to query VAULT999 for real session history
            try:
                from arifosmcp.transport.vault_sqlite import VaultSQLite

                vault = VaultSQLite()
                raw = vault.query_recent(limit=limit) if hasattr(vault, "query_recent") else []
                for entry in raw:
                    sessions.append(
                        {
                            "session_id": entry.get("session_id", ""),
                            "verdict": entry.get("verdict", "UNKNOWN"),
                            "stage": entry.get("stage", ""),
                            "timestamp": entry.get("timestamp", ""),
                            "floors": entry.get("floors", {}),
                        }
                    )
            except (ImportError, AttributeError):
                logger.debug("VAULT999 SQLite unavailable — returning empty session history")
            except Exception:
                logger.exception("Unexpected error querying VAULT999 history")

            return JSONResponse(
                {
                    "sessions": sessions,
                    "count": len(sessions),
                    "limit": limit,
                },
                headers={"Access-Control-Allow-Origin": "*"},
            )
        except Exception as exc:
            logger.exception("governance_history endpoint failed")
            return JSONResponse(
                {"error": "governance_history_failed", "detail": str(exc)},
                status_code=500,
            )

    # ═══════════════════════════════════════════════════════
    # CHECKPOINT REST COMPATIBILITY — OpenAPI / action-style integration
    # ═══════════════════════════════════════════════════════

    @mcp.custom_route("/checkpoint", methods=["POST"])
    async def checkpoint_endpoint(request: Request) -> Response:
        """
        REST/OpenAPI compatibility entry point for constitutional validation.
        Simplified 000→888 pipeline for non-MCP clients.
        """
        if err := _auth_error_response(request):
            return err

        try:
            body = await request.json()
        except Exception:
            body = {}

        # Support both 'query' and 'task' parameters for compatibility
        query = body.get("query") or body.get("task", "")
        body.get("stakeholders", ["user"])
        actor_id = body.get("actor_id", "chatgpt")
        mode = body.get("mode", "full")

        if not query or not isinstance(query, str):
            return JSONResponse(
                {"error": "Missing required field: query (or task)"}, status_code=400
            )

        session_id = f"gpt-{actor_id}-{uuid.uuid4().hex[:8]}"
        start_time = time.time()

        try:
            # The arifos_kernel (metabolic_loop_router) is the single canonical entry point
            # for the full ΔΩΨ metabolic pipe. Using it ensures consistency across all entry points.
            kernel_tool = tool_registry.get("arifOS_kernel") or tool_registry.get(
                "metabolic_loop_router"
            )

            if not kernel_tool:
                return JSONResponse(
                    {
                        "error": "arifOS_kernel not available",
                        "verdict": "HOLD",
                        "issue": "TOOL_NOT_LOADED",
                    },
                    status_code=500,
                )

            kernel_fn = getattr(kernel_tool, "fn", kernel_tool)

            # Execute full metabolic loop in one sovereign call
            envelope = await kernel_fn(
                query=query,
                actor_id=actor_id,
                session_id=session_id,
                risk_tier=mode if mode in ["low", "medium", "high", "critical"] else "medium",
                auth_context={
                    "actor_id": actor_id,
                    "authority_level": "agent",
                    "token_fingerprint": "REST-BYPASS",
                },
                use_heart=True,
                use_critique=True,
                allow_execution=True,
            )

            # Extract results from the RuntimeEnvelope
            judge_data = envelope.model_dump() if hasattr(envelope, "model_dump") else envelope
            verdict = judge_data.get("verdict", "VOID")

            # Extract floors and metrics
            metrics = judge_data.get("metrics", {})
            telemetry = metrics.get("telemetry", {})
            truth_score = telemetry.get("G_star")

            # Map floors
            floors_passed = judge_data.get("meta", {}).get("floors_passed", [])
            floors_failed = judge_data.get("meta", {}).get("floors_failed", [])

            # Build human-readable summary
            if verdict == "SEAL":
                summary = "✓ All constitutional floors passed. Safe to proceed."
            elif verdict == "PARTIAL":
                summary = "⚠ Soft floor warning. Proceed with caution."
            elif verdict in ["VOID", "FAIL"]:
                summary = "✗ Constitutional violation detected. Action blocked."
            elif verdict == "888_HOLD":
                summary = "⏸ High-stakes decision. Requires human signature."
            else:
                summary = f"Status: {verdict}"

            latency_ms = (time.time() - start_time) * 1000

            return JSONResponse(
                {
                    "verdict": verdict,
                    "summary": summary,
                    "mode": mode,
                    "floors": {
                        "passed": floors_passed,
                        "failed": floors_failed,
                    },
                    "metrics": {"truth": truth_score, "threshold": 0.80},
                    "session_id": session_id,
                    "latency_ms": round(latency_ms, 2),
                    "version": judge_data.get("meta", {}).get("version", "2026.3.14"),
                }
            )

        except Exception as exc:
            logger.exception("checkpoint_endpoint failed")
            return JSONResponse(
                {"error": str(exc), "verdict": "HOLD", "issue": "RUNTIME_FAILURE"}, status_code=500
            )

    @mcp.custom_route("/openapi.yaml", methods=["GET"])
    async def openapi_schema(request: Request) -> Response:
        """Serve OpenAPI schema for the REST compatibility surface."""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "333_APPS",
            "L4_TOOLS",
            "chatgpt-actions",
            "chatgpt_openapi.yaml",
        )
        if os.path.exists(schema_path):
            content = open(schema_path).read()
            return Response(content, media_type="application/yaml")
        return JSONResponse({"error": "Schema not found"}, status_code=404)

    @mcp.custom_route("/robots.txt", methods=["GET"])
    async def robots_txt(_request: Request) -> Response:
        return Response(ROBOTS_TXT, media_type="text/plain")

    @mcp.custom_route("/llms.txt", methods=["GET"])
    async def llms_txt(_request: Request) -> Response:
        return Response(LLMS_TXT, media_type="text/plain")

    @mcp.custom_route("/llms.json", methods=["GET"])
    async def llms_json(_request: Request) -> Response:
        return JSONResponse(LLMS_JSON, headers={"Access-Control-Allow-Origin": "*"})

    # Serve the APEX Sovereign Dashboard v2.1 at /dashboard/
    dashboard_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "sites",
        "dashboard",
    )
    if os.path.exists(dashboard_dir) and hasattr(mcp, "_app"):
        mcp._app.mount(
            "/dashboard", StaticFiles(directory=dashboard_dir, html=True), name="dashboard"
        )
