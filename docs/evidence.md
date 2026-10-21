# Validation scope

This alpha separates runnable checks from product plans. There is no claim of broad adoption or a long public maintenance history.

| Evidence | Scope |
|---|---|
| Existing minimal demo | Four fictional drafts, four query scenarios; no model |
| Rich story generator | Sixteen drafts across three fictional years, eight retrieval scenarios |
| MCP SDK roundtrip | Real subprocess stdio connection; 16 assertions including revocation on the same connection |
| Legacy stdio check | Official SDK client negotiated 2025-11-25 and listed the one read-only tool |
| Unit tests | Core disclosure rules, read-only adapters, MCP boundaries and public release/history guard |
| Phone handoff | Strict schema, review hash, bounded lifetime, cloud opt-in, private runtime and revocation; fictional records only |
| Swift/Python contract | Foundation exporter compiled and its output accepted by Python; inference stays excluded by default |
| iOS companion | SwiftUI review/export component and fictional demo compile in an isolated simulator build; physical phone transfer remains unverified |
| iOS UI checks | Two local simulator tests passed: default export denied/cloud off; selected-only JSON, final acknowledgment and system file picker |
| App screenshots and walkthrough | Actual native views in an isolated synthetic harness; no native export integration |
| GitHub Actions | Core on Python 3.10/3.12; optional MCP integration on 3.11/3.12; see the actual workflow results |

The MCP tests use a protocol client, not a language model. Citation previews concatenate exact approved sentences. They do not evaluate the quality of an LLM-generated introduction, source entailment or resistance to instructions embedded in retrieved evidence.

Three actual Codex CLI host scenarios were completed using fictional tool inputs: a cited introduction, an unsupported employer question, and a revoked approval. The introduction used three citations matching returned user statements. In the two negative cases the model reported insufficient evidence or unavailable access. See the [curated host examples](agent-demo.md). An earlier isolated-config attempt failed and was not counted; the configured client succeeded after HTTP fallback. These are small manually inspected examples, not a general answer-quality or prompt-injection benchmark.

The native app source was not modified in place; only a build copy received the fictional harness. External photos, accounts and personal libraries are not needed for any public check. Real-user adoption, performance at large scale, encryption at rest and multi-user authentication remain unverified.

The subsequent phone feature is standalone public Swift source, not a modification to the private Atlas Memoir app. A fourth actual Codex host check used a newly generated fictional phone bundle with explicit phone and desktop cloud opt-in. The host called the read-only tool once, retrieved three user statements, cited all three and excluded the inferred trip. This verifies one configured summary path; it does not establish universal model quality, local-model deployment or host compliance with a local-only policy. See [phone workflow](phone-handoff.md).

Links: [synthetic data](demo.md), [MCP setup](mcp.md), [App provenance](app-showcase.md), [CI runs](https://github.com/niulengxiao/atlas-context/actions/workflows/ci.yml).
