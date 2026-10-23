"""A reviewer's reproducible lifecycle, using fictional data only."""
import json
from pathlib import Path
import tempfile
import unittest

from atlas_context.mcp_server import BoundContext
from atlas_context.review_demo import run


class ReviewerWalkthroughTests(unittest.TestCase):
    def test_corrected_context_and_revocation_remain_true_after_demo_returns(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "review"
            report = run(root)
            self.assertEqual(report["checks_passed"], 9)
            self.assertEqual(report["model_calls"], 0)
            old = BoundContext.from_config(root / "original-session" / "private-server.json")
            with self.assertRaises(PermissionError):
                old.search()
            current = BoundContext.from_config(root / "corrected-session" / "private-server.json")
            items = current.search()["items"]
            self.assertEqual(len(items), 2)
            self.assertIn("structured indoor art workshop", items[0]["text"])
            result = json.loads((root / "private-review-results.json").read_text())
            self.assertEqual(result["corrected_context"]["items"], items)
            self.assertTrue(all(check["passed"] for check in result["checks"]))
            self.assertEqual((root / "private-review-results.json").stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                run(root)

    def test_review_runtime_cannot_be_written_inside_another_git_checkout(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "repo"
            (root / ".git").mkdir(parents=True)
            with self.assertRaises(ValueError):
                run(root / "review")
            self.assertFalse((root / "review").exists())
