# IKERUSIKI Verification 046
# Boundary Coordinate Grid and Inverted Index
#
# Objective:
# Build a coordinate grid for many large integers and evaluate:
# 1. Partial-axis exact-match search
# 2. Structural similarity search
# 3. Full-address hash lookup
# 4. Inverted-index set intersection
#
# Compare precomputed grid/index operations with direct modulo computation.
#
# Scope:
# - 512 to 4096-bit integers
# - 1000 rows per grid
# - maximal prime-power axes
# - benchmark and correctness validation
# - does not alter IKERUSIKI Theory v1.0

import csv
import math
import random
import statistics
import time

BIT_SIZES = [512, 1024, 2048, 4096]
ROWS = 1000
PARTIAL_AXES = 16
SAMPLES_PER_SIZE = 3
SEED = 46026


def informative_radices_for_interval(bit_size):
    interval_width = 1 << (bit_size - 1)
    selected = []
    modulus = 1
    radix = 2

    while modulus <= interval_width:
        new_modulus = math.lcm(modulus, radix)

        if new_modulus > modulus:
            selected.append(radix)
            modulus = new_modulus

        radix += 1

    return selected


def prime_power_base(radix):
    candidate = 2

    while candidate * candidate <= radix:
        value = candidate

        while value < radix:
            value *= candidate

        if value == radix:
            exponent = 0
            value = 1

            while value < radix:
                value *= candidate
                exponent += 1

            return candidate, exponent

        candidate += 1

    return radix, 1


def maximal_prime_power_basis(selected_radices):
    maximal = {}

    for radix in selected_radices:
        prime, exponent = prime_power_base(radix)
        previous = maximal.get(prime)

        if previous is None or exponent > previous[1]:
            maximal[prime] = (radix, exponent)

    return sorted(radix for radix, _ in maximal.values())


def generate_population(bit_size, sample_index):
    rng = random.Random(SEED + bit_size * 100 + sample_index)
    lower_bit = 1 << (bit_size - 1)

    values = []

    while len(values) < ROWS:
        values.append(
            rng.getrandbits(bit_size)
            | lower_bit
            | 1
        )

    return values


def build_grid(values, axes):
    return [
        tuple((value - 1) % axis for axis in axes)
        for value in values
    ]


def build_full_index(grid):
    index = {}

    for row_id, address in enumerate(grid):
        index.setdefault(address, []).append(row_id)

    return index


def build_inverted_index(grid, axes):
    inverted = {
        axis_index: {}
        for axis_index in range(len(axes))
    }

    for row_id, address in enumerate(grid):
        for axis_index, residue in enumerate(address):
            bucket = inverted[axis_index].setdefault(
                residue,
                set(),
            )
            bucket.add(row_id)

    return inverted


def choose_partial_indices(axis_count):
    if axis_count <= PARTIAL_AXES:
        return list(range(axis_count))

    return [
        round(
            index * (axis_count - 1)
            / (PARTIAL_AXES - 1)
        )
        for index in range(PARTIAL_AXES)
    ]


def direct_partial_search(values, axes, target, selected_indices):
    expected = {
        index: (target - 1) % axes[index]
        for index in selected_indices
    }

    matches = []

    for row_id, value in enumerate(values):
        base = value - 1

        for index in selected_indices:
            if base % axes[index] != expected[index]:
                break
        else:
            matches.append(row_id)

    return matches


def grid_partial_search(grid, target_address, selected_indices):
    return [
        row_id
        for row_id, address in enumerate(grid)
        if all(
            address[index] == target_address[index]
            for index in selected_indices
        )
    ]


def inverted_partial_search(
    inverted,
    target_address,
    selected_indices,
):
    sets = [
        inverted[index][target_address[index]]
        for index in selected_indices
    ]

    if not sets:
        return []

    result = set(sets[0])

    for candidate_set in sets[1:]:
        result.intersection_update(candidate_set)

        if not result:
            break

    return sorted(result)


def direct_similarity_search(values, axes, target):
    target_residues = [
        (target - 1) % axis
        for axis in axes
    ]

    best_score = -1
    best_rows = []

    for row_id, value in enumerate(values):
        base = value - 1
        score = sum(
            base % axis == expected
            for axis, expected in zip(
                axes,
                target_residues,
            )
        )

        if score > best_score:
            best_score = score
            best_rows = [row_id]
        elif score == best_score:
            best_rows.append(row_id)

    return best_score, best_rows


def grid_similarity_search(grid, target_address):
    best_score = -1
    best_rows = []

    for row_id, address in enumerate(grid):
        score = sum(
            left == right
            for left, right in zip(
                address,
                target_address,
            )
        )

        if score > best_score:
            best_score = score
            best_rows = [row_id]
        elif score == best_score:
            best_rows.append(row_id)

    return best_score, best_rows


def benchmark_one(bit_size, sample_index):
    values = generate_population(
        bit_size,
        sample_index,
    )
    axes = maximal_prime_power_basis(
        informative_radices_for_interval(bit_size)
    )

    target_row = (
        SEED + bit_size + sample_index
    ) % ROWS
    target = values[target_row]
    selected_indices = choose_partial_indices(len(axes))

    start = time.perf_counter_ns()
    grid = build_grid(values, axes)
    grid_build_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    full_index = build_full_index(grid)
    full_index_build_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    inverted = build_inverted_index(grid, axes)
    inverted_build_ns = time.perf_counter_ns() - start

    target_address = grid[target_row]

    start = time.perf_counter_ns()
    direct_partial = direct_partial_search(
        values,
        axes,
        target,
        selected_indices,
    )
    direct_partial_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    grid_partial = grid_partial_search(
        grid,
        target_address,
        selected_indices,
    )
    grid_partial_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    inverted_partial = inverted_partial_search(
        inverted,
        target_address,
        selected_indices,
    )
    inverted_partial_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    direct_similarity = direct_similarity_search(
        values,
        axes,
        target,
    )
    direct_similarity_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    grid_similarity = grid_similarity_search(
        grid,
        target_address,
    )
    grid_similarity_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    full_matches = full_index.get(
        target_address,
        [],
    )
    full_lookup_ns = time.perf_counter_ns() - start

    correct = (
        direct_partial == grid_partial
        == inverted_partial
        and direct_similarity == grid_similarity
        and target_row in full_matches
    )

    return {
        "correct": correct,
        "axis_count": len(axes),
        "partial_axis_count": len(selected_indices),
        "partial_match_count": len(direct_partial),
        "similarity_score": direct_similarity[0],
        "full_match_count": len(full_matches),
        "grid_build_ns": grid_build_ns,
        "full_index_build_ns": full_index_build_ns,
        "inverted_index_build_ns": inverted_build_ns,
        "direct_partial_ns": direct_partial_ns,
        "grid_partial_ns": grid_partial_ns,
        "inverted_partial_ns": inverted_partial_ns,
        "direct_similarity_ns": direct_similarity_ns,
        "grid_similarity_ns": grid_similarity_ns,
        "full_lookup_ns": full_lookup_ns,
        "partial_grid_speed_ratio": (
            direct_partial_ns / grid_partial_ns
            if grid_partial_ns > 0
            else None
        ),
        "partial_inverted_speed_ratio": (
            direct_partial_ns / inverted_partial_ns
            if inverted_partial_ns > 0
            else None
        ),
        "similarity_speed_ratio": (
            direct_similarity_ns / grid_similarity_ns
            if grid_similarity_ns > 0
            else None
        ),
    }


def main():
    rows = []
    summary_rows = []

    print("IKERUSIKI Verification046")
    print("Boundary Coordinate Grid and Inverted Index")
    print()

    total_start = time.perf_counter()

    for bit_size in BIT_SIZES:
        bit_rows = []

        for sample_index in range(1, SAMPLES_PER_SIZE + 1):
            metrics = benchmark_one(
                bit_size,
                sample_index,
            )

            row = {
                "bit_size": bit_size,
                "sample_index": sample_index,
                "rows": ROWS,
                **metrics,
            }

            rows.append(row)
            bit_rows.append(row)

        summary = {
            "bit_size": bit_size,
            "samples": SAMPLES_PER_SIZE,
            "rows": ROWS,
            "axis_count": bit_rows[0]["axis_count"],
            "partial_axis_count": bit_rows[0]["partial_axis_count"],
            "all_correct": all(row["correct"] for row in bit_rows),
            "median_partial_match_count": statistics.median(
                row["partial_match_count"] for row in bit_rows
            ),
            "median_grid_build_ms": statistics.median(
                row["grid_build_ns"] for row in bit_rows
            ) / 1_000_000,
            "median_inverted_build_ms": statistics.median(
                row["inverted_index_build_ns"] for row in bit_rows
            ) / 1_000_000,
            "median_partial_grid_speed_ratio": statistics.median(
                row["partial_grid_speed_ratio"] for row in bit_rows
            ),
            "median_partial_inverted_speed_ratio": statistics.median(
                row["partial_inverted_speed_ratio"] for row in bit_rows
            ),
            "median_similarity_speed_ratio": statistics.median(
                row["similarity_speed_ratio"] for row in bit_rows
            ),
            "median_full_lookup_us": statistics.median(
                row["full_lookup_ns"] for row in bit_rows
            ) / 1_000,
        }

        summary_rows.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'grid={ROWS}x{summary["axis_count"]} | '
            f'partial matches={summary["median_partial_match_count"]} | '
            f'grid partial={summary["median_partial_grid_speed_ratio"]:.2f}x | '
            f'inverted partial={summary["median_partial_inverted_speed_ratio"]:.2f}x | '
            f'similarity={summary["median_similarity_speed_ratio"]:.2f}x | '
            f'full lookup={summary["median_full_lookup_us"]:.3f} us'
        )

    with open(
        "verification046_results.csv",
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

    with open(
        "verification046_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(summary_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print()
    print("Verification046 Summary")
    print(
        "All grid and index searches matched direct computation:",
        all(row["all_correct"] for row in summary_rows),
    )
    print(
        "Interpretation:",
        "the coordinate grid converts repeated large-integer modular comparison into table lookup, while the inverted index implements candidate reconstruction as set intersection",
    )
    print(
        "Total elapsed seconds:",
        f'{time.perf_counter() - total_start:.6f}',
    )


if __name__ == "__main__":
    main()
