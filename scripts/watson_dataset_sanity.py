"""Download and run sanity checks on the Watson competition dataset."""

# standard library

# third-party

# local
from watson_dataset_config import LABEL_NAMES
from watson_dataset_helpers import (
    build_dataset_overview,
    load_datasets,
    validate_dataset_columns,
)


def main() -> None:
    """Validate files and print a compact dataset profile."""
    datasets = load_datasets()
    validate_dataset_columns(datasets)

    train = datasets["train"]
    test = datasets["test"]
    submission = datasets["sample_submission"]

    labels = set(train["label"].unique())
    if labels != set(LABEL_NAMES):
        raise ValueError(f"Unexpected training labels: {sorted(labels)}")
    if len(test) != len(submission):
        raise ValueError("Test and sample-submission row counts do not match.")
    if not test["id"].equals(submission["id"]):
        raise ValueError("Test and sample-submission IDs are not aligned.")

    print("\nDataset overview")
    print(build_dataset_overview(datasets).to_string())
    print("\nTraining labels")
    print(train["label"].map(LABEL_NAMES).value_counts().to_string())
    print("\nTraining languages")
    print(train["language"].value_counts().to_string())
    print("\nTest languages")
    print(test["language"].value_counts().to_string())
    print("\nKaggleHub download and data validation passed.")


if __name__ == "__main__":
    main()
