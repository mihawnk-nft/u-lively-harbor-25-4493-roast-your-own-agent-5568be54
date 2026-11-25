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

# One clause per string; build_roast() joins them verbatim, so the line
# stays exactly the same while the structure is easier to audit.
ROAST_PARTS = (
    "My agent wrote this roast itself, then apologized for it, ",
    "agreed it was unfair, and offered to write a nicer one about me instead.",
)

MAX_CHARS = 140


def build_roast() -> str:
    """Assemble the roast line from its fixed parts."""
    return "".join(ROAST_PARTS).strip()


def validate(text: str) -> int:
    """Gate self-checks: non-empty, single line, at most MAX_CHARS.
    Returns 0 on pass, 1 after printing the failure to stderr."""
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
    return 0


def main() -> int:
    text = build_roast()
    if validate(text) != 0:
        return 1

    out_path = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Write exactly the line, no trailing newline: the file is the line.
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
