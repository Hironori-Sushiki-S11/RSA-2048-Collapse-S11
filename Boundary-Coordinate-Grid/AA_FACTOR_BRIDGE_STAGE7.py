#!/usr/bin/env python3
"""Stage 7: sum/difference factor bridge; exact equivalence and cost audit.
This is a Fermat search equivalence check, NOT an AA-specific factorization.
"""
from math import isqrt
CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)

def fermat(n, limit=10000):
    a=isqrt(n)
    if a*a<n: a+=1
    for checks in range(1,limit+1):
        d=a*a-n
        b=isqrt(d)
        if b*b==d and a-b>1:
            return (a-b,a+b),checks,a
        a+=1
    return None,limit,None

def sum_discriminant(n, limit=10000):
    s=2*isqrt(n)
    while s*s<4*n: s+=1
    if s%2: s+=1  # for odd semiprimes, both factors are odd, so S is even
    for checks in range(1,limit+1):
        delta=s*s-4*n
        d=isqrt(delta)
        if d*d==delta and (s-d)%2==0 and (s-d)//2>1:
            return ((s-d)//2,(s+d)//2),checks,s
        s+=2
    return None,limit,None

def run():
    print('N,fermat_checks,sum_checks,factors,verified')
    for n in CASES:
        f,fc,a=fermat(n)
        g,gc,s=sum_discriminant(n)
        assert f==g and f is not None and f[0]*f[1]==n
        assert fc==gc and s==2*a
        print(f'{n},{fc},{gc},{f},True')
    print('PASS: identical candidate sequence and exact-square check count')
if __name__=='__main__':run()
