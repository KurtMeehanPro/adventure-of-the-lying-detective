# The Adventure of the Lying Detective

A multilingual natural-language inference project for Kaggle's
[Contradictory, My Dear Watson](https://www.kaggle.com/competitions/contradictory-my-dear-watson)
competition.

The task is to classify the relationship between a premise and a hypothesis as
entailment, neutral, or contradiction across 15 languages. Submissions are
evaluated using classification accuracy.

## Project layout

- `data/raw/` contains competition files downloaded from Kaggle and is excluded
  from Git.
- `notebooks/` contains numbered exploration, modeling, and submission
  notebooks.
- `scripts/` contains reusable dataset configuration and validation code.

## Setup

Python 3.12 is used for local development. Create and activate a virtual
environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Authenticate with Kaggle and accept the competition rules before downloading
the data.

## Dataset sanity check

Run:

```bash
python scripts/watson_dataset_sanity.py
```

The script:
- downloads missing competition files through KaggleHub into `data/raw`
- verifies the expected train, test, and sample-submission schemas,
- reports dataset sizes, languages, label counts, missing values, and duplicate IDs.

## Planned workflow

1. Explore class balance, language coverage, text lengths, and duplicate pairs.
2. Establish a reproducible multilingual baseline.
3. Fine-tune and validate a multilingual transformer without leaking examples
   across folds.
4. Analyze performance by language and class.
5. Train the selected model and generate a validated Kaggle submission.

