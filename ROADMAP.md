# Roadmap

The first complete user journey is: select a small set of life records, review the exact context for one writing task, retrieve it with citations, then correct or revoke it. This is a working plan, with no delivery dates or adoption claims.

## Available: local policy and adapter prototype

- [x] Atlas summary-shaped projection adapter; reject full backup envelopes.
- [x] Explicitly selected media catalog rows, read-only.
- [x] Exact-wording local approval with purpose, audience and expiry.
- [x] Retrieval over approved projections only; inference excluded by default.
- [x] Draft revision checks, local revocation and opaque citations.
- [x] Synthetic demo, 17 unit tests and public-source release guard.
- [x] English and Chinese documentation.

## Next: a usable local review flow

- [ ] Define and version a selective Atlas export contract, separate from full backup and social sharing.
- [ ] Add a native export entry point using fictional data first.
- [ ] Provide a local review screen for exact text, source attribution and optional metadata.
- [ ] Display purpose, recipient and expiry before approval.
- [ ] Refresh drafts when connected sources change; require re-review of affected records.
- [ ] Support correction and revocation through the local interface.

Acceptance: a user can select one fictional stage, correct it, inspect all outgoing text and approve it without editing JSON. Changing its source removes it from retrieval until re-reviewed.

## Then: one read-only MCP tool

- [ ] Implement the official SDK transport described in [MCP_PLAN.md](MCP_PLAN.md).
- [ ] Bind the grant and client policy in trusted configuration; do not let a model choose filesystem paths or its own audience.
- [ ] Re-check expiry, revocation and current draft revisions on each call.
- [ ] Exercise the actual client/host trust boundary, including adversarial retrieved text.
- [ ] Keep approval, source resolution and original media access outside the tool interface.

Acceptance: a real client retrieves only approved context, labels inference accurately and cannot read after revocation or expiry. No claim of MCP support before this runs end to end.

## Then: evaluate one writing task

- [ ] Use fictional life histories with supported, uncertain and unavailable details.
- [ ] Check whether generated introductions cite the right records and avoid inventing missing events.
- [ ] Measure corrections and the time needed to prepare useful context.
- [ ] After the synthetic path works, offer a user-controlled local trial with a small, explicitly selected real subset.

Any real-data cloud trial requires a separate explicit decision about the exact outgoing text. Personal trial records and outputs stay out of the public repository.

## Later, if these milestones justify it

Additional adapters, larger-library retrieval, local-model evaluation, encryption at rest and multiple clients. Full life understanding, personality judgments, relationship inference and autonomous life decisions are outside the initial project scope.
