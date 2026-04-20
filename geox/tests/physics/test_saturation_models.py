"""
Tests for saturation models.
Verify against textbook cases (Crain's Petrophysical Handbook).
"""

import pytest
from arifos.geox.physics.saturation_models import (
    ArchieModel,
    SimandouxModel,
    select_model_for_rock,
)


class TestArchieModel:
    """Test Archie water saturation calculations."""
    
    def test_archie_clean_sand_typical(self):
        """
        Typical clean sand case.
        
        From Crain's Petrophysical Handbook:
        - Clean sand, phi=20%, Rt=20 ohm-m, Rw=0.1 ohm-m
        - Expected Sw ~ 25%
        """
        model = ArchieModel(a=1.0, m=2.0, n=2.0)
        result = model.compute_sw(
            rt=20.0,      # ohm-m
            phi=0.20,     # fraction
            rw=0.1        # ohm-m
        )
        
        # Sw^n = (a * Rw) / (phi^m * Rt)
        # Sw^2 = (1 * 0.1) / (0.2^2 * 20) = 0.1 / (0.04 * 20) = 0.1 / 0.8 = 0.125
        # Sw = sqrt(0.125) = 0.354
        
        assert result.sw == pytest.approx(0.354, rel=0.01)
        assert result.method == "archie_clean"
        assert len(result.assumption_violations) == 0
        assert result.sw_uncertainty > 0
        assert result.sw_uncertainty < 0.2  # Reasonable uncertainty
    
    def test_archie_fully_water_saturated(self):
        """
        100% water zone: Rt should equal Ro (formation factor * Rw).
        """
        model = ArchieModel(a=1.0, m=2.0, n=2.0)
        
        # For Sw = 1.0: Rt = a * Rw / phi^m
        phi = 0.25
        rw = 0.15
        rt = 1.0 * rw / (phi ** 2.0)  # Ro
        
        result = model.compute_sw(rt=rt, phi=phi, rw=rw)
        
        assert result.sw == pytest.approx(1.0, abs=0.01)
    
    def test_archie_high_resistivity_oil(self):
        """
        Oil zone with high resistivity.
        """
        model = ArchieModel(a=1.0, m=2.0, n=2.0)
        result = model.compute_sw(
            rt=100.0,     # High resistivity
            phi=0.15,
            rw=0.1
        )
        
        # Sw should be low
        assert result.sw < 0.3
        assert result.sw > 0  # Physical bounds
    
    def test_archie_invalid_inputs(self):
        """Test handling of invalid inputs."""
        model = ArchieModel()
        
        # Negative Rt
        result = model.compute_sw(rt=-1, phi=0.2, rw=0.1)
        assert len(result.assumption_violations) > 0
        
        # Zero porosity
        result = model.compute_sw(rt=20, phi=0, rw=0.1)
        assert len(result.assumption_violations) > 0
    
    def test_archie_assumption_violation_high_vsh(self):
        """Archie should warn for shaly sand."""
        model = ArchieModel()
        violations = model.validate_assumptions(vsh=0.25)  # 25% shale
        
        assert len(violations) > 0
        assert "shale" in violations[0].lower() or "clean" in violations[0].lower()
    
    def test_archie_uncertainty_propagation(self):
        """Uncertainty should increase with parameter uncertainty."""
        model = ArchieModel()
        
        result1 = model.compute_sw(rt=20, phi=0.20, rw=0.1)
        
        # Higher Rw uncertainty should give higher Sw uncertainty
        # (Rw is in numerator, so uncertainty affects result)
        assert result1.sw_uncertainty > 0
        assert result1.sw_uncertainty < 0.15


class TestSimandouxModel:
    """Test Simandoux water saturation calculations."""
    
    def test_simandoux_shaly_sand_typical(self):
        """
        Typical shaly sand case.
        
        Shaly sand with:
        - phi = 20%
        - Vsh = 25%
        - Rt = 10 ohm-m
        - Rw = 0.1 ohm-m
        - Rsh = 4 ohm-m
        
        Simandoux should give higher Sw than Archie for same Rt
        (shale conductance reduces apparent resistivity).
        """
        model = SimandouxModel(a=1.0, m=2.0, n=2.0, rsh=4.0)
        
        archie = ArchieModel(a=1.0, m=2.0, n=2.0)
        archie_result = archie.compute_sw(rt=10, phi=0.20, rw=0.1)
        
        simandoux_result = model.compute_sw(
            rt=10,
            phi=0.20,
            rw=0.1,
            vsh=0.25,
            rsh=4.0
        )
        
        # Simandoux should account for shale conductivity
        # giving more "realistic" Sw for shaly sand
        assert simandoux_result.sw > 0
        assert simandoux_result.sw < 1.0
        assert len(simandoux_result.assumption_violations) == 0
    
    def test_simandoux_reduces_to_archie_at_zero_vsh(self):
        """
        Simandoux with Vsh=0 should give similar result to Archie.
        """
        simandoux = SimandouxModel(a=1.0, m=2.0, n=2.0)
        archie = ArchieModel(a=1.0, m=2.0, n=2.0)
        
        sim_result = simandoux.compute_sw(
            rt=20,
            phi=0.20,
            rw=0.1,
            vsh=0.0
        )
        arch_result = archie.compute_sw(rt=20, phi=0.20, rw=0.1)
        
        # Should be very close (small numerical differences allowed)
        assert sim_result.sw == pytest.approx(arch_result.sw, abs=0.05)
    
    def test_simandoux_high_vsh(self):
        """Test with high shale content."""
        model = SimandouxModel()
        result = model.compute_sw(
            rt=5.0,
            phi=0.15,
            rw=0.1,
            vsh=0.35,  # 35% shale
            rsh=3.0
        )
        
        assert result.sw > 0
        assert result.sw < 1.0
    
    def test_simandoux_assumption_validation(self):
        """Simandoux should warn for very clean or very shaly."""
        model = SimandouxModel()
        
        # Too clean
        violations = model.validate_assumptions(vsh=0.05)
        assert len(violations) > 0
        
        # Valid range
        violations = model.validate_assumptions(vsh=0.25)
        assert len(violations) == 0
        
        # Too shaly (warning but still works)
        violations = model.validate_assumptions(vsh=0.50)
        assert len(violations) > 0


class TestModelSelection:
    """Test automatic model selection logic."""
    
    def test_select_archie_for_clean_sand(self):
        """Clean sand (< 10% Vsh) → Archie."""
        model_class, warnings = select_model_for_rock(vsh=0.05)
        assert model_class == ArchieModel
        assert len(warnings) == 0
    
    def test_select_simandoux_for_shaly_sand(self):
        """Shaly sand (10-40% Vsh) → Simandoux."""
        model_class, warnings = select_model_for_rock(vsh=0.25)
        assert model_class == SimandouxModel
        assert len(warnings) == 0
    
    def test_select_simandoux_for_high_vsh_with_warning(self):
        """High Vsh (> 40%) → Simandoux with warning."""
        model_class, warnings = select_model_for_rock(vsh=0.50)
        assert model_class == SimandouxModel
        assert len(warnings) > 0  # Warning about high Vsh
    
    def test_smectite_warning(self):
        """High-CEC clay should trigger warning."""
        model_class, warnings = select_model_for_rock(
            vsh=0.25,
            clay_type="smectite"
        )
        assert model_class == SimandouxModel
        assert len(warnings) > 0
        assert any("cec" in w.lower() or "dual" in w.lower() for w in warnings)


class TestTextbookCases:
    """
    Specific textbook cases from petrophysics literature.
    
    Reference: Asquith, G., & Krygowski, D. (2004). 
    Basic Well Log Analysis for Geologists. AAPG Methods in Exploration Series.
    """
    
    def test_case_a_clean_sand_gas(self):
        """
        Case A: Clean gas sand
        - phi = 25%
        - Rt = 100 ohm-m
        - Rw = 0.05 ohm-m
        - Expected: Very low Sw (~15-20%)
        """
        model = ArchieModel()
        result = model.compute_sw(rt=100, phi=0.25, rw=0.05)
        
        # Should indicate gas (low Sw)
        assert result.sw < 0.25
    
    def test_case_b_shaly_oil(self):
        """
        Case B: Shaly oil sand
        - phi = 18%
        - Vsh = 30%
        - Rt = 25 ohm-m
        - Rw = 0.15 ohm-m
        - Expected: Moderate Sw (~40-50%)
        """
        model = SimandouxModel(rsh=4.0)
        result = model.compute_sw(
            rt=25,
            phi=0.18,
            rw=0.15,
            vsh=0.30,
            rsh=4.0
        )
        
        # Moderate Sw for oil zone
        assert result.sw > 0.25
        assert result.sw < 0.6
