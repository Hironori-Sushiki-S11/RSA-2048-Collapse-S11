# IKERUSIKI Verification 056
# Boundary Address Entropy and Information Gain
#
# Objective:
# Quantify the finite-corpus identifying information carried by each
# Boundary Address axis and by cumulative address prefixes.
#
# Measures:
# 1. Single-axis Shannon entropy
# 2. Cumulative prefix entropy
# 3. Marginal information gain from each added axis
# 4. Remaining ambiguity
# 5. Effective distinguishable-state count
# 6. First prefix reaching complete corpus information
#
# Scope:
# - Uses the verified prime corpora from Verification053-055
# - 512 / 1024 / 2048 / 4096-bit primes
# - Boundary Address axes 2..512
# - Finite-corpus empirical entropy only
#
# Important:
# These measurements describe only the supplied finite corpora. They do
# not prove entropy, independence, or uniqueness over all primes.

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
        raise FileNotFoundError(f"Required corpus file not found: {path.name}")

    primes = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
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


def full_address(prime):
    return tuple(boundary_component(prime, axis) for axis in AXES)


def shannon_entropy(values):
    counts = Counter(values)
    total = len(values)
    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def benchmark_bit_size(bit_size, primes):
    start = time.perf_counter_ns()
    addresses = [full_address(prime) for prime in primes]
    build_ns = time.perf_counter_ns() - start

    corpus_bits = math.log2(len(primes))
    previous_prefix_entropy = 0.0
    rows = []
    first_complete = None

    for position, axis in enumerate(AXES, start=1):
        axis_index = position - 1
        components = [address[axis_index] for address in addresses]
        prefixes = [address[:position] for address in addresses]

        axis_entropy = shannon_entropy(components)
        prefix_entropy = shannon_entropy(prefixes)
        marginal_gain = prefix_entropy - previous_prefix_entropy
        prefix_counts = Counter(prefixes)
        unique_count = sum(1 for count in prefix_counts.values() if count == 1)

        row = {
            "bit_size": bit_size,
            "prime_count": len(primes),
            "axis_position": position,
            "axis": axis,
            "component_state_count": len(set(components)),
            "single_axis_entropy_bits": axis_entropy,
            "single_axis_normalized_entropy": (
                axis_entropy / corpus_bits if corpus_bits > 0 else 0.0
            ),
            "prefix_state_count": len(prefix_counts),
            "cumulative_prefix_entropy_bits": prefix_entropy,
            "cumulative_information_fraction": (
                prefix_entropy / corpus_bits if corpus_bits > 0 else 0.0
            ),
            "marginal_information_gain_bits": marginal_gain,
            "remaining_ambiguity_bits": max(0.0, corpus_bits - prefix_entropy),
            "effective_distinguishable_states": 2 ** prefix_entropy,
            "unique_prefix_count": unique_count,
            "unique_prefix_ratio": unique_count / len(primes),
        }
        rows.append(row)

        if first_complete is None and math.isclose(
            prefix_entropy, corpus_bits, rel_tol=1e-12, abs_tol=1e-12
        ):
            first_complete = position

        previous_prefix_entropy = prefix_entropy

    single_ranked = sorted(
        rows,
        key=lambda row: (row["single_axis_entropy_bits"], -row["axis_position"]),
        reverse=True,
    )
    gain_ranked = sorted(
        rows,
        key=lambda row: (row["marginal_information_gain_bits"], -row["axis_position"]),
        reverse=True,
    )

    for rank, row in enumerate(single_ranked, start=1):
        row["single_axis_entropy_rank"] = rank
    for rank, row in enumerate(gain_ranked, start=1):
        row["marginal_gain_rank"] = rank

    positive_gains = [
        row["marginal_information_gain_bits"]
        for row in rows
        if row["marginal_information_gain_bits"] > 1e-15
    ]
    top_single = single_ranked[0]
    top_gain = gain_ranked[0]

    summary = {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "corpus_information_bits": corpus_bits,
        "address_axis_count": len(AXES),
        "first_complete_prefix_axis_count": first_complete,
        "first_complete_prefix_last_axis": (
            AXES[first_complete - 1] if first_complete is not None else None
        ),
        "top_single_entropy_axis": top_single["axis"],
        "top_single_entropy_bits": top_single["single_axis_entropy_bits"],
        "top_marginal_gain_axis": top_gain["axis"],
        "top_marginal_gain_bits": top_gain["marginal_information_gain_bits"],
        "positive_marginal_gain_axis_count": len(positive_gains),
        "median_positive_marginal_gain_bits": (
            statistics.median(positive_gains) if positive_gains else 0.0
        ),
        "final_prefix_entropy_bits": rows[-1]["cumulative_prefix_entropy_bits"],
        "final_information_fraction": rows[-1]["cumulative_information_fraction"],
        "final_unique_prefix_ratio": rows[-1]["unique_prefix_ratio"],
        "address_build_total_ms": build_ns / 1_000_000,
        "address_build_per_prime_us": build_ns / len(primes) / 1_000,
    }
    return rows, summary


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    print("IKERUSIKI Verification056")
    print("Boundary Address Entropy and Information Gain")
    print()

    total_start = time.perf_counter()
    all_rows = []
    summaries = []

    for bit_size in BIT_SIZES:
        primes = load_prime_corpus(bit_size)
        rows, summary = benchmark_bit_size(bit_size, primes)
        all_rows.extend(rows)
        summaries.append(summary)

        print(
            f'{bit_size:>4}-bit | primes={summary["prime_count"]} | '
            f'corpus info={summary["corpus_information_bits"]:.3f} bits | '
            f'complete prefix={summary["first_complete_prefix_axis_count"]} axes | '
            f'last axis={summary["first_complete_prefix_last_axis"]} | '
            f'top single axis={summary["top_single_entropy_axis"]} '
            f'({summary["top_single_entropy_bits"]:.3f} bits) | '
            f'final info={summary["final_information_fraction"]:.3f}'
        )

    base = Path(__file__).resolve().parent
    write_csv(base / "verification056_axis_entropy.csv", all_rows)
    write_csv(base / "verification056_summary.csv", summaries)

    print()
    print("Verification056 Summary")
    print(
        "All supplied corpora reached complete corpus information:",
        all(s["first_complete_prefix_axis_count"] is not None for s in summaries),
    )
    print(
        "All final information fractions equal 1:",
        all(
            math.isclose(
                s["final_information_fraction"],
                1.0,
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
            for s in summaries
        ),
    )
    print("Total elapsed seconds:", f"{time.perf_counter() - total_start:.6f}")


if __name__ == "__main__":
    main()
