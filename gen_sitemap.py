#!/usr/bin/env python3
"""Rebuild sitemap.xml with all core pages + 199 pSEO pages."""
import sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from pseo_boroughs import BOROUGH_SLUGS, BOROUGHS
from pseo_services import SERVICE_SLUGS

BASE = "https://www.architecturaldrawings.uk"
DATE = "2026-04-16"

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
    ("/privacy.html", "0.3", "yearly"),
    ("/terms.html", "0.3", "yearly"),
    ("/blog/", "0.8", "weekly"),
    ("/blog/planning-permission-london.html", "0.8", "monthly"),
    ("/blog/building-regulations-explained.html", "0.8", "monthly"),
    ("/blog/architect-vs-architectural-technologist.html", "0.8", "monthly"),
    ("/blog/planning-vs-permitted-development.html", "0.8", "monthly"),
    ("/blog/planning-drawings-cost-london.html", "0.8", "monthly"),
    ("/blog/extension-cost-guide-london.html", "0.8", "monthly"),
    ("/blog/loft-vs-mansard.html", "0.8", "monthly"),
    ("/blog/drawing-service-vs-architect.html", "0.8", "monthly"),
    ("/blog/kitchen-extension-cost-london.html", "0.8", "monthly"),
    ("/blog/permitted-development-rules-2026.html", "0.8", "monthly"),
    ("/blog/planning-permission-refused-what-next.html", "0.8", "monthly"),
    ("/blog/side-return-extension-guide.html", "0.8", "monthly"),
    ("/blog/loft-conversion-without-planning.html", "0.8", "monthly"),
    ("/blog/choosing-architect-london.html", "0.8", "monthly"),
    ("/blog/building-regs-part-l-guide.html", "0.8", "monthly"),
    ("/blog/conservation-area-planning-london.html", "0.8", "monthly"),
    ("/projects/", "0.7", "monthly"),
    ("/projects/side-return-camden.html", "0.6", "monthly"),
    ("/projects/dormer-loft-hackney.html", "0.6", "monthly"),
    ("/projects/mansard-islington.html", "0.6", "monthly"),
    ("/projects/double-storey-wandsworth.html", "0.6", "monthly"),
    ("/projects/planning-regs-southwark.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/hampstead.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/clapham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/dulwich.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/muswell-hill.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/notting-hill.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/crouch-end.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/brixton.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/chiswick.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/peckham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/wimbledon.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/battersea.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/fulham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/highgate.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/stoke-newington.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/richmond.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/angel-islington.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/shoreditch.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/dalston.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/camden-town.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/kentish-town.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/belsize-park.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/finsbury-park.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/holloway.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/tooting.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/balham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/bermondsey.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/streatham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/herne-hill.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/blackheath.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/deptford.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/woolwich.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/bow.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/bethnal-green.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/acton.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/twickenham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/teddington.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/wembley.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/kilburn.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/tottenham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/wood-green.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/walthamstow.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/sydenham.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/forest-hill.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/east-dulwich.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/earlsfield.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/putney.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/barnes.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/maida-vale.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/hackney-wick.html", "0.6", "monthly"),
    ("/areas/neighbourhoods/queens-park.html", "0.6", "monthly"),
    ("/team/", "0.7", "monthly"),
    ("/faq/", "0.8", "monthly"),
    ("/glossary/", "0.7", "monthly"),
    ("/calculator/", "0.8", "monthly"),
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

out = SCRIPT_DIR / "sitemap.xml"
out.write_text(xml, encoding="utf-8")

# Count URLs
print(f"[OK] sitemap.xml — {len(urls)} URLs")
