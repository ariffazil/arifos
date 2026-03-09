"""
core/philosophy/manifold.py — APEX-G Quote Manifold Selection Engine

Selects wisdom quotes by geometric proximity in 6D APEX-G space:

    v = (τ, ΔS, P², G, Ψ, κᵣ)

Selection algorithm:
    1. Build a k-d tree over all 99 quote coordinate vectors.
    2. For a given session state vector, query the k-d tree for the k
       nearest neighbours (default k=10).
    3. Score each candidate: score = 1/(1 + d) × (1 + floor_affinity_bonus)
    4. Return the highest-scored quote with full provenance.

Constitutional grounding:
    F4 Clarity  — selection is deterministic and auditable
    F8 Tri-Witness — k-d tree provides evidence-based geometric consensus
    F7 Humility — distance included in provenance; nearest ≠ certain best
    F1 Truth    — scores derived from real geometric distances

DITEMPA BUKAN DIBERI — Forged, Not Given.

Version: 2026.03.09-SEAL
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

try:
    from scipy.spatial import KDTree

    _SCIPY_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SCIPY_AVAILABLE = False

from core.philosophy.coordinates import (
    CATEGORY_AGI_DOCTRINE,
    CATEGORY_FLOOR_AFFINITIES,
    CATEGORY_POWER_MECHANISMS,
    DIM,
    LAYER_DESCRIPTIONS,
    APEXGCoordinate,
    WisdomLayer,
    session_state_to_coordinate,
)

# ── Constants ─────────────────────────────────────────────────────────────

_MANIFOLD_PATH = Path(__file__).parent.parent.parent / "data" / "wisdom_quotes_manifold.json"

FLOOR_AFFINITY_BONUS: float = 0.20  # added per matching active floor
RESONANCE_BONUS_WEIGHT: float = 0.15  # resonance_density × weight added to score
DEFAULT_K_NEIGHBOURS: int = 10  # candidates returned from k-d tree


# ── Data types ────────────────────────────────────────────────────────────


@dataclass
class QuoteSelection:
    """
    Result of a manifold-based quote selection.

    Includes the selected quote, its distance from the query vector,
    the final score, and full provenance for auditability (F4 Clarity).

    Word-power fields (F6 Empathy, F7 Humility):
        power_mechanisms    — which of the four language mechanisms activate
        resonance_density   — ρ ∈ [0,1], neurological potency of the quote
    """

    quote_id: int
    category: str
    author: str
    text: str
    source: str
    human_cost: str

    # Geometric position
    apex_g: dict[str, Any]

    # Selection telemetry
    distance: float
    score: float
    floor_affinity_bonus: float
    active_floors_matched: list[str]
    query_vector: list[float]

    # Word-power theory fields
    power_mechanisms: list[str]
    resonance_density: float  # ρ ∈ [0, 1]
    resonance_bonus: float  # resonance_density × RESONANCE_BONUS_WEIGHT

    # Full provenance (F4)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agi_doctrine = CATEGORY_AGI_DOCTRINE.get(self.category, "")
        return {
            "quote_id": self.quote_id,
            "category": self.category,
            "author": self.author,
            "text": self.text,
            "source": self.source,
            "human_cost": self.human_cost,
            "apex_g": self.apex_g,
            # ── AGI / ASI / APEX trinity layer output ──────────────────────
            "layers": {
                WisdomLayer.AGI: {
                    "role": LAYER_DESCRIPTIONS[WisdomLayer.AGI]["role"],
                    "question": LAYER_DESCRIPTIONS[WisdomLayer.AGI]["question"],
                    "quote_id": self.quote_id,
                    "category": self.category,
                    "text": self.text,
                    "author": self.author,
                    "doctrine": agi_doctrine,
                    "floor_affinities": self.apex_g.get("floor_affinities", []),
                    "power_mechanisms": self.power_mechanisms,
                },
                WisdomLayer.ASI: {
                    "role": LAYER_DESCRIPTIONS[WisdomLayer.ASI]["role"],
                    "question": LAYER_DESCRIPTIONS[WisdomLayer.ASI]["question"],
                    "distance": round(self.distance, 6),
                    "resonance_density": self.resonance_density,
                    "query_vector": [round(v, 4) for v in self.query_vector],
                    "manifold_position": {
                        k: v for k, v in self.apex_g.items()
                        if k not in ("floor_affinities", "power_mechanisms",
                                     "resonance_density")
                    },
                },
                WisdomLayer.APEX: {
                    "role": LAYER_DESCRIPTIONS[WisdomLayer.APEX]["role"],
                    "question": LAYER_DESCRIPTIONS[WisdomLayer.APEX]["question"],
                    "score": round(self.score, 6),
                    "formula": self.provenance.get("formula", ""),
                    "floor_affinity_bonus": round(self.floor_affinity_bonus, 4),
                    "active_floors_matched": self.active_floors_matched,
                    "resonance_bonus": round(self.resonance_bonus, 4),
                },
            },
            # ── Backward-compatible flat fields ────────────────────────────
            "word_power": {
                "power_mechanisms": self.power_mechanisms,
                "resonance_density": self.resonance_density,
                "resonance_bonus": round(self.resonance_bonus, 4),
            },
            "selection_telemetry": {
                "distance": round(self.distance, 6),
                "score": round(self.score, 6),
                "floor_affinity_bonus": round(self.floor_affinity_bonus, 4),
                "active_floors_matched": self.active_floors_matched,
                "query_vector": [round(v, 4) for v in self.query_vector],
            },
            "provenance": self.provenance,
        }


# ── Manifold engine ───────────────────────────────────────────────────────


class QuoteManifold:
    """
    APEX-G Quote Manifold — 6D k-d tree over the 99-quote corpus.

    Usage::

        manifold = QuoteManifold()
        result = manifold.select(tau=0.8, delta_s=-0.3, p2=1.1,
                                  g=0.88, psi=0.85, kappa_r=0.72)
        print(result.text)

    The manifold is built once on first instantiation and cached.
    """

    _instance: QuoteManifold | None = None

    def __init__(self, manifold_path: Path | str | None = None) -> None:
        path = Path(manifold_path) if manifold_path else _MANIFOLD_PATH
        self._quotes: list[dict[str, Any]] = []
        self._vectors: np.ndarray = np.empty((0, DIM))
        self._tree: Any = None  # KDTree or None
        self._loaded = False
        self._load(path)

    # ── Public API ────────────────────────────────────────────────────────

    def select(
        self,
        *,
        tau: float = 0.5,
        delta_s: float = 0.0,
        p2: float = 1.0,
        g: float = 0.85,
        psi: float = 0.5,
        kappa_r: float = 0.5,
        active_floors: list[str] | None = None,
        k: int = DEFAULT_K_NEIGHBOURS,
    ) -> QuoteSelection:
        """
        Select the best-matching quote for the given APEX-G state vector.

        Args:
            tau:           Temporal resonance τ ∈ [0, 1].
            delta_s:       Entropy delta ΔS ∈ [-1, 1].
            p2:            Peace squared P² ∈ [0, 2].
            g:             Governance score G ∈ [0, 1].
            psi:           Epistemic depth Ψ ∈ [0, 1].
            kappa_r:       Empathy coefficient κᵣ ∈ [0, 1].
            active_floors: Constitutional floors active in current session
                           (used to compute floor affinity bonus).
            k:             Number of nearest neighbours to score.

        Returns:
            QuoteSelection with the highest-scored quote and full provenance.
        """
        query_vec = [tau, delta_s, p2, g, psi, kappa_r]
        active_floors = active_floors or []

        if not self._loaded or len(self._quotes) == 0:
            return self._fallback(query_vec, active_floors)

        # Clamp k to the number of available quotes
        k_eff = min(k, len(self._quotes))

        if self._tree is not None:
            distances, indices = self._tree.query(query_vec, k=k_eff)
        else:
            # Pure-numpy fallback when scipy is unavailable
            diffs = self._vectors - np.array(query_vec)
            distances_all = np.sqrt((diffs**2).sum(axis=1))
            indices = np.argsort(distances_all)[:k_eff]
            distances = distances_all[indices]

        # Score each candidate
        best_score = -1.0
        best_idx = int(indices[0])
        best_dist = float(distances[0])
        best_bonus = 0.0
        best_matched: list[str] = []
        best_rho = 0.0
        best_rho_bonus = 0.0

        for dist, idx in zip(distances, indices, strict=False):
            d = float(dist)
            i = int(idx)
            quote = self._quotes[i]
            cat = quote.get("category", "")
            cat_floors = CATEGORY_FLOOR_AFFINITIES.get(cat, [])
            quote_floors = quote.get("apex_g", {}).get("floor_affinities", cat_floors)

            # Floor affinity bonus: +FLOOR_AFFINITY_BONUS per matched floor
            matched = [f for f in active_floors if f in quote_floors]
            bonus = len(matched) * FLOOR_AFFINITY_BONUS

            # Resonance density bonus: ρ × RESONANCE_BONUS_WEIGHT
            rho = float(quote.get("apex_g", {}).get("resonance_density", 0.8))
            rho_bonus = rho * RESONANCE_BONUS_WEIGHT

            # Final score: geometric proximity × floor affinity × resonance
            score = (1.0 / (1.0 + d)) * (1.0 + bonus) * (1.0 + rho_bonus)

            if score > best_score:
                best_score = score
                best_idx = i
                best_dist = d
                best_bonus = bonus
                best_matched = matched
                best_rho = rho
                best_rho_bonus = rho_bonus

        q = self._quotes[best_idx]
        apex_g = q.get("apex_g", {})
        cat = q.get("category", "")
        power_mechanisms = apex_g.get(
            "power_mechanisms", CATEGORY_POWER_MECHANISMS.get(cat, [])
        )

        return QuoteSelection(
            quote_id=q.get("id", best_idx + 1),
            category=cat,
            author=q.get("author", ""),
            text=q.get("text", ""),
            source=q.get("source", ""),
            human_cost=q.get("human_cost", ""),
            apex_g=apex_g,
            distance=best_dist,
            score=best_score,
            floor_affinity_bonus=best_bonus,
            active_floors_matched=best_matched,
            query_vector=query_vec,
            power_mechanisms=power_mechanisms,
            resonance_density=best_rho,
            resonance_bonus=best_rho_bonus,
            provenance={
                "method": "kd_tree" if self._tree is not None else "numpy_fallback",
                "k_neighbours_scored": k_eff,
                "total_quotes_in_manifold": len(self._quotes),
                "formula": (
                    "score = 1/(1+d) × (1 + floor_affinity_bonus) × (1 + ρ × resonance_weight)"
                ),
                "floor_affinity_bonus_per_match": FLOOR_AFFINITY_BONUS,
                "resonance_bonus_weight": RESONANCE_BONUS_WEIGHT,
            },
        )

    def select_from_coordinate(
        self,
        coord: APEXGCoordinate,
        k: int = DEFAULT_K_NEIGHBOURS,
    ) -> QuoteSelection:
        """Select using an :class:`APEXGCoordinate` directly."""
        return self.select(
            tau=coord.tau,
            delta_s=coord.delta_s,
            p2=coord.p2,
            g=coord.g,
            psi=coord.psi,
            kappa_r=coord.kappa_r,
            active_floors=coord.floor_affinities,
            k=k,
        )

    def select_from_session_state(
        self,
        *,
        stage: str | int = "444",
        delta_s: float = 0.0,
        p2: float = 1.0,
        g_score: float = 0.85,
        psi: float = 0.5,
        kappa_r: float = 0.5,
        active_floors: list[str] | None = None,
    ) -> QuoteSelection:
        """
        Convenience wrapper: convert runtime state → coordinate → selection.

        Accepts the same parameters as
        :func:`core.philosophy.coordinates.session_state_to_coordinate`.
        """
        coord = session_state_to_coordinate(
            stage=stage,
            delta_s=delta_s,
            p2=p2,
            g_score=g_score,
            psi=psi,
            kappa_r=kappa_r,
            active_floors=active_floors,
        )
        return self.select_from_coordinate(coord)

    @property
    def loaded(self) -> bool:
        """True when the manifold data was successfully loaded."""
        return self._loaded

    @property
    def quote_count(self) -> int:
        """Number of quotes currently in the manifold."""
        return len(self._quotes)

    # ── Private helpers ───────────────────────────────────────────────────

    def _load(self, path: Path) -> None:
        """Load manifold JSON and build the k-d tree."""
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            self._loaded = False
            return

        quotes = data.get("quotes", [])
        if not quotes:
            self._loaded = False
            return

        self._quotes = quotes
        vectors = []
        for q in quotes:
            apex_g = q.get("apex_g", {})
            v = [
                float(apex_g.get("tau", 0.5)),
                float(apex_g.get("delta_s", 0.0)),
                float(apex_g.get("p2", 1.0)),
                float(apex_g.get("g", 0.85)),
                float(apex_g.get("psi", 0.5)),
                float(apex_g.get("kappa_r", 0.5)),
            ]
            vectors.append(v)

        self._vectors = np.array(vectors, dtype=float)

        if _SCIPY_AVAILABLE:
            self._tree = KDTree(self._vectors)
        else:
            self._tree = None  # will use numpy fallback in select()

        self._loaded = True

    def _fallback(
        self, query_vec: list[float], active_floors: list[str]
    ) -> QuoteSelection:
        """Return a minimal placeholder when manifold data is unavailable."""
        return QuoteSelection(
            quote_id=0,
            category="wisdom",
            author="arifOS",
            text="Knowledge itself is power. (Manifold data unavailable.)",
            source="fallback",
            human_cost="",
            apex_g={},
            distance=0.0,
            score=0.0,
            floor_affinity_bonus=0.0,
            active_floors_matched=[],
            query_vector=query_vec,
            power_mechanisms=[],
            resonance_density=0.0,
            resonance_bonus=0.0,
            provenance={"method": "fallback", "reason": "manifold_not_loaded"},
        )


# ── Module-level singleton ────────────────────────────────────────────────

_manifold: QuoteManifold | None = None


def get_manifold() -> QuoteManifold:
    """
    Return the module-level :class:`QuoteManifold` singleton.

    Builds and caches the instance on first call.
    """
    global _manifold
    if _manifold is None:
        _manifold = QuoteManifold()
    return _manifold


def select_wisdom(
    *,
    stage: str | int = "444",
    delta_s: float = 0.0,
    p2: float = 1.0,
    g_score: float = 0.85,
    psi: float = 0.5,
    kappa_r: float = 0.5,
    active_floors: list[str] | None = None,
    k: int = DEFAULT_K_NEIGHBOURS,
) -> QuoteSelection:
    """
    Module-level convenience function: select the nearest wisdom quote for
    the given runtime state.

    Example::

        from core.philosophy.manifold import select_wisdom
        result = select_wisdom(stage="666", g_score=0.88, active_floors=["F6"])
        print(result.text)
    """
    return get_manifold().select_from_session_state(
        stage=stage,
        delta_s=delta_s,
        p2=p2,
        g_score=g_score,
        psi=psi,
        kappa_r=kappa_r,
        active_floors=active_floors,
    )


__all__ = [
    "QuoteManifold",
    "QuoteSelection",
    "FLOOR_AFFINITY_BONUS",
    "RESONANCE_BONUS_WEIGHT",
    "DEFAULT_K_NEIGHBOURS",
    "get_manifold",
    "select_wisdom",
]
