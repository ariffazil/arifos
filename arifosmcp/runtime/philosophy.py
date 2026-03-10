"""
arifosmcp/runtime/philosophy.py — The arifOS Philosophical Lattice

Unified wisdom system:
- 33 deterministic quotes for floor failures and stage alignment
- Minimal, zero-dependency implementation for 1.0.0

DITEMPA, BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
from typing import Any, TypedDict


class Quote(TypedDict):
    id: str
    category: str
    author: str
    text: str


class PhilosophySelection(TypedDict):
    apex_mode: str
    role: str
    stage: str
    g_score: float
    semantic_backend: str
    agi: dict[str, Any]
    asi: dict[str, Any] | None


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


def get_wisdom_for_context(
    context: str,
    stage: str = "444",
    g_score: float = 0.9,
    failed_floors: list[str] | None = None,
) -> Quote:
    """
    Simplified wisdom retrieval for 1.0.0.
    Falls back to stage-based deterministic selection.
    """
    failed_floors = failed_floors or []
    return get_philosophical_anchor(stage, g_score, failed_floors)


def _stage_number(stage: str) -> int:
    try:
        return int("".join(ch for ch in stage if ch.isdigit()) or "444")
    except ValueError:
        return 444


def _semantic_category(
    stage: str,
    g_score: float,
    failed_floors: list[str],
    verdict: str,
) -> str:
    if verdict in {"VOID", "HOLD", "HOLD_888"} or g_score < 0.5:
        return "wisdom"
    if "F6" in failed_floors:
        return "love"
    if "F2" in failed_floors or "F7" in failed_floors:
        return "wisdom"

    stage_num = _stage_number(stage)
    if stage_num >= 999:
        return "seal"
    if stage_num >= 666:
        return "power" if g_score >= 0.85 else "paradox"
    if stage_num >= 333:
        return "paradox"
    return "wisdom"


def _quote_block(quote: Quote, *, score: float | None = None, source: str) -> dict[str, Any]:
    block: dict[str, Any] = {
        "quote_id": quote["id"],
        "quote": quote["text"],
        "author": quote["author"],
        "category": quote["category"],
        "source": source,
    }
    if score is not None:
        block["score"] = round(score, 4)
    return block


def get_semantic_wisdom(
    context: str,
    *,
    stage: str = "444",
    g_score: float = 0.9,
    failed_floors: list[str] | None = None,
    verdict: str = "SABAR",
) -> tuple[dict[str, Any] | None, str]:
    """
    Best-effort semantic wisdom retrieval from the 99-quote ASI layer.

    Returns a tuple of (quote block or None, backend status).
    The runtime remains fully functional if the vector layer is absent.
    """
    failed_floors = failed_floors or []

    try:
        from arifosmcp.intelligence.tools.wisdom_quotes import retrieve_wisdom
    except ImportError:
        return None, "unavailable"

    category = _semantic_category(stage, g_score, failed_floors, verdict)

    try:
        result = retrieve_wisdom(context, category=category, n_results=1)
    except Exception:
        return None, "error"

    if not isinstance(result, dict):
        return None, "empty"

    quotes = result.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        return None, "empty"

    first = quotes[0]
    if not isinstance(first, dict):
        return None, "empty"

    quote_id = str(first.get("id") or first.get("quote_id") or "").strip()
    quote_text = str(first.get("text") or first.get("quote") or "").strip()
    author = str(first.get("author") or "unknown").strip() or "unknown"
    quote_category = str(first.get("category") or category).strip() or category
    if not quote_id or not quote_text:
        return None, "empty"

    score_raw = first.get("score", first.get("similarity"))
    try:
        score = float(score_raw) if score_raw is not None else None
    except (TypeError, ValueError):
        score = None

    return (
        {
            "quote_id": quote_id,
            "quote": quote_text,
            "author": author,
            "category": quote_category,
            "source": "semantic_99",
            "score": round(score, 4) if score is not None else None,
        },
        "available",
    )


def select_governed_philosophy(
    context: str,
    *,
    stage: str,
    verdict: str,
    g_score: float,
    failed_floors: list[str] | None = None,
    session_id: str = "global",
) -> PhilosophySelection:
    """
    Govern quote exposure without letting quotes influence the verdict.

    AGI  -> 33 deterministic constitutional anchors
    ASI  -> 99 semantic/vector wisdom when available
    APEX -> choose deterministic, hybrid, or semantic emphasis from G*, stage, verdict
    """
    failed_floors = failed_floors or []
    agi_quote = get_philosophical_anchor(stage, g_score, failed_floors, session_id=session_id)
    semantic_quote, semantic_backend = get_semantic_wisdom(
        context,
        stage=stage,
        g_score=g_score,
        failed_floors=failed_floors,
        verdict=verdict,
    )

    stage_num = _stage_number(stage)
    role = "seal" if stage_num >= 999 else "anchor" if stage_num <= 111 else "support"

    hard_governance = (
        bool(failed_floors) or verdict in {"VOID", "HOLD", "HOLD_888"} or g_score < 0.5
    )
    if stage_num in {0, 999} or hard_governance:
        apex_mode = "deterministic_33"
        semantic_quote = None
    elif semantic_quote is None:
        apex_mode = "deterministic_33"
    elif g_score >= 0.8:
        apex_mode = "semantic_99"
    else:
        apex_mode = "hybrid"

    return {
        "apex_mode": apex_mode,
        "role": role,
        "stage": stage,
        "g_score": round(g_score, 4),
        "semantic_backend": semantic_backend,
        "agi": _quote_block(agi_quote, source="deterministic_33"),
        "asi": semantic_quote,
    }


__all__ = [
    "PhilosophySelection",
    "Quote",
    "PHILOSOPHY_REGISTRY",
    "get_philosophical_anchor",
    "get_semantic_wisdom",
    "get_wisdom_for_context",
    "select_governed_philosophy",
]
