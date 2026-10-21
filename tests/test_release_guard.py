"""Publication boundaries, including exact reviewed assets and removed history."""
import binascii
import hashlib
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import zlib

from scripts.check_release import check, parse_media, validate_blob


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xffffffff)


def generated_png(metadata=False):
    # A generated one-pixel fixture, not a photo or committed binary.
    header = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    extra = chunk(b"eXIf", b"fictional metadata") if metadata else b""
    return b"\x89PNG\r\n\x1a\n" + header + extra + chunk(b"IDAT", zlib.compress(b"\0\0\0\0")) + chunk(b"IEND", b"")


class PublicationGuardTests(unittest.TestCase):
    def test_media_is_denied_without_exact_reviewed_manifest(self):
        name, data = "docs/assets/synthetic.png", generated_png()
        self.assertTrue(validate_blob(name, data, {name}))
        self.assertEqual(validate_blob(name, data, {name}, {name: hashlib.sha256(data).hexdigest()}), [])

    def test_modifying_an_approved_asset_invalidates_its_review(self):
        name, data = "docs/assets/synthetic.png", generated_png()
        errors = validate_blob(name, data, {name}, {name: "0" * 64})
        self.assertIn("reviewed-media hash mismatch", errors)

    def test_png_metadata_is_rejected_even_when_hash_matches(self):
        name, data = "docs/assets/synthetic.png", generated_png(metadata=True)
        errors = validate_blob(name, data, {name}, {name: hashlib.sha256(data).hexdigest()})
        self.assertIn("PNG contains unapproved metadata", errors)

    def test_corrupt_or_appended_png_is_rejected(self):
        name = "docs/assets/synthetic.png"
        for data in (generated_png() + b"trailing", generated_png()[:-4]):
            self.assertTrue(validate_blob(name, data, {name}, {name: hashlib.sha256(data).hexdigest()}))

    def test_manifest_does_not_allow_arbitrary_paths_or_types(self):
        for path in ("private.png", "docs/assets/../private.png", "docs/assets/secret.db"):
            media, errors = parse_media("0" * 64 + "  " + path)
            self.assertEqual(media, {})
            self.assertTrue(errors)

    def test_removed_unlisted_file_is_still_found_in_git_history(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            def git(*args):
                return subprocess.run(["git", "-c", "user.name=Synthetic Fixture", "-c",
                    "user.email=fixture" + "@" + "example.invalid", "-c", "commit.gpgsign=false", *args],
                    cwd=root, check=True, capture_output=True)
            git("init", "-b", "main")
            (root / "PUBLIC_FILES").write_text("PUBLIC_FILES\n")
            (root / "unlisted-private.txt").write_text("FICTIONAL_RUNTIME_SENTINEL")
            git("add", ".")
            git("commit", "-m", "Synthetic unsafe history")
            git("rm", "unlisted-private.txt")
            git("commit", "-m", "Remove synthetic runtime")
            result = check(root)
            self.assertFalse(result["passed"])
            self.assertEqual(result["git_commits_checked"], 2)
            self.assertTrue(any(item["file"] == "unlisted-private.txt" and "history:" in item["reason"] for item in result["problems"]))
