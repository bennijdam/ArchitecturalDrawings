#!/usr/bin/env python3
"""
Topic cluster internal linking: add pillar-page context strip to spoke content.
Every blog post + pSEO page gets a subtle link bar at the top pointing to the pillar guide
for its topic cluster. Pillar hubs get a visual "you are here" marker.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {'portal', 'api', 'node_modules', '__pycache__'}

# Pillar hubs and their topic clusters (slug keywords -> pillar URL)
PILLARS = [
    {
        'title': 'Extensions',
        'url': '/guides/extensions/',
        'keywords': ['extension', 'rear', 'side-return', 'wraparound', 'double-storey', 'kitchen-extension', 'flat-roof-extension', 'house-extensions'],
    },
    {
        'title': 'Lofts',
        'url': '/guides/lofts/',
        'keywords': ['loft', 'dormer', 'mansard', 'hip-to-gable', 'velux'],
    },
    {
        'title': 'Planning',
        'url': '/guides/planning/',
        'keywords': ['planning', 'permitted-development', 'conservation-area', 'article-4', 'pre-application', 'full-planning', 'prior-approval', 'lawful-development'],
    },
]

MARKER = '<!-- pillar-link -->'

def find_pillar(filename):
    fn = filename.lower()
    for p in PILLARS:
        for kw in p['keywords']:
            if kw in fn:
                return p
    return None

def make_strip(pillar, depth_prefix):
    """Build a subtle breadcrumb-style pillar link banner."""
    url = pillar['url']
    # Adjust URL for depth (if in /blog/, URL needs to stay absolute-ish)
    if depth_prefix:
        url = depth_prefix.rstrip('/') + url
    return (
        f'{MARKER}\n'
        f'<div style="background:var(--bg-2);border-bottom:1px solid var(--line);padding:10px 0;">'
        f'<div class="container" style="display:flex;align-items:center;justify-content:space-between;gap:16px;font-size:0.82rem;flex-wrap:wrap;">'
        f'<span style="color:var(--ink-soft);">Part of our <strong style="color:var(--ink);">{pillar["title"]} guide cluster</strong></span>'
        f'<a href="{url}" style="color:var(--accent-deep);font-weight:600;text-decoration:none;">View all {pillar["title"].lower()} guides &rarr;</a>'
        f'</div>'
        f'</div>\n'
    )

updated = 0
skipped = 0

for f in ROOT.rglob('*.html'):
    if any(p in EXCLUDE_DIRS for p in f.parts):
        continue
    # Skip hub pages, tools, and pages already linked
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith('guides/'):
        continue
    # Only add to blog posts, pSEO, and neighbourhood pages
    if not (rel.startswith('blog/') or rel.startswith('areas/')):
        continue
    if rel in ('blog/index.html', 'areas/index.html'):
        continue

    text = f.read_text(encoding='utf-8')
    if MARKER in text:
        skipped += 1
        continue

    pillar = find_pillar(f.stem)
    if not pillar:
        continue

    # Insert right after <body>
    strip = make_strip(pillar, '')  # absolute URLs work from anywhere
    text = re.sub(r'(<body[^>]*>)', r'\1\n' + strip, text, count=1)

    f.write_text(text, encoding='utf-8')
    updated += 1

print(f'[OK] Added pillar cluster links to {updated} pages (skipped {skipped} already-linked)')
