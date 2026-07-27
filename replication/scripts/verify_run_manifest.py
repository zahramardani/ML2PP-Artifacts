#!/usr/bin/env python3
"""Verify the existence, size, and SHA-256 of files in an ML2++ run manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_dir = manifest_path.parent
    errors = []
    for record in manifest.get("files", []):
        path = run_dir / record["path"]
        if not path.is_file():
            errors.append(f"missing: {record['path']}")
            continue
        if path.stat().st_size != record["bytes"]:
            errors.append(f"size mismatch: {record['path']}")
        if sha256(path) != record["sha256"]:
            errors.append(f"hash mismatch: {record['path']}")

    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Verified {len(manifest.get('files', []))} files for {manifest.get('run_id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
