# MacBook Air MPS, PyTorch 2.14.0 — September 14, 2026

XLM-R training on MacBook Air MPS, batch size 4, `padding='max_length'` with tokenizer default 512; FP32, AdamW. Separate environment with PyTorch 2.14.0, Python 3.12.10, and required setuptools 77.0.3 added; other baseline package versions unchanged. Progress printed every 100 batches.

Measured interval: batch 0 to batch 400, 18:17:15–18:21:57 = 282 seconds / 1,600 training examples = **0.17625 seconds/example**. Partial run; no epoch completion shown.

Compared with the [PyTorch 2.2.2 batch-4 interval](2026-09-14-mba-mps-padding512-batch4.md) (386 seconds / 1,600 examples), this interval took **26.94% less time**, with **1.369× throughput**.

## Training log

```text
2026-09-14 18:17:15 | Processing batch 0/2424
2026-09-14 18:18:24 | Processing batch 100/2424
2026-09-14 18:19:35 | Processing batch 200/2424
2026-09-14 18:20:46 | Processing batch 300/2424
2026-09-14 18:21:57 | Processing batch 400/2424
```
