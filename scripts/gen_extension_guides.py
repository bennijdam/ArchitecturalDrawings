#!/usr/bin/env python3
"""
Generate 33 borough-specific extension cost guide blog posts.

Each page targets "Extension Cost in {Borough}" with borough-specific
build costs, planning context, and drawing fees.

Usage:
    cd architectural-drawings
    python scripts/gen_extension_guides.py
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
# Borough tier classification for build costs
# ---------------------------------------------------------------------------
INNER_PREMIUM = {
    "westminster", "kensington-and-chelsea", "camden", "islington", "hackney"
}
INNER_STANDARD = {
    "lambeth", "southwark", "tower-hamlets", "hammersmith-and-fulham",
    "wandsworth", "lewisham", "greenwich", "newham", "haringey",
    "waltham-forest", "brent", "city-of-london"
}
# Everything else is outer London


def get_tier(slug):
    if slug in INNER_PREMIUM:
        return "inner_premium"
    elif slug in INNER_STANDARD:
        return "inner_standard"
    else:
        return "outer"


def cost_range(slug):
    tier = get_tier(slug)
    if tier == "inner_premium":
        return ("3,000", "4,500")
    elif tier == "inner_standard":
        return ("2,500", "3,800")
    else:
        return ("2,200", "3,200")


def tier_label(slug):
    tier = get_tier(slug)
    if tier == "inner_premium":
        return "inner London premium borough"
    elif tier == "inner_standard":
        return "inner London borough"
    else:
        return "outer London borough"


# ---------------------------------------------------------------------------
# Helper: FAQ schema JSON
# ---------------------------------------------------------------------------
def faq_schema(faqs):
    """Build FAQPage JSON-LD from list of (question, answer) tuples."""
    items = []
    for q, a in faqs:
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
                f'<a href="extension-cost-{adj_slug}.html" '
                f'style="padding:8px 14px;border:1px solid var(--line-strong);border-radius:var(--r-full);'
                f'font-size:0.84rem;font-weight:500;text-decoration:none;transition:all 0.2s var(--ease);">'
                f'{adj_name}</a>'
            )
    return "\n".join(links)


# ---------------------------------------------------------------------------
# Helper: what affects costs section
# ---------------------------------------------------------------------------
def affects_costs_section(b, slug):
    name = b["name"]
    conservation_count = b["conservation_areas"]
    notable = b["notable_conservation"]
    article_4 = b["article_4"]
    article_4_notes = b.get("article_4_notes", "")
    housing = b["typical_housing"]

    paragraphs = []

    paragraphs.append(
        f"<p>Several local factors affect extension costs in {name}. Understanding "
        f"these before you start will help you budget accurately and avoid surprises.</p>"
    )

    # Conservation areas
    paragraphs.append(
        f"<h3>Conservation areas</h3>"
        f"<p>{name} has <strong>{conservation_count} designated conservation areas</strong>, "
        f"including {notable}. If your property is in a conservation area, Permitted Development "
        f"rights are restricted, meaning you may need a full planning application (&pound;258 "
        f"council fee). Conservation area applications also tend to require higher-quality materials "
        f"and more sympathetic design, which can increase build costs by 10-20%.</p>"
    )

    # Article 4
    if article_4:
        paragraphs.append(
            f"<h3>Article 4 Directions</h3>"
            f"<p>{name} has Article 4 Directions in place. {article_4_notes} "
            f"Where Article 4 applies, works that would normally be Permitted Development require "
            f"a full planning application. This adds &pound;258 to the council fee and typically "
            f"2-3 months to the project timeline, which can affect overall costs if you are "
            f"renting alternative accommodation during the build.</p>"
        )

    # Housing stock
    paragraphs.append(
        f"<h3>Property type</h3>"
        f"<p>The housing stock in {name} is predominantly {housing.lower().split('.')[0].strip()}. "
        f"Victorian and Edwardian terraces typically suit side-return and rear extensions, while "
        f"1930s semi-detached properties are well suited to two-storey rear extensions. Detached "
        f"houses offer the most flexibility but often have larger footprints, meaning higher "
        f"absolute costs even if the per-sqm rate is similar.</p>"
    )

    # Access and logistics
    paragraphs.append(
        f"<h3>Access and logistics</h3>"
        f"<p>Terraced properties in {name} often have limited rear access, which can increase "
        f"build costs by &pound;3,000-8,000 due to the need to transport materials through "
        f"the house. Properties with side access or rear lane access avoid this premium. "
        f"Parking restrictions and CPZ zones in {name} can also add skip permit and parking "
        f"suspension costs of &pound;200-500.</p>"
    )

    return "\n".join(paragraphs)


# ---------------------------------------------------------------------------
# Helper: planning vs PD section
# ---------------------------------------------------------------------------
def planning_vs_pd_section(b, slug):
    name = b["name"]
    article_4 = b["article_4"]
    article_4_notes = b.get("article_4_notes", "")
    conservation_count = b["conservation_areas"]
    planning_auth = b["planning_authority"]

    pd_restrictions = ""
    if article_4:
        pd_restrictions = (
            f" However, {name} has Article 4 Directions that may remove some PD rights. "
            f"{article_4_notes}"
        )

    html = (
        f"<h2>Planning vs Permitted Development in {name}</h2>\n"
        f"<p>Many house extensions in {name} can be built under <strong>Permitted Development</strong> "
        f"(PD) rights without needing a planning application. Under PD, single-storey rear extensions "
        f"can extend up to 6 metres from the original rear wall for terraced and semi-detached houses, "
        f"or 8 metres for detached houses (under the Prior Approval process).{pd_restrictions}</p>\n"
        f"<p>Properties in {name}'s {conservation_count} conservation areas have more restricted PD "
        f"rights. In conservation areas, you cannot build side extensions under PD, rear extensions "
        f"are more limited, and cladding changes require planning permission.</p>\n"
        f"<p><strong>Two-storey extensions</strong> almost always require full planning permission. "
        f"{planning_auth} generally expects two-storey extensions to be subordinate to the original "
        f"dwelling, set in from the side boundary, and designed to avoid unacceptable loss of light "
        f"or privacy to neighbouring properties.</p>\n"
        f"<p>We recommend obtaining a <strong>Lawful Development Certificate</strong> (&pound;129) "
        f"even for PD projects. This provides legal proof that your extension is lawful and is "
        f"valuable when selling the property. We prepare the LDC drawings and application on your behalf.</p>"
    )
    return html


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
def generate_page(slug, b):
    """Generate complete HTML for one borough extension cost guide."""
    name = b["name"]
    council = b["council"]
    planning_auth = b["planning_authority"]
    postcodes = b["postcodes"]
    conservation_count = b["conservation_areas"]
    notable = b["notable_conservation"]
    housing = b["typical_housing"]
    character = b["character"]
    article_4 = b["article_4"]
    population = b.get("population", 0)

    low, high = cost_range(slug)
    t_label = tier_label(slug)

    # Title and meta
    title = f"Extension Cost in {name} 2026 | AD"
    if len(title) > 60:
        title = f"Extension Cost {name} 2026 | AD"

    meta_desc = (
        f"House extension costs in {name} range from {chr(163)}{low} to {chr(163)}{high}/sqm. "
        f"Our drawing fees start from {chr(163)}1,225. "
        f"Council fee {chr(163)}258. Complete 2026 price guide."
    )
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."

    canonical = f"https://www.architecturaldrawings.uk/blog/extension-cost-{slug}.html"

    # Build FAQs
    faqs = [
        (
            f"How much does a house extension cost in {name}?",
            f"Build costs for a house extension in {name} typically range from {chr(163)}{low} to {chr(163)}{high} per square metre, as {name} is an {t_label}. A typical single-storey rear extension of 15-20 sqm would cost between {chr(163)}{int(low.replace(',','')) * 15:,} and {chr(163)}{int(high.replace(',','')) * 20:,} for the build alone. On top of build costs, you need architectural drawings (from {chr(163)}1,225 with us) and a council planning fee of {chr(163)}258 if planning permission is required."
        ),
        (
            f"Can I extend under Permitted Development in {name}?",
            f"Many single-storey rear extensions in {name} qualify as Permitted Development, allowing you to build without planning permission. You can extend up to 6 metres from the rear wall for terraced and semi-detached houses, or up to 8 metres for detached houses under Prior Approval. However, properties in {name}'s {conservation_count} conservation areas have more restricted PD rights{', and Article 4 Directions may further limit PD in some areas' if article_4 else ''}. We recommend applying for a Lawful Development Certificate ({chr(163)}129) to confirm PD eligibility."
        ),
        (
            f"How long does a house extension take in {name}?",
            f"A typical house extension project in {name} takes 5-8 months from initial instruction to completion. This breaks down as: 2-3 weeks for measured survey and drawing preparation, 8 weeks for planning determination by {planning_auth} (if required), 2-4 weeks for building regulations approval, and 8-16 weeks for construction depending on the size and complexity of the extension."
        ),
        (
            f"Do I need a Party Wall Agreement for an extension in {name}?",
            f"If your extension in {name} involves building on or near a shared boundary wall, excavating within 3 metres of a neighbour's foundation, or excavating within 6 metres to a depth below their foundation, you will need a Party Wall Agreement under the Party Wall etc. Act 1996. This is common for side-return extensions on terraced properties in {name}. A Party Wall surveyor typically costs {chr(163)}700-1,500 per neighbour. We can recommend Party Wall surveyors who work in {name}."
        ),
        (
            f"What experience do you have with extensions in {name}?",
            f"We prepare extension drawings for properties across all {name} postcodes ({postcodes}). Our MCIAT chartered architectural technologists understand {planning_auth}'s policies, design guides, and local precedents. We have a 98% first-time approval rate across all 33 London boroughs. Our fixed fees start from {chr(163)}1,225 for extensions, which is 30% below typical London architect rates."
        ),
    ]

    # FAQ schema JSON
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

    # TL;DR SVG
    tldr_svg = '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>'

    # Adjacent borough links
    adj_html = adjacent_links(b)

    # Typical extension cost examples
    low_int = int(low.replace(",", ""))
    high_int = int(high.replace(",", ""))
    single_low = f"{low_int * 15:,}"
    single_high = f"{high_int * 20:,}"
    side_low = f"{low_int * 8:,}"
    side_high = f"{high_int * 12:,}"
    two_low = f"{low_int * 25:,}"
    two_high = f"{high_int * 40:,}"

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
<meta property="og:title" content="House Extension Cost in {name}: 2026 Price Guide" />
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
  "headline": "House Extension Cost in {name}: 2026 Price Guide",
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
    {{ "@type": "ListItem", "position": 3, "name": "Extension Cost in {name}" }}
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

/* Related articles */
.related-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 24px 0 0;
}}
@media (max-width: 700px) {{ .related-grid {{ grid-template-columns: 1fr; }} }}
.related-card {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  padding: 24px;
  transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease);
}}
.related-card:hover {{
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}}
.related-card h4 {{
  font-size: 1.05rem;
  margin-bottom: 8px;
  line-height: 1.25;
}}
.related-card p {{
  font-size: 0.88rem;
  color: var(--ink-soft);
  line-height: 1.5;
  margin: 0;
}}
.related-card a {{
  text-decoration: none;
  color: inherit;
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

<!-- Hero placeholder -->
<section class="hero" style="padding-bottom: clamp(20px, 4vw, 40px);">
  <div class="container" style="max-width: 760px;">
    <nav class="breadcrumbs">
      <a href="../">Home</a><span>/</span><a href="./">Blog</a><span>/</span>Extension Cost in {name}
    </nav>
    <span class="eyebrow">Cost Guide &middot; April 2026</span>
    <h1 style="margin: 16px 0 24px; font-size: clamp(2.4rem, 5.5vw, 4.2rem);">House Extension Cost in {name}: <em style="color: var(--accent); font-weight: 300;">2026 Price Guide</em></h1>
    <div class="author-byline">
      <div class="author-avatar">AD</div>
      <div class="author-info">
        <strong>By the Architectural Drawings team</strong>
        MCIAT Chartered &middot; 16 April 2026 &middot; 10 min read
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
        <li>{tldr_svg} <span><strong>Build cost per sqm:</strong> &pound;{low} &ndash; &pound;{high} ({t_label})</span></li>
        <li>{tldr_svg} <span><strong>Our drawing fees:</strong> Essentials from &pound;1,225 &middot; Complete from &pound;1,750</span></li>
        <li>{tldr_svg} <span><strong>Council planning fee:</strong> &pound;258 (householder application, 2026)</span></li>
        <li>{tldr_svg} <span><strong>Typical projects:</strong> rear extension, side-return, two-storey, wraparound</span></li>
        <li>{tldr_svg} <span><strong>Conservation areas:</strong> {conservation_count} designated areas in {name}</span></li>
        <li>{tldr_svg} <span><strong>Permitted Development:</strong> {"Restricted by Article 4 in some areas" if article_4 else "Generally available outside conservation areas"}</span></li>
      </ul>
    </div>


    <!-- ============================================================ -->
    <!-- Section 1: Extension costs overview -->
    <!-- ============================================================ -->
    <h2>Extension costs in {name}</h2>

    <p>House extension build costs in {name} typically range from <strong>&pound;{low} to &pound;{high} per square metre</strong>, reflecting {name}'s position as an {t_label}. These figures cover the construction cost only and do not include professional fees, planning fees, or VAT.</p>

    <p>The actual cost of your extension will depend on the size, specification, and complexity of the project. A basic rear extension with standard finishes will sit at the lower end, while a high-specification kitchen extension with bi-fold doors, underfloor heating, and bespoke joinery will sit at the upper end or above.</p>

    <div class="price-box">
      <h4>Typical extension costs in {name} (build only)</h4>
      <div class="price-row">
        <span class="label">Single-storey rear extension (15-20 sqm)</span>
        <span class="amount">&pound;{single_low} &ndash; &pound;{single_high}</span>
      </div>
      <div class="price-row">
        <span class="label">Side-return extension (8-12 sqm)</span>
        <span class="amount">&pound;{side_low} &ndash; &pound;{side_high}</span>
      </div>
      <div class="price-row">
        <span class="label">Two-storey rear extension (25-40 sqm)</span>
        <span class="amount">&pound;{two_low} &ndash; &pound;{two_high}</span>
      </div>
      <div class="price-row">
        <span class="label">Wraparound extension (20-30 sqm)</span>
        <span class="amount">&pound;{low_int * 20:,} &ndash; &pound;{high_int * 30:,}</span>
      </div>
    </div>

    <p>On top of the build cost, you will need architectural drawings. Our Essentials package starts from &pound;1,225 for extension drawings including existing and proposed plans, elevations, and a site plan. Our Complete package from &pound;1,750 includes full planning and building regulations drawings. These fees are 30% below typical London architect rates.</p>


    <!-- ============================================================ -->
    <!-- Section 2: What affects costs -->
    <!-- ============================================================ -->
    <h2>What affects extension costs in {name}</h2>

    {affects_costs_section(b, slug)}


    <!-- ============================================================ -->
    <!-- Section 3: Our drawing fees -->
    <!-- ============================================================ -->
    <h2>Our drawing fees for {name} extensions</h2>

    <p>At Architectural Drawings London, we offer fixed-fee packages for house extension drawings. No hourly billing, no surprises. Our fees cover everything needed for a valid planning submission to {planning_auth} and for building regulations approval.</p>

    <div class="price-box">
      <h4>Drawing fees for extensions in {name}</h4>
      <div class="price-row">
        <span class="label">Essentials &mdash; planning drawings only</span>
        <span class="amount">from &pound;1,225</span>
      </div>
      <div class="price-row">
        <span class="label">Complete &mdash; planning + building regulations</span>
        <span class="amount">from &pound;1,750</span>
      </div>
      <div class="price-row">
        <span class="label">Bespoke &mdash; complex or large projects</span>
        <span class="amount">Custom quote</span>
      </div>
      <div class="price-row">
        <span class="label">Householder planning application ({council})</span>
        <span class="amount">&pound;258</span>
      </div>
      <div class="price-row">
        <span class="label">Lawful Development Certificate</span>
        <span class="amount">&pound;129</span>
      </div>
    </div>

    <p>Every package includes a measured survey of your existing property, existing floor plans and elevations, proposed floor plans and elevations, a site plan, and a design and access statement where required. Our MCIAT chartered architectural technologists handle the full process from survey to submission, and we liaise with {planning_auth} on your behalf.</p>

    <p>We cover all {name} postcodes: <strong>{postcodes}</strong>.</p>


    <!-- ============================================================ -->
    <!-- Section 4: Planning vs PD -->
    <!-- ============================================================ -->
    {planning_vs_pd_section(b, slug)}


    <!-- ============================================================ -->
    <!-- Section 5: FAQ -->
    <!-- ============================================================ -->
    <h2>Frequently asked questions</h2>

    <div class="faq-list" style="margin-top: 24px;">

{faq_html}

    </div>


    <!-- ============================================================ -->
    <!-- Section 6: Related articles -->
    <!-- ============================================================ -->
    <h2>Related articles</h2>

    <div class="related-grid">
      <div class="related-card">
        <a href="extension-cost-guide-london.html">
          <h4>House Extension Cost Guide: London 2026</h4>
          <p>Complete breakdown of extension costs across London, including build costs, professional fees, and council charges.</p>
        </a>
      </div>
      <div class="related-card">
        <a href="kitchen-extension-cost-london.html">
          <h4>Kitchen Extension Cost London</h4>
          <p>How much does a kitchen extension cost in London? Costs, layouts, and planning considerations.</p>
        </a>
      </div>
      <div class="related-card">
        <a href="double-storey-extension-guide.html">
          <h4>Two-Storey Extension Guide</h4>
          <p>Planning permission, Party Wall, design considerations, and costs for two-storey rear extensions in London.</p>
        </a>
      </div>
    </div>


    <!-- ============================================================ -->
    <!-- Adjacent boroughs -->
    <!-- ============================================================ -->
    <h2>Extension costs in nearby boroughs</h2>

    <div style="display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 32px;">
{adj_html}
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
    <h2>Need extension drawings in <span class="accent">{name}?</span></h2>
    <p>Fixed fees from &pound;1,225. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.</p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <a href="../quote.html?service=extension" class="btn btn-primary btn-lg">Get a free quote &rarr;</a>
      <a href="../services/house-extensions.html" class="btn btn-outline btn-lg">Extension drawings service</a>
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
        out_path = BLOG_DIR / f"extension-cost-{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        count += 1
        print(f"  Generated: blog/extension-cost-{slug}.html")

    print(f"\nDone. {count} extension cost guide pages generated in blog/")


if __name__ == "__main__":
    main()
