#!/usr/bin/env python3
"""
Generate 33 borough-specific loft conversion cost guide blog posts.

Each page targets "Loft Conversion Cost in {Borough}" with borough-specific
build costs, planning context, and drawing fees.

Usage:
    cd architectural-drawings
    python scripts/gen_loft_guides.py
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


def loft_costs(slug):
    """Return (dormer_low, dormer_high, mansard_low, mansard_high, velux_low, velux_high)."""
    tier = get_tier(slug)
    if tier == "inner_premium":
        return ("50,000", "70,000", "80,000", "120,000", "28,000", "40,000")
    elif tier == "inner_standard":
        return ("45,000", "65,000", "70,000", "110,000", "25,000", "38,000")
    else:
        return ("40,000", "60,000", "60,000", "95,000", "25,000", "40,000")


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
                f'<a href="loft-cost-{adj_slug}.html" '
                f'style="padding:8px 14px;border:1px solid var(--line-strong);border-radius:var(--r-full);'
                f'font-size:0.84rem;font-weight:500;text-decoration:none;transition:all 0.2s var(--ease);">'
                f'{adj_name}</a>'
            )
    return "\n".join(links)


# ---------------------------------------------------------------------------
# Helper: which loft type suits this borough
# ---------------------------------------------------------------------------
def loft_type_section(b, slug):
    name = b["name"]
    housing = b["typical_housing"].lower()
    character = b.get("character", "").lower()
    conservation_count = b["conservation_areas"]

    paragraphs = []

    paragraphs.append(
        f"<p>The best type of loft conversion for your property in {name} depends on "
        f"the existing roof structure, the available head height, and the planning "
        f"constraints affecting your property.</p>"
    )

    # Terraced housing
    if "terrace" in housing or "terraced" in housing:
        paragraphs.append(
            f"<h3>Dormer loft conversions</h3>"
            f"<p>{name} has extensive streets of terraced housing, making rear dormer loft "
            f"conversions the most popular option. A flat-roof rear dormer on a Victorian or "
            f"Edwardian mid-terrace can add 20-30 square metres of living space. Rear dormers "
            f"on terraced houses generally fall under Permitted Development, provided they do "
            f"not exceed the highest part of the existing roof and are set back from the eaves. "
            f"Properties in conservation areas may need full planning permission for dormers "
            f"visible from the highway.</p>"
        )

    # Mansard opportunities
    if "mansard" in character or "mansard" in housing or "terrace" in housing:
        paragraphs.append(
            f"<h3>Mansard loft conversions</h3>"
            f"<p>Mansard conversions replace the existing roof slope with a near-vertical front "
            f"and a shallow-sloped top, creating a full additional storey. Mansard conversions "
            f"<strong>always require planning permission</strong> as they alter the roofline. "
            f"{'In ' + name + ', mansard conversions have established precedents, particularly on Victorian and Edwardian terraces where the planning authority has approved similar schemes on neighbouring properties.' if 'mansard' in character else 'In ' + name + ', mansard conversions are assessed on a case-by-case basis, with design quality, streetscene impact, and conservation area status being key considerations.'} "
            f"Mansard conversions are more expensive than dormers but create significantly more "
            f"usable floor area with full standing head height throughout.</p>"
        )

    # Semi-detached / detached
    if "semi-detach" in housing or "detach" in housing:
        paragraphs.append(
            f"<h3>Hip-to-gable and dormer combinations</h3>"
            f"<p>The semi-detached and detached properties in {name} often have hipped roofs, "
            f"which limit the usable loft space. A hip-to-gable conversion extends the hipped "
            f"end to a full gable, combined with a rear dormer to maximise floor area. This "
            f"combination can add 25-35 square metres. Hip-to-gable conversions on semi-detached "
            f"properties may fall under Permitted Development, though the gable extension must "
            f"not extend beyond the plane of the existing house front.</p>"
        )

    # Velux / rooflight
    paragraphs.append(
        f"<h3>Velux (rooflight) conversions</h3>"
        f"<p>A Velux or rooflight conversion is the simplest and most affordable option, "
        f"suitable where there is already sufficient head height in the existing loft space. "
        f"Rooflights are installed into the existing roof slope without changing its shape. "
        f"This type of conversion almost always falls under Permitted Development and is "
        f"particularly suitable for properties in {name}'s {conservation_count} conservation "
        f"areas where changes to the roofline may not be acceptable. The trade-off is less "
        f"usable floor area compared to a dormer or mansard.</p>"
    )

    return "\n".join(paragraphs)


# ---------------------------------------------------------------------------
# Helper: planning permission for lofts section
# ---------------------------------------------------------------------------
def planning_section(b, slug):
    name = b["name"]
    article_4 = b["article_4"]
    article_4_notes = b.get("article_4_notes", "")
    conservation_count = b["conservation_areas"]
    notable = b["notable_conservation"]
    planning_auth = b["planning_authority"]

    html_parts = []

    html_parts.append(
        f"<p>Whether your loft conversion in {name} needs planning permission depends on "
        f"the type of conversion and the planning constraints affecting your property.</p>"
    )

    # PD rules
    html_parts.append(
        f"<h3>Permitted Development for lofts</h3>"
        f"<p>Most rear dormer and Velux loft conversions fall under Permitted Development "
        f"and do not require a planning application. The key PD conditions are:</p>"
        f"<ul>"
        f"<li>The dormer must not exceed the highest part of the existing roof</li>"
        f"<li>The dormer must be set back at least 200mm from the eaves</li>"
        f"<li>Materials must be similar in appearance to the existing house</li>"
        f"<li>No verandas, balconies, or raised platforms</li>"
        f"<li>Side-facing windows must be obscure-glazed and non-opening below 1.7m</li>"
        f"<li>Volume limit: 40 cubic metres for terraced houses, 50 cubic metres for others</li>"
        f"</ul>"
    )

    # Article 4
    if article_4:
        html_parts.append(
            f"<h3>Article 4 Directions</h3>"
            f"<p>{name} has Article 4 Directions in place. {article_4_notes} "
            f"While most Article 4 Directions in London target HMO conversions or commercial "
            f"changes of use rather than loft conversions directly, it is important to check "
            f"whether any specific restrictions apply to your property. We verify this as part "
            f"of our initial assessment.</p>"
        )

    # Conservation areas
    html_parts.append(
        f"<h3>Conservation areas</h3>"
        f"<p>{name} has {conservation_count} conservation areas, including {notable}. "
        f"In conservation areas, Permitted Development rights for loft conversions are more "
        f"restricted. Front-facing dormers and side-facing dormers visible from the highway "
        f"generally require planning permission. Rear dormers may still qualify as PD, but "
        f"the conservation officer may have views on materials and design. Mansard conversions "
        f"in conservation areas are assessed against the area's character appraisal and "
        f"management plan.</p>"
    )

    # Mansard planning
    html_parts.append(
        f"<h3>Mansard planning permission</h3>"
        f"<p>Mansard loft conversions always require full planning permission because they "
        f"change the shape and height of the roof. {planning_auth} will assess the application "
        f"against the local plan policies on design, character, amenity, and (where applicable) "
        f"conservation area requirements. Key factors include the impact on the streetscene, "
        f"whether similar mansards have been approved on the same street, the quality of the "
        f"proposed design, and the effect on neighbouring properties' light and privacy.</p>"
        f"<p>We recommend a <strong>pre-application</strong> with {planning_auth} for mansard "
        f"proposals, particularly in conservation areas. Pre-application advice costs vary but "
        f"typically range from &pound;200-600 and can significantly reduce the risk of refusal.</p>"
    )

    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
def generate_page(slug, b):
    """Generate complete HTML for one borough loft cost guide."""
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

    dormer_low, dormer_high, mansard_low, mansard_high, velux_low, velux_high = loft_costs(slug)
    t_label = tier_label(slug)

    # Title and meta
    title = f"Loft Conversion Cost {name} 2026 | AD"
    if len(title) > 60:
        title = f"Loft Cost {name} 2026 | AD"

    meta_desc = (
        f"Loft conversion costs in {name}: dormer {chr(163)}{dormer_low}-{chr(163)}{dormer_high}, "
        f"mansard {chr(163)}{mansard_low}-{chr(163)}{mansard_high}. "
        f"Drawing fees from {chr(163)}1,225. 2026 guide."
    )
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."

    canonical = f"https://www.architecturaldrawings.uk/blog/loft-cost-{slug}.html"

    # Build FAQs
    faqs = [
        (
            f"How much does a loft conversion cost in {name}?",
            f"Loft conversion costs in {name} vary by type. A rear dormer loft conversion typically costs {chr(163)}{dormer_low} to {chr(163)}{dormer_high}. A mansard conversion costs {chr(163)}{mansard_low} to {chr(163)}{mansard_high}. A Velux (rooflight only) conversion costs {chr(163)}{velux_low} to {chr(163)}{velux_high}. These are build costs only. On top you need architectural drawings (from {chr(163)}1,225 with us) and a council planning fee of {chr(163)}258 if planning permission is required."
        ),
        (
            f"Do I need planning permission for a loft conversion in {name}?",
            f"Most rear dormer and Velux loft conversions in {name} fall under Permitted Development and do not require planning permission, provided they meet the size and design conditions. However, mansard conversions always need planning permission. Properties in {name}'s {conservation_count} conservation areas have more restricted PD rights, and front-facing or side-facing dormers may require a planning application. We recommend applying for a Lawful Development Certificate ({chr(163)}129) to formally confirm PD eligibility."
        ),
        (
            f"What is the minimum head height for a loft conversion in {name}?",
            f"The minimum usable head height for a loft conversion is generally considered to be 2.2 metres at the highest point of the existing loft space (measured from the top of the ceiling joists to the underside of the ridge beam). If your existing head height is below this, a dormer or mansard conversion can increase it. We carry out a feasibility check as part of our initial survey to confirm whether your {name} property is suitable for a loft conversion."
        ),
        (
            f"Do I need a Party Wall Agreement for a loft conversion in {name}?",
            f"If your loft conversion in {name} involves work on a shared party wall (common with terraced and semi-detached properties), you will need a Party Wall Agreement under the Party Wall etc. Act 1996. This applies to work such as cutting into a party wall to insert steel beams, raising the party wall for a mansard, or building on top of a party wall. A Party Wall surveyor typically costs {chr(163)}700-1,500 per neighbour. We can recommend Party Wall surveyors who work in {name}."
        ),
        (
            f"Can I get a mansard loft conversion approved in {name}?",
            f"{'Yes, ' + name + ' has established mansard precedents, particularly on Victorian and Edwardian terraces. ' + planning_auth + ' has approved mansard conversions on many streets, which creates positive precedent for new applications.' if 'mansard' in character.lower() else name + ' assesses mansard applications on a case-by-case basis. ' + planning_auth + ' will consider the impact on the streetscene, conservation area status, design quality, and any existing precedents on your street.'} We prepare mansard drawings from {chr(163)}1,575 and have a 98% first-time approval rate across all 33 London boroughs."
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

    # PD status text
    pd_status = "Restricted by Article 4 in some areas" if article_4 else "Generally available for rear dormers"

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
<meta property="og:title" content="Loft Conversion Cost in {name}: 2026 Guide" />
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
  "headline": "Loft Conversion Cost in {name}: 2026 Guide",
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
    {{ "@type": "ListItem", "position": 3, "name": "Loft Conversion Cost in {name}" }}
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
      <a href="../">Home</a><span>/</span><a href="./">Blog</a><span>/</span>Loft Conversion Cost in {name}
    </nav>
    <span class="eyebrow">Cost Guide &middot; April 2026</span>
    <h1 style="margin: 16px 0 24px; font-size: clamp(2.4rem, 5.5vw, 4.2rem);">Loft Conversion Cost in {name}: <em style="color: var(--accent); font-weight: 300;">2026 Guide</em></h1>
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
        <li>{tldr_svg} <span><strong>Dormer loft conversion:</strong> &pound;{dormer_low} &ndash; &pound;{dormer_high} ({t_label})</span></li>
        <li>{tldr_svg} <span><strong>Mansard conversion:</strong> &pound;{mansard_low} &ndash; &pound;{mansard_high}</span></li>
        <li>{tldr_svg} <span><strong>Velux conversion:</strong> &pound;{velux_low} &ndash; &pound;{velux_high}</span></li>
        <li>{tldr_svg} <span><strong>Our drawing fees:</strong> Loft from &pound;1,225 &middot; Mansard from &pound;1,575</span></li>
        <li>{tldr_svg} <span><strong>Planning permission:</strong> {pd_status}</span></li>
        <li>{tldr_svg} <span><strong>Conservation areas:</strong> {conservation_count} in {name}</span></li>
      </ul>
    </div>


    <!-- ============================================================ -->
    <!-- Section 1: Loft conversion costs -->
    <!-- ============================================================ -->
    <h2>Loft conversion costs in {name}</h2>

    <p>Loft conversion build costs in {name} depend primarily on the type of conversion. As an {t_label}, {name} sits {"at the higher end" if get_tier(slug) == "inner_premium" else "in the mid-range" if get_tier(slug) == "inner_standard" else "at the more affordable end"} of London loft conversion pricing.</p>

    <div class="price-box">
      <h4>Loft conversion build costs in {name}</h4>
      <div class="price-row">
        <span class="label">Rear dormer loft conversion</span>
        <span class="amount">&pound;{dormer_low} &ndash; &pound;{dormer_high}</span>
      </div>
      <div class="price-row">
        <span class="label">Mansard loft conversion</span>
        <span class="amount">&pound;{mansard_low} &ndash; &pound;{mansard_high}</span>
      </div>
      <div class="price-row">
        <span class="label">Velux / rooflight only conversion</span>
        <span class="amount">&pound;{velux_low} &ndash; &pound;{velux_high}</span>
      </div>
      <div class="price-row">
        <span class="label">Hip-to-gable + rear dormer</span>
        <span class="amount">&pound;{dormer_low} &ndash; &pound;{mansard_low}</span>
      </div>
    </div>

    <p>These figures are build costs only and do not include professional fees (architect, structural engineer, Party Wall surveyor) or council fees. The actual cost will depend on the size of your loft, the specification of the fit-out, the structural complexity, and access constraints.</p>

    <p>A standard dormer loft conversion typically adds 20-30 square metres of living space, while a mansard can add 30-50 square metres with full standing head height throughout. The additional floor area and value uplift typically exceeds the cost of the conversion, making loft conversions one of the most cost-effective home improvements in {name}.</p>


    <!-- ============================================================ -->
    <!-- Section 2: Which loft type -->
    <!-- ============================================================ -->
    <h2>Which loft type suits {name} properties?</h2>

    {loft_type_section(b, slug)}


    <!-- ============================================================ -->
    <!-- Section 3: Planning permission -->
    <!-- ============================================================ -->
    <h2>Planning permission for lofts in {name}</h2>

    {planning_section(b, slug)}


    <!-- ============================================================ -->
    <!-- Section 4: Our drawing fees -->
    <!-- ============================================================ -->
    <h2>Our drawing fees for loft conversions in {name}</h2>

    <p>At Architectural Drawings London, we offer fixed-fee packages for loft conversion drawings. Our MCIAT chartered architectural technologists prepare everything needed for planning submission (where required) and building regulations approval.</p>

    <div class="price-box">
      <h4>Drawing fees for loft conversions</h4>
      <div class="price-row">
        <span class="label">Loft conversion package (dormer, hip-to-gable, Velux)</span>
        <span class="amount">from &pound;1,225</span>
      </div>
      <div class="price-row">
        <span class="label">Mansard conversion package</span>
        <span class="amount">from &pound;1,575</span>
      </div>
      <div class="price-row">
        <span class="label">Complete package (loft + full building regs)</span>
        <span class="amount">from &pound;1,750</span>
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

    <p>Every package includes a measured survey, existing and proposed floor plans and elevations, roof plan, sections, and a site plan. For mansard conversions, we also prepare a design and access statement and streetscene elevation. Our fees are 30% below typical London architect rates for the same scope of work.</p>

    <p>We cover all {name} postcodes: <strong>{postcodes}</strong>.</p>


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
        <a href="loft-vs-mansard.html">
          <h4>Loft Conversion vs Mansard: Which Is Right?</h4>
          <p>Comparing dormer, mansard, hip-to-gable, and Velux conversions: cost, planning, space, and value.</p>
        </a>
      </div>
      <div class="related-card">
        <a href="dormer-vs-velux-loft.html">
          <h4>Dormer vs Velux Loft Conversion</h4>
          <p>Pros and cons of dormer and Velux loft conversions, including cost, head height, and planning.</p>
        </a>
      </div>
      <div class="related-card">
        <a href="loft-conversion-without-planning.html">
          <h4>Loft Conversion Without Planning Permission</h4>
          <p>What you can build under Permitted Development, PD conditions, and when you need a full application.</p>
        </a>
      </div>
    </div>


    <!-- ============================================================ -->
    <!-- Adjacent boroughs -->
    <!-- ============================================================ -->
    <h2>Loft conversion costs in nearby boroughs</h2>

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
    <h2>Need loft conversion drawings in <span class="accent">{name}?</span></h2>
    <p>Fixed fees from &pound;1,225. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.</p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <a href="../quote.html?service=loft" class="btn btn-primary btn-lg">Get a free quote &rarr;</a>
      <a href="../services/loft-conversions.html" class="btn btn-outline btn-lg">Loft conversion service</a>
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
        out_path = BLOG_DIR / f"loft-cost-{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        count += 1
        print(f"  Generated: blog/loft-cost-{slug}.html")

    print(f"\nDone. {count} loft cost guide pages generated in blog/")


if __name__ == "__main__":
    main()
