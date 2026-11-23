# Stage 13 — IKERU TABLE Fixed-Coordinate Control for Grok's GCD Graph (2026-11-23)

## Finding
The large changes in the Stage 12 moving-sqrt-anchor GCD graphs mostly disappear when the observation coordinates a are held fixed. In two of seven test cases the graph becomes identical, and in the other five only 1–3 of 210 possible edges differ. This is a control of observation position, **not** evidence that a hidden factor has been extracted.

## Setup
N is one of seven test composites. L=lcm(2..32)=144403552893600. Let a0=ceil(sqrt(N)). Baseline graph has 21 labeled vertices a=a0,...,a0+20 with values x_a=a²-N, and edge {a,b} iff gcd(|x_a|,|x_b|)>1.

Two controls use N'=N+L:
1. Fixed-coordinate control uses exactly the same a values as baseline.
2. Moving-coordinate control starts at ceil(sqrt(N')), reproducing the Stage 12 observational shift.

No factors are passed to the algorithm; no factor search is performed.

## Executed Python 3 results
| N | Baseline edges | Fixed-control edges | Fixed changed edges | Moving-control edges | Moving changed edges |
|---:|---:|---:|---:|---:|---:|
| 77 | 64 | 63 | 1 | 65 | 17 |
| 143 | 47 | 48 | 3 | 58 | 103 |
| 323 | 67 | 66 | 1 | 72 | 107 |
| 1022117 | 56 | 55 | 1 | 58 | 4 |
| 100160063 | 54 | 54 | 0 | 55 | 15 |
| 2021027 | 61 | 62 | 1 | 62 | 33 |
| 1010707 | 119 | 119 | 0 | 127 | 132 |

PASS: exact pairwise GCD graph comparison. Edges compared by their relative coordinate indices, so the moving-coordinate comparison tests changed observation positions.

## Mathematical interpretation
gcd(a²-N,b²-N)=gcd(a²-N,b²-a²), up to sign. For fixed a,b, the second argument is a fixed integer. Thus the edge condition is controlled by divisibility of a²-N by divisors of b²-a². For N' congruent to N modulo |b²-a²|, the edge is exactly invariant. In particular, if N' congruent to N modulo H=lcm of all nonzero |b²-a²| in the fixed coordinate window, the **entire** fixed-coordinate GCD graph is identical. The L=lcm(2..32) used here is generally not a multiple of H, so some differences are expected. GCD edges alone do not demonstrate factor-pair identification.

## IKERU TABLE assessment
A (mathematics): derive what edges depend on. B (creative hypothesis): retain relational graphs as candidates. C (evidence): separate anchor movement from factor-sensitive structure. Tabletop/stopper: do not claim factor discovery from graph change. Gyroscope/double loop: revise the observation protocol, not merely optimize the previous score.

## Next gate
Test graph signatures against exact periodic controls modulo H where tractable; define a target label for factor-pair discrimination; audit whether any proposed Pick Up/Select rule has information beyond standard GCD/divisibility tests. A true-factor-axis diagnostic is oracle-assisted and must be separate from factor-blind discovery.

## Reproducer
AA_FACTOR_BRIDGE_STAGE13.py
