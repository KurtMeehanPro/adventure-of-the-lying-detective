# MacBook Air MPS, dynamic padding, PyTorch 2.14.0 — September 14, 2026

XLM-R training on MacBook Air MPS, Python 3.12.10, PyTorch 2.14.0, batch size 4; FP32, AdamW. `DataCollatorWithPadding(tokenizer=tokenizer, return_tensors='pt')` uses default `padding=True`, padding to the longest sequence in each batch; explicit maximum-length padding removed. Progress printed every 100 batches.

Measured interval: batch 0 to batch 600, 18:26:37–18:29:03 = 146 seconds / 2,400 training examples = **0.0608333 seconds/example**. Partial run; dynamic padding passed the earlier batch-24 failure point, but no full epoch is shown.

Compared with [PyTorch 2.14.0 fixed-padding batch 4](2026-09-14-mba-mps-padding512-batch4-torch2.14.0.md) (0.17625 seconds/example), this interval used **65.48% less time per example**, with **2.897× throughput**. At this average pace, 9,694 examples would take approximately **590 seconds (9m 50s)**; this is a projection, not a measured epoch runtime.

## Training log

```text
2026-09-14 18:26:37 | Processing batch 0/2424
2026-09-14 18:27:04 | Processing batch 100/2424
2026-09-14 18:27:28 | Processing batch 200/2424
2026-09-14 18:27:52 | Processing batch 300/2424
2026-09-14 18:28:15 | Processing batch 400/2424
2026-09-14 18:28:38 | Processing batch 500/2424
2026-09-14 18:29:03 | Processing batch 600/2424
```
