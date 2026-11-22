#!/usr/bin/env python3
"""Stage 9: audit of product-congruence information, not a factorization algorithm."""
from math import gcd, prod
AXES=(3,5,7,11,13)
M=prod(AXES)
CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)

def run():
    phi=sum(gcd(u,M)==1 for u in range(M))
    assert phi==5760
    for n in CASES:
        g=gcd(n,M)
        if g!=1:
            status='proper factor' if 1<g<n else 'whole N, no proper factor'
            print(f'N={n}, gcd(N,M)={g}, nonunit boundary, {status}')
            continue
        units=[u for u in range(M) if gcd(u,M)==1]
        pair_count=sum((u*(n*pow(u,-1,M)))%M==n%M for u in units)
        assert pair_count==phi
        print(f'N={n}, gcd(N,M)=1, compatible_pairs={pair_count}, extracted_factor=none')
    print('PASS: congruence ambiguity confirmed; no AA factor extraction established')
if __name__=='__main__':run()
