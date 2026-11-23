#!/usr/bin/env python3
"""Stage 14: fixed-coordinate GCD graph invariance; no factor oracle."""
from math import gcd,isqrt,lcm
from itertools import combinations
CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)
L=lcm(*range(2,33))
def ceil_sqrt(n):
 a=isqrt(n)
 return a+(a*a<n)
def edges(n,coords):
 v=[a*a-n for a in coords]
 return frozenset((i,j) for i,j in combinations(range(len(v)),2) if gcd(abs(v[i]),abs(v[j]))>1)
def run():
 print('N,edges,changed_N_plus_L,changed_N_plus_H,H_bits')
 for n in CASES:
  a=ceil_sqrt(n); coords=list(range(a,a+21))
  H=lcm(*(abs(b*b-a*a) for a,b in combinations(coords,2)))
  base=edges(n,coords); ctrlL=edges(n+L,coords); ctrlH=edges(n+H,coords)
  assert base==ctrlH
  for i,j in combinations(range(len(coords)),2):
   d=abs(coords[j]**2-coords[i]**2)
   assert gcd(abs(coords[i]**2-n),abs(coords[j]**2-n))==gcd(abs(coords[i]**2-n),d)
  print(f'{n},{len(base)},{len(base^ctrlL)},{len(base^ctrlH)},{H.bit_length()}')
 print('PASS: exact GCD identity and H-periodic graph invariance')
if __name__=='__main__':run()
