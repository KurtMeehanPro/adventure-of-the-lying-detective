# XLM-Roberta training runtime comparisons

<br>

## Background

This project required a multitude of different training runs on different hardwares and configurations. I became curious about the configurations and associated runtimes. The results are documented below.

<br>

## Runtimes
| Device | Model | [Configuration](#configuration) | Batch size | Epochs completed | Examples completed | Examples in calculation | Measured time (s) | Examples/second | Epoch time (9,694 examples) | [Out of memory](../investigations/mps-memory.md) | Runtime log |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| iMac MPS | XLM-RoBERTa base | 1 | — | 0 | — | — | — | — | — | True | n/a |
| iMac CPU | XLM-RoBERTa base | 1 | 1 | 1 | 9,694 | 9,600 | 12,242 | **0.7842** | ~3h 26m 2s | False | [log](2026-09-11-imac-cpu-batch1.md) |
| MacBook Air MPS | XLM-RoBERTa base | 2 | 1 | 0 | — | — | — | — | — | True | n/a |
| MacBook Air CPU | XLM-RoBERTa base | 2 | 1 | 0 | 1,000 | 1,000 | 392 | **2.5510** | ~1h 3m 20s | False | [log](2026-09-13-mba-cpu-batch1.md) |
| MacBook Air MPS | XLM-RoBERTa base | 3 | 1 | 0 | 400 | 400 | 133 | **3.0075** | ~53m 43s | False | [log](2026-09-14-mba-mps-padding512-batch1.md) |
| MacBook Air MPS | XLM-RoBERTa base | 3 | 2 | 1 | 9,694 | 9,600 | 2,701 | **3.5542** | ~45m 27s | False | [log](2026-09-14-mba-mps-padding512-batch2.md) |
| MacBook Air MPS | XLM-RoBERTa base | 3 | 4 | 0 | 1,600 | 1,600 | 386 | **4.1451** | ~38m 59s | False | [log](2026-09-14-mba-mps-padding512-batch4.md) |
| MacBook Air MPS | XLM-RoBERTa base | 3 | 8 | 0 | 800 | 800 | 381 | **2.0997** | ~1h 16m 57s | False | [log](2026-09-14-mba-mps-padding512-batch8.md) |
| MacBook Air MPS | XLM-RoBERTa base | 3 | 16 | 0 | Unknown | 1,600 | 2,047 | **<0.7816 (upper bound)** | >3h 26m 42s (lower bound) | False | n/a* (see notes) |
| MacBook Air MPS | XLM-RoBERTa base | 4 | 4 | 0 | 1,600 | 1,600 | 282 | **5.6738** | ~28m 29s | False | [log](2026-09-14-mba-mps-padding512-batch4-torch2.14.0.md) |
| MacBook Air MPS | XLM-RoBERTa base | 5 | 4 | 0 | 2,400 | 2,400 | 146 | **16.4384** | ~9m 50s | False | [log](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0.md) |
| MacBook Air MPS | XLM-RoBERTa base | 6 | 4 | 1 | 9,694 | 9,600 | 574 | **16.7247** | ~9m 40s | False | [log](2026-09-14-mba-mps-dynamic-padding-batch4-torch2.14.0-py3.14-modern.md) |
| Mac Studio MPS | XLM-RoBERTa base | 7 | 8 | 1 | 9,694 | 9,694 | 120 | **80.7833** | 2m 0s | False | [log](2026-09-22-mac-studio-mps-dynamic-padding-batch8-modern.md) |
| Mac Studio MPS | XLM-RoBERTa base | 7 | 16 | 1 | 9,694 | 9,694 | 85 | **114.0471** | 1m 25s | False | [log](2026-09-22-mac-studio-mps-dynamic-padding-batch16-modern.md) |
| Mac Studio MPS | XLM-RoBERTa base | 7 | 32 | 2 | 19,388 | 19,388 | 138 | **140.4928** | 1m 9s | False | [log](2026-09-22-mac-studio-mps-dynamic-padding-batch32-modern.md) |
| Mac Studio MPS | XLM-RoBERTa base | 7 | 32 | 6 | 58,164 | 58,164 | 411 | **141.5182** | 1m 8.5s | False | [log](2026-09-22-mac-studio-mps-dynamic-padding-batch32-run2-modern.md) |
| Mac Studio MPS | XLM-RoBERTa base | 7 | 64 | 5 | 48,470 | 48,470 | 329 | **147.3252** | 1m 5.8s | False | [log](2026-09-22-mac-studio-mps-dynamic-padding-batch64-modern.md) |
| Mac Studio MPS | XLM-RoBERTa base | 7 | 128 | 5 | 48,470 | 48,470 | 375 | **129.2533** | 1m 15s | False | [log](2026-09-22-mac-studio-mps-dynamic-padding-batch128-modern.md) |
| Mac Studio MPS | XLM-RoBERTa large | 7 | 32 | 7 | 67,858 | 67,858 | 1,425 | **47.6196** | 3m 24s | False | [log](2026-09-28-mac-studio-mps-dynamic-padding-batch32-xlm-roberta-large-modern.md) |

<br>

### Notes:

In the Epoch time column:
- `~` marks an estimated value.
- Inequality signs mark upper and lower bounds.
- Unless otherwise marked, epoch time is either a directly measured single-epoch duration or the average of multiple measured epoch durations.

In the Runtime Log column:
- n/a marked for [Out of memory](../investigations/mps-memory.md) because no log generated before hitting OOM error
- n/a* marked for batch size 16 run - the run was manually aborted due to how much time it was taking

<br>

## Hardware
| Machine | Processor | Graphics | Memory |
|---|---|---|---|
| iMac | Intel 3.8 GHz 8-core i7 | AMD Radeon Pro 5500 XT 8 GB | 16 GB 2667 MHz DDR4 |
| MacBook Air | Apple M5 10 Core CPU | 10 Core GPU | 16 GB unified memory |
| Mac Studio | Apple M5 Max 18 Core CPU | 40 Core GPU | 64 GB unified memory |

<br>

## Configuration

| Configuration number | Python | PyTorch | Packages | Padding | Warmup, validation, early stopping, and checkpointing |
|---|---|---|---|---|---|
| 1 | 3.12.3 | 2.2.2 | [requirements-macos-intel.txt](../../requirements-macos-intel.txt) | dynamic padding | No |
| 2 | 3.12.10 | 2.2.2 | [requirements-macos-intel.txt](../../requirements-macos-intel.txt) | dynamic padding | No |
| 3 | 3.12.10 | 2.2.2 | [requirements-macos-intel.txt](../../requirements-macos-intel.txt) | fixed padding 512 (`padding='max_length'`) | No |
| 4 | 3.12.10 | 2.14.0 | [requirements-macos-intel.txt](../../requirements-macos-intel.txt) | fixed padding 512 (`padding='max_length'`) | No |
| 5 | 3.12.10 | 2.14.0 | [requirements-macos-intel.txt](../../requirements-macos-intel.txt) | dynamic padding | No |
| 6 | 3.14.7 | 2.14.0 | [requirements.txt](../../requirements.txt) | dynamic padding | No |
| 7 | 3.14.7 | 2.14.0 | [requirements.txt](../../requirements.txt) | dynamic padding | Yes |

### Note: If the PyTorch version listed in this table differs from the version in the linked packages file, the version listed in this table was used for the run.

<br>

## MPS Memory Issue

While fine-tuning FacebookAI/xlm-roberta-base on the iMac with an Intel chipset using MPS, I encountered an out-of-memory error. This led to an [investigation into MPS memory usage](../investigations/mps-memory.md), which continued on the MacBook Air M5. The same MPS memory issue was found on Mabook Air with PyTorch 2.2.2. Fixed-length padding and upgrading to newer PyTorch, both, individually, resolved the memory issue on the Macbook Air.

<br>

## Limitations
The iMac with Intel is limited to PyTorch 2.2.2 when using official macOS x86_64 binaries, as [support ended with the 2.2 series](https://dev-discuss.pytorch.org/t/pytorch-macos-x86-builds-deprecation-starting-january-2024/1690). It will not be tested whether fixed padding resolves the iMac's MPS memory issue. Even if it does fix the issue on iMac, as it did on the Macbook Air, newer official builds for PyTorch are unavailable for the iMac. Hence, the iMac can't get the same kind of speed improvements that are shown in the table below for Macbook Air using newer versions of PyTorch and dynamic padding.
