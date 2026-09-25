# Mac Studio MPS, batch size 64 — September 22, 2026

Model: `FacebookAI/xlm-roberta-base`

Hardware: Mac Studio

Configuration: batch size 64, 5 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: completed

## Training log

```text
batch size 64
###
2026-09-22 22:11:19 | Training on mps, 152 batches/epoch, 5 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-221118-ytvsvgza/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-22 22:12:25 | Epoch 1/5: training loss = 1.1027, validation loss = 1.0974, validation accuracy = 36.03%
Saved best checkpoint: epoch 1, validation loss=1.0974
2026-09-22 22:13:30 | Epoch 2/5: training loss = 1.0841, validation loss = 1.0238, validation accuracy = 51.40%
Saved best checkpoint: epoch 2, validation loss=1.0238
2026-09-22 22:14:36 | Epoch 3/5: training loss = 0.9239, validation loss = 0.7843, validation accuracy = 66.03%
Saved best checkpoint: epoch 3, validation loss=0.7843
2026-09-22 22:15:42 | Epoch 4/5: training loss = 0.7752, validation loss = 0.7435, validation accuracy = 69.46%
Saved best checkpoint: epoch 4, validation loss=0.7435
2026-09-22 22:16:48 | Epoch 5/5: training loss = 0.6729, validation loss = 0.7190, validation accuracy = 70.98%
Saved best checkpoint: epoch 5, validation loss=0.7190
Training complete. Restored best epoch 5: validation loss=0.7190, validation accuracy=70.98%; /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-221118-ytvsvgza/best.pt
```
