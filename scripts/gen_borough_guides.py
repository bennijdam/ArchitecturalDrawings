#!/usr/bin/env python3
"""
Generate 33 borough-specific planning guide blog posts.

Each page targets "Planning Permission in {Borough}" with 1500+ words
of borough-specific content drawn from pseo_boroughs.py data.

Usage:
    cd architectural-drawings
    python scripts/gen_borough_guides.py
"""

import sys
import os
from pathlib import Path

# Import borough data from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pseo_boroughs import BOROUGHS

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSS_PATH = PROJECT_ROOT / "assets" / "css" / "style.css"
BLOG_DIR = PROJECT_ROOT / "blog"

# ---------------------------------------------------------------------------
# Read external CSS for inlining
# ---------------------------------------------------------------------------
css_source = CSS_PATH.read_text(encoding="utf-8")

# Strip the @import for Google Fonts (loaded via <link> tags instead)
css_inline = css_source.replace(
    "@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap');",
    "/* Fonts loaded via non-blocking link tags in the document head */"
)

# Escape braces for f-string usage
css_escaped = css_inline.replace("{", "{{").replace("}", "}}")


# ---------------------------------------------------------------------------
# Helper: popular projects based on housing stock keywords
# ---------------------------------------------------------------------------
def popular_projects(b):
    """Return 3-5 project paragraphs based on housing stock."""
    slug = b.get("_slug", "")
    housing = b["typical_housing"].lower()
    name = b["name"]
    sections = []

    if "terrace" in housing or "terraced" in housing:
        sections.append(
            f"<h3>Loft conversions</h3>"
            f"<p>{name} has extensive streets of terraced housing, making loft conversions one of the "
            f"most popular home improvement projects in the borough. A rear dormer loft conversion on a "
            f"typical Victorian or Edwardian mid-terrace can add 20-30 square metres of living space "
            f"and significant value to the property. In many cases, rear dormers fall under Permitted "
            f"Development rights, though properties in conservation areas or subject to Article 4 "
            f"Directions will need full planning permission. We prepare loft conversion drawings for "
            f"properties across {name}, starting from &pound;1,225 for our dedicated loft conversion package.</p>"
        )
        sections.append(
            f"<h3>Side-return and rear extensions</h3>"
            f"<p>The classic Victorian and Edwardian terrace layout in {name} leaves a side return "
            f"passage that is prime territory for a kitchen extension. A single-storey rear or side-return "
            f"extension can often be built under Permitted Development, extending up to 6 metres from "
            f"the rear wall (or up to 8 metres for detached houses under the Prior Approval process). "
            f"We prepare extension plans for properties across all {name} postcodes ({b['postcodes']}), "
            f"with our Essentials package starting from &pound;840.</p>"
        )

    if "semi-detach" in housing or "detach" in housing:
        sections.append(
            f"<h3>Two-storey extensions</h3>"
            f"<p>The semi-detached and detached housing stock in {name} is well suited to two-storey "
            f"rear extensions, which almost always require planning permission. A two-storey extension "
            f"can add a larger kitchen-diner at ground floor and an additional bedroom and bathroom above. "
            f"{b['planning_authority']} generally supports two-storey extensions that are subordinate to "
            f"the original dwelling, set in from the boundary, and do not result in unacceptable loss of "
            f"light or privacy to neighbours. Our Complete package from &pound;1,750 covers full planning "
            f"and building regulations drawings.</p>"
        )

    if "mansion block" in housing or "flat" in housing.lower() or "estate" in housing:
        sections.append(
            f"<h3>Flat conversions and internal alterations</h3>"
            f"<p>With mansion blocks and converted flats forming part of {name}'s housing stock, internal "
            f"layout changes and flat conversions are common projects. While internal alterations rarely "
            f"need planning permission, converting a house to flats (C3 to C4 HMO) or vice versa may "
            f"require planning approval"
            + (f", particularly given {name}'s Article 4 Direction covering HMO conversions" if b["article_4"] else "")
            + f". We can prepare the necessary floor plans, elevations, and supporting documents for "
            f"flat conversion applications in {name}.</p>"
        )

    if b.get("basement_policy"):
        sections.append(
            f"<h3>Basement extensions</h3>"
            f"<p>Basement extensions in {name} are subject to specific planning policies. "
            f"{b.get('basement_notes', '')} Despite these restrictions, basement conversions remain "
            f"popular for adding living space in high-value {name} properties where lateral or upward "
            f"extension is limited. We prepare basement extension drawings that comply with "
            f"{b['planning_authority']}'s policies, including structural methodology statements.</p>"
        )

    if "mansard" in (b.get("character", "") + " " + housing).lower():
        sections.append(
            f"<h3>Mansard roof extensions</h3>"
            f"<p>{name} has established precedents for mansard roof extensions, particularly on "
            f"Victorian and Edwardian terraces. A mansard conversion replaces the existing roof slope "
            f"with a near-vertical front and a shallow-sloped top, creating a full additional storey. "
            f"Mansard extensions always require planning permission. We prepare mansard drawings for "
            f"properties across {name}, from &pound;1,575.</p>"
        )

    # Fallback if nothing matched
    if not sections:
        sections.append(
            f"<h3>Loft conversions and extensions</h3>"
            f"<p>Loft conversions and house extensions are the most common residential planning "
            f"projects in {name}. Whether you are extending a 1930s semi-detached, converting the "
            f"loft of a Victorian terrace, or adding a rear extension, we prepare the planning and "
            f"building regulations drawings needed for {b['planning_authority']}. Our Essentials "
            f"package starts from &pound;840 and our Complete package from &pound;1,750.</p>"
        )

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Helper: FAQ schema JSON
# ---------------------------------------------------------------------------
def faq_schema(faqs):
    """Build FAQPage JSON-LD from list of (question, answer) tuples."""
    items = []
    for q, a in faqs:
        # Escape for JSON
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"')
        items.append(
            f'    {{"@type": "Question", "name": "{q_esc}", '
            f'"acceptedAnswer": {{"@type": "Answer", "text": "{a_esc}"}}}}'
        )
    return ",\n".join(items)


# ---------------------------------------------------------------------------
# Helper: adjacent borough links
# ---------------------------------------------------------------------------
def adjacent_links(b):
    """Generate HTML links for adjacent boroughs."""
    links = []
    for adj_slug in b.get("adjacent", []):
        if adj_slug in BOROUGHS:
            adj_name = BOROUGHS[adj_slug]["name"]
            links.append(
                f'<a href="planning-{adj_slug}.html" '
                f'style="padding:8px 14px;border:1px solid var(--line-strong);border-radius:var(--r-full);'
                f'font-size:0.84rem;font-weight:500;text-decoration:none;transition:all 0.2s var(--ease);">'
                f'{adj_name}</a>'
            )
    return "\n".join(links)


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
def generate_page(slug, b):
    """Generate complete HTML for one borough planning guide."""
    name = b["name"]
    council = b["council"]
    planning_auth = b["planning_authority"]
    postcodes = b["postcodes"]
    conservation_count = b["conservation_areas"]
    notable = b["notable_conservation"]
    housing = b["typical_housing"]
    character = b["character"]
    article_4 = b["article_4"]
    article_4_notes = b.get("article_4_notes", "")
    population = b.get("population", 0)
    basement = b.get("basement_policy", False)
    basement_notes = b.get("basement_notes", "")

    # Title and meta
    title = f"Planning Permission in {name} 2026 | AD"
    if len(title) > 60:
        title = f"Planning Permission {name} 2026 | AD"

    meta_desc = (
        f"Complete guide to planning permission in {name}. "
        f"{conservation_count} conservation areas, Article 4 {'applies' if article_4 else 'none'}, "
        f"council fees, timelines, and how we help."
    )
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."

    canonical = f"https://www.architecturaldrawings.uk/blog/planning-{slug}.html"

    # Build FAQs
    faqs = [
        (
            f"Do I need planning permission in {name}?",
            f"Many home improvements in {name} fall under Permitted Development (PD) rights and do not need planning permission. This includes single-storey rear extensions up to 6 metres, most rear dormer loft conversions, and internal alterations. However, if your property is in one of {name}'s {conservation_count} conservation areas{' or affected by an Article 4 Direction' if article_4 else ''}, PD rights may be restricted and full planning permission may be required. We recommend checking with {planning_auth} or applying for a Lawful Development Certificate."
        ),
        (
            f"Does {name} have Article 4 Directions?",
            f"{'Yes. ' + article_4_notes if article_4 else f'No. {name} does not currently have any borough-wide Article 4 Directions that remove Permitted Development rights for residential householder developments. However, individual properties may still have conditions or restrictions, and conservation area rules apply separately.'}"
        ),
        (
            f"How many conservation areas are in {name}?",
            f"{name} has {conservation_count} designated conservation areas, including {notable}. In conservation areas, Permitted Development rights are more restricted. For example, you cannot add cladding, build side extensions, or install satellite dishes without planning permission. Rear extensions and loft conversions may also be restricted. Always check whether your property falls within a conservation area before starting work."
        ),
        (
            f"How much does a {council} planning application cost?",
            f"A householder planning application to {council} costs {chr(163)}258 (2026 rate). On top of the council fee, you need professional architectural drawings. At Architectural Drawings London, our Essentials package starts from {chr(163)}840 and our Complete package from {chr(163)}1,750, making a typical total cost between {chr(163)}1,098 and {chr(163)}2,008. A Lawful Development Certificate (for Permitted Development confirmation) costs {chr(163)}129."
        ),
        (
            f"How long does {council} take to decide a planning application?",
            f"The statutory target for a householder planning application is 8 weeks. In practice, {planning_auth} may take longer during busy periods. Pre-application advice typically takes 4-6 weeks. From initial instruction to final decision, expect 12-16 weeks for a straightforward householder application in {name}. Major applications have a 13-week determination period."
        ),
    ]

    # Article 4 section content
    if article_4:
        article_4_section = (
            f"<h2>Article 4 Directions in {name}</h2>\n"
            f"<p>{name} has Article 4 Directions in place that remove certain Permitted Development rights. "
            f"{article_4_notes}</p>\n"
            f"<p>Article 4 Directions are used by councils to protect the character of an area by requiring "
            f"planning permission for changes that would otherwise be permitted. If your property is affected "
            f"by an Article 4 Direction in {name}, you will need to submit a full planning application even for "
            f"works that would normally fall under Permitted Development. The council fee for a householder "
            f"application is &pound;258, and we prepare the necessary drawings and supporting documents.</p>\n"
            f"<p>It is important to note that Article 4 Directions in {name} are separate from conservation area "
            f"restrictions. A property can be affected by both, and in practice many Article 4 areas overlap "
            f"with conservation areas. We check the specific restrictions affecting your property as part of "
            f"our initial assessment.</p>"
        )
    else:
        article_4_section = (
            f"<h2>Article 4 Directions in {name}</h2>\n"
            f"<p>{name} does not currently have any borough-wide Article 4 Directions that restrict "
            f"Permitted Development rights for standard householder developments such as loft conversions, "
            f"rear extensions, or outbuildings.</p>\n"
            f"<p>This means that most common home improvements in {name} can proceed under Permitted "
            f"Development without needing to apply for planning permission, provided they meet the national "
            f"criteria for size, height, and position. We recommend applying for a Lawful Development "
            f"Certificate (&pound;129) to formally confirm that your project qualifies as Permitted Development. "
            f"This provides legal certainty and is valuable when selling the property.</p>\n"
            f"<p>Even without Article 4 Directions, properties in {name}'s {conservation_count} conservation areas "
            f"have additional restrictions on permitted development. We check the specific restrictions affecting "
            f"your property as part of our initial assessment.</p>"
        )

    # Conservation section content
    notable_list = notable.split(", ")
    conservation_li = "\n".join(f"<li>{area}</li>" for area in notable_list)
    conservation_section = (
        f"<h2>Conservation areas in {name}</h2>\n"
        f"<p>{name} has <strong>{conservation_count} designated conservation areas</strong>. Notable conservation "
        f"areas include:</p>\n"
        f"<ul>\n{conservation_li}\n</ul>\n"
        f"<p>In conservation areas, Permitted Development rights are more restricted than in non-designated areas. "
        f"Key restrictions include:</p>\n"
        f"<ul>\n"
        f"<li>No cladding, stone, artificial stone, pebble dash, render, timber, plastic, or tile to any external wall without planning permission</li>\n"
        f"<li>No side extensions under Permitted Development</li>\n"
        f"<li>Rear extensions are limited and may require planning permission</li>\n"
        f"<li>Dormer loft conversions facing the highway require planning permission</li>\n"
        f"<li>Satellite dishes on front elevations or chimneys are not permitted</li>\n"
        f"<li>Demolition of gates, walls, fences, or other boundary treatment requires planning permission</li>\n"
        f"</ul>\n"
        f"<p>If your property is in a {name} conservation area, we can advise on what is achievable and prepare "
        f"a planning application that addresses the conservation officer's requirements. Our 98% first-time "
        f"approval rate includes a strong record in conservation area applications.</p>"
    )

    # Our experience section
    postcode_list = postcodes.split(", ")
    adj_html = adjacent_links(b)
    experience_section = (
        f"<h2>Our experience in {name}</h2>\n"
        f"<p>We cover all {name} postcodes: <strong>{postcodes}</strong>. Whether your property is "
        f"in a conservation area, affected by an Article 4 Direction, or in an unrestricted residential street, "
        f"we have experience with {planning_auth} and understand the borough's planning policies.</p>\n"
        f"<p>Our MCIAT chartered architectural technologists prepare planning drawings and building regulations "
        f"drawings for residential projects across {name}. We handle the full process from initial measured survey "
        f"through to planning submission, and we liaise with {planning_auth} on your behalf.</p>\n"
        f"<p>We also work in {name}'s neighbouring boroughs:</p>\n"
        f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 32px;">\n{adj_html}\n</div>'
    )

    # Build full HTML
    faq_json = faq_schema(faqs)

    # FAQ HTML
    faq_html_items = []
    for q, a in faqs:
        faq_html_items.append(
            f'      <details class="faq-item">\n'
            f'        <summary>\n'
            f'          {q}\n'
            f'          <span class="faq-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v10M3 8h10"/></svg></span>\n'
            f'        </summary>\n'
            f'        <div class="faq-answer">\n'
            f'          <p>{a}</p>\n'
            f'        </div>\n'
            f'      </details>'
        )
    faq_html = "\n\n".join(faq_html_items)

    # TL;DR items
    tldr_svg = '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>'

    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{meta_desc}" />
<link rel="author" href="/team/" />
<link rel="canonical" href="{canonical}" />
<!-- Open Graph -->
<meta property="og:type" content="article" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="Planning Permission in {name}: 2026 Guide" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:locale" content="en_GB" />
<meta property="article:published_time" content="2026-04-16" />
<meta property="article:modified_time" content="2026-04-16" />
<meta property="article:author" content="Architectural Drawings London" />

<!-- Article schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Planning Permission in {name}: 2026 Guide",
  "description": "{meta_desc}",
  "datePublished": "2026-04-16",
  "dateModified": "2026-04-16",
  "author": {{
    "@type": "Organization",
    "name": "Architectural Drawings London",
    "url": "https://www.architecturaldrawings.uk"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Architectural Drawings London",
    "url": "https://www.architecturaldrawings.uk"
  }},
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{canonical}"
  }}
}}
</script>

<!-- BreadcrumbList schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.architecturaldrawings.uk/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.architecturaldrawings.uk/blog/" }},
    {{ "@type": "ListItem", "position": 3, "name": "Planning Permission in {name}" }}
  ]
}}
</script>

<!-- FAQPage schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_json}
  ]
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>
<style>
{css_escaped}

/* ============== Article ============== */
.article-body {{
  max-width: 760px;
  margin: 0 auto;
}}
.article-body h2 {{
  margin: 56px 0 20px;
  font-size: clamp(1.8rem, 3.5vw, 2.6rem);
}}
.article-body h3 {{
  margin: 40px 0 16px;
  font-size: clamp(1.3rem, 2.2vw, 1.7rem);
}}
.article-body h4 {{
  margin: 32px 0 12px;
}}
.article-body p {{
  margin-bottom: 18px;
  color: var(--ink);
  font-size: 1.05rem;
  line-height: 1.7;
}}
.article-body ul, .article-body ol {{
  margin: 0 0 24px 24px;
  color: var(--ink);
  font-size: 1.05rem;
  line-height: 1.7;
}}
.article-body li {{
  margin-bottom: 8px;
}}
.article-body a {{
  color: var(--accent-deep);
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.2s var(--ease);
}}
.article-body a:hover {{
  color: var(--accent);
}}
.article-body strong {{
  font-weight: 600;
}}
.article-body blockquote {{
  border-left: 3px solid var(--accent);
  padding: 16px 24px;
  margin: 28px 0;
  background: var(--accent-soft);
  border-radius: 0 var(--r-md) var(--r-md) 0;
  font-size: 1.05rem;
  color: var(--ink);
}}

/* Breadcrumbs */
.breadcrumbs {{
  font-size: 0.84rem;
  color: var(--ink-soft);
  margin-bottom: 32px;
}}
.breadcrumbs a {{
  color: var(--ink-soft);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s var(--ease);
}}
.breadcrumbs a:hover {{ color: var(--accent-deep); }}
.breadcrumbs span {{ margin: 0 6px; opacity: 0.5; }}

/* Author byline */
.author-byline {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 40px;
}}
.author-avatar {{
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--accent-soft);
  color: var(--accent-deep);
  font-family: var(--font-display);
  font-style: italic;
  font-size: 1.3rem;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}}
.author-info {{
  font-size: 0.92rem;
  color: var(--ink-soft);
  line-height: 1.5;
}}
.author-info strong {{
  color: var(--ink);
  display: block;
}}

/* TL;DR box */
.tldr-box {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 28px 32px;
  margin: 0 0 48px;
}}
.tldr-box h4 {{
  font-family: var(--font-body);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-deep);
  margin: 0 0 16px;
}}
.tldr-box ul {{
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}}
.tldr-box li {{
  font-size: 0.95rem;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  line-height: 1.5;
}}
.tldr-box li svg {{
  width: 18px;
  height: 18px;
  color: var(--success);
  flex-shrink: 0;
  margin-top: 2px;
}}

/* Price box */
.price-box {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 32px;
  margin: 28px 0;
}}
.price-box h4 {{
  margin: 0 0 20px;
}}
.price-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--line);
  font-size: 0.98rem;
}}
.price-row:last-child {{ border-bottom: 0; }}
.price-row .label {{ color: var(--ink-soft); }}
.price-row .amount {{
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-variation-settings: "opsz" 36;
  color: var(--ink);
}}

/* FAQ section in article */
.faq-list {{
  display: flex;
  flex-direction: column;
  gap: 0;
}}
.faq-item {{
  border-top: 1px solid var(--line-strong);
}}
.faq-item:last-child {{ border-bottom: 1px solid var(--line-strong); }}
.faq-item summary {{
  width: 100%;
  padding: 24px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-variation-settings: "opsz" 60;
  color: var(--ink);
  gap: 20px;
  letter-spacing: -0.01em;
  line-height: 1.3;
  cursor: pointer;
  list-style: none;
}}
.faq-item summary::-webkit-details-marker {{ display: none; }}
.faq-item summary:hover {{ color: var(--accent-deep); }}
.faq-item .faq-icon {{
  width: 28px; height: 28px;
  border-radius: 50%;
  border: 1px solid var(--line-strong);
  display: grid; place-items: center;
  flex-shrink: 0;
  transition: transform 0.3s var(--ease-spring), background 0.3s var(--ease);
  color: var(--ink-soft);
}}
.faq-item[open] .faq-icon {{
  transform: rotate(45deg);
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.faq-item .faq-answer {{
  padding: 0 0 24px;
  color: var(--ink-soft);
  font-size: 0.98rem;
  line-height: 1.6;
}}

/* Footer dark theme */
.footer {{ background: var(--ink); color: rgba(250,250,247,0.6); }}
.footer .logo {{ color: var(--bg); }}
.footer .logo-mark {{ background: var(--bg); color: var(--ink); }}
.footer-col p {{ color: rgba(250,250,247,0.5); }}
.footer-col h5 {{ color: rgba(250,250,247,0.5); }}
.footer-col a {{ color: rgba(250,250,247,0.6); }}
.footer-col a:hover {{ color: var(--accent); }}
.footer-bottom {{ border-top-color: rgba(255,255,255,0.1); color: rgba(250,250,247,0.5); }}

/* ===== Fail-safe reveal (works even if JS never runs) ===== */
@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="../" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav><ul class="nav-links">
      <li><a href="../services.html">Services</a></li>
      <li><a href="../pricing.html">Pricing</a></li>
      <li><a href="../index.html#process">Process</a></li>
      <li><a href="../about.html">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="../portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="../quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<section class="hero" style="padding-bottom: clamp(20px, 4vw, 40px);">
  <div class="container" style="max-width: 760px;">
    <nav class="breadcrumbs">
      <a href="../">Home</a><span>/</span><a href="./">Blog</a><span>/</span>Planning Permission in {name}
    </nav>
    <span class="eyebrow">Borough Guide &middot; April 2026</span>
    <h1 style="margin: 16px 0 24px; font-size: clamp(2.4rem, 5.5vw, 4.2rem);">Planning Permission in {name}: <em style="color: var(--accent); font-weight: 300;">2026 Guide</em></h1>
    <div class="author-byline">
      <div class="author-avatar">AD</div>
      <div class="author-info">
        <strong>By the Architectural Drawings team</strong>
        MCIAT Chartered &middot; 16 April 2026 &middot; 12 min read
      </div>
    </div>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container article-body">

    <!-- TL;DR -->
    <div class="tldr-box reveal">
      <h4>TL;DR &mdash; Key Facts</h4>
      <ul>
        <li>{tldr_svg} <span><strong>Planning authority:</strong> {planning_auth}</span></li>
        <li>{tldr_svg} <span><strong>Conservation areas:</strong> {conservation_count} designated areas</span></li>
        <li>{tldr_svg} <span><strong>Article 4 Directions:</strong> {"Yes" if article_4 else "None currently in force"}</span></li>
        <li>{tldr_svg} <span><strong>Postcodes covered:</strong> {postcodes}</span></li>
        <li>{tldr_svg} <span><strong>Typical housing:</strong> {housing.split('.')[0].split(';')[0].strip()}</span></li>
        <li>{tldr_svg} <span><strong>Householder application fee:</strong> &pound;258 (2026 rate)</span></li>
      </ul>
    </div>


    <!-- ============================================================ -->
    <!-- Section 1: Overview -->
    <!-- ============================================================ -->
    <h2>Planning in {name} &mdash; what you need to know</h2>

    <p>If you are planning a home improvement project in {name}, understanding the local planning landscape is essential before you begin. {name} is managed by <strong>{council}</strong>, which handles all planning applications, enforcement, and local plan policy for the borough.</p>

    <p>{character} The borough has a population of approximately {population:,} residents and covers postcodes {postcodes}.</p>

    <p>The housing stock in {name} is predominantly {housing.lower()[0]}{housing[1:].split('.')[0].strip()}. This mix of property types means that {planning_auth} deals with a wide range of applications, from rear extensions on terraced houses to loft conversions on semi-detached properties and full refurbishments of period homes in conservation areas.</p>

    <p>With <strong>{conservation_count} designated conservation areas</strong> and {"active Article 4 Directions" if article_4 else "no current Article 4 Directions"}, {name} {"has a relatively controlled planning environment where Permitted Development rights may be restricted in many areas" if article_4 and conservation_count > 25 else "has a planning environment that balances heritage protection in conservation areas with generally permissive policies elsewhere"}.</p>

    <p>At Architectural Drawings London, we prepare planning drawings and building regulations drawings for properties across all {name} postcodes. Our MCIAT chartered architectural technologists have experience with {planning_auth} and understand the specific policies, design guides, and precedents that apply in {name}. Our fixed fees start from &pound;840 for our Essentials package and &pound;1,750 for our Complete package &mdash; 30% below typical London architect rates.</p>


    <!-- ============================================================ -->
    <!-- Section 2: Article 4 -->
    <!-- ============================================================ -->
    {article_4_section}


    <!-- ============================================================ -->
    <!-- Section 3: Conservation areas -->
    <!-- ============================================================ -->
    {conservation_section}


    <!-- ============================================================ -->
    <!-- Section 4: Popular projects -->
    <!-- ============================================================ -->
    <h2>Popular projects in {name}</h2>

    <p>The types of planning applications most commonly submitted in {name} are shaped by the borough's housing stock. {housing.split('.')[0].strip()}, which drives demand for specific types of extensions and conversions.</p>

    {popular_projects(b)}


    <!-- ============================================================ -->
    <!-- Section 5: Costs -->
    <!-- ============================================================ -->
    <h2>How much do planning drawings cost in {name}?</h2>

    <p>The cost of a planning application in {name} has two components: the council application fee and the professional drawing fees.</p>

    <div class="price-box">
      <h4>Planning costs in {name}</h4>
      <div class="price-row">
        <span class="label">Householder planning application ({council})</span>
        <span class="amount">&pound;258</span>
      </div>
      <div class="price-row">
        <span class="label">Lawful Development Certificate</span>
        <span class="amount">&pound;129</span>
      </div>
      <div class="price-row">
        <span class="label">Our Essentials package (planning drawings)</span>
        <span class="amount">from &pound;840</span>
      </div>
      <div class="price-row">
        <span class="label">Our Complete package (planning + building regs)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
      <div class="price-row">
        <span class="label">Loft conversion package</span>
        <span class="amount">from &pound;1,225</span>
      </div>
      <div class="price-row">
        <span class="label">Mansard conversion package</span>
        <span class="amount">from &pound;1,575</span>
      </div>
    </div>

    <p>Our fixed-fee pricing means you know the cost upfront with no hourly billing surprises. We include a measured survey, existing and proposed plans, elevations, and a site plan &mdash; everything required for a valid planning submission to {planning_auth}. Our fees are 30% below typical London architect rates for the same scope of work.</p>

    <p>For Permitted Development projects that do not require a planning application, we recommend obtaining a Lawful Development Certificate (&pound;129 council fee). This provides formal legal confirmation that your project is lawful and prevents problems when selling the property. We prepare the LDC drawings and application on your behalf.</p>


    <!-- ============================================================ -->
    <!-- Section 6: Our experience -->
    <!-- ============================================================ -->
    {experience_section}


    <!-- ============================================================ -->
    <!-- Section 7: FAQ -->
    <!-- ============================================================ -->
    <h2>Frequently asked questions</h2>

    <div class="faq-list" style="margin-top: 24px;">

{faq_html}

    </div>


    <!-- ============================================================ -->
    <!-- Last updated -->
    <!-- ============================================================ -->
    <div style="margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--line); font-size: 0.88rem; color: var(--ink-softer);">
      Last updated: April 2026
    </div>

  </div>
</section>

<section class="cta-band" style="background: var(--bg-2);">
  <div class="container">
    <h2>Need planning drawings in <span class="accent">{name}?</span></h2>
    <p>Fixed fees from &pound;840. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.</p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <a href="../quote.html" class="btn btn-primary btn-lg">Get a free quote &rarr;</a>
      <a href="../services/planning-drawings.html" class="btn btn-outline btn-lg">Planning drawings service</a>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">

    <!-- SEO link grid -->
    <div class="footer-seo">
      <div>
        <h5>Services in London</h5>
        <ul>
          <li><a href="../services/planning-drawings.html">Planning permission drawings London</a></li>
          <li><a href="../services/building-regulations.html">Building regulations drawings London</a></li>
          <li><a href="../services/loft-conversions.html">Loft conversion drawings London</a></li>
          <li><a href="../services/house-extensions.html">House extension plans London</a></li>
          <li><a href="../services/mansard-roof.html">Mansard roof extensions London</a></li>
          <li><a href="../services.html">Measured survey London</a></li>
          <li><a href="../services.html">Lawful development certificate</a></li>
          <li><a href="../services.html">Permitted development drawings</a></li>
          <li><a href="../services.html">Party wall drawings</a></li>
          <li><a href="../services.html">Structural calculations</a></li>
        </ul>
      </div>
      <div>
        <h5>Loft conversions by borough</h5>
        <ul>
          <li><a href="../areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
          <li><a href="../areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
          <li><a href="../areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
          <li><a href="../areas/tower-hamlets/loft-conversions.html">Loft conversion Tower Hamlets</a></li>
          <li><a href="../areas/westminster/loft-conversions.html">Loft conversion Westminster</a></li>
          <li><a href="../areas/kensington-and-chelsea/loft-conversions.html">Loft conversion Kensington</a></li>
          <li><a href="../areas/hammersmith-and-fulham/loft-conversions.html">Loft conversion Hammersmith</a></li>
          <li><a href="../areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
          <li><a href="../areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
          <li><a href="../areas/southwark/loft-conversions.html">Loft conversion Southwark</a></li>
        </ul>
      </div>
      <div>
        <h5>Extension plans by borough</h5>
        <ul>
          <li><a href="../areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
          <li><a href="../areas/greenwich/house-extensions.html">Extension plans Greenwich</a></li>
          <li><a href="../areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
          <li><a href="../areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
          <li><a href="../areas/merton/house-extensions.html">Extension plans Merton</a></li>
          <li><a href="../areas/kingston-upon-thames/house-extensions.html">Extension plans Kingston</a></li>
          <li><a href="../areas/richmond-upon-thames/house-extensions.html">Extension plans Richmond</a></li>
          <li><a href="../areas/hounslow/house-extensions.html">Extension plans Hounslow</a></li>
          <li><a href="../areas/ealing/house-extensions.html">Extension plans Ealing</a></li>
          <li><a href="../areas/hillingdon/house-extensions.html">Extension plans Hillingdon</a></li>
          <li><a href="../areas/harrow/house-extensions.html">Extension plans Harrow</a></li>
          <li><a href="../areas/brent/house-extensions.html">Extension plans Brent</a></li>
        </ul>
      </div>
      <div>
        <h5>Planning drawings by borough</h5>
        <ul>
          <li><a href="../areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
          <li><a href="../areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
          <li><a href="../areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
          <li><a href="../areas/waltham-forest/planning-drawings.html">Planning drawings Waltham Forest</a></li>
          <li><a href="../areas/redbridge/planning-drawings.html">Planning drawings Redbridge</a></li>
          <li><a href="../areas/newham/planning-drawings.html">Planning drawings Newham</a></li>
          <li><a href="../areas/bexley/planning-drawings.html">Planning drawings Bexley</a></li>
          <li><a href="../areas/havering/planning-drawings.html">Planning drawings Havering</a></li>
          <li><a href="../areas/sutton/planning-drawings.html">Planning drawings Sutton</a></li>
          <li><a href="../areas/barking-and-dagenham/planning-drawings.html">Planning drawings Barking</a></li>
          <li><a href="../areas/city-of-london/planning-drawings.html">Planning drawings City of London</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom" style="border-top: 0; padding-top: 0;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; 86&ndash;90 Paul Street, London EC2A 4NE</span>
      <span><a href="../">Home</a> &middot; <a href="../services.html">Services</a> &middot; <a href="../pricing.html">Pricing</a> &middot; <a href="../privacy.html">Privacy</a> &middot; <a href="../terms.html">Terms</a></span>
    </div>
  </div>
</footer>

<script>
/* Architectural Drawings — main site interactions */
(() => {{
  'use strict';

  /* ---------- Scroll-triggered reveals ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {{
    const io = new IntersectionObserver((entries) => {{
      entries.forEach((entry) => {{
        if (entry.isIntersecting) {{
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }}
      }});
    }}, {{ threshold: 0.1, rootMargin: '0px 0px -60px 0px' }});
    reveals.forEach((el) => io.observe(el));
  }} else {{
    reveals.forEach((el) => el.classList.add('in'));
  }}

  /* ---------- Nav scroll state ---------- */
  const nav = document.getElementById('nav');
  if (nav) {{
    const onScroll = () => {{
      nav.classList.toggle('scrolled', window.scrollY > 12);
    }};
    onScroll();
    window.addEventListener('scroll', onScroll, {{ passive: true }});
  }}

  /* ---------- Mobile menu ---------- */
  const btnMenu = document.getElementById('btnMenu');
  if (btnMenu) {{
    btnMenu.addEventListener('click', () => {{
      document.body.classList.toggle('menu-open');
      const navLinks = document.querySelector('.nav-links');
      if (navLinks) {{
        navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '64px';
        navLinks.style.left = '0';
        navLinks.style.right = '0';
        navLinks.style.background = 'var(--bg)';
        navLinks.style.flexDirection = 'column';
        navLinks.style.padding = '16px 24px';
        navLinks.style.borderBottom = '1px solid var(--line)';
      }}
    }});
  }}

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq-item').forEach((item) => {{
    item.addEventListener('toggle', () => {{
      item.classList.toggle('open', item.open);
    }});
  }});

  /* ---------- Smooth anchor scrolling with nav offset ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {{
    anchor.addEventListener('click', (e) => {{
      const id = anchor.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const navHeight = nav ? nav.offsetHeight : 0;
      const y = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
      window.scrollTo({{ top: y, behavior: 'smooth' }});
    }});
  }});

}})();
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20for%20my%20project." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a3.04 3.04 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
  </a>
</div>

</body>
</html>"""

    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    for slug, borough in BOROUGHS.items():
        borough["_slug"] = slug
        html = generate_page(slug, borough)
        out_path = BLOG_DIR / f"planning-{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        count += 1
        print(f"  Generated: blog/planning-{slug}.html")

    print(f"\nDone. {count} borough guide pages generated in blog/")


if __name__ == "__main__":
    main()
