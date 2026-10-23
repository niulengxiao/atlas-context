# Contributing

Atlas Context is an experimental local prototype. Small improvements to review behavior, source attribution, synthetic examples and documentation are useful first contributions. Please discuss changes to disclosure boundaries before broadening what a query can return.

Start with the [five-minute reviewer guide](docs/reviewer-guide.md). Use the [reporting guide](docs/reporting.md) to choose a public fictional bug report or the private privacy/security channel.

## Reproduce with fictional data

Use Python 3.10+ and the standard library. Run from the repository root:

```sh
python3 demo.py --output ../atlas-contributor-runtime
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
```

Choose a new empty runtime directory outside the checkout. Keep environment directories outside it too: the release guard checks unlisted working-tree files even when Git ignores them.

For a bug report, describe the Python version, command, expected behavior and a minimal fictional fixture. Do not attach a real archive, photo, catalog, OCR text, grant, context export or screenshot of personal records. Check logs and error messages for private information before sharing them.

## Preserve the boundaries

- Importing a record must not approve its disclosure.
- Search must operate on the approved projection, not the whole private library followed by filtering.
- Preserve attribution. Approval to share does not turn a system inference into a fact.
- Do not return original handles, private locations or raw media through the retrieval interface.
- Keep local review, grant editing and local evidence resolution outside the proposed agent tool.
- Source freshness needs an explicit integration mechanism; revision checks alone do not watch external sources.

Add focused synthetic tests when changing these behaviors. Documentation-only changes do not require new tests.

## Before contributing or packaging

Review every changed file for private content. Add any intentional public source file to `PUBLIC_FILES`, then run the release guard. Do not add runtime files to the allowlist to silence a failure. Use generated fixtures in tests instead of committed catalogs or personal examples.

The guard detects selected file types, common credential/path patterns and historical source files when Git is present. A passing result is not proof that prose or screenshots contain no private information. Inspect the final diff and exact archive contents too.

The only media exception is an exact `PUBLIC_MEDIA` hash for a manually reviewed synthetic asset under `docs/assets/`. Review both visible content and metadata before adding or updating a digest. PNG text and EXIF metadata are rejected even with a matching hash. Do not use this exception for real screenshots, media libraries or logs. MCP tests require Python 3.11+ and `pip install '.[mcp]'`; core checks remain dependency-free on Python 3.10+.

Changes are contributed under the repository's MIT license. Keep the README and roadmap clear about which features run today and which are proposed.
