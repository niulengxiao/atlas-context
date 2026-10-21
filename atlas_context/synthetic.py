"""An entirely fictional three-year story; all runtime files stay outside source."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3

from .cli import write
from .core import approve_local, query_context
from .importers import from_atlas_summary, from_media_catalog


# A fresh fictional story, independent of any user's records or old app fixtures.
# period, city, title, user-reviewed wording, attribution, selection state
STAGES = [
    ("2023-03", "Harbor City", "Learning photography", "In 2023, I began learning photography in Harbor City.", "manual", "approve"),
    ("2023-10", "Harbor City", "Keeping a sketchbook", "In late 2023, I kept a weekly sketchbook.", "manual", "approve"),
    ("2023-12", "Harbor City", "A cooking course", "In 2023, I took a short cooking course.", "manual", "approve"),
    ("2024-02", "River Town", "A community garden", "In 2024, I helped at a community garden in River Town.", "manual", "approve"),
    ("2024-05", "River Town", "Weekend walks", "In 2024, I kept notes from weekend walks.", "manual", "approve"),
    ("2024-09", "River Town", "Possible short trip", "A short trip in 2024 is suggested by the records but remains unconfirmed.", "inferred", "approve"),
    ("2024-11", "River Town", "A photography workshop", "In 2024, I attended a photography workshop in River Town.", "manual", "approve"),
    ("2025-01", "Hill City", "A photography portfolio", "In 2025, I assembled a photography portfolio in Hill City.", "manual", "approve"),
    ("2025-04", "Hill City", "A small exhibition", "In 2025, I shared a small photography exhibition with a local group.", "manual", "approve"),
    ("2025-08", "Hill City", "A year of small projects", "In 2025, I reflected on a year of small creative projects.", "manual", "approve"),
    ("2025-09", "Hill City", "Hidden fictional entry", "HIDDEN_SYNTHETIC_DETAIL", "manual", "hidden"),
    ("2025-10", "Hill City", "Unselected fictional entry", "UNSELECTED_SYNTHETIC_DETAIL", "manual", "exclude"),
]

MEDIA = [
    ("course", "2023-03-01", "A catalog entry records photography course notes from 2023."),
    ("workshop", "2024-11-01", "A catalog entry records a photography workshop handout from 2024."),
    ("portfolio", "2025-01-01", "A catalog entry records a photography portfolio checklist from 2025."),
    ("garden", "2024-02-01", "A catalog entry records a community garden planning note from 2024."),
]

SCENARIOS = [
    ("photography", False, 7),
    ("garden", False, 2),
    ("trip", False, 0),
    ("trip", True, 1),
    ("SYNTHETIC_OCR_SECRET", False, 0),
    ("HIDDEN_SYNTHETIC_DETAIL", False, 0),
    ("UNSELECTED_SYNTHETIC_DETAIL", False, 0),
    ("employer", False, 0),
]


def generate(destination):
    """Generate a new private runtime from public, fictional definitions only."""
    dest = Path(destination).expanduser().resolve()
    source = Path(__file__).resolve().parents[1]
    if dest == source or source in dest.parents:
        raise ValueError("Choose a runtime directory outside the source checkout")
    dest.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any(dest.iterdir()):
        raise ValueError("Choose a new empty directory; files are never replaced")
    visits = [{"cityId": "fictional-" + name.lower().replace(" ", "-"), "cityName": name}
              for name in ("Harbor City", "River Town", "Hill City")]
    summary = {"cityVisits": visits, "lifeStages": []}
    for index, (period, city, title, text, attribution, state) in enumerate(STAGES):
        summary["lifeStages"].append({"id": "fictional-stage-" + str(index), "title": title,
            "cityId": next(item["cityId"] for item in visits if item["cityName"] == city),
            "startDate": period + "-01T00:00:00Z", "source": attribution,
            "narrative": text, "hiddenInShare": state == "hidden"})
    catalog = dest / "synthetic-catalog.sqlite"
    db = sqlite3.connect(catalog)
    db.executescript("CREATE TABLE assets(id TEXT,path TEXT,name TEXT,capture_date TEXT,capture_confirmed INTEGER,ocr_text TEXT,active INTEGER);"
                     "CREATE TABLE notes(id TEXT,title TEXT,note TEXT);")
    for key, date, text in MEDIA:
        db.execute("INSERT INTO assets VALUES (?,?,?,?,?,?,?)",
                   ("fictional-" + key, "SYNTHETIC_LOCATOR_" + key, "generated-" + key + ".png", date, 1, "SYNTHETIC_OCR_SECRET", 1))
        db.execute("INSERT INTO notes VALUES (?,?,?)", ("fictional-" + key, "Fictional " + key, text))
    db.commit()
    db.close()
    before = hashlib.sha256(catalog.read_bytes()).hexdigest()
    records = from_atlas_summary(summary) + from_media_catalog(catalog, ["fictional-" + item[0] for item in MEDIA])
    review = []
    for index, (period, city, _, text, _, state) in enumerate(STAGES):
        if state == "approve":
            review.append({"record_id": records[index]["id"], "revision": records[index]["revision"],
                           "text": text, "period": period, "city": city, "evidence_label": "Fictional stage description"})
    for index, (_, date, text) in enumerate(MEDIA, start=len(STAGES)):
        review.append({"record_id": records[index]["id"], "revision": records[index]["revision"],
                       "text": text, "period": date[:7], "evidence_label": "Synthetic media catalog entry"})
    now = datetime.now(timezone.utc)
    grant = approve_local(records, review, purpose="write_short_bio", audience="synthetic_agent",
                          expires_at=(now + timedelta(hours=1)).isoformat(), now=now)
    scenarios = []
    for query, inferred, count in SCENARIOS:
        result = query_context(records, grant, purpose=grant["purpose"], audience=grant["audience"],
                               query=query, include_inferred=inferred, now=now)
        if len(result["items"]) != count:
            raise AssertionError("Synthetic retrieval scenario did not match its expected count")
        scenarios.append({"query": query, "include_inferred": inferred, "expected_count": count, "result": result})
    assert before == hashlib.sha256(catalog.read_bytes()).hexdigest()
    write(dest / "private-summary.json", summary)
    write(dest / "private-draft.json", records)
    write(dest / "private-review.json", review)
    write(dest / "private-grant.json", grant)
    write(dest / "private-server.json", {"draft": "private-draft.json", "grant": "private-grant.json",
                                         "purpose": grant["purpose"], "audience": grant["audience"]})
    write(dest / "scenario-results.json", scenarios)
    return {"synthetic_only": True, "draft_records": len(records), "approved_records": len(review),
            "default_outgoing_records": 13, "query_scenarios_passed": len(scenarios),
            "source_catalog_unchanged": True, "model_calls": 0, "network_requests": 0}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description="Generate a fictional three-year context demo")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(generate(args.output), indent=2))
    except (ValueError, OSError):
        parser.exit(1, "Choose a new empty runtime directory outside the source checkout.\n")


if __name__ == "__main__":
    main()
