# IKERUSIKI Verification 045
# Repeated Candidate-Filtering Benchmark
#
# Objective:
# Measure whether precomputed Boundary / residue addresses accelerate an
# actual repeated filtering workload over many large integers.
#
# Workload:
# - Build a population containing one target plus random integers.
# - Repeatedly filter the same population against selected target residues.
# - Compare:
#   1. Direct modulo filtering on every pass.
#   2. Precomputed residue-address filtering.
#
# Metrics:
# - identical survivor sets
# - build time
# - direct filtering time
# - address filtering time
# - end-to-end time including address construction
# - break-even pass count
#
# Scope:
# - 512 to 8192-bit integers
# - repeated use of the same candidate population
# - benchmark only
# - does not alter IKERUSIKI Theory v1.0

import csv
import math
import random
import statistics
import time

BIT_SIZES = [512, 1024, 2048, 4096, 8192]
POPULATION_SIZE = 1200
FILTER_AXES_COUNT = 24
FILTER_PASSES = 100
SAMPLES_PER_SIZE = 3
SEED = 45026


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

    target = (
        rng.getrandbits(bit_size)
        | lower_bit
        | 1
    )

    population = [target]

    while len(population) < POPULATION_SIZE:
        population.append(
            rng.getrandbits(bit_size)
            | lower_bit
            | 1
        )

    rng.shuffle(population)
    return target, population


def choose_filter_axes(all_axes):
    if len(all_axes) <= FILTER_AXES_COUNT:
        return list(all_axes)

    # Spread selected axes across the retained basis.
    indices = [
        round(i * (len(all_axes) - 1) / (FILTER_AXES_COUNT - 1))
        for i in range(FILTER_AXES_COUNT)
    ]
    return [all_axes[index] for index in indices]


def target_signature(target, axes):
    value = target - 1
    return tuple(value % axis for axis in axes)


def direct_filter(population, axes, signature):
    survivors = []

    for candidate in population:
        value = candidate - 1

        for axis, expected in zip(axes, signature):
            if value % axis != expected:
                break
        else:
            survivors.append(candidate)

    return survivors


def build_population_addresses(population, axes):
    addresses = []

    for candidate in population:
        value = candidate - 1
        addresses.append(
            tuple(value % axis for axis in axes)
        )

    return addresses


def address_filter(population, addresses, signature):
    return [
        candidate
        for candidate, address in zip(population, addresses)
        if address == signature
    ]


def benchmark_one(bit_size, sample_index):
    target, population = generate_population(
        bit_size,
        sample_index,
    )

    all_axes = maximal_prime_power_basis(
        informative_radices_for_interval(bit_size)
    )
    axes = choose_filter_axes(all_axes)
    signature = target_signature(target, axes)

    # Verify once outside timing.
    reference = direct_filter(population, axes, signature)

    start = time.perf_counter_ns()
    addresses = build_population_addresses(population, axes)
    build_ns = time.perf_counter_ns() - start

    address_reference = address_filter(
        population,
        addresses,
        signature,
    )

    start = time.perf_counter_ns()
    direct_checksum = 0

    for _ in range(FILTER_PASSES):
        survivors = direct_filter(
            population,
            axes,
            signature,
        )
        direct_checksum ^= len(survivors)

    direct_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    address_checksum = 0

    for _ in range(FILTER_PASSES):
        survivors = address_filter(
            population,
            addresses,
            signature,
        )
        address_checksum ^= len(survivors)

    address_ns = time.perf_counter_ns() - start

    correct = (
        reference == address_reference
        and direct_checksum == address_checksum
        and target in reference
    )

    direct_per_pass = direct_ns / FILTER_PASSES
    address_per_pass = address_ns / FILTER_PASSES
    saving_per_pass = direct_per_pass - address_per_pass

    break_even_passes = (
        math.ceil(build_ns / saving_per_pass)
        if saving_per_pass > 0
        else None
    )

    return {
        "correct": correct,
        "axis_count": len(axes),
        "survivor_count": len(reference),
        "build_ns": build_ns,
        "direct_ns": direct_ns,
        "address_ns": address_ns,
        "direct_per_pass_ns": direct_per_pass,
        "address_per_pass_ns": address_per_pass,
        "filter_speed_ratio": (
            direct_ns / address_ns
            if address_ns > 0
            else None
        ),
        "end_to_end_address_ns": build_ns + address_ns,
        "end_to_end_ratio": (
            direct_ns / (build_ns + address_ns)
            if build_ns + address_ns > 0
            else None
        ),
        "break_even_passes": break_even_passes,
    }


def main():
    rows = []
    summary_rows = []

    print("IKERUSIKI Verification045")
    print("Repeated Candidate-Filtering Benchmark")
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
                "population_size": POPULATION_SIZE,
                "filter_axes": metrics["axis_count"],
                "filter_passes": FILTER_PASSES,
                "survivor_count": metrics["survivor_count"],
                "correct": metrics["correct"],
                "build_ns": metrics["build_ns"],
                "direct_ns": metrics["direct_ns"],
                "address_ns": metrics["address_ns"],
                "direct_per_pass_ns": metrics["direct_per_pass_ns"],
                "address_per_pass_ns": metrics["address_per_pass_ns"],
                "filter_speed_ratio": metrics["filter_speed_ratio"],
                "end_to_end_address_ns": metrics["end_to_end_address_ns"],
                "end_to_end_ratio": metrics["end_to_end_ratio"],
                "break_even_passes": metrics["break_even_passes"],
            }

            rows.append(row)
            bit_rows.append(row)

        summary = {
            "bit_size": bit_size,
            "samples": SAMPLES_PER_SIZE,
            "population_size": POPULATION_SIZE,
            "filter_axes": bit_rows[0]["filter_axes"],
            "filter_passes": FILTER_PASSES,
            "all_correct": all(row["correct"] for row in bit_rows),
            "median_survivor_count": statistics.median(
                row["survivor_count"] for row in bit_rows
            ),
            "median_build_ms": statistics.median(
                row["build_ns"] for row in bit_rows
            ) / 1_000_000,
            "median_direct_per_pass_ms": statistics.median(
                row["direct_per_pass_ns"] for row in bit_rows
            ) / 1_000_000,
            "median_address_per_pass_ms": statistics.median(
                row["address_per_pass_ns"] for row in bit_rows
            ) / 1_000_000,
            "median_filter_speed_ratio": statistics.median(
                row["filter_speed_ratio"] for row in bit_rows
            ),
            "median_end_to_end_ratio": statistics.median(
                row["end_to_end_ratio"] for row in bit_rows
            ),
            "median_break_even_passes": statistics.median(
                row["break_even_passes"] for row in bit_rows
                if row["break_even_passes"] is not None
            ),
        }

        summary_rows.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'population={POPULATION_SIZE} | '
            f'axes={summary["filter_axes"]} | '
            f'survivors={summary["median_survivor_count"]} | '
            f'direct/pass={summary["median_direct_per_pass_ms"]:.4f} ms | '
            f'address/pass={summary["median_address_per_pass_ms"]:.4f} ms | '
            f'filter speed={summary["median_filter_speed_ratio"]:.2f}x | '
            f'end-to-end={summary["median_end_to_end_ratio"]:.2f}x | '
            f'break-even={summary["median_break_even_passes"]}'
        )

    with open(
        "verification045_results.csv",
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
        "verification045_summary.csv",
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
    print("Verification045 Summary")
    print(
        "All survivor sets identical:",
        all(row["all_correct"] for row in summary_rows),
    )
    print(
        "Address method faster end-to-end at configured pass count:",
        all(row["median_end_to_end_ratio"] > 1 for row in summary_rows),
    )
    print(
        "Interpretation:",
        "precomputed addresses accelerate repeated filtering of a reused candidate population, while one-pass workloads still pay construction cost",
    )
    print(
        "Total elapsed seconds:",
        f'{time.perf_counter() - total_start:.6f}',
    )


if __name__ == "__main__":
    main()
