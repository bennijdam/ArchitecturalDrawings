#!/usr/bin/env python3
"""
Add a 'Related articles' section to all blog posts that don't already have one.

Inserts a styled section with 3 related article cards just before the CTA band.
Relatedness is determined by topic clusters defined below.

Usage:
    cd architectural-drawings
    python scripts/add_related_articles.py
"""

import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = PROJECT_ROOT / "blog"

# ---------------------------------------------------------------------------
# Import borough data for adjacent-borough linking
# ---------------------------------------------------------------------------
sys.path.insert(0, str(PROJECT_ROOT))
try:
    from pseo_boroughs import BOROUGHS
except ImportError:
    BOROUGHS = {}

# ---------------------------------------------------------------------------
# Topic clusters
# ---------------------------------------------------------------------------
PLANNING_CLUSTER = [
    "planning-permission-london",
    "permitted-development-rules-2026",
    "planning-permission-refused-what-next",
    "conservation-area-planning-london",
    "full-planning-vs-prior-approval",
    "planning-vs-permitted-development",
]

EXTENSION_CLUSTER = [
    "extension-cost-guide-london",
    "kitchen-extension-cost-london",
    "side-return-extension-guide",
    "wraparound-extension-guide",
    "double-storey-extension-guide",
]

LOFT_CLUSTER = [
    "loft-vs-mansard",
    "loft-conversion-without-planning",
    "dormer-vs-velux-loft",
]

BUILDING_REGS_CLUSTER = [
    "building-regulations-explained",
    "building-regs-part-l-guide",
    "labc-vs-approved-inspector",
]

COST_COMPARISON_CLUSTER = [
    "planning-drawings-cost-london",
    "architect-fees-vs-fixed-fee",
    "drawing-service-vs-architect",
    "choosing-architect-london",
    "architect-vs-architectural-technologist",
]

CONVERSION_CLUSTER = [
    "hmo-conversion-guide-london",
    "flat-conversion-guide-london",
    "change-of-use-planning-london",
    "outbuilding-planning-guide",
]

ALL_CLUSTERS = [
    PLANNING_CLUSTER,
    EXTENSION_CLUSTER,
    LOFT_CLUSTER,
    BUILDING_REGS_CLUSTER,
    COST_COMPARISON_CLUSTER,
    CONVERSION_CLUSTER,
]

# Adjacency between clusters (index-based): which clusters are "close" to each other
CLUSTER_ADJACENCY = {
    0: [3, 4],      # planning -> building regs, cost/comparison
    1: [2, 4],      # extension -> loft, cost/comparison
    2: [1, 0],      # loft -> extension, planning
    3: [0, 5],      # building regs -> planning, conversion
    4: [0, 1],      # cost/comparison -> planning, extension
    5: [0, 3],      # conversion -> planning, building regs
}

# ---------------------------------------------------------------------------
# Borough guide slugs (planning-{borough})
# ---------------------------------------------------------------------------
BOROUGH_SLUGS = [
    "barking-and-dagenham", "barnet", "bexley", "brent", "bromley",
    "camden", "city-of-london", "croydon", "ealing", "enfield",
    "greenwich", "hackney", "hammersmith-and-fulham", "haringey", "harrow",
    "havering", "hillingdon", "hounslow", "islington",
    "kensington-and-chelsea", "kingston-upon-thames", "lambeth", "lewisham",
    "merton", "newham", "redbridge", "richmond-upon-thames", "southwark",
    "sutton", "tower-hamlets", "waltham-forest", "wandsworth", "westminster",
]


def is_borough_guide(slug):
    """Check if a slug is a borough planning guide (planning-{borough})."""
    if slug.startswith("planning-"):
        borough_part = slug[len("planning-"):]
        return borough_part in BOROUGH_SLUGS
    return False


def get_borough_from_slug(slug):
    """Extract the borough slug from a planning-{borough} slug."""
    return slug[len("planning-"):]


# ---------------------------------------------------------------------------
# Extract title and description from an HTML file
# ---------------------------------------------------------------------------
def extract_meta(filepath):
    """Return (title, description) from an HTML file."""
    content = filepath.read_text(encoding="utf-8")

    title_match = re.search(r"<title>(.+?)</title>", content)
    title = title_match.group(1) if title_match else ""
    # Strip trailing " | AD" or " | Architectural Drawings" etc
    title = re.sub(r"\s*\|.*$", "", title).strip()

    desc_match = re.search(r'<meta\s+name="description"\s+content="(.+?)"', content)
    desc = desc_match.group(1) if desc_match else ""
    # Truncate description for the card (keep it short)
    if len(desc) > 120:
        desc = desc[:117].rsplit(" ", 1)[0] + "..."
    # Decode HTML entities
    desc = desc.replace("&pound;", "\u00a3").replace("&amp;", "&")

    return title, desc


# ---------------------------------------------------------------------------
# Build a lookup of all blog post metadata
# ---------------------------------------------------------------------------
def build_posts_index():
    """Return dict of slug -> {title, desc, filepath}."""
    posts = {}
    for f in BLOG_DIR.glob("*.html"):
        if f.name == "index.html":
            continue
        slug = f.stem
        title, desc = extract_meta(f)
        posts[slug] = {"title": title, "desc": desc, "filepath": f}
    return posts


# ---------------------------------------------------------------------------
# Find cluster for a given slug
# ---------------------------------------------------------------------------
def find_cluster_index(slug):
    """Return index of cluster containing slug, or -1."""
    for i, cluster in enumerate(ALL_CLUSTERS):
        if slug in cluster:
            return i
    return -1


# ---------------------------------------------------------------------------
# Pick 3 related articles for a non-borough post
# ---------------------------------------------------------------------------
def pick_related_general(slug, posts):
    """Return list of up to 3 related slugs."""
    cluster_idx = find_cluster_index(slug)
    candidates = []

    if cluster_idx >= 0:
        # Same cluster first (excluding self)
        same_cluster = [s for s in ALL_CLUSTERS[cluster_idx] if s != slug and s in posts]
        candidates.extend(same_cluster)

        # If we need more, pull from adjacent clusters
        if len(candidates) < 3:
            for adj_idx in CLUSTER_ADJACENCY.get(cluster_idx, []):
                for s in ALL_CLUSTERS[adj_idx]:
                    if s != slug and s not in candidates and s in posts:
                        candidates.append(s)
                    if len(candidates) >= 6:
                        break
                if len(candidates) >= 6:
                    break

    return candidates[:3]


# ---------------------------------------------------------------------------
# Pick 3 related articles for a borough guide
# ---------------------------------------------------------------------------
def pick_related_borough(slug, posts):
    """
    For planning-{borough} guides:
    1. planning-permission-london (main guide)
    2. permitted-development-rules-2026
    3. An adjacent borough guide (if available), else planning-permission-refused-what-next
    """
    related = []

    # 1. Main planning guide
    if "planning-permission-london" in posts:
        related.append("planning-permission-london")

    # 2. Permitted development rules
    if "permitted-development-rules-2026" in posts:
        related.append("permitted-development-rules-2026")

    # 3. Adjacent borough guide
    borough = get_borough_from_slug(slug)
    adjacent_borough_slug = None

    if borough in BOROUGHS:
        for adj in BOROUGHS[borough].get("adjacent", []):
            candidate = f"planning-{adj}"
            if candidate in posts and candidate != slug:
                adjacent_borough_slug = candidate
                break

    if adjacent_borough_slug:
        related.append(adjacent_borough_slug)
    elif "planning-permission-refused-what-next" in posts:
        related.append("planning-permission-refused-what-next")
    elif "conservation-area-planning-london" in posts:
        related.append("conservation-area-planning-london")

    return related[:3]


# ---------------------------------------------------------------------------
# Generate the related articles HTML
# ---------------------------------------------------------------------------
def build_related_html(related_slugs, posts):
    """Build the related articles section HTML."""
    cards = []
    for s in related_slugs:
        post = posts[s]
        title_escaped = post["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        desc_escaped = post["desc"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        card = (
            f'      <a href="{s}.html" class="service-card" style="padding: 24px;">\n'
            f'        <h3 style="font-size: 1.05rem;">{title_escaped}</h3>\n'
            f'        <p style="font-size: 0.85rem; color: var(--ink-soft); margin-top: 8px;">{desc_escaped}</p>\n'
            f'        <span class="service-card-link" style="margin-top: 12px;">Read article \u2192</span>\n'
            f'      </a>'
        )
        cards.append(card)

    cards_html = "\n".join(cards)

    section = (
        f'<!-- related-articles -->\n'
        f'<section style="background: var(--bg-2);">\n'
        f'  <div class="container">\n'
        f'    <div class="section-header">\n'
        f'      <span class="eyebrow">Keep reading</span>\n'
        f'      <h2 style="margin-top: 16px;">Related <em>articles</em></h2>\n'
        f'    </div>\n'
        f'    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">\n'
        f'{cards_html}\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</section>\n'
    )
    return section


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    posts = build_posts_index()
    updated = 0
    skipped_already = 0
    skipped_no_cta = 0
    skipped_no_related = 0

    for slug, info in sorted(posts.items()):
        filepath = info["filepath"]
        content = filepath.read_text(encoding="utf-8")

        # Skip if already has related articles
        if "related-articles" in content:
            skipped_already += 1
            continue

        # Find the CTA band insertion point
        cta_match = re.search(r'^<section class="cta-band"', content, re.MULTILINE)
        if not cta_match:
            skipped_no_cta += 1
            continue

        # Pick related articles
        if is_borough_guide(slug):
            related = pick_related_borough(slug, posts)
        else:
            related = pick_related_general(slug, posts)

        if not related:
            skipped_no_related += 1
            continue

        # Build the section HTML
        section_html = build_related_html(related, posts)

        # Insert just before the CTA band
        insert_pos = cta_match.start()
        new_content = content[:insert_pos] + section_html + "\n" + content[insert_pos:]

        filepath.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"  + {slug}.html ({len(related)} related)")

    print(f"\nDone. {updated} posts updated.")
    if skipped_already:
        print(f"  Skipped (already has related articles): {skipped_already}")
    if skipped_no_cta:
        print(f"  Skipped (no CTA band found): {skipped_no_cta}")
    if skipped_no_related:
        print(f"  Skipped (no related articles found): {skipped_no_related}")


if __name__ == "__main__":
    main()
