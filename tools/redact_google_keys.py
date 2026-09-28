#!/usr/bin/env python3
"""Remove Google API-key-shaped values from a tracked static artifact without printing them."""
from __future__ import annotations

import re
from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "Motlow KML Generator.mht"
PATTERNS = (
    re.compile(rb"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(rb"AQ\.[0-9A-Za-z_-]{20,}"),
)
REPLACEMENT = b"REDACTED_GOOGLE_API_KEY"


def normalize_redacted_lines(content: bytes) -> tuple[bytes, int]:
    """Use LF endings and no trailing whitespace only on redacted lines.

    The legacy MHT artifact mixes line endings. Normalizing only modified lines
    prevents Git from reporting a carriage return as trailing whitespace.
    """
    normalized_lines: list[bytes] = []
    normalized_count = 0
    for line in content.splitlines(keepends=True):
        if REPLACEMENT not in line:
            normalized_lines.append(line)
            continue
        body = line.rstrip(b" \t\r\n")
        normalized = body + b"\n"
        normalized_count += int(normalized != line)
        normalized_lines.append(normalized)
    return b"".join(normalized_lines), normalized_count


def main() -> int:
    content = TARGET.read_bytes()
    replacement_count = 0
    for pattern in PATTERNS:
        content, count = pattern.subn(REPLACEMENT, content)
        replacement_count += count
    content, normalized_count = normalize_redacted_lines(content)
    TARGET.write_bytes(content)
    print(
        f"Redacted {replacement_count} credential-like value(s) and normalized "
        f"{normalized_count} changed line(s) in {TARGET.name}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
