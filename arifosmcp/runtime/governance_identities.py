"""
governance_identities.py — Protected Sovereign Identity Registry (F11/F13)

Defines protected sovereign IDs that require cryptographic proof or explicit
human approval before session anchoring is permitted.
"""

from __future__ import annotations

# P0: Protected Sovereign IDs (F11 Identity Hardening)
# These IDs cannot be claimed without:
# 1. Valid cryptographic proof (signed token), OR
# 2. Explicit human_approval flag with acknowledgment
PROTECTED_SOVEREIGN_IDS: set[str] = {
    "arif",
    "ariffazil",
    "sovereign",
    "admin",
    "root",
    "system",
    "arif-fazil",
    "arif_fazil",
    "muhammad_arif",
}


# P0: Identity claim validation
def is_protected_sovereign_id(actor_id: str | None) -> bool:
    """Check if actor_id is a protected sovereign identity."""
    if not actor_id or actor_id == "anonymous":
        return False
    return actor_id.lower() in PROTECTED_SOVEREIGN_IDS


# P0: Proof validation helper (placeholder for cryptographic verification)
def validate_sovereign_proof(actor_id: str, proof: dict | None) -> bool:
    """
    Validate cryptographic proof for protected sovereign ID.

    TODO: Implement actual cryptographic signature verification
    using governance secret and nonce challenge-response.
    """
    if not proof:
        return False

    # Placeholder: Check for required proof fields
    required_fields = ["signature", "nonce", "timestamp"]
    if not all(field in proof for field in required_fields):
        return False

    # TODO: Add actual signature verification here
    # For now, reject all unsigned claims of protected IDs
    return False
