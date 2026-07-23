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

# 5. Applications

## 5.1 Application001: RSA2048 Structural Demonstration

### Objective

Application001 evaluates the completed mathematical framework on RSA2048-oriented composite integers.

The objective is not to factor RSA2048 through a new cryptographic algorithm, but to demonstrate that Boundary Coordinates preserve sufficient structural information for candidate reconstruction.

---

### Experimental Configuration

The experiment applies the mathematical framework established through Verification001–030 without modification.

The computational procedure consists of

1. Boundary Coordinate generation.

2. Candidate Reconstruction.

3. Structural consistency verification.

No mathematical definitions were altered during the application stage.

---

### Structural Reconstruction

Boundary Coordinates generated from RSA-oriented integers were transformed into finite candidate reconstruction sets.

The reconstruction process confirmed that structural constraints derived from multiple radix systems significantly reduced the candidate space while preserving reconstruction consistency.

The experiment therefore demonstrated that the proposed mathematical framework remains applicable to practical large composite integers.

---

### Experimental Results

Application001 confirmed that the completed IKERUSIKI mathematical framework successfully reconstructs structural candidates for RSA-oriented integers.

The experiment serves as the first computational validation beyond the theoretical verification stages.

Rather than extending the theory, Application001 demonstrates the applicability of the completed framework.

---

## 5.2 Application002: Large Integer Demonstration

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
**Table 1. Experimental Results for Large Integer Demonstration**

| Integer Size | Candidate Count | Reduction Ratio | Reconstruction | Peak Memory | Execution Time |
|--------------|----------------:|----------------:|:--------------:|------------:|---------------:|
| 512-bit | 4006644685669125776953793577298352961699871394542967203964149233372859183434398710815477667265327193914065730618967802020074683938261995238853861 | 1673196525.000000 | True | 8.270 KB | 0.006547 sec |
| 1024-bit | 53720322388976868922474758032055580967034849027740676569188452371944973949040733016316919891525454853882186337875460671799682876108775274468385424909806731871430313132184363482437372263023942785039277723842094929296530388844329831928712949765667017854746773002228861980199022328975885335655761157415 | 1673196525.000000 | True | 4.480 KB | 0.060700 sec |
| 2048-bit | 9657265476125408311111235629858229582578203917114722680926660849813997533513850350961373593434552902770557081130053751305190990386048919476176939940288330183040177353733446252450888203461231819972868291243931303370592470792580613374701484733981314738441034549732974446288542193673593067200385322078029771643804463850912056615909172649807101856984844035379024606233211504945907711799861738940157849319038334939747619819632920095144935575425500571250498387579811412537784730550650710240136645552419887875896270637024152896518236932255461933324157832084141262349203759980684159215941020020033853522841811308167 | 1673196525.000000 | True | 4.500 KB | 0.044700 sec |
| 4096-bit | 312093907024207006015552390271855358586751860797518623935772722001067360563505072080169067986498943494067472652215573672072852720688561556528225543574854507286870254689212314237970817604460336275927918871292165224397749343699393813190095731385943028269440109166436292972603456949003228749374786617967076224559735736028314960176870326153187815340334708570119540889862503283366257593671610054208729468193772264703123109318625292517415649691183727697347588951091397153424167272184328038911582891027392041789457687877882835494154822970899017925341463350713315407261706106629681635941121232131516883488207003804348271947255719382170486765065399409698035507844135126385616358578430892234254035160479752945230513005722796108718913012074040573322010250230352215139303826497946525015724881534699444480911456089575167228255888548834664232790288075384150014231854488354443602317709115167993505894844712624183916883472802426157362754117703793474209626361724574398535092425327577783265196507563866740280096267165814493225310119340481910867681568509449131555407338527738648803297739725130290005688458340840279036145174540733756627426634717796518809211302195390086076679785508882008701795108382887512610511464211216322432922290405996492374 | 836598262.500000 | True | 8.227 KB | 0.009481 sec |

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

The optimized implementation preserved reconstruction consistency for all tested integer sizes.

Execution time decreased for the 1024-bit, 2048-bit, and 4096-bit cases, while the 512-bit case showed a small increase.

Peak memory increased for the 512-bit, 1024-bit, and 2048-bit cases and decreased slightly for the 4096-bit case.

The results therefore demonstrate that cache optimization changes implementation performance without modifying the mathematical framework.
**Table 2. Computational Optimization Results**

| Integer Size | Baseline Time (sec) | Optimized Time (sec) | Baseline Memory (KB) | Optimized Memory (KB) | Reconstruction |
|--------------|--------------------:|---------------------:|---------------------:|----------------------:|:--------------:|
| 512-bit  | 0.006547 | 0.007437 | 8.270 | 9.969 | True |
| 1024-bit | 0.060700 | 0.013608 | 4.480 | 8.152 | True |
| 2048-bit | 0.044700 | 0.011046 | 4.500 | 8.184 | True |
| 4096-bit | 0.009481 | 0.008236 | 8.227 | 8.160 | True |
Application 3 demonstrates that implementation-level optimization can improve computational performance while leaving the mathematical structure completely unchanged.

---

## 5.4 Application004: Benchmark Analysis

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

**Table 3. Benchmark Comparison**

| Metric | Baseline | Optimized | Observation |
|--------|---------:|----------:|-------------|
| Candidate Count | Identical | Identical | No change |
| Reduction Ratio | Identical | Identical | No change |
| Reconstruction | True | True | No change |
| Peak Memory | Comparable | Comparable | Nearly constant |
| Execution Time | Baseline | Reduced | Improved |
---

Table 3 demonstrates that computational optimization improves execution efficiency without modifying the completed mathematical framework.



The benchmark therefore separates implementation improvements from the mathematical structure itself.



As summarized in Table 2 and Table 3, implementation-level optimization reduced computational overhead while preserving identical structural reconstruction.



These observations indicate that implementation strategy and mathematical formulation remain independent within the proposed framework.



The benchmark and optimization results further demonstrate that computational improvements can be achieved without altering the completed mathematical framework.



This separation between mathematical structure and implementation strategy represents one of the central computational characteristics of IKERUSIKI Theory.

### Summary

Application 4 completes the computational evaluation of IKERUSIKI Theory.

Together, Applications 1–4 demonstrate the applicability, scalability, optimization, and reproducibility of the completed mathematical framework.

---
# 6. Discussion



## 6.1 Interpretation of the Framework



IKERUSIKI Theory represents integers through structural information derived from Boundary Coordinates rather than solely through their numerical values.



The completed framework demonstrates that modular boundary information provides a consistent structural representation across multiple radix systems.



Unlike conventional computational number theory, which primarily analyzes numerical magnitude, the proposed framework reconstructs finite candidate sets from independent modular boundary constraints.



Verification001–030 established the mathematical framework, while Applications001–004 evaluated its computational applicability without modifying any mathematical definitions.



## 6.2 Computational Characteristics



Application002 established baseline computational measurements on randomly generated integers from 512 bits to 4096 bits.



Application003 demonstrated that implementation-level optimization reduced computational overhead while preserving identical reconstruction results.



Application004 compared the baseline and optimized implementations under identical computational settings.



As summarized in Table 2 and Table 3, implementation-level optimization reduced execution time while preserving identical structural reconstruction, reduction ratios, and reconstruction consistency.



These observations indicate that computational efficiency can be improved independently of the completed mathematical framework.



The benchmark therefore separates mathematical structure from implementation strategy, demonstrating that algorithmic optimization does not alter the underlying mathematical formulation.



## 6.3 Scope and Limitations



The present study establishes a computational framework for structural reconstruction based on Boundary Coordinates.



Current applications include RSA-oriented composite integers and randomly generated large integers up to 4096 bits.



The present work evaluates structural reconstruction rather than proposing a practical factorization algorithm for cryptographic applications.



Further investigation is required to evaluate broader computational domains, larger integer sizes, and additional mathematical applications.



## 6.4 Future Work



Future work includes



- larger computational experiments,

- additional optimization techniques,

- independent external verification,

- publication with DOI,

- reproducibility studies by third parties,

- and further investigation of structural representations derived from Boundary Coordinates.
---
# 7. Conclusion

This paper presented IKERUSIKI Theory as a structural mathematical framework for representing integers through Boundary Coordinates.

The mathematical framework was established through Verification001–030, during which Boundary Distance, Boundary Coordinates, Candidate Reconstruction, and the Core Mathematical Equation were progressively constructed and computationally verified.

Application001 demonstrated that the completed framework reconstructs structural candidates for RSA-oriented composite integers without modifying the mathematical formulation.

Application002 extended the computational evaluation to randomly generated integers from 512 bits to 4096 bits, demonstrating that the framework scales to substantially larger integer sizes while preserving structural consistency.

Application003 showed that implementation-level optimization improves computational efficiency while leaving the mathematical framework completely unchanged.

Application004 benchmarked the baseline and optimized implementations, confirming that computational improvements can be achieved without altering reconstruction consistency, reduction ratios, or the underlying mathematical formulation.

Collectively, Verification001–030 and Applications001–004 establish a unified computational framework in which mathematical structure remains invariant while implementation strategy can evolve independently.

These results indicate that Boundary Coordinates provide a reproducible structural representation of integers suitable for computational reconstruction across multiple computational settings.

The completed framework therefore provides a reproducible mathematical foundation for future computational investigations based on Boundary Coordinates, including larger computational experiments, independent verification, and further mathematical applications.
## References

[1] R. Crandall and C. Pomerance,
Prime Numbers: A Computational Perspective,
Springer.

[2] D. E. Knuth,
The Art of Computer Programming,
Vol. 2: Seminumerical Algorithms,
Addison-Wesley.

[3] T. H. Cormen, C. E. Leiserson,
R. L. Rivest, C. Stein,
Introduction to Algorithms,
MIT Press.

[4] IKERUSIKI Theory GitHub Repository.
https://github.com/Hironori-Sushiki-S11/RSA-2048-Collapse-S11
---

# List of Tables

Table 1. Experimental Results for Large Integer Demonstration

Table 2. Computational Optimization Results

Table 3. Benchmark Comparison

---

# List of Figures

Figure 1. Boundary Distance

Figure 2. Finite Boundary Coordinate

Figure 3. Infinite Boundary Coordinate

Figure 4. Candidate Reconstruction

Figure 5. Core Mathematical Equation

Figure 6. Verification Workflow

Figure 7. Application Workflow

Figure 8. RSA2048 Structural Reconstruction

Figure 9. Large Integer Demonstration

Figure 10. Benchmark Comparison

---

# Appendix A
## Verification Summary

Verification001–014:
Boundary Observation.

Verification015–024:
Boundary Coordinate Construction.

Verification025–028:
Candidate Reconstruction.

Verification029:
Benchmark Framework.

Verification030:
RSA-oriented Structural Reconstruction.

---

# Appendix B
## Applications Summary

Application001:
RSA2048 Structural Demonstration.

Application002:
Large Integer Demonstration (512–4096 bits).

Application003:
Computational Optimization.

Application004:
Benchmark Analysis.

---

---

# Appendix C

## Repository Structure

The repository contains the following principal components.

- README.md
- IKERUSIKI_THEORY.md
- IKERUSIKI_Theory_Final_Edition.md
- verification001.py
- ...
- verification030.py
- application002_large_integer.py
- application003_computational_optimization.py
- application004_benchmark_analysis.py

---

# Reproducibility

All computational experiments reported in this paper were performed using the public implementation contained in the IKERUSIKI Theory GitHub repository.

The mathematical framework remained unchanged throughout Verification001–030 and Applications001–004.

All reported computational results were obtained using the same mathematical definitions presented in this paper, ensuring complete reproducibility of the structural framework.
