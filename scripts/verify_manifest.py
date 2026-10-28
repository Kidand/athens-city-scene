"""Verify release files using only the Python standard library.

Usage: python scripts/verify_manifest.py [manifest.json] [--root DIRECTORY]
Manifest schema: {"files": [{"path": "relative/path", "bytes": 123,
                             "sha256": "64 lowercase hex characters"}]}
Extra files are allowed; the manifest need not include itself.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


class ManifestError(ValueError):
    pass


def verify(manifest, root):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    entries = data.get("files") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ManifestError("Manifest must contain a nonempty files array.")
    root = root.resolve()
    seen, failures = set(), []
    checked_bytes = 0
    for entry in entries:
        if not isinstance(entry, dict):
            raise ManifestError("Every files entry must be an object.")
        name = entry.get("path")
        if not isinstance(name, str) or not name or "\\" in name or ":" in name:
            raise ManifestError("Every path must be a nonempty relative POSIX path.")
        parts = name.split("/")
        if any(part in {"", ".", ".."} for part in parts) or PurePosixPath(name).is_absolute():
            raise ManifestError("Unsafe path in manifest.")
        if name in seen:
            raise ManifestError("Duplicate path in manifest.")
        seen.add(name)
        size, expected = entry.get("bytes"), entry.get("sha256")
        if type(size) is not int or size < 0:
            raise ManifestError("Every bytes value must be a nonnegative integer.")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ManifestError("Every sha256 must be 64 lowercase hexadecimal characters.")
        path = root.joinpath(*parts).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ManifestError("Path resolves outside the release root.") from exc
        if not path.is_file():
            failures.append({"path": name, "error": "missing file"})
            continue
        actual_size = path.stat().st_size
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        checked_bytes += actual_size
        if actual_size != size or digest.hexdigest() != expected:
            failures.append({"path": name, "error": "size or SHA-256 mismatch"})
    return {"ok": not failures, "listed_files": len(entries),
            "checked_bytes": checked_bytes, "failures": failures}


def main():
    default_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path,
                        default=default_root / "manifest.json")
    parser.add_argument("--root", type=Path, default=default_root)
    args = parser.parse_args()
    try:
        result = verify(args.manifest, args.root)
    except (OSError, ValueError) as exc:
        # Do not echo OS exceptions, which can expose private absolute paths.
        result = {"ok": False, "error": str(exc) if isinstance(exc, ManifestError)
                  else "Manifest could not be read or parsed, or a file could not be read."}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
