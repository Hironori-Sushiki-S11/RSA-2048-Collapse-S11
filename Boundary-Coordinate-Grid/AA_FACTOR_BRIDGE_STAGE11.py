#!/usr/bin/env python3
"""IKERU TABLE: audit what derived-corpus collisions actually measure."""
from math import gcd, lcm
from itertools import combinations
K=range(9)
R=(-2,-1,0,1,2)
CASES=(77,143,323,1009*1013,10007*10009,1009*2003,101*10007)
AXES=range(2,33)
L=lcm(*AXES)

def collision_edges(n,b):
    labels=[(k,r) for k in K for r in R]
    return frozenset((i,j) for i,j in combinations(range(len(labels)),2)
                     if ((labels[i][0]-labels[j][0])*n+labels[i][1]-labels[j][1])%b==0)

def partition(n,axes):
    labels=[(k,r) for k in K for r in R]
    return frozenset((i,j) for i,j in combinations(range(len(labels)),2)
                     if all(((labels[i][0]-labels[j][0])*n+labels[i][1]-labels[j][1])%b==0 for b in axes))

def aa_select_trace(n):
    current=[]
    remaining=set(AXES)
    trace=[]
    while remaining and partition(n,current):
        before=partition(n,current)
        ranked=[]
        for b in remaining:
            after=partition(n,current+[b])
            ranked.append((len(before)-len(after),-b,b))
        gain,_,chosen=max(ranked)
        if gain==0:break
        current.append(chosen)
        remaining.remove(chosen)
        trace.append((chosen,gain,len(partition(n,current))))
    return trace

def run():
    print('axes=2..32, corpus=45 indexed entries, matched N_prime=N+lcm(2..32)')
    print('L=',L)
    print('N,initial_collision_pairs,selected_trace,identical_matched_control')
    for n in CASES:
        m=n+L
        assert all(collision_edges(n,b)==collision_edges(m,b) for b in AXES)
        assert all(gcd(n,b)==gcd(m,b) for b in AXES)
        trace=aa_select_trace(n)
        assert trace==aa_select_trace(m)
        assert partition(n,AXES)==partition(m,AXES)
        print(n,len(partition(n,[])),trace,True,sep=',')
    print('PASS: identical collision graphs, AA reduction traces and gcd signatures for matched controls')
if __name__=='__main__':run()
