#!/usr/bin/env python3
"""Create a deterministic file inventory for one archived ML2++ run."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_NAME = "run-manifest.json"
REQUIRED_DIRECTORIES = ("model", "generated", "data", "environment", "results", "logs")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--generator-commit", required=True)
    parser.add_argument("--command", required=True, dest="execution_command")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    if not run_dir.is_dir():
        raise SystemExit(f"Run directory does not exist: {run_dir}")
    if len(args.generator_commit) != 40 or any(
        c not in "0123456789abcdef" for c in args.generator_commit.lower()
    ):
        raise SystemExit("--generator-commit must be a full 40-character Git SHA")

    missing = [name for name in REQUIRED_DIRECTORIES if not (run_dir / name).is_dir()]
    if missing:
        raise SystemExit("Missing required directories: " + ", ".join(missing))

    files = []
    for path in sorted(p for p in run_dir.rglob("*") if p.is_file()):
        if path.name == MANIFEST_NAME:
            continue
        files.append(
            {
                "path": path.relative_to(run_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    if not files:
        raise SystemExit("No artefact files found; refusing to create an empty manifest")

    manifest = {
        "schema_version": "1.0",
        "run_id": args.run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "generator_commit": args.generator_commit.lower(),
        "execution_command": args.execution_command,
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.splitlines()[0],
        },
        "files": files,
    }
    destination = run_dir / MANIFEST_NAME
    destination.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {destination} with {len(files)} file records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
