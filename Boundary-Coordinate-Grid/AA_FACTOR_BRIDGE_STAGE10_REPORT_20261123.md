# AA Factor Bridge Stage 10 — Grok Derived-Corpus Collision Audit (2026-11-23)

## Hypothesis
Generate a corpus from N without factor inputs: C(N)={kN+r | 0<=k<=8, -2<=r<=2}. Apply modular collision observation for axes b=2..512. Test whether high collision counts identify factor-revealing axes without searching factors.

## Mathematical fact
For fixed r, (kN+r) mod b has exact period b/gcd(N,b). This follows because (k+t)N+r ≡ kN+r (mod b) iff b divides tN. Thus a factor-related signature exists, but extracting it by scanning b and computing periods is mathematically linked to gcd(N,b). It is not evidence of a new factorization mechanism.

## Reproduced Python 3 results
| N | Axis with most colliding unordered pairs | Collision pairs | gcd(N, axis) | First proper gcd axis |
|---:|---:|---:|---:|---:|
| 77 | 2 | 484 | 1 | 7 |
| 143 | 2 | 484 | 1 | 11 |
| 323 | 2 | 484 | 1 | 17 |
| 1022117 | 2 | 484 | 1 | none |
| 100160063 | 2 | 484 | 1 | none |
| 2021027 | 2 | 484 | 1 | none |
| 1010707 | 2 | 484 | 1 | 101 |

All seven examples select b=2 under maximum raw collision count, tie-break smaller axis. The chosen axis does not reveal a factor. The first proper gcd axis column is an independent ascending GCD baseline, **not** a discovery by the collision selection rule. Seven-case assertions verify the modular period formula for sample axes.

## Interpretation
This experiment tests Grok's proposed N-derived corpus without feeding known factors into selection. The observed collisions encode divisibility of N by an axis, but naive collision maximization favors the smallest axis, not a factor axis. A distinguishing feature beyond gcd or raw collision count has **not** been demonstrated.

## Next evidence gate
Define a score normalized for axis size and baseline collision rate; prove whether any non-GCD-reducible signal exists before attributing factor extraction to AA. A diagnostic using a true factor as an axis must be explicitly marked oracle-assisted and cannot be counted as factor discovery.

## Reproducer
AA_FACTOR_BRIDGE_STAGE10.py
