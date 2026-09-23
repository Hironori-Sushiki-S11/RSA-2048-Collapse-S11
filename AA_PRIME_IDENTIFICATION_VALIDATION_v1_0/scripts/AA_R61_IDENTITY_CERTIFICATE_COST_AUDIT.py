#!/usr/bin/env python3
"""Compare exact factor certificates with and without AA address selection.

Only integers below 2**64 enter is_prime64.  This is an evidence/provenance
audit of the existing R61 corpus, not a new primality test for its Mersenne
numbers.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
import platform
import resource
import subprocess
import sys
from time import perf_counter

START_P = 1_000_000_000_039
CORPUS_SIZE = 64
AXIS_CAP = 4096
K_MAX = 20_000
# Deterministic Miller–Rabin witnesses for unsigned 64-bit integers.
WITNESSES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime64(n: int) -> bool:
    if n < 2 or n >= 1 << 64:
        raise ValueError("is_prime64 requires 2 <= n < 2**64")
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in WITNESSES:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def corpus() -> list[int]:
    out = []
    p = START_P
    while len(out) < CORPUS_SIZE:
        if is_prime64(p):
            out.append(p)
        p += 2
    return out


def select_axis(exponents: list[int]) -> tuple[int, int, int]:
    """Exact early stop: the first prime axis with zero collisions."""
    evaluated = 0
    for axis in range(2, AXIS_CAP + 1):
        if not is_prime64(axis):
            continue
        evaluated += 1
        counts = Counter(pow(2, p, axis) - 1 for p in exponents)
        phi = sum(c * (c - 1) // 2 for c in counts.values())
        if phi == 0:
            return axis, phi, evaluated
    raise RuntimeError("no collision-free axis within cap")


def exact_factor_scan(exponents: list[int]) -> tuple[list[dict], int, int]:
    """Identical exact classifier in either mode. Stop at first q per p."""
    certificates = []
    candidates = tested_prime_q = 0
    for p in exponents:
        for k in range(1, K_MAX + 1):
            q = 2 * k * p + 1
            if q % 8 not in (1, 7):
                continue
            candidates += 1
            if not is_prime64(q):
                continue
            tested_prime_q += 1
            if pow(2, p, q) == 1:
                certificates.append({"p": p, "k": k, "q": q})
                break
    return certificates, candidates, tested_prime_q


def run(mode: str) -> dict:
    t0 = perf_counter()
    exponents = corpus()
    t_corpus = perf_counter()
    axis = phi = evaluated = None
    if mode == "aa":
        axis, phi, evaluated = select_axis(exponents)
    t_address = perf_counter()
    certs, candidates, prime_q = exact_factor_scan(exponents)
    t_end = perf_counter()
    for c in certs:
        assert 1 < c["q"] and c["q"].bit_length() < c["p"]
        assert c["q"] == 2 * c["k"] * c["p"] + 1
        assert pow(2, c["p"], c["q"]) == 1
    return {
        "mode": mode,
        "p_min": exponents[0], "p_max": exponents[-1],
        "candidate_exponents": len(exponents),
        "aa_axis": axis, "aa_final_collision_pairs": phi,
        "aa_axes_evaluated": evaluated,
        "composite_certificates": certs, "unresolved": len(exponents) - len(certs),
        "eligible_q_checked": candidates, "prime_q_checked": prime_q,
        "wall_corpus_seconds": t_corpus - t0,
        "wall_address_seconds": t_address - t_corpus,
        "wall_factor_scan_seconds": t_end - t_address,
        "wall_total_seconds": t_end - t0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def compare(reps: int) -> dict:
    trials = []
    # Reverse order each repeat to reduce systematic timing drift.
    for i in range(reps):
        for mode in (("baseline", "aa") if i % 2 == 0 else ("aa", "baseline")):
            proc = subprocess.run(
                [sys.executable, __file__, "--mode", mode],
                check=True, capture_output=True, text=True,
            )
            trials.append(json.loads(proc.stdout))
    baseline = [r for r in trials if r["mode"] == "baseline"]
    aa = [r for r in trials if r["mode"] == "aa"]
    expected = baseline[0]["composite_certificates"]
    for r in trials:
        assert r["composite_certificates"] == expected
        assert r["eligible_q_checked"] == baseline[0]["eligible_q_checked"]
        assert r["prime_q_checked"] == baseline[0]["prime_q_checked"]
    from statistics import median
    totals = {mode: median(r["wall_total_seconds"] for r in rows)
              for mode, rows in (("baseline", baseline), ("aa", aa))}
    return {
        "protocol": {
            "comparison": "AA address selection + exact factor scan versus same exact factor scan",
            "input": "first 64 prime exponents >= 1000000000039",
            "factor_detector": "prime q=2kp+1, 1<=k<=20000, q mod8 in {1,7}, pow(2,p,q)==1",
            "preparation_included": True,
            "independent_process_per_trial": True,
            "repetitions_per_mode": reps,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "logical_cpus": os.cpu_count(),
        },
        "median_total_seconds": totals,
        "aa_over_baseline_total_cost_ratio": totals["aa"] / totals["baseline"],
        "verified_certificates": len(expected),
        "unresolved": baseline[0]["unresolved"],
        "trials": trials,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("aa", "baseline", "compare"), default="compare")
    ap.add_argument("--reps", type=int, default=3)
    args = ap.parse_args()
    if args.reps < 1:
        raise ValueError("reps must be >= 1")
    result = compare(args.reps) if args.mode == "compare" else run(args.mode)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
