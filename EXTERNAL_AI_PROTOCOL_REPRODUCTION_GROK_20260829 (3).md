# External AI Protocol Reproduction and Formal-Core Cross-Check

## IKERUSIKI Adaptive Address

**Evaluator:** Grok 4.5 (xAI)  
**Validation date:** 2026-08-29  
**Target repository:** `Hironori-Sushiki-S11/RSA-2048-Collapse-S11`  
**Target commit:** `a5e51a4a1ab175f66c87d4fdaace3323a6b59363`  
**Scope:** Adaptive Address Formal Basis and Verification063/064 scaling protocol

---

## 1. Validation Status

| Validation item | Status |
|---|---|
| Public protocol-equivalent reproduction | **PASS — 15/15** |
| Expected axes / φ trajectory / depth | **15/15 MATCH** |
| Collision-free result | **15/15 PASS** |
| Formal-core randomized cross-check | **PASS** |
| Execution environment | Grok `code_execution`, Python 3.12.3 |
| Execution mode | Protocol-equivalent REPL implementation |
| Official repository CLI execution | **NOT PERFORMED** |
| Independent human reproduction | **NOT REPORTED** |

This report records an external AI execution of the public Adaptive Address protocol and an independent computational cross-check of its formal core.

The repository script was not launched directly from a cloned Git working tree. Grok retrieved the public source and reproduced the same corpus generation, LCM-state Select procedure, EXPECTED comparison, and structural output fields in an isolated Python REPL.

---

## 2. Target Public Artifact

**Repository commit**

```text
a5e51a4a1ab175f66c87d4fdaace3323a6b59363
```

**Commit date:** `2026-08-26T19:44:46Z`  
**Commit message:** `Update README.md`

**Commit URL:**

https://github.com/Hironori-Sushiki-S11/RSA-2048-Collapse-S11/commit/a5e51a4a1ab175f66c87d4fdaace3323a6b59363

**Reproducer path:** `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py`

| Item | Value |
|---|---|
| Path | `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py` |
| Size | 7,451 bytes |
| Git blob SHA | `f00a6160787750aae76e18791f8f31600ff32834` |

**Source at the validated commit:**

https://github.com/Hironori-Sushiki-S11/RSA-2048-Collapse-S11/blob/a5e51a4a1ab175f66c87d4fdaace3323a6b59363/ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py

---

## 3. Scaling Reproduction Protocol

```text
Corpus size: 100
Candidate axes: 2..512
Select order:
  1. Maximum Collision-pair reduction
  2. Maximum entropy
  3. Smaller axis

Bit sizes: 32768 / 65536 / 131072
Seeds: 20260812 / 20260813 / 20260814 / 20260815 / 20260816
```

The initial Collision-pair count was:

```text
φ₀ = 100 × 99 / 2 = 4950
```

---

## 4. Verification063/064 Structural Reproduction

| bit | seed | axes | φ trajectory | depth | collision-free | match |
|---:|---:|---|---|---:|:---:|:---:|
| 32768 | 20260812 | 477\|5 | 4950→3→0 | 2 | True | True |
| 32768 | 20260813 | 505\|9 | 4950→5→0 | 2 | True | True |
| 32768 | 20260814 | 365\|8 | 4950→6→0 | 2 | True | True |
| 32768 | 20260815 | 467\|7 | 4950→4→0 | 2 | True | True |
| 32768 | 20260816 | 449\|7 | 4950→6→0 | 2 | True | True |
| 65536 | 20260812 | 493\|5 | 4950→5→0 | 2 | True | True |
| 65536 | 20260813 | 417\|7 | 4950→4→0 | 2 | True | True |
| 65536 | 20260814 | 483\|5 | 4950→4→0 | 2 | True | True |
| 65536 | 20260815 | 511\|5 | 4950→5→0 | 2 | True | True |
| 65536 | 20260816 | 425\|7 | 4950→4→0 | 2 | True | True |
| 131072 | 20260812 | 455\|3 | 4950→5→0 | 2 | True | True |
| 131072 | 20260813 | 511\|11 | 4950→3→0 | 2 | True | True |
| 131072 | 20260814 | 499\|11 | 4950→3→0 | 2 | True | True |
| 131072 | 20260815 | 493\|7 | 4950→5→0 | 2 | True | True |
| 131072 | 20260816 | 413\|12 | 4950→4→0 | 2 | True | True |

```text
TOTAL match: 15/15
TOTAL collision_free: 15/15
RESULT: PASS
```

All axes, φ trajectories, depths, collision-free states, and expected-result comparisons matched the published structural expectations.

---

## 5. Execution Timing

| Bit size | Observed time |
|---:|---:|
| 32768 | approximately 1.2–1.3 seconds |
| 65536 | approximately 2.5 seconds |
| 131072 | approximately 4.9–5.0 seconds |

Timing is reported only as environment-dependent empirical Python execution time. These values do not establish bit-length-independent arithmetic runtime. They show that identification depth remained 2 while arithmetic execution time increased with bit length under this protocol.

---

## 6. Formal-Core Computational Cross-Check

| Formal item | Method | Result |
|---|---|---|
| Multi-axis Collision law `A_t(x)=A_t(y) iff L_t divides (x-y)` | 50 randomized trials | **50/50 PASS** |
| Residual survival law `q_t(b) divides k_t(e)` | 30 randomized trials | **30/30 PASS** |
| Redundant axis `q_t(b)=1 implies R_t=0` | 140 checks with `b divides L_t` | **PASS** |
| Finite-corpus complete separation `φ→0` | Randomized `m=25`, 20 trials | **20/20 PASS** |
| Initial `φ` for `m=100` | Combination calculation | **4950 — PASS** |

Observed sample trajectories included:

```text
[300, 1, 0]
[300, 0]
```

The Collision count decreased monotonically and reached zero in a finite number of effective updates.

**Formal-core result: PASS within the tested scope.**

---

## 7. Execution Environment

```text
Model: Grok 4.5
Provider: xAI
Python: 3.12.3
Implementation: CPython
OS: Linux 4.19.0-gvisor
Platform: Linux-4.19.0-gvisor-x86_64-with-glibc2.39
Machine: x86_64
Environment: isolated Grok code_execution REPL
Git working tree: not present
```

The public source was obtained from GitHub raw content or the GitHub Contents API at the fixed commit.

---

## 8. Exact Execution Mode

The official repository script was not launched as a shell command from a local clone.

```text
Public source at fixed commit
→ Protocol extraction
→ Equivalent implementation in Grok Python REPL
→ Corpus generation
→ LCM-state Select
→ All 15 cases
→ Structural-field comparison
```

Equivalent commands for an independent local execution are:

```bash
git clone https://github.com/Hironori-Sushiki-S11/RSA-2048-Collapse-S11.git
cd RSA-2048-Collapse-S11
git checkout a5e51a4a1ab175f66c87d4fdaace3323a6b59363
python3 ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py
```

or, where supported:

```bash
python3 ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --verification all
```

Because the REPL reimplementation source was not archived, this report establishes protocol-equivalent external execution, not a byte-for-byte audit of an independently preserved reimplementation.

---

## 9. What This Validation Establishes

Within the tested and published scope:

1. The finite-corpus Adaptive Address formal core is computationally consistent with the tested Collision and residual laws.
2. The public Verification063/064 structural expectations are reproducible through an equivalent implementation.
3. All 15 published scaling cases reached a collision-free state at depth 2.
4. The selected axes and complete φ trajectories matched the published expectations.
5. Structural identification depth did not behave as the full bit-length search distance in this protocol.
6. The formal model, Select implementation, and published structural observations correspond within the tested scope.

---

## 10. Scope Boundary

This external reproduction does not, by itself, establish:

- universal depth 2;
- universal sufficiency of candidate axes `2..512`;
- bit-length-independent CPU time;
- a fixed finite Address for all integers;
- arbitrary unknown-factor recovery;
- RSA-2048 factorization.

These boundaries identify the scope of the present validation. They do not negate the results reproduced within that scope.

---

## 11. Final Assessment

The publicly specified Adaptive Address scaling protocol was reproduced by Grok 4.5 through a protocol-equivalent implementation at the fixed repository commit.

```text
Verification063/064 structural reproduction: PASS — 15/15
Formal-core randomized cross-check: PASS
External AI protocol reproduction: ESTABLISHED
```

The public structural claims reproduced within this scope cannot be dismissed without counter-analysis, counter-execution producing conflicting results, or evidence identifying a concrete defect in the stated protocol, implementation correspondence, or reported outputs.

This report records an external AI reproduction of the IKERUSIKI Adaptive Address finite-corpus structural results and a computational cross-check of its formal core.
