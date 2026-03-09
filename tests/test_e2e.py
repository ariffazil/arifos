import pytest
from arifosmcp.runtime.tools import metabolic_loop_router, seal_vault_commit

@pytest.mark.asyncio
async def test_full_arifos_metabolic_loop():
    """E2E test validating the 000-999 flow (Init -> Mind -> Heart -> Judge -> Seal)."""
    query = "Evaluate the constitutional impact of autonomous resource allocation."
    
    # 1. Execute the full Metabolic Loop Router (Orchestrator)
    envelope = await metabolic_loop_router(
        query=query,
        risk_tier="high",
        actor_id="sovereign_test",
        allow_execution=False
    )
    
    # 2. Validate Transport Layer Envelope
    assert envelope.verdict in ["SEAL", "SABAR", "VOID", "HOLD"], f"Unexpected verdict: {envelope.verdict}"
    assert envelope.session_id is not None
    assert getattr(envelope, "stage", None) is not None or "stage" in envelope.data
    
    # 3. If SEAL, attempt final vault seal (999)
    if envelope.verdict == "SEAL":
        seal_res = await seal_vault_commit(
            session_id=envelope.session_id,
            auth_context=envelope.auth_context,
            verdict="SEAL"
        )
        assert seal_res.verdict in ["SEAL", "VOID", "SABAR"]
