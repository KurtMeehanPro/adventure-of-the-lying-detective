# Training evaluations

The [training log](training-log.txt) preserves XLM-R training and
validation results, including:
- learning-rate trials
- adding a linear warmup
- a BF16 trial
- checkpoint selection

Some notes and findings:
- Falling training loss alongside rising validation loss in the later completed runs is consistent with overfitting
- The log does not establish the causes of run-to-run variation
- The log does not demonstrate a benefit from BF16
- These are validation results. Separate test-set performance remains to be done
