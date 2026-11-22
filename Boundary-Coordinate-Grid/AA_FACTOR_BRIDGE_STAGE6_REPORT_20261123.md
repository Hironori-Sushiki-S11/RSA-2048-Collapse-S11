# AA Factor Bridge Stage 6 — Invertible Residue Ambiguity (2026-11-23)

## Question
Can adding further product-congruence axes alone identify unknown factors of N, without factor enumeration?

## Exact result
Let M be a positive integer with gcd(N,M)=1. For each unit residue u modulo M, there is **exactly one** unit residue v=N*u^{-1} (mod M) satisfying uv=N (mod M). Hence the set of ordered compatible unit residue pairs has size phi(M). This is a bijection, not a reduction to one factor pair. For pairwise-coprime prime axes the count is product(b-1).

This is a statement about product-congruence residue states, **not** a no-go theorem for all AA observables or all factorization algorithms.

## Executed tests
Python 3, script `AA_FACTOR_BRIDGE_STAGE6.py`. Seven composites tested; local pair counts checked exhaustively for each selected prime modulus; a unit-bijection property checked on small composite moduli. All assertions passed.

| N | Axes coprime to N | Symbolic unit residue pairs | Coprime integer coordinates in [2,floor(sqrt(N))] |
|---:|---:|---:|---:|
| 77 | 8 | 510935040 | 4 |
| 143 | 8 | 255467520 | 4 |
| 323 | 8 | 106444800 | 5 |
| 1022117 | 10 | 30656102400 | 321 |
| 100160063 | 10 | 30656102400 | 3043 |
| 2021027 | 10 | 30656102400 | 443 |
| 1010707 | 10 | 30656102400 | 319 |

For cases where some original axes divide N, the reported unit-state count is restricted to the **subset of axes coprime to N**, not all axes. gcd(N,b)>1 is separately a factor-revealing possibility and must not be hidden.

## Implication for AA bridge
Product-congruence axes increase the modulus and encode factor-pair compatibility but cannot by themselves select the actual factor residue. In particular, an integer Address partition theorem over a known finite corpus does not automatically become a factor-identification theorem. Stage 5's interval boundary constrains magnitudes but cannot safely shrink to an arbitrary half-interval.

## Next experimental gate
Define an N-derived observable that separates possible *integer factor pairs* while preserving the actual pair, without supplying factors or scanning a preset factor list. Require a formally stated collision relation, Pick Up, Select, Address Update, and total-work comparison against a same-environment baseline. No nontrivial factors were recovered in this stage; no RSA break or runtime advantage is claimed.

## Reproducer
`AA_FACTOR_BRIDGE_STAGE6.py`
