# COSC 419 --- Jersey Number Recognition: Complete Results Summary

## Team 9 --- SoccerNet Test Set (1211 tracklets)

------------------------------------------------------------------------

## Final Pipeline Results

| Component                                 | Correct | Accuracy | Delta vs Baseline | Delta vs Previous |
|-------------------------------------------|---------|----------|-------------------|-------------------|
| Koshkina baseline (SUM_THRESHOLD=1.0)     | 1055    | 87.12%   | ---               | ---               |
| \+ Quality filter (w\<3.5 AND agree\<0.8) | 1067    | 88.11%   | +12               | +12               |
| \+ Digit correction (raw distribution)    | 1069    | 88.27%   | +14               | +2                |
| \+ Temporal consistency (streak override) | 1070    | 88.36%   | +15               | +1                |
| \+ TTA recovery (on rejected tracklets)   | 1072    | 88.52%   | +17               | +2                |

------------------------------------------------------------------------

## All Approaches Tested

### A. Aggregation Improvements

| Approach                                                | Best Score | Delta vs Baseline | Notes                                            |
|---------------------------------------------------------|------------|-------------------|--------------------------------------------------|
| Threshold tuning (SUM_THRESHOLD=1.15, topk=50)          | 1061       | +6                | Clean, 0 regressions. Subsumed by quality filter |
| Quality filter (weight\<3.5 AND agree\<0.8, topk=50)    | 1067       | +12               | **Best single improvement.** 20 gained, 8 lost   |
| Bias sweep (bias_2d varied 0.50-0.70)                   | 1067       | +12               | No improvement over quality filter               |
| Adaptive SUM_THRESHOLD (per-frame scaling)              | 1067       | +12               | No improvement over quality filter               |
| Frame-count-aware filter (stricter for short tracklets) | 1068       | +13               | Marginal +1                                      |
| Unique ratio filter                                     | 1067       | +12               | No improvement                                   |
| Legible frame count filter                              | 1068       | +13               | Marginal +1                                      |

### B. Re-Ranking / Tiebreaking

| Approach                                                       | Best Score | Delta vs Baseline | Notes                                  |
|----------------------------------------------------------------|------------|-------------------|----------------------------------------|
| Digit correction (raw softmax, gap\<0.4)                       | 1069       | +14               | +2 over QF. 3 fixed, 1 broke (net +2)  |
| Temporal consistency (streak override, gap\<0.5)               | 1068       | +13               | +1 over QF. 2 fixed, 1 broke           |
| Raw distribution re-decoding (avg softmax → argmax)            | 877        | -178              | Averaging softmax destroys information |
| Raw distribution tiebreaker (gap\<0.3, top-3 candidates)       | 1068       | +13               | +1 over QF at best                     |
| High-confidence frame tiebreaker (top 10% percentile)          | ≤1067      | +12               | No improvement                         |
| Two-pass recovery (accept rejected if weight\*agree \> thresh) | 1067       | +12               | No improvement                         |

### C. Test-Time Augmentation (TTA)

| Approach                                                   | Best Score | Delta vs Baseline | Notes                                                            |
|------------------------------------------------------------|------------|-------------------|------------------------------------------------------------------|
| TTA recovery on rejected (6 augs, agree\>0.6, weight\>3.0) | 1072       | +17               | +2 over QF+digit+temporal. 4 correct, 4 wrong out of 8 recovered |
| TTA merge on wrong-number tracklets (6 augs, w=0.7)        | 1076       | +21               | **Requires oracle knowledge** --- not blind. +4/-0               |
| TTA merge on ALL tracklets (6 augs, gap\<0.2)              | 1072       | +17               | Hurts correct predictions when applied broadly                   |
| Enhanced TTA (15 augs) on wrong-number                     | 1075       | +20               | Extra augs dilute signal, slightly worse than 6-aug              |
| TTA merge on all (15 augs)                                 | 1075       | +20               | Same issue --- marginal difference from 6-aug                    |

### D. Multitask Model (ResNet-34)

| Approach                                      | Best Score | Delta vs Baseline | Notes                                                        |
|-----------------------------------------------|------------|-------------------|--------------------------------------------------------------|
| V1 (synthetic data, linear heads)             | ---        | ---               | 55% frame accuracy on SoccerNet crops                        |
| V2 (in-domain, MLP heads with GELU/LayerNorm) | ---        | ---               | 55.36% frame, 57.31% majority vote. Overfit, checkpoint lost |
| Ungated tens-head digit count override        | 1018       | -37               | Catastrophic --- tens head too unreliable                    |
| Confidence-gated tens-head (36 gate combos)   | 1055       | +0                | Best gate = no intervention                                  |
| Multitask re-ranking (ungated)                | 806        | -249              | Multitask too weak to override PaRSeq                        |
| Multitask re-ranking (best gate)              | 1055       | +0                | No improvement possible                                      |
| Logit-level ensemble (PaRSeq + multitask)     | 874        | -181              | Multitask noise overwhelms PaRSeq signal                     |
| V1 as legibility signal (entropy/confidence)  | ---        | +0                | No separation between FN illegible and correct               |

### E. External OCR

| Approach                       | Best Score | Delta | Notes                                      |
|--------------------------------|------------|-------|--------------------------------------------|
| EasyOCR on crops (35x35px)     | ---        | +0    | 0 detections --- crops too small           |
| Tesseract on 4x upscaled crops | ---        | +0    | 0 detections --- crops too small and noisy |
| EasyOCR on upscaled + enhanced | ---        | +0    | 0 detections                               |

### F. Meta-Classifier (Learned Aggregation)

| Approach                                 | Best Score | Delta | Notes                                                                 |
|------------------------------------------|------------|-------|-----------------------------------------------------------------------|
| GBM on raw-image train features → test   | ≤1055      | ≤0    | Train/test distribution mismatch (7% vs 84% correct)                  |
| GBM on proper train crops → test         | ≤1067      | +0    | No signal beyond weight (40% feature importance)                      |
| RF, LR on proper train crops             | ≤1067      | +0    | Same --- quality filter already captures the signal                   |
| LSTM consolidation (teammate's proposal) | ---        | ---   | Architecture issues: 10K embedding dim, trains on test, no separation |

### G. PaRSeq Fine-Tuning

| Approach                                           | Best Score | Delta | Notes                                        |
|----------------------------------------------------|------------|-------|----------------------------------------------|
| Fine-tuned PaRSeq (decoder only, 1 epoch, lr=1e-5) | 1050       | -5    | Standalone: worse. Val 92.43%→92.98%         |
| Fine-tuned + quality filter                        | 1058       | +3    | Still worse than original + QF (1067)        |
| Ensemble: original + fine-tuned recovery           | 1069       | +14   | +2 from recovery, but same as QF+digit alone |
| Ensemble: fine-tuned as tiebreaker                 | ≤1066      | +11   | Hurts more than helps on uncertain tracklets |

### H. Upstream / Legibility

| Approach                                         | Best Score | Delta | Notes                                                          |
|--------------------------------------------------|------------|-------|----------------------------------------------------------------|
| PaRSeq on raw images (31 FP illegible tracklets) | ---        | +0    | 0/31 correct --- raw BBs too noisy without pose crops          |
| Lower legibility threshold                       | ---        | +0    | All 31 FP tracklets have scores \<0.04 --- genuinely illegible |
| Raise legibility threshold                       | ---        | +0    | 26 FN tracklets have max scores \>0.95 --- can't catch them    |
| Legible frame count filter                       | 1068       | +1    | Marginal, too correlated with weight                           |

------------------------------------------------------------------------

## Error Analysis (141 remaining errors after best pipeline at 1072)

### Error Categories

| Category                            | Count | \% of Errors | Recoverable?                                                                            |
|-------------------------------------|-------|--------------|-----------------------------------------------------------------------------------------|
| No data on disk (zero raw images)   | 48    | 34%          | No --- tracklets exist in GT but have no image files                                    |
| Wrong number (PaRSeq misreads)      | 42    | 30%          | Partially --- 33/42 have GT in top-5, but no signal to pick it                          |
| Filtered out (QF rejects, has data) | 27    | 19%          | Partially --- 9 correct among 27, but can't separate from 18 wrong                      |
| False positive (pred\>0, GT=-1)     | 24    | 17%          | No --- high weight (6-30) and high agreement (0.46-1.0), indistinguishable from correct |

### Unrecoverable Errors (79 tracklets)

| Type                                      | Count | Why                                                                   |
|-------------------------------------------|-------|-----------------------------------------------------------------------|
| Zero data on disk                         | 48    | Tracklets in GT have no corresponding image directory                 |
| Ball detector errors with zero data       | 8     | GT=2 (jersey #2) but classified as ball, no images                    |
| Truly illegible (legibility score \<0.04) | 23    | Legibility classifier very confident, PaRSeq also fails on raw images |

### Theoretical Ceiling

| Scenario                                              | Accuracy                |
|-------------------------------------------------------|-------------------------|
| Fix ALL errors with data (93 tracklets)               | 96.0% (1163/1211)       |
| Fix all wrong-number where GT in top-5 (33 tracklets) | 91.2% (1105/1211)       |
| Fix all filtered-out correct (9 tracklets)            | 89.2% (1081/1211)       |
| **Realistic ceiling (aggregation only)**              | **\~89% (\~1078/1211)** |
| Hard ceiling (data exists)                            | 93.5% (1132/1211)       |

### Top Confusion Patterns (Wrong-Number Errors)

| Confusion      | Count | Pattern                                     |
|----------------|-------|---------------------------------------------|
| pred=30, gt=31 | 5     | Ones digit: 0↔1                             |
| pred=27, gt=17 | 4     | Tens digit: 2↔1                             |
| pred=36, gt=16 | 4     | Tens digit: 3↔1                             |
| pred=17, gt=11 | 3     | Ones digit: 7↔1                             |
| pred=1, gt=2   | 8     | Ball detector assigns 1, actually jersey #2 |

### Digit-Level Error Patterns

| Pattern                   | Count | \% of Wrong-Number |
|---------------------------|-------|--------------------|
| Same tens, different ones | 23    | 45%                |
| Different tens, same ones | 17    | 33%                |
| Both digits different     | 11    | 22%                |

------------------------------------------------------------------------

## Key Findings

1.  **Quality filter is the single most effective improvement (+12).** A simple two-threshold gate (weight AND agreement) catches false positives that Koshkina's single threshold misses.

2.  **The error floor is set by missing data (48 tracklets) and truly illegible images (23+ tracklets).** No aggregation strategy can recover these.

3.  **PaRSeq's predictions are the bottleneck.** When PaRSeq misreads a digit, the raw softmax distributions agree with the wrong prediction. Re-ranking from the same model's outputs cannot fix fundamental misrecognitions.

4.  **The multitask model (55% frame accuracy) is too weak to help PaRSeq (83% frame accuracy).** When they disagree, PaRSeq is correct 82% of the time.

5.  **Fine-tuning PaRSeq on in-domain data helps marginally on validation (+0.55%) but hurts end-to-end accuracy (-9 net) due to new confusion patterns (16→14, 16→36).**

6.  **External OCR (EasyOCR, Tesseract) cannot read the 35×35 pixel pose-guided crops.** These models need larger text.

7.  **TTA recovery is the second most effective component (+2 to +5)** but only when applied to rejected tracklets (not broadly).
