#!/usr/bin/env python3
"""AA factor bridge: modular residue-pair ambiguity from N alone.
This does NOT factor N or implement AA factor-candidate Select.
"""
from math import gcd, lcm, prod

CASES = [(77, 7, 11), (143, 11, 13), (323, 17, 19),
         (1009*1013, 1009, 1013), (10007*10009, 10007, 10009)]
AXES = (2, 3, 5, 7, 11, 13)

def residue_pairs(n, modulus):
    return [(r, s) for r in range(modulus) for s in range(modulus)
            if (r*s-n) % modulus == 0]

def run():
    print("N,axis,compatible_pairs,unique_factor_residue_pair")
    for n, p, q in CASES:
        assert p*q == n  # test fixture only; not used for candidate generation
        for b in AXES:
            pairs = residue_pairs(n, b)
            assert (p % b, q % b) in pairs
            print(f"{n},{b},{len(pairs)},{len(pairs)==1}")
        modulus = lcm(*AXES)
        # CRT applies because the axes are pairwise coprime.
        count = prod(len(residue_pairs(n, b)) for b in AXES)
        print(f"{n},combined_modulus,{modulus},compatible_residue_pairs,{count},gcd_N_M,{gcd(n,modulus)}")

if __name__ == "__main__":
    run()
