# Roadmap

The first complete user journey is: select a small set of life records, review the exact context for one writing task, retrieve it with citations, then correct or revoke it. This is a working plan, with no delivery dates or adoption claims.

## Available: local policy and adapter prototype

- [x] Atlas summary-shaped projection adapter; reject full backup envelopes.
- [x] Explicitly selected media catalog rows, read-only.
- [x] Exact-wording local approval with purpose, audience and expiry.
- [x] Retrieval over approved projections only; inference excluded by default.
- [x] Draft revision checks, local revocation and opaque citations.
- [x] Minimal, three-year and phone-handoff fictional demos, with public-source/history guard.
- [x] English and Chinese documentation.
- [x] Native product screenshots and walkthrough from an isolated fictional harness.
- [x] Pinned core and MCP GitHub Actions workflows.

## Available: selective phone review and file handoff

- [x] Define and version a selective phone export contract, separate from full backup and social sharing.
- [x] Add a reusable native review/export component and standalone fictional companion app.
- [x] Provide exact text review, source attribution and optional coarse metadata; no selection by default.
- [x] Display purpose, disclosure mode and expiry before export, with cloud access off by default.
- [x] Require exact-file desktop review, bind a private session and generate summary instructions.
- [x] Provide a desktop revocation command and check existing-connection denial.
- [ ] Integrate the component in production Atlas Memoir and verify physical-device transfer.
- [ ] Refresh drafts when connected sources change; require re-review of affected records.
- [ ] Support correction and revocation through a persistent native connection interface.

The standalone component lets a user select and edit fictional text, inspect the complete JSON and export without hand-editing JSON. Desktop connection is explicit. Original phone changes do not refresh old exports; revoke and re-export. Automatic refresh and production app integration remain pending. See [phone handoff](docs/phone-handoff.md).

## Available: one read-only MCP tool

- [x] Implement official SDK 2.3.0 stdio transport; verify current and legacy SDK clients.
- [x] Bind the grant and client policy in trusted configuration; do not let a model choose filesystem paths or its own audience.
- [x] Re-check expiry, revocation and current draft revisions on each call.
- [ ] Exercise the actual client/host trust boundary, including adversarial retrieved text.
- [x] Keep approval, source resolution and original media access outside the tool interface.

Verified with the official SDK over a real subprocess connection. Actual model-host tests have a smaller documented scope; see [evidence](docs/evidence.md). Client labels are still local policy labels, not multi-user authentication.

## Then: evaluate one writing task

- [x] Use fictional life histories with supported, uncertain and unavailable details.
- [x] Try a real Codex client on a cited introduction using fictional approved context.
- [x] Observe actual host responses to an unsupported employer query and a revoked grant.
- [ ] Check whether generated introductions cite the right records and avoid inventing missing events.
- [ ] Measure corrections and the time needed to prepare useful context.
- [ ] After the synthetic path works, offer a user-controlled local trial with a small, explicitly selected real subset.

Any real-data cloud trial requires a separate explicit decision about the exact outgoing text. Personal trial records and outputs stay out of the public repository.

## Later, if these milestones justify it

Additional adapters, larger-library retrieval, local-model evaluation, encryption at rest and multiple clients. Full life understanding, personality judgments, relationship inference and autonomous life decisions are outside the initial project scope.
