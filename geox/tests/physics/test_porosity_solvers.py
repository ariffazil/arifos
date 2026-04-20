"""
Tests for porosity solvers.
Verify against textbook cases.
"""

import pytest
from arifos.geox.physics.porosity_solvers import (
    VshSolver,
    DensityNeutronSolver,
    compute_bvw,
    compute_permeability_proxy,
)


class TestVshSolver:
    """Test Vsh calculations from Gamma Ray."""
    
    def test_linear_clean_sand(self):
        """Clean sand: GR near clean baseline → Vsh ~ 0."""
        solver = VshSolver(gr_clean=30, gr_shale=120)
        result = solver.compute_linear(gr=35)  # Near clean
        
        assert result.vsh == pytest.approx(0.056, abs=0.01)
        assert result.vsh_uncertainty > 0
    
    def test_linear_shale(self):
        """Shale: GR at shale baseline → Vsh ~ 1."""
        solver = VshSolver(gr_clean=30, gr_shale=120)
        result = solver.compute_linear(gr=120)
        
        assert result.vsh == pytest.approx(1.0, abs=0.01)
    
    def test_linear_mid_range(self):
        """Mid-range: GR halfway → Vsh ~ 0.5."""
        solver = VshSolver(gr_clean=30, gr_shale=120)
        result = solver.compute_linear(gr=75)  # Halfway
        
        assert result.vsh == pytest.approx(0.5, abs=0.02)
    
    def test_clavier_fertl_lower_than_linear(self):
        """
        Clavier-Fertl should give lower Vsh than linear at low values.
        This is the key difference - linear overestimates Vsh.
        """
        solver = VshSolver(gr_clean=30, gr_shale=120)
        
        # Low GR reading (slightly above clean)
        gr = 45
        
        linear = solver.compute_linear(gr)
        cf = solver.compute_clavier_fertl(gr)
        
        # Clavier-Fertl should be lower than linear
        assert cf.vsh < linear.vsh
        
        # Both in valid range
        assert 0 <= cf.vsh <= 1
        assert 0 <= linear.vsh <= 1
    
    def test_vsh_bounds(self):
        """Vsh should always be in [0, 1]."""
        solver = VshSolver(gr_clean=30, gr_shale=120)
        
        # Very low GR
        result = solver.compute_linear(gr=10)
        assert result.vsh == 0.0
        
        # Very high GR
        result = solver.compute_linear(gr=200)
        assert result.vsh == 1.0
    
    def test_invalid_endpoints(self):
        """Should raise error if gr_shale <= gr_clean."""
        with pytest.raises(ValueError):
            VshSolver(gr_clean=120, gr_shale=30)


class TestDensityNeutronSolver:
    """Test porosity calculations."""
    
    def test_density_porosity_typical_sand(self):
        """
        Typical sandstone case.
        - Rhob = 2.35 g/cm³
        - Matrix = 2.65 (quartz)
        - Fluid = 1.0 (water)
        - Expected phi ~ 18%
        """
        solver = DensityNeutronSolver(
            rho_matrix=2.65,
            rho_fluid=1.0
        )
        result = solver.compute_phi(rhob=2.35)
        
        # phi = (2.65 - 2.35) / (2.65 - 1.0) = 0.30 / 1.65 = 0.182
        assert result.phi == pytest.approx(0.182, abs=0.01)
        assert result.method == "density_only"
    
    def test_density_porosity_zero(self):
        """Matrix density → phi = 0."""
        solver = DensityNeutronSolver(rho_matrix=2.65, rho_fluid=1.0)
        result = solver.compute_phi(rhob=2.65)
        
        assert result.phi == pytest.approx(0.0, abs=0.01)
    
    def test_density_porosity_high(self):
        """Fluid density → phi = 1 (theoretical)."""
        solver = DensityNeutronSolver(rho_matrix=2.65, rho_fluid=1.0)
        result = solver.compute_phi(rhob=1.0)
        
        assert result.phi == pytest.approx(1.0, abs=0.01)
    
    def test_density_neutron_average(self):
        """
        Normal case: density and neutron average.
        - Rhob = 2.35 (phi_d ~ 18%)
        - Nphi = 20% (0.20)
        - Expected phi ~ 19%
        """
        solver = DensityNeutronSolver(rho_matrix=2.65, rho_fluid=1.0)
        result = solver.compute_phi(rhob=2.35, nphi=0.20)
        
        # Average of ~18% and 20%
        assert result.phi == pytest.approx(0.19, abs=0.02)
        assert result.method == "density_neutron_average"
    
    def test_gas_crossover_detected(self):
        """
        Gas crossover: neutron reads low, density reads high.
        This should be detected and flagged.
        """
        solver = DensityNeutronSolver(rho_matrix=2.65, rho_fluid=1.0)
        
        # Gas case: low Rhob (high phi_d), very low Nphi
        result = solver.compute_phi(rhob=2.20, nphi=0.05)
        
        # Should detect crossover
        assert "crossover" in str(result.environmental_corrections).lower()
        # Should prefer density in gas
        assert result.phi > 0.20  # Density phi dominates
    
    def test_uncertainty_present(self):
        """All results should have uncertainty > 0."""
        solver = DensityNeutronSolver()
        result = solver.compute_phi(rhob=2.35, nphi=0.20)
        
        assert result.phi_uncertainty > 0
        assert result.phi_uncertainty < 0.1  # Reasonable bound
    
    def test_effective_porosity(self):
        """Test total to effective porosity conversion."""
        solver = DensityNeutronSolver()
        
        phi_total = 0.25
        vsh = 0.30
        phi_shale = 0.30
        
        result = solver.compute_effective_porosity(
            phi_total=phi_total,
            vsh=vsh,
            phi_shale=phi_shale
        )
        
        # phi_e = 0.25 - 0.30 * 0.30 = 0.25 - 0.09 = 0.16
        expected = phi_total - vsh * phi_shale
        assert result.phi == pytest.approx(expected, abs=0.01)
        assert result.method == "effective_from_total"


class TestBVW:
    """Test Bulk Volume Water calculations."""
    
    def test_bvw_basic(self):
        """BVW = phi * Sw."""
        bvw, unc = compute_bvw(phi=0.20, sw=0.30)
        
        assert bvw == pytest.approx(0.06, abs=0.001)
        assert unc >= 0
    
    def test_bvw_fully_saturated(self):
        """100% water: BVW = phi."""
        bvw, unc = compute_bvw(phi=0.20, sw=1.0)
        
        assert bvw == pytest.approx(0.20, abs=0.001)
    
    def test_bwv_uncertainty_propagation(self):
        """Uncertainty should increase with input uncertainty."""
        bvw1, unc1 = compute_bvw(phi=0.20, sw=0.30, phi_uncertainty=0.02, sw_uncertainty=0.05)
        bvw2, unc2 = compute_bvw(phi=0.20, sw=0.30, phi_uncertainty=0.04, sw_uncertainty=0.10)
        
        # Higher input uncertainty → higher output uncertainty
        assert unc2 > unc1


class TestPermeabilityProxy:
    """Test permeability estimation."""
    
    def test_permeability_increases_with_phi(self):
        """Higher porosity → higher permeability."""
        k1, _ = compute_permeability_proxy(phi=0.10)
        k2, _ = compute_permeability_proxy(phi=0.25)
        
        assert k2 > k1
    
    def test_permeability_order_of_magnitude(self):
        """
        Typical values:
        - 10% porosity → ~1 mD (tight)
        - 25% porosity → ~100 mD (good)
        """
        k_10, _ = compute_permeability_proxy(phi=0.10)
        k_25, _ = compute_permeability_proxy(phi=0.25)
        
        # Order of magnitude checks
        assert 0.1 < k_10 < 10  # Around 1 mD
        assert 10 < k_25 < 1000  # Around 100 mD
    
    def test_timur_coates_with_sw(self):
        """Timur-Coates uses Sw."""
        k, desc = compute_permeability_proxy(
            phi=0.20,
            sw=0.30,  # Low Sw = hydrocarbon
            method="timur_coates"
        )
        
        assert k > 0
        assert "timur" in desc.lower()
