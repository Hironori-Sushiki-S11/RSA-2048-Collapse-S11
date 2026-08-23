# IKERUSIKI Adaptive Boundary Address Demonstration
#
# Purpose:
# Make Verification061's internal adaptive selection visible to third parties.
#
# Demonstrates:
#   Current Held-Information Corpus
#   -> collision detection
#   -> all candidate axes evaluated
#   -> best axis selected
#   -> Address updated
#   -> collision rechecked
#   -> repeat until unique
#
# Selection rule inherited from Verification061:
#   1. maximize unresolved collision-pair reduction
#   2. break ties by higher Shannon entropy
#   3. break remaining ties by smaller axis
#
# Scope:
# - current held-information corpus empirical demonstration; each instantiated corpus is finite
# - does not prove universal identification over an unbounded range

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

AXES = list(range(2, 513))
TOP_CANDIDATES = 10


def load_values(path: Path) -> list[int]:
    values = []
    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            values.append(int(line))
        except ValueError as exc:
            raise ValueError(
                f"{path}:{line_number}: invalid integer"
            ) from exc

    if not values:
        raise ValueError("No integers found in corpus.")
    if len(values) != len(set(values)):
        raise ValueError("Duplicate integers found in corpus.")
    return values


def boundary_component(number: int, axis: int) -> tuple[int, int]:
    residue = (number - 1) % axis
    reflected = axis - 1 - residue
    distance = min(residue, reflected)

    if residue < reflected:
        direction = 0
    elif residue > reflected:
        direction = 1
    else:
        direction = 2

    return distance, direction


def shannon_entropy(values: Sequence[object]) -> float:
    counts = Counter(values)
    total = len(values)
    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def unresolved_pair_count(groups: Sequence[Sequence[int]]) -> int:
    return sum(
        len(group) * (len(group) - 1) // 2
        for group in groups
        if len(group) > 1
    )


def collision_groups(groups: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(group) for group in groups if len(group) > 1]


def partition_group(
    group: Sequence[int],
    components: Sequence[Sequence[tuple[int, int]]],
    axis_index: int,
) -> list[list[int]]:
    buckets: dict[tuple[int, int], list[int]] = defaultdict(list)

    for row_id in group:
        buckets[components[row_id][axis_index]].append(row_id)

    return list(buckets.values())


def evaluate_axis(
    groups: Sequence[Sequence[int]],
    components: Sequence[Sequence[tuple[int, int]]],
    axis_index: int,
) -> dict:
    before_pairs = unresolved_pair_count(groups)
    candidate_groups: list[list[int]] = []
    labels = []

    for group_number, group in enumerate(groups):
        children = partition_group(
            group,
            components,
            axis_index,
        )
        candidate_groups.extend(children)

        for child in children:
            component = components[child[0]][axis_index]
            labels.extend(
                (group_number, component)
                for _ in child
            )

    after_pairs = unresolved_pair_count(candidate_groups)
    reduction = before_pairs - after_pairs
    entropy = shannon_entropy(labels)

    return {
        "axis": AXES[axis_index],
        "axis_index": axis_index,
        "before_pairs": before_pairs,
        "after_pairs": after_pairs,
        "reduction": reduction,
        "entropy": entropy,
        "groups": candidate_groups,
        "collision_groups": len(
            collision_groups(candidate_groups)
        ),
        "largest_bucket": max(
            len(group) for group in candidate_groups
        ),
        "score": (
            reduction,
            entropy,
            -AXES[axis_index],
        ),
    }


def short_integer(value: int, width: int = 36) -> str:
    text = str(value)
    if len(text) <= width:
        return text
    side = (width - 3) // 2
    return text[:side] + "..." + text[-side:]


def print_collision_snapshot(
    groups: Sequence[Sequence[int]],
    values: Sequence[int],
) -> None:
    collisions = collision_groups(groups)

    if not collisions:
        print("Collision groups : 0")
        return

    print(f"Collision groups : {len(collisions)}")
    print(
        "Colliding values :",
        sum(len(group) for group in collisions),
    )
    print(
        "Largest bucket   :",
        max(len(group) for group in collisions),
    )

    for number, group in enumerate(collisions[:5], start=1):
        print(
            f"  collision[{number}] row_ids={group}"
        )
        for row_id in group[:5]:
            print(
                "    ",
                f"row {row_id:>3}:",
                short_integer(values[row_id]),
            )

    if len(collisions) > 5:
        print(
            f"  ... {len(collisions) - 5} more collision groups"
        )


def run_demo(
    values: Sequence[int],
    max_depth: int,
    top_candidates: int,
) -> None:
    components = [
        tuple(
            boundary_component(value, axis)
            for axis in AXES
        )
        for value in values
    ]

    groups: list[list[int]] = [
        list(range(len(values)))
    ]
    remaining = set(range(len(AXES)))
    selected_axes: list[int] = []

    print("=" * 72)
    print("IKERUSIKI ADAPTIVE BOUNDARY ADDRESS DEMONSTRATION")
    print("=" * 72)
    print(f"Current held-information corpus size : {len(values)}")
    print(f"Candidate axes     : {AXES[0]}..{AXES[-1]}")
    print("Current Address    : []")
    print()

    for depth in range(1, max_depth + 1):
        before_pairs = unresolved_pair_count(groups)

        if before_pairs == 0:
            break

        print("-" * 72)
        print(f"STEP {depth}")
        print("-" * 72)
        print(f"Current Address   : {selected_axes}")
        print(f"Unresolved pairs : {before_pairs}")
        print_collision_snapshot(groups, values)
        print()

        evaluations = [
            evaluate_axis(
                groups,
                components,
                axis_index,
            )
            for axis_index in sorted(remaining)
        ]
        evaluations.sort(
            key=lambda row: row["score"],
            reverse=True,
        )

        print("Candidate-axis comparison")
        print(
            " rank | axis | pair reduction | pairs after | "
            "entropy | collision groups | largest bucket"
        )
        print("-" * 72)

        for rank, row in enumerate(
            evaluations[:top_candidates],
            start=1,
        ):
            print(
                f" {rank:>4} | "
                f"{row['axis']:>4} | "
                f"{row['reduction']:>14} | "
                f"{row['after_pairs']:>11} | "
                f"{row['entropy']:>7.4f} | "
                f"{row['collision_groups']:>16} | "
                f"{row['largest_bucket']:>14}"
            )

        best = evaluations[0]
        best_axis = best["axis"]

        print()
        print(
            "SELECT",
            f"axis={best_axis}",
            "because it has the maximum lexicographic score",
            "(collision-pair reduction, entropy, smaller-axis tie-break).",
        )

        old_address = list(selected_axes)
        selected_axes.append(best_axis)
        remaining.remove(best["axis_index"])
        groups = best["groups"]

        print(
            "Address Update    :",
            f"{old_address} -> {selected_axes}",
        )
        print(
            "Pairs             :",
            f"{before_pairs} -> {best['after_pairs']}",
        )
        print(
            "Collision groups  :",
            best["collision_groups"],
        )
        print()

        if best["after_pairs"] == before_pairs:
            print("BLIND SPOT / STALL DETECTED")
            print(
                "No candidate axis in the current horizon "
                "reduced unresolved pairs."
            )
            print(
                "This is the point where a future implementation "
                "would expand the axis horizon."
            )
            break

        if best["after_pairs"] == 0:
            print("RESULT: UNIQUE WITHIN THE CURRENT HELD-INFORMATION CORPUS")
            break

    print()
    print("=" * 72)
    print("FINAL")
    print("=" * 72)
    print("Final Address      :", selected_axes)
    print(
        "Unresolved pairs   :",
        unresolved_pair_count(groups),
    )
    print(
        "Collision-free     :",
        unresolved_pair_count(groups) == 0,
    )
    print(
        "Scope              : current held-information corpus empirical demonstration (instantiated corpus finite)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Visualize adaptive Boundary Address selection "
            "step by step."
        )
    )
    parser.add_argument(
        "corpus",
        type=Path,
        help="Path to the currently instantiated finite integer corpus text file.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=32,
    )
    parser.add_argument(
        "--top",
        type=int,
        default=TOP_CANDIDATES,
        help="Number of candidate axes to display per step.",
    )
    args = parser.parse_args()

    values = load_values(args.corpus)
    run_demo(
        values=values,
        max_depth=args.max_depth,
        top_candidates=args.top,
    )


if __name__ == "__main__":
    main()
