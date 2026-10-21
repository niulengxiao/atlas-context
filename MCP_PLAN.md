# Proposed MCP boundary — not implemented

Use the official MCP SDK rather than maintaining a custom protocol stack. Register one initial tool, `search_life_context`, with model-supplied arguments limited to a bounded search string and `include_inferred` (default false). Bind its grant, purpose and audience in trusted local configuration. Re-read the current grant on each call; do not serve a stale cache after expiry, revocation or source revision changes.

The tool returns only the approved context structure from `query_context`. Its annotations should describe read-only, idempotent local retrieval. Annotations describe behavior; they do not implement access control.

Do not expose local approval, grant editing, evidence-location resolution, file opening, database selection, original image retrieval, raw OCR retrieval or source modification as tools in the first version. A user can inspect the opaque citations in the native/local review interface.

The host must treat retrieved text as untrusted data and keep it separate from system instructions. Provide a preview of the exact outgoing text before connecting a cloud model. Access logging should record minimal local grant/result metadata rather than raw questions, memories or source paths.

References:

- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
