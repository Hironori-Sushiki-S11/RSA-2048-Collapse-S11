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

Within the broader Adaptive Address procedure, this instantiated finite set S is the Current Held-Information Corpus: the information set presently retained and available for identification at this stage. The finiteness of S is a property of the current instantiated state; it does not assign a fixed global domain to future EXPAND.

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
f_b(n)=(D_b(n),\mathrm{direction}_b(n)),
$$

where `direction` records which side of the reflected interval contains $r_b(n)$, with the center treated separately.

The pair $(D_b,\mathrm{direction}_b)$ uniquely determines $r_b$. Therefore

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
A_t(x)=(f_{b_1}(x),\dots,f_{b_t}(x)).
$$

Define

$$
L_t=\mathrm{lcm}(b_1,\dots,b_t),
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
\{\{x,y\}\subset S:x\ne y,\ A_t(x)=A_t(y)\}
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
\mathrm{lcm}(L_t,b)
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
\mathrm{lcm}(L_t,b)\mid|x-y|.
$$

Substituting $\mathrm{lcm}(L_t,b)=L_tq_t(b)$ gives

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
\#\{e\in C_t:q_t(b)\mid k_t(e)\},
}
$$

and therefore

$$
\boxed{
R_t(b)
=
\#\{e\in C_t:q_t(b)\nmid k_t(e)\}.
}
$$

For $\Phi_t>0$, define the normalized Structural Relevance Ratio

$$
\boxed{
\mathrm{SR}_t(b)=\frac{R_t(b)}{\Phi_t}.
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
Q_t=\mathrm{lcm}\{q_t(b):b\in\mathcal G_t\}.
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
\mathrm{Select}
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
\{\{x,y\}\subset S:L_t\mid(x-y)\}.
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
