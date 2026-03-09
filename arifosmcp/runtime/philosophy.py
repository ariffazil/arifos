"""
arifosmcp/runtime/philosophy.py — The arifOS Philosophical Lattice
Deterministic quote selection for the 33 internal quotes.
"""

from __future__ import annotations

import random
from typing import List, TypedDict


class Quote(TypedDict):
    id: str
    category: str
    author: str
    text: str


PHILOSOPHY_REGISTRY: List[Quote] = [
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


def get_quote_for_tool(tool_name: str, verdict: str = "") -> Quote | None:
    """Select a quote deterministically for a given tool/verdict."""
    if verdict == "VOID":
        return next(q for q in PHILOSOPHY_REGISTRY if q["category"] == "void" and q["id"] == "V2")

    # Mapping: Tool -> Category
    category_map = {
        "init_anchor_state": "wisdom",
        "integrate_analyze_reflect": "wisdom",
        "reason_mind_synthesis": "paradox",
        "metabolic_loop_router": "paradox",
        "vector_memory_store": "wisdom",
        "assess_heart_impact": "paradox",
        "critique_thought_audit": "paradox",
        "quantum_eureka_forge": "power",
        "apex_judge_verdict": "paradox",
        "seal_vault_commit": "seal",
    }

    target_category = category_map.get(tool_name, "wisdom")

    # Filter registry for category
    options = [q for q in PHILOSOPHY_REGISTRY if q["category"] == target_category]
    if not options:
        return None

    # Use a simple hash or random for now
    # In a real system, we might use hash(session_id) % len(options)
    return random.choice(options)
    # In a real system, we might use hash(session_id) % len(options)
    return random.choice(options)
