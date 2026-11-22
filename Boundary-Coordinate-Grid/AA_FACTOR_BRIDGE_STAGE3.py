#!/usr/bin/env python3
"""Adaptive quadratic-residue prefilter for Fermat candidate a values.
Not an AA-specific factorization theorem or an efficient general factoring method.
"""
from math import isqrt
AXES=tuple(range(3,33))
CASES=((77,7,11),(143,11,13),(323,17,19),(1009*1013,1009,1013),(10007*10009,10007,10009),(1009*2003,1009,2003),(101*10007,101,10007))
WINDOW=6000
def exact(a,n):
    d=a*a-n
    b=isqrt(d)
    return (a-b,a+b) if b*b==d and a-b>1 else None
def run(n):
    a=isqrt(n)
    a+=a*a<n
    initial=list(range(a,a+WINDOW))
    remaining=initial[:]
    unused=list(AXES)
    selected=[]
    evaluations=0
    while unused and remaining:
        scores=[]
        for m in unused:
            squares={v*v%m for v in range(m)}
            survivors=[x for x in remaining if (x*x-n)%m in squares]
            evaluations+=len(remaining)
            scores.append((len(remaining)-len(survivors),-m,m,survivors))
        best=max(scores,key=lambda x:(x[0],x[1]))
        if best[0]==0: break
        selected.append(best[2])
        remaining=best[3]
        unused.remove(best[2])
    def search(candidates):
        for i,x in enumerate(candidates,1):
            ans=exact(x,n)
            if ans: return i,ans
        return len(candidates),None
    bc,ba=search(initial)
    fc,fa=search(remaining)
    return len(remaining),selected,evaluations,bc,fc,ba,fa
if __name__=="__main__":
    for n,p,q in CASES:
        survivors,axes,evals,bc,fc,ba,fa=run(n)
        assert ba==fa==(p,q),(n,ba,fa)
        print(f"N={n} window={WINDOW} survivors={survivors} axes={axes} selection_evals={evals} baseline_exact={bc} filtered_exact={fc} factors={fa}")
