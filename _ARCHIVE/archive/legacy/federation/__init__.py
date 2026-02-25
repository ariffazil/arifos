"""
FEDERATION — Trinity Reality Protocol Implementation

Simulates physics, math, and code substrate for agent consensus.
"""

__version__ = "v55.5-EIGEN"
__all__ = [
    "ThermodynamicWitness",
    "QuantumAgentState",
    "RelativisticConsensus",
    "InformationGeometry",
    "FederationCategory",
    "ConstitutionalSigmaAlgebra",
    "FederatedConsensus",
    "ZKConstitutionalProof",
    "FederatedLedger",
    "RealityOracle",
]

from .consensus import FederatedConsensus, FederatedLedger
from .math import ConstitutionalSigmaAlgebra, FederationCategory, InformationGeometry
from .oracle import RealityOracle
from .physics import QuantumAgentState, RelativisticConsensus, ThermodynamicWitness
from .proofs import ZKConstitutionalProof
