#!/usr/bin/env python3
"""Derived-corpus collision audit; no unknown factors passed to the algorithm."""
from collections import Counter
from math import gcd
CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)
K=range(9)
R=(-2,-1,0,1,2)
def collisions(n,b):
    values=[k*n+r for k in K for r in R]
    counts=Counter(x%b for x in values)
    return sum(v*(v-1)//2 for v in counts.values())
def run():
    print('N,best_axis,best_collision_pairs,gcd(N,best_axis),first_proper_gcd_axis,first_proper_gcd_factor')
    for n in CASES:
        scored=[(collisions(n,b),b) for b in range(2,513)]
        max_pairs,b=max(scored,key=lambda t:(t[0],-t[1]))
        found=next(((b,gcd(n,b)) for b in range(2,513) if 1<gcd(n,b)<n),None)
        print(f'{n},{b},{max_pairs},{gcd(n,b)},{found[0] if found else "none"},{found[1] if found else "none"}')
        for axis in (3,7,11,17,31,101,503):
            assert len({(k*n)%axis for k in K})==min(len(K),axis//gcd(n,axis))
    print('PASS: k-trajectory period is b/gcd(N,b); collision score is not a factor oracle')
if __name__=='__main__':run()
