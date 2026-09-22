"""Protect the training decisions made by watson_model_helpers.fine_tune.

These tests call the actual fine_tune function with a small model whose validation
losses follow a supplied sequence. Controlling those losses makes the expected
stopping epoch and best checkpoint known in advance. The tests verify patience
and early stopping, restoration of the lowest-loss checkpoint, separation of
checkpoints between runs, default and custom weight decay, and rejection of the
invalid patience and minimum-improvement settings covered below.

Keep this suite after the initial implementation: later edits can accidentally
change when training stops, which weights are returned, or how checkpoints are
saved. Run it after changing fine_tune or the helpers it uses, especially its
stopping rules, optimizer setup, checkpoint handling, or returned metadata.

The shared checks confirm that the returned model matches the selected epoch and
that the checkpoint records the expected settings.

From the repository root, activate the project's Python environment (with its
required dependencies installed), then run this portable discovery command:

    python -m unittest discover -s tests -p 'test_training_control.py' -v

The suite uses a tiny model on the CPU, needs no model or dataset downloads, and
writes checkpoints to temporary directories that are cleaned up after each test.
"""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import watson_model_helpers as helpers


class ScriptedLossModel(torch.nn.Module):
    """Supply predictable validation losses while allowing real optimizer steps.

    A single trainable weight and an epoch marker let the tests verify that
    fine_tune restores both parameters and saved model buffers. Validation also
    records the weight at each epoch so restoration can be checked directly.
    """
    def __init__(self, losses):
        """Store ordered validation losses and initialize the weight and marker.

        Each validation call consumes one entry from losses. The test loader has
        one batch per epoch, so the marker counts completed training epochs.
        """
        super().__init__()
        self.weight = torch.nn.Parameter(torch.tensor(1.0))
        self.register_buffer("epoch_marker", torch.tensor(0))
        self.losses = losses
        self.validation_weights = []

    def forward(self, labels):
        """Return a trainable loss or the next scripted validation result.

        Training increments the marker and uses the squared weight as its loss.
        Validation records the weight and returns fixed class-zero predictions;
        labels are accepted to match fine_tune's calling convention but unused.
        """
        if self.training:
            self.epoch_marker.add_(1)
            return SimpleNamespace(loss=self.weight.square())
        self.validation_weights.append(self.weight.detach().clone())
        loss = self.losses[len(self.validation_weights) - 1]
        return SimpleNamespace(loss=torch.tensor(loss), logits=torch.tensor([[1.0, 0.0]]))


class TrainingControlTests(unittest.TestCase):
    """Exercise fine_tune's stopping, checkpoint, and configuration behavior.

    Each test uses temporary checkpoint storage and a one-example loader to make
    the expected epoch decisions easy to inspect without a real dataset.
    """
    def setUp(self):
        """Create isolated checkpoint storage and a single class-zero example.

        Register cleanup so temporary files are removed even if a test fails.
        """
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.loader = torch.utils.data.DataLoader([{"labels": torch.tensor(0)}], batch_size=1)

    def run_case(self, losses, patience=2, min_delta=0.0, **training_options):
        """Run fine_tune with scripted losses and verify shared checkpoint rules.

        The loss sequence sets the maximum epoch count; patience and min_delta
        control stopping, and extra training options are forwarded to fine_tune.
        Force CPU execution and capture printed output for the caller's checks.

        Verify restored weights and buffers, evaluation mode, float32 weights,
        saved metrics and configuration, CPU checkpoint weights, a single saved
        file for the run, and the restoration message. Return the model, selected
        checkpoint metadata, and captured output for test-specific assertions.
        """
        model = ScriptedLossModel(losses)
        output = io.StringIO()
        with patch.object(helpers, "_training_device", return_value=torch.device("cpu")), contextlib.redirect_stdout(output):
            result = helpers.fine_tune(
                model, self.loader, self.loader, 7.5e-6, len(losses),
                checkpoint_dir=self.root,
                early_stopping_patience=patience, min_delta=min_delta, **training_options,
            )
        selected = result["epoch"]
        self.assertEqual(model.epoch_marker.item(), selected)
        self.assertTrue(torch.equal(model.weight, model.validation_weights[selected - 1]))
        self.assertFalse(model.training)
        self.assertEqual(model.weight.dtype, torch.float32)
        checkpoint = torch.load(result["checkpoint_path"], weights_only=True, map_location="cpu")
        self.assertEqual(checkpoint["epoch"], selected)
        self.assertEqual(checkpoint["validation_accuracy"], 1.0)
        self.assertEqual(checkpoint["config"]["max_epochs"], len(losses))
        self.assertEqual(checkpoint["config"]["total_steps"], len(losses))
        self.assertEqual(checkpoint["config"]["warmup_steps"], max(1, int(len(losses) * 0.1)))
        self.assertEqual(checkpoint["config"]["batch_size"], 1)
        self.assertEqual(checkpoint["config"]["learning_rate"], 7.5e-6)
        self.assertEqual(checkpoint["config"]["weight_decay"], training_options.get("weight_decay", 0.01))
        self.assertEqual(checkpoint["config"]["torch_initial_seed"], torch.initial_seed())
        self.assertEqual(checkpoint["model_state_dict"]["weight"].device.type, "cpu")
        self.assertEqual(list(Path(result["checkpoint_path"]).parent.iterdir()), [Path(result["checkpoint_path"])])
        self.assertIn(f"Restored best epoch {selected}", output.getvalue())
        return model, result, output.getvalue()

    def test_default_and_custom_weight_decay(self):
        """Verify default and explicit weight decay reach AdamW, metadata, and logs."""
        for options, expected in [({}, 0.01), ({"weight_decay": 0.05}, 0.05)]:
            with self.subTest(options=options), patch.object(
                helpers.torch.optim, "AdamW", wraps=torch.optim.AdamW
            ) as optimizer:
                _, result, log = self.run_case([2., 1.], **options)
                self.assertEqual(optimizer.call_args.kwargs["weight_decay"], expected)
                self.assertEqual(result["config"]["weight_decay"], expected)
                self.assertIn(f"weight decay {expected}", log)

    def test_stop_at_patience_boundary_and_restore(self):
        """Stop after two worsening epochs and restore epoch two's best weights.

        The later scripted improvement must remain unreached once patience runs
        out at epoch four.
        """
        model, result, log = self.run_case([3., 2., 2.5, 2.6, 1.])
        self.assertEqual(len(model.validation_weights), 4)
        self.assertEqual(result["epoch"], 2)
        self.assertEqual(result["validation_loss"], 2.)
        self.assertIn("Early stopping after epoch 4", log)

    def test_improvement_resets_patience(self):
        """Reset the patience counter when epoch three improves validation loss.

        Two subsequent worsening epochs stop the run at epoch five, with epoch
        three retained as the best checkpoint.
        """
        model, result, log = self.run_case([3., 4., 2., 3., 4., 1.])
        self.assertEqual(len(model.validation_weights), 5)
        self.assertEqual(result["epoch"], 3)
        self.assertIn("Early stopping after epoch 5", log)

    def test_improving_run_reaches_max_epochs(self):
        """Run all requested epochs when every validation loss improves."""
        model, result, log = self.run_case([5., 4., 3., 2., 1.])
        self.assertEqual(len(model.validation_weights), 5)
        self.assertEqual(result["epoch"], 5)
        self.assertNotIn("Early stopping after", log)

    def test_disabled_stopping_still_restores_best(self):
        """With patience disabled, finish all epochs and restore the best first epoch."""
        model, result, log = self.run_case([1., 2., 3., 4., 5.], patience=None)
        self.assertEqual(len(model.validation_weights), 5)
        self.assertEqual(result["epoch"], 1)
        self.assertNotIn("Early stopping after", log)

    def test_ties_do_not_improve(self):
        """Count equal losses toward patience and preserve the first best epoch."""
        model, result, _ = self.run_case([1., 1., 1., 0.5])
        self.assertEqual(len(model.validation_weights), 3)
        self.assertEqual(result["epoch"], 1)

    def test_min_delta_still_saves_absolute_best(self):
        """Save smaller losses even when their gains do not reset patience.

        With min_delta set to 0.2, losses of 0.95 and 0.9 do not sufficiently
        improve on 1.0 to extend training. Stop at epoch three but restore its
        0.9 checkpoint because it is the lowest loss actually reached.
        """
        model, result, _ = self.run_case([1., 0.95, 0.9, 0.5], min_delta=0.2)
        self.assertEqual(len(model.validation_weights), 3)
        self.assertEqual(result["epoch"], 3)

    def test_run_directories_do_not_collide(self):
        """Give successive runs distinct paths and leave the first checkpoint intact."""
        _, first, _ = self.run_case([1.])
        first_bytes = Path(first["checkpoint_path"]).read_bytes()
        _, second, _ = self.run_case([2.])
        self.assertNotEqual(first["checkpoint_path"], second["checkpoint_path"])
        self.assertEqual(Path(first["checkpoint_path"]).read_bytes(), first_bytes)

    def test_invalid_settings_fail_before_artifacts(self):
        """Reject zero patience and negative or NaN min_delta without creating files."""
        for kwargs in [{"early_stopping_patience": 0}, {"min_delta": -1}, {"min_delta": float("nan")}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                helpers.fine_tune(ScriptedLossModel([1.]), self.loader, self.loader, 7.5e-6, 1,
                                  checkpoint_dir=self.root, **kwargs)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
