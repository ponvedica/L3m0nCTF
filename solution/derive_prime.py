#!/usr/bin/env python3
"""
Derive the prime modulus P from Shamir shares

In Shamir's Secret Sharing, the prime P must be larger than the secret.
For k=2 scheme: f(x) = a0 + a1*x (mod P)

Given shares (x1, y1), (x2, y2), (x3, y3), we can derive P by:
1. Understanding that P > secret (the flag)
2. Finding P such that the shares satisfy the polynomial
3. Testing candidate primes

This script shows multiple methods to find P.
"""

from sympy import nextprime, isprime
import sys

def method1_brute_force_from_hint(shares):
    """
    Method 1: Consistency testing
    
    Key insight: P must make all shares consistent.
    For k=2: y = a0 + a1*x (mod P)
    
    We test primes and check if all 3 shares are consistent with the same polynomial.
    P should be slightly larger than the secret, but could be smaller than share y-values!
    """
    print("[*] Method 1: Consistency testing")
    print()
    
    x1, y1 = shares[0]
    x2, y2 = shares[1]
    x3, y3 = shares[2]
    
    # The shares y-values give us a rough magnitude
    max_y = max(y1, y2, y3)
    min_y = min(y1, y2, y3)
    
    print(f"[*] Share y-value range:")
    print(f"    Min: {str(min_y)[:50]}...")
    print(f"    Max: {str(max_y)[:50]}...")
    print()
    
    # P could be anywhere from secret size to slightly above max_y
    # Start from a reasonable lower bound (secret is ~50-60 char flag)
    # flag{...} when hex-encoded is huge
    # Try starting just below max_y and working down
    
    candidate = max_y
    if not isprime(candidate):
        # Find nearest prime below
        candidate = candidate - 1
        while not isprime(candidate) and candidate > 2:
            candidate -= 1
    
    tested = 0
    max_tests = 50000
    
    print("[*] Testing candidate primes (working downward from max)...")
    while tested < max_tests and candidate > 1000:
        P = candidate
        
        # Test if shares are consistent with this P
        try:
            # Calculate a1 from shares 1 and 2
            numerator = (y2 - y1) % P
            denominator = (x2 - x1) % P
            
            if denominator == 0:
                # Find next smaller prime
                candidate -= 1
                while not isprime(candidate) and candidate > 1000:
                    candidate -= 1
                tested += 1
                continue
                
            from sympy import mod_inverse
            a1 = (numerator * mod_inverse(denominator, P)) % P
            a0 = (y1 - a1 * x1) % P
            
            # Verify with third share
            y3_calculated = (a0 + a1 * x3) % P
            
            if y3_calculated == y3:
                print(f"\n[+] FOUND PRIME!")
                print(f"[+] P = {P}")
                print(f"[+] Verified with all 3 shares")
                print(f"[+] Tested {tested} candidates")
                return P
                
        except:
            pass
        
        # Find next smaller prime
        candidate -= 1
        while not isprime(candidate) and candidate > 1000:
            candidate -= 1
        tested += 1
        
        if tested % 1000 == 0:
            print(f"    Tested {tested} primes...")
    
    print("[-] Could not find prime in range")
    return None

def method2_mathematical_constraint(shares):
    """
    Method 2: Use mathematical constraints
    
    Given: y1 = a0 + a1*x1 (mod P)
           y2 = a0 + a1*x2 (mod P)
           y3 = a0 + a1*x3 (mod P)
    
    We know: (y2 - y1) = a1*(x2 - x1) (mod P)
    
    This means P divides: [y2 - y1 - a1*(x2 - x1)]
    But we don't know a1...
    
    We can test if a candidate P makes all shares consistent.
    """
    print("[*] Method 2: Mathematical constraint testing")
    print("    (Similar to Method 1, using consistency checks)")
    return method1_brute_force_from_hint(shares)

if __name__ == "__main__":
    print("="*70)
    print("  Prime Derivation for Shamir's Secret Sharing")
    print("  L3MON CTF - HARD MODE")
    print("="*70)
    print()
    
    # You need to have extracted the shares first!
    # Read from metadata (in real challenge, players don't have this)
    import json
    
    try:
        with open("builder_metadata.json", "r") as f:
            meta = json.load(f)
        
        shares = []
        for s in meta["shares"]:
            shares.append((s["x"], int(s["y"])))
        
        print(f"[*] Loaded {len(shares)} shares")
        for i, (x, y) in enumerate(shares, 1):
            print(f"    Share {i}: x={x}, y={str(y)[:40]}...")
        print()
        
        # Try to derive P
        P = method1_brute_force_from_hint(shares)
        
        if P:
            # Verify P is correct
            actual_P = int(meta["prime_P"])
            if P == actual_P:
                print(f"\n{'='*70}")
                print(f"  ✓ SUCCESS! Prime modulus derived correctly")
                print(f"{'='*70}")
                print(f"\nP = {P}")
            else:
                print(f"\n[-] ERROR: Derived P doesn't match actual")
                print(f"    Derived: {P}")
                print(f"    Actual:  {actual_P}")
        
    except FileNotFoundError:
        print("[-] Error: builder_metadata.json not found")
        print("[*] You need to extract shares first!")
        print()
        print("Usage:")
        print("  1. Extract all 3 shares using extract_share*.py scripts")
        print("  2. Format them as: (x, y) tuples")
        print("  3. Modify this script to use your shares")
        print("  4. Run prime derivation")
