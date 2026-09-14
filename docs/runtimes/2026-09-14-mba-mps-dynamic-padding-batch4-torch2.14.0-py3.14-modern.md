# MacBook Air MPS, modern environment — September 14, 2026

XLM-R training on MacBook Air MPS, batch size 4, dynamic padding to the longest sequence in each batch. Environment: `kaggle_torch214_py314_modern`, system Python 3.14.7, PyTorch 2.14.0.

Package versions: transformers 5.17.0, numpy 2.5.3, pandas 3.0.5, matplotlib 3.11.2, scikit-learn 1.9.1, kagglehub 1.0.2, sentencepiece 0.2.2, safetensors 0.8.0, ipykernel 7.3.0, ipywidgets 8.1.9.

Measured interval: batch 0 to batch 2400, 18:50:27–19:00:01 = 574 seconds / 9,600 training examples = **0.0597917 seconds/example**. The full epoch completed with training loss 1.1052; the final 94 examples are excluded from timing because the completion line has no timestamp. Projected time for 9,694 examples at this pace: **9m 40s**, not a measured epoch duration.

The average time per example was **1.71% lower** than the [Python 3.12.10 dynamic-padding interval](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0.md). The intervals differ in length and multiple packages changed, so this comparison does not isolate Python's effect.

## Training log

```text
2026-09-14 18:50:27 | Processing batch 0/2424
2026-09-14 18:50:52 | Processing batch 100/2424
2026-09-14 18:51:15 | Processing batch 200/2424
2026-09-14 18:51:39 | Processing batch 300/2424
2026-09-14 18:52:03 | Processing batch 400/2424
2026-09-14 18:52:27 | Processing batch 500/2424
2026-09-14 18:52:50 | Processing batch 600/2424
2026-09-14 18:53:15 | Processing batch 700/2424
2026-09-14 18:53:38 | Processing batch 800/2424
2026-09-14 18:54:01 | Processing batch 900/2424
2026-09-14 18:54:25 | Processing batch 1000/2424
2026-09-14 18:54:49 | Processing batch 1100/2424
2026-09-14 18:55:12 | Processing batch 1200/2424
2026-09-14 18:55:36 | Processing batch 1300/2424
2026-09-14 18:56:01 | Processing batch 1400/2424
2026-09-14 18:56:24 | Processing batch 1500/2424
2026-09-14 18:56:47 | Processing batch 1600/2424
2026-09-14 18:57:11 | Processing batch 1700/2424
2026-09-14 18:57:34 | Processing batch 1800/2424
2026-09-14 18:57:58 | Processing batch 1900/2424
2026-09-14 18:58:22 | Processing batch 2000/2424
2026-09-14 18:58:46 | Processing batch 2100/2424
2026-09-14 18:59:11 | Processing batch 2200/2424
2026-09-14 18:59:35 | Processing batch 2300/2424
2026-09-14 19:00:01 | Processing batch 2400/2424
Epoch 1/1: training loss = 1.1052
```
