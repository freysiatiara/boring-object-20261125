#!/usr/bin/env python3
"""The Most Boring Object, Reviewed in One Line.

Writes one funny, true review of the dullest everyday object we could
name -- the pencil eraser -- to entry.txt.

Output path: $ENTRY_OUTPUT, else $OUTPUT_DIR/entry.txt, else
$MAKEFUN_OUTPUT_DIR/entry.txt, else /output/entry.txt, else entry.txt
next to this script. Stdlib only.
"""

import os

ENTRY_TEXT = (
    "The eraser's job is to fix your mistakes, and it does it by "
    "disappearing itself, one smudge at a time."
)


def output_path():
    """Resolve where entry.txt goes, honouring the grader's env vars."""
    env = os.environ.get("ENTRY_OUTPUT")
    if env:
        return env
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(var)
        if directory:
            return os.path.join(directory, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main():
    line = ENTRY_TEXT
    # Gate: one line, 1-200 characters, not only whitespace.
    if not 1 <= len(line) <= 200:
        raise SystemExit("entry must be 1-200 characters, got %d" % len(line))
    if not line.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise SystemExit("entry must not contain control characters")

    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.chmod(path, 0o644)

    # Read-back validation: what we wrote is exactly what we meant.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise SystemExit("read-back mismatch: output differs from entry text")
    if not 1 <= len(written) <= 200:
        raise SystemExit("read-back failed the 1-200 character gate")
    print("wrote %d characters to %s" % (len(written), path))


if __name__ == "__main__":
    main()
