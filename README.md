# The Adventure of the Lying Detective

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


## Project layout

- `data/raw/` contains competition files downloaded from Kaggle and is excluded from Git.
- `data/checkpoints/` contains trained/saved models and is excluded from Git.
- `docs/` contains a memory investigation, runtime performance, and evaluations
- `notebooks/` contains numbered exploration, modeling, and submission notebooks.
- `scripts/` contains reusable dataset configuration and validation code.
- `tests/` tests to ensure functionality.


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

Use **Python 3.12** with
[requirements-macos-intel.txt](requirements-macos-intel.txt):

```bash
python -m pip install -r requirements-macos-intel.txt
```

### Kaggle authentication

Authenticate with Kaggle and accept the competition rules before downloading
the data.

### Hugging Face authentication

Authenticate with Hugging Face in order to use the Hugging Face calls that are a part of the notebooks.

## Dataset sanity check

Run:

```bash
python scripts/watson_dataset_sanity.py
```

The script:
- downloads missing competition files through KaggleHub into `data/raw`
- verifies the expected train, test, and sample-submission schemas,
- reports dataset sizes, languages, label counts, missing values, and duplicate IDs.
