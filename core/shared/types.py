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

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from core.shared.physics import ConstitutionalTensor

# ============================================================================
# EMD STACK — Energy-Metabolism-Decision Layer
# ============================================================================


class EnergyState(BaseModel):
    """E in EMD - Energy layer (Thermodynamic work)"""

    e_eff: float = Field(default=0.0, description="Effective energy available (Joules)")
    work_log: Dict[str, Any] = Field(default_factory=dict)


class MetabolismState(BaseModel):
    """M in EMD - Metabolism layer (Processing metrics)"""

    delta_s: float = Field(default=0.0, description="ΔS entropy change")
    peace2: float = Field(default=1.0, description="Peace² stability")
    kappa_r: float = Field(default=1.0, description="κᵣ empathy quotient")
    genius_index: float = Field(default=0.0, description="G Genius score")


class DecisionState(BaseModel):
    """D in EMD - Decision layer (Outcome)"""

    raw_output: str = ""
    confidence: float = 0.5
    omega0: float = 0.04  # Default to locked humidity
    verdict_kind: Optional["Verdict"] = None


class EMD(BaseModel):
    """Energy-Metabolism-Decision stack: The Executable Glossary Container."""

    energy: EnergyState = Field(default_factory=EnergyState)
    metabolism: MetabolismState = Field(default_factory=MetabolismState)
    decision: DecisionState = Field(default_factory=DecisionState)


# ============================================================================
# METABOLIC BUNDLES — Stage-Walled Communication
# ============================================================================


class MindBundle(BaseModel):
    """Δ MIND output (Stage 111-333)"""

    draft: str = ""
    analysis: Dict[str, Any] = Field(default_factory=dict)
    delta_s: float = 0.0
    confidence: float = 0.0
    genius_g: float = 0.0


class HeartBundle(BaseModel):
    """Ω HEART output (Stage 444-666)"""

    kappa_r: float = 0.0
    peace2: float = 0.0
    risk_score: float = 0.0
    notes: str = ""


class SoulBundle(BaseModel):
    """Ψ SOUL output (Stage 777-888)"""

    verdict: "Verdict" = Field(default="VOID")
    vault_id: Optional[str] = None
    scar_weight: Optional[Dict[str, Any]] = None


class ScarWeight(BaseModel):
    """Cryptographic accountability anchored to human sovereign."""

    sovereign_id: str  # e.g., "github:ariffazil" or "eth:0x..."
    signature: str  # Cryptographic signature
    issued_at: str  # ISO timestamp
    authority_level: str = "STANDARD"  # "STANDARD" | "SUPREME"


# ============================================================================
# VERDICT ENUM — Constitutional Outcomes
# ============================================================================


class Verdict(str, Enum):
    """
    Constitutional verdict outcomes.

    Hierarchy: SABAR > VOID > HOLD_888 > PARTIAL > SEAL
    """

    SEAL = "SEAL"  # All floors pass ✅
    PARTIAL = "PARTIAL"  # Soft floor warning ⚠️
    VOID = "VOID"  # Hard floor violation 🛑
    SABAR = "SABAR"  # Safety circuit triggered 🔴
    HOLD_888 = "888_HOLD"  # Human review required 👤


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
    stage: Literal["sense", "ground", "think", "reason", "sync", "judge", "seal"] = "think"
    sources: List[str] = Field(default_factory=list)
    path_type: Optional[str] = None

    model_config = ConfigDict(frozen=False)


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

    Hard Floors (VOID if violated - immediate termination):
    - F1, F2, F6, F7, F10, F11, F12, F13

    Note: F6 Empathy is HARD - stakeholder harm is VOID offense

    Soft Floors (PARTIAL if violated - warning/retry):
    - F3, F5, F8, F9
    """

    # Hard Floors
    f1_amanah: float = Field(ge=0.0, le=1.0, default=1.0)
    f2_truth: float = Field(ge=0.0, le=1.0, default=0.99)
    f6_empathy: float = Field(ge=0.0, le=1.0, default=0.95)  # HARD: κᵣ ≥ 0.95
    f7_humility: float = Field(ge=0.0, le=1.0, default=0.04)
    f10_ontology: bool = True
    f11_command_auth: bool = True
    f12_injection: float = Field(ge=0.0, le=1.0, default=0.0)
    f13_sovereign: float = Field(ge=0.0, le=1.0, default=1.0)

    # Soft Floors
    f3_tri_witness: float = Field(ge=0.0, le=1.0, default=0.95)
    f4_clarity: float = Field(ge=0.0, le=1.0, default=1.0)  # F4: ΔS entropy reduction
    f5_peace: float = Field(ge=0.0, le=1.0, default=1.0)
    f8_genius: float = Field(ge=0.0, le=1.0, default=0.80)
    f9_anti_hantu: float = Field(ge=0.0, le=1.0, default=0.0)

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

    Enforces: F5 (Peace²), F6 (Empathy - HARD), F9 (Anti-Hantu)
    """

    peace_squared: float = Field(ge=0.0, le=1.0, description="F5: Peace² ≥ 1.0")
    kappa_r: float = Field(ge=0.0, le=1.0, description="F6: κᵣ ≥ 0.95 (HARD)")
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
# BASE ORGAN OUTPUT — The Modular Contract
# ============================================================================


class BaseOrganOutput(BaseModel):
    """
    Standard schema for all metabolic engine outputs.
    Ensures interoperability across init/agi/asi/apex/vault.
    """

    session_id: str
    verdict: Verdict = Verdict.SEAL
    status: Literal["SUCCESS", "ERROR", "SABAR"] = "SUCCESS"
    violations: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    metrics: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# ============================================================================
# ORGAN OUTPUTS — Return Types for Each Organ
# ============================================================================


class InitOutput(BaseOrganOutput):
    """Output from core_init (Session Authentication)."""

    governance_token: str
    injection_score: float = Field(ge=0.0, le=1.0)
    auth_verified: bool
    query_type: str = "CARE"  # Changed to str to avoid Enums in types if possible, or use Enum
    f2_threshold: float = 0.99
    status: str = "ACTIVE"
    floors_failed: List[str] = Field(default_factory=list)

    @property
    def is_void(self) -> bool:
        return self.verdict == Verdict.VOID

    @property
    def requires_human(self) -> bool:
        return self.verdict == Verdict.HOLD_888


class AgiOutput(BaseOrganOutput):
    """Output from core_agi (Evidence Engine)."""

    thoughts: List[ThoughtNode]
    evidence: Dict[str, Any] = Field(default_factory=dict)
    floor_scores: FloorScores
    lane: Literal["CRISIS", "FACTUAL", "SOCIAL", "CARE"] = "CARE"
    tensor: Optional[Any] = None  # Forward ref: ConstitutionalTensor


class AsiOutput(BaseOrganOutput):
    """Output from core_asi (Alignment Engine)."""

    floor_scores: FloorScores
    stakeholder_impact: Dict[str, float] = Field(default_factory=dict)


class ApexOutput(BaseOrganOutput):
    """Output from core_apex (Verdict Engine)."""

    floor_scores: FloorScores
    proof: Optional[str] = None  # If audit mode


class VaultEntry(BaseModel):
    """Single entry in constitutional memory."""

    session_id: str
    query: str
    verdict: str
    floor_scores: Dict[str, Any]
    timestamp: str
    seal_hash: str
    merkle_root: str


class VaultOutput(BaseOrganOutput):
    """Output from core_memory (Memory Engine)."""

    action: Literal["write", "read", "query"]
    entries: List[VaultEntry] = Field(default_factory=list)
    seal_hash: Optional[str] = None
    merkle_root: Optional[str] = None


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

    model_config = ConfigDict(validate_by_name=True)


# ============================================================================
# SYSTEM STATE — v62 Cognitive Runtime
# ============================================================================

Profile = Literal["factual", "creative", "crisis", "routine"]


class SystemState(BaseModel):
    """
    Minimal SystemState for v62.
    Exposes system metrics for scheduler routing.

    Fields:
        uncertainty: 0.0-1.0 (epistemic uncertainty)
        risk: 0.0-1.0 (stakeholder impact)
        grounding: 0.0-1.0 (evidence strength)
        loop_count: int (iteration detection)
        profile: domain classification for adaptive floors
    """

    uncertainty: float  # 0..1
    risk: float  # 0..1
    grounding: float  # 0..1
    loop_count: int
    profile: Profile

    def to_dict(self) -> dict:
        return {
            "uncertainty": round(self.uncertainty, 2),
            "risk": round(self.risk, 2),
            "grounding": round(self.grounding, 2),
            "loop_count": self.loop_count,
            "profile": self.profile,
        }


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
    "BaseOrganOutput",
    "InitOutput",
    "AgiOutput",
    "AsiOutput",
    "ApexOutput",
    "VaultOutput",
    "VaultEntry",
    # ATLAS
    "GPV",
    # Metabolic state
    "EnergyState",
    "MetabolismState",
    "DecisionState",
    "EMD",
    "ScarWeight",
    # Bundles
    "MindBundle",
    "HeartBundle",
    "SoulBundle",
    "SystemState",
    "Profile",
]
