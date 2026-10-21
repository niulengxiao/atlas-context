"""One-way private drafts, with no implicit agent permission.

Atlas input is a summary-shaped projection, not the app's complete backup.
The app-side selective exporter and backup integrity checks are future work.
"""
from pathlib import Path
from datetime import datetime
import sqlite3

from .core import make_record


def month(value):
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return parsed.strftime("%Y-%m")
        except ValueError:
            pass
    return None


def from_atlas_summary(summary):
    if not isinstance(summary, dict) or "journeyArchive" in summary or "payload" in summary:
        raise ValueError("Expected an explicit summary projection, not a complete Atlas backup")
    visits = {visit["cityId"]: visit for visit in summary.get("cityVisits", [])}
    records = []
    for stage in summary.get("lifeStages", []):
        visit = visits.get(stage.get("cityId"), {})
        records.append(make_record(source="atlas_memoir", source_ref=stage["id"],
                                   attribution="user_statement" if stage.get("source") == "manual" else "inferred",
                                   title=stage.get("title", ""), period=month(stage.get("startDate")),
                                   city=visit.get("cityName"), private_text=stage.get("narrative") or "",
                                   hidden=stage.get("hiddenInShare", False)))
    return records


def from_media_catalog(database, selected_ids):
    if not selected_ids or len(selected_ids) > 200:
        raise ValueError("Explicitly select between 1 and 200 catalog items")
    path = Path(database).expanduser().resolve(strict=True)
    db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    try:
        records = []
        for identifier in dict.fromkeys(selected_ids):
            row = db.execute("SELECT a.id,a.path,a.name,a.capture_date,a.capture_confirmed,a.ocr_text,n.title,n.note "
                             "FROM assets a LEFT JOIN notes n USING(id) WHERE a.id=? AND a.active=1", (identifier,)).fetchone()
            if row is None:
                raise ValueError("A selected media record is unavailable")
            records.append(make_record(source="local_media_library", source_ref=row["id"], attribution="recorded",
                                       title=row["title"] or row["name"], period=month(row["capture_date"]) if row["capture_confirmed"] else None,
                                       private_text="\n".join(value for value in (row["note"], row["ocr_text"]) if value),
                                       locator=row["path"]))
        return records
    finally:
        db.close()
