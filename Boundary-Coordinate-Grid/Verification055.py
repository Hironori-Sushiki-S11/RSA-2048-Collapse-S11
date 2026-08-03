# IKERUSIKI Verification 055
# Boundary Address Collision Statistics
#
# Objective:
# Quantify how Boundary Address collision behavior changes as address axes
# are added.
#
# Measures:
# 1. Distinct address buckets
# 2. Collision-group count
# 3. Primes involved in collisions
# 4. Largest collision bucket
# 5. Unique-address ratio
# 6. First axis count at which the supplied corpus becomes collision-free
#
# Scope:
# - Uses the verified prime corpora from Verification053/054
# - 512 / 1024 / 2048 / 4096-bit primes
# - Boundary Address axes 2..512
# - Corpus-level verification only

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


def prefix_statistics(addresses, prefix_length):
    buckets = Counter(address[:prefix_length] for address in addresses)
    bucket_sizes = list(buckets.values())
    collision_sizes = [size for size in bucket_sizes if size > 1]
    colliding_prime_count = sum(collision_sizes)
    unique_prime_count = sum(1 for size in bucket_sizes if size == 1)
    ordered = sorted(bucket_sizes)
    p95_index = max(0, math.ceil(len(ordered) * 0.95) - 1)

    return {
        "axis_count": prefix_length,
        "last_axis": AXES[prefix_length - 1],
        "distinct_bucket_count": len(buckets),
        "unique_bucket_count": unique_prime_count,
        "collision_group_count": len(collision_sizes),
        "colliding_prime_count": colliding_prime_count,
        "colliding_prime_fraction": colliding_prime_count / len(addresses),
        "unique_prime_count": unique_prime_count,
        "unique_address_ratio": unique_prime_count / len(addresses),
        "largest_bucket_size": max(bucket_sizes),
        "mean_bucket_size": statistics.mean(bucket_sizes),
        "median_bucket_size": statistics.median(bucket_sizes),
        "p95_bucket_size": ordered[p95_index],
    }


def benchmark_bit_size(bit_size, primes):
    start = time.perf_counter_ns()
    addresses = [full_address(prime) for prime in primes]
    build_ns = time.perf_counter_ns() - start

    rows = []
    first_collision_free = None
    for prefix_length in range(1, len(AXES) + 1):
        row = prefix_statistics(addresses, prefix_length)
        row["bit_size"] = bit_size
        row["prime_count"] = len(primes)
        rows.append(row)
        if first_collision_free is None and row["collision_group_count"] == 0:
            first_collision_free = prefix_length

    final_row = rows[-1]
    summary = {
        "bit_size": bit_size,
        "prime_count": len(primes),
        "address_axis_count": len(AXES),
        "first_collision_free_axis_count": first_collision_free,
        "first_collision_free_last_axis": (
            AXES[first_collision_free - 1] if first_collision_free else None
        ),
        "final_distinct_bucket_count": final_row["distinct_bucket_count"],
        "final_collision_group_count": final_row["collision_group_count"],
        "final_colliding_prime_count": final_row["colliding_prime_count"],
        "final_unique_address_ratio": final_row["unique_address_ratio"],
        "final_largest_bucket_size": final_row["largest_bucket_size"],
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
    print("IKERUSIKI Verification055")
    print("Boundary Address Collision Statistics")
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
            f'collision-free axes={summary["first_collision_free_axis_count"]} | '
            f'last axis={summary["first_collision_free_last_axis"]} | '
            f'final collisions={summary["final_collision_group_count"]} | '
            f'unique ratio={summary["final_unique_address_ratio"]:.3f} | '
            f'build/prime={summary["address_build_per_prime_us"]:.2f} us'
        )

    base = Path(__file__).resolve().parent
    write_csv(base / "verification055_collision_curve.csv", all_rows)
    write_csv(base / "verification055_summary.csv", summaries)

    print()
    print("Verification055 Summary")
    print(
        "All supplied corpora became collision-free:",
        all(s["first_collision_free_axis_count"] is not None for s in summaries),
    )
    print(
        "All full addresses collision-free:",
        all(s["final_collision_group_count"] == 0 for s in summaries),
    )
    print("Total elapsed seconds:", f"{time.perf_counter() - total_start:.6f}")


if __name__ == "__main__":
    main()
