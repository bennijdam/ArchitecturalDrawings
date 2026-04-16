#!/usr/bin/env python3
"""Rebuild sitemap index + 3 sub-sitemaps for better crawl efficiency."""
import sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from pseo_boroughs import BOROUGH_SLUGS, BOROUGHS
from pseo_services import SERVICE_SLUGS

BASE = "https://www.architecturaldrawings.uk"
DATE = "2026-04-16"

def make_url(loc, priority, freq):
    return f"  <url><loc>{BASE}{loc}</loc><lastmod>{DATE}</lastmod><priority>{priority}</priority><changefreq>{freq}</changefreq></url>"

def write_sitemap(filename, urls):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    (SCRIPT_DIR / filename).write_text(xml, encoding="utf-8")
    return len(urls)

# ============================================================
# SITEMAP 1: Core pages + tools + blog
# ============================================================
core_urls = []

# Core pages
core_pages = [
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
    ("/why-us.html", "0.8", "monthly"),
    ("/privacy.html", "0.3", "yearly"),
    ("/terms.html", "0.3", "yearly"),
    ("/team/", "0.7", "monthly"),
    ("/faq/", "0.8", "monthly"),
    ("/glossary/", "0.7", "monthly"),
    ("/calculator/", "0.8", "monthly"),
    ("/tools/pd-checker/", "0.8", "monthly"),
    ("/resources/", "0.7", "monthly"),
    ("/projects/", "0.7", "monthly"),
    ("/projects/side-return-camden.html", "0.6", "monthly"),
    ("/projects/dormer-loft-hackney.html", "0.6", "monthly"),
    ("/projects/mansard-islington.html", "0.6", "monthly"),
    ("/projects/double-storey-wandsworth.html", "0.6", "monthly"),
    ("/projects/planning-regs-southwark.html", "0.6", "monthly"),
]
for loc, priority, freq in core_pages:
    core_urls.append(make_url(loc, priority, freq))

# Blog hub + all posts
core_urls.append(make_url("/blog/", "0.8", "weekly"))

blog_posts = [
    "planning-permission-london", "building-regulations-explained",
    "architect-vs-architectural-technologist", "planning-vs-permitted-development",
    "planning-drawings-cost-london", "extension-cost-guide-london",
    "loft-vs-mansard", "drawing-service-vs-architect",
    "kitchen-extension-cost-london", "permitted-development-rules-2026",
    "planning-permission-refused-what-next", "side-return-extension-guide",
    "loft-conversion-without-planning", "choosing-architect-london",
    "building-regs-part-l-guide", "conservation-area-planning-london",
    "hmo-conversion-guide-london", "flat-conversion-guide-london",
    "outbuilding-planning-guide", "wraparound-extension-guide",
    "double-storey-extension-guide", "change-of-use-planning-london",
    "dormer-vs-velux-loft", "labc-vs-approved-inspector",
    "full-planning-vs-prior-approval", "architect-fees-vs-fixed-fee",
    # Phase 2 comparison/guide posts
    "rear-vs-side-extension", "planning-agent-vs-diy",
    "how-long-planning-permission", "party-wall-guide-london",
    "structural-engineer-guide", "garden-room-planning-london",
    "basement-conversion-guide-london", "hip-to-gable-loft-guide",
    "flat-roof-extension-guide", "pre-application-advice-london",
]
for slug in blog_posts:
    core_urls.append(make_url(f"/blog/{slug}.html", "0.8", "monthly"))

# Borough planning guides
for borough_slug in BOROUGH_SLUGS:
    core_urls.append(make_url(f"/blog/planning-{borough_slug}.html", "0.7", "monthly"))

# Borough extension cost guides
for borough_slug in BOROUGH_SLUGS:
    core_urls.append(make_url(f"/blog/extension-cost-{borough_slug}.html", "0.7", "monthly"))

# Borough loft conversion guides
for borough_slug in BOROUGH_SLUGS:
    core_urls.append(make_url(f"/blog/loft-cost-{borough_slug}.html", "0.7", "monthly"))

# Cornerstone guide hubs
core_urls.append(make_url("/guides/extensions/", "0.9", "monthly"))
core_urls.append(make_url("/guides/lofts/", "0.9", "monthly"))
core_urls.append(make_url("/guides/planning/", "0.9", "monthly"))

# Additional case studies
for slug in ["garage-conversion-ealing", "basement-dig-kensington", "hmo-conversion-hackney", "rear-dormer-lewisham", "wraparound-extension-wandsworth"]:
    core_urls.append(make_url(f"/projects/{slug}.html", "0.6", "monthly"))

count_core = write_sitemap("sitemap-core.xml", core_urls)

# ============================================================
# SITEMAP 2: Areas (pSEO + neighbourhoods)
# ============================================================
area_urls = []

# Areas master index
area_urls.append(make_url("/areas/", "0.8", "monthly"))

# Borough hubs + services
for slug in BOROUGH_SLUGS:
    area_urls.append(make_url(f"/areas/{slug}/", "0.7", "monthly"))
    for svc in SERVICE_SLUGS:
        area_urls.append(make_url(f"/areas/{slug}/{svc}.html", "0.7", "monthly"))

# Neighbourhood pages (discover from filesystem)
neighbourhoods_dir = SCRIPT_DIR / "areas" / "neighbourhoods"
if neighbourhoods_dir.exists():
    for f in sorted(neighbourhoods_dir.glob("*.html")):
        area_urls.append(make_url(f"/areas/neighbourhoods/{f.name}", "0.6", "monthly"))

count_areas = write_sitemap("sitemap-areas.xml", area_urls)

# ============================================================
# SITEMAP INDEX
# ============================================================
total = count_core + count_areas
index_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{BASE}/sitemap-core.xml</loc><lastmod>{DATE}</lastmod></sitemap>
  <sitemap><loc>{BASE}/sitemap-areas.xml</loc><lastmod>{DATE}</lastmod></sitemap>
</sitemapindex>
'''
(SCRIPT_DIR / "sitemap.xml").write_text(index_xml, encoding="utf-8")

print(f"[OK] sitemap.xml — sitemap index (2 sub-sitemaps)")
print(f"  sitemap-core.xml — {count_core} URLs (core + blog + tools)")
print(f"  sitemap-areas.xml — {count_areas} URLs (boroughs + neighbourhoods)")
print(f"  Total: {total} URLs")
