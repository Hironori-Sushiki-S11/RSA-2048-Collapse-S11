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
