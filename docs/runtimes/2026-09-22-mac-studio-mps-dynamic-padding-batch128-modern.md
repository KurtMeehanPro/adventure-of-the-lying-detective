# Mac Studio MPS, batch size 128 — September 22, 2026

Model: `FacebookAI/xlm-roberta-base`

Hardware: Mac Studio

Configuration: batch size 128, 5 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: completed

## Training log

```text
batch size 128
###
2026-09-22 22:19:16 | Training on mps, 76 batches/epoch, 5 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-221916-q0ln63kd/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-22 22:20:25 | Epoch 1/5: training loss = 1.1033, validation loss = 1.0980, validation accuracy = 34.46%
Saved best checkpoint: epoch 1, validation loss=1.0980
2026-09-22 22:21:38 | Epoch 2/5: training loss = 1.0906, validation loss = 1.0714, validation accuracy = 44.39%
Saved best checkpoint: epoch 2, validation loss=1.0714
2026-09-22 22:22:51 | Epoch 3/5: training loss = 0.9731, validation loss = 0.8282, validation accuracy = 63.93%
Saved best checkpoint: epoch 3, validation loss=0.8282
2026-09-22 22:24:14 | Epoch 4/5: training loss = 0.8292, validation loss = 0.7523, validation accuracy = 68.30%
Saved best checkpoint: epoch 4, validation loss=0.7523
2026-09-22 22:25:31 | Epoch 5/5: training loss = 0.7282, validation loss = 0.7368, validation accuracy = 69.50%
Saved best checkpoint: epoch 5, validation loss=0.7368
Training complete. Restored best epoch 5: validation loss=0.7368, validation accuracy=69.50%; /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-221916-q0ln63kd/best.pt
```
