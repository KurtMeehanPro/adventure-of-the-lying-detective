# The Adventure of the Lying Detective

## Overview

A multilingual natural-language inference project for Kaggle's
[Contradictory, My Dear Watson](https://www.kaggle.com/competitions/contradictory-my-dear-watson)
competition.

excerpt from the Kaggle challenge:
> “If you have two sentences, there are three ways they could be related: one could entail the other, one could contradict the other, or they could be unrelated. Natural Language Inferencing (NLI) is a popular Natural Language Processing (NLP) problem that involves determining how pairs of sentences (consisting of a premise and a hypothesis) are related.”

Definitions:
- entailment: the hypothesis MUST be true given the premise
- contradiction: the hypothesis COULD NOT be true given the premise
- neutral: neither, not enough info, unrelated

The task is to classify the relationship between a premise and a hypothesis as
entailment, neutral, or contradiction across 15 languages. Submissions are
evaluated using classification accuracy.

<br><br>

## Results Summary

### Validation results

Using the same validation split and overall training approach and settings, XLM-RoBERTa large substantially outperformed XLM-RoBERTa base.

| Model | Validation accuracy | Macro F1 |
| --- | ---: | ---: |
| XLM-RoBERTa base | 70.40% | 0.7020 |
| XLM-RoBERTa large | 80.87% | 0.8090 |

The Large model improved validation accuracy by **10.47 percentage points** and improved precision, recall, and F1 across all three classes. This was especially encouraging because the pretrained checkpoint was the only intentional difference between the two runs.

See the [model evaluation report](docs/evaluations/README.md) for per-class metrics, confusion matrices, precision-recall curves, methodology, and detailed findings.

### Kaggle test result

**Accuracy: TBD**

Kaggle reports only overall accuracy and does not provide the test labels needed to calculate additional evaluation metrics.

<br><br>

## Documentation

- **Project README** — The project's top-level README, the document you're reading right now.
- [Model evaluations](docs/evaluations/README.md) — Compares XLM-RoBERTa base and large using validation accuracy, per-class metrics, confusion matrices, and precision-recall curves.
- [Training runtime comparisons](docs/runtimes/README.md) — Compares training performance across hardware, model sizes, batch sizes, padding strategies, and software environments.
- [Leaderboard models and dataset leakage](docs/investigations/leaderboard-models-and-dataset-leakage.md) — Discusses the use of larger models and previously fine-tuned checkpoints, including the dataset overlap that could introduce leakage.
- [MPS memory investigation](docs/investigations/mps-memory.md) — Documents the MPS memory issue encountered during training and the changes that made training successful.

<br><br>

## Layout

- `data/raw/` contains competition files downloaded from Kaggle and is excluded from Git.
- `data/checkpoints/` contains trained/saved models and is excluded from Git.
- `docs/` — See the [Documentation](#documentation) section above.
- `notebooks/` contains numbered exploration, modeling, data-overlap investigation, and submission notebooks.
- `scripts/` contains reusable dataset configuration, loading, validation, and model-training helpers.
- `tests/` tests to ensure functionality.

<br><br>

## Setup

- Choose one requirements file per separate virtual environment
- Install the specified Python version
- create and activate the environment with that interpreter
- pip install the packages
- Authenticate with Kaggle
- Authenticate with Hugging Face

### Recommended: Apple silicon

Use **Python 3.14.7** with [requirements.txt](requirements.txt):

```bash
python -m pip install -r requirements.txt
```

### Recommended only if you are a glutton for punishment: Intel Mac compatibility

Use **Python 3.12.3 or 3.12.10** (both were used in this project) with
[requirements-macos-intel.txt](requirements-macos-intel.txt):

```bash
python -m pip install -r requirements-macos-intel.txt
```

### Kaggle authentication

Authenticate with Kaggle and accept the competition rules before downloading
the data.

### Hugging Face authentication

Authenticate with Hugging Face in order to use the Hugging Face calls that are a part of the notebooks.

<br><br>

## Dataset sanity check

Run:

```bash
python scripts/watson_dataset_sanity.py
```

The script:
- downloads missing competition files through KaggleHub into `data/raw`
- verifies the expected train, test, and sample-submission schemas,
- reports dataset sizes, languages, label counts, missing values, and duplicate IDs.
