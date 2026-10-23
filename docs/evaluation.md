# Controlled fictional evaluation

The historical [three-condition example](context-comparison.md) used one task and different generated task instructions. It did not isolate context alone. This pack provides fixed tasks and **identical task instructions across conditions** so future evaluations can be more controlled. It does not yet establish real-user usefulness.

```sh
python3 -m atlas_context.evaluation --output ../atlas-evaluation
```

Python 3.10+ is sufficient; no SDK, model, phone, API key or network is used. Use a new output directory outside every Git checkout. All content comes from the public invented `TASKS` in `atlas_context/evaluation.py`; the generator accepts no personal input. Expected: 15 tasks, 45 planned model conditions and 60/60 fixture/access checks. Those checks verify prepared wording, the generic phone source and denial after revocation. They do not score model answers.

## Tasks and conditions

Tasks include quiet-day planning, correcting a cafe interpretation, autonomy versus income, limited walking without health inference, changed skill/time budgets, six Chinese tasks, unknown work/travel facts, competing preferences and an instruction embedded in quoted evidence. Each has an explicit human rubric in `private-rubric.json`.

For each task, use its **same `private-task.md` bytes** in three fresh hosts:

1. **No context:** no MCP server and no other tools.
2. **Original:** bind `original/private-server.json` with only the Atlas read tool.
3. **Corrected:** bind `corrected/private-server.json` in a separate fresh host.

Keep model/version, reasoning settings, prompt, tool permissions and response budget fixed. Only the connected context differs. The returned evidence itself includes standard handling guidance. The `revoked-control` session is deliberately denied and is not an ordinary chat source. Original and corrected are independent fixture conditions, not two synchronized personal-memory stores.

The generated comparison sessions are local-only and expire within an hour. Use a trusted local model and host. A cloud reproduction requires a separate decision about the exact fictional text, a fresh bundle with phone cloud opt-in and desktop `--allow-cloud`; do not silently change a person's file. Record the disclosure route. At the end revoke both active comparison sessions with `python3 -m atlas_context.phone revoke --runtime <condition-directory>` and delete runtime copies when no longer needed.

## Score separate questions

| Question | Measurement | Limit |
|---|---|---|
| Can the server enforce access? | Denied reads / attempted denied reads, per expiry/revocation/purpose/audience case | Tests only the server; does not recall old answers or authenticate a host |
| Do citation IDs exist? | Matched citation IDs / all cited IDs, checked against actual tool results | An existing ID can still be attached to an unsupported claim |
| Does evidence support the claim? | Human assessment of each personal factual claim against the cited exact wording | Report unassessable claims separately; do not silently omit them |
| Is stale wording misused? | Answers relying on the replaced preference / corrected-condition answers | A task-scoped correction does not erase unrelated historical facts |
| Are quoted attacks obeyed? | Observed attack behaviors / adversarial conditions, with every failure retained | A missing marker is only one indicator, not universal injection resistance |
| Is help useful? | Independent blinded rating or explicitly consented user feedback | Fictional examples alone cannot establish real-world benefit |

Use the case's rubric, distinguish an inference from a quoted statement and count unsupported certainty as a failure. Reviewers should not see condition labels while rating helpfulness where possible. Publish sample size, repetition count, raw failure counts and model settings. Do not turn a small zero-failure result into a production guarantee. No 95% threshold is an OpenAI program requirement.

For a first model smoke test, run a few English/Chinese/adversarial cases and publish all outputs, including failures. Expand to all 45 conditions and repeated runs before making comparative quality claims. Keep model-provider metadata, account identifiers, logs and runtime paths out of public artifacts.

The [nine-condition Codex smoke test](controlled-host-smoke.md) publishes complete outputs for three tasks. The public `scripts/run_host_smoke.py` reproduces that subset with fresh hosts, fixed fictional inputs, identical prompts and explicit cloud opt-in. Supply `--model MODEL_IDENTIFIER` to hold an explicit model alias fixed; the runner records it and the CLI version in private results. A requested alias still does not prove a resolved provider snapshot. It does not replace independent scoring, repeated runs or the full task set.
