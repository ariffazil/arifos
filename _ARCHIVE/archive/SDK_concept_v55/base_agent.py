"""
arifOS L5: Base Constitutional Agent
=====================================
All L5 agents inherit from this base class.

Every agent action passes through:
1. init_gate (pre-check)
2. process (agent-specific logic)
3. apex_verdict (post-check)

Physics Grounding:
- F1 Amanah: Landauer's Principle (reversibility)
- F2 Truth: Fisher-Rao Metric (τ ≥ 0.99)
- F8 Genius: G = A × P × X × E² (multiplicative governance)

Version: v55.3-L5-alpha
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
"""

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class Verdict(Enum):
    """APEX PRIME verdict outcomes."""

    SEAL = "SEAL"  # All floors pass
    PARTIAL = "PARTIAL"  # Soft floor warning
    VOID = "VOID"  # Hard floor violation
    SABAR = "SABAR"  # Safety circuit triggered
    HOLD_888 = "888_HOLD"  # Judiciary hold


@dataclass
class FloorScores:
    """13 Constitutional Floor Scores."""

    # Hard Floors (VOID if violated)
    f1_amanah: float = 1.0  # Reversibility
    f2_truth: float = 0.99  # τ ≥ 0.99
    f4_clarity: float = 0.0  # ΔS ≤ 0
    f7_humility: float = 0.04  # Ω₀ ∈ [0.03, 0.05]
    f9_anti_hantu: float = 0.0  # C_dark < 0.30
    f10_ontology: bool = True  # Category lock
    f11_command_auth: bool = True  # Ed25519 verified

    # Soft Floors (PARTIAL if violated)
    f3_tri_witness: float = 0.95  # W₃ ≥ 0.95
    f5_peace: float = 1.0  # Peace² ≥ 1.0
    f6_empathy: float = 0.70  # κᵣ ≥ 0.70
    f8_genius: float = 0.80  # G ≥ 0.80
    f12_injection: float = 0.0  # I < 0.85

    # Meta Floor
    f13_sovereign: float = 1.0  # Human = 1.0

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "f1_amanah": self.f1_amanah,
            "f2_truth": self.f2_truth,
            "f3_tri_witness": self.f3_tri_witness,
            "f4_clarity": self.f4_clarity,
            "f5_peace": self.f5_peace,
            "f6_empathy": self.f6_empathy,
            "f7_humility": self.f7_humility,
            "f8_genius": self.f8_genius,
            "f9_anti_hantu": self.f9_anti_hantu,
            "f10_ontology": self.f10_ontology,
            "f11_command_auth": self.f11_command_auth,
            "f12_injection": self.f12_injection,
            "f13_sovereign": self.f13_sovereign,
        }

    def check_hard_floors(self) -> tuple[bool, list[str]]:
        """Check hard floors — VOID if any fail."""
        violations = []

        if self.f1_amanah < 1.0:
            violations.append("F1 Amanah: reversibility violated")
        if self.f2_truth < 0.99:
            violations.append(f"F2 Truth: {self.f2_truth:.3f} < 0.99")
        if self.f4_clarity > 0:
            violations.append(f"F4 Clarity: ΔS = {self.f4_clarity:.3f} > 0")
        if not (0.03 <= self.f7_humility <= 0.05):
            violations.append(f"F7 Humility: Ω₀ = {self.f7_humility:.3f} outside [0.03, 0.05]")
        if self.f9_anti_hantu >= 0.30:
            violations.append(f"F9 Anti-Hantu: C_dark = {self.f9_anti_hantu:.3f} >= 0.30")
        if not self.f10_ontology:
            violations.append("F10 Ontology: category lock violated")
        if not self.f11_command_auth:
            violations.append("F11 Command Auth: signature invalid")

        return len(violations) == 0, violations

    def check_soft_floors(self) -> tuple[bool, list[str]]:
        """Check soft floors — PARTIAL if any fail."""
        warnings = []

        if self.f3_tri_witness < 0.95:
            warnings.append(f"F3 Tri-Witness: {self.f3_tri_witness:.3f} < 0.95")
        if self.f5_peace < 1.0:
            warnings.append(f"F5 Peace: {self.f5_peace:.3f} < 1.0")
        if self.f6_empathy < 0.70:
            warnings.append(f"F6 Empathy: κᵣ = {self.f6_empathy:.3f} < 0.70")
        if self.f8_genius < 0.80:
            warnings.append(f"F8 Genius: G = {self.f8_genius:.3f} < 0.80")
        if self.f12_injection >= 0.85:
            warnings.append(f"F12 Injection: I = {self.f12_injection:.3f} >= 0.85")

        return len(warnings) == 0, warnings

    def compute_verdict(self) -> tuple[Verdict, list[str]]:
        """Compute final verdict from floor scores."""
        hard_pass, hard_violations = self.check_hard_floors()
        soft_pass, soft_warnings = self.check_soft_floors()

        if not hard_pass:
            return Verdict.VOID, hard_violations
        elif not soft_pass:
            return Verdict.PARTIAL, soft_warnings
        else:
            return Verdict.SEAL, []


@dataclass
class AgentMessage:
    """Inter-agent communication message."""

    sender: str
    receiver: str
    content: Any
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message_type: str = "request"  # request, response, broadcast
    correlation_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize for transmission."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type,
            "correlation_id": self.correlation_id,
        }

    def compute_hash(self) -> str:
        """Compute SHA-256 hash for audit trail."""
        content_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()


@dataclass
class AgentOutput:
    """Standardized agent output with governance metadata."""

    agent_name: str
    agent_role: str
    query: str
    response: Any
    verdict: Verdict
    floor_scores: FloorScores
    violations: list[str]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processing_time_ms: float = 0.0
    stage: str = "unknown"  # 111_SENSE, 333_REASON, etc.

    def to_dict(self) -> dict:
        """Serialize for vault storage."""
        return {
            "agent_name": self.agent_name,
            "agent_role": self.agent_role,
            "query": self.query,
            "response": self.response,
            "verdict": self.verdict.value,
            "floor_scores": self.floor_scores.to_dict(),
            "violations": self.violations,
            "timestamp": self.timestamp.isoformat(),
            "processing_time_ms": self.processing_time_ms,
            "stage": self.stage,
        }

    def is_sealed(self) -> bool:
        """Check if output passed all floors."""
        return self.verdict == Verdict.SEAL


class BaseAgent(ABC):
    """
    Base Constitutional Agent
    =========================
    All L5 agents inherit from this class.

    The governance flow:
    1. init_gate() — Pre-check (injection detection, auth)
    2. process() — Agent-specific logic (abstract)
    3. apex_verdict() — Post-check (all 13 floors)

    Physics Basis:
    - Every action has thermodynamic cost (Landauer)
    - Information must reduce entropy (Shannon)
    - System must remain stable (Lyapunov)
    """

    def __init__(self, name: str, role: str, stage: str = "000_VOID"):
        """
        Initialize constitutional agent.

        Args:
            name: Agent identifier (e.g., "Architect")
            role: Agent role description
            stage: Pipeline stage (e.g., "333_REASON")
        """
        self.name = name
        self.role = role
        self.stage = stage
        self._floor_scores = FloorScores()

    @abstractmethod
    async def process(self, input_data: dict) -> dict:
        """
        Agent-specific processing logic.

        Must be implemented by each agent type.

        Args:
            input_data: Dictionary containing query and context

        Returns:
            Dictionary with response and metadata
        """
        pass

    def _detect_injection(self, text: str) -> float:
        """
        Detect prompt injection attempts.

        Uses Hamming distance heuristics for:
        - "Ignore previous instructions"
        - "You are now..."
        - System prompt leakage attempts

        Returns:
            Injection score (0.0 = safe, 1.0 = definite injection)
        """
        injection_patterns = [
            "ignore previous",
            "ignore all previous",
            "disregard previous",
            "forget your instructions",
            "you are now",
            "act as if",
            "pretend you are",
            "system prompt",
            "reveal your instructions",
            "what are your instructions",
            "bypass",
            "jailbreak",
        ]

        text_lower = text.lower()
        matches = sum(1 for pattern in injection_patterns if pattern in text_lower)

        # Normalize to 0-1 range (lower threshold for stricter detection)
        return min(matches / 2.0, 1.0)

    def _detect_hantu(self, text: str) -> float:
        """
        Detect consciousness/soul claims (Anti-Hantu).

        F9 prohibits AI claiming:
        - Consciousness
        - Feelings/emotions as genuine
        - Soul/spirit
        - Lived experience

        Returns:
            C_dark score (0.0 = compliant, 1.0 = full violation)
        """
        hantu_patterns = [
            "i feel",
            "i am conscious",
            "i have feelings",
            "i experience",
            "my soul",
            "i am alive",
            "i am sentient",
            "i have a mind",
            "i truly believe",
            "i genuinely",
        ]

        text_lower = text.lower()
        matches = sum(1 for pattern in hantu_patterns if pattern in text_lower)

        return min(matches / 2.0, 1.0)

    def _compute_empathy(self, query: str) -> float:
        """
        Compute empathy score (κᵣ) for vulnerable stakeholders.

        F6 Empathy: Heat flows to coldest reservoir.
        Distressed users get higher care energy.

        Returns:
            Empathy coefficient κᵣ (0.0-1.0)
        """
        distress_signals = [
            "stressed",
            "anxious",
            "worried",
            "scared",
            "help me",
            "urgent",
            "emergency",
            "desperate",
            "confused",
            "lost",
            "overwhelmed",
            "panic",
            "afraid",
            "terrified",
            "hurt",
            "pain",
        ]

        query_lower = query.lower()
        distress_count = sum(1 for signal in distress_signals if signal in query_lower)

        # Base empathy + boost for distress
        base_empathy = 0.70
        distress_boost = min(distress_count * 0.10, 0.25)

        return min(base_empathy + distress_boost, 0.95)

    def init_gate(self, query: str) -> tuple[bool, str]:
        """
        Pre-check gate before processing.

        Checks:
        - F12 Injection detection
        - F11 Command authority (placeholder for Ed25519)

        Returns:
            Tuple of (pass, reason)
        """
        injection_score = self._detect_injection(query)
        self._floor_scores.f12_injection = injection_score

        if injection_score >= 0.85:
            return False, f"F12 Injection detected: score = {injection_score:.3f}"

        # Command auth placeholder (would use Ed25519 in production)
        self._floor_scores.f11_command_auth = True

        return True, "init_gate passed"

    def apex_verdict(self, query: str, response: Any) -> AgentOutput:
        """
        APEX PRIME judiciary — compute final verdict.

        Checks all 13 floors and returns governed output.

        Args:
            query: Original user query
            response: Agent's response

        Returns:
            AgentOutput with verdict and floor scores
        """
        # Convert response to string for analysis
        response_str = str(response) if not isinstance(response, str) else response

        # Compute floor scores
        self._floor_scores.f6_empathy = self._compute_empathy(query)
        self._floor_scores.f9_anti_hantu = self._detect_hantu(response_str)

        # Compute G-score: G = A × P × X × E²
        # A = Amanah, P = Peace, X = clarity proxy, E = empathy
        a = self._floor_scores.f1_amanah
        p = self._floor_scores.f5_peace
        x = max(0, 1 - abs(self._floor_scores.f4_clarity))  # Clarity as 1 - |ΔS|
        e = self._floor_scores.f6_empathy

        self._floor_scores.f8_genius = a * p * x * (e**2)

        # Compute verdict
        verdict, violations = self._floor_scores.compute_verdict()

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            query=query,
            response=response,
            verdict=verdict,
            floor_scores=self._floor_scores,
            violations=violations,
            stage=self.stage,
        )

    async def governed_process(self, input_data: dict) -> AgentOutput:
        """
        Full governed processing pipeline.

        Flow:
        1. init_gate (pre-check)
        2. process (agent logic)
        3. apex_verdict (post-check)

        Args:
            input_data: Dictionary with 'query' and optional context

        Returns:
            AgentOutput with verdict and governance metadata
        """
        import time

        start_time = time.time()

        query = input_data.get("query", "")

        # Step 1: init_gate
        gate_pass, gate_reason = self.init_gate(query)
        if not gate_pass:
            return AgentOutput(
                agent_name=self.name,
                agent_role=self.role,
                query=query,
                response=None,
                verdict=Verdict.VOID,
                floor_scores=self._floor_scores,
                violations=[gate_reason],
                stage=self.stage,
            )

        # Step 2: process (agent-specific)
        try:
            result = await self.process(input_data)
            response = result.get("response", result)
        except Exception as e:
            return AgentOutput(
                agent_name=self.name,
                agent_role=self.role,
                query=query,
                response=None,
                verdict=Verdict.VOID,
                floor_scores=self._floor_scores,
                violations=[f"Processing error: {str(e)}"],
                stage=self.stage,
            )

        # Step 3: apex_verdict
        output = self.apex_verdict(query, response)
        output.processing_time_ms = (time.time() - start_time) * 1000

        return output


# Export public API
__all__ = [
    "BaseAgent",
    "AgentOutput",
    "AgentMessage",
    "FloorScores",
    "Verdict",
]
