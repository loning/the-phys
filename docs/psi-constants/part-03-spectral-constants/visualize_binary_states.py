#!/usr/bin/env python3
"""
Visualize all 34 binary states of Layer 7 and their phase distribution
Shows how the no-11 constraint creates the Fibonacci structure
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_no_11_strings(n):
    """Generate all n-bit strings with no consecutive 1s"""
    strings = []
    
    def build(current, remaining):
        if remaining == 0:
            strings.append(current)
            return
        
        # Can always add 0
        build(current + '0', remaining - 1)
        
        # Can only add 1 if last bit wasn't 1
        if not current or current[-1] == '0':
            build(current + '1', remaining - 1)
    
    build('', n)
    return sorted(strings)  # Sort for consistent ordering

def binary_to_phase(binary_string):
    """Convert binary string to phase angle"""
    n = len(binary_string)
    if n == 0:
        return 0
    value = int(binary_string, 2)
    return 2 * np.pi * value / (2**n)

def main():
    # Generate all Layer 7 states
    layer7_states = generate_no_11_strings(7)
    
    print("="*70)
    print("All 34 Binary States of Layer 7 (No Consecutive 1s)")
    print("="*70)
    
    # Calculate phases and display all states
    phases = []
    for i, state in enumerate(layer7_states):
        value = int(state, 2)
        phase_rad = binary_to_phase(state)
        phase_deg = np.degrees(phase_rad)
        phases.append(phase_rad)
        
        print(f"{i+1:2d}. {state} = {value:3d} → {phase_rad:6.4f} rad = {phase_deg:6.2f}°")
    
    print(f"\nTotal: {len(layer7_states)} states = F_9 = 34")
    
    # Golden ratio calculations
    phi = (1 + np.sqrt(5)) / 2
    golden_angle = np.pi / phi
    golden_complement = 2 * np.pi / phi
    
    print(f"\n=== Special Angles ===")
    print(f"Golden angle: π/φ = {golden_angle:.4f} rad = {np.degrees(golden_angle):.1f}°")
    print(f"Complement: 2π/φ = {golden_complement:.4f} rad = {np.degrees(golden_complement):.1f}°")
    print(f"Sum: {np.degrees(golden_angle + golden_complement):.1f}°")
    
    # Create phase wheel visualization
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, projection='polar')
    
    # Plot all states
    for i, (state, phase) in enumerate(zip(layer7_states, phases)):
        r = 0.9
        ax.plot([phase, phase], [0, r], 'b-', alpha=0.3)
        ax.plot(phase, r, 'bo', markersize=8)
        
        # Label some states
        if i % 5 == 0 or state == '1010101':  # Label every 5th and the last
            ax.text(phase, r + 0.1, state, ha='center', va='center', fontsize=8)
    
    # Mark golden angles
    ax.plot([golden_angle, golden_angle], [0, 1], 'r-', linewidth=2, label='π/φ')
    ax.plot([golden_complement, golden_complement], [0, 1], 'g-', linewidth=2, label='2π/φ')
    
    ax.set_ylim(0, 1.2)
    ax.set_title('Layer 7: Phase Distribution of 34 Binary States\n(No Consecutive 1s)', 
                 fontsize=14, pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
    plt.tight_layout()
    plt.savefig('layer7_phase_wheel.png', dpi=150, bbox_inches='tight')
    print("\nPhase wheel saved as 'layer7_phase_wheel.png'")
    
    # Analyze phase differences
    print("\n=== Phase Difference Analysis ===")
    
    # Count phase differences near golden angle
    tolerance = 0.1  # radians
    golden_resonances = 0
    
    for i in range(len(phases)):
        for j in range(i+1, len(phases)):
            diff = abs(phases[j] - phases[i])
            # Check both difference and 2π - difference
            if abs(diff - golden_angle) < tolerance or abs(2*np.pi - diff - golden_angle) < tolerance:
                golden_resonances += 1
    
    total_pairs = len(phases) * (len(phases) - 1) // 2
    print(f"Total phase pairs: {total_pairs}")
    print(f"Pairs near golden angle (±{tolerance} rad): {golden_resonances}")
    print(f"Fraction: {golden_resonances/total_pairs:.3f}")
    
    # Channel calculation demonstration
    print("\n=== Channel Calculation ===")
    F6, F7, F8, F9, F10 = 8, 13, 21, 34, 55
    
    print(f"F_6 = {F6} (states in Layer 4)")
    print(f"F_8 = {F8} (states in Layer 6)")
    print(f"F_9 = {F9} (states in Layer 7)")
    print(f"F_10 = {F10} (states in Layer 8)")
    
    channels = F9 + F8 - F6
    print(f"\nEffective channels = F_9 + F_8 - F_6")
    print(f"                   = {F9} + {F8} - {F6}")
    print(f"                   = {channels}")
    
    alt_channels = F10 - F6
    print(f"\nAlternative: F_10 - F_6 = {F10} - {F6} = {alt_channels}")
    print(f"Both give: {channels}")

if __name__ == "__main__":
    main()