# Validation scope

This alpha separates runnable checks from product plans. There is no claim of broad adoption or a long public maintenance history.

The [personal-agent direction](product-direction.md) now has a small implementation: selected-photo scene prompts, user explanations, separate confirmation/disclosure and contextual assistance through MCP. The checks establish those bounded mechanics. They do not establish generative photo understanding, long-term preference learning or improved real-user decision quality.

| Evidence | Scope |
|---|---|
| Existing minimal demo | Four fictional drafts, four query scenarios; no model |
| Rich story generator | Sixteen drafts across three fictional years, eight retrieval scenarios |
| MCP SDK roundtrip | Real subprocess stdio connection; 16 assertions including revocation on the same connection |
| Legacy stdio check | Official SDK client negotiated 2025-11-25 and listed the one read-only tool |
| Unit tests | 49 Python tests passed with the MCP extra: core disclosure, adapters, corrected-preference task purpose, reviewer lifecycle, MCP and publication/history checks |
| Reviewer walkthrough | Nine reproducible core checks, zero model/network calls; old session revoked and new preference separately reviewed |
| Package installation | Built wheel inspected against public Python sources; installed reviewer command runs outside the source checkout |
| Phone handoff | Strict schema, review hash, bounded lifetime, cloud opt-in, private runtime and revocation; fictional records only |
| Swift/Python contract | Foundation exporter compiled; actual confirmed reflection output accepted by Python under `personal_assistance`; only text/attribution exported |
| Reflection state | Swift checks require nonblank bounded wording, invalidate confirmation on edits and keep scene questions out of exported records |
| Local image processing | Apple Vision invoked on procedural pixels; preview metadata excludes invented GPS/EXIF marker; invalid/oversized bytes rejected; scene correctness is not benchmarked |
| iOS companion | Photo-reflection and review/export views compile in an isolated simulator build; physical phone transfer remains unverified |
| iOS UI checks | Four public test cases passed across local simulator runs: default denial/cloud off, confirmation before separate disclosure, session clearing, and selected-only JSON/final acknowledgment/system save picker. Off-screen lookup and changed picker-control assertions were corrected during QA. CI does not run these UI cases. |
| Selected-photo integration | A focused local UI harness selected an explicitly identified procedural image through the real system picker, ran the local processing path and verified blank wording, disabled confirmation and no authorized export. No personal library was used. |
| App screenshots and walkthrough | Actual native views in an isolated synthetic harness; no native export integration |
| GitHub Actions | Core on Python 3.10/3.12; optional MCP integration on 3.11/3.12; see the actual workflow results |

The MCP tests use a protocol client, not a language model. Citation previews concatenate exact approved sentences. They do not evaluate the quality of an LLM-generated introduction, source entailment or resistance to instructions embedded in retrieved evidence.

Three actual Codex CLI host scenarios were completed using fictional tool inputs: a cited introduction, an unsupported employer question, and a revoked approval. The introduction used three citations matching returned user statements. In the two negative cases the model reported insufficient evidence or unavailable access. See the [curated host examples](agent-demo.md). An earlier isolated-config attempt failed and was not counted; the configured client succeeded after HTTP fallback. These are small manually inspected examples, not a general answer-quality or prompt-injection benchmark.

The native app source was not modified in place; only a build copy received the fictional harness. External photos, accounts and personal libraries are not needed for any public check. Real-user adoption, performance at large scale, encryption at rest and multi-user authentication remain unverified.

The subsequent phone feature is standalone public Swift source, not a modification to the private Atlas Memoir app. A fourth actual Codex host check used a newly generated fictional phone bundle with explicit phone and desktop cloud opt-in. The host called the read-only tool once, retrieved three user statements, cited all three and excluded the inferred trip. This verifies one configured summary path; it does not establish universal model quality, local-model deployment or host compliance with a local-only policy. See [phone workflow](phone-handoff.md).

A fifth host example used the actual Swift-serialized, fictional reflection statements under `personal_assistance`. With explicit test-only cloud opt-in on both sides, Codex retrieved two user statements, cited both, rejected a café-hopping hobby inference and proposed two flexible day-off options. It asked whether the stated preference still applied. This checks one configured corrected-preference path; there is no no-context comparison or independent usefulness score. See [the curated example](agent-demo.md#personal-assistance-after-a-corrected-photo-interpretation).

Three subsequent fresh-host conditions used the same fictional day-off request without context, with original approved context and with a newly reviewed correction. The installed `0.4.0a2` package supplied two records in each connected condition; all four citation IDs matched actual tool items. The baseline claimed no specific preference evidence. The connected outputs followed the stated quiet-walk or indoor-workshop preference and retained the café-work correction. These bring the documented host examples to eight. They do not establish improved real-user usefulness or erasure of old conversation history. See [complete outputs, conditions and limits](context-comparison.md).

Links: [synthetic data](demo.md), [MCP setup](mcp.md), [App provenance](app-showcase.md), [CI runs](https://github.com/niulengxiao/atlas-context/actions/workflows/ci.yml).
