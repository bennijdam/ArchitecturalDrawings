#!/usr/bin/env python3
"""Rebuild sitemap.xml with all core pages + 199 pSEO pages."""
import sys
sys.path.insert(0, '/home/claude')
from pseo_boroughs import BOROUGH_SLUGS, BOROUGHS
from pseo_services import SERVICE_SLUGS
from pathlib import Path

BASE = "https://architecturaldrawings.co.uk"
DATE = "2026-04-13"

urls = []

# Core pages
core = [
    ("/", "1.0", "weekly"),
    ("/services.html", "0.9", "monthly"),
    ("/pricing.html", "0.9", "monthly"),
    ("/about.html", "0.7", "monthly"),
    ("/search.html", "0.5", "monthly"),
    ("/services/planning-drawings.html", "0.9", "monthly"),
    ("/services/building-regulations.html", "0.9", "monthly"),
    ("/services/loft-conversions.html", "0.9", "monthly"),
    ("/services/house-extensions.html", "0.9", "monthly"),
    ("/services/mansard-roof.html", "0.9", "monthly"),
]
for loc, priority, freq in core:
    urls.append(f"  <url><loc>{BASE}{loc}</loc><lastmod>{DATE}</lastmod><priority>{priority}</priority><changefreq>{freq}</changefreq></url>")

# Areas master
urls.append(f"  <url><loc>{BASE}/areas/</loc><lastmod>{DATE}</lastmod><priority>0.8</priority><changefreq>monthly</changefreq></url>")

# Each borough hub + services
for slug in BOROUGH_SLUGS:
    urls.append(f"  <url><loc>{BASE}/areas/{slug}/</loc><lastmod>{DATE}</lastmod><priority>0.7</priority><changefreq>monthly</changefreq></url>")
    for svc in SERVICE_SLUGS:
        urls.append(f"  <url><loc>{BASE}/areas/{slug}/{svc}.html</loc><lastmod>{DATE}</lastmod><priority>0.7</priority><changefreq>monthly</changefreq></url>")

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"

out = Path("/home/claude/architectural-drawings/sitemap.xml")
out.write_text(xml)

# Count URLs
print(f"✓ sitemap.xml — {len(urls)} URLs")
