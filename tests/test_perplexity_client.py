"""Unit tests for Perplexity external gateway client."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from aaa_mcp.external_gateways.perplexity_client import PerplexitySearchClient


async def test_perplexity_client_no_api_key_returns_no_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PPLX_API_KEY", raising=False)
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)

    client = PerplexitySearchClient()

    result = await client.search("arifOS")
    assert result["status"] == "NO_API_KEY"
    assert result["results"] == []


class _FakeResponse:
    def __init__(self, payload: Dict[str, Any]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> Dict[str, Any]:
        return self._payload


class _FakeAsyncClient:
    def __init__(self, payload: Dict[str, Any], **_: Any) -> None:
        self._payload = payload

    async def __aenter__(self) -> "_FakeAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def post(self, *args: Any, **kwargs: Any) -> _FakeResponse:
        return _FakeResponse(self._payload)


async def test_perplexity_client_uses_citations_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PPLX_API_KEY", "test-key")
    payload = {
        "citations": ["https://example.com/a", "https://example.com/b"],
        "choices": [{"message": {"content": "ignored when citations present"}}],
    }

    import aaa_mcp.external_gateways.perplexity_client as mod

    monkeypatch.setattr(mod.httpx, "AsyncClient", lambda **kwargs: _FakeAsyncClient(payload, **kwargs))

    client = PerplexitySearchClient()
    result = await client.search("arifOS")

    assert result["status"] == "OK"
    assert len(result["results"]) == 2
    assert result["results"][0]["url"] == "https://example.com/a"


async def test_perplexity_client_bad_json_content(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PPLX_API_KEY", "test-key")
    payload = {
        "choices": [{"message": {"content": "not-json"}}],
    }

    import aaa_mcp.external_gateways.perplexity_client as mod

    monkeypatch.setattr(mod.httpx, "AsyncClient", lambda **kwargs: _FakeAsyncClient(payload, **kwargs))

    client = PerplexitySearchClient()
    result = await client.search("arifOS")

    assert result["status"] == "BAD_JSON"
