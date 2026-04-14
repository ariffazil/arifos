"""
tests/core/organs/test_vault_router_regression.py — Vault Router Regression Tests

Validates that core.organs._4_vault.vault() maintains the unified router contract:
- operation="seal" -> delegates to _4_vault.seal()
- any other operation -> delegates to unified_memory.vault()

This prevents the regression introduced in PR #325 where non-seal operations
raised ValueError instead of routing to memory.
"""

import pytest
from unittest.mock import patch, AsyncMock


class TestVaultRouterRegression:
    """Regression tests for the unified vault router in _4_vault.py."""

    @pytest.mark.asyncio
    async def test_vault_seal_routes_to_seal(self):
        """operation='seal' must route to _4_vault.seal()."""
        from core.organs._4_vault import vault

        with patch("core.organs._4_vault.seal", new_callable=AsyncMock) as mock_seal:
            mock_seal.return_value = {"mocked": "seal_result"}
            result = await vault(operation="seal", session_id="sess-001", summary="test")

            mock_seal.assert_awaited_once()
            assert result == {"mocked": "seal_result"}

    @pytest.mark.asyncio
    async def test_vault_store_routes_to_unified_memory(self):
        """operation='store' must delegate to unified_memory.vault, not raise."""
        from core.organs._4_vault import vault

        with patch(
            "core.organs.unified_memory.vault", new_callable=AsyncMock
        ) as mock_mem_vault:
            mock_mem_vault.return_value = {"mocked": "memory_result"}
            result = await vault(
                operation="store", session_id="sess-002", content="hello"
            )

            mock_mem_vault.assert_awaited_once()
            assert result == {"mocked": "memory_result"}

    @pytest.mark.asyncio
    async def test_vault_search_routes_to_unified_memory(self):
        """operation='search' must delegate to unified_memory.vault."""
        from core.organs._4_vault import vault

        with patch(
            "core.organs.unified_memory.vault", new_callable=AsyncMock
        ) as mock_mem_vault:
            mock_mem_vault.return_value = {"mocked": "search_result"}
            result = await vault(
                operation="search", session_id="sess-003", content="query"
            )

            mock_mem_vault.assert_awaited_once()
            assert result == {"mocked": "search_result"}

    @pytest.mark.asyncio
    async def test_vault_unknown_operation_propagates_error(self):
        """An unsupported operation should still surface a meaningful error."""
        from core.organs._4_vault import vault

        with patch(
            "core.organs.unified_memory.vault", new_callable=AsyncMock
        ) as mock_mem_vault:
            mock_mem_vault.side_effect = ValueError("Unsupported vault operation: xyz")

            with pytest.raises(ValueError, match="Unsupported vault operation"):
                await vault(operation="xyz", session_id="sess-004")

    def test_public_exports_exist(self):
        """SealReceipt, seal_vault, and __all__ must remain public."""
        from core.organs import _4_vault

        assert hasattr(_4_vault, "SealReceipt")
        assert hasattr(_4_vault, "seal_vault")
        assert "vault" in _4_vault.__all__
        assert "seal_vault" in _4_vault.__all__
        assert "SealReceipt" in _4_vault.__all__
