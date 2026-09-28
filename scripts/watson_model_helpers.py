"""Load the Watson competition datasets using the existing dataset helper."""
# standard library
from datetime import datetime
import math
from pathlib import Path
from tempfile import mkdtemp

# third-party
import torch
from sklearn.model_selection import StratifiedGroupKFold
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding
from transformers import get_constant_schedule_with_warmup

# local


def split_training_data(training_data):
    """Take one approximately 20% holdout, balancing labels and grouping premises."""
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    train_index, validation_index = next(splitter.split(
        training_data, y=training_data["label"], groups=training_data["premise"]
    ))
    return training_data.iloc[train_index], training_data.iloc[validation_index]


def load_model_and_tokenizer(model_name=None):
    """Load a pretrained model with a three-label head and its matching tokenizer."""
    if model_name is None:
        raise ValueError("Model name is required when calling load_model_and_tokenizer.")

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
    # collator = DataCollatorWithPadding(tokenizer=tokenizer,
    #                                    return_tensors="pt",
    #                                    padding="max_length")
    collator = DataCollatorWithPadding(tokenizer=tokenizer,
                                       return_tensors="pt")
    training_loader = DataLoader(
        EncodedDataset(training_encodings), batch_size=batch_size,
        shuffle=True, collate_fn=collator,
    )
    validation_loader = DataLoader(
        EncodedDataset(validation_encodings), batch_size=batch_size,
        shuffle=False, collate_fn=collator,
    )
    return training_loader, validation_loader


def _training_device():
    """Use the same device selection for the support check and training."""
    return torch.device(
        "cuda" if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available()
        else "cpu"
    )


def check_bf16_support():
    """Raise clearly if BF16 forward/backward is unsupported; do not consume RNG."""
    device = _training_device()
    try:
        probe = torch.ones((2, 2), device=device, dtype=torch.float32, requires_grad=True)
        with torch.autocast(device_type=device.type, dtype=torch.bfloat16):
            probe_output = probe @ probe
            probe_loss = probe_output.float().sum()
        if probe_output.dtype != torch.bfloat16:
            raise RuntimeError("Autocast did not produce BF16 output")
        probe_loss.backward()
        del probe, probe_output, probe_loss
    except (RuntimeError, TypeError, NotImplementedError) as error:
        raise RuntimeError(
            f"BF16 autocast is unavailable on {device} with this PyTorch/OS setup. "
            "Set use_bf16=False and validation_use_bf16=False for FP32."
        ) from error


def fine_tune(model, training_loader, validation_loader, learning_rate, epochs,
              use_bf16=False, validation_use_bf16=False, checkpoint_dir=None,
              early_stopping_patience=2, min_delta=0.0, weight_decay=0.01):
    """Train and report loss/accuracy with linear warmup, then constant learning rate.

    Start at zero and reach learning_rate after the first 10% of optimizer steps
    (rounded down, minimum one step), with no learning-rate decay afterward.
    Training and validation forward/loss can independently use BF16 autocast.
    Parameters remain FP32, without gradient scaling.

    Save every strictly lower validation loss in a unique run directory under
    checkpoint_dir (default: data/checkpoints). Restore that best state on return.
    Patience counts epochs without a loss decrease greater than min_delta from
    the last significant improvement; None disables stopping, not checkpointing.
    The warmup horizon always uses the requested maximum epochs.

    best.pt contains CPU model_state_dict and epoch/metrics/training metadata;
    it excludes tokenizer, optimizer, scheduler and RNG state (not resumable).
    Returns the selected checkpoint's metadata and path. Files persist until
    manually removed; each invocation gets a new directory to avoid collisions.

    """
    if epochs < 1 or len(training_loader) == 0 or len(validation_loader) == 0:
        raise ValueError("Training needs positive epochs and nonempty loaders")
    if early_stopping_patience is not None and (
        not isinstance(early_stopping_patience, int) or early_stopping_patience < 1
    ):
        raise ValueError("early_stopping_patience must be a positive integer or None")
    if not math.isfinite(min_delta) or min_delta < 0:
        raise ValueError("min_delta must be finite and nonnegative")
    checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir is not None else (
        Path(__file__).resolve().parents[1] / "data" / "checkpoints"
    )
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    run_dir = Path(mkdtemp(prefix=datetime.now().strftime("run-%Y%m%d-%H%M%S-"), dir=checkpoint_dir))
    checkpoint_path = run_dir / "best.pt"
    best_loss = float("inf")
    stopping_best_loss = float("inf")
    epochs_without_improvement = 0
    best_metadata = None

    device = _training_device()
    # device = torch.device("cpu")
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    total_steps = len(training_loader) * epochs
    warmup_steps = max(1, int(total_steps * 0.1))
    scheduler = get_constant_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps,
    )

    print(
        f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
        f"Training on {device}, {len(training_loader)} batches/epoch, {epochs} epochs,"
        f" learning rate {learning_rate}, weight decay {weight_decay},"
        f" training precision {'BF16 mixed' if use_bf16 else 'FP32'};"
        f" validation precision {'BF16 mixed' if validation_use_bf16 else 'FP32'}"
    )

    print(f"Best checkpoint: {checkpoint_path}")
    print(f"Early stopping: patience={early_stopping_patience}, min_delta={min_delta}")

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        total_examples = 0

        for batch_idx, batch in enumerate(training_loader):
            # print(f"{datetime.now():%Y-%m-%d %H:%M:%S} | Processing batch {batch_idx}/{len(training_loader)}", flush=True)
            if batch_idx % 500 == 0:
                print(
                    f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
                    f"Processing batch {batch_idx}/{len(training_loader)}",
                    flush=True,
                )

            ## Move the batch to the same device as the model
            batch = {key: value.to(device) for key, value in batch.items()}

            optimizer.zero_grad()
            with torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=use_bf16):
                loss = model(**batch).loss
            loss.backward()
            optimizer.step()
            scheduler.step()
            batch_size = batch["labels"].size(0)
            total_loss += loss.item() * batch_size
            total_examples += batch_size
        model.eval()
        validation_loss = 0.0
        validation_correct = 0
        validation_examples = 0
        with torch.no_grad():
            for batch in validation_loader:
                batch = {key: value.to(device) for key, value in batch.items()}
                with torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=validation_use_bf16):
                    outputs = model(**batch)
                batch_size = batch["labels"].size(0)
                validation_loss += outputs.loss.item() * batch_size
                validation_correct += (
                    outputs.logits.argmax(dim=-1) == batch["labels"]
                ).sum().item()
                validation_examples += batch_size

        print(
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
            f"Epoch {epoch + 1}/{epochs}: "
            f"training loss = {total_loss / total_examples:.4f}, "
            f"validation loss = {validation_loss / validation_examples:.4f}, "
            f"validation accuracy = {validation_correct / validation_examples:.2%}"
        )
        epoch_loss = validation_loss / validation_examples
        epoch_accuracy = validation_correct / validation_examples
        if not math.isfinite(epoch_loss):
            raise RuntimeError(f"Non-finite validation loss at epoch {epoch + 1}; checkpoint: {checkpoint_path}")
        # Always select the lowest loss, even if its gain is smaller than min_delta.
        if epoch_loss < best_loss:
            best_metadata = {
                "epoch": epoch + 1,
                "validation_loss": epoch_loss,
                "validation_accuracy": epoch_accuracy,
                "config": {
                    "learning_rate": learning_rate,
                    "max_epochs": epochs,
                    "batch_size": getattr(training_loader, "batch_size", None),
                    "total_steps": total_steps,
                    "warmup_steps": warmup_steps,
                    "use_bf16": use_bf16,
                    "validation_use_bf16": validation_use_bf16,
                    "early_stopping_patience": early_stopping_patience,
                    "min_delta": min_delta,
                    "torch_initial_seed": torch.initial_seed(),
                    "weight_decay": optimizer.param_groups[0]["weight_decay"],
                },
            }
            temporary_path = run_dir / "best.pt.tmp"
            torch.save({
                "model_state_dict": {key: value.detach().cpu() for key, value in model.state_dict().items()},
                **best_metadata,
            }, temporary_path)
            temporary_path.replace(checkpoint_path)
            best_loss = epoch_loss
            print(f"Saved best checkpoint: epoch {epoch + 1}, validation loss={epoch_loss:.4f}")

        if epoch_loss < stopping_best_loss - min_delta:
            stopping_best_loss = epoch_loss
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            print(f"No significant validation-loss improvement: {epochs_without_improvement} consecutive epoch(s)")
        if early_stopping_patience is not None and epochs_without_improvement >= early_stopping_patience:
            print(f"Early stopping after epoch {epoch + 1} (patience={early_stopping_patience})")
            break
        # torch.mps.empty_cache()

    # Memory-map CPU tensors rather than keeping a deep copy during training.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True, mmap=True)
    model.load_state_dict(checkpoint["model_state_dict"])
    del checkpoint
    model.eval()
    print(
        f"Training complete. Restored best epoch {best_metadata['epoch']}: "
        f"validation loss={best_metadata['validation_loss']:.4f}, "
        f"validation accuracy={best_metadata['validation_accuracy']:.2%}; {checkpoint_path}"
    )
    return {**best_metadata, "checkpoint_path": str(checkpoint_path)}
