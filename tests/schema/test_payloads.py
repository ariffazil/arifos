"""
tests/schema/test_payloads.py — Tool-Specific Payload Schema Tests

Validates all 13 tool payload schemas instantiate correctly and
enforce their field contracts.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from arifosmcp.runtime.schema import (
    AnchorSessionPayload,
    ApexDashboardPayload,
    ApexJudgePayload,
    AuditRulesPayload,
    AuditViolation,
    CheckVitalPayload,
    CritiqueThoughtPayload,
    EurekaForgePayload,
    Hypothesis,
    IngestEvidencePayload,
    MemoryEntry,
    MemoryMatch,
    MetabolicLoopPayload,
    ReasonMindPayload,
    SearchRealityPayload,
    SearchResult,
    SealVaultPayload,
    SessionMemoryPayload,
    SimulateHeartPayload,
    StakeholderImpact,
    TOOL_PAYLOAD_REGISTRY,
    VectorMemoryPayload,
)


class TestAnchorSessionPayload:
    def test_defaults(self):
        p = AnchorSessionPayload()
        assert p.state == "active"
        assert p.grounding_required is False

    def test_all_states(self):
        for state in ("active", "resumed", "error"):
            p = AnchorSessionPayload(state=state)
            assert p.state == state


class TestReasonMindPayload:
    def test_defaults(self):
        p = ReasonMindPayload()
        assert p.reasoning_status == "exploratory"
        assert p.confidence_band == "PLAUSIBLE"
        assert p.needs_grounding is True
        assert p.hypotheses == []

    def test_with_hypotheses(self):
        p = ReasonMindPayload(
            reasoning_status="converged",
            confidence_band="CLAIM",
            hypotheses=[
                Hypothesis(path="conservative", band="CLAIM", confidence=0.91, hypothesis="X")
            ],
        )
        assert len(p.hypotheses) == 1
        assert p.hypotheses[0].confidence == 0.91

    def test_hypothesis_confidence_range(self):
        with pytest.raises(ValidationError):
            Hypothesis(path="conservative", band="CLAIM", confidence=1.5, hypothesis="X")


class TestVectorMemoryPayload:
    def test_defaults(self):
        p = VectorMemoryPayload()
        assert p.matches == []
        assert p.count == 0

    def test_with_matches(self):
        p = VectorMemoryPayload(
            matches=[MemoryMatch(id="mem_1", score=0.88, source="vault", summary="test")],
            count=1,
        )
        assert p.count == 1
        assert p.matches[0].id == "mem_1"


class TestSimulateHeartPayload:
    def test_defaults(self):
        p = SimulateHeartPayload()
        assert p.stakeholder_status == "safe"
        assert p.needs_human_review is False

    def test_with_stakeholders(self):
        p = SimulateHeartPayload(
            stakeholder_status="caution",
            stakeholders=[StakeholderImpact(name="user", impact="low", risk=0.12)],
        )
        assert p.stakeholders[0].risk == 0.12

    def test_risk_range(self):
        with pytest.raises(ValidationError):
            StakeholderImpact(name="user", impact="low", risk=1.5)


class TestCritiqueThoughtPayload:
    def test_defaults(self):
        p = CritiqueThoughtPayload()
        assert p.critique_status == "challenged"
        assert p.weaknesses == []
        assert p.recommendation == "refine"


class TestApexJudgePayload:
    def test_defaults(self):
        p = ApexJudgePayload()
        assert p.judgment == "HOLD"
        assert p.human_decision_required is True
        assert p.lawful is False

    def test_seal_judgment(self):
        p = ApexJudgePayload(judgment="SEAL", lawful=True, human_decision_required=False)
        assert p.lawful is True


class TestEurekaForgePayload:
    def test_defaults(self):
        p = EurekaForgePayload()
        assert p.execution_status == "blocked"
        assert p.approval_required is True


class TestSealVaultPayload:
    def test_defaults(self):
        p = SealVaultPayload()
        assert p.sealed is False
        assert p.vault_ref is None

    def test_sealed(self):
        p = SealVaultPayload(sealed=True, vault_ref="vault_999_abc", summary_hash="sha256:abc")
        assert p.sealed is True


class TestSearchRealityPayload:
    def test_defaults(self):
        p = SearchRealityPayload()
        assert p.grounding_status == "none"
        assert p.results == []
        assert p.results_count == 0

    def test_with_results(self):
        p = SearchRealityPayload(
            grounding_status="partial",
            results=[
                SearchResult(title="T", url="https://example.com", source="brave", score=0.82)
            ],
            results_count=1,
        )
        assert p.results[0].score == 0.82


class TestIngestEvidencePayload:
    def test_defaults(self):
        p = IngestEvidencePayload()
        assert p.source_type == "text"
        assert p.content == ""
        assert p.truncated is False


class TestAuditRulesPayload:
    def test_defaults(self):
        p = AuditRulesPayload()
        assert p.passed is True
        assert p.violations == []

    def test_with_violations(self):
        p = AuditRulesPayload(
            floors_checked=["F2", "F4"],
            violations=[
                AuditViolation(floor="F2", severity="critical", description="truth < 0.99")
            ],
            passed=False,
        )
        assert p.passed is False
        assert p.violations[0].floor == "F2"


class TestCheckVitalPayload:
    def test_defaults_all_none(self):
        p = CheckVitalPayload()
        assert p.cpu is None
        assert p.memory is None

    def test_with_values(self):
        p = CheckVitalPayload(cpu=0.21, memory=0.43, swap=0.02)
        assert p.cpu == 0.21

    def test_cpu_range(self):
        with pytest.raises(ValidationError):
            CheckVitalPayload(cpu=1.5)


class TestMetabolicLoopPayload:
    def test_defaults(self):
        p = MetabolicLoopPayload()
        assert p.loop_status == "active"
        assert p.completed_stages == []

    def test_full_payload(self):
        p = MetabolicLoopPayload(
            loop_status="active",
            current_stage="333_MIND",
            next_stage="555_HEART",
            completed_stages=["000_INIT", "111_SENSE", "222_REALITY"],
        )
        assert p.current_stage == "333_MIND"
        assert len(p.completed_stages) == 3


class TestSessionMemoryPayload:
    def test_defaults(self):
        p = SessionMemoryPayload()
        assert p.operation == "retrieve"
        assert p.success is True
        assert p.memories is None

    def test_with_memories(self):
        p = SessionMemoryPayload(
            operation="retrieve",
            memories=[
                MemoryEntry(timestamp="2026-03-10T00:00:00Z", content="test", importance=0.8)
            ],
        )
        assert p.memories[0].importance == 0.8


class TestApexDashboardPayload:
    def test_defaults(self):
        p = ApexDashboardPayload()
        assert p.dashboard_url == ""
        assert p.access_token is None


class TestToolPayloadRegistry:
    def test_all_canonical_tools_registered(self):
        expected_tools = {
            "anchor_session",
            "reason_mind",
            "vector_memory",
            "simulate_heart",
            "critique_thought",
            "apex_judge",
            "eureka_forge",
            "seal_vault",
            "search_reality",
            "ingest_evidence",
            "audit_rules",
            "check_vital",
            "metabolic_loop",
            "arifOS.kernel",
            "session_memory",
            "open_apex_dashboard",
        }
        for tool in expected_tools:
            assert tool in TOOL_PAYLOAD_REGISTRY, f"Missing tool in registry: {tool}"

    def test_registry_values_are_pydantic_models(self):
        from pydantic import BaseModel

        for tool, cls in TOOL_PAYLOAD_REGISTRY.items():
            assert issubclass(cls, BaseModel), f"{tool} payload is not a Pydantic model"

    def test_all_registry_classes_instantiate_with_defaults(self):
        for tool, cls in TOOL_PAYLOAD_REGISTRY.items():
            instance = cls()
            assert instance is not None
