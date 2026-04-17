#!/usr/bin/env python3
"""
Adds free Unsplash stock images to blog posts and key pages, replacing any
gradient placeholder hero divs with real imagery.

- Walks all HTML files under blog/, guides/, and projects/.
- Determines topic from filename keywords and picks the FIRST image from the
  matching curated Unsplash category (deterministic / idempotent).
- If a gradient placeholder div (linear-gradient(135deg, var(--ink) ...)) is
  present, replaces it with a responsive <img> wrapped in a rounded container.
- Otherwise, inserts the image block directly after the </h1> tag (before the
  article body content).
- Skips files that already contain an `images.unsplash.com` URL.
- Uses encoding="utf-8" throughout.

Usage:
    python3 scripts/add_stock_images.py
"""

from __future__ import annotations

import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
TARGET_DIRS = ["blog", "guides", "projects"]

# Curated Unsplash library — (URL, alt) pairs.
IMAGES: dict[str, list[tuple[str, str]]] = {
    # Planning / drawings
    "planning": [
        ("https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=75", "Architectural blueprints and technical drawings on a desk"),
        ("https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1600&q=75", "Architect reviewing planning drawings with a tablet"),
        ("https://images.unsplash.com/photo-1517022812141-23620dba5c23?auto=format&fit=crop&w=1600&q=75", "Technical drawing overlay on plans"),
    ],
    # Construction / building regs
    "building-regs": [
        ("https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=1600&q=75", "House construction site with scaffolding"),
        ("https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=75", "Building regulations compliance drawings"),
        ("https://images.unsplash.com/photo-1590644365607-1c0f865b5c09?auto=format&fit=crop&w=1600&q=75", "Construction drawings with calculations"),
    ],
    # Loft conversions
    "loft": [
        ("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=75", "Bright modern loft bedroom with dormer window"),
        ("https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=75", "Loft conversion with exposed beams"),
        ("https://images.unsplash.com/photo-1600210492493-0946911123ea?auto=format&fit=crop&w=1600&q=75", "Velux rooflight in converted loft"),
    ],
    # Extensions
    "extension": [
        ("https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1600&q=75", "Modern rear extension with bi-fold doors"),
        ("https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?auto=format&fit=crop&w=1600&q=75", "Open-plan kitchen side return extension"),
        ("https://images.unsplash.com/photo-1558346490-a72e53ae2d4f?auto=format&fit=crop&w=1600&q=75", "House extension under construction"),
    ],
    # Mansard
    "mansard": [
        ("https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1600&q=75", "London terraced houses with mansard roofs"),
        ("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1600&q=75", "Victorian house with mansard extension"),
    ],
    # London / boroughs
    "london": [
        ("https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1600&q=75", "London Victorian terraced street"),
        ("https://images.unsplash.com/photo-1520986606214-8b456906c813?auto=format&fit=crop&w=1600&q=75", "Georgian London townhouses"),
        ("https://images.unsplash.com/photo-1592595896616-c37162298647?auto=format&fit=crop&w=1600&q=75", "Traditional London residential street"),
        ("https://images.unsplash.com/photo-1568454537842-d933259bb258?auto=format&fit=crop&w=1600&q=75", "London suburban Victorian houses"),
    ],
    # Conservation / heritage
    "conservation": [
        ("https://images.unsplash.com/photo-1605146768851-eda79da39897?auto=format&fit=crop&w=1600&q=75", "Victorian conservation area terrace"),
        ("https://images.unsplash.com/photo-1551038247-3d9af20df552?auto=format&fit=crop&w=1600&q=75", "Listed building Georgian facade"),
    ],
    # Kitchen / interior
    "kitchen": [
        ("https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=1600&q=75", "Modern kitchen extension with island"),
        ("https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1600&q=75", "Open-plan kitchen diner in extension"),
    ],
    # Structural / technical
    "structural": [
        ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=1600&q=75", "Structural steel beam installation"),
        ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1600&q=75", "Structural engineering drawings"),
    ],
    # Party wall
    "party-wall": [
        ("https://images.unsplash.com/photo-1597216729923-2e36dfb60ecc?auto=format&fit=crop&w=1600&q=75", "Adjoining London terraced party walls"),
    ],
    # Basement
    "basement": [
        ("https://images.unsplash.com/photo-1600607687644-c7171b42498f?auto=format&fit=crop&w=1600&q=75", "Basement conversion excavation"),
    ],
    # Default fallback
    "default": [
        ("https://images.unsplash.com/photo-1486718448742-163732cd1544?auto=format&fit=crop&w=1600&q=75", "Modern residential architecture"),
    ],
}

# London borough slugs used in filenames like "planning-camden" or
# "extension-cost-camden". When detected we treat them as location pages.
LONDON_BOROUGH_SLUGS = {
    "barking-and-dagenham", "barnet", "bexley", "brent", "bromley", "camden",
    "city-of-london", "croydon", "ealing", "enfield", "greenwich", "hackney",
    "hammersmith-and-fulham", "haringey", "harrow", "havering", "hillingdon",
    "hounslow", "islington", "kensington-and-chelsea", "kingston-upon-thames",
    "lambeth", "lewisham", "merton", "newham", "redbridge",
    "richmond-upon-thames", "southwark", "sutton", "tower-hamlets",
    "waltham-forest", "wandsworth", "westminster",
}


def pick_category(filename: str) -> str:
    """Return the IMAGES key that best matches the given filename stem."""
    name = filename.lower()
    stem = name.rsplit(".", 1)[0]

    # Party wall — check first (contains "wall")
    if "party-wall" in stem:
        return "party-wall"

    # Basement
    if "basement" in stem:
        return "basement"

    # Structural
    if "structural" in stem or "steel" in stem:
        return "structural"

    # Conservation / heritage
    if "conservation" in stem or "heritage" in stem or "listed" in stem:
        return "conservation"

    # Mansard (specific roof type)
    if "mansard" in stem:
        return "mansard"

    # Loft / dormer
    if "loft" in stem or "dormer" in stem or "velux" in stem or "rooflight" in stem:
        return "loft"

    # Kitchen (before extension so kitchen-extension-* lands here)
    if "kitchen" in stem:
        return "kitchen"

    # Extensions (side-return, wraparound, rear, double-storey, etc.)
    if (
        "extension" in stem
        or "side-return" in stem
        or "wraparound" in stem
        or "rear-extension" in stem
        or "double-storey" in stem
        or "single-storey" in stem
    ):
        return "extension"

    # Building regulations
    if "building-regs" in stem or "building-regulations" in stem or "part-l" in stem:
        return "building-regs"

    # Planning — if followed by a borough slug, use london imagery
    if stem.startswith("planning-") or stem.startswith("planning_"):
        tail = stem.split("-", 1)[1] if "-" in stem else ""
        if tail in LONDON_BOROUGH_SLUGS:
            return "london"
        return "planning"
    if "planning" in stem:
        return "planning"

    # Borough-only filenames (e.g. "camden.html")
    if stem in LONDON_BOROUGH_SLUGS:
        return "london"

    # Anything mentioning a borough slug as a suffix
    for b in LONDON_BOROUGH_SLUGS:
        if stem.endswith("-" + b) or ("-" + b + "-") in stem:
            return "london"

    return "default"


def build_img_block(url: str, alt: str) -> str:
    """Return the responsive hero image block."""
    return (
        '<div style="border-radius: var(--r-lg); overflow: hidden; '
        'aspect-ratio: 16/9; margin: 32px 0; background: var(--ink);">\n'
        f'  <img src="{url}" alt="{alt}" loading="lazy" '
        'width="1600" height="900" style="width: 100%; height: 100%; '
        'object-fit: cover; display: block;" />\n'
        "</div>"
    )


# Matches a gradient-placeholder hero div. Uses DOTALL to span multiple lines.
# Example placeholder:
#   <div style="... background: linear-gradient(135deg, var(--ink) ...); ...">
#     ...
#   </div>
PLACEHOLDER_RE = re.compile(
    r'<div[^>]*linear-gradient\(\s*135deg\s*,\s*var\(--ink\)[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)

# Matches a full </h1> closing tag so we can insert after it.
H1_CLOSE_RE = re.compile(r"</h1>", re.IGNORECASE)


def process_file(path: Path) -> str:
    """
    Return one of:
        "skipped-existing" — already has an unsplash image
        "replaced"         — replaced a gradient placeholder
        "inserted"         — inserted after the first </h1>
        "no-target"        — neither placeholder nor <h1> found; untouched
    """
    try:
        html = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"  [!] failed to read {path}: {exc}")
        return "no-target"

    # Idempotence: skip if page already has an unsplash URL
    if "images.unsplash.com" in html:
        return "skipped-existing"

    category = pick_category(path.name)
    url, alt = IMAGES[category][0]
    img_block = build_img_block(url, alt)

    # Prefer replacing an existing gradient placeholder div.
    if PLACEHOLDER_RE.search(html):
        new_html = PLACEHOLDER_RE.sub(img_block, html, count=1)
        path.write_text(new_html, encoding="utf-8")
        return "replaced"

    # Otherwise, insert after the first </h1>.
    match = H1_CLOSE_RE.search(html)
    if match:
        insert_at = match.end()
        new_html = html[:insert_at] + "\n" + img_block + "\n" + html[insert_at:]
        path.write_text(new_html, encoding="utf-8")
        return "inserted"

    return "no-target"


def main() -> None:
    totals = {
        "replaced": 0,
        "inserted": 0,
        "skipped-existing": 0,
        "no-target": 0,
        "total-html": 0,
    }

    for rel_dir in TARGET_DIRS:
        base = PROJECT / rel_dir
        if not base.exists():
            print(f"[skip] {rel_dir}/ does not exist")
            continue

        html_files = sorted(base.rglob("*.html"))
        for path in html_files:
            totals["total-html"] += 1
            result = process_file(path)
            totals[result] = totals.get(result, 0) + 1
            rel = path.relative_to(PROJECT).as_posix()
            category = pick_category(path.name)
            print(f"  [{result:18s}] ({category:13s}) {rel}")

    print()
    print("=" * 60)
    print("Stock images pass complete")
    print(f"  Total HTML files scanned : {totals['total-html']}")
    print(f"  Replaced placeholders    : {totals['replaced']}")
    print(f"  Inserted after <h1>      : {totals['inserted']}")
    print(f"  Skipped (already had img): {totals['skipped-existing']}")
    print(f"  No insertion point found : {totals['no-target']}")
    updated = totals["replaced"] + totals["inserted"]
    print(f"  Files updated            : {updated}")


if __name__ == "__main__":
    main()
