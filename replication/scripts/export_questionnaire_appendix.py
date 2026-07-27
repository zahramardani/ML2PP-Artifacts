#!/usr/bin/env python3
"""Export the complete questionnaire-instrument appendix from the thesis."""

from __future__ import annotations

import argparse
from pathlib import Path


START = r"\chapter{Questionnaire Instruments}"
END = r"\chapter{Formal Notation}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    start = source.find(START)
    end = source.find(END, start + len(START))
    if start < 0 or end < 0:
        raise SystemExit("Could not locate the questionnaire appendix boundaries")

    header = (
        "% Extracted verbatim from the revised dissertation source.\n"
        "% This is an instrument fragment, not participant-response data.\n"
        "% The \\rev command may be defined as identity when compiled separately.\n\n"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(header + source[start:end].rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
