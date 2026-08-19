#!/usr/bin/env python3
"""
IKERUSIKI Adaptive Address Scaling — public structural reproducer.

This script reproduces the deterministic structural outputs archived for
Verification063 (32768/65536-bit) and Verification064 (131072-bit).

Important provenance note:
- This is a public reproducer built from the formal LCM-state selector.
- It is not claimed to be a byte-for-byte copy of the historical
  Verification063.py / Verification064.py scripts.
- It reproduces the structural fields used for external validation:
  selected axes, Collision trajectory, depth, and collision-free status.
- Runtime is machine-dependent and is not an identity check.
"""

from __future__ import annotations

import argparse
import math
import random
import time
from collections import defaultdict
from math import gcd, lcm

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
    (131072, 20260812): ("455|3", "4950->5->0"),
    (131072, 20260813): ("511|11", "4950->3->0"),
    (131072, 20260814): ("499|11", "4950->3->0"),
    (131072, 20260815): ("493|7", "4950->5->0"),
    (131072, 20260816): ("413|12", "4950->4->0"),
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


def collision_potential(groups: list[list[int]]) -> int:
    return sum(len(g) * (len(g) - 1) // 2 for g in groups if len(g) > 1)


def entropy_of_partition(groups: list[list[int]], total: int) -> float:
    out = 0.0
    for group in groups:
        p = len(group) / total
        out -= p * math.log2(p)
    return out


def refine_by_q(
    values: list[int],
    groups: list[list[int]],
    L: int,
    q: int,
) -> list[list[int]]:
    if q == 1:
        return [list(group) for group in groups]

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


def run_case(bit_size: int, seed: int) -> dict[str, object]:
    values = generate_corpus(bit_size, CORPUS_SIZE, seed)
    groups = [list(range(len(values)))]
    remaining = set(AXES)
    selected: list[int] = []
    trajectory = [collision_potential(groups)]
    L = 1

    t0 = time.perf_counter()

    for _depth in range(1, MAX_DEPTH + 1):
        before = collision_potential(groups)
        if before == 0:
            break

        q_cache: dict[int, tuple[int, float, list[list[int]]]] = {}
        best = None

        for b in sorted(remaining):
            q = b // gcd(L, b)

            if q not in q_cache:
                candidate_groups = refine_by_q(values, groups, L, q)
                after = collision_potential(candidate_groups)
                ent = entropy_of_partition(candidate_groups, len(values))
                q_cache[q] = (after, ent, candidate_groups)

            after, ent, candidate_groups = q_cache[q]
            score = (before - after, ent, -b)
            row = (score, b, after, candidate_groups)

            if best is None or row[0] > best[0]:
                best = row

        if best is None:
            raise RuntimeError("no candidate axis available")

        _, b_star, after, groups_star = best
        selected.append(b_star)
        remaining.remove(b_star)
        groups = groups_star
        L = lcm(L, b_star)
        trajectory.append(after)

        if after == 0 or after == before:
            break

    elapsed = time.perf_counter() - t0

    axes_text = "|".join(map(str, selected))
    trajectory_text = "->".join(map(str, trajectory))
    expected_axes, expected_trajectory = EXPECTED[(bit_size, seed)]
    match = axes_text == expected_axes and trajectory_text == expected_trajectory

    return {
        "bit_size": bit_size,
        "seed": seed,
        "selected_axes": axes_text,
        "trajectory": trajectory_text,
        "depth": len(selected),
        "collision_free": trajectory[-1] == 0,
        "elapsed_s": elapsed,
        "match": match,
    }


def choose_cases(args: argparse.Namespace) -> list[tuple[int, int]]:
    if args.bits is not None:
        seeds = [args.seed] if args.seed is not None else SEEDS
        return [(args.bits, seed) for seed in seeds]

    if args.verification == "063":
        bits = [32768, 65536]
    elif args.verification == "064":
        bits = [131072]
    else:
        bits = [32768, 65536, 131072]

    seeds = [args.seed] if args.seed is not None else SEEDS
    return [(bit_size, seed) for bit_size in bits for seed in seeds]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reproduce the archived structural outputs for Verification063/064."
    )
    parser.add_argument(
        "--verification",
        choices=["063", "064", "all"],
        default="all",
        help="run archived Verification063, Verification064, or both (default: all)",
    )
    parser.add_argument(
        "--bits",
        type=int,
        choices=[32768, 65536, 131072],
        help="run one bit size only; overrides --verification",
    )
    parser.add_argument(
        "--seed",
        type=int,
        choices=SEEDS,
        help="run one published seed only",
    )
    args = parser.parse_args()

    cases = choose_cases(args)
    all_match = True

    print("IKERUSIKI Adaptive Address Scaling — Public Structural Reproducer")
    print("=" * 92)

    for bit_size, seed in cases:
        result = run_case(bit_size, seed)
        all_match &= bool(result["match"])
        print(
            f"{bit_size:>6}-bit seed={seed}: "
            f"axes={result['selected_axes']:<8} "
            f"phi={result['trajectory']:<12} "
            f"depth={result['depth']} "
            f"collision_free={result['collision_free']} "
            f"match={result['match']} "
            f"time={result['elapsed_s']:.4f}s"
        )

    print("=" * 92)
    print("RESULT:", "PASS" if all_match else "FAIL")
    print(
        "Boundary: structural fields are deterministic under this protocol; "
        "runtime is machine-dependent."
    )
    print(
        "Provenance: this is a formal LCM-state reproducer, not a claim that the "
        "historical Verification063.py / Verification064.py files are byte-identical."
    )

    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
