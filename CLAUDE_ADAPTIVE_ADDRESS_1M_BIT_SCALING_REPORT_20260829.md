# Claude Adaptive Address Scaling Report — Extended Bit Range (32,768–1,048,576 bit)

**Date:** 2026-08-29
**Executed by:** Claude Sonnet 5 (this conversation)
**Repository under test:** `Hironori-Sushiki-S11/RSA-2048-Collapse-S11`
**Target script:** `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py`

---

## 1. Execution method (mandatory disclosure)

- **This is NOT a direct execution of the official CLI.** The `bash_tool` sandbox used for this run has network access disabled (`Enabled: false`), so the repository could not be `git clone`d or `curl`ed directly.
- The actual procedure was: (1) fetch the GitHub blob display of `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py` via `web_fetch`; (2) transcribe that source text verbatim into a local file (`original_reproducer_verbatim.py`); (3) apply the minimal documented changes below to produce `official_reproducer_modified.py`; (4) execute the modified file locally.
- **This is therefore a "protocol-equivalent execution from previously fetched source text," not a guarantee of byte-identical correspondence with the file currently hosted in the repository.** See `diff_output.txt` for the exact, complete diff against the verbatim-transcribed original.

## 2. Changes from the original source (see `diff_output.txt` for full diff)

1. `EXPECTED` dictionary lookup changed from direct indexing (`EXPECTED[(bit_size, seed)]`, which raises `KeyError` for unregistered keys) to `.get()`, so that bit sizes with no pre-registered baseline (262144 / 524288 / 1048576) return `match=None` instead of crashing. The existing 15 entries for 32768/65536/131072 were not altered.
2. `choose_cases()` / CLI `argparse` interface replaced with a direct loop over target bit sizes and seeds (not needed for this run).
3. All other logic — `generate_corpus`, `collision_potential`, `entropy_of_partition`, `refine_by_q`, and the body of `run_case` — is unmodified.
4. Two additional fields added to the returned result dict: `final_lcm` (the final LCM value `L`) and `executed` (boolean).

No other lines were changed.

## 3. Environment

- Python: 3.12.3 (CPython, cache_tag=cpython-312)
- OS: Linux 6.18.44-fc-v22 #1 SMP PREEMPT_DYNAMIC, x86_64
- Model: Claude Sonnet 5

## 4. Results summary

- **Existing range (32,768 / 65,536 / 131,072 bit, 5 seeds each = 15 cases):** all 15 cases re-executed under the modified script. **15/15 `match=True`** against the `EXPECTED` dictionary already present in the official source.
- **New range (262,144 / 524,288 / 1,048,576 bit, 5 seeds each = 15 cases):** no `EXPECTED` baseline exists in the official source for these bit sizes. **All 15 cases report `match=None` (N/A)** — no self-generated `match=True` values were produced, per instruction.
- **Depth:** 30/30 cases converged at **depth = 2**, with no case requiring more or fewer axes, across the full 32,768–1,048,576 bit range (a ~32× increase in bit length).
- **Collision-free status:** 30/30 cases reached `collision_free = True`.
- **Errors / resource constraints:** 0/30 cases errored or were skipped.
- **Execution time** scaled approximately linearly with bit length (≈1.3s at 32,768-bit → ≈41.6s at 1,048,576-bit), consistent with the cost of big-integer arithmetic rather than any increase in search depth.

## 5. Updated vs. unresolved assessment

**Updated by this run:**
- The reservation that depth might increase with bit length is withdrawn for the tested range. Depth remained fixed at 2 across all 30 cases spanning 32,768–1,048,576 bits.
- Execution-time growth was empirically confirmed to be a linear big-integer arithmetic cost, separable from and unrelated to any growth in search depth.

**Not updated / unresolved by this run:**
- This result concerns only the depth-vs-bit-length relationship for distinguishing a known finite corpus of 100 random values. It says nothing about, and was not designed to evaluate, RSA-2048 factorization or any single-unknown-integer factorization task.
- The flat depth-2 result is quantitatively consistent with a birthday-bound style combinatorial explanation (identification cost depends on corpus size, not on the bit length of individual elements), which was proposed prior to this run and is not contradicted by it.
- Correspondence between the Formal Basis document and the Reproducer implementation remains unconfirmed (not accessible via available tooling).
- Blind Spot / EXPAND behavior remains untested — no case in this run reached a depth where those paths would trigger.

---

## 6. File manifest (SHA-256, see `SHA256SUMS.txt` for the authoritative list)

| File | Purpose |
|---|---|
| `official_reproducer_modified.py` | Script actually executed |
| `original_reproducer_verbatim.py` | Verbatim-transcribed original (diff baseline) |
| `diff_output.txt` | Exact diff, original → modified |
| `new15_combined.json` | New 15 cases (262144/524288/1048576-bit × 5 seeds), raw |
| `all30_combined.json` | All 30 cases combined, raw |
| `raw_stdout_original_range.json` | Existing 15 cases (32768/65536/131072-bit × 5 seeds), raw |
| `raw_stdout_phase1.json` | 3 new bit sizes × seed 20260812 only |
| `raw_stdout_phase2_262144.json` | 262144-bit × remaining 4 seeds |
| `raw_stdout_phase2_524288.json` | 524288-bit × remaining 4 seeds |
| `raw_stdout_phase2_1048576.json` | 1048576-bit × remaining 4 seeds |
