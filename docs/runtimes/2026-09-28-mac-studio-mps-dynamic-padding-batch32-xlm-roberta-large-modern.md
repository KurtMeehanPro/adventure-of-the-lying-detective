# Mac Studio MPS, XLM-RoBERTa large, batch size 32, 20 epochs — September 28, 2026

Model: `FacebookAI/xlm-roberta-large`

Hardware: Mac Studio

Configuration: batch size 32, 20 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: completed with early stopping after epoch 7

## Training log

```text
2026-09-28 17:12:18 | Training on mps, 303 batches/epoch, 20 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-large/run-20260928-171218-ri_fmq3z/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-28 17:15:30 | Epoch 1/20: training loss = 1.1098, validation loss = 1.0980, validation accuracy = 34.34%
Saved best checkpoint: epoch 1, validation loss=1.0980
2026-09-28 17:18:47 | Epoch 2/20: training loss = 1.0999, validation loss = 0.9680, validation accuracy = 52.23%
Saved best checkpoint: epoch 2, validation loss=0.9680
2026-09-28 17:22:02 | Epoch 3/20: training loss = 0.8279, validation loss = 0.5739, validation accuracy = 77.45%
Saved best checkpoint: epoch 3, validation loss=0.5739
2026-09-28 17:25:37 | Epoch 4/20: training loss = 0.5604, validation loss = 0.5204, validation accuracy = 80.79%
Saved best checkpoint: epoch 4, validation loss=0.5204
2026-09-28 17:29:00 | Epoch 5/20: training loss = 0.4233, validation loss = 0.5174, validation accuracy = 80.87%
Saved best checkpoint: epoch 5, validation loss=0.5174
2026-09-28 17:32:27 | Epoch 6/20: training loss = 0.3045, validation loss = 0.5689, validation accuracy = 80.96%
No significant validation-loss improvement: 1 consecutive epoch(s)
2026-09-28 17:36:03 | Epoch 7/20: training loss = 0.2124, validation loss = 0.6359, validation accuracy = 80.34%
No significant validation-loss improvement: 2 consecutive epoch(s)
Early stopping after epoch 7 (patience=2)
Training complete. Restored best epoch 5: validation loss=0.5174, validation accuracy=80.87%; /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-large/run-20260928-171218-ri_fmq3z/best.pt
```
