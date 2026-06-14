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




## Note

Full composite survivor output was too long to record manually.
Only summary values will be recorded after extraction.
LIMIT: 1,000,000

Candidates: 999,999

Survivors : 207,796

Prime Axes: 78,498

Composite : 129,298


## Results
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

| LIMIT | Survivors | Prime Axes | Composite |
|---------|---------|---------|---------|
| 10,000 | 2,081 | 1,229 | 852 |
| 1,000,000 | 207,796 | 78,498 | 129,298 |

## Scale Stability Test

### Observation

LIMIT を

10,000
↓
1,000,000

へ拡大しても、生存率はほぼ変化しなかった。

10,000:
2081 / 9999 = 20.81%

1,000,000:
207,796 / 999,999 = 20.78%

### Axis Stability

消去支配軸の順位も維持された。

13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47

### Interpretation

観測範囲を100倍拡大しても、

- 生存率
- 軸順位
- 消去構造

は大きく崩れなかった。

これは残差空間が単純なランダムノイズではなく、

スケールに対して安定した構造を持つ可能性を示している。
## Quantitative Comparison

Survival Rate

10,000:
2081 / 9999 = 20.81%

1,000,000:
207796 / 999999 = 20.78%

Difference:
0.03%

Prime Axis Rate

10,000:
1229 / 2081 = 59.06%

1,000,000:
78498 / 207796 = 37.78%

Composite Rate

10,000:
852 / 2081 = 40.94%

1,000,000:
129298 / 207796 = 62.22%

### Conclusion

Verification001 と Verification002 の比較により、

候補生成空間には自己相似的な安定性が存在する可能性が確認された。

この結果を踏まえ、

Verification003 (LIMIT = 10,000,000)

に進む。

# Verification 003

## Objective

Scale extension test

## Limit

10,000,000

## Status

Pending

## Scale Comparison

| LIMIT | Survival Rate |
|--------|--------|
| 10,000 | 20.81% |
| 1,000,000 | 20.78% |
| 10,000,000 | 20.78% |

Observation:

The survival rate remained stable across three scales.
## Axis Rank Stability

Verification001

13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47

Verification002

13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47

Verification003

13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47

Observation:

Axis ranking remained unchanged across all tested scales.
## Interpretation
Across three scales
10,000
→ 1,000,000
→ 10,000,000
the candidate space exhibited:
- stable survival rate
- stable axis hierarchy
- persistent residual-space structure
The observed behavior suggests that the residual space is not random noise but contains scale-stable elimination patterns.
## Conclusion
Verification001
Verification002
Verification003
all produced consistent structural observations.
The survival rate remained near 20.8%.
The dominant elimination hierarchy
13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47
remained unchanged.
The observed results are consistent with the presence of scale-stable structure in the residual candidate space.

Verification004 (LIMIT = 100,000,000) is proposed as the next validation step.
## Status
Completed
## Status
Completed
# Verification 004

## Objective

Known prime axes variation test.

## Limit

1,000,000

## Results

| KNOWN_PRIMES | Survivors | Prime Axes | Composite | Survival Rate |
|---|---:|---:|---:|---:|
| [2,3,5,7] | 228,574 | 78,498 | 150,076 | 22.86% |
| [2,3,5,7,11] | 207,796 | 78,498 | 129,298 | 20.78% |
| [2,3,5,7,11,13,17] | 180,530 | 78,498 | 102,032 | 18.05% |

## Observation

Increasing the known prime axes reduces the residual candidate space.

The number of Prime Axes remains unchanged.

Composite survivors are reduced.

## Interpretation

Known-axis expansion compresses the search space while preserving prime axes.

This suggests that the method can reduce unnecessary composite candidates without losing prime-axis candidates.

## Energy Cost Note

This may contribute to computational cost reduction in candidate search tasks.

However, actual data-center energy savings require benchmark comparison against existing optimized methods.
# Verification 005

## Objective

Axis decay measurement.

## Limit

1,000,000

## Results

| Axis | Count | Ratio | Relative to 13 |
|---:|---:|---:|---:|
| 13 | 15,983 | 12.3614% | 100.00% |
| 17 | 11,283 | 8.7264% | 70.59% |
| 19 | 9,502 | 7.3489% | 59.45% |
| 23 | 7,434 | 5.7495% | 46.51% |
| 29 | 5,646 | 4.3667% | 35.33% |
| 31 | 5,098 | 3.9428% | 31.90% |
| 37 | 4,136 | 3.1988% | 25.88% |
| 41 | 3,617 | 2.7974% | 22.63% |
| 43 | 3,356 | 2.5956% | 21.00% |
| 47 | 2,982 | 2.3063% | 18.66% |

## Observation

The elimination contribution decreases smoothly as the axis increases.

The strongest elimination axis is 13.

Subsequent axes show a monotonic decay in contribution.

## Interpretation

The residual candidate space is not only stable in axis ranking, but also exhibits a measurable decay structure.

This suggests that prime-axis elimination strength may follow a regular attenuation pattern.
# Verification 006

## Objective

Axis decay fitting and mod 4 observation.

## Limit

1,000,000

## Known Prime Axes

[2, 3, 5, 7, 11]

## Results

Composite: 129,298

Power-law fit:

count ≈ C / axis^alpha

alpha = 1.4783

## Top Axis Data

| Axis | Count | Ratio | mod 4 |
|---:|---:|---:|---:|
| 13 | 15,983 | 12.3614% | 1 |
| 17 | 11,283 | 8.7264% | 1 |
| 19 | 9,502 | 7.3489% | 3 |
| 23 | 7,434 | 5.7495% | 3 |
| 29 | 5,646 | 4.3667% | 1 |
| 31 | 5,098 | 3.9428% | 3 |
| 37 | 4,136 | 3.1988% | 1 |
| 41 | 3,617 | 2.7974% | 1 |
| 43 | 3,356 | 2.5956% | 3 |
| 47 | 2,982 | 2.3063% | 3 |

## Observation

The axis decay is not flat.

The contribution decreases as the axis increases.

The fitted decay exponent is approximately:

alpha = 1.4783

This suggests that the elimination contribution follows a power-law-like attenuation pattern.

## Interpretation

The residual candidate space shows not only:

- survival-rate stability
- axis-rank stability
- axis-decay structure

but also a measurable decay exponent.

The observed exponent is between 1 and 2.

Further verification is required to determine whether this exponent is stable across larger LIMIT values.

## Next Step

Verification007 will compare total contribution between:

- mod 4 = 1 axes
- mod 4 = 3 axes

to examine possible links with square-sum structure, lattice geometry, and circular symmetry.
