#!/usr/bin/env python3
"""
Zeckendorf decomposition analysis for c = 299,792,458 m/s
Finds the exact representation as sum of non-consecutive Fibonacci numbers.
"""

def fibonacci_sequence(n):
    """Generate first n Fibonacci numbers"""
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def find_largest_fib_less_than(target, fib_list):
    """Find largest Fibonacci number less than or equal to target"""
    for i in range(len(fib_list) - 1, -1, -1):
        if fib_list[i] <= target:
            return i, fib_list[i]
    return 0, fib_list[0]

def zeckendorf_decomposition(n):
    """Find Zeckendorf representation of n"""
    # Generate enough Fibonacci numbers
    fib = fibonacci_sequence(50)  # Should be enough for our number
    
    decomposition = []
    indices = []
    remaining = n
    last_index = len(fib)  # Start from the end
    
    while remaining > 0:
        # Find largest Fibonacci number ≤ remaining that doesn't break non-consecutive rule
        found = False
        for i in range(min(last_index - 2, len(fib) - 1), -1, -1):  # Skip consecutive numbers
            if fib[i] <= remaining:
                decomposition.append(fib[i])
                indices.append(i + 1)  # Fibonacci indices typically start from F_1
                remaining -= fib[i]
                last_index = i
                found = True
                break
        
        if not found:
            break
    
    return decomposition, indices, remaining

def verify_decomposition(decomposition):
    """Verify that the decomposition sums correctly"""
    return sum(decomposition)

# Analyze c = 299,792,458
c_value = 299792458

print(f"Analyzing Zeckendorf decomposition of c = {c_value:,}")
print("="*60)

# Get Fibonacci sequence up to our target
fib = fibonacci_sequence(50)
print(f"Generated {len(fib)} Fibonacci numbers")
print(f"Largest: F_{len(fib)} = {fib[-1]:,}")

# Find decomposition
decomposition, indices, remainder = zeckendorf_decomposition(c_value)

print(f"\nZeckendorf Decomposition:")
print(f"Number of terms: {len(decomposition)}")
print(f"Remainder: {remainder}")

if remainder == 0:
    print("\nExact decomposition found!")
    total = verify_decomposition(decomposition)
    print(f"Verification: sum = {total:,}")
    print(f"Target:       {c_value:,}")
    print(f"Match: {total == c_value}")
    
    print(f"\nDecomposition as Fibonacci indices:")
    for i, (fib_val, idx) in enumerate(zip(decomposition, indices)):
        print(f"F_{idx:2d} = {fib_val:>12,}")
    
    print(f"\nMathematical representation:")
    print(f"299,792,458 = " + " + ".join([f"F_{idx}" for idx in indices]))
    
    # Analyze patterns
    print(f"\nPattern Analysis:")
    print(f"Indices: {indices}")
    if len(indices) > 1:
        gaps = [indices[i] - indices[i+1] for i in range(len(indices)-1)]
        print(f"Gaps between consecutive indices: {gaps}")
        print(f"Average gap: {sum(gaps)/len(gaps):.2f}")
        print(f"Median gap: {sorted(gaps)[len(gaps)//2]}")
    
    # Connection to electromagnetic structure
    print(f"\nElectromagnetic Structure Analysis:")
    print(f"Number of terms: {len(decomposition)} (related to φ-trace structure)")
    print(f"Largest index: {max(indices)} (related to information content)")
    print(f"Smallest index: {min(indices)} (fundamental scale)")
    
    # Check for patterns related to ranks 6 and 7
    rank_6_related = [idx for idx in indices if idx % 6 == 0 or (idx - 6) % 7 == 0]
    rank_7_related = [idx for idx in indices if idx % 7 == 0 or (idx - 7) % 6 == 0]
    
    print(f"Indices related to rank 6: {rank_6_related}")
    print(f"Indices related to rank 7: {rank_7_related}")
    
else:
    print(f"\nIncomplete decomposition - remainder: {remainder}")
    print("Need larger Fibonacci sequence or algorithm adjustment")

# Additional analysis: connection to golden ratio
phi = (1 + 5**0.5) / 2
print(f"\nGolden Ratio Analysis:")
print(f"φ = {phi:.10f}")

# Express in terms of powers of φ
import math
log_phi = math.log(phi)
log_c = math.log(c_value)
phi_power = log_c / log_phi
print(f"c ≈ φ^{phi_power:.2f}")

# Connection to electromagnetic coupling
alpha = 1/137.035999084
print(f"\nElectromagnetic Connection:")
print(f"c/α = {c_value * alpha:.0f}")
print(f"c·α = {c_value / alpha:.0f}")
print(f"log_φ(c·α) = {math.log(c_value / alpha) / log_phi:.2f}")