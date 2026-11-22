# AA Factor Bridge — Modular Pair Ambiguity (2026-11-23)

## Question
Given only a composite integer N=pq, can boundary/residue constraints supply information for an AA-style factor identification process without supplying p and q to the algorithm?

## Method
For each axis b in [2,3,5,7,11,13], enumerate *residue pairs* (r,s) modulo b satisfying r*s = N (mod b). This enumerates at most b^2 local states per axis, **not** integer factor candidates. All six axes are pairwise coprime; the Chinese Remainder Theorem implies that the number of compatible ordered residue pairs modulo L=lcm(2,3,5,7,11,13)=30030 equals the product of the six local counts.

Known p,q are test fixtures used solely for checking that their residue pair satisfies the condition, not as input to the construction.

## Executed results (Python 3)

| N | Compatible ordered residue pairs modulo 30030 |
|---:|---:|
| 77 | 26208 |
| 143 | 25200 |
| 323 | 5760 |
| 1022117 | 5760 |
| 100160063 | 5760 |

All checks passed. The small modulus is a probe, not a huge-integer factorization benchmark.

## Interpretation
- The product congruence provides a computable *factor-pair constraint* derived from N alone.
- It leaves many possible residue pairs. For coprime N and the combined modulus, every unit residue for p yields a matching q residue, which explains the 5760 possibilities.
- Thus ordinary residue constraints do not by themselves isolate unknown factors. No nontrivial factor was recovered.
- The local compatible pairs are not a pre-existing corpus of known integer factors, and their counts must not be described as a successful AA Collision reduction.
- The existing AA residual-difference theorem is for distinguishing known integers; its convergence proof cannot be transferred to unknown factor extraction without a new connection.

## Next structural step
Find an observable computable from N and current retained information that reduces *factor-pair ambiguity* beyond product-congruence compatibility. Explicitly define collision, Pick Up, Select and Address Update for factor-pair states, and test whether selected observables add information rather than merely re-encoding N. Compare with a matched baseline and include all candidate-generation costs.

## Reproducer
`AA_FACTOR_BRIDGE_MODULAR.py` (same directory).
