# Mac Studio MPS, batch size 32, 20 epochs — September 22, 2026

Model: `FacebookAI/xlm-roberta-base`

Hardware: Mac Studio

Configuration: batch size 32, 20 configured epochs, learning rate `7.5e-06`, weight decay `0.01`, FP32 training precision, FP32 validation precision, linear warmup 10%

Status: completed with early stopping after epoch 6

## Training log

```text
batch size 32
###
2026-09-22 23:26:00 | Training on mps, 303 batches/epoch, 20 epochs, learning rate 7.5e-06, weight decay 0.01, training precision FP32; validation precision FP32
Best checkpoint: /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-232600-r2g7cj77/best.pt
Early stopping: patience=2, min_delta=0.0
2026-09-22 23:27:10 | Epoch 1/20: training loss = 1.1044, validation loss = 1.0986, validation accuracy = 34.46%
Saved best checkpoint: epoch 1, validation loss=1.0986
2026-09-22 23:28:18 | Epoch 2/20: training loss = 1.0612, validation loss = 0.9210, validation accuracy = 58.70%
Saved best checkpoint: epoch 2, validation loss=0.9210
2026-09-22 23:29:25 | Epoch 3/20: training loss = 0.8465, validation loss = 0.7355, validation accuracy = 68.63%
Saved best checkpoint: epoch 3, validation loss=0.7355
2026-09-22 23:30:34 | Epoch 4/20: training loss = 0.6958, validation loss = 0.7110, validation accuracy = 70.49%
Saved best checkpoint: epoch 4, validation loss=0.7110
2026-09-22 23:31:43 | Epoch 5/20: training loss = 0.5790, validation loss = 0.7243, validation accuracy = 71.76%
No significant validation-loss improvement: 1 consecutive epoch(s)
2026-09-22 23:32:51 | Epoch 6/20: training loss = 0.4852, validation loss = 0.7598, validation accuracy = 72.38%
No significant validation-loss improvement: 2 consecutive epoch(s)
Early stopping after epoch 6 (patience=2)
Training complete. Restored best epoch 4: validation loss=0.7110, validation accuracy=70.49%; /Users/KurtMeehanPro/Documents/code/git/adventure-of-the-lying-detective/data/checkpoints/xlm-roberta-base/run-20260922-232600-r2g7cj77/best.pt
```
