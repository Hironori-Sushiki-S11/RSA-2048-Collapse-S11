# IKERUSIKI Verification 058
# Boundary Address Axis Importance Ranking
#
# Objective:
# Rank Boundary Address axes by their actual identifying contribution inside
# each supplied prime corpus.
#
# Measures:
# 1. Single-axis Shannon entropy
# 2. Single-axis unique-address ratio
# 3. Single-axis collision reduction
# 4. Mean normalized redundancy against all other informative axes
# 5. Leave-one-axis-out information loss from the full address
# 6. Leave-one-axis-out collision increase
# 7. Composite importance score
#
# Scope:
# - Uses the verified prime corpora from Verification053-057
# - 512 / 1024 / 2048 / 4096-bit primes
# - Boundary Address axes 2..512
# - Finite-corpus empirical ranking only
#
# Important:
# This ranks axes for the supplied finite corpora. It does not establish one
# universal ranking valid for every prime in an unbounded range.

import csv
import math
import statistics
import time
from collections import Counter
from pathlib import Path

BIT_SIZES = [512, 1024, 2048, 4096]
AXES = list(range(2, 513))


def load_prime_corpus(bit_size):
    path = Path(__file__).with_name(f"prime_corpus_{bit_size}.txt")

    if not path.exists():
        raise FileNotFoundError(
            f"Required corpus file not found: {path.name}"
        )

    primes = []

    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        try:
            prime = int(line)
        except ValueError as error:
            raise ValueError(
                f"{path.name}:{line_number}: invalid integer"
            ) from error

        if prime.bit_length() != bit_size:
            raise ValueError(
                f"{path.name}:{line_number}: expected {bit_size}-bit integer, "
                f"found {prime.bit_length()}-bit"
            )

        primes.append(prime)

    if not primes:
        raise ValueError(f"{path.name}: no primes loaded")

    if len(primes) != len(set(primes)):
        raise ValueError(f"{path.name}: duplicate values found")

    return primes


def boundary_component(number, axis):
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


def shannon_entropy(values):
    counts = Counter(values)
    total = len(values)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def normalized_mutual_information(
    left_values,
    right_values,
    left_entropy,
    right_entropy,
):
    normalizer = min(left_entropy, right_entropy)

    if normalizer <= 0:
        return 0.0

    joint_entropy = shannon_entropy(
        list(zip(left_values, right_values))
    )
    mutual_information = max(
        0.0,
        left_entropy + right_entropy - joint_entropy,
    )

    return mutual_information / normalizer


def collision_metrics(values):
    counts = Counter(values)
    sizes = list(counts.values())

    collision_groups = sum(
        1 for size in sizes if size > 1
    )
    colliding_items = sum(
        size for size in sizes if size > 1
    )
    unique_items = sum(
        1 for size in sizes if size == 1
    )

    return {
        "distinct_count": len(counts),
        "collision_group_count": collision_groups,
        "colliding_item_count": colliding_items,
        "unique_item_count": unique_items,
        "unique_ratio": unique_items / len(values),
        "largest_bucket_size": max(sizes),
    }


def minmax_normalize(rows, field):
    values = [row[field] for row in rows]
    minimum = min(values)
    maximum = max(values)

    if math.isclose(minimum, maximum):
        for row in rows:
            row[f"{field}_normalized"] = 0.0
        return

    for row in rows:
        row[f"{field}_normalized"] = (
            (row[field] - minimum)
            / (maximum - minimum)
        )


def benchmark_bit_size(bit_size, primes):
    start = time.perf_counter_ns()

    axis_values = {
        axis: [
            boundary_component(prime, axis)
            for prime in primes
        ]
        for axis in AXES
    }

    addresses = [
        tuple(axis_values[axis][row_id] for axis in AXES)
        for row_id in range(len(primes))
    ]

    preparation_ns = time.perf_counter_ns() - start

    entropies = {
        axis: shannon_entropy(axis_values[axis])
        for axis in AXES
    }

    informative_axes = [
        axis for axis in AXES
        if entropies[axis] > 0
    ]

    redundancy_start = time.perf_counter_ns()
    mean_redundancy = {}

    for axis in AXES:
        if entropies[axis] <= 0:
            mean_redundancy[axis] = 1.0
            continue

        values = []

        for other_axis in informative_axes:
            if other_axis == axis:
                continue

            values.append(
                normalized_mutual_information(
                    axis_values[axis],
                    axis_values[other_axis],
                    entropies[axis],
                    entropies[other_axis],
                )
            )

        mean_redundancy[axis] = (
            statistics.mean(values)
            if values
            else 0.0
        )

    redundancy_ns = time.perf_counter_ns() - redundancy_start

    full_entropy = shannon_entropy(addresses)
    full_collision = collision_metrics(addresses)
    corpus_information_bits = math.log2(len(primes))

    rows = []

    for axis_index, axis in enumerate(AXES):
        single_metrics = collision_metrics(
            axis_values[axis]
        )

        without_axis = [
            address[:axis_index] + address[axis_index + 1:]
            for address in addresses
        ]

        without_entropy = shannon_entropy(without_axis)
        without_collision = collision_metrics(without_axis)

        information_loss = max(
            0.0,
            full_entropy - without_entropy,
        )
        collision_group_increase = max(
            0,
            without_collision["collision_group_count"]
            - full_collision["collision_group_count"],
        )
        colliding_item_increase = max(
            0,
            without_collision["colliding_item_count"]
            - full_collision["colliding_item_count"],
        )

        rows.append(
            {
                "bit_size": bit_size,
                "prime_count": len(primes),
                "axis": axis,
                "axis_entropy_bits": entropies[axis],
                "axis_entropy_fraction": (
                    entropies[axis] / corpus_information_bits
                    if corpus_information_bits > 0
                    else 0.0
                ),
                "single_axis_distinct_count": (
                    single_metrics["distinct_count"]
                ),
                "single_axis_unique_ratio": (
                    single_metrics["unique_ratio"]
                ),
                "single_axis_collision_group_count": (
                    single_metrics["collision_group_count"]
                ),
                "single_axis_colliding_item_count": (
                    single_metrics["colliding_item_count"]
                ),
                "single_axis_largest_bucket_size": (
                    single_metrics["largest_bucket_size"]
                ),
                "mean_normalized_redundancy": (
                    mean_redundancy[axis]
                ),
                "independence_score": (
                    1.0 - mean_redundancy[axis]
                    if entropies[axis] > 0
                    else 0.0
                ),
                "leave_one_out_information_loss_bits": (
                    information_loss
                ),
                "leave_one_out_collision_group_increase": (
                    collision_group_increase
                ),
                "leave_one_out_colliding_item_increase": (
                    colliding_item_increase
                ),
            }
        )

    for field in (
        "axis_entropy_bits",
        "single_axis_unique_ratio",
        "independence_score",
        "leave_one_out_information_loss_bits",
        "leave_one_out_collision_group_increase",
        "leave_one_out_colliding_item_increase",
    ):
        minmax_normalize(rows, field)

    for row in rows:
        row["importance_score"] = (
            0.25 * row["axis_entropy_bits_normalized"]
            + 0.20 * row["single_axis_unique_ratio_normalized"]
            + 0.20 * row["independence_score_normalized"]
            + 0.15 * row[
                "leave_one_out_information_loss_bits_normalized"
            ]
            + 0.10 * row[
                "leave_one_out_collision_group_increase_normalized"
            ]
            + 0.10 * row[
                "leave_one_out_colliding_item_increase_normalized"
            ]
        )

    ranked = sorted(
        rows,
        key=lambda row: (
            row["importance_score"],
            row["axis_entropy_bits"],
            row["independence_score"],
            -row["axis"],
        ),
        reverse=True,
    )

    for rank, row in enumerate(ranked, start=1):
        row["importance_rank"] = rank

    top = ranked[0]

    summary = {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "axis_count": len(AXES),
        "informative_axis_count": len(informative_axes),
        "zero_entropy_axis_count": (
            len(AXES) - len(informative_axes)
        ),
        "full_address_entropy_bits": full_entropy,
        "corpus_information_bits": corpus_information_bits,
        "full_collision_group_count": (
            full_collision["collision_group_count"]
        ),
        "top_axis": top["axis"],
        "top_axis_importance_score": (
            top["importance_score"]
        ),
        "top_axis_entropy_bits": (
            top["axis_entropy_bits"]
        ),
        "top_axis_unique_ratio": (
            top["single_axis_unique_ratio"]
        ),
        "top_axis_independence_score": (
            top["independence_score"]
        ),
        "top_axis_leave_one_out_information_loss_bits": (
            top["leave_one_out_information_loss_bits"]
        ),
        "preparation_total_ms": (
            preparation_ns / 1_000_000
        ),
        "redundancy_analysis_total_ms": (
            redundancy_ns / 1_000_000
        ),
    }

    return rows, ranked[:20], summary


def write_csv(path, rows):
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    print("IKERUSIKI Verification058")
    print("Boundary Address Axis Importance Ranking")
    print()

    total_start = time.perf_counter()
    all_rows = []
    all_top_rows = []
    summaries = []

    for bit_size in BIT_SIZES:
        primes = load_prime_corpus(bit_size)

        rows, top_rows, summary = benchmark_bit_size(
            bit_size,
            primes,
        )

        all_rows.extend(rows)
        all_top_rows.extend(top_rows)
        summaries.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'primes={summary["prime_count"]} | '
            f'informative axes='
            f'{summary["informative_axis_count"]} | '
            f'top axis={summary["top_axis"]} | '
            f'score={summary["top_axis_importance_score"]:.3f} | '
            f'entropy={summary["top_axis_entropy_bits"]:.3f} bits | '
            f'unique ratio={summary["top_axis_unique_ratio"]:.3f} | '
            f'independence={summary["top_axis_independence_score"]:.3f}'
        )

    base = Path(__file__).resolve().parent

    write_csv(
        base / "verification058_axis_importance.csv",
        all_rows,
    )
    write_csv(
        base / "verification058_top20.csv",
        all_top_rows,
    )
    write_csv(
        base / "verification058_summary.csv",
        summaries,
    )

    print()
    print("Verification058 Summary")
    print(
        "All 511 axes ranked:",
        all(
            summary["axis_count"] == len(AXES)
            for summary in summaries
        ),
    )
    print(
        "All full addresses collision-free:",
        all(
            summary["full_collision_group_count"] == 0
            for summary in summaries
        ),
    )
    print(
        "Total elapsed seconds:",
        f"{time.perf_counter() - total_start:.6f}",
    )


if __name__ == "__main__":
    main()
