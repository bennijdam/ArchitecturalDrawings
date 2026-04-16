#!/usr/bin/env python3
"""
Programmatic SEO page generator for Architectural Drawings London.

Creates:
- 33 boroughs × 5 services = 165 location-service pages
- 33 borough hub pages (index.html per borough)
- 1 master areas index
= 199 pages total

Each page is SEO/AEO/GEO optimized:
- SEO: exact-match keyword in H1, URL, title; local entity density; schema markup
- AEO: direct-answer FAQ blocks, TL;DR summary, structured data
- GEO: citable facts with numbers, entity clarity, author/credential signals, dated content
"""
import sys
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from pseo_boroughs import BOROUGHS, BOROUGH_SLUGS, adjacent_names
from pseo_services import SERVICES, SERVICE_SLUGS

# Output
PROJECT = SCRIPT_DIR
AREAS_DIR = PROJECT / "areas"
AREAS_DIR.mkdir(exist_ok=True)

# Load inline CSS from the existing style.css (we inline into every page)
CSS = (PROJECT / "assets/css/style.css").read_text(encoding="utf-8")

# Additional CSS for pSEO-specific components (TL;DR box, fact grid, local stats)
PSEO_CSS = """
/* ===== Footer dark ===== */
.footer { background: var(--ink); color: rgba(250,250,247,0.6); }
.footer .logo { color: var(--bg); }
.footer-bottom { border-top-color: rgba(255,255,255,0.1); color: rgba(250,250,247,0.5); }

/* ===== Footer SEO ===== */
.footer-seo { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.5rem; padding-bottom: 3rem; margin-bottom: 3rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
@media (max-width: 820px) { .footer-seo { grid-template-columns: 1fr 1fr; gap: 2rem; } }
@media (max-width: 500px) { .footer-seo { grid-template-columns: 1fr; } }
.footer-seo h5 { font-family: var(--font-body); font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em; color: var(--bg); margin-bottom: 1.25rem; }
.footer-seo ul { list-style: none; display: flex; flex-direction: column; gap: 0.55rem; }
.footer-seo a { font-size: 0.85rem; color: rgba(250,250,247,0.45); transition: color 0.3s var(--ease); line-height: 1.4; }
.footer-seo a:hover { color: var(--accent); }

/* ===== pSEO additions ===== */
.tldr {
  background: var(--surface);
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  border-radius: var(--r-lg);
  padding: 28px 32px;
  margin: 32px 0;
}
.tldr h3 {
  font-size: 0.82rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-deep);
  font-family: var(--font-body);
  font-weight: 700;
  margin-bottom: 14px;
}
.tldr dl {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px 32px;
}
@media (max-width: 720px) { .tldr dl { grid-template-columns: 1fr; } }
.tldr dt {
  font-size: 0.84rem;
  color: var(--ink-soft);
  margin-bottom: 2px;
}
.tldr dd {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-variation-settings: "opsz" 36;
  letter-spacing: -0.005em;
  color: var(--ink);
}

.local-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 32px 0;
}
@media (max-width: 900px) { .local-grid { grid-template-columns: repeat(2, 1fr); } }
.local-stat {
  background: var(--bg-2);
  border-radius: var(--r-md);
  padding: 20px 22px;
}
.local-stat-label { font-size: 0.78rem; color: var(--ink-soft); margin-bottom: 6px; }
.local-stat-value {
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-variation-settings: "opsz" 60;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.adjacent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin: 20px 0;
}
.adjacent-card {
  padding: 16px 20px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  transition: all 0.2s var(--ease);
  display: block;
}
.adjacent-card:hover {
  border-color: var(--accent);
  background: var(--accent-soft);
  transform: translateY(-2px);
}
.adjacent-card strong { display: block; color: var(--ink); font-size: 0.96rem; }
.adjacent-card span { font-size: 0.82rem; color: var(--ink-soft); }

.related-services {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
  margin: 20px 0;
}
"""

# -------- Helper functions --------

def article_4_answer(b):
    """Generate Article 4 answer for this borough."""
    if b["article_4"]:
        return (f"Yes — {b['name']} has Article 4 Directions in force. "
                f"{b['article_4_notes']} "
                "Article 4 removes specific permitted development rights that would otherwise apply, "
                "meaning full planning permission is required where PD would normally be sufficient. "
                "We check Article 4 status for your specific property before quoting.")
    else:
        return (f"{b['name']} does not currently have a borough-wide Article 4 Direction for "
                "residential extensions or HMO conversions. Most householder permitted development "
                f"rights apply normally in {b['name']} — though conservation areas and listed "
                "buildings still restrict PD. We confirm at the free site survey.")

def loft_planning_answer(b):
    """Generate loft permission answer for this borough."""
    if b["article_4"]:
        return (f"It depends on your exact address in {b['name']}. Most standard loft conversions "
                "qualify as Permitted Development (no planning permission needed) if under 40m³ "
                "for terraced or 50m³ for semi-detached, with matching materials and 20cm eaves setback. "
                f"However {b['name']} has Article 4 Directions that may remove these rights — "
                "and flats, conservation areas and listed buildings always require full planning. "
                "We confirm permitted development eligibility at the free feasibility visit.")
    else:
        return (f"Most loft conversions in {b['name']} qualify as Permitted Development under the "
                "standard householder allowances — up to 40m³ for terraced or 50m³ for semi-detached, "
                "with matching materials and 20cm eaves setback. Flats, properties in conservation "
                "areas and listed buildings need full planning. We check eligibility at the free site visit.")

def mansard_answer(b):
    """Generate mansard approval likelihood for this borough."""
    conservation = b["notable_conservation"]
    if "mansard" in b.get("character", "").lower() or b["name"] in ["Hackney", "Islington", "Tower Hamlets", "Lambeth", "Southwark"]:
        return (f"Very often yes in {b['name']}. Rear mansards are routinely approved by "
                f"{b['planning_authority']} where the design matches the terrace — including within "
                f"conservation areas like {conservation.split(',')[0].strip()}. "
                "A Heritage Statement and sensitive design following the borough's published guidance "
                "are essential for conservation area mansards.")
    elif b["name"] in ["Westminster", "Kensington and Chelsea", "Camden"]:
        return (f"Mansards in {b['name']} are more heavily scrutinised than in outer boroughs. "
                f"{b['planning_authority']} prioritises heritage and townscape — approvals require "
                "exceptional design quality, clear precedents on the street, and a full Heritage Statement. "
                "We've delivered mansard approvals in the borough; each application is bespoke.")
    else:
        return (f"Mansards in {b['name']} are less common historically — {b['planning_authority']} "
                "considers each application on its merits. Rear mansards on suitable terraced or "
                "semi-detached properties, matching the roofscape, have a reasonable approval "
                "rate with the right design and supporting heritage commentary where relevant.")

def extension_planning_answer(b):
    """Generate extension planning answer."""
    if b["article_4"]:
        return (f"Most standard extensions in {b['name']} fall under Permitted Development — single-storey rear up to 3m (attached) or 4m (detached), side returns up to half the width of the house. "
                f"However, {b['name']} has Article 4 Directions that may remove these rights in specific streets, "
                "and flats, listed buildings and conservation areas always need full planning. "
                "We check PD eligibility before quoting.")
    else:
        return (f"Most standard extensions in {b['name']} qualify as Permitted Development — single-storey rear up to 3m/4m, side extensions up to half the width of the house, under standard national rules. "
                "Flats, listed buildings and conservation areas need full planning permission. "
                "We confirm eligibility at the free site survey.")

def basement_answer(b):
    """Generate basement policy answer."""
    if b["basement_policy"]:
        return (f"{b['name']} has a specific basement policy. {b.get('basement_notes', '')}")
    else:
        return (f"{b['name']} does not have a borough-specific basement policy beyond the national framework — "
                "basement conversions are generally permissible subject to structural, drainage and "
                "flood-risk considerations. Thames Water Build Over Agreements apply where you're within "
                "3m of a public sewer.")


def fill_placeholders(text, borough, service=None):
    """Replace {location}, {location_council}, {conservation_list} etc. in service copy."""
    if not text:
        return text

    conservation_list = borough["notable_conservation"]
    # "A, B, C, D, E" → "A, B, and C" (first 3)
    parts = [p.strip() for p in conservation_list.split(",")]
    short_list = ", ".join(parts[:3]) + (" and others" if len(parts) > 3 else "")
    first_conservation = parts[0] if parts else borough["name"]

    typical_short = borough["typical_housing"].split(";")[0].strip()
    if typical_short.endswith("."):
        typical_short = typical_short[:-1]
    # lowercase first char for mid-sentence insertion
    if typical_short:
        typical_short = typical_short[0].lower() + typical_short[1:]

    building_control_route = f"{borough['planning_authority']} Building Control or an approved inspector"

    replacements = {
        "{location}": borough["name"],
        "{location_council}": borough["planning_authority"],
        "{authority}": borough["planning_authority"],
        "{conservation_count}": str(borough["conservation_areas"]),
        "{conservation_list}": short_list,
        "{conservation_first}": first_conservation,
        "{typical_housing_short}": typical_short,
        "{article_4_answer}": article_4_answer(borough),
        "{loft_planning_answer}": loft_planning_answer(borough),
        "{mansard_answer}": mansard_answer(borough),
        "{extension_planning_answer}": extension_planning_answer(borough),
        "{basement_answer}": basement_answer(borough),
        "{building_control_route}": building_control_route,
    }
    out = text
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def faq_schema_json(faqs):
    """Generate FAQPage schema JSON from FAQ list."""
    items = []
    for q, a in faqs:
        # Strip HTML tags for schema
        a_clean = re.sub(r'<[^>]+>', '', a)
        a_clean = a_clean.replace('"', '\\"').replace('\n', ' ')
        q_clean = q.replace('"', '\\"')
        items.append(
            f'{{"@type":"Question","name":"{q_clean}","acceptedAnswer":{{"@type":"Answer","text":"{a_clean}"}}}}'
        )
    return "[" + ",".join(items) + "]"


# ============================================================
# SERVICE-LOCATION PAGE TEMPLATE
# ============================================================

def render_service_location(borough_slug, service_slug):
    b = BOROUGHS[borough_slug]
    s = SERVICES[service_slug]

    location = b["name"]
    service_short = s["short"]
    price_from = s["price_display"]

    # Fill service copy
    summary = fill_placeholders(s["summary"], b)
    whats_included_html = "".join(
        f'<div class="service-card"><div class="service-icon">{SERVICE_ICON}</div><h3>{title}</h3><p>{fill_placeholders(desc, b)}</p></div>'
        for title, desc in s["what_included"]
    )

    # FAQs
    faqs = [(fill_placeholders(q, b), fill_placeholders(a, b)) for q, a in s["local_faqs"]]
    faq_html = "".join(
        f'<details class="faq-item"><summary class="faq-q">{q}<span class="faq-q-icon"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 2v8M2 6h8"/></svg></span></summary><div class="faq-a"><p>{a}</p></div></details>'
        for q, a in faqs
    )
    faq_schema = faq_schema_json(faqs)

    # Adjacent boroughs
    adjacent_html = "".join(
        f'<a href="../{adj}/{service_slug}.html" class="adjacent-card"><strong>{service_short.title()} in {BOROUGHS[adj]["name"]}</strong><span>Adjacent borough</span></a>'
        for adj in b["adjacent"] if adj in BOROUGHS
    )

    # Other services in this location
    other_services = [ss for ss in SERVICE_SLUGS if ss != service_slug]
    related_services_html = "".join(
        f'<a href="{ss}.html" class="service-card"><h3>{SERVICES[ss]["name"]} in {location}</h3><p>From {SERVICES[ss]["price_display"]}. {SERVICES[ss]["summary"][:120]}...</p><div class="service-card-footer"><span class="service-card-price"><span class="from">from</span>{SERVICES[ss]["price_display"]}</span><span class="service-card-link">View →</span></div></a>'
        for ss in other_services
    )

    # Page metadata
    title = f"{s['name']} in {location} | From {price_from} Fixed Fee · Architectural Drawings London"
    # Cap title to reasonable length
    if len(title) > 68:
        title = f"{s['name']} in {location} | Architectural Drawings London"
    meta_desc = (f"{s['name']} in {location} — fixed fee from {price_from}. "
                 f"MCIAT chartered team covering {b['planning_authority']}. "
                 f"Planning, building regs, structural calcs, {b['conservation_areas']} conservation areas, Article 4 checked.")[:159]

    # Image
    hero = s["hero_img"]

    # Quick facts box values
    article_4_short = "Yes" if b["article_4"] else "No"
    basement_note = "Restricted" if b["basement_policy"] else "Standard"

    # Canonical URL
    canonical = f"https://architecturaldrawings.co.uk/areas/{borough_slug}/{service_slug}.html"

    # Inline CSS + any data URI embed is deferred — external ref is fine for these pages (deploy-compatible)
    # But for standalone preview we inline. We'll inline the main CSS with pSEO additions.

    html = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#FAFAF7" />

<title>{title}</title>
<meta name="description" content="{meta_desc}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="{canonical}" />

<!-- Open Graph -->
<meta property="og:type" content="article" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{s['name']} in {location}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:locale" content="en_GB" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />

<!-- Schema: Service -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{s['name']}",
  "provider": {{
    "@type": "ProfessionalService",
    "name": "Architectural Drawings London",
    "@id": "https://architecturaldrawings.co.uk/#business",
    "url": "https://architecturaldrawings.co.uk/",
    "telephone": "+44 20 7946 0000",
    "priceRange": "££"
  }},
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "{location}",
    "containedInPlace": {{"@type": "City", "name": "London"}}
  }},
  "offers": {{"@type": "Offer", "price": "{s['price_from']}", "priceCurrency": "GBP"}},
  "description": "{meta_desc}"
}}
</script>

<!-- Schema: FAQPage (AEO) -->
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{faq_schema}}}
</script>

<!-- Schema: BreadcrumbList -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://architecturaldrawings.co.uk/"}},
    {{"@type": "ListItem", "position": 2, "name": "Areas", "item": "https://architecturaldrawings.co.uk/areas/"}},
    {{"@type": "ListItem", "position": 3, "name": "{location}", "item": "https://architecturaldrawings.co.uk/areas/{borough_slug}/"}},
    {{"@type": "ListItem", "position": 4, "name": "{s['name']}", "item": "{canonical}"}}
  ]
}}
</script>

<style>
{CSS}
{PSEO_CSS}
/* Reveal safety net */
@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="/" class="logo" aria-label="Architectural Drawings London home">
      <span class="logo-mark">A</span>
      <span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
        <li><a href="/services.html">Services</a></li>
        <li><a href="/pricing.html">Pricing</a></li>
        <li><a href="/areas/">Areas</a></li>
        <li><a href="/about.html">About</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a href="/portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="/quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<!-- ===== HERO with H1 = exact-match keyword ===== -->
<section class="hero">
  <div class="container hero-grid">
    <div>
      <nav aria-label="Breadcrumb" style="font-size: 0.85rem; color: var(--ink-soft); margin-bottom: 20px;">
        <a href="/" style="color: var(--ink-soft);">Home</a> /
        <a href="/areas/" style="color: var(--ink-soft);">Areas</a> /
        <a href="./" style="color: var(--ink-soft);">{location}</a> /
        <strong style="color: var(--ink);">{s['name']}</strong>
      </nav>
      <span class="eyebrow">{s['name']} · {location}</span>
      <h1 style="margin: 16px 0 24px;">{s['h1_lead']} in <span style="color: var(--accent); font-style: italic; font-weight: 300;">{location}</span></h1>
      <p class="hero-lede">{summary}</p>
      <div class="hero-ctas">
        <a href="/quote.html?service={service_slug}&amp;location={borough_slug}" class="btn btn-primary btn-lg">Get a free quote →</a>
        <a href="#pricing" class="btn btn-outline btn-lg">See pricing</a>
      </div>
      <div class="hero-trust" style="margin-top: 32px;">
        <span class="hero-trust-item"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>From {price_from} fixed fee</span>
        <span class="hero-trust-item"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>{s['turnaround']}</span>
        <span class="hero-trust-item"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Covering all {location} postcodes</span>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-img-main">
        <picture>
          <source type="image/avif" srcset="/assets/img/{hero}-640.avif 640w, /assets/img/{hero}-1024.avif 1024w, /assets/img/{hero}-1600.avif 1600w" sizes="(max-width: 960px) 100vw, 50vw" />
          <source type="image/webp" srcset="/assets/img/{hero}-640.webp 640w, /assets/img/{hero}-1024.webp 1024w, /assets/img/{hero}-1600.webp 1600w" sizes="(max-width: 960px) 100vw, 50vw" />
          <img src="/assets/img/{hero}-1600.jpg" alt="{s['name']} in {location} — architectural technologist at work" width="1600" height="945" fetchpriority="high" />
        </picture>
      </div>
    </div>
  </div>
</section>

<!-- ===== TL;DR — AEO/GEO optimised quick-facts block ===== -->
<section style="padding-top: 0;">
  <div class="container">
    <div class="tldr">
      <h3>Quick facts · {s['name']} in {location}</h3>
      <dl>
        <div><dt>Fixed fee from</dt><dd>{price_from} + VAT</dd></div>
        <div><dt>Typical turnaround</dt><dd>{s['turnaround']}</dd></div>
        <div><dt>Planning authority</dt><dd>{b['planning_authority']}</dd></div>
        <div><dt>Conservation areas</dt><dd>{b['conservation_areas']} in {location}</dd></div>
        <div><dt>Article 4 Direction</dt><dd>{article_4_short}</dd></div>
        <div><dt>Postcodes covered</dt><dd>{b['postcodes'].split(',')[0].strip()} and others</dd></div>
      </dl>
    </div>
  </div>
</section>

<!-- ===== LOCAL CONTEXT — GEO-optimised factual content ===== -->
<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Planning context</span>
      <h2 style="margin-top: 16px;">{s['name']} in {location} — <em>local planning context</em></h2>
    </div>
    <div style="max-width: 800px;">
      <p style="font-size: 1.1rem; color: var(--ink-soft); margin-bottom: 20px;">{fill_placeholders(s["summary"], b)}</p>
      <p style="color: var(--ink-soft); margin-bottom: 20px;">
        <strong>Housing stock in {location}:</strong> {b['typical_housing']}
      </p>
      <p style="color: var(--ink-soft); margin-bottom: 20px;">
        <strong>Character:</strong> {b['character']}
      </p>
      {"<p style='color: var(--ink-soft); margin-bottom: 20px;'><strong>Article 4:</strong> " + b['article_4_notes'] + "</p>" if b['article_4'] else ""}
      {"<p style='color: var(--ink-soft); margin-bottom: 20px;'><strong>Basement policy:</strong> " + b.get('basement_notes', '') + "</p>" if b['basement_policy'] else ""}

      <div class="local-grid">
        <div class="local-stat"><div class="local-stat-label">Population</div><div class="local-stat-value">{b['population']:,}</div></div>
        <div class="local-stat"><div class="local-stat-label">Conservation areas</div><div class="local-stat-value">{b['conservation_areas']}</div></div>
        <div class="local-stat"><div class="local-stat-label">Planning authority</div><div class="local-stat-value">{b['planning_authority'].replace('London Borough of ', '').replace('Royal Borough of ', '')}</div></div>
        <div class="local-stat"><div class="local-stat-label">Postcodes</div><div class="local-stat-value">{len(b['postcodes'].split(','))} areas</div></div>
      </div>
    </div>
  </div>
</section>

<!-- ===== WHAT'S INCLUDED ===== -->
<section id="included" style="background: var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">What's included</span>
      <h2 style="margin-top: 16px;">Fully <em>end-to-end</em> in {location}.</h2>
    </div>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
      {whats_included_html}
    </div>
  </div>
</section>

<!-- ===== PRICING ===== -->
<section id="pricing">
  <div class="container">
    <div class="section-header" style="text-align: center; margin: 0 auto;">
      <span class="eyebrow">Fixed fee — 30% below London architects</span>
      <h2 style="margin-top: 16px;">{s['name']} pricing in {location}</h2>
    </div>
    <div class="pricing-grid">
      <div class="pricing-card">
        <h3>Essentials</h3>
        <p class="muted">Single planning or regs submission.</p>
        <div class="pricing-price"><span class="from">from</span><span class="amount">{price_from}</span></div>
        <ul class="pricing-features">
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Measured survey</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Drawings &amp; submission</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Unlimited revisions</li>
        </ul>
        <a href="/quote.html?service={service_slug}&amp;location={borough_slug}&amp;tier=essentials" class="btn btn-outline btn-block">Start Essentials →</a>
      </div>
      <div class="pricing-card popular">
        <span class="pricing-popular-tag">Most popular</span>
        <h3>Complete</h3>
        <p style="color: rgba(250,250,247,0.7);">Planning + building regs + structural.</p>
        <div class="pricing-price"><span class="from">from</span><span class="amount">£{int(s['price_from'] * 1.4):,}</span></div>
        <ul class="pricing-features">
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Everything in Essentials</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Building regs drawings</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Structural calculations</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Submitted to {b['planning_authority']}</li>
        </ul>
        <a href="/quote.html?service={service_slug}&amp;location={borough_slug}&amp;tier=complete" class="btn btn-accent btn-block">Start Complete →</a>
      </div>
      <div class="pricing-card">
        <h3>Bespoke</h3>
        <p class="muted">Listed, conservation, complex sites.</p>
        <div class="pricing-price"><span class="amount serif">Custom</span></div>
        <ul class="pricing-features">
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Everything in Complete</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Heritage Statement</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Committee representation</li>
        </ul>
        <a href="/quote.html?service={service_slug}&amp;location={borough_slug}&amp;tier=bespoke" class="btn btn-outline btn-block">Discuss Bespoke →</a>
      </div>
    </div>
  </div>
</section>

<!-- ===== FAQ — AEO CORE ===== -->
<section class="faq">
  <div class="container">
    <div class="faq-grid">
      <div class="faq-aside">
        <span class="eyebrow">{location} FAQs</span>
        <h2 style="margin-top: 16px;">{s['name']} in {location} — <em>your questions answered.</em></h2>
        <p>Direct answers to the questions {location} homeowners ask every week about {service_short}.</p>
        <a href="/quote.html?service={service_slug}&amp;location={borough_slug}" class="btn btn-primary">Start a free quote →</a>
      </div>
      <div class="faq-list">
        {faq_html}
      </div>
    </div>
  </div>
</section>

<!-- ===== NEARBY AREAS — internal linking for SEO ===== -->
<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Nearby boroughs</span>
      <h2 style="margin-top: 16px;">{s['name']} in areas <em>adjacent to {location}</em></h2>
      <p>We cover every London borough with the same fixed-fee approach. If your property sits on a boundary, here are the neighbouring options.</p>
    </div>
    <div class="adjacent-grid">
      {adjacent_html}
    </div>
  </div>
</section>

<!-- ===== OTHER SERVICES IN THIS LOCATION ===== -->
<section style="background: var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Other services in {location}</span>
      <h2 style="margin-top: 16px;">Need more than <em>{service_short}</em>?</h2>
      <p>We cover every architectural technology service in {location} with one chartered team.</p>
    </div>
    <div class="services-grid">
      {related_services_html}
    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="cta-band">
  <div class="container">
    <h2>Start your {location} {service_short} application <span class="accent">this week.</span></h2>
    <p>Free quote in 60 seconds. Fixed fee from {price_from}. MCIAT chartered.</p>
    <a href="/quote.html?service={service_slug}&amp;location={borough_slug}" class="btn btn-primary btn-lg">Get my free quote →</a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="/services/planning-drawings.html">Planning permission drawings London</a></li>
        <li><a href="/services/building-regulations.html">Building regulations drawings London</a></li>
        <li><a href="/services/loft-conversions.html">Loft conversion drawings London</a></li>
        <li><a href="/services/house-extensions.html">House extension plans London</a></li>
        <li><a href="/services/mansard-roof.html">Mansard roof extensions London</a></li>
      </ul></div>
      <div><h5>Loft conversions by borough</h5><ul>
        <li><a href="/areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="/areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="/areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="/areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="/areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
      </ul></div>
      <div><h5>Extension plans by borough</h5><ul>
        <li><a href="/areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
        <li><a href="/areas/greenwich/house-extensions.html">Extension plans Greenwich</a></li>
        <li><a href="/areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
        <li><a href="/areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
        <li><a href="/areas/merton/house-extensions.html">Extension plans Merton</a></li>
      </ul></div>
      <div><h5>Planning drawings by borough</h5><ul>
        <li><a href="/areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
        <li><a href="/areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
        <li><a href="/areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
        <li><a href="/areas/newham/planning-drawings.html">Planning drawings Newham</a></li>
        <li><a href="/areas/bexley/planning-drawings.html">Planning drawings Bexley</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom" style="border-top: 0; padding-top: 0;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; Serving {location} and all 33 London boroughs</span>
      <span><a href="/">Home</a> &middot; <a href="/services.html">All services</a> &middot; <a href="/pricing.html">Pricing</a> &middot; <a href="/areas/">All areas</a> &middot; <a href="/privacy.html">Privacy</a> &middot; <a href="/terms.html">Terms</a></span>
    </div>
  </div>
</footer>

<script>
// Reveal + nav scroll
document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
const nav = document.getElementById('nav');
if (nav) {{
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 12);
  onScroll();
  window.addEventListener('scroll', onScroll, {{ passive: true }});
}}
document.querySelectorAll('.faq-item').forEach(i => i.addEventListener('toggle', () => i.classList.toggle('open', i.open)));
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20{service_slug.replace('-', '%20')}%20in%20{location.replace(' ', '%20')}." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 0 0 .613.613l4.458-1.495A11.952 11.952 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.39-1.586l-.386-.232-2.644.886.886-2.644-.232-.386A9.94 9.94 0 0 1 2 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
  </a>
</div>
<!-- STICKY-CTA -->
<style>
/* ===== Sticky CTA Bar ===== */
.sticky-cta-bar {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 80;
  background: rgba(14, 17, 22, 0.95);
  border-top: 2px solid var(--accent, #C8664A);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  transform: translateY(100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  font-family: 'Manrope', sans-serif;
}}
.sticky-cta-bar.visible {{ transform: translateY(0); }}
.sticky-cta-bar-text {{
  color: rgba(250, 250, 247, 0.9);
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}}
.sticky-cta-bar-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 22px;
  border-radius: var(--r-md, 16px);
  border: none;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.2s, transform 0.2s;
}}
.sticky-cta-bar-btn:hover {{
  background: var(--accent-deep, #9D4A32);
  transform: translateY(-1px);
}}
.sticky-cta-bar-close {{
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(250, 250, 247, 0.5);
  font-size: 1.3rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}}
.sticky-cta-bar-close:hover {{ color: #fff; }}
@media (max-width: 640px) {{
  .sticky-cta-bar {{
    flex-direction: column;
    gap: 10px;
    padding: 14px 48px 14px 16px;
    text-align: center;
  }}
  .sticky-cta-bar-text {{ font-size: 0.88rem; }}
}}
/* ===== Exit-Intent Modal ===== */
.exit-overlay {{
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(14, 17, 22, 0.6);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}}
.exit-overlay.active {{
  opacity: 1;
  pointer-events: auto;
}}
.exit-card {{
  background: var(--surface, #FFFFFF);
  border-radius: var(--r-lg, 24px);
  max-width: 480px;
  width: 92%;
  padding: 40px 36px 32px;
  position: relative;
  transform: scale(0.95);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 24px 60px rgba(14, 17, 22, 0.25), 0 8px 20px rgba(14, 17, 22, 0.12);
}}
.exit-overlay.active .exit-card {{ transform: scale(1); }}
.exit-card-close {{
  position: absolute;
  top: 14px;
  right: 14px;
  background: none;
  border: none;
  color: var(--ink-soft, #4A5260);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}}
.exit-card-close:hover {{ color: var(--ink, #0E1116); }}
.exit-card h3 {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.65rem;
  font-weight: 300;
  font-style: italic;
  font-variation-settings: "opsz" 72, "SOFT" 60;
  letter-spacing: -0.02em;
  color: var(--ink, #0E1116);
  margin: 0 0 10px;
}}
.exit-card p {{
  font-family: 'Manrope', sans-serif;
  font-size: 0.95rem;
  color: var(--ink-soft, #4A5260);
  line-height: 1.6;
  margin: 0 0 22px;
}}
.exit-form {{
  display: flex;
  gap: 8px;
}}
.exit-form input[type="email"] {{
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--line, rgba(14,17,22,0.08));
  border-radius: var(--r-md, 16px);
  font-family: 'Manrope', sans-serif;
  font-size: 0.9rem;
  color: var(--ink, #0E1116);
  background: var(--bg, #FAFAF7);
  outline: none;
  transition: border-color 0.2s;
}}
.exit-form input[type="email"]:focus {{
  border-color: var(--accent, #C8664A);
}}
.exit-form button {{
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 12px 20px;
  border: none;
  border-radius: var(--r-md, 16px);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
}}
.exit-form button:hover {{ background: var(--accent-deep, #9D4A32); }}
.exit-trust {{
  font-family: 'Manrope', sans-serif;
  font-size: 0.78rem;
  color: var(--ink-soft, #4A5260);
  margin-top: 14px;
  text-align: center;
  opacity: 0.7;
}}
.exit-success {{
  text-align: center;
  padding: 12px 0 4px;
}}
.exit-success p {{
  font-size: 1.05rem;
  color: var(--ink, #0E1116);
  font-weight: 600;
}}
@media (max-width: 480px) {{
  .exit-card {{ padding: 32px 24px 24px; }}
  .exit-form {{ flex-direction: column; }}
}}
</style>
<div class="sticky-cta-bar" id="stickyCta" aria-label="Get a free quote">
  <span class="sticky-cta-bar-text">Free quote in 60 seconds &mdash; From &pound;840 fixed fee</span>
  <a href="/quote.html" class="sticky-cta-bar-btn">Get my free quote &rarr;</a>
  <button class="sticky-cta-bar-close" id="stickyCtaClose" aria-label="Dismiss">&times;</button>
</div>
<div class="exit-overlay" id="exitOverlay">
  <div class="exit-card">
    <button class="exit-card-close" id="exitClose" aria-label="Close">&times;</button>
    <div id="exitContent">
      <h3>Before you go&hellip;</h3>
      <p>Get a free, no-obligation quote for your project. Fixed fees from &pound;840. MCIAT chartered.</p>
      <form class="exit-form" id="exitForm">
        <input type="email" name="exit_email" placeholder="Your email address" required autocomplete="email" />
        <button type="submit">Send my quote &rarr;</button>
      </form>
      <div class="exit-trust">98% first-time approval rate &middot; All 33 London boroughs</div>
    </div>
    <div id="exitSuccess" class="exit-success" style="display:none;">
      <p>Thanks! We&rsquo;ll be in touch within 24 hours.</p>
    </div>
  </div>
</div>
<script>
(function() {{
  var bar = document.getElementById('stickyCta');
  var closeBtn = document.getElementById('stickyCtaClose');
  if (bar && closeBtn) {{
    var dismissed = false;
    try {{ dismissed = sessionStorage.getItem('__ad_sticky_dismissed') === '1'; }} catch(e) {{}}
    if (!dismissed) {{
      var onScroll = function() {{
        if (window.scrollY > 400) {{ bar.classList.add('visible'); }}
        else {{ bar.classList.remove('visible'); }}
      }};
      window.addEventListener('scroll', onScroll, {{ passive: true }});
      onScroll();
    }}
    closeBtn.addEventListener('click', function() {{
      bar.classList.remove('visible');
      try {{ sessionStorage.setItem('__ad_sticky_dismissed', '1'); }} catch(e) {{}}
      window.removeEventListener('scroll', onScroll);
    }});
  }}
  var overlay = document.getElementById('exitOverlay');
  var exitCloseBtn = document.getElementById('exitClose');
  var exitForm = document.getElementById('exitForm');
  var exitContent = document.getElementById('exitContent');
  var exitSuccess = document.getElementById('exitSuccess');
  if (overlay && exitCloseBtn) {{
    var exitFired = false;
    try {{ exitFired = sessionStorage.getItem('__ad_exit_fired') === '1'; }} catch(e) {{}}
    function closeModal() {{
      overlay.classList.remove('active');
      try {{ sessionStorage.setItem('__ad_exit_fired', '1'); }} catch(e) {{}}
    }}
    if (!exitFired && window.innerWidth > 768) {{
      document.addEventListener('mouseout', function(e) {{
        if (e.clientY <= 0 && !exitFired) {{
          exitFired = true;
          overlay.classList.add('active');
          try {{ sessionStorage.setItem('__ad_exit_fired', '1'); }} catch(e2) {{}}
        }}
      }});
    }}
    exitCloseBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {{
      if (e.target === overlay) closeModal();
    }});
    if (exitForm) {{
      exitForm.addEventListener('submit', function(e) {{
        e.preventDefault();
        if (exitContent) exitContent.style.display = 'none';
        if (exitSuccess) exitSuccess.style.display = 'block';
        setTimeout(closeModal, 3000);
      }});
    }}
  }}
}})();
</script>
<!-- /STICKY-CTA -->
</body>
</html>
'''
    return html


# Simple service icon for "what's included" cards
SERVICE_ICON = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 4h14l6 6v18H6z"/><path d="M20 4v6h6"/><path d="M10 14h12M10 18h12M10 22h8"/></svg>'


# ============================================================
# BOROUGH HUB PAGE (index of services in that borough)
# ============================================================

def render_borough_hub(borough_slug):
    b = BOROUGHS[borough_slug]
    location = b["name"]
    canonical = f"https://architecturaldrawings.co.uk/areas/{borough_slug}/"

    title = f"Architectural Drawings in {location} | Planning, Loft, Extension — from £556"
    if len(title) > 68:
        title = f"Architectural Services in {location} | Planning &amp; Building Regs"
    meta_desc = (f"Chartered architectural technology in {location}. Planning drawings from £840, "
                 f"loft conversions from £1,225, house extensions from £1,225. MCIAT. "
                 f"Covering {b['planning_authority']}.")[:159]

    # Service cards for this borough
    services_html = "".join(
        f'<a href="{ss}.html" class="service-card"><div class="service-icon">{SERVICE_ICON}</div><h3>{SERVICES[ss]["name"]} in {location}</h3><p>{fill_placeholders(SERVICES[ss]["summary"][:140], b)}...</p><div class="service-card-footer"><span class="service-card-price"><span class="from">from</span>{SERVICES[ss]["price_display"]}</span><span class="service-card-link">View →</span></div></a>'
        for ss in SERVICE_SLUGS
    )

    # Adjacent boroughs
    adjacent_html = "".join(
        f'<a href="../{adj}/" class="adjacent-card"><strong>{BOROUGHS[adj]["name"]}</strong><span>Adjacent borough</span></a>'
        for adj in b["adjacent"] if adj in BOROUGHS
    )

    html = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="Architectural Drawings in {location}" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Architectural Drawings London — {location}",
  "url": "{canonical}",
  "areaServed": {{"@type": "AdministrativeArea", "name": "{location}", "containedInPlace": {{"@type": "City", "name": "London"}}}},
  "provider": {{"@type": "ProfessionalService", "@id": "https://architecturaldrawings.co.uk/#business"}},
  "priceRange": "££"
}}
</script>

<style>
{CSS}
{PSEO_CSS}
@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="/" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav><ul class="nav-links">
      <li><a href="/services.html">Services</a></li>
      <li><a href="/pricing.html">Pricing</a></li>
      <li><a href="/areas/">Areas</a></li>
      <li><a href="/about.html">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="/portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="/quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<section class="hero">
  <div class="container">
    <nav aria-label="Breadcrumb" style="font-size: 0.85rem; color: var(--ink-soft); margin-bottom: 20px;">
      <a href="/" style="color: var(--ink-soft);">Home</a> /
      <a href="/areas/" style="color: var(--ink-soft);">Areas</a> /
      <strong style="color: var(--ink);">{location}</strong>
    </nav>
    <span class="eyebrow">{b['planning_authority']}</span>
    <h1 style="margin: 16px 0 24px; max-width: 920px;">Architectural technology in <span style="color: var(--accent); font-style: italic; font-weight: 300;">{location}</span></h1>
    <p style="color: var(--ink-soft); max-width: 680px; font-size: 1.15rem;">Planning drawings, building regulations, loft conversions, house extensions and mansards — delivered across {location} by MCIAT chartered technologists with deep knowledge of {b['planning_authority']}'s policies.</p>

    <div class="tldr" style="margin-top: 32px;">
      <h3>{location} at a glance</h3>
      <dl>
        <div><dt>Planning authority</dt><dd>{b['planning_authority']}</dd></div>
        <div><dt>Population</dt><dd>{b['population']:,}</dd></div>
        <div><dt>Conservation areas</dt><dd>{b['conservation_areas']}</dd></div>
        <div><dt>Article 4 Direction</dt><dd>{"Yes — HMO and more" if b['article_4'] else "No borough-wide"}</dd></div>
        <div><dt>Postcodes</dt><dd>{b['postcodes']}</dd></div>
        <div><dt>Typical housing</dt><dd>{b['typical_housing'].split(';')[0]}</dd></div>
      </dl>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Services available in {location}</span>
      <h2 style="margin-top: 16px;">Every architectural service in {location} — <em>one chartered team.</em></h2>
    </div>
    <div class="services-grid">
      {services_html}
    </div>
  </div>
</section>

<section style="background: var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">{location} planning context</span>
      <h2 style="margin-top: 16px;">Planning in {location}</h2>
    </div>
    <div style="max-width: 800px;">
      <p style="color: var(--ink-soft); margin-bottom: 20px;">
        <strong>Housing stock:</strong> {b['typical_housing']}
      </p>
      <p style="color: var(--ink-soft); margin-bottom: 20px;">
        <strong>Character:</strong> {b['character']}
      </p>
      <p style="color: var(--ink-soft); margin-bottom: 20px;">
        <strong>Notable conservation areas:</strong> {b['notable_conservation']}
      </p>
      {"<p style='color: var(--ink-soft); margin-bottom: 20px;'><strong>Article 4 Direction:</strong> " + b['article_4_notes'] + "</p>" if b['article_4'] else ""}
      {"<p style='color: var(--ink-soft); margin-bottom: 20px;'><strong>Basement policy:</strong> " + b.get('basement_notes', '') + "</p>" if b['basement_policy'] else ""}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Nearby boroughs</span>
      <h2 style="margin-top: 16px;">Boroughs <em>adjacent to {location}</em></h2>
    </div>
    <div class="adjacent-grid">
      {adjacent_html}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Start your {location} project <span class="accent">this week.</span></h2>
    <p>Free quote in 60 seconds. Fixed fees from £556. MCIAT chartered.</p>
    <a href="/quote.html?location={borough_slug}" class="btn btn-primary btn-lg">Get my free quote →</a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="/services/planning-drawings.html">Planning permission drawings London</a></li>
        <li><a href="/services/building-regulations.html">Building regulations drawings London</a></li>
        <li><a href="/services/loft-conversions.html">Loft conversion drawings London</a></li>
        <li><a href="/services/house-extensions.html">House extension plans London</a></li>
        <li><a href="/services/mansard-roof.html">Mansard roof extensions London</a></li>
      </ul></div>
      <div><h5>Loft conversions by borough</h5><ul>
        <li><a href="/areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="/areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="/areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="/areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="/areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
      </ul></div>
      <div><h5>Extension plans by borough</h5><ul>
        <li><a href="/areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
        <li><a href="/areas/greenwich/house-extensions.html">Extension plans Greenwich</a></li>
        <li><a href="/areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
        <li><a href="/areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
        <li><a href="/areas/merton/house-extensions.html">Extension plans Merton</a></li>
      </ul></div>
      <div><h5>Planning drawings by borough</h5><ul>
        <li><a href="/areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
        <li><a href="/areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
        <li><a href="/areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
        <li><a href="/areas/newham/planning-drawings.html">Planning drawings Newham</a></li>
        <li><a href="/areas/bexley/planning-drawings.html">Planning drawings Bexley</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom" style="border-top: 0; padding-top: 0;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; Covering {location}</span>
      <span><a href="/">Home</a> &middot; <a href="/areas/">All areas</a> &middot; <a href="/privacy.html">Privacy</a> &middot; <a href="/terms.html">Terms</a></span>
    </div>
  </div>
</footer>

<script>
document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
const nav = document.getElementById('nav');
if (nav) {{ const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 12); onScroll(); window.addEventListener('scroll', onScroll, {{ passive: true }}); }}
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20in%20{location.replace(' ', '%20')}." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 0 0 .613.613l4.458-1.495A11.952 11.952 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.39-1.586l-.386-.232-2.644.886.886-2.644-.232-.386A9.94 9.94 0 0 1 2 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
  </a>
</div>
<!-- STICKY-CTA -->
<style>
.sticky-cta-bar {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 80;
  background: rgba(14, 17, 22, 0.95);
  border-top: 2px solid var(--accent, #C8664A);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  transform: translateY(100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  font-family: 'Manrope', sans-serif;
}}
.sticky-cta-bar.visible {{ transform: translateY(0); }}
.sticky-cta-bar-text {{
  color: rgba(250, 250, 247, 0.9);
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}}
.sticky-cta-bar-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 22px;
  border-radius: var(--r-md, 16px);
  border: none;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.2s, transform 0.2s;
}}
.sticky-cta-bar-btn:hover {{
  background: var(--accent-deep, #9D4A32);
  transform: translateY(-1px);
}}
.sticky-cta-bar-close {{
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(250, 250, 247, 0.5);
  font-size: 1.3rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}}
.sticky-cta-bar-close:hover {{ color: #fff; }}
@media (max-width: 640px) {{
  .sticky-cta-bar {{
    flex-direction: column;
    gap: 10px;
    padding: 14px 48px 14px 16px;
    text-align: center;
  }}
  .sticky-cta-bar-text {{ font-size: 0.88rem; }}
}}
.exit-overlay {{
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(14, 17, 22, 0.6);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}}
.exit-overlay.active {{
  opacity: 1;
  pointer-events: auto;
}}
.exit-card {{
  background: var(--surface, #FFFFFF);
  border-radius: var(--r-lg, 24px);
  max-width: 480px;
  width: 92%;
  padding: 40px 36px 32px;
  position: relative;
  transform: scale(0.95);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 24px 60px rgba(14, 17, 22, 0.25), 0 8px 20px rgba(14, 17, 22, 0.12);
}}
.exit-overlay.active .exit-card {{ transform: scale(1); }}
.exit-card-close {{
  position: absolute;
  top: 14px;
  right: 14px;
  background: none;
  border: none;
  color: var(--ink-soft, #4A5260);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}}
.exit-card-close:hover {{ color: var(--ink, #0E1116); }}
.exit-card h3 {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.65rem;
  font-weight: 300;
  font-style: italic;
  font-variation-settings: "opsz" 72, "SOFT" 60;
  letter-spacing: -0.02em;
  color: var(--ink, #0E1116);
  margin: 0 0 10px;
}}
.exit-card p {{
  font-family: 'Manrope', sans-serif;
  font-size: 0.95rem;
  color: var(--ink-soft, #4A5260);
  line-height: 1.6;
  margin: 0 0 22px;
}}
.exit-form {{
  display: flex;
  gap: 8px;
}}
.exit-form input[type="email"] {{
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--line, rgba(14,17,22,0.08));
  border-radius: var(--r-md, 16px);
  font-family: 'Manrope', sans-serif;
  font-size: 0.9rem;
  color: var(--ink, #0E1116);
  background: var(--bg, #FAFAF7);
  outline: none;
  transition: border-color 0.2s;
}}
.exit-form input[type="email"]:focus {{
  border-color: var(--accent, #C8664A);
}}
.exit-form button {{
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 12px 20px;
  border: none;
  border-radius: var(--r-md, 16px);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
}}
.exit-form button:hover {{ background: var(--accent-deep, #9D4A32); }}
.exit-trust {{
  font-family: 'Manrope', sans-serif;
  font-size: 0.78rem;
  color: var(--ink-soft, #4A5260);
  margin-top: 14px;
  text-align: center;
  opacity: 0.7;
}}
.exit-success {{
  text-align: center;
  padding: 12px 0 4px;
}}
.exit-success p {{
  font-size: 1.05rem;
  color: var(--ink, #0E1116);
  font-weight: 600;
}}
@media (max-width: 480px) {{
  .exit-card {{ padding: 32px 24px 24px; }}
  .exit-form {{ flex-direction: column; }}
}}
</style>
<div class="sticky-cta-bar" id="stickyCta" aria-label="Get a free quote">
  <span class="sticky-cta-bar-text">Free quote in 60 seconds &mdash; From &pound;840 fixed fee</span>
  <a href="/quote.html" class="sticky-cta-bar-btn">Get my free quote &rarr;</a>
  <button class="sticky-cta-bar-close" id="stickyCtaClose" aria-label="Dismiss">&times;</button>
</div>
<div class="exit-overlay" id="exitOverlay">
  <div class="exit-card">
    <button class="exit-card-close" id="exitClose" aria-label="Close">&times;</button>
    <div id="exitContent">
      <h3>Before you go&hellip;</h3>
      <p>Get a free, no-obligation quote for your project. Fixed fees from &pound;840. MCIAT chartered.</p>
      <form class="exit-form" id="exitForm">
        <input type="email" name="exit_email" placeholder="Your email address" required autocomplete="email" />
        <button type="submit">Send my quote &rarr;</button>
      </form>
      <div class="exit-trust">98% first-time approval rate &middot; All 33 London boroughs</div>
    </div>
    <div id="exitSuccess" class="exit-success" style="display:none;">
      <p>Thanks! We&rsquo;ll be in touch within 24 hours.</p>
    </div>
  </div>
</div>
<script>
(function() {{
  var bar = document.getElementById('stickyCta');
  var closeBtn = document.getElementById('stickyCtaClose');
  if (bar && closeBtn) {{
    var dismissed = false;
    try {{ dismissed = sessionStorage.getItem('__ad_sticky_dismissed') === '1'; }} catch(e) {{}}
    if (!dismissed) {{
      var onScroll = function() {{
        if (window.scrollY > 400) {{ bar.classList.add('visible'); }}
        else {{ bar.classList.remove('visible'); }}
      }};
      window.addEventListener('scroll', onScroll, {{ passive: true }});
      onScroll();
    }}
    closeBtn.addEventListener('click', function() {{
      bar.classList.remove('visible');
      try {{ sessionStorage.setItem('__ad_sticky_dismissed', '1'); }} catch(e) {{}}
      window.removeEventListener('scroll', onScroll);
    }});
  }}
  var overlay = document.getElementById('exitOverlay');
  var exitCloseBtn = document.getElementById('exitClose');
  var exitForm = document.getElementById('exitForm');
  var exitContent = document.getElementById('exitContent');
  var exitSuccess = document.getElementById('exitSuccess');
  if (overlay && exitCloseBtn) {{
    var exitFired = false;
    try {{ exitFired = sessionStorage.getItem('__ad_exit_fired') === '1'; }} catch(e) {{}}
    function closeModal() {{
      overlay.classList.remove('active');
      try {{ sessionStorage.setItem('__ad_exit_fired', '1'); }} catch(e) {{}}
    }}
    if (!exitFired && window.innerWidth > 768) {{
      document.addEventListener('mouseout', function(e) {{
        if (e.clientY <= 0 && !exitFired) {{
          exitFired = true;
          overlay.classList.add('active');
          try {{ sessionStorage.setItem('__ad_exit_fired', '1'); }} catch(e2) {{}}
        }}
      }});
    }}
    exitCloseBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {{
      if (e.target === overlay) closeModal();
    }});
    if (exitForm) {{
      exitForm.addEventListener('submit', function(e) {{
        e.preventDefault();
        if (exitContent) exitContent.style.display = 'none';
        if (exitSuccess) exitSuccess.style.display = 'block';
        setTimeout(closeModal, 3000);
      }});
    }}
  }}
}})();
</script>
<!-- /STICKY-CTA -->
</body>
</html>
'''
    return html


# ============================================================
# MASTER AREAS INDEX
# ============================================================

def render_master_index():
    canonical = "https://architecturaldrawings.co.uk/areas/"
    boroughs_html = "".join(
        f'<a href="{slug}/" class="adjacent-card"><strong>{BOROUGHS[slug]["name"]}</strong><span>{BOROUGHS[slug]["planning_authority"].replace("London Borough of ", "").replace("Royal Borough of ", "")} · {BOROUGHS[slug]["conservation_areas"]} conservation areas</span></a>'
        for slug in sorted(BOROUGH_SLUGS, key=lambda s: BOROUGHS[s]["name"])
    )

    html = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>London Areas We Cover | Architectural Drawings London</title>
<meta name="description" content="We provide architectural technology services — planning drawings, building regs, loft conversions, extensions — across all 33 London boroughs. Find your area." />
<link rel="canonical" href="{canonical}" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

<style>
{CSS}
{PSEO_CSS}
@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="/" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav><ul class="nav-links">
      <li><a href="/services.html">Services</a></li>
      <li><a href="/pricing.html">Pricing</a></li>
      <li><a href="/areas/">Areas</a></li>
      <li><a href="/about.html">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="/portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="/quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<section class="hero">
  <div class="container">
    <span class="eyebrow">All 33 London boroughs</span>
    <h1 style="margin: 16px 0 24px; max-width: 920px;">Architectural drawings in every <span style="color: var(--accent); font-style: italic; font-weight: 300;">London borough.</span></h1>
    <p style="color: var(--ink-soft); max-width: 680px; font-size: 1.15rem;">We cover all 33 London boroughs from Barking and Dagenham to Westminster — with chartered architectural technologists who know each borough's Article 4 Directions, conservation areas, and local planning quirks.</p>
  </div>
</section>

<section style="padding-top: 20px;">
  <div class="container">
    <div class="section-header">
      <h2>Pick your borough</h2>
      <p>Each borough page has location-specific planning context, all services and local pricing.</p>
    </div>
    <div class="adjacent-grid" style="grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));">
      {boroughs_html}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Don't see your borough above? <span class="accent">We cover it anyway.</span></h2>
    <p>If it's within the M25 we almost certainly work there. Free quote — no obligation.</p>
    <a href="/quote.html" class="btn btn-primary btn-lg">Get my free quote →</a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="/services/planning-drawings.html">Planning permission drawings London</a></li>
        <li><a href="/services/building-regulations.html">Building regulations drawings London</a></li>
        <li><a href="/services/loft-conversions.html">Loft conversion drawings London</a></li>
        <li><a href="/services/house-extensions.html">House extension plans London</a></li>
        <li><a href="/services/mansard-roof.html">Mansard roof extensions London</a></li>
      </ul></div>
      <div><h5>Loft conversions by borough</h5><ul>
        <li><a href="/areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="/areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="/areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="/areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="/areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
      </ul></div>
      <div><h5>Extension plans by borough</h5><ul>
        <li><a href="/areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
        <li><a href="/areas/greenwich/house-extensions.html">Extension plans Greenwich</a></li>
        <li><a href="/areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
        <li><a href="/areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
        <li><a href="/areas/merton/house-extensions.html">Extension plans Merton</a></li>
      </ul></div>
      <div><h5>Planning drawings by borough</h5><ul>
        <li><a href="/areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
        <li><a href="/areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
        <li><a href="/areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
        <li><a href="/areas/newham/planning-drawings.html">Planning drawings Newham</a></li>
        <li><a href="/areas/bexley/planning-drawings.html">Planning drawings Bexley</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom" style="border-top: 0; padding-top: 0;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; 33 London boroughs</span>
      <span><a href="/">Home</a> &middot; <a href="/services.html">Services</a> &middot; <a href="/privacy.html">Privacy</a> &middot; <a href="/terms.html">Terms</a></span>
    </div>
  </div>
</footer>
<script>
document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20in%20London." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 0 0 .613.613l4.458-1.495A11.952 11.952 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.39-1.586l-.386-.232-2.644.886.886-2.644-.232-.386A9.94 9.94 0 0 1 2 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
  </a>
</div>
<!-- STICKY-CTA -->
<style>
.sticky-cta-bar {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 80;
  background: rgba(14, 17, 22, 0.95);
  border-top: 2px solid var(--accent, #C8664A);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  transform: translateY(100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  font-family: 'Manrope', sans-serif;
}}
.sticky-cta-bar.visible {{ transform: translateY(0); }}
.sticky-cta-bar-text {{
  color: rgba(250, 250, 247, 0.9);
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}}
.sticky-cta-bar-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 22px;
  border-radius: var(--r-md, 16px);
  border: none;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.2s, transform 0.2s;
}}
.sticky-cta-bar-btn:hover {{
  background: var(--accent-deep, #9D4A32);
  transform: translateY(-1px);
}}
.sticky-cta-bar-close {{
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(250, 250, 247, 0.5);
  font-size: 1.3rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}}
.sticky-cta-bar-close:hover {{ color: #fff; }}
@media (max-width: 640px) {{
  .sticky-cta-bar {{
    flex-direction: column;
    gap: 10px;
    padding: 14px 48px 14px 16px;
    text-align: center;
  }}
  .sticky-cta-bar-text {{ font-size: 0.88rem; }}
}}
.exit-overlay {{
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(14, 17, 22, 0.6);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}}
.exit-overlay.active {{
  opacity: 1;
  pointer-events: auto;
}}
.exit-card {{
  background: var(--surface, #FFFFFF);
  border-radius: var(--r-lg, 24px);
  max-width: 480px;
  width: 92%;
  padding: 40px 36px 32px;
  position: relative;
  transform: scale(0.95);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 24px 60px rgba(14, 17, 22, 0.25), 0 8px 20px rgba(14, 17, 22, 0.12);
}}
.exit-overlay.active .exit-card {{ transform: scale(1); }}
.exit-card-close {{
  position: absolute;
  top: 14px;
  right: 14px;
  background: none;
  border: none;
  color: var(--ink-soft, #4A5260);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}}
.exit-card-close:hover {{ color: var(--ink, #0E1116); }}
.exit-card h3 {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.65rem;
  font-weight: 300;
  font-style: italic;
  font-variation-settings: "opsz" 72, "SOFT" 60;
  letter-spacing: -0.02em;
  color: var(--ink, #0E1116);
  margin: 0 0 10px;
}}
.exit-card p {{
  font-family: 'Manrope', sans-serif;
  font-size: 0.95rem;
  color: var(--ink-soft, #4A5260);
  line-height: 1.6;
  margin: 0 0 22px;
}}
.exit-form {{
  display: flex;
  gap: 8px;
}}
.exit-form input[type="email"] {{
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--line, rgba(14,17,22,0.08));
  border-radius: var(--r-md, 16px);
  font-family: 'Manrope', sans-serif;
  font-size: 0.9rem;
  color: var(--ink, #0E1116);
  background: var(--bg, #FAFAF7);
  outline: none;
  transition: border-color 0.2s;
}}
.exit-form input[type="email"]:focus {{
  border-color: var(--accent, #C8664A);
}}
.exit-form button {{
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 12px 20px;
  border: none;
  border-radius: var(--r-md, 16px);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
}}
.exit-form button:hover {{ background: var(--accent-deep, #9D4A32); }}
.exit-trust {{
  font-family: 'Manrope', sans-serif;
  font-size: 0.78rem;
  color: var(--ink-soft, #4A5260);
  margin-top: 14px;
  text-align: center;
  opacity: 0.7;
}}
.exit-success {{
  text-align: center;
  padding: 12px 0 4px;
}}
.exit-success p {{
  font-size: 1.05rem;
  color: var(--ink, #0E1116);
  font-weight: 600;
}}
@media (max-width: 480px) {{
  .exit-card {{ padding: 32px 24px 24px; }}
  .exit-form {{ flex-direction: column; }}
}}
</style>
<div class="sticky-cta-bar" id="stickyCta" aria-label="Get a free quote">
  <span class="sticky-cta-bar-text">Free quote in 60 seconds &mdash; From &pound;840 fixed fee</span>
  <a href="/quote.html" class="sticky-cta-bar-btn">Get my free quote &rarr;</a>
  <button class="sticky-cta-bar-close" id="stickyCtaClose" aria-label="Dismiss">&times;</button>
</div>
<div class="exit-overlay" id="exitOverlay">
  <div class="exit-card">
    <button class="exit-card-close" id="exitClose" aria-label="Close">&times;</button>
    <div id="exitContent">
      <h3>Before you go&hellip;</h3>
      <p>Get a free, no-obligation quote for your project. Fixed fees from &pound;840. MCIAT chartered.</p>
      <form class="exit-form" id="exitForm">
        <input type="email" name="exit_email" placeholder="Your email address" required autocomplete="email" />
        <button type="submit">Send my quote &rarr;</button>
      </form>
      <div class="exit-trust">98% first-time approval rate &middot; All 33 London boroughs</div>
    </div>
    <div id="exitSuccess" class="exit-success" style="display:none;">
      <p>Thanks! We&rsquo;ll be in touch within 24 hours.</p>
    </div>
  </div>
</div>
<script>
(function() {{
  var bar = document.getElementById('stickyCta');
  var closeBtn = document.getElementById('stickyCtaClose');
  if (bar && closeBtn) {{
    var dismissed = false;
    try {{ dismissed = sessionStorage.getItem('__ad_sticky_dismissed') === '1'; }} catch(e) {{}}
    if (!dismissed) {{
      var onScroll = function() {{
        if (window.scrollY > 400) {{ bar.classList.add('visible'); }}
        else {{ bar.classList.remove('visible'); }}
      }};
      window.addEventListener('scroll', onScroll, {{ passive: true }});
      onScroll();
    }}
    closeBtn.addEventListener('click', function() {{
      bar.classList.remove('visible');
      try {{ sessionStorage.setItem('__ad_sticky_dismissed', '1'); }} catch(e) {{}}
      window.removeEventListener('scroll', onScroll);
    }});
  }}
  var overlay = document.getElementById('exitOverlay');
  var exitCloseBtn = document.getElementById('exitClose');
  var exitForm = document.getElementById('exitForm');
  var exitContent = document.getElementById('exitContent');
  var exitSuccess = document.getElementById('exitSuccess');
  if (overlay && exitCloseBtn) {{
    var exitFired = false;
    try {{ exitFired = sessionStorage.getItem('__ad_exit_fired') === '1'; }} catch(e) {{}}
    function closeModal() {{
      overlay.classList.remove('active');
      try {{ sessionStorage.setItem('__ad_exit_fired', '1'); }} catch(e) {{}}
    }}
    if (!exitFired && window.innerWidth > 768) {{
      document.addEventListener('mouseout', function(e) {{
        if (e.clientY <= 0 && !exitFired) {{
          exitFired = true;
          overlay.classList.add('active');
          try {{ sessionStorage.setItem('__ad_exit_fired', '1'); }} catch(e2) {{}}
        }}
      }});
    }}
    exitCloseBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {{
      if (e.target === overlay) closeModal();
    }});
    if (exitForm) {{
      exitForm.addEventListener('submit', function(e) {{
        e.preventDefault();
        if (exitContent) exitContent.style.display = 'none';
        if (exitSuccess) exitSuccess.style.display = 'block';
        setTimeout(closeModal, 3000);
      }});
    }}
  }}
}})();
</script>
<!-- /STICKY-CTA -->
</body>
</html>
'''
    return html


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    count = 0

    # Master index
    (AREAS_DIR / "index.html").write_text(render_master_index(), encoding="utf-8")
    count += 1
    print("[OK] /areas/index.html")

    # Each borough
    for slug in BOROUGH_SLUGS:
        bdir = AREAS_DIR / slug
        bdir.mkdir(exist_ok=True)

        # Borough hub
        (bdir / "index.html").write_text(render_borough_hub(slug), encoding="utf-8")
        count += 1

        # Each service in this borough
        for service_slug in SERVICE_SLUGS:
            (bdir / f"{service_slug}.html").write_text(render_service_location(slug, service_slug), encoding="utf-8")
            count += 1

        print(f"[OK] /areas/{slug}/ + {len(SERVICE_SLUGS)} service pages")

    print(f"\n[OK] Generated {count} pSEO pages total")
    print(f"  Master index: 1")
    print(f"  Borough hubs: {len(BOROUGH_SLUGS)}")
    print(f"  Service × borough: {len(BOROUGH_SLUGS) * len(SERVICE_SLUGS)}")
