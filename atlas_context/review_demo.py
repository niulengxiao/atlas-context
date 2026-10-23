"""A reproducible fictional context lifecycle. No photos, model, SDK or API key."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import sys

from .cli import read, write
from .core import query_context, revision
from .mcp_server import BoundContext
from .phone import connect, load_bundle, outside_source, revoke, synthetic_assistance_bundle


def run(destination):
    root = outside_source(destination)
    root.mkdir(parents=True, exist_ok=False, mode=0o700)
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError("Fictional review check failed: " + name)
        checks.append({"case": name, "passed": True})

    def denied(action):
        try:
            action()
        except PermissionError:
            return True
        return False

    def session(bundle, name):
        path = root / ("private-" + name + ".json")
        write(path, bundle)
        path.chmod(0o600)
        _, digest = load_bundle(path)
        # Scripted approval is valid only for these known fictional fixtures.
        connect(path, root / name, reviewed_sha256=digest, audience="fictional_reviewer")
        return BoundContext.from_config(root / name / "private-server.json")

    bundle = synthetic_assistance_bundle()
    original = session(bundle, "original-session")
    before = original.search()
    check("two_reviewed_user_statements", len(before["items"]) == 2
          and all(item["attribution"] == "user_statement" for item in before["items"]))
    check("scene_guesses_not_exported", all(set(record) == {"text", "attribution"} for record in bundle["records"])
          and len(original.search(include_inferred=True)["items"]) == 2)
    check("unsupported_employer_has_no_evidence", original.search("employer")["items"] == [])
    _, digest = load_bundle(root / "private-original-session.json")
    check("local_only_rejects_cloud_opt_in", denied(lambda: connect(
        root / "private-original-session.json", root / "denied-cloud-session", reviewed_sha256=digest,
        audience="fictional_cloud", allow_cloud=True)) and not (root / "denied-cloud-session").exists())
    drafts, grant = read(original.draft), read(original.grant)
    check("different_task_is_denied", denied(lambda: query_context(
        drafts, grant, purpose="short_bio", audience="fictional_reviewer")))

    # An imported draft edit invalidates its old approval. This is not a phone watcher.
    changed = deepcopy(drafts)
    changed[0]["private_text"] = "Changed fictional source; exact wording needs a fresh review."
    changed[0]["revision"] = revision(changed[0])
    original.draft.write_text(json.dumps(changed), encoding="utf-8")
    after_edit = original.search()
    check("changed_draft_is_withheld", len(after_edit["items"]) == 1
          and "work assignment" in after_edit["items"][0]["text"])

    # Explicitly revoke the old export, then separately review a new one.
    revoke(root / "original-session")
    check("revoked_session_denies_next_read", denied(original.search))
    corrected_bundle = synthetic_assistance_bundle()
    corrected_bundle["records"][0]["text"] = (
        "For my next day off, I want a structured indoor art workshop with a scheduled start time. "
        "My earlier preference for an unplanned outdoor day does not apply to this request.")
    corrected = session(corrected_bundle, "corrected-session")
    after = corrected.search()
    check("newly_reviewed_preference_replaces_old_wording", len(after["items"]) == 2
          and after["items"][0]["text"] == corrected_bundle["records"][0]["text"]
          and not any("I enjoy quiet outdoor walks" in item["text"] for item in after["items"]))
    check("new_session_does_not_reactivate_old_session", denied(original.search))
    report = {"synthetic_only": True, "backend": "local_python_core", "model_calls": 0,
              "network_calls": 0, "checks_passed": len(checks), "checks": checks,
              "original_context": before, "after_draft_edit": after_edit, "corrected_context": after,
              "original_session_revoked": True, "corrected_session_disclosure": "local_only",
              "limits": "Scripted fictional approval; no language-model quality evaluation or automatic phone refresh."}
    write(root / "private-review-results.json", report)
    (root / "private-review-results.json").chmod(0o600)
    overview = "# Fictional context lifecycle (no model)\n\n"
    overview += "\n".join("- PASS: " + item["case"] for item in checks)
    for title, response in (("Original reviewed context", before), ("Newly reviewed context", after)):
        overview += "\n\n## " + title + "\n\n"
        overview += "\n\n".join(item["text"] + " [" + item["citation"] + "]" for item in response["items"])
    overview += ("\n\nThese are exact reviewed fictional sentences, not generated advice. The old session remains revoked. "
                 "Bind corrected-session/private-server.json only to a local model/host, then use its task prompt.\n")
    overview_path = root / "private-review-walkthrough.md"
    overview_path.write_text(overview, encoding="utf-8")
    overview_path.chmod(0o600)
    return {key: report[key] for key in ("synthetic_only", "backend", "model_calls", "network_calls",
            "checks_passed", "original_session_revoked", "corrected_session_disclosure")}


def main(argv=None):
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="New private directory outside every Git checkout")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args.output), indent=2))
        return 0
    except (ValueError, OSError, PermissionError):
        print("Choose a new writable runtime directory outside every Git checkout.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
