#!/usr/bin/env python3
"""Rebuild sitemap index + 3 sub-sitemaps for better crawl efficiency."""
import sys
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from pseo_boroughs import BOROUGH_SLUGS, BOROUGHS
from pseo_services import SERVICE_SLUGS

BASE = "https://www.architecturaldrawings.uk"

def get_lastmod(filepath):
    """Get lastmod date from file's modification time. Falls back to today."""
    try:
        mtime = Path(filepath).stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")
    except (FileNotFoundError, OSError):
        return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

def make_url(loc, priority, freq, filepath=None):
    """Build URL entry. If filepath given, use its mtime; otherwise use today."""
    if filepath:
        lastmod = get_lastmod(filepath)
    else:
        # For generated/derived pages with no filesystem backing, use today's date
        lastmod = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    return f"  <url><loc>{BASE}{loc}</loc><lastmod>{lastmod}</lastmod><priority>{priority}</priority><changefreq>{freq}</changefreq></url>"

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
    ("/guides/extensions/", "0.9", "monthly"),
    ("/guides/lofts/", "0.9", "monthly"),
    ("/guides/planning/", "0.9", "monthly"),
    ("/guides/properties/victorian-terrace/", "0.8", "monthly"),
    ("/guides/properties/edwardian-semi/", "0.8", "monthly"),
    ("/guides/properties/georgian-townhouse/", "0.8", "monthly"),
    ("/guides/properties/1930s-semi/", "0.8", "monthly"),
    ("/guides/properties/modern-flat/", "0.8", "monthly"),
    ("/tools/planning-timeline/", "0.8", "monthly"),
    ("/tools/planning-fee-calculator/", "0.8", "monthly"),
    ("/tools/pd-volume-calculator/", "0.8", "monthly"),
    ("/stats/", "0.8", "monthly"),
    # M25 commuter belt
    ("/areas/commuter/", "0.8", "monthly"),
    ("/areas/commuter/guildford/", "0.7", "monthly"),
    ("/areas/commuter/woking/", "0.7", "monthly"),
    ("/areas/commuter/epsom/", "0.7", "monthly"),
    ("/areas/commuter/reigate/", "0.7", "monthly"),
    ("/areas/commuter/dorking/", "0.7", "monthly"),
    ("/areas/commuter/staines-upon-thames/", "0.7", "monthly"),
    ("/areas/commuter/leatherhead/", "0.7", "monthly"),
    ("/areas/commuter/watford/", "0.7", "monthly"),
    ("/areas/commuter/st-albans/", "0.7", "monthly"),
    ("/areas/commuter/hemel-hempstead/", "0.7", "monthly"),
    ("/areas/commuter/hertford/", "0.7", "monthly"),
    ("/areas/commuter/stevenage/", "0.7", "monthly"),
    ("/areas/commuter/welwyn-garden-city/", "0.7", "monthly"),
    ("/areas/commuter/brentwood/", "0.7", "monthly"),
    ("/areas/commuter/chelmsford/", "0.7", "monthly"),
    ("/areas/commuter/harlow/", "0.7", "monthly"),
    ("/areas/commuter/epping/", "0.7", "monthly"),
    ("/areas/commuter/loughton/", "0.7", "monthly"),
    ("/areas/commuter/sevenoaks/", "0.7", "monthly"),
    ("/areas/commuter/tunbridge-wells/", "0.7", "monthly"),
    ("/areas/commuter/tonbridge/", "0.7", "monthly"),
    ("/areas/commuter/dartford/", "0.7", "monthly"),
    ("/areas/commuter/gravesend/", "0.7", "monthly"),
    ("/areas/commuter/high-wycombe/", "0.7", "monthly"),
    ("/areas/commuter/amersham/", "0.7", "monthly"),
    ("/areas/commuter/beaconsfield/", "0.7", "monthly"),
    ("/areas/commuter/slough/", "0.7", "monthly"),
    ("/areas/commuter/windsor/", "0.7", "monthly"),
    ("/areas/commuter/luton/", "0.7", "monthly"),
    ("/areas/commuter/oxford/", "0.7", "monthly"),
    # UK cities
    ("/areas/uk/", "0.7", "monthly"),
    ("/areas/uk/nationwide/", "0.7", "monthly"),
    ("/areas/uk/manchester/", "0.7", "monthly"),
    ("/areas/uk/birmingham/", "0.7", "monthly"),
    ("/areas/uk/leeds/", "0.7", "monthly"),
    ("/areas/uk/liverpool/", "0.7", "monthly"),
    ("/areas/uk/bristol/", "0.7", "monthly"),
    ("/areas/uk/edinburgh/", "0.7", "monthly"),
    ("/areas/uk/glasgow/", "0.7", "monthly"),
    ("/areas/uk/brighton/", "0.7", "monthly"),
    ("/areas/uk/cambridge/", "0.7", "monthly"),
    ("/areas/uk/oxford/", "0.7", "monthly"),
    ("/areas/uk/bath/", "0.7", "monthly"),
    ("/areas/uk/york/", "0.7", "monthly"),
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
    # Map URL path to filesystem path
    if loc == "/":
        filepath = SCRIPT_DIR / "index.html"
    elif loc.endswith("/"):
        filepath = SCRIPT_DIR / loc.lstrip("/") / "index.html"
    else:
        filepath = SCRIPT_DIR / loc.lstrip("/")

    core_urls.append(make_url(loc, priority, freq, str(filepath)))

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
    filepath = SCRIPT_DIR / "blog" / f"{slug}.html"
    core_urls.append(make_url(f"/blog/{slug}.html", "0.8", "monthly", str(filepath)))

# Borough planning guides
for borough_slug in BOROUGH_SLUGS:
    filepath = SCRIPT_DIR / "blog" / f"planning-{borough_slug}.html"
    core_urls.append(make_url(f"/blog/planning-{borough_slug}.html", "0.7", "monthly", str(filepath)))

# Borough extension cost guides
for borough_slug in BOROUGH_SLUGS:
    filepath = SCRIPT_DIR / "blog" / f"extension-cost-{borough_slug}.html"
    core_urls.append(make_url(f"/blog/extension-cost-{borough_slug}.html", "0.7", "monthly", str(filepath)))

# Borough loft conversion guides
for borough_slug in BOROUGH_SLUGS:
    filepath = SCRIPT_DIR / "blog" / f"loft-cost-{borough_slug}.html"
    core_urls.append(make_url(f"/blog/loft-cost-{borough_slug}.html", "0.7", "monthly", str(filepath)))

# Cornerstone guide hubs
core_urls.append(make_url("/guides/extensions/", "0.9", "monthly"))
core_urls.append(make_url("/guides/lofts/", "0.9", "monthly"))
core_urls.append(make_url("/guides/planning/", "0.9", "monthly"))

# Additional case studies
for slug in ["garage-conversion-ealing", "basement-dig-kensington", "hmo-conversion-hackney", "rear-dormer-lewisham", "wraparound-extension-wandsworth"]:
    filepath = SCRIPT_DIR / "projects" / f"{slug}.html"
    core_urls.append(make_url(f"/projects/{slug}.html", "0.6", "monthly", str(filepath)))

count_core = write_sitemap("sitemap-core.xml", core_urls)

# ============================================================
# SITEMAP 2: Areas (pSEO + neighbourhoods)
# ============================================================
area_urls = []

# Areas master index
area_urls.append(make_url("/areas/", "0.8", "monthly"))

# Borough hubs + services
for slug in BOROUGH_SLUGS:
    filepath = SCRIPT_DIR / "areas" / slug / "index.html"
    area_urls.append(make_url(f"/areas/{slug}/", "0.7", "monthly", str(filepath)))
    for svc in SERVICE_SLUGS:
        filepath = SCRIPT_DIR / "areas" / slug / f"{svc}.html"
        area_urls.append(make_url(f"/areas/{slug}/{svc}.html", "0.7", "monthly", str(filepath)))

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
today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
index_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{BASE}/sitemap-core.xml</loc><lastmod>{today}</lastmod></sitemap>
  <sitemap><loc>{BASE}/sitemap-areas.xml</loc><lastmod>{today}</lastmod></sitemap>
</sitemapindex>
'''
(SCRIPT_DIR / "sitemap.xml").write_text(index_xml, encoding="utf-8")

print(f"[OK] sitemap.xml — sitemap index (2 sub-sitemaps)")
print(f"  sitemap-core.xml — {count_core} URLs (core + blog + tools)")
print(f"  sitemap-areas.xml — {count_areas} URLs (boroughs + neighbourhoods)")
print(f"  Total: {total} URLs")
