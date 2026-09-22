# XLM-Roberta Base training runtime comparisons

## Background

While fine-tuning FacebookAI/xlm-roberta-base on the iMac with an Intel chipset using MPS, I encountered an out-of-memory error. This led to an [investigation into MPS memory usage](../investigations/mps-memory.md), which continued on the MacBook Air M5. The same MPS memory issue was found on Mabook Air with PyTorch 2.2.2. During the investigation, I also recorded training runtimes across different hardware and software configurations. The comparisons below document those results.

## Limitations
The iMac with Intel is limited to PyTorch 2.2.2 when using official macOS x86_64 binaries, as [support ended with the 2.2 series](https://dev-discuss.pytorch.org/t/pytorch-macos-x86-builds-deprecation-starting-january-2024/1690).

## Findings
Fixed-length padding and upgrading to newer PyTorch, both, individually, resolved the memory issue on the Macbook Air. It's still untested whether fixed padding resolves the iMac's MPS memory issue. Even if it does fix the issue on iMac, as it did on the Macbook Air, newer official builds for PyTorch are unavailable for the iMac. Hence, we can't get the same kind of speed improvements that were shown in the table below for Macbook Air using newer versions of PyTorch and dynamic padding. The fastest measured configuration was the MacBook Air using newer PyTorch 2.14.0 with batch size 4, dynamic padding, and Python 3.14.7.

## Runtimes
| Configuration | Batch size | Measured interval | Examples | Seconds/example | Projected epoch time | Status |
|---|---:|---|---:|---:|---:|---|
| iMac MPS | — | — | — | — | — | Out of memory; no runtime data |
| [iMac CPU](2026-09-11-imac-cpu-batch1.md) | 1 | Sept 11, 20:28:26–23:52:28 (12,242 s) | 9,600 | **1.2752** | 3h 26m 2s | Epoch completed; training loss 1.1096 |
| MacBook Air MPS, original dynamic padding | 1 | — | — | — | — | Out of memory during batch 24; no runtime data |
| [MacBook Air CPU](2026-09-13-mba-cpu-batch1.md) | 1 | Sept 13, 19:27:51–19:34:23 (392 s) | 1,000 | **0.392** | 1h 3m 20s | Partial run, stopped intentionally. |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch1.md) | 1 | Sept 14, 15:48:50–15:51:03 (133 s) | 400 | **0.3325** | 53m 43s | Partial run, stopped intentionally. |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch2.md) | 2 | Sept 14, 15:53:06–16:38:07 (2,701 s) | 9,600 | **0.2814** | 45m 27s | Epoch 1 completed; training loss 1.1077 |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch4.md) | 4 | Sept 14, 16:45:37–16:52:03 (386 s) | 1,600 | **0.2413** | 38m 59s | Partial run, stopped intentionally. |
| [MacBook Air MPS, fixed padding 512](2026-09-14-mba-mps-padding512-batch8.md) | 8 | Sept 14, 16:55:38–17:01:59 (381 s) | 800 | **0.4763** | 1h 16m 57s | Partial run, stopped intentionally. |
| MacBook Air MPS, fixed padding 512 | 16 | 34m 7s elapsed | Unknown | **>1.279 (lower bound)** | >3h 26m 42s (lower bound) | Run incomplete; stopped before batch 100 / 1,600-example milestone |
| [MacBook Air MPS, fixed padding 512, PyTorch 2.14.0](2026-09-14-mba-mps-padding512-batch4-torch2.14.0.md) | 4 | Sept 14, 18:17:15–18:21:57 (282 s) | 1,600 | **0.17625** | 28m 29s | Partial run, stopped intentionally. |
| [MacBook Air MPS, dynamic padding, PyTorch 2.14.0](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0.md) | 4 | Sept 14, 18:26:37–18:29:03 (146 s) | 2,400 | **0.0608333** | 9m 50s | Partial run, stopped intentionally. |
| [MacBook Air MPS, dynamic padding, PyTorch 2.14.0, Python 3.14.7 modern](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0-py3.14-modern.md) | 4 | Sept 14, 18:50:27–19:00:01 (574 s) | 9,600 | **0.0597917** | 9m 40s | Epoch completed; training loss 1.1052; final 94 examples untimed |

## Dates
Dates are in 2026.

## Recorded Time and estimations
- progress was printed every 100 batches. It does not include a timestamp for the final completion of the training epoch
- In cases where the epoch completed, the remaining examples were not used in the averages.
- time estimation excludes validation and other overhead

## Projections
- use 9,694 training examples and full-precision interval averages, rounded to the nearest second.
- assume the measured average pace holds.
- do not prove the training epoch would definitely complete (though it seems perfectly reasonable to assume it would)

## Batch size 16
Batch size 16 run did not complete. I did not let it get to batch 100 as it was taking so long. It uses a lower bound of 2,047 / 1,600 seconds per example.

## Settings
- Fixed-padding MPS: `padding='max_length'`
- tokenizer default 512
- PyTorch 2.2.2 unless marked otherwise
- FP32
- AdamW

## Hardware
| Machine | Processor | Graphics | Memory |
|---|---|---|---|
| iMac | 3.8 GHz 8-core Intel Core i7 | AMD Radeon Pro 5500 XT 8 GB | 16 GB 2667 MHz DDR4 |
| MacBook Air | Apple M5 | — | 16 GB unified memory |
