#!/usr/bin/env python3
"""IKERUSIKI Adaptive Address — LCM-state selector validation.

Reimplements the existing finite-corpus Select rule using the Formal Basis state
(L_t, current collision groups, q_t(b)) instead of a precomputed full
(distance,direction) component matrix.

The run is compared against the archived Verification063 scaling report for
32768- and 65536-bit, corpus size 100, axes 2..512, seeds 20260812..20260816.

This is implementation validation, not a replacement for the mathematical proof
and not a bit-length-independent runtime claim.
"""
from __future__ import annotations

import math
import random
import time
from collections import defaultdict
from math import gcd, lcm
from statistics import mean

BIT_SIZES = [32768, 65536]
CORPUS_SIZE = 100
AXES = list(range(2, 513))
SEEDS = [20260812, 20260813, 20260814, 20260815, 20260816]
MAX_DEPTH = 32

EXPECTED = {
    (32768, 20260812): ("477|5", "4950->3->0"),
    (32768, 20260813): ("505|9", "4950->5->0"),
    (32768, 20260814): ("365|8", "4950->6->0"),
    (32768, 20260815): ("467|7", "4950->4->0"),
    (32768, 20260816): ("449|7", "4950->6->0"),
    (65536, 20260812): ("493|5", "4950->5->0"),
    (65536, 20260813): ("417|7", "4950->4->0"),
    (65536, 20260814): ("483|5", "4950->4->0"),
    (65536, 20260815): ("511|5", "4950->5->0"),
    (65536, 20260816): ("425|7", "4950->4->0"),
}


def generate_corpus(bit_size: int, corpus_size: int, seed: int) -> list[int]:
    rng = random.Random((seed << 20) ^ bit_size)
    values: set[int] = set()
    while len(values) < corpus_size:
        value = rng.getrandbits(bit_size)
        value |= 1 << (bit_size - 1)
        value |= 1
        values.add(value)
    return list(values)


def phi(groups: list[list[int]]) -> int:
    return sum(len(g) * (len(g) - 1) // 2 for g in groups if len(g) > 1)


def entropy_of_partition(groups: list[list[int]], total: int) -> float:
    out = 0.0
    for g in groups:
        p = len(g) / total
        out -= p * math.log2(p)
    return out


def refine_by_q(values: list[int], groups: list[list[int]], L: int, q: int) -> list[list[int]]:
    if q == 1:
        return [list(g) for g in groups]
    out: list[list[int]] = []
    for group in groups:
        if len(group) <= 1:
            out.append(list(group))
            continue
        ref = values[group[0]]
        buckets: dict[int, list[int]] = defaultdict(list)
        for row_id in group:
            delta = values[row_id] - ref
            if delta % L != 0:
                raise AssertionError("current group violates LCM collision invariant")
            k_rel = delta // L
            buckets[k_rel % q].append(row_id)
        out.extend(buckets.values())
    return out


def run_lcm_selector(bit_size: int, seed: int):
    values = generate_corpus(bit_size, CORPUS_SIZE, seed)
    groups = [list(range(len(values)))]
    remaining = set(AXES)
    selected: list[int] = []
    trajectory = [phi(groups)]
    L = 1
    distinct_q_evaluations = 0
    raw_candidate_evaluations = 0

    t0 = time.perf_counter()
    for _depth in range(1, MAX_DEPTH + 1):
        before = phi(groups)
        if before == 0:
            break

        q_cache: dict[int, tuple[int, float, list[list[int]]]] = {}
        best = None

        for b in sorted(remaining):
            raw_candidate_evaluations += 1
            q = b // gcd(L, b)
            if q not in q_cache:
                candidate_groups = refine_by_q(values, groups, L, q)
                after = phi(candidate_groups)
                ent = entropy_of_partition(candidate_groups, len(values))
                q_cache[q] = (after, ent, candidate_groups)
                distinct_q_evaluations += 1
            after, ent, candidate_groups = q_cache[q]
            score = (before - after, ent, -b)
            row = (score, b, q, after, candidate_groups)
            if best is None or row[0] > best[0]:
                best = row

        assert best is not None
        _, b_star, q_star, after, groups_star = best
        selected.append(b_star)
        remaining.remove(b_star)
        groups = groups_star
        L = lcm(L, b_star)
        trajectory.append(after)

        if after == 0 or after == before:
            break

    elapsed = time.perf_counter() - t0
    return {
        "selected_axes": "|".join(map(str, selected)),
        "trajectory": "->".join(map(str, trajectory)),
        "depth": len(selected),
        "collision_free": trajectory[-1] == 0,
        "elapsed_s": elapsed,
        "raw_candidate_evaluations": raw_candidate_evaluations,
        "distinct_q_evaluations": distinct_q_evaluations,
    }


def main() -> int:
    rows = []
    all_match = True
    print("IKERUSIKI LCM-State Selector Validation")
    print("=" * 90)
    for bits in BIT_SIZES:
        for seed in SEEDS:
            result = run_lcm_selector(bits, seed)
            exp_axes, exp_traj = EXPECTED[(bits, seed)]
            match = result["selected_axes"] == exp_axes and result["trajectory"] == exp_traj
            all_match &= match
            rows.append((bits, seed, result, match))
            ratio = result["raw_candidate_evaluations"] / result["distinct_q_evaluations"]
            print(
                f"{bits:>6}-bit seed={seed}: axes={result['selected_axes']:<8} "
                f"phi={result['trajectory']:<12} match={str(match):<5} "
                f"time={result['elapsed_s']:.4f}s  q-compression={ratio:.2f}x"
            )

    print("\nAggregate")
    for bits in BIT_SIZES:
        subset = [r for b, _, r, _ in rows if b == bits]
        print(
            f"{bits:>6}-bit: mean LCM-selector time={mean(r['elapsed_s'] for r in subset):.4f}s; "
            f"all collision-free={all(r['collision_free'] for r in subset)}"
        )
    print(f"Archived Verification063 axis/trajectory reproduction: {sum(m for *_, m in rows)}/{len(rows)}")
    print("RESULT:", "PASS" if all_match else "FAIL")
    print("Boundary: timing is empirical for this Python implementation; no universal runtime claim.")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
