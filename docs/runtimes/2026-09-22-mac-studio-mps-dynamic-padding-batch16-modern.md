# Mac Studio MPS, batch size 16 — September 22, 2026

Model: `FacebookAI/xlm-roberta-base`

Hardware: Mac Studio

Configuration: batch size 16, 5 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: intentionally stopped

## Training log

```text
batch size 16
###
2026-09-22 22:03:36 | Training on mps, 606 batches/epoch, 5 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-220336-qer3gxkw/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-22 22:05:01 | Epoch 1/5: training loss = 1.0990, validation loss = 1.0841, validation accuracy = 41.84%
Saved best checkpoint: epoch 1, validation loss=1.0841
2026-09-22 22:05:01 | Processing batch 0/606
```
