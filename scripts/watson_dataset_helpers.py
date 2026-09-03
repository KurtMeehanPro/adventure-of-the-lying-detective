"""Helpers for acquiring and validating the Watson competition dataset."""

# standard library
from collections.abc import Mapping
from pathlib import Path

# third-party
import kagglehub
import pandas as pd

# local
from watson_dataset_config import (
    COMPETITION,
    DATA_DIR,
    FILES,
    PROJECT_ROOT,
    SUBMISSION_COLUMNS,
    TEST_COLUMNS,
    TRAIN_COLUMNS,
)


def ensure_dataset_downloaded() -> None:
    """Download the Kaggle competition files when any expected file is absent."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    display_path = f"(project_root)/{DATA_DIR.relative_to(PROJECT_ROOT)}"

    if all(path.is_file() for path in FILES.values()):
        print(f"Kaggle files already present; using: {display_path}")
        return

    kagglehub.competition_download(COMPETITION, output_dir=str(DATA_DIR))
    _normalize_downloaded_files()
    print(f"KaggleHub download path: {display_path}")


def _normalize_downloaded_files() -> None:
    """Move expected files from a nested download directory into data/raw."""
    for expected_path in FILES.values():
        if expected_path.is_file():
            continue

        matches = [
            path
            for path in DATA_DIR.rglob(expected_path.name)
            if path.is_file() and path != expected_path
        ]
        if len(matches) == 1:
            matches[0].replace(expected_path)


def load_datasets() -> dict[str, pd.DataFrame]:
    """Download, validate, and return fresh competition DataFrames."""

    try:
        ensure_dataset_downloaded()
    except Exception as e:
        raise RuntimeError("Failed to download and normalize the dataset.") from e

    missing_files = [path for path in FILES.values() if not path.is_file()]
    if missing_files:
        missing = ", ".join(str(path) for path in missing_files)
        raise FileNotFoundError(f"Expected Kaggle files were not found: {missing}")

    competition_dfs = {name: pd.read_csv(path) for name, path in FILES.items()}
    return competition_dfs


def build_dataset_overview(
    datasets: Mapping[str, pd.DataFrame],
) -> pd.DataFrame:
    """Summarize shapes, missing values, and duplicate IDs by dataset."""
    rows = []
    for name, data in datasets.items():
        rows.append(
            {
                "dataset": name,
                "rows": len(data),
                "columns": data.shape[1],
                "missing_values": int(data.isna().sum().sum()),
                "duplicate_ids": int(data["id"].duplicated().sum()),
            }
        )
    return pd.DataFrame(rows).set_index("dataset")


def validate_columns(data: pd.DataFrame, expected: set[str], name: str) -> None:
    """Raise a clear error when a dataset's columns differ from expectations."""
    actual = set(data.columns)
    if actual != expected:
        # which columns were expected but not found in the actual dataset
        missing = sorted(expected - actual)

        # which columns were found in the actual dataset but not expected
        unexpected = sorted(actual - expected)

        msg1 = "columns were expected but not found"
        msg2 = "columns were found but not expected"
        raise ValueError(
            f"Unexpected {name} schema; {msg1}: {missing}; {msg2}: {unexpected}"
        )


def validate_dataset_columns(datasets: Mapping[str, pd.DataFrame]) -> None:
    """Validate the schemas of all competition datasets."""
    validate_columns(datasets["train"], TRAIN_COLUMNS, "training data")
    validate_columns(datasets["test"], TEST_COLUMNS, "test data")
    validate_columns(
        datasets["sample_submission"],
        SUBMISSION_COLUMNS,
        "sample submission",
    )
