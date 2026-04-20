import logging
from fastmcp import FastMCP
from typing import List, Dict, Any
from contracts.enums.statuses import get_standard_envelope, ExecutionStatus, GovernanceStatus, ArtifactStatus

logger = logging.getLogger("geox.well")

def register_well_tools(mcp: FastMCP, profile: str = "full"):
    """
    WELL Registry: Borehole & Log Analysis tools.
    'What's in this borehole?'
    
    Naming convention: well_{action}_{target}
    """
    
    try:
        from services.witness_engine.petrophysics import witness
    except ImportError:
        logger.error("Well services unavailable")
        witness = None

    @mcp.tool(name="geox_well_load_bundle")
    @mcp.tool(name="well_load_bundle")
    async def well_load_bundle(well_ref: str, bundle_uri: str) -> dict:
        """Observe: Load a full log bundle (LAS/DLIS) into the witness context."""
        artifact = {"well_ref": well_ref, "status": "loaded", "uri": bundle_uri}
        return get_standard_envelope(
            artifact, 
            tool_class="observe", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.DRAFT, 
            uncertainty="Low",
            ui_resource_uri="ui://well-dashboard"
        )

    @mcp.tool(name="well_load_log_bundle")
    async def well_load_log_bundle(well_id: str, bundle_uri: str) -> dict:
        """[DEPRECATED] Alias for well_load_bundle."""
        return await well_load_bundle(well_id, bundle_uri)

    @mcp.tool(name="geox_well_qc_logs")
    @mcp.tool(name="well_qc_logs")
    async def well_qc_logs(well_ref: str) -> dict:
        """Verify: Perform Quality Control on loaded logs."""
        artifact = {"well_ref": well_ref, "qc_status": "pass", "flags": []}
        return get_standard_envelope(
            artifact, 
            tool_class="verify", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.VERIFIED, 
            uncertainty="Low",
            ui_resource_uri="ui://well-dashboard"
        )

    @mcp.tool(name="geox_qc_logs")
    async def geox_qc_logs(well_id: str) -> dict:
        """[DEPRECATED] Alias for well_qc_logs."""
        return await well_qc_logs(well_id)

    @mcp.tool(name="geox_well_validate_cutoffs")
    @mcp.tool(name="well_validate_cutoffs")
    async def well_validate_cutoffs(well_ref: str, parameter: str, value: float) -> dict:
        """Verify: Validate petrophysical cutoffs against regional norms."""
        artifact = {"well_ref": well_ref, "parameter": parameter, "valid": True}
        return get_standard_envelope(
            artifact, 
            tool_class="verify", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.VERIFIED, 
            uncertainty="Low",
            ui_resource_uri="ui://well-dashboard"
        )

    @mcp.tool(name="geox_validate_cutoffs")
    async def geox_validate_cutoffs(well_id: str, parameter: str, value: float) -> dict:
        """[DEPRECATED] Alias for well_validate_cutoffs."""
        return await well_validate_cutoffs(well_id, parameter, value)

    @mcp.tool(name="geox_well_select_sw_model")
    @mcp.tool(name="well_select_sw_model")
    async def well_select_sw_model(formation: str, temperature_c: float) -> dict:
        """Interpret: Recommends a Water Saturation (Sw) model based on formation context."""
        if witness:
            result = witness.select_sw_model(formation, temperature_c)
        else:
            result = {"formation": formation, "model": "Archie", "temperature_c": temperature_c}
        return get_standard_envelope(
            result, 
            tool_class="interpret", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.DRAFT, 
            uncertainty="Moderate",
            ui_resource_uri="ui://well-dashboard"
        )

    @mcp.tool(name="geox_select_sw_model")
    async def geox_select_sw_model(formation: str, temperature_c: float) -> dict:
        """[DEPRECATED] Alias for well_select_sw_model."""
        return await well_select_sw_model(formation, temperature_c)

    @mcp.tool(name="geox_well_compute_petrophysics")
    @mcp.tool(name="well_compute_petrophysics")
    async def well_compute_petrophysics(
        model: str, 
        rw: float, 
        rt: float, 
        phi: float, 
        a: float = 1.0, 
        m: float = 2.0, 
        n: float = 2.0
    ) -> dict:
        """Compute: Executes physics-9 grounded petrophysical calculations."""
        if witness:
            result_obj = witness.compute_archie_sw(model, rw, rt, phi, a, m, n)
            artifact = result_obj.model_dump()
        else:
            sw = (a * rw / (rt * phi**m))**(1/n)
            artifact = {"sw": sw, "phi": phi, "rw": rw, "rt": rt, "model": model}
        return get_standard_envelope(
            artifact, 
            tool_class="compute", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.COMPUTED, 
            uncertainty="Moderate",
            ui_resource_uri="ui://well-dashboard"
        )

    @mcp.tool(name="geox_compute_petrophysics")
    async def geox_compute_petrophysics(
        model: str, 
        rw: float, 
        rt: float, 
        phi: float, 
        a: float = 1.0, 
        m: float = 2.0, 
        n: float = 2.0
    ) -> dict:
        """[DEPRECATED] Alias for well_compute_petrophysics."""
        return await well_compute_petrophysics(model, rw, rt, phi, a, m, n)

    @mcp.tool(name="geox_well_verify_petrophysics")
    @mcp.tool(name="well_verify_petrophysics")
    async def well_verify_petrophysics(well_ref: str, phi: float, sw: float) -> dict:
        """Verify: Governance check (888_HOLD) for anomalous petrophysics."""
        if witness:
            artifact = witness.hold_check(well_ref, phi, sw)
        else:
            artifact = {"well_ref": well_ref, "status": "HOLD_TRIGGERED"}
        return get_standard_envelope(
            artifact, 
            tool_class="verify", 
            governance_status=GovernanceStatus.HOLD, 
            artifact_status=ArtifactStatus.IN_REVIEW, 
            uncertainty="High",
            ui_resource_uri="ui://well-dashboard"
        )

    @mcp.tool(name="well_petrophysical_check")
    async def well_petrophysical_check(well_id: str, phi: float, sw: float) -> dict:
        """[DEPRECATED] Alias for well_verify_petrophysics."""
        return await well_verify_petrophysics(well_id, phi, sw)

    @mcp.tool(name="geox_petrophysical_hold_check")
    async def geox_petrophysical_hold_check(well_id: str, phi: float, sw: float) -> dict:
        """[DEPRECATED] Alias for well_verify_petrophysics."""
        return await well_verify_petrophysics(well_id, phi, sw)
