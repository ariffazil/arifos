"""
codebase.vault — Immutable Storage & Governance (999)

Primary backend: Postgres (PersistentVaultLedger)
"""

from .persistent_ledger import (
    PersistentVaultLedger,
    should_use_postgres,
    get_vault_dsn,
    get_vault_ledger,
    GENESIS_HASH,
)

__all__ = [
    "PersistentVaultLedger",
    "should_use_postgres",
    "get_vault_dsn",
    "get_vault_ledger",
    "GENESIS_HASH",
]
