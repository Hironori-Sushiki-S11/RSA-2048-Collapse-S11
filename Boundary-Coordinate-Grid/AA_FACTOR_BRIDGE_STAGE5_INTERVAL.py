#!/usr/bin/env python3
"""Stage 5: interval-boundary ambiguity counts without trial division.
For gcd(N,M)=1 each unit p modulo M has q=N*p^-1 modulo M.
Counts of unit p in an interval use inclusion-exclusion, not factor testing.
"""
from math import gcd, isqrt, prod
from itertools import combinations
AXES=(3,5,7,11,13,17,19,23,29,31)
M=prod(AXES)
CASES=((1009*1013,1009,1013),(10007*10009,10007,10009),
       (1009*2003,1009,2003),(101*10007,101,10007))
def coprime_count(lo,hi):
    if lo>hi: return 0
    total=0
    for k in range(len(AXES)+1):
        for group in combinations(AXES,k):
            d=prod(group)
            total+=(-1)**k*(hi//d-(lo-1)//d)
    return total
def run():
    for n,p,q in CASES:
        assert p*q==n and p<=q and gcd(n,M)==1
        upper=isqrt(n)
        full=coprime_count(2,upper)
        lower=(upper+1)//2
        restricted=coprime_count(lower,upper)
        assert full>=1 and restricted<=full
        print(f'N={n} sqrt_floor={upper} full_interval=[2,{upper}] unit_pair_states={full} '
              f'half_interval=[{lower},{upper}] unit_pair_states={restricted} '
              f'factor_in_half={lower<=p<=upper} factor_recovered=False')
    print('All assertions passed; no candidate factor was enumerated or tested for divisibility.')
if __name__=='__main__':run()
