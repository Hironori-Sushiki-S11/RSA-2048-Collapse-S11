import time
import tracemalloc
from application002_large_integer import run_experiment, BIT_SIZES


def main():
    print("Application003: Computational Optimization")
    print("Baseline measurement using Application002 formal implementation.")
    print()

    results = []

    for bit_size in BIT_SIZES:
        tracemalloc.start()
        start = time.perf_counter()

        result = run_experiment(bit_size)

        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        result["total_execution_time_sec"] = elapsed
        result["total_peak_memory_kb"] = peak / 1024

        results.append(result)

        print(f"{bit_size}-bit")
        print(f"Candidate Count: {result['candidate_count']}")
        print(f"Reduction Ratio: {result['reduction_ratio']:.6f}")
        print(f"Reconstruction Consistency: {result['reconstruction_consistency']}")
        print(f"Total Execution Time: {elapsed:.6f} sec")
        print(f"Total Peak Memory: {peak / 1024:.3f} KB")
        print()

    print("Markdown Table")
    print()
    print("| Integer Size | Candidate Count | Reduction Ratio | Reconstruction | Total Memory | Total Time |")
    print("|--------------|----------------:|----------------:|----------------|-------------:|-----------:|")

    for r in results:
        print(
            f"| {r['bit_size']}-bit "
            f"| {r['candidate_count']} "
            f"| {r['reduction_ratio']:.6f} "
            f"| {r['reconstruction_consistency']} "
            f"| {r['total_peak_memory_kb']:.3f} KB "
            f"| {r['total_execution_time_sec']:.6f} sec |"
        )


if __name__ == "__main__":
    main()
