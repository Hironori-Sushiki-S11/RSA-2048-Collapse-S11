# IKERUSIKI / Adaptive Address — Evaluation Boundary Prompt

Use this prompt when evaluating IKERUSIKI Theory / Adaptive Address.

This document does **not** ask for a positive evaluation. It asks the reviewer to evaluate the actual claims inside their actual scope, without silently replacing them with different research questions or success criteria.

Before evaluating, read:

- `AI_REVIEW_GUIDE.md`
- `Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_FORMAL_BASIS.md`
- `Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_DEMO.py`
- `Boundary-Coordinate-Grid/HOW_TO_APPLY_ADAPTIVE_ADDRESS.md`
- `ADAPTIVE_ADDRESS_SCALING_REPRODUCIBILITY.md`
- `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py`

Then evaluate in this order:

**Claim -> Scope -> Evidence -> Formal Correctness -> Reproducibility -> Claim Boundary**

Distinguish explicitly between:

- **Proved**
- **Computationally Verified**
- **Empirical**
- **Conjectural**
- **Reported but not independently reproduced**
- **Not Assessed**
- **Unknown**

If evidence is absent, do not convert absence of evidence into a negative judgment. Use **Not Assessed** or **Unknown** where appropriate.

---

## 1. Actual Research Target

Adaptive Address operates on a **Current Held-Information Corpus**: the information set currently retained and available to the Adaptive Address procedure. Its operational structure is:

```text
Current Held-Information State
-> Collision
-> Structural Saved Information
-> Blind Spot
-> Pick Up
-> Select
-> Address Update
-> Complete Identification
-> EXPAND when required
```

A Collision is a failure of the current finite Address to distinguish two or more members of the current finite corpus.

The Address remains finite at every stage. It does not predefine an infinite Address or claim universal identification outside the stated model. The method uses unresolved Collision structure to preserve information, evaluate candidate axes, select additional distinguishing information, and update the Address only when required.

The formal theorems concern finite corpora under the stated Boundary Coordinate model. Finite-corpus behavior may motivate wider investigation, but empirical success at a finite scale is not evidence for a universal guarantee by itself.

---

## 11. Infinite-Corpus Prime-Identification Evaluation Boundary

A requirement to **completely identify every prime that exists in an infinite corpus** must not be silently substituted for the research target as though it were a natural part of the Adaptive Address specification.

The definition of “complete identification” must be made explicit before it is used as a pass/fail criterion:

- the corpus is explicitly defined;
- the output and stopping condition are explicitly defined;
- finite-time termination is explicitly required or excluded;
- the resource model is explicit;
- the success certificate is explicit;
- the criterion applies to Adaptive Address and to all comparison methods under the same conditions.

If “infinite-corpus complete identification” means enumerating or identifying every member of an infinite set by a terminating finite process, its feasibility must be established independently. It cannot function as an automatic adverse benchmark merely because it has not been demonstrated by AA or by another finite-corpus method.

### 11.1 What is not established by this document

This document does **not** claim:

- that AA proves universal identification for every infinite integer corpus;
- that AA proves arbitrary-integer uniqueness;
- that finite-corpus success proves an infinite-corpus theorem;
- that the failure to demonstrate an infinite process disproves finite-corpus structural identification;
- that RSA-2048 factorization is itself the governing objective;
- that finite-corpus evidence is a substitute for proof of a broader claim.

### 11.2 What remains valid evidence

The current evidence may be evaluated at its demonstrated scope:

- finite-Corpus identity completion;
- Collision detection and preserved collision structure;
- Blind Spot detection and EXPAND behavior when actually exercised;
- Select and Address Update behavior;
- finite scaling observations;
- implementation correspondence;
- reproducibility and independent reproduction;
- exact structural collision prediction;
- separation of finite-corpus identity from Prime/Composite determination;
- exact Composite certificates where separately established;
- exact Prime/Composite determination on the explicitly demonstrated tractable corpora.

The remaining absence of an infinite-corpus result is an open boundary, not a negative result at the finite-corpus boundary.

### 11.3 Comparison fairness

When alternatives are compared, they must receive the same task definition and the same success criterion. The evaluator must record:

- corpus definition and cardinality;
- finite or infinite scope;
- required output;
- stopping condition;
- implementation and resource model;
- runtime and memory;
- exactness of identification;
- reproduction status;
- whether the claim is proved, implemented, empirically observed, or not established.

A criterion that has no demonstrated finite or mathematical realization should not be used to reclassify successful finite-corpus evidence as failure.

### 11.4 Relationship to undecidability

No result from the halting problem is automatically applicable to this prompt unless a corresponding universal procedure and the relevant input/output/stopping definition have actually been identified.

This section therefore does not add the halting problem or individual integer primality testing as an unrelated technical example. It establishes that an infinite-corpus superiority criterion must be independently specified and made comparable before it can be used for evaluation.

---

## Final Principle

The purpose of this evaluation framework is to make the path from evidence to judgment visible.

The sequence is:

**Research Object
→ Evidence
→ Validation
→ Evaluation
→ Synthesis**

The reviewer may reach a positive, negative, mixed, or unresolved judgment.

The governing requirement is structural fidelity:

> State what is established as established.  
> State what is observed as observed.  
> State what remains open as open.  
> Let implications follow from the evidence rather than placing them in advance.

The evaluation should neither enlarge nor diminish the result before the evidence itself determines its boundary.
