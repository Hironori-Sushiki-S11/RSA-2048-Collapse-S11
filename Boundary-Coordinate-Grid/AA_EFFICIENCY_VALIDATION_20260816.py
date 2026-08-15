#!/usr/bin/env python3
"""
IKERUSIKI Adaptive Address — Structural-State Efficiency Validation

Purpose
-------
Empirically cross-check consequences already derived from the finite-corpus
Formal Basis for the current (distance, direction) address component:

1) LCM State Sufficiency
   Same LCM state => same collision partition.

2) Candidate Quotient Sufficiency
   Same q_t(b) = b / gcd(L_t, b) => same refinement of current collisions.

3) Exact Select / Survival Law
   A current collision pair e survives candidate b iff q_t(b) | k_t(e),
   where k_t(e) = |x-y| / L_t.

4) Selection-state contraction
   Direct candidate evaluation is compared with evaluation using only
   (L_t, K_t, Q_t). Timing is reported as an empirical implementation result,
   not as a proof of bit-length-independent runtime.

This script validates implementation agreement; it does not replace the proof.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import gcd, lcm
from random import Random
from time import perf_counter
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Pair = Tuple[int, int]


def component(n: int, b: int) -> Tuple[int, int]:
    """Current invertible (distance, direction) component for residue r=(n-1) mod b.

    direction: -1 = left, 0 = center, +1 = right.
    Together with distance, this uniquely determines the residue.
    """
    r = (n - 1) % b
    mirror = b - 1 - r
    d = r if r <= mirror else mirror
    direction = -1 if r < mirror else (1 if r > mirror else 0)
    return d, direction


def address(n: int, axes: Sequence[int]) -> Tuple[Tuple[int, int], ...]:
    return tuple(component(n, b) for b in axes)


def lcm_of(axes: Sequence[int]) -> int:
    out = 1
    for b in axes:
        out = lcm(out, b)
    return out


def collision_pairs_by_address(corpus: Sequence[int], axes: Sequence[int]) -> Set[Pair]:
    groups: Dict[Tuple[Tuple[int, int], ...], List[int]] = defaultdict(list)
    for x in corpus:
        groups[address(x, axes)].append(x)
    pairs: Set[Pair] = set()
    for vals in groups.values():
        vals = sorted(vals)
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                pairs.add((vals[i], vals[j]))
    return pairs


def collision_pairs_by_lcm(corpus: Sequence[int], L: int) -> Set[Pair]:
    groups: Dict[int, List[int]] = defaultdict(list)
    for x in corpus:
        groups[(x - 1) % L].append(x)
    pairs: Set[Pair] = set()
    for vals in groups.values():
        vals = sorted(vals)
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                pairs.add((vals[i], vals[j]))
    return pairs


def q_factor(L: int, b: int) -> int:
    return b // gcd(L, b)


def residuals(collisions: Iterable[Pair], L: int) -> Dict[Pair, int]:
    out: Dict[Pair, int] = {}
    for x, y in collisions:
        d = abs(x - y)
        assert d % L == 0
        out[(x, y)] = d // L
    return out


def predicted_survivors(collisions: Set[Pair], ks: Dict[Pair, int], L: int, b: int) -> Set[Pair]:
    q = q_factor(L, b)
    return {e for e in collisions if ks[e] % q == 0}


def direct_survivors(corpus: Sequence[int], axes: Sequence[int], b: int) -> Set[Pair]:
    return collision_pairs_by_address(corpus, list(axes) + [b])


def make_collision_corpus(rng: Random, bit_length: int, L: int,
                          groups: int = 12, group_size: int = 4,
                          unique_count: int = 20) -> List[int]:
    """Build a finite corpus with guaranteed collisions modulo L."""
    if bit_length < 16:
        raise ValueError("bit_length must be >= 16")
    high = 1 << (bit_length - 1)
    span_bits = max(8, bit_length - 4)
    values: Set[int] = set()

    # Collision groups: same base residue modulo L.
    for _ in range(groups):
        base = high | rng.getrandbits(span_bits)
        base -= (base - 1) % L
        base += 1 + rng.randrange(L)
        # Normalize residue once, then add multiples of L.
        residue = (base - 1) % L
        base = (high | rng.getrandbits(span_bits))
        base = base - ((base - 1 - residue) % L)
        for j in range(group_size):
            step = (j + 1) * (1 + rng.randrange(1, 50))
            values.add(base + step * L)

    # Additional values, allowed to be singleton blocks.
    while len(values) < groups * group_size + unique_count:
        values.add(high | rng.getrandbits(span_bits))

    return sorted(values)


@dataclass
class ValidationResult:
    bit_length: int
    corpus_size: int
    axes: Tuple[int, ...]
    L: int
    collisions: int
    candidates: int
    distinct_q: int
    lcm_state_ok: bool
    quotient_equivalence_ok: bool
    exact_select_ok: bool
    direct_eval_s: float
    residual_eval_s: float


def validate_case(bit_length: int, seed: int, candidate_max: int = 128) -> ValidationResult:
    rng = Random(seed)
    axes = (6, 10, 14, 15)  # L = 210; deliberately contains redundant history.
    L = lcm_of(axes)
    corpus = make_collision_corpus(rng, bit_length, L)

    # 1) LCM State Sufficiency: compare two different histories with same LCM.
    axes_prime = (2, 3, 5, 7, 21, 30, 35)  # same LCM = 210
    assert lcm_of(axes_prime) == L
    c_a = collision_pairs_by_address(corpus, axes)
    c_b = collision_pairs_by_address(corpus, axes_prime)
    c_l = collision_pairs_by_lcm(corpus, L)
    lcm_state_ok = (c_a == c_b == c_l)

    collisions = c_a
    ks = residuals(collisions, L)
    candidates = list(range(2, candidate_max + 1))

    # 2) Candidate quotient sufficiency: same q => same direct survivor set.
    by_q: Dict[int, List[int]] = defaultdict(list)
    for b in candidates:
        by_q[q_factor(L, b)].append(b)

    quotient_equivalence_ok = True
    for q, bs in by_q.items():
        if len(bs) < 2:
            continue
        reference = direct_survivors(corpus, axes, bs[0])
        for b in bs[1:]:
            if direct_survivors(corpus, axes, b) != reference:
                quotient_equivalence_ok = False
                break
        if not quotient_equivalence_ok:
            break

    # 3) Exact Select law: direct refinement equals divisibility prediction.
    exact_select_ok = True
    for b in candidates:
        if direct_survivors(corpus, axes, b) != predicted_survivors(collisions, ks, L, b):
            exact_select_ok = False
            break

    # 4) Timing comparison for complete candidate scoring.
    t0 = perf_counter()
    direct_counts = {b: len(direct_survivors(corpus, axes, b)) for b in candidates}
    direct_eval_s = perf_counter() - t0

    q_values = sorted(by_q)
    t1 = perf_counter()
    q_counts = {q: sum(1 for k in ks.values() if k % q == 0) for q in q_values}
    residual_counts = {b: q_counts[q_factor(L, b)] for b in candidates}
    residual_eval_s = perf_counter() - t1

    if direct_counts != residual_counts:
        exact_select_ok = False

    return ValidationResult(
        bit_length=bit_length,
        corpus_size=len(corpus),
        axes=axes,
        L=L,
        collisions=len(collisions),
        candidates=len(candidates),
        distinct_q=len(q_values),
        lcm_state_ok=lcm_state_ok,
        quotient_equivalence_ok=quotient_equivalence_ok,
        exact_select_ok=exact_select_ok,
        direct_eval_s=direct_eval_s,
        residual_eval_s=residual_eval_s,
    )



def randomized_crosscheck(trials: int = 100, seed: int = 20260815) -> Tuple[int, int]:
    """Randomized finite-corpus cross-check across varying LCM states.

    Returns (passed, total). This is empirical implementation validation only.
    """
    rng = Random(seed)
    bit_choices = [64, 128, 256, 512, 1024, 2048, 4096]
    passed = 0
    for _ in range(trials):
        bits = rng.choice(bit_choices)
        pool = list(range(2, 33))
        rng.shuffle(pool)
        axes = tuple(sorted(pool[:rng.randint(2, 6)]))
        L = lcm_of(axes)

        # Same-LCM alternate history by appending random divisors already absorbed by L.
        redundant = [d for d in range(2, 65) if L % d == 0 and d not in axes]
        rng.shuffle(redundant)
        axes_prime = tuple(list(axes) + redundant[:rng.randint(0, min(6, len(redundant)))])
        assert lcm_of(axes_prime) == L

        corpus = make_collision_corpus(
            rng, bits, L,
            groups=rng.randint(4, 8),
            group_size=rng.randint(3, 5),
            unique_count=rng.randint(5, 12),
        )
        c1 = collision_pairs_by_address(corpus, axes)
        c2 = collision_pairs_by_address(corpus, axes_prime)
        cL = collision_pairs_by_lcm(corpus, L)
        if not (c1 == c2 == cL):
            continue

        ks = residuals(c1, L)
        candidates = list(range(2, 97))
        by_q: Dict[int, List[int]] = defaultdict(list)
        for b in candidates:
            by_q[q_factor(L, b)].append(b)

        ok = True
        direct_cache: Dict[int, Set[Pair]] = {}
        for b in candidates:
            direct = direct_survivors(corpus, axes, b)
            direct_cache[b] = direct
            if direct != predicted_survivors(c1, ks, L, b):
                ok = False
                break
        if not ok:
            continue

        for bs in by_q.values():
            ref = direct_cache[bs[0]]
            if any(direct_cache[b] != ref for b in bs[1:]):
                ok = False
                break
        if ok:
            passed += 1

    return passed, trials

def main() -> int:
    bit_lengths = [64, 512, 4096, 16384, 65536]
    results: List[ValidationResult] = []
    for i, bits in enumerate(bit_lengths):
        results.append(validate_case(bits, seed=20260815 + i))

    print("IKERUSIKI Adaptive Address — Structural-State Efficiency Validation")
    print("=" * 78)
    print("Formal identities are proved separately; this run checks implementation agreement.\n")
    header = (
        "bits", "n", "L", "collisions", "cand", "|Q|",
        "LCM-state", "same-q", "exact-select", "direct(s)", "residual(s)", "speedup"
    )
    print("{:>8} {:>4} {:>5} {:>10} {:>5} {:>4} {:>10} {:>8} {:>12} {:>10} {:>12} {:>9}".format(*header))
    for r in results:
        speedup = r.direct_eval_s / r.residual_eval_s if r.residual_eval_s else float('inf')
        print(
            f"{r.bit_length:>8} {r.corpus_size:>4} {r.L:>5} {r.collisions:>10} "
            f"{r.candidates:>5} {r.distinct_q:>4} "
            f"{str(r.lcm_state_ok):>10} {str(r.quotient_equivalence_ok):>8} "
            f"{str(r.exact_select_ok):>12} {r.direct_eval_s:>10.6f} "
            f"{r.residual_eval_s:>12.6f} {speedup:>8.2f}x"
        )

    random_passed, random_total = randomized_crosscheck(trials=100)
    print(f"\nRandomized cross-check: {random_passed}/{random_total} PASS")

    all_ok = (random_passed == random_total) and all(
        r.lcm_state_ok and r.quotient_equivalence_ok and r.exact_select_ok for r in results
    )
    print("\nRESULT:", "PASS" if all_ok else "FAIL")
    print("Checked identities:")
    print("  lcm(B)=lcm(B') => same collision partition")
    print("  q_t(b)=q_t(b') => same refinement")
    print("  e survives b <=> q_t(b) divides k_t(e)")
    print("  direct candidate scores == residual (K_t,Q_t) scores")
    print("\nTiming note: empirical Python timing only; no bit-length-independent runtime claim.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
