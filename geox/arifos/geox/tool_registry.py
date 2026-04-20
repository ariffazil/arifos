"""
tool_registry.py — Unified Tool Registry for GEOX
DITEMPA BUKAN DIBERI

Centralized registry for tool metadata, versioning, and constitutional requirements.
Used to harden the MCP server and provide rich discovery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolMetadata:
    """Metadata for a GEOX tool."""
    name: str
    version: str
    description: str
    required_floors: list[str] = field(default_factory=lambda: ["F4", "F7", "F11"])
    ac_risk_enabled: bool = False
    error_codes: list[str] = field(default_factory=lambda: ["UNKNOWN_ERROR", "PHYSICS_VIOLATION"])
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "required_floors": self.required_floors,
            "ac_risk_enabled": self.ac_risk_enabled,
            "error_codes": self.error_codes,
            "tags": self.tags,
        }


class UnifiedToolRegistry:
    """Registry of all hardened GEOX tools."""
    
    _registry: dict[str, ToolMetadata] = {
        "geox_load_seismic_line": ToolMetadata(
            name="geox_load_seismic_line",
            version="1.0.0",
            description="Load seismic data and generate contrast canon views.",
            required_floors=["F4", "F11"],
            ac_risk_enabled=True,
            error_codes=["FILE_NOT_FOUND", "INVALID_FORMAT", "SCALE_UNKNOWN"],
            tags=["seismic", "vision"]
        ),
        "geox_build_structural_candidates": ToolMetadata(
            name="geox_build_structural_candidates",
            version="1.0.0",
            description="Generate multi-model structural interpretations.",
            required_floors=["F7", "F11"],
            ac_risk_enabled=True,
            error_codes=["INTERPRETATION_FAILED", "INSUFFICIENT_DATA"],
            tags=["seismic", "structural"]
        ),
        "geox_compute_ac_risk": ToolMetadata(
            name="geox_compute_ac_risk",
            version="1.1.0",
            description="Calculate Anomalous Contrast Risk (ToAC).",
            required_floors=["F4", "F7", "F11", "F13"],
            ac_risk_enabled=False,
            error_codes=["INVALID_COMPONENTS", "MISSING_TRANSFORM"],
            tags=["governance", "risk"]
        ),
        "geox_feasibility_check": ToolMetadata(
            name="geox_feasibility_check",
            version="1.0.0",
            description="Verify physical feasibility of a geological plan.",
            required_floors=["F1", "F2", "F4", "F7", "F9", "F11", "F13"],
            ac_risk_enabled=True,
            error_codes=["PHYSICS_VIOLATION", "CONSTRAINT_MISMATCH"],
            tags=["governance", "physics"]
        ),
        "geox_verify_geospatial": ToolMetadata(
            name="geox_verify_geospatial",
            version="1.0.0",
            description="Verify coordinates and jurisdictional boundaries.",
            required_floors=["F4", "F11"],
            ac_risk_enabled=False,
            error_codes=["OUT_OF_BOUNDS", "PROJECTION_ERROR"],
            tags=["gis", "spatial"]
        ),
        "geox_evaluate_prospect": ToolMetadata(
            name="geox_evaluate_prospect",
            version="1.0.0",
            description="Generate governed verdict on a prospect.",
            required_floors=["F1", "F4", "F7", "F9", "F11", "F13"],
            ac_risk_enabled=True,
            error_codes=["INSUFFICIENT_GROUNDING", "VERDICT_VOID"],
            tags=["governance", "prospect"]
        ),
        "geox_query_memory": ToolMetadata(
            name="geox_query_memory",
            version="1.0.0",
            description="Retrieve past evaluations from GEOX memory.",
            required_floors=["F11"],
            ac_risk_enabled=False,
            error_codes=["QUERY_FAILED", "STORE_UNAVAILABLE"],
            tags=["memory", "retrieval"]
        ),
        "geox_query_macrostrat": ToolMetadata(
            name="geox_query_macrostrat",
            version="1.0.0",
            description="Retrieve regional stratigraphy from Macrostrat.",
            required_floors=["F2", "F7", "F11"],
            ac_risk_enabled=False,
            error_codes=["MACROSTRAT_API_ERROR", "NO_COVERAGE"],
            tags=["stratigraphy", "external"]
        ),
        "geox_calculate_saturation": ToolMetadata(
            name="geox_calculate_saturation",
            version="1.0.0",
            description="Compute Sw with uncertainty propagation.",
            required_floors=["F2", "F4", "F7", "F13"],
            ac_risk_enabled=True,
            error_codes=["SW_MODEL_ERROR", "PARAMETER_OUT_OF_RANGE"],
            tags=["petrophysics"]
        ),
    }

    @classmethod
    def get(cls, name: str) -> ToolMetadata | None:
        return cls._registry.get(name)

    @classmethod
    def list_tools(cls) -> list[ToolMetadata]:
        return list(cls._registry.values())
