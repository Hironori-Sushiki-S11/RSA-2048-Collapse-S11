#!/usr/bin/env python3
"""Independent residue-partition audit of the published AA scaling expectations.
Uses the published corpus generator but NOT refine_by_q / collision_potential.
This is a computational cross-check, not independent human replication.
"""
from collections import Counter
from ADAPTIVE_ADDRESS_SCALING_REPRODUCER import CORPUS_SIZE, EXPECTED, generate_corpus


def collision_count(values, axes):
    buckets = Counter(tuple(n % b for b in axes) for n in values)
    return sum(k * (k - 1) // 2 for k in buckets.values())


def main():
    passed = 0
    for (bits, seed), (axis_text, trace_text) in sorted(EXPECTED.items()):
        axes = [int(b) for b in axis_text.split('|')]
        values = generate_corpus(bits, CORPUS_SIZE, seed)
        assert len(values) == len(set(values)) == 100
        observed = [collision_count(values, axes[:k]) for k in range(len(axes) + 1)]
        expected = [int(phi) for phi in trace_text.split('->')]
        assert observed == expected and observed[-1] == 0, (bits, seed, observed, expected)
        passed += 1
        print(f"{bits}-bit seed={seed} axes={axes} collisions={observed} verified=PASS")
    print(f"RESULT: {passed}/{len(EXPECTED)} independent residue-partition checks PASS")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
