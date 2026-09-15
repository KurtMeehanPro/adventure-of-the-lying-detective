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
- `docs/` contains investigation and runtime performance documentation.

## Setup

Choose one requirements file per separate virtual environment. Install the
specified Python version first, then create and activate the environment with
that interpreter; pip installs the packages, not Python itself.

### Recommended: Apple silicon

Use **Python 3.14.7** with [requirements.txt](requirements.txt):

```bash
python -m pip install -r requirements.txt
```

This setup was validated on an Apple silicon MacBook Air with PyTorch 2.14.0.
XLM-R completed a full training epoch with batch size 4 and dynamic padding,
with training loss 1.1052.

### Intel Mac compatibility

Use **Python 3.12** with
[requirements-macos-intel.txt](requirements-macos-intel.txt):

```bash
python -m pip install -r requirements-macos-intel.txt
```

This preserves the previous dependency pins, including PyTorch 2.2.2, whose
official packages support Intel Macs. A CPU baseline exists. MPS training with
the current dynamic padding has not been validated on the Intel iMac; the
fixed-padding workaround was demonstrated on the MacBook Air only.

### Kaggle authentication

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
