# MPS Memory Investigation

## 13 September 2026 — Original failure

Full FP32 fine-tuning of `FacebookAI/xlm-roberta-base` ran out of MPS memory on an Apple M5 MacBook Air with 16 GB unified memory, macOS 26.6.2, Python 3.12.10, PyTorch 2.2.2 and Transformers 4.44.2. Training used a three-label classification head, AdamW (`lr=2e-5`), batch size 1 and dynamic padding of premise–hypothesis pairs.

Two fresh runs failed during the 24th batch, after 23 completed batches, about 14 seconds after training began. AdamW's update requested another **732.43 MB**, which MPS could not allocate. A single full-model training update succeeded in isolation, but repeated training failed. MPS training also ran out of memory on the Intel iMac.

Related PyTorch reports describe memory growth with [varying-length Transformer training](https://github.com/pytorch/pytorch/issues/121113), [varying-length attention (SDPA)](https://github.com/pytorch/pytorch/issues/152550), and [`nn.Linear`](https://github.com/pytorch/pytorch/issues/132332). These suggested testing fixed padding and a newer PyTorch version.

## 2026-09-14 — Successful training

On the MacBook Air, fixed padding to `max_length=512` with PyTorch 2.2.2 enabled a full training epoch at batch size 2.

Upgrading directly to PyTorch 2.14.0 allowed dynamic padding at batch size 4. A full epoch then completed in the modern environment with Python 3.14.7 and PyTorch 2.14.0.

The fixed-padding workaround will not be tested on the Intel iMac. See the [runtime performance documentation](../runtimes/README.md) for timings, environments and training logs.
