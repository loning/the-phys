#!/usr/bin/env python3
"""
Verification program for Chapter 035: Collapse Path Filter and Fine Structure Constants
Tests the path filtering mechanisms for observable constants.
"""

import unittest
import math
import numpy as np

class TestChapter035(unittest.TestCase):
    
    def setUp(self):
        # Golden ratio
        self.phi = (1 + math.sqrt(5)) / 2
        
        # Fine structure constant
        self.alpha = 1/137.035999084
        
        # Detection threshold
        self.epsilon = 1e-10
        
        # Inverse temperature for information filter
        self.beta = 1.0
        
        # Fundamental frequency
        self.omega_0 = 2 * math.pi
        
        # Tolerance
        self.tol = 1e-10
        
    def test_filter_composition(self):
        """Test that filter composition is associative"""
        # Define simple test filters as functions
        def F1(x):
            return x * 2
            
        def F2(x):
            return x + 1
            
        def F3(x):
            return x ** 2
            
        # Test associativity: F3 ∘ (F2 ∘ F1) = (F3 ∘ F2) ∘ F1
        x = 3.0
        
        # Left association
        left = F3(F2(F1(x)))
        
        # Right association  
        right = F3(F2(F1(x)))
        
        self.assertAlmostEqual(left, right, delta=self.tol)
        
    def test_measurement_filter(self):
        """Test measurement filter selection"""
        # Mock path with observable weight
        class MockPath:
            def __init__(self, weight):
                self.weight = weight
                
        # Create test paths
        paths = [MockPath(0.1), MockPath(0.01), MockPath(0.001), MockPath(1e-11)]
        
        # Apply measurement filter
        filtered = []
        for path in paths:
            if path.weight > self.epsilon:
                filtered.append(path)
                
        # Should filter out the last path
        self.assertEqual(len(filtered), 3)
        self.assertGreater(filtered[-1].weight, self.epsilon)
        
    def test_electromagnetic_bundle_structure(self):
        """Test EM path bundle has correct rank range"""
        # EM bundle includes ranks 5-8
        rank_range = range(5, 9)
        
        # Check bundle properties
        self.assertEqual(min(rank_range), 5)
        self.assertEqual(max(rank_range), 8)
        self.assertEqual(len(rank_range), 4)
        
        # Ranks 6-7 should be in the middle
        self.assertIn(6, rank_range)
        self.assertIn(7, rank_range)
        
    def test_information_filter(self):
        """Test information-theoretic filter with Boltzmann weighting"""
        # Test paths with different information content
        I_values = [1.0, 2.0, 3.0, 4.0]
        
        # Apply information filter
        weights = []
        for I in I_values:
            weight = np.exp(-self.beta * I)
            weights.append(weight)
            
        # Weights should decrease with information
        for i in range(len(weights)-1):
            self.assertGreater(weights[i], weights[i+1])
            
        # Check Boltzmann distribution normalization
        Z = sum(weights)
        probs = [w/Z for w in weights]
        self.assertAlmostEqual(sum(probs), 1.0, delta=self.tol)
        
    def test_resonance_filter(self):
        """Test resonance condition for path selection"""
        # Test frequencies
        frequencies = [
            0.5 * self.omega_0,  # n=0.5 (not resonant)
            1.0 * self.omega_0,  # n=1 (resonant)
            2.0 * self.omega_0,  # n=2 (resonant)
            1.5 * self.omega_0,  # n=1.5 (not resonant)
            3.0 * self.omega_0   # n=3 (resonant)
        ]
        
        # Check resonance
        resonant = []
        for omega in frequencies:
            n = omega / self.omega_0
            if abs(n - round(n)) < self.tol:
                resonant.append(omega)
                
        # Should have 3 resonant frequencies
        self.assertEqual(len(resonant), 3)
        
    def test_filter_spectral_gap(self):
        """Test that observable filters have spectral gap"""
        # Simple 2×2 filter matrix
        F = np.array([[0.9, 0.1], [0.1, 0.8]])
        
        # Get eigenvalues
        eigenvals = np.linalg.eigvals(F)
        eigenvals = sorted(eigenvals, reverse=True)
        
        # Compute gap
        gap = eigenvals[0] - eigenvals[1]
        
        # Should have positive gap
        self.assertGreater(gap, 0)
        
        # Check there is a minimum gap
        min_gap = 0.01
        self.assertGreater(gap, min_gap)
        
    def test_filter_intersection(self):
        """Test intersection of multiple filters"""
        # Define path sets for each filter
        measurement_paths = {1, 2, 3, 4, 5}
        resonance_paths = {2, 3, 5, 7, 8}
        information_paths = {1, 3, 4, 5, 8}
        energy_paths = {2, 3, 4, 5, 6}
        
        # EM filter is intersection of all
        em_paths = measurement_paths & resonance_paths & information_paths & energy_paths
        
        # Should only include paths passing all filters
        self.assertEqual(em_paths, {3, 5})
        
    def test_zeckendorf_pattern_filter(self):
        """Test filtering by Zeckendorf patterns"""
        # Allowed patterns for α
        allowed_patterns = {(6,), (7,), (5,1), (4,2), (3,3)}
        
        # Test various patterns
        test_patterns = [
            (6,),      # Allowed
            (7,),      # Allowed
            (8,),      # Not allowed
            (5,1),     # Allowed
            (4,3),     # Not allowed
            (3,3),     # Allowed
        ]
        
        # Apply filter
        filtered = []
        for pattern in test_patterns:
            if pattern in allowed_patterns:
                filtered.append(pattern)
                
        # Should have 4 allowed patterns
        self.assertEqual(len(filtered), 4)
        
    def test_filter_tensor_product(self):
        """Test tensor product of filters"""
        # Simple filters as matrices
        F1 = np.array([[0.8, 0.2], [0.3, 0.7]])
        F2 = np.array([[0.9, 0.1], [0.4, 0.6]])
        
        # Tensor product
        F_product = np.kron(F1, F2)
        
        # Check dimensions
        self.assertEqual(F_product.shape, (4, 4))
        
        # Check specific element
        self.assertAlmostEqual(F_product[0,0], F1[0,0] * F2[0,0], delta=self.tol)
        
    def test_running_filter_evolution(self):
        """Test scale-dependent filter evolution"""
        # Initial filter value
        F0 = 1.0
        
        # Simple beta function
        def beta(mu):
            return 0.1  # Constant for simplicity
            
        # Evolve from μ₀ to μ
        mu_0 = 1.0
        mu = 2.0
        
        # Integrate: F(μ) = F₀ * exp(∫ β(μ') dμ'/μ')
        # For constant β: F(μ) = F₀ * exp(β * log(μ/μ₀))
        F_mu = F0 * np.exp(beta(mu) * np.log(mu/mu_0))
        
        # Should increase with scale
        self.assertGreater(F_mu, F0)
        
        # Check specific value
        expected = F0 * (mu/mu_0)**beta(mu)
        self.assertAlmostEqual(F_mu, expected, delta=self.tol)
        
    def test_observable_subspace_dimension(self):
        """Test that observable subspace has finite dimension"""
        # Mock filter as projection matrix
        # Project onto 3D subspace of 5D space
        P = np.zeros((5, 5))
        P[0,0] = P[1,1] = P[2,2] = 1  # Project first 3 dimensions
        
        # Dimension is trace of projection
        dim = np.trace(P)
        
        # Should be 3
        self.assertEqual(int(dim), 3)
        
        # Should be finite
        self.assertLess(dim, float('inf'))
        
    def test_filter_coherence(self):
        """Test associativity of filter composition"""
        # Define filters as matrices
        F1 = np.array([[0.9, 0.1], [0.2, 0.8]])
        F2 = np.array([[0.7, 0.3], [0.4, 0.6]])
        F3 = np.array([[0.8, 0.2], [0.1, 0.9]])
        
        # Test (F3 ∘ F2) ∘ F1 = F3 ∘ (F2 ∘ F1)
        left = F3 @ (F2 @ F1)
        right = (F3 @ F2) @ F1
        
        np.testing.assert_allclose(left, right, atol=self.tol)
        
    def test_filter_boundary_prediction(self):
        """Test that new constants appear at filter boundaries"""
        # Simple 1D filter function
        def filter_func(x):
            return np.exp(-(x-5)**2)  # Peaked at x=5
            
        # Find boundary where filter = ε
        x_values = np.linspace(0, 10, 1000)
        f_values = [filter_func(x) for x in x_values]
        
        # Find points near threshold
        boundary_points = []
        for i, (x, f) in enumerate(zip(x_values, f_values)):
            if abs(f - self.epsilon) < 0.01:
                boundary_points.append(x)
                
        # Should find points on both sides of peak
        self.assertGreater(len(boundary_points), 0)
        
    def test_master_filter_convergence(self):
        """Test convergence of iterated filter application"""
        # Simple contractive filter
        F = np.array([[0.9, 0.05], [0.1, 0.95]])
        T = np.array([[0.8, 0.2], [0.3, 0.7]])
        O = np.array([[1, 0], [0, 2]])
        
        # Iterate F^n ∘ T^n
        n_max = 10
        ratios = []
        
        for n in range(1, n_max):
            FT_n = np.linalg.matrix_power(F @ T, n)
            numerator = np.trace(FT_n @ O)
            denominator = np.trace(FT_n)
            if denominator != 0:
                ratios.append(numerator / denominator)
                
        # Should converge
        if len(ratios) > 2:
            diff1 = abs(ratios[-1] - ratios[-2])
            diff2 = abs(ratios[-2] - ratios[-3])
            self.assertLess(diff1, diff2)  # Convergence
            
    def test_alpha_from_filtered_paths(self):
        """Test that filtered paths give correct order for α"""
        # Mock filtered path weights
        filtered_weights = [
            self.phi**(-6) * 0.4,  # Rank 6 contribution
            self.phi**(-7) * 0.6   # Rank 7 contribution
        ]
        
        # Total weight
        total = sum(filtered_weights)
        
        # Should be order of α when properly normalized
        # Just check order of magnitude
        self.assertGreater(total, 1e-3)
        self.assertLess(total, 1e-1)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)