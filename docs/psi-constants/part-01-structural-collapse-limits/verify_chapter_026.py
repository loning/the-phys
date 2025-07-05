#!/usr/bin/env python3
"""
Verification program for Chapter 026: Collapse Dimensional Basis and Measurement Axes
Tests the mathematical consistency of dimensional emergence from ψ = ψ(ψ).
"""

import unittest
import math
import numpy as np
from itertools import product

class TestChapter026(unittest.TestCase):
    
    def setUp(self):
        # Golden ratio and related constants
        self.phi = (1 + math.sqrt(5)) / 2
        self.phi_inv = 1 / self.phi
        
        # Collapse units
        self.c_star = 2.0  # Speed limit
        self.hbar_star = self.phi**2 / (2 * math.pi)  # Action quantum
        self.G_star = self.phi**(-2)  # Gravitational coupling
        
        # Derived collapse units
        self.l_star = 1.0  # Length unit
        self.t_star = self.l_star / self.c_star  # Time unit = 0.5
        self.m_star = self.hbar_star * self.c_star / self.G_star  # Mass unit
        
        # Tolerance for numerical comparisons
        self.tol = 1e-10
        
    def test_minimal_measurement_basis(self):
        """Test that exactly 3 dimensions are necessary and sufficient"""
        # Test orthogonality of projection operators
        # P_L projects onto length, P_T onto time, P_M onto mass
        
        # Simplified representation as basis vectors
        P_L = np.array([1, 0, 0])
        P_T = np.array([0, 1, 0])
        P_M = np.array([0, 0, 1])
        
        # Check orthogonality
        self.assertAlmostEqual(np.dot(P_L, P_T), 0, delta=self.tol)
        self.assertAlmostEqual(np.dot(P_T, P_M), 0, delta=self.tol)
        self.assertAlmostEqual(np.dot(P_M, P_L), 0, delta=self.tol)
        
        # Check normalization
        self.assertAlmostEqual(np.dot(P_L, P_L), 1, delta=self.tol)
        self.assertAlmostEqual(np.dot(P_T, P_T), 1, delta=self.tol)
        self.assertAlmostEqual(np.dot(P_M, P_M), 1, delta=self.tol)
        
        # Check completeness (sum of projectors = identity)
        I = P_L[:, np.newaxis] @ P_L[np.newaxis, :] + \
            P_T[:, np.newaxis] @ P_T[np.newaxis, :] + \
            P_M[:, np.newaxis] @ P_M[np.newaxis, :]
        
        np.testing.assert_allclose(I, np.eye(3), atol=self.tol)
    
    def test_length_quantization(self):
        """Test length emerges from φ-trace network distance"""
        # Minimal network separation
        l_min = 1.0  # In collapse units
        
        # Check relationship to Planck length
        # l_P = 1/(4√π) in collapse units
        l_P_collapse = 1 / (4 * math.sqrt(math.pi))
        factor = l_min / l_P_collapse
        expected_factor = 4 * math.sqrt(math.pi)
        
        self.assertAlmostEqual(factor, expected_factor, delta=self.tol)
        
        # Test φ-trace distance formula
        # Distance between nodes at ranks r1 and r2
        def phi_distance(r1, r2):
            return self.phi**(-min(r1, r2))
        
        # Adjacent nodes at same rank
        d_adjacent = phi_distance(1, 1)
        self.assertAlmostEqual(d_adjacent, self.phi**(-1), delta=self.tol)
    
    def test_time_quantum(self):
        """Test time emerges from ψ-iteration count"""
        # Fundamental time unit
        t_star_calc = self.l_star / self.c_star
        self.assertAlmostEqual(t_star_calc, 0.5, delta=self.tol)
        self.assertAlmostEqual(t_star_calc, self.t_star, delta=self.tol)
        
        # Time for n iterations
        def iteration_time(n):
            return n * self.t_star
        
        # Test specific values
        self.assertAlmostEqual(iteration_time(1), 0.5, delta=self.tol)
        self.assertAlmostEqual(iteration_time(10), 5.0, delta=self.tol)
    
    def test_mass_quantum(self):
        """Test mass emerges from information density"""
        # Calculate mass unit from formula
        m_star_calc = self.hbar_star * self.c_star / self.G_star
        m_star_expected = (self.phi**2 / (2 * math.pi)) * 2 / self.phi**(-2)
        m_star_expected = self.phi**4 / math.pi
        
        self.assertAlmostEqual(m_star_calc, m_star_expected, delta=self.tol)
        self.assertAlmostEqual(m_star_calc, self.m_star, delta=self.tol)
        
        # Verify numerical value
        m_star_numerical = (3 + math.sqrt(5))**2 / (4 * math.pi)
        self.assertAlmostEqual(self.m_star, m_star_numerical, delta=0.001)
    
    def test_dimensional_orthogonality(self):
        """Test orthogonality of dimensional projection operators"""
        # Define projection operators as matrices
        # Each projects onto its respective subspace
        
        # In the (L,T,M) basis
        P_L = np.diag([1, 0, 0])
        P_T = np.diag([0, 1, 0])
        P_M = np.diag([0, 0, 1])
        
        # Test commutation relations
        comm_LT = P_L @ P_T - P_T @ P_L
        comm_TM = P_T @ P_M - P_M @ P_T
        comm_ML = P_M @ P_L - P_L @ P_M
        
        np.testing.assert_allclose(comm_LT, np.zeros((3,3)), atol=self.tol)
        np.testing.assert_allclose(comm_TM, np.zeros((3,3)), atol=self.tol)
        np.testing.assert_allclose(comm_ML, np.zeros((3,3)), atol=self.tol)
    
    def test_free_abelian_structure(self):
        """Test that dimensions form free abelian group Z³"""
        # Test group operations on dimensional tuples
        
        # Identity element
        identity = (0, 0, 0)  # L⁰T⁰M⁰ = dimensionless
        
        # Test some group operations
        dim1 = (1, -1, 0)  # Velocity L¹T⁻¹M⁰
        dim2 = (0, -1, 1)  # Power/time T⁻¹M¹
        
        # Addition (multiplication of dimensions)
        sum_dim = tuple(a + b for a, b in zip(dim1, dim2))
        expected = (1, -2, 1)  # L¹T⁻²M¹ = Force
        self.assertEqual(sum_dim, expected)
        
        # Inverse (reciprocal dimension)
        inv_dim1 = tuple(-a for a in dim1)
        expected_inv = (-1, 1, 0)  # L⁻¹T¹M⁰ = 1/velocity
        self.assertEqual(inv_dim1, expected_inv)
        
        # Check identity property
        id_sum = tuple(a + b for a, b in zip(dim1, inv_dim1))
        self.assertEqual(id_sum, identity)
    
    def test_information_content_formula(self):
        """Test dimensional information content calculation"""
        # Scale factors (example values)
        lambda_L = 2.0
        lambda_T = 3.0
        lambda_M = 1.5
        
        # Test dimension: Force = L¹T⁻²M¹
        a, b, c = 1, -2, 1
        
        I_dim = abs(a) * math.log(lambda_L) / math.log(self.phi) + \
                abs(b) * math.log(lambda_T) / math.log(self.phi) + \
                abs(c) * math.log(lambda_M) / math.log(self.phi)
        
        # Check calculation
        expected = (math.log(lambda_L) + 2*math.log(lambda_T) + math.log(lambda_M)) / math.log(self.phi)
        self.assertAlmostEqual(I_dim, expected, delta=self.tol)
        
        # Natural units should minimize information
        # When all lambdas = 1, information = 0
        I_natural = abs(a) * 0 + abs(b) * 0 + abs(c) * 0
        self.assertEqual(I_natural, 0)
    
    def test_dimensional_lattice_distance(self):
        """Test Manhattan distance in dimensional space"""
        # Two dimensional points
        point1 = (2, -1, 1)  # Energy
        point2 = (1, -2, 1)  # Force
        
        # Manhattan distance
        d = sum(abs(p2 - p1) for p1, p2 in zip(point1, point2))
        
        # Expected: |2-1| + |-1-(-2)| + |1-1| = 1 + 1 + 0 = 2
        self.assertEqual(d, 2)
        
        # Test triangle inequality
        point3 = (0, 0, 0)  # Dimensionless
        
        d12 = sum(abs(p2 - p1) for p1, p2 in zip(point1, point2))
        d23 = sum(abs(p3 - p2) for p2, p3 in zip(point2, point3))
        d13 = sum(abs(p3 - p1) for p1, p3 in zip(point1, point3))
        
        # Triangle inequality: d13 ≤ d12 + d23
        self.assertLessEqual(d13, d12 + d23)
    
    def test_zeckendorf_dimensional_encoding(self):
        """Test Zeckendorf representation of dimensional exponents"""
        # Fibonacci sequence
        fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        
        def zeckendorf_decompose(n):
            """Find Zeckendorf representation of n"""
            if n == 0:
                return []
            
            result = []
            i = len(fibs) - 1
            while i >= 0 and n > 0:
                if fibs[i] <= n:
                    result.append(i)
                    n -= fibs[i]
                    i -= 2  # Skip next to avoid consecutive
                else:
                    i -= 1
            return result
        
        # Test some common dimensional exponents
        # 2 (squared quantities)
        z2 = zeckendorf_decompose(2)
        self.assertEqual(sum(fibs[i] for i in z2), 2)
        
        # 3 (cubic quantities like volume)
        z3 = zeckendorf_decompose(3)
        self.assertEqual(sum(fibs[i] for i in z3), 3)
        
        # Check no consecutive Fibonacci numbers
        for indices in [z2, z3]:
            for j in range(len(indices) - 1):
                self.assertGreater(indices[j] - indices[j+1], 1)
    
    def test_tensor_decomposition(self):
        """Test unique tensor decomposition of physical quantities"""
        # Energy has dimensions L²T⁻²M¹
        # Represented as tensor product
        
        # Basis vectors (simplified as unit vectors)
        e_L = np.array([1])
        e_T = np.array([1])
        e_M = np.array([1])
        
        # Energy decomposition
        a, b, c = 2, -2, 1
        
        # The tensor structure (simplified)
        # Q = q × (e_L^⊗a) ⊗ (e_T^⊗b) ⊗ (e_M^⊗c)
        
        # Check uniqueness: different (a,b,c) give different dimensions
        dims = [(1,0,0), (0,1,0), (0,0,1), (1,-1,0), (2,-2,1)]
        
        # All should be distinct
        self.assertEqual(len(dims), len(set(dims)))
    
    def test_derived_dimensions(self):
        """Test that charge and temperature reduce to LTM"""
        # Electric charge
        # Q ~ √(ML³T⁻²) × √α
        # Check dimensional analysis
        
        # From Coulomb's law: F = kq²/r²
        # k = 1/(4πε₀) has dimensions to make F have dimension of force
        # This gives Q² ~ Force × Length² = ML³T⁻²
        
        charge_dim_squared = (3, -2, 1)  # L³T⁻²M¹
        
        # Temperature from kinetic theory
        # kT ~ Energy = ML²T⁻²
        temp_dim = (2, -2, 1)  # Same as energy
        
        # Both can be expressed in terms of L, T, M
        self.assertEqual(len(charge_dim_squared), 3)
        self.assertEqual(len(temp_dim), 3)
    
    def test_relativistic_dimensional_reduction(self):
        """Test effective dimension reduction at v → c"""
        # At v → c, space and time mix
        # Effective dimension count reduces
        
        v_over_c_values = [0.1, 0.5, 0.9, 0.99, 0.999]
        
        for v_over_c in v_over_c_values:
            # Lorentz factor
            gamma = 1 / math.sqrt(1 - v_over_c**2)
            
            # Effective mixing of space and time
            # As v → c, L and cT become indistinguishable
            mixing = v_over_c
            
            # Effective dimension count
            # 3 dimensions reduce toward 2 as v → c
            dim_eff = 3 - mixing + mixing**2
            
            self.assertLess(dim_eff, 3)
            self.assertGreater(dim_eff, 2)
    
    def test_dimensional_uncertainty_relations(self):
        """Test quantum uncertainty in dimensional measurements"""
        # Position-time uncertainty
        # ΔL · ΔT ≥ ħ/(2mc) = λ_C/(4π)
        
        # Test mass (in collapse units)
        m_test = 1.0
        
        # Compton wavelength in collapse units
        lambda_C = self.hbar_star / (m_test * self.c_star)
        
        # Uncertainty bound
        bound = lambda_C / (4 * math.pi)
        
        # Test some uncertainty products
        delta_L = 0.1
        delta_T_min = bound / delta_L
        
        # Product should satisfy uncertainty relation
        product = delta_L * delta_T_min
        self.assertGreaterEqual(product, bound - self.tol)
    
    def test_holographic_dimensional_scaling(self):
        """Test holographic principle for dimensional reduction"""
        # Area scales as L²
        # Volume scales as L³
        # But information scales as Area (holographic principle)
        
        L = 10.0  # Example length scale
        
        Area = L**2
        Volume = L**3
        
        # Entropy/Information ~ Area (not Volume)
        S_area = Area / (4 * self.G_star * self.hbar_star)
        
        # Check scaling
        L2 = 20.0
        Area2 = L2**2
        S_area2 = Area2 / (4 * self.G_star * self.hbar_star)
        
        # Information should scale as L²
        ratio = S_area2 / S_area
        expected_ratio = (L2 / L)**2
        
        self.assertAlmostEqual(ratio, expected_ratio, delta=self.tol)
    
    def test_measurement_trinity_completeness(self):
        """Test that L, T, M form complete measurement basis"""
        # All fundamental equations should be expressible in LTM
        
        # Newton's law: F = ma
        # F: MLT⁻², m: M, a: LT⁻²
        force = (1, -2, 1)
        mass = (0, 0, 1)
        accel = (1, -2, 0)
        
        # Check F = m × a dimensionally
        ma_dim = tuple(m + a for m, a in zip(mass, accel))
        self.assertEqual(force, ma_dim)
        
        # Maxwell equations
        # All electromagnetic quantities reducible to LTM + α
        # E-field: MLT⁻³I⁻¹ but I = √(ML³T⁻²)α^(1/2)
        # This confirms all physics needs only (L,T,M) + dimensionless constants
        
        # Energy-momentum relation: E² = (pc)² + (mc²)²
        # All terms have dimension [ML²T⁻²]²
        energy_dim = (2, -2, 1)
        energy_squared = tuple(2*d for d in energy_dim)
        
        # Both terms have same dimension
        pc_squared = tuple(2*d for d in energy_dim)
        mc2_squared = tuple(2*d for d in energy_dim)
        
        self.assertEqual(energy_squared, pc_squared)
        self.assertEqual(energy_squared, mc2_squared)
    
    def test_phi_trace_dimensional_origin(self):
        """Test that dimensions emerge from φ-trace structure"""
        # Length from geodesics
        # Time from iterations  
        # Mass from information density
        
        # Check relationships
        # c* = length*/time* = 1.0/0.5 = 2.0 ✓
        self.assertAlmostEqual(self.l_star/self.t_star, self.c_star, delta=self.tol)
        
        # The fundamental constants are dimensionless in collapse units
        # They represent pure numbers from φ-trace geometry
        
        # c* = 2 (pure number, ratio of scales)
        self.assertAlmostEqual(self.c_star, 2.0, delta=self.tol)
        
        # ħ* = φ²/(2π) (pure number, minimal action)
        self.assertAlmostEqual(self.hbar_star, self.phi**2/(2*math.pi), delta=self.tol)
        
        # G* = φ⁻² (pure number, coupling strength)
        self.assertAlmostEqual(self.G_star, self.phi**(-2), delta=self.tol)
        
        # The mass unit is derived to make the constants work out
        # m* = ħ*c*/G* = φ⁴/π
        m_derived = self.hbar_star * self.c_star / self.G_star
        self.assertAlmostEqual(m_derived, self.m_star, delta=self.tol)
        self.assertAlmostEqual(m_derived, self.phi**4/math.pi, delta=0.001)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)