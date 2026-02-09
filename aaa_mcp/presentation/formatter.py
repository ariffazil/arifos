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
    - user: slim, stable envelope (answer/risk/need + error)
    """
    if mode == "debug":
        return payload

    # Non-dict outputs: keep as-is (e.g., resources returning text)
    if not isinstance(payload, dict):
        return payload

    verdict = payload.get("verdict") or payload.get("status")
    out: Dict[str, Any] = {}

    # Stable envelope keys
    for k in ("verdict", "status", "session_id", "stage", "seal_id", "hash", "error"):
        if k in payload:
            out[k] = payload.get(k)

    # Common failure/repair info
    for k in ("reason", "justification", "blocked_by", "warnings"):
        if k in payload and payload.get(k) not in (None, "", [], {}):
            out[k] = payload.get(k)

    # Prefer a single human-facing answer field if present
    answer = _pick_first(payload, ("answer", "response", "result", "solution", "solution_draft"))
    if isinstance(answer, str) and answer.strip():
        out["answer"] = answer

    # Keep minimal evidence in audit mode, or when not SEALED/SEAL
    include_constitutional = mode == "audit" or str(verdict).upper() not in {"SEAL", "SEALED"}
    if include_constitutional and "_constitutional" in payload:
        out["_constitutional"] = payload.get("_constitutional")

    if mode == "audit" or tool_name == "reality_search":
        if "evidence" in payload:
            out["evidence"] = _slim_evidence(payload.get("evidence"))
        # Reality grounding: keep a small slice of results if present
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
            out["results"] = slim_results

    out["meta"] = {"output_mode": mode, "tool": tool_name}
    return out

