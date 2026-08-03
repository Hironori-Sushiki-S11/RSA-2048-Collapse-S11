# IKERUSIKI Verification 054
# Boundary Coordinate Grid Search Benchmark
#
# Objective:
# Build a Boundary Address grid and compare:
# 1. Direct modulo-based partial search
# 2. Precomputed grid partial search
# 3. Inverted-index partial search
# 4. Full-address exact lookup
#
# Scope:
# - Uses the same verified prime corpora as Verification053
# - 512 / 1024 / 2048 / 4096-bit primes
# - axes 2..512
# - partial searches use selected address axes
# - measures correctness, candidate counts, build time, storage, and lookup time
#
# Important:
# This verifies search behavior inside the supplied finite prime corpora.
# It does not prove unique identification over all primes in an unbounded range.

import csv
import json
import math
import statistics
import time
import tracemalloc
from collections import defaultdict
from pathlib import Path

BIT_SIZES = [512, 1024, 2048, 4096]
AXES = list(range(2, 513))
PARTIAL_AXIS_COUNTS = [4, 8, 16, 32]
REPEATS = 200


def load_prime_corpus(bit_size):
    path = Path(__file__).with_name(
        f"prime_corpus_{bit_size}.txt"
    )

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


def prime_address(prime):
    return tuple(
        boundary_component(prime, axis)
        for axis in AXES
    )


def choose_axis_indices(axis_count):
    if axis_count <= 0:
        return []

    if axis_count >= len(AXES):
        return list(range(len(AXES)))

    return sorted({
        round(
            index * (len(AXES) - 1)
            / (axis_count - 1)
        )
        for index in range(axis_count)
    })


def build_grid(primes):
    return [prime_address(prime) for prime in primes]


def build_inverted_index(grid):
    inverted = {
        axis_index: defaultdict(set)
        for axis_index in range(len(AXES))
    }

    for row_id, address in enumerate(grid):
        for axis_index, component in enumerate(address):
            inverted[axis_index][component].add(row_id)

    return inverted


def build_full_index(grid):
    index = defaultdict(list)

    for row_id, address in enumerate(grid):
        index[address].append(row_id)

    return dict(index)


def direct_partial_search(
    primes,
    target,
    selected_indices,
):
    matches = []

    expected = {
        axis_index: boundary_component(
            target,
            AXES[axis_index],
        )
        for axis_index in selected_indices
    }

    for row_id, prime in enumerate(primes):
        for axis_index in selected_indices:
            if boundary_component(
                prime,
                AXES[axis_index],
            ) != expected[axis_index]:
                break
        else:
            matches.append(row_id)

    return matches


def grid_partial_search(
    grid,
    target_address,
    selected_indices,
):
    return [
        row_id
        for row_id, address in enumerate(grid)
        if all(
            address[axis_index]
            == target_address[axis_index]
            for axis_index in selected_indices
        )
    ]


def inverted_partial_search(
    inverted,
    target_address,
    selected_indices,
):
    if not selected_indices:
        return []

    posting_sets = [
        inverted[axis_index].get(
            target_address[axis_index],
            set(),
        )
        for axis_index in selected_indices
    ]

    result = set(posting_sets[0])

    for posting_set in posting_sets[1:]:
        result.intersection_update(posting_set)

        if not result:
            break

    return sorted(result)


def median_runtime_ns(function, repeats):
    timings = []
    result = None

    for _ in range(repeats):
        start = time.perf_counter_ns()
        result = function()
        timings.append(time.perf_counter_ns() - start)

    return result, statistics.median(timings)


def benchmark_bit_size(bit_size, primes):
    tracemalloc.start()

    start = time.perf_counter_ns()
    grid = build_grid(primes)
    grid_build_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    inverted = build_inverted_index(grid)
    inverted_build_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    full_index = build_full_index(grid)
    full_index_build_ns = time.perf_counter_ns() - start

    _, peak_memory_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    serialized_grid_bytes = len(
        json.dumps(
            grid,
            separators=(",", ":"),
        ).encode("utf-8")
    )

    rows = []

    for target_row, target in enumerate(primes):
        target_address = grid[target_row]

        for requested_axis_count in PARTIAL_AXIS_COUNTS:
            selected_indices = choose_axis_indices(
                requested_axis_count
            )
            actual_axis_count = len(selected_indices)

            direct_matches, direct_ns = median_runtime_ns(
                lambda: direct_partial_search(
                    primes,
                    target,
                    selected_indices,
                ),
                REPEATS,
            )

            grid_matches, grid_ns = median_runtime_ns(
                lambda: grid_partial_search(
                    grid,
                    target_address,
                    selected_indices,
                ),
                REPEATS,
            )

            inverted_matches, inverted_ns = median_runtime_ns(
                lambda: inverted_partial_search(
                    inverted,
                    target_address,
                    selected_indices,
                ),
                REPEATS,
            )

            full_matches, full_ns = median_runtime_ns(
                lambda: full_index.get(
                    target_address,
                    [],
                ),
                REPEATS,
            )

            correct = (
                direct_matches
                == grid_matches
                == inverted_matches
                and target_row in full_matches
                and target_row in direct_matches
            )

            rows.append(
                {
                    "bit_size": bit_size,
                    "target_row": target_row,
                    "prime_count": len(primes),
                    "requested_axis_count": (
                        requested_axis_count
                    ),
                    "actual_axis_count": (
                        actual_axis_count
                    ),
                    "candidate_count": len(
                        inverted_matches
                    ),
                    "correct": correct,
                    "direct_partial_us": (
                        direct_ns / 1_000
                    ),
                    "grid_partial_us": (
                        grid_ns / 1_000
                    ),
                    "inverted_partial_us": (
                        inverted_ns / 1_000
                    ),
                    "full_lookup_us": (
                        full_ns / 1_000
                    ),
                    "direct_vs_grid_ratio": (
                        direct_ns / grid_ns
                        if grid_ns > 0
                        else None
                    ),
                    "direct_vs_inverted_ratio": (
                        direct_ns / inverted_ns
                        if inverted_ns > 0
                        else None
                    ),
                }
            )

    summary_rows = []

    for requested_axis_count in PARTIAL_AXIS_COUNTS:
        selected = [
            row
            for row in rows
            if row["requested_axis_count"]
            == requested_axis_count
        ]

        summary_rows.append(
            {
                "bit_size": bit_size,
                "prime_count": len(primes),
                "requested_axis_count": (
                    requested_axis_count
                ),
                "actual_axis_count": selected[0][
                    "actual_axis_count"
                ],
                "all_correct": all(
                    row["correct"]
                    for row in selected
                ),
                "median_candidate_count": (
                    statistics.median(
                        row["candidate_count"]
                        for row in selected
                    )
                ),
                "max_candidate_count": max(
                    row["candidate_count"]
                    for row in selected
                ),
                "median_direct_partial_us": (
                    statistics.median(
                        row["direct_partial_us"]
                        for row in selected
                    )
                ),
                "median_grid_partial_us": (
                    statistics.median(
                        row["grid_partial_us"]
                        for row in selected
                    )
                ),
                "median_inverted_partial_us": (
                    statistics.median(
                        row["inverted_partial_us"]
                        for row in selected
                    )
                ),
                "median_full_lookup_us": (
                    statistics.median(
                        row["full_lookup_us"]
                        for row in selected
                    )
                ),
                "median_direct_vs_grid_ratio": (
                    statistics.median(
                        row["direct_vs_grid_ratio"]
                        for row in selected
                    )
                ),
                "median_direct_vs_inverted_ratio": (
                    statistics.median(
                        row[
                            "direct_vs_inverted_ratio"
                        ]
                        for row in selected
                    )
                ),
                "grid_build_ms": (
                    grid_build_ns / 1_000_000
                ),
                "inverted_build_ms": (
                    inverted_build_ns / 1_000_000
                ),
                "full_index_build_ms": (
                    full_index_build_ns
                    / 1_000_000
                ),
                "serialized_grid_bytes": (
                    serialized_grid_bytes
                ),
                "peak_memory_bytes": (
                    peak_memory_bytes
                ),
            }
        )

    return rows, summary_rows


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
    print("IKERUSIKI Verification054")
    print("Boundary Coordinate Grid Search Benchmark")
    print()

    total_start = time.perf_counter()
    all_rows = []
    all_summaries = []

    for bit_size in BIT_SIZES:
        primes = load_prime_corpus(bit_size)

        rows, summaries = benchmark_bit_size(
            bit_size,
            primes,
        )

        all_rows.extend(rows)
        all_summaries.extend(summaries)

        for summary in summaries:
            print(
                f'{bit_size:>4}-bit | '
                f'primes={summary["prime_count"]} | '
                f'axes={summary["actual_axis_count"]} | '
                f'candidates='
                f'{summary["median_candidate_count"]} | '
                f'direct='
                f'{summary["median_direct_partial_us"]:.3f} us | '
                f'grid='
                f'{summary["median_grid_partial_us"]:.3f} us | '
                f'inverted='
                f'{summary["median_inverted_partial_us"]:.3f} us | '
                f'full='
                f'{summary["median_full_lookup_us"]:.3f} us | '
                f'correct={summary["all_correct"]}'
            )

    base = Path(__file__).resolve().parent

    write_csv(
        base / "verification054_results.csv",
        all_rows,
    )
    write_csv(
        base / "verification054_summary.csv",
        all_summaries,
    )

    print()
    print("Verification054 Summary")
    print(
        "All search methods matched:",
        all(
            row["all_correct"]
            for row in all_summaries
        ),
    )
    print(
        "Total elapsed seconds:",
        f"{time.perf_counter() - total_start:.6f}",
    )


if __name__ == "__main__":
    main()
