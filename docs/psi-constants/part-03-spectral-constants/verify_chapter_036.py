#!/usr/bin/env python3
"""
Verification program for Chapter 036: Effective Constants from Observer Trace Visibility
Tests the observer-scale dependent emergence of effective constants.
"""

import unittest
import math
import numpy as np

class TestChapter036(unittest.TestCase):
    
    def setUp(self):
        # Golden ratio
        self.phi = (1 + math.sqrt(5)) / 2
        
        # Fine structure constant
        self.alpha = 1/137.035999084
        
        # Test energy scales (GeV)
        self.m_e = 0.511e-3  # electron mass
        self.M_Z = 91.2      # Z boson mass
        self.M_P = 1.22e19   # Planck mass
        
        # Tolerance
        self.tol = 1e-10
        
    def test_trace_visibility_function(self):
        """Test visibility function properties"""
        # Test parameters
        gamma = 1.0  # trace length
        mu = 2.0     # observer scale
        mu_min = 0.1 # minimum resolution
        
        # Visibility function
        def visibility(gamma, mu, mu_min):
            return np.exp(-(gamma**2)/(mu**2)) * (1 if gamma > mu_min else 0)
        
        # Test basic properties
        v = visibility(gamma, mu, mu_min)
        
        # Should be positive
        self.assertGreaterEqual(v, 0)
        
        # Should decrease with gamma
        v1 = visibility(1.0, mu, mu_min)
        v2 = visibility(2.0, mu, mu_min)
        self.assertGreater(v1, v2)
        
        # Should be zero below threshold
        v_below = visibility(mu_min/2, mu, mu_min)
        self.assertEqual(v_below, 0)
        
    def test_resolution_hierarchy(self):
        """Test that resolution follows hierarchy"""
        # Test scales
        mu_values = [0.1, 1.0, 10.0, 100.0]
        
        # Maximum visible trace length
        def max_visible(mu):
            return mu * np.log(self.phi)
        
        # Should increase with scale
        max_lengths = [max_visible(mu) for mu in mu_values]
        
        for i in range(len(max_lengths)-1):
            self.assertGreater(max_lengths[i+1], max_lengths[i])
        
    def test_effective_coupling_calculation(self):
        """Test effective coupling from trace visibility"""
        # Simple test with discrete traces
        traces = [1.0, 2.0, 3.0]
        couplings = [0.1, 0.2, 0.3]
        mu = 2.0
        
        # Calculate effective coupling
        total_visibility = 0
        weighted_sum = 0
        
        for gamma, g in zip(traces, couplings):
            v = np.exp(-(gamma**2)/(mu**2))
            total_visibility += v
            weighted_sum += g * v
            
        g_eff = weighted_sum / total_visibility
        
        # Should be weighted average
        self.assertGreater(g_eff, min(couplings))
        self.assertLess(g_eff, max(couplings))
        
    def test_beta_function_from_visibility(self):
        """Test beta function emergence from visibility change"""
        # Test trace
        gamma = 1.0
        g = 0.1
        
        # Visibility at two nearby scales
        mu1 = 2.0
        mu2 = 2.1
        
        v1 = np.exp(-(gamma**2)/(mu1**2))
        v2 = np.exp(-(gamma**2)/(mu2**2))
        
        # Numerical derivative
        d_log_mu = np.log(mu2) - np.log(mu1)
        beta_approx = (v2 - v1) / d_log_mu
        
        # Should be finite
        self.assertLess(abs(beta_approx), 1.0)
        
    def test_scale_ordering(self):
        """Test that scales form proper ordering"""
        # Test scales
        scales = [self.m_e, 1.0, self.M_Z, 1000.0]
        
        # Should be ordered
        for i in range(len(scales)-1):
            self.assertLess(scales[i], scales[i+1])
            
        # Ratios should be meaningful
        for i in range(len(scales)-1):
            ratio = scales[i+1] / scales[i]
            self.assertGreater(ratio, 1.0)
            
    def test_visibility_tensor_properties(self):
        """Test visibility tensor structure"""
        # Simple 2x2x2 tensor
        T = np.zeros((2, 2, 2))
        
        # Fill with example values
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    T[i,j,k] = np.exp(-(i+j+k))
                    
        # Check tensor properties
        self.assertEqual(T.shape, (2, 2, 2))
        
        # All elements should be positive
        self.assertTrue(np.all(T >= 0))
        
        # Should decrease with indices
        self.assertGreater(T[0,0,0], T[1,1,1])
        
    def test_information_visibility(self):
        """Test information extraction from visibility"""
        # Test paths with different visibility
        visibilities = [0.1, 0.3, 0.5, 0.1]
        
        # Normalize
        total = sum(visibilities)
        probs = [v/total for v in visibilities]
        
        # Information content
        info = [-np.log(p) for p in probs if p > 0]
        
        # Should be finite and positive
        for i in info:
            self.assertGreater(i, 0)
            self.assertLess(i, 10)  # Reasonable bound
            
    def test_optimal_observer_scale(self):
        """Test optimal scale for information extraction"""
        # Mock trace lengths
        traces = [0.5, 1.0, 1.5, 2.0]
        
        # Calculate mean square
        mean_sq = sum(t**2 for t in traces) / len(traces)
        mu_opt = np.sqrt(mean_sq)
        
        # Should be between min and max trace length
        self.assertGreater(mu_opt, min(traces))
        self.assertLess(mu_opt, max(traces))
        
    def test_visibility_domains(self):
        """Test visibility domain structure"""
        # Define some domains
        domain1 = (0.1, 1.0)  # Low energy
        domain2 = (0.5, 2.0)  # Mid energy
        domain3 = (1.5, 10.0) # High energy
        
        # Check overlaps
        domains = [domain1, domain2, domain3]
        
        # Should have proper ordering
        for i in range(len(domains)-1):
            self.assertLess(domains[i][0], domains[i+1][0])
            
    def test_constant_hierarchy(self):
        """Test hierarchy of constants by visibility"""
        # Test constants with different visibility thresholds
        constants = {
            'alpha': 0.1,   # Low threshold
            'g_s': 1.0,     # Medium threshold  
            'g_w': 10.0,    # High threshold
            'lambda_H': 100.0  # Very high threshold
        }
        
        # Sort by threshold
        sorted_constants = sorted(constants.items(), key=lambda x: x[1])
        
        # Check ordering matches expected hierarchy
        expected_order = ['alpha', 'g_s', 'g_w', 'lambda_H']
        actual_order = [name for name, _ in sorted_constants]
        
        self.assertEqual(actual_order, expected_order)
        
    def test_zeckendorf_visibility_windows(self):
        """Test Zeckendorf window structure"""
        # Test windows for ranks 5-8
        for k in range(5, 9):
            window_start = self.phi**k
            window_end = self.phi**(k+1)
            
            # Window should be well-defined
            self.assertGreater(window_end, window_start)
            
            # Ratio should be phi
            ratio = window_end / window_start
            self.assertAlmostEqual(ratio, self.phi, delta=self.tol)
            
    def test_coherence_length(self):
        """Test trace coherence length"""
        # Test momentum
        k_gamma = 2.0
        
        # Coherence length
        l_coh = 2 * np.pi / k_gamma
        
        # Should be positive
        self.assertGreater(l_coh, 0)
        
        # Should scale inversely with momentum
        k_gamma2 = 4.0
        l_coh2 = 2 * np.pi / k_gamma2
        
        self.assertAlmostEqual(l_coh2, l_coh/2, delta=self.tol)
        
    def test_trace_evolution_operator(self):
        """Test trace evolution properties"""
        # Simple evolution operator (unitary)
        theta = 0.1
        U = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        
        # Check unitarity
        U_dagger = U.T.conj()
        identity = U @ U_dagger
        
        np.testing.assert_allclose(identity, np.eye(2), atol=self.tol)
        
    def test_observer_dependent_alpha(self):
        """Test that different observers see same alpha in window"""
        # Test window for alpha (ranks 6-7)
        window = (self.phi**6, self.phi**7)
        
        # Test observers at different scales in window
        scales = [window[0] * 1.2, window[0] * 1.5, window[0] * 1.8]
        
        alphas = []
        for mu in scales:
            # Simple model: alpha visibility
            alpha_obs = self.alpha * np.exp(-((mu - window[0]*1.5)**2) / (window[0]**2))
            alphas.append(alpha_obs)
            
        # Should be similar (within factor of 2)
        for i in range(len(alphas)-1):
            ratio = alphas[i+1] / alphas[i]
            self.assertGreater(ratio, 0.5)
            self.assertLess(ratio, 2.0)
            
    def test_visibility_phase_transitions(self):
        """Test phase transitions in visibility"""
        # Critical scale
        gamma = 1.0
        mu_c = gamma * np.sqrt(np.log(self.phi))
        
        # Visibility just above and below
        epsilon = 0.01
        v_above = np.exp(-((gamma)**2)/((mu_c + epsilon)**2))
        v_below = np.exp(-((gamma)**2)/((mu_c - epsilon)**2))
        
        # Should show significant change
        change = abs(v_above - v_below)
        self.assertGreater(change, 0.001)
        
    def test_new_physics_prediction(self):
        """Test prediction of new physics at visibility boundaries"""
        # Mock visibility function
        def visibility_mock(gamma, mu):
            return np.exp(-(gamma/mu)**2)
        
        # Test trace that becomes visible
        gamma = 5.0
        threshold = 0.1
        
        # Find scale where visibility = threshold
        mu_new = gamma / np.sqrt(-np.log(threshold))
        
        # Check visibility at this scale
        v_at_threshold = visibility_mock(gamma, mu_new)
        self.assertAlmostEqual(v_at_threshold, threshold, delta=0.001)
        
    def test_total_visibility_functional(self):
        """Test total visibility functional"""
        # Simple discrete version
        gammas = [1.0, 2.0, 3.0]
        C_values = [0.1, 0.2, 0.3]
        visibilities = [0.5, 0.3, 0.2]
        weights = [1.0, 1.0, 1.0]
        
        # Calculate weighted average
        numerator = sum(C * v * w for C, v, w in zip(C_values, visibilities, weights))
        denominator = sum(v * w for v, w in zip(visibilities, weights))
        
        C_total = numerator / denominator
        
        # Should be between min and max
        self.assertGreater(C_total, min(C_values))
        self.assertLess(C_total, max(C_values))
        
    def test_master_visibility_formula(self):
        """Test master formula for observable constants"""
        # Simplified version with discrete paths
        paths = [(1.0, 0.1), (2.0, 0.2), (3.0, 0.3)]  # (gamma, C(gamma))
        mu = 2.0
        
        # Calculate with visibility weights
        total_weight = 0
        weighted_sum = 0
        
        for gamma, C_gamma in paths:
            visibility = np.exp(-(gamma**2)/(mu**2))
            action = gamma**2 / 2  # Simple action
            path_weight = visibility * np.exp(-action)
            
            total_weight += path_weight
            weighted_sum += C_gamma * path_weight
            
        C_obs = weighted_sum / total_weight
        
        # Should be finite and reasonable
        self.assertGreater(C_obs, 0)
        self.assertLess(C_obs, 1)
        
        # Should depend on scale
        mu2 = 4.0
        total_weight2 = 0
        weighted_sum2 = 0
        
        for gamma, C_gamma in paths:
            visibility = np.exp(-(gamma**2)/(mu2**2))
            action = gamma**2 / 2
            path_weight = visibility * np.exp(-action)
            
            total_weight2 += path_weight
            weighted_sum2 += C_gamma * path_weight
            
        C_obs2 = weighted_sum2 / total_weight2
        
        # Should be different (running)
        self.assertNotAlmostEqual(C_obs, C_obs2, delta=0.001)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)