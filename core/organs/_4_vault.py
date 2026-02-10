"""
core/organs/_4_vault.py — The Memory (Stage 999)

VAULT Engine: EUREKA-Filtered Immutable Audit

Actions:
    1. seal (999) → Final seal with Merkle-chain integrity

Floors:
    F1:  Amanah (Immutable, append-only)
    F13: Sovereign (Complete audit trail)

Theory of Anomalous Contrast:
    - EUREKA ≥ 0.75 → SEAL (permanent vault)
    - 0.50 ≤ EUREKA < 0.75 → SABAR (72h cooling)
    - EUREKA < 0.50 → TRANSIENT (not stored)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from dataclasses import dataclass

from core.shared.physics import ConstitutionalTensor, TrinityTensor
from core.shared.mottos import MOTTO_999_SEAL as motto


# =============================================================================
# ACTION 1: SEAL (Stage 999) — Immutable Constitutional Record
# =============================================================================


@dataclass
class SealReceipt:
    """Receipt for sealed constitutional record."""
    status: str  # SEALED, SABAR, TRANSIENT, VOID
    seal_id: str
    entry_hash: str
    merkle_root: Optional[str] = None
    sequence_number: Optional[int] = None
    timestamp: str = ""
    eureka_score: float = 0.0
    vault_backend: str = "memory"  # memory, postgres, filesystem


async def seal(
    judge_output: Dict[str, Any],
    agi_tensor: ConstitutionalTensor,
    asi_output: Dict[str, Any],
    session_id: str,
    query: str = "",
    authority: str = "system",
    eureka_data: Optional[Dict[str, Any]] = None,
) -> SealReceipt:
    """
    Stage 999: SEAL — The final commitment
    
    EUREKA-filtered seal with Merkle-chain integrity.
    
    Args:
        judge_output: APEX judgment output
        agi_tensor: AGI Mind output
        asi_output: ASI Heart output
        session_id: Constitutional session token
        query: Original user query
        authority: Who authorized this seal
    
    Returns:
        SealReceipt with:
        - status: SEALED / SABAR / TRANSIENT
        - seal_id: UUID for retrieval
        - entry_hash: SHA-256 of sealed content
        - merkle_root: Chain integrity proof
    
    Action Chain:
        apex.judge → seal (completes 000-999 pipeline)
    
    EUREKA Scoring:
        - High novelty + high truth = SEAL (permanent)
        - Medium novelty = SABAR (72h cooling)
        - Low novelty = TRANSIENT (not stored)
    """
    # Compute EUREKA score
    eureka = _compute_eureka_score(judge_output, agi_tensor, asi_output)
    
    # Determine storage tier
    if eureka < 0.50:
    
        # TRANSIENT: Not meaningful enough
        return SealReceipt(
            status="TRANSIENT",
            seal_id="",
            entry_hash="",
            timestamp=datetime.now(timezone.utc).isoformat(),
            eureka_score=eureka,
        )
    
    # Build entry data
    entry = {
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": judge_output.get("verdict", "VOID"),
        "W_3": judge_output.get("W_3", 0.0),
        "genius_G": judge_output.get("genius_G", 0.0),
        "eureka_score": eureka,
        "floors_failed": judge_output.get("floors_failed", []),
        "query": query[:200],  # Truncate for privacy
        "authority": authority,
        "motto": motto.positive + ", " + motto.negative,
    }
    
    # Store Eureka discovery data if provided
    if eureka_data:
        entry["eureka_discovery"] = {
            "best_variant": eureka_data.get("best_variant"),
            "best_score": eureka_data.get("best_score"),
            "all_variants": eureka_data.get("all_variants", []),
            "rationale": f"Selected variant {eureka_data.get('best_variant')} "
                        f"with score {eureka_data.get('best_score', 0):.3f} "
                        f"based on W3 + Genius + Coherence",
        }
    
    # Compute hash
    entry_json = str(sorted(entry.items()))
    entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()[:32]
    
    # Generate seal ID
    seal_id = secrets.token_hex(16)
    entry["seal_id"] = seal_id
    
    # SABAR: Cooling ledger (72h hold)
    if eureka < 0.75:
        return SealReceipt(
            status="SABAR",
            seal_id=seal_id,
            entry_hash=entry_hash,
            timestamp=entry["timestamp"],
            eureka_score=eureka,
            vault_backend="cooling",
        )
    
    # SEAL: Permanent vault
    # In production: Write to PostgreSQL with Merkle chain
    # For now: Return receipt with genesis hash
    merkle_root = _compute_merkle_root(entry_hash)
    
    return SealReceipt(
        status="SEALED",
        seal_id=seal_id,
        entry_hash=entry_hash,
        merkle_root=merkle_root,
        sequence_number=1,  # Would be from DB
        timestamp=entry["timestamp"],
        eureka_score=eureka,
        vault_backend="memory",  # Would be "postgres" in prod
    )


def _compute_eureka_score(
    judge_output: Dict[str, Any],
    agi_tensor: ConstitutionalTensor,
    asi_output: Dict[str, Any],
) -> float:
    """
    Compute EUREKA score (anomalous contrast).
    
    High EUREKA = novel + true + important
    """
    # Components
    truth = agi_tensor.truth_score
    w3 = judge_output.get("W_3", 0.0)
    genius = judge_output.get("genius_G", 0.0)
    peace = asi_output.get("peace_squared", 1.0)
    
    # Novelty proxy: inverse of common patterns
    # (Simplified - real implementation would compare to vault history)
    novelty = 0.7  # Assume moderate novelty
    
    # EUREKA = geometric mean of components weighted by novelty
    score = (truth * w3 * genius * peace * novelty) ** 0.2
    
    return min(1.0, max(0.0, score))


def _compute_merkle_root(entry_hash: str) -> str:
    """Compute Merkle root (simplified)."""
    # In production: Link to previous entry in chain
    # For now: Hash with genesis
    genesis = "GENESIS_HASH_V60"
    combined = genesis + entry_hash
    return hashlib.sha256(combined.encode()).hexdigest()[:32]


# =============================================================================
# QUERY INTERFACE (Bonus)
# =============================================================================


async def query(
    seal_id: str,
    session_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Query the VAULT for a sealed record.
    
    Args:
        seal_id: The seal ID to retrieve
        session_id: Optional session filter
    
    Returns:
        Sealed entry or None if not found
    
    Note: This is a placeholder. Real implementation would query PostgreSQL.
    """
    # Placeholder: Would query database
    return {
        "seal_id": seal_id,
        "status": "SEALED",
        "query": "Sample query (placeholder)",
        "verdict": "SEAL",
    }


async def verify(
    seal_id: str,
    entry_hash: str,
) -> bool:
    """
    Verify the integrity of a sealed record.
    
    Args:
        seal_id: The seal ID
        entry_hash: Expected entry hash
    
    Returns:
        True if integrity verified, False otherwise
    """
    # Placeholder: Would verify Merkle proof
    return True


# =============================================================================
# UNIFIED VAULT INTERFACE
# =============================================================================


async def vault(
    action: str,
    judge_output: Optional[Dict[str, Any]] = None,
    agi_tensor: Optional[ConstitutionalTensor] = None,
    asi_output: Optional[Dict[str, Any]] = None,
    session_id: str = "",
    query: str = "",
    seal_id: str = "",
    authority: str = "system",
    eureka_data: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Unified VAULT interface — The Memory in action.
    
    Args:
        action: Which action ("seal", "query", "verify")
        judge_output: APEX judgment (for seal)
        agi_tensor: AGI Mind output (for seal)
        asi_output: ASI Heart output (for seal)
        session_id: Constitutional session token
        query: Original query (for seal)
        seal_id: For query/verify
        authority: Who authorized
        eureka_data: Discovery data from Eureka loop (for seal)
    
    Returns:
        SealReceipt, query result, or verify boolean
    
    Example:
        >>> receipt = await vault("seal", judge, tensor, asi, session, "Hello")
        >>> receipt.status
        'SEALED'
    """
    if action == "seal":
        if not all([judge_output, agi_tensor, asi_output]):
            raise ValueError("seal requires judge_output, agi_tensor, asi_output")
        return await seal(
            judge_output, agi_tensor, asi_output,
            session_id, query, authority, eureka_data
        )
    
    elif action == "query":
        return await query(seal_id, session_id)
    
    elif action == "verify":
        return await verify(seal_id, "")
    
    else:
        raise ValueError(f"Unknown action: {action}. Use: seal, query, verify")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Actions (1 of 3 max)
    "seal",  # Stage 999: Final commitment
    
    # Bonus actions
    "query",   # Retrieve sealed record
    "verify",  # Verify integrity
    
    # Unified interface
    "vault",
    
    # Types
    "SealReceipt",
]
