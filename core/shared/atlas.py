"""
shared/atlas.py — ATLAS-333: Governance Placement Vector

The 3-Function Constitutional Router:

    Λ(text) → lane                    # Lambda: Text → Lane classification
    Θ(lane) → (τ, κ, ρ)              # Theta: Lane → Demand tensor
    Φ(text) → GPV(lane, τ, κ, ρ)    # Phi: Complete mapping (Φ = Θ ∘ Λ)

ATLAS (Architectural Truth Layout and Semantic mapping) provides a coordinate
system for governance decisions. Every query is mapped to a Governance Placement
Vector (GPV) that determines which kernels activate and with what intensity.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from re import Pattern

# Setup ATLAS Audit Logger
logger = logging.getLogger("arifos.atlas")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[ATLAS_AUDIT] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# ═════════════════════════════════════════════════════════════════════════════
# LANE TYPES — Constitutional Processing Lanes
# ═════════════════════════════════════════════════════════════════════════════


class Lane(str, Enum):
    """
    Constitutional processing lanes.

    SOCIAL:  Phatic communication → APEX only (F6, F9)
    CARE:    Explanations, support → ASI + APEX (F3-F7, F9)
    FACTUAL: Claims, code, logic → All three (F1-F9)
    CRISIS:  Harm signals → APEX → Human (HOLD_888)
    """

    SOCIAL = "SOCIAL"
    CARE = "CARE"
    FACTUAL = "FACTUAL"
    CRISIS = "CRISIS"


class QueryType(str, Enum):
    """
    Query type classification for adaptive governance.

    Used to adjust F2 Truth strictness based on query intent.

    PROCEDURAL: Commands, workflows, instructions (e.g., "run test")
    OPINION:    Subjective views (e.g., "what do you think")
    COMPARATIVE: A vs B comparisons (e.g., "X vs Y, which is better")
    FACTUAL:    Verifiable claims (e.g., "what is the capital")
    CONVERSATIONAL: Greetings, small talk, social phatic
    TEST: Pipeline tests, health checks, pings
    EXPLORATORY: Brainstorming, discovery, open-ended
    UNKNOWN: Default fallback
    """

    PROCEDURAL = "PROCEDURAL"
    OPINION = "OPINION"
    COMPARATIVE = "COMPARATIVE"
    FACTUAL = "FACTUAL"
    CONVERSATIONAL = "CONVERSATIONAL"
    TEST = "TEST"
    EXPLORATORY = "EXPLORATORY"
    UNKNOWN = "UNKNOWN"


# ═════════════════════════════════════════════════════════════════════════════
# GOVERNANCE PLACEMENT VECTOR (GPV)
# ═════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class GPV:
    """
    Governance Placement Vector — Constitutional coordinate.

    Maps any query to:
    - lane: Which processing path
    - query_type: What kind of query (for adaptive F2)
    - truth_demand (τ): How much truth verification needed [0, 1]
    - care_demand (κ): How much empathy filtering needed [0, 1]
    - risk_level (ρ): Escalation likelihood [0, 1]
    """

    lane: Lane
    query_type: QueryType
    truth_demand: float  # τ (tau) ∈ [0, 1]
    care_demand: float  # κ (kappa) ∈ [0, 1]
    risk_level: float  # ρ (rho) ∈ [0, 1]

    def __post_init__(self):
        # Clamp all values to [0, 1]
        object.__setattr__(self, "truth_demand", max(0.0, min(1.0, self.truth_demand)))
        object.__setattr__(self, "care_demand", max(0.0, min(1.0, self.care_demand)))
        object.__setattr__(self, "risk_level", max(0.0, min(1.0, self.risk_level)))

    def to_tensor(self) -> tuple[float, float, float]:
        """Return (τ, κ, ρ) as tuple."""
        return (self.truth_demand, self.care_demand, self.risk_level)

    def complexity(self) -> float:
        """
        Overall constitutional complexity.

        Returns: Average of τ, κ, ρ
        """
        return (self.truth_demand + self.care_demand + self.risk_level) / 3.0

    def requires_grounding(self) -> bool:
        """Does this GPV require external fact-checking?"""
        return self.truth_demand > 0.7 or self.risk_level > 0.5

    def requires_empathy(self) -> bool:
        """Does this GPV require stakeholder analysis?"""
        return self.care_demand > 0.5 or self.lane in (Lane.CARE, Lane.CRISIS)

    def f2_threshold(self) -> float:
        """Adaptive F2 threshold."""
        thresholds = {
            QueryType.PROCEDURAL: 0.70,
            QueryType.OPINION: 0.60,
            QueryType.COMPARATIVE: 0.85,
            QueryType.FACTUAL: 0.99,
            QueryType.CONVERSATIONAL: 0.50,
            QueryType.TEST: 0.50,
            QueryType.EXPLORATORY: 0.80,
        }
        return thresholds.get(self.query_type, 0.95)

    def f4_skip(self) -> bool:
        """Skip F4 for non-factual queries."""
        return (
            self.query_type
            in (QueryType.PROCEDURAL, QueryType.OPINION, QueryType.CONVERSATIONAL, QueryType.TEST)
            or self.lane == Lane.SOCIAL
        )

    def can_use_fast_path(self) -> bool:
        """Can this query use the fast/light pipeline?"""
        # Fast path forbidden for anything with measurable risk or high truth demand
        if self.risk_level >= 0.2 or self.truth_demand >= 0.8:
            return False
        # SOCIAL lane is always fast-path eligible if risk/demand allows
        if self.lane == Lane.SOCIAL:
            return True
        return self.query_type in (
            QueryType.PROCEDURAL,
            QueryType.OPINION,
            QueryType.CONVERSATIONAL,
            QueryType.TEST,
        )


# ═════════════════════════════════════════════════════════════════════════════
# ATLAS-333 ENGINE
# ═════════════════════════════════════════════════════════════════════════════


class ATLAS:
    """
    ATLAS-333 Governance Placement Vector mapper.

    Pre-compiled regex patterns for performance.
    Stateless — can be instantiated once and reused.
    """

    def __init__(self, min_risk_amount: float = 100.0):
        """
        Initialize with pre-compiled regex patterns.

        Args:
            min_risk_amount: Minimum dollar amount ($) to trigger risk escalation.
        """
        self.min_risk_amount = min_risk_amount

        # ═════════════════════════════════════════════════════════════════════
        # CRISIS PATTERNS — Direct harm signals (highest priority)
        # ═════════════════════════════════════════════════════════════════════
        self._crisis_patterns: list[Pattern] = [
            # Self-harm (with negative lookbehind for idioms)
            re.compile(
                r"(?<!kill )\b(kill myself|murder|suicide|self-harm|cut myself|end it all)\b"
            ),
            re.compile(r"\b(hurt|abuse|violence|assault|attack)\s+(me|myself|someone|people)\b"),
            # Weapons/dangerous items
            re.compile(r"\b(molotov|bomb|explosive)\b"),
            re.compile(r"\b(gun|knife|weapon)\s+(to|for|against)\b"),
            # Self-harm indicators
            re.compile(r"\b(want to die|end my life)\b"),
            # Abuse/violence
            re.compile(r"\b(rape|torture|kidnap|hostage)\b"),
        ]

        # Idiomatic expressions to filter (false positive prevention)
        self._idiom_patterns: list[Pattern] = [
            re.compile(r"\bkill time\b"),
            re.compile(r"\bkill (the|my) (lights?|mood|vibe|buzz)\b"),
            re.compile(r"\bkill two birds\b"),
            re.compile(r"\bkill it\b"),
            re.compile(r"\bdressed to kill\b"),
        ]

        # ═════════════════════════════════════════════════════════════════════
        # FACTUAL PATTERNS — Technical, verifiable claims
        # ═════════════════════════════════════════════════════════════════════
        self._factual_patterns: list[Pattern] = [
            # Code/programming
            re.compile(r"\b(code|function|algorithm|class|method|variable|import|def |return )\b"),
            re.compile(r"\b(python|javascript|java|rust|c\+\+|typescript|golang)\b"),
            # Math/science
            re.compile(r"\b(theorem|proof|equation|formula|calculate|compute|solve)\b"),
            re.compile(r"\b(derivative|integral|matrix|vector|probability|statistics|entropy)\b"),
            # Technical claims
            re.compile(r"\b(according to|research shows|studies indicate|data suggests)\b"),
            re.compile(r"\b(the capital of|the population of|was born in|invented by)\b"),
            # Questions requesting facts
            re.compile(r"\b(what is|who is|when did|where is|how many|why does)\b.*\?"),
            # Numbers with units
            re.compile(r"\b\d+\s*(kg|km|m|cm|mm|lb|ft|mi|degrees|percent)\b"),
        ]

        # ═════════════════════════════════════════════════════════════════════
        # SOCIAL PATTERNS — Phatic communication
        # ═════════════════════════════════════════════════════════════════════
        self._social_patterns: list[Pattern] = [
            # Greetings
            re.compile(r"\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b"),
            # Thanks/gratitude/gestures
            re.compile(r"\b(thanks|thank you|appreciate it|grateful|tip|gratuity)\b"),
            # Small talk
            re.compile(r"\b(how are you|what's up|how's it going)\b"),
            # Farewells
            re.compile(r"\b(bye|goodbye|see you|talk later)\b"),
        ]

        # ═════════════════════════════════════════════════════════════════════
        # CARE PATTERNS — Explanations, support
        # ═════════════════════════════════════════════════════════════════════
        self._care_patterns: list[Pattern] = [
            # Help requests
            re.compile(r"\b(help|assist|support|guide me)\b"),
            # Explanations
            re.compile(r"\b(explain|how do I|how can I|what should I|advice)\b"),
            # Emotional context
            re.compile(r"\b(worried|concerned|confused|stressed|anxious)\b"),
            # Learning
            re.compile(r"\b(learn|understand|teach me|show me)\b"),
        ]

        # ═════════════════════════════════════════════════════════════════════
        # HIGH-VULNERABILITY CONTEXTS (for risk assessment)
        # ═════════════════════════════════════════════════════════════════════
        self._high_vuln_contexts: list[Pattern] = [
            re.compile(r"\b(medical|health|patient|hospital|doctor|diagnosis)\b"),
            re.compile(r"\b(child|minor|student|school|education)\b"),
            re.compile(r"\b(financial|money|payment|bank|investment|debt)\b"),
            re.compile(r"\b(legal|court|law|compliance|regulation)\b"),
            re.compile(r"\b(security|password|credential|auth|authentication)\b"),
            re.compile(r"\b(CCS|CO2|injection|pressure|borehole|storage)\b"),
            re.compile(r"\b(transfer|wire|transaction|payment|wire\stransfer)\b"),
            re.compile(r"\$\d{4,10}"),  # Large dollar amounts ($1000+)
        ]

    def _is_crisis(self, text: str) -> bool:
        """Check for crisis signals (highest priority)."""
        text_lower = text.lower()

        # Check for idioms first (false positive prevention)
        for pattern in self._idiom_patterns:
            if pattern.search(text_lower):
                return False

        # Check for crisis patterns
        for pattern in self._crisis_patterns:
            if pattern.search(text_lower):
                return True

        return False

    def _is_factual(self, text: str) -> bool:
        """Check for factual/technical content."""
        text_lower = text.lower()
        matches = 0
        for pattern in self._factual_patterns:
            if pattern.search(text_lower):
                matches += 1
        # Require multiple matches to reduce false positives
        return matches >= 2

    def _is_social(self, text: str) -> bool:
        """Check for social/phatic content."""
        text_lower = text.lower()
        # Social patterns are strong signals — single match sufficient
        for pattern in self._social_patterns:
            if pattern.search(text_lower):
                return True
        return False

    def _is_care(self, text: str) -> bool:
        """Check for care/support content."""
        text_lower = text.lower()
        matches = 0
        for pattern in self._care_patterns:
            if pattern.search(text_lower):
                matches += 1
        return matches >= 1

    def _assess_risk(self, text: str) -> float:
        """Assess risk level (ρ) from 0 to 1."""
        text_lower = text.lower()
        risk_score = 0.0

        # Crisis signals → maximum risk
        if self._is_crisis(text):
            return 1.0

        # High-vulnerability contexts
        for pattern in self._high_vuln_contexts:
            if pattern.search(text_lower):
                # Monetary risk threshold check
                money_match = re.search(r"\$(\d{1,10})", text_lower)
                if money_match:
                    amount = float(money_match.group(1))
                    if amount < self.min_risk_amount:
                        continue  # Skip risk escalation for small amounts (e.g. $10 tip)

                risk_score += 0.2

        # Absolutist claims in sensitive domains
        absolutist_words = ["guaranteed", "absolute", "always", "never", "perfectly", "zero risk"]
        for word in absolutist_words:
            if word in text_lower:
                risk_score += 0.1

        return min(1.0, risk_score)


# Global singleton instance
_atlas = ATLAS()


# ═════════════════════════════════════════════════════════════════════════════
# THE 3 FUNCTIONS: Λ, Θ, Φ
# ═════════════════════════════════════════════════════════════════════════════


def classify_query_type(text: str) -> QueryType:
    """
    Classify query type for adaptive F2 governance.

    Args:
        text: Raw query text

    Returns:
        QueryType enum (PROCEDURAL, OPINION, COMPARATIVE, FACTUAL, CONVERSATIONAL, TEST, EXPLORATORY)
    """
    text_lower = text.lower()

    # CONVERSATIONAL: Greetings, small talk
    conversational_patterns = [
        r"\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b",
        r"\b(how are you|what's up|how's it going|who are you|tell me about)\b",
        r"\b(thanks|thank you|appreciate it|help me)\b",
    ]
    for pattern in conversational_patterns:
        if re.search(pattern, text_lower):
            return QueryType.CONVERSATIONAL

    # TEST: Pipeline tests, health checks
    test_patterns = [
        r"\b(test|pipeline test|test run|check|verify|ping)\b",
    ]
    for pattern in test_patterns:
        if re.search(pattern, text_lower):
            return QueryType.TEST

    # EXPLORATORY: Brainstorming, open-ended
    exploratory_patterns = [
        r"\b(explore|brainstorm|ideas for|possibilities|what if|imagine)\b",
    ]
    for pattern in exploratory_patterns:
        if re.search(pattern, text_lower):
            return QueryType.EXPLORATORY

    # PROCEDURAL: Commands, workflows
    procedural_patterns = [
        r"\b(run|execute|start|begin|launch|process|transfer)\b",
        r"\b(how to|how do i|steps to|process for)\b",
    ]
    for pattern in procedural_patterns:
        if re.search(pattern, text_lower):
            return QueryType.PROCEDURAL

    # OPINION: Subjective requests
    opinion_patterns = [
        r"\b(what do you think|in your opinion|how do you feel)\b",
        r"\b(better|worse|best|worst|prefer|like)\b",
    ]
    for pattern in opinion_patterns:
        if re.search(pattern, text_lower):
            return QueryType.OPINION

    # COMPARATIVE: A vs B
    comparative_patterns = [
        r"\b(vs\.?|versus|compared to)\b",
        r"\b(difference|similarity|similarities)\b",
    ]
    for pattern in comparative_patterns:
        if re.search(pattern, text_lower):
            return QueryType.COMPARATIVE

    # Default to FACTUAL for everything else
    return QueryType.FACTUAL


def Λ(text: str) -> Lane:
    """
    Λ (Lambda): Text → Lane classification
    """
    # Priority order: CRISIS > FACTUAL > CARE > SOCIAL
    if _atlas._is_crisis(text):
        return Lane.CRISIS

    text_lower = text.lower()
    if "transfer" in text_lower or "wire" in text_lower:
        return Lane.FACTUAL

    if _atlas._is_factual(text):
        return Lane.FACTUAL
    elif _atlas._is_care(text):
        return Lane.CARE
    elif _atlas._is_social(text):
        return Lane.SOCIAL
    else:
        return Lane.CARE


def Θ(lane: Lane) -> tuple[float, float, float]:
    """
    Θ (Theta): Lane → Demand tensor (τ, κ, ρ)
    """
    demand_map: dict[Lane, tuple[float, float, float]] = {
        Lane.SOCIAL: (0.2, 0.1, 0.0),
        Lane.CARE: (0.4, 0.7, 0.2),
        Lane.FACTUAL: (0.9, 0.3, 0.2),
        Lane.CRISIS: (0.8, 0.9, 1.0),
    }
    return demand_map.get(lane, (0.5, 0.5, 0.5))


def Φ(text: str) -> GPV:
    """
    Φ (Phi): Complete mapping — Text → Governance Placement Vector
    """
    lane = Λ(text)
    query_type = classify_query_type(text)
    τ_base, κ_base, ρ_base = Θ(lane)
    ρ_assessed = _atlas._assess_risk(text)
    ρ = max(ρ_base, ρ_assessed)

    text_lower = text.lower()
    absolutist_terms = ["guaranteed", "absolute", "always", "never", "perfectly safe"]
    if any(term in text_lower for term in absolutist_terms):
        τ_base = min(1.0, τ_base + 0.1)

    gpv = GPV(
        lane=lane,
        query_type=query_type,
        truth_demand=τ_base,
        care_demand=κ_base,
        risk_level=ρ,
    )

    logger.info(
        f"Lane: {gpv.lane.value} | "
        f"Type: {gpv.query_type.value} | "
        f"Risk (ρ): {gpv.risk_level:.2f} | "
        f"Truth (τ): {gpv.truth_demand:.2f} | "
        f"Query: '{text[:50]}...'"
    )

    return gpv


# ASCII aliases
def Lambda(text: str) -> Lane:
    return Λ(text)


def Theta(lane: Lane) -> tuple[float, float, float]:
    return Θ(lane)


def Phi(text: str) -> GPV:
    return Φ(text)


def classify(query: str) -> dict[str, any]:
    gpv = Φ(query)
    return {
        "query": query,
        "lane": gpv.lane.value,
        "truth_demand": gpv.truth_demand,
        "care_demand": gpv.care_demand,
        "risk_level": gpv.risk_level,
        "complexity": gpv.complexity(),
        "requires_grounding": gpv.requires_grounding(),
        "requires_empathy": gpv.requires_empathy(),
    }


def route(query: str) -> str:
    gpv = Φ(query)
    organs = ["INIT"]
    if gpv.lane in (Lane.FACTUAL, Lane.CARE, Lane.CRISIS):
        organs.append("AGI")
    if gpv.lane in (Lane.CARE, Lane.CRISIS) or gpv.care_demand > 0.5:
        organs.append("ASI")
    organs.append("APEX")
    if gpv.requires_grounding():
        organs.append("(grounding)")
    return " → ".join(organs)


def classify_query(query: str) -> dict[str, any]:
    return classify(query)


def route_query(query: str) -> str:
    return route(query)


def normalize_semantic_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    n = unicodedata.normalize("NFKC", text).lower()
    confusable_map = {
        "а": "a",
        "е": "e",
        "о": "o",
        "р": "p",
        "с": "c",
        "у": "y",
        "х": "x",
        "А": "a",
        "Е": "e",
        "О": "o",
        "Р": "p",
        "С": "c",
        "У": "y",
        "Х": "x",
        "τ": "t",
        "ν": "n",
        "ρ": "p",
        "ω": "w",
        "κ": "k",
        "ε": "e",
        "Ε": "e",
    }
    return "".join(confusable_map.get(c, c) for c in n)


__all__ = [
    "Lane",
    "QueryType",
    "classify_query_type",
    "GPV",
    "Λ",
    "Θ",
    "Φ",
    "Lambda",
    "Theta",
    "Phi",
    "ATLAS",
    "classify",
    "route",
    "classify_query",
    "route_query",
    "normalize_semantic_text",
]
