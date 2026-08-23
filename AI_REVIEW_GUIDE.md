# AI Review Guide - IKERUSIKI Adaptive Address

This guide defines an evidence-first technical review path for IKERUSIKI Adaptive Address.

Begin from the research object, its formal structure, its implementation, and its observed evidence.

## Review Orientation

The principal technical coordinates are:

- Current Finite State
- Collision Structure
- Structural Saved Information
- Residual Difference
- Candidate Quotient
- Pick Up
- Candidate Generation
- Select
- Address Update
- Blind Spot
- EXPAND
- finite convergence conditions
- implementation correspondence
- empirical scaling
- reproducibility

The central procedure is:

**Current Finite
→ Collision
→ Structural Saved Information
→ Blind Spot
→ Pick Up
→ Candidate Axes
→ Select
→ Address Update
→ EXPAND when required**

A review should first determine what each of these objects means in the published formal model and implementation.

## Review Order

1. Read the primary technical sources:

   - `Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_FORMAL_BASIS.md`
   - `Boundary-Coordinate-Grid/IKERUSIKI_ADAPTIVE_ADDRESS_DEMO.py`
   - `Boundary-Coordinate-Grid/AA_EFFICIENCY_COROLLARIES_20260816.md`
   - `ADAPTIVE_ADDRESS_SCALING_REPRODUCIBILITY.md`
   - `ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py`
   - `Boundary-Coordinate-Grid/HOW_TO_APPLY_ADAPTIVE_ADDRESS.md`

2. Preserve the distinction between:

   - mathematically proved structure;
   - implemented structure;
   - computationally verified structure;
   - empirical observations;
   - interpretations and possible applications;
   - open questions.

3. Bind substantive statements to their source, condition, and evidence type.

4. Inspect the formal transition from the current Collision state to the next candidate-axis decision.

5. Determine whether the implementation corresponds to the published formal procedure.

6. Distinguish deterministic structural outputs from machine-dependent measurements.

7. State the boundary of the inspected evidence where that boundary is actually reached.

The governing review principle is:

> Establish the object first.  
> Inspect the evidence second.  
> Evaluate only after the evidence state is explicit.

A review should neither enlarge nor diminish the meaning of a result before evaluating the result itself.

## Comparative Evaluation Procedures

Comparative judgments should be built from matched evidence.

The purpose of comparison is to determine what the observed structure means under clearly stated conditions.

### 1. Performance and Scaling

When evaluating computational behavior, record the state being measured:

- task definition;
- corpus size;
- input distribution;
- bit size or relevant scale;
- candidate-axis family;
- selected Address depth;
- implementation;
- hardware and software environment;
- runtime;
- memory;
- deterministic structural outputs.

Separate:

**structural depth**
from
**arithmetic runtime**
from
**machine-dependent execution time**.

A shallow Address depth is a structural observation.

A measured runtime is an implementation observation.

Neither should silently substitute for the other.

When comparing two methods, first establish that they are solving the same or meaningfully comparable task under compatible conditions.

If such a matched comparison has not been performed, record:

**Comparative Performance: Not Assessed**

---

### 2. Prior-Art and Novelty Comparison

Novelty evaluation begins by identifying the closest relevant prior mechanisms.

Compare the actual structures, including where applicable:

- maintained state;
- representation;
- Collision or unresolved-equivalence definition;
- residual distinguishing information;
- candidate-generation rule;
- candidate quotient or equivalent refinement criterion;
- Select rule;
- Address or partition update;
- Blind Spot condition;
- EXPAND rule;
- stopping condition;
- convergence statement;
- proved scope.

The comparison should identify separately:

- mathematically identical components;
- structurally similar components;
- differently organized components;
- mechanisms for which no close correspondence was established.

If this comparison has not been performed, record:

**Novelty: Not Assessed**

The purpose is to locate the work accurately in relation to prior structures, not to infer identity or difference from terminology alone.

---

### 3. Evidence Maturity

Evaluate evidence maturity by recording what has actually been completed.

Relevant states include:

- formally proved;
- implemented;
- computationally cross-checked;
- empirically reproduced;
- independently reproduced;
- externally compared;
- not yet assessed.

Evidence maturity is a description of the current evidential state.

It is separate from mathematical correctness, novelty, performance, and possible future significance.

---

### 4. Evaluation Dimensions

Keep independent dimensions independent.

Where relevant, report separately:

- formal correctness;
- implementation correspondence;
- reproducibility;
- empirical scaling;
- comparative performance;
- novelty / prior-art relation;
- scope of demonstrated results;
- open technical questions.

A combined conclusion may be written only after these dimensions have been established separately.

The governing principle is:

> Compare like with like.  
> Preserve the state of the evidence.  
> Let the comparison reveal the boundary instead of assuming the boundary in advance.

---

## Access and Reproducibility

If a referenced file, script, or result cannot be accessed:

- report it as inaccessible or unverified;
- do not infer missing results from surrounding documentation;
- do not convert an access limitation into a criticism of the method.

When possible, execute the published reproducer before making computational claims.

For the scaling results, use:

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py
```

or a constrained single case such as:

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py --bits 32768 --seed 20260812
```

Compare deterministic structural outputs with the published reproducibility guide.

## Criticism Protocol

When criticizing a claim, identify:

- the exact claim;
- the file and section where it occurs;
- whether the objection concerns proof, implementation, experiment, interpretation, or application;
- whether the objection is based on direct inspection, execution, comparison, literature review, or inference.

Do not present an inference as if it were an observed result.

If the criticism depends on an external comparison, identify the comparator or source rather than relying on a generic analogy.

## Review Output Discipline

A technically useful review should make it possible to tell which conclusions came from which evidence.

Where applicable, classify important statements as:

- Proved in the repository;
- Computationally cross-checked;
- Empirically reproduced;
- Reported but not independently reproduced;
- Inferred;
- Not assessed.

For novelty, performance, scalability, or scientific-value judgments, state whether an external literature search, benchmark, or independent execution was actually performed.

## Claim Boundary

This guide does not ask reviewers to accept IKERUSIKI Theory or Adaptive Address.

It asks reviewers, human or AI, to evaluate the claims actually made against the definitions, proofs, code, and reproducible evidence actually provided.

A valid review may be positive, negative, or mixed.

The requirement is methodological accuracy:
read first, distinguish claim types, execute when relevant, identify what was measured, identify the basis of comparisons, and criticize the actual claim rather than a substituted one.
