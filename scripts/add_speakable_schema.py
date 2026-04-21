#!/usr/bin/env python3
"""Phase 1: Add SpeakableSpecification schema to core + service + blog pages.

SpeakableSpecification tells Google and AI assistants which parts of the page
to read aloud or surface in voice/AI overview responses. Targeting the H1 and
the first meaningful paragraph gives the clearest answer for featured snippets.

Idempotent: skips any page already containing 'SpeakableSpecification'.
"""
from __future__ import annotations

import glob
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))

# Pages to process
GLOBS = [
    os.path.join(ROOT, "*.html"),
    os.path.join(ROOT, "services", "*.html"),
    os.path.join(ROOT, "blog", "*.html"),
    os.path.join(ROOT, "blog", "**", "*.html"),
    os.path.join(ROOT, "pricing.html"),
    os.path.join(ROOT, "about.html"),
]

SKIP_FILES = {"quote.html", "search.html"}


def extract_page_url(html: str) -> str:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    return m.group(1) if m else "https://architecturaldrawings.uk/"


def build_speakable_schema(page_url: str) -> str:
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "url": "{page_url}",
  "speakable": {{
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".hero-lede", ".page-lede", ".section-intro", "article > p:first-of-type", ".tl-dr", ".tldr"]
  }}
}}
</script>"""


def process_file(path: str) -> bool:
    fname = os.path.basename(path)
    if fname in SKIP_FILES:
        return False

    with open(path, encoding="utf-8") as f:
        html = f.read()

    if "SpeakableSpecification" in html:
        return False  # already done

    if "</head>" not in html:
        return False

    page_url = extract_page_url(html)
    schema_block = build_speakable_schema(page_url)

    updated = html.replace("</head>", schema_block + "\n</head>", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)

    return True


def main() -> None:
    seen: set[str] = set()
    updated = 0
    skipped = 0

    for pattern in GLOBS:
        for path in sorted(glob.glob(pattern, recursive=True)):
            abs_path = os.path.abspath(path)
            if abs_path in seen:
                continue
            seen.add(abs_path)

            if process_file(abs_path):
                updated += 1
                print(f"  + {os.path.relpath(abs_path, ROOT)}")
            else:
                skipped += 1

    print(f"\nSpeakable schema: {updated} updated, {skipped} skipped (already done or excluded)")


if __name__ == "__main__":
    main()
