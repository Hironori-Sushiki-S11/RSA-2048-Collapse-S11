# IKERUSIKI Adaptive Address — Publication Evidence Ledger
## 公開証拠台帳・外部再現の入口

**Reviewed:** 2026-11-26  
**Status:** evidence routing and reproduction audit, not a new mathematical claim.  
**Research object:** Adaptive Address (AA). RSA and unknown-factor recovery remain downstream applications, not the standard by which the established finite-corpus result is judged.

## 1. Evidence classes / 証拠の階層

| Subject | Current published evidence | Interpretation |
|---|---|---|
| Finite-corpus Address and Collision | [Formal Mathematical Basis](Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_FORMAL_BASIS.md) | Exact residue-equivalence, LCM collision law, residual difference, and finite-state refinement theorems under stated assumptions |
| 32,768 / 65,536 / 131,072-bit, 100-integer corpora | [Reproducer](ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py), [reproduction guide](ADAPTIVE_ADDRESS_SCALING_REPRODUCIBILITY.md) | 15 deterministic published cases: depth 2, zero residual Collisions; the guide records an in-package 15/15 self-check |
| External AI reproduction (Grok 4.5, 2026-08-29) | [Grok report](EXTERNAL_AI_PROTOCOL_REPRODUCTION_GROK_20260829.md) | Reported 15/15 protocol-equivalent execution plus randomized formal checks. It was not direct CLI execution of a Git checkout and is not a human independent reproduction |
| Extended external AI reproduction (Claude Sonnet 5, 2026-08-29) | [Claude report](CLAUDE_ADAPTIVE_ADDRESS_1M_BIT_SCALING_REPORT_20260829.md), [audit archive](ADAPTIVE_ADDRESS_1M_BIT_AUDIT_20260829.zip) | Reported 30/30 collision-free at depth 2 through 1,048,576 bits. The 15 original cases matched archived EXPECTED results; the 15 extended cases had no pre-published EXPECTED baseline. Modified protocol-equivalent source was used |
| 52 + 52 and combined 104 huge integers | [Huge Integers repository](https://github.com/Hironori-Sushiki-S11/IKERUSIKI-Adaptive-Address-Huge-Integers) | Published corpus-specific one-to-one distinctions and controls. Generation by modular exponentiation is an important separate computational effect. The 52 extra integers are not certified primes |
| Fixed-coordinate GCD graph invariance, Stage 14 | [Theorem and results](Boundary-Coordinate-Grid/AA_FACTOR_BRIDGE_STAGE14_REPORT_20261123.md), [reproducer](Boundary-Coordinate-Grid/AA_FACTOR_BRIDGE_STAGE14.py) | Exact fixed-coordinate graph periodicity theorem and scripted checks. Not an impossibility theorem for other AA observables, and not unknown-factor recovery |
| General unknown-factor Address extraction, new primality certificates, universal shallow depth, RSA-2048 break | No established demonstration in the cited evidence | Open, separately testable application questions. Do not infer them from finite-corpus one-to-one identification |

**Scope discipline:** formal theorem, source-code implementation, author self-check, externally reported AI protocol reproduction, and independent human reproduction are different evidence levels. Do not substitute one for another.

### Direct public-source execution (2026-11-26)

[15-case direct execution report](AA_SCALING_DIRECT_REPRODUCTION_20261126.md) and [full stdout](AA_SCALING_DIRECT_REPRODUCTION_20261126.log) record **15/15 matched**, **15/15 Collision-free**, with direct Git-blob SHA confirmation. A [separate Address-residue cross-check](AA_SCALING_ADDRESS_CROSSCHECK_20261126.py) returned **15/15** matching partition trajectories without calling the reproducer's refinement function. This is a ChatGPT execution-environment audit, not independent human replication.

## 2. Reproduce the published AA core

From the main repository root with Python 3:

~~~bash
python3 ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --bits 32768 --seed 20260812
python3 ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --verification all
python3 Boundary-Coordinate-Grid/AA_FACTOR_BRIDGE_STAGE14.py
~~~

The guide states that the first command should report **axes=477|5**, **phi=4950->3->0**, **depth=2**, **collision_free=True**, and **match=True**. The full run covers 15 archived cases. Record the full stdout and environment before making performance comparisons.

For the historical 512/1024/2048/4096-bit finite-corpus exploration, run:

~~~bash
python3 Boundary-Coordinate-Grid/Verification061.py
python3 Boundary-Coordinate-Grid/Verification062.py
~~~

The corpus loader requires exactly named files such as `prime_corpus_512.txt` in `Boundary-Coordinate-Grid/`. The 2026-11-26 publication repair corrects the earlier stray-space filename without modifying its bytes.

For the Huge Integers application, use the **separate** repository's `README.md`, `README.ja.md`, `AA_HUGE_INTEGER.py`, `validate.py`, `results.json`, `validation.json`, and `SHA256SUMS.txt`. Its `validate.py` is a bounded compatibility/invariant test, **not** an independent proof of every unbounded exponent claim.

## 3. External review handoff / 外部検証の記録項目

Ask any reviewer to provide:

- Exact repository, commit SHA, file SHA, environment, and executed command
- Corpus generation, seed, corpus size and bit length; candidate-axis family and Select score
- Selected Address axes, Collision trajectories, depth, and exact-result agreement
- Correct/incorrect/unresolved outcomes, total CPU/wall time, and peak memory where measurable
- Matched controls: same objects, same conditions and same final decision rule, with AA enabled and removed
- Explicit separation of externally rerun outputs from interpretations or source-document assertions

Reviewers should not require a one-time exhaustive identification of an infinite set as an evaluation criterion for per-input or current finite-state work.

## 4. Publication repairs made on 2026-11-26

- Renamed `Boundary-Coordinate-Grid/prime_corpus_512 .txt` to `Boundary-Coordinate-Grid/prime_corpus_512.txt`, matching the import paths used by `Verification061.py` and `Verification062.py`. Content SHA is unchanged.
- Renamed `EXTERNAL_AI_PROTOCOL_REPRODUCTION_GROK_20260829 .md` to `EXTERNAL_AI_PROTOCOL_REPRODUCTION_GROK_20260829.md` to repair the existing README link. Report content is unchanged.
- Created this ledger and added its entry point to the root README.

## 5. Next publication actions

1. Independently run the smallest deterministic case and preserve full execution records.
2. Complete matched AA/AA-removed outcome and resource comparisons where valid.
3. Request independent external replication with archived code, reproducible logs, and a documented source hash.
4. Only upgrade claim status after the relevant evidence passes review.

**No change to AA's existing mathematical proofs or experimental algorithms is asserted by this documentation repair.**
