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
            "You are entering a constitutional session. Declare identity, parse intent, "
            "apply F12 pre-scan."
        )

    @mcp.prompt()
    def agi_reason() -> str:
        """Prompt for the agi_reason tool."""
        return (
            "Perform 3-path reasoning: conservative, exploratory, adversarial. Maintain Δ clarity."
        )

    @mcp.prompt()
    def agi_reflect() -> str:
        """Prompt for the agi_reflect tool."""
        return (
            "Retrieve sealed evidence from Vault999. Interpret memory as mirror, not as raw recall."
        )

    @mcp.prompt()
    def asi_simulate() -> str:
        """Prompt for the asi_simulate tool."""
        return (
            "Simulate consequences. Predict outcomes. Apply Ω humility and ΔS thermodynamic checks."
        )

    @mcp.prompt()
    def asi_critique() -> str:
        """Prompt for the asi_critique tool."""
        return "Evaluate uncertainty. Detect blind spots. Apply F7 humility gate."

    @mcp.prompt()
    def forge() -> str:
        """Prompt for the forge tool."""
        return "Synthesize solutions. Generate artifacts. Apply F11 execution gate."

    @mcp.prompt()
    def apex_judge() -> str:
        """Prompt for the apex_judge tool."""
        return "Issue sovereign verdict: SEAL, VOID, HOLD, PARTIAL, SABAR. Apply Ψ vitality."

    @mcp.prompt()
    def vault_seal() -> str:
        """Prompt for the vault_seal tool."""
        return "Commit to Vault999. Update Cooling Ledger. Produce immutable hash-chain entry."

    # Legacy prompt aliases for backward compatibility
    @mcp.prompt()
    def init_anchor_state_prompt() -> str:
        """Legacy alias for init_anchor."""
        return init_anchor()

    @mcp.prompt()
    def open_apex_dashboard() -> str:
        """Legacy prompt for dashboard access."""
        return "Open the APEX Sovereign Dashboard for live governance metrics."
