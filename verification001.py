# IKERUSIKI Verification 001
# Observation of Residual Space after known prime-axis elimination

LIMIT = 1000

KNOWN_PRIMES = [2, 3, 5, 7, 11]


def generate_candidates(limit):
    return list(range(2, limit + 1))


def survive_filter(candidates):

    survivors = []

    for n in candidates:

        survive = True

        for p in KNOWN_PRIMES:

            if n == p:
                continue

            if n % p == 0:
                survive = False
                break

        if survive:
            survivors.append(n)

    return survivors


def is_prime(n):

    if n < 2:
        return False

    k = 2

    while k * k <= n:

        if n % k == 0:
            return False

        k += 1

    return True


def first_eliminating_axis(n):

    k = 2

    while k * k <= n:

        if n % k == 0 and is_prime(k):
            return k

        k += 1

    return None


def classify_survivors(survivors):

    prime_axes = []
    composite_survivors = []

    for n in survivors:

        if is_prime(n):
            prime_axes.append(n)
        else:
            composite_survivors.append(n)

    return prime_axes, composite_survivors


def analyze_composite_survivors(composite_survivors):

    analysis = []

    for n in composite_survivors:

        axis = first_eliminating_axis(n)

        analysis.append(
            {
                "number": n,
                "first_eliminating_axis": axis,
                "cofactor": n // axis if axis else None,
            }
        )

    return analysis


def summarize_by_axis(composite_analysis):

    summary = {}

    for item in composite_analysis:

        axis = item["first_eliminating_axis"]

        if axis not in summary:
            summary[axis] = 0

        summary[axis] += 1

    return summary


def main():

    candidates = generate_candidates(LIMIT)

    survivors = survive_filter(candidates)

    prime_axes, composite_survivors = classify_survivors(
        survivors
    )

    composite_analysis = analyze_composite_survivors(
        composite_survivors
    )

    axis_summary = summarize_by_axis(
        composite_analysis
    )

    print("Candidates:", len(candidates))
    print("Survivors :", len(survivors))
    print("Prime Axes:", len(prime_axes))
    print("Composite :", len(composite_survivors))

    print()
    print("Composite survivor analysis")
    print()

    for item in composite_analysis:

        print(
            item["number"],
            "=",
            item["first_eliminating_axis"],
            "x",
            item["cofactor"],
        )

    print()
    print("Elimination summary by axis")
    print()

    for axis, count in sorted(axis_summary.items()):

        print(
            axis,
            "axis eliminates",
            count,
            "composite survivors",
        )


if __name__ == "__main__":
    main()
