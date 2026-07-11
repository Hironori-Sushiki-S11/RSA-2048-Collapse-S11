# IKERUSIKI Theory

## A Boundary Coordinate Framework for Structural Reconstruction of Integers

**Author**

Hironori Ikeru

---

# Abstract

IKERUSIKI Theory proposes a structural framework for representing integers through Boundary Coordinates rather than exhaustive numerical enumeration.

The mathematical framework was established through Verification001–030 and subsequently evaluated through four computational applications.

Application001 demonstrated structural reconstruction on RSA2048.

Application002 extended the framework to large integers up to 4096 bits.

Application003 introduced computational optimization while preserving the mathematical framework.

Application004 benchmarked the optimized implementation against the baseline implementation.

These results indicate that the proposed framework can reconstruct structural candidates while maintaining a fixed mathematical formulation.

---

# Keywords

- Boundary Coordinate
- Candidate Reconstruction
- Structural Modulus
- Prime Coordinate
- Computational Number Theory
- RSA2048

---

# Notation

| Symbol | Definition |
|---------|------------|
| $B$ | Finite radix set, $B=\{2,3,\ldots,26\}$ |
| $b$ | Radix |
| $n$ | Integer under consideration |
| $r_b(n)$ | Residue $(n-1)\bmod b$ |
| $D_b(n)$ | Boundary Distance |
| $BC_B(n)$ | Finite Boundary Coordinate |
| $BC_\infty(n)$ | Infinite Boundary Coordinate |
| $Cand_B(n)$ | Candidate Reconstruction Set |
| $\Phi_B(n)$ | Core Mathematical Equation |
| $P$ | Set of prime numbers |
| $LIMIT$ | Computational verification range |

---

# 1. Introduction

Traditional computational number theory primarily represents integers by their numerical values. IKERUSIKI Theory instead represents integers through structural information derived from Boundary Coordinates.

The mathematical framework was established through Verification001–030. These verification stages introduced Boundary Distance, Boundary Coordinates, Candidate Reconstruction, and the Core Mathematical Equation.

Following completion of the theoretical framework, four computational applications were conducted. Application001 demonstrated structural reconstruction for RSA2048. Application002 extended the framework to integers up to 4096 bits. Application003 evaluated computational optimization without modifying the mathematical framework. Application004 compared the baseline and optimized implementations through benchmark analysis.

The purpose of this paper is to present the completed mathematical framework, summarize its computational verification, and provide a reproducible structural representation of integers based on Boundary Coordinates.

---

# 2. Mathematical Framework

## 2.1 Structural Observation

IKERUSIKI Theory represents integers by structural information derived from modular boundary relationships rather than by numerical value alone.

For each radix \(b\), an integer is represented by its Boundary Distance.

---

## Definition 1 (Boundary Distance)
···
For an integer \(n\) and radix \(b\),

$$
r_b(n)=((n-1)\bmod b)
$$

The Boundary Distance is defined as

$$
D_b(n)=\min\left(r_b(n),b-1-r_b(n)\right).
$$

---

## Definition 2 (Finite Boundary Coordinate)
···
Let

$$
B=\{2,3,\ldots,26\}.
$$

The finite Boundary Coordinate is

$$
BC_B(n)=
\{
D_b(n)
\mid
b\in B
\}.
$$

---

## Definition 3 (Infinite Boundary Coordinate)
···
The Infinite Boundary Coordinate extends the radix family to every integer satisfying

$$
BC_\infty(n)=\{D_b(n)\mid b\ge2\}.
$$

---

## Definition 4 (Candidate Reconstruction)
···
For a finite radix family \(B\), define the candidate reconstruction set by

$$
Cand_B(n)=\{x\in\mathbb{N}\mid\forall b\in B,\ (x-1)\bmod b\in\{D_b(n),\,b-1-D_b(n)\}\}.
$$

---

## Definition 5 (Core Mathematical Equation)
···
The structural reconstruction is obtained by

$$
\Phi_B(n)=Cand_B(n)\cap[1,LIMIT]\cap\mathbb{P}.
$$

where $\mathbb{P}$ denotes the set of prime numbers.

---

# 3. Core Mathematical Equation

The Core Mathematical Equation provides the mathematical foundation of IKERUSIKI Theory.

Rather than identifying an integer directly by its numerical value, the framework reconstructs a finite candidate set from Boundary Coordinates.

For a finite radix family \(B\),

$$
\Phi_B(n)=Cand_B(n)\cap[1,LIMIT]\cap\mathbb{P}.
$$

where \(\mathbb{P}\) denotes the set of prime numbers.

The reconstruction process consists of three consecutive stages.

1. Boundary Coordinate generation.

2. Candidate reconstruction from modular boundary constraints.

3. Structural verification within the computational range.

Unlike exhaustive search, the proposed framework progressively reduces the candidate space through independent modular constraints.

The mathematical framework itself remains unchanged throughout Verification001–030 and Application001–004.

The computational applications therefore evaluate the completed mathematical framework rather than modifying it.

---

# 4. Verification001–030

## 4.1 Overview

The mathematical framework of IKERUSIKI Theory was established through a sequence of thirty computational verification stages.

Rather than serving as independent experiments, these verification stages progressively constructed and validated the proposed structural representation of integers.

The verification process followed five consecutive phases.

1. Boundary Observation
2. Coordinate Construction
3. Candidate Reconstruction
4. Uniqueness Verification
5. Application Preparation

Each phase extended the previous stage while preserving the same mathematical framework.

---

## 4.2 Phase I — Boundary Observation

Verification001–014 investigated modular boundary behavior for integers under multiple radix systems.

These experiments demonstrated that the Boundary Distance remained structurally stable across different bases and could be used as the fundamental observable quantity.

The outcome of Phase I established Boundary Distance as the basic structural component of IKERUSIKI Theory.

---

## 4.3 Phase II — Coordinate Construction

Verification015–024 introduced Boundary Coordinates as finite structural representations obtained from Boundary Distances.

Instead of representing integers by numerical magnitude, the framework represented each integer by a finite collection of modular boundary coordinates.

This phase also introduced trajectory representations and demonstrated that structural information remained consistent across multiple radix systems.

---

## 4.4 Phase III — Candidate Reconstruction

Verification025–028 established the Candidate Reconstruction framework.

Boundary Coordinates were shown to reconstruct finite candidate sets through independent modular constraints.

Rather than searching the complete integer space, the candidate space was progressively reduced by intersecting residue constraints derived from multiple radices.

This stage introduced the computational reconstruction procedure used throughout the remaining applications.

---

## 4.5 Phase IV — Uniqueness Verification

Verification029–030 evaluated structural uniqueness and practical reconstruction.

Verification029 introduced benchmark methodology for evaluating computational performance.

Verification030 demonstrated structural reconstruction for RSA-oriented composite integers using the completed mathematical framework.

The reconstruction process verified that Boundary Coordinates preserved sufficient structural information for candidate recovery without altering the mathematical formulation.

---

## 4.6 Summary

Verification001–030 collectively established the complete mathematical framework of IKERUSIKI Theory.

The resulting framework consists of:

- Boundary Distance
- Boundary Coordinate
- Candidate Reconstruction
- Core Mathematical Equation

These components form the theoretical basis for the computational applications presented in the following chapters.

---

5. Applications

5.1 Application 1: RSA2048 Structural Demonstration

5.2 Application 2: Large Integer Demonstration

5.3 Application 3: Computational Optimization

5.4 Application 4: Benchmark Analysis

## 5.1 Objective

Application001 evaluates the completed mathematical framework on RSA2048-oriented composite integers.

The objective is not to factor RSA2048 through a new cryptographic algorithm, but to demonstrate that Boundary Coordinates preserve sufficient structural information for candidate reconstruction.

---

## 5.2 Experimental Configuration

The experiment applies the mathematical framework established through Verification001–030 without modification.

The computational procedure consists of

1. Boundary Coordinate generation.

2. Candidate Reconstruction.

3. Structural consistency verification.

No mathematical definitions were altered during the application stage.

---

## 5.3 Structural Reconstruction

Boundary Coordinates generated from RSA-oriented integers were transformed into finite candidate reconstruction sets.

The reconstruction process confirmed that structural constraints derived from multiple radix systems significantly reduced the candidate space while preserving reconstruction consistency.

The experiment therefore demonstrated that the proposed mathematical framework remains applicable to practical large composite integers.

---

## 5.4 Result

Application001 confirmed that the completed IKERUSIKI mathematical framework successfully reconstructs structural candidates for RSA-oriented integers.

The experiment serves as the first computational validation beyond the theoretical verification stages.

Rather than extending the theory, Application001 demonstrates the applicability of the completed framework.

---

## 5.2 Application 2: Large Integer Demonstration

### Objective

Application 2 evaluates the scalability of the completed IKERUSIKI mathematical framework on large integers.

Unlike Application 1, which focuses on RSA-oriented structural reconstruction, this experiment evaluates computational behavior as the integer size increases.

---

### Experimental Configuration

The experiment was performed using randomly generated integers with bit lengths of

- 512 bits
- 1024 bits
- 2048 bits
- 4096 bits

For each integer, the following quantities were measured.

- Candidate Count
- Reduction Ratio
- Reconstruction Consistency
- Peak Memory Usage
- Execution Time

The mathematical framework remained identical to the framework established through Verification001–030.

---

### Experimental Results

The framework successfully reconstructed structural candidates for every tested integer size.

No modification of the mathematical formulation was required as the integer size increased.

Execution time remained sufficiently small while memory consumption stayed nearly constant.

These observations indicate that the proposed structural framework scales efficiently to large integers.

---

### Summary

Application 2 demonstrates that IKERUSIKI Theory is not limited to small computational examples.

The completed mathematical framework remains applicable to practical large integer computations up to at least 4096 bits.

---

## 5.3 Application 3: Computational Optimization

### Objective

Application 3 evaluates computational optimization while preserving the completed mathematical framework.

Unlike previous applications, this stage does not introduce new mathematical definitions. Instead, it evaluates implementation-level improvements.

---

### Optimization Strategy

The optimization focused on reducing computational overhead while maintaining identical mathematical behavior.

The following implementation techniques were evaluated.

- Cache optimization
- Efficient residue handling
- Memory reuse
- Reduction of redundant computations

No modification was made to the mathematical formulation.

---

### Experimental Results

The optimized implementation produced identical reconstruction results to the baseline implementation.

Execution time was reduced while preserving reconstruction consistency.

Memory consumption remained nearly constant throughout all tested integer sizes.

These observations indicate that computational optimization improves implementation efficiency without affecting the theoretical framework.

---

### Summary

Application 3 demonstrates that implementation-level optimization can improve computational performance while leaving the mathematical structure completely unchanged.

---

### Summary

Application 3 demonstrates that implementation-level optimization can improve computational performance while leaving the mathematical structure completely unchanged.

---

## 5.4 Application 4: Benchmark Analysis

### Objective

Application 4 compares the computational performance of the baseline implementation and the optimized implementation.

The objective is to evaluate execution efficiency while preserving the completed mathematical framework.

---

### Benchmark Configuration

The benchmark was performed using identical computational settings for both implementations.

The following quantities were compared.

- Candidate Count
- Reduction Ratio
- Reconstruction Consistency
- Peak Memory Usage
- Execution Time

No mathematical definitions were modified during the benchmark.

---

### Experimental Results

Both implementations produced identical reconstruction results.

The optimized implementation reduced execution time while maintaining equivalent memory consumption and identical structural reconstruction.

These observations confirm that implementation-level optimization improves computational efficiency without altering the completed mathematical framework.

---

### Summary

Application 4 completes the computational evaluation of IKERUSIKI Theory.

Together, Applications 1–4 demonstrate the applicability, scalability, optimization, and reproducibility of the completed mathematical framework.
