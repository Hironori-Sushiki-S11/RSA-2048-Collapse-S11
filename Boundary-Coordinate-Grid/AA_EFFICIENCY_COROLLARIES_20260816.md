# IKERUSIKI Adaptive Address — Efficiency Corollaries and Validation Note

**Date:** 2026-08-15  
**Scope:** current finite-corpus `(distance, direction)` model  
**Status:** derived from the current Formal Basis; implementation cross-checked separately

## 1. LCM State Sufficiency

Let `B` and `B'` be two finite Address-axis histories and let

\[
L_B=\operatorname{lcm}(B),\qquad L_{B'}=\operatorname{lcm}(B').
\]

From the exact multi-axis Collision law,

\[
A_B(x)=A_B(y)\iff L_B\mid(x-y).
\]

Therefore, if

\[
L_B=L_{B'},
\]

then the two histories induce the same equivalence relation on the current finite corpus `S`. Hence

\[
\boxed{\Pi_B=\Pi_{B'},\qquad C_B=C_{B'},\qquad \Phi_B=\Phi_{B'}.}
\]

Thus the full axis history is not required to determine the current Collision partition; its relevant arithmetic state is compressed to its LCM.

## 2. Candidate Quotient Sufficiency

At current state `L_t`, define

\[
q_t(b)=\frac{b}{\gcd(L_t,b)}.
\]

Since

\[
\operatorname{lcm}(L_t,b)=L_tq_t(b),
\]

if two candidate axes satisfy

\[
q_t(b)=q_t(c),
\]

then

\[
\operatorname{lcm}(L_t,b)=\operatorname{lcm}(L_t,c).
\]

By LCM State Sufficiency, they induce the same refinement of the current partition:

\[
\boxed{q_t(b)=q_t(c)\Rightarrow \Pi_t^{(b)}=\Pi_t^{(c)},\ C_t^{(b)}=C_t^{(c)},\ \Phi_t^{(b)}=\Phi_t^{(c)}.}
\]

Therefore candidate axes may be evaluated by distinct quotient classes rather than by axis identity whenever only their structural refinement effect matters.

## 3. Exact Collision-Reduction Sufficiency

For every current Collision pair `e={x,y}`, define

\[
k_t(e)=\frac{|x-y|}{L_t}.
\]

The residual-difference theorem gives

\[
\boxed{e\text{ survives }b\iff q_t(b)\mid k_t(e).}
\]

Hence

\[
\boxed{C_{t+1}^{(b)}=\{e\in C_t:q_t(b)\mid k_t(e)\}}
\]

and

\[
\boxed{\Phi_t^{(b)}=\#\{e\in C_t:q_t(b)\mid k_t(e)\}.}
\]

The primary Select score, unresolved-pair reduction,

\[
R_t(b)=\Phi_t-\Phi_t^{(b)},
\]

is therefore determined exactly by the current pair-indexed residual map `e -> k_t(e)` and the candidate quotient `q_t(b)`.

## 4. Important Select tie-break boundary

The present implementation uses the lexicographic rule:

1. maximum unresolved-pair reduction;
2. higher Shannon entropy;
3. smaller axis.

The **first criterion** is determined by the residual divisibility counts above.

For the **entropy tie-break**, an unlabeled multiset of residual values alone need not encode the full child-block size distribution. Exact reproduction of the complete Select rule therefore retains either:

- the current Collision partition together with normalized within-block residual labels; or
- equivalent pair/block-labeled residual information.

Candidate Quotient Sufficiency still applies: candidates with the same `q_t` produce the same full refinement, including the same entropy. Thus at most one refinement/entropy evaluation is needed per distinct quotient class.

## 5. Structural operation-count statement

Let

\[
m_t=|C_t|
\]

and let

\[
r_t=|\{q_t(b):b\in\mathcal G_t\}|
\]

be the number of distinct candidate quotient classes.

After the residual map has been constructed, all candidate unresolved-pair counts can be evaluated with at most

\[
\boxed{O(m_t r_t)}
\]

integer divisibility tests in a unit-cost operation-count model.

This is an **operation-count reduction statement**, not a bit-complexity or wall-clock theorem. The arithmetic cost of operating on large integers, the cost of constructing the residual state, and implementation overhead remain separate.

## 6. Implementation validation completed

Two independent finite validation layers were run.

### A. General identity cross-check

`IKERUSIKI_ADAPTIVE_ADDRESS_EFFICIENCY_VALIDATION.py`

- deterministic cases at 64, 512, 4096, 16384, and 65536 bits;
- varying finite corpora with forced current Collisions;
- candidate axes `2..128` in the deterministic benchmark;
- 100 additional randomized finite-corpus / varying-LCM trials.

Result:

- LCM State Sufficiency: PASS;
- Candidate Quotient Sufficiency: PASS;
- exact survival law: PASS;
- direct candidate score = residual-divisibility score: PASS;
- randomized cross-check: **100/100 PASS**.

### B. Archived Verification063 reproduction

`IKERUSIKI_LCM_STATE_SELECTOR_VALIDATION.py`

The LCM/q-state selector was run under the archived Verification063 scaling protocol:

- 32768 and 65536 bits;
- corpus size 100;
- axes `2..512`;
- seeds `20260812..20260816`.

It reproduced the archived selected-axis sequences and Collision trajectories exactly in **10/10 runs**.

This validates that the LCM/q-state formulation is not merely algebraically equivalent on paper; it reproduces the existing finite empirical Select behavior for the tested protocol.

## 7. What is not proved

None of the results above proves:

- universal Address depth 2 or 3;
- permanent sufficiency of axes `2..512`;
- bit-length-independent CPU cost;
- asymptotic practical optimality;
- universal indexing of arbitrary huge integers;
- direct recovery of unknown factors or RSA factorization.

The current result is narrower and exact: **Address history can be collapsed to the current LCM for Collision state, candidate axes can be collapsed to quotient-equivalence classes, and current Collision reduction is exactly a residual divisibility problem.**
