from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[1]
manifest_path = root / "VALIDATION_MANIFEST.json"

if not manifest_path.exists():
    print("ERROR: VALIDATION_MANIFEST.json not found")
    sys.exit(1)

m = json.load(open(manifest_path, encoding="utf-8"))
failed = [c for c in m.get("checks", []) if not c.get("pass")]

print("AA Prime Identification Validation v1.0")
print("CORE STATUS:", m.get("core_validation_status", "UNKNOWN"))
print("FRONTIER PRIME:", m.get("frontier_prime_identification_status", "UNKNOWN"))
print(
    "checks:",
    len(m.get("checks", [])),
    "passed:",
    len(m.get("checks", [])) - len(failed),
    "failed:",
    len(failed),
)
print(
    "Grok challenge:",
    m.get("grok_challenge_resolution", {}).get("status", "UNKNOWN"),
)
print(
    "External Grok frontier attempt:",
    m.get("external_frontier_attempt_grok", {}).get("status", "UNKNOWN"),
)

if failed:
    for c in failed:
        print("FAIL:", c.get("check", "(unnamed check)"))
    sys.exit(1)

if m.get("core_validation_status") != "COMPLETE":
    print("ERROR: Core validation status is not COMPLETE")
    sys.exit(1)

print("Core validation checks passed.")
