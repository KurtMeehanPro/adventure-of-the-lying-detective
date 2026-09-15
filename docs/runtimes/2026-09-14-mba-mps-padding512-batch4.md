# MacBook Air MPS — September 14, 2026

XLM-R training on MacBook Air MPS, batch size 4, `padding='max_length'` with tokenizer default 512; PyTorch 2.2.2, FP32, AdamW. Progress printed every 100 batches.

Measured interval: batch 0 to batch 400, 16:45:37–16:52:03 = 386 seconds / 1,600 training examples = **0.2413 seconds/example** (unrounded: 0.24125). Successive 100-batch intervals took 89, 89, 98, and 110 seconds. Partial run, stopped intentionally.

## Training log

```text
2026-09-14 16:45:37 | Processing batch 0/2424
2026-09-14 16:47:06 | Processing batch 100/2424
2026-09-14 16:48:35 | Processing batch 200/2424
2026-09-14 16:50:13 | Processing batch 300/2424
2026-09-14 16:52:03 | Processing batch 400/2424
```
