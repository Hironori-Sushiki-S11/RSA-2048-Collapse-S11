# IKERUSIKI Verification 062
# Adaptive Address Expansion Trigger
#
# Objective:
# Convert the stage measurements produced by Verification061 into an explicit
# rule for deciding whether the current Boundary Address should:
#
#   CONTINUE  : keep using the existing axis pool,
#   EXPAND    : introduce a new axis range / new address information,
#   COMPLETE  : stop because all corpus values are uniquely separated,
#   STALLED   : stop because no measurable separation remains.
#
# This verification evaluates both:
#
#   Vertical persistence:
#   - target branch shrinkage across consecutive depths
#
#   Horizontal separation:
#   - unresolved collision-pair reduction across the whole corpus
#
# Scope:
# - Finite-corpus empirical verification only.
# - Imports the exploration engine from Verification061.py.
# - Does not prove universal identification over an unbounded integer range.
#
# Required files in the same directory:
# - Verification061.py
# - prime_corpus_512.txt
# - prime_corpus_1024.txt
# - prime_corpus_2048.txt
# - prime_corpus_4096.txt
#
# Outputs:
# - verification062_trigger_trace.csv
# - verification062_summary.csv
# - verification062_result.json

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from Verification061 import (
    BIT_SIZES,
    load_prime_corpus,
    run_adaptive_explorer,
)

# Trigger policy.
#
# EXPAND is recommended when unresolved collisions remain and either:
# 1. no unresolved-pair reduction occurs, or
# 2. both horizontal and vertical gains remain weak for
#    WEAK_GAIN_PATIENCE consecutive stages.
#
# The values are explicit experimental settings, not mathematical constants.
MIN_HORIZONTAL_GAIN_RATIO = 0.10
MIN_VERTICAL_GAIN_RATIO = 0.10
WEAK_GAIN_PATIENCE = 2


@dataclass
class TriggerTrace:
    bit_size: int
    depth: int
    selected_axis: int
    unresolved_pairs_before: int
    unresolved_pairs_after: int
    horizontal_gain_ratio: float
    target_bucket_before: int
    target_bucket_after: int
    vertical_gain_ratio: float
    weak_horizontal_gain: bool
    weak_vertical_gain: bool
    consecutive_weak_stages: int
    collisions_remain: bool
    decision: str
    reason: str


@dataclass
class TriggerSummary:
    bit_size: int
    value_count: int
    explored_depth: int
    selected_axes: str
    final_decision: str
    decision_depth: int
    final_unresolved_pairs: int
    final_target_bucket_size: int
    address_expansion_required: bool
    trigger_reason: str


def safe_gain_ratio(before: int, after: int) -> float:
    if before <= 0:
        return 0.0
    return (before - after) / before


def evaluate_trigger(
    bit_size: int,
    values: Sequence[int],
    target_row_id: int = 0,
) -> tuple[list[TriggerTrace], TriggerSummary, dict]:
    stage_rows, _, exploration_result = run_adaptive_explorer(
        bit_size=bit_size,
        values=values,
        target_row_id=target_row_id,
    )

    traces: list[TriggerTrace] = []
    consecutive_weak = 0
    final_decision = "STALLED"
    final_reason = "No stage was produced."
    decision_depth = 0

    for stage in stage_rows:
        horizontal_gain = safe_gain_ratio(
            stage.unresolved_pairs_before,
            stage.unresolved_pairs_after,
        )
        vertical_gain = safe_gain_ratio(
            stage.target_bucket_before,
            stage.target_bucket_after,
        )

        weak_horizontal = (
            stage.unresolved_pairs_after > 0
            and horizontal_gain < MIN_HORIZONTAL_GAIN_RATIO
        )
        weak_vertical = (
            stage.target_bucket_after > 1
            and vertical_gain < MIN_VERTICAL_GAIN_RATIO
        )

        if weak_horizontal and weak_vertical:
            consecutive_weak += 1
        else:
            consecutive_weak = 0

        collisions_remain = stage.unresolved_pairs_after > 0

        if not collisions_remain:
            decision = "COMPLETE"
            reason = (
                "All corpus-level collision pairs were resolved by the "
                "current address axes."
            )
        elif stage.unresolved_pair_reduction == 0:
            decision = "EXPAND"
            reason = (
                "Unresolved collisions remain, but the selected axis produced "
                "no horizontal separation."
            )
        elif consecutive_weak >= WEAK_GAIN_PATIENCE:
            decision = "EXPAND"
            reason = (
                "Horizontal collision reduction and target-branch shrinkage "
                f"were both below threshold for {consecutive_weak} "
                "consecutive stages."
            )
        else:
            decision = "CONTINUE"
            reason = (
                "The existing address axes still produce measurable "
                "separation."
            )

        traces.append(
            TriggerTrace(
                bit_size=bit_size,
                depth=stage.depth,
                selected_axis=stage.selected_axis,
                unresolved_pairs_before=stage.unresolved_pairs_before,
                unresolved_pairs_after=stage.unresolved_pairs_after,
                horizontal_gain_ratio=horizontal_gain,
                target_bucket_before=stage.target_bucket_before,
                target_bucket_after=stage.target_bucket_after,
                vertical_gain_ratio=vertical_gain,
                weak_horizontal_gain=weak_horizontal,
                weak_vertical_gain=weak_vertical,
                consecutive_weak_stages=consecutive_weak,
                collisions_remain=collisions_remain,
                decision=decision,
                reason=reason,
            )
        )

        if decision in {"COMPLETE", "EXPAND"}:
            final_decision = decision
            final_reason = reason
            decision_depth = stage.depth
            break

    if traces and final_decision == "STALLED":
        last = traces[-1]
        final_decision = last.decision
        final_reason = last.reason
        decision_depth = last.depth

    if traces:
        final_unresolved_pairs = traces[-1].unresolved_pairs_after
        final_target_bucket = traces[-1].target_bucket_after
    else:
        final_unresolved_pairs = (
            len(values) * (len(values) - 1) // 2
        )
        final_target_bucket = len(values)

    summary = TriggerSummary(
        bit_size=bit_size,
        value_count=len(values),
        explored_depth=len(traces),
        selected_axes="|".join(
            str(row.selected_axis) for row in traces
        ),
        final_decision=final_decision,
        decision_depth=decision_depth,
        final_unresolved_pairs=final_unresolved_pairs,
        final_target_bucket_size=final_target_bucket,
        address_expansion_required=(final_decision == "EXPAND"),
        trigger_reason=final_reason,
    )

    result = {
        "bit_size": bit_size,
        "policy": {
            "minimum_horizontal_gain_ratio": MIN_HORIZONTAL_GAIN_RATIO,
            "minimum_vertical_gain_ratio": MIN_VERTICAL_GAIN_RATIO,
            "weak_gain_patience": WEAK_GAIN_PATIENCE,
        },
        "summary": asdict(summary),
        "exploration_result": exploration_result,
        "interpretation": {
            "CONTINUE": (
                "Existing axes still separate the current collision structure."
            ),
            "EXPAND": (
                "Existing axes have become insufficient; add a new axis range "
                "or a new structural address component."
            ),
            "COMPLETE": (
                "All values in the supplied finite corpus are uniquely "
                "separated."
            ),
            "STALLED": (
                "The experiment ended without a conclusive complete/expand "
                "trigger."
            ),
        },
        "scope": "finite-corpus empirical verification",
    }
    return traces, summary, result


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base = Path(__file__).resolve().parent
    all_traces: list[dict] = []
    all_summaries: list[dict] = []
    all_results: list[dict] = []

    print("IKERUSIKI Verification062")
    print("Adaptive Address Expansion Trigger")
    print()

    for bit_size in BIT_SIZES:
        values = load_prime_corpus(bit_size)
        traces, summary, result = evaluate_trigger(
            bit_size=bit_size,
            values=values,
            target_row_id=0,
        )

        all_traces.extend(asdict(row) for row in traces)
        all_summaries.append(asdict(summary))
        all_results.append(result)

        print(
            f"{bit_size:>4}-bit | values={summary.value_count} | "
            f"depth={summary.explored_depth} | "
            f"decision={summary.final_decision} | "
            f"target bucket={summary.final_target_bucket_size} | "
            f"unresolved pairs={summary.final_unresolved_pairs}"
        )
        print(f"  reason: {summary.trigger_reason}")

    write_csv(
        base / "verification062_trigger_trace.csv",
        all_traces,
    )
    write_csv(
        base / "verification062_summary.csv",
        all_summaries,
    )
    (base / "verification062_result.json").write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print(
        "Expansion required for any corpus:",
        any(
            summary["address_expansion_required"]
            for summary in all_summaries
        ),
    )
    print(
        "All corpora completed without expansion:",
        all(
            summary["final_decision"] == "COMPLETE"
            for summary in all_summaries
        ),
    )


if __name__ == "__main__":
    main()
