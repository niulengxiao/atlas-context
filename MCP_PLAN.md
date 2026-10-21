# MCP boundary — implemented in the experimental alpha

The read-only stdio server and official SDK client roundtrip are now implemented. See [setup and enforced boundaries](docs/mcp.md) and [validation scope](docs/evidence.md). The native exporter and model-host answer evaluation remain separate work.

The implementation uses the official MCP SDK rather than a custom protocol stack. It registers one tool, `search_life_context`, with model-supplied arguments limited to a bounded search string and `include_inferred` (default false). Its grant, purpose and audience are bound in trusted local configuration. It re-reads the current grant on each call and does not serve a stale cache after expiry, revocation or draft revision changes.

The tool returns only the approved context structure from `query_context`. Its annotations should describe read-only, idempotent local retrieval. Annotations describe behavior; they do not implement access control.

Do not expose local approval, grant editing, evidence-location resolution, file opening, database selection, original image retrieval, raw OCR retrieval or source modification as tools in the first version. A user can inspect the opaque citations in the native/local review interface.

The host must treat retrieved text as untrusted data and keep it separate from system instructions. Provide a preview of the exact outgoing text before connecting a cloud model. Access logging should record minimal local grant/result metadata rather than raw questions, memories or source paths.

References:

- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
