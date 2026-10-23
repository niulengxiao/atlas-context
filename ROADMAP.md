# Roadmap

The product direction is to help an agent understand a person's experiences, interests and preferences through selected everyday photo clues and that person's own explanations. The first product trial should connect one confirmed piece of context to one useful task, with sources, correction and disclosure control. This is a working plan, with no delivery dates or adoption claims. See the [fictional walkthrough and evaluation criteria](docs/product-direction.md).

## First product milestone: ask before interpreting

- [x] Extract bounded clues from up to five picker-selected photos using local Vision classification.
- [x] Ask a template question about meaning; accept the person's explanation, correction or decision to skip.
- [x] Keep tentative scene clues local; export only confirmed user statements, with confirmation invalidated by edits.
- [x] Separately review exact context for `personal_assistance`, with nothing selected and cloud off by default.
- [x] Compare one fixed fictional day-off request across no context, approved context and a separately reviewed correction; document actual host outputs and limits.
- [ ] Collect independent usefulness feedback and a controlled comparison on authorized private tasks.
- [ ] Record user corrections and source errors; verify that changed preferences do not silently reuse old authorization.

The alpha now adds selected-photo scene prompts and user explanations to the review/export/MCP foundation. A fictional café-work correction exercises the distinction between a photo and a preference. Generative photo interpretation, autonomous clarification dialogue, preference learning and a long-term profile remain future work. A complete personality inferred from photos is outside the scope of this milestone.

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

Additional adapters, larger-library retrieval, local-model evaluation, encryption at rest, changing life context and multiple clients. Inferring a complete personality, relationships or life history solely from photos, and autonomous life decisions, remain outside the project scope. The intended personal context is selected, explained and corrected by its owner.
