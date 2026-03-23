"""
arifosmcp/runtime/substrate_policy.py — The Intelligence Mapping for AAA Wire

This policy defines the Substrate Capability Class and Risk Tier for every mode
in the M-11 Mega-Tool surface. It ensures F4 Clarity and F13 Sovereignty.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

class SubstrateClass(str, Enum):
    INSPECT = "inspect"      # Structure-only observation
    READ = "read"            # Content retrieval (no mutation)
    RECALL = "recall"        # Memory retrieval (no mutation)
    WRITE = "write"          # Create new state
    UPDATE = "update"        # Modify existing state
    DELETE = "delete"        # Remove state (High Risk)
    EXECUTE = "execute"      # Run code/commands (High Risk)
    COMMIT = "commit"        # Atomic finalize (High Risk)
    COMMUNICATE = "communicate" # External signaling (High Risk)

class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"           # Triggers 888_HOLD in hardened loops

@dataclass(frozen=True)
class ModePolicy:
    substrate: SubstrateClass
    risk: RiskTier
    organ_stage: str
    description: str

# The Canonical AAA Tool Policy Matrix
AAA_SUBSTRATE_POLICY = {
    "init_anchor": {
        "init": ModePolicy(SubstrateClass.WRITE, RiskTier.LOW, "000_INIT", "Bind session identity"),
        "state": ModePolicy(SubstrateClass.INSPECT, RiskTier.LOW, "000_INIT", "Check session status"),
        "refresh": ModePolicy(SubstrateClass.UPDATE, RiskTier.MEDIUM, "000_INIT", "Rotate tokens"),
        "revoke": ModePolicy(SubstrateClass.DELETE, RiskTier.HIGH, "000_INIT", "Kill session authority")
    },
    "physics_reality": {
        "search": ModePolicy(SubstrateClass.READ, RiskTier.MEDIUM, "111_SENSE", "Web grounding"),
        "ingest": ModePolicy(SubstrateClass.WRITE, RiskTier.MEDIUM, "111_SENSE", "Evidence creation"),
        "compass": ModePolicy(SubstrateClass.READ, RiskTier.LOW, "111_SENSE", "Directional grounding"),
        "time": ModePolicy(SubstrateClass.INSPECT, RiskTier.LOW, "111_SENSE", "Temporal sync")
    },
    "agi_mind": {
        "reason": ModePolicy(SubstrateClass.READ, RiskTier.MEDIUM, "333_MIND", "First-principles logic"),
        "reflect": ModePolicy(SubstrateClass.INSPECT, RiskTier.MEDIUM, "333_MIND", "Self-audit loop"),
        "forge": ModePolicy(SubstrateClass.WRITE, RiskTier.MEDIUM, "333_MIND", "Artifact synthesis")
    },
    "asi_heart": {
        "critique": ModePolicy(SubstrateClass.READ, RiskTier.MEDIUM, "666_HEART", "Adversarial safety audit"),
        "simulate": ModePolicy(SubstrateClass.READ, RiskTier.MEDIUM, "666_HEART", "Stakeholder impact modeling")
    },
    "engineering_memory": {
        "vector_query": ModePolicy(SubstrateClass.RECALL, RiskTier.MEDIUM, "555_MEMORY", "Semantic retrieval"),
        "vector_store": ModePolicy(SubstrateClass.WRITE, RiskTier.MEDIUM, "555_MEMORY", "Memory commit"),
        "engineer": ModePolicy(SubstrateClass.EXECUTE, RiskTier.HIGH, "555_MEMORY", "High-stakes tool generation")
    },
    "code_engine": {
        "fs": ModePolicy(SubstrateClass.INSPECT, RiskTier.MEDIUM, "M-3_EXEC", "Filesystem inspection"),
        "process": ModePolicy(SubstrateClass.INSPECT, RiskTier.MEDIUM, "M-3_EXEC", "Process monitoring"),
        "run": ModePolicy(SubstrateClass.EXECUTE, RiskTier.HIGH, "M-3_EXEC", "Sandboxed script execution")
    },
    "vault_ledger": {
        "seal": ModePolicy(SubstrateClass.COMMIT, RiskTier.HIGH, "999_VAULT", "Immutable audit seal"),
        "verify": ModePolicy(SubstrateClass.READ, RiskTier.MEDIUM, "999_VAULT", "Integrity check")
    }
}

def get_policy(tool: str, mode: str) -> ModePolicy | None:
    return AAA_SUBSTRATE_POLICY.get(tool, {}).get(mode)
