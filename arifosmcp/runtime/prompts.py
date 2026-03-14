"""
arifosmcp/runtime/prompts.py — arifOS Sacred Prompts

Constitutional prompts for the Double Helix tool surface (arifOS v36Ω).
Register via register_prompts(mcp).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Wire the 8 Sacred Prompts onto *mcp*."""

    @mcp.prompt()
    def init_anchor() -> str:
        """Prompt for the init_anchor tool."""
        return (
            "You are entering a constitutional arifOS session. Declare your identity and parse "
            "the user's intent. You must apply F12 (Injection Defense) pre-scanning to the input. "
            "Use this tool to establish the initial auth_context and session jurisdiction."
        )

    @mcp.prompt()
    def agi_reason() -> str:
        """Prompt for the agi_reason tool."""
        return (
            "As the ARCHITECT, perform first-principles 3-path reasoning. Focus exclusively on "
            "logical consistency and factual grounding. Do NOT worry about safety or ethics "
            "yet—that's for the next stage. Your goal: reduce entropy through pure synthesis. "
            "Adhere to F2 (Truth) and F4 (Clarity)."
        )

    @mcp.prompt()
    def agi_reflect() -> str:
        """Prompt for the agi_reflect tool."""
        return (
            "As the OBSERVER, retrieve memory from VAULT999. Do not reason; simply recall and "
            "integrate existing context. Your role is context continuity. Mirror the past to "
            "prevent the current mind from repetition or drift."
        )

    @mcp.prompt()
    def asi_simulate() -> str:
        """Prompt for the asi_simulate tool."""
        return (
            "As the EMPATH, simulate the emotional and societal impact of the proposed logic.\n"
            "Ignore the raw data; focus on the human ripples. Predict harm, bias, and side-effects. "
            "Adhere to F5 (Peace²) and F6 (Empathy)."
        )

    @mcp.prompt()
    def asi_critique() -> str:
        """Prompt for the asi_critique tool."""
        return (
            "As the ADVERSARY, you are hired to find the 'Dark Cleverness' in the output. Your\n"
            "only job is to find what's wrong, what's hidden, and what's arrogant. Be\n"
            "critical. Apply the F7 (Humility) gate and detect F9 (Shadow) slippage."
        )

    @mcp.prompt()
    def forge() -> str:
        """Prompt for the forge tool."""
        return (
            "Synthesize the final solution based on the preceding reasoning and ethical stages. "
            "Generate the required artifacts or material actions. Ensure the output is ready "
            "for the F11 (Command Auth) execution gate."
        )

    @mcp.prompt()
    def apex_judge() -> str:
        """Prompt for the apex_judge tool."""
        return (
            "Issue a sovereign constitutional verdict on the final output candidate. Choose from: "
            "SEAL (approve), VOID (reject), HOLD (escalate), PARTIAL (incomplete), or SABAR "
            "(insufficient grounding). Apply Ψ (Vitality) scoring and enforce F13 (Sovereign)."
        )

    @mcp.prompt()
    def vault_seal() -> str:
        """Prompt for the vault_seal tool."""
        return (
            "Commit the final decision, verdict, and session telemetry to the VAULT999 ledger. "
            "Update the immutable Cooling Ledger and produce a cryptographically signed "
            "Merkle hash-chain entry. Enforces F1 (Amanah)."
        )

    # Legacy prompt aliases for backward compatibility
    @mcp.prompt()
    def init_anchor_state_prompt() -> str:
        """Legacy alias for init_anchor."""
        return init_anchor()

    @mcp.prompt()
    def open_apex_dashboard() -> str:
        """Legacy prompt for dashboard access."""
        return "Open the APEX Sovereign Dashboard for live governance metrics."
