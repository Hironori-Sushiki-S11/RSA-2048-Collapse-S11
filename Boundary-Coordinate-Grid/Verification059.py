# IKERUSIKI Verification 059
# Minimal Boundary Address Axis Set
#
# Objective:
# Find a compact axis subset that preserves unique identification inside each
# supplied finite prime corpus.
#
# Method:
# 1. Build all Boundary Address components for axes 2..512.
# 2. Rank candidate axes greedily by the largest reduction of unresolved
#    collision pairs.
# 3. Add the best axis until all supplied primes are uniquely identified.
# 4. Remove any selected axis that is no longer necessary.
# 5. Compare the optimized subset with the natural prefix order.
#
# Measures:
# - selected axis count
# - selected axes
# - collision groups and colliding primes after every step
# - unique-address ratio
# - information entropy
# - serialized storage
# - build and lookup time
#
# Scope:
# - Uses verified prime corpora from Verification053-058
# - 512 / 1024 / 2048 / 4096-bit primes
# - Boundary Address axes 2..512
# - Finite-corpus empirical verification only
#
# Important:
# The resulting subset is minimal under the implemented greedy selection and
# backward-elimination procedure for each supplied corpus. It is not a proof
# of the globally smallest subset over all possible axis combinations or all
# primes in an unbounded interval.

import csv
import json
import math
import statistics
import time
import tracemalloc
from collections import Counter
from pathlib import Path

BIT_SIZES = [512, 1024, 2048, 4096]
AXES = list(range(2, 513))
LOOKUP_REPEATS = 500


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


def addresses_for_indices(component_rows, axis_indices):
    return [
        tuple(row[index] for index in axis_indices)
        for row in component_rows
    ]


def address_metrics(addresses):
    counts = Counter(addresses)
    bucket_sizes = list(counts.values())
    collision_sizes = [size for size in bucket_sizes if size > 1]

    return {
        "distinct_address_count": len(counts),
        "collision_group_count": len(collision_sizes),
        "colliding_prime_count": sum(collision_sizes),
        "unique_prime_count": sum(
            1 for size in bucket_sizes if size == 1
        ),
        "unique_address_ratio": sum(
            1 for size in bucket_sizes if size == 1
        ) / len(addresses),
        "largest_bucket_size": max(bucket_sizes),
        "address_entropy_bits": shannon_entropy(addresses),
    }


def unresolved_pair_count(addresses):
    counts = Counter(addresses)
    return sum(
        count * (count - 1) // 2
        for count in counts.values()
        if count > 1
    )


def greedy_select_axes(component_rows):
    selected = []
    remaining = set(range(len(AXES)))
    rows = []

    current_addresses = [tuple() for _ in component_rows]
    current_pairs = unresolved_pair_count(current_addresses)

    while current_pairs > 0:
        best_index = None
        best_addresses = None
        best_pairs = None
        best_entropy = None

        for axis_index in sorted(remaining):
            candidate_addresses = [
                current_addresses[row_id]
                + (component_rows[row_id][axis_index],)
                for row_id in range(len(component_rows))
            ]
            candidate_pairs = unresolved_pair_count(candidate_addresses)
            candidate_entropy = shannon_entropy(candidate_addresses)

            score = (
                current_pairs - candidate_pairs,
                candidate_entropy,
                -AXES[axis_index],
            )

            if best_index is None:
                best_index = axis_index
                best_addresses = candidate_addresses
                best_pairs = candidate_pairs
                best_entropy = candidate_entropy
                best_score = score
            elif score > best_score:
                best_index = axis_index
                best_addresses = candidate_addresses
                best_pairs = candidate_pairs
                best_entropy = candidate_entropy
                best_score = score

        if best_index is None:
            break

        selected.append(best_index)
        remaining.remove(best_index)
        current_addresses = best_addresses
        reduction = current_pairs - best_pairs
        current_pairs = best_pairs
        metrics = address_metrics(current_addresses)

        rows.append(
            {
                "selection_step": len(selected),
                "selected_axis": AXES[best_index],
                "unresolved_pair_reduction": reduction,
                "unresolved_pair_count": current_pairs,
                **metrics,
            }
        )

    return selected, rows


def backward_eliminate(component_rows, selected_indices):
    selected = list(selected_indices)
    changed = True

    while changed:
        changed = False

        for axis_index in list(selected):
            trial = [
                index for index in selected
                if index != axis_index
            ]
            trial_addresses = addresses_for_indices(
                component_rows,
                trial,
            )

            if unresolved_pair_count(trial_addresses) == 0:
                selected = trial
                changed = True
                break

    return selected


def natural_prefix_minimum(component_rows):
    for length in range(1, len(AXES) + 1):
        indices = list(range(length))
        addresses = addresses_for_indices(
            component_rows,
            indices,
        )
        if unresolved_pair_count(addresses) == 0:
            return indices
    return list(range(len(AXES)))


def benchmark_lookup(addresses):
    index = {
        address: row_id
        for row_id, address in enumerate(addresses)
    }

    timings = []
    correct = []

    for row_id, address in enumerate(addresses):
        for _ in range(LOOKUP_REPEATS):
            start = time.perf_counter_ns()
            found = index.get(address)
            timings.append(time.perf_counter_ns() - start)
            correct.append(found == row_id)

    return statistics.median(timings), all(correct)


def benchmark_bit_size(bit_size, primes):
    tracemalloc.start()

    start = time.perf_counter_ns()
    component_rows = [
        tuple(boundary_component(prime, axis) for axis in AXES)
        for prime in primes
    ]
    full_build_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    greedy_indices, curve_rows = greedy_select_axes(component_rows)
    greedy_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    compact_indices = backward_eliminate(
        component_rows,
        greedy_indices,
    )
    elimination_ns = time.perf_counter_ns() - start

    natural_indices = natural_prefix_minimum(component_rows)

    compact_addresses = addresses_for_indices(
        component_rows,
        compact_indices,
    )
    natural_addresses = addresses_for_indices(
        component_rows,
        natural_indices,
    )
    full_addresses = addresses_for_indices(
        component_rows,
        list(range(len(AXES))),
    )

    compact_metrics = address_metrics(compact_addresses)
    natural_metrics = address_metrics(natural_addresses)
    full_metrics = address_metrics(full_addresses)

    compact_lookup_ns, compact_lookup_correct = benchmark_lookup(
        compact_addresses
    )
    full_lookup_ns, full_lookup_correct = benchmark_lookup(
        full_addresses
    )

    compact_serialized_bytes = len(
        json.dumps(
            compact_addresses,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    full_serialized_bytes = len(
        json.dumps(
            full_addresses,
            separators=(",", ":"),
        ).encode("utf-8")
    )

    _, peak_memory_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    for row in curve_rows:
        row["bit_size"] = bit_size
        row["prime_count"] = len(primes)

    summary = {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "full_axis_count": len(AXES),
        "greedy_axis_count_before_elimination": len(greedy_indices),
        "compact_axis_count": len(compact_indices),
        "compact_axes": "|".join(
            str(AXES[index]) for index in compact_indices
        ),
        "natural_prefix_axis_count": len(natural_indices),
        "natural_prefix_last_axis": AXES[natural_indices[-1]],
        "axis_count_reduction_ratio": (
            len(AXES) / len(compact_indices)
        ),
        "axis_fraction_retained": (
            len(compact_indices) / len(AXES)
        ),
        "compact_collision_group_count": (
            compact_metrics["collision_group_count"]
        ),
        "compact_colliding_prime_count": (
            compact_metrics["colliding_prime_count"]
        ),
        "compact_unique_address_ratio": (
            compact_metrics["unique_address_ratio"]
        ),
        "compact_largest_bucket_size": (
            compact_metrics["largest_bucket_size"]
        ),
        "compact_address_entropy_bits": (
            compact_metrics["address_entropy_bits"]
        ),
        "natural_collision_group_count": (
            natural_metrics["collision_group_count"]
        ),
        "full_collision_group_count": (
            full_metrics["collision_group_count"]
        ),
        "compact_serialized_bytes": compact_serialized_bytes,
        "full_serialized_bytes": full_serialized_bytes,
        "storage_reduction_ratio": (
            full_serialized_bytes / compact_serialized_bytes
        ),
        "compact_lookup_median_us": (
            compact_lookup_ns / 1_000
        ),
        "full_lookup_median_us": (
            full_lookup_ns / 1_000
        ),
        "compact_lookup_correct": compact_lookup_correct,
        "full_lookup_correct": full_lookup_correct,
        "full_component_build_ms": (
            full_build_ns / 1_000_000
        ),
        "greedy_selection_ms": (
            greedy_ns / 1_000_000
        ),
        "backward_elimination_ms": (
            elimination_ns / 1_000_000
        ),
        "peak_memory_bytes": peak_memory_bytes,
    }

    return curve_rows, summary


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
    print("IKERUSIKI Verification059")
    print("Minimal Boundary Address Axis Set")
    print()

    total_start = time.perf_counter()
    all_curve_rows = []
    summaries = []

    for bit_size in BIT_SIZES:
        primes = load_prime_corpus(bit_size)
        curve_rows, summary = benchmark_bit_size(
            bit_size,
            primes,
        )

        all_curve_rows.extend(curve_rows)
        summaries.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'primes={summary["prime_count"]} | '
            f'compact axes={summary["compact_axis_count"]} '
            f'[{summary["compact_axes"]}] | '
            f'natural prefix={summary["natural_prefix_axis_count"]} | '
            f'axis reduction={summary["axis_count_reduction_ratio"]:.2f}x | '
            f'storage reduction={summary["storage_reduction_ratio"]:.2f}x | '
            f'unique={summary["compact_unique_address_ratio"]:.3f} | '
            f'lookup={summary["compact_lookup_median_us"]:.3f} us'
        )

    base = Path(__file__).resolve().parent

    write_csv(
        base / "verification059_selection_curve.csv",
        all_curve_rows,
    )
    write_csv(
        base / "verification059_summary.csv",
        summaries,
    )

    print()
    print("Verification059 Summary")
    print(
        "All compact subsets collision-free:",
        all(
            summary["compact_collision_group_count"] == 0
            for summary in summaries
        ),
    )
    print(
        "All compact lookups correct:",
        all(
            summary["compact_lookup_correct"]
            for summary in summaries
        ),
    )
    print(
        "Total elapsed seconds:",
        f"{time.perf_counter() - total_start:.6f}",
    )


if __name__ == "__main__":
    main()
