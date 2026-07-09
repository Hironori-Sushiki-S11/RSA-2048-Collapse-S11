import math
import time
import random
import tracemalloc
from functools import lru_cache

RADIX_LIST = range(2, 27)
LAYER = 1
BIT_SIZES = [512, 1024, 2048, 4096]


@lru_cache(maxsize=None)
def modulus_of(b):
    return b ** LAYER


@lru_cache(maxsize=None)
def lcm_cached(a, b):
    return math.lcm(a, b)


@lru_cache(maxsize=None)
def gcd_cached(a, b):
    return math.gcd(a, b)


def boundary_distance(n, b):
    modulus = modulus_of(b)
    position = ((n - 1) % modulus) + 1
    return min(position - 1, modulus - position)


def boundary_coordinate(n):
    return {b: boundary_distance(n, b) for b in RADIX_LIST}


def crt_merge_pair(r0, m0, r1, m1):
    g = gcd_cached(m0, m1)

    if (r1 - r0) % g != 0:
        return None

    m0_g = m0 // g
    m1_g = m1 // g

    t = ((r1 - r0) // g * pow(m0_g, -1, m1_g)) % m1_g
    new_mod = lcm_cached(m0, m1)

    return (r0 + m0 * t) % new_mod


def merge_constraint(residues, current_mod, b, d):
    modulus = modulus_of(b)

    possible_residues = {
        d,
        modulus - 1 - d
    }

    new_mod = lcm_cached(current_mod, modulus)
    new_residues = set()

    for r0 in residues:
        for r1 in possible_residues:
            merged = crt_merge_pair(r0, current_mod, r1, modulus)
            if merged is not None:
                new_residues.add(merged % new_mod)

    return new_residues, new_mod


def reconstruct_residue_classes(coord):
    residues = {0}
    current_mod = 1

    for b, d in coord.items():
        residues, current_mod = merge_constraint(
            residues,
            current_mod,
            b,
            d
        )

    return residues, current_mod


def generate_large_odd_integer(bit_size):
    n = random.getrandbits(bit_size)
    n |= (1 << (bit_size - 1))
    n |= 1
    return n


def count_candidates_in_bit_range(residues, modulus, bit_size):
    low = 2 ** (bit_size - 1)
    high = (2 ** bit_size) - 1

    count = 0

    for r in residues:
        first = r + 1

        if first < low:
            k = (low - first + modulus - 1) // modulus
            first += k * modulus

        if first <= high:
            count += ((high - first) // modulus) + 1

    return count


def run_optimized_experiment(bit_size):
    n = generate_large_odd_integer(bit_size)

    total_range = 2 ** (bit_size - 1)

    tracemalloc.start()
    start = time.perf_counter()

    coord = boundary_coordinate(n)
    residues, structural_modulus = reconstruct_residue_classes(coord)

    candidate_count = count_candidates_in_bit_range(
        residues,
        structural_modulus,
        bit_size
    )

    elapsed = time.perf_counter() - start
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    reduction_ratio = total_range / candidate_count if candidate_count else 0
    reconstruction_consistency = ((n - 1) % structural_modulus) in residues

    return {
        "bit_size": bit_size,
        "optimization": "Cache Optimization",
        "structural_modulus": structural_modulus,
        "residue_classes": len(residues),
        "candidate_count": candidate_count,
        "reduction_ratio": reduction_ratio,
        "reconstruction_consistency": reconstruction_consistency,
        "execution_time_sec": elapsed,
        "peak_memory_kb": peak_memory / 1024
    }


def main():
    print("Application003: Computational Optimization")
    print("Cache optimization applied without modifying IKERUSIKI Theory.")
    print()

    results = []

    for bit_size in BIT_SIZES:
        result = run_optimized_experiment(bit_size)
        results.append(result)

        print(f"{bit_size}-bit")
        print(f"Optimization: {result['optimization']}")
        print(f"Structural Modulus: {result['structural_modulus']}")
        print(f"Residue Classes: {result['residue_classes']}")
        print(f"Candidate Count: {result['candidate_count']}")
        print(f"Reduction Ratio: {result['reduction_ratio']:.6f}")
        print(f"Reconstruction Consistency: {result['reconstruction_consistency']}")
        print(f"Execution Time: {result['execution_time_sec']:.6f} sec")
        print(f"Peak Memory: {result['peak_memory_kb']:.3f} KB")
        print()

    print("Markdown Table")
    print()
    print("| Integer Size | Optimization | Structural Modulus | Residue Classes | Reduction Ratio | Reconstruction | Memory | Execution Time |")
    print("|--------------|--------------|-------------------:|----------------:|----------------:|----------------|-------:|---------------:|")

    for r in results:
        print(
            f"| {r['bit_size']}-bit "
            f"| {r['optimization']} "
            f"| {r['structural_modulus']} "
            f"| {r['residue_classes']} "
            f"| {r['reduction_ratio']:.6f} "
            f"| {r['reconstruction_consistency']} "
            f"| {r['peak_memory_kb']:.3f} KB "
            f"| {r['execution_time_sec']:.6f} sec |"
        )


if __name__ == "__main__":
    main()
