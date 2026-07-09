# IKERUSIKI Theory

> **From Search to Structure**

IKERUSIKI Theory is a coordinate-based mathematical framework for representing, analyzing, and reconstructing integer structures through Boundary Coordinates and structural constraints.

Unlike exhaustive search approaches, the framework investigates structural properties of integers and evaluates how coordinate-derived information reduces candidate search spaces.

---

# Overview

The repository consists of two major stages.

## Theory

The Theory section establishes the mathematical framework.

It includes

- Boundary Coordinate
- Prime Coordinate
- Structural Layers
- Candidate Factor Space
- Prime Reconstruction
- Structural Verification

The mathematical foundation is completed through Verification001–030.

---

## Applications

The Applications section evaluates the completed framework on practical computational problems.

Applications include

- Application001
  - RSA2048 Structural Demonstration

- Application002
  - Large Integer Demonstration

- Application003
  - Computational Optimization

- Application004
  - Benchmark Analysis

Applications do **not** introduce new mathematical assumptions.

They evaluate how the completed framework behaves under increasingly practical computational conditions.

---

# Repository Structure

```
README.md

IKERUSIKI_THEORY.md

IKERUSIKI_COMPUTATIONAL_VERIFICATION.md

IKERUSIKI_PRIME_FORMULA.md

IKERUSIKI_PRIME_EXPERIMENT.md

verification001.py
...
```

---

# Current Status

- Theory Completion ✅
- Verification001–030 Completed ✅
- Core Mathematical Equation Established ✅
- Application001 (RSA2048 Structural Demonstration) Completed ✅
- Application002 (Large Integer Demonstration) Completed ✅
- Application003 (Computational Optimization) Completed ✅
- Application004 (Benchmark Analysis) Completed ✅
# Vision

Future work includes

- Computational optimization (Application003)
- Benchmark analysis (Application004)
- GitHub v1.0 Release
- Paper
- DOI
- External verification

The long-term objective is to establish IKERUSIKI Theory as a reusable mathematical framework for structural analysis of integers.

---

# Research Philosophy

IKERUSIKI Theory investigates integer structures through structural information rather than exhaustive enumeration.

The objective is not to replace existing number theory, but to provide an additional structural viewpoint for mathematical investigation.

---

# License

MIT License

## Application002: Large Integer Demonstration

Completed IKERUSIKI Theory was applied without modification to large odd integers of 512, 1024, 2048, and 4096 bits.

| Integer Size | Structural Modulus | Residue Classes | Reduction Ratio | Reconstruction | Memory Usage | Execution Time |
|--------------|-------------------:|----------------:|----------------:|:--------------|-------------:|---------------:|
| 512-bit  | 26771144400 | 16 | 1673196525.000000 | True | 8.270 KB | 0.006547 sec |
| 1024-bit | 26771144400 | 16 | 1673196525.000000 | True | 8.270 KB | 0.006553 sec |
| 2048-bit | 26771144400 | 16 | 1673196525.000000 | True | 8.266 KB | 0.006298 sec |
| 4096-bit | 26771144400 | 16 | 1673196525.000000 | True | 6.941 KB | 0.003462 sec |

### Result

For all tested large integers, Boundary Coordinate generation, candidate reconstruction, and reconstruction consistency succeeded.

---

## Application003: Computational Optimization

Cache optimization was applied without modifying IKERUSIKI Theory.

| Integer Size | Optimization | Structural Modulus | Residue Classes | Reduction Ratio | Reconstruction | Memory | Execution Time |
|--------------|--------------|-------------------:|----------------:|----------------:|----------------|-------:|---------------:|
| 512-bit | Cache Optimization | 26771144400 | 16 | 1673196525.000000 | True | 9.969 KB | 0.007437 sec |
| 1024-bit | Cache Optimization | 26771144400 | 16 | 1673196525.000000 | True | 8.152 KB | 0.013608 sec |
| 2048-bit | Cache Optimization | 26771144400 | 16 | 1673196525.000000 | True | 8.184 KB | 0.011046 sec |
| 4096-bit | Cache Optimization | 26771144400 | 16 | 1673196525.000000 | True | 8.160 KB | 0.008236 sec |

### Result

Reconstruction consistency remained **True** for all tested integer sizes.

The Core Mathematical Equation was not modified.

The structural modulus remained constant:

## Application004: Benchmark Analysis

Comparison between the baseline implementation (Application002) and the optimized implementation (Application003).

| Metric | Application002 | Application003 |
|--------|----------------|----------------|
| Theory | Fixed | Fixed |
| Optimization | None | Cache Optimization |
| Structural Modulus | 26771144400 | 26771144400 |
| Residue Classes | 16 | 16 |
| Reduction Ratio | 1673196525.000000 | 1673196525.000000 |
| Reconstruction | True | True |

### Benchmark Summary

- Core Mathematical Equation remained unchanged.
- Structural Modulus remained identical.
- Residue Classes remained identical.
- Reduction Ratio remained identical.
- Reconstruction Consistency remained True.
- Computational optimization was introduced without modifying the mathematical framework.
```text
26771144400

---

## Current Release Status

IKERUSIKI Theory v1.0 is in the final validation phase.

Completed:

- Theory Completion ✅
- Core Mathematical Equation ✅
- Verification001–030 ✅
- Application001 ✅
- Application002 ✅
- Application003 ✅
- Application004 ✅

Next:

- GitHub v1.0 Release
- Paper
- DOI
- External Verification
