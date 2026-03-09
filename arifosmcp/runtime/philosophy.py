"""
arifosmcp/runtime/philosophy.py — The arifOS Philosophical Lattice

Unified wisdom system:
- 33 deterministic quotes for floor failures and stage alignment
- 99 semantic quotes for context-aware retrieval (Qdrant + BGE-M3)

DITEMPA, BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
import os
from typing import Literal, TypedDict

try:
    from arifosmcp.intelligence.tools.wisdom_quotes import retrieve_wisdom

    SEMANTIC_WISDOM_AVAILABLE = True
except ImportError:
    SEMANTIC_WISDOM_AVAILABLE = False


class Quote(TypedDict):
    id: str
    category: str
    author: str
    text: str


PHILOSOPHY_REGISTRY: list[Quote] = [
    # 1-10: WISDOM (Humility / Knowledge)
    {
        "id": "W1",
        "category": "wisdom",
        "author": "Socrates",
        "text": "The only true wisdom is in knowing you know nothing.",
    },
    {
        "id": "W2",
        "category": "wisdom",
        "author": "Aristotle",
        "text": "Knowing yourself is the beginning of all wisdom.",
    },
    {
        "id": "W3",
        "category": "wisdom",
        "author": "Confucius",
        "text": "Real knowledge is to know the extent of one's ignorance.",
    },
    {
        "id": "W4",
        "category": "wisdom",
        "author": "Lao Tzu",
        "text": "He who knows others is wise; he who knows himself is enlightened.",
    },
    {
        "id": "W5",
        "category": "wisdom",
        "author": "Marcus Aurelius",
        "text": "You have power over your mind—not outside events. Realize this, and you will find strength.",
    },
    {
        "id": "W6",
        "category": "wisdom",
        "author": "Albert Einstein",
        "text": "The important thing is not to stop questioning.",
    },
    {
        "id": "W7",
        "category": "wisdom",
        "author": "Isaac Newton",
        "text": "If I have seen further it is by standing on the shoulders of giants.",
    },
    {
        "id": "W8",
        "category": "wisdom",
        "author": "Carl Sagan",
        "text": "Extraordinary claims require extraordinary evidence.",
    },
    {
        "id": "W9",
        "category": "wisdom",
        "author": "Francis Bacon",
        "text": "Knowledge itself is power.",
    },
    {
        "id": "W10",
        "category": "wisdom",
        "author": "Alan Turing",
        "text": "We can only see a short distance ahead, but we can see plenty there that needs to be done.",
    },
    # 11-20: POWER (Action / Will)
    {
        "id": "P1",
        "category": "power",
        "author": "Napoleon Bonaparte",
        "text": "Impossible is a word to be found only in the dictionary of fools.",
    },
    {
        "id": "P2",
        "category": "power",
        "author": "Julius Caesar",
        "text": "I came, I saw, I conquered.",
    },
    {
        "id": "P3",
        "category": "power",
        "author": "Friedrich Nietzsche",
        "text": "He who has a why to live can bear almost any how.",
    },
    {
        "id": "P4",
        "category": "power",
        "author": "Niccolò Machiavelli",
        "text": "It is better to be feared than loved, if you cannot be both.",
    },
    {
        "id": "P5",
        "category": "power",
        "author": "Thomas Edison",
        "text": "Genius is one percent inspiration and ninety-nine percent perspiration.",
    },
    {
        "id": "P6",
        "category": "power",
        "author": "Winston Churchill",
        "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    },
    {
        "id": "P7",
        "category": "power",
        "author": "Theodore Roosevelt",
        "text": "The credit belongs to the man who is actually in the arena.",
    },
    {
        "id": "P8",
        "category": "power",
        "author": "George S. Patton",
        "text": "A good plan violently executed now is better than a perfect plan executed next week.",
    },
    {
        "id": "P9",
        "category": "power",
        "author": "Henry Ford",
        "text": "Whether you think you can, or you think you can't – you're right.",
    },
    {
        "id": "P10",
        "category": "power",
        "author": "Sun Tzu",
        "text": "In the midst of chaos, there is also opportunity.",
    },
    # 21-30: PARADOX (Balance / Contradiction)
    {
        "id": "R1",
        "category": "paradox",
        "author": "Heraclitus",
        "text": "The only constant in life is change.",
    },
    {
        "id": "R2",
        "category": "paradox",
        "author": "Lao Tzu",
        "text": "When I let go of what I am, I become what I might be.",
    },
    {
        "id": "R3",
        "category": "paradox",
        "author": "Niels Bohr",
        "text": "The opposite of a profound truth may well be another profound truth.",
    },
    {
        "id": "R4",
        "category": "paradox",
        "author": "Blaise Pascal",
        "text": "The heart has its reasons which reason knows nothing of.",
    },
    {
        "id": "R5",
        "category": "paradox",
        "author": "Søren Kierkegaard",
        "text": "Life can only be understood backwards; but it must be lived forwards.",
    },
    {
        "id": "R6",
        "category": "paradox",
        "author": "G.K. Chesterton",
        "text": "The whole secret of life is to be interested in one thing profoundly and in a thousand things well.",
    },
    {
        "id": "R7",
        "category": "paradox",
        "author": "Bertrand Russell",
        "text": "The trouble with the world is that the stupid are cocksure and the intelligent are full of doubt.",
    },
    {
        "id": "R8",
        "category": "paradox",
        "author": "Albert Camus",
        "text": "In the depth of winter, I finally learned that within me there lay an invincible summer.",
    },
    {
        "id": "R9",
        "category": "paradox",
        "author": "Carl Jung",
        "text": "One does not become enlightened by imagining figures of light, but by making the darkness conscious.",
    },
    {
        "id": "R10",
        "category": "paradox",
        "author": "F. Scott Fitzgerald",
        "text": "The test of a first-rate intelligence is the ability to hold two opposed ideas in mind at the same time and still retain the ability to function.",
    },
    # 31-32: VOID (Gödel Lock)
    {
        "id": "V1",
        "category": "void",
        "author": "Kurt Gödel",
        "text": "Either mathematics is too big for the human mind, or the human mind is more than a machine.",
    },
    {
        "id": "V2",
        "category": "void",
        "author": "Ludwig Wittgenstein",
        "text": "Whereof one cannot speak, thereof one must be silent.",
    },
    # 33: SEAL (Sovereign)
    {"id": "S1", "category": "seal", "author": "Arif Fazil", "text": "DITEMPA, BUKAN DIBERI."},
]


def get_philosophical_anchor(
    stage: str, g_score: float, failed_floors: list[str], session_id: str = "global"
) -> Quote:
    """
    Selects a philosophical anchor from the 33-quote registry based on:
    1. Metabolic Stage (000-999)
    2. G-Score (Vitality level)
    3. Failed Floors (Constitutional relation)
    """
    # 1. Handle Critical/Void states first
    if "F2" in failed_floors:  # Truth failure
        return next(q for q in PHILOSOPHY_REGISTRY if q["id"] == "W8")  # Carl Sagan
    if "F7" in failed_floors:  # Humility failure
        return next(q for q in PHILOSOPHY_REGISTRY if q["id"] == "W1")  # Socrates
    if g_score < 0.5:
        return next(q for q in PHILOSOPHY_REGISTRY if q["id"] == "V2")  # Wittgenstein (Silent)

    # 2. Stage-based Category Mapping
    # Logic:
    # 000-222: Wisdom (Foundations)
    # 333-555: Paradox (Reasoning/Memory)
    # 666-888: Power/Paradox (Action/Judgment)
    # 999: Seal

    try:
        stage_num = int("".join(filter(str.isdigit, stage)) or "444")
    except ValueError:
        stage_num = 444

    if stage_num >= 999:
        return next(q for q in PHILOSOPHY_REGISTRY if q["id"] == "S1")

    category = "wisdom"
    if 300 <= stage_num <= 600:
        category = "paradox"
    elif 600 < stage_num <= 900:
        category = "power" if g_score > 0.85 else "paradox"

    options = [q for q in PHILOSOPHY_REGISTRY if q["category"] == category]

    # 3. Deterministic selection via session hash
    seed = hashlib.sha256(f"{session_id}:{stage}:{g_score}".encode()).hexdigest()
    idx = int(seed, 16) % len(options)

    return options[idx]


def get_semantic_wisdom(
    query: str,
    category: Literal[
        "scar", "triumph", "paradox", "wisdom", "power", "love", "seal", "all"
    ] = "all",
    n_results: int = 3,
) -> list[Quote]:
    """
    Retrieve semantically relevant quotes from the 99-quote corpus.

    Uses BGE-M3 embeddings for multilingual support.
    Falls back to PHILOSOPHY_REGISTRY if Qdrant unavailable.

    Args:
        query: Natural language query
        category: Filter by category
        n_results: Number of quotes to return

    Returns:
        List of Quote objects with semantic scores
    """
    if not SEMANTIC_WISDOM_AVAILABLE:
        return _fallback_to_registry(category, n_results)

    result = retrieve_wisdom(query, category=category, n_results=n_results)

    if result.get("status") != "ok":
        return _fallback_to_registry(category, n_results)

    return [
        Quote(
            id=str(q["id"]),
            category=q["category"],
            author=q["author"],
            text=q["text"],
        )
        for q in result.get("quotes", [])
    ]


def _fallback_to_registry(category: str, n: int) -> list[Quote]:
    """Fallback to PHILOSOPHY_REGISTRY when semantic search unavailable."""
    if category == "all":
        options = PHILOSOPHY_REGISTRY
    else:
        options = [q for q in PHILOSOPHY_REGISTRY if q["category"] == category]
    return options[:n]


def get_wisdom_for_context(
    context: str,
    stage: str = "444",
    g_score: float = 0.9,
    failed_floors: list[str] | None = None,
    use_semantic: bool = True,
) -> Quote:
    """
    Unified wisdom retrieval combining deterministic and semantic approaches.

    Priority:
    1. Floor failures → deterministic quote (PHILOSOPHY_REGISTRY)
    2. Semantic match → 99-quote corpus (if available)
    3. Stage-based → deterministic quote (PHILOSOPHY_REGISTRY)

    Args:
        context: Current situation/query for semantic matching
        stage: Metabolic stage (000-999)
        g_score: Vitality score
        failed_floors: List of failed constitutional floors
        use_semantic: Whether to use semantic retrieval

    Returns:
        Single most relevant Quote
    """
    failed_floors = failed_floors or []

    # 1. Critical floor failures always use deterministic quotes
    if "F2" in failed_floors:
        return next(q for q in PHILOSOPHY_REGISTRY if q["id"] == "W8")
    if "F7" in failed_floors:
        return next(q for q in PHILOSOPHY_REGISTRY if q["id"] == "W1")

    # 2. Try semantic retrieval if available and requested
    if use_semantic and SEMANTIC_WISDOM_AVAILABLE and context:
        semantic_quotes = get_semantic_wisdom(context, n_results=1)
        if semantic_quotes:
            return semantic_quotes[0]

    # 3. Fallback to stage-based deterministic selection
    return get_philosophical_anchor(stage, g_score, failed_floors)


__all__ = [
    "Quote",
    "PHILOSOPHY_REGISTRY",
    "get_philosophical_anchor",
    "get_semantic_wisdom",
    "get_wisdom_for_context",
]
