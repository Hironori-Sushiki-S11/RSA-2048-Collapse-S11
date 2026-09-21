# Round 66 — Exact Packed Lucas–Lehmer Bundles

Factor prefilter is disabled. Each packed bundle carries an exact LL state modulo the product of active Mersenne moduli.
Packed and separate Prime/Composite labels must match exactly.

## C1_100s — p=101..137

- targets: **8**
- separate: **0.000227s**, 912 recurrence updates

|bundle|updates|update reduction|wall|wall speedup|
|---:|---:|---:|---:|---:|
|2|468|1.949x|0.000268s|0.846x|
|3|365|2.499x|0.000221s|1.028x|
|4|242|3.769x|0.000219s|1.038x|
|8|135|6.756x|0.000269s|0.842x|

## C2_300s — p=307..337

- targets: **6**
- separate: **0.000916s**, 1904 recurrence updates

|bundle|updates|update reduction|wall|wall speedup|
|---:|---:|---:|---:|---:|
|2|959|1.985x|0.001171s|0.782x|
|3|646|2.947x|0.001417s|0.646x|
|4|650|2.929x|0.001589s|0.576x|
|6|335|5.684x|0.002262s|0.405x|

## C3_700s — p=701..727

- targets: **4**
- separate: **0.004373s**, 2848 recurrence updates

|bundle|updates|update reduction|wall|wall speedup|
|---:|---:|---:|---:|---:|
|2|1432|1.989x|0.006124s|0.714x|
|3|1442|1.975x|0.007088s|0.617x|
|4|725|3.928x|0.010864s|0.402x|

## Result
All packed executions matched separate Lucas–Lehmer exactly.
Packing reduces recurrence-count, but larger bundles increase product-modulus arithmetic cost. Therefore the proof-state layer has a real tradeoff rather than a monotonic 'pack more is better' rule.

## AA implication
The next Select target is bundle size itself: Current Finite should choose the bundle size minimizing measured total proof cost.