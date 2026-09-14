"""Load the Watson competition datasets using the existing dataset helper."""
# standard library
from datetime import datetime

# third-party
import torch
from sklearn.model_selection import StratifiedGroupKFold
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding

# local


def split_training_data(training_data):
    """Take one approximately 20% holdout, balancing labels and grouping premises."""
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    train_index, validation_index = next(splitter.split(
        training_data, y=training_data["label"], groups=training_data["premise"]
    ))
    return training_data.iloc[train_index], training_data.iloc[validation_index]


def load_model_and_tokenizer():
    """Load XLM-RoBERTa base with a three-label head and its matching tokenizer."""
    model_name = "FacebookAI/xlm-roberta-base"
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, clean_up_tokenization_spaces=False)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=3)
    except OSError as error:
        raise RuntimeError(f"Failed to load the model or tokenizer for {model_name}.") from error
    return model, tokenizer


def tokenize_data(data, tokenizer):
    """Tokenize premise–hypothesis pairs without padding, retaining their labels."""
    encodings = tokenizer(
        data["premise"].tolist(),
        data["hypothesis"].tolist(),
        truncation=True,
        padding=False,
    )
    encodings["labels"] = data["label"].tolist()
    return encodings


class EncodedDataset(Dataset):
    """Expose one encoded example and its label at a time."""

    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings["labels"])

    def __getitem__(self, index):
        return {key: values[index] for key, values in self.encodings.items()}


def make_loaders(training_encodings, validation_encodings, tokenizer, batch_size):
    """Pad each batch to its longest example and return PyTorch tensors."""
    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")
    training_loader = DataLoader(
        EncodedDataset(training_encodings), batch_size=batch_size,
        shuffle=True, collate_fn=collator,
    )
    validation_loader = DataLoader(
        EncodedDataset(validation_encodings), batch_size=batch_size,
        shuffle=False, collate_fn=collator,
    )
    return training_loader, validation_loader


def fine_tune(model, training_loader, learning_rate, epochs):
    """Update the model in place and print average training loss each epoch."""
    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available()
        else "cpu"
    )
    # device = torch.device("cpu")
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        total_examples = 0

        for batch_idx, batch in enumerate(training_loader):
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S} | Processing batch {batch_idx}/{len(training_loader)}", flush=True)
            if batch_idx % 100 == 0:
                print(
                    f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
                    f"Processing batch {batch_idx}/{len(training_loader)}",
                    flush=True,
                )

            ## Move the batch to the same device as the model
            batch = {key: value.to(device) for key, value in batch.items()}

            optimizer.zero_grad()
            loss = model(**batch).loss  
            loss.backward()
            optimizer.step()
            batch_size = batch["labels"].size(0)
            total_loss += loss.item() * batch_size
            total_examples += batch_size
        print(f"Epoch {epoch + 1}/{epochs}: training loss = {total_loss / total_examples:.4f}")
        # torch.mps.empty_cache()
