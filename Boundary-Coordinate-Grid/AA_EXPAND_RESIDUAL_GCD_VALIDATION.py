#!/usr/bin/env python3
"""Adaptive Address EXPAND integration regression test.

This standalone test exercises Blind Spot -> residual-GCD candidate generation
-> Pick Up -> Select -> Address Update -> Collision re-evaluation, without
factorization, trial division, or searching for factors.

Formal-model facts used here:
- Address equality for the (distance, direction) component is equivalent to
  congruence modulo the axis, so an address is represented exactly by its
  residue labels.
- At current LCM L, each unresolved pair has positive residual
  k(e) = |x-y| // L.
- For candidate b, q(b) = b // gcd(L, b); a pair survives iff q(b) divides
  k(e).
- A candidate with q(b) not dividing G = gcd_e k(e) separates at least one
  current collision pair.

New implementation policy exercised by this regression test:
- On a true Blind Spot, Pick Up b_new = L * (G + 1).
- Add that axis to the candidate pool and return to the ordinary Select rule.
This policy is a direct constructive choice consistent with the formal
EXPAND condition; it is not claimed to be an already specified universal
candidate-generation rule in the repository.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from math import gcd, lcm, log2
from typing import Iterable, Sequence

INITIAL_AXES = tuple(range(2, 513))


def boundary_component(value: int, axis: int) -> tuple[int, int]:
    """Return the repository's invertible (distance, direction) component."""
    residue = (value - 1) % axis
    reflected = axis - 1 - residue
    distance = min(residue, reflected)
    if residue < reflected:
        direction = 0
    elif residue > reflected:
        direction = 1
    else:
        direction = 2
    return distance, direction


def partition(values: Sequence[int], axes: Sequence[int]) -> list[list[int]]:
    """Build Address-equivalence groups using the selected axes."""
    groups_by_address: dict[tuple[tuple[int, int], ...], list[int]] = defaultdict(list)
    for value in values:
        address = tuple(boundary_component(value, axis) for axis in axes)
        groups_by_address[address].append(value)
    return list(groups_by_address.values())


def collision_pairs(groups: Sequence[Sequence[int]]) -> list[tuple[int, int]]:
    return [
        (left, right)
        for group in groups
        for index, left in enumerate(group)
        for right in group[index + 1 :]
    ]


def collision_potential(groups: Sequence[Sequence[int]]) -> int:
    return sum(len(group) * (len(group) - 1) // 2 for group in groups)


def entropy(groups: Sequence[Sequence[int]], total: int) -> float:
    if total == 0:
        return 0.0
    return -sum(
        (size / total) * log2(size / total)
        for size in (len(group) for group in groups)
        if size
    )


def refine(groups: Sequence[Sequence[int]], axis: int) -> list[list[int]]:
    refined: list[list[int]] = []
    for group in groups:
        buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
        for value in group:
            buckets[boundary_component(value, axis)].append(value)
        refined.extend(buckets.values())
    return refined


def residual_gcd(groups: Sequence[Sequence[int]], current_lcm: int) -> int:
    pairs = collision_pairs(groups)
    if not pairs:
        raise ValueError("Residual GCD is undefined after complete identification")
    result = 0
    for left, right in pairs:
        difference = abs(left - right)
        if difference % current_lcm:
            raise AssertionError("Collision pair violates the current-LCM invariant")
        result = gcd(result, difference // current_lcm)
    assert result > 0
    return result


def select_axis(
    values: Sequence[int],
    groups: Sequence[Sequence[int]],
    candidates: Iterable[int],
) -> tuple[int, list[list[int]], int]:
    """Apply the documented lexicographic Select score to available axes."""
    before = collision_potential(groups)
    best: tuple[tuple[int, float, int], int, list[list[int]], int] | None = None
    for axis in sorted(set(candidates)):
        trial_groups = refine(groups, axis)
        after = collision_potential(trial_groups)
        score = (before - after, entropy(trial_groups, len(values)), -axis)
        row = (score, axis, trial_groups, after)
        if best is None or row[0] > best[0]:
            best = row
    if best is None:
        return 0, [list(group) for group in groups], before
    return best[1], best[2], best[3]


def run_expand(values: Sequence[int], initial_axes: Sequence[int]) -> dict[str, object]:
    if len(values) != len(set(values)):
        raise ValueError("The held-information corpus must contain distinct values")
    if any(value <= 0 for value in values):
        raise ValueError("The integer-model corpus must contain positive values")
    if any(axis < 2 for axis in initial_axes):
        raise ValueError("Axes must be integers >= 2")

    candidates = set(initial_axes)
    selected: list[int] = []
    groups = [list(values)]
    current_lcm = 1
    trajectory = [collision_potential(groups)]
    events: list[tuple[str, int | None]] = []

    while collision_potential(groups):
        available = candidates - set(selected)
        axis, trial_groups, after = select_axis(values, groups, available)
        before = collision_potential(groups)

        if axis == 0 or after == before:
            # Exact residual-GCD EXPAND construction; no factorization or
            # divisor/factor search is performed.
            g_value = residual_gcd(groups, current_lcm)
            new_axis = current_lcm * (g_value + 1)
            q_value = new_axis // gcd(current_lcm, new_axis)
            if q_value != g_value + 1 or q_value % g_value == 0:
                raise AssertionError("Constructed axis does not satisfy the EXPAND condition")
            if new_axis in candidates or new_axis in selected:
                raise AssertionError("EXPAND generated a duplicate axis")
            candidates.add(new_axis)
            events.append(("EXPAND_PICK_UP", new_axis))
            # Return to the top: the generated axis is evaluated by normal Select.
            continue

        selected.append(axis)
        groups = trial_groups
        current_lcm = lcm(current_lcm, axis)
        trajectory.append(after)
        events.append(("SELECT_ADDRESS_UPDATE_REEVALUATE", axis))
        if after >= before:
            raise AssertionError("An accepted Address update must strictly reduce collisions")

    return {
        "selected_axes": selected,
        "trajectory": trajectory,
        "events": events,
        "collision_free": collision_potential(groups) == 0,
        "final_groups": groups,
    }


def run_regression() -> dict[str, object]:
    current_lcm = lcm(*INITIAL_AXES)
    corpus = (1, 1 + current_lcm)

    # The current candidate family is a Blind Spot: each axis divides L.
    initial_groups = [list(corpus)]
    assert collision_potential(initial_groups) == 1
    for axis in INITIAL_AXES:
        assert (corpus[1] - corpus[0]) % axis == 0
        assert collision_potential(refine(initial_groups, axis)) == 1

    result = run_expand(corpus, INITIAL_AXES)
    assert result["collision_free"] is True
    assert result["trajectory"] == [1, 0]
    assert len(result["events"]) == 2
    assert result["events"][0][0] == "EXPAND_PICK_UP"
    assert result["events"][1][0] == "SELECT_ADDRESS_UPDATE_REEVALUATE"

    generated_axis = result["events"][0][1]
    assert isinstance(generated_axis, int)
    assert generated_axis == current_lcm * 2
    assert result["selected_axes"] == [generated_axis]
    assert result["final_groups"] == [[corpus[0]], [corpus[1]]]
    return result


def main() -> None:
    result = run_regression()
    print("AA residual-GCD EXPAND integration regression: PASS")
    print(f"initial candidates: {INITIAL_AXES[0]}..{INITIAL_AXES[-1]}")
    print(f"events: {result['events']}")
    print(f"selected axes: {result['selected_axes']}")
    print(f"Collision Potential: {result['trajectory']}")
    print(f"collision-free: {result['collision_free']}")
    print("factorization / trial division / factor search: NOT USED")


if __name__ == "__main__":
    main()
