# Local MCP setup

Atlas Context exposes one read-only tool over **stdio**, implemented with the official Python SDK, pinned to `mcp==2.3.0`. MCP support requires Python 3.11+; the core and fixture generator still support Python 3.10.

```sh
python3 -m venv ../atlas-env
../atlas-env/bin/python -m pip install '.[mcp]'
../atlas-env/bin/python -m atlas_context.synthetic --output ../atlas-host-demo
../atlas-env/bin/python -m atlas_context.mcp_server --config ../atlas-host-demo/private-server.json
```

The last command speaks protocol messages on stdin/stdout; it is normally launched by an MCP host, not typed into a chat. Stop a manually started server before configuring the host. No HTTP port, account login, model call or API key is part of this server.

## Tool contract

```json
{
  "name": "search_life_context",
  "arguments": {"query": "photography", "include_inferred": false}
}
```

Only these two arguments are accepted. The query is limited to 256 characters and 12 whitespace-separated terms; `include_inferred` must be a JSON boolean. Extra arguments, including file paths, purpose labels or grant selectors, are rejected. The response has structured context, opaque citations, attribution, coverage and untrusted-evidence handling guidance.

There are no tools to approve a grant, change records, resolve a citation to a source location, read raw OCR or open media. A trusted local UI can resolve citations separately.

## Trusted host configuration

The generator writes `private-server.json` next to its runtime files. The local administrator chooses the draft and grant files plus purpose and audience. Relative paths resolve against the configuration file's directory, not the model or the process working directory. The server binds these choices at startup and re-reads the draft and grant on **every call**.

Configure your host to launch the virtual environment's Python with these arguments:

```text
-m atlas_context.mcp_server --config <absolute-path-to-private-server.json>
```

For a Codex CLI or desktop configuration, the equivalent template is:

```toml
[mcp_servers.atlas_context]
command = "<absolute-path-to-virtualenv-python>"
args = ["-m", "atlas_context.mcp_server", "--config", "<absolute-path-to-private-server.json>"]
enabled = true
```

Replace placeholders locally. The selected environment must have this package and its MCP extra installed. Keep real configuration paths out of public issues and screenshots. Protocol interoperability with SDK clients is verified; see [validation scope](evidence.md) for the separate status of actual model/host evaluation.

## Access and privacy boundaries

Purpose and audience remain local labels, not authenticated identities. Anyone able to edit the config, draft or grant is trusted by this prototype. Run it within your operating system's local access controls. This is a single-user local integration, not a public multi-user service.

Revocation and expiry stop subsequent tool reads. A changed imported draft revision removes the affected record until re-review. The server does not watch the original native app or source catalog; integrations must refresh drafts when sources change. It does not keep raw query, result or source-path logs. The host may have its own logs and caches.

Connecting a cloud model sends the returned text off the device. Preview it first. Revocation cannot recall text already received. A citation supports local inspection, not automatic proof of truth. Retrieved instructions remain untrusted data; this release does not establish model prompt-injection resistance.

References: [official Python SDK](https://py.sdk.modelcontextprotocol.io/), [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
