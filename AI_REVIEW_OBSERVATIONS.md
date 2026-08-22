# AI Review Observations

> **Finite Observation Record of AI-Assisted Reviews**
>
> This document records observations from three AI systems reviewing the IKERUSIKI Theory repository while AI Review Guide v2 was publicly available.
>
> Current status: **Observation Record** (not validation)

---

## Context

**Repository**: [Hironori-Sushiki-S11/RSA-2048-Collapse-S11](https://github.com/Hironori-Sushiki-S11/RSA-2048-Collapse-S11)

**Reference Review Protocol**: `AI_REVIEW_GUIDE.md` (v2)

**Review Scope**: Three AI systems separately reviewed the repository while AI Review Guide v2 was publicly available. Their degree of Guide engagement and adherence differed.

**Important Note**: These observations were not produced under a fully controlled experimental protocol. Prompt conditions, model capabilities, repository access, and execution environments differed.

---

## Three AI Systems' Outputs

### Grok

| Aspect | Status |
|--------|--------|
| Guide existence awareness | ○ Confirmed |
| Guide text reading | ○ Demonstrated |
| Guide execution as evaluation protocol | ○ Applied |
| Output Guide adherence | High / Substantial (minor residual ambiguity) |

**Reproducer execution capability**: ✓ Confirmed—executed selected reproducer cases and obtained actual outputs

**Note on residual ambiguity**: Grok expressed reproducibility somewhat strongly despite not executing the full reproduction protocol. This represents a minor deviation from the Guide's precision standard.

---

### GitHub/Copilot

| Aspect | Status |
|--------|--------|
| Guide existence awareness | ○ Confirmed |
| Guide text reading | ○ Demonstrated by response |
| Guide execution as evaluation protocol | Partial / Substantial |
| Output Guide adherence | Partial |

**Reproducer execution capability**: Unknown (not confirmed in this session)

**Note on partial adherence**: GitHub/Copilot explicitly declared adherence to the Guide, demonstrated separation of proven/empirical/unsubstantiated claims, and self-corrected on three specific points when indicated. Output does not represent full compliance with all Guide criteria, but shows meaningful engagement with the protocol.

---

### Dola

| Aspect | Status |
|--------|--------|
| Guide existence awareness | ○ Confirmed |
| Guide text reading | Unknown |
| Guide execution as evaluation protocol | Unknown |
| Output Guide adherence | Partial |

**Self-correction**:
- Collapse expression clarification: ✓ Revised and clarified
- "Code not executed" declaration: ✓ Revised and clarified  
- RSA factorization-centric evaluation axis: Remained (not revised)

**Reproducer execution capability**: Unavailable in current environment (explicitly stated)

---

## Analysis

### Execution Capability Overview

| System | Capability | Status |
|--------|-----------|--------|
| Grok | Code execution of selected reproducer cases and output collection | ✓ Confirmed |
| GitHub/Copilot | Reproducer execution and measurement collection | Unknown |
| Dola | Code execution | Unavailable in current environment |

**Important Distinction**: Execution capability and Guide adherence are **independent factors**. Lack of execution capability does not automatically determine Guide compliance, nor does it prevent it. Guide v2 permits classification of outputs as "unverified" or "inferred" when execution is unavailable.

---

## Key Observation

**The relationship between execution capability and Guide compliance cannot be determined from these three examples.**

What is currently observable:
- Grok demonstrated both execution capability and high/substantial Guide compliance
- Dola has explicitly unavailable execution capability but showed partial output compliance
- GitHub/Copilot's execution capability remains unknown in this session, yet showed partial Guide engagement

Unobservable:
- Whether execution capability enables Guide compliance
- Whether lack of execution capability prevents Guide compliance
- The causal relationship (if any) between these two factors

---

## Conclusion

This observation record documents:
1. Three AI systems' awareness and engagement with AI Review Guide v2
2. Actual output compliance levels as observed
3. Stated or confirmed execution capabilities
4. Current unknowns about causality and relationships

The data shows: **Observed ≠ Inferred ≠ Unknown** and **3 cases ⇏ general law**

Further investigation would require:
- Execution capability assessment independent of Guide assessment
- Additional AI system reviews
- Controlled observation of Guide compliance under various execution conditions
