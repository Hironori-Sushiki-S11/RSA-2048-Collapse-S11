# IKERUSIKI Verification 060
# Boundary Address Research Final Integration
#
# Objective:
# Recalculate and integrate the principal findings of Verification053-059
# from the same finite verified prime corpora.
#
# Integrated checks:
# 1. Boundary Address construction
# 2. Full-address collision freedom
# 3. Exact lookup correctness
# 4. Natural-prefix collision convergence
# 5. Corpus information entropy
# 6. Axis entropy ranking
# 7. Greedy compact axis subset
# 8. Storage reduction
# 9. Grid / inverted-index search agreement
# 10. CSV and Markdown final report generation
#
# Scope:
# - 512 / 1024 / 2048 / 4096-bit supplied prime corpora
# - Boundary Address axes 2..512
# - Finite-corpus empirical verification only
#
# Important:
# This final integration summarizes what the supplied corpora demonstrate.
# It does not prove universal uniqueness, global minimality, primality
# recognition, or factorization performance over an unbounded integer range.

import csv
import json
import math
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

BIT_SIZES = [512, 1024, 2048, 4096]
AXES = list(range(2, 513))
SEARCH_AXIS_COUNTS = [4, 8, 16, 32]


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


def addresses_for_indices(component_rows, indices):
    return [
        tuple(row[index] for index in indices)
        for row in component_rows
    ]


def natural_prefix_minimum(component_rows):
    for length in range(1, len(AXES) + 1):
        indices = list(range(length))
        addresses = addresses_for_indices(component_rows, indices)
        if unresolved_pair_count(addresses) == 0:
            return indices
    return list(range(len(AXES)))


def greedy_compact_subset(component_rows):
    selected = []
    remaining = set(range(len(AXES)))
    current_addresses = [tuple() for _ in component_rows]
    current_pairs = unresolved_pair_count(current_addresses)

    while current_pairs > 0:
        best = None

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

            if best is None or score > best[0]:
                best = (
                    score,
                    axis_index,
                    candidate_addresses,
                    candidate_pairs,
                )

        if best is None:
            break

        _, axis_index, current_addresses, current_pairs = best
        selected.append(axis_index)
        remaining.remove(axis_index)

    changed = True
    while changed:
        changed = False

        for axis_index in list(selected):
            trial = [i for i in selected if i != axis_index]
            trial_addresses = addresses_for_indices(
                component_rows,
                trial,
            )
            if unresolved_pair_count(trial_addresses) == 0:
                selected = trial
                changed = True
                break

    return selected


def choose_axis_indices(axis_count):
    if axis_count >= len(AXES):
        return list(range(len(AXES)))

    if axis_count == 1:
        return [0]

    return sorted({
        round(
            index * (len(AXES) - 1)
            / (axis_count - 1)
        )
        for index in range(axis_count)
    })


def build_inverted_index(addresses):
    inverted = {
        axis_index: defaultdict(set)
        for axis_index in range(len(AXES))
    }

    for row_id, address in enumerate(addresses):
        for axis_index, component in enumerate(address):
            inverted[axis_index][component].add(row_id)

    return inverted


def inverted_search(inverted, target_address, selected_indices):
    posting_sets = [
        inverted[axis_index].get(
            target_address[axis_index],
            set(),
        )
        for axis_index in selected_indices
    ]

    if not posting_sets:
        return []

    result = set(posting_sets[0])
    for posting_set in posting_sets[1:]:
        result.intersection_update(posting_set)
        if not result:
            break

    return sorted(result)


def direct_search(primes, target, selected_indices):
    expected = {
        axis_index: boundary_component(
            target,
            AXES[axis_index],
        )
        for axis_index in selected_indices
    }

    matches = []
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


def benchmark_bit_size(bit_size, primes):
    start = time.perf_counter_ns()

    component_rows = [
        tuple(boundary_component(prime, axis) for axis in AXES)
        for prime in primes
    ]
    full_addresses = component_rows

    address_build_ns = time.perf_counter_ns() - start

    full_metrics = address_metrics(full_addresses)
    corpus_information_bits = math.log2(len(primes))

    natural_indices = natural_prefix_minimum(component_rows)
    compact_indices = greedy_compact_subset(component_rows)
    compact_addresses = addresses_for_indices(
        component_rows,
        compact_indices,
    )
    compact_metrics = address_metrics(compact_addresses)

    axis_entropies = []
    for axis_index, axis in enumerate(AXES):
        values = [
            row[axis_index]
            for row in component_rows
        ]
        axis_entropies.append(
            (shannon_entropy(values), axis)
        )

    top_axis_entropy, top_axis = max(
        axis_entropies,
        key=lambda item: (item[0], -item[1]),
    )

    full_index = {
        address: row_id
        for row_id, address in enumerate(full_addresses)
    }
    lookup_correct = all(
        full_index.get(address) == row_id
        for row_id, address in enumerate(full_addresses)
    )

    inverted = build_inverted_index(full_addresses)
    search_agreement = True
    median_candidates = {}

    for axis_count in SEARCH_AXIS_COUNTS:
        selected_indices = choose_axis_indices(axis_count)
        candidate_counts = []

        for row_id, prime in enumerate(primes):
            direct = direct_search(
                primes,
                prime,
                selected_indices,
            )
            indexed = inverted_search(
                inverted,
                full_addresses[row_id],
                selected_indices,
            )

            if direct != indexed or row_id not in indexed:
                search_agreement = False

            candidate_counts.append(len(indexed))

        median_candidates[str(axis_count)] = (
            statistics.median(candidate_counts)
        )

    full_serialized_bytes = len(
        json.dumps(
            full_addresses,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    compact_serialized_bytes = len(
        json.dumps(
            compact_addresses,
            separators=(",", ":"),
        ).encode("utf-8")
    )

    return {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "axis_count": len(AXES),
        "full_distinct_address_count": (
            full_metrics["distinct_address_count"]
        ),
        "full_collision_group_count": (
            full_metrics["collision_group_count"]
        ),
        "full_colliding_prime_count": (
            full_metrics["colliding_prime_count"]
        ),
        "full_unique_address_ratio": (
            full_metrics["unique_address_ratio"]
        ),
        "full_address_entropy_bits": (
            full_metrics["address_entropy_bits"]
        ),
        "corpus_information_bits": corpus_information_bits,
        "entropy_complete": math.isclose(
            full_metrics["address_entropy_bits"],
            corpus_information_bits,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ),
        "exact_lookup_correct": lookup_correct,
        "search_methods_agree": search_agreement,
        "natural_prefix_axis_count": len(natural_indices),
        "natural_prefix_last_axis": AXES[natural_indices[-1]],
        "top_single_entropy_axis": top_axis,
        "top_single_entropy_bits": top_axis_entropy,
        "compact_axis_count": len(compact_indices),
        "compact_axes": "|".join(
            str(AXES[index])
            for index in compact_indices
        ),
        "compact_collision_group_count": (
            compact_metrics["collision_group_count"]
        ),
        "compact_unique_address_ratio": (
            compact_metrics["unique_address_ratio"]
        ),
        "axis_reduction_ratio": (
            len(AXES) / len(compact_indices)
        ),
        "full_serialized_bytes": full_serialized_bytes,
        "compact_serialized_bytes": compact_serialized_bytes,
        "storage_reduction_ratio": (
            full_serialized_bytes / compact_serialized_bytes
        ),
        "median_candidates_4_axes": median_candidates["4"],
        "median_candidates_8_axes": median_candidates["8"],
        "median_candidates_16_axes": median_candidates["16"],
        "median_candidates_32_axes": median_candidates["32"],
        "address_build_total_ms": (
            address_build_ns / 1_000_000
        ),
    }


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


def write_markdown(path, summaries, elapsed_seconds):
    lines = [
        "# IKERUSIKI Verification060 Final Report",
        "",
        "## Scope",
        "",
        "This report integrates Verification053-059 using the supplied finite "
        "prime corpora at 512, 1024, 2048, and 4096 bits.",
        "",
        "It confirms corpus-level Boundary Address construction, collision "
        "analysis, lookup consistency, information measurements, and compact "
        "axis selection. It does not establish universal prime identification "
        "or factorization over an unbounded range.",
        "",
        "## Integrated Results",
        "",
        "| Bits | Primes | Full collisions | Natural prefix axes | Compact axes | Axis reduction | Storage reduction |",
        "|---:|---:|---:|---:|---|---:|---:|",
    ]

    for row in summaries:
        lines.append(
            f'| {row["bit_size"]} | {row["prime_count"]} | '
            f'{row["full_collision_group_count"]} | '
            f'{row["natural_prefix_axis_count"]} | '
            f'{row["compact_axes"]} | '
            f'{row["axis_reduction_ratio"]:.2f}x | '
            f'{row["storage_reduction_ratio"]:.2f}x |'
        )

    lines.extend(
        [
            "",
            "## Final Checks",
            "",
            f'- All full addresses collision-free: '
            f'{all(r["full_collision_group_count"] == 0 for r in summaries)}',
            f'- All compact subsets collision-free: '
            f'{all(r["compact_collision_group_count"] == 0 for r in summaries)}',
            f'- All exact lookups correct: '
            f'{all(r["exact_lookup_correct"] for r in summaries)}',
            f'- All direct and indexed searches agree: '
            f'{all(r["search_methods_agree"] for r in summaries)}',
            f'- All corpora reach complete empirical information: '
            f'{all(r["entropy_complete"] for r in summaries)}',
            "",
            "## Conclusion",
            "",
            "Within each supplied finite corpus, Boundary Addresses were "
            "constructed consistently, full addresses were collision-free, "
            "direct and indexed searches agreed, and compact corpus-specific "
            "axis subsets preserved unique identification.",
            "",
            "These compact subsets are empirical corpus-specific results. "
            "They are not universal minimal axis sets for all primes.",
            "",
            f"Total elapsed seconds: {elapsed_seconds:.6f}",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    print("IKERUSIKI Verification060")
    print("Boundary Address Research Final Integration")
    print()

    total_start = time.perf_counter()
    summaries = []

    for bit_size in BIT_SIZES:
        primes = load_prime_corpus(bit_size)
        summary = benchmark_bit_size(bit_size, primes)
        summaries.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'primes={summary["prime_count"]} | '
            f'collisions={summary["full_collision_group_count"]} | '
            f'natural={summary["natural_prefix_axis_count"]} axes | '
            f'compact=[{summary["compact_axes"]}] | '
            f'axis reduction={summary["axis_reduction_ratio"]:.2f}x | '
            f'storage reduction={summary["storage_reduction_ratio"]:.2f}x | '
            f'lookup={summary["exact_lookup_correct"]} | '
            f'search={summary["search_methods_agree"]}'
        )

    elapsed = time.perf_counter() - total_start
    base = Path(__file__).resolve().parent

    write_csv(
        base / "verification060_summary.csv",
        summaries,
    )
    write_markdown(
        base / "VERIFICATION060_FINAL_REPORT.md",
        summaries,
        elapsed,
    )

    print()
    print("Verification060 Final Checks")
    print(
        "All full addresses collision-free:",
        all(
            row["full_collision_group_count"] == 0
            for row in summaries
        ),
    )
    print(
        "All compact subsets collision-free:",
        all(
            row["compact_collision_group_count"] == 0
            for row in summaries
        ),
    )
    print(
        "All exact lookups correct:",
        all(
            row["exact_lookup_correct"]
            for row in summaries
        ),
    )
    print(
        "All search methods agree:",
        all(
            row["search_methods_agree"]
            for row in summaries
        ),
    )
    print(
        "All empirical entropy complete:",
        all(
            row["entropy_complete"]
            for row in summaries
        ),
    )
    print(
        "Boundary Address series complete:",
        True,
    )
    print(
        "Total elapsed seconds:",
        f"{elapsed:.6f}",
    )


if __name__ == "__main__":
    main()
