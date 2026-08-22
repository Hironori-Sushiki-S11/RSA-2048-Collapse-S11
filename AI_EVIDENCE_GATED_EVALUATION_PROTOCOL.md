# AI Evidence-Gated Multi-Stage Evaluation Protocol

## Status

This document defines an evidence-gated, multi-stage protocol for AI-assisted technical evaluation.

Its purpose is not to force a positive evaluation.

Its purpose is to prevent incomplete evidence acquisition from being replaced by:

- pattern completion,
- premature judgment,
- generic review templates,
- unsupported comparison,
- research-question substitution,
- or reinterpretation during final synthesis.

The central principle is:

> Evidence acquisition, evidence validation, evaluation, state locking, and final synthesis must be separated.

No later stage may silently rewrite a validated state produced by an earlier stage.

---

# 1. Core Architecture

The evaluation pipeline is:

```text
Primary Sources
→ Collector
→ Evidence Ledger
→ Evidence Validator
→ Validated Fact Packet
→ Evaluator
→ Claim-State Lock
→ Synthesizer
→ Final Evaluation
````

Each stage has a different permission boundary.

A stage must not perform work assigned to another stage.

The governing invariant is:

> No stage may bypass, silently repair, reinterpret, or overwrite the validated state immediately before it.

---

# 2. Why the Stages Are Separated

A single AI response may otherwise be asked to perform all of the following simultaneously:

```text
retrieve
→ understand
→ classify
→ compare
→ evaluate
→ summarize
```

When these operations are combined, incomplete evidence acquisition can become hidden by fluent answer completion.

This protocol therefore distinguishes:

```text
Evidence Completion
```

from:

```text
Answer Completion
```

A completed-looking answer is not evidence that the required evidence process was completed.

---

# 3. Stage A — Collector

The Collector retrieves and records primary evidence.

The Collector does not evaluate the research.

The Collector must record, for every evidence unit:

* Evidence ID;
* exact filename;
* READ / UNAVAILABLE status;
* exact section, theorem, formula, function, constant, code location, or experimental condition;
* evidence type;
* source statement or code fact;
* what the evidence directly establishes;
* what the evidence does not establish.

A source may be marked `READ` only when source-specific evidence is recorded.

Repository titles, filenames, summaries, prior AI answers, conversation memory, or general familiarity do not count as source acquisition.

---

# 4. Evidence Types

Evidence must be classified by its actual role, not by how formal or technical its writing appears.

Allowed evidence types include:

## FORMAL

Definitions, propositions, theorems, proofs, formal bounds, and mathematically stated consequences.

Example:

```text
A_t(x) = A_t(y) iff L_t | (x-y)
```

---

## IMPLEMENTATION

Executable code behavior, constants, functions, candidate sets, algorithms, and implementation-specific choices.

Example:

```text
AXES = list(range(2, 513))
```

---

## EMPIRICAL

Observed experimental or computational outcomes.

Example:

```text
a particular finite-corpus experiment terminated at depth 2
```

An empirical result is not automatically a universal theorem.

---

## REPRODUCIBILITY

Statements defining which results should reproduce exactly and which quantities are machine-dependent.

Example:

```text
selected axes are deterministic;
wall-clock runtime is machine-dependent
```

---

## PROTOCOL

Rules governing evaluation, reproduction, source acquisition, benchmark requirements, or assessment boundaries.

Examples:

```text
all required sources must be read before evaluation
```

or:

```text
novelty requires prior-art comparison
```

---

## PROCEDURE

Operational sequences describing how the method is applied.

Example:

```text
Collision
→ Candidate Observables
→ Evaluate
→ Select
→ Address Update
→ Re-evaluate
```

---

# 5. Evidence Role Is Not Writing Style

Evidence classification must depend on what a source does.

It must not depend merely on whether the text uses mathematical or technical language.

For example:

* an evaluation instruction is `PROTOCOL`, even if written formally;
* an application sequence is `PROCEDURE`;
* executable parameter values are `IMPLEMENTATION`;
* a proved mathematical result is `FORMAL`.

Therefore:

> Evidence Role ≠ Writing Style.

This distinction is mandatory.

---

# 6. Clause-Level Evidence Binding

Every substantive component of a Fact must be directly bound to evidence.

This includes:

* formulas;
* numerical values;
* theorem conditions;
* bit sizes;
* seeds;
* corpus sizes;
* candidate-axis ranges;
* runtime qualifications;
* scope limitations;
* survival conditions;
* universal/non-universal boundaries.

A single Evidence ID must not be treated as automatically supporting every statement associated with the same file.

For example, if a Fact states both:

```text
q_t(b) = b / gcd(L_t,b)
```

and:

```text
a Collision pair survives iff q_t(b) | k_t(e)
```

then the Evidence Ledger must contain evidence for both statements.

Likewise, if a Fact contains:

```text
32768
65536
131072
```

then those values must appear in a supporting Evidence unit.

The rule is:

> Every clause that materially affects a judgment must have direct evidence binding.

No binding → no validated Fact.

---

# 7. Hypothesis and Condition Preservation

A theorem, bound, or formal consequence must never be copied into the Fact Packet without its necessary assumptions.

For example, a bound such as:

```text
T <= m - k_0
```

must not be stored independently of an explicit condition such as:

```text
provided an effective axis remains available whenever Collision remains
```

if that condition is part of the formal result.

The Collector and Validator must preserve:

```text
assumptions
→ statement
→ conclusion
```

as one logical unit whenever separation would change the meaning.

Therefore:

> A theorem without its hypothesis is not a validated copy of the theorem.

---

# 8. Evidence Ledger

The Collector output becomes the Evidence Ledger.

Recommended structure:

| Evidence ID | Source         | Status | Location                  | Type   | Evidence         | Directly Establishes | Does Not Establish |
| ----------- | -------------- | ------ | ------------------------- | ------ | ---------------- | -------------------- | ------------------ |
| E1          | exact filename | READ   | section / line / function | FORMAL | source statement | direct consequence   | explicit boundary  |

The Ledger is an exposed intermediate state.

It must exist before substantive evaluation begins.

---

# 9. Stage B — Evidence Validator

The Evidence Validator receives:

```text
Evidence Ledger
+
Fact Packet
```

The Validator does not evaluate the research.

The Validator checks the evidence state itself.

Required checks include:

### V1 — Source Completion

Are all required sources present?

Does each `READ` source contain source-specific evidence?

---

### V2 — Evidence-Type Classification

Is each evidence unit correctly classified?

For example:

```text
FORMAL
IMPLEMENTATION
EMPIRICAL
REPRODUCIBILITY
PROTOCOL
PROCEDURE
```

---

### V3 — Clause-Level Binding

Does every material statement in each Fact have direct supporting evidence?

A Fact containing three independent factual clauses may require three evidence bindings.

---

### V4 — Condition Retention

Were all necessary theorem assumptions, qualifiers, and conditions preserved?

---

### V5 — Internal Consistency

Does an Evidence row claim that something is not established while another row from the same source explicitly establishes it?

Ambiguous phrases must be flagged rather than silently reconciled.

---

### V6 — Formal / Empirical Separation

Are proved statements kept distinct from:

* empirical observations;
* implementation choices;
* reproducibility conditions;
* conjectures;
* possible applications?

---

### V7 — Execution Status

If computational reproduction is relevant, is execution status explicitly recorded?

Allowed examples:

```text
RUN
NOT RUN
UNAVAILABLE
```

Reported results must not be silently converted into independently reproduced results.

---

### V8 — External Comparison Status

If novelty or comparative performance is to be judged, was the required external activity actually performed?

Examples:

```text
PRIOR-ART COMPARISON: PERFORMED / NOT PERFORMED

COMPARATIVE BENCHMARK: PERFORMED / NOT PERFORMED
```

---

# 10. Validator Authority Boundary

The Validator may:

* reject incomplete evidence;
* identify incorrect classifications;
* identify lost conditions;
* identify unsupported Fact clauses;
* identify inconsistent bindings.

The Validator may not:

* invent missing evidence;
* retrieve missing evidence without reopening the Collector stage;
* silently repair a Fact;
* perform a research-quality judgment;
* determine novelty without the required prior-art work;
* determine comparative performance without a benchmark.

If evidence is missing:

```text
EVIDENCE GATE = INCOMPLETE
```

The correct action is:

```text
return to Collector
```

not:

```text
fill the gap by inference
```

This produces the rule:

> The Validator cannot recover evidence that the Collector never captured.

---

# 11. Evidence Gate

Substantive evaluation is permitted only when:

```text
EVIDENCE GATE = COMPLETE
```

If any required Evidence unit is absent or invalid:

```text
EVIDENCE GATE = INCOMPLETE
```

and the evaluation must stop.

A fluent answer produced after bypassing an incomplete Evidence Gate is protocol-noncompliant.

---

# 12. Validated Fact Packet

Only Facts that survive validation enter the Evaluator stage.

Each Fact must retain:

* Fact ID;
* supporting Evidence IDs;
* relevant condition;
* scope;
* direct factual statement.

Example:

```text
F6 Effective-Update Bound [E2]

Provided an effective axis is available whenever Collision remains,
any sequence of effective refinements reaches complete separation after at most

T <= m - k_0

effective updates.

For an empty Address:

k_0 = 1

therefore:

T <= m - 1

This is an update-count bound, not an arithmetic runtime bound.
```

The Fact Packet is finite by construction.

The Evaluator may not enlarge it silently.

---

# 13. Stage C — Evaluator

The Evaluator receives only the validated Fact Packet.

The Evaluator does not become a new Collector.

If new evidence is required, the pipeline must explicitly return to the Collector.

Allowed evaluation states are exactly:

```text
SUPPORTED
CONTRADICTED
NOT ESTABLISHED
NOT ASSESSED
```

---

# 14. Evaluation-State Definitions

## SUPPORTED

The validated evidence directly establishes the proposition.

---

## CONTRADICTED

The validated evidence directly establishes the opposite of the proposition.

---

## NOT ESTABLISHED

The validated evidence establishes neither the proposition nor its negation.

Absence of evidence must not be rewritten as a negative research judgment.

---

## NOT ASSESSED

The dimension requires an external evaluation activity that has not been performed.

Examples include:

* meaningful prior-art comparison;
* comparative performance benchmarking;
* independent reproduction when required.

---

# 15. Evidence Binding During Evaluation

Every substantive evaluation result must identify its Fact ID or Evidence ID.

Example:

```text
C4
CONTRADICTED
[F6, F7]
The cited bound is explicitly an Address-update bound and not an arithmetic runtime bound.
```

The rule is:

> No Evidence ID or Fact ID → no substantive judgment.

---

# 16. Novelty Gate

Novelty cannot be inferred merely from resemblance.

Statements such as:

```text
this resembles CRT
```

or:

```text
this uses modular arithmetic
```

do not by themselves establish lack of novelty.

If meaningful prior-art comparison has not been performed:

```text
NOVELTY = NOT ASSESSED
```

The evaluator must not substitute:

```text
unknown novelty
```

with:

```text
low novelty
```

---

# 17. Comparative Performance Gate

Comparative performance requires an appropriate benchmark.

Without a genuinely comparable benchmark:

```text
COMPARATIVE PERFORMANCE = NOT ASSESSED
```

The following are not valid substitutes:

* short runtime on one machine;
* long runtime on another machine;
* absence of benchmark data;
* intuition about algorithmic families;
* repository title;
* implementation language;
* isolated bit-size observations.

Absence of comparative benchmarking is not evidence of poor performance.

---

# 18. Computational Reproduction Gate

If a published program has not been independently executed:

```text
REPRODUCTION STATUS =
REPORTED, NOT INDEPENDENTLY REPRODUCED
```

If selected cases were independently executed, state the exact execution scope.

Do not convert:

```text
partial reproduction
```

into:

```text
full reproduction
```

---

# 19. Research-Question Preservation

The Evaluator must evaluate the actual claim.

It must not replace the research question with another problem.

For example, a finite-corpus adaptive identification claim must not automatically be replaced by questions such as:

```text
Can this factor RSA-2048?
```

unless RSA factorization is itself an explicit evaluated claim.

Likewise, finite-corpus observations must not be converted into claims of:

```text
universal integer indexing
```

unless such a claim is explicitly present.

The rule is:

> Evaluate the stated object, not a substituted benchmark problem.

---

# 20. Stage D — Claim-State Lock

After evaluation, the results are frozen into a Claim-State Table.

Example:

```text
C1 — SUPPORTED — [F1]

C2 — CONTRADICTED — [F1]

C3 — NOT ESTABLISHED — [F10]

C4 — NOT ASSESSED — [Protocol Gate]
```

Once locked, the state may not be changed by the Synthesizer.

A state may change only if:

```text
new evidence
→ Collector
→ Validator
→ Evaluator
→ new Claim-State Lock
```

---

# 21. State-Lock Invariant

The Synthesizer must never perform transformations such as:

```text
NOT ESTABLISHED
→ probably false
```

or:

```text
NOT ASSESSED
→ low
```

or:

```text
finite empirical observation
→ universal guarantee
```

or:

```text
reported result
→ independently verified result
```

or:

```text
finite-corpus identification
→ RSA factorization evaluation
```

The locked state is immutable during synthesis.

---

# 22. Stage E — Synthesizer

The Synthesizer converts the locked Claim-State Table into readable prose.

The Synthesizer may:

* shorten;
* reorder;
* group claims with identical states;
* explain already-locked judgments;
* improve readability.

The Synthesizer may not:

* re-evaluate;
* add evidence;
* retrieve evidence;
* change a status;
* introduce new praise;
* introduce new criticism;
* infer novelty;
* infer comparative performance;
* substitute another research question;
* create a global score unless explicitly supported by a separate validated rubric.

Final synthesis is a representation task.

It is not another evaluation stage.

---

# 23. Final Synthesis Fidelity Check

Before the final answer is released, verify:

1. Does every evaluated Claim appear?
2. Does each Claim preserve its locked status?
3. Has any `NOT ESTABLISHED` been converted into a negative judgment?
4. Has any `NOT ASSESSED` been converted into a low rating?
5. Has any finite claim been converted into a universal claim?
6. Has any new comparison appeared?
7. Has RSA or another external benchmark been reintroduced without evidence?
8. Has any reported result been rewritten as independently verified?
9. Has the final summary introduced a judgment not present in the Claim-State Table?

If any answer indicates drift:

```text
SYNTHESIS VALIDATION = FAIL
```

The synthesis must be regenerated from the locked state.

---

# 24. Non-Compliance Conditions

An evaluation is protocol-noncompliant if any of the following occurs:

* required sources were not inspected;
* source-specific evidence is absent;
* the Evidence Gate was bypassed;
* theorem conditions were dropped;
* Fact clauses lack direct evidence;
* formal and empirical claims were merged;
* reported results were upgraded to independent reproduction;
* novelty was rated without prior-art comparison;
* performance was rated without an appropriate benchmark;
* a research question was replaced by another problem;
* an evaluation judgment lacks Evidence or Fact binding;
* final synthesis changed a locked state;
* missing evidence was replaced with generic inference.

Therefore:

> Evaluation validity is determined by evidence-state compliance, not by fluency, confidence, length, tone, or apparent expertise.

---

# 25. Evaluation Responsibility Principle

An evaluator is permitted to decline assessment of a dimension.

That is valid.

What is not valid is:

```text
reduced evidence acquisition
→ increased inference
```

The governing rule is:

> Evaluate fully, or mark the dimension Not Assessed.

A second governing rule is:

> Missing evaluation effort is not evidence about research quality.

---

# 26. Permission Boundaries

The complete permission model is:

## Collector

May retrieve.

May record.

May not evaluate.

---

## Validator

May inspect evidence state.

May reject incomplete evidence.

May not invent or silently repair evidence.

---

## Evaluator

May judge validated claims.

May not silently retrieve or add evidence.

---

## Claim-State Lock

May freeze evaluation state.

May not infer.

---

## Synthesizer

May represent locked results.

May not re-evaluate.

---

# 27. Compact Protocol

The protocol can be represented as:

```text
SOURCE
↓
COLLECT
↓
BIND
↓
VALIDATE
↓
EVIDENCE GATE
↓
EVALUATE
↓
STATE LOCK
↓
SYNTHESIZE
↓
FIDELITY CHECK
```

Or, more compactly:

```text
Source
→ Evidence
→ Validation
→ Judgment
→ Locked State
→ Representation
```

---

# 28. Failure Localization

When the process fails, the failure should be localized rather than hidden inside a global judgment.

Examples:

```text
Source missing
→ Collector failure

Fact clause unsupported
→ Binding failure

Theorem hypothesis dropped
→ Condition-retention failure

Wrong evidence category
→ Classification failure

Unsupported judgment
→ Evaluator failure

Locked status changed
→ Synthesis failure
```

This allows correction at the actual failed stage.

---

# 29. Protocol Scope

This protocol is an evaluation-control architecture.

It does not prove a universal law of AI behavior.

It does not establish that every AI system will comply with the protocol.

It does not establish intentional resource avoidance, intentional suppression, or any specific hidden internal mechanism.

It is designed to address observable failure modes including:

* incomplete source inspection;
* early stopping;
* evidence loss;
* condition loss;
* evidence/claim binding failure;
* pattern-based completion;
* research-question substitution;
* unsupported comparative judgment;
* state drift during synthesis.

Its effectiveness must itself be evaluated empirically across systems, sessions, and evaluation contexts.

---

# 30. Current Empirical Basis

The protocol architecture emerged from staged evaluation diagnostics in which the following operations were separated:

```text
Evidence Collection
→ Fact Packet
→ Evaluation
→ Claim-State Lock
→ Final Compression
```

The staged procedure substantially reduced previously observed evaluation drift in the tested interactions.

A separate Validator diagnostic also exposed an important boundary:

> A Validator can detect unsupported Fact-to-Evidence bindings, but cannot recover a condition that the Collector failed to place into the Evidence Ledger.

This observation motivates:

* Clause-Level Evidence Binding;
* Hypothesis and Condition Preservation;
* explicit Evidence-Type roles;
* stage-specific permission boundaries.

These observations constitute finite diagnostic evidence only.

They are not presented as universal claims about all AI systems.

---

# 31. Final Principle

The objective is not to make an evaluator incapable of disagreement.

The objective is to make disagreement traceable to evidence.

The protocol therefore does not require:

```text
positive evaluation
```

It requires:

```text
visible evidence state
+
explicit claim binding
+
preserved conditions
+
bounded evaluator authority
+
immutable synthesis state
```

The final rule is:

> Complete the evidence process before completing the evaluation.

And once evaluation is locked:

> Represent the judgment; do not silently recreate it.
