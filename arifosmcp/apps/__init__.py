"""
arifosmcp/apps — FastMCP Prefab UI Apps for arifOS.

Human-interface layer: concise APEX G-score metrics, stage pipeline,
philosophy quotes, and constitutional floor explanations rendered as
interactive Prefab UI iframes inside the MCP host conversation.

Apps
----
apex_score_app       — APEX G-score panel: stage, metrics, philosophy, verdict
stage_pipeline_app   — 000→999 Sacred Chain visualiser with per-stage status

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from .apex_score import apex_score_app
from .stage_pipeline import stage_pipeline_app

__all__ = [
    "apex_score_app",
    "stage_pipeline_app",
]
