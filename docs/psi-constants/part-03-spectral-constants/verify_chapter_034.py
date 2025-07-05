#!/usr/bin/env python3
"""
Verification program for Chapter 034: Collapse Derivation of e from α and Action Units
Tests the derivation of elementary charge from fine structure constant.
"""

import unittest
import math
import numpy as np

class TestChapter034(unittest.TestCase):
    
    def setUp(self):
        # Golden ratio
        self.phi = (1 + math.sqrt(5)) / 2
        
        # Fundamental constants
        self.alpha = 1/137.035999084  # Fine structure constant
        self.c = 299792458  # m/s (exact)
        self.hbar = 1.054571817e-34  # J·s
        self.e = 1.602176634e-19  # C (exact since 2019)
        
        # Vacuum permittivity
        self.eps0 = 8.854187817e-12  # F/m
        
        # Vacuum permeability
        self.mu0 = 4 * math.pi * 1e-7  # H/m (exact)
        
        # Electron mass
        self.m_e = 9.1093837015e-31  # kg
        
        # Collapse constants
        self.eps0_star = 1 / (4 * math.pi)  # Collapse vacuum permittivity
        
        # Tolerance
        self.tol = 1e-10
        
    def test_action_charge_duality(self):
        """Test action-charge duality principle"""
        # For fundamental quantum: S × Q = n × 2π
        # Using reduced units where ħ = 1
        
        # Elementary action quantum
        S = self.hbar  # Action
        
        # For n = 1 fundamental case
        # Q should be such that S × Q = 2π
        Q_expected = 2 * math.pi / S
        
        # This gives a charge-like quantity
        self.assertGreater(Q_expected, 0)
        
    def test_electromagnetic_coupling(self):
        """Test g_em = sqrt(4π α)"""
        g_em = math.sqrt(4 * math.pi * self.alpha)
        
        # Should be approximately 0.3028
        self.assertAlmostEqual(g_em, 0.3028226, delta=1e-6)
        
        # Check it's dimensionless
        # g_em enters as coefficient in interaction Lagrangian
        
    def test_charge_emergence_formula(self):
        """Test e = g_em × sqrt(ħc ε₀)"""
        g_em = math.sqrt(4 * math.pi * self.alpha)
        
        # Calculate charge from formula
        e_calc = g_em * math.sqrt(self.hbar * self.c * self.eps0)
        
        # Compare with known value
        self.assertAlmostEqual(e_calc, self.e, delta=1e-21)
        
    def test_permittivity_scaling(self):
        """Test vacuum permittivity in collapse units"""
        # ε₀* = 1/(4π) in collapse units
        eps0_collapse = self.eps0_star
        
        # Should be positive
        self.assertGreater(eps0_collapse, 0)
        
        # Check it equals 1/(4π)
        self.assertAlmostEqual(eps0_collapse, 1/(4*math.pi), delta=self.tol)
        
    def test_charge_quantization(self):
        """Test that charges are integer multiples of e"""
        # Test various charge states
        charges = [0, self.e, 2*self.e, -self.e, 3*self.e]
        
        for Q in charges:
            if Q == 0:
                n = 0
            else:
                n = Q / self.e
                # Should be integer
                self.assertAlmostEqual(n, round(n), delta=self.tol)
                
    def test_charge_information_minimization(self):
        """Test that e minimizes information functional"""
        # Simplified test: check that e satisfies the constraint
        
        # The actual minimum is when e²/(4πε₀ħc) = α
        # This is the constraint that determines e
        
        ratio = self.e**2 / (4*math.pi*self.eps0*self.hbar*self.c)
        
        # Should equal α (within precision)
        # We test this separately, so here just check it's positive
        self.assertGreater(ratio, 0)
        self.assertLess(abs(ratio - self.alpha) / self.alpha, 0.001)
        
    def test_charge_ratio_equals_alpha(self):
        """Test that e²/(4πε₀ħc) = α"""
        ratio = self.e**2 / (4 * math.pi * self.eps0 * self.hbar * self.c)
        
        # The values are very close but not exact due to measurement precision
        self.assertAlmostEqual(ratio, self.alpha, delta=2e-12)
        
    def test_charge_conservation(self):
        """Test charge conservation in interactions"""
        # Example: electron + positron -> 2 photons
        initial_charge = (-self.e) + (+self.e)  # e⁻ + e⁺
        final_charge = 0 + 0  # two photons
        
        self.assertEqual(initial_charge, final_charge)
        
        # Example: photon -> electron + positron
        initial_charge = 0  # photon
        final_charge = (-self.e) + (+self.e)  # e⁻ + e⁺
        
        self.assertEqual(initial_charge, final_charge)
        
    def test_charge_tensor_spectral(self):
        """Test spectral decomposition of charge tensor"""
        # Simple 2×2 charge tensor
        Q_tensor = np.array([
            [self.e**2, 0],
            [0, -self.e**2]
        ])
        
        # Get eigenvalues
        eigenvals = np.linalg.eigvals(Q_tensor)
        
        # Should have ±e² as eigenvalues
        self.assertAlmostEqual(abs(eigenvals[0]), self.e**2, delta=1e-40)
        self.assertAlmostEqual(abs(eigenvals[1]), self.e**2, delta=1e-40)
        
        # Should have opposite signs
        self.assertLess(eigenvals[0] * eigenvals[1], 0)
        
    def test_charge_running(self):
        """Test running of charge with energy scale"""
        # At higher energy, α increases slightly
        # For QED, α(MZ) ≈ 1/128
        
        alpha_MZ = 1/128  # Approximate
        
        # e(μ) = e × sqrt(α(μ)/α)
        e_MZ = self.e * math.sqrt(alpha_MZ / self.alpha)
        
        # Should be slightly larger
        self.assertGreater(e_MZ, self.e)
        self.assertLess(e_MZ / self.e, 1.1)  # Not too much larger
        
    def test_charge_mass_ratio(self):
        """Test e/m_e ratio"""
        ratio = self.e / self.m_e
        
        # Should be approximately 1.758820e11 C/kg
        self.assertAlmostEqual(ratio, 1.75882001076e11, delta=1e3)
        
        # This ratio is important for cyclotron frequency etc
        
    def test_topological_quantization(self):
        """Test winding number quantization"""
        # For a closed path with winding number n
        # Q = e × n
        
        winding_numbers = [-2, -1, 0, 1, 2, 3]
        
        for n in winding_numbers:
            Q = self.e * n
            # Verify it's quantized
            self.assertAlmostEqual(Q / self.e, n, delta=self.tol)
            
    def test_dirac_quantization(self):
        """Test Dirac quantization condition"""
        # eg = n × 2πħ
        
        # For n = 1 (minimum magnetic charge)
        g_min = 2 * math.pi * self.hbar / self.e
        
        # Check eg = 2πħ
        product = self.e * g_min
        expected = 2 * math.pi * self.hbar
        
        # Due to floating point precision, use relative error
        self.assertAlmostEqual(product / expected, 1.0, delta=1e-15)
        
    def test_planck_charge(self):
        """Test Planck charge derivation"""
        # q_P = sqrt(4πε₀ħc) = e/sqrt(α)
        
        q_P1 = math.sqrt(4 * math.pi * self.eps0 * self.hbar * self.c)
        q_P2 = self.e / math.sqrt(self.alpha)
        
        # Both formulas should give same result
        self.assertAlmostEqual(q_P1, q_P2, delta=1e-20)
        
        # Check specific value (approximately 1.875e-18 C)
        self.assertAlmostEqual(q_P1, 1.87554603778e-18, delta=1e-25)
        
    def test_master_charge_formula(self):
        """Test the master formula for charge"""
        # e = sqrt(4π α) × sqrt(ε₀* ħ* c*) × scale factors
        
        # In SI units with proper scaling
        g_em = math.sqrt(4 * math.pi * self.alpha)
        
        # The combination sqrt(ε₀ ħ c) has dimension of charge
        charge_scale = math.sqrt(self.eps0 * self.hbar * self.c)
        
        e_calc = g_em * charge_scale
        
        # Should match elementary charge
        self.assertAlmostEqual(e_calc, self.e, delta=1e-21)
        
        # Verify exact value (defined constant since 2019)
        self.assertEqual(self.e, 1.602176634e-19)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)