# XLM-R training runtime comparisons

All timings are average seconds per **training example**

| Configuration | Batch size | Measured interval | Examples | Seconds/example | Projected epoch time | Status |
|---|---:|---|---:|---:|---:|---|
| iMac MPS | — | — | — | — | — | Out of memory; no runtime data |
| [iMac CPU](2026-09-11-imac-cpu-batch1.md) | 1 | Sept 11, 20:28:26–23:52:28 (12,242 s) | 9,600 | **1.2752** | 3h 26m 2s | Epoch completed; training loss 1.1096 |
| MacBook Air MPS, original dynamic padding | 1 | — | — | — | — | Out of memory during batch 24; no runtime data |
| [MacBook Air CPU](2026-09-13-mba-cpu-batch1.md) | 1 | Sept 13, 19:27:51–19:34:23 (392 s) | 1,000 | **0.392** | 1h 3m 20s | Measured; no complete epoch shown |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch1.md) | 1 | Sept 14, 15:48:50–15:51:03 (133 s) | 400 | **0.3325** | 53m 43s | Stopped intentionally |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch2.md) | 2 | Sept 14, 15:53:06–16:38:07 (2,701 s) | 9,600 | **0.2814** | 45m 27s | Epoch 1 completed; training loss 1.1077 |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch4.md) | 4 | Sept 14, 16:45:37–16:52:03 (386 s) | 1,600 | **0.2413** | 38m 59s | Partial run; no full epoch shown |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch8.md) | 8 | Sept 14, 16:55:38–17:01:59 (381 s) | 800 | **0.4763** | 1h 16m 57s | Partial run; no full epoch shown |
| MacBook Air MPS, fixed padding 512 | 16 | 34m 7s elapsed | Unknown | **>1.279 (lower bound)** | >3h 26m 42s (lower bound) | Run incomplete; stopped before batch 100 / 1,600-example milestone |
| [MacBook Air MPS, fixed padding 512, PyTorch 2.14.0](2026-09-14-mba-mps-padding512-batch4-torch2.14.0.md) | 4 | Sept 14, 18:17:15–18:21:57 (282 s) | 1,600 | **0.17625** | 28m 29s | Partial run; no full epoch shown |
| [MacBook Air MPS, dynamic padding, PyTorch 2.14.0](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0.md) | 4 | Sept 14, 18:26:37–18:29:03 (146 s) | 2,400 | **0.0608333** | 9m 50s | Partial run; no full epoch shown |
| [MacBook Air MPS, dynamic padding, PyTorch 2.14.0, Python 3.14.7 modern](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0-py3.14-modern.md) | 4 | Sept 14, 18:50:27–19:00:01 (574 s) | 9,600 | **0.0597917** | 9m 40s | Epoch completed; training loss 1.1052; final 94 examples untimed |

Projections use 9,694 training examples and full-precision interval averages, rounded to the nearest second. They assume the measured average pace holds, exclude validation and other overhead, and do not establish epoch completion. Batch 16 uses a lower bound of 2,047 / 1,600 seconds per example; the run is incomplete.

Dates are in 2026. iMac CPU timing covers batches 0–9600; the final 94 examples have no end timestamp and are excluded from the average.

Fixed-padding MPS: `padding='max_length'`, tokenizer default 512, PyTorch 2.2.2 unless marked otherwise, FP32, AdamW; progress printed every 100 batches. Batch 2 completed one full epoch; timing covers batches 0–4800, excluding the final 94 examples without a completion timestamp. Longer-run stability remains unverified.

PyTorch 2.2.2 batch 4's successive 100-batch intervals took 89, 89, 98, and 110 seconds. The PyTorch 2.14.0 batch-4 interval took 26.94% less time for the same 1,600 examples (1.369× throughput).

## Hardware

| Machine | Processor | Graphics | Memory |
|---|---|---|---|
| iMac | 3.8 GHz 8-core Intel Core i7 | AMD Radeon Pro 5500 XT 8 GB | 16 GB 2667 MHz DDR4 |
| MacBook Air | Apple M5 | — | 16 GB unified memory |
