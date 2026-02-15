"""
codebase.vault — HARDENED Immutable Storage & Governance (999)

Canonical backend: HardenedPersistentVaultLedger (Postgres JSONB + Incremental Merkle)
Legacy modules archived in codebase/vault/legacy/

Doctrine: Theory of Anomalous Contrast (888_SOUL_VERDICT.md)
- VOID must be EXPENSIVE (requires justification)
- SEAL must be EARNED (EUREKA score >= 0.75, tri_witness >= 0.95)
- SABAR is DEFAULT (cooling period for medium insights)
"""

# HARDENED: Only export hardened implementations
from .persistent_ledger_hardened import (
    HardenedPersistentVaultLedger,
    should_use_postgres,
    get_vault_dsn,
    get_hardened_vault_ledger,
    GENESIS_HASH,
    SealContractViolation,
    enforce_seal_contract,
)

# HARDENED: EUREKA sieve
from .eureka_sieve_hardened import (
    HardenedEUREKASieve,
    HardenedAnomalousContrastEngine,
    EUREKAScore,
    should_seal_to_vault_hardened,
    create_hardened_sieve,
    EUREKA_THRESHOLD,
    SABAR_THRESHOLD,
)

# Incremental Merkle (O(log N))
from .incremental_merkle import (
    IncrementalMerkleTree,
    PersistentMerkleState,
)

# Backwards compatibility aliases
get_vault_ledger = get_hardened_vault_ledger
PersistentVaultLedger = HardenedPersistentVaultLedger
should_seal_to_vault = should_seal_to_vault_hardened
EUREKASieve = HardenedEUREKASieve

# Legacy VaultLedger (filesystem JSONL backend)
from .legacy.ledger_v0 import VaultLedger

__all__ = [
    # Hardened ledger
    "HardenedPersistentVaultLedger",
    "PersistentVaultLedger",  # Backwards compat alias
    "get_vault_ledger",  # Returns hardened
    "get_hardened_vault_ledger",
    "should_use_postgres",
    "get_vault_dsn",
    "GENESIS_HASH",
    # Seal contract
    "SealContractViolation",
    "enforce_seal_contract",
    # EUREKA sieve
    "HardenedEUREKASieve",
    "HardenedAnomalousContrastEngine",
    "EUREKAScore",
    "should_seal_to_vault_hardened",
    "create_hardened_sieve",
    "EUREKA_THRESHOLD",
    "SABAR_THRESHOLD",
    # Merkle
    "IncrementalMerkleTree",
    "PersistentMerkleState",
    # Legacy compat
    "should_seal_to_vault",
    "EUREKASieve",
    "VaultLedger",
]
