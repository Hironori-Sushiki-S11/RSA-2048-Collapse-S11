#!/usr/bin/env python3
"""Stage 13: controlled GCD-graph comparison for N and N+L.
No factor inputs; fixed a-coordinates vs moving sqrt(N) coordinates.
"""
from math import gcd,lcm,isqrt
from itertools import combinations

CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)
L=lcm(*range(2,33))
def ceil_sqrt(n):
    a=isqrt(n)
    return a+(a*a<n)
def graph(n, coordinates):
    values=[a*a-n for a in coordinates]
    return {(i,j) for i,j in combinations(range(len(values)),2)
            if gcd(abs(values[i]),abs(values[j]))>1}
def run():
    print('L',L)
    print('N,base_edges,fixed_control_edges,fixed_changed,moving_control_edges,moving_changed')
    for n in CASES:
        start=ceil_sqrt(n)
        fixed=range(start,start+21)
        base=graph(n,fixed)
        fixed_control=graph(n+L,fixed)
        moving_control=graph(n+L,range(ceil_sqrt(n+L),ceil_sqrt(n+L)+21))
        print(n,len(base),len(fixed_control),len(base^fixed_control),
              len(moving_control),len(base^moving_control),sep=',')
        assert len(base)<=210 and len(fixed_control)<=210
    print('PASS: exact pairwise GCD graph comparison')
if __name__=='__main__':run()
