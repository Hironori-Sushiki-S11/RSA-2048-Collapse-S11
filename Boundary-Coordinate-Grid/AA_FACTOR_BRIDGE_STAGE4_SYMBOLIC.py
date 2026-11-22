#!/usr/bin/env python3
"""Stage 4: symbolic factor-pair collision states, no candidate factor enumeration.
For prime b: if N mod b != 0 there are b-1 compatible ordered residue pairs;
otherwise there are 2*b-1. CRT counts multiply over distinct prime axes.
"""
from math import gcd, prod
CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)
AXES=(3,5,7,11,13,17,19,23,29,31)
def count_local(n,b):
    return b-1 if n%b else 2*b-1
def test():
    for n in CASES:
        M=1
        states=1
        for b in AXES:
            assert all(b%d for d in range(2,int(b**0.5)+1))
            c=count_local(n,b)
            assert c==sum((u*v-n)%b==0 for u in range(b) for v in range(b))
            M*=b
            states*=c
        assert states>1
        print(f"N={n} modulus={M} symbolic_pair_states={states} gcd_N_modulus={gcd(n,M)} recovered_factor=none")
    print("All checks passed; no integer-factor candidates were enumerated.")
if __name__=="__main__":test()
