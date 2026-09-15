# iMac CPU — September 11, 2026

XLM-R training on iMac CPU, batch size 1.

Measured interval: batch 0 to batch 9600, 20:28:26–23:52:28 = 12,242 seconds / 9,600 training examples = **1.2752 seconds/example**. The epoch completed with training loss 1.1096; the final 94 examples are excluded from timing because the completion line has no timestamp.

## Training log

```text
2026-09-11 20:28:26 | Processing batch 0/9694
2026-09-11 20:31:07 | Processing batch 100/9694
2026-09-11 20:33:32 | Processing batch 200/9694
2026-09-11 20:35:54 | Processing batch 300/9694
2026-09-11 20:38:16 | Processing batch 400/9694
2026-09-11 20:40:41 | Processing batch 500/9694
2026-09-11 20:42:58 | Processing batch 600/9694
2026-09-11 20:45:29 | Processing batch 700/9694
2026-09-11 20:47:51 | Processing batch 800/9694
2026-09-11 20:50:11 | Processing batch 900/9694
2026-09-11 20:52:26 | Processing batch 1000/9694
2026-09-11 20:54:34 | Processing batch 1100/9694
2026-09-11 20:56:43 | Processing batch 1200/9694
2026-09-11 20:58:48 | Processing batch 1300/9694
2026-09-11 21:00:49 | Processing batch 1400/9694
2026-09-11 21:02:50 | Processing batch 1500/9694
2026-09-11 21:04:55 | Processing batch 1600/9694
2026-09-11 21:07:01 | Processing batch 1700/9694
2026-09-11 21:09:11 | Processing batch 1800/9694
2026-09-11 21:11:18 | Processing batch 1900/9694
2026-09-11 21:13:24 | Processing batch 2000/9694
2026-09-11 21:15:31 | Processing batch 2100/9694
2026-09-11 21:17:38 | Processing batch 2200/9694
2026-09-11 21:19:45 | Processing batch 2300/9694
2026-09-11 21:21:57 | Processing batch 2400/9694
2026-09-11 21:24:14 | Processing batch 2500/9694
2026-09-11 21:26:27 | Processing batch 2600/9694
2026-09-11 21:28:36 | Processing batch 2700/9694
2026-09-11 21:30:47 | Processing batch 2800/9694
2026-09-11 21:33:01 | Processing batch 2900/9694
2026-09-11 21:35:14 | Processing batch 3000/9694
2026-09-11 21:37:30 | Processing batch 3100/9694
2026-09-11 21:39:43 | Processing batch 3200/9694
2026-09-11 21:41:48 | Processing batch 3300/9694
2026-09-11 21:43:55 | Processing batch 3400/9694
2026-09-11 21:46:01 | Processing batch 3500/9694
2026-09-11 21:48:08 | Processing batch 3600/9694
2026-09-11 21:50:14 | Processing batch 3700/9694
2026-09-11 21:52:19 | Processing batch 3800/9694
2026-09-11 21:54:28 | Processing batch 3900/9694
2026-09-11 21:56:48 | Processing batch 4000/9694
2026-09-11 21:59:21 | Processing batch 4100/9694
2026-09-11 22:01:54 | Processing batch 4200/9694
2026-09-11 22:04:28 | Processing batch 4300/9694
2026-09-11 22:07:05 | Processing batch 4400/9694
2026-09-11 22:09:28 | Processing batch 4500/9694
2026-09-11 22:11:37 | Processing batch 4600/9694
2026-09-11 22:13:40 | Processing batch 4700/9694
2026-09-11 22:15:41 | Processing batch 4800/9694
2026-09-11 22:17:41 | Processing batch 4900/9694
2026-09-11 22:19:41 | Processing batch 5000/9694
2026-09-11 22:21:41 | Processing batch 5100/9694
2026-09-11 22:23:40 | Processing batch 5200/9694
2026-09-11 22:25:40 | Processing batch 5300/9694
2026-09-11 22:27:39 | Processing batch 5400/9694
2026-09-11 22:29:39 | Processing batch 5500/9694
2026-09-11 22:31:40 | Processing batch 5600/9694
2026-09-11 22:33:39 | Processing batch 5700/9694
2026-09-11 22:35:39 | Processing batch 5800/9694
2026-09-11 22:37:39 | Processing batch 5900/9694
2026-09-11 22:39:39 | Processing batch 6000/9694
2026-09-11 22:41:40 | Processing batch 6100/9694
2026-09-11 22:43:41 | Processing batch 6200/9694
2026-09-11 22:45:41 | Processing batch 6300/9694
2026-09-11 22:47:43 | Processing batch 6400/9694
2026-09-11 22:49:45 | Processing batch 6500/9694
2026-09-11 22:51:47 | Processing batch 6600/9694
2026-09-11 22:53:49 | Processing batch 6700/9694
2026-09-11 22:55:51 | Processing batch 6800/9694
2026-09-11 22:57:53 | Processing batch 6900/9694
2026-09-11 22:59:55 | Processing batch 7000/9694
2026-09-11 23:01:58 | Processing batch 7100/9694
2026-09-11 23:04:00 | Processing batch 7200/9694
2026-09-11 23:06:03 | Processing batch 7300/9694
2026-09-11 23:08:06 | Processing batch 7400/9694
2026-09-11 23:10:08 | Processing batch 7500/9694
2026-09-11 23:12:10 | Processing batch 7600/9694
2026-09-11 23:14:12 | Processing batch 7700/9694
2026-09-11 23:16:15 | Processing batch 7800/9694
2026-09-11 23:18:17 | Processing batch 7900/9694
2026-09-11 23:20:19 | Processing batch 8000/9694
2026-09-11 23:22:22 | Processing batch 8100/9694
2026-09-11 23:24:24 | Processing batch 8200/9694
2026-09-11 23:26:25 | Processing batch 8300/9694
2026-09-11 23:28:25 | Processing batch 8400/9694
2026-09-11 23:30:25 | Processing batch 8500/9694
2026-09-11 23:32:26 | Processing batch 8600/9694
2026-09-11 23:34:26 | Processing batch 8700/9694
2026-09-11 23:36:26 | Processing batch 8800/9694
2026-09-11 23:38:26 | Processing batch 8900/9694
2026-09-11 23:40:27 | Processing batch 9000/9694
2026-09-11 23:42:27 | Processing batch 9100/9694
2026-09-11 23:44:27 | Processing batch 9200/9694
2026-09-11 23:46:28 | Processing batch 9300/9694
2026-09-11 23:48:28 | Processing batch 9400/9694
2026-09-11 23:50:28 | Processing batch 9500/9694
2026-09-11 23:52:28 | Processing batch 9600/9694
Epoch 1/1: training loss = 1.1096
```
