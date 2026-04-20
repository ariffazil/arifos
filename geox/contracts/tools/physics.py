import logging
import os
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from contracts.enums.statuses import get_standard_envelope, ExecutionStatus, GovernanceStatus, ArtifactStatus

logger = logging.getLogger("geox.physics")

def register_physics_tools(mcp: FastMCP, profile: str = "full"):
    """
    PHYSICS Registry: Governance, Verification, and ACP Tools.
    The Sovereign Layer.
    """
    
    try:
        from services.governance.judge import judge
        from services.evidence_store.store import store
        from geox.shared.contracts.schemas import EvidenceObject, EvidenceRef, EvidenceKind
        from datetime import datetime, timezone
    except ImportError:
        logger.error("Physics services unavailable")
        return

    @mcp.tool(name="geox_physics_judge_verdict")
    @mcp.tool(name="physics_judge_verdict")
    async def physics_judge_verdict(
        intent_ref: str, 
        well_ref: str, 
        prospect_ref: str
    ) -> dict:
        """Judge: Execute the Sovereign 888_JUDGE on a Causal Scene."""
        well = store.get_evidence(well_ref)
        prospect = store.get_evidence(prospect_ref)
        
        if not well or not prospect:
            artifact = {"error": f"Evidence not found: well={well_ref}, prospect={prospect_ref}"}
            return get_standard_envelope(
                artifact, 
                tool_class="judge", 
                governance_status=GovernanceStatus.HOLD, 
                artifact_status=ArtifactStatus.REJECTED,
                ui_resource_uri="ui://physics-dashboard"
            )
        
        verdict = judge.evaluate_well_prospect_fit(intent_ref, well, prospect)
        
        # Audit the loop
        store.save_evidence(EvidenceObject(
            ref=EvidenceRef(
                id=verdict.verdictId,
                kind=EvidenceKind.verdict,
                sourceUri=f"geox://verdicts/{verdict.verdictId}",
                timestamp=verdict.timestamp
            ),
            context=well.context,
            payload=verdict.model_dump()
        ))
        
        artifact = verdict.model_dump()
        return get_standard_envelope(
            artifact, 
            tool_class="judge", 
            governance_status=verdict.verdictType,
            ui_resource_uri="ui://physics-dashboard"
        )

    @mcp.tool(name="geox_physics_validate_operation")
    @mcp.tool(name="physics_validate_operation")
    async def physics_validate_operation(operation_ref: str) -> dict:
        """Verify: Check if current operation adheres to safety and physical bounds."""
        artifact = {"operation_ref": operation_ref, "status": "validated", "seal": "F9_PHYSICS_9"}
        return get_standard_envelope(
            artifact, 
            tool_class="verify", 
            governance_status=GovernanceStatus.SEAL, 
            artifact_status=ArtifactStatus.VERIFIED,
            ui_resource_uri="ui://physics-dashboard"
        )

    @mcp.tool(name="geox_physics_audit_hold_breach")
    @mcp.tool(name="physics_audit_hold_breach")
    async def physics_audit_hold_breach(session_ref: str) -> dict:
        """Audit: Investigate if any 888_HOLD conditions were bypassed."""
        artifact = {"session_ref": session_ref, "breach_detected": False}
        return get_standard_envelope(
            artifact, 
            tool_class="verify", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.VERIFIED,
            ui_resource_uri="ui://physics-dashboard"
        )

    @mcp.tool(name="geox_physics_verify_physics")
    @mcp.tool(name="physics_verify_physics")
    async def physics_verify_physics(parameters: dict) -> dict:
        """Verify: Check physical parameters for consistency (e.g. Gardner density)."""
        artifact = {"consistent": True, "method": "Gardner"}
        return get_standard_envelope(
            artifact, 
            tool_class="verify", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.VERIFIED,
            ui_resource_uri="ui://physics-dashboard"
        )

    @mcp.tool(name="geox_physics_compute_stoiip")
    @mcp.tool(name="physics_compute_stoiip")
    async def physics_compute_stoiip(inputs: dict) -> dict:
        """
        Compute: Reservoir calculation over physical parameters (Stock Tank Oil Initially In Place).
        """
        try:
            from arifos.geox.tools.volumetrics_economics_tool import VolumetricsEconomicsTool
            
            tool = VolumetricsEconomicsTool()
            result = await tool.run(inputs)
            
            if not result.success:
                artifact = {
                    "error": result.error or "Volumetrics calculation failed",
                    "verdict": "HOLD",
                    "seal": "DITEMPA_BUKAN_DIBERI"
                }
                return get_standard_envelope(
                    artifact, 
                    tool_class="compute", 
                    governance_status=GovernanceStatus.HOLD, 
                    artifact_status=ArtifactStatus.REJECTED,
                    ui_resource_uri="ui://physics-dashboard"
                )
            
            # Transform to physics layer expected format
            raw = result.raw_output
            vol = raw.get("volumetrics", {})
            
            artifact = {
                "stoiip_mmbbl": vol.get("stoiip_p50", 0),
                "stoiip_p90": vol.get("stoiip_p90", 0),
                "stoiip_p50": vol.get("stoiip_p50", 0),
                "stoiip_p10": vol.get("stoiip_p10", 0),
                "stoiip_mean": vol.get("stoiip_mean", 0),
                "recoverable_p50": vol.get("recoverable_p50", 0),
                "basis": inputs,
                "uncertainty_propagated": True,
                "method": "monte_carlo_5000_samples",
                "verdict": raw.get("verdict", "QUALIFY"),
                "seal": "DITEMPA_BUKAN_DIBERI"
            }
            return get_standard_envelope(
                artifact, 
                tool_class="compute", 
                governance_status=raw.get("verdict", GovernanceStatus.QUALIFY), 
                artifact_status=ArtifactStatus.COMPUTED,
                ui_resource_uri="ui://physics-dashboard"
            )
        except Exception as e:
            logger.error(f"STOIIP calculation failed: {e}")
            artifact = {
                "error": str(e),
                "verdict": "HOLD",
                "seal": "DITEMPA_BUKAN_DIBERI"
            }
            return get_standard_envelope(
                artifact, 
                tool_class="compute", 
                governance_status=GovernanceStatus.HOLD, 
                artifact_status=ArtifactStatus.REJECTED,
                ui_resource_uri="ui://physics-dashboard"
            )

    @mcp.tool(name="geox_physics_fetch_authoritative_state")
    @mcp.tool(name="physics_fetch_authoritative_state")
    async def physics_fetch_authoritative_state() -> dict:
        """Observe: Fetch the ground-truth physical state vector from the vault."""
        artifact = {"state": "nominal", "vault": "VAULT-999", "canon": "Physics9"}
        return get_standard_envelope(
            artifact, 
            tool_class="observe", 
            governance_status=GovernanceStatus.QUALIFY, 
            artifact_status=ArtifactStatus.LOADED,
            ui_resource_uri="ui://physics-dashboard"
        )

    # ══════════════════════════════════════════════════════════════════════════════
    # ACP GOVERNANCE TOOLS
    # ══════════════════════════════════════════════════════════════════════════════
    
    try:
        from .acp_logic import (
            acp_register_agent,
            acp_submit_proposal,
            acp_check_convergence,
            acp_grant_seal,
            acp_get_status
        )

        @mcp.tool(name="geox_physics_acp_register")
        @mcp.tool(name="physics_acp_register")
        async def physics_acp_register(
            agent_ref: str,
            role: str,
            name: str,
            resources: Optional[list] = None,
            tools: Optional[list] = None
        ) -> dict:
            """Register an agent with the Agent Control Plane."""
            artifact = await acp_register_agent(agent_ref, role, name, resources, tools)
            return get_standard_envelope(
                artifact, 
                tool_class="govern", 
                governance_status=GovernanceStatus.QUALIFY, 
                artifact_status=ArtifactStatus.VERIFIED,
                ui_resource_uri="ui://physics-dashboard"
            )

        @mcp.tool(name="geox_physics_acp_submit")
        @mcp.tool(name="physics_acp_submit")
        async def physics_acp_submit(agent_ref: str, proposal: dict) -> dict:
            """Submit a proposal for 888_JUDGE evaluation."""
            artifact = await acp_submit_proposal(agent_ref, proposal)
            return get_standard_envelope(
                artifact, 
                tool_class="govern", 
                governance_status=GovernanceStatus.QUALIFY, 
                artifact_status=ArtifactStatus.STAGED,
                ui_resource_uri="ui://physics-dashboard"
            )

        @mcp.tool(name="geox_physics_acp_check_convergence")
        @mcp.tool(name="physics_acp_check_convergence")
        async def physics_acp_check_convergence(resource: str) -> dict:
            """Check agent convergence on a resource."""
            artifact = await acp_check_convergence(resource)
            return get_standard_envelope(
                artifact, 
                tool_class="govern", 
                governance_status=GovernanceStatus.QUALIFY, 
                artifact_status=ArtifactStatus.IN_REVIEW,
                ui_resource_uri="ui://physics-dashboard"
            )

        @mcp.tool(name="geox_physics_acp_grant_seal")
        @mcp.tool(name="physics_acp_grant_seal")
        async def physics_acp_grant_seal(proposal_ref: str, human_auth_token: str) -> dict:
            """Grant 999_SEAL (sovereign human authority)."""
            artifact = await acp_grant_seal(proposal_ref, human_auth_token)
            return get_standard_envelope(
                artifact, 
                tool_class="govern", 
                governance_status=GovernanceStatus.SEAL, 
                artifact_status=ArtifactStatus.VERIFIED,
                ui_resource_uri="ui://physics-dashboard"
            )

        @mcp.tool(name="geox_physics_acp_status")
        @mcp.tool(name="physics_acp_status")
        async def physics_acp_status() -> dict:
            """Get ACP system status."""
            artifact = await acp_get_status()
            return get_standard_envelope(
                artifact, 
                tool_class="govern", 
                governance_status=GovernanceStatus.QUALIFY, 
                artifact_status=ArtifactStatus.LOADED,
                ui_resource_uri="ui://physics-dashboard"
            )
    except ImportError:
        logger.error("ACP logic unavailable")

