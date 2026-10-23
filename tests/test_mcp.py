"""Transport and invalidation tests using fictional records; no model or API key."""
import asyncio
from datetime import datetime, timedelta, timezone
from functools import wraps
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from atlas_context.cli import read
from atlas_context.core import revision
from atlas_context.mcp_server import BoundContext, build_server
from atlas_context.synthetic import generate

HAS_MCP = importlib.util.find_spec("mcp") is not None


def connected(test):
    # MCP/AnyIO context entry and exit must run in the same async task.
    @wraps(test)
    async def run(self):
        from mcp import Client
        async with Client(build_server(self.bound), cache=None) as client:
            self.client = client
            await test(self)
    return run


class SyntheticStoryTests(unittest.TestCase):
    def test_richer_story_is_generated_outside_source_without_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "demo"
            report = generate(destination)
            self.assertEqual(report["draft_records"], 16)
            self.assertEqual(report["approved_records"], 14)
            self.assertEqual(report["query_scenarios_passed"], 8)
            with self.assertRaises(ValueError):
                generate(destination)

    def test_runtime_cannot_be_generated_inside_checkout(self):
        with self.assertRaises(ValueError):
            generate(Path(__file__).resolve().parents[1] / "unsafe-runtime")


@unittest.skipUnless(HAS_MCP, "Optional MCP extra requires Python 3.11+")
class MCPBoundaryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name) / "demo"
        generate(self.root)
        self.bound = BoundContext.from_config(self.root / "private-server.json")

    def tearDown(self):
        self.directory.cleanup()

    def edit(self, name, value):
        from atlas_context.mcp_demo import replace_local
        replace_local(self.root / name, value)

    async def search(self, **arguments):
        return await self.client.call_tool("search_life_context", arguments)

    @connected
    async def test_tool_exposes_no_source_or_grant_controls(self):
        tools = (await self.client.list_tools()).tools
        self.assertEqual([tool.name for tool in tools], ["search_life_context"])
        self.assertEqual(set(tools[0].input_schema["properties"]), {"query", "include_inferred", "max_results", "max_chars"})
        self.assertFalse(tools[0].input_schema["additionalProperties"])
        self.assertEqual(tools[0].input_schema["properties"]["query"]["maxLength"], 256)
        self.assertEqual(tools[0].input_schema["properties"]["max_results"]["maximum"], 50)
        self.assertEqual(tools[0].input_schema["properties"]["max_chars"]["minimum"], 2500)
        self.assertTrue(tools[0].annotations.read_only_hint)

    @connected
    async def test_private_text_cannot_match_and_inference_stays_labeled(self):
        for query in ("SYNTHETIC_OCR_SECRET", "UNSELECTED_SYNTHETIC_DETAIL", "employer", "trip"):
            result = await self.search(query=query)
            self.assertEqual(result.structured_content["items"], [])
        result = await self.search(query="trip", include_inferred=True)
        self.assertEqual(result.structured_content["items"][0]["attribution"], "inferred")

    @connected
    async def test_extra_arguments_and_coerced_booleans_are_rejected(self):
        from mcp import MCPError
        for arguments in ({"grant": "untrusted"}, {"purpose": "anything"}, {"include_inferred": "false"},
                          {"query": 42}, {"query": "x" * 257}, {"query": " ".join(["word"] * 13)},
                          {"max_results": True}, {"max_results": 0}, {"max_results": 51},
                          {"max_chars": "6000"}, {"max_chars": 2499}, {"max_chars": 20001}):
            with self.assertRaises(MCPError):
                await self.search(**arguments)

    @connected
    async def test_results_are_bounded_without_widening_the_grant(self):
        result = await self.search(query="photography", max_results=2, max_chars=2500)
        data = result.structured_content
        self.assertEqual(len(data["items"]), 2)
        self.assertTrue(data["retrieval"]["has_more"])
        self.assertLessEqual(data["retrieval"]["returned_chars"], 2500)
        self.edit("private-grant.json", dict(read(self.root / "private-grant.json"), active=False))
        self.assertTrue((await self.search(max_results=50, max_chars=20000)).is_error)

    @connected
    async def test_changed_source_does_not_reuse_previous_approval(self):
        before = await self.search(query="photography")
        self.assertEqual(len(before.structured_content["items"]), 7)
        records = read(self.root / "private-draft.json")
        records[0]["private_text"] = "Updated fictional source"
        records[0]["revision"] = revision(records[0])
        self.edit("private-draft.json", records)
        after = await self.search(query="photography")
        self.assertEqual(len(after.structured_content["items"]), 6)

    @connected
    async def test_revocation_expiry_and_identity_labels_checked_each_call(self):
        grant = read(self.root / "private-grant.json")
        patches = ({"active": False}, {"expires_at": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()},
                   {"purpose": "another_task"}, {"audience": "another_client"})
        for patch in patches:
            self.edit("private-grant.json", dict(grant, **patch))
            result = await self.search(query="photography")
            self.assertTrue(result.is_error)
            self.assertNotIn(str(self.root), json.dumps(result.model_dump()))

    @connected
    async def test_missing_draft_does_not_disclose_location(self):
        (self.root / "private-draft.json").unlink()
        result = await self.search(query="photography")
        self.assertTrue(result.is_error)
        self.assertNotIn(str(self.root), json.dumps(result.model_dump()))


@unittest.skipUnless(HAS_MCP, "Optional MCP extra requires Python 3.11+")
class StdioRoundtripTests(unittest.TestCase):
    def test_actual_subprocess_transport_and_same_connection_revocation(self):
        from atlas_context.mcp_demo import run
        with tempfile.TemporaryDirectory() as folder:
            report = asyncio.run(run(Path(folder) / "demo"))
            self.assertEqual(report["mcp_checks_passed"], 16)
            self.assertTrue(report["same_connection_revocation_verified"])
            self.assertEqual(report["model_calls"], 0)

    def test_legacy_client_negotiation_uses_the_same_disclosure_checks(self):
        from atlas_context.mcp_demo import run
        with tempfile.TemporaryDirectory() as folder:
            report = asyncio.run(run(Path(folder) / "demo", mode="legacy"))
            self.assertEqual(report["protocol_version"], "2025-11-25")
            self.assertEqual(report["mcp_checks_passed"], 16)
