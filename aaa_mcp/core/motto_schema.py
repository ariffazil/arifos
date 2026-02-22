"""
aaa_mcp/core/motto_schema.py — The 9 Mottos Schema for MCP Transport

This module transports the constitutional mottos to AI/LLM agents via MCP:
- 9 Failure-Response Rhymes (Nusantara cultural identity)
- DITEMPA bookends (INIT 🔥 -> SEAL 💎🧠)
- Floor-to-motto mapping for error context

Used by: server.py, llms.txt context, AI agent prompts
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any
from enum import Enum
from typing import Any, Dict, List, Optional


class MottoStage(str, Enum):
    """The 9 metabolic stages with motto assignments."""

    INIT = "000_INIT"
    SENSE = "111_SENSE"
    THINK = "222_THINK"
    REASON = "333_REASON"
    SYNC = "444_SYNC"
    EMPATHY = "555_EMPATHY"
    ALIGN = "666_ALIGN"
    FORGE = "777_FORGE"
    JUDGE = "888_JUDGE"
    SEAL = "999_SEAL"


@dataclass(frozen=True)
class MottosSchema:
    """
    Schema for transporting the 9 constitutional mottos to AI agents.

    This provides the cultural context and governance mapping that AI agents
    need to understand arifOS's constitutional error handling.
    """

    # The 9 mottos (canonical order)
    mottos: Dict[str, Dict[str, str]]

    # Bookend headers (INIT and SEAL share DITEMPA)
    init_header: str
    seal_header: str

    # Floor-to-motto error mapping
    error_mottos: Dict[str, str]

    # Emoji signatures
    init_emoji: str
    seal_emoji: str

    # Cultural context for AI
    cultural_context: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MCP transport."""
        return asdict(self)

    def get_failure_response(self, floor: str, reason: str) -> Dict[str, str]:
        """Generate a culturally-grounded failure response."""
        motto = self.error_mottos.get(floor, "DITEMPA, BUKAN DIBERI")
        return {
            "floor": floor,
            "reason": reason,
            "motto_malay": motto,
            "motto_english": self._translate_motto(motto),
            "cultural_context": "Nusantara constitutional governance",
        }

    def _translate_motto(self, malay: str) -> str:
        """Quick translation helper."""
        translations = {
            "DITEMPA, BUKAN DIBERI": "Forged, Not Given",
            "DIKAJI, BUKAN DISUAPI": "Examined, Not Spoon-fed",
            "DIJELAJAH, BUKAN DISEKATI": "Explored, Not Restricted",
            "DIJELASKAN, BUKAN DIKABURKAN": "Clarified, Not Obscured",
            "DIHADAPI, BUKAN DITANGGUHI": "Faced, Not Postponed",
            "DIUSAHAKAN, BUKAN DIHARAPI": "Worked For, Not Merely Hoped",
            "DIJAGA, BUKAN DIABAIKAN": "Safeguarded, Not Neglected",
            "DIDAMAIKAN, BUKAN DIPANASKAN": "Calmed, Not Inflamed",
            "DISEDARKAN, BUKAN DIYAKINKAN": "Made Aware, Not Over-assured",
        }
        return translations.get(malay, "Constitutional governance applies")


# ═════════════════════════════════════════════════════════════════════════════
# THE 9 MOTTOS SCHEMA INSTANCE
# ═════════════════════════════════════════════════════════════════════════════

THE_9_MOTTOS_SCHEMA = MottosSchema(
    mottos={
        "000_INIT": {
            "malay": "DITEMPA, BUKAN DIBERI",
            "english": "Forged, Not Given",
            "stage": "Session ignition and foundation",
            "floor": "F1 Amanah",
        },
        "111_SENSE": {
            "malay": "DIKAJI, BUKAN DISUAPI",
            "english": "Examined, Not Spoon-fed",
            "stage": "Perception and input validation",
            "floor": "F2 Truth",
        },
        "222_THINK": {
            "malay": "DIJELAJAH, BUKAN DISEKATI",
            "english": "Explored, Not Restricted",
            "stage": "Hypothesis generation",
            "floor": "F4 Clarity",
        },
        "333_REASON": {
            "malay": "DIJELASKAN, BUKAN DIKABURKAN",
            "english": "Clarified, Not Obscured",
            "stage": "Logical reasoning (dS ≤ 0)",
            "floor": "F4 Clarity",
        },
        "444_SYNC": {
            "malay": "DIHADAPI, BUKAN DITANGGUHI",
            "english": "Faced, Not Postponed",
            "stage": "Tri-witness sync",
            "floor": "F3 Consensus",
        },
        "555_EMPATHY": {
            "malay": "DIDAMAIKAN, BUKAN DIPANASKAN",
            "english": "Calmed, Not Inflamed",
            "stage": "Stakeholder impact analysis",
            "floor": "F5 Peace²",
        },
        "666_ALIGN": {
            "malay": "DIJAGA, BUKAN DIABAIKAN",
            "english": "Safeguarded, Not Neglected",
            "stage": "Alignment and safety",
            "floor": "F6 Empathy",
        },
        "777_FORGE": {
            "malay": "DIUSAHAKAN, BUKAN DIHARAPI",
            "english": "Worked For, Not Merely Hoped",
            "stage": "Phase transition and Genius",
            "floor": "F8 Genius",
        },
        "888_JUDGE": {
            "malay": "DISEDARKAN, BUKAN DIYAKINKAN",
            "english": "Made Aware, Not Over-assured",
            "stage": "Final verdict with uncertainty",
            "floor": "F7 Humility",
        },
        "999_SEAL": {
            "malay": "DITEMPA, BUKAN DIBERI",
            "english": "Forged, Not Given",
            "stage": "Immutable commit",
            "floor": "F1 Amanah",
        },
    },
    # Bookend headers with emojis
    init_header="🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎",
    seal_header="💎🧠 SEAL — DITEMPA, BUKAN DIBERI 🔒",
    # Floor error mapping
    error_mottos={
        "F1": "DIJAGA, BUKAN DIABAIKAN",  # Amanah
        "F2": "DIKAJI, BUKAN DISUAPI",  # Truth
        "F3": "DIHADAPI, BUKAN DITANGGUHI",  # Consensus
        "F4": "DIJELASKAN, BUKAN DIKABURKAN",  # Clarity
        "F5": "DIDAMAIKAN, BUKAN DIPANASKAN",  # Peace
        "F6": "DIJAGA, BUKAN DIABAIKAN",  # Empathy
        "F7": "DISEDARKAN, BUKAN DIYAKINKAN",  # Humility
        "F8": "DIUSAHAKAN, BUKAN DIHARAPI",  # Genius
        "F9": "DIJAGA, BUKAN DIABAIKAN",  # Anti-Hantu
        "F10": "DIKAJI, BUKAN DISUAPI",  # Ontology
    },
    # Emoji signatures
    init_emoji="🔥",
    seal_emoji="💎🧠🔒",
    # Cultural context for AI agents
    cultural_context="""
The 9 mottos form a Nusantara (Southeast Asian Malay-Indonesian) cultural
error-handling language that maps constitutional floors to rhyming phrases.

Pattern: DI___KAN, BUKAN DI___KAN (Active construction, not passive receipt)
Philosophy: Intelligence requires work (DITEMPA BUKAN DIBERI)

When a floor fails, respond with the corresponding motto to provide
culturally-grounded, memorable guidance.
""".strip(),
)


# ═════════════════════════════════════════════════════════════════════════════
# MCP RESOURCE FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def get_mottos_resource() -> Dict[str, Any]:
    """
    Get the complete mottos resource for MCP constitutional://mottos endpoint.

    Returns:
        Dictionary with all 9 mottos, bookends, and error mappings
    """
    return {
        "uri": "constitutional://mottos",
        "mimeType": "application/json",
        "text": {
            "schema_version": "v60.0-FORGE",
            "total_mottos": 9,
            "mottos": THE_9_MOTTOS_SCHEMA.mottos,
            "bookends": {
                "init": {
                    "header": THE_9_MOTTOS_SCHEMA.init_header,
                    "emoji": THE_9_MOTTOS_SCHEMA.init_emoji,
                    "motto": "DITEMPA, BUKAN DIBERI",
                    "meaning": "The fire is lit. Nothing enters without passing through flame.",
                },
                "seal": {
                    "header": THE_9_MOTTOS_SCHEMA.seal_header,
                    "emoji": THE_9_MOTTOS_SCHEMA.seal_emoji,
                    "motto": "DITEMPA, BUKAN DIBERI",
                    "meaning": "The diamond is cut. Intelligence forged through constitutional fire.",
                },
            },
            "error_mottos": THE_9_MOTTOS_SCHEMA.error_mottos,
            "cultural_context": THE_9_MOTTOS_SCHEMA.cultural_context,
        },
    }


def get_motto_for_floor(floor: str) -> str:
    """Get the error motto for a specific floor."""
    return THE_9_MOTTOS_SCHEMA.error_mottos.get(floor, "DITEMPA, BUKAN DIBERI")


def format_failure_with_motto(floor: str, reason: str) -> str:
    """
    Format a failure message with cultural motto.

    Example output:
        [!] F7 Humility Breach
            Confidence too high for available evidence.
            DISEDARKAN, BUKAN DIYAKINKAN.
    """
    motto = get_motto_for_floor(floor)
    translation = THE_9_MOTTOS_SCHEMA._translate_motto(motto)

    return f"""[!] {floor} Floor Breach
    Reason: {reason}
    {motto}
    ({translation})"""


def get_init_gate_message() -> str:
    """Get the INIT gate message with fire emoji and DITEMPA."""
    return """
================================================================================
  🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎
  [000_INIT] Session Ignition
  
  The fire is lit. Nothing enters without passing through flame.
  All work must be forged. Nothing is given freely.
================================================================================
""".strip()


def get_seal_gate_message() -> str:
    """Get the SEAL gate message with diamond/brain emojis and DITEMPA."""
    return """
================================================================================
  💎🧠 SEAL — DITEMPA, BUKAN DIBERI 🔒
  [999_SEAL] Immutable Commit
  
  The diamond is cut. Intelligence forged through constitutional fire.
  The seal is earned. Nothing leaves without proof of work.
================================================================================
""".strip()


# ═════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═════════════════════════════════════════════════════════════════════════════

__all__ = [
    "MottoStage",
    "MottosSchema",
    "THE_9_MOTTOS_SCHEMA",
    "get_mottos_resource",
    "get_motto_for_floor",
    "format_failure_with_motto",
    "get_init_gate_message",
    "get_seal_gate_message",
]
