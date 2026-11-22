# AA Factor Bridge Stage 5 — Interval Boundary and Symbolic Ambiguity (2026-11-23)

## Purpose
Examine whether a magnitude boundary derived from N alone reduces the number of possible factor-coordinate states without enumerating candidate integer factors or performing trial division.

## Method
For N=pq, the smaller nontrivial factor must satisfy 2 <= p <= floor(sqrt(N)). Let M be the product of prime axes [3,5,7,11,13,17,19,23,29,31]. For the four test N, gcd(N,M)=1. Any integer p coprime to M determines one compatible residue for q modulo M via q=N*p^{-1} mod M. Count p coordinates in an interval coprime to M using exact inclusion-exclusion over 2^10 subsets, not enumerating candidate p or testing p|N.

Compare the guaranteed full interval [2,floor(sqrt(N))] with a narrower illustrative interval [ceil(floor(sqrt(N))/2),floor(sqrt(N))]. The latter is **not guaranteed to retain the actual factor**.

## Executed Python 3 output

| N | Full interval unit coordinates | Half interval unit coordinates | True smaller factor in half interval? |
|---:|---:|---:|:---:|
| 1022117 | 321 | 159 | yes |
| 100160063 | 3043 | 1519 | yes |
| 2021027 | 443 | 214 | yes |
| 1010707 | 319 | 158 | no |

All assertions passed. The true factors appear in the test fixtures solely to check the interval-preservation condition, not in the counting algorithm.

## Interpretation
- A magnitude boundary can reduce the count of *potential residue-compatible factor coordinates* without trial division.
- These counts are not the number of actual divisors and do not prove AA factor collision reduction.
- A narrower interval may discard the correct factor, as N=1010707 demonstrates.
- The guaranteed interval still retains many coordinates. No factors were recovered and no new independent factor-identifying observable was found.
- This stage is a structural boundary probe, not an implementation of the established AA residual-difference Select or a claim of RSA compromise.

## Next
Construct an N-derived, correctness-preserving observable that discriminates candidate factor-pair states, explicitly quantify its information gain and cost, and compare with a matched baseline. Do not use the true p,q in Pick Up or Select, and do not quietly replace the AA problem with sequential factor testing.

Reproducer: `AA_FACTOR_BRIDGE_STAGE5_INTERVAL.py`.
