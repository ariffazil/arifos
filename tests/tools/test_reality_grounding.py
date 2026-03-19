import asyncio
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Mock optional dependencies before import
# NOTE: httpx is NOT mocked — it's installed via FastMCP and mocking it
# causes metaclass conflicts in authlib's httpx integration.
import sys

sys.modules["ddgs"] = MagicMock()
sys.modules["playwright"] = MagicMock()
sys.modules["playwright.async_api"] = MagicMock()
sys.modules["bs4"] = MagicMock()

from aaa_mcp.tools import reality_grounding

# Now, we can import the module
from aaa_mcp.tools.reality_grounding import (
    BraveSearchEngine,
    DDGSEngine,
    PlaywrightDDGEngine,
    PlaywrightGoogleEngine,
    RealityGroundingCascade,
    RealityGroundingResult,
    SearchResult,
    ThrottleGovernor,
    WebBrowser,
    reality_check,
    should_reality_check,
)


@pytest.fixture
def mock_search_result():
    """Fixture for a sample SearchResult."""
    return SearchResult(
        title="Test Title",
        url="https://example.com",
        snippet="Test snippet.",
        source="test_engine",
        rank=1,
        uncertainty=0.1,
    )


def test_search_result_to_dict(mock_search_result: SearchResult):
    """
    Given: A SearchResult object.
    When: The to_dict method is called.
    Then: It should return a dictionary representation with correct keys.
    """
    # Arrange
    # Act
    result_dict = mock_search_result.to_dict()

    # Assert
    assert result_dict["title"] == "Test Title"
    assert result_dict["url"] == "https://example.com"
    assert result_dict["source"] == "test_engine"
    assert "timestamp" in result_dict


def test_reality_grounding_result_to_dict(mock_search_result: SearchResult):
    """
    Given: A RealityGroundingResult object.
    When: The to_dict method is called.
    Then: It should return a dictionary representation with nested results.
    """
    # Arrange
    grounding_result = RealityGroundingResult(
        status="OK",
        query="test query",
        results=[mock_search_result],
        engines_used=["test_engine"],
        engines_failed=[],
        uncertainty_aggregate=0.1,
        audit_trail={"note": "test"},
    )

    # Act
    result_dict = grounding_result.to_dict()

    # Assert
    assert result_dict["status"] == "OK"
    assert result_dict["query"] == "test query"
    assert result_dict["results_count"] == 1
    assert len(result_dict["results"]) == 1
    assert result_dict["results"][0]["title"] == "Test Title"


@pytest.mark.asyncio
async def test_throttle_governor_waits_correctly():
    """
    Given: A ThrottleGovernor with a specific interval.
    When: wait() is called multiple times in quick succession.
    Then: It should sleep for the appropriate amount of time to enforce the interval.
    """
    # Arrange
    interval = 0.1
    governor = ThrottleGovernor(min_interval=interval)

    # Act
    start_time = asyncio.get_event_loop().time()
    await governor.wait()
    await governor.wait()
    end_time = asyncio.get_event_loop().time()

    # Assert
    assert (end_time - start_time) >= interval


@patch("aaa_mcp.tools.reality_grounding.DDGS_AVAILABLE", True)
def test_ddgs_engine_asean_bias_query_build():
    """
    Given: The DDGSEngine.
    When: _build_query is called with region 'asean'.
    Then: It should add the ASEAN site search operators to the query.
    """
    # Arrange
    engine = DDGSEngine()
    query = "test query"

    # Act
    biased_query = engine._build_query(query, region="asean")

    # Assert
    # ASEAN site operators use wildcard: site:*.my
    assert "site:*.my" in biased_query
    assert "site:*.sg" in biased_query
    assert f"({query})" in biased_query


@pytest.mark.parametrize(
    "query, expected_result, reason",
    [
        ("what is the capital of France", False, "no_verification_needed"),
        ("can you verify the latest news on technology?", True, "explicit_verification"),
        ("what are the health benefits of meditation", True, "high_stakes_domain"),
        ("what happened this week in politics", True, "temporal_query"),
        ("who won the 2026 world cup", True, "temporal_query"),
    ],
)
def test_should_reality_check_scenarios(query, expected_result, reason):
    """
    Given: Various query strings.
    When: should_reality_check is called.
    Then: It should return the correct boolean and reason based on keywords.
    """
    # Arrange
    # Act
    needs_check, check_reason = should_reality_check(query)

    # Assert
    assert needs_check == expected_result
    assert check_reason == reason


@patch.dict(os.environ, {"BRAVE_API_KEY": "test-key"}, clear=True)
@patch("aaa_mcp.tools.reality_grounding.PlaywrightGoogleEngine")
@patch("aaa_mcp.tools.reality_grounding.PlaywrightDDGEngine")
@patch("aaa_mcp.tools.reality_grounding.DDGSEngine")
@patch("aaa_mcp.tools.reality_grounding.BraveSearchEngine")
def test_cascade_initializes_engines_with_brave_key(
    mock_brave, mock_ddgs, mock_playwright_ddg, mock_playwright_google
):
    """
    Given: The BRAVE_API_KEY environment variable is set.
    When: RealityGroundingCascade is initialized.
    Then: The BraveSearchEngine should be instantiated.
    """
    # Arrange & Act
    cascade = RealityGroundingCascade()

    # Assert
    mock_brave.assert_called_once()
    assert len(cascade.engines) > 0
    assert cascade.engines[0] == mock_brave.return_value


@patch("aaa_mcp.tools.reality_grounding.DDGS_AVAILABLE", True)
@patch("aaa_mcp.tools.reality_grounding.PLAYWRIGHT_AVAILABLE", True)
@patch.dict(os.environ, {}, clear=True)
@patch("aaa_mcp.tools.reality_grounding.PlaywrightGoogleEngine")
@patch("aaa_mcp.tools.reality_grounding.PlaywrightDDGEngine")
@patch("aaa_mcp.tools.reality_grounding.DDGSEngine")
@patch("aaa_mcp.tools.reality_grounding.BraveSearchEngine")
def test_cascade_skips_brave_without_key(
    mock_brave, mock_ddgs, mock_playwright_ddg, mock_playwright_google
):
    """
    Given: The BRAVE_API_KEY environment variable is NOT set.
    When: RealityGroundingCascade is initialized.
    Then: The BraveSearchEngine should NOT be in the engine list, but others should.
    """
    # Arrange & Act
    cascade = RealityGroundingCascade()

    # Assert
    mock_brave.assert_not_called()
    mock_ddgs.assert_called_once()
    assert len(cascade.engines) > 0
    assert cascade.engines[0] == mock_ddgs.return_value


@pytest.mark.asyncio
async def test_cascade_search_tries_engines_in_order():
    """
    Given: A cascade with multiple mock engines.
    When: The first engine returns no results, but the second one does.
    Then: The cascade should call both engines and return results from the second.
    """
    # Arrange
    cascade = RealityGroundingCascade()

    mock_engine1 = AsyncMock()
    mock_engine1.NAME = "engine1"
    mock_engine1.search.return_value = ([], "no_results")  # Fails

    mock_engine2 = AsyncMock()
    mock_engine2.NAME = "engine2"
    mock_engine2.search.return_value = (
        [SearchResult("title", "url", "snippet", "engine2", 1, 0.5)],
        None,
    )

    cascade.engines = [mock_engine1, mock_engine2]

    # Act
    result = await cascade.search("test query")

    # Assert
    mock_engine1.search.assert_called_once()
    mock_engine2.search.assert_called_once()
    assert result.status == "PARTIAL"  # Partial because one engine failed
    assert len(result.results) == 1
    assert result.results[0].source == "engine2"
    assert "engine1: no_results" in result.engines_failed
    assert "engine2" in result.engines_used


@pytest.mark.asyncio
async def test_cascade_search_stops_after_success():
    """
    Given: A cascade with multiple mock engines.
    When: The first engine returns results.
    Then: The cascade should NOT call the subsequent engines.
    """
    # Arrange
    cascade = RealityGroundingCascade()

    mock_engine1 = AsyncMock()
    mock_engine1.NAME = "engine1"
    mock_engine1.search.return_value = (
        [SearchResult("title", "url", "snippet", "engine1", 1, 0.5)],
        None,
    )

    mock_engine2 = AsyncMock()
    mock_engine2.NAME = "engine2"

    cascade.engines = [mock_engine1, mock_engine2]

    # Act
    result = await cascade.search("test query")

    # Assert
    mock_engine1.search.assert_called_once()
    mock_engine2.search.assert_not_called()
    assert result.status == "OK"
    assert len(result.results) == 1
    assert result.results[0].source == "engine1"


@pytest.mark.asyncio
@patch("aaa_mcp.tools.reality_grounding.get_cascade")
@patch("aaa_mcp.tools.reality_grounding.get_browser")
@patch("aaa_mcp.tools.reality_grounding.route_refuse")
@patch("aaa_mcp.tools.reality_grounding.should_reality_check")
async def test_reality_check_fetches_sources_when_requested(
    mock_should_check, mock_refuse, mock_get_browser, mock_get_cascade
):
    """
    Given: A call to reality_check with fetch_sources=True.
    When: The search cascade returns results.
    Then: The browser's fetch method should be called for the top results.
    """
    # Arrange
    mock_should_check.return_value = (True, "test_reason")
    mock_refuse.return_value = MagicMock()
    mock_refuse.return_value.to_dict.return_value = {}

    mock_cascade = AsyncMock()
    mock_search_results = [SearchResult("title", "https://example.com", "snippet", "test", 1, 0.1)]
    mock_cascade.search.return_value = RealityGroundingResult(
        "OK", "query", mock_search_results, ["test"], [], 0.1, {}
    )
    mock_get_cascade.return_value = mock_cascade

    mock_browser = AsyncMock()
    mock_browser.fetch.return_value = {"status": "OK", "content": "fetched content"}
    mock_get_browser.return_value = mock_browser

    # Act
    response = await reality_check("test query", fetch_sources=True, max_sources=1)

    # Assert
    mock_cascade.search.assert_called_once()
    mock_get_browser.assert_called_once()
    mock_browser.fetch.assert_called_with("https://example.com")
    assert "sources_fetched" in response
    assert len(response["sources_fetched"]) == 1
    assert response["sources_fetched"][0]["url"] == "https://example.com"
