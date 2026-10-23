"""The public evaluation uses fixed fictional cases and no model calls."""
import json
from pathlib import Path
import tempfile
import unittest

from atlas_context.evaluation import TASKS, generate
from atlas_context.mcp_server import BoundContext


class EvaluationTests(unittest.TestCase):
    def test_fixed_tasks_have_inspectable_rubrics_and_revoked_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evaluation"
            result = generate(root)
            self.assertEqual(result["tasks"], 15)
            self.assertEqual(result["planned_model_conditions"], 45)
            self.assertEqual(result["model_calls"], 0)
            self.assertEqual(result["mechanical_passed"], 60)
            self.assertEqual(len({task[0] for task in TASKS}), 15)
            rubric = json.loads((root / "quiet-day" / "private-rubric.json").read_text())
            self.assertIn("scheduled indoor art workshop", rubric["corrected"]["items"][0]["text"])
            with self.assertRaises(PermissionError):
                BoundContext.from_config(root / "quiet-day" / "revoked-control" / "private-server.json").search()
            self.assertEqual((root / "quiet-day" / "private-rubric.json").stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                generate(root)

    def test_evaluation_runtime_is_rejected_inside_git(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "checkout"
            (root / ".git").mkdir(parents=True)
            with self.assertRaises(ValueError):
                generate(root / "evaluation")
