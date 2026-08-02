# IKERUSIKI Verification 047
# Persistent Boundary Database
#
# Objective:
# Persist Boundary Coordinate Grid data to SQLite and verify that:
# 1. Stored rows can be reconstructed after reopening the database.
# 2. Partial-axis candidate search matches in-memory inverted-index search.
# 3. Full-address lookup returns the same row set.
# 4. Build, reopen, and query performance are measured.
#
# Scope:
# - 512 to 4096-bit integers
# - 1000 rows per database
# - 16-axis partial search
# - SQLite persistent storage
# - correctness and benchmark validation
# - does not alter IKERUSIKI Theory v1.0

import csv
import json
import math
import os
import random
import sqlite3
import statistics
import tempfile
import time

BIT_SIZES = [512, 1024, 2048, 4096]
ROWS = 1000
PARTIAL_AXES = 16
SAMPLES_PER_SIZE = 3
SEED = 47026


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
    values = []

    while len(values) < ROWS:
        values.append(
            rng.getrandbits(bit_size)
            | lower_bit
            | 1
        )

    return values


def build_grid(values, axes):
    return [
        tuple((value - 1) % axis for axis in axes)
        for value in values
    ]


def build_inverted_index(grid):
    inverted = {
        axis_index: {}
        for axis_index in range(len(grid[0]))
    }

    for row_id, address in enumerate(grid):
        for axis_index, residue in enumerate(address):
            inverted[axis_index].setdefault(
                residue,
                set(),
            ).add(row_id)

    return inverted


def choose_partial_indices(axis_count):
    if axis_count <= PARTIAL_AXES:
        return list(range(axis_count))

    return [
        round(
            index * (axis_count - 1)
            / (PARTIAL_AXES - 1)
        )
        for index in range(PARTIAL_AXES)
    ]


def in_memory_partial_search(
    inverted,
    target_address,
    selected_indices,
):
    sets = [
        inverted[index][target_address[index]]
        for index in selected_indices
    ]

    if not sets:
        return []

    result = set(sets[0])

    for candidate_set in sets[1:]:
        result.intersection_update(candidate_set)

        if not result:
            break

    return sorted(result)


def address_key(address):
    return ",".join(str(value) for value in address)


def create_database(path, values, grid):
    connection = sqlite3.connect(path)

    try:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")
        connection.execute("PRAGMA temp_store = MEMORY")

        connection.executescript(
            """
            CREATE TABLE rows (
                row_id INTEGER PRIMARY KEY,
                integer_text TEXT NOT NULL,
                address_key TEXT NOT NULL
            );

            CREATE TABLE coordinates (
                row_id INTEGER NOT NULL,
                axis_index INTEGER NOT NULL,
                residue INTEGER NOT NULL,
                PRIMARY KEY (row_id, axis_index)
            );

            CREATE INDEX idx_coordinates_axis_residue
            ON coordinates(axis_index, residue);

            CREATE INDEX idx_rows_address_key
            ON rows(address_key);
            """
        )

        connection.executemany(
            """
            INSERT INTO rows(row_id, integer_text, address_key)
            VALUES (?, ?, ?)
            """,
            [
                (
                    row_id,
                    str(value),
                    address_key(grid[row_id]),
                )
                for row_id, value in enumerate(values)
            ],
        )

        coordinate_rows = []

        for row_id, address in enumerate(grid):
            coordinate_rows.extend(
                (
                    row_id,
                    axis_index,
                    residue,
                )
                for axis_index, residue in enumerate(address)
            )

        connection.executemany(
            """
            INSERT INTO coordinates(row_id, axis_index, residue)
            VALUES (?, ?, ?)
            """,
            coordinate_rows,
        )

        connection.commit()
    finally:
        connection.close()


def persistent_partial_search(
    connection,
    target_address,
    selected_indices,
):
    clauses = []
    parameters = []

    for index in selected_indices:
        clauses.append("(axis_index = ? AND residue = ?)")
        parameters.extend(
            [
                index,
                target_address[index],
            ]
        )

    query = f"""
        SELECT row_id
        FROM coordinates
        WHERE {" OR ".join(clauses)}
        GROUP BY row_id
        HAVING COUNT(*) = ?
        ORDER BY row_id
    """

    parameters.append(len(selected_indices))

    return [
        row[0]
        for row in connection.execute(
            query,
            parameters,
        )
    ]


def persistent_full_lookup(connection, target_address):
    key = address_key(target_address)

    return [
        row[0]
        for row in connection.execute(
            """
            SELECT row_id
            FROM rows
            WHERE address_key = ?
            ORDER BY row_id
            """,
            (key,),
        )
    ]


def verify_reopen(connection, values, grid):
    row_count = connection.execute(
        "SELECT COUNT(*) FROM rows"
    ).fetchone()[0]

    coordinate_count = connection.execute(
        "SELECT COUNT(*) FROM coordinates"
    ).fetchone()[0]

    sample_row = len(values) // 2

    stored_integer = connection.execute(
        """
        SELECT integer_text
        FROM rows
        WHERE row_id = ?
        """,
        (sample_row,),
    ).fetchone()[0]

    stored_coordinates = tuple(
        residue
        for _, residue in connection.execute(
            """
            SELECT axis_index, residue
            FROM coordinates
            WHERE row_id = ?
            ORDER BY axis_index
            """,
            (sample_row,),
        )
    )

    return (
        row_count == len(values)
        and coordinate_count == len(values) * len(grid[0])
        and stored_integer == str(values[sample_row])
        and stored_coordinates == grid[sample_row]
    )


def benchmark_one(bit_size, sample_index):
    values = generate_population(
        bit_size,
        sample_index,
    )
    axes = maximal_prime_power_basis(
        informative_radices_for_interval(bit_size)
    )
    selected_indices = choose_partial_indices(len(axes))

    start = time.perf_counter_ns()
    grid = build_grid(values, axes)
    grid_build_ns = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    inverted = build_inverted_index(grid)
    inverted_build_ns = time.perf_counter_ns() - start

    target_row = (
        SEED + bit_size + sample_index
    ) % ROWS
    target_address = grid[target_row]

    start = time.perf_counter_ns()
    memory_matches = in_memory_partial_search(
        inverted,
        target_address,
        selected_indices,
    )
    memory_partial_ns = time.perf_counter_ns() - start

    with tempfile.TemporaryDirectory() as directory:
        database_path = os.path.join(
            directory,
            f"verification047_{bit_size}_{sample_index}.sqlite3",
        )

        start = time.perf_counter_ns()
        create_database(
            database_path,
            values,
            grid,
        )
        persistent_build_ns = time.perf_counter_ns() - start

        database_bytes = os.path.getsize(database_path)

        start = time.perf_counter_ns()
        connection = sqlite3.connect(database_path)
        reopen_ns = time.perf_counter_ns() - start

        try:
            reopen_correct = verify_reopen(
                connection,
                values,
                grid,
            )

            start = time.perf_counter_ns()
            persistent_matches = persistent_partial_search(
                connection,
                target_address,
                selected_indices,
            )
            persistent_partial_ns = (
                time.perf_counter_ns() - start
            )

            start = time.perf_counter_ns()
            full_matches = persistent_full_lookup(
                connection,
                target_address,
            )
            full_lookup_ns = time.perf_counter_ns() - start
        finally:
            connection.close()

    direct_full_matches = [
        row_id
        for row_id, address in enumerate(grid)
        if address == target_address
    ]

    correct = (
        reopen_correct
        and memory_matches == persistent_matches
        and direct_full_matches == full_matches
        and target_row in persistent_matches
        and target_row in full_matches
    )

    return {
        "correct": correct,
        "axis_count": len(axes),
        "partial_axis_count": len(selected_indices),
        "partial_match_count": len(memory_matches),
        "full_match_count": len(full_matches),
        "grid_build_ns": grid_build_ns,
        "inverted_build_ns": inverted_build_ns,
        "persistent_build_ns": persistent_build_ns,
        "reopen_ns": reopen_ns,
        "memory_partial_ns": memory_partial_ns,
        "persistent_partial_ns": persistent_partial_ns,
        "full_lookup_ns": full_lookup_ns,
        "database_bytes": database_bytes,
        "persistent_vs_memory_ratio": (
            persistent_partial_ns / memory_partial_ns
            if memory_partial_ns > 0
            else None
        ),
    }


def main():
    rows = []
    summary_rows = []

    print("IKERUSIKI Verification047")
    print("Persistent Boundary Database")
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
                "rows": ROWS,
                **metrics,
            }

            rows.append(row)
            bit_rows.append(row)

        summary = {
            "bit_size": bit_size,
            "samples": SAMPLES_PER_SIZE,
            "rows": ROWS,
            "axis_count": bit_rows[0]["axis_count"],
            "partial_axis_count": bit_rows[0]["partial_axis_count"],
            "all_correct": all(
                row["correct"]
                for row in bit_rows
            ),
            "median_partial_match_count": statistics.median(
                row["partial_match_count"]
                for row in bit_rows
            ),
            "median_database_mb": statistics.median(
                row["database_bytes"]
                for row in bit_rows
            ) / 1_000_000,
            "median_persistent_build_ms": statistics.median(
                row["persistent_build_ns"]
                for row in bit_rows
            ) / 1_000_000,
            "median_reopen_ms": statistics.median(
                row["reopen_ns"]
                for row in bit_rows
            ) / 1_000_000,
            "median_memory_partial_us": statistics.median(
                row["memory_partial_ns"]
                for row in bit_rows
            ) / 1_000,
            "median_persistent_partial_us": statistics.median(
                row["persistent_partial_ns"]
                for row in bit_rows
            ) / 1_000,
            "median_full_lookup_us": statistics.median(
                row["full_lookup_ns"]
                for row in bit_rows
            ) / 1_000,
        }

        summary_rows.append(summary)

        print(
            f'{bit_size:>4}-bit | '
            f'rows={ROWS} | '
            f'axes={summary["axis_count"]} | '
            f'db={summary["median_database_mb"]:.3f} MB | '
            f'build={summary["median_persistent_build_ms"]:.3f} ms | '
            f'reopen={summary["median_reopen_ms"]:.3f} ms | '
            f'persistent partial={summary["median_persistent_partial_us"]:.3f} us | '
            f'full lookup={summary["median_full_lookup_us"]:.3f} us'
        )

    with open(
        "verification047_results.csv",
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
        "verification047_summary.csv",
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
    print("Verification047 Summary")
    print(
        "All persistent database results matched in-memory results:",
        all(row["all_correct"] for row in summary_rows),
    )
    print(
        "Interpretation:",
        "Boundary Grid data can be persisted, reopened, reconstructed, and queried without recomputing the original large-integer coordinates.",
    )
    print(
        "Total elapsed seconds:",
        f'{time.perf_counter() - total_start:.6f}',
    )


if __name__ == "__main__":
    main()
