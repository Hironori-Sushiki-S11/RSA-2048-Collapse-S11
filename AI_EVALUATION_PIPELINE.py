#!/usr/bin/env python3
"""
IKERUSIKI / Adaptive Address — AI Evidence-Gated Evaluation Pipeline

Machine-checkable state-preservation layer for:
Collector -> Evidence Ledger -> Validator -> Evidence Gate
-> Evaluator / Claim-State Lock -> Synthesizer -> Structural Fidelity Check

This script does not decide mathematical truth, novelty, performance, utility,
or cryptographic significance. It checks protocol structure and whether declared
claim states are preserved across stages.

No third-party packages are required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

VERSION = "1.0.0"

REQUIRED_SOURCES = [
    "AI_REVIEW_GUIDE.md",
    "Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_FORMAL_BASIS.md",
    "Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_DEMO.py",
    "Boundary-Coordinate-Grid/HOW_TO_APPLY_ADAPTIVE_ADDRESS.md",
    "ADAPTIVE_ADDRESS_SCALING_REPRODUCIBILITY.md",
    "ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py",
]

REQUIRED_VALIDATOR_CHECKS = [
    "source_completion",
    "evidence_type_classification",
    "clause_level_binding",
    "condition_retention",
    "internal_consistency",
    "layer_separation",
    "execution_status",
    "external_comparison_status",
]

ALLOWED_CLAIM_STATES = {
    "SUPPORTED",
    "CONTRADICTED",
    "NOT ESTABLISHED",
    "NOT ASSESSED",
    "REPORTED BUT NOT INDEPENDENTLY REPRODUCED",
    "INDEPENDENTLY REPRODUCED",
    "OPEN",
    "UNKNOWN",
}
ALLOWED_EXECUTION_STATES = {"RUN", "NOT RUN", "UNAVAILABLE IN CURRENT ENVIRONMENT"}
ALLOWED_COMPARISON_STATES = {"PERFORMED", "NOT PERFORMED"}

FILES = {
    "ledger": "evidence_ledger.json",
    "validator": "validator_result.json",
    "claims": "claim_state.json",
    "lock": "claim_state.lock.json",
    "synthesis": "final_synthesis.md",
    "manifest": "synthesis_manifest.json",
}


class ProtocolError(Exception):
    pass


def norm(s: str) -> str:
    return s.replace("\\", "/").strip()


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    if not path.exists():
        raise ProtocolError(f"missing file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ProtocolError(f"invalid JSON: {path}: {e}") from e


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def nonempty(v: Any) -> bool:
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, list):
        return len(v) > 0
    return v is not None


def require_fields(row: dict[str, Any], fields: list[str], label: str) -> None:
    for field in fields:
        if field not in row or not nonempty(row[field]):
            raise ProtocolError(f"{label}: missing/non-empty field required: {field}")


def validate_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    evidence = ledger.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ProtocolError("Evidence Ledger: 'evidence' must be a non-empty list")

    ids: set[str] = set()
    source_rows: dict[str, dict[str, Any]] = {}
    required = [
        "id", "source", "status", "location", "type", "evidence",
        "directly_establishes", "does_not_establish",
    ]

    for i, row in enumerate(evidence, 1):
        if not isinstance(row, dict):
            raise ProtocolError(f"Evidence Ledger row {i}: must be an object")
        require_fields(row, required, f"Evidence Ledger row {i}")
        eid = str(row["id"]).strip()
        if eid in ids:
            raise ProtocolError(f"duplicate Evidence ID: {eid}")
        ids.add(eid)
        source = norm(str(row["source"]))
        status = str(row["status"]).upper().strip()
        if status != "READ":
            raise ProtocolError(f"{eid}: source status must be READ, got {status}")
        if source in source_rows:
            raise ProtocolError(f"duplicate source row: {source}")
        source_rows[source] = row

    missing = [s for s in REQUIRED_SOURCES if s not in source_rows]
    if missing:
        raise ProtocolError("Collector incomplete; missing required source(s): " + ", ".join(missing))

    return {
        "collector": "COMPLETE",
        "evidence_ledger": "PRESENT",
        "evidence_ids": sorted(ids),
        "source_count": len(source_rows),
    }


def validate_validator(validator: dict[str, Any], ledger_summary: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "collector": "COMPLETE",
        "evidence_ledger": "PRESENT",
        "validator": "PASS",
        "evidence_gate": "COMPLETE",
    }
    for key, value in expected.items():
        actual = str(validator.get(key, "")).upper().strip()
        if actual != value:
            raise ProtocolError(f"Validator Result: {key} must be {value}, got {actual or '<missing>'}")

    checks = validator.get("checks")
    if not isinstance(checks, dict):
        raise ProtocolError("Validator Result: 'checks' must be an object")
    for name in REQUIRED_VALIDATOR_CHECKS:
        actual = str(checks.get(name, "")).upper().strip()
        if actual != "PASS":
            raise ProtocolError(f"Validator check '{name}' must be PASS, got {actual or '<missing>'}")

    execution = str(validator.get("execution_status", "")).upper().strip()
    prior_art = str(validator.get("prior_art_comparison", "")).upper().strip()
    benchmark = str(validator.get("comparative_benchmark", "")).upper().strip()
    if execution not in ALLOWED_EXECUTION_STATES:
        raise ProtocolError("invalid execution_status")
    if prior_art not in ALLOWED_COMPARISON_STATES:
        raise ProtocolError("prior_art_comparison must be PERFORMED / NOT PERFORMED")
    if benchmark not in ALLOWED_COMPARISON_STATES:
        raise ProtocolError("comparative_benchmark must be PERFORMED / NOT PERFORMED")

    return {
        **ledger_summary,
        "validator": "PASS",
        "evidence_gate": "COMPLETE",
        "execution_status": execution,
        "prior_art_comparison": prior_art,
        "comparative_benchmark": benchmark,
    }


def validate_claims(claims_doc: dict[str, Any], evidence_ids: set[str], gate: dict[str, Any]) -> dict[str, Any]:
    claims = claims_doc.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ProtocolError("Claim State: 'claims' must be a non-empty list")

    ids: set[str] = set()
    dimensions: dict[str, list[dict[str, Any]]] = {}
    required_nonempty = ["id", "claim", "state", "conditions_scope", "reason"]

    for i, row in enumerate(claims, 1):
        if not isinstance(row, dict):
            raise ProtocolError(f"Claim row {i}: must be an object")
        require_fields(row, required_nonempty, f"Claim row {i}")
        if "evidence_ids" not in row:
            raise ProtocolError(f"Claim row {i}: missing field required: evidence_ids")
        cid = str(row["id"]).strip()
        if cid in ids:
            raise ProtocolError(f"duplicate Claim ID: {cid}")
        ids.add(cid)

        state = str(row["state"]).upper().strip()
        if state not in ALLOWED_CLAIM_STATES:
            raise ProtocolError(f"{cid}: unsupported claim state '{state}'")

        ev = row["evidence_ids"]
        if not isinstance(ev, list):
            raise ProtocolError(f"{cid}: evidence_ids must be a list")
        unknown = [str(e) for e in ev if str(e) not in evidence_ids]
        if unknown:
            raise ProtocolError(f"{cid}: unknown Evidence ID(s): {', '.join(unknown)}")

        if state in {
            "SUPPORTED", "CONTRADICTED",
            "REPORTED BUT NOT INDEPENDENTLY REPRODUCED",
            "INDEPENDENTLY REPRODUCED",
        } and not ev:
            raise ProtocolError(f"{cid}: state {state} requires Evidence IDs")

        dim = str(row.get("dimension", "")).upper().strip()
        if dim:
            dimensions.setdefault(dim, []).append(row)

    if gate["prior_art_comparison"] == "NOT PERFORMED":
        rows = dimensions.get("NOVELTY", [])
        if not rows:
            raise ProtocolError("Novelty comparison NOT PERFORMED requires a NOVELTY claim locked as NOT ASSESSED")
        for row in rows:
            if str(row["state"]).upper().strip() != "NOT ASSESSED":
                raise ProtocolError(f"{row['id']}: NOVELTY must remain NOT ASSESSED")

    if gate["comparative_benchmark"] == "NOT PERFORMED":
        rows = dimensions.get("COMPARATIVE_PERFORMANCE", [])
        if not rows:
            raise ProtocolError("Comparative benchmark NOT PERFORMED requires a COMPARATIVE_PERFORMANCE claim locked as NOT ASSESSED")
        for row in rows:
            if str(row["state"]).upper().strip() != "NOT ASSESSED":
                raise ProtocolError(f"{row['id']}: COMPARATIVE_PERFORMANCE must remain NOT ASSESSED")

    if gate["execution_status"] != "RUN":
        for row in claims:
            if str(row["state"]).upper().strip() == "INDEPENDENTLY REPRODUCED":
                raise ProtocolError(f"{row['id']}: cannot claim INDEPENDENTLY REPRODUCED when execution_status={gate['execution_status']}")

    return {
        "claim_count": len(claims),
        "claim_ids": sorted(ids),
        "claims": claims,
    }


def build_lock(ledger: dict[str, Any], validator: dict[str, Any], claims_doc: dict[str, Any]) -> dict[str, Any]:
    ls = validate_ledger(ledger)
    gate = validate_validator(validator, ls)
    cs = validate_claims(claims_doc, set(ls["evidence_ids"]), gate)
    return {
        "pipeline_version": VERSION,
        "evidence_gate": "COMPLETE",
        "ledger_sha256": sha256_obj(ledger),
        "validator_sha256": sha256_obj(validator),
        "claim_state_sha256": sha256_obj(claims_doc),
        "claim_ids": cs["claim_ids"],
        "claim_states": {
            str(row["id"]): str(row["state"]).upper().strip() for row in cs["claims"]
        },
        "execution_status": gate["execution_status"],
        "prior_art_comparison": gate["prior_art_comparison"],
        "comparative_benchmark": gate["comparative_benchmark"],
    }


def verify_lock(ledger: dict[str, Any], validator: dict[str, Any], claims_doc: dict[str, Any], lock: dict[str, Any]) -> None:
    expected = build_lock(ledger, validator, claims_doc)
    fields = [
        "evidence_gate", "ledger_sha256", "validator_sha256", "claim_state_sha256",
        "claim_ids", "claim_states", "execution_status", "prior_art_comparison",
        "comparative_benchmark",
    ]
    for field in fields:
        if lock.get(field) != expected.get(field):
            raise ProtocolError(f"Claim-State Lock mismatch in '{field}'; state changed after locking")


def make_manifest(directory: Path, lock: dict[str, Any]) -> dict[str, Any]:
    synthesis = directory / FILES["synthesis"]
    if not synthesis.exists():
        raise ProtocolError(f"missing final synthesis: {synthesis}")
    return {
        "pipeline_version": VERSION,
        "claim_state_sha256": lock["claim_state_sha256"],
        "claim_states": lock["claim_states"],
        "claim_ids": lock["claim_ids"],
        "execution_status": lock["execution_status"],
        "prior_art_comparison": lock["prior_art_comparison"],
        "comparative_benchmark": lock["comparative_benchmark"],
        "final_synthesis_file": FILES["synthesis"],
        "final_synthesis_sha256": sha256_file(synthesis),
    }


def validate_manifest(directory: Path, lock: dict[str, Any], manifest: dict[str, Any]) -> None:
    synthesis = directory / FILES["synthesis"]
    if not synthesis.exists():
        raise ProtocolError(f"missing final synthesis: {synthesis}")

    for field in [
        "claim_state_sha256", "claim_states", "claim_ids", "execution_status",
        "prior_art_comparison", "comparative_benchmark",
    ]:
        if manifest.get(field) != lock.get(field):
            raise ProtocolError(f"Synthesis Manifest mismatch in '{field}'")

    if manifest.get("final_synthesis_file") != FILES["synthesis"]:
        raise ProtocolError("Synthesis Manifest points to an unexpected synthesis file")
    if manifest.get("final_synthesis_sha256") != sha256_file(synthesis):
        raise ProtocolError("final_synthesis.md changed after synthesis manifest creation")

    text = synthesis.read_text(encoding="utf-8")
    missing = [cid for cid in lock["claim_ids"] if re.search(rf"\b{re.escape(cid)}\b", text) is None]
    if missing:
        raise ProtocolError("Final synthesis does not visibly reference Claim ID(s): " + ", ".join(missing))


def init_package(directory: Path, force: bool = False) -> None:
    if directory.exists() and any(directory.iterdir()) and not force:
        raise ProtocolError(f"{directory} is not empty; use --force only if overwrite is intended")
    directory.mkdir(parents=True, exist_ok=True)

    evidence = []
    for i, source in enumerate(REQUIRED_SOURCES, 1):
        evidence.append({
            "id": f"E{i}",
            "source": source,
            "status": "READ",
            "location": "REPLACE_WITH_EXACT_SECTION_FUNCTION_OR_CONDITION",
            "type": "REPLACE_WITH_EVIDENCE_TYPE",
            "evidence": "REPLACE_WITH_SOURCE_SPECIFIC_STATEMENT_OR_CODE_FACT",
            "directly_establishes": "REPLACE_WITH_DIRECTLY_SUPPORTED_FACT",
            "does_not_establish": "REPLACE_WITH_EXPLICIT_LIMIT_OR_NON_IMPLICATION",
            "conditions": [],
        })

    validator = {
        "collector": "COMPLETE",
        "evidence_ledger": "PRESENT",
        "validator": "PASS",
        "evidence_gate": "COMPLETE",
        "execution_status": "NOT RUN",
        "prior_art_comparison": "NOT PERFORMED",
        "comparative_benchmark": "NOT PERFORMED",
        "checks": {name: "PASS" for name in REQUIRED_VALIDATOR_CHECKS},
    }

    claims = {
        "claims": [
            {
                "id": "C1",
                "claim": "REPLACE_WITH_EVALUATED_CLAIM",
                "state": "SUPPORTED",
                "evidence_ids": ["E1"],
                "conditions_scope": "REPLACE_WITH_SCOPE_AND_CONDITIONS",
                "reason": "REPLACE_WITH_REASON",
                "dimension": "FORMAL",
            },
            {
                "id": "C2",
                "claim": "Novelty / prior-art relation",
                "state": "NOT ASSESSED",
                "evidence_ids": [],
                "conditions_scope": "Prior-art comparison was not performed.",
                "reason": "Protocol requires Novelty = NOT ASSESSED.",
                "dimension": "NOVELTY",
            },
            {
                "id": "C3",
                "claim": "Comparative performance",
                "state": "NOT ASSESSED",
                "evidence_ids": [],
                "conditions_scope": "Matched comparative benchmark was not performed.",
                "reason": "Protocol requires Comparative Performance = NOT ASSESSED.",
                "dimension": "COMPARATIVE_PERFORMANCE",
            },
        ]
    }

    synthesis = """# Final Technical Synthesis\n\nWrite only from the locked Claim-State.\nEvery locked Claim ID must remain visibly traceable.\n\nC1 — SUPPORTED\nC2 — NOT ASSESSED\nC3 — NOT ASSESSED\n"""

    save_json(directory / FILES["ledger"], {"evidence": evidence})
    save_json(directory / FILES["validator"], validator)
    save_json(directory / FILES["claims"], claims)
    (directory / FILES["synthesis"]).write_text(synthesis, encoding="utf-8")


def cmd_lock(directory: Path) -> None:
    ledger = load_json(directory / FILES["ledger"])
    validator = load_json(directory / FILES["validator"])
    claims = load_json(directory / FILES["claims"])
    lock = build_lock(ledger, validator, claims)
    save_json(directory / FILES["lock"], lock)
    print("COLLECTOR: PASS")
    print("EVIDENCE LEDGER: PASS")
    print("VALIDATOR: PASS")
    print("EVIDENCE GATE: COMPLETE")
    print("CLAIM-STATE LOCK: PASS")
    print("LOCK SHA256:", lock["claim_state_sha256"])


def cmd_manifest(directory: Path) -> None:
    ledger = load_json(directory / FILES["ledger"])
    validator = load_json(directory / FILES["validator"])
    claims = load_json(directory / FILES["claims"])
    lock = load_json(directory / FILES["lock"])
    verify_lock(ledger, validator, claims, lock)
    manifest = make_manifest(directory, lock)
    save_json(directory / FILES["manifest"], manifest)
    print("CLAIM-STATE LOCK: PASS")
    print("SYNTHESIS MANIFEST: CREATED")
    print("SYNTHESIS SHA256:", manifest["final_synthesis_sha256"])


def cmd_check(directory: Path) -> None:
    ledger = load_json(directory / FILES["ledger"])
    validator = load_json(directory / FILES["validator"])
    claims = load_json(directory / FILES["claims"])
    lock = load_json(directory / FILES["lock"])
    manifest = load_json(directory / FILES["manifest"])

    ls = validate_ledger(ledger)
    gate = validate_validator(validator, ls)
    validate_claims(claims, set(ls["evidence_ids"]), gate)
    verify_lock(ledger, validator, claims, lock)
    validate_manifest(directory, lock, manifest)

    print("COLLECTOR: PASS")
    print("EVIDENCE LEDGER: PASS")
    print("VALIDATOR: PASS")
    print("EVIDENCE GATE: COMPLETE")
    print("CLAIM-STATE LOCK: PASS")
    print("SYNTHESIS STRUCTURAL FIDELITY: PASS")
    print("OVERALL: PROTOCOL COMPLIANT")
    print("NOTE: this is structural/state validation; semantic truth of free prose is not proven by this script.")


def _make_valid_test_package(root: Path) -> None:
    init_package(root)
    ledger = load_json(root / FILES["ledger"])
    for row in ledger["evidence"]:
        row["location"] = "test location"
        row["type"] = "TEST"
        row["evidence"] = f"test evidence for {row['source']}"
        row["directly_establishes"] = "test direct fact"
        row["does_not_establish"] = "test non-implication"
    save_json(root / FILES["ledger"], ledger)

    claims = {
        "claims": [
            {
                "id": "C1",
                "claim": "Current Held-Information Corpus is the present retained information set.",
                "state": "SUPPORTED",
                "evidence_ids": ["E1", "E2", "E4"],
                "conditions_scope": "Current instantiated formal state.",
                "reason": "Bound to protocol/formal/application sources.",
                "dimension": "FORMAL",
            },
            {
                "id": "C2",
                "claim": "Published scaling outcome under fixed protocol.",
                "state": "REPORTED BUT NOT INDEPENDENTLY REPRODUCED",
                "evidence_ids": ["E5", "E6"],
                "conditions_scope": "Execution NOT RUN in this evaluation.",
                "reason": "Published result exists; not re-executed here.",
                "dimension": "REPRODUCIBILITY",
            },
            {
                "id": "C9",
                "claim": "Novelty / prior-art relation",
                "state": "NOT ASSESSED",
                "evidence_ids": [],
                "conditions_scope": "Prior-art comparison NOT PERFORMED.",
                "reason": "Protocol lock.",
                "dimension": "NOVELTY",
            },
            {
                "id": "C10",
                "claim": "Comparative performance",
                "state": "NOT ASSESSED",
                "evidence_ids": [],
                "conditions_scope": "Comparative benchmark NOT PERFORMED.",
                "reason": "Protocol lock.",
                "dimension": "COMPARATIVE_PERFORMANCE",
            },
        ]
    }
    save_json(root / FILES["claims"], claims)
    (root / FILES["synthesis"]).write_text(
        "# Final Synthesis\n\nC1 — SUPPORTED.\nC2 — REPORTED BUT NOT INDEPENDENTLY REPRODUCED.\nC9 — NOT ASSESSED.\nC10 — NOT ASSESSED.\n",
        encoding="utf-8",
    )


def self_test() -> None:
    passed = 0
    total = 5
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)

        p1 = base / "valid"
        _make_valid_test_package(p1)
        ledger = load_json(p1 / FILES["ledger"])
        validator = load_json(p1 / FILES["validator"])
        claims = load_json(p1 / FILES["claims"])
        lock = build_lock(ledger, validator, claims)
        save_json(p1 / FILES["lock"], lock)
        manifest = make_manifest(p1, lock)
        save_json(p1 / FILES["manifest"], manifest)
        validate_manifest(p1, lock, manifest)
        passed += 1
        print("[PASS] valid package")

        p2 = base / "missing-source"
        shutil.copytree(p1, p2)
        led = load_json(p2 / FILES["ledger"])
        led["evidence"] = led["evidence"][:-1]
        try:
            build_lock(led, load_json(p2 / FILES["validator"]), load_json(p2 / FILES["claims"]))
        except ProtocolError:
            passed += 1
            print("[PASS] missing required source rejected")

        p3 = base / "bad-novelty"
        shutil.copytree(p1, p3)
        cl = load_json(p3 / FILES["claims"])
        for row in cl["claims"]:
            if row.get("dimension") == "NOVELTY":
                row["state"] = "SUPPORTED"
                row["evidence_ids"] = ["E1"]
        try:
            build_lock(load_json(p3 / FILES["ledger"]), load_json(p3 / FILES["validator"]), cl)
        except ProtocolError:
            passed += 1
            print("[PASS] novelty rating without prior-art comparison rejected")

        p4 = base / "bad-reproduction"
        shutil.copytree(p1, p4)
        cl = load_json(p4 / FILES["claims"])
        for row in cl["claims"]:
            if row["id"] == "C2":
                row["state"] = "INDEPENDENTLY REPRODUCED"
        try:
            build_lock(load_json(p4 / FILES["ledger"]), load_json(p4 / FILES["validator"]), cl)
        except ProtocolError:
            passed += 1
            print("[PASS] false independent-reproduction upgrade rejected")

        p5 = base / "lock-drift"
        shutil.copytree(p1, p5)
        cl = load_json(p5 / FILES["claims"])
        cl["claims"][0]["state"] = "OPEN"
        try:
            verify_lock(load_json(p5 / FILES["ledger"]), load_json(p5 / FILES["validator"]), cl, load_json(p5 / FILES["lock"]))
        except ProtocolError:
            passed += 1
            print("[PASS] post-lock claim-state drift rejected")

    print(f"SELF-TEST: {passed}/{total} PASS")
    if passed != total:
        raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="IKERUSIKI AI Evidence-Gated Evaluation Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", metavar="DIR", help="create an evaluation package template")
    group.add_argument("--lock", metavar="DIR", help="validate evidence/gate/claims and lock state")
    group.add_argument("--manifest", metavar="DIR", help="create synthesis structural manifest")
    group.add_argument("--check", metavar="DIR", help="validate the complete evaluation package")
    group.add_argument("--self-test", action="store_true", help="run built-in protocol tests")
    parser.add_argument("--force", action="store_true", help="allow --init in a non-empty directory")
    args = parser.parse_args()

    try:
        if args.init:
            init_package(Path(args.init), args.force)
            print(f"Template created: {args.init}")
            print("Next: fill evidence_ledger.json, validator_result.json, claim_state.json")
        elif args.lock:
            cmd_lock(Path(args.lock))
        elif args.manifest:
            cmd_manifest(Path(args.manifest))
        elif args.check:
            cmd_check(Path(args.check))
        elif args.self_test:
            self_test()
        return 0
    except ProtocolError as e:
        print(f"PROTOCOL ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
