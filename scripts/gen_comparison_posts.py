#!/usr/bin/env python3
"""Phase 6: Generate 15 comparison blog posts (X vs Y format).
Idempotent — skips existing files. Adds new URLs to sitemap-core.xml.
"""
from __future__ import annotations
import os, re, json

BLOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "blog"))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Extract CSS from existing post
ref = open(os.path.join(BLOG_DIR, "rear-vs-side-extension.html"), encoding="utf-8").read()
css_match = re.search(r"<style>.*?</style>", ref, re.DOTALL)
CSS_BLOCK = css_match.group(0) if css_match else "<style></style>"

HEAD_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>"""

FAVICON = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />"""

ANALYTICS = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-77CQ2PWJM4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-77CQ2PWJM4',{anonymize_ip:true});</script>"""

NAV = """<header class="nav" id="nav">
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
      <a href="../quote.html" class="btn btn-primary btn-sm">Free quote <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M4 10h12m-4-4 4 4-4 4"/></svg></a>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="../services/planning-drawings.html">Planning permission drawings London</a></li>
        <li><a href="../services/building-regulations.html">Building regulations drawings London</a></li>
        <li><a href="../services/loft-conversions.html">Loft conversion drawings London</a></li>
        <li><a href="../services/house-extensions.html">House extension plans London</a></li>
        <li><a href="../services/mansard-roof.html">Mansard roof extensions London</a></li>
        <li><a href="../services.html">All services</a></li>
      </ul></div>
      <div><h5>Loft conversions by borough</h5><ul>
        <li><a href="../areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="../areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="../areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="../areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="../areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
        <li><a href="../areas/barnet/loft-conversions.html">Loft conversion Barnet</a></li>
      </ul></div>
      <div><h5>Extension plans by borough</h5><ul>
        <li><a href="../areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
        <li><a href="../areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
        <li><a href="../areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
        <li><a href="../areas/ealing/house-extensions.html">Extension plans Ealing</a></li>
        <li><a href="../areas/brent/house-extensions.html">Extension plans Brent</a></li>
        <li><a href="../areas/hounslow/house-extensions.html">Extension plans Hounslow</a></li>
      </ul></div>
      <div><h5>Planning drawings by borough</h5><ul>
        <li><a href="../areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
        <li><a href="../areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
        <li><a href="../areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
        <li><a href="../areas/tower-hamlets/planning-drawings.html">Planning drawings Tower Hamlets</a></li>
        <li><a href="../areas/greenwich/planning-drawings.html">Planning drawings Greenwich</a></li>
        <li><a href="../areas/sutton/planning-drawings.html">Planning drawings Sutton</a></li>
      </ul></div>
    </div>
    <div class="footer-grid">
      <div class="footer-col footer-col-brand">
        <a href="../" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
        <p>Chartered architectural technology for London homeowners, landlords and developers. MCIAT &middot; ICO &middot; &pound;2m PI.</p>
        <p class="tiny" style="margin-top:16px;color:rgba(250,250,247,.45);">86-90 Paul Street, London EC2A 4NE<br/>020 7946 0000 &middot; hello@architecturaldrawings.uk</p>
      </div>
      <div class="footer-col"><h5>Services</h5><ul>
        <li><a href="../services/planning-drawings.html">Planning drawings</a></li>
        <li><a href="../services/building-regulations.html">Building regs</a></li>
        <li><a href="../services/loft-conversions.html">Loft conversions</a></li>
        <li><a href="../services/house-extensions.html">House extensions</a></li>
        <li><a href="../services/mansard-roof.html">Mansard &amp; dormers</a></li>
      </ul></div>
      <div class="footer-col"><h5>Company</h5><ul>
        <li><a href="../about.html">About</a></li>
        <li><a href="../pricing.html">Pricing</a></li>
        <li><a href="../projects/">Projects</a></li>
        <li><a href="../reviews/">Reviews</a></li>
        <li><a href="./">Blog</a></li>
      </ul></div>
      <div class="footer-col"><h5>Account</h5><ul>
        <li><a href="../portal/login.html">Sign in</a></li>
        <li><a href="../portal/register.html">Create account</a></li>
        <li><a href="../quote.html">Start a quote</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Architectural Drawings Ltd. Registered in England No. 14872049.</span>
      <span><a href="../sitemap.xml">Sitemap</a> &middot; <a href="../privacy.html">Privacy</a> &middot; <a href="../terms.html">Terms</a></span>
    </div>
  </div>
</footer>"""

JS = """<script>
(() => {
  const nav = document.getElementById('nav');
  if (nav) window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 12), {passive:true});
  const io = new IntersectionObserver(e => e.forEach(x => { if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);} }), {threshold:0.1});
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  document.querySelectorAll('.faq-item').forEach(item => item.addEventListener('toggle', () => item.classList.toggle('open', item.open)));
})();
</script>"""

CK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5" width="18" height="18"><path d="m5 10 3 3 7-7"/></svg>'
FI = '<span class="faq-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v10M3 8h10"/></svg></span>'


def faq_html(q, a):
    return f"""      <details class="faq-item">
        <summary>{q}{FI}</summary>
        <div class="faq-answer"><p>{a}</p></div>
      </details>"""


def faq_schema(q, a):
    return {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}


def related_card(href, title, desc):
    return f"""      <a href="{href}" class="service-card" style="padding:24px;">
        <h3 style="font-size:1.05rem;">{title}</h3>
        <p style="font-size:0.85rem;color:var(--ink-soft);margin-top:8px;">{desc}</p>
        <span class="service-card-link" style="margin-top:12px;">Read article &rarr;</span>
      </a>"""


def build(p: dict) -> str:
    canon = f"https://www.architecturaldrawings.uk/blog/{p['slug']}.html"
    tldr_lis = "\n".join(f"        <li>{CK} {t}</li>" for t in p["tldrs"])
    faqs_html = "\n".join(faq_html(q, a) for q, a in p["faqs"])
    faqs_schema = json.dumps([faq_schema(q, a) for q, a in p["faqs"]], indent=2)
    rels_html = "\n".join(related_card(*r) for r in p["related"])

    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}" />
<link rel="canonical" href="{canon}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{canon}" />
<meta property="og:title" content="{p['og_title']}" />
<meta property="og:description" content="{p['desc']}" />
<meta property="og:locale" content="en_GB" />
<meta property="article:published_time" content="2026-04-22" />
<meta property="article:author" content="Architectural Drawings London" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{p['og_title']}",
  "description": "{p['desc']}",
  "datePublished": "2026-04-22",
  "dateModified": "2026-04-22",
  "author": {{"@type":"Organization","name":"Architectural Drawings London","url":"https://www.architecturaldrawings.uk"}},
  "publisher": {{"@type":"Organization","name":"Architectural Drawings London","url":"https://www.architecturaldrawings.uk"}},
  "mainEntityOfPage": {{"@type":"WebPage","@id":"{canon}"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://www.architecturaldrawings.uk/"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"https://www.architecturaldrawings.uk/blog/"}},
    {{"@type":"ListItem","position":3,"name":"{p['breadcrumb']}"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": {faqs_schema}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "url": "{canon}",
  "speakable": {{"@type":"SpeakableSpecification","cssSelector":["h1",".tldr-box",".page-verdict"]}}
}}
</script>
{HEAD_FONTS}
{CSS_BLOCK}
{FAVICON}
{ANALYTICS}
</head>
<body>
{NAV}

<section class="hero" style="padding-bottom:clamp(20px,4vw,40px);">
  <div class="container" style="max-width:760px;">
    <nav class="breadcrumbs">
      <a href="../">Home</a><span>/</span><a href="./">Blog</a><span>/</span>{p['breadcrumb']}
    </nav>
    <span class="eyebrow">{p['eyebrow']} &middot; April 2026</span>
    <h1 style="margin:16px 0 24px;font-size:clamp(2.2rem,5vw,3.8rem);">{p['h1']}</h1>
    <div class="author-byline">
      <div class="author-avatar">AD</div>
      <div class="author-info">
        <strong>By the Architectural Drawings team</strong>
        MCIAT Chartered &middot; 22 April 2026 &middot; {p['mins']} min read
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0;">
  <div class="container article-body">

    <div class="tldr-box reveal">
      <h4>Key facts at a glance</h4>
      <ul>
{tldr_lis}
      </ul>
    </div>

{p['body']}

    <div class="page-verdict reveal" style="background:var(--accent-soft);border:1px solid var(--accent);border-radius:var(--r-lg);padding:28px 32px;margin:40px 0;">
      <h3 style="margin-bottom:12px;font-size:1.2rem;">Verdict</h3>
      <p style="color:var(--ink-soft);margin:0;">{p['verdict']}</p>
    </div>

    <h2 id="faq" class="reveal">Frequently asked questions</h2>
    <div class="faq-list" style="margin-top:24px;">
{faqs_html}
    </div>

    <div style="margin-top:56px;padding-top:24px;border-top:1px solid var(--line);font-size:0.88rem;color:var(--ink-softer);">
      Last updated: April 2026
    </div>
  </div>
</section>

<section style="background:var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Keep reading</span>
      <h2 style="margin-top:16px;">Related <em>articles</em></h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;">
{rels_html}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>{p['cta_h2']}</h2>
    <p>{p['cta_p']}</p>
    <a href="../quote.html" class="btn btn-accent btn-lg">
      Get a free quote in 60 seconds
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M4 10h12m-4-4 4 4-4 4"/></svg>
    </a>
  </div>
</section>

{FOOTER}
{JS}
</body>
</html>"""


# ─── POST DATA ──────────────────────────────────────────────────────────────

POSTS = [

  {
    "slug": "hip-to-gable-vs-rear-dormer",
    "title": "Hip-to-Gable vs Rear Dormer Loft Conversion | Which is Right for You?",
    "og_title": "Hip-to-Gable vs Rear Dormer Loft Conversion",
    "desc": "Hip-to-gable vs rear dormer loft conversion — costs, planning routes, usable space, and which London property types suit each option. Includes London planning context.",
    "breadcrumb": "Hip-to-Gable vs Rear Dormer",
    "eyebrow": "Loft conversions",
    "h1": "Hip-to-Gable vs Rear Dormer: <em>Which Loft Conversion is Right for You?</em>",
    "mins": "7",
    "tldrs": [
      "Hip-to-gable suits semi-detached and detached houses; rear dormers suit any roof type",
      "Hip-to-gable adds 15–25% more floor area than a rear dormer alone",
      "Combining both (L-shape) is the maximum-space option on semis",
      "Both routes can use permitted development on most London properties",
      "Hip-to-gable costs £800–£1,200 more to build than a straight rear dormer",
      "Both need a Lawful Development Certificate or planning permission depending on location",
    ],
    "body": """
    <h2 class="reveal">What is a hip-to-gable loft conversion?</h2>
    <p class="reveal">A hip-to-gable conversion infills the sloping hipped end of a roof, replacing it with a vertical gable wall. This creates a rectangular box room at the end of the loft where previously there was only a sloping void. On a 1930s semi-detached — the most common candidate — it turns a tight triangular space into a usable bedroom or dressing room.</p>
    <p class="reveal">The hip-to-gable element alone rarely provides enough headroom for a full bedroom. It is almost always combined with a full-width rear dormer to create a proper loft floor with two bedrooms and a bathroom. The combined form is called an L-shape loft conversion.</p>

    <h2 class="reveal">What is a rear dormer loft conversion?</h2>
    <p class="reveal">A rear dormer is a vertical extension built out from the rear slope of an existing roof. It creates a box-shaped addition at roof level, with vertical walls and a flat roof. On a terrace, a full-width rear dormer running from party wall to party wall is the standard approach. On a semi, the dormer must be set back 200 mm from the party wall boundary projection under permitted development rules.</p>
    <p class="reveal">A rear dormer alone is sufficient for a Victorian or Edwardian terrace, where the hip does not exist. On a semi, a rear dormer alone produces a loft with a triangular room at the end — functional but limited.</p>

    <h2 class="reveal">Planning: which route applies?</h2>
    <p class="reveal">Both conversions can proceed via permitted development (no planning permission required) provided the property meets the standard PD criteria: not in an Article 4 direction area, volume within limits (40 m³ terraces, 50 m³ detached/semis), set back from the eaves, and not visible from the principal elevation. A Lawful Development Certificate is strongly recommended — most mortgage lenders and conveyancers require it for either type.</p>
    <p class="reveal">In Article 4 direction areas — which are common in inner London boroughs such as Islington, Camden, Hackney, and parts of Lambeth — both conversions require full planning permission. The hip-to-gable is more contentious in conservation areas because it alters the roofline visible from neighbouring streets.</p>

    <h2 class="reveal">Cost and space comparison</h2>
    <p class="reveal">A rear dormer alone on a terrace costs £35,000–£55,000 to build (2026 London prices). A hip-to-gable plus rear dormer on a semi typically costs £45,000–£70,000 — the additional £8,000–£15,000 reflects the structural work of infilling the hip and rebuilding the gable. The additional floor area gained by the hip-to-gable element is typically 6–10 m², which in London translates to meaningful added value.</p>
    <p class="reveal">In terms of drawings fees, both conversions fall under our standard <a href="../services/loft-conversions.html">loft conversion drawings</a> package from £1,225, which covers existing and proposed plans, four elevations, a roof plan, and all documents needed for LDC or planning.</p>
    """,
    "verdict": "On a semi-detached or detached, choose the L-shape (hip-to-gable plus rear dormer) — the extra build cost delivers significantly more usable space. On a terrace, a full-width rear dormer is the standard and most cost-effective approach.",
    "faqs": [
      ("Can I do a hip-to-gable on a terraced house?", "No. Terraced houses have gable ends, not hipped ends, so the hip-to-gable conversion does not apply. Terraces use a full-width rear dormer instead."),
      ("Does a hip-to-gable need planning permission in London?", "Not in most cases. Permitted development covers hip-to-gable conversions on semis and detached houses that are not in Article 4 direction areas. A Lawful Development Certificate is required to confirm the works are lawful."),
      ("How much floor space does a hip-to-gable add?", "Typically 6–10 m² of additional usable floor area compared to a rear dormer alone. Combined with a rear dormer, an L-shape loft conversion commonly adds 25–40 m² of new floor space to a 1930s semi."),
      ("What is an L-shape loft conversion?", "An L-shape combines a hip-to-gable at the side with a full-width rear dormer. The two elements together produce the maximum usable loft space on a semi-detached house."),
      ("Which loft conversion adds more value in London?", "The L-shape (hip-to-gable plus dormer) typically adds more absolute value because it creates a larger, more marketable floor area. Estate agents consistently report that a two-bedroom loft with en-suite adds 15–25% to a property's value in most London boroughs."),
    ],
    "related": [
      ("loft-vs-mansard.html", "Loft Conversion vs Mansard Roof", "Full comparison of the two main upper-level extension options for London terraces."),
      ("loft-conversion-without-planning.html", "Loft Conversion Without Planning Permission", "When permitted development applies and how to get an LDC."),
      ("dormer-vs-velux-loft.html", "Dormer vs Velux Loft Conversion", "Which roof opening works best for your property and budget?"),
    ],
    "cta_h2": "Ready to <em>design your loft conversion?</em>",
    "cta_p": "MCIAT-chartered drawings from £1,225. Fixed fee, 98% first-time approval rate across all 33 London boroughs.",
  },

  {
    "slug": "single-vs-double-storey-extension",
    "title": "Single vs Double Storey Extension London | Planning, Cost & Value Guide 2026",
    "og_title": "Single vs Double Storey Extension: Planning, Cost & Value",
    "desc": "Single storey vs double storey rear extension — London planning rules, build costs, added value, and when each option makes sense. 2026 guide by MCIAT-chartered technologists.",
    "breadcrumb": "Single vs Double Storey Extension",
    "eyebrow": "House extensions",
    "h1": "Single vs Double Storey Extension: <em>Which Should You Build?</em>",
    "mins": "8",
    "tldrs": [
      "Single storey: simpler planning, lower cost, suits most properties",
      "Double storey: more space per £ of building cost, higher planning complexity",
      "Single storey PD limit: 3 m on semis, 4 m on detached (or 6/8 m via LHES)",
      "Double storey always needs full planning permission — no PD route",
      "Double storey costs 60–80% more to build but adds 90–120% more floor area",
      "Both need building regulations drawings regardless of planning route",
    ],
    "body": """
    <h2 class="reveal">The planning permission difference</h2>
    <p class="reveal">Single-storey rear extensions can proceed via permitted development on most London properties — no planning application required, just a Lawful Development Certificate if you want legal confirmation. The standard PD limit is 3 m depth on semis and terraces, 4 m on detached houses. The Larger Home Extension Scheme (LHES) extends this to 6 m and 8 m respectively via a simple prior approval process.</p>
    <p class="reveal">Double-storey extensions have no PD route. Every two-storey rear extension requires a full householder planning application. The main policy test is the 45-degree rule applied from the nearest neighbouring habitable window — this limits how deep a two-storey extension can be before it overshadows neighbours. Most London boroughs also require upper-floor windows to be at high sill levels (1.7 m+) or obscure-glazed to address privacy concerns.</p>

    <h2 class="reveal">Cost comparison (London 2026)</h2>
    <p class="reveal">Single-storey rear extensions typically cost £45,000–£80,000 to build in London, depending on size, specification, and finishes. A 4 m × 6 m single-storey extension adds approximately 24 m² of new floor space.</p>
    <p class="reveal">Double-storey extensions cost £75,000–£130,000 for a similar footprint — the additional cost reflects the structural frame, staircase modifications, and more complex building regulations. However, a two-storey extension of the same footprint adds roughly 48 m² of new floor space, making the cost per square metre considerably lower than two separate single-storey phases.</p>

    <h2 class="reveal">Added value in London</h2>
    <p class="reveal">In London's property market, floor area is the primary value driver. A single-storey 24 m² extension typically adds £60,000–£120,000 to a property's value depending on the borough. A double-storey 48 m² extension adds £110,000–£220,000. Both tend to return more than their build cost in London's higher-value boroughs.</p>
    <p class="reveal">The double storey is particularly efficient in inner boroughs where garden depth is limited — if you can only build 3 m deep before hitting your garden constraints, going up doubles your return without reducing garden further.</p>

    <h2 class="reveal">When to choose single storey</h2>
    <p class="reveal">Choose single storey when: you want to avoid planning permission risk, your budget is under £80,000, you want a faster programme (8–12 weeks vs 12–18 weeks for two-storey), or the planning policy in your area makes a two-storey application marginal. Conservation areas often make double-storey extensions difficult to approve.</p>

    <h2 class="reveal">When to choose double storey</h2>
    <p class="reveal">Choose double storey when: you need significantly more space (e.g. adding a bedroom as well as kitchen), you are planning to stay long-term, your garden can absorb the footprint, and your neighbours are unlikely to object. The cost per m² is lower, and the value uplift per £ spent is generally higher.</p>
    """,
    "verdict": "If budget and planning risk are the main constraints, build single storey first via PD. If you need maximum space and can navigate a planning application, double storey delivers more floor area per pound spent.",
    "faqs": [
      ("Does a double storey extension always need planning permission?", "Yes. There is no permitted development route for two-storey rear extensions. A householder planning application is always required."),
      ("Can I build single storey first then add a second storey later?", "Yes, but you will need planning permission for the second phase. The planning officer will assess the complete two-storey result, so the cumulative impact on neighbours is considered. It is generally more efficient to apply for both storeys at once."),
      ("What is the 45-degree rule for extensions?", "The 45-degree rule checks that a proposed extension does not block daylight to the nearest habitable window of a neighbouring property by more than 45 degrees. It is measured in both plan and elevation. It primarily limits how deep a two-storey extension can be relative to neighbouring windows."),
      ("How long does planning permission take for a double storey extension?", "Householder planning applications have an 8-week statutory determination period in England, but many London boroughs take 10–14 weeks in practice. Barnet, Croydon, and Sutton tend to be faster; Haringey, Hackney, and Tower Hamlets are typically slower."),
      ("Are building regulations required for both?", "Yes. All extensions require building regulations approval regardless of the planning route. Building regulations cover structure, insulation, fire safety, drainage, and energy performance. Full Plans submission is recommended — it gives your builder an approved specification before starting on site."),
    ],
    "related": [
      ("rear-vs-side-extension.html", "Rear vs Side Return Extension", "Which direction adds more value on a Victorian terrace?"),
      ("side-return-vs-wraparound.html", "Side Return vs Wraparound Extension", "Comparing two popular L-shaped extension configurations."),
      ("extension-vs-loft-conversion.html", "Extension vs Loft Conversion", "Which adds more value and space for the money in London?"),
    ],
    "cta_h2": "Get <em>extension drawings</em> from £840",
    "cta_p": "Planning drawings, building regulations, or both — MCIAT-chartered, fixed fee, 98% first-time approval rate.",
  },

  {
    "slug": "flat-vs-pitched-roof-extension",
    "title": "Flat Roof vs Pitched Roof Extension | Planning, Cost & Longevity 2026",
    "og_title": "Flat Roof vs Pitched Roof Extension: Which is Better?",
    "desc": "Flat roof vs pitched roof extension — planning acceptability, build cost, longevity, and which London councils prefer which. Expert guide from MCIAT-chartered technologists.",
    "breadcrumb": "Flat vs Pitched Roof Extension",
    "eyebrow": "House extensions",
    "h1": "Flat Roof vs Pitched Roof Extension: <em>What London Councils Actually Prefer</em>",
    "mins": "6",
    "tldrs": [
      "Flat roofs cost 15–25% less to build than equivalent pitched roofs",
      "Most London councils accept flat roofs on rear extensions — it is the modern standard",
      "Pitched roofs are often required in conservation areas to match the host building",
      "Modern flat roofs (EPDM or GRP) last 25–50 years with minimal maintenance",
      "Pitched roofs suit properties where the extension is visible from the street",
      "Roof lanterns and glazed roofs only work on flat roof structures",
    ],
    "body": """
    <h2 class="reveal">What London planning officers actually say</h2>
    <p class="reveal">The majority of London boroughs accept flat roofs on rear extensions as the default — the 2016 National Planning Policy Framework abandoned the earlier preference for pitched roofs to match host buildings. Planning officers across Southwark, Lambeth, Lewisham, and Wandsworth routinely approve flat-roof rear extensions on Victorian and Edwardian terraces without conditions.</p>
    <p class="reveal">Conservation areas are the exception. Many conservation area character appraisals specify that extensions should use materials and forms sympathetic to the host building — which on a Victorian terrace typically means pitched roofs in slate or clay tile. If your property is in a conservation area, check the specific character appraisal before committing to a flat roof design.</p>

    <h2 class="reveal">Build cost comparison</h2>
    <p class="reveal">A flat roof extension costs approximately £1,200–£1,600/m² to build in London. A pitched roof extension of the same footprint costs £1,400–£1,900/m² — the additional cost reflects the roof structure (rafters, ridge, purlins), the covering (tiles or slate), and the longer labour time to build the pitch correctly. For a typical 4 m × 5 m extension, the flat roof option saves £3,000–£8,000.</p>

    <h2 class="reveal">Longevity and maintenance</h2>
    <p class="reveal">The old reputation of flat roofs as leak-prone is outdated. Modern EPDM (rubber) flat roofs carry 20-year manufacturer warranties and last 30–50 years in practice. GRP (fibreglass) roofs are similarly durable. The key is a properly designed drainage fall (minimum 1:40) and quality installation. A flat roof installed correctly in 2026 will outlast most pitched roofs on the cost-of-maintenance comparison.</p>
    <p class="reveal">Pitched roofs do have the advantage of passive water shedding — rain leaves the roof surface faster on a 35-degree pitch than on a 1:40 flat. In London's climate, this is a marginal factor when both roof types are properly installed.</p>

    <h2 class="reveal">Roof lanterns and glazed roofs</h2>
    <p class="reveal">The primary functional advantage of a flat roof is the ability to incorporate roof lanterns, frameless glazing, and structural rooflights. These are not possible on a pitched roof without a separate dormer or rooflight. Flat roof extensions with large overhead glazing are the current standard for kitchen-diners in London, and many planning officers actively support them as a high-quality design response.</p>
    """,
    "verdict": "For most rear extensions in London, a flat roof is the better choice — lower cost, accepted by planners, and enables overhead glazing. Opt for pitched only if your property is in a conservation area or the extension will be visible from the street.",
    "faqs": [
      ("Do flat roofs need planning permission?", "No more than pitched roofs. Planning permission is triggered by the size and location of the extension, not the roof type."),
      ("What is the best flat roof material for a London extension?", "EPDM (rubber membrane) is the most widely specified material for new flat roofs in London — durable, fully welded seams, 20-year guarantee. GRP (fibreglass) is also excellent for smaller roofs. Avoid built-up felt on new construction."),
      ("Can I put a roof terrace on a flat roof extension?", "Yes, but it requires planning permission even if the extension itself was permitted development. The roof terrace adds a new level of activity that can affect neighbours' privacy, which planning officers assess carefully."),
      ("Will a flat roof extension devalue my home?", "No. A well-designed flat roof extension adds value. Estate agents and surveyors value extensions by floor area, not roof style. Flat roofs on rear extensions are now the norm and are not penalised in valuations."),
      ("How much fall does a flat roof need?", "A minimum 1:40 fall (2.5%) is required to ensure drainage. Many builders specify 1:60 falls which are technically acceptable but marginal — insist on 1:40 or steeper, especially for EPDM roofs with welded seams."),
    ],
    "related": [
      ("single-vs-double-storey-extension.html", "Single vs Double Storey Extension", "Planning, cost and value comparison for London homeowners."),
      ("rear-vs-side-extension.html", "Rear vs Side Return Extension", "Direction matters — which adds more value?"),
      ("extension-cost-guide-london.html", "House Extension Cost Guide London", "Full breakdown of London extension costs by type and borough."),
    ],
    "cta_h2": "Need <em>extension drawings?</em>",
    "cta_p": "Planning drawings from £840. Fixed fee, no hidden costs, MCIAT-chartered team.",
  },

  {
    "slug": "ldc-vs-planning-permission",
    "title": "Lawful Development Certificate vs Planning Permission | When Do You Need Each?",
    "og_title": "Lawful Development Certificate vs Planning Permission: Key Differences",
    "desc": "LDC vs planning permission — what each is, when you need one, how long each takes, and the consequences of getting it wrong. Essential guide for London homeowners.",
    "breadcrumb": "LDC vs Planning Permission",
    "eyebrow": "Planning guidance",
    "h1": "Lawful Development Certificate vs Planning Permission: <em>Which Do You Need?</em>",
    "mins": "7",
    "tldrs": [
      "LDC confirms works are lawful under PD — planning permission grants rights that don't exist yet",
      "LDC takes 6–8 weeks; planning permission takes 8–13 weeks in London",
      "LDC costs £234 in council fees; planning permission costs £258 (householder, 2026 rates)",
      "Both provide legal certainty for lenders and conveyancers",
      "Neither is required to start work — but both protect you if challenged",
      "Article 4 directions remove PD rights, forcing a planning application instead of an LDC",
    ],
    "body": """
    <h2 class="reveal">What is a Lawful Development Certificate?</h2>
    <p class="reveal">A Lawful Development Certificate (LDC) is a legal document issued by the council confirming that proposed works fall within your existing permitted development rights — meaning planning permission is not required. It is not planning permission itself. The council is confirming that the law already gives you the right to do the works, and issuing a certificate as evidence of that fact.</p>
    <p class="reveal">LDCs are commonly used for loft conversions, rear extensions within PD limits, outbuildings, and solar panels. The certificate is essential when selling a property — without it, the buyer's solicitor has no documentary evidence that the works were lawful, and the sale can be delayed or the purchase price reduced.</p>

    <h2 class="reveal">What is planning permission?</h2>
    <p class="reveal">Planning permission is a formal grant of permission to carry out works that are not covered by permitted development rights. It requires a planning application to the local authority, a period of public consultation, and a decision by a planning officer (or committee for contested applications). Planning permission is required for: two-storey extensions, works in conservation areas that exceed PD limits, new dwellings, changes of use, and any works in Article 4 direction areas where PD rights have been removed.</p>

    <h2 class="reveal">The Article 4 complication</h2>
    <p class="reveal">Article 4 directions are the primary reason London homeowners who expect to need only an LDC find themselves needing full planning permission. Councils can apply Article 4 directions to remove permitted development rights in specific areas — most commonly in conservation areas, but also in some interwar housing estates. If your property is in an Article 4 area, any extension or loft conversion that would normally be PD requires a full householder planning application instead.</p>
    <p class="reveal">Check the council's interactive planning map before assuming your works are PD. Article 4 directions are not always obvious from street-level observation — they cover entire roads or postcodes rather than individual properties.</p>

    <h2 class="reveal">Which gives stronger legal protection?</h2>
    <p class="reveal">Planning permission is more absolute — it grants a new right that did not previously exist, and once implemented it is permanent. An LDC confirms an existing right but does not create new ones. For enforcement purposes, both documents provide strong protection. However, if the information submitted for an LDC was inaccurate — for example, the volume calculation was wrong — the certificate can be revisited. Planning permission granted on accurate information is harder to overturn.</p>
    """,
    "verdict": "If your works fall within permitted development, apply for an LDC — it is faster, cheaper, and all you legally need. If PD rights don't apply (Article 4, conservation area limits exceeded, two-storey works), you need planning permission.",
    "faqs": [
      ("Do I need an LDC to start building?", "No. You can legally build permitted development works without any certificate. An LDC is not a prerequisite for starting — it is evidence of lawfulness for future sale, mortgage, and enforcement purposes."),
      ("Can I get an LDC after the work is done?", "Yes. A Certificate of Lawful Use or Development (CLUD) can be applied for retrospectively. It requires the same information as a prospective LDC but applies to works already carried out."),
      ("How long is an LDC valid?", "An LDC does not expire. It is a permanent legal document confirming the works were lawful under the rules in force at the time of issue."),
      ("What happens if I build without an LDC or planning permission?", "If your works are genuinely permitted development, the council cannot enforce against them — but without an LDC you have no documentary proof, which creates problems on sale. If the works are not PD, the council can issue an enforcement notice requiring demolition."),
      ("Can my neighbour challenge an LDC?", "An LDC is issued by the council as a legal determination. Neighbours cannot appeal against an LDC as they can against planning permission. However, if the LDC was based on incorrect information, the council can revoke it."),
    ],
    "related": [
      ("planning-vs-permitted-development.html", "Planning Permission vs Permitted Development", "Understanding the fundamental distinction every London homeowner needs."),
      ("full-planning-vs-prior-approval.html", "Full Planning vs Prior Approval", "When prior approval applies and how it differs from full planning."),
      ("loft-conversion-without-planning.html", "Loft Conversion Without Planning Permission", "How the PD route works for loft conversions in practice."),
    ],
    "cta_h2": "Need <em>drawings for an LDC or planning application?</em>",
    "cta_p": "MCIAT-chartered drawings from £840. We prepare the full application package — drawings, forms, and supporting documents.",
  },

  {
    "slug": "building-notice-vs-full-plans",
    "title": "Building Notice vs Full Plans | Which Building Regs Route is Right for You?",
    "og_title": "Building Notice vs Full Plans: Building Regulations Routes Compared",
    "desc": "Building notice vs full plans submission — the two routes to building regulations approval explained. Costs, risks, timescales, and which is right for your London project.",
    "breadcrumb": "Building Notice vs Full Plans",
    "eyebrow": "Building regulations",
    "h1": "Building Notice vs Full Plans: <em>Which Building Regs Route Should You Use?</em>",
    "mins": "6",
    "tldrs": [
      "Full Plans: detailed drawings checked before work starts — maximum certainty",
      "Building Notice: no drawings submitted — BCO inspects as you build",
      "Full Plans is recommended for extensions, loft conversions, and any structural work",
      "Building Notice suits simple, low-risk work (e.g. boiler replacement, internal wall removal)",
      "Full Plans approval takes 5–8 weeks; Building Notice gives same-day registration",
      "Building Notice cannot be used for commercial buildings or shops",
    ],
    "body": """
    <h2 class="reveal">Full Plans submission explained</h2>
    <p class="reveal">A Full Plans submission involves providing detailed technical drawings to the building control body (BCB) before work starts. The BCO checks the drawings against all relevant Approved Documents — structure, insulation, fire safety, drainage, ventilation, accessibility — and issues a decision notice approving or conditionally approving the plans. The builder then works to the approved drawings, and the BCO inspects at key stages.</p>
    <p class="reveal">The main advantage of Full Plans is certainty. Your builder knows exactly what they are building to an approved specification. Any design issues are resolved at drawing stage — before concrete is poured. This is vastly cheaper than resolving problems on site.</p>

    <h2 class="reveal">Building Notice explained</h2>
    <p class="reveal">A Building Notice is a simpler notification route. You give the council 48 hours' notice of intention to start work, paying a fee. No drawings are required — the BCO inspects at key stages and advises on compliance as work progresses. It is faster to initiate but transfers risk to the builder and client.</p>
    <p class="reveal">The risk with Building Notice is that if the BCO requires changes at inspection — a foundation too shallow, insulation below Part L standards, fire stopping inadequate — the builder may need to demolish and redo finished work. This is uncommon on simple projects but a real cost risk on complex ones.</p>

    <h2 class="reveal">Which route for extensions and loft conversions?</h2>
    <p class="reveal">Always use Full Plans for structural extensions and loft conversions. The structural content alone — foundation design, beam sizing, floor structure, roof structure — requires detailed drawings that must be checked against Part A. A Building Notice on a structural project means the BCO is making structural judgements on site without pre-approved calculations — not a position most experienced BCOs or structural engineers are comfortable with.</p>
    <p class="reveal">Our standard <a href="../services/building-regulations.html">building regulations drawings</a> package is designed for Full Plans submission. It includes structural drawings coordinated with an engineer, Part L energy calculations, Part B fire spread details, Part F ventilation, and Part P electrical notes — everything the BCO needs to issue a Full Plans approval.</p>

    <h2 class="reveal">Approved inspectors vs local authority building control</h2>
    <p class="reveal">Both routes — Full Plans and Building Notice — can be administered by either the local authority building control (LABC) or an approved inspector (private sector). Approved inspectors typically offer faster turnaround on Full Plans (3–5 weeks vs 5–8 weeks for LABC) and more flexible inspection scheduling. The choice does not affect the technical standard — both must apply the same Approved Documents.</p>
    """,
    "verdict": "Use Full Plans for any project involving structure, extensions, or loft conversions. The pre-approval certainty is worth the 5–8 week wait. Reserve Building Notice for simple, low-risk works where drawings are not needed.",
    "faqs": [
      ("Can I switch from Building Notice to Full Plans mid-project?", "Yes. You can regularise a Building Notice project by submitting Full Plans drawings at any stage. The BCO will assess the work already completed. This is more expensive and disruptive than submitting Full Plans at the start."),
      ("Is a completion certificate issued under both routes?", "Yes. Both Full Plans and Building Notice result in a final completion certificate once the BCO is satisfied all work complies. The completion certificate is required for sale and for insurance purposes."),
      ("How much does building regulations approval cost?", "The fee depends on the project type and local authority. For a typical single-storey rear extension, the Full Plans fee is approximately £800–£1,200. This covers all inspections from foundation to completion."),
      ("Do building regulations expire?", "Building regulations approval does not expire, but work must start within 3 years of the Full Plans approval date. The completion certificate must be issued within a reasonable time after the work is finished."),
      ("Can I sell a house without a building regulations completion certificate?", "Technically yes, but solicitors and mortgage lenders typically require it. Without a certificate, you may need indemnity insurance, which is cheaper but provides less protection than the certificate itself."),
    ],
    "related": [
      ("labc-vs-approved-inspector.html", "LABC vs Approved Inspector", "Choosing between council and private building control."),
      ("ldc-vs-planning-permission.html", "LDC vs Planning Permission", "Understanding the two main planning compliance routes."),
      ("structural-engineer-vs-architectural-technologist.html", "Structural Engineer vs Architectural Technologist", "Who does what on a building project?"),
    ],
    "cta_h2": "Need <em>building regulations drawings?</em>",
    "cta_p": "Full Plans packages from £1,095. Structural coordination, Part L calculations, and all Approved Document compliance included.",
  },

  {
    "slug": "side-return-vs-wraparound",
    "title": "Side Return vs Wraparound Extension | London Guide 2026",
    "og_title": "Side Return vs Wraparound Extension: Which is Right for Your Property?",
    "desc": "Side return vs wraparound extension comparison — costs, planning routes, space gained, and which suits Victorian and Edwardian terraces in London. Expert guide 2026.",
    "breadcrumb": "Side Return vs Wraparound Extension",
    "eyebrow": "House extensions",
    "h1": "Side Return vs Wraparound Extension: <em>The London Homeowner's Guide</em>",
    "mins": "6",
    "tldrs": [
      "Side return: infills the narrow gap beside a terrace — typically adds 10–18 m²",
      "Wraparound: extends both rear and side simultaneously — adds 20–35 m²",
      "Both need planning permission on semis; may be PD on detached",
      "Side return costs £35,000–£60,000; wraparound costs £55,000–£90,000",
      "Wraparound creates a stronger open-plan flow but reduces garden more",
      "Victorian and Edwardian terraces are the primary candidates for both",
    ],
    "body": """
    <h2 class="reveal">What is a side return extension?</h2>
    <p class="reveal">Victorian and Edwardian terraced houses were built with a narrow gap — typically 600 mm to 1.8 m wide — running alongside the kitchen at the rear. This void was originally used for coal storage, drainage, and access. A side return extension infills this gap, widening the existing ground floor by the width of the return and typically extending it slightly to the rear. The result is a much wider kitchen-diner with improved natural light from the side elevation.</p>

    <h2 class="reveal">What is a wraparound extension?</h2>
    <p class="reveal">A wraparound extension combines a side return infill with a full rear extension, creating an L-shaped addition that runs the full width of the rear and wraps around into the side return. It is the maximum-area ground floor extension option on a terrace — typically adding 20–35 m² of new space. The combined plan allows a large open-plan kitchen, dining area, and living space with dual-aspect glazing to the rear garden and a rooflight over the side return section.</p>

    <h2 class="reveal">Planning: when is permission required?</h2>
    <p class="reveal">Side returns on semi-detached houses almost always need planning permission — extending to the side of a semi is not covered by PD rights when the extension exceeds half the width of the original house. On a detached house, a side extension within PD limits may be possible without permission, but this is uncommon on Victorian stock.</p>
    <p class="reveal">Wraparound extensions, by definition, extend in two directions simultaneously — the side element always triggers the planning requirement on a semi or terrace. A householder planning application covering both the rear and side elements is the standard approach.</p>

    <h2 class="reveal">The key design choices</h2>
    <p class="reveal">The side return section has lower headroom potential than the main rear extension — the neighbouring wall typically limits how high you can build on the boundary. Most architects and architectural technologists design the side return with a glazed or translucent roof (frameless glass or polycarbonate) to bring light in from above without obstructing the neighbour's outlook.</p>
    <p class="reveal">The planning officer's main concern on wraparound extensions is the impact on the street scene from the side elevation and the impact on the neighbouring property from the boundary wall. Setting the boundary wall back from the property boundary by 50–100 mm — and using glazing rather than solid materials — typically addresses both concerns.</p>
    """,
    "verdict": "If your side return is less than 1.2 m wide, a simple side return infill maximises light without major structural cost. If you can extend at least 2–3 m to the rear simultaneously, the wraparound delivers far more usable space for marginal additional cost.",
    "faqs": [
      ("Does a side return extension need planning permission?", "On a terrace or semi, yes — extending to the side is not normally covered by PD. On a detached house, a narrow side extension may be PD if it meets the relevant criteria. A Lawful Development Certificate or planning application is required in most cases."),
      ("How wide can a side return extension be?", "The width is determined by the existing side return gap. Typically 600 mm–1.8 m on Victorian terraces. The extension fills this gap to the boundary, gaining the full width of the return."),
      ("Will a side return extension block my neighbour's light?", "It can. The party wall along the side return typically has windows from the neighbouring kitchen or utility room. A structural engineer's party wall assessment and potentially a party wall award are required. In most cases, the impact is manageable and accepted by neighbours."),
      ("What is the party wall procedure for a side return?", "If your extension is on or within 3 m of the party wall (which a side return typically is), you must serve party wall notices on the adjoining owner under the Party Wall etc. Act 1996. They can consent or appoint a surveyor. Most straightforward side returns are resolved by consent."),
      ("What roof should a side return extension have?", "A frameless glass or polycarbonate roof is standard — it allows daylight into the extension without adding bulk visible from the street. Some designs use a continuation of the main flat roof with a large rooflight over the side section."),
    ],
    "related": [
      ("rear-vs-side-extension.html", "Rear vs Side Extension", "Which direction adds more value on your property type?"),
      ("single-vs-double-storey-extension.html", "Single vs Double Storey Extension", "Going up vs going out — the full comparison."),
      ("flat-vs-pitched-roof-extension.html", "Flat vs Pitched Roof Extension", "What London councils accept and what costs more."),
    ],
    "cta_h2": "Get <em>wraparound or side return drawings</em> from £840",
    "cta_p": "Planning drawings, building regulations, or both. MCIAT-chartered, fixed fee, first-time approval rate of 98%.",
  },

  {
    "slug": "extension-vs-loft-conversion",
    "title": "Extension vs Loft Conversion | Which Adds More Value in London? 2026",
    "og_title": "Extension vs Loft Conversion: Which Adds More Value in London?",
    "desc": "Extension vs loft conversion — comparing added value, build cost, planning complexity, and disruption for London homeowners. Data-driven guide for 2026.",
    "breadcrumb": "Extension vs Loft Conversion",
    "eyebrow": "Home improvements",
    "h1": "Extension vs Loft Conversion: <em>Which Adds More Value in London?</em>",
    "mins": "8",
    "tldrs": [
      "Loft conversions add 15–25% to property value; extensions add 8–20% depending on type",
      "Loft conversions disrupt living space less — work happens above you",
      "Extensions typically cost less per m² to build than loft conversions",
      "Loft conversions often need only PD or LDC; extensions more often need planning permission",
      "Adding a bedroom via loft vs extending kitchen-diner depends on what your home is missing",
      "In London, bedroom count drives value more than ground floor open plan",
    ],
    "body": """
    <h2 class="reveal">Value uplift: the London evidence</h2>
    <p class="reveal">In London's market, bedroom count is the single strongest predictor of sale value. Converting from a 3-bed to a 4-bed via a loft conversion typically adds 15–25% to the property value — in a £700,000 house, that is £105,000–£175,000 of added value for a project costing £50,000–£75,000 to build. The return on investment is consistently strong.</p>
    <p class="reveal">Rear extensions — which typically add a kitchen-diner rather than a bedroom — add 8–15% in most London boroughs. The value is more modest because open-plan ground floor living is already common in the buyer pool, whereas an additional bedroom widens the market to families who need the space.</p>

    <h2 class="reveal">Cost per square metre</h2>
    <p class="reveal">Single-storey extensions typically cost £1,200–£1,800/m² to build in London. Loft conversions cost £1,400–£2,200/m² — they are more expensive per square metre because of the structural complexity (new floor, dormer, staircase) and the access constraints of working at roof level.</p>
    <p class="reveal">However, loft conversions start from a smaller total project cost for the same number of new rooms — a typical loft adding two bedrooms and a bathroom costs £50,000–£70,000, comparable to a medium rear extension adding only additional kitchen space.</p>

    <h2 class="reveal">Planning complexity</h2>
    <p class="reveal">Most loft conversions proceed via permitted development (LDC route) — particularly on terraces in boroughs without extensive Article 4 coverage. Extensions are more likely to need planning permission, particularly on semis (side elements), in conservation areas, or when exceeding PD depth limits.</p>
    <p class="reveal">This planning difference has a practical impact on programme. A loft with an LDC (6–8 weeks) plus building regs (4–6 weeks) can be on site within 12–14 weeks of instruction. An extension needing planning permission adds 8–13 weeks of planning determination before building regs can start.</p>

    <h2 class="reveal">Disruption during construction</h2>
    <p class="reveal">Loft conversions are less disruptive than extensions. The builder works primarily at roof level — new floor joists, dormer, roofing — and the main internal work is the staircase, which takes 1–2 days to install once the structure is ready. You can typically remain in the house throughout, with the main disruption being the staircase installation and final decoration.</p>
    <p class="reveal">Extensions involve opening up the rear of the house, removing the existing rear wall, and installing temporary weatherproofing. In wet weather, this is a genuine disruption to daily life. Most families with young children find loft conversions significantly more liveable during construction.</p>
    """,
    "verdict": "If your house is short on bedrooms, do the loft conversion first — it adds more value per pound spent and is less disruptive. If your house has enough bedrooms but a cramped ground floor, the extension is the right call.",
    "faqs": [
      ("Which adds more value: a loft bedroom or a ground floor extension?", "In London, an additional bedroom (via loft) almost always adds more absolute value than an equivalent cost spent on ground floor space. Bedroom count is the primary driver of asking price in London's market."),
      ("Can I do both a loft conversion and an extension?", "Yes — many London homeowners do both, often starting with the loft (faster, less disruptive) and then the extension. Both can be planned together with a single set of architectural drawings covering the complete scheme."),
      ("Does a loft conversion need building regulations?", "Yes, always. Even a permitted development loft conversion requires full building regulations approval for structure, insulation, fire safety (escape windows on each new bedroom), and staircase. Building regulations are separate from planning permission."),
      ("How long does a loft conversion take?", "Typically 8–12 weeks on site for a rear dormer loft conversion. The programme splits roughly into 3 weeks for structural/dormer work, 2 weeks for first fix (electrics, plumbing), 2 weeks for insulation and plasterboarding, and 3 weeks for second fix and finish."),
      ("What is the minimum headroom for a habitable loft room?", "Building regulations require 2.2 m headroom over at least 50% of the floor area for the space to be classified as a habitable room. The 2.2 m measurement is taken at the finished ceiling level — factor in floor build-up when assessing your existing roof structure."),
    ],
    "related": [
      ("hip-to-gable-vs-rear-dormer.html", "Hip-to-Gable vs Rear Dormer", "Comparing the two main loft conversion types for semis."),
      ("single-vs-double-storey-extension.html", "Single vs Double Storey Extension", "Going up one floor vs two — cost and value guide."),
      ("loft-vs-mansard.html", "Loft Conversion vs Mansard Roof", "Maximum-space upper level options compared."),
    ],
    "cta_h2": "Get <em>loft or extension drawings</em> — from £840",
    "cta_p": "MCIAT-chartered drawings. Fixed fee. 98% first-time approval rate across all 33 London boroughs.",
  },

  {
    "slug": "kitchen-extension-vs-garage-conversion",
    "title": "Kitchen Extension vs Garage Conversion | Which Creates the Best Space? London 2026",
    "og_title": "Kitchen Extension vs Garage Conversion: Cost, Planning & Space Compared",
    "desc": "Kitchen extension vs garage conversion — comparing cost, planning routes, space quality, and resale value for London homeowners. Expert MCIAT guide for 2026.",
    "breadcrumb": "Kitchen Extension vs Garage Conversion",
    "eyebrow": "Home improvements",
    "h1": "Kitchen Extension vs Garage Conversion: <em>Which Creates the Best Space?</em>",
    "mins": "6",
    "tldrs": [
      "Garage conversion costs £20,000–£35,000; kitchen extension costs £45,000–£80,000",
      "Garage conversion is cheaper but creates a less flexible space",
      "Kitchen extensions add more square footage and better natural light",
      "Garage conversions often don't need planning permission",
      "Losing a garage can reduce property value by 3–5% in some outer London boroughs",
      "Both need building regulations approval",
    ],
    "body": """
    <h2 class="reveal">The garage conversion case</h2>
    <p class="reveal">Converting an integral or attached garage to habitable space is one of the cheapest ways to add usable floor area to a house. The structure already exists — you need insulation, a new floor, heating, electrical work, and glazing to replace the garage door. In London, where garages are increasingly rare as parking, most integral garages are already used as storage. Converting them to a playroom, home office, utility room, or bedroom can be done for £20,000–£35,000 including building regulations compliance.</p>
    <p class="reveal">The main limitation is natural light. Garages typically have only a front-facing opening (the door) and sometimes a side window. Converting to habitable space requires either a large front window (which changes the street appearance) or accepting a degree of reliance on rooflights. A new rear-facing window requires structural works to the existing wall.</p>

    <h2 class="reveal">The kitchen extension case</h2>
    <p class="reveal">A rear kitchen extension adds new space to the rear of the existing house, typically enlarging the kitchen into an open-plan kitchen-diner. Natural light comes from rear-facing bifold or sliding doors and roof lanterns or rooflights. The space quality is generally higher than a garage conversion because it is purpose-designed for living, with the best garden aspect.</p>
    <p class="reveal">A kitchen extension costs £45,000–£80,000 in London (2026 prices) — significantly more than a garage conversion. Planning permission is required for most rear extensions on semi-detached properties or where the extension exceeds PD limits.</p>

    <h2 class="reveal">Resale value</h2>
    <p class="reveal">In inner London (zones 1–3), where street parking is scarce and garages are rarely used for cars, a well-executed garage conversion has minimal negative impact on value. In outer London (zones 4–6), where kerb appeal and parking matter more to buyers, losing a visible garage can affect the asking price — though the floor area gained typically offsets this.</p>
    <p class="reveal">A kitchen extension reliably adds value in any London borough — the open-plan kitchen-diner is a standard buyer expectation in the £500,000+ market. Estate agents consistently report that improved kitchen space is one of the top three value-adding works.</p>
    """,
    "verdict": "If cost is the primary constraint and you have an underused garage, convert it — it is the most efficient spend. If you want the highest quality new space and best return on value, a kitchen extension wins.",
    "faqs": [
      ("Does a garage conversion need planning permission?", "Usually not. Converting an integral or attached garage to habitable use is typically permitted development, provided it does not involve extending the building's footprint. A Lawful Development Certificate is advisable to confirm lawfulness."),
      ("Do I need building regulations for a garage conversion?", "Yes. Garage conversions require building regulations approval covering insulation (Part L), structural adequacy of the floor, fire safety, ventilation, and electrical works. A Full Plans submission is recommended."),
      ("Can I convert a detached garage?", "Yes, but planning permission may be required if the conversion involves changing its use to a separate dwelling. Converting a detached garage to a home office or studio (ancillary to the main house) is typically permitted development."),
      ("Will converting my garage reduce my home's value?", "In most London boroughs, no — the floor area gained outweighs the loss of parking. In outer boroughs with limited street parking (e.g. Havering, Bromley, Sutton), check local comparables before proceeding."),
      ("How long does a garage conversion take?", "Typically 6–10 weeks from building regulations approval to completion. The programme is shorter than a full extension because the structure is already in place."),
    ],
    "related": [
      ("extension-vs-loft-conversion.html", "Extension vs Loft Conversion", "Which adds more value in London — the full comparison."),
      ("single-vs-double-storey-extension.html", "Single vs Double Storey Extension", "Going up vs going further back."),
      ("outbuilding-vs-extension.html", "Outbuilding vs Extension", "For home offices and extra space — which is better?"),
    ],
    "cta_h2": "Need <em>drawings for a garage conversion or extension?</em>",
    "cta_p": "Building regulations drawings from £1,095. Planning drawings from £840. Fixed fee, MCIAT-chartered.",
  },

  {
    "slug": "outbuilding-vs-extension",
    "title": "Outbuilding vs Extension | Home Office & Studio Options for London Homeowners",
    "og_title": "Outbuilding vs Extension: Which is Better for a Home Office or Studio?",
    "desc": "Outbuilding vs extension for a home office or studio — planning, cost, insulation, and which works better for remote working in London. 2026 expert guide.",
    "breadcrumb": "Outbuilding vs Extension",
    "eyebrow": "Home improvements",
    "h1": "Outbuilding vs Extension: <em>Which is Better for a Home Office or Studio?</em>",
    "mins": "6",
    "tldrs": [
      "Outbuildings under 2.5 m eaves height don't need planning permission in most gardens",
      "Outbuildings cost £15,000–£40,000; an equivalent extension costs £45,000–£80,000",
      "Outbuildings cannot be used as separate dwellings without planning permission",
      "A well-insulated outbuilding can be as comfortable as an extension for year-round work",
      "Extensions add permanent floor area that counts toward the property value",
      "Outbuildings don't need building regulations for structures under 15 m² (some caveats apply)",
    ],
    "body": """
    <h2 class="reveal">When an outbuilding works</h2>
    <p class="reveal">A garden outbuilding — studio, home office, or workshop — is the fastest and cheapest way to create a separate work space without altering the main house. Under permitted development, an outbuilding with eaves no higher than 2.5 m and a maximum ridge height of 4 m (3 m if within 2 m of a boundary) does not require planning permission on most residential properties. An outbuilding under 15 m² footprint and not used as a dwelling also does not require building regulations, though good insulation and a stable electrical connection should still be designed in.</p>
    <p class="reveal">The practical limitation of outbuildings is the separation from the house. In London winters, walking 20 m across a wet garden to reach a cold outbuilding each morning is a genuine friction point. A well-insulated timber-frame outbuilding with underfloor heating and fibre broadband resolves most of this — but it is a different experience from stepping out of the kitchen into an extension.</p>

    <h2 class="reveal">When an extension works better</h2>
    <p class="reveal">If you want the new workspace to be directly connected to the main house — accessible from the kitchen or hallway without going outside — an extension is the only option. An extension also adds permanent floor area that is classified as habitable space, which counts toward the property's overall floor area measurement and increases value. An outbuilding, even a high-quality one, is not classified as habitable floor area and does not add to the measured floor area of the house.</p>
    <p class="reveal">The extension is more expensive and disruptive to build, but the quality of connection to the rest of the house is categorically different. If you plan to sell in the next 5 years, an extension adds more to the sale value than an outbuilding of equivalent construction cost.</p>

    <h2 class="reveal">Planning in practice</h2>
    <p class="reveal">Most outbuildings in London gardens proceed without planning permission provided they comply with PD limits. The main restrictions are: not in front of the principal elevation, not covering more than 50% of the garden area, and eaves below 2.5 m. In conservation areas, permitted development rights for outbuildings are more restricted — check with the council before proceeding.</p>
    """,
    "verdict": "For a home office used primarily for focused work, a quality outbuilding is the faster, cheaper option. For a space you will use all day, every day, in all weather, and which you want to add to your property's value, extend the house.",
    "faqs": [
      ("Can I sleep in a garden outbuilding?", "An outbuilding can be used for occasional sleeping (e.g. as a guest room) without changing its planning use class. Permanent use as a bedroom or self-contained dwelling requires planning permission."),
      ("Does an outbuilding need building regulations?", "Outbuildings under 15 m² with no sleeping accommodation and not close to a boundary do not require building regulations. Larger structures do. Regardless, proper insulation, damp-proofing, and electrical installation to BS 7671 are strongly recommended."),
      ("How much does a quality garden office cost?", "A timber-frame garden office with insulation, electrics, double glazing, and cladding costs £15,000–£40,000 in London (2026), depending on size and specification. Higher-end units with underfloor heating and acoustic insulation reach £40,000–£60,000."),
      ("Will an outbuilding add value to my house?", "A well-built outbuilding adds modest value — buyers appreciate the space. However, it does not add to the measured floor area of the house, so it does not affect the £/m² valuation the same way an extension does."),
      ("Can I have broadband and heating in an outbuilding?", "Yes. Running power to an outbuilding requires a registered electrician and, for a permanent structure, an armoured cable from the consumer unit. Fibre broadband can be run on the same external route. Underfloor heating (electric) is common in outbuildings."),
    ],
    "related": [
      ("kitchen-extension-vs-garage-conversion.html", "Kitchen Extension vs Garage Conversion", "Comparing two popular ways to add ground-floor space."),
      ("extension-vs-loft-conversion.html", "Extension vs Loft Conversion", "Which adds more value in London?"),
      ("garden-room-planning-london.html", "Garden Room Planning Permission London", "When you do and don't need planning permission for a garden building."),
    ],
    "cta_h2": "Need <em>drawings for an outbuilding or extension?</em>",
    "cta_p": "MCIAT-chartered architectural drawings. Fixed fees. We advise on the planning route before you commit.",
  },

  {
    "slug": "pre-app-vs-direct-application",
    "title": "Pre-Application Advice vs Going Direct | Is Pre-App Worth the Cost in London?",
    "og_title": "Pre-Application Advice vs Direct Planning Application: Is Pre-App Worth It?",
    "desc": "Pre-application advice vs going direct — when London pre-app adds value, when it wastes time and money, and how to decide for your specific project. MCIAT guide 2026.",
    "breadcrumb": "Pre-App vs Direct Application",
    "eyebrow": "Planning guidance",
    "h1": "Pre-Application Advice vs Going Direct: <em>Is Pre-App Worth the Cost in London?</em>",
    "mins": "6",
    "tldrs": [
      "Pre-app costs £50–£800 in London depending on council and project type",
      "Pre-app is not binding — councils can change their view at application stage",
      "Pre-app adds 6–12 weeks to total project timeline",
      "Recommended for: conservation area works, large extensions, basement conversions",
      "Not recommended for: standard loft conversions, PD extensions, simple householder works",
      "Good pre-app feedback reduces the risk of refusal but does not eliminate it",
    ],
    "body": """
    <h2 class="reveal">What is pre-application advice?</h2>
    <p class="reveal">Pre-application advice (pre-app) is a formal paid consultation with the local planning authority before submitting a planning application. You submit a description of the proposed works (and usually outline drawings or photos), pay a fee, and receive a written response from a planning officer assessing the proposal against local planning policy. The response typically indicates whether the council is likely to support, object to, or require amendments to the scheme.</p>
    <p class="reveal">Pre-app is entirely optional. There is no legal requirement to seek pre-app advice before submitting a planning application. But for complex or sensitive projects, it can prevent expensive failures.</p>

    <h2 class="reveal">When pre-app is worth the cost</h2>
    <p class="reveal"><strong>Conservation area works:</strong> If your proposed mansard, extension, or loft conversion is in a conservation area and you are uncertain whether the design is acceptable, pre-app can clarify the officer's position before you invest in full drawings. Camden, Islington, and Westminster conservation area officers are often willing to give substantive pre-app responses that meaningfully shape the design.</p>
    <p class="reveal"><strong>Basement conversions:</strong> London basement policy is complex and variable by borough. Pre-app is almost always advisable for basement conversions — especially in boroughs like Kensington & Chelsea and Westminster where basement SPDs impose strict conditions.</p>
    <p class="reveal"><strong>Large residential developments:</strong> Where a project involves multiple units, change of use, or commercial elements, pre-app is standard practice.</p>

    <h2 class="reveal">When to skip pre-app and go direct</h2>
    <p class="reveal">For standard householder applications — loft conversions, single or double storey rear extensions, side returns — experienced architectural technologists can assess planning likelihood from published policy without needing a formal pre-app response. A well-prepared application that addresses the council's residential design guidance and SPDs has a high probability of success without pre-app.</p>
    <p class="reveal">Our <a href="../projects/">case studies</a> show that 98% of our applications are approved on the first attempt, with no pre-app advice on any of them. Thorough upfront design work — addressing likely officer concerns in the drawings and supporting documents — is a more efficient route than a separate pre-app consultation.</p>
    """,
    "verdict": "Skip pre-app for standard householder works — a well-prepared application from experienced technologists achieves the same outcome faster and cheaper. Commission pre-app for conservation area works, basement conversions, or any project where borough-specific policy creates genuine uncertainty.",
    "faqs": [
      ("Is pre-application advice binding on the planning authority?", "No. Pre-app advice is the officer's opinion at that point in time. The formal application is decided independently, and the officer's final view can differ from the pre-app response — especially if material considerations change."),
      ("How much does pre-application advice cost in London?", "Council fees vary widely. Westminster charges £400–£800 for householder pre-app. Camden charges £200–£600. Many outer boroughs charge £50–£200. Some councils offer free pre-app for simple householder works."),
      ("How long does pre-application advice take?", "Most London councils target 4–6 weeks for a written pre-app response, but some take 8–12 weeks. This adds to the overall project programme before the formal application is even submitted."),
      ("Can I submit a planning application without pre-app?", "Yes, always. Pre-app is voluntary. Many straightforward applications succeed without any pre-app consultation."),
      ("Does pre-app advice reduce planning fees?", "No. The pre-app fee is additional to the standard planning application fee. You pay both if you seek pre-app advice and then submit a formal application."),
    ],
    "related": [
      ("planning-agent-vs-diy.html", "Planning Agent vs DIY Application", "When to hire a professional vs handle your own application."),
      ("ldc-vs-planning-permission.html", "LDC vs Planning Permission", "Understanding which route your project needs."),
      ("conservation-area-planning-london.html", "Conservation Area Planning London", "How to navigate London's most complex planning environments."),
    ],
    "cta_h2": "Want a <em>free assessment</em> before committing to pre-app?",
    "cta_p": "We assess planning likelihood from published policy at no charge as part of your quote. Fixed fees from £840.",
  },

  {
    "slug": "mansard-vs-hip-to-gable",
    "title": "Mansard vs Hip-to-Gable Loft Conversion | London Planning & Cost Guide 2026",
    "og_title": "Mansard vs Hip-to-Gable Loft Conversion: Full Comparison",
    "desc": "Mansard vs hip-to-gable loft conversion — which suits your property, which planning route applies, cost comparison, and space gained. Expert guide for London homeowners 2026.",
    "breadcrumb": "Mansard vs Hip-to-Gable",
    "eyebrow": "Loft conversions",
    "h1": "Mansard vs Hip-to-Gable: <em>Which Loft Conversion Suits Your Property?</em>",
    "mins": "7",
    "tldrs": [
      "Mansards suit terraces and can be visible from the street — always need planning permission",
      "Hip-to-gable suits semis and detached houses only — often permitted development",
      "Mansards create more volume but cost 40–60% more than a hip-to-gable plus dormer",
      "Both create a full floor at loft level with vertical walls",
      "Mansard SPDs exist in Hammersmith, Richmond, and several conservation-area-heavy boroughs",
      "Hip-to-gable plus rear dormer (L-shape) is cheaper than full mansard on a semi",
    ],
    "body": """
    <h2 class="reveal">What is a mansard conversion?</h2>
    <p class="reveal">A mansard is a roof form with steep front and rear slopes (typically 70–72 degrees) and a nearly flat top. A mansard loft conversion rebuilds the entire roof structure in this form, creating a full additional storey at roof level with near-vertical walls on all four sides. On a London terrace, the mansard wraps around the front, rear, and both party walls — creating the maximum possible volume from a roof conversion. The front mansard slope is typically clad in zinc or lead and is visible from the street.</p>
    <p class="reveal">Mansards always require full planning permission — they alter the primary roof structure significantly and are visible from the street. Several London boroughs (Hammersmith & Fulham, Richmond, Westminster) have Supplementary Planning Documents specifically governing mansard design.</p>

    <h2 class="reveal">What is a hip-to-gable conversion?</h2>
    <p class="reveal">A hip-to-gable conversion applies to semi-detached and detached houses with hipped roofs. It infills the sloping hip at the end of the roof, creating a vertical gable, and is almost always combined with a full-width rear dormer to create the maximum loft space. The combined form (L-shape) creates two bedrooms and a bathroom at loft level on a typical 1930s semi.</p>
    <p class="reveal">Hip-to-gable conversions on semis and detached houses can usually proceed via permitted development — a Lawful Development Certificate rather than planning permission. The hipped end of the roof is not visible from the street in most cases, so the impact on the street scene is minimal.</p>

    <h2 class="reveal">Cost comparison</h2>
    <p class="reveal">A hip-to-gable plus rear dormer on a semi costs £45,000–£75,000 to build. A full mansard conversion on a terrace costs £70,000–£120,000 — the additional cost reflects the full roof rebuild, the front mansard slope structure and cladding, and the more complex planning and party wall process. The space created is comparable, but the mansard creates a slightly squarer floor plan on all four sides.</p>

    <h2 class="reveal">Which is right for your property?</h2>
    <p class="reveal">The choice is largely determined by property type. If you have a semi-detached or detached house with a hipped roof, hip-to-gable is the natural and cost-effective approach. If you have a terraced house, hip-to-gable is structurally impossible (terraces have gable ends, not hips) — your options are a rear dormer or a full mansard. A rear dormer is cheaper; a mansard creates more volume and a better-proportioned floor plan.</p>
    """,
    "verdict": "On a semi or detached: hip-to-gable plus rear dormer (L-shape) — cheaper, often PD, comparable result. On a terrace where maximum space is the priority: mansard — more expensive and always needs planning, but creates a complete additional storey.",
    "faqs": [
      ("Can a terraced house have a hip-to-gable conversion?", "No. Terraced houses have gable ends (vertical end walls), not hipped roofs. The hip-to-gable technique requires a hipped end to infill. Terraces use rear dormers or full mansard conversions instead."),
      ("Does a mansard always need planning permission?", "Yes. Mansard conversions alter the primary roof structure and are visible from the street — they always require a householder or full planning application. There is no PD route for a mansard."),
      ("Which adds more property value — mansard or hip-to-gable?", "In absolute terms, a mansard on a terrace typically adds more value because it creates a larger floor area. But the hip-to-gable on a semi delivers a better return on investment because it costs significantly less to build for a comparable result."),
      ("What is a mansard SPD?", "A Supplementary Planning Document (SPD) is additional planning guidance produced by a council to explain how they interpret planning policy for a specific type of development. Mansard SPDs specify slope angles, parapet heights, setbacks, and materials requirements that go beyond the standard residential design guide."),
      ("How long does a mansard conversion take?", "A full mansard conversion typically takes 14–20 weeks on site. This is longer than a rear dormer (8–12 weeks) because the entire roof structure is being rebuilt. The planning process also typically adds 12–16 weeks before work can start."),
    ],
    "related": [
      ("loft-vs-mansard.html", "Loft Conversion vs Mansard Roof", "The full loft type comparison for London terraces."),
      ("hip-to-gable-vs-rear-dormer.html", "Hip-to-Gable vs Rear Dormer", "Choosing between the two main loft types for semis."),
      ("mansard-hammersmith.html", "Mansard Case Study — Hammersmith W12", "Real-world example: conservation area mansard approved first time."),
    ],
    "cta_h2": "Get <em>mansard or loft conversion drawings</em> — from £1,225",
    "cta_p": "MCIAT-chartered drawings. Fixed fee. We have delivered mansards in every London conservation area borough.",
  },

  {
    "slug": "online-vs-local-architect",
    "title": "Online Architect vs Local Architect | Fixed Fee vs Traditional for London Projects",
    "og_title": "Online/Fixed-Fee Architect vs Local Architect: Which is Better for London?",
    "desc": "Online fixed-fee drawing service vs local architect — cost, quality, planning success rates, and when each option is right for London homeowners. Honest 2026 comparison.",
    "breadcrumb": "Online vs Local Architect",
    "eyebrow": "Choosing a service",
    "h1": "Online Fixed-Fee vs Local Architect: <em>What the Cost Difference Actually Buys You</em>",
    "mins": "7",
    "tldrs": [
      "Traditional architects charge 8–15% of build cost; fixed-fee services charge a flat rate",
      "For a £80,000 extension: traditional architect = £6,400–£12,000; fixed-fee = £840–£1,750",
      "Planning success rates are comparable — the drawings quality is what matters, not the fee model",
      "Traditional architects offer design flair for complex or listed building projects",
      "Fixed-fee services are optimal for defined scope: loft, extension, building regs",
      "MCIAT chartered qualifications are equivalent to RIBA for residential work",
    ],
    "body": """
    <h2 class="reveal">What you actually pay</h2>
    <p class="reveal">Traditional architects in London typically charge 8–15% of the estimated build cost for a full service (concept through to construction monitoring). For a £80,000 rear extension, that is £6,400–£12,000 in professional fees. For a £60,000 loft conversion, £4,800–£9,000. These fees are for a full service that includes concept design, planning, building regulations, and periodic site visits during construction.</p>
    <p class="reveal">Fixed-fee drawing services charge a flat rate for a defined scope — typically planning drawings, building regulations drawings, or both. For the same rear extension, a fixed-fee planning drawings package costs £840–£1,095. Building regulations drawings cost an additional £1,095. Total professional fees: £1,935–£2,190 vs £6,400–£12,000 for the traditional route.</p>

    <h2 class="reveal">What the difference pays for</h2>
    <p class="reveal">The traditional fee pays for: an architect's creative input into the design concept, more frequent site visits during construction, a named individual who manages the contractor relationship, and the reassurance of the RIBA brand. For complex projects — listed buildings, unusual sites, architect-designed bespoke homes — this creative input and site presence is genuinely valuable.</p>
    <p class="reveal">For defined-scope residential works — a rear dormer, a rear extension, building regulations drawings for an approved scheme — the planning and building control drawings need to be technically correct and presented in the format the council requires. The creative design is typically constrained by planning policy and PD limits. In this context, the quality of the technical drawings matters more than the conceptual design process.</p>

    <h2 class="reveal">Planning success rates</h2>
    <p class="reveal">Planning applications are decided on their policy compliance, not on the fee model of the professional who prepared them. Planning officers assess: does the proposal comply with the NPPF, the London Plan, the borough's local plan, and any relevant SPDs? A technically compliant application prepared by a fixed-fee MCIAT-chartered service has the same approval probability as one prepared by a traditional architect at three times the cost.</p>
    <p class="reveal">Our 98% first-time approval rate across all 33 London boroughs demonstrates this. The drawings and supporting documents matter; the billing model of the professional does not.</p>

    <h2 class="reveal">When to choose a traditional architect</h2>
    <p class="reveal">Commission a traditional architect when: the project involves significant creative design decisions (new build, listed building, unique site), you want ongoing site visits and contractor management, or the project is sufficiently complex that you need a single professional managing the whole process. The additional fee is justified by the value of that design and management input.</p>
    """,
    "verdict": "For loft conversions, rear extensions, mansards, and building regulations drawings, a fixed-fee MCIAT-chartered service delivers the same planning outcome at 20–30% of the cost. Hire a traditional architect for complex design projects where creative input and full-service management are the product.",
    "faqs": [
      ("Is an architectural technologist as qualified as an architect?", "MCIAT-chartered architectural technologists hold professional qualifications equivalent to RIBA-chartered architects for residential and technical design work. Both require degree-level study, professional experience, and ongoing CPD. ARB registration (required to call yourself an 'architect') is the only functional distinction for residential design."),
      ("Can a fixed-fee service do listed building work?", "Listed building consent and listed building design require specialist historic building knowledge. Most fixed-fee services handle standard residential work. If your property is listed, ask specifically whether the practice has listed building experience before instructing."),
      ("What is the difference between MCIAT and RIBA?", "MCIAT is membership of the Chartered Institute of Architectural Technologists. RIBA is membership of the Royal Institute of British Architects. Both are professional bodies with rigorous qualification and CPD requirements. For residential design and planning drawings, both qualifications indicate equivalent professional competence."),
      ("Do online drawing services visit the property?", "It varies by service. At Architectural Drawings London, we conduct a measured survey of the property before preparing drawings — the survey is the foundation of accurate existing drawings from which all proposed work is drawn."),
      ("What happens if my planning application is refused?", "Most fixed-fee services include an amendment service if refusal is due to matters within the drawings. At Architectural Drawings London, we handle planning queries and pre-decision negotiations as part of the service."),
    ],
    "related": [
      ("drawing-service-vs-architect.html", "Drawing Service vs Architect", "When a drawing service is the right choice."),
      ("architect-fees-vs-fixed-fee.html", "Architect Fees vs Fixed Fee", "Full cost comparison across project types."),
      ("planning-agent-vs-diy.html", "Planning Agent vs DIY Application", "The case for and against submitting your own application."),
    ],
    "cta_h2": "MCIAT-chartered drawings. <em>Fixed fee. No surprises.</em>",
    "cta_p": "Planning drawings from £840. Building regulations from £1,095. 98% first-time approval rate across all 33 London boroughs.",
  },

  {
    "slug": "structural-engineer-vs-architectural-technologist",
    "title": "Structural Engineer vs Architectural Technologist | Who Does What on Your Project?",
    "og_title": "Structural Engineer vs Architectural Technologist: Roles on a Building Project",
    "desc": "Structural engineer vs architectural technologist — roles, qualifications, when you need each, and how they work together on London residential projects. Expert guide 2026.",
    "breadcrumb": "Structural Engineer vs Architectural Technologist",
    "eyebrow": "Professional roles",
    "h1": "Structural Engineer vs Architectural Technologist: <em>Who Does What on Your Project?</em>",
    "mins": "6",
    "tldrs": [
      "Architectural technologist: design, planning drawings, building regulations drawings",
      "Structural engineer: foundation design, beam sizing, structural calculations",
      "Most extensions and loft conversions need both — they work in parallel",
      "The architectural technologist typically coordinates the structural engineer's input",
      "Structural engineer fees: £500–£2,000 for residential projects",
      "Building control requires structural calculations — this is the engineer's primary deliverable",
    ],
    "body": """
    <h2 class="reveal">What an architectural technologist does</h2>
    <p class="reveal">An architectural technologist produces the design drawings and documentation for planning permission and building regulations approval. This includes: measured survey drawings, existing and proposed floor plans, elevations, sections, roof plans, a site location plan, a Design and Access Statement (where required), and all the technical drawings showing construction details for building regulations compliance. They are the project's primary professional and typically coordinate other consultants.</p>

    <h2 class="reveal">What a structural engineer does</h2>
    <p class="reveal">A structural engineer designs the load-bearing elements of the proposed works — foundations, beams, columns, floor structures, and roof structures. For a rear extension, the engineer calculates the pad foundation sizes, designs the steel or timber beam spanning the new opening, and specifies the new floor joist scheme. For a loft conversion, the engineer designs the new loft floor structure, the ridge beam, and the structural supports for the dormer.</p>
    <p class="reveal">Structural calculations are required by building control as part of the Part A (Structure) compliance review. Without an engineer's calculations, the building control officer cannot approve the structural elements of the works.</p>

    <h2 class="reveal">How they work together</h2>
    <p class="reveal">On a typical residential project, the architectural technologist produces the initial design drawings (which are used for planning if needed). Once planning is approved (or the LDC granted), the engineer designs the structural scheme based on the architectural drawings. The technologist then incorporates the engineer's structural details into the building regulations package — showing how the beam sits in the structure, how foundations are specified, and how structural elements relate to the architectural design.</p>
    <p class="reveal">Our <a href="../services/building-regulations.html">building regulations packages</a> are produced in coordination with structural engineers. We manage the relationship and ensure the engineer's calculations are incorporated correctly — you deal with one professional rather than two.</p>

    <h2 class="reveal">Do you always need both?</h2>
    <p class="reveal">For simple, non-structural works (redecorations, non-structural internal alterations), you need neither. For extensions and loft conversions — which always involve structural changes — you need both, but the architectural technologist coordinates the engineer and you typically only communicate directly with one practice.</p>
    """,
    "verdict": "For any project involving new openings, extensions, or loft conversions, you need both. Commission the architectural technologist first — they design the scheme and manage the structural engineer's brief. You should not need to manage the engineer directly.",
    "faqs": [
      ("Can a structural engineer produce planning drawings?", "Structural engineers are not trained in planning policy, design, or the production of planning application drawings. They produce structural calculations and structural drawings only. Planning drawings require an architectural technologist or architect."),
      ("Do I need to find my own structural engineer?", "At Architectural Drawings London, we coordinate the structural engineer on your behalf as part of our building regulations package. You do not need to source or brief an engineer separately."),
      ("What qualifications should a structural engineer have?", "Look for CEng (Chartered Engineer) status and membership of the Institution of Structural Engineers (MIStructE) or Institute of Civil Engineers (MICE). Both require degree-level study and several years of professional experience."),
      ("How much does a structural engineer cost for an extension?", "Structural engineer fees for a single-storey rear extension typically range from £500–£1,200. A more complex project (basement, two-storey extension, steel frame) costs £1,500–£3,000. The fee is for calculations and structural drawings only."),
      ("Can the building control officer request structural calculations without a structural engineer?", "No. Building control officers assess whether the submitted calculations comply with Approved Document A — they do not produce calculations themselves. If no calculations are submitted, the BCO cannot approve the structural elements."),
    ],
    "related": [
      ("building-notice-vs-full-plans.html", "Building Notice vs Full Plans", "Which building regulations route is right for your project?"),
      ("labc-vs-approved-inspector.html", "LABC vs Approved Inspector", "Choosing between council and private building control."),
      ("architect-vs-architectural-technologist.html", "Architect vs Architectural Technologist", "Qualifications, roles, and when each is the right choice."),
    ],
    "cta_h2": "Need <em>building regulations drawings with structural coordination?</em>",
    "cta_p": "Our building regulations packages include structural engineer coordination. From £1,095, MCIAT-chartered.",
  },

  {
    "slug": "velux-vs-dormer-vs-hip-gable",
    "title": "Velux vs Dormer vs Hip-to-Gable Loft Conversion | Full Comparison 2026",
    "og_title": "Velux vs Dormer vs Hip-to-Gable Loft Conversion: Which is Right for You?",
    "desc": "Velux vs dormer vs hip-to-gable loft conversion — three-way comparison of cost, space, planning, and which suits which property type in London. Complete guide 2026.",
    "breadcrumb": "Velux vs Dormer vs Hip-to-Gable",
    "eyebrow": "Loft conversions",
    "h1": "Velux vs Dormer vs Hip-to-Gable: <em>The Three Loft Conversion Types Compared</em>",
    "mins": "8",
    "tldrs": [
      "Velux (rooflight) conversion: cheapest — £15,000–£25,000 but limited headroom",
      "Rear dormer: most common — £35,000–£55,000, works on terraces and semis",
      "Hip-to-gable + dormer: largest space — £45,000–£75,000, semis and detached only",
      "Velux conversions often need no planning permission; dormers may or may not",
      "Headroom is the key constraint for Velux; volume limits for dormers",
      "All three need building regulations approval",
    ],
    "body": """
    <h2 class="reveal">Velux (rooflight) loft conversion</h2>
    <p class="reveal">A Velux or rooflight conversion uses the existing roof structure without adding any external extensions — it installs rooflights into the existing roof slope and converts the existing loft space into a habitable room. This is the simplest and cheapest loft conversion type, costing £15,000–£25,000 to convert an existing loft.</p>
    <p class="reveal">The fundamental limitation is headroom. The usable floor area with 2.2 m headroom (the Building Regulations minimum for a habitable room) is determined entirely by the existing roof pitch and ridge height. On a steep Victorian roof (45+ degrees), a Velux conversion can be very effective. On a shallow 1960s roof (25–30 degrees), the 2.2 m zone may be too narrow for practical use.</p>
    <p class="reveal">Planning: rooflight conversions that do not alter the existing roof profile are generally permitted development. They are the most planning-friendly loft option.</p>

    <h2 class="reveal">Rear dormer conversion</h2>
    <p class="reveal">A rear dormer is the standard London loft conversion — a vertical box-shaped extension built out from the rear slope of the roof. It creates new vertical wall space at the rear, dramatically increasing the usable floor area regardless of the original roof pitch. A full-width rear dormer on a Victorian terrace typically creates a loft floor of 30–45 m² with 2.4–2.7 m headroom throughout.</p>
    <p class="reveal">Rear dormers cost £35,000–£55,000 to build and are permitted development in most London properties not in Article 4 areas. They are the optimal balance of cost, planning simplicity, and usable space for terraced houses.</p>

    <h2 class="reveal">Hip-to-gable plus rear dormer (L-shape)</h2>
    <p class="reveal">The L-shape combines hip-to-gable (infilling the hipped end on a semi or detached) with a full-width rear dormer. This creates the maximum loft floor area from a single project — typically 35–50 m² on a 1930s semi. Two bedrooms and a bathroom is the standard output.</p>
    <p class="reveal">The L-shape costs £45,000–£75,000 and can be permitted development on properties meeting the 50 m³ volume limit. It is the standard choice for semi-detached homeowners wanting maximum loft space.</p>

    <h2 class="reveal">Decision guide by property type</h2>
    <p class="reveal"><strong>Detached or semi:</strong> If your loft already has good headroom, Velux is cheapest. If not, go L-shape — the extra cost delivers significantly more usable space.<br/><strong>Victorian/Edwardian terrace:</strong> Full-width rear dormer — standard choice, best value.<br/><strong>Conservation area, inner London:</strong> Check Article 4 status. If PD rights are removed, you need planning permission for any dormer — budget accordingly.</p>
    """,
    "verdict": "Velux if headroom exists and budget is tight. Rear dormer for terraces — the right balance of cost and space. L-shape (hip-to-gable plus dormer) for semis wanting maximum space.",
    "faqs": [
      ("Which loft conversion is cheapest?", "A Velux (rooflight) conversion is cheapest at £15,000–£25,000. It uses the existing roof structure and requires no external structural additions. However, usable space is limited by the existing roof pitch."),
      ("Do all loft conversions need planning permission?", "No. Velux conversions typically don't (they don't alter the external roof profile). Rear dormers and hip-to-gable conversions are often permitted development, but require a Lawful Development Certificate if you want documentary evidence of lawfulness."),
      ("What is the minimum roof pitch for a Velux conversion?", "A usable Velux conversion typically requires a roof pitch of at least 40 degrees to achieve the minimum 2.2 m headroom over an adequate floor area. Below 35 degrees, the usable zone is often too narrow for a habitable bedroom."),
      ("How long does a loft conversion take?", "Velux conversion: 4–6 weeks. Rear dormer: 8–12 weeks. L-shape (hip-to-gable plus dormer): 10–14 weeks. These are on-site build times after drawings and approvals are in place."),
      ("Can I have a Velux and a dormer?", "Yes. Some loft conversions combine a rear dormer for main headroom with additional Velux rooflights on the front slope for natural light. This is a common design on Victorian terraces where front-facing rooflights are acceptable under planning policy."),
    ],
    "related": [
      ("hip-to-gable-vs-rear-dormer.html", "Hip-to-Gable vs Rear Dormer", "Detailed comparison of the two structural loft types for semis."),
      ("dormer-vs-velux-loft.html", "Dormer vs Velux Loft", "Two-way comparison for terraced house owners."),
      ("mansard-vs-hip-to-gable.html", "Mansard vs Hip-to-Gable", "Maximum-space options for terraces vs semis."),
    ],
    "cta_h2": "Get <em>loft conversion drawings</em> from £1,225",
    "cta_p": "MCIAT-chartered drawings for all loft types. Fixed fee. Permitted development assessment included.",
  },

  {
    "slug": "householder-vs-full-planning",
    "title": "Householder Planning vs Full Planning Application | What's the Difference?",
    "og_title": "Householder vs Full Planning Application: Key Differences Explained",
    "desc": "Householder planning application vs full planning permission — when each applies, fees, timescales, and what types of residential work require which route. London guide 2026.",
    "breadcrumb": "Householder vs Full Planning",
    "eyebrow": "Planning guidance",
    "h1": "Householder vs Full Planning Application: <em>Which Does Your Project Need?</em>",
    "mins": "5",
    "tldrs": [
      "Householder: for extensions, loft conversions, and alterations to an existing dwelling",
      "Full planning: for new dwellings, change of use, or commercial development",
      "Householder fee: £258 (2026); full planning fee: higher, based on floor area or units",
      "Both have an 8-week statutory determination period (often longer in practice)",
      "Householder applications cannot be used for works that create a new dwelling",
      "Planning appeals for householder refusals are decided by written representations",
    ],
    "body": """
    <h2 class="reveal">What is a householder planning application?</h2>
    <p class="reveal">A householder application is the planning route for works to an existing dwelling — where you live, or a residential property you own. It covers: rear extensions, side extensions, loft conversions, dormer windows, porches, outbuildings, boundary walls, and other alterations. It is the most common planning application type in London and has a flat fee of £258 (from December 2023 rates in England).</p>
    <p class="reveal">Crucially, a householder application can only be used for works to an existing dwelling that do not create additional dwellings. If your project involves converting a house into two flats, adding a self-contained annexe, or building a new house in the garden, a householder application does not apply.</p>

    <h2 class="reveal">What is a full planning application?</h2>
    <p class="reveal">A full planning application covers all development that does not fit the householder route — new dwellings, change of use, commercial development, flats, HMOs, and basement conversions where the use changes. The fee is calculated based on floor area, number of dwellings, or other metrics depending on the development type. For a single new dwelling, the fee is £578 (2026); for multiple dwellings, it scales per unit.</p>
    <p class="reveal">Full planning applications involve a more extensive public consultation process — surrounding residents are notified, planning officers may recommend referral to planning committee for contentious applications, and the process is generally more complex and slower than householder applications.</p>

    <h2 class="reveal">Common borderline cases</h2>
    <p class="reveal"><strong>Basement conversion:</strong> Converting a basement to a living space within a single dwelling — householder. Converting a basement to a separate flat — full planning.<br/><strong>Garage conversion:</strong> Converting a garage to a habitable room within the same dwelling — usually PD or householder. Converting to a self-contained annexe — may require full planning depending on independence.<br/><strong>Loft with separate entrance:</strong> Adding a loft room accessible only from the main house — householder. Adding a loft flat with its own entrance and facilities — full planning for change of use.</p>
    """,
    "verdict": "If you are extending or altering your existing house without creating a new separate dwelling, a householder application is the route. If you are creating new dwellings, converting commercial space, or making any change of use, you need a full planning application.",
    "faqs": [
      ("Can I convert my house into flats with a householder application?", "No. Converting a house into two or more flats is a change of use (Class C3 to C3 HMO or additional dwelling) and requires a full planning application."),
      ("Is the householder fee the same across all London boroughs?", "Planning application fees are set nationally by the government, not by individual councils. The householder fee is £258 across all English planning authorities as of 2026."),
      ("What is the difference between householder and outline planning?", "Outline planning establishes the principle of development for a new dwelling or development before detailed design is finalised. It is not used for works to existing dwellings. Householder applications are always for detailed proposals on an existing house."),
      ("Can I appeal a householder planning refusal?", "Yes. Householder planning appeals are decided by the Planning Inspectorate via written representations — you submit your case in writing, the council submits their response, and an inspector decides. The appeal fee is free for householder appeals."),
      ("What documents are needed for a householder application?", "Completed application form, existing and proposed drawings (floor plans, elevations), site location plan, Design and Access Statement (for conservation areas or significant extensions), and the application fee. Our planning drawings packages include all required documents."),
    ],
    "related": [
      ("ldc-vs-planning-permission.html", "LDC vs Planning Permission", "When you need a certificate vs a planning application."),
      ("full-planning-vs-prior-approval.html", "Full Planning vs Prior Approval", "When prior approval is a faster alternative."),
      ("planning-permission-refused-what-next.html", "Planning Refused — What Next?", "Options after a planning refusal, including appeal rights."),
    ],
    "cta_h2": "Need <em>drawings for a householder application?</em>",
    "cta_p": "Planning drawings from £840 including all required documents. MCIAT-chartered, 98% first-time approval rate.",
  },

]


def main() -> None:
    created = 0
    skipped = 0
    sitemap_urls = []

    for p in POSTS:
        path = os.path.join(BLOG_DIR, f"{p['slug']}.html")
        if os.path.exists(path):
            skipped += 1
            print(f"  skip  {p['slug']}.html")
            continue
        html = build(p)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        sitemap_urls.append(
            f"  <url><loc>https://www.architecturaldrawings.uk/blog/{p['slug']}.html</loc>"
            f"<lastmod>2026-04-22</lastmod><priority>0.6</priority><changefreq>monthly</changefreq></url>"
        )
        created += 1
        print(f"  +  {p['slug']}.html")

    if sitemap_urls:
        sitemap_path = os.path.join(ROOT, "sitemap-core.xml")
        with open(sitemap_path, encoding="utf-8") as f:
            sitemap = f.read()
        insert = "\n".join(sitemap_urls) + "\n</urlset>"
        sitemap = sitemap.replace("</urlset>", insert)
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(sitemap)
        print(f"\nSitemap: added {len(sitemap_urls)} URLs")

    print(f"\nPhase 6: {created} posts created, {skipped} already existed")


if __name__ == "__main__":
    main()
