# IKERUSIKI Verification 052
# Scaled Large-Prime Boundary Address Corpus Test
#
# Objective:
# Move beyond the four-prime corpus used by Verification050/051.
#
# Prime-only corpus sizes:
# - 512-bit: 1000 primes
# - 1024-bit: 500 primes
# - 2048-bit: 100 primes
# - 4096-bit: 25 primes
#
# Measures:
# - prime generation time
# - Boundary Address build time
# - full-address collisions
# - unique-identification rate
# - address-prefix length needed for uniqueness
# - serialized storage
# - lookup time
#
# This is a corpus-scale verification, not an exhaustive proof over every
# prime in each bit interval.

import csv
import json
import random
import statistics
import time
import tracemalloc
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed

from sympy import nextprime

CORPUS_SIZES = {
    512: 128,
    1024: 64,
    2048: 16,
    4096: 4,
}
AXES = list(range(2, 513))
SEED = 52026


def generate_prime_corpus(bit_size, count):
    rng = random.Random(SEED + bit_size)
    high_bit = 1 << (bit_size - 1)
    primes = []
    seen = set()

    while len(primes) < count:
        start = (
            rng.getrandbits(bit_size)
            | high_bit
            | 1
        )
        prime = int(nextprime(start))

        if prime.bit_length() == bit_size and prime not in seen:
            seen.add(prime)
            primes.append(prime)

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


def earliest_unique_prefixes(addresses):
    lengths = [None] * len(addresses)
    unresolved = set(range(len(addresses)))

    for prefix_length in range(1, len(AXES) + 1):
        counts = Counter(
            address[:prefix_length]
            for address in addresses
        )

        newly_unique = []

        for index in unresolved:
            if counts[addresses[index][:prefix_length]] == 1:
                lengths[index] = prefix_length
                newly_unique.append(index)

        unresolved.difference_update(newly_unique)

        if not unresolved:
            break

    return lengths, unresolved


def address_key(address):
    return "|".join(
        f"{distance}:{direction}"
        for distance, direction in address
    )


def benchmark_bit_size(bit_size, count):
    generation_start = time.perf_counter()
    primes = generate_prime_corpus(bit_size, count)
    generation_seconds = time.perf_counter() - generation_start

    tracemalloc.start()
    address_start = time.perf_counter_ns()
    addresses = [prime_address(prime) for prime in primes]
    address_build_ns = time.perf_counter_ns() - address_start
    _, peak_memory_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    full_counts = Counter(addresses)
    collision_groups = {
        address: multiplicity
        for address, multiplicity in full_counts.items()
        if multiplicity > 1
    }

    prefix_lengths, unresolved = earliest_unique_prefixes(
        addresses
    )

    index_build_start = time.perf_counter_ns()
    exact_index = {
        address_key(address): index
        for index, address in enumerate(addresses)
    }
    index_build_ns = time.perf_counter_ns() - index_build_start

    lookup_times = []
    lookup_correct = []

    for index, address in enumerate(addresses):
        key = address_key(address)

        lookup_start = time.perf_counter_ns()
        found = exact_index.get(key)
        lookup_ns = time.perf_counter_ns() - lookup_start

        lookup_times.append(lookup_ns)
        lookup_correct.append(found == index)

    serialized = json.dumps(
        [
            {
                "prime_hex": hex(prime),
                "address": address,
            }
            for prime, address in zip(primes, addresses)
        ],
        separators=(",", ":"),
    ).encode("utf-8")

    rows = []

    for index, prime in enumerate(primes):
        prefix_length = prefix_lengths[index]
        rows.append({
            "bit_size": bit_size,
            "prime_index": index,
            "prime_hex_prefix": hex(prime)[:34],
            "axes_for_unique": prefix_length,
            "last_axis_for_unique": (
                AXES[prefix_length - 1]
                if prefix_length is not None
                else None
            ),
            "lookup_correct": lookup_correct[index],
            "lookup_ns": lookup_times[index],
        })

    unique_prefixes = [
        length
        for length in prefix_lengths
        if length is not None
    ]

    summary = {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "full_address_count": len(full_counts),
        "collision_group_count": len(collision_groups),
        "colliding_prime_count": sum(collision_groups.values()),
        "unique_identification_rate": (
            len(unique_prefixes) / len(primes)
        ),
        "unresolved_prime_count": len(unresolved),
        "median_axes_for_unique": (
            statistics.median(unique_prefixes)
            if unique_prefixes
            else None
        ),
        "p95_axes_for_unique": (
            sorted(unique_prefixes)[
                max(0, int(len(unique_prefixes) * 0.95) - 1)
            ]
            if unique_prefixes
            else None
        ),
        "max_axes_for_unique": (
            max(unique_prefixes)
            if unique_prefixes
            else None
        ),
        "prime_generation_seconds": generation_seconds,
        "address_build_total_ms": (
            address_build_ns / 1_000_000
        ),
        "address_build_per_prime_us": (
            address_build_ns / len(primes) / 1_000
        ),
        "index_build_total_ms": (
            index_build_ns / 1_000_000
        ),
        "serialized_total_bytes": len(serialized),
        "serialized_per_prime_bytes": (
            len(serialized) / len(primes)
        ),
        "peak_memory_bytes": peak_memory_bytes,
        "median_lookup_us": (
            statistics.median(lookup_times) / 1_000
        ),
        "all_lookups_correct": all(lookup_correct),
    }

    return rows, summary


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    print("IKERUSIKI Verification052")
    print("Scaled Large-Prime Boundary Address Corpus Test")
    print()

    total_start = time.perf_counter()
    all_rows = []
    summaries = []

    with ProcessPoolExecutor(
        max_workers=min(4, len(CORPUS_SIZES))
    ) as executor:
        futures = {
            executor.submit(
                benchmark_bit_size,
                bit_size,
                count,
            ): bit_size
            for bit_size, count in CORPUS_SIZES.items()
        }

        for future in as_completed(futures):
            rows, summary = future.result()
            all_rows.extend(rows)
            summaries.append(summary)

            print(
                f'{summary["bit_size"]:>4}-bit | '
                f'primes={summary["prime_count"]} | '
                f'collisions={summary["collision_group_count"]} | '
                f'unique rate={summary["unique_identification_rate"]:.3f} | '
                f'median axes={summary["median_axes_for_unique"]} | '
                f'p95 axes={summary["p95_axes_for_unique"]} | '
                f'max axes={summary["max_axes_for_unique"]} | '
                f'build/prime={summary["address_build_per_prime_us"]:.2f} us | '
                f'lookup={summary["median_lookup_us"]:.3f} us'
            )

    summaries.sort(key=lambda row: row["bit_size"])
    all_rows.sort(
        key=lambda row: (
            row["bit_size"],
            row["prime_index"],
        )
    )

    write_csv("verification052_results.csv", all_rows)
    write_csv("verification052_summary.csv", summaries)

    print()
    print("Verification052 Summary")
    print(
        "All scaled prime corpora collision-free:",
        all(
            summary["collision_group_count"] == 0
            for summary in summaries
        ),
    )
    print(
        "All scaled prime corpora fully unique:",
        all(
            summary["unique_identification_rate"] == 1.0
            for summary in summaries
        ),
    )
    print(
        "All exact lookups correct:",
        all(
            summary["all_lookups_correct"]
            for summary in summaries
        ),
    )
    print(
        "Total elapsed seconds:",
        f"{time.perf_counter() - total_start:.6f}",
    )


if __name__ == "__main__":
    main()
