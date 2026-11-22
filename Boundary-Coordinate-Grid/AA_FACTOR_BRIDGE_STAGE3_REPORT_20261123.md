# AA Factor Bridge Stage 3 — Adaptive Quadratic-Residue Filtering (2026-11-23)

## Goal and method
Starting only from N, use Fermat's established identity N=(a-b)(a+b) and a²-N=b². Define 6000 candidate a values from ceil(sqrt(N)). For each axis m=3..32, reject a when (a²-N) mod m is not a quadratic residue. Pick the axis that removes the most current candidates (tie: smaller m); update survivors; repeat until no improvement. Compare exact square checks with plain Fermat on the **same ordered window**. Known p,q are assertion fixtures only.

This is **AA-style Select**, not an implementation or proof of the AA residual-difference collision theorem. It is a bounded Fermat candidate enumeration, not a non-enumerative factor extraction.

## Executed Python 3 results

| N | Extracted factors | Window | Survivors | Baseline exact checks | Filtered exact checks | Selection candidate evaluations |
|---:|---|---:|---:|---:|---:|---:|
| 77 | 7 × 11 | 6000 | 2 | 1 | 1 | 206941 |
| 143 | 11 × 13 | 6000 | 3 | 1 | 1 | 204048 |
| 323 | 17 × 19 | 6000 | 5 | 1 | 1 | 204863 |
| 1022117 | 1009 × 1013 | 6000 | 1 | 1 | 1 | 206415 |
| 100160063 | 10007 × 10009 | 6000 | 3 | 1 | 1 | 204124 |
| 2021027 | 1009 × 2003 | 6000 | 1 | 85 | 1 | 204183 |
| 1010707 | 101 × 10007 | 6000 | 2 | 4049 | 2 | 214301 |

All assertions passed in local execution. Counts are **not runtime**. Selection evaluations exclude square-table setup. The adaptive procedure uses far more total work than the baseline in these examples despite fewer final exact square checks.

## Findings
- The modular square boundary is computable from N and a, without knowing p or q.
- Adaptive rejection preserves valid Fermat solutions and reduced the current candidate set.
- Factors were recovered for seven small test cases, using the existing Fermat identity.
- No AA-specific factoring theorem, general speedup, unbounded non-enumerative factor discovery, or RSA security break has been established.
- The fixed 6000-candidate window may fail when it does not contain a valid solution.

## Next boundary
Develop an observable on unknown factor-pair states without first enumerating a finite Fermat window. Measure total time and memory with same-environment baselines. Keep AA's established finite-corpus identification distinct from this exploratory application.

Reproducer: `AA_FACTOR_BRIDGE_STAGE3.py`.
