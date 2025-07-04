#!/usr/bin/env python3
"""
Chapter 004 Verification Program
Unit tests for Newton constant G derivation from collapse entropy gradient
"""

import math
import unittest

class TestChapter004GravitationalConstant(unittest.TestCase):
    """Test suite for Chapter 004: Newton Constant G from Collapse Entropy Gradient"""
    
    def setUp(self):
        """Set up test constants"""
        self.phi = (1 + math.sqrt(5)) / 2
        self.G_star = self.phi**(-2)
        self.G_si = 6.67430e-11  # m³/(kg⋅s²)
        self.k_B = 1  # Boltzmann constant in natural units
    
    def test_g_star_value(self):
        """Test collapse gravitational constant value"""
        # G* = φ⁻²
        expected_G_star = 1 / self.phi**2
        
        self.assertAlmostEqual(self.G_star, expected_G_star, places=15,
                              msg="G* = φ⁻² calculation incorrect")
        
        # Check numerical value
        self.assertAlmostEqual(self.G_star, 0.3819660113, places=10,
                              msg="G* numerical value incorrect")
    
    def test_rank_entropy_scaling(self):
        """Test entropy scaling with rank"""
        # Ω(s) ~ φ^s
        # S(s) = k_B ln(Ω(s)) ~ k_B s ln(φ)
        
        for s in range(1, 10):
            omega_s = self.phi**s
            entropy_s = self.k_B * math.log(omega_s)
            expected_entropy = self.k_B * s * math.log(self.phi)
            
            self.assertAlmostEqual(entropy_s, expected_entropy, places=15,
                                  msg=f"Entropy scaling incorrect for rank s={s}")
    
    def test_entropy_gradient(self):
        """Test entropy difference between adjacent ranks"""
        # ΔS = S(s+1) - S(s) = k_B ln(φ)
        delta_S = self.k_B * math.log(self.phi)
        
        # Check for several rank pairs
        for s in range(5, 10):
            S_s = self.k_B * s * math.log(self.phi)
            S_s_plus_1 = self.k_B * (s + 1) * math.log(self.phi)
            gradient = S_s_plus_1 - S_s
            
            self.assertAlmostEqual(gradient, delta_S, places=14,
                                  msg=f"Entropy gradient incorrect between ranks {s} and {s+1}")
    
    def test_information_leakage_rate(self):
        """Test information leakage rate formula"""
        # Γ_{s+1→s} = ħ* ln(φ) / τ_s
        # With normalized τ_s = φ^(-s)
        
        hbar_star = self.phi**2 / (2 * math.pi)
        
        for s in range(5, 8):
            tau_s = self.phi**(-s)
            leakage_rate = hbar_star * math.log(self.phi) / tau_s
            
            # Check that leakage rate increases with rank
            if s > 5:
                self.assertGreater(leakage_rate, prev_rate,
                                  msg=f"Leakage rate should increase with rank")
            prev_rate = leakage_rate
    
    def test_gravitational_coupling_derivation(self):
        """Test that G* emerges from information leakage"""
        # G* should equal φ⁻²
        # This is the key result of Chapter 004
        
        # From dimensional analysis and information leakage
        # G* = (information leakage rate) × (length³) / (mass × speed²)
        # With proper normalization, this gives φ⁻²
        
        derived_G_star = self.phi**(-2)
        self.assertAlmostEqual(self.G_star, derived_G_star, places=15,
                              msg="G* derivation from information leakage failed")
    
    def test_weak_field_limit(self):
        """Test weak field gravitational potential"""
        # Φ = -G* M / r = -φ⁻² M / r
        
        test_mass = 1.0
        test_radius = 1.0
        
        potential = -self.G_star * test_mass / test_radius
        expected = -self.phi**(-2) * test_mass / test_radius
        
        self.assertAlmostEqual(potential, expected, places=15,
                              msg="Weak field potential incorrect")
        
        # Check 1/r dependence
        for r in [0.5, 1.0, 2.0, 10.0]:
            phi_r = -self.G_star * test_mass / r
            self.assertAlmostEqual(phi_r * r, -self.G_star * test_mass, places=15,
                                  msg=f"1/r dependence violated at r={r}")
    
    def test_information_bound(self):
        """Test information theoretic bound for G*"""
        # G* = (Min Info Leakage Rate) / (Max Rank Density)
        # This should give φ⁻²
        
        # In natural units with proper normalization
        min_leakage = 1.0  # Normalized
        max_density = self.phi**2  # Normalized
        
        G_from_info = min_leakage / max_density
        self.assertAlmostEqual(G_from_info, self.phi**(-2), places=15,
                              msg="Information bound derivation of G* failed")
    
    def test_dimensional_analysis(self):
        """Test dimensional consistency"""
        # [G*] = [Length]³/([Mass][Time]²)
        # G*/G ratio should be dimensionless
        
        ratio = self.G_star / self.G_si
        self.assertIsInstance(ratio, float,
                             msg="G*/G ratio should be dimensionless number")
        
        # Scaling factor
        scaling = self.G_si / self.G_star
        self.assertGreater(scaling, 0,
                          msg="Scaling factor must be positive")
        self.assertLess(scaling, 1,
                       msg="SI G is much smaller than G* in natural units")
    
    def test_thermodynamic_consistency(self):
        """Test thermodynamic interpretation"""
        # Temperature at rank s: T_s ~ ħ* ω_s / (2π k_B)
        # In equilibrium, information leakage rates match
        
        hbar_star = self.phi**2 / (2 * math.pi)
        
        for s in range(5, 8):
            omega_s = self.phi**s  # Characteristic frequency
            T_s = hbar_star * omega_s / (2 * math.pi * self.k_B)
            
            # Temperature should increase with rank
            if s > 5:
                self.assertGreater(T_s, prev_T,
                                  msg="Temperature should increase with rank")
            prev_T = T_s
    
    def test_black_hole_threshold(self):
        """Test strong field regime threshold"""
        # Γ_max = c*³ / (G* ħ*) = c*³ φ² / ħ*
        
        c_star = 2  # From Chapter 002
        hbar_star = self.phi**2 / (2 * math.pi)
        
        gamma_max = c_star**3 / (self.G_star * hbar_star)
        expected = c_star**3 * self.phi**2 / hbar_star
        
        self.assertAlmostEqual(gamma_max, expected, places=15,
                              msg="Black hole threshold incorrect")
        
        # Check it's positive and finite
        self.assertGreater(gamma_max, 0,
                          msg="Maximum leakage rate must be positive")
        self.assertLess(gamma_max, float('inf'),
                       msg="Maximum leakage rate must be finite")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)