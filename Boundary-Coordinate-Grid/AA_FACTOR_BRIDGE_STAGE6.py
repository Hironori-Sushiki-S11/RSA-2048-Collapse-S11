#!/usr/bin/env python3
"""Stage 6: exact invertible-residue ambiguity theorem regression.
Only N is used to construct states; expected factors are not supplied.
"""
from math import gcd, prod, isqrt
from itertools import combinations
AXES = (3,5,7,11,13,17,19,23,29,31)
CASES = (77,143,323,1009*1013,10007*10009,1009*2003,101*10007)

def count_coprime_interval(lo,hi,axes):
    result=0
    for k in range(len(axes)+1):
        for subset in combinations(axes,k):
            d=prod(subset)
            result+=(-1)**k*(hi//d-(lo-1)//d)
    return result

def run():
    for n in CASES:
        active=tuple(b for b in AXES if gcd(n,b)==1)
        M=prod(active)
        phi=prod(b-1 for b in active)
        for b in active:
            pairs=sum((u*v-n)%b==0 for u in range(b) for v in range(b))
            assert pairs==b-1
        bound=isqrt(n)
        states=count_coprime_interval(2,bound,active)
        assert states>0
        print(f'N={n} coprime_axes={len(active)} modulus={M} CRT_pair_states={phi} '
              f'bounded_unit_coordinates={states} factor_extracted=False')
    for n in (77,143,323,1009*1013):
        for M in (15,35,77,143):
            if gcd(n,M)!=1: continue
            units=[u for u in range(M) if gcd(u,M)==1]
            pairset={(u,(n*pow(u,-1,M))%M) for u in units}
            assert len(pairset)==len(units)
            assert all(u*v%M==n%M for u,v in pairset)
    print('PASS: exact CRT ambiguity and unit-bijection regression; no factor extraction.')
if __name__=='__main__':run()
