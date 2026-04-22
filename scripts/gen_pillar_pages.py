#!/usr/bin/env python3
"""Phase 7: Generate 4 pillar/hub pages at root level.
Each page is a comprehensive guide that links to all related service, blog,
pSEO, and case-study pages — completing the hub-and-spoke link structure.
Idempotent: skips existing files. Adds URLs to sitemap-core.xml.
"""
from __future__ import annotations
import os, re, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Pull CSS from existing root page
ref = open(os.path.join(ROOT, "why-us.html"), encoding="utf-8").read()
css_match = re.search(r"<style>.*?</style>", ref, re.DOTALL)
CSS_BLOCK = css_match.group(0) if css_match else "<style></style>"

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>"""

FAVICON = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />"""

ANALYTICS = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-77CQ2PWJM4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-77CQ2PWJM4',{anonymize_ip:true});</script>"""

NAV = """<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="/" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav aria-label="Primary"><ul class="nav-links">
      <li><a href="/services.html">Services</a></li>
      <li><a href="/pricing.html">Pricing</a></li>
      <li><a href="/blog/">Resources</a></li>
      <li><a href="/about.html">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="/portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="/quote.html" class="btn btn-primary btn-sm">Free quote <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M4 10h12m-4-4 4 4-4 4"/></svg></a>
      <button class="btn-menu" aria-label="Menu" id="btnMenu"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="/services/planning-drawings.html">Planning permission drawings</a></li>
        <li><a href="/services/building-regulations.html">Building regulations drawings</a></li>
        <li><a href="/services/loft-conversions.html">Loft conversion drawings</a></li>
        <li><a href="/services/house-extensions.html">House extension plans</a></li>
        <li><a href="/services/mansard-roof.html">Mansard roof extensions</a></li>
        <li><a href="/services.html">All services</a></li>
      </ul></div>
      <div><h5>Loft conversions</h5><ul>
        <li><a href="/areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="/areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="/areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="/areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="/areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
        <li><a href="/areas/barnet/loft-conversions.html">Loft conversion Barnet</a></li>
      </ul></div>
      <div><h5>Extension plans</h5><ul>
        <li><a href="/areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
        <li><a href="/areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
        <li><a href="/areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
        <li><a href="/areas/ealing/house-extensions.html">Extension plans Ealing</a></li>
        <li><a href="/areas/brent/house-extensions.html">Extension plans Brent</a></li>
        <li><a href="/areas/hounslow/house-extensions.html">Extension plans Hounslow</a></li>
      </ul></div>
      <div><h5>Planning drawings</h5><ul>
        <li><a href="/areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
        <li><a href="/areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
        <li><a href="/areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
        <li><a href="/areas/tower-hamlets/planning-drawings.html">Planning drawings Tower Hamlets</a></li>
        <li><a href="/areas/greenwich/planning-drawings.html">Planning drawings Greenwich</a></li>
        <li><a href="/areas/sutton/planning-drawings.html">Planning drawings Sutton</a></li>
      </ul></div>
    </div>
    <div class="footer-grid">
      <div class="footer-col footer-col-brand">
        <a href="/" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
        <p>Chartered architectural technology for London homeowners, landlords and developers. MCIAT &middot; ICO &middot; &pound;2m PI.</p>
        <p class="tiny" style="margin-top:16px;color:rgba(250,250,247,.45);">86-90 Paul Street, London EC2A 4NE<br/>020 7946 0000 &middot; hello@architecturaldrawings.uk</p>
      </div>
      <div class="footer-col"><h5>Services</h5><ul>
        <li><a href="/services/planning-drawings.html">Planning drawings</a></li>
        <li><a href="/services/building-regulations.html">Building regs</a></li>
        <li><a href="/services/loft-conversions.html">Loft conversions</a></li>
        <li><a href="/services/house-extensions.html">House extensions</a></li>
        <li><a href="/services/mansard-roof.html">Mansard &amp; dormers</a></li>
      </ul></div>
      <div class="footer-col"><h5>Company</h5><ul>
        <li><a href="/about.html">About</a></li>
        <li><a href="/pricing.html">Pricing</a></li>
        <li><a href="/projects/">Projects</a></li>
        <li><a href="/reviews/">Reviews</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/areas/">All boroughs</a></li>
      </ul></div>
      <div class="footer-col"><h5>Account</h5><ul>
        <li><a href="/portal/login.html">Sign in</a></li>
        <li><a href="/portal/register.html">Create account</a></li>
        <li><a href="/quote.html">Start a quote</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Architectural Drawings Ltd. Registered in England No. 14872049.</span>
      <span><a href="/sitemap.xml">Sitemap</a> &middot; <a href="/privacy.html">Privacy</a> &middot; <a href="/terms.html">Terms</a></span>
    </div>
  </div>
</footer>"""

JS = """<script>
const nav = document.getElementById('nav');
if (nav) window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 12), {passive:true});
new IntersectionObserver(e => e.forEach(x => { if(x.isIntersecting){x.target.classList.add('in');} }), {threshold:0.1})
  .observe || document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
const io = new IntersectionObserver(e => e.forEach(x => { if(x.isIntersecting) x.target.classList.add('in'); }), {threshold:0.1});
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
document.querySelectorAll('.faq-item').forEach(item => item.addEventListener('toggle', () => item.classList.toggle('open', item.open)));
</script>"""

FI = '<span class="faq-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M8 3v10M3 8h10"/></svg></span>'

PILLAR_CSS = """
<style>
.pillar-body{max-width:800px;margin:0 auto;}
.pillar-body h2{font-size:clamp(1.7rem,3vw,2.4rem);margin:48px 0 16px;padding-top:48px;border-top:1px solid var(--line);}
.pillar-body h2:first-of-type{border-top:none;margin-top:0;padding-top:0;}
.pillar-body h3{font-size:clamp(1.2rem,2vw,1.5rem);margin:32px 0 12px;color:var(--ink);}
.pillar-body p{color:var(--ink-soft);font-size:1.05rem;line-height:1.7;margin-bottom:18px;}
.pillar-body a{color:var(--accent-deep);font-weight:600;text-decoration:underline;text-underline-offset:3px;}
.pillar-body a:hover{color:var(--accent);}
.pillar-body ul{color:var(--ink-soft);font-size:1.05rem;line-height:1.7;margin:0 0 18px 1.4em;}
.pillar-body li{margin-bottom:6px;}
.link-hub{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:24px 0 40px;}
.link-hub a{display:block;padding:14px 18px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);font-size:0.9rem;font-weight:600;color:var(--ink);text-decoration:none;transition:border-color .2s,box-shadow .2s,transform .2s;}
.link-hub a:hover{border-color:var(--accent);box-shadow:0 4px 16px rgba(37,99,235,.12);transform:translateY(-2px);color:var(--accent-deep);}
.toc-box{background:var(--accent-soft);border:1px solid rgba(37,99,235,.2);border-radius:var(--r-lg);padding:28px 32px;margin:0 0 48px;}
.toc-box h4{font-family:var(--font-body);font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:var(--accent-deep);margin:0 0 16px;}
.toc-box ol{padding-left:1.4em;display:flex;flex-direction:column;gap:8px;}
.toc-box li a{color:var(--accent-deep);font-weight:600;text-decoration:underline;text-underline-offset:3px;}
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:32px 0;}
@media(max-width:600px){.stat-row{grid-template-columns:1fr 1fr;}.link-hub{grid-template-columns:1fr;}}
.stat-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;text-align:center;}
.stat-num{font-family:var(--font-display);font-size:2.4rem;font-variation-settings:"opsz" 80,"SOFT" 40;color:var(--accent-deep);line-height:1;}
.stat-label{font-size:.82rem;color:var(--ink-soft);margin-top:6px;}
</style>"""


def faq_item(q, a):
    return f"""  <details class="faq-item">
    <summary>{q}{FI}</summary>
    <div class="faq-answer"><p>{a}</p></div>
  </details>"""


def build(p: dict) -> str:
    canon = f"https://www.architecturaldrawings.uk/{p['slug']}.html"
    faqs_html = "\n".join(faq_item(q, a) for q, a in p["faqs"])
    faqs_schema = json.dumps([
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in p["faqs"]
    ], indent=2)

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
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"Article",
  "headline":"{p['og_title']}","description":"{p['desc']}",
  "datePublished":"2026-04-22","dateModified":"2026-04-22",
  "author":{{"@type":"Organization","name":"Architectural Drawings London","url":"https://www.architecturaldrawings.uk"}},
  "publisher":{{"@type":"Organization","name":"Architectural Drawings London","url":"https://www.architecturaldrawings.uk"}},
  "mainEntityOfPage":{{"@type":"WebPage","@id":"{canon}"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://www.architecturaldrawings.uk/"}},
    {{"@type":"ListItem","position":2,"name":"{p['breadcrumb']}"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"FAQPage",
  "mainEntity":{faqs_schema}
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"WebPage","url":"{canon}",
  "speakable":{{"@type":"SpeakableSpecification","cssSelector":["h1",".hero-lede",".pillar-intro"]}}
}}
</script>
{FONTS}
{CSS_BLOCK}
{PILLAR_CSS}
{FAVICON}
{ANALYTICS}
</head>
<body>
{NAV}

<section class="hero" style="padding-bottom:clamp(32px,5vw,60px);">
  <div class="container" style="max-width:860px;">
    <nav style="font-size:.84rem;color:var(--ink-soft);margin-bottom:28px;">
      <a href="/" style="color:var(--ink-soft);font-weight:500;">Home</a>
      <span style="margin:0 6px;opacity:.5;">/</span>
      <span>{p['breadcrumb']}</span>
    </nav>
    <span class="eyebrow">{p['eyebrow']}</span>
    <h1 style="margin:16px 0 20px;">{p['h1']}</h1>
    <p class="hero-lede pillar-intro">{p['lede']}</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px;">
      <a href="/quote.html" class="btn btn-primary">Get a free quote <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M4 10h12m-4-4 4 4-4 4"/></svg></a>
      <a href="{p['service_href']}" class="btn btn-ghost" style="border:1px solid var(--line-strong);">{p['service_label']}</a>
    </div>
  </div>
</section>

<section style="padding-top:0;padding-bottom:clamp(60px,9vw,120px);">
  <div class="container">
    <div class="pillar-body">

      <div class="toc-box reveal">
        <h4>In this guide</h4>
        <ol>
{p['toc']}
        </ol>
      </div>

{p['body']}

      <h2 id="faq">Frequently asked questions</h2>
      <div class="faq-list">
{faqs_html}
      </div>

      <div style="margin-top:48px;padding-top:24px;border-top:1px solid var(--line);font-size:.88rem;color:var(--ink-softer);">
        Last updated: April 2026 &middot; By the Architectural Drawings London team (MCIAT Chartered)
      </div>
    </div>
  </div>
</section>

<section class="cta-band" style="background:linear-gradient(160deg,#142040 0%,#0B1222 100%);">
  <div class="container">
    <h2 style="color:#fff;max-width:640px;margin:0 auto 16px;">{p['cta_h2']}</h2>
    <p style="color:rgba(255,255,255,.6);max-width:520px;margin:0 auto 32px;">{p['cta_p']}</p>
    <a href="/quote.html" class="btn btn-accent" style="font-size:1rem;padding:16px 28px;">
      Get a free quote in 60 seconds
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M4 10h12m-4-4 4 4-4 4"/></svg>
    </a>
  </div>
</section>

{FOOTER}
{JS}
</body>
</html>"""


# ─── PILLAR PAGE DATA ────────────────────────────────────────────────────────

PAGES = [

  {
    "slug": "loft-conversions-london-guide",
    "title": "Loft Conversions London: The Complete Guide 2026 | Architectural Drawings London",
    "og_title": "Loft Conversions London: Complete Guide 2026",
    "desc": "Complete guide to loft conversions in London 2026. Types, planning routes, costs, building regulations, and how to choose the right drawings service. MCIAT expert guide.",
    "breadcrumb": "Loft Conversions London Guide",
    "eyebrow": "Complete guide · 2026",
    "h1": "Loft Conversions London: <em>The Complete Guide</em>",
    "lede": "Everything London homeowners need to know about loft conversions — types, planning routes, permitted development, costs, building regulations, and choosing the right drawings service. Updated April 2026.",
    "service_href": "/services/loft-conversions.html",
    "service_label": "View loft conversion drawings",
    "toc": """          <li><a href="#types">Types of loft conversion</a></li>
          <li><a href="#planning">Planning permission and PD</a></li>
          <li><a href="#costs">Costs and fees</a></li>
          <li><a href="#building-regs">Building regulations</a></li>
          <li><a href="#boroughs">London borough guide</a></li>
          <li><a href="#case-studies">Case studies</a></li>
          <li><a href="#guides">Further reading</a></li>
          <li><a href="#faq">FAQs</a></li>""",
    "body": """
      <div class="stat-row reveal">
        <div class="stat-card"><div class="stat-num">+20%</div><div class="stat-label">Average London property value uplift</div></div>
        <div class="stat-card"><div class="stat-num">98%</div><div class="stat-label">Our first-time approval rate</div></div>
        <div class="stat-card"><div class="stat-num">£1,225</div><div class="stat-label">Drawings from (fixed fee)</div></div>
      </div>

      <h2 id="types">Types of loft conversion</h2>
      <p>London properties suit different loft conversion types depending on roof structure and location. The four main types are:</p>
      <ul>
        <li><strong>Velux (rooflight) conversion</strong> — cheapest option (£15,000–£25,000 build), uses existing roof structure, best for steep-pitched roofs with existing headroom.</li>
        <li><strong>Rear dormer</strong> — standard London conversion (£35,000–£55,000 build), creates a vertical box at the rear, works on terraces and semis. Permitted development in most boroughs.</li>
        <li><strong>Hip-to-gable + rear dormer (L-shape)</strong> — for semis and detached (£45,000–£75,000 build), maximum space, often permitted development, combines gable infill with full-width dormer.</li>
        <li><strong>Mansard conversion</strong> — full roof rebuild (£70,000–£120,000 build), always needs planning permission, creates the most volume, typically on terraces in conservation-area boroughs.</li>
      </ul>
      <p>See our detailed comparisons: <a href="/blog/hip-to-gable-vs-rear-dormer.html">hip-to-gable vs rear dormer</a>, <a href="/blog/velux-vs-dormer-vs-hip-gable.html">Velux vs dormer vs hip-to-gable</a>, <a href="/blog/mansard-vs-hip-to-gable.html">mansard vs hip-to-gable</a>, and <a href="/blog/loft-vs-mansard.html">loft conversion vs mansard roof</a>.</p>

      <h2 id="planning">Planning permission and permitted development</h2>
      <p>Most rear dormers and hip-to-gable conversions in London proceed via <strong>permitted development</strong> — no planning application required. PD limits for loft conversions are 40 m³ on terraces and 50 m³ on semis/detached. A <a href="/blog/ldc-vs-planning-permission.html">Lawful Development Certificate</a> is strongly recommended to confirm lawfulness for mortgage and sale purposes.</p>
      <p><strong>Article 4 directions</strong> remove PD rights in specific areas — common in conservation area boroughs such as Islington, Camden, Hackney, Kensington &amp; Chelsea, and parts of Lambeth. In Article 4 areas, a full householder planning application is required. See our <a href="/blog/planning-vs-permitted-development.html">planning vs permitted development guide</a> and <a href="/blog/loft-conversion-without-planning.html">loft conversion without planning permission</a> article.</p>
      <p>Mansard conversions always require planning permission — there is no PD route. Several boroughs have Supplementary Planning Documents governing mansard design: <a href="/areas/hammersmith-and-fulham/loft-conversions.html">Hammersmith &amp; Fulham</a>, <a href="/areas/richmond-upon-thames/loft-conversions.html">Richmond</a>, and <a href="/areas/westminster/loft-conversions.html">Westminster</a>.</p>

      <h2 id="costs">Costs and drawing fees</h2>
      <p>Build costs for loft conversions in London (2026): £35,000–£75,000 for rear dormers and L-shapes; £70,000–£120,000 for full mansards. Our fixed-fee <a href="/services/loft-conversions.html">loft conversion drawings</a> start from <strong>£1,225</strong>, covering existing and proposed plans, all elevations, roof plan, and LDC or planning application documents. See <a href="/blog/extension-vs-loft-conversion.html">extension vs loft conversion</a> for ROI comparison, and borough-specific costs: <a href="/blog/loft-cost-camden.html">Camden</a>, <a href="/blog/loft-cost-islington.html">Islington</a>, <a href="/blog/loft-cost-hackney.html">Hackney</a>, <a href="/blog/loft-cost-wandsworth.html">Wandsworth</a>, <a href="/blog/loft-cost-lambeth.html">Lambeth</a>.</p>

      <h2 id="building-regs">Building regulations</h2>
      <p>All loft conversions require building regulations approval regardless of the planning route. Key Approved Documents for loft conversions: Part A (structure — new floor, beam, dormer), Part B (fire safety — escape windows on every new bedroom), Part L (insulation), and Part K (staircase). Our <a href="/services/building-regulations.html">building regulations drawings</a> include coordinated structural calculations and all Approved Document compliance details. See <a href="/blog/building-notice-vs-full-plans.html">building notice vs full plans</a> for the two submission routes.</p>

      <h2 id="boroughs">London borough guide</h2>
      <p>Approval rates and PD coverage vary significantly by borough. We cover all 33 London boroughs:</p>
      <div class="link-hub reveal">
        <a href="/areas/camden/loft-conversions.html">Loft conversions Camden</a>
        <a href="/areas/islington/loft-conversions.html">Loft conversions Islington</a>
        <a href="/areas/hackney/loft-conversions.html">Loft conversions Hackney</a>
        <a href="/areas/tower-hamlets/loft-conversions.html">Loft conversions Tower Hamlets</a>
        <a href="/areas/southwark/loft-conversions.html">Loft conversions Southwark</a>
        <a href="/areas/lambeth/loft-conversions.html">Loft conversions Lambeth</a>
        <a href="/areas/wandsworth/loft-conversions.html">Loft conversions Wandsworth</a>
        <a href="/areas/hammersmith-and-fulham/loft-conversions.html">Loft conversions Hammersmith</a>
        <a href="/areas/kensington-and-chelsea/loft-conversions.html">Loft conversions Kensington</a>
        <a href="/areas/westminster/loft-conversions.html">Loft conversions Westminster</a>
        <a href="/areas/barnet/loft-conversions.html">Loft conversions Barnet</a>
        <a href="/areas/haringey/loft-conversions.html">Loft conversions Haringey</a>
        <a href="/areas/enfield/loft-conversions.html">Loft conversions Enfield</a>
        <a href="/areas/waltham-forest/loft-conversions.html">Loft conversions Waltham Forest</a>
        <a href="/areas/redbridge/loft-conversions.html">Loft conversions Redbridge</a>
        <a href="/areas/newham/loft-conversions.html">Loft conversions Newham</a>
        <a href="/areas/croydon/loft-conversions.html">Loft conversions Croydon</a>
        <a href="/areas/bromley/loft-conversions.html">Loft conversions Bromley</a>
        <a href="/areas/merton/loft-conversions.html">Loft conversions Merton</a>
        <a href="/areas/sutton/loft-conversions.html">Loft conversions Sutton</a>
        <a href="/areas/ealing/loft-conversions.html">Loft conversions Ealing</a>
        <a href="/areas/hillingdon/loft-conversions.html">Loft conversions Hillingdon</a>
        <a href="/areas/harrow/loft-conversions.html">Loft conversions Harrow</a>
        <a href="/areas/brent/loft-conversions.html">Loft conversions Brent</a>
      </div>

      <h2 id="case-studies">Loft conversion case studies</h2>
      <div class="link-hub reveal">
        <a href="/projects/loft-conversion-barnet.html">L-Shape Dormer — Barnet EN5</a>
        <a href="/projects/loft-enfield.html">Rear Dormer — Enfield EN1</a>
        <a href="/projects/loft-waltham-forest.html">Hip-to-Gable — Waltham Forest E17</a>
        <a href="/projects/loft-croydon.html">L-Shape Dormer — Croydon SE25</a>
        <a href="/projects/loft-merton.html">Full-Width Dormer — Merton SW19</a>
        <a href="/projects/loft-hillingdon.html">Rear Dormer — Hillingdon HA4</a>
        <a href="/projects/loft-harrow.html">Flat-Roof Dormer — Harrow HA5</a>
        <a href="/projects/mansard-hammersmith.html">Mansard Roof — Hammersmith W12</a>
        <a href="/projects/mansard-richmond.html">Mansard Roof — Richmond TW1</a>
        <a href="/projects/mansard-ealing.html">Mansard + Dormer — Ealing W13</a>
      </div>

      <h2 id="guides">Further reading</h2>
      <div class="link-hub reveal">
        <a href="/blog/loft-conversion-without-planning.html">Loft conversion without planning</a>
        <a href="/blog/hip-to-gable-loft-guide.html">Hip-to-gable guide</a>
        <a href="/blog/dormer-vs-velux-loft.html">Dormer vs Velux</a>
        <a href="/blog/loft-vs-mansard.html">Loft vs mansard roof</a>
        <a href="/blog/extension-vs-loft-conversion.html">Extension vs loft conversion</a>
        <a href="/blog/hip-to-gable-vs-rear-dormer.html">Hip-to-gable vs rear dormer</a>
        <a href="/blog/velux-vs-dormer-vs-hip-gable.html">Velux vs dormer vs hip-to-gable</a>
        <a href="/blog/mansard-vs-hip-to-gable.html">Mansard vs hip-to-gable</a>
        <a href="/blog/planning-permission-london.html">Planning permission in London</a>
        <a href="/blog/ldc-vs-planning-permission.html">LDC vs planning permission</a>
        <a href="/planning-data/london-planning-approval-rates.html">London planning approval rates</a>
      </div>
""",
    "faqs": [
      ("Do I need planning permission for a loft conversion in London?", "Most rear dormers and hip-to-gable conversions in London are permitted development — no planning permission needed. A Lawful Development Certificate is strongly recommended. Article 4 directions in conservation area boroughs (Camden, Islington, Hackney, Kensington) remove PD rights, requiring a full planning application. Mansard conversions always require planning permission."),
      ("How much do loft conversion drawings cost?", "Our fixed-fee loft conversion drawings start from £1,225 for a full LDC or planning application package — existing and proposed plans, all elevations, roof plan, and all supporting documents. Building regulations drawings are a separate package from £1,095."),
      ("What is the maximum loft conversion size under permitted development?", "40 cubic metres of additional roof space on a terrace or mid-terrace; 50 cubic metres on a semi-detached or detached house. Volume is measured from the original roof structure, not any previous extensions."),
      ("How long does a loft conversion take?", "Drawings and approvals: 8–14 weeks (6–8 weeks for LDC, 8–13 weeks for planning permission plus 4–6 weeks for building regulations). Build time on site: 8–14 weeks depending on conversion type."),
      ("Which loft conversion adds the most value in London?", "An L-shape (hip-to-gable plus full-width rear dormer) on a semi-detached typically adds the most absolute value — two new bedrooms and a bathroom can add 15–25% to a property's value. On a terrace, a full-width rear dormer delivers the best return relative to build cost."),
      ("What building regulations apply to loft conversions?", "Key Approved Documents: Part A (structure), Part B (fire safety — escape window required in every new bedroom), Part L (thermal insulation), Part K (staircase gradient and headroom). All loft conversions require building regulations approval regardless of the planning route."),
      ("Can I do a loft conversion in a conservation area?", "Yes, but planning permission is almost always required. The council will assess the impact on the street scene — mansard conversions and rear dormers visible from the principal elevation face the most scrutiny. A well-prepared Heritage Statement and design that references the character appraisal significantly improves approval likelihood."),
      ("How do I find out if my property has Article 4 directions?", "Check the council's interactive planning map (available on every London borough council website) or call the planning department. Article 4 directions are also listed in the council's Local Development Framework documents. We check Article 4 status as part of every project assessment."),
    ],
    "cta_h2": "Ready to start your <em>loft conversion?</em>",
    "cta_p": "MCIAT-chartered drawings from £1,225. Fixed fee. 98% first-time approval rate across all 33 London boroughs.",
  },

  {
    "slug": "house-extensions-london-guide",
    "title": "House Extensions London: The Complete Guide 2026 | Architectural Drawings London",
    "og_title": "House Extensions London: Complete Guide 2026",
    "desc": "Complete guide to house extensions in London 2026. Types, planning routes, costs, building regulations, and permitted development rules. MCIAT expert guide.",
    "breadcrumb": "House Extensions London Guide",
    "eyebrow": "Complete guide · 2026",
    "h1": "House Extensions London: <em>The Complete Guide</em>",
    "lede": "Everything London homeowners need to know about house extensions — rear, side, single and double storey, planning routes, permitted development, costs, and building regulations. Updated April 2026.",
    "service_href": "/services/house-extensions.html",
    "service_label": "View extension drawings",
    "toc": """          <li><a href="#types">Types of extension</a></li>
          <li><a href="#planning">Planning and permitted development</a></li>
          <li><a href="#costs">Costs and drawing fees</a></li>
          <li><a href="#building-regs">Building regulations</a></li>
          <li><a href="#boroughs">London borough guide</a></li>
          <li><a href="#case-studies">Case studies</a></li>
          <li><a href="#guides">Further reading</a></li>
          <li><a href="#faq">FAQs</a></li>""",
    "body": """
      <div class="stat-row reveal">
        <div class="stat-card"><div class="stat-num">+12%</div><div class="stat-label">Average value uplift, rear extension</div></div>
        <div class="stat-card"><div class="stat-num">98%</div><div class="stat-label">Our first-time approval rate</div></div>
        <div class="stat-card"><div class="stat-num">£840</div><div class="stat-label">Planning drawings from (fixed fee)</div></div>
      </div>

      <h2 id="types">Types of house extension</h2>
      <p>London homeowners have several extension options depending on property type, garden depth, and planning context:</p>
      <ul>
        <li><strong>Single-storey rear extension</strong> — the most common type, adding an enlarged kitchen-diner. PD permitted up to 3 m depth (semis/terraces) or 4 m (detached), with the Larger Home Extension Scheme allowing 6 m and 8 m respectively.</li>
        <li><strong>Double-storey rear extension</strong> — always needs planning permission. Adds a bedroom above and enlarged ground floor below. Best ROI where garden depth is sufficient.</li>
        <li><strong>Side return extension</strong> — infills the narrow gap alongside Victorian and Edwardian terraces. Usually requires planning permission on semis.</li>
        <li><strong>Wraparound extension</strong> — combines rear and side return in an L-shape. Planning permission required. Maximum ground floor space on a terrace.</li>
        <li><strong>Garage conversion</strong> — lowest cost option. Often permitted development. Loses parking but gains habitable space.</li>
      </ul>
      <p>Compare your options: <a href="/blog/single-vs-double-storey-extension.html">single vs double storey</a>, <a href="/blog/rear-vs-side-extension.html">rear vs side return</a>, <a href="/blog/side-return-vs-wraparound.html">side return vs wraparound</a>, <a href="/blog/flat-vs-pitched-roof-extension.html">flat vs pitched roof</a>.</p>

      <h2 id="planning">Planning permission and permitted development</h2>
      <p>Single-storey rear extensions within PD limits don't require planning permission. The Larger Home Extension Scheme (LHES) allows 6 m on semis/terraces and 8 m on detached via a simple <a href="/blog/full-planning-vs-prior-approval.html">prior approval</a> process. Double-storey extensions, side extensions on semis, and all works in Article 4 direction areas require a <a href="/blog/householder-vs-full-planning.html">householder planning application</a>.</p>
      <p>See also: <a href="/blog/pre-app-vs-direct-application.html">pre-application advice vs going direct</a>, <a href="/blog/conservation-area-planning-london.html">conservation area planning London</a>, <a href="/blog/planning-vs-permitted-development.html">planning vs permitted development</a>.</p>

      <h2 id="costs">Costs and drawing fees</h2>
      <p>Single-storey extensions: £45,000–£80,000 to build. Double-storey: £75,000–£130,000. Our fixed-fee <a href="/services/house-extensions.html">extension planning drawings</a> start from <strong>£840</strong>. Building regulations drawings from £1,095. Borough-specific extension costs: <a href="/blog/extension-cost-camden.html">Camden</a>, <a href="/blog/extension-cost-islington.html">Islington</a>, <a href="/blog/extension-cost-hackney.html">Hackney</a>, <a href="/blog/extension-cost-wandsworth.html">Wandsworth</a>, <a href="/blog/extension-cost-bromley.html">Bromley</a>, <a href="/blog/extension-cost-croydon.html">Croydon</a>. Full cost guide: <a href="/blog/extension-cost-guide-london.html">house extension cost guide London</a>.</p>

      <h2 id="building-regs">Building regulations</h2>
      <p>All extensions require building regulations approval. Key elements: Part A (foundations, beams, structural frame), Part B (fire spread), Part L (thermal insulation — SAP calculation required for extensions), Part F (ventilation), Part H (drainage). <a href="/blog/building-notice-vs-full-plans.html">Full Plans submission</a> is recommended for all structural extensions. See <a href="/blog/labc-vs-approved-inspector.html">LABC vs approved inspector</a> for the two BCO options.</p>

      <h2 id="boroughs">London borough extension guides</h2>
      <div class="link-hub reveal">
        <a href="/areas/camden/house-extensions.html">Extensions Camden</a>
        <a href="/areas/islington/house-extensions.html">Extensions Islington</a>
        <a href="/areas/hackney/house-extensions.html">Extensions Hackney</a>
        <a href="/areas/tower-hamlets/house-extensions.html">Extensions Tower Hamlets</a>
        <a href="/areas/southwark/house-extensions.html">Extensions Southwark</a>
        <a href="/areas/lambeth/house-extensions.html">Extensions Lambeth</a>
        <a href="/areas/wandsworth/house-extensions.html">Extensions Wandsworth</a>
        <a href="/areas/lewisham/house-extensions.html">Extensions Lewisham</a>
        <a href="/areas/greenwich/house-extensions.html">Extensions Greenwich</a>
        <a href="/areas/bromley/house-extensions.html">Extensions Bromley</a>
        <a href="/areas/croydon/house-extensions.html">Extensions Croydon</a>
        <a href="/areas/merton/house-extensions.html">Extensions Merton</a>
        <a href="/areas/sutton/house-extensions.html">Extensions Sutton</a>
        <a href="/areas/kingston-upon-thames/house-extensions.html">Extensions Kingston</a>
        <a href="/areas/richmond-upon-thames/house-extensions.html">Extensions Richmond</a>
        <a href="/areas/hounslow/house-extensions.html">Extensions Hounslow</a>
        <a href="/areas/ealing/house-extensions.html">Extensions Ealing</a>
        <a href="/areas/hillingdon/house-extensions.html">Extensions Hillingdon</a>
        <a href="/areas/harrow/house-extensions.html">Extensions Harrow</a>
        <a href="/areas/brent/house-extensions.html">Extensions Brent</a>
        <a href="/areas/barnet/house-extensions.html">Extensions Barnet</a>
        <a href="/areas/enfield/house-extensions.html">Extensions Enfield</a>
        <a href="/areas/haringey/house-extensions.html">Extensions Haringey</a>
        <a href="/areas/waltham-forest/house-extensions.html">Extensions Waltham Forest</a>
      </div>

      <h2 id="case-studies">Extension case studies</h2>
      <div class="link-hub reveal">
        <a href="/projects/rear-extension-brent.html">Single-Storey Rear — Brent NW10</a>
        <a href="/projects/planning-drawings-tower-hamlets.html">Conservation Area Extension — Tower Hamlets E1W</a>
        <a href="/projects/extension-hounslow.html">Side Return — Hounslow W4</a>
        <a href="/projects/planning-drawings-greenwich.html">Double-Storey Rear — Greenwich SE3</a>
        <a href="/projects/extension-bromley.html">Wraparound — Bromley BR3</a>
        <a href="/projects/planning-haringey.html">Side + Loft — Haringey N10</a>
        <a href="/projects/extension-sutton.html">Two-Storey Rear — Sutton SM3</a>
        <a href="/projects/planning-drawings-redbridge.html">Article 4 Extension — Redbridge IG1</a>
        <a href="/projects/extension-kingston.html">Ground Floor Extension — Kingston KT6</a>
        <a href="/projects/pd-havering.html">LHES Extension — Havering RM1</a>
      </div>

      <h2 id="guides">Further reading</h2>
      <div class="link-hub reveal">
        <a href="/blog/single-vs-double-storey-extension.html">Single vs double storey</a>
        <a href="/blog/flat-vs-pitched-roof-extension.html">Flat vs pitched roof</a>
        <a href="/blog/side-return-vs-wraparound.html">Side return vs wraparound</a>
        <a href="/blog/rear-vs-side-extension.html">Rear vs side extension</a>
        <a href="/blog/double-storey-extension-guide.html">Double storey extension guide</a>
        <a href="/blog/kitchen-extension-cost-london.html">Kitchen extension costs London</a>
        <a href="/blog/kitchen-extension-vs-garage-conversion.html">Kitchen extension vs garage conversion</a>
        <a href="/blog/outbuilding-vs-extension.html">Outbuilding vs extension</a>
        <a href="/blog/extension-vs-loft-conversion.html">Extension vs loft conversion</a>
        <a href="/blog/party-wall-guide-london.html">Party wall guide London</a>
        <a href="/blog/structural-engineer-vs-architectural-technologist.html">Structural engineer vs architectural technologist</a>
      </div>
""",
    "faqs": [
      ("How far can I extend without planning permission?", "Single-storey rear extension: 3 m on a semi or terrace, 4 m on a detached house under standard PD. The Larger Home Extension Scheme extends this to 6 m (semi/terrace) and 8 m (detached) via prior approval notification. Side extensions on semis and double-storey extensions always require planning permission."),
      ("How much do extension planning drawings cost?", "Our fixed-fee planning drawings start from £840 for a single-storey rear extension householder application. Combined planning and building regulations packages from £1,935. Fees are fixed regardless of determination time."),
      ("How long does planning permission take for an extension in London?", "Householder applications have an 8-week statutory target. In practice, inner London boroughs often take 10–14 weeks; outer boroughs like Bromley, Sutton, and Havering frequently decide within 8 weeks. We track borough-specific determination times to set realistic client expectations."),
      ("What is the Larger Home Extension Scheme?", "The LHES (also called the neighbour consultation scheme) allows single-storey rear extensions of up to 6 m on semis/terraces and 8 m on detached houses. The council notifies neighbours for 42 days. If no material objections are raised, the works proceed. It is faster and cheaper than a full planning application."),
      ("Do I need building regulations for an extension?", "Yes — all extensions require building regulations approval regardless of the planning route. Building regulations cover structure, insulation, fire safety, drainage, and ventilation. A Full Plans submission is recommended for extensions involving structural work."),
      ("Can I extend in a conservation area?", "Yes. Conservation area restrictions primarily affect extensions visible from the street. Rear extensions on properties in conservation areas are often approvable provided they are subservient to the host building, use sympathetic materials, and comply with the conservation area character appraisal. A Heritage Impact Assessment may be required."),
      ("What is the 45-degree rule for extensions?", "The 45-degree rule assesses whether a proposed extension blocks daylight to the nearest habitable room window in a neighbouring property by more than 45 degrees. It is the primary policy tool limiting double-storey extension depth relative to neighbouring windows."),
      ("Should I use a local architect or a fixed-fee drawing service?", "For defined-scope extensions — rear extensions, side returns, wraparounds — a fixed-fee MCIAT-chartered service delivers the same planning outcome at 20–30% of the cost of a traditional architect. See our <a href='/blog/online-vs-local-architect.html'>online vs local architect comparison</a>."),
    ],
    "cta_h2": "Get <em>extension drawings</em> from £840",
    "cta_p": "MCIAT-chartered. Fixed fee. 98% first-time approval rate. We cover all 33 London boroughs.",
  },

  {
    "slug": "planning-permission-london-guide",
    "title": "Planning Permission London: The Complete Guide 2026 | Architectural Drawings London",
    "og_title": "Planning Permission London: Complete Guide 2026",
    "desc": "Complete guide to planning permission in London 2026. Application types, timescales, fees, approval rates by borough, permitted development, and how to maximise your chances. MCIAT expert guide.",
    "breadcrumb": "Planning Permission London Guide",
    "eyebrow": "Complete guide · 2026",
    "h1": "Planning Permission London: <em>The Complete Guide</em>",
    "lede": "Everything you need to know about planning permission in London — application types, permitted development, timescales, council fees, approval rates across all 33 boroughs, and how to get approved first time. Updated April 2026.",
    "service_href": "/services/planning-drawings.html",
    "service_label": "View planning drawings service",
    "toc": """          <li><a href="#types">Application types</a></li>
          <li><a href="#pd">Permitted development</a></li>
          <li><a href="#process">The application process</a></li>
          <li><a href="#approval-rates">Approval rates by borough</a></li>
          <li><a href="#boroughs">Borough-specific guides</a></li>
          <li><a href="#case-studies">Case studies</a></li>
          <li><a href="#guides">Further reading</a></li>
          <li><a href="#faq">FAQs</a></li>""",
    "body": """
      <div class="stat-row reveal">
        <div class="stat-card"><div class="stat-num">87%</div><div class="stat-label">London average approval rate (all applications)</div></div>
        <div class="stat-card"><div class="stat-num">98%</div><div class="stat-label">Our first-time approval rate</div></div>
        <div class="stat-card"><div class="stat-num">£258</div><div class="stat-label">Householder application fee (2026)</div></div>
      </div>

      <h2 id="types">Planning application types</h2>
      <p>The application type determines the fee, process, and determination timescale:</p>
      <ul>
        <li><strong>Householder application</strong> — for extensions, loft conversions, and alterations to an existing dwelling. Fee: £258. 8-week determination target. See <a href="/blog/householder-vs-full-planning.html">householder vs full planning</a>.</li>
        <li><strong>Prior approval (LHES)</strong> — for larger single-storey rear extensions (6 m semis, 8 m detached). 42-day neighbour consultation. Lower risk than full planning. See <a href="/blog/full-planning-vs-prior-approval.html">full planning vs prior approval</a>.</li>
        <li><strong>Lawful Development Certificate</strong> — confirms works are permitted development (no planning permission needed). Fee: £234. See <a href="/blog/ldc-vs-planning-permission.html">LDC vs planning permission</a>.</li>
        <li><strong>Full planning application</strong> — for new dwellings, change of use, commercial development, and works not covered by householder PD. Higher fee, longer process. See <a href="/blog/householder-vs-full-planning.html">householder vs full planning</a>.</li>
      </ul>

      <h2 id="pd">Permitted development rights</h2>
      <p>Permitted development (PD) allows many common works without planning permission. Key PD rights relevant to London homeowners: single-storey rear extensions (3 m semis, 4 m detached), loft conversions within volume limits (40 m³ terraces, 50 m³ semis/detached), outbuildings under 2.5 m eaves height, and roof lights that don't protrude above the roof plane.</p>
      <p><strong>Article 4 directions</strong> remove PD rights in designated areas — most commonly conservation areas and certain interwar housing estates. Always check the council's planning map before assuming PD applies. See <a href="/blog/planning-vs-permitted-development.html">planning vs permitted development</a> and <a href="/blog/permitted-development-rules-2026.html">permitted development rules 2026</a>.</p>

      <h2 id="process">The planning application process</h2>
      <p>A householder planning application typically follows this process: (1) site visit and measured survey; (2) design and drawings; (3) application submission to the council; (4) validation by planning department (typically 1–2 weeks); (5) neighbour notification and consultation period (21 days); (6) officer assessment and determination (8–14 weeks from validation). Consider <a href="/blog/pre-app-vs-direct-application.html">pre-application advice</a> for complex conservation area projects.</p>
      <p>If refused, options include: amending and resubmitting (free within 12 months), or <a href="/blog/planning-permission-refused-what-next.html">appealing to the Planning Inspectorate</a>.</p>

      <h2 id="approval-rates">London planning approval rates 2026</h2>
      <p>Approval rates for householder applications vary significantly across the 33 boroughs. Full data and borough rankings in our <a href="/planning-data/london-planning-approval-rates.html">London planning approval rates report</a>. Top-performing boroughs (90%+): Havering (96%), Bromley (94%), Sutton (94%), Barnet (91%). More contested boroughs (under 82%): Hackney, Tower Hamlets, Newham, Lambeth.</p>

      <h2 id="boroughs">Borough-specific planning guides</h2>
      <div class="link-hub reveal">
        <a href="/planning-barnet.html">Planning in Barnet</a>
        <a href="/planning-camden.html">Planning in Camden</a>
        <a href="/planning-hackney.html">Planning in Hackney</a>
        <a href="/planning-haringey.html">Planning in Haringey</a>
        <a href="/planning-islington.html">Planning in Islington</a>
        <a href="/planning-tower-hamlets.html">Planning in Tower Hamlets</a>
        <a href="/planning-southwark.html">Planning in Southwark</a>
        <a href="/planning-lambeth.html">Planning in Lambeth</a>
        <a href="/planning-wandsworth.html">Planning in Wandsworth</a>
        <a href="/planning-lewisham.html">Planning in Lewisham</a>
        <a href="/planning-greenwich.html">Planning in Greenwich</a>
        <a href="/planning-bromley.html">Planning in Bromley</a>
        <a href="/planning-croydon.html">Planning in Croydon</a>
        <a href="/planning-merton.html">Planning in Merton</a>
        <a href="/planning-sutton.html">Planning in Sutton</a>
        <a href="/planning-ealing.html">Planning in Ealing</a>
        <a href="/planning-hammersmith-and-fulham.html">Planning in Hammersmith</a>
        <a href="/planning-kensington-and-chelsea.html">Planning in Kensington</a>
        <a href="/planning-westminster.html">Planning in Westminster</a>
        <a href="/planning-richmond-upon-thames.html">Planning in Richmond</a>
      </div>

      <h2 id="case-studies">Planning case studies</h2>
      <div class="link-hub reveal">
        <a href="/projects/planning-drawings-tower-hamlets.html">Conservation Area — Tower Hamlets E1W</a>
        <a href="/projects/rear-extension-brent.html">Article 4 Zone — Brent NW10</a>
        <a href="/projects/planning-drawings-greenwich.html">Double-Storey — Greenwich SE3</a>
        <a href="/projects/planning-haringey.html">Conservation Area — Haringey N10</a>
        <a href="/projects/planning-drawings-redbridge.html">Article 4 — Redbridge IG1</a>
        <a href="/projects/extension-hounslow.html">Side Return — Hounslow W4</a>
        <a href="/projects/extension-sutton.html">Two-Storey — Sutton SM3</a>
        <a href="/projects/pd-havering.html">Prior Approval — Havering RM1</a>
      </div>

      <h2 id="guides">Further reading</h2>
      <div class="link-hub reveal">
        <a href="/blog/planning-permission-london.html">Planning permission in London guide</a>
        <a href="/blog/planning-vs-permitted-development.html">Planning vs permitted development</a>
        <a href="/blog/permitted-development-rules-2026.html">PD rules 2026</a>
        <a href="/blog/ldc-vs-planning-permission.html">LDC vs planning permission</a>
        <a href="/blog/householder-vs-full-planning.html">Householder vs full planning</a>
        <a href="/blog/full-planning-vs-prior-approval.html">Full planning vs prior approval</a>
        <a href="/blog/conservation-area-planning-london.html">Conservation area planning</a>
        <a href="/blog/pre-app-vs-direct-application.html">Pre-application advice</a>
        <a href="/blog/planning-agent-vs-diy.html">Planning agent vs DIY</a>
        <a href="/blog/planning-permission-refused-what-next.html">Planning refused — what next</a>
        <a href="/blog/how-long-planning-permission.html">How long planning permission takes</a>
        <a href="/planning-data/london-planning-approval-rates.html">London planning approval rates</a>
      </div>
""",
    "faqs": [
      ("How much does a planning application cost in London?", "Council fees are set nationally. Householder application: £258. Lawful Development Certificate: £234. Prior approval (LHES): £120. Full planning for a new dwelling: £578. These fees are additional to the professional fees for preparing the drawings and application."),
      ("How long does planning permission take in London?", "The statutory target for householder applications is 8 weeks from validation. In practice, inner London boroughs average 10–14 weeks; outer boroughs often decide within 8 weeks. Hackney, Tower Hamlets, and Haringey are consistently slower; Havering, Bromley, and Sutton are consistently faster."),
      ("What is the difference between planning permission and permitted development?", "Planning permission is a formal approval granted by the council for works that require it. Permitted development rights allow certain common works without any planning application — the law grants the right automatically. A Lawful Development Certificate confirms which category your works fall into."),
      ("What is an Article 4 direction?", "An Article 4 direction removes permitted development rights in a specific area, requiring a planning application for works that would otherwise be automatic. Common in conservation areas and some interwar housing estates across London. Always check before assuming PD applies."),
      ("Do I need planning permission for a loft conversion?", "Most rear dormers and hip-to-gable conversions are permitted development. Mansard conversions always require planning permission. Works in Article 4 direction areas always require planning permission regardless of conversion type."),
      ("What drawings are required for a planning application?", "A householder application requires: existing and proposed floor plans (all affected levels), four elevations (north/south/east/west), a site location plan (1:1250), a block plan (1:500), and usually a Design and Access Statement for conservation area works or significant extensions. Our planning drawings packages include all required documents."),
      ("Can I appeal a planning refusal in London?", "Yes. Planning appeals for householder refusals are free and decided by the Planning Inspectorate via written representations. The appeal process takes approximately 6 months. Our team can advise on appeal strength before you commit to the process."),
      ("What is pre-application advice and is it worth it?", "Pre-app is a paid consultation with the planning officer before submitting a formal application. It can clarify policy interpretation for complex conservation area or basement projects. For standard householder works (extensions, loft conversions), thorough upfront design usually makes pre-app unnecessary. See our <a href='/blog/pre-app-vs-direct-application.html'>pre-app vs direct application comparison</a>."),
    ],
    "cta_h2": "Need <em>planning drawings</em> for your London project?",
    "cta_p": "MCIAT-chartered drawings from £840. Fixed fee. 98% first-time approval rate across all 33 London boroughs.",
  },

  {
    "slug": "building-regulations-london-guide",
    "title": "Building Regulations London: The Complete Guide 2026 | Architectural Drawings London",
    "og_title": "Building Regulations London: Complete Guide 2026",
    "desc": "Complete guide to building regulations in London 2026. Approved Documents, Full Plans vs Building Notice, approved inspectors, structural calculations, and what building control checks. MCIAT expert guide.",
    "breadcrumb": "Building Regulations London Guide",
    "eyebrow": "Complete guide · 2026",
    "h1": "Building Regulations London: <em>The Complete Guide</em>",
    "lede": "Everything London homeowners need to know about building regulations — Approved Documents, Full Plans vs Building Notice, LABC vs approved inspectors, what gets checked, and how to get Full Plans approval fast. Updated April 2026.",
    "service_href": "/services/building-regulations.html",
    "service_label": "View building regulations drawings",
    "toc": """          <li><a href="#what">What building regulations cover</a></li>
          <li><a href="#routes">Full Plans vs Building Notice</a></li>
          <li><a href="#who">LABC vs approved inspector</a></li>
          <li><a href="#structural">Structural calculations</a></li>
          <li><a href="#part-l">Part L energy compliance</a></li>
          <li><a href="#case-studies">Case studies</a></li>
          <li><a href="#guides">Further reading</a></li>
          <li><a href="#faq">FAQs</a></li>""",
    "body": """
      <div class="stat-row reveal">
        <div class="stat-card"><div class="stat-num">100%</div><div class="stat-label">Extensions that need building regs</div></div>
        <div class="stat-card"><div class="stat-num">5–8 wks</div><div class="stat-label">Typical Full Plans approval time</div></div>
        <div class="stat-card"><div class="stat-num">£1,095</div><div class="stat-label">Building regs drawings from (fixed fee)</div></div>
      </div>

      <h2 id="what">What building regulations cover</h2>
      <p>Building regulations set the minimum technical standards for construction work in England. Unlike planning permission (which controls appearance and use), building regulations control how buildings are built — safety, energy efficiency, and structural integrity.</p>
      <p>Key Approved Documents relevant to residential extensions and loft conversions:</p>
      <ul>
        <li><strong>Part A — Structure:</strong> Foundation design, wall thickness, beam and joist sizing, loft floor structure, dormer structure. Structural engineer's calculations required.</li>
        <li><strong>Part B — Fire safety:</strong> Means of escape, fire spread between dwellings, fire detection. Every new bedroom in a loft conversion requires a fire escape window (min 0.33 m² clear opening).</li>
        <li><strong>Part C — Damp:</strong> Damp-proof course, cavity wall construction, drainage away from foundations.</li>
        <li><strong>Part F — Ventilation:</strong> Background ventilation (trickle vents) and purge ventilation (openable windows). Converted garages need mechanical ventilation as habitable rooms.</li>
        <li><strong>Part L — Conservation of fuel and power:</strong> Thermal insulation values for new elements. An energy performance calculation (SAP assessment) is required to show the extension does not worsen the dwelling's overall energy performance.</li>
        <li><strong>Part K — Protection from falling:</strong> Staircase gradient (max 42 degrees), balustrade height, headroom on staircases (min 2.0 m).</li>
        <li><strong>Part P — Electrical safety:</strong> New electrical circuits must be installed by a Part P registered electrician or notified to building control.</li>
      </ul>

      <h2 id="routes">Full Plans vs Building Notice</h2>
      <p>Two routes to building regulations approval exist. <strong>Full Plans</strong> involves submitting detailed technical drawings before work starts — the building control officer checks and approves the drawings, and the builder works to the approved specification. This is the correct route for all structural work including extensions and loft conversions.</p>
      <p><strong>Building Notice</strong> requires only a notification to the council — no drawings submitted upfront. The BCO inspects as work progresses. This is appropriate only for simple, low-risk, non-structural works. See our detailed <a href="/blog/building-notice-vs-full-plans.html">building notice vs full plans comparison</a>.</p>

      <h2 id="who">LABC vs approved inspector</h2>
      <p>Building control can be carried out by the Local Authority Building Control (LABC) or by a private approved inspector. Both apply the same Approved Documents to the same standard. Approved inspectors typically offer faster Full Plans turnaround (3–5 weeks vs 5–8 weeks for LABC) and more flexible inspection scheduling. See <a href="/blog/labc-vs-approved-inspector.html">LABC vs approved inspector</a> for the full comparison.</p>

      <h2 id="structural">Structural calculations</h2>
      <p>Part A compliance requires structural calculations prepared by a chartered structural engineer (MIStructE or MICE). Calculations cover: foundation pad sizes, beam and column design, floor joist schemes, dormer structural frame, and any new openings in load-bearing walls. Our building regulations packages are produced in coordination with structural engineers — you deal with one team rather than two. See <a href="/blog/structural-engineer-vs-architectural-technologist.html">structural engineer vs architectural technologist</a> for roles explained.</p>

      <h2 id="part-l">Part L energy compliance</h2>
      <p>Approved Document Part L requires that new extensions do not worsen the overall energy performance of the dwelling. This is demonstrated via an energy calculation (simplified SAP assessment for most extensions) comparing the before and after performance. Key compliance points: U-values for new roof (0.18 W/m²K), new walls (0.28 W/m²K), new floor (0.22 W/m²K), and new glazing (max 2.0 W/m²K). See our <a href="/blog/building-regs-part-l-guide.html">Part L building regulations guide</a>.</p>

      <h2 id="case-studies">Building regulations case studies</h2>
      <div class="link-hub reveal">
        <a href="/projects/building-regs-newham.html">Full Plans — Newham E7 (5 wks)</a>
        <a href="/projects/building-regs-bexley.html">Extension + Loft — Bexley DA14 (4 wks)</a>
        <a href="/projects/building-regs-barking.html">Extension + Garage — Barking RM10 (3 wks)</a>
        <a href="/projects/loft-enfield.html">Loft LDC + Building Regs — Enfield EN1</a>
        <a href="/projects/loft-harrow.html">Loft Building Regs — Harrow HA5</a>
        <a href="/projects/extension-hounslow.html">Combined Package — Hounslow W4</a>
      </div>

      <h2 id="guides">Further reading</h2>
      <div class="link-hub reveal">
        <a href="/blog/building-regulations-explained.html">Building regulations explained</a>
        <a href="/blog/building-notice-vs-full-plans.html">Building notice vs full plans</a>
        <a href="/blog/labc-vs-approved-inspector.html">LABC vs approved inspector</a>
        <a href="/blog/building-regs-part-l-guide.html">Part L guide</a>
        <a href="/blog/structural-engineer-vs-architectural-technologist.html">Structural engineer vs architectural technologist</a>
        <a href="/blog/party-wall-guide-london.html">Party wall guide London</a>
        <a href="/blog/ldc-vs-planning-permission.html">LDC vs planning permission</a>
        <a href="/blog/householder-vs-full-planning.html">Householder vs full planning</a>
        <a href="/blog/how-long-planning-permission.html">Timescales guide</a>
      </div>
""",
    "faqs": [
      ("Do I need building regulations for an extension or loft conversion?", "Yes — always. Building regulations are required for all structural extensions, loft conversions, garage conversions, and most internal alterations regardless of whether planning permission was needed. The only exemptions are very small detached structures (under 15 m²) and some minor internal works."),
      ("What is the difference between planning permission and building regulations?", "Planning permission controls what you build and where — appearance, use, and impact on neighbours. Building regulations control how you build — structure, safety, insulation, ventilation, and fire protection. Most projects need both, but they are separate processes with separate fees and different approval bodies."),
      ("How long does building regulations approval take?", "Full Plans submissions are typically approved in 5–8 weeks by LABC; 3–5 weeks by an approved inspector. The building control officer checks drawings against the Approved Documents and issues a formal approval notice. Inspections then happen at key stages during construction."),
      ("What is a completion certificate?", "A completion certificate is issued by the building control body after a final inspection confirms all work complies with the approved plans and building regulations. It is a permanent legal document required for sale and for mortgage purposes. Without it, indemnity insurance is the only alternative — which provides less protection."),
      ("Do building regulations drawings need a structural engineer?", "Yes, for any project involving new beams, foundations, or structural alterations. Part A requires structural calculations from a chartered structural engineer (MIStructE or MICE). Our building regulations packages coordinate the structural engineer's input — you receive a single coordinated drawing set."),
      ("What is a Full Plans submission?", "A Full Plans submission provides detailed technical drawings to the building control body before work starts. The BCO checks and approves (or conditions) the drawings. This gives maximum certainty — your builder works to an approved specification. It is the recommended route for all structural residential projects."),
      ("How much do building regulations drawings cost?", "Our fixed-fee building regulations drawings packages start from £1,095 for a standard single-storey rear extension or loft conversion. The package includes structural coordination, Part L energy calculations, Part B fire details, and all Approved Document compliance information required for Full Plans approval."),
      ("Can I start work before building regulations approval?", "You can start work under a Building Notice route immediately after giving 48 hours' notice. Under the Full Plans route, you should wait for approval before starting structural work — building without approval risks having to demolish and redo work that doesn't comply."),
    ],
    "cta_h2": "Need <em>building regulations drawings?</em>",
    "cta_p": "Fixed-fee Full Plans packages from £1,095. Structural coordination included. MCIAT-chartered team covering all 33 London boroughs.",
  },

]


def main():
    created = 0
    skipped = 0
    sitemap_urls = []

    for p in PAGES:
        path = os.path.join(ROOT, f"{p['slug']}.html")
        if os.path.exists(path):
            skipped += 1
            print(f"  skip  {p['slug']}.html")
            continue
        html = build(p)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        sitemap_urls.append(
            f"  <url><loc>https://www.architecturaldrawings.uk/{p['slug']}.html</loc>"
            f"<lastmod>2026-04-22</lastmod><priority>0.8</priority><changefreq>monthly</changefreq></url>"
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
        print(f"\nSitemap: added {len(sitemap_urls)} URLs (priority 0.8)")

    print(f"\nPhase 7 pillar pages: {created} created, {skipped} already existed")


if __name__ == "__main__":
    main()
