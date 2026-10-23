# Review Atlas Context in five minutes

Atlas Context helps personal-agent developers pass **user-explained, reviewed life context** to an agent. The reusable part is the boundary between a private source, the wording a person approves and the context a model may retrieve. The current iOS companion supplies a selected-photo entry point; Python and MCP work independently of that app.

The goal is assistance that understands a person's stated experiences and tradeoffs. The current implementation uses local scene prompts and the person's explanations. It does not reconstruct a life or learn a personality from a photo archive.

## 1. Run without a phone, account or API key

Use Python 3.10+:

```sh
git clone https://github.com/niulengxiao/atlas-context.git
cd atlas-context
python3 -m atlas_context.review_demo --output ../atlas-review-demo
```

Expected result: `synthetic_only: true`, `checks_passed: 9`, `model_calls: 0`, `network_calls: 0`. Open `../atlas-review-demo/private-review-walkthrough.md` locally. Every sentence is fictional; the preview repeats reviewed wording rather than generating advice. Use a new output directory on later runs.

The first context says the person prefers quiet walks and flexible days off. Their café photos were for work. The walkthrough then edits an imported draft, verifies that its stale approval withholds it, explicitly revokes the old session and separately reviews a new preference for a structured indoor art workshop. The old session remains denied. This is an explicit correction workflow, not automatic source refresh or long-term memory.

The nine checks cover two reviewed user statements, minimal exported fields, unsupported employer evidence, denial of cloud use for local-only text, a task mismatch, changed-draft withholding, old-session revocation, newly reviewed wording and continued denial of the old session.

## 2. Inspect the actual transport

For Python 3.11+ and the optional MCP dependency:

```sh
python3 -m venv ../atlas-env
../atlas-env/bin/python -m pip install '.[mcp]'
../atlas-env/bin/python -m atlas_context.mcp_demo --output ../atlas-transport-demo
```

Expected result: `mcp_checks_passed: 16`, `same_connection_revocation_verified: true`, `model_calls: 0`. This uses an actual SDK subprocess connection and intentionally ends with a revoked demo grant. Do not bind that revoked session for an ordinary chat.

For your own agent integration, bind `../atlas-review-demo/corrected-session/private-server.json` as described in [MCP setup](mcp.md). That session defaults to **local-only**. It needs a local model and a host that respects the policy. The project does not install a local model or attest to host behavior. For cloud use, create a separately reviewed cloud-allowed export and explicitly opt in on the desktop; never silently relabel a personal local-only file.

## 3. Trace claims to implementation

| Claim | Code and checks | Practical limit |
|---|---|---|
| Selected photos stay on the phone's processing path | `mobile/LocalPhotoAnalyzer.swift`, `mobile/PhotoReflectionView.swift`, `tests/photo_analysis_check.swift` | Apple's picker may download a selected iCloud photo; scene quality is not benchmarked |
| Meaning comes from the person | `mobile/PhotoReflection.swift`, `tests/phone_contract_check.swift` | Confirmation is a user statement, not independent verification |
| Confirmation and disclosure are separate | `mobile/AtlasContextExportView.swift`, `tests/PhoneReviewUITests.swift` | A person can still type identifying information into approved text |
| Agent retrieval is bounded and read-only | `atlas_context/core.py`, `atlas_context/mcp_server.py`, `tests/test_mcp.py` | Local purpose/audience labels are not client authentication |
| Corrections require current authorization | `atlas_context/review_demo.py`, `tests/test_review_demo.py` | Previous copies cannot be recalled; original phone sources are not watched |
| Source publishing excludes runtime data | `PUBLIC_FILES`, `PUBLIC_MEDIA`, `scripts/check_release.py` | Pattern/hash checks support manual review; they cannot identify all private prose |

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/check_release.py` for the maintained checks. Tests that need the optional MCP SDK skip when it is absent. [CI](https://github.com/niulengxiao/atlas-context/actions/workflows/ci.yml) also installs the package and runs the reviewer demo from outside the source checkout.

## 4. See the phone and model examples

- [Native screenshots and provenance](app-showcase.md): actual isolated app views with fictional records.
- [Phone setup and exact export contract](phone-handoff.md): selected photos, explanation, confirmation, full JSON review and explicit transfer.
- [Agent examples](agent-demo.md): limited actual Codex host checks; no personal data or broad quality claim.
- [Three context conditions](context-comparison.md): the same fictional request, actual outputs and citation checks, including a changed preference.
- [Privacy boundaries](../PRIVACY.md) and [validation scope](evidence.md): what the code enforces and what remains unverified.

## What another project can reuse

Use `PhoneBundle.swift` and the review view to create a minimal phone projection; use the Python validator/connector to bind it to a private session; use the single `search_life_context` MCP tool from a compatible host. The runtime does not require a Codex-specific model API. The [MIT license](../LICENSE) covers this code; a person's records are not licensed or published with it.

This is an early-stage project. External production use, broad adoption, physical-device transfer, encryption at rest, long-term preference learning and improved real-user usefulness are not established. The next contribution targets are source refresh, private local-model trials and measuring whether users recognize and find the resulting help useful. Report problems using fictional reproductions through [the reporting guide](reporting.md).
