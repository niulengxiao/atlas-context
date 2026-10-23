"""Inspect approved context locally. This CLI neither calls a model nor uploads data."""
import argparse
import json
import os
from pathlib import Path
import sys

from .core import DEFAULT_CHARS, DEFAULT_RESULTS, approve_local, query_context
from .importers import from_atlas_summary, from_media_catalog


def read(path):
    if Path(path).stat().st_size > 10_000_000:
        raise ValueError("Prototype input exceeds 10 MB")
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main(argv=None):
    os.umask(0o077)
    parser = argparse.ArgumentParser(description="Experimental local review and approved-context preview")
    commands = parser.add_subparsers(dest="command", required=True)
    atlas = commands.add_parser("import-atlas")
    atlas.add_argument("--summary", required=True)
    atlas.add_argument("--output", required=True)
    media = commands.add_parser("import-media")
    media.add_argument("--catalog", required=True)
    media.add_argument("--id", action="append", required=True)
    media.add_argument("--output", required=True)
    approval = commands.add_parser("approve-local")
    approval.add_argument("--draft", required=True)
    approval.add_argument("--review", required=True)
    approval.add_argument("--purpose", required=True)
    approval.add_argument("--audience", required=True)
    approval.add_argument("--expires-at", required=True)
    approval.add_argument("--output", required=True)
    query = commands.add_parser("preview")
    query.add_argument("--draft", required=True)
    query.add_argument("--grant", required=True)
    query.add_argument("--purpose", required=True)
    query.add_argument("--audience", required=True)
    query.add_argument("--query", default="")
    query.add_argument("--include-inferred", action="store_true")
    query.add_argument("--max-results", type=int, default=DEFAULT_RESULTS)
    query.add_argument("--max-chars", type=int, default=DEFAULT_CHARS)
    args = parser.parse_args(argv)
    try:
        if args.command == "import-atlas":
            result = from_atlas_summary(read(args.summary))
        elif args.command == "import-media":
            result = from_media_catalog(args.catalog, args.id)
        elif args.command == "approve-local":
            result = approve_local(read(args.draft), read(args.review), purpose=args.purpose, audience=args.audience, expires_at=args.expires_at)
        else:
            result = query_context(read(args.draft), read(args.grant), purpose=args.purpose, audience=args.audience,
                                   query=args.query, include_inferred=args.include_inferred,
                                   max_results=args.max_results, max_chars=args.max_chars)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        write(args.output, result)
        print(json.dumps({"written_locally": True, "private_runtime_data": True}))
        return 0
    except (ValueError, OSError, PermissionError, KeyError, TypeError):
        print("Cannot complete this local operation: verify the draft, explicit review, grant and destination.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
