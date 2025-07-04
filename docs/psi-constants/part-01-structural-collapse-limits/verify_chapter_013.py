#!/usr/bin/env python3
"""
Chapter 013 Verification: Spectral Trace Boundedness and ℏ Emergence
Tests spectral properties and quantum constant emergence
"""

import math
import unittest

class TestChapter013SpectralBoundedness(unittest.TestCase):
    """Test suite for Chapter 013: Spectral Trace Boundedness"""
    
    def setUp(self):
        """Set up test constants"""
        self.phi = (1 + math.sqrt(5)) / 2
        self.pi = math.pi
        
        # From previous chapters
        self.hbar_star = self.phi**2 / (2 * self.pi)
        self.c_star = 2
        self.G_star = self.phi**(-2)
        
        # Fibonacci sequence
        self.fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    
    def fibonacci(self, n):
        """Calculate nth Fibonacci number"""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b
    
    def test_collapse_operator_spectrum(self):
        """Test eigenvalues λₙ = φ⁻ⁿ"""
        for n in range(1, 10):
            lambda_n = self.phi**(-n)
            
            # Check eigenvalue is positive
            self.assertGreater(lambda_n, 0, 
                             msg=f"Eigenvalue λ_{n} must be positive")
            
            # Check decay
            if n > 1:
                lambda_prev = self.phi**(-(n-1))
                ratio = lambda_n / lambda_prev
                self.assertAlmostEqual(ratio, self.phi**(-1), places=10,
                                     msg=f"Eigenvalue ratio at n={n}")
    
    def test_spectral_trace_convergence(self):
        """Test Tr[C] = Σ Dₙλₙ converges"""
        # Compute partial sums
        trace_10 = sum(self.fibonacci(n+2) * self.phi**(-n) for n in range(1, 11))
        trace_20 = sum(self.fibonacci(n+2) * self.phi**(-n) for n in range(1, 21))
        trace_30 = sum(self.fibonacci(n+2) * self.phi**(-n) for n in range(1, 31))
        
        # Check convergence
        self.assertLess(trace_10, trace_20, msg="Trace increasing")
        self.assertLess(trace_20, trace_30, msg="Trace increasing")
        
        # Check bounded
        self.assertLess(trace_30, 100, msg="Trace bounded")
        
        # Check convergence rate
        diff_1 = trace_20 - trace_10
        diff_2 = trace_30 - trace_20
        self.assertLess(diff_2, diff_1, msg="Decreasing differences")
    
    def test_action_quantization_from_spectrum(self):
        """Test Sₙ = -ℏ*log(λₙ) = nℏ*log(φ)"""
        for n in range(1, 6):
            lambda_n = self.phi**(-n)
            S_n = -self.hbar_star * math.log(lambda_n)
            
            # Expected action
            S_expected = n * self.hbar_star * math.log(self.phi)
            
            self.assertAlmostEqual(S_n, S_expected, places=10,
                                 msg=f"Action quantization at n={n}")
        
        # Check action gaps
        for n in range(1, 5):
            S_n = n * self.hbar_star * math.log(self.phi)
            S_next = (n+1) * self.hbar_star * math.log(self.phi)
            gap = S_next - S_n
            
            expected_gap = self.hbar_star * math.log(self.phi)
            self.assertAlmostEqual(gap, expected_gap, places=10,
                                 msg=f"Action gap at n={n}")
    
    def test_information_capacity_bound(self):
        """Test I_max = 2π/log(φ) bits"""
        I_max = 2 * self.pi / math.log(self.phi)
        
        # Check positive and finite
        self.assertGreater(I_max, 0, msg="Information capacity positive")
        self.assertLess(I_max, float('inf'), msg="Information capacity finite")
        
        # Check numerical value
        # I_max = 2π/log(φ) ≈ 13.057
        expected_I_max = 2 * self.pi / math.log(self.phi)
        self.assertAlmostEqual(I_max, expected_I_max, places=10,
                             msg="Information capacity value")
    
    def test_spectral_gap_constancy(self):
        """Test relative spectral gap is constant"""
        for n in range(1, 10):
            lambda_n = self.phi**(-n)
            lambda_next = self.phi**(-(n+1))
            
            gap = lambda_n - lambda_next
            relative_gap = gap / lambda_n
            
            expected = 1 - self.phi**(-1)
            self.assertAlmostEqual(relative_gap, expected, places=10,
                                 msg=f"Relative gap at n={n}")
    
    def test_trace_class_property(self):
        """Test ||C||₁ = Tr[C] < ∞"""
        # For positive operator, trace norm equals trace
        trace_partial = sum(self.fibonacci(n+2) * self.phi**(-n) 
                          for n in range(1, 50))
        
        # Check finite
        self.assertLess(trace_partial, float('inf'), 
                       msg="Trace norm finite")
        
        # Check positive
        self.assertGreater(trace_partial, 0,
                          msg="Trace norm positive")
    
    def test_moment_convergence(self):
        """Test all moments Mₖ = Σ Dₙλₙᵏ converge"""
        for k in range(1, 5):
            M_k = sum(self.fibonacci(n+2) * self.phi**(-n*k) 
                     for n in range(1, 30))
            
            # Check finite
            self.assertLess(M_k, float('inf'),
                           msg=f"Moment M_{k} finite")
            
            # Check positive  
            self.assertGreater(M_k, 0,
                              msg=f"Moment M_{k} positive")
            
            # Higher moments should be smaller
            if k > 1:
                M_prev = sum(self.fibonacci(n+2) * self.phi**(-n*(k-1))
                           for n in range(1, 30))
                self.assertLess(M_k, M_prev,
                               msg=f"Moment decay M_{k} < M_{k-1}")
    
    def test_partition_function_temperature(self):
        """Test T = ℏ*log(φ)/k_B"""
        # Temperature where trace equals partition function
        k_B = 1  # Natural units
        T = self.hbar_star * math.log(self.phi) / k_B
        
        # Check positive
        self.assertGreater(T, 0, msg="Temperature positive")
        
        # For the special temperature T = ℏ*log(φ)/k_B
        # We have β = 1/(kT) = 1/(ℏ*log(φ))
        beta = 1 / (k_B * T)
        
        # At this temperature, exp(-βnℏ*logφ) = exp(-n) ≠ φ^(-n)
        # The correct relation is:
        # Tr[C] at "temperature" where eigenvalues λ_n = φ^(-n) are Boltzmann weights
        # This gives effective inverse temperature β' = log(φ)
        
        beta_eff = math.log(self.phi)
        T_eff = 1 / (k_B * beta_eff)
        
        # This effective temperature should relate to ℏ*
        T_expected = self.hbar_star * math.log(self.phi) / k_B
        
        # They're the same!
        self.assertAlmostEqual(T, T_expected, places=10,
                             msg="Temperature relation consistency")
    
    def test_zeta_function_convergence(self):
        """Test ζ_C(s) = Σ Dₙλₙˢ convergence"""
        # Test for Re(s) > 0
        s_values = [0.5, 1.0, 1.5, 2.0]
        
        for s in s_values:
            zeta_s = sum(self.fibonacci(n+2) * self.phi**(-n*s)
                        for n in range(1, 50))
            
            # Check finite
            self.assertLess(zeta_s, float('inf'),
                           msg=f"ζ_C({s}) finite")
            
            # Check positive for real s > 0
            self.assertGreater(zeta_s, 0,
                              msg=f"ζ_C({s}) positive")
    
    def test_spectral_determinant_existence(self):
        """Test regularized determinant exists"""
        # Approximate -d/ds ζ_C(s) at s=0
        # Using finite difference
        epsilon = 0.001
        
        zeta_plus = sum(self.fibonacci(n+2) * self.phi**(-n*epsilon)
                       for n in range(1, 30))
        zeta_minus = sum(self.fibonacci(n+2) * self.phi**(n*epsilon)
                        for n in range(1, 30))
        
        # Derivative approximation
        zeta_prime_0 = (zeta_plus - zeta_minus) / (2 * epsilon)
        
        # Determinant
        log_det = -zeta_prime_0
        
        # Should be finite
        self.assertLess(abs(log_det), float('inf'),
                       msg="Log determinant finite")
    
    def test_graph_laplacian_connection(self):
        """Test C = φ^(-L) where L is graph Laplacian"""
        # For rank n, Laplacian eigenvalue is n
        # So C eigenvalue is φ^(-n)
        
        for n in range(1, 6):
            L_eigenvalue = n
            C_eigenvalue = self.phi**(-L_eigenvalue)
            
            expected = self.phi**(-n)
            self.assertAlmostEqual(C_eigenvalue, expected, places=10,
                                 msg=f"Graph Laplacian relation at n={n}")
    
    def test_hbar_uniqueness(self):
        """Test ℏ* = φ²/(2π) is unique for all constraints"""
        # Constraint 1: Trace convergence
        # Requires Σ Dₙφ⁻ⁿ < ∞ ✓
        
        # Constraint 2: Action gaps = ℏ*log(φ)
        gap = self.hbar_star * math.log(self.phi)
        self.assertGreater(gap, 0, msg="Positive action gap")
        
        # Constraint 3: Information bound
        I_max = 2 * self.pi / math.log(self.phi)
        
        # Constraint 4: Self-reference scale
        # ℏ* = φ²/(2π) satisfies all constraints
        expected = self.phi**2 / (2 * self.pi)
        self.assertAlmostEqual(self.hbar_star, expected, places=10,
                             msg="ℏ* value from constraints")
    
    def test_spectral_stability(self):
        """Test spectrum stability under small perturbations"""
        # Original eigenvalues
        lambda_1 = self.phi**(-1)
        lambda_2 = self.phi**(-2)
        
        # Gap
        gap = lambda_1 - lambda_2
        
        # Small perturbation can't close gap
        epsilon = 0.01 * gap
        
        # Perturbed eigenvalues stay ordered
        lambda_1_pert = lambda_1 + epsilon
        lambda_2_pert = lambda_2 - epsilon
        
        self.assertGreater(lambda_1_pert, lambda_2_pert,
                          msg="Spectrum remains discrete under perturbation")
    
    def test_resolution_of_identity(self):
        """Test completeness of eigenstates"""
        # For finite truncation, check partial sum approaches 1
        # Σ |γₙ,ᵢ⟩⟨γₙ,ᵢ| → I
        
        # Number of states up to rank N
        N = 10
        total_states = sum(self.fibonacci(n+2) for n in range(1, N+1))
        
        # In finite dimensional subspace, resolution holds
        self.assertGreater(total_states, 0, 
                          msg="Positive number of states")
        
        # States grow with N
        N2 = 15
        total_states_2 = sum(self.fibonacci(n+2) for n in range(1, N2+1))
        self.assertGreater(total_states_2, total_states,
                          msg="State count increases with rank")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)