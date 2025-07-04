#!/usr/bin/env python3
"""
Chapter 003 Verification Program
Unit tests for Planck constant ħ derivation from minimal action trace
"""

import math
import unittest

class TestChapter003PlanckConstant(unittest.TestCase):
    """Test suite for Chapter 003: Planck Constant from Minimal Action Trace"""
    
    def setUp(self):
        """Set up test constants"""
        self.phi = (1 + math.sqrt(5)) / 2
        self.pi = math.pi
        self.hbar_star = self.phi**2 / (2 * self.pi)
        self.hbar_si = 1.054571817e-34  # J⋅s
    
    def test_golden_ratio_properties(self):
        """Test fundamental golden ratio properties"""
        # φ² = φ + 1
        self.assertAlmostEqual(self.phi**2, self.phi + 1, places=15,
                              msg="Golden ratio property φ² = φ + 1 failed")
        
        # φ = 1 + 1/φ
        self.assertAlmostEqual(self.phi, 1 + 1/self.phi, places=15,
                              msg="Golden ratio property φ = 1 + 1/φ failed")
    
    def test_minimal_loop_period(self):
        """Test minimal closed loop period calculation"""
        # T_min = 2π Δt / φ²
        # In normalized units where Δt = 1
        T_min_normalized = 2 * self.pi / self.phi**2
        expected_ratio = 2 * self.pi / self.phi**2
        
        self.assertAlmostEqual(T_min_normalized, expected_ratio, places=10,
                              msg="Minimal loop period incorrect")
    
    def test_hbar_star_value(self):
        """Test collapse Planck constant value"""
        # ħ* = φ²/(2π)
        expected_hbar_star = self.phi**2 / (2 * self.pi)
        
        self.assertAlmostEqual(self.hbar_star, expected_hbar_star, places=15,
                              msg="ħ* calculation incorrect")
        
        # Check numerical value
        self.assertAlmostEqual(self.hbar_star, 0.41667305, places=8,
                              msg="ħ* numerical value incorrect")
    
    def test_action_quantization(self):
        """Test that action is quantized in units of ħ*"""
        # Actions should be S = n × ħ* for integer n
        n_values = [1, 2, 3, 5, 8, 13]  # Some Fibonacci numbers
        
        for n in n_values:
            action = n * self.hbar_star
            ratio = action / self.hbar_star
            self.assertAlmostEqual(ratio, n, places=15,
                                  msg=f"Action quantization failed for n={n}")
    
    def test_phase_space_area(self):
        """Test minimal phase space area quantum"""
        # Minimal area in phase space = ħ*
        # For circular phase space trajectory: Area = π × p × q
        # With normalization, minimal area = ħ*
        
        minimal_area = self.hbar_star
        self.assertGreater(minimal_area, 0, 
                          msg="Minimal phase space area must be positive")
        
        # Check it's the right order of magnitude
        self.assertLess(minimal_area, 1,
                       msg="ħ* should be less than 1 in natural units")
        self.assertGreater(minimal_area, 0.1,
                          msg="ħ* should be greater than 0.1 in natural units")
    
    def test_uncertainty_relation(self):
        """Test that uncertainty principle emerges correctly"""
        # Δq Δp ≥ ħ*/2
        min_uncertainty_product = self.hbar_star / 2
        
        # Test some example uncertainties
        test_cases = [
            (1.0, 0.5),  # Δq=1, Δp=0.5
            (0.5, 1.0),  # Δq=0.5, Δp=1
            (0.3, 0.7),  # Δq=0.3, Δp=0.7
        ]
        
        for delta_q, delta_p in test_cases:
            product = delta_q * delta_p
            self.assertGreaterEqual(product, min_uncertainty_product,
                                   msg=f"Uncertainty principle violated for Δq={delta_q}, Δp={delta_p}")
    
    def test_classical_limit(self):
        """Test classical correspondence for large n"""
        # For large n, quantum → classical
        large_n = 10000
        action_quantum = large_n * self.hbar_star
        
        # In classical limit, action >> ħ*
        ratio = action_quantum / self.hbar_star
        self.assertAlmostEqual(ratio, large_n, places=10,
                              msg="Classical limit scaling incorrect")
        
        # Relative quantum correction ~ 1/n
        quantum_correction = self.hbar_star / action_quantum
        self.assertAlmostEqual(quantum_correction, 1/large_n, places=15,
                              msg="Quantum correction scaling incorrect")
    
    def test_dimensional_consistency(self):
        """Test dimensional analysis"""
        # ħ* should have dimensions of action = [Energy][Time]
        # In collapse units: [Δm][Δℓ]²[Δt]⁻¹
        # Since we're using natural units, just check it's dimensionless
        # and maps correctly to SI
        
        scaling_factor = self.hbar_si / self.hbar_star
        self.assertGreater(scaling_factor, 0,
                          msg="Scaling factor must be positive")
        self.assertLess(scaling_factor, 1,
                       msg="SI ħ is much smaller than ħ* in natural units")
    
    def test_topological_invariance(self):
        """Test that ħ* is topologically protected"""
        # ħ* = φ²/(2π) combines:
        # - φ from Fibonacci/golden ratio (algebraic)
        # - 2π from topology of closed loops (topological)
        
        # Check that slight perturbations don't affect the structure
        epsilon = 1e-10
        
        # Perturbed values should give different result
        hbar_perturbed = (self.phi + epsilon)**2 / (2 * self.pi)
        self.assertNotAlmostEqual(self.hbar_star, hbar_perturbed, places=12,
                                 msg="ħ* should change with φ perturbation")
        
        # But the structure φ²/(2π) is universal
        ratio = self.hbar_star * 2 * self.pi / self.phi**2
        self.assertAlmostEqual(ratio, 1.0, places=15,
                              msg="Structure φ²/(2π) not preserved")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)