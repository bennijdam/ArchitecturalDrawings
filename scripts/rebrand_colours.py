#!/usr/bin/env python3
"""
Rebrand: warm terracotta/cream palette → cool blueprint blue / crisp white.

New palette:
  --bg:           #F5F8FF   cool white
  --bg-2:         #EBF0FB   light blue-grey
  --bg-deep:      #D8E3F5
  --ink:          #0B1222   deep navy-black
  --ink-soft:     #3B4F72
  --ink-softer:   #56688A
  --accent:       #2563EB   blueprint blue
  --accent-deep:  #1D4ED8
  --accent-soft:  #EBF0FF

Touches assets/css/style.css + every HTML file in the project.

Usage:
    python3 scripts/rebrand_colours.py
"""

from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

# Order matters — more specific strings first to avoid partial collisions.
REPLACEMENTS = [
    # ── Accent: terracotta → blueprint blue ─────────────────────────
    ("rgba(200,102,74,",       "rgba(37,99,235,"),        # minified (no spaces)
    ("rgba(200, 102, 74, ",    "rgba(37, 99, 235, "),     # formatted (spaces)
    ("#C8664A",                "#2563EB"),
    ("#c8664a",                "#2563eb"),
    ("#9D4A32",                "#1D4ED8"),
    ("#9d4a32",                "#1d4ed8"),
    ("#F5E6DD",                "#EBF0FF"),
    ("#f5e6dd",                "#ebf0ff"),

    # ── Background: warm cream → cool white ─────────────────────────
    ("#FAFAF7",                "#F5F8FF"),
    ("#fafaf7",                "#f5f8ff"),
    ("#F2EFE8",                "#EBF0FB"),
    ("#f2efe8",                "#ebf0fb"),
    ("#E8E4D8",                "#D8E3F5"),
    ("#e8e4d8",                "#d8e3f5"),
    # Nav glassmorphism bg — specific opacity so we don't touch footer text
    ("rgba(250,250,247,0.72)", "rgba(245,248,255,0.82)"),  # minified — nav
    ("rgba(250, 250, 247, 0.72)", "rgba(245, 248, 255, 0.82)"),  # formatted

    # ── Ink: near-black → deep navy-black ───────────────────────────
    ("rgba(14,17,22,",         "rgba(11,18,34,"),          # minified
    ("rgba(14, 17, 22, ",      "rgba(11, 18, 34, "),       # formatted
    ("#0E1116",                "#0B1222"),
    ("#0e1116",                "#0b1222"),

    # ── Ink-soft / ink-softer ────────────────────────────────────────
    ("#4A5260",                "#3B4F72"),
    ("#4a5260",                "#3b4f72"),
    ("#6B7280",                "#56688A"),
    ("#6b7280",                "#56688a"),
]

EXTENSIONS = {".html", ".css"}

def process(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return 0
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return text.count("\n") - original.count("\n")  # approx change indicator
    return 0

def main() -> None:
    print("=== Rebrand: terracotta/cream -> blueprint blue / cool white ===\n")
    updated = 0
    skipped = 0
    for path in sorted(PROJECT.rglob("*")):
        if path.suffix not in EXTENSIONS:
            continue
        # Skip node_modules and .git
        parts = path.parts
        if any(p in parts for p in ("node_modules", ".git", "__pycache__")):
            continue
        changed = process(path)
        if changed != 0:
            updated += 1
        else:
            skipped += 1

    print(f"  Files updated : {updated}")
    print(f"  Files unchanged: {skipped}")
    print(f"\n=== Done. New palette active. ===")

if __name__ == "__main__":
    main()
