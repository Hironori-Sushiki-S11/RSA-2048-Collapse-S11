# AA Factor Bridge Stage 9 — Information-Gain Gate (2026-11-23)

## Objective
Determine whether adding product-congruence axes provides actual information about which unknown factor pair is correct, rather than merely providing a larger Address representation.

## Mathematical observation
Let M be the product of axes 3,5,7,11,13 (=15015). When gcd(N,M)=1, each unit u modulo M has exactly one compatible v=N*u^(-1) mod M. There are phi(M)=5760 ordered compatible residue pairs. The product relation alone does not identify which one corresponds to actual integer factors. This is a restricted observation about modular product information, not a theorem excluding all AA factor extraction.

When gcd(N,M)>1, gcd may equal a proper factor or all of N; the latter is not an extraction.

## Executed Python 3 results

| N | gcd(N,M) | Compatible unit pairs if coprime | Extracted proper factor |
|---:|---:|---:|---|
| 77 | 77 | n/a | no |
| 143 | 143 | n/a | no |
| 323 | 1 | 5760 | no |
| 1022117 | 1 | 5760 | no |
| 100160063 | 1 | 5760 | no |
| 2021027 | 1 | 5760 | no |
| 1010707 | 1 | 5760 | no |

The reproducible script completed with all assertions passing. This counts modular pair states, **not actual integer factor pairs**. The local script was executed before publication.

## Evidence gate for future AA factor bridge
Before calling a procedure an AA-based factor extraction, require:
1. A collision state representing ambiguity between **unknown factor-pair solutions**, not simply a known-integer corpus.
2. A new observable derived from N and retained information, with a correctness-preserving elimination rule.
3. A Pick Up/Select/Address Update that demonstrates measurable reduction in that ambiguity.
4. Extraction verified by p*q=N, without p or q seeded in the algorithm.
5. Same-environment comparison including axis-selection, candidate generation, verification, time, and memory.

Stages 3 and 7 recovered small factors via established Fermat-type searches; stage 8 used bounded GCD probing. These are not evidence that AA uniquely extracts factors. Earlier AA finite-corpus identification results remain separate and are not invalidated.

## Next step
Research a factor-pair-specific observable with a provable nonzero information gain beyond pq=N modulo additional axes. Do not continue numbering repeated restatements as independent factorization breakthroughs.

Reproducer: `AA_FACTOR_BRIDGE_STAGE9.py`.
