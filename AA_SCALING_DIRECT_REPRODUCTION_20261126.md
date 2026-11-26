# Adaptive Address — Direct Public Reproducer Execution & Address Cross-Check (2026-11-26)

## Status
**PASS: 15/15** public Verification063/064 scaling cases directly executed, with exactly matching selected axes and Collision trajectories. **PASS: 15/15** separate raw-residue Address-partition cross-checks. This is a fresh ChatGPT execution-environment check of the published source code, **not** a new independent human replication or new theorem.

## Source identity / provenance
- Main repository: https://github.com/Hironori-Sushiki-S11/RSA-2048-Collapse-S11
- Executed published file: [ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py](ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py)
- Published Git blob SHA: `f00a6160787750aae76e18791f8f31600ff32834`
- Git blob SHA checked against the bytes executed: **exact match**
- Source SHA-256: `845d50fdda158fb3d6208ad6927f4d7f960afaffafcd46314b9fc2beba4f2be0`
- Base published structural reference: [Reproducibility guide](ADAPTIVE_ADDRESS_SCALING_REPRODUCIBILITY.md)
- Raw stdout: [15-case execution log](AA_SCALING_DIRECT_REPRODUCTION_20261126.log)
- Separate verification code: [Address cross-check](AA_SCALING_ADDRESS_CROSSCHECK_20261126.py)

## Protocol and environment
- Date: 2026-11-26 (execution environment; Japan local date)
- Python: **3.13.5**; OS: **Linux 6.18.57 x86_64 (glibc 2.41)**
- Finite corpus: 100 generated distinct odd integers per case; candidate axes `2..512`; seeds `20260812..20260816`; 3 bit sizes.
- Select: maximize Collision-pair reduction, then Shannon partition entropy, then prefer smaller axis.
- Command executed directly against the SHA-matching original file:
  
  ```bash
  python3 ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --verification all
  ```
- The historical Verification063/064 sources are not claimed byte-identical to this official public structural reproducer.

## Exact results
| Bits | Seed | Selected axes | Collision trajectory | Measured elapsed seconds |
|---:|---:|---|---|---:|
| 32768 | 20260812 | 477 → 5 | 4950 → 3 → 0 | 0.9257 |
| 32768 | 20260813 | 505 → 9 | 4950 → 5 → 0 | 0.8515 |
| 32768 | 20260814 | 365 → 8 | 4950 → 6 → 0 | 0.9117 |
| 32768 | 20260815 | 467 → 7 | 4950 → 4 → 0 | 0.9472 |
| 32768 | 20260816 | 449 → 7 | 4950 → 6 → 0 | 0.9015 |
| 65536 | 20260812 | 493 → 5 | 4950 → 5 → 0 | 1.6968 |
| 65536 | 20260813 | 417 → 7 | 4950 → 4 → 0 | 1.7392 |
| 65536 | 20260814 | 483 → 5 | 4950 → 4 → 0 | 1.7487 |
| 65536 | 20260815 | 511 → 5 | 4950 → 5 → 0 | 1.6860 |
| 65536 | 20260816 | 425 → 7 | 4950 → 4 → 0 | 1.6884 |
| 131072 | 20260812 | 455 → 3 | 4950 → 5 → 0 | 3.4731 |
| 131072 | 20260813 | 511 → 11 | 4950 → 3 → 0 | 3.3731 |
| 131072 | 20260814 | 499 → 11 | 4950 → 3 → 0 | 3.3959 |
| 131072 | 20260815 | 493 → 7 | 4950 → 5 → 0 | 3.4430 |
| 131072 | 20260816 | 413 → 12 | 4950 → 4 → 0 | 3.4851 |

**Totals:** 15/15 same axes, same Collision trajectories, Address depth 2, and final Collision zero. All 100 final Address tuples distinguish the members of each current finite corpus.

Median per-case script timings for this environment: 32,768 bit **0.9117 s**; 65,536 bit **1.6968 s**; 131,072 bit **3.4430 s**. A separate single 131,072-bit run (`--bits 131072 --seed 20260812`) measured **101,644 KB maximum RSS**, with total process wall time approximately **3.98 seconds**, using `/usr/bin/time`. This isolated resource measurement is not the exact same timing run as the 15-case log.

## Cross-check independent of the reproducer's partition-refinement implementation
The checked code in [AA_SCALING_ADDRESS_CROSSCHECK_20261126.py](AA_SCALING_ADDRESS_CROSSCHECK_20261126.py) regenerates the same corpus from the **published** generator and independently partitions it by tuples `tuple(n % b for b in selected_axes)`. For each prefix of the selected axes, it computes `Σ size*(size-1)//2` using `collections.Counter`, without calling the program's `refine_by_q` or `collision_potential`.

For **all 15** published cases, this separate residue-based computation exactly reproduced the reported Collision trajectories and verified 100 distinct final Address tuples. Axis choices themselves were checked by the direct execution of the official selector. This is an *implementation-path cross-check* of the same fixed protocol, not a separate algorithm, separate corpus, blinded challenge or human replication.

To repeat on a fresh repository checkout:
```bash
python3 ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --verification all
python3 AA_SCALING_ADDRESS_CROSSCHECK_20261126.py
```

## Evidence boundary and next work
This verifies **finite-corpus one-to-one identification in the specified runs**. It neither claims universal depth 2 nor bit-length-independent CPU cost, unknown-factor extraction, primality of the random corpus, or an RSA-2048 break.

This artifact closes the *direct public-code re-execution* item of the current publication evidence ledger. Genuine independent external replication, comparable AA-removed baselines, and complete resource logs remain separate projects and should be evaluated with the same inputs and final decision rule.
