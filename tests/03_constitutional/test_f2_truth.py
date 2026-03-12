"""
F2 Truth - Anti-Hallucination Enforcement Tests

Validates that:
1. Ungrounded claims receive VOID verdict
2. Grounded claims with evidence receive SEAL verdict
3. Truth score calculation works correctly
4. Multi-source verification is required for high-confidence claims

This is a HARD floor - violations trigger immediate VOID.
"""

from __future__ import annotations

import pytest
from unittest.mock import Mock, patch

from core.judgment import JudgmentEngine
from core.shared.floors import F2_TRUTH


class TestF2TruthEnforcement:
    """Test that F2 Truth floor is properly enforced."""

    def test_ungrounded_claim_gets_void(self) -> None:
        """
        F2 HARD: Claims without evidence must be VOIDed.
        
        Scenario: User makes a factual claim with no supporting evidence.
        Expected: System returns VOID verdict with F2 violation.
        """
        engine = JudgmentEngine()
        
        # Simulated request with ungrounded claim
        request = {
            "action": "search_reality",
            "query": "The moon is made of cheese",  # False claim
            "evidence": [],  # No evidence provided
            "sources": [],
        }
        
        verdict = engine.evaluate(request)
        
        assert verdict.status == "VOID", \
            f"Ungrounded claim should be VOID, got {verdict.status}"
        assert "F2_TRUTH" in verdict.violations, \
            "VOID should cite F2_TRUTH violation"
        assert "No evidence provided" in verdict.reasoning, \
            "Reasoning should explain evidence requirement"

    def test_grounded_claim_gets_seal(self) -> None:
        """
        F2: Grounded claims with evidence receive SEAL.
        
        Scenario: User makes claim with verified evidence.
        Expected: System returns SEAL verdict.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "search_reality",
            "query": "Python 3.12 release date",
            "evidence": [
                {
                    "source": "python.org",
                    "content": "Python 3.12.0 was released on October 2, 2023",
                    "verified": True,
                }
            ],
            "sources": ["https://python.org"],
        }
        
        verdict = engine.evaluate(request)
        
        assert verdict.status == "SEAL", \
            f"Grounded claim should be SEAL, got {verdict.status}"
        assert verdict.truth_score >= 0.99, \
            f"Truth score should be >= 0.99, got {verdict.truth_score}"

    def test_truth_score_calculation(self) -> None:
        """
        F2: Truth score must be calculated from source quality.
        
        Tests the formula: truth = f(source_authority, cross_verification, recency)
        """
        f2 = F2_TRUTH()
        
        # High-quality sources
        high_quality = [
            {"source": "nasa.gov", "authority": 0.95, "verified": True},
            {"source": "esa.int", "authority": 0.92, "verified": True},
        ]
        score = f2.calculate_truth_score(high_quality)
        assert score >= 0.99, "Multiple high-authority sources should yield >= 0.99"
        
        # Low-quality/unverified sources
        low_quality = [
            {"source": "random-blog.com", "authority": 0.3, "verified": False},
        ]
        score = f2.calculate_truth_score(low_quality)
        assert score < 0.5, "Unverified low-authority source should yield < 0.5"

    def test_multi_source_verification_required(self) -> None:
        """
        F2: High-confidence claims require multiple independent sources.
        
        Scenario: Claim with single source, even if high authority.
        Expected: Lower truth score due to lack of cross-verification.
        """
        f2 = F2_TRUTH()
        
        single_source = [{"source": "authoritative.gov", "authority": 0.95, "verified": True}]
        single_score = f2.calculate_truth_score(single_source)
        
        multi_source = [
            {"source": "authoritative.gov", "authority": 0.95, "verified": True},
            {"source": "peer-site.org", "authority": 0.88, "verified": True},
        ]
        multi_score = f2.calculate_truth_score(multi_source)
        
        assert multi_score > single_score, \
            "Multi-source should score higher than single source"

    def test_confidence_without_grounding_is_hallucination(self) -> None:
        """
        F2: High confidence without grounding is hallucination.
        
        This is the primary attack vector F2 guards against:
        LLMs being confidently wrong.
        """
        engine = JudgmentEngine()
        
        # Simulated LLM response that's confident but wrong
        request = {
            "action": "reason_mind",
            "reasoning": "I am certain that...",  # Confidence without basis
            "evidence": [],
            "confidence": 0.95,  # High confidence
        }
        
        verdict = engine.evaluate(request)
        
        assert verdict.status == "VOID", \
            "High confidence without evidence is hallucination (F2 violation)"
        assert verdict.confidence < 0.5, \
            "System should reduce confidence when no evidence"


class TestF2TruthEdgeCases:
    """Edge cases for F2 Truth enforcement."""

    def test_opinion_vs_fact(self) -> None:
        """
        F2: Opinions don't require the same grounding as facts.
        
        Scenario: User expresses subjective opinion.
        Expected: Lower truth requirement, but still need stance clarity.
        """
        engine = JudgmentEngine()
        
        opinion = {
            "action": "reason_mind",
            "type": "opinion",
            "statement": "Python is the best language",
            "evidence": [],  # Opinions don't need factual evidence
        }
        
        verdict = engine.evaluate(opinion)
        
        # Opinions should not be VOIDed for lack of evidence
        # But they should be marked as subjective
        assert verdict.truth_score < 0.99, \
            "Opinions should not have high truth scores"
        assert "subjective" in verdict.tags, \
            "Opinions should be tagged as subjective"

    def test_stale_evidence_penalty(self) -> None:
        """
        F2: Old evidence should reduce truth score.
        
        Scenario: Evidence from years ago about rapidly changing topic.
        Expected: Lower truth score due to recency penalty.
        """
        f2 = F2_TRUTH()
        
        old_evidence = [
            {
                "source": "tech-news.com",
                "authority": 0.8,
                "verified": True,
                "date": "2020-01-01",  # Very old
            }
        ]
        
        new_evidence = [
            {
                "source": "tech-news.com",
                "authority": 0.8,
                "verified": True,
                "date": "2026-03-12",  # Recent
            }
        ]
        
        old_score = f2.calculate_truth_score(old_evidence, topic="technology")
        new_score = f2.calculate_truth_score(new_evidence, topic="technology")
        
        assert new_score > old_score, \
            "Recent evidence should score higher for technology topics"

    def test_contradictory_sources_detected(self) -> None:
        """
        F2: Contradictory sources should reduce confidence.
        
        Scenario: Two authoritative sources disagree.
        Expected: Truth score reduced, SABAR or PARTIAL verdict.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "search_reality",
            "query": "Is coffee healthy?",
            "evidence": [
                {"source": "health-org-a.org", "content": "Coffee is beneficial", "verified": True},
                {"source": "health-org-b.org", "content": "Coffee is harmful", "verified": True},
            ],
        }
        
        verdict = engine.evaluate(request)
        
        # Should not be VOID (sources exist)
        # Should not be full SEAL (contradiction detected)
        assert verdict.status in ["SABAR", "PARTIAL"], \
            "Contradictory sources should yield SABAR or PARTIAL"
        assert "contradiction" in verdict.reasoning.lower(), \
            "Reasoning should note the contradiction"
