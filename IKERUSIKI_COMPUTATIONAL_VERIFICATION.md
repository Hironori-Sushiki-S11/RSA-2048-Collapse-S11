# IKERUSIKI Computational Verification

## Verification Roadmap

- [ ] 10,000 digits
- [ ] 100,000 digits
- [ ] 1,000,000 digits
- [ ] 10,000,000 digits
- [ ] 100,000,000 digits

## Purpose

This document records computational verification results related to IKERUSIKI Theory.

The objective is to document:

- computational resources
- execution time
- candidate generation behavior
- residual-space observations
- reproducibility

## Current Status

Verification not yet started.

Results will be added as experiments are completed.
# Verification 001

## Objective

Test candidate generation behavior up to 100,000,000 digits.

## Status

In Progress

## Target

100,000,000 digits

## Results

Pending
## Verification 001

Limit: 10,000

Candidates: 9999
Survivors : 2081
Prime Axes: 1229
Composite : 852

### Elimination Summary

13 axis : 159
17 axis : 110
19 axis : 94
23 axis : 76
29 axis : 59
31 axis : 56
37 axis : 46
41 axis : 41
43 axis : 37
47 axis : 33
...
## Verification 002

Limit: 1000000

## Results

Candidates: 未記録
Survivors : 未記録
Prime Axes: 未記録
Composite : 未記録

## Note

Full composite survivor output was too long to record manually.
Only summary values will be recorded after extraction.
LIMIT: 1,000,000

Candidates: 999,999

Survivors : 207,796

Prime Axes: 78,498

Composite : 129,298



13軸 → 15,983 個（12.36%）

17軸 → 11,283 個（8.73%）

19軸 → 9,502 個（7.35%）

23軸 → 7,434 個（5.75%）

29軸 → 5,646 個（4.37%）

31軸 → 5,098 個（3.94%）

37軸 → 4,136 個（3.20%）
## Observation
The elimination hierarchy remains stable.
13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47
The dominant axes are preserved when the observation range increases from 10,000 to 1,000,000.
This suggests that the residual space is not random noise, but has a stable prime-axis elimination structure.
41軸 → 3,617 個（2.80%）

43軸 → 3,356 個（2.60%）

47軸 → 2,982 個（2.31%）
