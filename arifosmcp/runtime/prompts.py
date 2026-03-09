"""
arifosmcp/runtime/prompts.py — arifOS Prompt Templates

Public prompts for the semantic arifOS tool surface.
Register via register_prompts(mcp).

These prompts guide LLMs to call the right tool with correct parameters,
keeping the canonical JSON Schema contract in the conversation context.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Wire the core 7 arifOS prompts onto *mcp*."""

    @mcp.prompt()
    def arifos_kernel_prompt(query: str, risk_tier: str = "medium") -> str:
        """Guide the LLM to use the core constitutional intelligence engine."""
        return (
            f"Use 'arifOS.kernel' as the core constitutional intelligence engine "
            f"for the following query:\n\n"
            f"  Query: {query}\n"
            f"  Risk tier: {risk_tier}\n\n"
            f"The kernel is the semantic execution authority of arifOS. "
            f"It may orchestrate internal reasoning, memory, judgment, and vault stages, "
            f"but externally it should be treated as the governed execution layer."
        )

    @mcp.prompt()
    def search_reality_prompt(query: str) -> str:
        """Guide the LLM to discover external facts."""
        return (
            f"Use 'search_reality' to find real-world sources and evidence "
            f"before reasoning about:\n\n"
            f"  Topic: {query}\n\n"
            f"This provides high-entropy grounding for F2 Truth floors."
        )

    @mcp.prompt()
    def ingest_evidence_prompt(url: str) -> str:
        """Guide the LLM to load a source for analysis."""
        return (
            f"Use 'ingest_evidence' to load and analyze content from:\n\n"
            f"  URL: {url}\n\n"
            f"This ingests the source into the reasoning context as validated evidence."
        )

    @mcp.prompt()
    def session_memory_prompt(operation: str, content: str | None = None) -> str:
        """Guide the LLM to manage session context."""
        return (
            f"Use 'session_memory' to {operation} context for the current session.\n"
            f"Content to process: {content or 'N/A'}\n\n"
            f"Operations: store | retrieve | forget | search."
        )

    @mcp.prompt()
    def audit_rules_prompt() -> str:
        """Guide the LLM to inspect the constitutional floors."""
        return (
            "Use 'audit_rules' to inspect the 13 constitutional floors (F1-F13) "
            "and verify current system logic against the Law."
        )

    @mcp.prompt()
    def check_vital_prompt() -> str:
        """Guide the LLM to check system health and metrics."""
        return (
            "Use 'check_vital' to monitor kernel health, reporting G★, η, "
            "entropy delta, and sovereign status."
        )

    @mcp.prompt()
    def open_apex_dashboard_prompt() -> str:
        """Guide the LLM to open the monitoring dashboard."""
        return (
            "Use 'open_apex_dashboard' to view the live APEX constitutional dashboard, "
            "displaying pipeline traces, floor scores, and telemetry."
        )
