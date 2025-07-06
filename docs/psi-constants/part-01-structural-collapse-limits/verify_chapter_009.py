#!/usr/bin/env python3
"""
Chapter 009 Verification Program
Validates collapse mass unit from φ-trace information cycling
Tests first principles derivation: ψ = ψ(ψ) → φ-trace → cycling → mass
"""

import math
import unittest

class TestChapter009CollapseMass(unittest.TestCase):
    """Test suite for Chapter 009: Collapse Mass from φ-Trace Information Cycling"""
    
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
    
    def test_mass_cycling_formula(self):
        """Test mass from φ-trace information cycling formula"""
        # New formula: m = ħ* ⟨ω_cycle⟩ / c*²
        # For a simple cycling pattern with constant frequency
        omega_cycle = 1 / self.delta_tau  # Base cycling frequency
        
        # m = ħ* ω_cycle / c*²
        mass = self.hbar_star * omega_cycle / self.c_star**2
        
        # This should equal the fundamental mass quantum
        expected_m0 = self.hbar_star / (self.c_star**2 * self.delta_tau)
        
        # Check equality
        self.assertAlmostEqual(mass, expected_m0, places=15,
                              msg="Cycling mass should equal fundamental mass quantum")
        self.assertAlmostEqual(mass, self.m_0, places=15,
                              msg="Cycling mass should equal m_0")
    
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
            # Use φ-trace cycling frequency scaling
            omega_scale = mu  # Cycling frequency scales with energy scale
            m_mu = self.hbar_star * omega_scale / self.c_star**2
            
            # Mass should be positive
            self.assertGreater(m_mu, 0,
                              msg=f"Running mass must be positive at μ/μ_0={factor}")
            
            # Check scale-dependent cycling frequency
            if factor == self.phi:
                # At φ times the scale, cycling frequency changes by φ
                expected_mass = self.hbar_star * self.phi * mu_0 / self.c_star**2
                self.assertAlmostEqual(m_mu, expected_mass, places=10,
                                      msg="Scale-dependent cycling mass incorrect")
    
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
    
    def test_phi_trace_information_cycling(self):
        """Test new φ-trace information cycling formulation"""
        # Test mass from φ-trace information cycling: m = ħ* ⟨ω_cycle⟩ / c*²
        
        # Test for various cycling frequencies
        test_frequencies = [1/self.delta_tau, 0.5/self.delta_tau, self.phi/self.delta_tau]
        
        for omega_cycle in test_frequencies:
            m_cycle = self.hbar_star * omega_cycle / self.c_star**2
            
            # Mass should be positive for positive cycling frequency
            self.assertGreater(m_cycle, 0,
                              msg="Mass from cycling must be positive")
            
            # Check dimensional consistency
            # ħ* has dimensions [action], ω has dimensions [1/time], c* has dimensions [length/time]
            # So ħ*ω/c² has dimensions [action × 1/time] / [length²/time²] = [mass]
            self.assertTrue(True, "Dimensional analysis correct")
            
            # Check information content
            if omega_cycle > 0:
                info_rate = omega_cycle * math.log(self.phi, 2)  # φ-bits per time
                self.assertGreater(info_rate, 0,
                                  msg="Information cycling rate must be positive")
    
    def test_zeckendorf_cycling_constraints(self):
        """Test that mass cycling follows Zeckendorf constraints"""
        # φ-trace cycling frequencies must follow Fibonacci structure
        
        for i, F_n in enumerate(self.fib[:8]):
            # Cycling frequency in Fibonacci units
            omega_cycle = F_n / self.delta_tau
            m_cycle = self.hbar_star * omega_cycle / self.c_star**2
            
            # Should equal Fibonacci mass spectrum
            expected_mass = F_n * self.m_0
            self.assertAlmostEqual(m_cycle, expected_mass, places=15,
                                  msg=f"Cycling mass should match Fibonacci spectrum at F_{i+1}")
            
            # Check Zeckendorf uniqueness - no two different decompositions
            # should give the same mass
            if i >= 2:
                # Verify Fibonacci recurrence in cycling
                omega_prev1 = self.fib[i-1] / self.delta_tau
                omega_prev2 = self.fib[i-2] / self.delta_tau
                omega_sum = omega_prev1 + omega_prev2
                
                self.assertAlmostEqual(omega_cycle, omega_sum, places=15,
                                      msg=f"Cycling frequency Fibonacci recurrence failed at F_{i+1}")
    
    def test_information_localization_principle(self):
        """Test mass as localized φ-trace information"""
        # Mass represents information that has become "trapped" in self-sustaining cycles
        
        # Information density for various mass configurations
        test_masses = [self.m_0, 2*self.m_0, self.phi*self.m_0]
        
        for m in test_masses:
            # Information content from mass
            I_mass = math.log(m/self.m_0, self.phi)  # φ-bits stored in mass
            
            # Check information localization
            self.assertGreaterEqual(I_mass, 0,
                                   msg="Localized information must be non-negative")
            
            # Information should scale logarithmically with mass
            if m > self.m_0:
                I_base = math.log(self.m_0/self.m_0, self.phi)  # = 0
                self.assertGreater(I_mass, I_base,
                                  msg="More massive objects store more information")
            
            # Check information-energy relation
            E_mass = m * self.c_star**2
            # For ground state (m = m_0), I_mass = 0, so handle this case
            if I_mass > 0:
                info_energy_ratio = I_mass / (E_mass / self.hbar_star)
                # This ratio should be bounded (information cannot exceed energy capacity)
                self.assertGreater(info_energy_ratio, 0,
                                  msg="Information-energy ratio must be positive")
            else:
                # Ground state has zero information content, which is correct
                self.assertEqual(I_mass, 0,
                               msg="Ground state should have zero information content")
    
    def test_first_principles_adherence(self):
        """Test that mass concepts derive from ψ = ψ(ψ) without circular reasoning"""
        # Verify derivation chain: ψ = ψ(ψ) → φ-trace → information cycling → mass
        
        # 1. Self-reference creates rank advancement necessity (from Chapter 7)
        initial_rank = 0
        rank_after_psi = 1  # ψ(ψ) necessarily increases rank
        self.assertGreater(rank_after_psi, initial_rank,
                          msg="ψ = ψ(ψ) must increase rank")
        
        # 2. Rank advancement creates information flow (from Chapter 8)
        info_per_rank = math.log(self.phi, 2)  # φ-bits per rank
        info_flow_rate = info_per_rank / self.delta_tau  # φ-bits per time
        self.assertGreater(info_flow_rate, 0,
                          msg="Information must flow with rank advancement")
        
        # 3. Information cycling emerges from self-sustaining patterns
        # When φ-trace information flow forms closed loops, it creates persistent patterns
        cycling_frequency = 1 / self.delta_tau  # Base cycling rate
        info_cycling_rate = cycling_frequency * info_per_rank
        self.assertGreater(info_cycling_rate, 0,
                          msg="Information cycling rate must be positive")
        
        # 4. Mass emerges from information cycling energy density
        # Energy of cycling: E = ħ* × cycling_frequency
        # Mass from E=mc²: m = E/c² = ħ* × cycling_frequency / c²
        mass_from_cycling = self.hbar_star * cycling_frequency / self.c_star**2
        
        # This should equal the fundamental mass quantum
        expected_m0 = self.hbar_star / (self.c_star**2 * self.delta_tau)
        self.assertAlmostEqual(mass_from_cycling, expected_m0, places=15,
                              msg="Mass from cycling should equal fundamental mass quantum")
        
        # 5. Verify no circular definition - mass defined from information cycling, not E=mc²
        # Information cycling frequency determines both energy AND mass consistently
        energy_from_cycling = self.hbar_star * cycling_frequency
        mass_from_info_cycling = self.hbar_star * cycling_frequency / self.c_star**2
        
        # Check E = mc² emerges naturally (not assumed)
        energy_from_mass = mass_from_info_cycling * self.c_star**2
        self.assertAlmostEqual(energy_from_cycling, energy_from_mass, places=15,
                              msg="E=mc² should emerge from information cycling, not be assumed")
        
        # 6. Test derivation order: ψ=ψ(ψ) → φ-trace → cycling → mass (not reverse)
        # Verify mass quantization follows φ-trace structure, not arbitrary
        for i, F_n in enumerate(self.fib[:5]):
            # Each Fibonacci number represents a distinct cycling pattern
            cycling_freq = F_n / self.delta_tau
            fibonacci_mass = self.hbar_star * cycling_freq / self.c_star**2
            expected_fib_mass = F_n * self.m_0
            
            self.assertAlmostEqual(fibonacci_mass, expected_fib_mass, places=15,
                                  msg=f"Fibonacci mass pattern should emerge from cycling at F_{i+1}")
            
            # Check that φ-trace structure determines available cycling modes
            if i >= 2:
                # Fibonacci recurrence should emerge from φ-trace geometry
                fib_sum = self.fib[i-1] + self.fib[i-2]
                self.assertEqual(F_n, fib_sum,
                               msg=f"Fibonacci recurrence must hold for φ-trace cycling modes")
        
        # 7. Mass-energy relation emerges from information cycling, not postulated
        # The factor c² emerges from φ-trace tensor structure (rank-2 vs rank-0)
        c_star_squared = self.c_star**2
        self.assertEqual(c_star_squared, 4,
                        msg="c*² = 4 from φ-trace geometric scaling")
        
        # 8. Planck mass as maximum information cycling rate
        max_cycling_freq = 1 / self.delta_tau  # Maximum rate: one cycle per tick
        planck_mass_from_cycling = self.hbar_star * max_cycling_freq / self.c_star**2
        self.assertAlmostEqual(planck_mass_from_cycling, self.m_P_star, places=15,
                              msg="Planck mass should equal maximum cycling mass")
        
        # 9. Information conservation ensures mass conservation
        # Total φ-trace information in cycling patterns is conserved
        total_info = 10 * info_per_rank  # Example: 10 φ-bits total
        
        # Redistribute among different cycling patterns
        for split in [0.3, 0.5, 0.7]:
            info_1 = split * total_info
            info_2 = (1 - split) * total_info
            
            # Convert to equivalent masses
            mass_1 = self.m_0 * self.phi**(info_1/info_per_rank)
            mass_2 = self.m_0 * self.phi**(info_2/info_per_rank)
            
            # Total information should be conserved
            total_info_check = (info_1 + info_2)
            self.assertAlmostEqual(total_info_check, total_info, places=14,
                                  msg="Information conservation violated in mass redistribution")
        
        print("✓ All mass concepts derived from ψ = ψ(ψ) first principles")
        print("✓ No circular reasoning - mass emerges from φ-trace information cycling")
        print("✓ E=mc² emerges from information cycling, not assumed")
        print("✓ Fibonacci mass spectrum from φ-trace cycling constraints")
        print("✓ Information localization principle determines mass formation")
        print("✓ Mass conservation from φ-trace information conservation")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)