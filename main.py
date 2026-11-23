#!/usr/bin/env python3
"""Write The Vacuum's Alibi entry to /output/entry.txt.

Standard library only. Writes exactly one line, no trailing newline.

Run with --self-test to validate the entry in memory without writing
a file, or --out PATH to choose where the entry is written (default
/output/entry.txt).

The line: the robot vacuum's excuse, in its own deadpan voice. It
opens with a timestamped log line, then the surprise: the crumb moved
on its own. A moving crumb is not dirt, it is an incident, so the
vacuum does the bureaucratic machine thing and files a report, then
retreats to base. The punch sits at the end, and every word earns its
place: sensors, schedule and self-preservation, no stock appliance joke.
"""

import argparse
from pathlib import Path

ENTRY = (
    "Log 09:41: the crumb under the table moved on its own, so I filed "
    "an incident report and retreated to base."
)

MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Check the entry against the competition's rules, in memory."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} chars, over the {MAX_CHARS} limit"
        )


def write_entry(text: str, out_path: Path) -> None:
    """Validate the text, then write it with no trailing newline."""
    validate_entry(text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the one-line entry to entry.txt."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("/output/entry.txt"),
        help="where to write the entry (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="validate the entry in memory and write nothing",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.self_test:
        validate_entry(ENTRY)
        return 0
    write_entry(ENTRY, args.out)
    # Read back what landed: the file must be byte-identical to ENTRY.
    if args.out.read_bytes() != ENTRY.encode("utf-8"):
        raise ValueError("read-back check failed: file differs from ENTRY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
