"""Project-specific configuration for the Watson competition dataset."""

# standard library
from pathlib import Path

# third-party

# local

# constants
COMPETITION = "contradictory-my-dear-watson"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
FILES = {
    "train": DATA_DIR / "train.csv",
    "test": DATA_DIR / "test.csv",
    "sample_submission": DATA_DIR / "sample_submission.csv",
}
TRAIN_COLUMNS = {"id", "premise", "hypothesis", "lang_abv", "language", "label"}
TEST_COLUMNS = TRAIN_COLUMNS - {"label"}
SUBMISSION_COLUMNS = {"id", "prediction"}
LABEL_NAMES = {
    0: "entailment",
    1: "neutral",
    2: "contradiction",
}

