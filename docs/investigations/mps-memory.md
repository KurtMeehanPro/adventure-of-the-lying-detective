# GPU memory investigation — 13 September 2026

**Status:** Individual MPS updates work; a complete GPU training epoch remains unresolved.

## Configuration and observed failure

The investigation used a reported Apple M5 MacBook Air with 16 GB unified memory, macOS 26.6.2, native arm64 Python 3.12.10, PyTorch 2.2.2 and Transformers 4.44.2. The workload was full FP32 fine-tuning of `FacebookAI/xlm-roberta-base` with a three-label classification head, stock AdamW (`lr=2e-5`), batch size 1, and dynamic padding of tokenized premise–hypothesis pairs. MPS execution was verified with actual GPU operations; no separate acceleration plugin was missing.

Two fresh notebook runs reached the last printed batch index **23** approximately 14 seconds after index 0. Logging occurs **before** batch computation: this indicates that batches 0–22 completed and the 24th batch began, not that 24 updates completed. Earlier logging only every 100 batches had obscured this progression; the failure was not established to occur on the first update.

Both runs failed inside `optimizer.step()`, at AdamW's denominator calculation, `exp_avg_sq.sqrt() / bias_correction2_sqrt`. The errors reported allocator/other allocations of **4.92/15.06 GB** or **5.73/14.34 GB**, a **20.13 GB** ceiling, and a **732.43 MB** private-pool request. These labels reproduce the error's formatting. The requested size matches one `[250002, 768]` FP32 vocabulary embedding tensor (732.43 MiB). AdamW maintains two moment buffers and creates large update temporaries; the failure location alone does not establish an optimizer leak.

In this PyTorch version, “other allocations” means same-process Metal allocations outside PyTorch's allocator heaps, including framework allocations—not memory attributed to other applications. Driver allocation minus live-tensor allocation also includes allocator cache, so it is not the same counter. These figures are not measurements of physical resident RAM or a hardware-RAM requirement. See the [version-specific allocator source](https://github.com/pytorch/pytorch/blob/v2.2.2/aten/src/ATen/mps/MPSAllocator.mm).

## Isolation tests completed

Fresh processes used the existing environment and default memory ceiling; no updated model weights were saved.

| Test | Result | Highest sampled driver allocation | Allocator-reported other allocations |
|---|---|---:|---:|
| One embedding-sized FP32 parameter plus dense gradient; one AdamW update | Passed | 4.309 GiB | 448 KiB at cleanup |
| Full model; one real 33-token example; forward, backward and one AdamW update | Passed | 6.38 GiB | Approximately 737 MiB after backward and update |

For the full-model test, driver allocation was approximately 1.07 GiB after model transfer, 1.11 GiB after forward, 2.86 GiB after backward, and 6.38 GiB after the update. Pre-update cache clearing freed only 8 MiB; post-update clearing reduced driver allocation to 4.94 GiB.

These are **sampled maxima, not absolute peaks**. Phase synchronization changes execution overlap, and cache clearing changes allocator state. A single short example does not test accumulation across varying sequence lengths or establish steady-state training performance.

## Working hypothesis and next controlled test

Shape-dependent MPS graph caching or retention is a plausible explanation for growth across batches, but is not a verified cause here. Related upstream evidence includes [variable-length Transformer training growth](https://github.com/pytorch/pytorch/issues/121113), a [BERT reporter's fixed-padding workaround](https://github.com/pytorch/pytorch/issues/121113#issuecomment-1976851242), and a [maintainer explanation of input-shape-based graph caching](https://github.com/pytorch/pytorch/issues/152550#issuecomment-2843624998). These reports motivate a test; they do not demonstrate a fix for this notebook. Newer PyTorch backend changes have not been tested in this environment.

**Proposed, not run:** compare the same approximately 40 examples in the same order using dynamic versus fixed right padding to one common maximum length. Retain identical real tokens, truncation limits and attention-mask semantics; hold FP32, model, AdamW and batch size 1 constant. Record token lengths and per-batch live/driver allocation. Keep raw measurements separate from synchronization/cache-clearing variants so instrumentation is not confounded with padding. Preserve the default memory safety ceiling. Evaluate memory growth and update completion before attempting another full epoch.
