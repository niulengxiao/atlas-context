"""Reproducible synthetic integration example. Writes only to a new local directory."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sqlite3

from atlas_context.cli import write
from atlas_context.core import approve_local, query_context, resolve_evidence_local
from atlas_context.importers import from_atlas_summary, from_media_catalog


def run(destination):
    dest = Path(destination).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any(dest.iterdir()):
        raise ValueError("Choose an empty demo directory; existing files are never replaced")
    now = datetime.now(timezone.utc)
    summary = {"cityVisits": [{"cityId": "fictional-city", "cityName": "Example City"}], "lifeStages": [
        {"id": "fictional-stage-learning", "title": "Learning photography", "cityId": "fictional-city", "startDate": "2025-06-01T00:00:00Z",
         "source": "manual", "narrative": "Started learning photography. This is a synthetic example.", "hiddenInShare": False},
        {"id": "fictional-stage-guess", "title": "Possible short trip", "startDate": "2025-08-01T00:00:00Z", "source": "inferred", "hiddenInShare": False},
        {"id": "fictional-stage-private", "title": "Unshared fictional experience", "source": "manual", "narrative": "UNAPPROVED_FIXTURE_DETAIL", "hiddenInShare": True},
    ]}
    catalog = dest / "synthetic-catalog.sqlite"
    db = sqlite3.connect(catalog)
    db.executescript("CREATE TABLE assets(id TEXT,path TEXT,name TEXT,capture_date TEXT,capture_confirmed INTEGER,ocr_text TEXT,active INTEGER);"
                     "CREATE TABLE notes(id TEXT,title TEXT,note TEXT);")
    db.execute("INSERT INTO assets VALUES (?,?,?,?,?,?,?)", ("fictional-media-1", "SYNTHETIC_PRIVATE_LOCATOR", "generated-sample.png", "2025-06-01", 1, "UNAPPROVED_OCR_DETAIL", 1))
    db.execute("INSERT INTO notes VALUES (?,?,?)", ("fictional-media-1", "Course notes", "Synthetic study-material record"))
    db.commit()
    db.close()
    before = hashlib.sha256(catalog.read_bytes()).hexdigest()
    records = from_atlas_summary(summary) + from_media_catalog(catalog, ["fictional-media-1"])
    selections = [
        {"record_id": records[0]["id"], "revision": records[0]["revision"], "text": "In 2025, I started learning photography.", "period": "2025", "evidence_label": "User-written stage summary (synthetic)"},
        {"record_id": records[1]["id"], "revision": records[1]["revision"], "text": "There may have been a short trip in 2025; this is unconfirmed.", "period": "2025", "evidence_label": "System suggestion (synthetic)"},
        {"record_id": records[3]["id"], "revision": records[3]["revision"], "text": "The media catalog contains a record of photography study notes.", "period": "2025", "evidence_label": "Media catalog record (synthetic)"},
    ]
    grant = approve_local(records, selections, purpose="write_short_bio", audience="synthetic_agent", expires_at=(now + timedelta(hours=1)).isoformat(), now=now)
    args = {"purpose": "write_short_bio", "audience": "synthetic_agent", "now": now}
    exported = query_context(records, grant, **args)
    results = [
        {"case": "Search photography experience", "result": query_context(records, grant, query="photography", **args)},
        {"case": "Search unapproved OCR", "result": query_context(records, grant, query="UNAPPROVED_OCR_DETAIL", **args)},
        {"case": "Exclude inferred trip by default", "result": query_context(records, grant, query="trip", **args)},
        {"case": "Explicitly include inferred trip", "result": query_context(records, grant, query="trip", include_inferred=True, **args)},
    ]
    for value in ("SYNTHETIC_PRIVATE_LOCATOR", "UNAPPROVED_OCR_DETAIL", "UNAPPROVED_FIXTURE_DETAIL", "fictional-stage-learning"):
        assert value not in json.dumps(exported, ensure_ascii=False)
    local_evidence = resolve_evidence_local(records, grant, exported["items"][0]["citation"], **args)
    assert local_evidence["source_ref"] == "fictional-stage-learning"
    assert before == hashlib.sha256(catalog.read_bytes()).hexdigest()
    assert len(results[0]["result"]["items"]) == 2
    assert not results[1]["result"]["items"] and not results[2]["result"]["items"]
    assert results[3]["result"]["items"][0]["attribution"] == "inferred"
    write(dest / "private-draft.json", records)
    write(dest / "private-grant.json", grant)
    write(dest / "approved-context.json", exported)
    write(dest / "scenario-results.json", results)
    grant["active"] = False
    try:
        query_context(records, grant, **args)
    except PermissionError:
        revoked = True
    else:
        revoked = False
    assert revoked
    return {"synthetic_only": True, "draft_records": len(records), "default_outgoing_items": len(exported["items"]),
            "private_search_blocked": True, "inference_excluded_by_default": True, "revocation_checked": revoked,
            "source_catalog_unchanged": True, "model_calls": 0, "network_requests": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
