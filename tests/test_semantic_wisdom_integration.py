"""
Semantic Wisdom Integration Tests — BGE-M3 / Qdrant

Validates:
- get_wisdom_for_context() is callable and returns a Quote
- Fallback works when Qdrant is unavailable
- Floor F2 override still returns Carl Sagan (W8)
- Floor F7 override still returns Socrates (W1)
- SEMANTIC_WISDOM_AVAILABLE flag is defined
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from arifosmcp.runtime.philosophy import SEMANTIC_WISDOM_AVAILABLE, get_wisdom_for_context

# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

_CORPUS_PATH = Path(__file__).parent.parent / "data" / "wisdom_quotes.json"


@pytest.fixture(scope="module")
def wisdom_corpus() -> dict:
    """Load the 99-quote corpus once per module."""
    with _CORPUS_PATH.open() as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Helper: check Quote shape (dict or TypedDict)
# ---------------------------------------------------------------------------


def _quote_text(q: object) -> str:
    if isinstance(q, dict):
        return q.get("text", "")
    return getattr(q, "text", "")


def _quote_author(q: object) -> str:
    if isinstance(q, dict):
        return q.get("author", "")
    return getattr(q, "author", "")


# ---------------------------------------------------------------------------
# 1. Flag availability
# ---------------------------------------------------------------------------


def test_semantic_wisdom_flag_defined():
    """SEMANTIC_WISDOM_AVAILABLE must be defined (True or False)."""
    assert isinstance(SEMANTIC_WISDOM_AVAILABLE, bool)


# ---------------------------------------------------------------------------
# 2. Basic call — always returns a Quote regardless of Qdrant state
# ---------------------------------------------------------------------------


def test_get_wisdom_for_context_returns_quote():
    """get_wisdom_for_context() should always return a non-None Quote."""
    quote = get_wisdom_for_context(
        context="I am struggling with a difficult challenge",
        stage="444",
        g_score=0.7,
        failed_floors=[],
        use_semantic=True,
    )

    assert quote is not None
    assert _quote_text(quote) != ""
    assert _quote_author(quote) != ""


def test_get_wisdom_for_context_triumph():
    """get_wisdom_for_context() should return a Quote for triumph context."""
    quote = get_wisdom_for_context(
        context="I just achieved a major breakthrough and feel amazing",
        stage="777",
        g_score=0.95,
        failed_floors=[],
        use_semantic=True,
    )

    assert quote is not None
    assert _quote_text(quote) != ""


# ---------------------------------------------------------------------------
# 3. Floor override — F2 must return Carl Sagan (W8) regardless of query
# ---------------------------------------------------------------------------


def test_floor_f2_override_returns_sagan():
    """F2 failure should return Carl Sagan (W8) regardless of query."""
    quote = get_wisdom_for_context(
        context="Tell me about puppies and rainbows",
        stage="666",
        g_score=0.9,
        failed_floors=["F2"],
        use_semantic=True,
    )

    assert quote is not None
    assert "Sagan" in _quote_author(quote)


def test_floor_f7_override_returns_socrates():
    """F7 failure should return Socrates (W1) regardless of query."""
    quote = get_wisdom_for_context(
        context="I am absolutely certain about everything",
        stage="444",
        g_score=0.9,
        failed_floors=["F7"],
        use_semantic=True,
    )

    assert quote is not None
    assert "Socrates" in _quote_author(quote)


# ---------------------------------------------------------------------------
# 4. Fallback when Qdrant unreachable
# ---------------------------------------------------------------------------


def test_fallback_works_when_qdrant_unreachable():
    """System should return a Quote even when Qdrant is unreachable."""
    original_url = os.environ.get("QDRANT_URL")
    os.environ["QDRANT_URL"] = "http://nonexistent-host:9999"

    try:
        quote = get_wisdom_for_context(
            context="Test query for fallback",
            stage="444",
            g_score=0.9,
            failed_floors=[],
            use_semantic=True,
        )

        assert quote is not None
        assert _quote_text(quote) != ""
    finally:
        if original_url is not None:
            os.environ["QDRANT_URL"] = original_url
        else:
            os.environ.pop("QDRANT_URL", None)


# ---------------------------------------------------------------------------
# 5. use_semantic=False always goes deterministic
# ---------------------------------------------------------------------------


def test_use_semantic_false_skips_qdrant():
    """use_semantic=False must bypass Qdrant entirely."""
    quote = get_wisdom_for_context(
        context="Any context at all",
        stage="444",
        g_score=0.9,
        failed_floors=[],
        use_semantic=False,
    )

    assert quote is not None
    assert _quote_text(quote) != ""


# ---------------------------------------------------------------------------
# 6. Corpus completeness — 99 quotes in data/wisdom_quotes.json
# ---------------------------------------------------------------------------


def test_wisdom_corpus_has_99_quotes(wisdom_corpus: dict):
    """data/wisdom_quotes.json must contain exactly 99 quotes."""
    assert _CORPUS_PATH.exists(), f"Missing corpus file: {_CORPUS_PATH}"
    quotes = wisdom_corpus.get("quotes", [])
    assert len(quotes) == 99, f"Expected 99 quotes, found {len(quotes)}"


def test_wisdom_corpus_categories(wisdom_corpus: dict):
    """All required categories must be present in the corpus."""
    categories = {q["category"] for q in wisdom_corpus["quotes"]}
    required = {"scar", "triumph", "paradox", "wisdom", "power", "love", "seal"}
    assert required <= categories, f"Missing categories: {required - categories}"
