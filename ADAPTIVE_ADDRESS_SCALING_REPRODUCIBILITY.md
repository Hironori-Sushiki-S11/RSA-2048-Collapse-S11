# IKERUSIKI Adaptive Address Scaling - Reproducibility Guide

## Purpose

This package provides a directly runnable public reproducer for the finite-corpus scaling results archived as Verification063 and Verification064.

It reproduces the observed Adaptive Address structural trajectories at:

- 32768-bit
- 65536-bit
- 131072-bit

These are **finite-corpus empirical verifications only**.

They do **not** establish universal depth 2, a universal `2..512` axis bound, bit-length-independent runtime, RSA factorization, or universal integer indexing.

---

## Public Reproducer

Run:

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py
```

The public reproducer is:

- `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py`

It reproduces the deterministic structural outputs archived for Verification063 and Verification064.

### Provenance note

The public reproducer uses the formally equivalent LCM-state selector.

It is **not claimed to be a byte-for-byte copy of the historical `Verification063.py` or `Verification064.py` scripts**.

The public validation target is the deterministic structural output:

- generated corpus for each `(bit_size, seed)`
- selected axes
- Collision trajectory
- Address depth
- collision-free status

Runtime is machine-dependent and is not an identity check.

---

## Fixed Protocol

The reproducer uses:

- finite corpus size: `100`
- candidate axes: `2..512`
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

## Minimal Commands

### Verification063 structural reproduction

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --verification 063
```

This runs:

- 32768-bit
- 65536-bit
- 5 seeds each

### Verification064 structural reproduction

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --verification 064
```

This runs:

- 131072-bit
- 5 seeds

### Smallest single published case

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --bits 32768 --seed 20260812
```

Expected:

```text
axes=477|5
phi=4950->3->0
depth=2
collision_free=True
match=True
```

### One 131072-bit case

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --bits 131072 --seed 20260812
```

Expected:

```text
axes=455|3
phi=4950->5->0
depth=2
collision_free=True
match=True
```

This one-case command is useful when a constrained execution environment cannot complete all 15 runs at once.

---

## Expected Verification063 Structural Results

| bit | seed | selected axes | Collision trajectory | depth |
|---:|---:|---|---|---:|
| 32768 | 20260812 | 477 -> 5 | 4950 -> 3 -> 0 | 2 |
| 32768 | 20260813 | 505 -> 9 | 4950 -> 5 -> 0 | 2 |
| 32768 | 20260814 | 365 -> 8 | 4950 -> 6 -> 0 | 2 |
| 32768 | 20260815 | 467 -> 7 | 4950 -> 4 -> 0 | 2 |
| 32768 | 20260816 | 449 -> 7 | 4950 -> 6 -> 0 | 2 |
| 65536 | 20260812 | 493 -> 5 | 4950 -> 5 -> 0 | 2 |
| 65536 | 20260813 | 417 -> 7 | 4950 -> 4 -> 0 | 2 |
| 65536 | 20260814 | 483 -> 5 | 4950 -> 4 -> 0 | 2 |
| 65536 | 20260815 | 511 -> 5 | 4950 -> 5 -> 0 | 2 |
| 65536 | 20260816 | 425 -> 7 | 4950 -> 4 -> 0 | 2 |

---

## Expected Verification064 Structural Results

| seed | selected axes | Collision trajectory | depth |
|---:|---|---|---:|
| 20260812 | 455 -> 3 | 4950 -> 5 -> 0 | 2 |
| 20260813 | 511 -> 11 | 4950 -> 3 -> 0 | 2 |
| 20260814 | 499 -> 11 | 4950 -> 3 -> 0 | 2 |
| 20260815 | 493 -> 7 | 4950 -> 5 -> 0 | 2 |
| 20260816 | 413 -> 12 | 4950 -> 4 -> 0 | 2 |

---

## What Should Reproduce Exactly?

Under the same Python integer arithmetic and public script, the deterministic fields are:

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

## Package Self-Check

Before publication of this reproducer, a fresh run of the script reproduced all 15 archived structural cases:

```text
Verification063:
32768-bit: 5/5 matched
65536-bit: 5/5 matched

Verification064:
131072-bit: 5/5 matched

TOTAL: 15/15 matched
All runs collision-free at Address depth 2.
```

This is a package self-check, not third-party independent validation.

---

## Interpretation Boundary

The reproducible empirical statement is:

> Under this fixed finite-corpus protocol, all tested 32768-, 65536-, and 131072-bit runs reached a collision-free state at Address depth 2 within candidate axes `2..512`.

The result supports an empirical distinction between:

1. integer arithmetic magnitude and its machine cost; and
2. observed structural identification depth in the supplied Current Finite corpus.

It does not prove that depth 2 persists universally.

---

## Suggested External-Validation Report

A third party can report:

```text
Python version:
OS / hardware:
command:
bit size:
seed:
selected axes:
Collision trajectory:
depth:
collision-free:
match:
runtime:
```

A structural reproduction is successful when the deterministic fields match, even if runtime differs.
