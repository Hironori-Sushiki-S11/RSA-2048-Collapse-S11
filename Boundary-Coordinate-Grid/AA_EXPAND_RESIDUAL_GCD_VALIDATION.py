#!/usr/bin/env python3
"""Adaptive Address EXPAND integration regression tests.

Exercises Blind Spot -> residual-GCD candidate generation -> Pick Up -> Select
-> Address Update -> Collision re-evaluation, without factorization, trial
division, or searching for factors.

Formal-model facts used here:
- The current (distance, direction) component is equivalent to residue modulo
  the axis, so its Address partition can be tested by exact components.
- At current selected-axis LCM L, each unresolved pair has residual
  k(e) = |x-y| // L.
- For candidate b, q(b) = b // gcd(L, b); a pair survives iff q(b) divides
  k(e).
- A candidate with q(b) not dividing G = gcd_e k(e) separates at least one
  current collision pair.

New implementation policy tested here (not an existing universal repository
rule): on a true Blind Spot, Pick Up b_new = L * (G + 1), add it to candidates,
and return to ordinary Select. This is a direct constructive policy satisfying
the formal EXPAND condition; it does not prescribe a general domain-wide
candidate-generation principle.
"""

from __future__ import annotations

from collections import defaultdict
from math import gcd, lcm, log2
from typing import Iterable, Sequence

INITIAL_AXES = tuple(range(2, 513))


def boundary_component(value: int, axis: int) -> tuple[int, int]:
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
    groups_by_address: dict[tuple[tuple[int, int], ...], list[int]] = defaultdict(list)
    for value in values:
        address = tuple(boundary_component(value, axis) for axis in axes)
        groups_by_address[address].append(value)
    return list(groups_by_address.values())


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
    result = 0
    pair_count = 0
    for group in groups:
        for index, left in enumerate(group):
            for right in group[index + 1 :]:
                difference = abs(left - right)
                if difference % current_lcm:
                    raise AssertionError("Collision pair violates current-LCM invariant")
                result = gcd(result, difference // current_lcm)
                pair_count += 1
    if pair_count == 0:
        raise ValueError("Residual GCD is undefined after complete identification")
    assert result > 0
    return result


def select_axis(
    values: Sequence[int],
    groups: Sequence[Sequence[int]],
    candidates: Iterable[int],
) -> tuple[int, list[list[int]], int]:
    """Apply the repository's (pair reduction, entropy, smaller axis) Select."""
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
    current_lcm = 1  # LCM of selected Address axes only; candidates are not selected yet.
    trajectory = [collision_potential(groups)]
    events: list[dict[str, int | str]] = []

    while collision_potential(groups):
        available = candidates - set(selected)
        axis, trial_groups, after = select_axis(values, groups, available)
        before = collision_potential(groups)

        if axis == 0 or after == before:
            g_value = residual_gcd(groups, current_lcm)
            new_axis = current_lcm * (g_value + 1)
            q_value = new_axis // gcd(current_lcm, new_axis)
            if q_value != g_value + 1 or g_value % q_value == 0:
                raise AssertionError("Constructed axis does not satisfy the EXPAND condition")
            if new_axis in candidates or new_axis in selected:
                raise AssertionError("EXPAND generated a duplicate axis")
            candidates.add(new_axis)
            events.append({"event": "EXPAND_PICK_UP", "axis": new_axis, "residual_gcd": g_value})
            continue  # Picked-up axis returns to ordinary Select.

        selected.append(axis)
        groups = trial_groups
        current_lcm = lcm(current_lcm, axis)
        trajectory.append(after)
        events.append({"event": "SELECT_ADDRESS_UPDATE_REEVALUATE", "axis": axis, "collision_potential": after})
        if after >= before:
            raise AssertionError("An accepted Address update must strictly reduce collisions")

    return {
        "selected_axes": selected,
        "trajectory": trajectory,
        "events": events,
        "collision_free": collision_potential(groups) == 0,
        "final_groups": groups,
    }


def assert_blind_spot(values: Sequence[int], axes: Sequence[int]) -> None:
    groups = [list(values)]
    assert collision_potential(groups) > 0
    for axis in axes:
        assert collision_potential(refine(groups, axis)) == collision_potential(groups)


def test_original_large_lcm_case() -> dict[str, object]:
    candidate_lcm = lcm(*INITIAL_AXES)
    corpus = (1, 1 + candidate_lcm)
    assert_blind_spot(corpus, INITIAL_AXES)

    result = run_expand(corpus, INITIAL_AXES)
    generated_axis = int(result["events"][0]["axis"])
    # No axis has been selected before EXPAND, so L_t=1 and G_t=candidate_lcm.
    assert generated_axis == candidate_lcm + 1
    assert result["trajectory"] == [1, 0]
    assert result["selected_axes"] == [generated_axis]
    assert result["collision_free"] is True
    assert result["final_groups"] == [[corpus[0]], [corpus[1]]]
    return result


def test_multiple_collision_pairs() -> dict[str, object]:
    # Six unresolved pairs, with all current candidates 2 and 3 ineffective.
    corpus = (1, 7, 13, 25)
    axes = (2, 3)
    assert_blind_spot(corpus, axes)

    result = run_expand(corpus, axes)
    assert result["trajectory"][0] == 6
    assert result["trajectory"][-1] == 0
    assert result["collision_free"] is True
    assert len(result["selected_axes"]) == 1
    assert len(result["final_groups"]) == 4
    assert result["events"][0]["event"] == "EXPAND_PICK_UP"
    assert result["events"][0]["residual_gcd"] == 6
    assert result["events"][1]["event"] == "SELECT_ADDRESS_UPDATE_REEVALUATE"
    return result


def main() -> None:
    large = test_original_large_lcm_case()
    multiple = test_multiple_collision_pairs()
    print("AA residual-GCD EXPAND integration regressions: PASS")
    print("case=large_lcm_two_values")
    print(f"  events={large['events']}")
    print(f"  selected_axes={large['selected_axes']}")
    print(f"  Collision_Potential={large['trajectory']}")
    print("case=multiple_collision_pairs")
    print(f"  events={multiple['events']}")
    print(f"  selected_axes={multiple['selected_axes']}")
    print(f"  Collision_Potential={multiple['trajectory']}")
    print(f"  final_Address={multiple['selected_axes']}")
    print("factorization / trial division / factor search: NOT USED")


if __name__ == "__main__":
    main()
