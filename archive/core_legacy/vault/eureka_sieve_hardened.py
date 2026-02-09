"""
EUREKA Sieve — HARDENED Theory of Anomalous Contrast Filter

Only meaningful insights enter VAULT999.
Trivial queries are TRANSIENT (not stored).
Medium insights go to SABAR (cooling ledger).
EUREKA insights get SEALed permanently.

Doctrine: Theory of Anomalous Contrast (888_SOUL_VERDICT.md)
Hardening: Fixed fingerprint dedup, real similarity, ledger wiring
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Set
import asyncio

# Anomalous Contrast Thresholds
EUREKA_THRESHOLD = 0.75  # SEAL worthy
SABAR_THRESHOLD = 0.50   # Cooling worthy

# Novelty detection
NOVELTY_SIMILARITY_THRESHOLD = 0.85  # Below this = novel
JACCARD_THRESHOLD = 0.70  # N-gram Jaccard similarity threshold


@dataclass
class EUREKAScore:
    """EUREKA evaluation result."""
    
    # Four velocities of anomalous contrast
    novelty: float  # 0-1: How different from history
    entropy_reduction: float  # 0-1: Did we reduce confusion
    ontological_shift: float  # 0-1: Did framework change
    decision_weight: float  # 0-1: Irreversibility + stakes
    
    # Composite
    eureka_score: float  # Weighted average
    verdict: str  # SEAL, SABAR, TRANSIENT
    
    # Metadata
    reasoning: List[str] = field(default_factory=list)
    fingerprint: str = ""  # Full 64-char hash for dedup
    jaccard_sim: float = 0.0  # Max similarity to history
    degraded: bool = False  # True if history cache failed to load


class HardenedAnomalousContrastEngine:
    """
    HARDENED: Detects EUREKA moments with real similarity computation.
    
    Fixes:
    - Fingerprint dedup uses consistent 64-char hashes
    - Real Jaccard similarity on n-grams (not placeholder)
    - Properly wired to vault ledger
    - Caches history n-grams for O(1) similarity
    """
    
    def __init__(self, vault_ledger: Optional[Any] = None):
        self.vault_ledger = vault_ledger
        # Cache: fingerprint -> ngrams set
        self._history_ngrams: Dict[str, Set[str]] = {}
        self._history_fingerprints: Set[str] = set()
        self._cache_loaded = False
        self._cache_lock = asyncio.Lock()
    
    async def evaluate(
        self,
        query: str,
        response: str,
        trinity_bundle: Dict[str, Any],
    ) -> EUREKAScore:
        """
        Evaluate if this deserves to enter VAULT999.
        
        Returns EUREKAScore with verdict:
        - SEAL: EUREKA moment (≥0.75) → Permanent storage
        - SABAR: Potential (0.50-0.75) → Cooling ledger
        - TRANSIENT: Trivial (<0.50) → Don't store
        """
        reasoning = []
        
        # Compute fingerprint and n-grams once
        fingerprint = self._compute_fingerprint(query, response)
        query_ngrams = self._get_ngrams(query, n=3)
        
        # 1. NOVELTY DETECTION (HARDENED)
        novelty, max_jaccard = await self._calculate_novelty_hardened(
            query, response, fingerprint, query_ngrams
        )
        if novelty > 0.8:
            reasoning.append(f"High novelty ({novelty:.2f}): Unprecedented query pattern (Jaccard {max_jaccard:.2f})")
        elif novelty < 0.3:
            reasoning.append(f"Low novelty ({novelty:.2f}): Routine query (Jaccard {max_jaccard:.2f})")
        
        # 2. ENTROPY REDUCTION (ΔS ≤ 0)
        entropy_reduction = self._calculate_entropy_reduction(trinity_bundle)
        if entropy_reduction > 0.8:
            reasoning.append(f"High clarity ({entropy_reduction:.2f}): Significant entropy reduction")
        elif entropy_reduction < 0.3:
            reasoning.append(f"Low clarity ({entropy_reduction:.2f}): Minimal entropy change")
        
        # 3. ONTOLOGICAL SHIFT
        ontological_shift = self._calculate_ontological_shift(trinity_bundle)
        if ontological_shift > 0.8:
            reasoning.append(f"Major ontological shift ({ontological_shift:.2f}): Framework change detected")
        
        # 4. DECISION WEIGHT
        decision_weight = self._calculate_decision_weight(trinity_bundle)
        if decision_weight > 0.8:
            reasoning.append(f"High stakes ({decision_weight:.2f}): Irreversible or multi-stakeholder")
        
        # HARDENED: Weighted composite (not simple average)
        # Novelty and entropy reduction matter most
        weights = {
            'novelty': 0.35,
            'entropy_reduction': 0.30,
            'ontological_shift': 0.20,
            'decision_weight': 0.15,
        }
        eureka_score = (
            novelty * weights['novelty'] +
            entropy_reduction * weights['entropy_reduction'] +
            ontological_shift * weights['ontological_shift'] +
            decision_weight * weights['decision_weight']
        )
        
        # Determine verdict
        if eureka_score >= EUREKA_THRESHOLD:
            verdict = "SEAL"
            reasoning.append(f"EUREKA Score {eureka_score:.2f} ≥ {EUREKA_THRESHOLD}: Permanent seal")
        elif eureka_score >= SABAR_THRESHOLD:
            verdict = "SABAR"
            reasoning.append(f"EUREKA Score {eureka_score:.2f}: Cooling period required")
        else:
            verdict = "TRANSIENT"
            reasoning.append(f"EUREKA Score {eureka_score:.2f}: Not meaningful enough to store")
        
        return EUREKAScore(
            novelty=novelty,
            entropy_reduction=entropy_reduction,
            ontological_shift=ontological_shift,
            decision_weight=decision_weight,
            eureka_score=eureka_score,
            verdict=verdict,
            reasoning=reasoning,
            fingerprint=fingerprint,  # Full 64-char hash
            jaccard_sim=max_jaccard,
        )
    
    async def _calculate_novelty_hardened(
        self,
        query: str,
        response: str,
        fingerprint: str,
        query_ngrams: Set[str],
    ) -> Tuple[float, float]:
        """
        HARDENED: Real Jaccard similarity on n-grams.
        
        Returns: (novelty_score, max_jaccard_similarity)
        """
        # Load history if not cached (thread-safe)
        if not self._cache_loaded:
            async with self._cache_lock:
                if not self._cache_loaded:
                    await self._load_history_cache_hardened()
                    self._cache_loaded = True
        
        # Exact fingerprint match = zero novelty (exact duplicate)
        if fingerprint in self._history_fingerprints:
            return 0.0, 1.0
        
        if not self._history_ngrams:
            # First ever query - maximally novel
            return 1.0, 0.0
        
        # Compute Jaccard similarity with historical queries
        # Jaccard = |A ∩ B| / |A ∪ B|
        similarities = []
        query_len = len(query_ngrams)
        
        for hist_fingerprint, hist_ngrams in list(self._history_ngrams.items())[-100:]:
            intersection = len(query_ngrams & hist_ngrams)
            union = len(query_ngrams | hist_ngrams)
            
            if union == 0:
                jaccard = 0.0
            else:
                jaccard = intersection / union
            
            similarities.append(jaccard)
        
        if not similarities:
            return 1.0, 0.0
        
        max_jaccard = max(similarities)
        
        # Novelty = 1 - similarity (clamped)
        novelty = max(0.0, min(1.0, 1.0 - max_jaccard))
        
        # Boost novelty for EUREKA keywords
        query_lower = query.lower()
        eureka_keywords = [
            "eureka", "breakthrough", "discovered", "novel", "new insight",
            "contradiction", "paradox", "anomaly", "revelation", "insight",
            "fundamental", "ontological", "framework", "paradigm shift"
        ]
        if any(kw in query_lower for kw in eureka_keywords):
            novelty = min(1.0, novelty + 0.15)
        
        return novelty, max_jaccard
    
    async def _load_history_cache_hardened(self):
        """HARDENED: Load history with n-grams for real similarity."""
        if not self.vault_ledger:
            return
        
        try:
            entries = await self.vault_ledger.list_entries(limit=100)
            for entry in entries.get("entries", []):
                seal_data = entry.get("seal_data", {})
                
                # Get fingerprint (prefer full 64-char)
                fingerprint = seal_data.get("eureka", {}).get("fingerprint", "")
                if not fingerprint:
                    # Reconstruct from query/response if available
                    query = seal_data.get("query", "")
                    response = seal_data.get("response", "")
                    fingerprint = self._compute_fingerprint(query, response)
                
                if fingerprint:
                    self._history_fingerprints.add(fingerprint)
                    
                    # Cache n-grams for similarity
                    query = seal_data.get("query", "")
                    self._history_ngrams[fingerprint] = self._get_ngrams(query, n=3)
                    
        except Exception as e:
            # Fail gracefully - empty cache means all queries are novel
            import logging
            logging.getLogger(__name__).warning(
                f"EUREKA sieve history cache load failed: {e}. "
                "Operating in degraded mode (no dedup)."
            )
            self._degraded = True  # Mark for metadata
    
    def _calculate_entropy_reduction(self, trinity_bundle: Dict[str, Any]) -> float:
        """Did this reduce entropy (confusion)?"""
        agi = trinity_bundle.get("agi", {})
        entropy_delta = agi.get("entropy_delta", 0.0)
        
        # entropy_delta < 0 means entropy reduction (good)
        # Map -1.0 -> 1.0, 0 -> 0.5, +1.0 -> 0.0
        if entropy_delta <= 0:
            return min(1.0, 0.5 + (abs(entropy_delta) / 2.0))
        else:
            return max(0.0, 0.5 - (entropy_delta / 2.0))
    
    def _calculate_ontological_shift(self, trinity_bundle: Dict[str, Any]) -> float:
        """Did this change the ontological framework?"""
        score = 0.0
        
        # Check for canon proposals
        reasoning = trinity_bundle.get("reasoning", {})
        if reasoning.get("proposed_canon"):
            score += 0.4
        
        # Check for code changes
        if reasoning.get("code_modified"):
            score += 0.3
        
        # Check for new floor triggers
        apex = trinity_bundle.get("apex", {})
        if apex.get("novelty_detected"):
            score += 0.3
        
        # Check for constitutional amendments
        if reasoning.get("constitutional_amendment"):
            score += 0.5
        
        return min(1.0, score)
    
    def _calculate_decision_weight(self, trinity_bundle: Dict[str, Any]) -> float:
        """How weighty is this decision?"""
        score = 0.0
        
        # F1 Amanah - irreversible = high weight
        init = trinity_bundle.get("init", {})
        if not init.get("f1_amanah", True):
            score += 0.4
        
        # 888_HOLD - high stakes
        apex = trinity_bundle.get("apex", {})
        if apex.get("verdict") == "888_HOLD":
            score += 0.3
        
        # Multi-stakeholder (ASI)
        asi = trinity_bundle.get("asi", {})
        stakeholders = asi.get("stakeholders", [])
        if len(stakeholders) > 2:
            score += 0.2
        elif len(stakeholders) > 0:
            score += 0.1
        
        # Lane = HARD (higher stakes than SOFT)
        lane = init.get("lane", "SOFT")
        if lane == "HARD":
            score += 0.15
        elif lane == "CRISIS":
            score += 0.25
        
        return min(1.0, score)
    
    def _compute_fingerprint(self, query: str, response: str) -> str:
        """HARDENED: Full 64-char hash for consistent dedup."""
        content = f"{query}|{response}".lower().strip()
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_ngrams(self, text: str, n: int = 3) -> Set[str]:
        """Extract character n-grams from text."""
        text = text.lower()
        if len(text) < n:
            return set([text]) if text else set()
        return set(text[i:i+n] for i in range(len(text) - n + 1))


class HardenedEUREKASieve:
    """
    HARDENED Pre-vault filter with real ledger wiring.
    """
    
    def __init__(self, vault_ledger: Optional[Any] = None):
        # HARDENED: Pass ledger to engine
        self.engine = HardenedAnomalousContrastEngine(vault_ledger=vault_ledger)
    
    async def filter(
        self,
        query: str,
        response: str,
        trinity_bundle: Dict[str, Any],
    ) -> Tuple[str, EUREKAScore]:
        """
        Filter content before vault entry.
        
        Returns: (target_ledger, eureka_score)
        """
        score = await self.engine.evaluate(query, response, trinity_bundle)
        
        if score.verdict == "SEAL":
            return "vault", score
        elif score.verdict == "SABAR":
            return "cooling", score
        else:
            return None, score


# HARDENED: Factory function with proper ledger wiring
async def create_hardened_sieve(vault_ledger: Optional[Any] = None):
    """Create a properly wired EUREKA Sieve."""
    return HardenedEUREKASieve(vault_ledger=vault_ledger)


async def should_seal_to_vault_hardened(
    query: str,
    response: str,
    trinity_bundle: Dict[str, Any],
    vault_ledger: Optional[Any] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    HARDENED: Should this be sealed to VAULT999?
    
    Returns (should_seal, metadata)
    """
    sieve = await create_hardened_sieve(vault_ledger)
    target, score = await sieve.filter(query, response, trinity_bundle)
    
    metadata = {
        "eureka_score": score.eureka_score,
        "novelty": score.novelty,
        "entropy_reduction": score.entropy_reduction,
        "ontological_shift": score.ontological_shift,
        "decision_weight": score.decision_weight,
        "jaccard_sim": score.jaccard_sim,
        "verdict": score.verdict,
        "reasoning": score.reasoning,
        "fingerprint": score.fingerprint,
        "target_ledger": target,
    }
    
    return target == "vault", metadata
