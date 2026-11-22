# AA Factor Bridge Stage 8 — Nonunit Boundary and Baseline Audit (2026-11-23)

## Aim
Check whether a nontrivial shared divisor between N and an axis b provides an extraction signal. Separate this established GCD mechanism from the Adaptive Address collision-reduction Select mechanism.

## Procedure
Use only N as algorithm input. For each integer axis b from 2 to 512, compute gcd(N,b), stopping on 1 < gcd(N,b) < N. The expected factor values are **not passed to the algorithm**. The same GCD sequence is the baseline; thus no AA-specific advantage can be claimed. This is explicitly a bounded small-divisor probe, not a replacement for AA or a new factorization algorithm.

## Executed Python 3 output
| N | First extracted factor | First axis | GCD evaluations |
|---:|---:|---:|---:|
| 77 | 7 | 7 | 6 |
| 143 | 11 | 11 | 10 |
| 323 | 17 | 17 | 16 |
| 1022117 | none | none | 511 |
| 100160063 | none | none | 511 |
| 2021027 | none | none | 511 |
| 1010707 | 101 | 101 | 100 |

All assertions passed. The identical baseline uses the same number of GCD evaluations in each case.

## Structural interpretation
If gcd(N,b) is a proper divisor, the factor is revealed immediately. When gcd(N,b)=1, the multiplicative-residue relation has many compatible factor pairs; when gcd(N,b)=N, it does not itself isolate a proper factor. These are different observables from the AA integer-identity collision partition. The observed extraction is **not** an AA-specific success: the selected axes were simply tried in ascending order and the procedure is equivalent to bounded small-divisor testing.

## Research boundary
An AA factor bridge requires a new, justified Pick Up/Select rule that predicts discriminating axes from current retained structural information without testing candidate factors in sequence. Its effect must be measured on factor-pair collisions, with no factors seeded into inputs and with all selection and verification work included. This experiment does not establish such a rule, a speedup, or RSA compromise.

## Reproducer
`AA_FACTOR_BRIDGE_STAGE8.py`.
