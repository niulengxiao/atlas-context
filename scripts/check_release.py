"""Reject unlisted data, personal paths, credentials and unsafe Git history."""
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

FORBIDDEN_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".heif", ".tif", ".tiff", ".bmp",
                      ".mov", ".mp4", ".m4v", ".mkv", ".avi", ".webm", ".sqlite", ".db", ".csv", ".jsonl", ".log", ".aae"}
PATTERNS = [
    ("personal absolute path", re.compile(r"/(?:Users|home|Volumes)/" + r"[^/\s]+/")),
    ("access token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16}")),
    ("private key", re.compile("-----BEGIN " + r"(?:RSA |OPENSSH |EC )?PRIVATE KEY-----")),
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("embedded media", re.compile(r"data:(?:image|video)/[^;,]+;base64,")),
]


def validate_blob(name, data, allowed):
    errors = []
    path = PurePosixPath(name)
    if name not in allowed or path.is_absolute() or ".." in path.parts:
        errors.append("file is not on the public allowlist")
    if path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name.startswith(".env"):
        errors.append("runtime media/data or environment file")
    if len(data) > 1_000_000:
        errors.append("unexpectedly large source file")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return errors + ["non-text file"]
    if "\x00" in text:
        errors.append("binary content")
    for reason, pattern in PATTERNS:
        if pattern.search(text):
            errors.append(reason)
    return errors


def check(root):
    allowed = {line.strip() for line in (root / "PUBLIC_FILES").read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.startswith("#")}
    problems = []
    present = set()
    # Only bytecode caches and Git internals are excluded from working-tree review.
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_symlink():
            problems.append({"file": relative.as_posix(), "reason": "symlink"})
            continue
        if path.is_file():
            name = relative.as_posix()
            present.add(name)
            problems.extend({"file": name, "reason": reason} for reason in validate_blob(name, path.read_bytes(), allowed))
    for name in allowed - present:
        problems.append({"file": name, "reason": "allowlisted file is missing"})
    commits = 0
    if (root / ".git").exists():
        result = subprocess.run(["git", "rev-list", "--all"], cwd=root, capture_output=True, text=True, check=True)
        visited = set()
        for commit in result.stdout.splitlines():
            commits += 1
            manifest = subprocess.run(["git", "show", commit + ":PUBLIC_FILES"], cwd=root, capture_output=True)
            if manifest.returncode:
                problems.append({"file": "PUBLIC_FILES", "reason": "history: missing public allowlist"})
                historical_allowed = set()
            else:
                historical_allowed = {line.strip() for line in manifest.stdout.decode("utf-8").splitlines()
                                      if line.strip() and not line.startswith("#")}
            tree = subprocess.run(["git", "ls-tree", "-rz", "--full-tree", commit], cwd=root, capture_output=True, check=True).stdout
            for entry in tree.split(b"\0"):
                if not entry:
                    continue
                meta, raw_name = entry.split(b"\t", 1)
                mode, kind, oid = meta.decode().split()
                name = raw_name.decode("utf-8", "replace")
                if mode != "100644" or kind != "blob":
                    problems.append({"file": name, "reason": "non-regular file in Git history"})
                    continue
                if name not in historical_allowed:
                    problems.append({"file": name, "reason": "history: path not on that commit's public allowlist"})
                if (name, oid) in visited:
                    continue
                visited.add((name, oid))
                data = subprocess.run(["git", "cat-file", "blob", oid], cwd=root, capture_output=True, check=True).stdout
                problems.extend({"file": name, "reason": "history: " + reason} for reason in validate_blob(name, data, historical_allowed))
        # Protect an archive created from the index as well as from a commit.
        tracked = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout
        for raw_name in tracked.split(b"\0"):
            if raw_name and raw_name.decode("utf-8", "replace") not in allowed:
                problems.append({"file": raw_name.decode("utf-8", "replace"), "reason": "unlisted staged/tracked path"})
    return {"passed": not problems, "public_files": len(present), "git_commits_checked": commits, "problems": problems}


if __name__ == "__main__":
    result = check(Path(__file__).resolve().parents[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
