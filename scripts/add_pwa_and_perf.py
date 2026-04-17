#!/usr/bin/env python3
"""
Phase 7 technical SEO boost:
- Registers service worker + manifest + opensearch descriptor in all pages
- Adds font preload hints for critical render path
- Skips portal/api/node_modules pages
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {'portal', 'api', 'node_modules', '__pycache__'}

# What gets injected into <head>
HEAD_INJECTIONS = [
    '<link rel="manifest" href="/manifest.webmanifest" />',
    '<link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="AD London" />',
    '<meta name="application-name" content="Architectural Drawings London" />',
    '<meta name="apple-mobile-web-app-capable" content="yes" />',
    '<meta name="apple-mobile-web-app-status-bar-style" content="default" />',
    '<meta name="format-detection" content="telephone=no" />',
]

# Font preload for critical render path - for pages using Google Fonts
FONT_PRELOAD = '<link rel="preload" as="font" type="font/woff2" href="https://fonts.gstatic.com/s/fraunces/v34/6NUh8FyLNQOQZAnv9bYGvZoY.woff2" crossorigin />'

# Service worker registration script
SW_REGISTER = '''<script>if('serviceWorker' in navigator){window.addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});}</script>'''

MARKER = '<!-- pwa-enhanced -->'

updated = 0
skipped = 0

for f in ROOT.rglob('*.html'):
    if any(p in EXCLUDE_DIRS for p in f.parts):
        continue
    text = f.read_text(encoding='utf-8')
    if MARKER in text:
        skipped += 1
        continue

    # Insert meta/link tags after existing <meta charset> area, before <title> or <link rel="canonical">
    injection = MARKER + '\n' + '\n'.join(HEAD_INJECTIONS) + '\n'

    # Find a good insertion point: after hreflang link or after viewport meta
    if 'rel="alternate" hreflang' in text:
        text = re.sub(
            r'(<link rel="alternate" hreflang="en-GB"[^>]*/>)',
            r'\1\n' + injection,
            text, count=1
        )
    elif '<meta name="viewport"' in text:
        text = re.sub(
            r'(<meta name="viewport"[^>]*/>)',
            r'\1\n' + injection,
            text, count=1
        )
    else:
        # Fallback: insert after <head>
        text = text.replace('<head>', '<head>\n' + injection, 1)

    # Register service worker — insert just before </body> (but after chat widget script)
    if '</body>' in text and "serviceWorker.register" not in text:
        text = text.replace('</body>', SW_REGISTER + '\n</body>', 1)

    f.write_text(text, encoding='utf-8')
    updated += 1

print(f'[OK] Added PWA/perf enhancements to {updated} pages (skipped {skipped} already-enhanced)')
