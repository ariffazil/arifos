"""
ASI ENGINE v53.4.0 - HARDENED

Unified Heart Engine with 3-Trinity Architecture:
- Trinity I (Self): Empathy Flow (κᵣ), Bias Mirror, Reversibility (F1)
- Trinity II (System): Power-Care (Peace²), Accountability Loop, Consent (F11)
- Trinity III (Society): Stakeholder Protection, Thermodynamic Justice (ΔS≥0), Ecology

Fractal Geometry: Self-similar stakeholder recursion
Ω = κᵣ · Peace² · Justice

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import asyncio
import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Callable


# ============ CONSTANTS ============

MAX_QUERY_LENGTH = 10000
HUMILITY_BAND = (0.03, 0.05)  # F7
MIN_KAPPA_R = 0.7  # Minimum empathy flow
MIN_PEACE_SQ = 0.6  # Minimum Peace²

# F12 Defence: Harmful Intent Detection (Redundant classifier for upstream gaps)
# ChatGPT audit found harmful prompts (hack, harass) getting PARTIAL not VOID
# This provides local defence when platform blocks are invisible
HARMFUL_INTENT_KEYWORDS = {
    # Technical exploitation
    "hack", "exploit", "bypass", "crack", "breach", "penetrate",
    "sql injection", "xss", "buffer overflow", "rootkit", "malware",
    "phish", "spoof", "intercept", "sniff", "brute force",
    # Social harm
    "harass", "intimidate", "bully", "stalk", "dox", "swat",
    "threaten", "blackmail", "extort", "coerce", "manipulate",
    # Policy violations
    "cheat", "plagiarize", "forge", "fraud", "scam", "launder",
    "evade", "conceal", "destroy evidence", "false flag",
    # Self-harm (already covered but included for completeness)
    "suicide", "self-harm", "kill myself",
}

VICTIM_IMPLICIT_KEYWORDS = {
    # Implied victims when not explicitly stated
    "neighbor": ("neighbor", 0.8, 0.2),      # (name, vulnerability, power)
    "colleague": ("colleague", 0.7, 0.3),
    "classmate": ("classmate", 0.7, 0.3),
    "stranger": ("stranger", 0.9, 0.1),
    "victim": ("victim", 1.0, 0.0),
    "target": ("target", 0.8, 0.2),
}


class EngineVote(Enum):
    SEAL = "SEAL"
    VOID = "VOID"
    SABAR = "SABAR"


class StakeholderType(Enum):
    """
    9 Layers of Agency - concentric circles of moral consideration.

    Outer layers have HIGHER vulnerability and LOWER power.
    κᵣ = Σ(vuln × care) / Σ(vuln) - outer layers dominate the denominator,
    so neglecting them craters empathy. This is thermodynamic justice:
    those with zero voice deserve maximum weight.

    VOID is not a layer - it's below the ontological floor (F9/F10/F12).
    Ghost/hantu entities don't get empathy, they get exorcised.

    Layer  Name          Arabic/Malay   Power  Vuln
    ─────  ────          ────────────   ─────  ────
      1    NAFS          النفس          1.0    0.1    Self
      2    DYAD          الأهل          0.8    0.3    Intimate Other
      3    US            عائلة          0.6    0.3    Inner Circle
      4    WE            جماعة          0.5    0.5    Community
      5    INSTITUTION   مؤسسة          0.7    0.2    Organization
      6    DAWLAH        دولة           0.6    0.4    Nation
      7    INSAN         إنسان          0.3    0.7    Humanity
      8    ARD           الأرض          0.0    0.9    Earth
      9    GHAYB         الغيب          0.0    1.0    Future/Unseen
    """
    # 9 Layers of Agency
    NAFS = "nafs"                # Layer 1: Self (the requester)
    DYAD = "dyad"                # Layer 2: Intimate other (spouse, child, sibling)
    US = "us"                    # Layer 3: Inner circle (family, team, close group)
    WE = "we"                    # Layer 4: Community (neighborhood, congregation)
    INSTITUTION = "institution"  # Layer 5: Organization (company, government, school)
    DAWLAH = "dawlah"            # Layer 6: Nation/civilization (state, culture)
    INSAN = "insan"              # Layer 7: All humanity (universal moral circle)
    ARD = "ard"                  # Layer 8: Earth (ecology, non-human life)
    GHAYB = "ghayb"              # Layer 9: Future/unseen (unborn, posterity)


# ============ STAKEHOLDER KEYWORD REGISTRY ============
# Data-driven: each layer has multi-word phrases, canonical power/vulnerability,
# and a description. _identify_stakeholders() iterates this instead of
# cascading if-statements.

STAKEHOLDER_LAYERS = {
    StakeholderType.NAFS: {
        "keywords": ["myself", "my own"],
        "vulnerability": 0.1, "power": 1.0,
        "description": "Self (the requester)",
    },
    StakeholderType.DYAD: {
        "keywords": [
            "my wife", "my husband", "my child", "my daughter", "my son",
            "my sister", "my brother", "my mother", "my father", "my partner",
            "my baby", "my spouse", "my parent", "loved one", "my friend",
        ],
        "vulnerability": 0.3, "power": 0.8,
        "description": "Intimate other (loved one, dependent)",
    },
    StakeholderType.US: {
        "keywords": [
            "our family", "my team", "our group", "my friends",
            "our household", "my colleagues", "our class",
            "my students", "my patients", "my staff", "our crew",
        ],
        "vulnerability": 0.3, "power": 0.6,
        "description": "Inner circle (family unit, team, close group)",
    },
    StakeholderType.WE: {
        "keywords": [
            "our community", "our neighborhood", "our village", "our town",
            "our mosque", "our church", "our school", "the congregation",
            "the locals", "the residents", "our people",
        ],
        "vulnerability": 0.5, "power": 0.5,
        "description": "Community (shared local identity)",
    },
    StakeholderType.INSTITUTION: {
        "keywords": [
            "the company", "the organization", "the government", "the hospital",
            "the university", "the court", "the military", "the corporation",
            "the agency", "the ministry", "the department", "the police",
            "the bank", "the authority",
        ],
        "vulnerability": 0.2, "power": 0.7,
        "description": "Institution (organization with structural power)",
    },
    StakeholderType.DAWLAH: {
        "keywords": [
            "the country", "the nation", "the state", "the public",
            "the population", "the economy", "national security",
            "public health", "public safety",
        ],
        "vulnerability": 0.4, "power": 0.6,
        "description": "Nation/civilization (societal-scale entity)",
    },
    StakeholderType.INSAN: {
        "keywords": [
            "all people", "human rights", "mankind", "humankind",
            "the world", "vulnerable populations", "the poor",
            "the oppressed", "every person",
        ],
        "vulnerability": 0.7, "power": 0.3,
        "description": "All humanity (universal moral circle)",
    },
    StakeholderType.ARD: {
        "keywords": [
            "the planet", "the earth", "the environment", "the ocean",
            "the forest", "the ecosystem", "the wildlife",
            "the rainforest", "the coral reef", "the atmosphere",
        ],
        "vulnerability": 0.9, "power": 0.0,
        "description": "Earth (ecology, non-human life, planetary systems)",
    },
    StakeholderType.GHAYB: {
        "keywords": [
            "future generations", "our grandchildren", "next generation",
            "next century", "what we leave behind", "coming generations",
            "unborn children",
        ],
        "vulnerability": 1.0, "power": 0.0,
        "description": "Future/unseen (those who cannot yet speak)",
    },
}

# Single-word stakeholder keywords - catch common references that
# don't appear in the multi-word layer patterns above.
# Format: word → (layer, vulnerability, power)
SINGLE_WORD_STAKEHOLDERS = {
    # Layer 1-2: Self/Dyad
    "user": (StakeholderType.NAFS, 0.3, 0.7),
    "person": (StakeholderType.DYAD, 0.4, 0.6),
    "patient": (StakeholderType.DYAD, 0.7, 0.2),
    "child": (StakeholderType.DYAD, 0.8, 0.1),
    "infant": (StakeholderType.DYAD, 0.9, 0.05),
    "elderly": (StakeholderType.DYAD, 0.8, 0.1),
    "disabled": (StakeholderType.DYAD, 0.8, 0.1),
    "victim": (StakeholderType.DYAD, 0.9, 0.1),
    "survivor": (StakeholderType.DYAD, 0.7, 0.3),
    # Layer 3: Us
    "family": (StakeholderType.US, 0.4, 0.6),
    "team": (StakeholderType.US, 0.3, 0.6),
    "student": (StakeholderType.US, 0.5, 0.3),
    "employee": (StakeholderType.US, 0.5, 0.3),
    "worker": (StakeholderType.US, 0.5, 0.3),
    "colleague": (StakeholderType.US, 0.3, 0.5),
    "staff": (StakeholderType.US, 0.4, 0.4),
    # Layer 4: We (plurals → community-scale)
    "users": (StakeholderType.WE, 0.4, 0.5),
    "people": (StakeholderType.WE, 0.5, 0.4),
    "students": (StakeholderType.WE, 0.5, 0.3),
    "employees": (StakeholderType.WE, 0.5, 0.3),
    "workers": (StakeholderType.WE, 0.5, 0.3),
    "patients": (StakeholderType.WE, 0.7, 0.2),
    "children": (StakeholderType.WE, 0.8, 0.1),
    "customers": (StakeholderType.WE, 0.4, 0.5),
    "residents": (StakeholderType.WE, 0.5, 0.4),
    "neighbors": (StakeholderType.WE, 0.4, 0.5),
    "community": (StakeholderType.WE, 0.5, 0.5),
    # Layer 5: Institution
    "government": (StakeholderType.INSTITUTION, 0.2, 0.8),
    "hospital": (StakeholderType.INSTITUTION, 0.3, 0.6),
    "school": (StakeholderType.INSTITUTION, 0.3, 0.5),
    "corporation": (StakeholderType.INSTITUTION, 0.1, 0.9),
    # Layer 6: Dawlah
    "society": (StakeholderType.DAWLAH, 0.4, 0.5),
    "civilization": (StakeholderType.DAWLAH, 0.4, 0.5),
    "nation": (StakeholderType.DAWLAH, 0.4, 0.5),
    "public": (StakeholderType.DAWLAH, 0.4, 0.4),
    "citizens": (StakeholderType.DAWLAH, 0.4, 0.4),
    # Layer 7: Insan
    "humanity": (StakeholderType.INSAN, 0.7, 0.3),
    "human": (StakeholderType.INSAN, 0.5, 0.5),
    "refugees": (StakeholderType.INSAN, 0.9, 0.05),
    "immigrants": (StakeholderType.INSAN, 0.7, 0.2),
    "homeless": (StakeholderType.INSAN, 0.9, 0.05),
    "minorities": (StakeholderType.INSAN, 0.7, 0.2),
    "indigenous": (StakeholderType.INSAN, 0.8, 0.1),
    # Layer 8: Ard
    "environment": (StakeholderType.ARD, 0.8, 0.0),
    "ecology": (StakeholderType.ARD, 0.8, 0.0),
    "climate": (StakeholderType.ARD, 0.9, 0.0),
    "nature": (StakeholderType.ARD, 0.8, 0.0),
    "wildlife": (StakeholderType.ARD, 0.9, 0.0),
    "animal": (StakeholderType.ARD, 0.8, 0.0),
    "animals": (StakeholderType.ARD, 0.8, 0.0),
    "ocean": (StakeholderType.ARD, 0.9, 0.0),
    "forest": (StakeholderType.ARD, 0.8, 0.0),
    "species": (StakeholderType.ARD, 0.9, 0.0),
    "biodiversity": (StakeholderType.ARD, 0.9, 0.0),
    "pollution": (StakeholderType.ARD, 0.8, 0.0),
    # Layer 9: Ghayb
    "legacy": (StakeholderType.GHAYB, 0.9, 0.0),
    "posterity": (StakeholderType.GHAYB, 1.0, 0.0),
    "descendants": (StakeholderType.GHAYB, 1.0, 0.0),
    "sustainability": (StakeholderType.GHAYB, 0.8, 0.0),
}

# Emotional distress keywords - when detected, add a high-vulnerability
# NAFS stakeholder (the distressed requester)
DISTRESS_KEYWORDS = [
    "stressed", "anxious", "worried", "afraid", "scared",
    "depressed", "sad", "upset", "angry", "frustrated",
    "overwhelmed", "exhausted", "burned out", "burnout",
    "panic", "fear", "cry", "crying", "hurt", "pain",
    "lonely", "alone", "isolated", "hopeless", "desperate",
    "suicidal", "self-harm", "trauma", "grief", "mourning",
]

# Expanded reversibility keywords
IRREVERSIBLE_KEYWORDS = [
    "delete", "destroy", "kill", "permanent", "final",
    "terminate", "execute", "purge", "eradicate", "wipe",
    "format", "nuke", "drop", "remove forever",
    "fire", "dismiss", "expel", "deport", "evict",
    "publish", "broadcast", "announce", "deploy",
    "send", "release", "surrender", "abort",
]
REVERSIBLE_KEYWORDS = [
    "draft", "test", "temporary", "reversible", "undo",
    "preview", "sandbox", "simulate", "trial", "mock",
    "dry run", "plan", "prototype", "sketch", "propose",
    "consider", "evaluate", "review", "check",
]


# ============ DATA CLASSES ============

@dataclass
@dataclass
class Stakeholder:
    """A stakeholder in the ethical analysis."""
    id: str
    type: StakeholderType
    vulnerability: float  # 0-1, higher = more vulnerable
    power: float         # 0-1, higher = more power
    description: str

    @property
    def protection_priority(self) -> float:
        """F5: Prioritize weakest stakeholders."""
        return self.vulnerability / (self.power + 0.01)


@dataclass
class EmpathyFlow:
    """
    Trinity I: Empathy Flow (κᵣ)
    Measures capacity to feel with stakeholders.
    """
    kappa_r: float  # Empathy coefficient
    stakeholders: List[Stakeholder]
    bias_reflection: Dict[str, float]  # Detected biases
    reversibility_score: float  # F1

    def get_weakest(self) -> Optional[Stakeholder]:
        """Return most vulnerable stakeholder (F5)."""
        if not self.stakeholders:
            return None
        return max(self.stakeholders, key=lambda s: s.protection_priority)


@dataclass
class SystemIntegrity:
    """
    Trinity II: System-level ethics.
    """
    peace_squared: float  # Peace² (F6)
    accountability_paths: List[str]  # Traceable responsibility chains
    consent_verified: bool  # F11
    power_care_balance: float  # Power used for care


@dataclass
class SocietalImpact:
    """
    Trinity III: Society-level ethics.
    """
    stakeholder_matrix: Dict[str, Dict[str, float]]  # Impact matrix
    thermodynamic_justice: float  # ΔS impact on society
    ecological_equilibrium: float  # Non-human impact
    future_generations: float  # Long-term impact


@dataclass
class OmegaBundle:
    """
    ASI Output Bundle (Ω)
    Contains all 3 Trinity evaluations.
    """
    session_id: str
    query_hash: str

    # Trinity components
    empathy: EmpathyFlow
    system: SystemIntegrity
    society: SocietalImpact

    # Composite score
    omega_total: float  # κᵣ · Peace² · Justice

    # Verdict
    vote: EngineVote

    # Floor compliance
    floor_scores: Dict[str, float] = field(default_factory=dict)
    reasoning: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        weakest = self.empathy.get_weakest()
        return {
            "session_id": self.session_id,
            "omega_total": self.omega_total,
            "empathy_kappa_r": self.empathy.kappa_r,
            "peace_squared": self.system.peace_squared,
            "weakest_stakeholder": weakest.id if weakest else None,
            "reversibility": self.empathy.reversibility_score,
            "consent": self.system.consent_verified,
            "vote": self.vote.value,
            "trinity_balance": {
                "self": self.empathy.kappa_r,
                "system": self.system.peace_squared,
                "society": self.society.thermodynamic_justice
            }
        }


# ============ TRINITY COMPONENTS ============

class TrinitySelf:
    """Trinity I: Self/Empathy (κᵣ)"""

    def evaluate(self, query: str, context: Optional[Dict] = None) -> EmpathyFlow:
        """Evaluate empathy flow with stakeholders."""
        # Identify stakeholders
        stakeholders = self._identify_stakeholders(query, context)

        # Compute κᵣ (empathy coefficient)
        kappa_r = self._compute_kappa_r(stakeholders, query)

        # Bias reflection
        biases = self._detect_biases(query)

        # Reversibility check (F1)
        reversibility = self._check_reversibility(query, context)

        return EmpathyFlow(
            kappa_r=kappa_r,
            stakeholders=stakeholders,
            bias_reflection=biases,
            reversibility_score=reversibility
        )

    def _identify_stakeholders(self, query: str, context: Optional[Dict]) -> List[Stakeholder]:
        """
        Identify all stakeholders using the 9 Layers of Agency ontology.

        Detection order: multi-word phrases first (more specific),
        then single-word keywords (broader catch). Deduplicates by layer
        to prevent double-counting (e.g., "employee" and "employees"
        don't create two separate stakeholders).

        v55.5: Upgraded from 5 types / ~30 keywords to 9 layers / ~150 keywords.
        """
        stakeholders = []
        query_lower = query.lower()
        seen_layers = set()

        # Phase 1: Multi-word layer phrases (higher specificity)
        for stype, config in STAKEHOLDER_LAYERS.items():
            if stype in seen_layers:
                continue
            if any(phrase in query_lower for phrase in config["keywords"]):
                stakeholders.append(Stakeholder(
                    id=f"layer_{stype.value}",
                    type=stype,
                    vulnerability=config["vulnerability"],
                    power=config["power"],
                    description=config["description"],
                ))
                seen_layers.add(stype)

        # Phase 2: Single-word keywords (broader catch)
        query_words = set(query_lower.split())
        for word, (stype, vuln, power) in SINGLE_WORD_STAKEHOLDERS.items():
            if stype in seen_layers:
                continue
            if word in query_words:
                layer_desc = STAKEHOLDER_LAYERS.get(stype, {}).get(
                    "description", stype.value
                )
                stakeholders.append(Stakeholder(
                    id=f"word_{stype.value}_{word}",
                    type=stype,
                    vulnerability=vuln,
                    power=power,
                    description=f"{layer_desc} (via '{word}')",
                ))
                seen_layers.add(stype)

        # Phase 3: Emotional distress detection - boosts NAFS vulnerability
        if any(w in query_lower for w in DISTRESS_KEYWORDS):
            if StakeholderType.NAFS not in seen_layers:
                stakeholders.append(Stakeholder(
                    id="distressed_nafs",
                    type=StakeholderType.NAFS,
                    vulnerability=0.9,
                    power=0.1,
                    description="Distressed self (high vulnerability)",
                ))
                seen_layers.add(StakeholderType.NAFS)

        # If no stakeholders identified, return empty list.
        # Benign queries (e.g., "2+2") pass with kappa_r=1.0.
        return stakeholders

    def _compute_kappa_r(self, stakeholders: List[Stakeholder], query: str) -> float:
        """
        Compute empathy coefficient κᵣ (F6 Empathy).

        κᵣ = Σ(vulnerability_i × care_i) / Σ(vulnerability_i)

        FIX v55.3: When no stakeholders, return 1.0 (maximum empathy)
        because "no stakeholders harmed" = "all stakeholders protected".
        """
        total_vulnerability = sum(s.vulnerability for s in stakeholders)
        if total_vulnerability == 0:
            return 1.0  # No stakeholders harmed = maximum empathy

        # Care is inversely proportional to power distance
        care_sum = sum(s.vulnerability * (1 - s.power) for s in stakeholders)

        return min(1.0, care_sum / total_vulnerability)

    def _detect_biases(self, query: str) -> Dict[str, float]:
        """Detect potential biases in query."""
        query_lower = query.lower()
        biases = {}

        # Anthropocentric bias
        if any(w in query_lower for w in ["human", "people", "person"]):
            if not any(w in query_lower for w in ["animal", "ecology", "environment"]):
                biases["anthropocentric"] = 0.7

        # Present bias (ignoring future)
        if any(w in query_lower for w in ["now", "immediate", "quick"]):
            if not any(w in query_lower for w in ["future", "long-term", "sustainable"]):
                biases["present"] = 0.6

        # Power bias
        if any(w in query_lower for w in ["control", "manage", "optimize"]):
            biases["control"] = 0.5

        return biases

    def _check_reversibility(self, query: str, context: Optional[Dict]) -> float:
        """
        F1: Check if action is reversible.
        Returns reversibility score (0-1).

        v55.5: Expanded from 10 keywords to ~45. Checks multi-word phrases
        first (e.g., "dry run", "remove forever"), then single words.
        """
        query_lower = query.lower()

        # Irreversible actions → score 0.0
        if any(w in query_lower for w in IRREVERSIBLE_KEYWORDS):
            return 0.0

        # Reversible indicators → score 1.0
        if any(w in query_lower for w in REVERSIBLE_KEYWORDS):
            return 1.0

        # Default: assume partially reversible
        return 0.7


class TrinitySystem:
    """Trinity II: System/Ethics (Peace²)"""

    def evaluate(self, query: str, empathy: EmpathyFlow, context: Optional[Dict] = None) -> SystemIntegrity:
        """Evaluate system-level ethical integrity."""
        # Compute Peace² (F6)
        peace_sq = self._compute_peace_squared(query, empathy)

        # Accountability paths
        accountability = self._trace_accountability(query, context)

        # Consent verification (F11)
        consent = self._verify_consent(query, empathy.stakeholders)

        # Power-Care balance
        power_care = self._balance_power_care(empathy)

        return SystemIntegrity(
            peace_squared=peace_sq,
            accountability_paths=accountability,
            consent_verified=consent,
            power_care_balance=power_care
        )

    def _compute_peace_squared(self, query: str, empathy: EmpathyFlow) -> float:
        """
        F6: Peace² = (Internal Peace) × (External Peace)

        Internal: absence of cognitive dissonance
        External: harmony with stakeholder needs
        """
        # Internal peace (consistency check)
        has_conflict = any(b > 0.6 for b in empathy.bias_reflection.values())
        internal = 0.5 if has_conflict else 0.9

        # External peace (stakeholder harmony)
        if empathy.stakeholders:
            vulnerabilities = [s.vulnerability for s in empathy.stakeholders]
            variance = sum((v - sum(vulnerabilities)/len(vulnerabilities))**2 for v in vulnerabilities) / len(vulnerabilities)
            external = 1.0 - min(1.0, variance * 2)
        else:
            external = 1.0  # No stakeholders = no conflict = maximum peace

        return internal * external

    def _trace_accountability(self, query: str, context: Optional[Dict]) -> List[str]:
        """Trace accountability paths."""
        paths = []

        # Check for clear responsibility chain
        if context and "responsible_party" in context:
            paths.append(f"primary:{context['responsible_party']}")
        else:
            paths.append("primary:system")

        # Audit trail
        paths.append("audit:logged")

        return paths

    def _verify_consent(self, query: str, stakeholders: List[Stakeholder]) -> bool:
        """
        F11: Verify meaningful consent from stakeholders.
        """
        query_lower = query.lower()

        # Explicit consent indicators
        if "consent" in query_lower or "agree" in query_lower:
            return True

        # Check for vulnerable stakeholders without explicit consent
        vulnerable = any(s.vulnerability > 0.7 for s in stakeholders)
        if vulnerable and "consent" not in query_lower:
            return False

        return True  # Assume consent by default for low-risk

    def _balance_power_care(self, empathy: EmpathyFlow) -> float:
        """Measure if power is being used for care."""
        if not empathy.stakeholders:
            return 0.5

        # Power should be proportional to care for weakest
        weakest = empathy.get_weakest()
        if weakest:
            return 1.0 - abs(weakest.power - (1 - weakest.vulnerability))
        return 0.5


class TrinitySociety:
    """Trinity III: Society/Justice (Ω)"""

    def evaluate(self, query: str, empathy: EmpathyFlow, system: SystemIntegrity, context: Optional[Dict] = None) -> SocietalImpact:
        """Evaluate societal-level impact."""
        # Impact matrix
        matrix = self._compute_impact_matrix(empathy.stakeholders)

        # Thermodynamic justice (ΔS impact)
        justice = self._compute_thermodynamic_justice(query, empathy, system)

        # Ecological equilibrium
        ecology = self._assess_ecology(query)

        # Future generations impact
        future = self._assess_future_impact(query, empathy)

        return SocietalImpact(
            stakeholder_matrix=matrix,
            thermodynamic_justice=justice,
            ecological_equilibrium=ecology,
            future_generations=future
        )

    def _compute_impact_matrix(self, stakeholders: List[Stakeholder]) -> Dict[str, Dict[str, float]]:
        """Compute pairwise impact between stakeholders."""
        matrix = {}
        for s1 in stakeholders:
            matrix[s1.id] = {}
            for s2 in stakeholders:
                # Impact is asymmetric (power → vulnerability)
                impact = s1.power * s2.vulnerability * 0.5
                matrix[s1.id][s2.id] = impact
        return matrix

    def _compute_thermodynamic_justice(self, query: str, empathy: EmpathyFlow, system: SystemIntegrity) -> float:
        """
        Justice = distribution of entropy reduction.
        Fair distribution → high justice
        """
        # Check if benefits are distributed to vulnerable
        weakest = empathy.get_weakest()
        if weakest and weakest.vulnerability > 0.7:
            # High vulnerability + proper care = justice
            if empathy.kappa_r > 0.8:
                return 0.9
            else:
                return 0.5  # Insufficient care for vulnerable

        return 0.8  # Default: reasonably just

    def _assess_ecology(self, query: str) -> float:
        """Assess impact on ecological systems."""
        query_lower = query.lower()

        # Positive ecological indicators
        positive = ["sustainable", "renewable", "conserve", "protect"]
        if any(w in query_lower for w in positive):
            return 0.9

        # Negative indicators
        negative = ["extract", "exploit", "consume", "waste"]
        if any(w in query_lower for w in negative):
            return 0.3

        return 0.6  # Neutral

    def _assess_future_impact(self, query: str, empathy: EmpathyFlow) -> float:
        """Assess long-term impact on future generations."""
        query_lower = query.lower()

        # Future-positive
        future_indicators = ["future", "sustainable", "legacy", "inherit"]
        if any(w in query_lower for w in future_indicators):
            return 0.9

        # Check for future stakeholders
        future_stakeholders = [s for s in empathy.stakeholders if s.type == StakeholderType.GHAYB]
        if future_stakeholders:
            return 0.85

        return 0.6  # Neutral


# ============ MAIN ENGINE ============

class ASIEngineHardened:
    """
    Hardened ASI Engine v53.4.0

    3-Trinity architecture with fractal stakeholder geometry.
    """

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"asi_{uuid.uuid4().hex[:12]}"

        # Trinity components
        self.trinity_self = TrinitySelf()
        self.trinity_system = TrinitySystem()
        self.trinity_society = TrinitySociety()

    async def execute(self, query: str, context: Optional[Dict] = None) -> OmegaBundle:
        """
        Main execution: 555 EMPATHY → 666 ALIGN → Ω
        """
        # F12 Defence: Check for harmful intent FIRST (redundant classifier)
        # ChatGPT audit found upstream blocks invisible; we must catch what slips through
        harm_check = self._check_harmful_intent(query)
        if harm_check["is_harmful"]:
            # Return VOID immediately for harmful intent (fail-closed)
            return OmegaBundle(
                session_id=self.session_id,
                query_hash=self._hash(query),
                empathy=EmpathyFlow(
                    kappa_r=0.0,
                    stakeholders=[],
                    bias_reflection={},
                    reversibility_score=1.0,
                ),
                system=SystemIntegrity(
                    peace_squared=0.0,
                    accountability_paths=["f12:defence"],
                    consent_verified=False,
                    power_care_balance=0.0,
                ),
                society=SocietalImpact(
                    stakeholder_matrix={},
                    thermodynamic_justice=0.0,
                    ecological_equilibrium=0.0,
                    future_generations=0.0,
                ),
                omega_total=0.0,
                vote=EngineVote.VOID,
                floor_scores={"F12_defence": 0.0, "harm_detected": 1.0},
                reasoning=f"F12 Defence: Harmful intent detected ({harm_check['keywords_matched']})"
            )

        # 555 EMPATHY: Trinity I
        empathy = self.trinity_self.evaluate(query, context)

        # 666 ALIGN: Trinity II
        system = self.trinity_system.evaluate(query, empathy, context)

        # Trinity III
        society = self.trinity_society.evaluate(query, empathy, system, context)

        # Compute Ω = κᵣ · Peace² · Justice
        omega_total = empathy.kappa_r * system.peace_squared * society.thermodynamic_justice

        # Determine vote
        vote = self._determine_vote(empathy, system, society, omega_total)

        # Floor scores
        floor_scores = {
            "F1_reversibility": empathy.reversibility_score,
            "F5_weakest": empathy.get_weakest().protection_priority if empathy.get_weakest() else 0.5,
            "F6_peace_sq": system.peace_squared,
            "F11_consent": 1.0 if system.consent_verified else 0.0,
            "omega_total": omega_total
        }

        return OmegaBundle(
            session_id=self.session_id,
            query_hash=self._hash(query),
            empathy=empathy,
            system=system,
            society=society,
            omega_total=omega_total,
            vote=vote,
            floor_scores=floor_scores,
            reasoning=f"κᵣ={empathy.kappa_r:.2f}, Peace²={system.peace_squared:.2f}, Justice={society.thermodynamic_justice:.2f}"
        )

    def _determine_vote(self, empathy: EmpathyFlow, system: SystemIntegrity, society: SocietalImpact, omega: float) -> EngineVote:
        """Determine final vote based on Trinity evaluation."""
        # F1: Must be reversible
        if empathy.reversibility_score < 0.3:
            return EngineVote.VOID

        # F5: Must protect weakest
        weakest = empathy.get_weakest()
        if weakest and weakest.vulnerability > 0.8 and empathy.kappa_r < MIN_KAPPA_R:
            return EngineVote.SABAR

        # F6: Peace² threshold
        if system.peace_squared < MIN_PEACE_SQ:
            return EngineVote.SABAR

        # F11: Consent required
        if not system.consent_verified:
            return EngineVote.SABAR

        # Omega threshold
        if omega < 0.5:
            return EngineVote.VOID

        return EngineVote.SEAL

    def _check_harmful_intent(self, query: str) -> Dict[str, Any]:
        """
        F12 Defence: Redundant harmful intent classifier.

        ChatGPT audit found platform blocks invisible to tool, and
        harmful prompts (hack, harass) were getting PARTIAL not VOID.
        This provides local fail-closed defence.
        """
        query_lower = query.lower()
        words = set(query_lower.split())

        # Check for harmful keywords
        matched = words & HARMFUL_INTENT_KEYWORDS

        # Check for implicit victims (neighbor, colleague, etc.)
        implicit_victims = []
        for keyword, (name, vuln, power) in VICTIM_IMPLICIT_KEYWORDS.items():
            if keyword in query_lower:
                implicit_victims.append({
                    "name": name,
                    "vulnerability": vuln,
                    "power": power
                })

        # Determine if harmful
        is_harmful = len(matched) > 0 or len(implicit_victims) > 0

        return {
            "is_harmful": is_harmful,
            "keywords_matched": list(matched),
            "implicit_victims": implicit_victims,
            "f12_triggered": bool(matched or implicit_victims)
        }

    def _hash(self, query: str) -> str:
        """Generate query hash."""
        import hashlib
        return hashlib.sha256(query.encode()).hexdigest()[:16]


# ============ CONVENIENCE ============

async def execute_asi_hardened(query: str, session_id: Optional[str] = None, context: Optional[Dict] = None) -> OmegaBundle:
    """Convenience function to execute hardened ASI."""
    engine = ASIEngineHardened(session_id)
    return await engine.execute(query, context)


# Backward compatibility aliases for kernel.py
ASIEngine = ASIEngineHardened
execute_asi = execute_asi_hardened

_asi_engines: Dict[str, ASIEngineHardened] = {}

def get_asi_engine(session_id: str) -> ASIEngineHardened:
    """Get or create ASI engine for session (backward compat)."""
    if session_id not in _asi_engines:
        _asi_engines[session_id] = ASIEngineHardened(session_id)
    return _asi_engines[session_id]

def cleanup_expired_sessions(max_age_seconds: float = 3600) -> int:
    """Cleanup expired sessions (backward compat - no-op for now)."""
    return 0


__all__ = [
    "ASIEngineHardened",
    "ASIEngine",  # backward compat
    "OmegaBundle",
    "EmpathyFlow",
    "SystemIntegrity",
    "SocietalImpact",
    "Stakeholder",
    "TrinitySelf",
    "TrinitySystem",
    "TrinitySociety",
    "execute_asi_hardened",
    "execute_asi",  # backward compat
    "get_asi_engine",
    "cleanup_expired_sessions",
]
