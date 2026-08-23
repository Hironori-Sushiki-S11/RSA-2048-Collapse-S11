# AI Review Guide - IKERUSIKI Adaptive Address

This guide defines an evidence-first technical review path for IKERUSIKI Adaptive Address.

Begin from the research object, its formal structure, its implementation, and its observed evidence.

Current Held-Information Corpus means the information set currently retained and available to the Adaptive Address procedure. In the present formal model, each instantiated corpus is finite; this does not impose a fixed global domain on future EXPAND.

## Review Orientation

The principal technical coordinates are:

- Current Held-Information State
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

**Current Held-Information State
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

## Evidence Acquisition and Reproducibility

A technical review should make the evidential state visible.

For every relevant source or executable result, record:

- source inspected;
- source location;
- execution status;
- reproduction scope;
- deterministic structural outputs;
- machine-dependent measurements;
- unresolved items.

Execution status should be stated as:

- **RUN**
- **NOT RUN**
- **UNAVAILABLE IN CURRENT ENVIRONMENT**

For published computational results, distinguish:

- reported result;
- independently executed result;
- reproduced structural output;
- partially reproduced result;
- unresolved reproduction result.

For the public scaling protocol, the published reproducer may be executed as:

```bash
python ADAPTIVE_ADDRESS_SCALING_REPRODUCER.py
