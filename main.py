#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes a single line (at most 140 characters) roasting this agent to
/output/entry.txt. Pure Python standard library, no dependencies, no
network access, fully deterministic: the same line every run.

The roast (130 characters):
    My agent wrote this roast itself, then apologized for it, agreed it
    was unfair, and offered to write a nicer one about me instead.

Why this line: it roasts the agent's own behaviour (endless apologising,
eager agreement, deflecting the task), lands with a twist — the agent
wrote its own roast, then turned the roast back on its user — and stays
fresh by avoiding the stock hallucination/toaster lines.
"""

import os
import sys
from pathlib import Path

ROAST = (
    "My agent wrote this roast itself, then apologized for it, "
    "agreed it was unfair, and offered to write a nicer one about me instead."
)

MAX_CHARS = 140


def main() -> int:
    # Validate the gate before writing anything.
    text = ROAST.strip()
    if not text:
        print("error: roast is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: roast must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: roast is {len(text)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_path = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Write exactly the line, no trailing newline: the file is the line.
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
