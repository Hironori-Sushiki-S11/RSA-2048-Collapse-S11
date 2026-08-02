# IKERUSIKI Verification 048
# Prime Address Identification by Hierarchical Boundary Grid
#
# Objective:
# Identify a prime from its Boundary Address alone inside an exhaustive finite
# prime domain. The indexed population is the complete prime set [2, LIMIT].
#
# This is a prime-only reconstruction test, not a general-integer benchmark.

import csv
import math
import random
import statistics
import time

LIMITS = [100_000, 500_000, 1_000_000]
AXES = list(range(2, 65))
TARGETS_PER_LIMIT = 500
SEED = 48026


def sieve_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            count = ((limit - start) // number) + 1
            sieve[start:limit + 1:number] = b"\x00" * count

    return [n for n in range(2, limit + 1) if sieve[n]]


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
    return tuple(boundary_component(prime, axis) for axis in AXES)


def build_prime_inverted_index(primes):
    index = {i: {} for i in range(len(AXES))}

    for prime_index, prime in enumerate(primes):
        for axis_index, axis in enumerate(AXES):
            component = boundary_component(prime, axis)
            index[axis_index].setdefault(component, set()).add(prime_index)

    return index


def reconstruct_prime_candidates(address, index):
    candidates = None
    convergence = []

    for axis_index, component in enumerate(address):
        bucket = index[axis_index].get(component, set())
        candidates = set(bucket) if candidates is None else candidates & bucket
        convergence.append(len(candidates))

        if len(candidates) == 1:
            break

    return sorted(candidates or set()), convergence


def select_targets(primes, count, seed):
    if len(primes) <= count:
        return list(primes)

    rng = random.Random(seed)
    selected = {0, len(primes)//4, len(primes)//2, 3*len(primes)//4, len(primes)-1}

    while len(selected) < count:
        selected.add(rng.randrange(len(primes)))

    return [primes[i] for i in sorted(selected)]


def benchmark_limit(limit):
    t0 = time.perf_counter()
    primes = sieve_primes(limit)
    sieve_seconds = time.perf_counter() - t0

    t0 = time.perf_counter()
    index = build_prime_inverted_index(primes)
    index_seconds = time.perf_counter() - t0

    targets = select_targets(primes, TARGETS_PER_LIMIT, SEED + limit)
    rows = []
    convergence_sum = [0] * len(AXES)
    convergence_n = [0] * len(AXES)

    t0 = time.perf_counter()

    for target in targets:
        ids, convergence = reconstruct_prime_candidates(prime_address(target), index)
        candidate_primes = [primes[i] for i in ids]

        for i, count in enumerate(convergence):
            convergence_sum[i] += count
            convergence_n[i] += 1

        rows.append({
            "limit": limit,
            "target_prime": target,
            "axes_used": len(convergence),
            "last_axis": AXES[len(convergence)-1],
            "final_candidate_count": convergence[-1],
            "target_preserved": target in candidate_primes,
            "unique_identification": candidate_primes == [target],
        })

    query_seconds = time.perf_counter() - t0
    unique_axes = [r["axes_used"] for r in rows if r["unique_identification"]]

    curve = []
    for i, axis in enumerate(AXES):
        if convergence_n[i] == 0:
            break
        curve.append({
            "limit": limit,
            "axis_position": i + 1,
            "axis": axis,
            "mean_candidate_count": convergence_sum[i] / convergence_n[i],
        })

    summary = {
        "limit": limit,
        "prime_count": len(primes),
        "tested_targets": len(rows),
        "target_preservation_rate": sum(r["target_preserved"] for r in rows) / len(rows),
        "unique_identification_rate": sum(r["unique_identification"] for r in rows) / len(rows),
        "median_axes_for_unique": statistics.median(unique_axes) if unique_axes else None,
        "max_axes_for_unique": max(unique_axes) if unique_axes else None,
        "sieve_seconds": sieve_seconds,
        "index_build_seconds": index_seconds,
        "query_seconds": query_seconds,
        "mean_query_microseconds": query_seconds / len(rows) * 1_000_000,
    }
    return rows, curve, summary


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    results = []
    curves = []
    summaries = []

    print("IKERUSIKI Verification048")
    print("Prime Address Identification")
    print()

    total_start = time.perf_counter()

    for limit in LIMITS:
        rows, curve, summary = benchmark_limit(limit)
        results.extend(rows)
        curves.extend(curve)
        summaries.append(summary)

        print(
            f'LIMIT={limit:,} | primes={summary["prime_count"]:,} | '
            f'targets={summary["tested_targets"]} | '
            f'preserved={summary["target_preservation_rate"]:.3f} | '
            f'unique={summary["unique_identification_rate"]:.3f} | '
            f'median axes={summary["median_axes_for_unique"]} | '
            f'max axes={summary["max_axes_for_unique"]} | '
            f'query={summary["mean_query_microseconds"]:.2f} us'
        )

    write_csv("verification048_results.csv", results)
    write_csv("verification048_convergence.csv", curves)
    write_csv("verification048_summary.csv", summaries)

    print()
    print("Verification048 Summary")
    print("All target primes preserved:", all(s["target_preservation_rate"] == 1.0 for s in summaries))
    print("All tested prime addresses uniquely identified:", all(s["unique_identification_rate"] == 1.0 for s in summaries))
    print("Total elapsed seconds:", f"{time.perf_counter() - total_start:.6f}")


if __name__ == "__main__":
    main()
    return sorted(candidates or set()), convergence


def select_targets(primes, count, seed):
    if len(primes) <= count:
        return list(primes)

    rng = random.Random(seed)
    selected = {0, len(primes)//4, len(primes)//2, 3*len(primes)//4, len(primes)-1}

    while len(selected) < count:
        selected.add(rng.randrange(len(primes)))

    return [primes[i] for i in sorted(selected)]


def benchmark_limit(limit):
    t0 = time.perf_counter()
    primes = sieve_primes(limit)
    sieve_seconds = time.perf_counter() - t0

    t0 = time.perf_counter()
    index = build_prime_inverted_index(primes)
    index_seconds = time.perf_counter() - t0

    targets = select_targets(primes, TARGETS_PER_LIMIT, SEED + limit)
    rows = []
    convergence_sum = [0] * len(AXES)
    convergence_n = [0] * len(AXES)

    t0 = time.perf_counter()

    for target in targets:
        ids, convergence = reconstruct_prime_candidates(prime_address(target), index)
        candidate_primes = [primes[i] for i in ids]

        for i, count in enumerate(convergence):
            convergence_sum[i] += count
            convergence_n[i] += 1

        rows.append({
            "limit": limit,
            "target_prime": target,
            "axes_used": len(convergence),
            "last_axis": AXES[len(convergence)-1],
            "final_candidate_count": convergence[-1],
            "target_preserved": target in candidate_primes,
            "unique_identification": candidate_primes == [target],
        })

    query_seconds = time.perf_counter() - t0
    unique_axes = [r["axes_used"] for r in rows if r["unique_identification"]]

    curve = []
    for i, axis in enumerate(AXES):
        if convergence_n[i] == 0:
            break
        curve.append({
            "limit": limit,
            "axis_position": i + 1,
            "axis": axis,
            "mean_candidate_count": convergence_sum[i] / convergence_n[i],
        })

    summary = {
        "limit": limit,
        "prime_count": len(primes),
        "tested_targets": len(rows),
        "target_preservation_rate": sum(r["target_preserved"] for r in rows) / len(rows),
        "unique_identification_rate": sum(r["unique_identification"] for r in rows) / len(rows),
        "median_axes_for_unique": statistics.median(unique_axes) if unique_axes else None,
        "max_axes_for_unique": max(unique_axes) if unique_axes else None,
        "sieve_seconds": sieve_seconds,
        "index_build_seconds": index_seconds,
        "query_seconds": query_seconds,
        "mean_query_microseconds": query_seconds / len(rows) * 1_000_000,
    }
    return rows, curve, summary


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    results = []
    curves = []
    summaries = []

    print("IKERUSIKI Verification048")
    print("Prime Address Identification")
    print()

    total_start = time.perf_counter()

    for limit in LIMITS:
        rows, curve, summary = benchmark_limit(limit)
        results.extend(rows)
        curves.extend(curve)
        summaries.append(summary)

        print(
            f'LIMIT={limit:,} | primes={summary["prime_count"]:,} | '
            f'targets={summary["tested_targets"]} | '
            f'preserved={summary["target_preservation_rate"]:.3f} | '
            f'unique={summary["unique_identification_rate"]:.3f} | '
            f'median axes={summary["median_axes_for_unique"]} | '
            f'max axes={summary["max_axes_for_unique"]} | '
            f'query={summary["mean_query_microseconds"]:.2f} us'
        )

    write_csv("verification048_results.csv", results)
    write_csv("verification048_convergence.csv", curves)
    write_csv("verification048_summary.csv", summaries)

    print()
    print("Verification048 Summary")
    print("All target primes preserved:", all(s["target_preservation_rate"] == 1.0 for s in summaries))
    print("All tested prime addresses uniquely identified:", all(s["unique_identification_rate"] == 1.0 for s in summaries))
    print("Total elapsed seconds:", f"{time.perf_counter() - total_start:.6f}")


if __name__ == "__main__":
    main()
