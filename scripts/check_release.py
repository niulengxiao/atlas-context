"""Reject unlisted data, personal paths, credentials and unsafe Git history."""
import json
import binascii
import hashlib
from pathlib import Path, PurePosixPath
import re
import subprocess
import struct
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


def parse_media(text):
    """Explicit reviewed asset hashes, never a general media-file exception."""
    media, errors = {}, []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([a-f0-9]{64})  (docs/assets/[a-z0-9-]+\.(?:png|mp4))", line)
        if not match or (match and match[2] in media):
            errors.append("invalid or duplicate reviewed-media entry")
        else:
            media[match[2]] = match[1]
    return media, errors


def validate_media(name, data, expected):
    errors = []
    if hashlib.sha256(data).hexdigest() != expected:
        errors.append("reviewed-media hash mismatch")
    if len(data) > 8_000_000:
        errors.append("reviewed media exceeds 8 MB")
    if name.endswith(".png"):
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            return errors + ["invalid PNG"]
        offset, kinds = 8, []
        while offset + 12 <= len(data):
            size = struct.unpack(">I", data[offset:offset + 4])[0]
            kind = data[offset + 4:offset + 8]
            end = offset + 12 + size
            if end > len(data):
                return errors + ["truncated PNG"]
            if kind not in {b"IHDR", b"sRGB", b"gAMA", b"cHRM", b"pHYs", b"iCCP", b"IDAT", b"IEND"}:
                errors.append("PNG contains unapproved metadata")
            if binascii.crc32(data[offset + 4:end - 4]) & 0xffffffff != struct.unpack(">I", data[end - 4:end])[0]:
                errors.append("invalid PNG checksum")
            kinds.append(kind)
            offset = end
            if kind == b"IEND":
                break
        if not kinds or kinds[0] != b"IHDR" or kinds[-1] != b"IEND" or offset != len(data):
            errors.append("invalid PNG structure or trailing data")
    elif name.endswith(".mp4"):
        if len(data) < 12 or data[4:8] != b"ftyp":
            errors.append("invalid MP4 container")
        if any(marker in data for marker in (b"com.apple.quicktime.location", b"\xa9xyz")):
            errors.append("video contains location metadata")
    else:
        errors.append("unsupported reviewed-media type")
    for reason, pattern in PATTERNS:
        if pattern.search(data.decode("latin-1")):
            errors.append(reason)
    return errors


def validate_blob(name, data, allowed, media=None):
    errors = []
    path = PurePosixPath(name)
    if name not in allowed or path.is_absolute() or ".." in path.parts:
        errors.append("file is not on the public allowlist")
    if media and name in media:
        return errors + validate_media(name, data, media[name])
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
    media_path = root / "PUBLIC_MEDIA"
    media, media_errors = parse_media(media_path.read_text(encoding="utf-8") if media_path.exists() else "")
    problems.extend({"file": "PUBLIC_MEDIA", "reason": reason} for reason in media_errors)
    for name in media:
        if name not in allowed:
            problems.append({"file": name, "reason": "reviewed media is not on public allowlist"})
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
            problems.extend({"file": name, "reason": reason} for reason in validate_blob(name, path.read_bytes(), allowed, media))
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
            historical_manifest = subprocess.run(["git", "show", commit + ":PUBLIC_MEDIA"], cwd=root, capture_output=True)
            historical_media, historical_errors = parse_media(historical_manifest.stdout.decode("utf-8") if historical_manifest.returncode == 0 else "")
            problems.extend({"file": "PUBLIC_MEDIA", "reason": "history: " + reason} for reason in historical_errors)
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
                key = (name, oid, historical_media.get(name))
                if key in visited:
                    continue
                visited.add(key)
                data = subprocess.run(["git", "cat-file", "blob", oid], cwd=root, capture_output=True, check=True).stdout
                problems.extend({"file": name, "reason": "history: " + reason} for reason in validate_blob(name, data, historical_allowed, historical_media))
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
