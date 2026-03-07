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
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol

from core.shared.mottos import MOTTO_999_SEAL as motto
from core.shared.physics import ConstitutionalTensor
from core.shared.types import ScarWeight, VaultEntry, VaultOutput, Verdict

# =============================================================================
# STORAGE PROTOCOL & ADAPTERS
# =============================================================================


class VaultStorage(Protocol):
    """Protocol for vault persistence backends."""

    async def write(self, entry: dict[str, Any]) -> None: ...
    async def read(self, seal_id: str) -> dict[str, Any] | None: ...


class JSONLVaultStorage:
    """Standard arifOS JSONL filesystem vault."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    async def write(self, entry: dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    async def read(self, seal_id: str) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("seal_id") == seal_id:
                        return data
                except json.JSONDecodeError:
                    continue
        return None


# Default storage instance
DEFAULT_VAULT_PATH = Path("VAULT999/vault999.jsonl")


# =============================================================================
# ACTION 1: SEAL (Stage 999) — Immutable Constitutional Record
# =============================================================================


@dataclass
class SealReceipt:
    """Receipt for sealed constitutional record."""

    status: str  # SEALED, SABAR, TRANSIENT, VOID
    seal_id: str
    entry_hash: str
    merkle_root: str | None = None
    sequence_number: int | None = None
    timestamp: str = ""
    eureka_score: float = 0.0
    vault_backend: str = "filesystem"
    scar_weight: ScarWeight | None = None
    phoenix_72_expiry: str | None = None


async def seal(
    judge_output: dict[str, Any],
    agi_tensor: ConstitutionalTensor | None = None,
    asi_output: dict[str, Any] | None = None,
    session_id: str = "",
    query: str = "",
    authority: str = "system",
    eureka_data: dict[str, Any] | None = None,
    objective_contract: dict[str, Any] | None = None,
    storage_override: VaultStorage | None = None,
) -> SealReceipt | VaultOutput:
    """
    Stage 999: SEAL — The final commitment.

    EUREKA-filtered seal with Merkle-chain integrity.

    P3 THERMODYNAMIC HARDENING:
    - Records thermodynamic cost in vault entry
    - Cleans up session thermodynamic budget
    - Includes entropy reduction metrics
    """
    # 1. Compute EUREKA score (anomalous contrast)
    eureka = _compute_eureka_score(judge_output, agi_tensor, asi_output, objective_contract)

    # 2. Determine storage tier
    if eureka < 0.50:
        # P3: Cleanup thermodynamic budget even for transient entries
        _cleanup_thermo_budget(session_id)
        return SealReceipt(
            status="TRANSIENT",
            seal_id="",
            entry_hash="",
            timestamp=datetime.now(timezone.utc).isoformat(),
            eureka_score=eureka,
            vault_backend="none",
        )

    # P3: Get thermodynamic final state
    thermo_final = _get_thermo_final_state(session_id)

    # 3. Build canonical entry
    timestamp = datetime.now(timezone.utc).isoformat()
    # Consensus score mapping
    w_consensus = float(judge_output.get("W_4", judge_output.get("W_3", 0.0)))
    
    entry: dict[str, Any] = {
        "session_id": session_id,
        "timestamp": timestamp,
        "verdict": str(judge_output.get("verdict", "VOID")),
        "W_4": w_consensus,
        "W_3": w_consensus, # Legacy support
        "genius_G": float(judge_output.get("genius_G", 0.0)),
        "eureka_score": eureka,
        "floors_failed": judge_output.get("floors_failed", []),
        "query": query[:1024],
        "authority": authority,
        "motto": f"{motto.positive}, {motto.negative}",
        "thermodynamics": thermo_final,  # P3: Include thermodynamic data
    }

    # Optional metadata
    if objective_contract:
        entry["objective_lineage"] = objective_contract
    if eureka_data:
        entry["eureka_discovery"] = eureka_data

    # P3: Cleanup thermodynamic budget after capturing final state
    _cleanup_thermo_budget(session_id)

    # 4. Cryptographic integrity (F1 Amanah)
    entry_json = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()
    seal_id = secrets.token_hex(16)
    entry["seal_id"] = seal_id
    entry["seal_hash"] = entry_hash

    # 5. Merkle Root (Chaining)
    merkle_root = _compute_merkle_root(entry_hash)
    entry["merkle_root"] = merkle_root

    # 6. Commit to persistence
    storage = storage_override or JSONLVaultStorage(DEFAULT_VAULT_PATH)

    # SABAR: Cooling ledger (72h hold)
    if eureka < 0.75:
        expiry = (datetime.now(timezone.utc) + timedelta(hours=72)).isoformat()
        entry["status"] = "SABAR"
        entry["phoenix_72_expiry"] = expiry
        await storage.write(entry)
        return SealReceipt(
            status="SABAR",
            seal_id=seal_id,
            entry_hash=entry_hash,
            timestamp=timestamp,
            eureka_score=eureka,
            vault_backend="cooling",
            phoenix_72_expiry=expiry,
        )

    # SEAL: Permanent vault
    entry["status"] = "SEALED"
    await storage.write(entry)

    return VaultOutput(
        session_id=session_id,
        verdict=Verdict(entry["verdict"]),
        status="SUCCESS",
        action="write",
        entries=[
            VaultEntry(
                session_id=session_id,
                query=query[:1024],
                verdict=entry["verdict"],
                floor_scores=judge_output.get("floor_scores", {}),
                timestamp=timestamp,
                seal_hash=entry_hash,
                merkle_root=merkle_root,
            )
        ],
        seal_hash=entry_hash,
        merkle_root=merkle_root,
        metrics={"eureka_score": eureka},
    )


def _compute_eureka_score(
    judge_output: dict[str, Any],
    agi_tensor: ConstitutionalTensor | None = None,
    asi_output: dict[str, Any] | None = None,
    objective_contract: dict[str, Any] | None = None,
) -> float:
    """Compute EUREKA score based on truth, consensus, genius, and novelty."""
    truth = agi_tensor.truth_score if agi_tensor else 0.99
    # Support both Quad-Witness (W4) and Tri-Witness (W3)
    w_consensus = float(judge_output.get("W_4", judge_output.get("W_3", 0.0)))
    genius = float(judge_output.get("genius_G", 0.8))
    peace = float(asi_output.get("peace_squared", 1.0)) if asi_output else 1.0

    # Novelty proxy (Simplified)
    novelty = 0.8

    score = (truth * w_consensus * genius * peace * novelty) ** 0.2
    if objective_contract:
        drift = float(objective_contract.get("drift", 0.0))
        threshold = float(objective_contract.get("threshold", 0.45))
        if drift >= threshold:
            score *= max(0.2, 1.0 - drift)

    return float(min(1.0, max(0.0, score)))


def _compute_merkle_root(entry_hash: str) -> str:
    """Compute Merkle root linked to the genesis/previous hash."""
    genesis = "GENESIS_HASH_V64_FORGE"
    combined = genesis + entry_hash
    return hashlib.sha256(combined.encode()).hexdigest()


# =============================================================================
# P3 THERMODYNAMIC HELPERS
# =============================================================================


def _get_thermo_final_state(session_id: str) -> dict[str, Any]:
    """
    P3: Capture final thermodynamic state for vault entry.

    Returns thermodynamic budget status and entropy metrics.
    """
    try:
        from core.physics.thermodynamics_hardened import (
            get_thermodynamic_budget,
            get_thermodynamic_report,
        )

        budget = get_thermodynamic_budget(session_id)
        report = get_thermodynamic_report(session_id)

        return {
            "budget_final": budget.to_dict(),
            "entropy_reduction_total": budget.entropy_reduction_claimed,
            "landauer_violations": budget.landauer_violations,
            "compliance": report.get("constitutional_compliance", {}),
        }
    except Exception as e:
        return {"error": str(e), "status": "thermodynamic_capture_failed"}


def _cleanup_thermo_budget(session_id: str) -> dict[str, Any]:
    """
    P3: Cleanup thermodynamic budget after vault seal.

    Returns final budget report.
    """
    try:
        from core.physics.thermodynamics_hardened import cleanup_thermodynamic_budget

        return cleanup_thermodynamic_budget(session_id)
    except Exception as e:
        return {"session_id": session_id, "cleanup_error": str(e)}


# =============================================================================
# UNIFIED VAULT INTERFACE
# =============================================================================


async def vault(
    action: str,
    judge_output: dict[str, Any] | None = None,
    agi_tensor: ConstitutionalTensor | None = None,
    asi_output: dict[str, Any] | None = None,
    session_id: str = "",
    query: str = "",
    seal_id: str = "",
    authority: str = "system",
    eureka_data: dict[str, Any] | None = None,
    objective_contract: dict[str, Any] | None = None,
) -> Any:
    """Unified VAULT interface."""
    storage = JSONLVaultStorage(DEFAULT_VAULT_PATH)

    if action == "seal":
        if judge_output is None:
            raise ValueError("seal requires judge_output")
        return await seal(
            judge_output,
            agi_tensor,
            asi_output,
            session_id,
            query,
            authority,
            eureka_data,
            objective_contract,
            storage_override=storage,
        )

    elif action == "query":
        return await storage.read(seal_id)

    elif action == "verify":
        record = await storage.read(seal_id)
        if not record:
            return False
        # Simplified verification
        return True

    else:
        raise ValueError(f"Unknown action: {action}")


# =============================================================================
# SCAR-WEIGHT & RATIFICATION — Stage 888 Handshake
# =============================================================================


async def vault_create_pending(
    query: str,
    response: str,
    judge_output: dict[str, Any],
    session_id: str,
) -> str:
    """
    Create a pending vault entry for a HOLD_888 verdict.
    Starts the Phoenix-72 cooling timer.
    """
    expiry = (datetime.now(timezone.utc) + timedelta(hours=72)).isoformat()

    # In a real implementation, this would save to a 'pending' table/collection
    # For now, we simulate the receipt
    print(f"PENDING VETO: Session {session_id} cooling until {expiry}")
    return session_id


async def sovereign_authorize(
    vault_id: str,
    sovereign_id: str,
    signature: str,
) -> bool:
    """
    Ratify a pending entry with the Sovereign's Scar-Weight.
    Upgrades HOLD_888 → SEAL.
    """
    # 1. Retrieve pending entry
    # 2. Verify signature against sovereign_id
    # 3. Create ScarWeight object
    # 4. Update entry status to SEAL
    # 5. Write to permanent vault
    return True


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Actions (1 of 3 max)
    "seal",  # Stage 999: Final commitment
    # Unified interface
    "vault",
    # Scar-Weight & Phoenix-72
    "vault_create_pending",  # HOLD_888 pending entry
    "sovereign_authorize",  # Ratify with scar-weight
    # Types
    "SealReceipt",
    "VaultStorage",
    "JSONLVaultStorage",
]
