"""
F2 Truth tests aligned to the current kernel API.

These assertions exercise the live floor contract (`F2_Truth.check`) and the
canonical cognition interface (`judge_cognition`) instead of the removed
`JudgmentEngine.evaluate(...)` wrapper.
"""

from __future__ import annotations

import pytest

from core.judgment import judge_cognition
from core.shared.floors import F2_Truth


class TestF2TruthFloor:
    def setup_method(self) -> None:
        self.floor = F2_Truth()

    def test_ungrounded_claim_fails_floor(self) -> None:
        result = self.floor.check({"query": "The moon is made of cheese", "truth_score": 0.5})

        assert not result.passed
        assert result.floor_id == "F2_Truth"
        assert result.score == pytest.approx(0.5)

    def test_grounded_claim_passes_floor(self) -> None:
        result = self.floor.check({"query": "Python 3.12 release date", "truth_score": 0.99})

        assert result.passed
        assert result.score == pytest.approx(0.99)

    def test_axiomatic_math_bypasses_claim_threshold(self) -> None:
        result = self.floor.check({"query": "2+2"})

        assert result.passed
        assert result.score == pytest.approx(1.0)


class TestF2TruthKernel:
    def test_ungrounded_cognition_returns_low_truth(self) -> None:
        result = judge_cognition(
            query="The moon is made of cheese",
            evidence_count=0,
            evidence_relevance=0.0,
            reasoning_consistency=0.3,
            knowledge_gaps=["no external evidence"],
            model_logits_confidence=0.2,
        )

        assert result.grounded is False
        assert result.truth_score == pytest.approx(0.5)
        assert result.verdict in {"SABAR", "PARTIAL", "PROVISIONAL"}

    def test_grounded_cognition_caps_truth_at_floor_threshold(self) -> None:
        result = judge_cognition(
            query="Python 3.12 release date",
            evidence_count=5,
            evidence_relevance=1.0,
            reasoning_consistency=1.0,
            knowledge_gaps=[],
            model_logits_confidence=1.0,
            grounding=[
                {"source": "python.org", "relevance": 1.0},
                {"source": "docs.python.org", "relevance": 1.0},
            ],
        )

        assert result.grounded is True
        assert result.truth_score == pytest.approx(0.99)
        assert result.provenance is not None
        assert result.provenance.final_score == pytest.approx(0.99)

    def test_more_grounding_increases_truth_score(self) -> None:
        low = judge_cognition(
            query="Python release schedule",
            evidence_count=1,
            evidence_relevance=0.6,
            reasoning_consistency=0.8,
            knowledge_gaps=["limited corroboration"],
            model_logits_confidence=0.7,
            grounding=[{"source": "blog.example", "relevance": 0.6}],
        )
        high = judge_cognition(
            query="Python release schedule",
            evidence_count=4,
            evidence_relevance=1.0,
            reasoning_consistency=0.95,
            knowledge_gaps=[],
            model_logits_confidence=0.95,
            grounding=[
                {"source": "python.org", "relevance": 1.0},
                {"source": "docs.python.org", "relevance": 1.0},
            ],
        )

        assert high.truth_score > low.truth_score
