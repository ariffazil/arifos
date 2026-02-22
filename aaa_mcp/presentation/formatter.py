from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional


def resolve_output_mode(kwargs: Dict[str, Any] | None = None) -> str:
    """
    Resolve desired output mode.

    Precedence:
    1) Explicit tool arg `output_mode`
    2) Env var `AAA_MCP_OUTPUT_MODE`
    3) Default: "user"
    """
    kwargs = kwargs or {}
    mode = kwargs.get("output_mode") or os.getenv("AAA_MCP_OUTPUT_MODE", "user")
    mode = str(mode).strip().lower()
    if mode in {"debug", "internal", "dev"}:
        return "debug"
    if mode in {"audit", "compliance"}:
        return "audit"
    return "user"


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "…"


def _slim_evidence(evidence: Any, limit: int = 3) -> List[Dict[str, Any]]:
    if not isinstance(evidence, list):
        return []
    slim: List[Dict[str, Any]] = []
    for item in evidence[:limit]:
        if not isinstance(item, dict):
            continue
        content = item.get("content") if isinstance(item.get("content"), dict) else {}
        source_meta = item.get("source_meta") if isinstance(item.get("source_meta"), dict) else {}
        metrics = item.get("metrics") if isinstance(item.get("metrics"), dict) else {}
        text = content.get("text", "")
        if not isinstance(text, str):
            text = str(text)
        slim.append(
            {
                "evidence_id": item.get("evidence_id"),
                "type": source_meta.get("type"),
                "uri": source_meta.get("uri"),
                "text": _truncate(text, 300),
                "trust_weight": metrics.get("trust_weight"),
            }
        )
    return slim


def _pick_first(payload: Dict[str, Any], keys: Iterable[str]) -> Optional[Any]:
    for k in keys:
        if k in payload:
            return payload.get(k)
    return None


def format_tool_output(tool_name: str, payload: Any, mode: str) -> Any:
    """
    Format tool output for UX.

    - debug: return full payload (developer ergonomics)
    - audit: include constitutional metadata + evidence summaries
    - user: MCP-compliant format with content + structuredContent

    Per auditor feedback v60: Always include _constitutional for governance audit trail.
    """
    if mode == "debug":
        return payload

    # Non-dict outputs: keep as-is (e.g., resources returning text)
    if not isinstance(payload, dict):
        return payload

    verdict = payload.get("verdict") or payload.get("status")
    stage = payload.get("stage", "000")
    session_id = payload.get("session_id", "unknown")

    # Build human-friendly message
    message = payload.get("message", "")
    if not message:
        # Default message based on stage/verdict
        stage_names = {
            "000": "Init Gate",
            "111": "AGI Sense",
            "222": "AGI Think",
            "333": "AGI Reason",
            "444": "Trinity Sync",
            "555": "ASI Empathize",
            "666": "ASI Align",
            "777": "Forge",
            "888": "Apex Verdict",
            "999": "Vault Seal",
        }
        stage_name = stage_names.get(stage, f"Stage {stage}")
        if str(verdict).upper() == "SEAL":
            message = f"{stage_name} complete. Verdict: SEAL."
        else:
            message = f"{stage_name} blocked. Verdict: {verdict}."

    # Determine next_action for orchestrators
    next_action_map = {
        "000": "PROCEED_TO_111_SENSE",
        "111": "PROCEED_TO_222_THINK",
        "222": "PROCEED_TO_333_REASON",
        "333": "PROCEED_TO_444_EMPATHY",
        "444": "PROCEED_TO_555_ALIGN",
        "555": "PROCEED_TO_666_ALIGN",
        "666": "PROCEED_TO_777_FORGE",
        "777": "PROCEED_TO_888_JUDGE",
        "888": "PROCEED_TO_999_SEAL" if str(verdict).upper() == "SEAL" else "HALT_REVIEW_VERDICT",
        "999": "PIPELINE_COMPLETE",
    }
    next_action = next_action_map.get(stage, "UNKNOWN")
    if str(verdict).upper() != "SEAL":
        next_action = "HALT_REVIEW_CONSTITUTIONAL_BLOCK"

    # Build structured content (machine/governance layer)
    structured_content: Dict[str, Any] = {
        "tool": tool_name,
        "stage": stage,
        "session_id": session_id,
        "status": payload.get("status", "OK"),
        "verdict": verdict,
        "next_action": next_action,
    }

    # Add constitutional details (ALWAYS for audit trail)
    if "_constitutional" in payload:
        structured_content["_constitutional"] = payload.get("_constitutional")

    # Add data fields
    data_fields = [
        "data",
        "intent",
        "lane",
        "requires_grounding",
        "truth_score",
        "confidence",
        "empathy_score",
        "stakeholder_count",
        "is_reversible",
        "risk_level",
        "seal_id",
        "seal_hash",
        "mode",
        "grounding_required",
    ]
    for field in data_fields:
        if field in payload:
            structured_content[field] = payload.get(field)

    # Add failure/repair info
    for k in ("reason", "justification", "blocked_by", "warnings"):
        if k in payload and payload.get(k) not in (None, "", [], {}):
            structured_content[k] = payload.get(k)

    # Add motto/bookend for INIT (000) and SEAL (999)
    if stage == "000":
        structured_content["motto"] = "🔨⚒️🛠️ DITEMPA, BUKAN DIBERI"
        structured_content["motto_english"] = "Forged, Not Given"
        structured_content["bookend"] = "INIT"
    elif stage == "999":
        structured_content["motto"] = "💎🧠🔒 DITEMPA, BUKAN DIBERI"
        structured_content["motto_english"] = "Forged, Not Given"
        structured_content["bookend"] = "SEAL"

    # Add slim evidence in audit mode
    if mode == "audit" or tool_name == "reality_search":
        if "evidence" in payload:
            structured_content["evidence"] = _slim_evidence(payload.get("evidence"))
        results = payload.get("results")
        if isinstance(results, list) and results:
            slim_results = []
            for r in results[:3]:
                if not isinstance(r, dict):
                    continue
                slim_results.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("url") or r.get("link") or r.get("uri") or "",
                        "snippet": _truncate(str(r.get("snippet", "")), 300),
                        "rank": r.get("rank"),
                    }
                )
            structured_content["results"] = slim_results

    # Build MCP-compliant output with content + structuredContent
    # AUDIT_MARKER_v60: New format per external auditor feedback
    out: Dict[str, Any] = {
        "_format_version": "v60-MCP-AUDIT",
        "content": [{"type": "text", "text": message}],
        "structuredContent": structured_content,
        "meta": {"output_mode": mode, "tool": tool_name},
    }

    return out
