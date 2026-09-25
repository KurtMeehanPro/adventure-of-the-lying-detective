# Mac Studio MPS, batch size 32 — September 22, 2026

Model: `FacebookAI/xlm-roberta-base`

Hardware: Mac Studio

Configuration: batch size 32, 5 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: intentionally stopped

## Training log

```text
batch size 32
###
2026-09-22 22:06:37 | Training on mps, 303 batches/epoch, 5 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-220637-hc21zu0v/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-22 22:07:46 | Epoch 1/5: training loss = 1.1024, validation loss = 1.0949, validation accuracy = 34.46%
Saved best checkpoint: epoch 1, validation loss=1.0949
2026-09-22 22:08:55 | Epoch 2/5: training loss = 0.9743, validation loss = 0.7946, validation accuracy = 65.99%
Saved best checkpoint: epoch 2, validation loss=0.7946
2026-09-22 22:08:56 | Processing batch 0/303
```
