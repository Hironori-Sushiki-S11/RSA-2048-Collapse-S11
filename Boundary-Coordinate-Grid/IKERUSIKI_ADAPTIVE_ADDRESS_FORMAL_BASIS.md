# IKERUSIKI Adaptive Boundary Address - Formal Mathematical Basis

**Revision:** 2026-08-15 (refactored)  
**Scope:** finite-corpus adaptive identification  
**Implementation reference:** `Verification061.py`, `Verification062.py`, `IKERUSIKI_ADAPTIVE_ADDRESS_DEMO.py`

---

## 0. Scope and claim discipline

Let the current corpus be a finite set of distinct positive integers

$$
S=\{x_1,\dots,x_m\}.
$$

This document proves properties of adaptive identification inside the current finite corpus. It separates:

- **theorems** about the current `(distance, direction)` component;
- **implementation choices** such as the finite candidate-axis pool and lexicographic Select rule;
- **empirical outcomes** such as particular Address depths or Collision trajectories.

No result below implies a fixed finite Address for all integers, a universal depth bound, a universal `2..512` guarantee, bit-length-independent arithmetic runtime, RSA factorization, or recovery of arbitrary unknown factors.

---

## 1. Address component and residue equivalence

For every axis $b\ge2$, define

$$
r_b(n)=(n-1)\bmod b,
$$

$$
D_b(n)=\min\{r_b(n),\,b-1-r_b(n)\},
$$

and let

$$
f_b(n)=\bigl(D_b(n),\operatorname{direction}_b(n)\bigr),
$$

where `direction` records which side of the reflected interval contains $r_b(n)$, with the center treated separately.

The pair $(D_b,\operatorname{direction}_b)$ uniquely determines $r_b$. Therefore

$$
\boxed{
f_b(x)=f_b(y)
\iff
x\equiv y\pmod b
\iff
b\mid(x-y).
}
$$

This equivalence is specific to the current `(distance, direction)` implementation. The distance-only coordinate is treated in Appendix A.

---

## 2. Exact multi-axis Collision law

Let the selected Address axes after $t$ updates be

$$
B_t=(b_1,\dots,b_t),
$$

with Address

$$
A_t(x)=\bigl(f_{b_1}(x),\dots,f_{b_t}(x)\bigr).
$$

Define

$$
L_t=\operatorname{lcm}(b_1,\dots,b_t),
$$

with $L_0=1$.

Then

$$
\boxed{
A_t(x)=A_t(y)
\iff
L_t\mid(x-y).
}
$$

### Proof

Address equality holds exactly when every selected axis collides:

$$
A_t(x)=A_t(y)
\iff
b_i\mid(x-y)\quad\forall i.
$$

A number is divisible by every $b_i$ exactly when it is divisible by their least common multiple. Hence

$$
A_t(x)=A_t(y)
\iff
L_t\mid(x-y).
$$

QED

This theorem is the arithmetic core of the current Adaptive Address model.

---

## 3. Partition and Collision Potential

The Address induces the equivalence relation

$$
x\sim_t y
\iff
A_t(x)=A_t(y),
$$

with partition $\Pi_t$ of $S$.

Define the unresolved pair set

$$
C_t=
\bigl\{\{x,y\}\subset S:x\ne y,\ A_t(x)=A_t(y)\bigr\}
$$

and Collision Potential

$$
\Phi_t=|C_t|.
$$

If the block sizes of $\Pi_t$ are $s_1,\dots,s_k$, then

$$
\boxed{
\Phi_t=\sum_j\binom{s_j}{2}.
}
$$

Because an Address update appends a component without deleting old components,

$$
\boxed{
\Pi_{t+1}\preceq\Pi_t,
\qquad
C_{t+1}\subseteq C_t,
\qquad
\Phi_{t+1}\le\Phi_t.
}
$$

If the new axis separates at least one current Collision pair, then

$$
\boxed{
\Phi_{t+1}<\Phi_t.
}
$$

Resolved distinctions never re-merge.

---

## 4. Residual Difference Theorem

Assume $\Phi_t>0$. For every current Collision pair $e=\{x,y\}\in C_t$, Section 2 gives

$$
L_t\mid(x-y).
$$

Define its normalized residual difference

$$
\boxed{
k_t(e)=\frac{|x-y|}{L_t}\in\mathbb Z_{>0}.
}
$$

For a candidate axis $b$, define its novel constraint factor

$$
\boxed{
q_t(b)=\frac{b}{\gcd(L_t,b)}.
}
$$

Because

$$
\operatorname{lcm}(L_t,b)
=
L_t q_t(b),
$$

a current Collision pair survives after appending $b$ exactly when

$$
\boxed{
q_t(b)\mid k_t(e).
}
$$

### Proof

For $e\in C_t$, write

$$
|x-y|=L_tk_t(e).
$$

After appending $b$, the pair remains colliding iff

$$
\operatorname{lcm}(L_t,b)\mid|x-y|.
$$

Substituting $\operatorname{lcm}(L_t,b)=L_tq_t(b)$ gives

$$
L_tq_t(b)\mid L_tk_t(e)
\iff
q_t(b)\mid k_t(e).
$$

QED

Thus the next adaptive step is determined by the residual integers $k_t(e)$ and the novel constraint factors $q_t(b)$.

---

## 5. Select as exact residual reduction

For a candidate axis $b$, define

$$
R_t(b)=\Phi_t-\Phi_t^{(b)},
$$

where $\Phi_t^{(b)}$ is the Collision Potential after hypothetically appending $b$.

By the Residual Difference Theorem,

$$
\boxed{
\Phi_t^{(b)}
=
\#\bigl\{e\in C_t:q_t(b)\mid k_t(e)\bigr\},
}
$$

and therefore

$$
\boxed{
R_t(b)
=
\#\bigl\{e\in C_t:q_t(b)\nmid k_t(e)\bigr\}.
}
$$

For $\Phi_t>0$, define the normalized Structural Relevance Ratio

$$
\boxed{
\operatorname{SR}_t(b)=\frac{R_t(b)}{\Phi_t}.
}
$$

It is the fraction of current unresolved pairs separated by candidate $b$.

The current implementation selects lexicographically by:

1. maximum $R_t(b)$;
2. higher Shannon entropy;
3. smaller axis.

### Candidate equivalence

If

$$
q_t(b)=q_t(c),
$$

then $b$ and $c$ induce the same refinement of the current partition. Their effect on every current Collision pair is identical.

### Divisibility dominance

If

$$
q_1\mid q_2,
$$

then

$$
\{e:q_2\mid k_t(e)\}
\subseteq
\{e:q_1\mid k_t(e)\},
$$

so

$$
\boxed{
R_t(q_2)\ge R_t(q_1).
}
$$

### Redundant axis

If $b\mid L_t$, then $q_t(b)=1$, so

$$
\boxed{R_t(b)=0.}
$$

An axis already contained in the current LCM adds no new distinction.

---

## 6. Exact Blind Spot and EXPAND condition

Let the current candidate-axis family be $\mathcal G_t$.

For $\Phi_t>0$, define

$$
G_t=\gcd\{k_t(e):e\in C_t\}.
$$

A candidate axis has zero reduction exactly when

$$
\boxed{
R_t(b)=0
\iff
q_t(b)\mid G_t.
}
$$

Define

$$
Q_t=\operatorname{lcm}\{q_t(b):b\in\mathcal G_t\}.
$$

Then the whole current candidate family is stalled exactly when

$$
\boxed{
R_t(b)=0\quad\forall b\in\mathcal G_t
\iff
Q_t\mid G_t.
}
$$

This is the exact Blind Spot condition for the current implementation.

An effective EXPAND step introduces at least one new admissible axis $b$ satisfying

$$
\boxed{
q_t(b)\nmid G_t.
}
$$

Such an axis necessarily gives $R_t(b)>0$ and therefore strictly decreases $\Phi_t$.

---

## 7. Separating prime existence and finite convergence

For the current Collision state, define

$$
\Delta_t=
\prod_{e=\{x,y\}\in C_t}|x-y|.
$$

If $\Phi_t>0$, then $\Delta_t\ne0$ and has only finitely many prime divisors. Hence there exists a prime $p$ such that

$$
p\nmid\Delta_t.
$$

For every $e=\{x,y\}\in C_t$,

$$
p\nmid(x-y),
$$

so residue equivalence gives

$$
f_p(x)\ne f_p(y).
$$

Therefore

$$
\boxed{
C_{t+1}=\varnothing
}
$$

after appending such a prime axis.

This proves **existence**, not efficient discovery.

### Fair-EXPAND corollary

If EXPAND evaluates primes under a fair schedule, for example

$$
2,3,5,7,11,\dots,
$$

then it must eventually evaluate a prime not dividing $\Delta_t$, because only finitely many primes divide $\Delta_t$.

Thus a fair unbounded prime EXPAND policy terminates after finitely many candidate expansions for every finite Collision state.

---

## 8. General effective-update bound

Let

$$
k_t=|\Pi_t|.
$$

Every effective Address update splits at least one block, so

$$
k_{t+1}\ge k_t+1.
$$

Since a partition of $m$ elements has at most $m$ singleton blocks, any sequence of effective refinements reaches complete separation after at most

$$
\boxed{
T\le m-k_0
}
$$

effective updates, provided an effective axis is available whenever Collision remains.

For an empty Address, $k_0=1$, so

$$
\boxed{T\le m-1.}
$$

This is an update-count bound, not an arithmetic runtime bound.

---

## 9. Quantitative information bridge

Let $X$ be uniformly distributed over $S$, and let $K_t(X)$ be the size of the partition block containing $X$.

If the block sizes are $s_1,\dots,s_k$, then

$$
2\Phi_t
=
\sum_j s_j^2-m.
$$

Therefore

$$
\boxed{
\mathbb E[K_t]
=
1+\frac{2\Phi_t}{m}.
}
$$

The conditional entropy is

$$
\boxed{
H(X\mid A_t)
=
\frac1m\sum_j s_j\log_2s_j
=
\mathbb E[\log_2K_t(X)].
}
$$

By Jensen's inequality,

$$
\boxed{
H(X\mid A_t)
\le
\log_2\left(1+\frac{2\Phi_t}{m}\right).
}
$$

At complete identification,

$$
\Phi_T=0,
\qquad
\mathbb E[K_T]=1,
\qquad
H(X\mid A_T)=0.
$$

If

$$
U_t=\bigcup_{e\in C_t}e,
\qquad
N_t=|U_t|,
$$

then partition refinement gives $U_{t+1}\subseteq U_t$ and

$$
\boxed{N_t\le2\Phi_t.}
$$

These are finite-corpus identification quantities. They do not by themselves determine implementation runtime.

---

## 10. Current-finite interpretation

The finite corpus $S$ is the reference state in which Address equality, Collision, reduction, and Select are defined.

A Collision

$$
A_t(x)=A_t(y),\qquad x\ne y,
$$

does not mean that $x$ and $y$ lack difference. It means that the current Address has not yet represented a distinction between them.

For the present `(distance, direction)` model, the residual arithmetic structure is explicit:

$$
\boxed{
\mathcal K_t
=
\{k_t(e):e\in C_t\}.
}
$$

Candidate relevance is state-relative and is measured exactly by how $q_t(b)$ acts on $\mathcal K_t$.

The adaptive cycle can therefore be written compactly as

$$
\boxed{
A_t
\rightarrow
C_t
\rightarrow
\mathcal K_t
\rightarrow
q_t(b)
\rightarrow
\operatorname{Select}
\rightarrow
A_{t+1}.
}
$$

---

## 11. What is proved and what remains empirical

### Proved for the current `(distance, direction)` model

- single-axis residue equivalence;
- exact multi-axis Collision law $L_t\mid(x-y)$;
- partition refinement and Collision monotonicity;
- strict reduction under an effective axis;
- normalized residual-difference law;
- exact candidate reduction through $q_t(b)$;
- candidate equivalence, divisibility dominance, and redundant-axis criterion;
- exact Blind Spot condition;
- separating-prime existence;
- finite termination under fair unbounded prime EXPAND;
- general effective-update bound;
- exact bridge from $\Phi_t$ to expected finite-corpus candidate count and entropy bounds.

### Empirical or implementation-dependent

- any particular Collision trajectory;
- depth 2 or depth 3 in a given experiment;
- any transition point as corpus size changes;
- sufficiency of the fixed candidate pool `2..512`;
- observed runtime or memory behavior;
- claims of practical optimality.

---

## 12. Core result

For the current implementation, Adaptive Address is exactly a finite sequence of divisibility refinements.

At stage $t$:

$$
\boxed{
C_t
=
\bigl\{\{x,y\}\subset S:L_t\mid(x-y)\bigr\}.
}
$$

For each current Collision pair,

$$
\boxed{
k_t(e)=\frac{|x-y|}{L_t}.}
$$

For each candidate axis,

$$
\boxed{
q_t(b)=\frac{b}{\gcd(L_t,b)}.}
$$

The pair survives that candidate exactly when

$$
\boxed{q_t(b)\mid k_t(e).}
$$

Thus the adaptive problem contracts from the original integers to the current residual divisibility structure.

That statement is a theorem about the present finite-corpus model. Efficiency, fixed-horizon sufficiency, and empirical Address-depth behavior remain separate questions.

---

# Appendix A - Distance-only Boundary Coordinate

If direction is discarded and only

$$
D_b(n)=\min\{r_b(n),b-1-r_b(n)\}
$$

is retained, then reflection symmetry changes the Collision law:

$$
\boxed{
D_b(x)=D_b(y)
\iff
b\mid(x-y)
\quad\text{or}\quad
b\mid(x+y-1).
}
$$

For a finite corpus $S$, define

$$
Q(S)
=
\prod_{1\le i<j\le m}
|x_i-x_j|\,(x_i+x_j-1).
$$

Because $Q(S)\ne0$, any prime $p$ satisfying

$$
p\nmid Q(S)
$$

separates every pair under the distance-only coordinate.

This appendix is not the model used by the current Adaptive Address demonstration; it is included only to prevent the two Collision laws from being conflated.
Therefore

$$
f_b(x)=f_b(y)
\iff
r_b(x)=r_b(y).
$$

Because $r_b(n)=(n-1)\bmod b$,

$$
r_b(x)=r_b(y)
\iff
x\equiv y\pmod b
\iff
b\mid(x-y).
$$

QED

### Consequence

For the **current implementation**, a collision under one axis is exactly a modular-residue collision.

This fact is specific to `(distance, direction)`. The distance-only formulation is treated separately in Appendix A.

---

## 3. Current Partition

The current Address induces an equivalence relation

$$
x\sim_t y
\iff
A_t(x)=A_t(y).
$$

Let

$$
\Pi_t
$$

be the corresponding partition of $S$.

Each block $G\in\Pi_t$ consists of values that are still indistinguishable under the current Address.

A block with $|G|>1$ is a **Collision group**.

---

## 4. Collision Set and Collision Potential

Define the unresolved pair set

$$
C_t=
\bigl\{
\{x,y\}\subset S:
x\ne y,\,
A_t(x)=A_t(y)
\bigr\}.
$$

Define the **Collision Potential**

$$
\Phi_t=|C_t|.
$$

Equivalently,

$$
\boxed{
\Phi_t=
\sum_{G\in\Pi_t}
\binom{|G|}{2}.
}
$$

For an empty Address,

$$
\Phi_0=\binom{m}{2}.
$$

For a fully collision-free Address,

$$
\Phi_T=0.
$$

Collision Potential is therefore an exact count of currently unresolved pairwise distinctions.

---

## 5. Theorem 1 - Partition Refinement

### Statement

Appending a new Address component without deleting existing components gives

$$
\boxed{
\Pi_{t+1}\preceq\Pi_t,
}
$$

where $\preceq$ denotes partition refinement.

### Proof

The updated Address is

$$
A_{t+1}(x)=\bigl(A_t(x),f_b(x)\bigr).
$$

If

$$
A_t(x)\ne A_t(y),
$$

then the old Address portion already distinguishes $x$ and $y$. Appending another component cannot make the full tuples equal.

Hence distinct old blocks cannot merge. An old block can only remain unchanged or split into smaller blocks.

Therefore $\Pi_{t+1}$ refines $\Pi_t$.

QED

---

## 6. Corollary - Collision Monotonicity

From Theorem 1,

$$
\boxed{
C_{t+1}\subseteq C_t
}
$$

and therefore

$$
\boxed{
\Phi_{t+1}\le\Phi_t.
}
$$

A distinction already acquired by the Address is never lost by further Address expansion.

---

## 7. Theorem 2 - Strict Decrease Under an Effective Axis

### Statement

If a candidate axis splits at least one current Collision group, then

$$
\boxed{
\Phi_{t+1}<\Phi_t.
}
$$

### Proof

Let one current block $G$ have size $n$. Suppose the new axis splits it into nonempty children of sizes

$$
n_1,\dots,n_r,
\qquad
\sum_{i=1}^{r}n_i=n,
\qquad
r\ge2.
$$

Before the split, this block contributes

$$
\binom n2
$$

unresolved pairs.

After the split, it contributes

$$
\sum_{i=1}^{r}\binom{n_i}{2}.
$$

The reduction is

$$
\binom n2-
\sum_i\binom{n_i}{2}
=
\sum_{i<j}n_in_j.
$$

Because $r\ge2$ and all child blocks are nonempty,

$$
\sum_{i<j}n_in_j>0.
$$

At least one unresolved pair disappears, while Theorem 1 prevents any resolved pair from returning. Hence

$$
\Phi_{t+1}<\Phi_t.
$$

QED

---

## 8. Candidate-Axis Reduction Score and Select

For a candidate axis $b$, define

$$
R_t(b)=
\Phi_t-\Phi_t^{(b)},
$$

where $\Phi_t^{(b)}$ is the Collision Potential after hypothetically appending $b$.

For the current implementation, the residue-equivalence lemma gives the exact form

$$
\boxed{
R_t(b)
=
\#\bigl\{
\{x,y\}\in C_t:
b\nmid(x-y)
\bigr\}.
}
$$

Thus $R_t(b)$ counts how many currently unresolved pairs would be separated by axis $b$.

The current demonstration selects the axis using the lexicographic rule:

1. maximize unresolved-pair reduction $R_t(b)$;
2. break ties by higher Shannon entropy;
3. break remaining ties by smaller axis.

If at least one available axis satisfies

$$
R_t(b)>0,
$$

the selected axis also has positive reduction, and Theorem 2 guarantees strict progress.

---

## 9. Theorem 3 - Exact Blind-Spot Characterization for a Fixed Candidate Family

Let the current finite candidate family be

$$
\mathcal B_t\subset\{2,3,\dots\}
$$

and define

$$
L_t=\operatorname{lcm}(\mathcal B_t).
$$

Assume $\Phi_t>0$.

### Statement

The following are equivalent:

$$
\boxed{
R_t(b)=0
\quad
\text{for every }b\in\mathcal B_t
}
$$

and

$$
\boxed{
L_t\mid(x-y)
\quad
\text{for every }\{x,y\}\in C_t.
}
$$

### Proof

By the residue-equivalence lemma, a current pair $\{x,y\}\in C_t$ remains unresolved under candidate axis $b$ exactly when

$$
b\mid(x-y).
$$

Therefore $R_t(b)=0$ means that every current Collision pair remains colliding under $b$.

If this is true for every $b\in\mathcal B_t$, then every $b$ divides every current pair difference. Hence their least common multiple $L_t$ also divides every current pair difference.

The converse is immediate: if $L_t$ divides every current pair difference, then every $b\in\mathcal B_t$ divides every current pair difference, so no candidate axis has positive reduction.

QED

### Interpretation

For the current implementation, a Blind Spot is not merely an abstract failure state.

It has an exact arithmetic form:

> the current unresolved pair differences lie inside the common divisibility structure of the entire current candidate family.

Therefore **EXPAND** means extending the observation family beyond the divisibility structure that leaves the current Collisions unchanged.

---

## 10. Theorem 4 - Separating Prime Existence

Define

$$
\Delta(S)
=
\prod_{1\le i<j\le m}
|x_i-x_j|.
$$

Because the integers in $S$ are distinct,

$$
\Delta(S)\ne0.
$$

### Statement

There exists a prime $p$ such that

$$
p\nmid\Delta(S).
$$

Every such prime separates every pair in $S$ under the current `(distance, direction)` component:

$$
\boxed{
f_p(x_i)\ne f_p(x_j)
\qquad
\text{for all }i\ne j.
}
$$

### Proof

The nonzero integer $\Delta(S)$ has only finitely many distinct prime divisors.

There are infinitely many primes.

Therefore there exists a prime $p$ that does not divide $\Delta(S)$.

For every $i\ne j$,

$$
p\nmid(x_i-x_j).
$$

By the residue-equivalence lemma,

$$
f_p(x_i)\ne f_p(x_j).
$$

Thus one such prime axis separates the entire finite corpus.

QED

### Important scope

This is an **existence theorem**.

It does not imply that:

- the separating prime lies in the fixed pool `2..512`;
- the smallest separating prime is always small;
- finding an efficient separating prime is free;
- or a one-axis Address is the preferred practical strategy.

It proves only that finite-corpus separability is guaranteed when admissible prime axes may expand without a fixed upper bound.

---

## 11. Corollary - A Separating Prime Exists from Every Finite Collision State

For the current unresolved pair set $C_t$, define

$$
\Delta_t=
\prod_{\{x,y\}\in C_t}|x-y|.
$$

If $\Phi_t>0$, then $\Delta_t\ne0$.

Choose a prime $p$ such that

$$
p\nmid\Delta_t.
$$

Then every currently unresolved pair is separated by $p$.

Because previously separated pairs cannot merge,

$$
\boxed{
C_{t+1}=\varnothing
}
$$

after appending this axis.

Thus, from **every finite current state**, at least one admissible prime axis exists that can resolve all remaining Collisions in one additional Address component.

Again, this is an existence result, not an efficiency claim.

---

## 12. Theorem 5 - Finite Convergence Without a Separability Assumption

Earlier formulations stated finite convergence under an eventual-separability assumption.

For the current `(distance, direction)` implementation, Theorem 4 removes that assumption if EXPAND is allowed to introduce arbitrarily large prime axes.

### Statement

For every finite corpus of distinct positive integers, Adaptive Address can reach a collision-free partition after finitely many effective updates.

### Proof

If $\Phi_t=0$, the process is already complete.

If $\Phi_t>0$, Section 11 guarantees the existence of a prime axis that separates every current Collision pair.

Therefore an effective update always exists after sufficient admissible-axis expansion.

By Theorem 2, every effective update strictly decreases the nonnegative integer $\Phi_t$.

Hence the process cannot perform infinitely many effective updates without reaching

$$
\boxed{
\Phi_T=0.
}
$$

QED

### Stronger existence observation

Because Theorem 4 gives a prime that separates the entire original finite corpus, finite convergence can even be achieved in one axis **in principle**.

Adaptive selection remains meaningful because practical objectives may include:

- small axes,
- bounded candidate families,
- low arithmetic cost,
- low Address storage,
- incremental reuse,
- and responsiveness to the current Collision structure.

The remaining research question is therefore not mere existence of finite separation, but **efficient adaptive separation**.

---

## 13. General Effective-Update Bound from Partition Refinement

Let

$$
k_t=|\Pi_t|
$$

be the number of current partition blocks.

Every effective update splits at least one block, so

$$
k_{t+1}\ge k_t+1.
$$

A partition of $m$ objects has at most $m$ singleton blocks.

Therefore, beginning from $k_0$ blocks, any sequence of effective refinements reaches the discrete partition after at most

$$
\boxed{
T\le m-k_0
}
$$

effective updates, provided an effective axis is made available whenever Collision remains.

For an empty Address, $k_0=1$, giving

$$
\boxed{
T\le m-1.
}
$$

This combinatorial update-count bound depends on corpus size and partition structure, not directly on integer bit length.

Arithmetic runtime can still depend strongly on bit length.

---

## 14. Adaptive Structural Contraction Principle

The preceding results support the following finite-corpus principle.

> **Adaptive Structural Contraction Principle.**  
> If new Address components preserve previously acquired distinctions and effective components are selected from the currently unresolved structure, then unresolved relations decrease monotonically. After each effective update, the next identification problem is the residual Collision structure rather than the original unresolved state. When the admissible axis family can expand to arbitrary primes, finite separation is guaranteed.

Symbolically,

$$
\boxed{
S
\rightarrow
\Pi_t
\rightarrow
C_t
\rightarrow
\Phi_t
\rightarrow
\Phi_{t+1}.
}
$$

For every effective Select,

$$
\Phi_{t+1}<\Phi_t.
$$

The central shift is therefore:

$$
\boxed{
\text{ambient magnitude}
\longrightarrow
\text{current unresolved structural information}.
}
$$

This does **not** mean that bit length is irrelevant to arithmetic cost.

It means that the logical object requiring further distinction at stage $t$ is the current unresolved partition, not the entire unbounded integer domain.

---

## 15. Current Finite Observability Principle

A finite corpus is not merely a computational size limit. It supplies the current observational frame in which Address equality, Collision, refinement, and reduction scores are defined.

For the current Address $A_t$,

$$
x\sim_t y
\iff
A_t(x)=A_t(y).
$$

If

$$
A_t(x)=A_t(y)
$$

but an admissible unused component satisfies

$$
f_b(x)\ne f_b(y),
$$

then the current Collision does **not** imply absence of structural difference.

It means only that the current Address has not yet represented that difference.

Thus a remaining Collision may contain **residual structural information relative to a richer admissible observation family**.

The adaptive cycle can therefore be written as

$$
\boxed{
\text{Current finite structure}
\rightarrow
\text{observable Collision}
\rightarrow
\text{residual structural information}
\rightarrow
\text{Select}
\rightarrow
\text{next finite structure}.
}
$$

This principle does not claim that infinite sets lack mathematical structure.

It states only that **unboundedness itself is not the operational observation state used by this adaptive mechanism**. The mechanism proceeds through explicit finite current states.

---

## 16. Structural Relevance of Select

Let $\mathcal B_t$ be the currently available candidate-axis family.

A larger candidate family provides more possible observations, but candidate axes need not have equal value for the current unresolved structure.

The reduction score

$$
R_t(b)=\Phi_t-\Phi_t^{(b)}
$$

measures the discrimination supplied by candidate $b$ relative to the current Collision state.

An axis may be mathematically valid yet contribute no new distinction:

$$
R_t(b)=0.
$$

Another axis may have high current structural relevance because it separates many unresolved pairs:

$$
R_t(b)\gg0.
$$

Thus Select performs the transformation

$$
\boxed{
\text{available observations}
\rightarrow
\text{Collision-conditioned evaluation}
\rightarrow
\text{currently relevant structural information}.
}
$$

In the present implementation, Select has two simultaneous roles:

1. **Contraction** - reduce the unresolved Collision structure.
2. **Information selection** - choose the currently available observation with the highest implemented discrimination score.

Address depth and candidate-family size should therefore not be treated as direct measures of useful information. What matters operationally is how much distinction an added component contributes to the current unresolved partition.

---

## 17. Active Unresolved Set

Define the active unresolved set

$$
U_t=
\bigcup_{\{x,y\}\in C_t}\{x,y\}
$$

and its size

$$
N_t=|U_t|.
$$

These are the corpus elements that still belong to non-singleton blocks.

Because partitions only refine,

$$
\boxed{
U_{t+1}\subseteq U_t
}
$$

and therefore

$$
\boxed{
N_{t+1}\le N_t.
}
$$

For every non-singleton block of size $s\ge2$,

$$
\binom{s}{2}\ge\frac{s}{2}.
$$

Summing over all non-singleton blocks gives

$$
\boxed{
N_t\le2\Phi_t.
}
$$

Thus Collision Potential bounds the number of values that can still be active in unresolved groups.

For example, if

$$
\Phi_t=4,
$$

then

$$
N_t\le8.
$$

This is a statement about the **structural active set**. It does not automatically imply that an implementation performs only $N_t$ arithmetic operations; implementation-level runtime depends on how candidate evaluation is coded.

---

## 18. Theorem 6 - Exact Bridge from Collision Potential to Expected Candidate Count

Let $X$ be uniformly distributed over the finite corpus $S$.

Let

$$
K_t(X)
$$

be the size of the current partition block containing $X$. In finite-corpus identification, $K_t(X)$ is the number of corpus candidates that remain indistinguishable from $X$ under the current Address.

Let the block sizes of $\Pi_t$ be

$$
s_1,\dots,s_k,
\qquad
\sum_{j=1}^{k}s_j=m.
$$

### Statement

$$
\boxed{
\mathbb E[K_t]
=
1+\frac{2\Phi_t}{m}.
}
$$

### Proof

A uniformly selected corpus element belongs to block $j$ with probability $s_j/m$. Therefore

$$
\mathbb E[K_t]
=
\sum_j\frac{s_j}{m}s_j
=
\frac{1}{m}\sum_j s_j^2.
$$

Also,

$$
2\Phi_t
=
2\sum_j\binom{s_j}{2}
=
\sum_j s_j(s_j-1)
=
\sum_j s_j^2-m.
$$

Hence

$$
\sum_j s_j^2=m+2\Phi_t,
$$

and therefore

$$
\mathbb E[K_t]
=
\frac{m+2\Phi_t}{m}
=
1+\frac{2\Phi_t}{m}.
$$

QED

### Interpretation

Collision Potential is not merely a qualitative ambiguity measure.

It gives an **exact finite-corpus average candidate count**.

For $m=100$ and $\Phi_t=4$,

$$
\mathbb E[K_t]
=
1+\frac{8}{100}
=
1.08.
$$

For $m=100$ and $\Phi_t=6$,

$$
\mathbb E[K_t]
=
1+\frac{12}{100}
=
1.12.
$$

These values refer only to identification within the known current finite corpus.

---

## 19. Theorem 7 - Information-Theoretic Bridge

Again let $X$ be uniformly distributed over $S$.

Because $A_t$ is deterministic and all elements of a block are equally likely,

$$
\boxed{
H(X\mid A_t)
=
\frac{1}{m}
\sum_j
s_j\log_2 s_j.
}
$$

Since $K_t(X)=s_j$ when $X$ lies in block $j$,

$$
\boxed{
H(X\mid A_t)
=
\mathbb E[\log_2 K_t(X)].
}
$$

By Jensen's inequality,

$$
\mathbb E[\log_2 K_t]
\le
\log_2\mathbb E[K_t].
$$

Using Theorem 6,

$$
\boxed{
H(X\mid A_t)
\le
\log_2\left(
1+\frac{2\Phi_t}{m}
\right).
}
$$

Therefore the three quantities

$$
\boxed{
\text{Collision Potential}
\leftrightarrow
\text{expected finite-corpus candidate count}
\leftrightarrow
\text{conditional entropy}
}
$$

are quantitatively linked.

At complete identification,

$$
\Phi_T=0,
\qquad
\mathbb E[K_T]=1,
\qquad
H(X\mid A_T)=0.
$$

---

## 20. Entropy Monotonicity

Appending an Address component gives

$$
A_{t+1}=(A_t,f_b).
$$

Conditioning on additional information cannot increase conditional entropy:

$$
\boxed{
H(X\mid A_{t+1})
\le
H(X\mid A_t).
}
$$

If the new component produces a genuine refinement with positive information gain, the inequality is strict.

This is the information-theoretic counterpart of partition refinement and Collision Potential monotonicity.

---

## 21. Empirical Trajectories Are Examples, Not Universal Constants

The adaptive demonstration may produce trajectories such as

$$
4950\rightarrow4\rightarrow0
$$

or

$$
4950\rightarrow6\rightarrow0.
$$

These intermediate values are **corpus-dependent empirical outcomes**.

The formal result is not that a particular value such as 4 or 6 must occur.

The general adaptive form is

$$
\boxed{
\Phi_0
\rightarrow
\Phi_1
\rightarrow
\cdots
\rightarrow
\Phi_T=0,
}
$$

with strict decrease whenever an effective axis is selected.

Therefore the mechanism responds to the Collision structure that actually appears. It does not require a predetermined future Address trajectory.

---

## 22. Relationship to Veri- on the right side, $r_b(n)=b-1-D_b(n)$;
- at the center, the residue is uniquely determined.

Therefore

$$
f_b(x)=f_b(y)
\iff
r_b(x)=r_b(y).
$$

Because $r_b(n)=(n-1)\bmod b$,

$$
r_b(x)=r_b(y)
\iff
x\equiv y\pmod b
\iff
b\mid(x-y).
$$

竏�

### Consequence

For the **current implementation**, a collision under one axis is exactly a modular-residue collision.

This fact is specific to `(distance, direction)`. The distance-only formulation is treated separately in Appendix A.

---

## 3. Current Partition

The current Address induces an equivalence relation

$$
x\sim_t y
\iff
A_t(x)=A_t(y).
$$

Let

$$
\Pi_t
$$

be the corresponding partition of $S$.

Each block $G\in\Pi_t$ consists of values that are still indistinguishable under the current Address.

A block with $|G|>1$ is a **Collision group**.

---

## 4. Collision Set and Collision Potential

Define the unresolved pair set

$$
C_t=
\bigl\{
\{x,y\}\subset S:
x\ne y,\,
A_t(x)=A_t(y)
\bigr\}.
$$

Define the **Collision Potential**

$$
\Phi_t=|C_t|.
$$

Equivalently,

$$
\boxed{
\Phi_t=
\sum_{G\in\Pi_t}
\binom{|G|}{2}.
}
$$

For an empty Address,

$$
\Phi_0=\binom{m}{2}.
$$

For a fully collision-free Address,

$$
\Phi_T=0.
$$

Collision Potential is therefore an exact count of currently unresolved pairwise distinctions.

---

## 5. Theorem 1 窶� Partition Refinement

### Statement

Appending a new Address component without deleting existing components gives

$$
\boxed{
\Pi_{t+1}\preceq\Pi_t,
}
$$

where $\preceq$ denotes partition refinement.

### Proof

The updated Address is

$$
A_{t+1}(x)=\bigl(A_t(x),f_b(x)\bigr).
$$

If

$$
A_t(x)\ne A_t(y),
$$

then the old Address portion already distinguishes $x$ and $y$. Appending another component cannot make the full tuples equal.

Hence distinct old blocks cannot merge. An old block can only remain unchanged or split into smaller blocks.

Therefore $\Pi_{t+1}$ refines $\Pi_t$.

竏�

---

## 6. Corollary 窶� Collision Monotonicity

From Theorem 1,

$$
\boxed{
C_{t+1}\subseteq C_t
}
$$

and therefore

$$
\boxed{
\Phi_{t+1}\le\Phi_t.
}
$$

A distinction already acquired by the Address is never lost by further Address expansion.

---

## 7. Theorem 2 窶� Strict Decrease Under an Effective Axis

### Statement

If a candidate axis splits at least one current Collision group, then

$$
\boxed{
\Phi_{t+1}<\Phi_t.
}
$$

### Proof

Let one current block $G$ have size $n$. Suppose the new axis splits it into nonempty children of sizes

$$
n_1,\dots,n_r,
\qquad
\sum_{i=1}^{r}n_i=n,
\qquad
r\ge2.
$$

Before the split, this block contributes

$$
\binom n2
$$

unresolved pairs.

After the split, it contributes

$$
\sum_{i=1}^{r}\binom{n_i}{2}.
$$

The reduction is

$$
\binom n2-
\sum_i\binom{n_i}{2}
=
\sum_{i<j}n_in_j.
$$

Because $r\ge2$ and all child blocks are nonempty,

$$
\sum_{i<j}n_in_j>0.
$$

At least one unresolved pair disappears, while Theorem 1 prevents any resolved pair from returning. Hence

$$
\Phi_{t+1}<\Phi_t.
$$

竏�

---

## 8. Candidate-Axis Reduction Score and Select

For a candidate axis $b$, define

$$
R_t(b)=
\Phi_t-\Phi_t^{(b)},
$$

where $\Phi_t^{(b)}$ is the Collision Potential after hypothetically appending $b$.

For the current implementation, the residue-equivalence lemma gives the exact form

$$
\boxed{
R_t(b)
=
\#\bigl\{
\{x,y\}\in C_t:
b\nmid(x-y)
\bigr\}.
}
$$

Thus $R_t(b)$ counts how many currently unresolved pairs would be separated by axis $b$.

The current demonstration selects the axis using the lexicographic rule:

1. maximize unresolved-pair reduction $R_t(b)$;
2. break ties by higher Shannon entropy;
3. break remaining ties by smaller axis.

If at least one available axis satisfies

$$
R_t(b)>0,
$$

the selected axis also has positive reduction, and Theorem 2 guarantees strict progress.

---

## 9. Theorem 3 窶� Exact Blind-Spot Characterization for a Fixed Candidate Family

Let the current finite candidate family be

$$
\mathcal B_t\subset\{2,3,\dots\}
$$

and define

$$
L_t=\operatorname{lcm}(\mathcal B_t).
$$

Assume $\Phi_t>0$.

### Statement

The following are equivalent:

$$
\boxed{
R_t(b)=0
\quad
\text{for every }b\in\mathcal B_t
}
$$

and

$$
\boxed{
L_t\mid(x-y)
\quad
\text{for every }\{x,y\}\in C_t.
}
$$

### Proof

By the residue-equivalence lemma, a current pair $\{x,y\}\in C_t$ remains unresolved under candidate axis $b$ exactly when

$$
b\mid(x-y).
$$

Therefore $R_t(b)=0$ means that every current Collision pair remains colliding under $b$.

If this is true for every $b\in\mathcal B_t$, then every $b$ divides every current pair difference. Hence their least common multiple $L_t$ also divides every current pair difference.

The converse is immediate: if $L_t$ divides every current pair difference, then every $b\in\mathcal B_t$ divides every current pair difference, so no candidate axis has positive reduction.

竏�

### Interpretation

For the current implementation, a Blind Spot is not merely an abstract failure state.

It has an exact arithmetic form:

> the current unresolved pair differences lie inside the common divisibility structure of the entire current candidate family.

Therefore **EXPAND** means extending the observation family beyond the divisibility structure that leaves the current Collisions unchanged.

---

## 10. Theorem 4 窶� Separating Prime Existence

Define

$$
\Delta(S)
=
\prod_{1\le i<j\le m}
|x_i-x_j|.
$$

Because the integers in $S$ are distinct,

$$
\Delta(S)\ne0.
$$

### Statement

There exists a prime $p$ such that

$$
p\nmid\Delta(S).
$$

Every such prime separates every pair in $S$ under the current `(distance, direction)` component:

$$
\boxed{
f_p(x_i)\ne f_p(x_j)
\qquad
\text{for all }i\ne j.
}
$$

### Proof

The nonzero integer $\Delta(S)$ has only finitely many distinct prime divisors.

There are infinitely many primes.

Therefore there exists a prime $p$ that does not divide $\Delta(S)$.

For every $i\ne j$,

$$
p\nmid(x_i-x_j).
$$

By the residue-equivalence lemma,

$$
f_p(x_i)\ne f_p(x_j).
$$

Thus one such prime axis separates the entire finite corpus.

竏�

### Important scope

This is an **existence theorem**.

It does not imply that:

- the separating prime lies in the fixed pool `2..512`;
- the smallest separating prime is always small;
- finding an efficient separating prime is free;
- or a one-axis Address is the preferred practical strategy.

It proves only that finite-corpus separability is guaranteed when admissible prime axes may expand without a fixed upper bound.

---

## 11. Corollary 窶� A Separating Prime Exists from Every Finite Collision State

For the current unresolved pair set $C_t$, define

$$
\Delta_t=
\prod_{\{x,y\}\in C_t}|x-y|.
$$

If $\Phi_t>0$, then $\Delta_t\ne0$.

Choose a prime $p$ such that

$$
p\nmid\Delta_t.
$$

Then every currently unresolved pair is separated by $p$.

Because previously separated pairs cannot merge,

$$
\boxed{
C_{t+1}=\varnothing
}
$$

after appending this axis.

Thus, from **every finite current state**, at least one admissible prime axis exists that can resolve all remaining Collisions in one additional Address component.

Again, this is an existence result, not an efficiency claim.

---

## 12. Theorem 5 窶� Finite Convergence Without a Separability Assumption

Earlier formulations stated finite convergence under an eventual-separability assumption.

For the current `(distance, direction)` implementation, Theorem 4 removes that assumption if EXPAND is allowed to introduce arbitrarily large prime axes.

### Statement

For every finite corpus of distinct positive integers, Adaptive Address can reach a collision-free partition after finitely many effective updates.

### Proof

If $\Phi_t=0$, the process is already complete.

If $\Phi_t>0$, Section 11 guarantees the existence of a prime axis that separates every current Collision pair.

Therefore an effective update always exists after sufficient admissible-axis expansion.

By Theorem 2, every effective update strictly decreases the nonnegative integer $\Phi_t$.

Hence the process cannot perform infinitely many effective updates without reaching

$$
\boxed{
\Phi_T=0.
}
$$

竏�

### Stronger existence observation

Because Theorem 4 gives a prime that separates the entire original finite corpus, finite convergence can even be achieved in one axis **in principle**.

Adaptive selection remains meaningful because practical objectives may include:

- small axes,
- bounded candidate families,
- low arithmetic cost,
- low Address storage,
- incremental reuse,
- and responsiveness to the current Collision structure.

The remaining research question is therefore not mere existence of finite separation, but **efficient adaptive separation**.

---

## 13. General Effective-Update Bound from Partition Refinement

Let

$$
k_t=|\Pi_t|
$$

be the number of current partition blocks.

Every effective update splits at least one block, so

$$
k_{t+1}\ge k_t+1.
$$

A partition of $m$ objects has at most $m$ singleton blocks.

Therefore, beginning from $k_0$ blocks, any sequence of effective refinements reaches the discrete partition after at most

$$
\boxed{
T\le m-k_0
}
$$

effective updates, provided an effective axis is made available whenever Collision remains.

For an empty Address, $k_0=1$, giving

$$
\boxed{
T\le m-1.
}
$$

This combinatorial update-count bound depends on corpus size and partition structure, not directly on integer bit length.

Arithmetic runtime can still depend strongly on bit length.

---

## 14. Adaptive Structural Contraction Principle

The preceding results support the following finite-corpus principle.

> **Adaptive Structural Contraction Principle.**  
> If new Address components preserve previously acquired distinctions and effective components are selected from the currently unresolved structure, then unresolved relations decrease monotonically. After each effective update, the next identification problem is the residual Collision structure rather than the original unresolved state. When the admissible axis family can expand to arbitrary primes, finite separation is guaranteed.

Symbolically,

$$
\boxed{
S
\rightarrow
\Pi_t
\rightarrow
C_t
\rightarrow
\Phi_t
\rightarrow
\Phi_{t+1}.
}
$$

For every effective Select,

$$
\Phi_{t+1}<\Phi_t.
$$

The central shift is therefore:

$$
\boxed{
\text{ambient magnitude}
\longrightarrow
\text{current unresolved structural information}.
}
$$

This does **not** mean that bit length is irrelevant to arithmetic cost.

It means that the logical object requiring further distinction at stage $t$ is the current unresolved partition, not the entire unbounded integer domain.

---

## 15. Current Finite Observability Principle

A finite corpus is not merely a computational size limit. It supplies the current observational frame in which Address equality, Collision, refinement, and reduction scores are defined.

For the current Address $A_t$,

$$
x\sim_t y
\iff
A_t(x)=A_t(y).
$$

If

$$
A_t(x)=A_t(y)
$$

but an admissible unused component satisfies

$$
f_b(x)\ne f_b(y),
$$

then the current Collision does **not** imply absence of structural difference.

It means only that the current Address has not yet represented that difference.

Thus a remaining Collision may contain **residual structural information relative to a richer admissible observation family**.

The adaptive cycle can therefore be written as

$$
\boxed{
\text{Current finite structure}
\rightarrow
\text{observable Collision}
\rightarrow
\text{residual structural information}
\rightarrow
\text{Select}
\rightarrow
\text{next finite structure}.
}
$$

This principle does not claim that infinite sets lack mathematical structure.

It states only that **unboundedness itself is not the operational observation state used by this adaptive mechanism**. The mechanism proceeds through explicit finite current states.

---

## 16. Structural Relevance of Select

Let $\mathcal B_t$ be the currently available candidate-axis family.

A larger candidate family provides more possible observations, but candidate axes need not have equal value for the current unresolved structure.

The reduction score

$$
R_t(b)=\Phi_t-\Phi_t^{(b)}
$$

measures the discrimination supplied by candidate $b$ relative to the current Collision state.

An axis may be mathematically valid yet contribute no new distinction:

$$
R_t(b)=0.
$$

Another axis may have high current structural relevance because it separates many unresolved pairs:

$$
R_t(b)\gg0.
$$

Thus Select performs the transformation

$$
\boxed{
\text{available observations}
\rightarrow
\text{Collision-conditioned evaluation}
\rightarrow
\text{currently relevant structural information}.
}
$$

In the present implementation, Select has two simultaneous roles:

1. **Contraction** 窶� reduce the unresolved Collision structure.
2. **Information selection** 窶� choose the currently available observation with the highest implemented discrimination score.

Address depth and candidate-family size should therefore not be treated as direct measures of useful information. What matters operationally is how much distinction an added component contributes to the current unresolved partition.

---

## 17. Active Unresolved Set

Define the active unresolved set

$$
U_t=
\bigcup_{\{x,y\}\in C_t}\{x,y\}
$$

and its size

$$
N_t=|U_t|.
$$

These are the corpus elements that still belong to non-singleton blocks.

Because partitions only refine,

$$
\boxed{
U_{t+1}\subseteq U_t
}
$$

and therefore

$$
\boxed{
N_{t+1}\le N_t.
}
$$

For every non-singleton block of size $s\ge2$,

$$
\binom{s}{2}\ge\frac{s}{2}.
$$

Summing over all non-singleton blocks gives

$$
\boxed{
N_t\le2\Phi_t.
}
$$

Thus Collision Potential bounds the number of values that can still be active in unresolved groups.

For example, if

$$
\Phi_t=4,
$$

then

$$
N_t\le8.
$$

This is a statement about the **structural active set**. It does not automatically imply that an implementation performs only $N_t$ arithmetic operations; implementation-level runtime depends on how candidate evaluation is coded.

---

## 18. Theorem 6 窶� Exact Bridge from Collision Potential to Expected Candidate Count

Let $X$ be uniformly distributed over the finite corpus $S$.

Let

$$
K_t(X)
$$

be the size of the current partition block containing $X$. In finite-corpus identification, $K_t(X)$ is the number of corpus candidates that remain indistinguishable from $X$ under the current Address.

Let the block sizes of $\Pi_t$ be

$$
s_1,\dots,s_k,
\qquad
\sum_{j=1}^{k}s_j=m.
$$

### Statement

$$
\boxed{
\mathbb E[K_t]
=
1+\frac{2\Phi_t}{m}.
}
$$

### Proof

A uniformly selected corpus element belongs to block $j$ with probability $s_j/m$. Therefore

$$
\mathbb E[K_t]
=
\sum_j\frac{s_j}{m}s_j
=
\frac{1}{m}\sum_j s_j^2.
$$

Also,

$$
2\Phi_t
=
2\sum_j\binom{s_j}{2}
=
\sum_j s_j(s_j-1)
=
\sum_j s_j^2-m.
$$

Hence

$$
\sum_j s_j^2=m+2\Phi_t,
$$

and therefore

$$
\mathbb E[K_t]
=
\frac{m+2\Phi_t}{m}
=
1+\frac{2\Phi_t}{m}.
$$

竏�

### Interpretation

Collision Potential is not merely a qualitative ambiguity measure.

It gives an **exact finite-corpus average candidate count**.

For $m=100$ and $\Phi_t=4$,

$$
\mathbb E[K_t]
=
1+\frac{8}{100}
=
1.08.
$$

For $m=100$ and $\Phi_t=6$,

$$
\mathbb E[K_t]
=
1+\frac{12}{100}
=
1.12.
$$

These values refer only to identification within the known current finite corpus.

---

## 19. Theorem 7 窶� Information-Theoretic Bridge

Again let $X$ be uniformly distributed over $S$.

Because $A_t$ is deterministic and all elements of a block are equally likely,

$$
\boxed{
H(X\mid A_t)
=
\frac{1}{m}
\sum_j
s_j\log_2 s_j.
}
$$

Since $K_t(X)=s_j$ when $X$ lies in block $j$,

$$
\boxed{
H(X\mid A_t)
=
\mathbb E[\log_2 K_t(X)].
}
$$

By Jensen's inequality,

$$
\mathbb E[\log_2 K_t]
\le
\log_2\mathbb E[K_t].
$$

Using Theorem 6,

$$
\boxed{
H(X\mid A_t)
\le
\log_2\left(
1+\frac{2\Phi_t}{m}
\right).
}
$$

Therefore the three quantities

$$
\boxed{
\text{Collision Potential}
\leftrightarrow
\text{expected finite-corpus candidate count}
\leftrightarrow
\text{conditional entropy}
}
$$

are quantitatively linked.

At complete identification,

$$
\Phi_T=0,
\qquad
\mathbb E[K_T]=1,
\qquad
H(X\mid A_T)=0.
$$

---

## 20. Entropy Monotonicity

Appending an Address component gives

$$
A_{t+1}=(A_t,f_b).
$$

Conditioning on additional information cannot increase conditional entropy:

$$
\boxed{
H(X\mid A_{t+1})
\le
H(X\mid A_t).
}
$$

If the new component produces a genuine refinement with positive information gain, the inequality is strict.

This is the information-theoretic counterpart of partition refinement and Collision Potential monotonicity.

---

## 21. Empirical Trajectories Are Examples, Not Universal Constants

The adaptive demonstration may produce trajectories such as

$$
4950\rightarrow4\rightarrow0
$$

or

$$
4950\rightarrow6\rightarrow0.
$$

These intermediate values are **corpus-dependent empirical outcomes**.

The formal result is not that a particular value such as 4 or 6 must occur.

The general adaptive form is

$$
\boxed{
\Phi_0
\rightarrow
\Phi_1
\rightarrow
\cdots
\rightarrow
\Phi_T=0,
}
$$

with strict decrease whenever an effective axis is selected.

Therefore the mechanism responds to the Collision structure that actually appears. It does not require a predetermined future Address trajectory.

---

## 22. Relationshi
\[
\Phi_0=\binom{m}{2}.
\]

完全に衝突のないアドレスの場合、

\[
\Phi_T=0。
\]

---

## 4. 定理 1 分割細分化

＃＃＃ 声明

既存のアドレスコンポーネントを削除せずに新しい軸 \(b\) を追加すると、

\[
\boxed{
\Pi_{t+1}\preceq\Pi_t
}
\]

ここで、\(\preceq\)は分割細分化を表す。

＃＃＃ 証拠

更新された住所は

\[
A_{t+1}(x)=\bigl(A_t(x),f_b(x)\bigr).
\]

もし

\[
A_t(x)\neq A_t(y)
\]

すると、\(A_{t+1}(x)\)と\(A_{t+1}(y)\)の最初の成分は既に異なっています。したがって、新しい成分を追加しても、それらは等しくなることはありません。

したがって、以前に分離されたペアはアドレス拡張によってマージされることはありません。各古いブロックはそのまま残るか、より小さなブロックに分割される可能性がありますが、異なる古いブロックは決してマージされません。

---

## 5. 系 衝突単調性

定理1より、

\[
\boxed{
C_{t+1}\subseteq C_t
}
\]

そのため

\[
\boxed{
\Phi_{t+1}\le\Phi_t。
}
\]

したがって、適応型アドレス拡張は、**既に達成された分離に関して情報を保持する**。

---

## 6. 定理 2 有効軸の下での厳密な減少

＃＃＃ 声明

候補軸が少なくとも１つの現在の衝突グループを分割する場合、

\[
\boxed{
\Phi_{t+1}<\Phi_t.
}
\]

＃＃＃ 証拠

サイズ \(n\) の現在のブロック \(G\) を考えます。新しい軸がそれをサイズが空でない子に分割するとします。

\[
n_1,\dots,n_r,
\qquad
\sum_{i=1}^{r}n_i=n,
\qquad r\ge2.
\]

分割前は、ブロックは貢献する

\[
\binom n2
\]

未解決のペア。

分割後は貢献する

\[
\sum_{i=1}^{r}\binom{n_i}{2}.
\]

削減額は

\[
\binom n2-
\sum_i\binom{n_i}{2}
=
\sum_{i<j}n_in_j.
\]

\(r\ge2\)であり、すべての子が空ではないため、

\[
\sum_{i<j}n_in_j>0.
\]

したがって、少なくとも1つの未解決ペアが消滅し、解決済みのペアは戻らない。

\[
\Phi_{t+1}<\Phi_t.
\]

竏

---

## 7. 候補軸削減スコア

候補軸 \(b\) に対して、以下のように定義する。

\[
R_t(b)=
\Phi_t-\Phi_t^{(b)}、
\]

ここで、\(\Phi_t^{(b)}\) は、\(b\) を仮に追加した後の衝突ポテンシャルです。

現在の適応型実装では、辞書式スコアが最大となる軸を選択します。

1. 最大未解決ペア削減 \(R_t(b)\)
2. シャノンエントロピーが高い方が最初のタイブレークとなり、
3. 最終的なタイブレークは、より小さい軸を使用する。

候補者が条件を満たしている場合

\[
R_t(b)>0、
\]

すると、選択された軸も以下を満たす。

\[
R_t(b_{\mathrm{selected}})>0、
\]

したがって、定理2は厳密な進歩を保証する。

---

## 8. 定理 3 EXPAND の論理的役割

＃＃＃ 声明

衝突が残っていると仮定すると、

\[
\Phi_t>0、
\]

しかし、現在利用可能なすべての候補軸は

\[
R_t(b)=0。
\]

すると、現在の候補ファミリー内のどの軸も、現在の衝突パーティションを細分化できなくなります。

＃＃＃ 結果

さらなる身元確認が必要な場合は、候補者の家族自体を変更する必要があります。

これは論理的な役割です

\[
\boxed{\text{展開}}
\]

適応型アドレスフレームワークにおいて。

EXPANDは、将来のアドレスを事前に定義する必要があるという意味ではありません。これは単に、現在の衝突構造において、**現在の観測ファミリーがブラインドスポット**に達したことを意味します。

---

## 9. 定理 4 分離可能性の下での有限収束

＃＃＃ 予測

\(\Phi_t>0\)の場合、以下のいずれかが成り立つ。

1. 現在の候補ファミリーには、\(R_t(b)>0\) の軸が含まれているか、
2. EXPANDは最終的にそのような軸を利用可能にする。

これは、許容観測群に関する**分離可能性の仮定**です。

＃＃＃ 声明

この仮定の下では、アダプティブアドレスは有限回の有効なアドレス更新後に衝突のないパーティションに到達する。

＃＃＃ 証拠

コーパス\(S\)は有限なので、

\[
0\le\Phi_t\le\binom m2。
\]

定理2によれば、すべての有効なアドレス更新は非負整数\(\Phi_t\)を厳密に減少させる。

非負整数の厳密に減少する数列は、無限に続くことはできない。

分離可能性の仮定により正の \(\Phi_t\) での終了が妨げられるため、プロセスは最終的に次の値に到達しなければならない。

\[
\boxed{\Phi_T=0}
\]

ある有限の \(T\) に対して。

---

## 10. パーティションの精緻化による更新回数の上限の強化

\(k_t=|\Pi_t|\) を現在のパーティションブロックの数とする。

有効な軸はすべて少なくとも1つのブロックを分割するので、

\[
k_{t+1}\ge k_t+1.
\]

m 個のオブジェクトのパーティションには、最大で m 個のシングルトンブロックが含まれます。

したがって、\(k_0\)ブロックから始めて、

\[
\boxed{
T\le m-k_0
}
\]

分離可能性の仮定の下では、有効な更新で十分である。

空のアドレスの場合、\(k_0=1\)となり、粗い普遍的境界が得られます。

\[
\boxed{T\le m-1.}
\]

重要なのは、この上限は**現在の有限コーパスのサイズ**に依存し、ビット長や整数の大きさには直接依存しないということです。

---

## 11. 適応構造収縮原理

以上の結果は、以下の有限コーパス原理を示唆している。

**適応型構造収縮原理**  
有限のコーパスにおいて、新しいアドレス要素が以前に取得した区別を保持し、有効な要素が現在未解決の構造から選択される場合、未解決の関係は単調に減少します。有効な更新が行われるたびに、次の問題は元の周辺探索空間ではなく、残りの衝突構造のみとなります。最終的な分離可能性の下では、プロセスは有限回の有効な更新で衝突のない状態に到達します。

象徴的に言えば、

\[
\boxed{
S
\rightarrow
\ピット
\rightarrow
C_t
\rightarrow
\Phi_t
\rightarrow
\Phi_{t+1}
}
\]

と

\[
\Phi_{t+1}<\Phi_t
\]

すべての効果的な選択のために。

したがって、中心的な変化は次のとおりである。

\[
\boxed{
\text{周囲サイズ}
\quad\longrightarrow\quad
\text{現在未解決の構造情報}
}
\]

次の計算は、無限の整数空間全体を事前にアドレス指定する必要性ではなく、残余衝突構造によって規定される。

---

## 12. 電流有限観測可能性原理

有限なコーパスは、単なる計算上の制約ではない。それは、衝突や残存する構造的差異を測定可能にする、現在の観測枠組みを提供する。

境界のない領域は、単に境界がないとみなされるだけでは、アドレス、同値関係、衝突分割、または削減スコアを規定しません。これらの構造は、現在の有限観測規則が指定された後にのみ生じます。

現在のアドレス \(A_t\) の場合、

\[
x\sim_t y
\iff
A_t(x)=A_t(y)
\]

そのアドレスを基準として衝突を観測可能にする。

もし

\[
A_t(x)=A_t(y)
\]

しかし、許容される未使用のコンポーネントは以下を満たす。

\[
f_b(x)\neq f_b(y)、
\]

したがって、現在の衝突は構造的な差異がないことを意味するものではありません。それは単に、現在のアドレスがまだその差異を表現していないことを意味するだけです。

したがって、未解決の衝突は、より豊富な許容観測群に関連する**残存構造情報**を保持する可能性がある。

したがって、適応プロセスは次のように記述できる。

\[
\boxed{
\text{現在の有限構造}
\rightarrow
観測可能な衝突
\rightarrow
\text{残余構造情報}
\rightarrow
\text{選択}
\rightarrow
\text{次の有限構造}
}
\]

この原理は、無限集合が数学的構造を担えないと主張するものではありません。むしろ、**無限性そのものが、このフレームワークで使用される観測構造ではない**ことを述べています。適応アドレス機構は、明示的に指定された有限の観測状態を通して動作します。

したがって、現在の有限状態は、事前に計算された無限アドレスの不完全な近似値として扱われるのではなく、次に必要な改良が観測可能となる操作構造として扱われる。

---

## 13. 選択の構造的関連性

Selectの役割は、単に格納されるアドレスコンポーネントの数を減らすことだけではありません。

\(\mathcal{B}_t\) を現在利用可能な候補軸群とする。候補群が大きいほど、**可能な観測値の数**は増えるが、候補は現在の未解決構造に対して必ずしも同じ値を持つ必要はない。

各候補 \(b\in\mathcal{B}_t\) について、削減スコア

\[
R_t(b)=\Phi_t-\Phi_t^{(b)}
\]

このコンポーネントによって、現在未解決のペア構造のうちどれだけが除去されるかを測定します。

したがって、Select は変換を実行します

\[
\boxed{
候補数
\rightarrow
衝突条件付き評価
\rightarrow
構造的に関連する情報
}
\]

現在の有限コーパスおよび現在のアドレスに関して。

候補となる構成要素は、現在の衝突構造に新たな特徴をもたらさないにもかかわらず、数学的に妥当である可能性がある。

\[
R_t(b)=0。
\]

逆に、大きな \(R_t(b)\) を持つ単一のコンポーネントは、他の多くの候補が存在する場合でも、現在の状態に対して高い構造的関連性を持つ可能性があります。

したがって、適応目標は単に

\[
\text{その他のコンポーネント}
\]

むしろ

\[
\boxed{
\text{差別化価値を示すために選択されたコンポーネント}。
}
\]

現在の実装で使用されている辞書式規則は、未解決ペアの削減を優先し、次にエントロピー、最後に小軸のタイブレークを優先することで、この原則を具体化しています。

これにより、2 つの同時役割を選択できます。

1. **収縮** 未解決の衝突構造を縮小します。
2. **情報の選択** 実装されたスコアの下で、現在利用可能な観測値のうち、最も識別価値の高いものを特定します。

したがって、アドレス深度と候補ファミリーサイズは、有用な構造情報を直接示す指標として解釈すべきではありません。運用上重要なのは、現在未解決のパーティションに寄与する情報です。

---

## 14. 情報理論的形式

確率変数 \(X\) は、現在の有限コーパス \(S\) 上で一様に分布しているとします。

現在のアドレスを観察した後の残りの曖昧さは

\[
H(X\mid A_t)
\]

新しいコンポーネントを追加した後、

\[
A_{t+1}=(A_t,f_b),
\]

また、より多くの情報に基づいて条件付けを行っても、条件付きエントロピーは増加しない。

\[
\boxed{
H(X\mid A_{t+1})
\le
H(X\mid A_t)
}
\]

新しい軸が、正の情報利得を伴う真の改良をもたらす場合、不等式は厳密に成り立つ。

完全な識別では、

\[
\boxed{
H(X\mid A_T)=0。
}
\]

これは、衝突ポテンシャルの単調性に対応する情報理論的な概念を与えるものである。

---

## 15. 経験的軌跡は一例であり、普遍的な定数ではない

適応型デモンストレーションでは、次のような軌跡が生成される可能性があります。

\[
4950\rightarrow4\rightarrow0
\]

または

\[
4950\rightarrow6\rightarrow0。
\]

これらの特定の中間値は、**コーパスに依存する経験的結果**である。

正式な主張は、4や6といった特定の値が必ず発生しなければならないというものではない。

一般的な声明は

\[
\boxed{
\Phi_0
\rightarrow
\Phi_1
\rightarrow
…
\rightarrow
\Phi_T=0
}
\]

有効な軸が選択されるたびに、単調減少する。

したがって、適応ルールは、あらかじめ定められた将来のアドレスを必要とするのではなく、実際に発生する衝突構造に対応する。

---

## 16. 検証061 / 検証062 との関係

### 検証061

運用面で実証される内容：

- 衝突検出、
- 候補軸評価、
- 未解決ペア削減、
- アダプティブセレクト。

定理1と定理2は、有効なSelectが以前の分離を元に戻すことができず、未解決の構造を厳密に縮小しなければならない理由を形式的に説明しています。

### 検証062

現在の候補ファミリーが不十分な場合に「EXPAND」決定を行う手順を、運用面で実証します。

定理3は、衝突が残っているが現在利用可能なすべての候補がゼロ削減である場合に、EXPANDが論理的に必要となる理由を形式化している。

### 適応型アドレス指定のデモンストレーション

有限なプロセス全体を可視化する：

**電流有限  
「衝突」  
候補軸  
「選択」  
住所更新  
再評価  
必要に応じて繰り返し/拡張してください**

定理4は、最終的な分離可能性の下での有限収束の保証を提供する。

---

## 17. スコープ境界

これらの結果は、**現在の有限コーパス内での適応的識別**のための正式な基礎を確立するものである。

それらはそれ自体では主張しない。

- 無限領域内のすべての整数を一意に識別する固定有限アドレス、
- ユニバーサル2軸識別、
- 特定の中間衝突回数、
- RSA因数分解、
- または、コーパスコンテキストなしで有限コーパスアドレスから任意の未知の整数を復元する。

形式的な対象は、有限な現在の候補集合の適応的な洗練である。

---

＃＃ 結論

適応型境界アドレス機構は、単調な有限細分化プロセスとして説明できる。

その基本的な数学的構造は次のとおりです。

\[
\boxed{
電流有限
\rightarrow
衝突
\rightarrow
構造的な違い
\rightarrow
\text{選択}
\rightarrow
\text{改良}
\rightarrow
衝突可能性の低減
}
\]

重要な不変条件は、以前に獲得した区別が保持されるということである。

重要な点は、有効な更新を行うたびに、未解決の構造が厳密に縮小されるということである。

重要な境界ルールは、現在の候補が衝突を減らすことができない場合、既に解決された構造の観測ファミリーを拡張する必要があるということです。

したがって、現在の有限状態は単なるサイズ制限ではない。それは、衝突が定義され、残存構造情報を選択可能となる観測状態なのである。

選択は、単なる量の削減にとどまりません。実装されたスコアに基づいて、現在最も識別価値の高い候補観測値を特定し、可能性のある観測値の集合を、現在の未解決構造に関連する情報に変換します。

したがって、正式なプロセスは次のように要約できます。

\[
\boxed{
電流有限
\rightarrow
衝突
\rightarrow
\text{残余構造情報}
\rightarrow
\text{選択}
\rightarrow
レスポンシブ・リファインメント
}
\]

これは有限集合に関する形式的な結果に過ぎません。それ自体では、素数の出現、無限領域における普遍的同一性、あるいは完全な無限アドレスに関する主張を確立するものではありません。

これは、現在実施されているIKERUSIKI適応型境界アドレスの実証実験における、正式な数学的基礎となるものです。
