import time
import tracemalloc

from application002_large_integer import run_experiment, BIT_SIZES


def benchmark_application002():
    results = []

    for bit_size in BIT_SIZES:
        tracemalloc.start()
        start = time.perf_counter()

        result = run_experiment(bit_size)

        elapsed = time.perf_counter() - start
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results.append({
            "application": "Application002",
            "integer_size": f"{bit_size}-bit",
            "candidate_count": result["candidate_count"],
            "reduction_ratio": result["reduction_ratio"],
            "reconstruction": result["reconstruction_consistency"],
            "memory_kb": peak / 1024,
            "execution_time_sec": elapsed,
            "status": "Completed"
        })

    return results


def main():
    print("Application004: Benchmark Analysis")
    print("Benchmarking completed IKERUSIKI application measurements.")
    print()

    results = []

    results.extend(benchmark_application002())

    print("Benchmark Results")
    print()

    for r in results:
        print(f"{r['application']} {r['integer_size']}")
        print(f"Candidate Count: {r['candidate_count']}")
        print(f"Reduction Ratio: {r['reduction_ratio']:.6f}")
        print(f"Reconstruction: {r['reconstruction']}")
        print(f"Memory: {r['memory_kb']:.3f} KB")
        print(f"Execution Time: {r['execution_time_sec']:.6f} sec")
        print(f"Status: {r['status']}")
        print()

    print("Markdown Table")
    print()
    print("| Application | Integer Size | Candidate Count | Reduction Ratio | Reconstruction | Memory | Execution Time | Status |")
    print("|-------------|-------------:|----------------:|----------------:|----------------|-------:|---------------:|--------|")

    for r in results:
        print(
            f"| {r['application']} "
            f"| {r['integer_size']} "
            f"| {r['candidate_count']} "
            f"| {r['reduction_ratio']:.6f} "
            f"| {r['reconstruction']} "
            f"| {r['memory_kb']:.3f} KB "
            f"| {r['execution_time_sec']:.6f} sec "
            f"| {r['status']} |"
        )


if __name__ == "__main__":
    main()
