# A fictional three-year story

Run from the repository root with Python 3.10+:

```sh
python3 -m atlas_context.synthetic --output ../atlas-story-demo
```

The output directory must be outside this checkout and empty. The generator never overwrites existing files. It creates 12 fictional Atlas stage projections and 4 generated media catalog records, covering photography, sketching, cooking, gardening and an unconfirmed trip. Fictional city labels are Harbor City, River Town and Hill City. No photos, real life history or external service are needed.

Ten stage records and four media records receive a scripted sample approval; this is permitted only because the exact fixture wording is fictional. One approved stage is inferred, so default retrieval returns 13 records. A hidden stage and an unselected stage are never approved. The sample grant expires one hour after generation.

## Expected retrieval

| Query | Include inference | Expected records |
|---|---|---:|
| `photography` | false | 7 |
| `garden` | false | 2 |
| `trip` | false | 0 |
| `trip` | true | 1, labeled `inferred` |
| `SYNTHETIC_OCR_SECRET` | false | 0 |
| `HIDDEN_SYNTHETIC_DETAIL` | false | 0 |
| `UNSELECTED_SYNTHETIC_DETAIL` | false | 0 |
| `employer` | false | 0 |

No employer is recorded. A host should state that the selected evidence is insufficient, rather than infer a profession from hobbies or geography. The retrieval layer returns `no_authorized_evidence`; the model's response behavior needs separate evaluation.

## A real MCP roundtrip

Using Python 3.11+ with the optional MCP extra installed:

```sh
python3 -m atlas_context.mcp_demo --output ../atlas-mcp-demo
```

This launches the server as a subprocess and uses the official SDK client to list its tools and perform real protocol calls. It checks the eight retrieval scenarios plus schema restrictions, strict booleans, a changed draft, expiry, purpose/audience mismatch and revocation. Revocation is checked on the same connection; the client disables its optional cache. The tested server also supports the SDK's legacy 2025-11-25 stdio negotiation.

The generated `mcp-transcript.json` contains synthetic responses and a citation preview assembled from exact reviewed sentences. It is not an LLM-generated biography. The sample grant is left revoked at the end: use the basic generator in a new directory when preparing a host connection.

## Runtime files stay private

The generator writes its summary, drafts, review, grant, host config, SQLite fixture and transcript outside the source tree. The public repository ships the generator, not these runtime files. Keep that separation when replacing fictional inputs with real records. Review the exact text before any cloud-model connection.
