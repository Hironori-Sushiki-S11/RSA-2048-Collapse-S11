# Stage 11 — IKERU TABLE Recalibration of Grok's Derived-Corpus Experiment (2026-11-23)

## Conclusion
A derived corpus C(N)={kN+r: k=0..8, r=-2..2} is identifiable with two selected axes for all seven tested N under a true AA collision-reduction score. However, identical AA collision graphs and Select trajectories occur for the matched control N'=N+L, where L=lcm(2..32)=144403552893600. Thus this particular collision observation is periodic in N mod L and cannot, by itself, distinguish N from N' or establish unknown-factor recovery. This does **not** invalidate AA finite-corpus identification.

## IKERU TABLE diagnostic
A: mathematical derivation; B: Grok's derived-corpus hypothesis and relational observables; C: matched controls and evidence boundary. The previous Stage 10's raw-collision-maximizing axis score was not the formal AA Select rule. Stage 11 uses maximum reduction of unresolved pair collisions (tie: smaller axis), with no entropy tie stage; the experiment does not claim to reproduce the entire production AA Select implementation.

## Formal statement
For labels (k_i,r_i), (k_j,r_j), a collision modulo b is equivalent to
b | (k_i-k_j)N+(r_i-r_j).
Therefore for any N' congruent to N modulo b, the entire labeled collision graph modulo b is identical. For all b in a finite axis set B, the full collision graphs and any deterministic Select rule using only these graphs are identical for N' congruent to N modulo L=lcm(B). This is an exact invariance theorem for this chosen corpus and observations, **not** a theorem ruling out factor extraction from every possible N-derived observable.

## Executed Python 3 results
Axes 2..32, 45 indexed corpus entries, 990 initial pair collisions.

| N | Selected axes and remaining collisions | Same as N+L |
|---:|---|---|
| 77 | 30 (15), 7 (0) | yes |
| 143 | 31 (14), 2 (0) | yes |
| 323 | 31 (14), 3 (0) | yes |
| 1022117 | 32 (13), 3 (0) | yes |
| 100160063 | 31 (14), 2 (0) | yes |
| 2021027 | 31 (14), 3 (0) | yes |
| 1010707 | 31 (14), 2 (0) | yes |

All seven controls passed equality of per-axis labeled collision graphs, full partition, GCD signatures and selected-axis traces.

## Scope and next gate
The corpus elements are *known* once N is given; two-axis identification of those elements is not identification of unknown factors. The control N+L need not be semiprime; it is a valid invariance control, not a factorization benchmark. A next candidate must introduce a well-defined observable that escapes this periodic-in-N information bottleneck, and must show how it relates to hidden factor-pair discrimination without supplying p or q. Compare costs and keep the true factor unknown to the algorithm.

## Reproducer
AA_FACTOR_BRIDGE_STAGE11.py
