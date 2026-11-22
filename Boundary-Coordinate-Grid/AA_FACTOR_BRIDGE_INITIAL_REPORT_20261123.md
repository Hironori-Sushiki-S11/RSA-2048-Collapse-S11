# AA Factor Bridge — Initial Boundary Experiment (2026-11-23)

## Purpose
Test whether unique integer Addresses, starting from a public composite integer N without supplying its factors to the Address algorithm, suffice to recover two unknown factors. This is an exploratory boundary test, not a claim of AA factorization.

## Protocol
- Input: N only to Address construction and GCD operations.
- AA identity observation: residues (x-1) mod b on axes [2,3,5,7] for the three integers N-1,N,N+1. This is the directed component equivalent to the distance/direction Address model.
- Separate extraction probe: g=gcd(N,lcm(2,...,512)). A nontrivial factor requires 1<g<N.
- Expected factors are stored solely as test fixtures to verify the selected composite examples; they are not used by the Address or GCD computation.
- This probe is not the AA residual-difference Select mechanism and is not an efficient general-purpose factoring method.

## Executed results (Python 3, 2026-11-23)

| N | Distinct Addresses for N-1,N,N+1 | gcd(N,LCM(2..512)) | Nontrivial factor extracted |
|---:|:---:|---:|:---:|
| 77 | yes | 77 | no |
| 143 | yes | 143 | no |
| 323 | yes | 323 | no |
| 1022117 | yes | 1 | no |
| 100160063 | yes | 1 | no |

The run completed and all assertions passed.

## Interpretation
- AA-style residue Addresses distinguished the three known integers in each small test.
- This alone did not identify the factors of N.
- The separate GCD probe also yielded no proper factor for these cases. A GCD of N means all factors were included; a GCD of 1 means no factor was exposed.
- No Blind Spot -> Pick Up -> Select -> Address Update process for unknown factor candidates has yet been implemented or tested here.
- This experiment does not evaluate the previously reported large-integer corpus results, nor RSA-2048 security.

## Next test
Define a factor-candidate representation derived from N alone, a collision relation relevant to divisibility, and a candidate observable whose selection reduces *factor ambiguity*, not merely ambiguity between already-known integers. Log candidate generation cost and compare against a same-environment baseline. Do not seed the unknown factors or replace AA with sequential trial division.

## Reproducer
See `AA_FACTOR_BRIDGE_EXPERIMENT.py` in the same directory.
