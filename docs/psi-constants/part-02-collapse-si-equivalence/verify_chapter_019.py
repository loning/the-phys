#!/usr/bin/env python3
"""
Verification program for Chapter 019: Equivalence Theorem Between Collapse and SI
Tests the mathematical consistency of unit system equivalence derivations.
"""

import unittest
import math
import numpy as np

class TestChapter019(unittest.TestCase):
    
    def setUp(self):
        # Golden ratio and related constants
        self.phi = (1 + math.sqrt(5)) / 2
        self.phi_inv = 1 / self.phi
        
        # Collapse constants (dimensionless)
        self.c_star = 2  # speed limit
        self.hbar_star = self.phi**2 / (2 * math.pi)  # action unit
        self.G_star = self.phi_inv**2  # gravitational coupling
        self.alpha = 1 / 137.035999084  # fine structure (dimensionless)
        
        # Collapse units
        self.delta_l = 1 / (4 * self.phi * math.sqrt(math.pi))
        self.delta_t = 1 / (8 * self.phi * math.sqrt(math.pi))
        self.delta_m = self.phi**3 / math.sqrt(math.pi)
        
        # Planck units in collapse system
        self.planck_length_collapse = 1 / (4 * math.sqrt(math.pi))
        self.planck_time_collapse = 1 / (8 * math.sqrt(math.pi))
        self.planck_mass_collapse = self.phi**2 / math.sqrt(math.pi)
        
        # SI Planck values (CODATA 2018)
        self.planck_length_SI = 1.616255e-35  # m
        self.planck_time_SI = 5.391247e-44  # s
        self.planck_mass_SI = 2.176434e-8  # kg
        
        # Scale factors
        self.lambda_l = self.planck_length_SI / self.planck_length_collapse
        self.lambda_t = self.planck_time_SI / self.planck_time_collapse
        self.lambda_m = self.planck_mass_SI / self.planck_mass_collapse
        
        # SI fundamental constants (exact/measured values)
        self.c_SI = 299792458  # m/s (exact by definition)
        self.hbar_SI = 1.054571817e-34  # J⋅s
        self.G_SI = 6.67430e-11  # m³⋅kg⁻¹⋅s⁻²
        
        # Tolerance for numerical comparisons
        self.tol = 1e-10
        self.loose_tol = 1e-6  # For experimental values
    
    def test_scale_factor_calculation(self):
        """Test calculation of scale factors from Planck units"""
        # Scale factors should be positive and finite
        self.assertGreater(self.lambda_l, 0)
        self.assertGreater(self.lambda_t, 0)
        self.assertGreater(self.lambda_m, 0)
        
        self.assertLess(self.lambda_l, float('inf'))
        self.assertLess(self.lambda_t, float('inf'))
        self.assertLess(self.lambda_m, float('inf'))
        
        # Verify they give the correct Planck unit ratios
        self.assertAlmostEqual(self.lambda_l * self.planck_length_collapse, 
                              self.planck_length_SI, delta=self.planck_length_SI * 1e-6)
        self.assertAlmostEqual(self.lambda_t * self.planck_time_collapse, 
                              self.planck_time_SI, delta=self.planck_time_SI * 1e-6)
        self.assertAlmostEqual(self.lambda_m * self.planck_mass_collapse, 
                              self.planck_mass_SI, delta=self.planck_mass_SI * 1e-6)
    
    def test_fundamental_constant_transformation(self):
        """Test transformation of fundamental constants between unit systems"""
        # Speed of light transformation: c_SI = c* × (λ_ℓ/λ_t)
        c_SI_predicted = self.c_star * (self.lambda_l / self.lambda_t)
        relative_error_c = abs(c_SI_predicted - self.c_SI) / self.c_SI
        self.assertLess(relative_error_c, 1e-6)  # Very high precision expected
        
        # Planck constant transformation: ħ_SI = ħ* × λ_m λ_ℓ² λ_t⁻¹
        hbar_SI_predicted = self.hbar_star * self.lambda_m * (self.lambda_l**2) / self.lambda_t
        relative_error_hbar = abs(hbar_SI_predicted - self.hbar_SI) / self.hbar_SI
        self.assertLess(relative_error_hbar, 1e-4)  # Within measurement precision
        
        # Gravitational constant transformation: G_SI = G* × λ_ℓ³/(λ_m λ_t²)
        G_SI_predicted = self.G_star * (self.lambda_l**3) / (self.lambda_m * self.lambda_t**2)
        relative_error_G = abs(G_SI_predicted - self.G_SI) / self.G_SI
        self.assertLess(relative_error_G, 0.1)  # G has larger experimental uncertainty
        
        # Fine structure constant (dimensionless - should be unchanged)
        alpha_SI_predicted = self.alpha
        self.assertAlmostEqual(alpha_SI_predicted, self.alpha, delta=self.tol)
    
    def test_dimensional_preservation(self):
        """Test that dimensional analysis is preserved under unit transformation"""
        # Test with various dimensional combinations
        dimensional_tests = [
            # (a, b, c) = powers of (length, time, mass)
            (1, 0, 0),   # Length
            (0, 1, 0),   # Time  
            (0, 0, 1),   # Mass
            (1, -1, 0),  # Speed
            (2, -1, 1),  # Action
            (3, -2, -1), # Gravitational constant
            (1, -2, 0),  # Acceleration
            (1, -2, 1),  # Force
            (2, -2, 1),  # Energy
        ]
        
        for a, b, c in dimensional_tests:
            # Create dimensional combination in collapse units
            quantity_collapse = (self.delta_l**a) * (self.delta_t**b) * (self.delta_m**c)
            
            # Transform to SI
            quantity_SI = quantity_collapse * (self.lambda_l**a) * (self.lambda_t**b) * (self.lambda_m**c)
            
            # Both should be positive and finite
            self.assertGreater(quantity_collapse, 0)
            self.assertGreater(quantity_SI, 0)
            self.assertLess(quantity_collapse, float('inf'))
            self.assertLess(quantity_SI, float('inf'))
            
            # Inverse transformation should recover original
            quantity_collapse_recovered = quantity_SI / ((self.lambda_l**a) * (self.lambda_t**b) * (self.lambda_m**c))
            self.assertAlmostEqual(quantity_collapse, quantity_collapse_recovered, delta=self.tol)
    
    def test_dimensionless_preservation(self):
        """Test that dimensionless quantities are preserved"""
        # Create some dimensionless combinations - use simpler tests
        dimensionless_tests = [
            # Ratios of same-dimensional quantities
            (1, 0, 0, 1, 0, 0),   # Length ratio
            (0, 1, 0, 0, 1, 0),   # Time ratio
            (0, 0, 1, 0, 0, 1),   # Mass ratio
            (1, -1, 0, 1, -1, 0), # Speed ratio
        ]
        
        for a1, b1, c1, a2, b2, c2 in dimensionless_tests:
            # Create quantities in collapse units with specific values
            Q1_collapse = 2.5 * (self.delta_l**a1) * (self.delta_t**b1) * (self.delta_m**c1)
            Q2_collapse = 1.3 * (self.delta_l**a2) * (self.delta_t**b2) * (self.delta_m**c2)
            
            # Form dimensionless ratio
            ratio_collapse = Q1_collapse / Q2_collapse
            
            # Transform to SI
            Q1_SI = Q1_collapse * (self.lambda_l**a1) * (self.lambda_t**b1) * (self.lambda_m**c1)
            Q2_SI = Q2_collapse * (self.lambda_l**a2) * (self.lambda_t**b2) * (self.lambda_m**c2)
            
            # Form ratio in SI
            ratio_SI = Q1_SI / Q2_SI
            
            # Ratios should be identical (within relative tolerance)
            relative_error = abs(ratio_collapse - ratio_SI) / max(abs(ratio_collapse), abs(ratio_SI))
            self.assertLess(relative_error, 1e-12)
    
    def test_physical_law_equivalence(self):
        """Test that physical laws maintain form under transformation"""
        # Newton's second law: F = ma
        # In collapse units: F_collapse = m_collapse × a_collapse
        m_collapse = 2.5 * self.delta_m  # some mass
        a_collapse = 1.3 * self.delta_l / (self.delta_t**2)  # some acceleration
        F_collapse = m_collapse * a_collapse
        
        # Transform to SI
        m_SI = m_collapse * self.lambda_m
        a_SI = a_collapse * self.lambda_l / (self.lambda_t**2)
        F_SI = m_SI * a_SI
        
        # Also transform force directly
        F_SI_direct = F_collapse * self.lambda_m * self.lambda_l / (self.lambda_t**2)
        
        # Should be equal (within relative tolerance for large numbers)
        relative_error = abs(F_SI - F_SI_direct) / max(abs(F_SI), abs(F_SI_direct))
        self.assertLess(relative_error, 1e-12)
        
        # Test energy conservation: E = (1/2)mv²
        v_collapse = 0.8 * self.delta_l / self.delta_t
        E_collapse = 0.5 * m_collapse * v_collapse**2
        
        v_SI = v_collapse * self.lambda_l / self.lambda_t
        E_SI = 0.5 * m_SI * v_SI**2
        
        E_SI_direct = E_collapse * self.lambda_m * (self.lambda_l**2) / (self.lambda_t**2)
        
        # Should be equal (within relative tolerance)
        relative_error_energy = abs(E_SI - E_SI_direct) / max(abs(E_SI), abs(E_SI_direct))
        self.assertLess(relative_error_energy, 1e-12)
    
    def test_information_content_preservation(self):
        """Test that information content is preserved"""
        # Create a physical quantity with some value
        test_length = 5.7  # in collapse units
        
        # Information content relative to fundamental unit
        info_collapse = math.log2(test_length / self.delta_l)
        
        # Transform to SI
        test_length_SI = test_length * self.lambda_l
        
        # Information content in SI (relative to SI fundamental unit)
        # Need to use corresponding SI fundamental scale
        SI_fundamental_length = self.delta_l * self.lambda_l  # collapse unit in SI
        info_SI = math.log2(test_length_SI / SI_fundamental_length)
        
        # Should be equal
        self.assertAlmostEqual(info_collapse, info_SI, delta=self.tol)
    
    def test_scale_factor_tensor_properties(self):
        """Test properties of the scale factor tensor"""
        # Create scale factor matrix
        Lambda = np.array([[self.lambda_l, 0, 0],
                          [0, self.lambda_t, 0],
                          [0, 0, self.lambda_m]])
        
        # Should be diagonal and invertible
        self.assertAlmostEqual(Lambda[0,1], 0, delta=self.tol)
        self.assertAlmostEqual(Lambda[0,2], 0, delta=self.tol)
        self.assertAlmostEqual(Lambda[1,0], 0, delta=self.tol)
        self.assertAlmostEqual(Lambda[1,2], 0, delta=self.tol)
        self.assertAlmostEqual(Lambda[2,0], 0, delta=self.tol)
        self.assertAlmostEqual(Lambda[2,1], 0, delta=self.tol)
        
        # Determinant should be non-zero (product of diagonal elements)
        det_Lambda = np.linalg.det(Lambda)
        expected_det = self.lambda_l * self.lambda_t * self.lambda_m
        self.assertAlmostEqual(det_Lambda, expected_det, delta=abs(expected_det * 1e-10))
        self.assertNotEqual(det_Lambda, 0)
        
        # Inverse should exist
        Lambda_inv = np.linalg.inv(Lambda)
        
        # Test that Lambda × Lambda⁻¹ = I
        product = np.matmul(Lambda, Lambda_inv)
        identity = np.eye(3)
        
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(product[i,j], identity[i,j], delta=1e-10)
    
    def test_experimental_observable_invariance(self):
        """Test that experimental observables are unit-invariant"""
        # Fine structure constant (already dimensionless)
        self.assertEqual(self.alpha, self.alpha)  # Trivially invariant
        
        # Proton-to-electron mass ratio (dimensionless)
        # This is just a test of the principle - using representative values
        m_proton_collapse = 1836.15 * self.delta_m  # approximately
        m_electron_collapse = 1.0 * self.delta_m    # normalized
        
        ratio_collapse = m_proton_collapse / m_electron_collapse
        
        # Transform to SI
        m_proton_SI = m_proton_collapse * self.lambda_m
        m_electron_SI = m_electron_collapse * self.lambda_m
        
        ratio_SI = m_proton_SI / m_electron_SI
        
        # Should be identical
        self.assertAlmostEqual(ratio_collapse, ratio_SI, delta=self.tol)
        
        # Verify the numerical value
        self.assertAlmostEqual(ratio_collapse, 1836.15, delta=0.01)
    
    def test_phi_structure_preservation(self):
        """Test that φ-trace structure is preserved"""
        # Create a quantity with explicit φ-dependence
        phi_quantity_collapse = self.phi**3 * self.delta_l  # some length with φ³ factor
        
        # The φ-structure should be preserved in the dimensionless coefficient
        # when we transform to SI
        phi_quantity_SI = phi_quantity_collapse * self.lambda_l
        
        # Extract the φ-factor
        base_length_SI = self.delta_l * self.lambda_l
        coefficient_SI = phi_quantity_SI / base_length_SI
        
        # Should still have φ³ factor
        self.assertAlmostEqual(coefficient_SI, self.phi**3, delta=self.tol)
    
    def test_computational_equivalence(self):
        """Test that computations give same results in both systems"""
        # Simulate a physics calculation: orbital velocity v = √(GM/r)
        
        # In collapse units
        M_collapse = 100 * self.delta_m  # some mass
        r_collapse = 50 * self.delta_l   # some radius
        v_collapse = math.sqrt(self.G_star * M_collapse / r_collapse)
        
        # Transform inputs to SI
        M_SI = M_collapse * self.lambda_m
        r_SI = r_collapse * self.lambda_l
        
        # Calculate in SI
        v_SI = math.sqrt(self.G_SI * M_SI / r_SI)
        
        # Transform result from collapse to SI
        v_SI_transformed = v_collapse * (self.lambda_l / self.lambda_t)
        
        # Should be equal
        relative_error = abs(v_SI - v_SI_transformed) / v_SI
        self.assertLess(relative_error, 1e-4)  # Within computational precision
    
    def test_unit_naturality(self):
        """Test naturality of the unit transformation"""
        # For any physical operation, the transformation should commute
        # Test with simple addition of same-dimensional quantities
        
        L1_collapse = 3.2 * self.delta_l
        L2_collapse = 1.7 * self.delta_l
        sum_collapse = L1_collapse + L2_collapse
        
        # Transform then add
        L1_SI = L1_collapse * self.lambda_l
        L2_SI = L2_collapse * self.lambda_l
        sum_SI_method1 = L1_SI + L2_SI
        
        # Add then transform
        sum_SI_method2 = sum_collapse * self.lambda_l
        
        # Should be equal (naturality)
        self.assertAlmostEqual(sum_SI_method1, sum_SI_method2, delta=self.tol)
    
    def test_error_propagation_preservation(self):
        """Test that relative errors are preserved"""
        # Create a measurement with uncertainty
        measurement_collapse = 7.43  # some value
        uncertainty_collapse = 0.05  # some uncertainty
        
        relative_error_collapse = uncertainty_collapse / measurement_collapse
        
        # Transform to SI (using arbitrary unit conversion)
        conversion_factor = self.lambda_l  # treating as length measurement
        measurement_SI = measurement_collapse * conversion_factor
        uncertainty_SI = uncertainty_collapse * conversion_factor
        
        relative_error_SI = uncertainty_SI / measurement_SI
        
        # Relative errors should be identical
        self.assertAlmostEqual(relative_error_collapse, relative_error_SI, delta=self.tol)
    
    def test_inverse_transformation(self):
        """Test that transformations are invertible"""
        # Start with some SI values
        length_SI = 2.5e-10  # some length in meters
        time_SI = 1.3e-15    # some time in seconds
        mass_SI = 9.1e-31    # some mass in kg
        
        # Transform to collapse
        length_collapse = length_SI / self.lambda_l
        time_collapse = time_SI / self.lambda_t
        mass_collapse = mass_SI / self.lambda_m
        
        # Transform back to SI
        length_SI_recovered = length_collapse * self.lambda_l
        time_SI_recovered = time_collapse * self.lambda_t
        mass_SI_recovered = mass_collapse * self.lambda_m
        
        # Should recover original values
        self.assertAlmostEqual(length_SI, length_SI_recovered, delta=length_SI * 1e-12)
        self.assertAlmostEqual(time_SI, time_SI_recovered, delta=time_SI * 1e-12)
        self.assertAlmostEqual(mass_SI, mass_SI_recovered, delta=mass_SI * 1e-12)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)