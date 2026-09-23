# AA Prime Identification Validation v1.0

## Status (corrected 2026-09-23)

- **Core Validation: COMPLETE**
- **Final Core Checks: 27/27 PASS**
- **Frontier Prime Identification: OPEN**
- **External Grok attempt: computationally unresolved; its target `p=141566927` was already known Composite**

This directory records the completed Core Validation phase of Adaptive Address (AA) Prime Identification. It separates finite-corpus identity from exact Prime/Composite certificates.

AA has demonstrated:

- finite-corpus identity completion;
- exact structural collision prediction on tested corpora;
- separation of identity from Prime/Composite determination;
- exact Composite certificate paths;
- direct exact Prime/Composite determination without requiring a factor-first path on tractable Mersenne corpora;
- adaptive representation with preserved exact trajectory;
- symbolic collision-free identification at exponent scales through \(10^{18}\).

**The remaining open frontier is an exact Prime certificate for a genuinely unresolved Mersenne candidate beyond the public first-test frontier.** The prior Grok target `p=141566927` was already Composite, with three factors reported in 2007. See [`EXTERNAL_FRONTIER_ATTEMPT_GROK.md`](EXTERNAL_FRONTIER_ATTEMPT_GROK.md) and [`VALIDATION_COMPLETE.md`](VALIDATION_COMPLETE.md).

## R61 factor-certificate cost audit (2026-09-23)

For 64 prime exponents near \(10^{12}\), AA's axis 1019 distinguishes all 64 targets. A separate factor scan exactly certifies 12 Composite cases; 52 remain unresolved and **zero new Prime certificates** result. With and without AA address selection, the same factor detector returns the same 12 certificates and executes the same 524,725 eligible candidate checks and 28,351 modular checks. Five runs per mode found no evidence that the AA address reduces certificate cost in this pipeline. The small axis 1019 itself cannot be a factor of any of these targets.

- [`AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT_2026-09-23.md`](AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT_2026-09-23.md) — claim, comparison, full factors, and scope.
- [`scripts/AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT.py`](scripts/AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT.py) — reproducer (`python scripts/AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT.py --mode compare --reps 5`).
- [`results/AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT_RESULTS.json`](results/AA_R61_IDENTITY_CERTIFICATE_COST_AUDIT_RESULTS.json) — ten raw trials and all certificates.
- [`AA_FRONTIER_EXACTNESS_BOUNDARY_2026-09-23.md`](AA_FRONTIER_EXACTNESS_BOUNDARY_2026-09-23.md) — Lucas–Lehmer residue-axis boundary and actual trajectory counterexample.

See also `VALIDATION_MANIFEST.json`, `scripts/FINAL_VALIDATION_CHECK.py`, and `results/` for earlier Core Validation artifacts. This package does not claim a new Mersenne Prime or a newly discovered factor.
