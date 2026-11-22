#!/usr/bin/env python3
"""Stage 8: nonunit boundary audit. GCD probing is NOT AA-specific Select."""
from math import gcd
CASES = (77, 143, 323, 1009*1013, 10007*10009, 1009*2003, 101*10007)
AXES = range(2, 513)

def run():
    print('N,first_axis,first_proper_gcd,axes_checked,baseline_axes_checked')
    for n in CASES:
        first = next(((b, gcd(n,b),i) for i,b in enumerate(AXES,1)
                      if 1 < gcd(n,b) < n), None)
        if first:
            b,g,i=first
            assert n%g==0 and g>1
            print(f'{n},{b},{g},{i},{i}')
        else:
            print(f'{n},none,none,511,511')
    print('PASS: deterministic GCD baseline equals this probe by construction.')
if __name__ == '__main__': run()
