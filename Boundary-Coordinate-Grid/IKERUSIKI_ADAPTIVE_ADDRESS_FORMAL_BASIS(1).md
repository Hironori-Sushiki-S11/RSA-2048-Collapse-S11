# IKERUSIKI Adaptive Boundary Address — Formal Mathematical Basis

## Scope

This document gives a finite-corpus mathematical basis for the adaptive selection process implemented in:

- `Verification061.py`
- `Verification062.py`
- `IKERUSIKI_ADAPTIVE_ADDRESS_DEMO.py`

It formalizes the following process:

**Current finite corpus  
→ Collision detection  
→ Candidate-axis evaluation  
→ Select  
→ Address update  
→ Collision re-evaluation  
→ EXPAND only when the current candidate family is insufficient**

This document does **not** claim universal one-shot identification over an unbounded integer range. The object of analysis is always a **current finite corpus**.

---

## 1. Finite Corpus and Address

Let

\[
S=\{x_1,\dots,x_m\}
\]

be a finite set of distinct integers.

For every admissible axis \(b\), let

\[
f_b:S\to Y_b
\]

be the structural component returned by that axis.

In the current demonstration implementation,

\[
f_b(n)=(D_b(n),\operatorname{direction}_b(n)),
\]

where

\[
r_b(n)=(n-1)\bmod b,
\]

\[
D_b(n)=\min\{r_b(n),\,b-1-r_b(n)\}.
\]

The `direction` component records which side of the reflected boundary produced the distance. Therefore the pair `(distance, direction)` preserves the full residue state for that axis.

For a finite selected axis set

\[
B_t=\{b_1,\dots,b_t\},
\]

define the current Address by

\[
A_t(x)=\bigl(f_{b_1}(x),\dots,f_{b_t}(x)\bigr).
\]

---

## 2. Current Partition

The current Address induces an equivalence relation

\[
x\sim_t y
\iff
A_t(x)=A_t(y).
\]

Let

\[
\Pi_t
\]

be the corresponding partition of \(S\).

Every block of \(\Pi_t\) is a set of values that are still indistinguishable under the current Address.

A block of size greater than one is a **Collision group**.

---

## 3. Collision Set and Collision Potential

Define the unresolved pair set

\[
C_t=
\{\{x,y\}\subset S:x\neq y,\ A_t(x)=A_t(y)\}.
\]

Define the **Collision Potential**

\[
\Phi_t=|C_t|.
\]

Equivalently, if \(\Pi_t\) has blocks \(G\),

\[
\boxed{
\Phi_t=
\sum_{G\in\Pi_t}
\binom{|G|}{2}
}
\]

This is exactly the number of unresolved pairs used by the adaptive demonstration.

For an empty Address and a corpus of size \(m\),

\[
\Phi_0=\binom{m}{2}.
\]

For a fully collision-free Address,

\[
\Phi_T=0.
\]

---

## 4. Theorem 1 — Partition Refinement

### Statement

If a new axis \(b\) is appended without deleting the existing Address components, then

\[
\boxed{
\Pi_{t+1}\preceq\Pi_t
}
\]

where \(\preceq\) denotes partition refinement.

### Proof

The updated Address is

\[
A_{t+1}(x)=\bigl(A_t(x),f_b(x)\bigr).
\]

If

\[
A_t(x)\neq A_t(y),
\]

then the first components of \(A_{t+1}(x)\) and \(A_{t+1}(y)\) already differ. Therefore they cannot become equal after appending a new component.

Hence a previously separated pair can never be merged by Address extension. Each old block may remain intact or split into smaller blocks, but distinct old blocks never merge. ∎

---

## 5. Corollary — Collision Monotonicity

From Theorem 1,

\[
\boxed{
C_{t+1}\subseteq C_t
}
\]

and therefore

\[
\boxed{
\Phi_{t+1}\le\Phi_t.
}
\]

Thus Adaptive Address extension is **information-preserving with respect to already achieved separation**.

---

## 6. Theorem 2 — Strict Decrease Under an Effective Axis

### Statement

If a candidate axis splits at least one current Collision group, then

\[
\boxed{
\Phi_{t+1}<\Phi_t.
}
\]

### Proof

Consider one current block \(G\) of size \(n\). Suppose the new axis splits it into nonempty children of sizes

\[
n_1,\dots,n_r,
\qquad
\sum_{i=1}^{r}n_i=n,
\qquad r\ge2.
\]

Before the split, the block contributes

\[
\binom n2
\]

unresolved pairs.

After the split it contributes

\[
\sum_{i=1}^{r}\binom{n_i}{2}.
\]

The reduction is

\[
\binom n2-
\sum_i\binom{n_i}{2}
=
\sum_{i<j}n_in_j.
\]

Because \(r\ge2\) and all children are nonempty,

\[
\sum_{i<j}n_in_j>0.
\]

Therefore at least one unresolved pair disappears and no resolved pair can return. Hence

\[
\Phi_{t+1}<\Phi_t.
\]

∎

---

## 7. Candidate-Axis Reduction Score

For a candidate axis \(b\), define

\[
R_t(b)=
\Phi_t-\Phi_t^{(b)},
\]

where \(\Phi_t^{(b)}\) is the Collision Potential after hypothetically appending \(b\).

The current adaptive implementation selects the axis with maximum lexicographic score:

1. maximum unresolved-pair reduction \(R_t(b)\),
2. higher Shannon entropy as first tie-break,
3. smaller axis as final tie-break.

If any candidate satisfies

\[
R_t(b)>0,
\]

then the selected axis also satisfies

\[
R_t(b_{\mathrm{selected}})>0,
\]

so Theorem 2 guarantees strict progress.

---

## 8. Theorem 3 — Logical Role of EXPAND

### Statement

Suppose Collision remains,

\[
\Phi_t>0,
\]

but every currently available candidate axis satisfies

\[
R_t(b)=0.
\]

Then no axis in the current candidate family can refine the current Collision partition.

### Consequence

If further identification is required, the candidate family itself must change.

This is the logical role of

\[
\boxed{\text{EXPAND}}
\]

in the Adaptive Address framework.

EXPAND does not mean that a future Address should be predefined in advance. It means only that the **current observation family has reached a Blind Spot** for the present Collision structure.

---

## 9. Theorem 4 — Finite Convergence Under Separability

### Assumption

Whenever \(\Phi_t>0\), either:

1. the current candidate family contains an axis with \(R_t(b)>0\), or
2. EXPAND eventually makes such an axis available.

This is a **separability assumption** on the admissible observation family.

### Statement

Under this assumption, Adaptive Address reaches a collision-free partition after finitely many effective Address updates.

### Proof

The corpus \(S\) is finite, so

\[
0\le\Phi_t\le\binom m2.
\]

By Theorem 2, every effective Address update strictly decreases the nonnegative integer \(\Phi_t\).

A strictly decreasing sequence of nonnegative integers cannot continue indefinitely.

Because the separability assumption prevents termination at a positive \(\Phi_t\), the process must eventually reach

\[
\boxed{\Phi_T=0}
\]

for some finite \(T\). ∎

---

## 10. Stronger Update-Count Bound from Partition Refinement

Let \(k_t=|\Pi_t|\) be the number of current partition blocks.

Every effective axis splits at least one block, so

\[
k_{t+1}\ge k_t+1.
\]

A partition of \(m\) objects has at most \(m\) singleton blocks.

Therefore, starting from \(k_0\) blocks,

\[
\boxed{
T\le m-k_0
}
\]

effective updates are sufficient under the separability assumption.

For an empty Address, \(k_0=1\), giving the coarse universal bound

\[
\boxed{T\le m-1.}
\]

Importantly, this bound depends on the **current finite corpus size**, not directly on the bit length or magnitude of its integers.

---

## 11. Adaptive Structural Contraction Principle

The preceding results imply the following finite-corpus principle.

> **Adaptive Structural Contraction Principle.**  
> In a finite corpus, if new Address components preserve previously acquired distinctions and effective components are selected from the currently unresolved structure, then unresolved relations decrease monotonically. After every effective update, the next problem is not the original ambient search space but only the residual Collision structure. Under eventual separability, the process reaches a collision-free state in finitely many effective updates.

Symbolically,

\[
\boxed{
S
\rightarrow
\Pi_t
\rightarrow
C_t
\rightarrow
\Phi_t
\rightarrow
\Phi_{t+1}
}
\]

with

\[
\Phi_{t+1}<\Phi_t
\]

for every effective Select.

The central shift is therefore:

\[
\boxed{
\text{ambient size}
\quad\longrightarrow\quad
\text{current unresolved structural information}
}
\]

The next computation is governed by the residual Collision structure, not by a requirement to pre-address the entire unbounded integer space.

---

## 12. Information-Theoretic Form

Let a random variable \(X\) be uniformly distributed over the current finite corpus \(S\).

The remaining ambiguity after observing the current Address is

\[
H(X\mid A_t).
\]

After appending a new component,

\[
A_{t+1}=(A_t,f_b),
\]

and conditioning on more information cannot increase conditional entropy:

\[
\boxed{
H(X\mid A_{t+1})
\le
H(X\mid A_t).
}
\]

If the new axis produces a genuine refinement with positive information gain, the inequality is strict.

At complete identification,

\[
\boxed{
H(X\mid A_T)=0.
}
\]

This gives an information-theoretic counterpart to Collision Potential monotonicity.

---

## 13. Empirical Trajectories Are Examples, Not Universal Constants

The adaptive demonstration may produce trajectories such as

\[
4950\rightarrow4\rightarrow0
\]

or

\[
4950\rightarrow6\rightarrow0.
\]

These particular intermediate values are **corpus-dependent empirical outcomes**.

The formal claim is not that a specific value such as 4 or 6 must occur.

The general statement is

\[
\boxed{
\Phi_0
\rightarrow
\Phi_1
\rightarrow
\cdots
\rightarrow
\Phi_T=0
}
\]

with monotonic decrease whenever an effective axis is selected.

Thus the adaptive rule responds to the Collision structure that actually appears, rather than requiring a predetermined future Address.

---

## 14. Relationship to Verification061 / Verification062

### Verification061

Operationally demonstrates:

- Collision detection,
- candidate-axis evaluation,
- unresolved-pair reduction,
- adaptive Select.

Theorems 1 and 2 formalize why an effective Select cannot undo previous separation and must strictly reduce the unresolved structure.

### Verification062

Operationally demonstrates the `EXPAND` decision when the current candidate family is insufficient.

Theorem 3 formalizes why EXPAND is logically required when Collision remains but all currently available candidates have zero reduction.

### Adaptive Address Demonstration

Makes the full finite process visible:

**Current finite  
→ Collision  
→ Candidate axes  
→ Select  
→ Address Update  
→ Re-evaluate  
→ Repeat / EXPAND as required**

Theorem 4 supplies the finite-convergence guarantee under eventual separability.

---

## 15. Scope Boundary

These results establish a formal basis for **adaptive identification within a current finite corpus**.

They do not by themselves claim:

- a fixed finite Address that uniquely identifies every integer in an unbounded domain,
- universal two-axis identification,
- a specific intermediate Collision count,
- RSA factorization,
- or recovery of an arbitrary unknown integer from a finite-corpus Address without the corpus context.

The formal object is the adaptive refinement of a finite current candidate set.

---

## Conclusion

The Adaptive Boundary Address mechanism can be described as a monotone finite refinement process.

Its essential mathematical structure is:

\[
\boxed{
\text{Current finite}
\rightarrow
\text{Collision}
\rightarrow
\text{Structural difference}
\rightarrow
\text{Select}
\rightarrow
\text{Refinement}
\rightarrow
\text{Reduced Collision Potential}
}
\]

The key invariant is that previously acquired distinctions are preserved.

The key dynamic is that every effective update strictly contracts the unresolved structure.

The key boundary rule is that, when no current candidate can reduce Collision, the observation family—not the already resolved structure—must be expanded.

This is the formal mathematical basis of the current IKERUSIKI Adaptive Boundary Address demonstration.
