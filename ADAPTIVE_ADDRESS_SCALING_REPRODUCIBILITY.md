# IKERUSIKI Adaptive Address Scaling — Reproducibility Guide

## Purpose

This package closes the public reproducibility gap for the finite-corpus scaling runs reported in Verification063 and Verification064.

It reproduces the observed Adaptive Address trajectories at:

- 32768-bit
- 65536-bit
- 131072-bit

These are **finite-corpus empirical verifications only**.

They do **not** establish universal depth 2, a universal `2..512` axis bound, bit-length-independent runtime, RSA factorization, or universal integer indexing.

---

## Fixed protocol

The two scripts use the same experimental structure:

- finite corpus size: `100`
- candidate axes: `2..512`
- component: `(distance, direction)`
- Select rule:
  1. maximum unresolved-pair reduction
  2. higher Shannon entropy
  3. smaller axis
- seeds: `20260812..20260816`
- maximum Address depth: `32`

Corpus generation is deterministic for a given bit size and seed:

```python
rng = random.Random((seed << 20) ^ bit_size)
value = rng.getrandbits(bit_size)
value |= 1 << (bit_size - 1)
value |= 1
```

Thus the selected axes and Collision trajectories are reproducible from the public script itself.

---

## Files

### Verification063.py

Tests:

- 32768-bit
- 65536-bit
- 5 seeds each

Run:

```bash
python Verification063.py
```

Expected structural results:

| bit | seed | selected axes | Collision trajectory | depth |
|---:|---:|---|---|---:|
| 32768 | 20260812 | 477 → 5 | 4950 → 3 → 0 | 2 |
| 32768 | 20260813 | 505 → 9 | 4950 → 5 → 0 | 2 |
| 32768 | 20260814 | 365 → 8 | 4950 → 6 → 0 | 2 |
| 32768 | 20260815 | 467 → 7 | 4950 → 4 → 0 | 2 |
| 32768 | 20260816 | 449 → 7 | 4950 → 6 → 0 | 2 |
| 65536 | 20260812 | 493 → 5 | 4950 → 5 → 0 | 2 |
| 65536 | 20260813 | 417 → 7 | 4950 → 4 → 0 | 2 |
| 65536 | 20260814 | 483 → 5 | 4950 → 4 → 0 | 2 |
| 65536 | 20260815 | 511 → 5 | 4950 → 5 → 0 | 2 |
| 65536 | 20260816 | 425 → 7 | 4950 → 4 → 0 | 2 |

### Verification064.py

Tests:

- 131072-bit
- 5 seeds

Run:

```bash
python Verification064.py
```

Expected structural results:

| seed | selected axes | Collision trajectory | depth |
|---:|---|---|---:|
| 20260812 | 455 → 3 | 4950 → 5 → 0 | 2 |
| 20260813 | 511 → 11 | 4950 → 3 → 0 | 2 |
| 20260814 | 499 → 11 | 4950 → 3 → 0 | 2 |
| 20260815 | 493 → 7 | 4950 → 5 → 0 | 2 |
| 20260816 | 413 → 12 | 4950 → 4 → 0 | 2 |

---

## What should reproduce exactly?

The following are deterministic under the same Python integer arithmetic and script:

- generated corpus for each `(bit_size, seed)`
- selected axes
- Collision trajectory
- Address depth
- collision-free status
- first-stage Collision Potential

The following are **not** expected to match exactly across machines:

- wall-clock runtime
- peak memory
- operating-system scheduling effects

Runtime should therefore be treated as a machine-dependent measurement, not as an identity check.

---

## Independent rerun performed from this package

A fresh rerun reproduced the structural outputs exactly.

### Verification063 fresh rerun

```text
32768-bit:
[477|5]   4950->3->0
[505|9]   4950->5->0
[365|8]   4950->6->0
[467|7]   4950->4->0
[449|7]   4950->6->0

65536-bit:
[493|5]   4950->5->0
[417|7]   4950->4->0
[483|5]   4950->4->0
[511|5]   4950->5->0
[425|7]   4950->4->0
```

### Verification064 fresh rerun

```text
131072-bit:
[455|3]    4950->5->0
[511|11]   4950->3->0
[499|11]   4950->3->0
[493|7]    4950->5->0
[413|12]   4950->4->0
```

All 15 runs were collision-free at Address depth 2.

---

## Interpretation boundary

The reproducible empirical statement is:

> Under this fixed finite-corpus protocol, all tested 32768-, 65536-, and 131072-bit runs reached a collision-free state at Address depth 2 within candidate axes `2..512`.

The result supports an empirical distinction between:

1. integer arithmetic magnitude and its machine cost; and
2. observed structural identification depth in the supplied Current Finite corpus.

It does not prove that depth 2 persists universally.

---

## Suggested external-validation report

A third party can report only the following minimal fields:

```text
Python version:
OS / hardware:
Verification:
bit size:
seed:
selected axes:
Collision trajectory:
depth:
collision-free:
runtime:
```

A structural reproduction is successful when the deterministic fields match, even if runtime differs.
