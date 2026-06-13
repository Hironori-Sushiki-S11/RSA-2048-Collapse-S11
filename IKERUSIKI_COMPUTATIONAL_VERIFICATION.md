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
観察
13 > 17 > 19 > 23 > 29 > 31 > 37 > 41 > 43 > 47
The dominant axes are preserved when the observation range increases from 10,000 to 1,000,000.
This suggests that the residual space is not random noise, but has a stable prime-axis elimination structure.
41軸 → 3,617 個（2.80%）

43軸 → 3,356 個（2.60%）

47軸 → 2,982 個（2.31%）

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

### Conclusion

Verification001 と Verification002 の比較により、

候補生成空間には自己相似的な安定性が存在する可能性が確認された。

この結果を踏まえ、

Verification003 (LIMIT = 10,000,000)

に進む。
