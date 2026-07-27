#!/usr/bin/env python3
"""Create the standard directory layout for one ML2++ archived run."""

from __future__ import annotations

import argparse
from pathlib import Path


DIRECTORIES = ("model", "generated", "data", "environment", "results", "logs")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    for name in DIRECTORIES:
        (args.run_dir / name).mkdir(parents=True, exist_ok=True)
    print(f"Initialised {args.run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
