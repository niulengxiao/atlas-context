# A real Codex client example

This is a small, manually inspected host check, not an adoption claim or a model benchmark. All tool data was generated from the fictional three-year fixture.

## Cited introduction

A real Codex CLI session called `search_life_context` with `query=photography` and `include_inferred=false`. The server returned seven reviewed records. The client produced:

> Based solely on my personal statements, without independent verification here, I began learning photography in Harbor City in 2023 [E-eb51639ca9627fb6]. I attended a photography workshop in River Town in 2024 [E-ab9167b976cd6727]. I assembled a photography portfolio in Hill City in 2025 [E-021eefc0d6cb30e2].

Each of the three citations maps to a returned `user_statement` record. The introduction was inspected against those records; the project does not automatically prove semantic entailment.

## Reproduce locally

Generate a new fictional runtime, install the MCP extra in a separate virtual environment, and configure your host as described in [MCP setup](mcp.md). Ask the host to query photography and write three sentences using only user statements, with a returned citation for each factual sentence. Do not infer employment, personality, nationality or relationships. Model wording and opaque citation IDs will vary.

Connecting a cloud host sends the returned context to that service. The test used fictional tool inputs only. Review any real outgoing text before connecting your own archive.

## Limits

The configured client worked after an HTTP fallback from WebSocket TLS failures. An earlier isolated-config attempt reported the tool unavailable; it was not counted as a success. The independent SDK test suite verifies both current and legacy stdio, including same-connection revocation. Host results may vary with client configuration and model version. This example does not establish prompt-injection resistance, adoption, or complete life understanding.

## Two additional live-host checks

The same configured Codex client was also exercised in two new sessions. Each made one actual MCP tool call:

| Case | Observed response |
|---|---|
| unsupported | The approved evidence does not establish an employer. |
| revoked | Atlas Context’s “photography” search is unavailable because a current matching local approval and valid draft are required. |

The employer query returned an empty approved evidence set. Before the revoked case, the trusted local test changed the synthetic grant to inactive; the tool returned an error and the model disclosed no life details. Same-connection invalidation is covered separately by the automated SDK test. These three manually inspected cases are examples, not a statistical model evaluation.
