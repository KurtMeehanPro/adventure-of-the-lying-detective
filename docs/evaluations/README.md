# Model evaluations

This page compares the validation performance of XLM-RoBERTa base and XLM-RoBERTa large after fine-tuning on the Watson training examples. Both models used the same validation split and overall training approach and settings.

## Results summary

| Model | Validation loss | Validation accuracy | Macro F1 |
| --- | ---: | ---: | ---: |
| XLM-RoBERTa base | 0.7267 | 70.40% | 0.7020 |
| XLM-RoBERTa large | 0.5174 | 80.87% | 0.8090 |

Using XLM-RoBERTa large improved validation accuracy by **10.47 percentage points** and macro F1 by **0.1070** over XLM-RoBERTa base.

That is a HUGE improvement using a drop-in replacement of the pre-trained model. That's encouraging from the perspective of training approach. My approach works well. A more powerful pre-trained model would likely be even more accurate.

TODO: Add the Kaggle accuracy score. Kaggle reports only the overall accuracy score and does not provide the test labels needed to calculate additional evaluation metrics. The remainder of this report focuses on validation performance.

## Per-class results

| Class | Base precision | Large precision | Base recall | Large recall | Base F1 | Large F1 | Support |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Entailment | 0.7484 | 0.8628 | 0.6902 | 0.7751 | 0.7181 | 0.8166 | 836 |
| Neutral | 0.6801 | 0.7206 | 0.6293 | 0.8031 | 0.6537 | 0.7596 | 777 |
| Contradiction | 0.6859 | 0.8529 | 0.7897 | 0.8487 | 0.7341 | 0.8508 | 813 |

## Findings

- XLM-RoBERTa large improved precision, recall, and F1 for all three classes.
- Neutral was the weakest class for the base model. The large model increased neutral recall from 0.6293 to 0.8031 and neutral F1 from 0.6537 to 0.7596.
- Contradiction had the largest F1 improvement, increasing from 0.7341 to 0.8508.
- For both models, training loss continued to fall after validation loss stopped improving, which is consistent with overfitting.
- Checkpoints were selected using the lowest validation loss, not the highest validation accuracy observed during training.

## Evaluation approach

The comparison used:

- the same premise-grouped, label-stratified training and validation split
- 9,694 training examples and 2,426 validation examples
- a batch size of 32 with dynamic padding
- a learning rate of `7.5e-6` and weight decay of `0.01`
- FP32 training and validation
- a maximum of 20 epochs
- early stopping after two consecutive epochs without lower validation loss
- restoration of the checkpoint with the lowest validation loss

The pretrained checkpoint was the only intentional difference: `FacebookAI/xlm-roberta-base` for the base run and `FacebookAI/xlm-roberta-large` for the large run. Neither checkpoint had already been fine-tuned on SNLI, MNLI, ANLI, or XNLI. See the [leaderboard models and dataset leakage investigation](../investigations/leaderboard-models-and-dataset-leakage.md) for why that constraint matters.

## Detailed outputs

The evaluation sections in the notebooks include training curves, confusion matrices, per-class metrics, and precision-recall curves:

- [Notebook 2 — XLM-RoBERTa base](../../notebooks/02_pytorch_xlm_roberta_base.ipynb)
- [Notebook 4 — XLM-RoBERTa large](../../notebooks/04_pytorch_xlm_roberta_large.ipynb)

The [training log](training-log.txt) preserves results from earlier experiments, including learning-rate trials, linear warmup, a BF16 trial, and checkpoint selection.

Training runtime comparisons and individual runtime logs are documented separately in the [runtime performance documentation](../runtimes/README.md).

## Further notes

- These results come from one validation split. It's possible other splits would produce different results.
