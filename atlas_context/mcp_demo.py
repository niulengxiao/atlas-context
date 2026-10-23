"""Real SDK client/server stdio roundtrip, with fictional records and no LLM."""
import argparse
import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import tempfile

from .cli import read, write
from .core import revision
from .synthetic import generate, SCENARIOS


def replace_local(path, value):
    """Atomic trusted-local edit; used only on the newly generated demo runtime."""
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".local-edit-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


def context_data(result):
    if result.is_error:
        raise AssertionError("Expected an approved context response")
    if result.structured_content is None:
        raise AssertionError("Expected structured MCP output")
    return result.structured_content


async def run(destination, mode="auto"):
    from mcp import Client, MCPError, StdioServerParameters

    generated = generate(destination)
    dest = Path(destination).expanduser().resolve()
    draft_path, grant_path = dest / "private-draft.json", dest / "private-grant.json"
    records, grant = read(draft_path), read(grant_path)
    server = StdioServerParameters(command=sys.executable,
        args=["-m", "atlas_context.mcp_server", "--config", str(dest / "private-server.json")])
    checks = []
    async with Client(server, mode=mode, cache=None, read_timeout_seconds=20) as client:
        listed = await client.list_tools()
        assert [tool.name for tool in listed.tools] == ["search_life_context"]
        schema = listed.tools[0].input_schema
        assert set(schema["properties"]) == {"query", "include_inferred", "max_results", "max_chars"} and schema["additionalProperties"] is False
        checks.append({"case": "only_bounded_read_tool_exposed", "passed": True})
        responses = []
        for query, inferred, count in SCENARIOS:
            result = await client.call_tool("search_life_context", {"query": query, "include_inferred": inferred})
            data = context_data(result)
            assert len(data["items"]) == count
            if inferred and count:
                assert all(item["attribution"] == "inferred" for item in data["items"])
            serialized = json.dumps(data)
            for secret in ("SYNTHETIC_OCR_SECRET", "SYNTHETIC_LOCATOR_", "HIDDEN_SYNTHETIC_DETAIL", "UNSELECTED_SYNTHETIC_DETAIL", "fictional-stage-"):
                assert secret not in serialized
            responses.append({"query": query, "include_inferred": inferred, "result": data})
            checks.append({"case": "query:" + query + (":include_inferred" if inferred else ""), "passed": True})

        async def denied(arguments=None):
            try:
                result = await client.call_tool("search_life_context", arguments or {"query": "photography"})
                assert result.is_error
                text = json.dumps(result.model_dump())
            except MCPError as error:
                text = str(error)
            for secret in (str(dest), "SYNTHETIC_LOCATOR_", "SYNTHETIC_OCR_SECRET"):
                assert secret not in text

        await denied({"query": "photography", "grant": "untrusted-path"})
        checks.append({"case": "model_cannot_select_grant_or_files", "passed": True})
        await denied({"query": "trip", "include_inferred": "false"})
        checks.append({"case": "strict_boolean_input", "passed": True})
        changed = deepcopy(records)
        changed[0]["private_text"] = "Changed fictional source; review is now stale."
        changed[0]["revision"] = revision(changed[0])
        replace_local(draft_path, changed)
        after_change = context_data(await client.call_tool("search_life_context", {"query": "photography"}))
        assert len(after_change["items"]) == 6
        replace_local(draft_path, records)
        checks.append({"case": "changed_draft_is_not_served_from_cache", "passed": True})
        expired = dict(grant, expires_at=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat())
        replace_local(grant_path, expired)
        await denied()
        checks.append({"case": "expiry_checked_on_next_call", "passed": True})
        replace_local(grant_path, dict(grant, purpose="another_purpose"))
        await denied()
        checks.append({"case": "purpose_bound_by_host", "passed": True})
        replace_local(grant_path, dict(grant, audience="another_audience"))
        await denied()
        checks.append({"case": "audience_bound_by_host", "passed": True})
        replace_local(grant_path, dict(grant, active=False))
        await denied()
        checks.append({"case": "revocation_checked_on_same_connection", "passed": True})
        protocol = client.protocol_version

    # Exact reviewed sentences, not a model-generated biography or a semantic evaluation.
    preview = "\n".join(item["text"] + " [" + item["citation"] + "]"
                        for item in responses[0]["result"]["items"] if item["attribution"] == "user_statement")
    write(dest / "mcp-transcript.json", {"synthetic_only": True, "protocol_version": protocol,
          "checks": checks, "responses": responses, "citation_preview": preview,
          "preview_kind": "deterministic_exact_reviewed_sentences", "model_calls": 0})
    return {**generated, "transport": "stdio", "protocol_version": protocol, "mcp_checks_passed": len(checks),
            "same_connection_revocation_verified": True, "demo_grant_left_revoked": True, "model_calls": 0}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description="Verify a real MCP stdio roundtrip using a new fictional runtime")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(asyncio.run(run(args.output)), indent=2))
    except ImportError:
        parser.exit(2, "Use Python 3.11+ and install '.[mcp]' first.\n")


if __name__ == "__main__":
    main()
