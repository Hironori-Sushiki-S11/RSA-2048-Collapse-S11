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
# Verification 007

## Objective

mod4 contribution comparison.

## Limit

1,000,000

## Known Prime Axes

[2, 3, 5, 7, 11]

## Results

Composite: 129,298

| mod4 | Count | Ratio |
|---:|---:|---:|
| 1 | 70,057 | 54.1826% |
| 3 | 59,241 | 45.8174% |

Difference:

mod4=1 - mod4=3 = 10,816

## Observation

The contribution is not evenly split between mod4=1 and mod4=3 axes.

mod4=1 axes contribute more than mod4=3 axes.

## Interpretation

This suggests that the residual candidate space may contain a mod4-dependent asymmetry.

Further investigation is required to determine whether this asymmetry is related to square-sum structure, lattice geometry, or circular symmetry.
# Verification 008

## Objective

mod4 average contribution comparison.

## Limit

1,000,000

## Known Prime Axes

[2, 3, 5, 7, 11]

## Results

Composite: 129,298

| mod4 | Axis Count | Total Count | Average Per Axis |
|--------|--------:|--------:|--------:|
| 1 | 79 | 70,057 | 886.80 |
| 3 | 84 | 59,241 | 705.25 |

Difference:

Average contribution difference

886.80 − 705.25 = 181.55

## Observation

The asymmetry remains after normalization by axis count.

mod4=1 axes contribute more composite eliminations per axis than mod4=3 axes.

Even though the mod4=3 group contains more axes (84 vs 79), the average elimination contribution remains larger for mod4=1.

## Interpretation

The residual candidate space exhibits not only total-contribution asymmetry but also per-axis asymmetry.

This suggests that the observed bias is not explained solely by axis count.

Further investigation is required to determine whether this behavior reflects a deeper arithmetic structure or a finite-scale effect.

## Status

Completed

## Next Step

Verification009

Top-layer persistence test:

- Top20 axes
- Top50 axes
- Top100 axes
- Top150 axes

to determine whether the mod4 asymmetry persists across ranking depth.
# Verification 009

## Objective

Top-layer persistence test of mod4 asymmetry.

## Limit

1,000,000

## Known Prime Axes

[2, 3, 5, 7, 11]

## Results

| Range | mod4=1 Total | mod4=3 Total | Difference |
|---------|---------:|---------:|---------:|
| Top20 | 49,681 | 37,331 | 12,350 |
| Top50 | 60,360 | 49,452 | 10,908 |
| Top100 | 67,599 | 56,887 | 10,712 |
| Top150 | 69,970 | 59,141 | 10,829 |

## Observation

The contribution difference remains near 10,000 across all tested ranking depths.

Top20:

12,350

Top50:

10,908

Top100:

10,712

Top150:

10,829

The asymmetry does not disappear as deeper layers are included.

## Interpretation

If the observed imbalance were caused only by a small number of dominant axes, the difference would be expected to diminish as more axes were added.

Instead, the difference remains approximately stable.

This suggests that the mod4 asymmetry is distributed across multiple ranking layers rather than being concentrated in only a few dominant axes.

## Conclusion

The mod4=1 contribution advantage persists across Top20–Top150 ranking depths.

The observed asymmetry therefore appears to be structurally distributed rather than localized.

Further testing at larger limits is required to determine whether the effect remains scale-stable.

## Status

Completed

## Next Step

Verification010

Prime preservation and composite reduction test.
# Verification 010

## Objective

Prime preservation and composite reduction test.

## Limit

1,000,000

## Results

| Known Axes Count | Last Axis | Survivors | Prime Axes | Composite | Survival Rate | Prime Preservation Rate | Composite Rate |
|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| 4 | 7 | 228,574 | 78,498 | 150,076 | 22.8574% | 100.0% | 65.6575% |
| 5 | 11 | 207,796 | 78,498 | 129,298 | 20.7796% | 100.0% | 62.2235% |
| 6 | 13 | 191,813 | 78,498 | 113,315 | 19.1813% | 100.0% | 59.0758% |
| 7 | 17 | 180,530 | 78,498 | 102,032 | 18.0530% | 100.0% | 56.5180% |
| 8 | 19 | 171,028 | 78,498 | 92,530 | 17.1028% | 100.0% | 54.1023% |
| 9 | 23 | 163,594 | 78,498 | 85,096 | 16.3594% | 100.0% | 52.0166% |
| 10 | 29 | 157,948 | 78,498 | 79,450 | 15.7948% | 100.0% | 50.3014% |

## Observation

As additional known prime axes are introduced:

- Survivors decrease.
- Composite survivors decrease.
- Prime Axes remain unchanged.
- Prime Preservation Rate remains 100%.

Prime Axes:

78,498

for every tested configuration.

Composite survivors:

150,076

↓

129,298

↓

113,315

↓

102,032

↓

92,530

↓

85,096

↓

79,450

## Interpretation

Known-axis expansion compresses the candidate space while preserving all observed prime axes within the tested range.

The reduction occurs primarily in composite survivors.

This suggests that candidate-space compression can be achieved without observed loss of prime-axis candidates under the tested conditions.

## Quantitative Effect

Composite reduction:

150,076

↓

79,450

Reduction:

70,626

Reduction Ratio:

47.06%

Prime Preservation:

100%

within LIMIT = 1,000,000.

## Conclusion

The tested candidate-space compression method reduces composite survivors while maintaining complete preservation of observed prime axes.

Within the tested range, increased known-axis coverage improves search-space efficiency without reducing the detected prime-axis population.

## Status

Completed

## Next Step

Verification011

Composite reduction efficiency curve.

Measure:

- Composite reduction per added axis
- Marginal gain of each added prime axis
- Compression efficiency saturation

to determine whether candidate-space compression follows a predictable law.
# Verification 011

## Objective

Composite reduction efficiency analysis.

## Source

Verification010 results.

## Limit

1,000,000

## Results

| Added Axis | Composite Before | Composite After | Reduction |
|---:|---:|---:|---:|
| 11 | 150,076 | 129,298 | 20,778 |
| 13 | 129,298 | 113,315 | 15,983 |
| 17 | 113,315 | 102,032 | 11,283 |
| 19 | 102,032 | 92,530 | 9,502 |
| 23 | 92,530 | 85,096 | 7,434 |
| 29 | 85,096 | 79,450 | 5,646 |

## Observation

Each added known prime axis reduces the number of composite survivors.

The marginal reduction decreases as the added axis increases.

The reduction sequence is:

20,778

↓

15,983

↓

11,283

↓

9,502

↓

7,434

↓

5,646

## Interpretation

Composite reduction efficiency follows the same structure as prime-axis elimination contribution.

This means that the observed axis contribution is not merely descriptive.

It directly corresponds to candidate-space compression efficiency.

## Key Point

Axis contribution

=

Composite reduction efficiency

within the tested range.

## Conclusion

Verification011 connects the axis-elimination structure with practical candidate-space compression.

The method preserves all observed prime axes while progressively reducing composite candidates.

This supports the interpretation that known-axis expansion can function as a structured candidate-space compression method.

## Status

Completed

## Next Step

Verification012

Compression efficiency decay fitting.

Measure whether the marginal reduction sequence follows the same attenuation pattern observed in Verification006.
# Verification012 (LIMIT = 100,000,000 実証実験)

## Results

LIMIT: 100,000,000

KNOWN_AXES:

[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

SEGMENT_SIZE: 500,000

Candidates: 99,999,999

Survivors: 15,794,728

Prime Axes: 5,761,455

Composite: 10,033,273

Survival Rate: 15.794728%

Prime Axis Rate: 36.477076%

Composite Rate: 63.522924%

Elapsed seconds: 450.01

## Top Elimination Axes

| Axis | Count | Ratio |
|---:|---:|---:|
| 31 | 509,508 | 5.078183% |
| 37 | 413,103 | 4.117330% |
| 41 | 362,709 | 3.615062% |
| 43 | 337,382 | 3.362632% |
| 47 | 301,484 | 3.004842% |
| 53 | 261,684 | 2.608162% |
| 59 | 230,683 | 2.299180% |
| 61 | 219,393 | 2.186654% |
| 67 | 196,552 | 1.959002% |
| 71 | 182,782 | 1.821758% |
| 73 | 175,351 | 1.747695% |
| 79 | 159,910 | 1.593797% |
| 83 | 150,351 | 1.498524% |
| 89 | 138,581 | 1.381214% |
| 97 | 125,778 | 1.253609% |
| 101 | 119,552 | 1.191555% |
| 103 | 116,075 | 1.156901% |
| 107 | 110,630 | 1.102631% |
| 109 | 107,564 | 1.072073% |
| 113 | 102,739 | 1.023983% |

## Observation

The LIMIT = 100,000,000 experiment completed successfully using segmented processing.

The known-axis set was extended to:

[2,3,5,7,11,13,17,19,23,29]

The remaining candidate space was compressed to:

15.794728%

Prime Axes remained at:

5,761,455

Composite candidates were:

10,033,273

The next dominant elimination axis became 31, as expected after known axes up to 29 were removed.

## Interpretation

This confirms that known-axis expansion continues to compress the candidate space at LIMIT = 100,000,000.

The dominant residual elimination structure begins from the next unremoved prime axis.

This supports the interpretation that candidate-space compression is governed by sequential prime-axis elimination.

## Status

Completed

# Verification013

## IKERUSIKI Phase-Difference Prime Extractor (Prototype Ver.1)

### Objective

After Verification001–012 confirmed the stability of the residual space,
the next step was to test whether a phase-based function could directly
extract prime coordinates from the residual space.

This verification is therefore the first prototype implementation of
the IKERUSIKI phase extractor.

---

## Experimental Parameters

LIMIT = 1,000,000

KNOWN_AXES

2,3,5,7,11,13,17,19,23,29

Constants

K_B = 11

S = 1.2

PHI = 1.618033988749895

PSI_SCALE = 3.141640786499874

---

## Experimental Result

Residual survivors

157948

Total primes in residual

78498

Extractor output

Extracted candidates

36867

Extracted primes

18418

Extracted composites

18449

Missed primes

60080

---

## Performance

Precision

49.958 %

Recall

23.463 %

Compression

23.341 %

---

## Phase Score

Average phase score (Prime)

0.256088

Average phase score (Composite)

0.255897

Difference

0.000191

---

## Interpretation

The prototype successfully compressed the search space to approximately
23.3% of the residual space.

However, Version 1 showed almost no discrimination between primes and
composites.

The phase score difference was extremely small, indicating that the
current phase function does not yet provide sufficient separating power.

This does **not** invalidate the residual-space observations obtained in
Verification001–012.

Instead, it falsifies the first implementation of the phase extractor
while preserving the residual-space dataset for future reinterpretation.

---

## Conclusion

Verification013 demonstrates:

- Residual-space compression remains valid.
- The first IKERUSIKI extractor is insufficient for prime prediction.
- New structural observables are required.
- Future work should investigate boundary windows, carry transitions,
  numeral-system structures, and phase transitions rather than only
  static residual statistics.

Status

Prototype completed.

Result:

Phase Extractor Ver.1 → NOT sufficient.

Residual-space observations → retained for further structural analysis.

# Verification 014

## Objective

Boundary Window Analysis.

This verification reinterprets the previous residual-space statistics through boundary windows.

The focus is not only on how many candidates survive, but on where structural behavior changes.

## Concept

In Iroha-base interpretation:

- 0 functions like punctuation.
- Carrying functions like framing.
- Digit-boundaries function like phase transitions.
- A base system is not only a counting system, but also a boundary-generating system.

Therefore, the residual space should be observed near boundary windows.

## Target

The target is to observe whether prime behavior changes near:

- digit boundaries
- carry boundaries
- base-transition windows
- residual-space phase shifts

## Interpretation Shift

Previous verifications mainly measured:

- survival rate
- axis contribution
- composite reduction
- prime preservation

Verification014 reads these same structures as:

- boundary behavior
- phase transition behavior
- punctuation-like zero behavior
- framing behavior caused by carry operations

## Status

Design phase.
