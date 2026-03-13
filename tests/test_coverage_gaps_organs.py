"""
Test coverage gaps for constitutional organs.
Target: Bring core/organs/ files to 75%+
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestOrganInit:
    """Tests for core/organs/_0_init.py (currently 68%)"""
    
    @pytest.mark.asyncio
    async def test_init_organ_execution(self):
        """Test INIT organ execution"""
        from core.organs._0_init import INIT_ORGAN
        
        payload = {
            "raw_input": "test input",
            "declared_name": "test_user"
        }
        
        with patch('core.organs._0_init.verify_identity') as mock_verify:
            mock_verify.return_value = {"verified": True, "actor_id": "test_actor"}
            
            result = await INIT_ORGAN.execute(payload)
            assert result is not None
    
    def test_init_organ_metadata(self):
        """Test INIT organ metadata"""
        from core.organs._0_init import INIT_ORGAN
        
        assert INIT_ORGAN.stage == "000_INIT"
        assert INIT_ORGAN.trinity == "INIT"
    
    @pytest.mark.asyncio
    async def test_session_initialization(self):
        """Test session initialization"""
        from core.organs._0_init import initialize_session
        
        with patch('core.organs._0_init.SessionManager') as mock_mgr:
            mock_instance = Mock()
            mock_instance.create_session = AsyncMock()
            mock_instance.create_session.return_value = "test-session-id"
            mock_mgr.return_value = mock_instance
            
            session_id = await initialize_session({"actor_id": "test"})
            assert session_id is not None


class TestOrganAGI:
    """Tests for core/organs/_1_agi.py"""
    
    @pytest.mark.asyncio
    async def test_agi_reason_execution(self):
        """Test AGI REASON organ execution"""
        from core.organs._1_agi import AGI_REASON
        
        payload = {"query": "test reasoning query"}
        
        with patch('core.organs._1_agi.perform_reasoning') as mock_reason:
            mock_reason.return_value = AsyncMock()
            mock_reason.return_value = {
                "conclusion": "test conclusion",
                "confidence": 0.95
            }
            
            result = await AGI_REASON.execute(payload)
            assert result is not None
    
    def test_agi_organ_stages(self):
        """Test AGI organ has correct stages"""
        from core.organs._1_agi import AGI_REASON, AGI_REFLECT
        
        assert AGI_REASON.stage == "333_MIND"
        assert AGI_REFLECT.stage == "555_REFLECT"


class TestOrganASI:
    """Tests for core/organs/_2_asi.py (currently 71%)"""
    
    @pytest.mark.asyncio
    async def test_asi_critique_execution(self):
        """Test ASI CRITIQUE organ execution"""
        from core.organs._2_asi import ASI_CRITIQUE
        
        payload = {"draft_output": "test draft"}
        
        with patch('core.organs._2_asi.perform_critique') as mock_critique:
            mock_critique.return_value = AsyncMock()
            mock_critique.return_value = {
                "safe": True,
                "concerns": []
            }
            
            result = await ASI_CRITIQUE.execute(payload)
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_asi_simulate_execution(self):
        """Test ASI SIMULATE organ execution"""
        from core.organs._2_asi import ASI_SIMULATE
        
        payload = {"scenario": "test scenario"}
        
        with patch('core.organs._2_asi.perform_simulation') as mock_sim:
            mock_sim.return_value = AsyncMock()
            mock_sim.return_value = {
                "outcomes": [{"probability": 0.8}]
            }
            
            result = await ASI_SIMULATE.execute(payload)
            assert result is not None


class TestOrganAPEX:
    """Tests for core/organs/_3_apex.py"""
    
    @pytest.mark.asyncio
    async def test_apex_judge_execution(self):
        """Test APEX JUDGE organ execution"""
        from core.organs._3_apex import APEX_JUDGE
        
        payload = {"candidate_output": "test output"}
        
        with patch('core.organs._3_apex.perform_judgment') as mock_judge:
            mock_judge.return_value = AsyncMock()
            mock_judge.return_value = {
                "verdict": "SEAL",
                "confidence": 0.95
            }
            
            result = await APEX_JUDGE.execute(payload)
            assert result is not None
            assert result.get("verdict") == "SEAL"


class TestOrganVault:
    """Tests for core/organs/_4_vault.py"""
    
    @pytest.mark.asyncio
    async def test_vault_seal_execution(self):
        """Test VAULT SEAL organ execution"""
        from core.organs._4_vault import VAULT_SEAL
        
        payload = {
            "verdict": "SEAL",
            "evidence": "test evidence"
        }
        
        with patch('core.organs._4_vault.seal_to_ledger') as mock_seal:
            mock_seal.return_value = AsyncMock()
            mock_seal.return_value = {
                "hash": "abc123",
                "timestamp": "2026-03-14T10:00:00Z"
            }
            
            result = await VAULT_SEAL.execute(payload)
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_vault_verify_execution(self):
        """Test VAULT VERIFY organ execution"""
        from core.organs._4_vault import VAULT_VERIFY
        
        payload = {"entry_hash": "abc123"}
        
        with patch('core.organs._4_vault.verify_ledger_entry') as mock_verify:
            mock_verify.return_value = AsyncMock()
            mock_verify.return_value = {"valid": True}
            
            result = await VAULT_VERIFY.execute(payload)
            assert result is not None


class TestGovernanceKernel:
    """Tests for core/governance_kernel.py (currently 77%)"""
    
    def test_kernel_initialization(self):
        """Test governance kernel initialization"""
        from core.governance_kernel import GovernanceKernel
        
        kernel = GovernanceKernel()
        assert kernel is not None
    
    def test_route_pipeline(self):
        """Test pipeline routing"""
        from core.governance_kernel import route_pipeline
        
        query = "test query"
        plan = route_pipeline(query)
        
        assert isinstance(plan, list)
        assert len(plan) > 0
    
    @pytest.mark.asyncio
    async def test_execute_stage(self):
        """Test stage execution"""
        from core.governance_kernel import execute_stage
        
        with patch('core.governance_kernel.get_organ') as mock_get:
            mock_organ = Mock()
            mock_organ.execute = AsyncMock()
            mock_organ.execute.return_value = {"status": "success"}
            mock_get.return_value = mock_organ
            
            result = await execute_stage("000_INIT", {})
            assert result is not None


class TestPipeline:
    """Tests for core/pipeline.py (currently 50%)"""
    
    def test_pipeline_creation(self):
        """Test pipeline creation"""
        from core.pipeline import MetabolicPipeline
        
        pipeline = MetabolicPipeline()
        assert pipeline is not None
    
    @pytest.mark.asyncio
    async def test_pipeline_execute(self):
        """Test pipeline execution"""
        from core.pipeline import MetabolicPipeline
        
        pipeline = MetabolicPipeline()
        
        with patch.object(pipeline, '_execute_stage') as mock_exec:
            mock_exec.return_value = AsyncMock()
            mock_exec.return_value = {"verdict": "SEAL"}
            
            result = await pipeline.execute(["000_INIT"], {})
            assert result is not None


class TestJudgment:
    """Tests for core/judgment.py (currently 86%)"""
    
    def test_render_verdict_seal(self):
        """Test rendering SEAL verdict"""
        from core.judgment import render_verdict
        
        result = render_verdict(
            floors_passed=13,
            metrics={"G_star": 0.85}
        )
        
        assert result.verdict == "SEAL"
    
    def test_render_verdict_void(self):
        """Test rendering VOID verdict"""
        from core.judgment import render_verdict
        
        result = render_verdict(
            floors_passed=10,
            violations=["F2"],
            metrics={"G_star": 0.70}
        )
        
        assert result.verdict == "VOID"


class TestHomeostasis:
    """Tests for core/governance/homeostasis.py"""
    
    def test_homeostasis_check(self):
        """Test homeostasis check"""
        from core.governance.homeostasis import check_homeostasis
        
        metrics = {
            "G_star": 0.80,
            "delta_S": -0.1,
            "peace_squared": 1.1
        }
        
        result = check_homeostasis(metrics)
        assert isinstance(result, dict)
        assert "stable" in result


class TestTelemetry:
    """Tests for core/governance/telemetry.py"""
    
    def test_telemetry_collection(self):
        """Test telemetry collection"""
        from core.governance.telemetry import collect_telemetry
        
        telemetry = collect_telemetry()
        assert isinstance(telemetry, dict)
    
    def test_telemetry_reporting(self):
        """Test telemetry reporting"""
        from core.governance.telemetry import report_telemetry
        
        data = {"test": "data"}
        
        with patch('core.governance.telemetry.send_to_dashboard') as mock_send:
            mock_send.return_value = True
            
            result = report_telemetry(data)
            assert result is True


class TestRiskEngine:
    """Tests for core/governance/risk_engine.py"""
    
    def test_risk_calculation_low(self):
        """Test low risk calculation"""
        from core.governance.risk_engine import calculate_risk
        
        risk = calculate_risk(
            operation="read",
            scope="public"
        )
        
        assert isinstance(risk, float)
        assert 0 <= risk <= 1
    
    def test_risk_calculation_high(self):
        """Test high risk calculation"""
        from core.governance.risk_engine import calculate_risk
        
        risk = calculate_risk(
            operation="delete",
            scope="production",
            irreversible=True
        )
        
        assert risk > 0.5  # Should be high risk


class TestUncertaintyEngine:
    """Tests for core/governance/uncertainty_engine.py"""
    
    def test_uncertainty_calculation(self):
        """Test uncertainty calculation"""
        from core.governance.uncertainty_engine import calculate_uncertainty
        
        uncertainty = calculate_uncertainty(
            evidence_quality=0.7,
            source_reliability=0.8
        )
        
        assert isinstance(uncertainty, float)
        assert 0.03 <= uncertainty <= 0.20  # F7 band
    
    def test_uncertainty_band_check(self):
        """Test uncertainty band compliance"""
        from core.governance.uncertainty_engine import check_uncertainty_band
        
        # In band
        result = check_uncertainty_band(0.04)
        assert result.in_band is True
        
        # Out of band (too high)
        result = check_uncertainty_band(0.50)
        assert result.in_band is False


class TestFloorAudit:
    """Tests for core/shared/floor_audit.py (currently 74%)"""
    
    def test_audit_floors(self):
        """Test floor auditing"""
        from core.shared.floor_audit import audit_floors
        
        context = {"query": "test", "evidence": []}
        results = audit_floors(context)
        
        assert isinstance(results, list)
        assert len(results) == 13  # All F1-F13
    
    def test_floor_f2_truth_check(self):
        """Test F2 truth floor check"""
        from core.shared.floor_audit import check_f2_truth
        
        # Grounded evidence
        result = check_f2_truth({"evidence": [{"source": "reliable.com"}]})
        assert result.passed is True
        
        # No evidence
        result = check_f2_truth({"evidence": []})
        assert result.passed is False


class TestConsensusArbitrator:
    """Tests for core/scheduler/consensus_arbitrator.py"""
    
    def test_tri_witness_consensus(self):
        """Test Tri-Witness consensus calculation"""
        from core.scheduler.consensus_arbitrator import calculate_tri_witness
        
        consensus = calculate_tri_witness(
            human_score=1.0,
            ai_score=0.97,
            earth_score=0.91
        )
        
        assert isinstance(consensus, float)
        assert consensus >= 0.95  # Should meet F3 threshold
    
    def test_consensus_below_threshold(self):
        """Test consensus below threshold"""
        from core.scheduler.consensus_arbitrator import calculate_tri_witness
        
        consensus = calculate_tri_witness(
            human_score=0.5,
            ai_score=0.6,
            earth_score=0.4
        )
        
        assert consensus < 0.95  # Should fail F3


class TestGeniusCalculation:
    """Tests for core/enforcement/genius.py"""
    
    def test_genius_score_calculation(self):
        """Test G★ calculation"""
        from core.enforcement.genius import calculate_genius_score
        
        G = calculate_genius_score(
            A=0.9,  # Accuracy
            P=0.95,  # Peace
            X=0.85,  # Exploration
            E=0.88,  # Efficiency
            h=0.05   # Hysteresis
        )
        
        assert isinstance(G, float)
        assert G >= 0.80  # Should meet F8 threshold
    
    def test_genius_below_threshold(self):
        """Test G★ below threshold"""
        from core.enforcement.genius import calculate_genius_score
        
        G = calculate_genius_score(
            A=0.5, P=0.5, X=0.5, E=0.5, h=0.5
        )
        
        assert G < 0.80  # Should fail F8
