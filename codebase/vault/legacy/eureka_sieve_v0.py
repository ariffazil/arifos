"""
EUREKA Sieve — Theory of Anomalous Contrast Filter

Only meaningful insights enter VAULT999.
Trivial queries are TRANSIENT (not stored).
Medium insights go to SABAR (cooling ledger).
EUREKA insights get SEALed permanently.

Doctrine: Theory of Anomalous Contrast (888_SOUL_VERDICT.md)
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Anomalous Contrast Thresholds
EUREKA_THRESHOLD = 0.75  # SEAL worthy
SABAR_THRESHOLD = 0.50   # Cooling worthy
TRANSIENT_THRESHOLD = 0.0  # Don't store

# Novelty detection
NOVELTY_SIMILARITY_THRESHOLD = 0.85  # Below this = novel


@dataclass
class EUREKAScore:
    """EUREKA evaluation result."""
    
    # Four velocities of anomalous contrast
    novelty: float  # 0-1: How different from history
    entropy_reduction: float  # 0-1: Did we reduce confusion
    ontological_shift: float  # 0-1: Did framework change
    decision_weight: float  # 0-1: Irreversibility + stakes
    
    # Composite
    eureka_score: float  # Average of four
    verdict: str  # SEAL, SABAR, TRANSIENT
    
    # Metadata
    reasoning: List[str] = field(default_factory=list)
    fingerprint: str = ""  # Content hash for dedup


class AnomalousContrastEngine:
    """
    Detects EUREKA moments — insights that stand out from the background.
    
    Theory: Meaning emerges from contrast.
    If something is not anomalous (different), it's not meaningful.
    """
    
    def __init__(self, vault_ledger: Optional[Any] = None):
        self.vault_ledger = vault_ledger
        self._history_cache: List[str] = []
        self._cache_loaded = False
    
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
        
        # 1. NOVELTY DETECTION
        novelty = await self._calculate_novelty(query, response)
        if novelty > 0.8:
            reasoning.append(f"High novelty ({novelty:.2f}): Unprecedented query pattern")
        elif novelty < 0.3:
            reasoning.append(f"Low novelty ({novelty:.2f}): Routine query")
        
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
        
        # Composite EUREKA Score
        eureka_score = (novelty + entropy_reduction + ontological_shift + decision_weight) / 4.0
        
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
        
        # Content fingerprint for deduplication
        fingerprint = self._compute_fingerprint(query, response)
        
        return EUREKAScore(
            novelty=novelty,
            entropy_reduction=entropy_reduction,
            ontological_shift=ontological_shift,
            decision_weight=decision_weight,
            eureka_score=eureka_score,
            verdict=verdict,
            reasoning=reasoning,
            fingerprint=fingerprint,
        )
    
    async def _calculate_novelty(self, query: str, response: str) -> float:
        """
        Calculate how novel this query/response is vs history.
        
        Uses simple cosine similarity on content hash fingerprints.
        Returns 0-1 where 1 = completely novel.
        """
        content = f"{query} {response}".lower().strip()
        
        # Load history if not cached
        if not self._cache_loaded and self.vault_ledger:
            await self._load_history_cache()
        
        if not self._history_cache:
            # First ever query - maximally novel
            return 1.0
        
        # Compute similarity with recent history
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Simple dedup: exact hash match = zero novelty
        if content_hash in self._history_cache:
            return 0.0
        
        # Semantic similarity using character n-grams
        similarities = []
        query_ngrams = self._get_ngrams(query, n=3)
        
        for hist_hash in self._history_cache[-100:]:  # Last 100 entries
            # We store hashes, not full text, so approximate
            # In production, use vector DB (pgvector)
            similarities.append(0.5)  # Placeholder
        
        if not similarities:
            return 1.0
        
        max_sim = max(similarities)
        novelty = 1.0 - max_sim
        
        # Boost novelty for certain patterns
        if any(kw in query.lower() for kw in [
            "eureka", "breakthrough", "discovered", "novel", "new insight",
            "contradiction", "paradox", "anomaly"
        ]):
            novelty = min(1.0, novelty + 0.2)
        
        return novelty
    
    def _calculate_entropy_reduction(self, trinity_bundle: Dict[str, Any]) -> float:
        """
        Did this reduce entropy (confusion)?
        
        Based on AGI entropy_delta and F4 Clarity score.
        """
        agi = trinity_bundle.get("agi", {})
        entropy_delta = agi.get("entropy_delta", 0.0)
        
        # entropy_delta < 0 means entropy reduction (good)
        # Map -1.0 -> 1.0, 0 -> 0.5, +1.0 -> 0.0
        if entropy_delta <= 0:
            return 0.5 + (abs(entropy_delta) / 2.0)
        else:
            return max(0.0, 0.5 - (entropy_delta / 2.0))
    
    def _calculate_ontological_shift(self, trinity_bundle: Dict[str, Any]) -> float:
        """
        Did this change the ontological framework?
        
        Detected by:
        - New canon proposed
        - Code changes
        - Constitutional amendments
        - New floor definitions
        """
        score = 0.0
        reasoning = trinity_bundle.get("reasoning", {})
        
        # Check for canon proposals
        if reasoning.get("proposed_canon"):
            score += 0.4
        
        # Check for code changes
        if reasoning.get("code_modified"):
            score += 0.3
        
        # Check for new floor triggers
        apex = trinity_bundle.get("apex", {})
        if apex.get("novelty_detected"):
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_decision_weight(self, trinity_bundle: Dict[str, Any]) -> float:
        """
        How weighty is this decision?
        
        Based on:
        - F1 Amanah (reversibility)
        - 888_HOLD triggered (high stakes)
        - Multi-stakeholder impact (ASI)
        """
        score = 0.0
        
        # F1 Amanah - irreversible = high weight
        init = trinity_bundle.get("init", {})
        if not init.get("f1_amanah", True):
            score += 0.4  # Irreversible action
        
        # 888_HOLD - high stakes
        apex = trinity_bundle.get("apex", {})
        if apex.get("verdict") == "888_HOLD":
            score += 0.3
        
        # Multi-stakeholder (ASI)
        asi = trinity_bundle.get("asi", {})
        stakeholders = asi.get("stakeholders", [])
        if len(stakeholders) > 2:
            score += 0.2
        
        # Lane = HARD (higher stakes than SOFT)
        lane = init.get("lane", "SOFT")
        if lane == "HARD":
            score += 0.1
        
        return min(1.0, score)
    
    def _compute_fingerprint(self, query: str, response: str) -> str:
        """Compute content fingerprint for deduplication."""
        content = f"{query}|{response}".lower().strip()
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _get_ngrams(self, text: str, n: int = 3) -> set:
        """Extract character n-grams from text."""
        text = text.lower()
        return set(text[i:i+n] for i in range(len(text) - n + 1))
    
    async def _load_history_cache(self):
        """Load recent entry fingerprints from vault."""
        if not self.vault_ledger:
            return
        
        try:
            # Get last 100 entries
            entries = await self.vault_ledger.list_entries(limit=100)
            for entry in entries.get("entries", []):
                seal_data = entry.get("seal_data", {})
                fingerprint = seal_data.get("eureka", {}).get("fingerprint", "")
                if fingerprint:
                    self._history_cache.append(fingerprint)
            self._cache_loaded = True
        except Exception:
            pass  # Fail silently, treat as empty history


class EUREKASieve:
    """
    Pre-vault filter implementing Theory of Anomalous Contrast.
    
    Prevents VAULT999 from becoming "tong sampah" (trash bin).
    Only EUREKA moments get permanent storage.
    """
    
    def __init__(self):
        self.engine = AnomalousContrastEngine()
    
    async def filter(
        self,
        query: str,
        response: str,
        trinity_bundle: Dict[str, Any],
    ) -> Tuple[str, EUREKAScore]:
        """
        Filter content before vault entry.
        
        Returns:
            (target_ledger, eureka_score)
            
        target_ledger can be:
        - "vault" → Permanent VAULT999 (SEAL)
        - "cooling" → BBB_LEDGER/cooling_ledger.jsonl (SABAR)
        - None → TRANSIENT, don't store
        """
        score = await self.engine.evaluate(query, response, trinity_bundle)
        
        if score.verdict == "SEAL":
            return "vault", score
        elif score.verdict == "SABAR":
            return "cooling", score
        else:
            return None, score


# Singleton instance
eureka_sieve = EUREKASieve()


async def should_seal_to_vault(
    query: str,
    response: str,
    trinity_bundle: Dict[str, Any],
) -> Tuple[bool, Dict[str, Any]]:
    """
    Convenience function: Should this be sealed to VAULT999?
    
    Returns (should_seal, metadata)
    """
    target, score = await eureka_sieve.filter(query, response, trinity_bundle)
    
    metadata = {
        "eureka_score": score.eureka_score,
        "novelty": score.novelty,
        "entropy_reduction": score.entropy_reduction,
        "ontological_shift": score.ontological_shift,
        "decision_weight": score.decision_weight,
        "verdict": score.verdict,
        "reasoning": score.reasoning,
        "fingerprint": score.fingerprint,
        "target_ledger": target,
    }
    
    return target == "vault", metadata
