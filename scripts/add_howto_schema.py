#!/usr/bin/env python3
"""Add HowTo schema to process-oriented guide pages AND QAPage schema to FAQ-heavy pages.

For every HTML file under blog/ and guides/ we:
  1. Skip any page already marked with "@type": "HowTo" or "@type": "QAPage".
  2. If the page contains multiple <details> FAQ blocks, extract each
     <summary> question + its answer and emit a QAPage schema listing them.
  3. If the filename matches a process/guide heuristic (contains "guide",
     "how-to", "process", "planning-permission-london", or starts with
     "planning-"), emit a HowTo schema with 5 generic application steps,
     substituting the page's own <h1> and meta description where possible.
  4. Insert the new schema block(s) immediately before </head>.

The script is idempotent thanks to the "@type" marker check.
"""
from __future__ import annotations

import glob
import json
import os
import re
from html import unescape

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))

BLOG_GLOB = os.path.join(PROJECT_ROOT, "blog", "**", "*.html")
GUIDES_GLOB = os.path.join(PROJECT_ROOT, "guides", "**", "*.html")

# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------

HOWTO_FILENAME_HINTS = (
    "guide",
    "how-to",
    "process",
    "planning-permission-london",
)


def is_howto_candidate(path: str) -> bool:
    """Return True if the filename indicates a process-oriented page."""
    basename = os.path.basename(path).lower()
    # Strip the .html so matches like "guide" in "guide.html" still hit.
    stem = basename[:-5] if basename.endswith(".html") else basename

    # Borough planning guides start with "planning-" (but not our cost/cost-guide
    # series which also work as walkthroughs — we still want them if they match
    # "guide" via the generic hint).
    if stem.startswith("planning-"):
        return True

    return any(hint in stem for hint in HOWTO_FILENAME_HINTS)


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\'][^>]*/?>',
    re.IGNORECASE | re.DOTALL,
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\'](.*?)["\'][^>]*/?>',
    re.IGNORECASE | re.DOTALL,
)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)

# Match a <details> ... </details> block (non-greedy).
DETAILS_RE = re.compile(r"<details\b[^>]*>(.*?)</details>", re.IGNORECASE | re.DOTALL)
SUMMARY_RE = re.compile(r"<summary\b[^>]*>(.*?)</summary>", re.IGNORECASE | re.DOTALL)

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_tags(fragment: str) -> str:
    """Strip HTML tags and collapse whitespace to a clean single-line string."""
    text = TAG_RE.sub(" ", fragment)
    text = unescape(text)
    text = WS_RE.sub(" ", text).strip()
    return text


def first_group(pattern: re.Pattern, content: str) -> str | None:
    match = pattern.search(content)
    if not match:
        return None
    return strip_tags(match.group(1))


def extract_qa_pairs(content: str) -> list[tuple[str, str]]:
    """Return list of (question, answer) tuples from <details><summary>...</summary>...</details> blocks."""
    pairs: list[tuple[str, str]] = []
    for details_match in DETAILS_RE.finditer(content):
        inner = details_match.group(1)
        summary_match = SUMMARY_RE.search(inner)
        if not summary_match:
            continue
        question = strip_tags(summary_match.group(1))
        # Answer = everything inside <details> after the </summary> tag.
        after_summary = inner[summary_match.end():]
        answer = strip_tags(after_summary)
        if not question or not answer:
            continue
        pairs.append((question, answer))
    return pairs


# ---------------------------------------------------------------------------
# Schema builders
# ---------------------------------------------------------------------------

DEFAULT_HOWTO_STEPS = [
    {
        "@type": "HowToStep",
        "position": 1,
        "name": "Initial consultation",
        "text": (
            "Contact a chartered architectural technologist to discuss the project "
            "scope and requirements."
        ),
    },
    {
        "@type": "HowToStep",
        "position": 2,
        "name": "Site measured survey",
        "text": (
            "A technologist visits the property to laser-measure rooms, elevations, "
            "and context."
        ),
    },
    {
        "@type": "HowToStep",
        "position": 3,
        "name": "Draft architectural drawings",
        "text": (
            "Existing and proposed plans are drafted in Revit or AutoCAD at 1:50 or "
            "1:100 scale."
        ),
    },
    {
        "@type": "HowToStep",
        "position": 4,
        "name": "Council submission",
        "text": (
            "The complete application package is lodged with the local planning "
            "authority via the Planning Portal."
        ),
    },
    {
        "@type": "HowToStep",
        "position": 5,
        "name": "Decision & next steps",
        "text": (
            "Council issues a decision within 8 weeks for householder applications. "
            "Next step: building regulations drawings and construction."
        ),
    },
]


def build_howto_schema(name: str, description: str) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "totalTime": "PT4W",
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": "GBP",
            "value": "840",
        },
        "step": DEFAULT_HOWTO_STEPS,
    }
    body = json.dumps(schema, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'


def build_qapage_schema(pairs: list[tuple[str, str]], canonical_url: str) -> str:
    url = canonical_url or ""
    main_entity = []
    for question, answer in pairs:
        main_entity.append(
            {
                "@type": "Question",
                "name": question,
                "answerCount": 1,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                    "upvoteCount": 0,
                    "url": url,
                    "author": {
                        "@type": "Organization",
                        "name": "Architectural Drawings London",
                    },
                },
            }
        )
    schema = {
        "@context": "https://schema.org",
        "@type": "QAPage",
        "mainEntity": main_entity,
    }
    body = json.dumps(schema, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_file(path: str) -> tuple[bool, bool]:
    """Process one HTML file. Returns (added_howto, added_qapage)."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Idempotency — bail early on either marker.
    has_howto_marker = '"@type": "HowTo"' in content
    has_qapage_marker = '"@type": "QAPage"' in content

    qa_pairs = extract_qa_pairs(content)
    howto_eligible = is_howto_candidate(path)

    add_howto = howto_eligible and not has_howto_marker
    add_qapage = bool(qa_pairs) and not has_qapage_marker

    if not add_howto and not add_qapage:
        return (False, False)

    # Extract page-level metadata once if we'll need it.
    h1_text = first_group(H1_RE, content) or first_group(TITLE_RE, content) or ""
    meta_desc = first_group(META_DESC_RE, content) or h1_text
    canonical = first_group(CANONICAL_RE, content) or ""

    blocks: list[str] = []
    if add_howto:
        blocks.append(build_howto_schema(h1_text, meta_desc))
    if add_qapage:
        blocks.append(build_qapage_schema(qa_pairs, canonical))

    injection = "\n" + "\n".join(blocks) + "\n"

    # Insert immediately before the first closing </head>.
    head_close_re = re.compile(r"</head>", re.IGNORECASE)
    match = head_close_re.search(content)
    if not match:
        print(f"  SKIP (no </head>): {path}")
        return (False, False)

    new_content = content[: match.start()] + injection + content[match.start():]

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return (add_howto, add_qapage)


def main() -> None:
    files = sorted(
        set(glob.glob(BLOG_GLOB, recursive=True))
        | set(glob.glob(GUIDES_GLOB, recursive=True))
    )

    howto_count = 0
    qapage_count = 0
    touched = 0
    skipped_no_change = 0

    for path in files:
        # Skip generator/helper python files that might linger as .html? — no,
        # glob already limits to *.html. But protect against index partials etc.
        added_howto, added_qapage = process_file(path)
        if added_howto:
            howto_count += 1
        if added_qapage:
            qapage_count += 1
        if added_howto or added_qapage:
            touched += 1
            tag_parts = []
            if added_howto:
                tag_parts.append("HowTo")
            if added_qapage:
                tag_parts.append("QAPage")
            rel = os.path.relpath(path, PROJECT_ROOT)
            print(f"  + {'+'.join(tag_parts):<13} {rel}")
        else:
            skipped_no_change += 1

    print()
    print(f"Files scanned:       {len(files)}")
    print(f"Files updated:       {touched}")
    print(f"HowTo schemas added: {howto_count}")
    print(f"QAPage schemas added:{qapage_count}")
    print(f"Unchanged/skipped:   {skipped_no_change}")


if __name__ == "__main__":
    main()
