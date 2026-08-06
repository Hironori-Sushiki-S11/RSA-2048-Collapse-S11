# IKERUSIKI Verification 061
# Adaptive Boundary Address Explorer
#
# Objective:
# Extend Verification059 from one-shot compact axis selection to a recursive,
# stage-by-stage exploration that evaluates both:
#
#   1. Vertical persistence:
#      Does the selected target branch continue to shrink at deeper stages?
#
#   2. Horizontal collision separation:
#      How efficiently does each newly selected axis split the unresolved
#      collision groups at the current stage?
#
# Scope:
# - Finite-corpus empirical verification only.
# - Uses prime_corpus_512.txt, prime_corpus_1024.txt,
#   prime_corpus_2048.txt, and prime_corpus_4096.txt when present.
# - Does not prove universal uniqueness over an unbounded integer range.
#
# Outputs:
# - verification061_stage_summary.csv
# - verification061_bucket_trace.csv
# - verification061_result.json

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

BIT_SIZES = [512, 1024, 2048, 4096]
AXES = list(range(2, 513))
MAX_DEPTH = 32


def load_prime_corpus(bit_size: int) -> list[int]:
    path = Path(__file__).with_name(f"prime_corpus_{bit_size}.txt")
    if not path.exists():
        raise FileNotFoundError(
            f"Required corpus file not found: {path.name}. "
            "Place the verified corpus in the same directory."
        )

    values: list[int] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        try:
            value = int(line)
        except ValueError as exc:
            raise ValueError(
                f"{path.name}:{line_number}: invalid integer"
            ) from exc

        if value.bit_length() != bit_size:
            raise ValueError(
                f"{path.name}:{line_number}: expected {bit_size}-bit integer, "
                f"found {value.bit_length()}-bit"
            )
        values.append(value)

    if not values:
        raise ValueError(f"{path.name}: no values loaded")
    if len(values) != len(set(values)):
        raise ValueError(f"{path.name}: duplicate values found")
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


def unresolved_pair_count(groups: Iterable[Sequence[int]]) -> int:
    return sum(
        len(group) * (len(group) - 1) // 2
        for group in groups
        if len(group) > 1
    )


def partition_rows(
    row_ids: Sequence[int],
    components: Sequence[Sequence[tuple[int, int]]],
    axis_index: int,
) -> list[list[int]]:
    buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row_id in row_ids:
        buckets[components[row_id][axis_index]].append(row_id)
    return list(buckets.values())


def all_collision_groups(
    groups: Sequence[Sequence[int]],
) -> list[list[int]]:
    return [list(group) for group in groups if len(group) > 1]


@dataclass
class StageSummary:
    bit_size: int
    depth: int
    selected_axis: int
    group_count_before: int
    group_count_after: int
    collision_group_count_before: int
    collision_group_count_after: int
    unresolved_pairs_before: int
    unresolved_pairs_after: int
    unresolved_pair_reduction: int
    colliding_values_before: int
    colliding_values_after: int
    largest_bucket_before: int
    largest_bucket_after: int
    entropy_after_bits: float
    target_bucket_before: int
    target_bucket_after: int
    target_preserved: bool


@dataclass
class BucketTrace:
    bit_size: int
    depth: int
    selected_axis: int
    parent_bucket_size: int
    child_bucket_size: int
    contains_target: bool
    member_row_ids: str


def choose_best_axis(
    groups: Sequence[Sequence[int]],
    components: Sequence[Sequence[tuple[int, int]]],
    remaining_axis_indices: set[int],
) -> tuple[int, list[list[int]], tuple[int, float, int]]:
    before_pairs = unresolved_pair_count(groups)
    best_index: int | None = None
    best_groups: list[list[int]] | None = None
    best_score: tuple[int, float, int] | None = None

    for axis_index in sorted(remaining_axis_indices):
        candidate_groups: list[list[int]] = []
        labels: list[tuple[int, tuple[int, int]]] = []

        for group_number, group in enumerate(groups):
            children = partition_rows(group, components, axis_index)
            candidate_groups.extend(children)
            for child in children:
                component = components[child[0]][axis_index]
                labels.extend((group_number, component) for _ in child)

        candidate_pairs = unresolved_pair_count(candidate_groups)
        reduction = before_pairs - candidate_pairs
        entropy = shannon_entropy(labels)
        score = (reduction, entropy, -AXES[axis_index])

        if best_score is None or score > best_score:
            best_index = axis_index
            best_groups = candidate_groups
            best_score = score

    if best_index is None or best_groups is None or best_score is None:
        raise RuntimeError("No selectable axis remains")

    return best_index, best_groups, best_score


def run_adaptive_explorer(
    bit_size: int,
    values: Sequence[int],
    target_row_id: int = 0,
) -> tuple[list[StageSummary], list[BucketTrace], dict]:
    if not 0 <= target_row_id < len(values):
        raise ValueError("target_row_id is outside the corpus")

    components = [
        tuple(boundary_component(value, axis) for axis in AXES)
        for value in values
    ]

    groups: list[list[int]] = [list(range(len(values)))]
    remaining = set(range(len(AXES)))
    selected_axes: list[int] = []
    summaries: list[StageSummary] = []
    traces: list[BucketTrace] = []

    for depth in range(1, MAX_DEPTH + 1):
        collision_groups_before = all_collision_groups(groups)
        if not collision_groups_before:
            break

        before_pairs = unresolved_pair_count(groups)
        before_colliding = sum(len(group) for group in collision_groups_before)
        largest_before = max(len(group) for group in groups)
        target_group_before = next(
            group for group in groups if target_row_id in group
        )

        axis_index, candidate_groups, _ = choose_best_axis(
            groups=groups,
            components=components,
            remaining_axis_indices=remaining,
        )

        remaining.remove(axis_index)
        selected_axis = AXES[axis_index]
        selected_axes.append(selected_axis)

        collision_groups_after = all_collision_groups(candidate_groups)
        after_pairs = unresolved_pair_count(candidate_groups)
        after_colliding = sum(len(group) for group in collision_groups_after)
        largest_after = max(len(group) for group in candidate_groups)
        target_group_after = next(
            group for group in candidate_groups if target_row_id in group
        )

        group_labels: list[tuple[int, ...]] = []
        for group_number, group in enumerate(candidate_groups):
            group_labels.extend([(group_number,)] * len(group))

        summaries.append(
            StageSummary(
                bit_size=bit_size,
                depth=depth,
                selected_axis=selected_axis,
                group_count_before=len(groups),
                group_count_after=len(candidate_groups),
                collision_group_count_before=len(collision_groups_before),
                collision_group_count_after=len(collision_groups_after),
                unresolved_pairs_before=before_pairs,
                unresolved_pairs_after=after_pairs,
                unresolved_pair_reduction=before_pairs - after_pairs,
                colliding_values_before=before_colliding,
                colliding_values_after=after_colliding,
                largest_bucket_before=largest_before,
                largest_bucket_after=largest_after,
                entropy_after_bits=shannon_entropy(group_labels),
                target_bucket_before=len(target_group_before),
                target_bucket_after=len(target_group_after),
                target_preserved=target_row_id in target_group_after,
            )
        )

        parent_lookup: dict[int, int] = {}
        for parent in groups:
            for row_id in parent:
                parent_lookup[row_id] = len(parent)

        for child in candidate_groups:
            traces.append(
                BucketTrace(
                    bit_size=bit_size,
                    depth=depth,
                    selected_axis=selected_axis,
                    parent_bucket_size=parent_lookup[child[0]],
                    child_bucket_size=len(child),
                    contains_target=target_row_id in child,
                    member_row_ids="|".join(str(row_id) for row_id in child),
                )
            )

        groups = candidate_groups

        # No axis reduced any unresolved pair: vertical inertia has stopped.
        if before_pairs == after_pairs:
            break

    final_collisions = all_collision_groups(groups)
    result = {
        "bit_size": bit_size,
        "value_count": len(values),
        "target_row_id": target_row_id,
        "selected_axes": selected_axes,
        "depth_reached": len(summaries),
        "collision_free": len(final_collisions) == 0,
        "final_collision_group_count": len(final_collisions),
        "final_colliding_value_count": sum(
            len(group) for group in final_collisions
        ),
        "final_largest_bucket_size": max(len(group) for group in groups),
        "target_final_bucket_size": len(
            next(group for group in groups if target_row_id in group)
        ),
        "stopped_by_no_reduction": bool(
            summaries
            and summaries[-1].unresolved_pairs_before
            == summaries[-1].unresolved_pairs_after
        ),
        "scope": "finite-corpus empirical verification",
    }
    return summaries, traces, result


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base = Path(__file__).resolve().parent
    all_summaries: list[dict] = []
    all_traces: list[dict] = []
    all_results: list[dict] = []

    print("IKERUSIKI Verification061")
    print("Adaptive Boundary Address Explorer")
    print()

    for bit_size in BIT_SIZES:
        values = load_prime_corpus(bit_size)
        summaries, traces, result = run_adaptive_explorer(
            bit_size=bit_size,
            values=values,
            target_row_id=0,
        )

        all_summaries.extend(asdict(row) for row in summaries)
        all_traces.extend(asdict(row) for row in traces)
        all_results.append(result)

        print(
            f"{bit_size:>4}-bit | values={len(values)} | "
            f"depth={result['depth_reached']} | "
            f"axes={result['selected_axes']} | "
            f"target bucket={result['target_final_bucket_size']} | "
            f"largest bucket={result['final_largest_bucket_size']} | "
            f"collision-free={result['collision_free']}"
        )

    write_csv(
        base / "verification061_stage_summary.csv",
        all_summaries,
    )
    write_csv(
        base / "verification061_bucket_trace.csv",
        all_traces,
    )
    (base / "verification061_result.json").write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print(
        "All target branches preserved:",
        all(row["target_preserved"] for row in all_summaries),
    )
    print(
        "All corpora collision-free:",
        all(result["collision_free"] for result in all_results),
    )


if __name__ == "__main__":
    main()
