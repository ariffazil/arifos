# Legacy vault ledger v0 stub
# This module is deprecated - use HardenedPersistentVaultLedger instead

class VaultLedger:
    """Deprecated: Use HardenedPersistentVaultLedger instead."""
    
    def __init__(self, *args, **kwargs):
        pass  # Allow construction but don't do anything
    
    async def append(self, *args, **kwargs):
        raise NotImplementedError("VaultLedger is deprecated. Use get_hardened_vault_ledger().")
    
    async def list_entries(self, *args, **kwargs):
        return {"entries": [], "next_cursor": None, "has_more": False}
