"""
arifOS v60: Constitutional Type System
=======================================

Pydantic contracts for inter-organ communication.

The Contract: All 5 organs speak the same type language.

Version: v60.0-FORGE
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
DITEMPA BUKAN DIBERI 💎🔥🧠
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


# ============================================================================
# VERDICT ENUM — Constitutional Outcomes
# ============================================================================

class Verdict(str, Enum):
    """
    Constitutional verdict outcomes.

    Hierarchy: SABAR > VOID > HOLD_888 > PARTIAL > SEAL
    """
    SEAL = "SEAL"           # All floors pass ✅
    PARTIAL = "PARTIAL"     # Soft floor warning ⚠️
    VOID = "VOID"           # Hard floor violation 🛑
    SABAR = "SABAR"         # Safety circuit triggered 🔴
    HOLD_888 = "888_HOLD"   # Human review required 👤


# ============================================================================
# THOUGHT STRUCTURES — Sequential Reasoning
# ============================================================================

class ThoughtNode(BaseModel):
    """
    Single node in AGI sequential thinking chain.

    Represents one thought in the 333_REASON loop.
    """
    thought: str
    thought_number: int = Field(ge=1)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    next_thought_needed: bool = True
    stage: Literal["sense", "ground", "think", "sync", "judge", "seal"] = "think"
    sources: List[str] = Field(default_factory=list)

    class Config:
        frozen = False  # Allow mutations during reasoning loop


class ThoughtChain(BaseModel):
    """Complete chain of sequential thoughts."""
    thoughts: List[ThoughtNode]
    total_steps: int
    convergence_achieved: bool = False
    final_confidence: float = Field(ge=0.0, le=1.0, default=0.0)


# ============================================================================
# FLOOR SCORES — The 13 Constitutional Floors
# ============================================================================

class FloorScores(BaseModel):
    """
    All 13 constitutional floor scores.

    Hard Floors (VOID if violated):
    - F1, F2, F4, F7, F9, F10, F11, F12, F13

    Soft Floors (PARTIAL if violated):
    - F3, F5, F6, F8
    """
    # Hard Floors
    f1_amanah: float = Field(ge=0.0, le=1.0, default=1.0)
    f2_truth: float = Field(ge=0.0, le=1.0, default=0.99)
    f4_clarity: float = Field(le=0.0, default=0.0)  # ΔS must be ≤ 0
    f7_humility: float = Field(ge=0.0, le=1.0, default=0.04)
    f9_anti_hantu: float = Field(ge=0.0, le=1.0, default=0.0)
    f10_ontology: bool = True
    f11_command_auth: bool = True
    f12_injection: float = Field(ge=0.0, le=1.0, default=0.0)
    f13_sovereign: float = Field(ge=0.0, le=1.0, default=1.0)

    # Soft Floors
    f3_tri_witness: float = Field(ge=0.0, le=1.0, default=0.95)
    f5_peace: float = Field(ge=0.0, le=1.0, default=1.0)
    f6_empathy: float = Field(ge=0.0, le=1.0, default=0.70)
    f8_genius: float = Field(ge=0.0, le=1.0, default=0.80)

    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary."""
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


# ============================================================================
# AGI METRICS — Mind Engine Outputs
# ============================================================================

class AgiMetrics(BaseModel):
    """
    AGI Mind Engine output metrics.

    Enforces: F2 (Truth), F4 (Clarity), F7 (Humility), F8 (Genius partial)
    """
    truth_score: float = Field(ge=0.0, le=1.0, description="F2: τ ≥ 0.99")
    delta_s: float = Field(le=0.0, description="F4: ΔS ≤ 0 (entropy reduction)")
    omega_0: float = Field(ge=0.03, le=0.05, description="F7: Ω₀ ∈ [0.03, 0.05]")
    precision: float = Field(ge=0.0, description="π (Kalman precision)")
    free_energy: float = Field(description="Δ = ΔS + Ω₀·π⁻¹")


class AsiMetrics(BaseModel):
    """
    ASI Heart Engine output metrics.

    Enforces: F5 (Peace²), F6 (Empathy), F9 (Anti-Hantu)
    """
    peace_squared: float = Field(ge=0.0, le=1.0, description="F5: Peace² ≥ 1.0")
    kappa_r: float = Field(ge=0.0, le=1.0, description="F6: κᵣ ≥ 0.70")
    c_dark: float = Field(ge=0.0, le=1.0, description="F9: C_dark < 0.30")


class ApexMetrics(BaseModel):
    """
    APEX Soul Engine output metrics.

    Enforces: F3 (Tri-Witness), F8 (Genius), F10 (Ontology)
    """
    tri_witness: float = Field(ge=0.0, le=1.0, description="F3: W₃ ≥ 0.95")
    genius_g: float = Field(ge=0.0, le=1.0, description="F8: G ≥ 0.80")
    ontology_valid: bool = Field(description="F10: Category lock")


# ============================================================================
# ORGAN OUTPUTS — Return Types for Each Organ
# ============================================================================

class InitOutput(BaseModel):
    """Output from core_init (Session Authentication)."""
    session_id: str
    governance_token: str
    injection_score: float = Field(ge=0.0, le=1.0)
    auth_verified: bool
    verdict: Verdict
    violations: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class AgiOutput(BaseModel):
    """Output from core_agi (Evidence Engine)."""
    thoughts: List[ThoughtNode]
    metrics: AgiMetrics
    evidence: Dict[str, Any] = Field(default_factory=dict)
    floor_scores: FloorScores
    verdict: Verdict
    violations: List[str] = Field(default_factory=list)
    lane: Literal["CRISIS", "FACTUAL", "SOCIAL", "CARE"] = "CARE"
    session_id: str


class AsiOutput(BaseModel):
    """Output from core_asi (Alignment Engine)."""
    metrics: AsiMetrics
    floor_scores: FloorScores
    verdict: Verdict
    violations: List[str] = Field(default_factory=list)
    stakeholder_impact: Dict[str, float] = Field(default_factory=dict)
    session_id: str


class ApexOutput(BaseModel):
    """Output from core_apex (Verdict Engine)."""
    verdict: Verdict
    metrics: ApexMetrics
    floor_scores: FloorScores
    violations: List[str] = Field(default_factory=list)
    proof: Optional[str] = None  # If audit mode
    session_id: str


class VaultEntry(BaseModel):
    """Single entry in constitutional memory."""
    session_id: str
    query: str
    verdict: str
    floor_scores: Dict[str, Any]
    timestamp: str
    seal_hash: str
    merkle_root: str


class VaultOutput(BaseModel):
    """Output from core_memory (Memory Engine)."""
    action: Literal["write", "read", "query"]
    entries: List[VaultEntry] = Field(default_factory=list)
    seal_hash: Optional[str] = None
    merkle_root: Optional[str] = None
    status: Literal["SUCCESS", "ERROR"] = "SUCCESS"
    error_message: Optional[str] = None


# ============================================================================
# GOVERNANCE PLACEMENT VECTOR — ATLAS Types
# ============================================================================

class GPV(BaseModel):
    """
    Governance Placement Vector (from ATLAS Φ function).

    4D constitutional coordinate:
    - lane: Categorical routing
    - τ (tau): Truth demand
    - κ (kappa): Care demand
    - ρ (rho): Risk level
    """
    lane: Literal["CRISIS", "FACTUAL", "SOCIAL", "CARE"]
    tau: float = Field(ge=0.0, le=1.0, alias="τ")  # Truth demand
    kappa: float = Field(ge=0.0, le=1.0, alias="κ")  # Care demand
    rho: float = Field(ge=0.0, le=1.0, alias="ρ")  # Risk level

    class Config:
        allow_population_by_field_name = True


# ============================================================================
# EXPORT PUBLIC API
# ============================================================================

__all__ = [
    # Enums
    "Verdict",

    # Thought Structures
    "ThoughtNode",
    "ThoughtChain",

    # Floor Scores
    "FloorScores",

    # Metrics
    "AgiMetrics",
    "AsiMetrics",
    "ApexMetrics",

    # Organ Outputs
    "InitOutput",
    "AgiOutput",
    "AsiOutput",
    "ApexOutput",
    "VaultOutput",
    "VaultEntry",

    # ATLAS
    "GPV",
]
