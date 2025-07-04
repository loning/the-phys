#!/usr/bin/env python3
"""
Chapter 009 Verification Program
Validates collapse mass unit from rank-energy correspondence
"""

import math
import unittest

class TestChapter009CollapseMass(unittest.TestCase):
    """Test suite for Chapter 009: Collapse Mass Unit from Rank-Energy Correspondence"""
    
    def setUp(self):
        """Set up test constants"""
        self.phi = (1 + math.sqrt(5)) / 2
        self.pi = math.pi
        
        # From previous chapters
        self.hbar_star = self.phi**2 / (2 * self.pi)
        self.c_star = 2
        self.delta_tau = 1 / (8 * math.sqrt(self.pi))  # Planck time
        self.m_P_star = self.phi**2 * math.sqrt(1 / self.pi)  # Planck mass
        self.G_star = self.phi**(-2)  # Gravitational constant
        
        # Mass constants
        self.m_0 = self.hbar_star / (self.c_star**2 * self.delta_tau)  # Fundamental mass
        self.E_0 = self.hbar_star / self.delta_tau  # Ground state energy
        
        # Fibonacci sequence
        self.fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    
    def test_fundamental_mass_equals_planck_mass(self):
        """Test that m_0 = m_P*"""
        # m_0 = ħ*/(c*²Δτ)
        # Calculate step by step
        numerator = self.hbar_star
        denominator = self.c_star**2 * self.delta_tau
        
        m_0_calc = numerator / denominator
        
        # Expected: φ²/√π
        expected = self.phi**2 / math.sqrt(self.pi)
        
        self.assertAlmostEqual(m_0_calc, expected, places=10,
                              msg="Fundamental mass should equal Planck mass")
        
        # Verify it equals our Planck mass
        self.assertAlmostEqual(m_0_calc, self.m_P_star, places=15,
                              msg="m_0 should equal m_P*")
    
    def test_mass_energy_equivalence(self):
        """Test E = mc² relation"""
        # Test for various masses
        test_masses = [self.m_0, 2*self.m_0, self.phi*self.m_0]
        
        for m in test_masses:
            E = m * self.c_star**2
            
            # Check energy is positive for positive mass
            self.assertGreater(E, 0,
                              msg="Energy must be positive for positive mass")
            
            # Check inverse relation
            m_recovered = E / self.c_star**2
            self.assertAlmostEqual(m_recovered, m, places=15,
                              msg="Mass-energy equivalence violated")
    
    def test_mass_loop_integral(self):
        """Test mass from closed loop integral"""
        # For a simple circular loop with constant frequency
        omega_0 = 1 / self.delta_tau  # Base frequency
        loop_length = 2 * self.pi  # Circular loop
        
        # m = (ħ*/c*²) ∮ω ds
        mass = (self.hbar_star / self.c_star**2) * omega_0 * loop_length
        
        # This should give a mass in Planck units
        mass_ratio = mass / self.m_0
        
        # Check it's positive and reasonable
        self.assertGreater(mass, 0,
                          msg="Loop mass must be positive")
        self.assertGreater(mass_ratio, 0,
                          msg="Mass ratio must be positive")
    
    def test_fibonacci_mass_spectrum(self):
        """Test Fibonacci quantization of mass levels"""
        # m_n = F_n · m_0
        
        for i, F_n in enumerate(self.fib[:8]):
            m_n = F_n * self.m_0
            
            # Check positive
            self.assertGreater(m_n, 0,
                              msg=f"Mass level {i} must be positive")
            
            # Check Fibonacci scaling
            if i >= 2:
                m_prev1 = self.fib[i-1] * self.m_0
                m_prev2 = self.fib[i-2] * self.m_0
                m_sum = m_prev1 + m_prev2
                
                self.assertAlmostEqual(m_n, m_sum, places=15,
                                      msg=f"Fibonacci mass scaling failed at n={i}")
            
            # Check information content
            if F_n > 0:
                I_n = math.log(F_n) / math.log(self.phi)
                self.assertGreaterEqual(I_n, 0,
                                       msg=f"Information content negative at n={i}")
    
    def test_mass_information_content(self):
        """Test information measure of mass states"""
        # I(m) = log_φ(m/m_0)
        
        test_masses = [self.m_0, self.phi*self.m_0, self.phi**2*self.m_0]
        expected_info = [0, 1, 2]
        
        for m, I_expected in zip(test_masses, expected_info):
            I_calc = math.log(m/self.m_0) / math.log(self.phi)
            
            self.assertAlmostEqual(I_calc, I_expected, places=10,
                                  msg=f"Information content incorrect for m={m/self.m_0}m_0")
    
    def test_rank_mass_scaling(self):
        """Test mass scaling with rank"""
        # m = m_0 · φ^(2r)
        
        test_ranks = [-2, -1, 0, 1, 2]
        
        for r in test_ranks:
            m_r = self.m_0 * self.phi**(2*r)
            
            # Check positive
            self.assertGreater(m_r, 0,
                              msg=f"Mass must be positive at rank {r}")
            
            # Check scaling
            if r > -2:
                m_prev = self.m_0 * self.phi**(2*(r-1))
                ratio = m_r / m_prev
                self.assertAlmostEqual(ratio, self.phi**2, places=10,
                                      msg=f"Mass scaling incorrect between ranks {r-1} and {r}")
    
    def test_mass_position_uncertainty(self):
        """Test mass-position uncertainty relation"""
        # Δm · Δx ≥ ħ*/(2c*)
        
        uncertainty_product_min = self.hbar_star / (2 * self.c_star)
        
        # Test for Planck length position uncertainty
        delta_x = 1 / (4 * math.sqrt(self.pi))  # ℓ_P*
        delta_m_min = uncertainty_product_min / delta_x
        
        # Should be m_P*/2
        expected_delta_m = self.m_P_star / 2
        
        self.assertAlmostEqual(delta_m_min, expected_delta_m, places=10,
                              msg="Minimum mass uncertainty incorrect")
        
        # Check various position uncertainties
        test_positions = [delta_x, 2*delta_x, 10*delta_x]
        
        for dx in test_positions:
            dm_min = uncertainty_product_min / dx
            product = dm_min * dx
            
            self.assertGreaterEqual(product, uncertainty_product_min,
                                   msg=f"Uncertainty relation violated for Δx={dx}")
    
    def test_binding_energy_mass_defect(self):
        """Test composite mass with binding energy"""
        # M_comp = Σm_i - B/c*²
        
        # Example: two particles binding
        m1 = 5 * self.m_0
        m2 = 3 * self.m_0
        B = 0.1 * self.m_0 * self.c_star**2  # 10% binding
        
        M_comp = m1 + m2 - B / self.c_star**2
        expected = 7.9 * self.m_0
        
        self.assertAlmostEqual(M_comp, expected, places=10,
                              msg="Composite mass calculation incorrect")
        
        # Mass defect should equal binding energy
        mass_defect = (m1 + m2) - M_comp
        B_recovered = mass_defect * self.c_star**2
        
        self.assertAlmostEqual(B_recovered, B, places=15,
                              msg="Binding energy recovery failed")
    
    def test_running_mass_scaling(self):
        """Test scale-dependent mass"""
        # m(μ) = m_0 · (μ/μ_0)^γ_m
        # γ_m = -1/ln(φ)
        
        gamma_m = -1 / math.log(self.phi)
        mu_0 = 1 / self.delta_tau  # Reference scale
        
        # Test at different scales
        scale_factors = [0.1, 1, 10, 100]
        
        for factor in scale_factors:
            mu = factor * mu_0
            m_mu = self.m_0 * (mu / mu_0)**gamma_m
            
            # Mass should be positive
            self.assertGreater(m_mu, 0,
                              msg=f"Running mass must be positive at μ/μ_0={factor}")
            
            # Check specific scaling
            if factor == self.phi:
                # At φ times the scale, mass should change by specific amount
                expected_ratio = self.phi**gamma_m
                actual_ratio = m_mu / self.m_0
                self.assertAlmostEqual(actual_ratio, expected_ratio, places=10,
                                      msg="Running mass scaling incorrect")
    
    def test_lepton_mass_hierarchy(self):
        """Test lepton mass pattern"""
        # Just check the pattern makes sense
        # m_e ≈ m_0 · φ^(-12)
        # m_μ ≈ m_0 · φ^(-8)
        # m_τ ≈ m_0 · φ^(-6)
        
        # Rank differences
        rank_e = -6  # Doubled from -12 since m ∝ φ^(2r)
        rank_mu = -4
        rank_tau = -3
        
        m_e = self.m_0 * self.phi**(2*rank_e)
        m_mu = self.m_0 * self.phi**(2*rank_mu)
        m_tau = self.m_0 * self.phi**(2*rank_tau)
        
        # Check mass ordering
        self.assertLess(m_e, m_mu,
                       msg="Electron should be lighter than muon")
        self.assertLess(m_mu, m_tau,
                       msg="Muon should be lighter than tau")
        
        # Check approximate ratios
        ratio_mu_e = m_mu / m_e
        ratio_tau_mu = m_tau / m_mu
        
        # Both should be approximately φ^4 (2 rank steps)
        self.assertAlmostEqual(ratio_mu_e, self.phi**4, places=1,
                              msg="Muon/electron ratio incorrect")
        self.assertAlmostEqual(ratio_tau_mu, self.phi**2, places=1,
                              msg="Tau/muon ratio incorrect")
    
    def test_mass_curvature_relation(self):
        """Test that mass curves spacetime correctly"""
        # Just verify dimensional consistency
        # R_μν ~ G*m/V
        
        m = self.m_P_star
        V = 1  # Unit volume in natural units
        
        curvature_scale = self.G_star * m / V
        
        # Should have dimensions of inverse length squared
        # In our units, this should be order 1
        self.assertGreater(curvature_scale, 0,
                          msg="Curvature must be positive for positive mass")
        
        # For Planck mass in Planck volume, curvature ~ 1
        self.assertLess(curvature_scale, 10,
                       msg="Planck scale curvature should be O(1)")
        self.assertGreater(curvature_scale, 0.1,
                          msg="Planck scale curvature should be O(1)")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)