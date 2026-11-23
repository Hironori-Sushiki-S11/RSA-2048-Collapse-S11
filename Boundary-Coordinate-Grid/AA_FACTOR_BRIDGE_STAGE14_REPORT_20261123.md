# Stage 14 — IKERU TABLE GCD Graph Invariance (2026-11-23)

## Theorem
For fixed distinct coordinates a_i, set x_i(N)=a_i²−N. The identity gcd(|x_i|,|x_j|)=gcd(|a_i²−N|,|a_j²−a_i²|) holds. Let H=lcm_{i<j}|a_j²−a_i²|. Then for any integer k, every pairwise GCD value, hence the entire labeled GCD graph, is unchanged under N→N+kH. Proof: every fixed difference divides H; the first GCD argument is unchanged modulo that difference.

This is an exact result for the **fixed-coordinate** graph, not an impossibility theorem for AA or all adaptive observations.

## Executed Python 3 results
Seven composite N values; 21 coordinates a=ceil(sqrt(N))..+20, held fixed in controls. L=lcm(2..32).

| N | Graph edges | Changed edges N+L | Changed edges N+H | H bits |
|---:|---:|---:|---:|---:|
| 77 | 64 | 1 | 0 | 96 |
| 143 | 47 | 3 | 0 | 103 |
| 323 | 67 | 1 | 0 | 128 |
| 1022117 | 56 | 1 | 0 | 305 |
| 100160063 | 54 | 0 | 0 | 460 |
| 2021027 | 61 | 1 | 0 | 340 |
| 1010707 | 119 | 0 | 0 | 322 |

All assertions passed. No hidden factors were provided and no factor extraction was attempted.

## IKERU TABLE
A (mathematics): derive exact edge-dependence. B (creative exploration): preserve relational-graph ideas while searching for other observables. C (verification): distinguish graph change from factor-pair discrimination. Stopper/tabletop: do not count graph splitting as factor extraction. Gyroscope: revise the observable and require factor-blind Pick Up/Select plus matched baseline and full costs.

## Next Grok request
Use IKERU TABLE to find a factor-relevant observable that is not merely this fixed-coordinate congruence/GCD information. Require mathematical derivation, factor-blind selection, preservation of true solutions, counterexamples, and honest comparison with established algorithms.

## Reproducer
`AA_FACTOR_BRIDGE_STAGE14.py`
