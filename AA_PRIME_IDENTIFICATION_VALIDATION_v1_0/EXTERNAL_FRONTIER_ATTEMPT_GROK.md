# External Frontier Attempt — Grok (corrected 2026-09-23)

## Status

- **Core Validation:** COMPLETE
- **Frontier Prime Identification:** OPEN
- **Grok computation:** COMPLETED / UNRESOLVED within that attempt
- **Target $p=141,566,927$:** ALREADY KNOWN COMPOSITE, so invalid as an uncharted Prime target

## Correction of the target

The earlier report selected $M_p=2^p-1$ with $p=141,566,927$ merely because its exponent exceeded GIMPS's first-test boundary. A boundary does not certify the status of an individual exponent. [PrimeNet's individual exponent record](https://www.mersenne.org/report_exponent/?exp_lo=141566927) lists **three prime factors discovered on 2007-10-25**:

| Exact divisor $q$ | Independent divisibility check |
| ---: | ---: |
| 183753871247 | `pow(2, 141566927, q) == 1` |
| 1837255578607 | `pow(2, 141566927, q) == 1` |
| 255228181349761 | `pow(2, 141566927, q) == 1` |

Each checked $q$ is strictly between 1 and $M_p$, hence $q\mid M_p$ proves **Composite** exactly. The three modular checks were independently executed here; their results were all 1. The assertion that these divisors are themselves prime comes from PrimeNet, and is not needed for the Composite conclusion.

## What the Grok attempt established

Grok did not produce an LL/PRP result or find a factor in its own execution environment. This records that attempt's outcome, not the actual mathematical status of the target. It cannot be used as evidence that $M_{141566927}$ is an unresolved Prime candidate.

For a genuine unresolved example, [PrimeNet's entry for $p=141,566,917$](https://www.mersenne.org/report_exponent/?exp_lo=141566917) said on 2026-09-23 that it had no known factors and had not been tested for primality. It also showed a PRP assignment 81.38% complete, updated 2026-09-22; this is time-sensitive and does not guarantee that the candidate remains unresolved later. It had already been trial factored below $2^{77}$.

## Relation to Adaptive Address

The correction does not change verified finite-corpus AA identity results or Core Validation. It changes the interpretation of this one frontier attempt. An exact new Prime result still requires a valid candidate and a completed exact proof; collision-free symbolic identification is a separate achievement. Small residue axes alone cannot propagate every exact LL state or certify the terminal zero without additional information.

**Frontier Prime Identification: OPEN.** Do not cite $p=141,566,927$ as a new or unresolved Prime candidate.
