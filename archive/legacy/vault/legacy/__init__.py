# Legacy vault ledger stub
# This module is deprecated - use HardenedPersistentVaultLedger instead

class VaultLedger:
    """Deprecated: Use HardenedPersistentVaultLedger instead."""
    
    def __init__(self, *args, **kwargs):
        raise DeprecationWarning(
            "VaultLedger is deprecated. Use HardenedPersistentVaultLedger instead."
        )
