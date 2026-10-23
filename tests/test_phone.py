"""Phone projection and consent failures. All records are fictional."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from atlas_context.cli import read, write
from atlas_context.core import query_context
from atlas_context.phone import connect, demo, load_bundle, revoke, synthetic_bundle, synthetic_assistance_bundle, validate_bundle
from atlas_context.mcp_server import BoundContext, build_server


class PhoneHandoffTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        self.path = self.root / "private-phone.json"
        self.bundle = synthetic_bundle()
        write(self.path, self.bundle)

    def tearDown(self):
        self.folder.cleanup()

    def connection(self, **kwargs):
        _, digest = load_bundle(self.path)
        return connect(self.path, self.root / "session", reviewed_sha256=digest, audience="fictional_local_agent", **kwargs)

    def bound(self):
        return BoundContext.from_config(self.root / "session" / "private-server.json")

    def test_unknown_phone_and_record_fields_fail_closed(self):
        for key in ("payload", "journeyArchive", "gps", "photos", "device_id", "approval"):
            candidate = dict(self.bundle, **{key: "PRIVATE_SENTINEL"})
            with self.assertRaises(ValueError):
                validate_bundle(candidate)
        for key in ("source_ref", "private_locator", "photo_id", "latitude", "raw_ocr", "hidden"):
            candidate = deepcopy(self.bundle)
            candidate["records"][0][key] = "PRIVATE_SENTINEL"
            with self.assertRaises(ValueError):
                validate_bundle(candidate)

    def test_duplicate_fields_and_oversized_files_rejected(self):
        self.path.write_text('{"format":"first","format":"second"}')
        with self.assertRaises(ValueError):
            load_bundle(self.path)
        self.path.write_bytes(b" " * 256_001)
        with self.assertRaises(ValueError):
            load_bundle(self.path)

    def test_expiry_lifetime_and_future_creation_rejected(self):
        now = datetime.now(timezone.utc)
        for created, expires in ((now - timedelta(hours=2), now - timedelta(hours=1)),
                                 (now, now + timedelta(hours=25)),
                                 (now + timedelta(minutes=6), now + timedelta(hours=1)),
                                 (now, now)):
            candidate = dict(self.bundle, created_at=created.isoformat(), expires_at=expires.isoformat())
            with self.assertRaises(ValueError):
                validate_bundle(candidate, now=now)

    def test_count_text_and_exact_date_limits(self):
        for records in ([], self.bundle["records"] * 13,
                        [{"text": "x" * 2001, "attribution": "recorded"}],
                        [{"text": "x" * 2000, "attribution": "recorded"}] * 11,
                        [{"text": "Fictional", "attribution": "recorded", "period": "2025-01-13"}],
                        [{"text": "Fictional", "attribution": "recorded", "period": "2025-13"}]):
            with self.assertRaises(ValueError):
                validate_bundle(dict(self.bundle, records=records))

    def test_exact_bundle_acknowledgment_required_without_side_effects(self):
        with self.assertRaises(PermissionError):
            connect(self.path, self.root / "session", reviewed_sha256="0" * 64, audience="local")
        self.assertFalse((self.root / "session").exists())
        _, old_digest = load_bundle(self.path)
        changed = deepcopy(self.bundle)
        changed["records"][0]["text"] = "Different fictional sentence"
        self.path.write_text(json.dumps(changed))
        with self.assertRaises(PermissionError):
            connect(self.path, self.root / "session", reviewed_sha256=old_digest, audience="local")

    def test_cloud_requires_both_phone_and_desktop_opt_in(self):
        with self.assertRaises(PermissionError):
            self.connection(allow_cloud=True)
        self.bundle["disclosure"] = "cloud_allowed"
        self.path.write_text(json.dumps(self.bundle))
        report = self.connection()
        self.assertEqual(report["disclosure"], "local_only")
        _, digest = load_bundle(self.path)
        report = connect(self.path, self.root / "cloud-session", reviewed_sha256=digest, audience="fictional_cloud_agent", allow_cloud=True)
        self.assertEqual(report["disclosure"], "cloud_allowed")
        self.assertFalse(report["model_called"])

    def test_minimal_projection_inference_and_private_permissions(self):
        self.connection()
        bound = self.bound()
        result = bound.search()
        self.assertEqual(len(result["items"]), 3)
        self.assertEqual(len(bound.search(include_inferred=True)["items"]), 4)
        self.assertEqual(bound.search("trip")["items"], [])
        for item in result["items"]:
            self.assertNotIn("source_ref", item)
            self.assertNotIn("private_locator", item)
            self.assertNotIn("city", item)
            self.assertEqual(item["attribution"], "user_statement")
            self.assertEqual(item["source"], "phone_export")
        self.assertEqual((self.root / "session").stat().st_mode & 0o777, 0o700)
        for path in (self.root / "session").iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_no_overwrite_or_runtime_inside_git(self):
        self.connection()
        before = (self.root / "session" / "private-grant.json").read_bytes()
        with self.assertRaises(FileExistsError):
            self.connection()
        self.assertEqual(before, (self.root / "session" / "private-grant.json").read_bytes())
        checkout = self.root / "checkout"
        (checkout / ".git").mkdir(parents=True)
        _, digest = load_bundle(self.path)
        with self.assertRaises(ValueError):
            connect(self.path, checkout / "runtime", reviewed_sha256=digest, audience="local")

    def test_connection_does_not_extend_phone_expiry(self):
        now = datetime.now(timezone.utc)
        self.bundle["expires_at"] = (now + timedelta(minutes=5)).isoformat()
        self.path.write_text(json.dumps(self.bundle))
        report = self.connection()
        self.assertEqual(report["expires_at"], self.bundle["expires_at"])

    def test_revocation_applies_to_the_existing_bound_session(self):
        self.connection()
        bound = self.bound()
        self.assertEqual(len(bound.search()["items"]), 3)
        report = revoke(self.root / "session")
        self.assertFalse(report["recalls_previously_disclosed_text"])
        with self.assertRaises(PermissionError):
            bound.search()

    def test_one_command_fictional_demo(self):
        report = demo(self.root / "demo")
        self.assertEqual(report["default_evidence_count"], 3)
        self.assertFalse(report["model_called"])

    def test_personal_assistance_keeps_correction_and_excludes_photo_guess(self):
        self.bundle = synthetic_assistance_bundle()
        self.path.write_text(json.dumps(self.bundle))
        self.connection()
        bound = self.bound()
        result = bound.search()
        self.assertEqual(len(result["items"]), 2)
        self.assertEqual(len(bound.search(include_inferred=True)["items"]), 2)
        self.assertTrue(all(item["attribution"] == "user_statement" for item in result["items"]))
        self.assertIn("work assignment", " ".join(item["text"] for item in result["items"]))
        self.assertFalse(any("café hopping" in item["text"] for item in result["items"]))
        task = (self.root / "session" / "private-agent-task.md").read_text()
        self.assertIn("honor explicit corrections", task)
        self.assertNotIn(self.bundle["records"][0]["text"], task)
        # Same trusted configuration, purpose gate and revocation as life summaries.
        grant = read(self.root / "session" / "private-grant.json")
        with self.assertRaises(PermissionError):
            query_context(read(self.root / "session" / "private-draft.json"), grant,
                          purpose="life_reflection", audience="fictional_local_agent")
        revoke(self.root / "session")
        with self.assertRaises(PermissionError):
            bound.search()

    def test_personal_assistance_demo_uses_existing_review_pipeline(self):
        report = demo(self.root / "assistance", scenario="personal-assistance")
        self.assertEqual(report["default_evidence_count"], 2)
        self.assertFalse(report["model_called"])
        with self.assertRaises(ValueError):
            demo(self.root / "bad", scenario="unknown")
        self.assertFalse((self.root / "bad").exists())


@unittest.skipUnless(importlib.util.find_spec("mcp"), "Optional MCP extra required")
class PhoneMCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_phone_handoff_through_real_stdio_and_revoke(self):
        import sys
        from mcp import Client, StdioServerParameters
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "phone"
            demo(root)
            parameters = StdioServerParameters(command=sys.executable,
                args=["-m", "atlas_context.mcp_server", "--config", str(root / "session" / "private-server.json")])
            async with Client(parameters, cache=None, read_timeout_seconds=20) as client:
                result = await client.call_tool("search_life_context", {"query": "", "include_inferred": False})
                self.assertEqual(len(result.structured_content["items"]), 3)
                revoke(root / "session")
                result = await client.call_tool("search_life_context", {"query": ""})
                self.assertTrue(result.is_error)
                self.assertNotIn(str(root), json.dumps(result.model_dump()))
