# Physical-device acceptance checklist

**Status: not completed.** Simulator UI checks, Swift serialization, MCP transport and model examples are separate evidence. Do not mark physical-device transfer verified until the full sequence below has been observed on a real iPhone.

Use a fresh drawing of simple geometric shapes, not a personal photograph. A small fictional note is sufficient for the explanation. Avoid screenshots containing account names, real location, notifications or transfer destinations.

1. Generate the standalone companion with `scripts/create_phone_project.py`, open it in Xcode, select your signing team and install on the test iPhone. Production Atlas Memoir integration is a separate milestone.
2. Choose only the new drawing through the system Photos picker. Verify the explanation starts blank, export remains unavailable and no full-library permission is requested. Record failures as well as successes.
3. Enter a fictional explanation, confirm it, then edit it. Verify confirmation is cleared. Reconfirm and enter the separate disclosure screen; verify no record is selected and cloud is off.
4. Select that statement only. Review the complete JSON and acknowledge the exact wording before saving. Verify the saved file contains no image data, classifier labels, photo IDs, coordinates or unexpected records. Review text itself for personal facts; schema validation does not redact prose.
5. Save locally, then transfer the file to a trusted computer. In a local terminal, run `python3 -m atlas_context.phone inspect --bundle <file>`. After personally reviewing the exact text, connect with its displayed SHA-256 to a fresh runtime outside Git.
6. Bind the generated server config to a trusted local model/host. Ask for a short cited summary. Confirm every personal claim is supported by the selected statement and note whether any information was invented. A cloud test requires separate exact-text approval and dual opt-in.
7. Keep the host connection open. Revoke with `python3 -m atlas_context.phone revoke --runtime <runtime>`. Make another tool call and verify denial. Prior answers may remain in history; this is not a forgetting test.
8. Correct the wording on the phone. Revoke the old session, export and review a new file, and connect a new session. Verify the old session stays denied and the new wording is used.
9. Clear the phone session, revoke the new desktop session and delete test exports/runtime copies. Record device/OS, commit, host/model, each step's outcome and limitations without publishing personal identifiers or logs.

Publish only a manually reviewed synthetic acceptance report. A successful run demonstrates that device/configuration, not every phone, file provider or Agent host.
