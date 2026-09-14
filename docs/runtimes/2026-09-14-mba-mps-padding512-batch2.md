# MacBook Air MPS — September 14, 2026

XLM-R training on MacBook Air MPS, batch size 2, `padding='max_length'` with tokenizer default 512; PyTorch 2.2.2, FP32, AdamW. Progress printed every 100 batches.

Measured interval: batch 0 to batch 4800, 15:53:06–16:38:07 = 2,701 seconds / 9,600 training examples = **0.2814 seconds/example**. Epoch 1 completed with training loss 1.1077; the final 94 examples are excluded from timing because the completion line has no timestamp.

## Training log

```text
2026-09-14 15:53:06 | Processing batch 0/4847
2026-09-14 15:53:57 | Processing batch 100/4847
2026-09-14 15:54:44 | Processing batch 200/4847
2026-09-14 15:55:33 | Processing batch 300/4847
2026-09-14 15:56:30 | Processing batch 400/4847
2026-09-14 15:57:28 | Processing batch 500/4847
2026-09-14 15:58:26 | Processing batch 600/4847
2026-09-14 15:59:21 | Processing batch 700/4847
2026-09-14 16:00:21 | Processing batch 800/4847
2026-09-14 16:01:17 | Processing batch 900/4847
2026-09-14 16:02:14 | Processing batch 1000/4847
2026-09-14 16:03:10 | Processing batch 1100/4847
2026-09-14 16:04:04 | Processing batch 1200/4847
2026-09-14 16:04:53 | Processing batch 1300/4847
2026-09-14 16:05:50 | Processing batch 1400/4847
2026-09-14 16:06:46 | Processing batch 1500/4847
2026-09-14 16:07:39 | Processing batch 1600/4847
2026-09-14 16:08:28 | Processing batch 1700/4847
2026-09-14 16:09:25 | Processing batch 1800/4847
2026-09-14 16:10:26 | Processing batch 1900/4847
2026-09-14 16:11:27 | Processing batch 2000/4847
2026-09-14 16:12:24 | Processing batch 2100/4847
2026-09-14 16:13:17 | Processing batch 2200/4847
2026-09-14 16:14:23 | Processing batch 2300/4847
2026-09-14 16:15:27 | Processing batch 2400/4847
2026-09-14 16:16:31 | Processing batch 2500/4847
2026-09-14 16:17:27 | Processing batch 2600/4847
2026-09-14 16:18:23 | Processing batch 2700/4847
2026-09-14 16:19:31 | Processing batch 2800/4847
2026-09-14 16:20:32 | Processing batch 2900/4847
2026-09-14 16:21:30 | Processing batch 3000/4847
2026-09-14 16:22:26 | Processing batch 3100/4847
2026-09-14 16:23:21 | Processing batch 3200/4847
2026-09-14 16:24:15 | Processing batch 3300/4847
2026-09-14 16:25:07 | Processing batch 3400/4847
2026-09-14 16:26:01 | Processing batch 3500/4847
2026-09-14 16:26:56 | Processing batch 3600/4847
2026-09-14 16:27:50 | Processing batch 3700/4847
2026-09-14 16:28:44 | Processing batch 3800/4847
2026-09-14 16:29:38 | Processing batch 3900/4847
2026-09-14 16:30:33 | Processing batch 4000/4847
2026-09-14 16:31:28 | Processing batch 4100/4847
2026-09-14 16:32:21 | Processing batch 4200/4847
2026-09-14 16:33:15 | Processing batch 4300/4847
2026-09-14 16:34:16 | Processing batch 4400/4847
2026-09-14 16:35:17 | Processing batch 4500/4847
2026-09-14 16:36:15 | Processing batch 4600/4847
2026-09-14 16:37:12 | Processing batch 4700/4847
2026-09-14 16:38:07 | Processing batch 4800/4847
Epoch 1/3: training loss = 1.1077
```
