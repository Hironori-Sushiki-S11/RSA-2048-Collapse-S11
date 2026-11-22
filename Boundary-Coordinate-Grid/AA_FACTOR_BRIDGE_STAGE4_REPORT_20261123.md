# AA Factor Bridge Stage 4 — Symbolic Collision-State Growth (2026-11-23)

## Objective
Test whether factor-pair residue constraints from N alone can be retained **symbolically** without enumerating a window of candidate integer factors, and whether expanding the axes makes unknown factors uniquely identifiable.

## Method
For distinct prime axes b=3,5,7,11,13,17,19,23,29,31, retain only the count of ordered residue pairs (u,v) with uv=N (mod b). Exact local count is b-1 if b does not divide N, otherwise 2b-1. By CRT, the total count of compatible ordered residue pairs modulo M=product(b) is the product of local counts. No factor candidates or CRT pair states are enumerated. Local counts are cross-checked by exhaustive b² *residue-pair* validation, not integer factor trial division. GCD(N,M) is printed only as a separate diagnostic.

## Executed outcome
The program was run in Python 3 with seven test composites, and all local-count assertions passed. Every case retained multiple compatible residue-pair states and **no factors were extracted**. Run the companion script to obtain exact large integer counts and diagnostics.

## Structural finding
This is a precise Blind Spot: adding product-congruence axes grows the modulus but does not in itself identify the unknown factors. For gcd(N,M)=1, every invertible residue u mod M corresponds to exactly one v=N*u^{-1} mod M; hence the compatible ordered residue-pair count is phi(M), not one. An axis can refine known *integer identities* while still failing to reduce *factor-pair uncertainty*. Thus the prior AA finite-corpus collision reduction cannot simply be reused as a factor-candidate reduction theorem.

## Interpretation and next step
The symbolic state is a useful compact representation of ambiguity, not a factorization result or a security claim. The next needed observable must introduce independently useful restrictions (for example magnitude/interval or cross-factor structure) that are not simply repetitions of pq=N modulo more axes, and its information gain and computation cost must be measured. A new collision definition over *factor-pair states* is required before calling the process AA Select. Do not seed p,q or substitute a large candidate scan.

Reproducer: `AA_FACTOR_BRIDGE_STAGE4_SYMBOLIC.py`.
