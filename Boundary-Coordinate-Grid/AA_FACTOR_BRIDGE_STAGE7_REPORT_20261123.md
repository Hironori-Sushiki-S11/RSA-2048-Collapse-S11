# AA Factor Bridge Stage 7 — Sum/Difference Coordinate Equivalence (2026-11-23)

## Objective
Investigate an N-derived structural observable linking two unknown factors, without supplying the factors to the algorithm. Determine whether sum/difference coordinates yield independent discrimination or merely reparameterize an existing search.

## Derivation
For odd N=pq with odd p,q, define S=p+q and D=q-p. Then S²-D²=4N, and p=(S-D)/2, q=(S+D)/2. Let S=2a and D=2b: the condition is exactly a²-N=b², the established Fermat difference-of-squares method. The sum-coordinate and Fermat candidates therefore correspond one-to-one.

## Executed test
Python 3, seven semiprime test cases, both methods given the same 10,000-step cap and the same initial candidate. Known factors were not provided to the algorithms; products alone were passed. Both returned identical factors and exact-square-check counts.

| N | Factors | Fermat checks | Sum-coordinate checks |
|---:|---|---:|---:|
| 77 | 7 x 11 | 1 | 1 |
| 143 | 11 x 13 | 1 | 1 |
| 323 | 17 x 19 | 1 | 1 |
| 1022117 | 1009 x 1013 | 1 | 1 |
| 100160063 | 10007 x 10009 | 1 | 1 |
| 2021027 | 1009 x 2003 | 85 | 85 |
| 1010707 | 101 x 10007 | 4049 | 4049 |

All assertions passed in a local Python 3 run. No elapsed-time or memory speedup was measured or claimed.

## Finding
The relation S²-D²=4N is exact and factor-recovering, but in this implementation it is **not an independent observable** beyond Fermat's method. It is a coordinate transformation of the same candidate sequence, with identical exact-square-check counts. Therefore factor extraction here is not evidence of AA-specific factor discovery or AA Select improvement.

## Next evidence gate
A proposed Pick Up observable must show factor-pair discrimination beyond coordinate reparameterization, with explicit collision states, preservation of the correct solution, Select/Address Update, and complete cost accounting against a matched baseline. Do not count changing coordinates as new information.

## Reproducer
`AA_FACTOR_BRIDGE_STAGE7.py`
