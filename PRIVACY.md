# Privacy and disclosure boundaries

**Your life records are private runtime data. Open source publishes the software and fictional examples, not your archive.** The phone component and Python connector have no upload client, analytics, model API, account identifier or network listener. The MCP server uses local stdio. Your chosen Agent host, file provider and model have their own behavior and retention policies.

## What you choose before export

The iOS component selects nothing by default. You choose individual records, edit the exact outgoing sentences, optionally include a year/month or city, pick a task and review the entire JSON before saving. City and period fields default off. Inferred records keep their attribution and are excluded from default Agent retrieval.

The versioned phone contract permits only reviewed text, attribution and optional coarse period, city and evidence label, plus temporary export/task metadata. It rejects extra fields, including original photo IDs, filesystem locations, GPS coordinates, raw OCR, thumbnails, device identifiers and full backup envelopes. It limits a bundle to 50 records, 20,000 text characters and 256 KB. **These structural restrictions do not redact sentences.** Names, precise locations or sensitive facts typed into text will still be disclosed unless you remove them.

The companion demo has no Photos permission or scanner. An embedding app must apply its own photo permissions and local processing rules before offering draft text. Hidden Atlas stages must be excluded by the embedding adapter; social-sharing permissions are not Agent consent.

## What happens on your computer

Transfer the reviewed JSON to a trusted computer, for example with AirDrop. USB connection alone grants no access. Review it locally, then acknowledge the exact file hash. This catches a changed file between review and import; it is not a signature or authenticated proof that a person approved it. Anyone able to edit trusted local policy files can alter access.

The connector writes a new private runtime directory outside Git, with owner-only directory/file modes on POSIX systems. It never replaces an existing session. These modes are not encryption and do not protect against the account owner, malware, backups or a privileged process.

The read-only MCP tool exposes approved wording and opaque citations. It cannot approve exports, choose files, read originals, edit records or extend access. Trusted configuration fixes the purpose and audience; they are local labels, not authenticated identities. Each tool call rechecks approval, expiry and imported draft revisions. Original phone data is not watched: a correction or deletion on the phone does not automatically update a previously exported copy. Revoke the desktop session and prepare a newly reviewed export after changes.

## Local models and cloud models

The default disclosure mode is `local_only`. Use a local model and host that honors that policy. There is no verified local-model deployment bundled here.

Cloud use requires two explicit settings: `cloud_allowed` on the phone and `--allow-cloud` on the desktop. Connecting the resulting server to a cloud host lets that host send approved text and prompts to its provider. **The MCP server cannot authenticate the host, inspect where it runs, or prevent a host with filesystem access from copying data.** A policy label is not an upload firewall. Review the actual model provider's retention and training settings before sending personal text.

Saving to iCloud Drive, another Files provider or a shared folder may also transfer the JSON independently of any Agent. Choose a local destination when required and check OS sharing settings. The exported JSON is plaintext; anyone who receives a copy can read it.

## Expiry, revocation and deletion

Phone exports can live for at most 24 hours; the provided interface chooses one hour. Desktop sessions expire at the earlier of the phone expiry and one hour after connection. Expiry is enforced on future Atlas tool reads; it does not make saved plaintext unreadable.

Run `python3 -m atlas_context.phone revoke --runtime ../atlas-private-session` to block future reads, including on an existing MCP connection. Revocation cannot erase received files, chat histories, provider copies, screenshots or earlier answers. Delete local runtime files and transferred copies separately using your OS. Renew access only by reviewing a new export.

## Limits and reporting

The project has no claim of end-to-end encryption, zero-knowledge storage, secure hardware attestation, multi-user isolation, semantic redaction or complete prompt-injection protection. A summary covers selected evidence, not an objective account of a whole life; missing evidence is not evidence that something never happened. Avoid unsupported judgments about health, personality, relationships or identity.

Report problems with synthetic reproductions. Do not post private exports or secrets in public issues. The publication guard checks known secret/path patterns, exact public file lists and reviewed media hashes; manual review is still required. See [validation scope](docs/evidence.md) and [contribution guidance](CONTRIBUTING.md).
