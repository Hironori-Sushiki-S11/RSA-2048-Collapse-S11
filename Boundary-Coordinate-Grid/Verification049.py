# IKERUSIKI Verification 049
# Exhaustive Prime Address Collision Test
#
# Objective:
# Exhaustively verify prime-address uniqueness for every prime in a finite
# domain, rather than testing a sample of target primes.
#
# For every prime p <= LIMIT:
# 1. Construct the hierarchical Boundary Address over axes 2..64.
# 2. Count complete-address collisions among all primes.
# 3. Determine the earliest axis prefix at which each prime becomes unique.
#
# Scope:
# - complete prime sets up to 1,000,000
# - no random target sampling
# - prime-only address space
# - finite-domain exhaustive verification
# - not an unbounded proof

import csv
import math
import statistics
import time
from collections import Counter, defaultdict

LIMITS = [100_000, 500_000, 1_000_000]
AXES = list(range(2, 65))


def sieve_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            count = ((limit - start) // number) + 1
            sieve[start:limit + 1:number] = b"\x00" * count

    return [number for number in range(2, limit + 1) if sieve[number]]


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


def exhaustive_limit(limit):
    start = time.perf_counter()
    primes = sieve_primes(limit)
    sieve_seconds = time.perf_counter() - start

    start = time.perf_counter()
    addresses = [prime_address(prime) for prime in primes]
    address_seconds = time.perf_counter() - start

    full_counts = Counter(addresses)
    collision_groups = {
        address: count
        for address, count in full_counts.items()
        if count > 1
    }

    unique_at_axis = [None] * len(primes)
    unresolved = set(range(len(primes)))
    convergence_rows = []

    start = time.perf_counter()

    for prefix_length, axis in enumerate(AXES, start=1):
        prefix_counts = Counter(
            address[:prefix_length]
            for address in addresses
        )

        newly_unique = []

        for prime_index in unresolved:
            prefix = addresses[prime_index][:prefix_length]

            if prefix_counts[prefix] == 1:
                unique_at_axis[prime_index] = prefix_length
                newly_unique.append(prime_index)

        unresolved.difference_update(newly_unique)

        convergence_rows.append({
            "limit": limit,
            "axis_position": prefix_length,
            "axis": axis,
            "remaining_nonunique_primes": len(unresolved),
            "newly_unique_primes": len(newly_unique),
            "unique_fraction": (
                (len(primes) - len(unresolved)) / len(primes)
            ),
        })

        if not unresolved:
            break

    prefix_seconds = time.perf_counter() - start

    result_rows = []

    for prime, axes_used in zip(primes, unique_at_axis):
        result_rows.append({
            "limit": limit,
            "prime": prime,
            "unique": axes_used is not None,
            "axes_used": axes_used,
            "last_axis": (
                AXES[axes_used - 1]
                if axes_used is not None
                else None
            ),
        })

    unique_axes = [
        axes_used
        for axes_used in unique_at_axis
        if axes_used is not None
    ]

    summary = {
        "limit": limit,
        "prime_count": len(primes),
        "full_address_count": len(full_counts),
        "collision_group_count": len(collision_groups),
        "colliding_prime_count": sum(collision_groups.values()),
        "all_primes_unique": len(collision_groups) == 0,
        "all_primes_prefix_unique": not unresolved,
        "median_axes_for_unique": (
            statistics.median(unique_axes)
            if unique_axes
            else None
        ),
        "mean_axes_for_unique": (
            statistics.mean(unique_axes)
            if unique_axes
            else None
        ),
        "max_axes_for_unique": (
            max(unique_axes)
            if unique_axes
            else None
        ),
        "sieve_seconds": sieve_seconds,
        "address_build_seconds": address_seconds,
        "prefix_analysis_seconds": prefix_seconds,
    }

    return result_rows, convergence_rows, summary


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    all_results = []
    all_convergence = []
    summaries = []

    print("IKERUSIKI Verification049")
    print("Exhaustive Prime Address Collision Test")
    print()

    total_start = time.perf_counter()

    for limit in LIMITS:
        results, convergence, summary = exhaustive_limit(limit)

        all_results.extend(results)
        all_convergence.extend(convergence)
        summaries.append(summary)

        print(
            f'LIMIT={limit:,} | '
            f'primes={summary["prime_count"]:,} | '
            f'addresses={summary["full_address_count"]:,} | '
            f'collision groups={summary["collision_group_count"]} | '
            f'colliding primes={summary["colliding_prime_count"]} | '
            f'all unique={summary["all_primes_unique"]} | '
            f'median axes={summary["median_axes_for_unique"]} | '
            f'max axes={summary["max_axes_for_unique"]}'
        )

    write_csv("verification049_results.csv", all_results)
    write_csv("verification049_convergence.csv", all_convergence)
    write_csv("verification049_summary.csv", summaries)

    print()
    print("Verification049 Summary")
    print(
        "All primes in all finite domains have collision-free full addresses:",
        all(summary["all_primes_unique"] for summary in summaries),
    )
    print(
        "Every prime became unique under an address prefix:",
        all(summary["all_primes_prefix_unique"] for summary in summaries),
    )
    print(
        "Total elapsed seconds:",
        f"{time.perf_counter() - total_start:.6f}",
    )


if __name__ == "__main__":
    main()
