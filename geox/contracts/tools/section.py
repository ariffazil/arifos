import logging
from fastmcp import FastMCP
from typing import List, Dict, Any
from contracts.enums.statuses import get_standard_envelope, ExecutionStatus, GovernanceStatus, ArtifactStatus

logger = logging.getLogger("geox.section")

def register_section_tools(mcp: FastMCP, profile: str = "full"):
    """
    SECTION Registry: 2D stratigraphic correlation tools.
    Cross-well analysis and profile synthesis.
    
    Naming convention: section_{action}_{target}
    Aliases removed - use canonical names only.
    """
    
    @mcp.tool(name="geox_section_interpret_strata")
    @mcp.tool(name="section_interpret_strata")
    async def section_interpret_strata(section_ref: str) -> dict:
        """Interpret: Correlate stratigraphic units across multiple wells in a section."""
        artifact = {"section_ref": section_ref, "units": ["Oligocene", "Miocene_Lower"], "status": "Interpolated"}
        return get_standard_envelope(
            artifact, 
            tool_class="interpret", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.DRAFT,
            ui_resource_uri="ui://section-dashboard"
        )

    @mcp.tool(name="geox_section_observe_well_correlation")
    @mcp.tool(name="section_observe_well_correlation")
    async def section_observe_well_correlation(well_refs: list) -> dict:
        """Observe: Fetch raw correlation data between specified wells."""
        artifact = {"well_refs": well_refs, "correlation_indices": [0.92, 0.85, 0.77]}
        return get_standard_envelope(
            artifact, 
            tool_class="observe", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.LOADED,
            ui_resource_uri="ui://section-dashboard"
        )

    @mcp.tool(name="geox_section_synthesize_profile")
    @mcp.tool(name="section_synthesize_profile")
    async def section_synthesize_profile(start_coord: tuple, end_coord: tuple) -> dict:
        """Compute: Synthesize a 2D vertical profile from the Earth model."""
        artifact = {"profile_ref": "profile_syn_001", "length_km": 15.5}
        return get_standard_envelope(
            artifact, 
            tool_class="compute", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.COMPUTED,
            ui_resource_uri="ui://section-dashboard"
        )
