# Local MCP setup

For a phone export, start with [Phone to Agent](phone-handoff.md). Its generated `session/private-server.json` uses the same server configuration below. Default phone sessions are local-only; a cloud host requires explicit phone and desktop opt-in for the reviewed text. Read [PRIVACY.md](../PRIVACY.md) before connecting personal data.

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
  "arguments": {"query": "photography", "include_inferred": false, "max_results": 5, "max_chars": 6000}
}
```

Only these four arguments are accepted, all optional. The query is limited to 256 characters and 12 whitespace-separated terms; `include_inferred` must be a JSON boolean. `max_results` is an integer from 1 to 50 (default 10); `max_chars` is an integer from 2,500 to 20,000 (default 6,000). Booleans, strings and fractional numbers are rejected for budgets. Extra arguments, including file paths, purpose labels or grant selectors, are rejected.

Nonempty queries use NFKC/case normalization, whole-word matching, a small English function-word list and overlapping Han bigrams. Any matching term qualifies; more distinct matches rank first, with review order breaking ties. This permits partial matches, so returned evidence need not answer the whole question. There is no stemming, synonym expansion, translation or semantic index. Private titles, OCR, locations and unapproved wording never influence search or ranking. Evidence labels are returned if reviewed but not searched.

An empty/whitespace query requests an overview in review order. A punctuation-only or function-word-only nonempty query does not become an overview. Both modes obey result and character budgets, preserve exact wording and return `retrieval.mode`, `max_results`, `max_chars`, `returned_chars` and `has_more`. The character budget sums reviewed text, period, city and evidence label values, not JSON/protocol overhead. `has_more` concerns eligible authorized matches only. It does not expose private-source counts. Refine the query if it is true; a capped overview is not a complete life history. A larger budget never expands approval, attribution or expiry.

The response also has opaque citations, source/attribution, coverage and untrusted-evidence handling guidance. Phone imports now use the generic source `phone_export`, because their v1 file does not authenticate a producer. Explicit Atlas-summary adapter records retain `atlas_memoir`; neither source string proves identity or truth. Existing v1 phone files remain accepted; regenerate old phone sessions to obtain the corrected source label.

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
