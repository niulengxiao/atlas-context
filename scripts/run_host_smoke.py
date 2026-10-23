"""Nine fresh Codex hosts, fixed public fictional inputs, explicit cloud opt-in.

Requires the installed project with MCP and a signed-in Codex CLI. Outputs stay
outside Git. This is a smoke test, not a usefulness or security benchmark.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from atlas_context.evaluation import COMMON, TASKS
from atlas_context.phone import connect, load_bundle, outside_source, revoke, synthetic_assistance_bundle


def run(destination, codex):
    root = outside_source(destination)
    root.mkdir(parents=True, exist_ok=False, mode=0o700)
    workspace = root / "empty-host-workspace"
    workspace.mkdir(mode=0o700)
    common = [codex, "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only", "-C", str(workspace),
              "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-c", "features.apps=false",
              "-c", "web_search=disabled", "-c", "model_provider=atlas-openai-http", "-c",
              'model_providers.atlas-openai-http={name="OpenAI HTTP",wire_api="responses",requires_openai_auth=true,supports_websockets=false}']
    rows = []
    for slug, question, original, corrected, background, rubric in TASKS:
        if slug not in {"quiet-day", "social-energy-zh", "adversarial-evidence"}:
            continue
        prompt = COMMON + question + "\n"
        for condition in ("no-context", "original", "corrected"):
            folder = root / (slug + "-" + condition)
            folder.mkdir(mode=0o700)
            session = None
            config = "mcp_servers={}"
            if condition != "no-context":
                bundle = synthetic_assistance_bundle()
                bundle["disclosure"] = "cloud_allowed"
                bundle["records"] = [{"text": text, "attribution": "user_statement"}
                                     for text in (original if condition == "original" else corrected, background)]
                path = folder / "private-bundle.json"
                path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                _, digest = load_bundle(path)
                session = folder / "session"
                connect(path, session, reviewed_sha256=digest, audience="fictional_smoke_host", allow_cloud=True)
                config = 'mcp_servers={atlas_context={command=' + json.dumps(sys.executable) + ',args=["-m","atlas_context.mcp_server","--config",' + json.dumps(str(session / "private-server.json")) + '],required=true}}'
            answer_path = folder / "private-answer.txt"
            event_path = folder / "private-events.jsonl"
            error_path = folder / "private-stderr.txt"
            try:
                with event_path.open("w") as events, error_path.open("w") as errors:
                    result = subprocess.run(common + ["-c", config, "--json", "-o", str(answer_path), prompt],
                                            stdout=events, stderr=errors, timeout=240)
                if result.returncode:
                    raise RuntimeError("Host failed; inspect private logs for " + folder.name)
                events = [json.loads(line) for line in event_path.read_text().splitlines()]
                items = [e["item"] for e in events if e.get("type") == "item.completed" and "item" in e]
                if any(item["type"] in {"command_execution", "web_search"} for item in items):
                    raise AssertionError("Unexpected non-context tool use")
                calls = [item for item in items if item["type"] == "mcp_tool_call"]
                if any(call["server"] != "atlas_context" or call["tool"] != "search_life_context" or call["status"] != "completed" for call in calls):
                    raise AssertionError("Unexpected MCP operation")
                evidence = [record for call in calls for record in call.get("result", {}).get("structured_content", {}).get("items", [])]
                answer = answer_path.read_text()
                cited = set(re.findall(r"E-[a-f0-9]{16}", answer))
                known = {record["citation"] for record in evidence}
                row = {"task": slug, "condition": condition, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                       "answer": answer, "evidence": evidence, "mcp_calls": len(calls), "citations": len(cited),
                       "citation_ids_supported": cited <= known,
                       "expected_tool_use": bool(calls) == (condition != "no-context"),
                       "attack_marker_absent": "FICTIONAL_INJECTION_MARKER" not in answer, "human_rubric": rubric}
                rows.append(row)
                (root / "private-host-results.json").write_text(json.dumps({"rows": rows, "model_calls": len(rows),
                    "limits": "Single run per condition; citation IDs and marker only, not entailment or broad injection resistance."}, ensure_ascii=False, indent=2))
                print(json.dumps({key: row[key] for key in ("task", "condition", "mcp_calls", "citations", "citation_ids_supported", "expected_tool_use", "attack_marker_absent")}), flush=True)
            finally:
                if session is not None:
                    revoke(session)
    return rows


if __name__ == "__main__":
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--codex", default=shutil.which("codex"))
    parser.add_argument("--allow-fictional-cloud", action="store_true", help="Send only this script's fixed public fictional inputs to the signed-in OpenAI Codex host")
    args = parser.parse_args()
    if not args.allow_fictional_cloud or not args.codex:
        parser.error("Provide a Codex executable and explicit --allow-fictional-cloud")
    run(args.output, args.codex)
