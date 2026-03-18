#!/usr/bin/env python3
"""
Reconstruct the secret flag using Shamir's Secret Sharing
Requires: 2 shares (out of 3) and the prime modulus P

Supports format: "x, y" or "SHARE: x, y"
"""
from sympy import mod_inverse
import sys
import re

def parse_share(share_str):
    """Parse share string in format 'x, y' or 'SHARE: x, y'"""
    share_str = share_str.strip()
    
    # Remove "SHARE:" prefix if present
    if share_str.upper().startswith("SHARE:"):
        share_str = share_str[6:].strip()
    
    # Split by comma
    parts = [p.strip() for p in share_str.split(',')]
    if len(parts) != 2:
        raise ValueError(f"Invalid share format: {share_str}")
    
    x = int(parts[0])
    y = int(parts[1])
    return x, y

def reconstruct_secret(share1_str, share2_str, prime_str):
    """
    Reconstruct secret using Shamir's Secret Sharing
    
    For k=2 threshold scheme:
    f(x) = a0 + a1*x (mod P)
    where a0 is the secret
    
    Given two points (x1, y1) and (x2, y2):
    Using Lagrange interpolation at x=0:
    secret = (y1*x2 - y2*x1) / (x2 - x1) (mod P)
    """
    # Parse inputs
    x1, y1 = parse_share(share1_str)
    x2, y2 = parse_share(share2_str)
    P = int(prime_str.strip())
    
    print(f"[*] Share 1: x={x1}")
    print(f"[*] Share 2: x={x2}")
    print(f"[*] Prime P: {P}")
    print(f"[*] Reconstructing secret using Lagrange interpolation...")
    
    # Lagrange interpolation at x=0
    numerator = (y1 * x2 - y2 * x1) % P
    denominator = (x2 - x1) % P
    
    secret_int = (numerator * mod_inverse(denominator, P)) % P
    
    print(f"[*] Secret (integer): {secret_int}")
    
    # Convert integer to hex then to ASCII
    hex_str = hex(secret_int)[2:]
    if len(hex_str) % 2:
        hex_str = "0" + hex_str
    
    try:
        flag = bytes.fromhex(hex_str).decode('utf-8')
        print(f"\n[+] FLAG: {flag}")
        return flag
    except (ValueError, UnicodeDecodeError) as e:
        print(f"[-] Failed to decode secret as text: {e}")
        print(f"[*] Hex: {hex_str}")
        return None

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        # Command-line arguments: share1 share2 prime
        share1 = sys.argv[1]
        share2 = sys.argv[2]
        prime = sys.argv[3]
        reconstruct_secret(share1, share2, prime)
    else:
        # Interactive mode
        print("=== Shamir Secret Reconstruction ===")
        print()
        share1 = input("Enter Share #1 (format 'x, y'): ")
        share2 = input("Enter Share #2 (format 'x, y'): ")
        prime = input("Enter Prime P: ")
        print()
        reconstruct_secret(share1, share2, prime)
