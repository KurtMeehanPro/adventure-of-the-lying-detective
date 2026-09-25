# Mac Studio MPS, batch size 8 — September 22, 2026

Model: `FacebookAI/xlm-roberta-base`

Hardware: Mac Studio

Configuration: batch size 8, 5 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: intentionally stopped after epoch 1.

## Training log

```text
batch size 8
###
2026-09-22 22:00:44 | Training on mps, 1212 batches/epoch, 5 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-220044-fbzmsbom/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-22 22:02:44 | Epoch 1/5: training loss = 1.0954, validation loss = 1.0593, validation accuracy = 47.90%
Saved best checkpoint: epoch 1, validation loss=1.0593
>>> stopped intentionally
```
