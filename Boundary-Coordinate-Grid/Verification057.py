# IKERUSIKI Verification 057
# Boundary Address Mutual Information and Axis Redundancy
#
# Objective:
# Measure how much information is shared between Boundary Address axes.
#
# Measures:
# 1. Shannon entropy of each axis
# 2. Pairwise mutual information
# 3. Normalized mutual information
# 4. Conditional information H(Y|X)
# 5. Mean and maximum redundancy per axis
# 6. Most redundant axis pairs
# 7. Least redundant informative axis pairs
#
# Scope:
# - Uses the verified prime corpora from Verification053-056
# - 512 / 1024 / 2048 / 4096-bit primes
# - Boundary Address axes 2..512
# - All unordered axis pairs are evaluated
# - Finite-corpus empirical measurements only
#
# Important:
# These values describe the supplied finite corpora. They do not prove
# independence or redundancy over all primes in an unbounded range.

import csv
import math
import statistics
import time
from collections import Counter
from pathlib import Path

BIT_SIZES = [512, 1024, 2048, 4096]
AXES = list(range(2, 513))
TOP_PAIR_COUNT = 50


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
                f"{path.name}:{line_number}: "
                f"expected {bit_size}-bit integer, "
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


def mutual_information(left_values, right_values, left_entropy, right_entropy):
    joint_entropy = shannon_entropy(
        list(zip(left_values, right_values))
    )
    shared_bits = max(
        0.0,
        left_entropy + right_entropy - joint_entropy,
    )

    normalizer = min(left_entropy, right_entropy)
    normalized = (
        shared_bits / normalizer
        if normalizer > 0
        else 0.0
    )

    return (
        shared_bits,
        normalized,
        joint_entropy,
        max(0.0, right_entropy - shared_bits),
        max(0.0, left_entropy - shared_bits),
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

    entropies = {
        axis: shannon_entropy(axis_values[axis])
        for axis in AXES
    }

    preparation_ns = time.perf_counter_ns() - start
    pair_start = time.perf_counter_ns()

    per_axis_shared = {
        axis: []
        for axis in AXES
    }
    per_axis_normalized = {
        axis: []
        for axis in AXES
    }

    pair_rows = []

    for left_position, left_axis in enumerate(AXES[:-1]):
        left_values = axis_values[left_axis]
        left_entropy = entropies[left_axis]

        for right_axis in AXES[left_position + 1:]:
            right_values = axis_values[right_axis]
            right_entropy = entropies[right_axis]

            (
                shared_bits,
                normalized,
                joint_entropy,
                right_given_left,
                left_given_right,
            ) = mutual_information(
                left_values,
                right_values,
                left_entropy,
                right_entropy,
            )

            per_axis_shared[left_axis].append(shared_bits)
            per_axis_shared[right_axis].append(shared_bits)
            per_axis_normalized[left_axis].append(normalized)
            per_axis_normalized[right_axis].append(normalized)

            pair_rows.append(
                {
                    "bit_size": bit_size,
                    "prime_count": len(primes),
                    "left_axis": left_axis,
                    "right_axis": right_axis,
                    "left_entropy_bits": left_entropy,
                    "right_entropy_bits": right_entropy,
                    "joint_entropy_bits": joint_entropy,
                    "mutual_information_bits": shared_bits,
                    "normalized_mutual_information": normalized,
                    "right_given_left_bits": right_given_left,
                    "left_given_right_bits": left_given_right,
                }
            )

    pair_ns = time.perf_counter_ns() - pair_start

    axis_rows = []

    for axis in AXES:
        normalized_values = per_axis_normalized[axis]
        shared_values = per_axis_shared[axis]

        axis_rows.append(
            {
                "bit_size": bit_size,
                "prime_count": len(primes),
                "axis": axis,
                "axis_entropy_bits": entropies[axis],
                "mean_mutual_information_bits": (
                    statistics.mean(shared_values)
                ),
                "median_mutual_information_bits": (
                    statistics.median(shared_values)
                ),
                "max_mutual_information_bits": max(shared_values),
                "mean_normalized_redundancy": (
                    statistics.mean(normalized_values)
                ),
                "median_normalized_redundancy": (
                    statistics.median(normalized_values)
                ),
                "max_normalized_redundancy": max(normalized_values),
                "independence_score": (
                    1.0 - statistics.mean(normalized_values)
                ),
            }
        )

    for row in axis_rows:
        row["independence_rank"] = None
        row["redundancy_rank"] = None

    informative_axis_rows = [
        row
        for row in axis_rows
        if row["axis_entropy_bits"] > 0
    ]

    ranked_independence = sorted(
        informative_axis_rows,
        key=lambda row: (
            row["independence_score"],
            row["axis_entropy_bits"],
            -row["axis"],
        ),
        reverse=True,
    )

    ranked_redundancy = sorted(
        informative_axis_rows,
        key=lambda row: (
            row["mean_normalized_redundancy"],
            row["axis_entropy_bits"],
            -row["axis"],
        ),
        reverse=True,
    )

    for rank, row in enumerate(ranked_independence, start=1):
        row["independence_rank"] = rank

    for rank, row in enumerate(ranked_redundancy, start=1):
        row["redundancy_rank"] = rank

    most_redundant_pairs = sorted(
        pair_rows,
        key=lambda row: (
            row["normalized_mutual_information"],
            row["mutual_information_bits"],
            -row["left_axis"],
            -row["right_axis"],
        ),
        reverse=True,
    )[:TOP_PAIR_COUNT]

    informative_pairs = [
        row
        for row in pair_rows
        if row["left_entropy_bits"] > 0
        and row["right_entropy_bits"] > 0
    ]

    least_redundant_pairs = sorted(
        informative_pairs,
        key=lambda row: (
            row["normalized_mutual_information"],
            -(
                row["left_entropy_bits"]
                + row["right_entropy_bits"]
            ),
            row["left_axis"],
            row["right_axis"],
        ),
    )[:TOP_PAIR_COUNT]

    top_pair_rows = []

    for category, rows in (
        ("most_redundant", most_redundant_pairs),
        ("least_redundant_informative", least_redundant_pairs),
    ):
        for rank, row in enumerate(rows, start=1):
            output = dict(row)
            output["category"] = category
            output["rank"] = rank
            top_pair_rows.append(output)

    all_normalized = [
        row["normalized_mutual_information"]
        for row in pair_rows
    ]
    all_shared = [
        row["mutual_information_bits"]
        for row in pair_rows
    ]

    most_independent_axis = ranked_independence[0]
    most_redundant_axis = ranked_redundancy[0]
    highest_pair = most_redundant_pairs[0]
    lowest_pair = least_redundant_pairs[0]

    summary = {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "axis_count": len(AXES),
        "axis_pair_count": len(pair_rows),
        "informative_axis_count": len(informative_axis_rows),
        "zero_entropy_axis_count": (
            len(axis_rows) - len(informative_axis_rows)
        ),
        "mean_pair_mutual_information_bits": (
            statistics.mean(all_shared)
        ),
        "median_pair_mutual_information_bits": (
            statistics.median(all_shared)
        ),
        "mean_pair_normalized_redundancy": (
            statistics.mean(all_normalized)
        ),
        "median_pair_normalized_redundancy": (
            statistics.median(all_normalized)
        ),
        "most_independent_axis": (
            most_independent_axis["axis"]
        ),
        "most_independent_axis_entropy_bits": (
            most_independent_axis["axis_entropy_bits"]
        ),
        "most_independent_axis_score": (
            most_independent_axis["independence_score"]
        ),
        "most_redundant_axis": (
            most_redundant_axis["axis"]
        ),
        "most_redundant_axis_entropy_bits": (
            most_redundant_axis["axis_entropy_bits"]
        ),
        "most_redundant_axis_mean_normalized": (
            most_redundant_axis[
                "mean_normalized_redundancy"
            ]
        ),
        "highest_redundancy_left_axis": (
            highest_pair["left_axis"]
        ),
        "highest_redundancy_right_axis": (
            highest_pair["right_axis"]
        ),
        "highest_pair_mutual_information_bits": (
            highest_pair["mutual_information_bits"]
        ),
        "highest_pair_normalized_redundancy": (
            highest_pair[
                "normalized_mutual_information"
            ]
        ),
        "lowest_redundancy_left_axis": (
            lowest_pair["left_axis"]
        ),
        "lowest_redundancy_right_axis": (
            lowest_pair["right_axis"]
        ),
        "lowest_pair_mutual_information_bits": (
            lowest_pair["mutual_information_bits"]
        ),
        "lowest_pair_normalized_redundancy": (
            lowest_pair[
                "normalized_mutual_information"
            ]
        ),
        "preparation_total_ms": (
            preparation_ns / 1_000_000
        ),
        "pair_analysis_total_ms": (
            pair_ns / 1_000_000
        ),
    }

    return axis_rows, top_pair_rows, summary


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
    print("IKERUSIKI Verification057")
    print("Boundary Address Mutual Information and Axis Redundancy")
    print()

    total_start = time.perf_counter()
    all_axis_rows = []
    all_top_pair_rows = []
    summaries = []

    for bit_size in BIT_SIZES:
        primes = load_prime_corpus(bit_size)

        axis_rows, pair_rows, summary = benchmark_bit_size(
            bit_size,
            primes,
        )

        all_axis_rows.extend(axis_rows)
        all_top_pair_rows.extend(pair_rows)
        summaries.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'primes={summary["prime_count"]} | '
            f'pairs={summary["axis_pair_count"]} | '
            f'mean NMI='
            f'{summary["mean_pair_normalized_redundancy"]:.3f} | '
            f'independent axis='
            f'{summary["most_independent_axis"]} '
            f'({summary["most_independent_axis_score"]:.3f}) | '
            f'highest pair='
            f'{summary["highest_redundancy_left_axis"]}/'
            f'{summary["highest_redundancy_right_axis"]} '
            f'({summary["highest_pair_normalized_redundancy"]:.3f})'
        )

    base = Path(__file__).resolve().parent

    write_csv(
        base / "verification057_axis_redundancy.csv",
        all_axis_rows,
    )
    write_csv(
        base / "verification057_top_pairs.csv",
        all_top_pair_rows,
    )
    write_csv(
        base / "verification057_summary.csv",
        summaries,
    )

    print()
    print("Verification057 Summary")
    print(
        "All 511 axes evaluated:",
        all(
            summary["axis_count"] == len(AXES)
            for summary in summaries
        ),
    )
    print(
        "All unordered axis pairs evaluated:",
        all(
            summary["axis_pair_count"]
            == len(AXES) * (len(AXES) - 1) // 2
            for summary in summaries
        ),
    )
    print(
        "Total elapsed seconds:",
        f"{time.perf_counter() - total_start:.6f}",
    )


if __name__ == "__main__":
    main()
