#!/usr/bin/env python3
"""
Schema markup validator + BreadcrumbList auto-adder.
- Parses every JSON-LD block
- Reports invalid JSON
- Counts schema types across the site
- Adds BreadcrumbList schema to pages missing it
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {'portal', 'api', 'node_modules', '__pycache__'}
BASE = 'https://www.architecturaldrawings.uk'

schema_counts = {}
invalid_files = []
missing_breadcrumb = []
added_breadcrumb = 0
total = 0

for f in ROOT.rglob('*.html'):
    if any(p in EXCLUDE_DIRS for p in f.parts):
        continue
    total += 1
    text = f.read_text(encoding='utf-8')

    # Find all JSON-LD blocks
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.DOTALL)

    has_breadcrumb = False
    for block in blocks:
        try:
            data = json.loads(block.strip())
            items = data if isinstance(data, list) else [data]
            for item in items:
                t = item.get('@type', 'Unknown')
                if isinstance(t, list):
                    t = t[0]
                schema_counts[t] = schema_counts.get(t, 0) + 1
                if t == 'BreadcrumbList':
                    has_breadcrumb = True
        except json.JSONDecodeError as e:
            invalid_files.append((str(f.relative_to(ROOT)), str(e)[:60]))

    if not has_breadcrumb:
        # Try to add a minimal BreadcrumbList based on path
        rel = f.relative_to(ROOT).as_posix()
        segments = [s for s in rel.split('/') if s and s != 'index.html']
        if not segments:
            # root index.html — already has it, skip
            continue

        # Build breadcrumb items
        items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{BASE}/'}]
        path_so_far = ''
        for i, seg in enumerate(segments):
            path_so_far += '/' + seg
            name_base = seg.replace('.html', '').replace('-', ' ').title()
            # Last item: no URL (per Google docs)
            if i == len(segments) - 1:
                items.append({'@type': 'ListItem', 'position': i + 2, 'name': name_base})
            else:
                items.append({'@type': 'ListItem', 'position': i + 2, 'name': name_base, 'item': f'{BASE}{path_so_far}/'})

        breadcrumb = {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': items
        }
        snippet = '<script type="application/ld+json">\n' + json.dumps(breadcrumb, separators=(',', ':')) + '\n</script>\n'

        # Insert into <head>, before </head>
        if '</head>' in text:
            text = text.replace('</head>', snippet + '</head>', 1)
            f.write_text(text, encoding='utf-8')
            added_breadcrumb += 1

print(f'=== Schema Audit Report ===')
print(f'Total pages scanned: {total}')
print(f'\nSchema type distribution:')
for t, c in sorted(schema_counts.items(), key=lambda x: -x[1]):
    print(f'  {t:.<40} {c}')

print(f'\nPages with invalid JSON-LD: {len(invalid_files)}')
for path, err in invalid_files[:10]:
    print(f'  {path}: {err}')
if len(invalid_files) > 10:
    print(f'  ... and {len(invalid_files) - 10} more')

print(f'\nBreadcrumbList added to: {added_breadcrumb} pages')
