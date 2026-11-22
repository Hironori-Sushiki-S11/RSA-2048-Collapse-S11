#!/usr/bin/env python3
"""AA factor-bridge boundary experiment; not a claim of general factoring."""
from math import gcd, lcm

AXES = tuple(range(2, 513))
L = lcm(*AXES)
CASES = [(77, 7, 11), (143, 11, 13), (323, 17, 19),
         (1009 * 1013, 1009, 1013), (10007 * 10009, 10007, 10009)]

def address(x, axes):
    return tuple((x - 1) % b for b in axes)

def aa_identifies(values, axes):
    return len({address(x, axes) for x in values}) == len(values)

def test():
    print("N, unique_addresses, gcd_N_L, nontrivial_factor, expected_p, expected_q")
    for n, p, q in CASES:
        unique = aa_identifies((n - 1, n, n + 1), (2, 3, 5, 7))
        g = gcd(n, L)
        factor = g if 1 < g < n else None
        print(f"{n}, {unique}, {g}, {factor}, {p}, {q}")
        assert p * q == n
        if factor is not None:
            assert n % factor == 0
    print("GCD probe is separate from AA Select; unique Address is not factor recovery.")

if __name__ == "__main__":
    test()
