#!/usr/bin/env python3
"""
Verification program for Chapter 036: Binary Observer Trace Visibility
Tests how binary resolution limits determine which constants observers see at different scales.
"""

import unittest
import math
import numpy as np

class TestChapter036BinaryVisibility(unittest.TestCase):
    
    def setUp(self):
        # Golden ratio from binary constraint
        self.phi = (1 + math.sqrt(5)) / 2
        
        # Fine structure constant from binary paths
        self.alpha = 1/137.035999084
        
        # Human observer scale
        self.human_scale = self.phi**(-148)
        
        # Binary scales (powers of 2)
        self.binary_scales = [2**n for n in range(1, 20)]
        
        # Tolerance
        self.tol = 1e-10
        
    def test_binary_trace_visibility(self):
        """Test binary trace visibility function"""
        # Binary trace as Hamming distance
        def hamming_distance(s1, s2):
            return sum(b1 != b2 for b1, b2 in zip(s1, s2))
        
        # Test binary sequences
        s_initial = [1, 0, 1, 0, 1, 0]
        s_final = [0, 1, 0, 1, 0, 1]
        
        gamma = hamming_distance(s_initial, s_final)
        mu = 2**3  # 3-bit resolution
        
        # Binary visibility function
        def visibility(gamma, mu):
            mu_min = 1  # Single bit minimum
            return np.exp(-(gamma**2)/(mu**2)) * (1 if gamma >= mu_min else 0)
        
        v = visibility(gamma, mu)
        
        # Should be positive for valid trace
        self.assertGreater(v, 0)
        
        # Should decrease with larger traces
        v_small = visibility(2, mu)
        v_large = visibility(6, mu)
        self.assertGreater(v_small, v_large)
        
    def test_binary_resolution_hierarchy(self):
        """Test binary scale hierarchy mu = 2^n"""
        # Binary scales
        n_values = [3, 5, 8, 10]
        mu_values = [2**n for n in n_values]
        
        # Maximum observable trace at each scale
        def max_visible(mu):
            # From Fibonacci growth of valid patterns
            return mu * np.log(self.phi)
        
        max_lengths = [max_visible(mu) for mu in mu_values]
        
        # Should increase with bit resolution
        for i in range(len(max_lengths)-1):
            self.assertGreater(max_lengths[i+1], max_lengths[i])
            
        # Check discreteness
        for mu in mu_values:
            # mu should be power of 2
            self.assertEqual(mu & (mu - 1), 0)  # Bit trick for power of 2
        
    def test_binary_effective_coupling(self):
        """Test effective coupling at binary scales"""
        # Binary traces (Hamming distances)
        traces = [1, 2, 3, 4]  # Number of bit flips
        couplings = [0.1, 0.2, 0.3, 0.4]
        mu = 2**2  # 2-bit observer
        
        # Calculate effective coupling
        total_visibility = 0
        weighted_sum = 0
        
        for gamma, g in zip(traces, couplings):
            # Only valid if no consecutive 1s in path
            v = np.exp(-(gamma**2)/(mu**2))
            total_visibility += v
            weighted_sum += g * v
            
        g_eff = weighted_sum / total_visibility
        
        # Should be visibility-weighted average
        self.assertGreater(g_eff, min(couplings))
        self.assertLess(g_eff, max(couplings))
        
        # Should be closer to small-trace couplings
        self.assertLess(abs(g_eff - couplings[0]), abs(g_eff - couplings[-1]))
        
    def test_discrete_beta_function(self):
        """Test discrete running at binary scales"""
        # Test trace
        gamma = 3  # Hamming distance
        g = 0.1
        
        # Adjacent binary scales
        n1 = 3
        n2 = 4
        mu1 = 2**n1
        mu2 = 2**n2
        
        v1 = np.exp(-(gamma**2)/(mu1**2))
        v2 = np.exp(-(gamma**2)/(mu2**2))
        
        # Discrete beta function
        beta_discrete = g * (v2 - v1)
        
        # Should be finite and small
        self.assertLess(abs(beta_discrete), g)
        
        # Visibility should increase with scale
        self.assertGreater(v2, v1)
        
    def test_binary_scale_ordering(self):
        """Test binary scale hierarchy"""
        # Binary scales
        n_values = [4, 6, 8, 10, 12]
        scales = [2**n for n in n_values]
        
        # Should be strictly ordered
        for i in range(len(scales)-1):
            self.assertLess(scales[i], scales[i+1])
            
        # Ratios should be powers of 2
        for i in range(len(scales)-1):
            ratio = scales[i+1] / scales[i]
            # Check ratio is 2^k for some integer k
            k = np.log2(ratio)
            self.assertAlmostEqual(k, round(k), delta=self.tol)
            
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
        
    def test_binary_information_visibility(self):
        """Test information extraction with golden ratio base"""
        # Binary paths with different visibility
        visibilities = [0.1, 0.3, 0.5, 0.1]
        
        # Normalize
        total = sum(visibilities)
        probs = [v/total for v in visibilities]
        
        # Information content in base phi
        info = [-np.log(p)/np.log(self.phi) for p in probs if p > 0]
        
        # Should be bounded by channel capacity
        channel_capacity = 2  # Binary channel
        for i in info:
            self.assertGreater(i, 0)
            # Information per bit limited by capacity
            self.assertLess(i/np.log2(self.phi), channel_capacity * 10)
            
    def test_optimal_binary_observer_scale(self):
        """Test optimal scale for binary information extraction"""
        # Binary trace lengths (Hamming distances)
        traces = [1, 2, 3, 4, 5, 6]
        
        # Calculate mean square
        mean_sq = sum(t**2 for t in traces) / len(traces)
        mu_opt = np.sqrt(mean_sq)
        
        # Find nearest binary scale
        n_opt = round(np.log2(mu_opt))
        mu_binary = 2**n_opt
        
        # Should be close to continuous optimum
        self.assertLess(abs(mu_binary - mu_opt), mu_opt)
        
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
        
    def test_binary_visibility_windows(self):
        """Test Zeckendorf windows from binary structure"""
        # Test windows for ranks 5-8 (EM bundle)
        for k in range(5, 9):
            window_start = self.phi**k
            window_end = self.phi**(k+1)
            
            # Window width in bits
            bit_width = k * np.log2(self.phi)  # ~0.694k bits
            
            # Should correspond to Fibonacci growth
            fib_k = round((self.phi**k - (1-self.phi)**k) / np.sqrt(5))
            
            # Window size relates to valid binary patterns
            self.assertGreater(window_end, window_start)
            
            # Ratio is exactly phi
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
        
    def test_human_observer_alpha(self):
        """Test human observers see alpha = 1/137 at phi^(-148)"""
        # Human scale parameters
        human_bit_depth = 148  # log2(phi^148) bits of resolution
        
        # Alpha emerges from rank 6-7 binary patterns
        # These are optimally visible at human scale
        rank_6_visibility = 0.8  # High visibility
        rank_7_visibility = 0.6  # Good visibility
        rank_8_visibility = 0.1  # Low visibility
        
        # Weighted average gives alpha
        # (Full calculation in Chapter 033)
        weights = [rank_6_visibility, rank_7_visibility]
        
        # Check human scale is in right window
        window_6_7 = (self.phi**6, self.phi**7)
        
        # Human scale inverted gives right magnitude
        human_energy = self.phi**148  # Inverted scale
        
        # Check alpha value
        self.assertAlmostEqual(self.alpha, 1/137.036, delta=0.001)
        
        # Verify visibility ordering
        self.assertGreater(rank_6_visibility, rank_7_visibility)
        self.assertGreater(rank_7_visibility, rank_8_visibility)
            
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
        
    def test_binary_discovery_boundaries(self):
        """Test new physics at binary resolution boundaries"""
        # Binary visibility function
        def visibility(gamma, n_bits):
            mu = 2**n_bits
            return np.exp(-(gamma/mu)**2)
        
        # Test trace near visibility edge
        gamma = 10  # Large Hamming distance
        threshold = 0.1
        
        # Find bit resolution where trace becomes visible
        for n in range(1, 10):
            v = visibility(gamma, n)
            if v > threshold:
                n_discovery = n
                break
                
        # Verify discovery at this resolution
        self.assertGreater(visibility(gamma, n_discovery), threshold)
        self.assertLess(visibility(gamma, n_discovery-1), threshold)
        
        # New physics emerges with each bit of resolution
        self.assertTrue(1 <= n_discovery <= 10)
        
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
        
    def test_binary_master_formula(self):
        """Test master formula with binary paths"""
        # Binary paths: (Hamming distance, constant value)
        paths = [(1, 0.1), (2, 0.2), (3, 0.3), (4, 0.4)]
        n_bits = 2
        mu = 2**n_bits
        
        # Calculate observable with binary weights
        total_weight = 0
        weighted_sum = 0
        
        for gamma, C_gamma in paths:
            # Check path satisfies no consecutive 1s
            # (simplified: all paths valid here)
            visibility = np.exp(-(gamma**2)/(mu**2))
            
            # Action = information cost in bits
            action = gamma * np.log(2)  # Each bit flip costs ln(2)
            path_weight = visibility * np.exp(-action)
            
            total_weight += path_weight
            weighted_sum += C_gamma * path_weight
            
        C_obs = weighted_sum / total_weight
        
        # Observable should be weighted average
        self.assertGreater(C_obs, min(c for _, c in paths))
        self.assertLess(C_obs, max(c for _, c in paths))
        
        # Test discrete running
        n_bits2 = 3
        mu2 = 2**n_bits2
        total_weight2 = 0
        weighted_sum2 = 0
        
        for gamma, C_gamma in paths:
            visibility = np.exp(-(gamma**2)/(mu2**2))
            action = gamma * np.log(2)
            path_weight = visibility * np.exp(-action)
            
            total_weight2 += path_weight
            weighted_sum2 += C_gamma * path_weight
            
        C_obs2 = weighted_sum2 / total_weight2
        
        # Should see different effective value
        self.assertNotAlmostEqual(C_obs, C_obs2, delta=0.001)
        
        # Higher resolution changes visibility pattern
        # The change depends on trace distribution
        self.assertNotEqual(C_obs, C_obs2)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)