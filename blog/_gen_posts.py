"""Generate the remaining 7 blog posts using the established template pattern."""
import os, re, sys

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))

# Read the reference file to extract boilerplate
ref_path = os.path.join(BLOG_DIR, 'rear-vs-side-extension.html')
print(f"Reading reference file: {ref_path}")
ref = open(ref_path, encoding='utf-8').read()
css_match = re.search(r'<style>.*?</style>', ref, re.DOTALL)
if not css_match:
    print("ERROR: Could not find CSS block in reference file")
    sys.exit(1)
CSS_BLOCK = css_match.group(0)
print(f"CSS block extracted ({len(CSS_BLOCK)} chars)")

HEAD_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>"""

FAVICON = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />"""

ANALYTICS = """  <script defer data-domain="architecturaldrawings.uk" src="https://plausible.io/js/script.js"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-77CQ2PWJM4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  window.gtag = window.gtag || gtag;
  gtag('js', new Date());
  gtag('config', 'G-77CQ2PWJM4', { anonymize_ip: true, allow_google_signals: false });
  document.addEventListener('click', function (event) {
    var target = event.target.closest('a, button'); if (!target) return;
    var label = (target.textContent || target.getAttribute('aria-label') || '').trim().slice(0, 120) || 'unknown';
    var href = target.getAttribute('href') || '';
    if (/quote|book|get started|contact|call/i.test(label) || /quote\\.html/i.test(href)) { gtag('event', 'cta_click', { event_category: 'engagement', event_label: label, link_url: href || window.location.pathname }); }
    if (href.startsWith('tel:')) { gtag('event', 'phone_click', { event_category: 'contact', event_label: href.replace('tel:', '') }); }
    if (href.startsWith('mailto:')) { gtag('event', 'email_click', { event_category: 'contact', event_label: href.replace('mailto:', '') }); }
  }, { passive: true });
</script>"""

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
      <a href="../quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul><li><a href="../services/planning-drawings.html">Planning permission drawings London</a></li><li><a href="../services/building-regulations.html">Building regulations drawings London</a></li><li><a href="../services/loft-conversions.html">Loft conversion drawings London</a></li><li><a href="../services/house-extensions.html">House extension plans London</a></li><li><a href="../services/mansard-roof.html">Mansard roof extensions London</a></li><li><a href="../services.html">Measured survey London</a></li><li><a href="../services.html">Lawful development certificate</a></li><li><a href="../services.html">Permitted development drawings</a></li><li><a href="../services.html">Party wall drawings</a></li><li><a href="../services.html">Structural calculations</a></li></ul></div>
      <div><h5>Loft conversions by borough</h5><ul><li><a href="../areas/camden/loft-conversions.html">Loft conversion Camden</a></li><li><a href="../areas/islington/loft-conversions.html">Loft conversion Islington</a></li><li><a href="../areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li><li><a href="../areas/tower-hamlets/loft-conversions.html">Loft conversion Tower Hamlets</a></li><li><a href="../areas/westminster/loft-conversions.html">Loft conversion Westminster</a></li><li><a href="../areas/kensington-and-chelsea/loft-conversions.html">Loft conversion Kensington</a></li><li><a href="../areas/hammersmith-and-fulham/loft-conversions.html">Loft conversion Hammersmith</a></li><li><a href="../areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li><li><a href="../areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li><li><a href="../areas/southwark/loft-conversions.html">Loft conversion Southwark</a></li></ul></div>
      <div><h5>Extension plans by borough</h5><ul><li><a href="../areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li><li><a href="../areas/greenwich/house-extensions.html">Extension plans Greenwich</a></li><li><a href="../areas/bromley/house-extensions.html">Extension plans Bromley</a></li><li><a href="../areas/croydon/house-extensions.html">Extension plans Croydon</a></li><li><a href="../areas/merton/house-extensions.html">Extension plans Merton</a></li><li><a href="../areas/kingston-upon-thames/house-extensions.html">Extension plans Kingston</a></li><li><a href="../areas/richmond-upon-thames/house-extensions.html">Extension plans Richmond</a></li><li><a href="../areas/hounslow/house-extensions.html">Extension plans Hounslow</a></li><li><a href="../areas/ealing/house-extensions.html">Extension plans Ealing</a></li><li><a href="../areas/hillingdon/house-extensions.html">Extension plans Hillingdon</a></li><li><a href="../areas/harrow/house-extensions.html">Extension plans Harrow</a></li><li><a href="../areas/brent/house-extensions.html">Extension plans Brent</a></li></ul></div>
      <div><h5>Planning drawings by borough</h5><ul><li><a href="../areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li><li><a href="../areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li><li><a href="../areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li><li><a href="../areas/waltham-forest/planning-drawings.html">Planning drawings Waltham Forest</a></li><li><a href="../areas/redbridge/planning-drawings.html">Planning drawings Redbridge</a></li><li><a href="../areas/newham/planning-drawings.html">Planning drawings Newham</a></li><li><a href="../areas/bexley/planning-drawings.html">Planning drawings Bexley</a></li><li><a href="../areas/havering/planning-drawings.html">Planning drawings Havering</a></li><li><a href="../areas/sutton/planning-drawings.html">Planning drawings Sutton</a></li><li><a href="../areas/barking-and-dagenham/planning-drawings.html">Planning drawings Barking</a></li><li><a href="../areas/city-of-london/planning-drawings.html">Planning drawings City of London</a></li></ul></div>
    </div>
    <div class="footer-bottom" style="border-top: 0; padding-top: 0;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; 86&ndash;90 Paul Street, London EC2A 4NE</span>
      <span><a href="../">Home</a> &middot; <a href="../services.html">Services</a> &middot; <a href="../pricing.html">Pricing</a> &middot; <a href="../privacy.html">Privacy</a> &middot; <a href="../terms.html">Terms</a></span>
    </div>
  </div>
</footer>"""

JS = """<script>
(() => {
  'use strict';
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    const io = new IntersectionObserver((entries) => { entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); } }); }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
    reveals.forEach((el) => io.observe(el));
  } else { reveals.forEach((el) => el.classList.add('in')); }
  const nav = document.getElementById('nav');
  if (nav) { const onScroll = () => { nav.classList.toggle('scrolled', window.scrollY > 12); }; onScroll(); window.addEventListener('scroll', onScroll, { passive: true }); }
  document.querySelectorAll('.faq-item').forEach((item) => { item.addEventListener('toggle', () => { item.classList.toggle('open', item.open); }); });
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => { const id = anchor.getAttribute('href'); if (id.length < 2) return; const target = document.querySelector(id); if (!target) return; e.preventDefault(); const navHeight = nav ? nav.offsetHeight : 0; window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20, behavior: 'smooth' }); });
  });
})();
</script>"""

FABS = """<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="Call us"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg></a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20for%20my%20project." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);transition:transform 0.3s var(--ease);" aria-label="WhatsApp"><svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a3.04 3.04 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg></a>
</div>"""

CK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>'
FI = '<span class="faq-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v10M3 8h10"/></svg></span>'

def faq_detail(q, a):
    return f"""      <details class="faq-item">
        <summary>
          {q}
          {FI}
        </summary>
        <div class="faq-answer">
          <p>{a}</p>
        </div>
      </details>"""

def faq_schema_entry(q, a):
    a_escaped = a.replace('"', '\\"')
    return f"""    {{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a_escaped}"
      }}
    }}"""

def related_card(href, title, desc):
    return f"""      <a href="{href}" class="service-card" style="padding: 24px;">
        <h3 style="font-size: 1.05rem;">{title}</h3>
        <p style="font-size: 0.85rem; color: var(--ink-soft); margin-top: 8px;">{desc}</p>
        <span class="service-card-link" style="margin-top: 12px;">Read article &rarr;</span>
      </a>"""

def build(slug, title, og_title, desc, breadcrumb, eyebrow, h1, minutes, tldrs, img_ph, body, faqs, faq_schemas, relateds, cta_h2, cta_p, cta1_href, cta1_text, cta2_href, cta2_text):
    canon = f"https://www.architecturaldrawings.uk/blog/{slug}.html"
    tldr_lis = "\n".join(f"        <li>{CK}{t}</li>" for t in tldrs)
    faq_html = "\n".join(faq_detail(q,a) for q,a in faqs)
    faq_schema = ",\n".join(faq_schema_entry(q,a) for q,a in faq_schemas)
    rel_html = "\n".join(related_card(*r) for r in relateds)

    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="author" href="/team/" />
<link rel="canonical" href="{canon}" />
<!-- Open Graph -->
<meta property="og:type" content="article" />
<meta property="og:url" content="{canon}" />
<meta property="og:title" content="{og_title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:locale" content="en_GB" />
<meta property="article:published_time" content="2026-04-16" />
<meta property="article:modified_time" content="2026-04-16" />
<meta property="article:author" content="Architectural Drawings London" />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{og_title}",
  "description": "{desc}",
  "datePublished": "2026-04-16",
  "dateModified": "2026-04-16",
  "author": {{ "@type": "Organization", "name": "Architectural Drawings London", "url": "https://www.architecturaldrawings.uk" }},
  "publisher": {{ "@type": "Organization", "name": "Architectural Drawings London", "url": "https://www.architecturaldrawings.uk" }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{canon}" }}
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.architecturaldrawings.uk/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.architecturaldrawings.uk/blog/" }},
    {{ "@type": "ListItem", "position": 3, "name": "{breadcrumb}" }}
  ]
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_schema}
  ]
}}
</script>

{HEAD_FONTS}
{CSS_BLOCK}
{FAVICON}
{ANALYTICS}
</head>
<body>

{NAV}

<section class="hero" style="padding-bottom: clamp(20px, 4vw, 40px);">
  <div class="container" style="max-width: 760px;">
    <nav class="breadcrumbs">
      <a href="../">Home</a><span>/</span><a href="./">Blog</a><span>/</span>{breadcrumb}
    </nav>
    <span class="eyebrow">{eyebrow} &middot; April 2026</span>
    <h1 style="margin: 16px 0 24px; font-size: clamp(2.4rem, 5.5vw, 4.2rem);">{h1}</h1>
    <div class="author-byline">
      <div class="author-avatar">AD</div>
      <div class="author-info">
        <strong>By the Architectural Drawings team</strong>
        MCIAT Chartered &middot; 16 April 2026 &middot; {minutes} min read
      </div>
    </div>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container article-body">

    <div class="tldr-box reveal">
      <h4>Key facts at a glance</h4>
      <ul>
{tldr_lis}
      </ul>
    </div>

    <div style="background:var(--bg-2);border-radius:var(--r-lg);padding:60px 24px;text-align:center;color:var(--ink-soft);margin:0 0 48px;">
      <p style="font-size:0.9rem;">{img_ph}</p>
    </div>

{body}

    <h2 id="faq" class="reveal">Frequently asked questions</h2>

    <div class="faq-list" style="margin-top: 24px;">

{faq_html}

    </div>

    <div style="margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--line); font-size: 0.88rem; color: var(--ink-softer);">
      Last updated: April 2026
    </div>

  </div>
</section>

<!-- related-articles -->
<section style="background: var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Keep reading</span>
      <h2 style="margin-top: 16px;">Related <em>articles</em></h2>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
{rel_html}
    </div>
  </div>
</section>

<section class="cta-band" style="background: var(--bg-2);">
  <div class="container">
    <h2>{cta_h2}</h2>
    <p>{cta_p}</p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <a href="{cta1_href}" class="btn btn-primary btn-lg">{cta1_text}</a>
      <a href="{cta2_href}" class="btn btn-outline btn-lg">{cta2_text}</a>
    </div>
  </div>
</section>

{FOOTER}

{JS}

{FABS}

</body>
</html>"""

    path = os.path.join(BLOG_DIR, f"{slug}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {path}")


##############################################################################
# POST 4: party-wall-guide-london
##############################################################################
build(
    slug="party-wall-guide-london",
    title="Party Wall Guide London 2026 | AD",
    og_title="Party Wall Guide London 2026: Everything You Need to Know",
    desc="Complete guide to Party Wall Act in London. When notices are needed, the surveyor process, costs, timelines, dispute resolution, and how it affects your extension project.",
    breadcrumb="Party Wall Guide",
    eyebrow="Guide",
    h1='Party Wall guide for London homeowners: <em style="color: var(--accent); font-weight: 300;">the complete 2026 handbook</em>',
    minutes="15",
    tldrs=[
        "Party Wall Act 1996 applies to most London extensions and loft conversions",
        "Notice must be served at least 2 months before starting work",
        "If neighbour consents in writing: no surveyor needed, no cost",
        "If neighbour dissents or ignores: both appoint surveyors, cost &pound;1,000&ndash;&pound;2,500+",
        "Three trigger types: work on the boundary, within 3m, or within 6m of neighbour",
        "Starting without serving notice is illegal and can lead to injunctions",
    ],
    img_ph="IMAGE PLACEHOLDER -- diagram showing the three types of Party Wall notice triggers: on the boundary, 3-metre zone, and 6-metre zone",
    body="""
    <h2 id="what" class="reveal">What is the Party Wall Act?</h2>

    <p>The Party Wall etc. Act 1996 is an English and Welsh law that provides a framework for preventing and resolving disputes between neighbours when one of them wants to carry out building work that could affect a shared wall, boundary, or the structural integrity of the neighbouring property. In London, where terraced and semi-detached houses share party walls and sit close to their boundaries, the Act applies to the vast majority of extension, loft conversion, and basement projects.</p>

    <p>The Act is not about whether you can do the work. Planning permission and building regulations deal with that. The Party Wall Act is about protecting your neighbour's property from damage during the work, and giving them a legal right to be informed before you start.</p>


    <h2 id="when" class="reveal">When does the Party Wall Act apply?</h2>

    <p>The Act is triggered by three types of building work:</p>

    <h3>1. Work directly on a party wall (Section 2)</h3>

    <p>This applies when you are cutting into, raising, lowering, demolishing, or altering a wall that is shared with your neighbour. Examples: inserting a steel beam into a party wall for a loft conversion, raising a party wall to build a mansard roof, or underpinning a shared wall for a basement conversion.</p>

    <h3>2. Building on or at the boundary line (Section 1)</h3>

    <p>This applies when you want to build a new wall on or astride the boundary line between your property and your neighbour's. Examples: a rear extension wall built on the boundary, a garden wall on the boundary, or a side return extension where the new external wall sits on the property line.</p>

    <h3>3. Excavation near neighbouring buildings (Section 6)</h3>

    <p>This applies when you excavate within 3 metres of your neighbour's building and go below the level of their foundations, or within 6 metres if a 45-degree line drawn from the bottom of your excavation would pass through their foundations. Examples: new extension foundations near a neighbour's house, basement excavation, or underpinning.</p>


    <h2 id="notice" class="reveal">The notice process step by step</h2>

    <ol>
      <li><strong>Identify affected neighbours.</strong> Determine which neighbours are affected by the work. For a typical rear extension, this might be one or two neighbours. For a loft conversion with work on the party wall, it is the neighbour on the other side of that wall.</li>
      <li><strong>Serve the correct notice.</strong> There are three notice types: a Party Structure Notice (Section 2, for work on the party wall), a Line of Junction Notice (Section 1, for new walls on the boundary), and a Section 6 Notice (for excavation). The notice must describe the proposed work, state the start date (at least 2 months away for party wall work, 1 month for excavation), and include your name and address.</li>
      <li><strong>Wait for the neighbour to respond.</strong> The neighbour has 14 days to consent or dissent. If they consent in writing, the process is complete -- no surveyor is needed, and you can proceed after the notice period expires. If they dissent, or do not respond within 14 days, a dispute is deemed to have arisen.</li>
      <li><strong>Appoint surveyors.</strong> If a dispute arises, both you and your neighbour must each appoint a surveyor, or you can agree to appoint a single Agreed Surveyor. The surveyors prepare a Party Wall Award -- a legal document that records the condition of the neighbour's property before work starts, sets out the scope of works, and determines any compensation or requirements.</li>
      <li><strong>Receive the Party Wall Award.</strong> The surveyors produce the Award, which both parties must comply with. The Award typically includes a Schedule of Condition (photographs and descriptions of the neighbour's property) and may impose conditions on working hours, access, and making good any damage.</li>
      <li><strong>Commence work.</strong> Once the Award is in place (or the neighbour has consented), you can start work on or after the date stated in the notice.</li>
    </ol>


    <h2 id="costs" class="reveal">Party Wall surveyor costs in London</h2>

    <p>If the neighbour consents, there is no surveyor cost at all. If a dispute arises:</p>

    <div class="price-box reveal">
      <h4>Typical Party Wall costs</h4>
      <div class="price-row">
        <span class="label">Agreed Surveyor (acting for both parties)</span>
        <span class="amount">&pound;1,000&ndash;&pound;1,500</span>
      </div>
      <div class="price-row">
        <span class="label">Two surveyors (each party appoints one)</span>
        <span class="amount">&pound;1,500&ndash;&pound;2,500+</span>
      </div>
      <div class="price-row">
        <span class="label">Third Surveyor (if the two cannot agree)</span>
        <span class="amount">&pound;500&ndash;&pound;1,000 additional</span>
      </div>
      <div class="price-row">
        <span class="label">Schedule of Condition only</span>
        <span class="amount">&pound;500&ndash;&pound;800</span>
      </div>
    </div>

    <p>Important: the building owner (you) pays for both surveyors' reasonable fees. This is a cost that many homeowners do not budget for. We always include Party Wall costs in our project cost estimates so you have a realistic total budget from the outset.</p>


    <h2 id="timeline" class="reveal">Party Wall timeline</h2>

    <p>The timeline depends entirely on whether the neighbour consents or dissents:</p>

    <ul>
      <li><strong>Best case (neighbour consents):</strong> Serve notice, receive written consent within 14 days, wait for the notice period to expire (2 months from the date of the notice for Section 2 work, 1 month for Section 6). Total: approximately 2 months.</li>
      <li><strong>Typical case (neighbour dissents or ignores):</strong> Serve notice, 14-day response period expires, appoint surveyors, surveyors conduct site inspections and prepare the Award. Total: 2&ndash;4 months.</li>
      <li><strong>Worst case (dispute about surveyor costs or scope):</strong> If the surveyors cannot agree, a Third Surveyor is appointed to determine the dispute. This can add months. Total: 4&ndash;8 months.</li>
    </ul>

    <blockquote>We recommend serving Party Wall notices as early as possible -- ideally while the planning application is being determined. This allows the Party Wall timeline to run in parallel with the planning timeline, rather than adding months to the overall project.</blockquote>


    <h2 id="disputes" class="reveal">Common disputes and how to avoid them</h2>

    <p>Most Party Wall disputes in London arise from poor communication, not genuine disagreement about the work. Here are the most common issues and how to prevent them:</p>

    <ul>
      <li><strong>Neighbour feels ambushed.</strong> Prevention: talk to your neighbour informally before serving the formal notice. Show them the drawings, explain what the work involves, and give them time to ask questions.</li>
      <li><strong>Neighbour objects to the building work itself.</strong> The Party Wall Act does not give the neighbour a right to prevent the work. It only requires that their property is protected. If a neighbour objects to the work itself, that is a planning matter, not a Party Wall matter. However, a dissent from the Party Wall notice will trigger the surveyor process and its costs.</li>
      <li><strong>Damage during construction.</strong> The Schedule of Condition records the state of the neighbour's property before work starts. If damage occurs during construction, the Award requires you to make it good. Good builders carry public liability insurance that covers party wall damage.</li>
      <li><strong>Access issues.</strong> If you need access to the neighbour's property during construction (e.g. to scaffold on their side), the Act provides a framework for this. But always discuss access requirements with the neighbour early.</li>
    </ul>


    <h2 id="without-notice" class="reveal">What happens if you start work without serving notice?</h2>

    <p>Starting work without serving the required Party Wall notice is a breach of the Act. Your neighbour can:</p>

    <ul>
      <li>Seek a <strong>court injunction</strong> to stop the work until the notice process is completed. This causes significant delay and legal costs.</li>
      <li>Claim <strong>damages</strong> for any damage caused to their property without a Schedule of Condition in place (making it harder to prove what was pre-existing).</li>
      <li>Appoint a surveyor at your expense to prepare a retrospective Award.</li>
    </ul>

    <p>It is always cheaper and simpler to serve notice properly before starting work. We can advise on Party Wall requirements as part of every project and recommend experienced Party Wall surveyors in your area.</p>


    <h2 id="our-role" class="reveal">How we help with Party Wall</h2>

    <p>While we are not Party Wall surveyors ourselves (the roles are deliberately separate under the Act), we help our clients in several ways:</p>

    <ul>
      <li>We identify whether the Party Wall Act applies to your project as part of the initial assessment</li>
      <li>We provide drawings that clearly show the relationship between your proposed work and the neighbouring property -- essential for the Party Wall notice</li>
      <li>We recommend experienced, RICS-accredited Party Wall surveyors across all 33 London boroughs</li>
      <li>We factor Party Wall timelines into the overall project schedule so there are no surprises</li>
    </ul>

    <div class="price-box reveal">
      <h4>Our drawing fees</h4>
      <div class="price-row">
        <span class="label">Essentials (planning drawings)</span>
        <span class="amount">from &pound;840</span>
      </div>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html?service=extension" class="btn btn-primary">Get a free quote &rarr;</a></p>
""",
    faqs=[
        ("When do I need a Party Wall notice in London?", "You need a Party Wall notice when your building work involves: (1) work directly on a shared wall (e.g. inserting a beam, raising the wall); (2) building a new wall on or at the boundary line; or (3) excavating within 3 metres of a neighbour's building below their foundation level, or within 6 metres under certain conditions. Most London extensions and loft conversions trigger at least one of these."),
        ("How much does a Party Wall surveyor cost?", "If the neighbour consents, there is no surveyor cost. If they dissent, an Agreed Surveyor costs &pound;1,000&ndash;&pound;1,500, while two separate surveyors cost &pound;1,500&ndash;&pound;2,500+ total. The building owner pays all reasonable surveyor fees."),
        ("How long does the Party Wall process take?", "Best case (neighbour consents): approximately 2 months from serving notice. Typical case (neighbour dissents): 2&ndash;4 months including surveyor appointment and Award preparation. We recommend serving notices early so the process runs in parallel with planning."),
        ("Can my neighbour stop my building work under the Party Wall Act?", "No. The Party Wall Act does not give the neighbour a right to prevent the work. It requires that their property is protected during the work. If they dissent from the notice, surveyors are appointed to prepare an Award that protects both parties, but the work can still proceed once the Award is in place."),
        ("What happens if I start work without a Party Wall notice?", "Starting without notice is a breach of the Act. Your neighbour can seek a court injunction to stop the work, claim damages, and appoint a surveyor at your expense. It is always cheaper and simpler to serve notice properly before starting work."),
    ],
    faq_schemas=[
        ("When do I need a Party Wall notice in London?", "You need a Party Wall notice when your building work involves: work directly on a shared wall, building a new wall on or at the boundary line, or excavating within 3 metres of a neighbour's building below their foundation level. Most London extensions and loft conversions trigger the Act."),
        ("How much does a Party Wall surveyor cost in London?", "If the neighbour consents, there is no cost. If they dissent, an Agreed Surveyor costs 1,000-1,500 pounds, while two separate surveyors cost 1,500-2,500+ pounds total. The building owner pays all reasonable surveyor fees."),
        ("How long does the Party Wall process take?", "Best case with neighbour consent: approximately 2 months. Typical case with dissent: 2-4 months including surveyor appointment and Award preparation. Serving notices early allows the process to run in parallel with planning permission."),
        ("Can my neighbour stop my building work under the Party Wall Act?", "No. The Party Wall Act does not give the neighbour a right to prevent the work. It requires that their property is protected during the work through a formal Award prepared by surveyors."),
        ("What happens if I start work without a Party Wall notice?", "Starting without notice is a breach of the Act. Your neighbour can seek a court injunction to stop the work, claim damages, and appoint a surveyor at your expense. It is always cheaper to serve notice properly before starting."),
    ],
    relateds=[
        ("side-return-extension-guide.html", "Side Return Extension Guide London", "Costs, planning vs PD, structural steel, Party Wall, kitchen design tips, rooflights..."),
        ("structural-engineer-guide.html", "Do I Need a Structural Engineer?", "When required, what they do, beam calcs, foundation design, costs, how to find one..."),
        ("how-long-planning-permission.html", "How Long Does Planning Take London 2026", "8-week householder, 13-week major, pre-app timelines, and borough-specific wait times..."),
    ],
    cta_h2='Need drawings for your <span class="accent">extension project?</span>',
    cta_p="Fixed fees from &pound;840. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.",
    cta1_href="../quote.html?service=extension",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services/house-extensions.html",
    cta2_text="Extension drawings service",
)

##############################################################################
# POST 5: structural-engineer-guide
##############################################################################
build(
    slug="structural-engineer-guide",
    title="Do I Need a Structural Engineer? London | AD",
    og_title="Do I Need a Structural Engineer for My London Project?",
    desc="When you need a structural engineer in London, what they do, beam calculations, foundation design, typical costs, and how to find a good one for your extension or loft conversion.",
    breadcrumb="Structural Engineer Guide",
    eyebrow="Guide",
    h1='Do I need a structural engineer? <em style="color: var(--accent); font-weight: 300;">London homeowner\'s guide</em>',
    minutes="14",
    tldrs=[
        "A structural engineer is needed for most extensions, loft conversions, and internal wall removals",
        "They design beams, foundations, and load paths &mdash; not the architectural design",
        "Typical costs: &pound;500&ndash;&pound;2,500 depending on project complexity",
        "Required for building regulations approval (Part A &mdash; Structure)",
        "Our Complete package includes structural calculations from &pound;1,750",
        "Always use a Chartered Engineer (CEng) or IStructE member",
    ],
    img_ph="IMAGE PLACEHOLDER -- structural engineer reviewing beam calculations at a construction site with exposed RSJ steelwork in a London terraced house",
    body="""
    <h2 id="what" class="reveal">What does a structural engineer do?</h2>

    <p>A structural engineer designs the structural elements of your building project -- the bones that hold everything up. While an architect or architectural technologist designs the layout, appearance, and spatial quality of your home, the structural engineer makes sure the building does not fall down.</p>

    <p>On a typical London residential project, the structural engineer's work includes:</p>

    <ul>
      <li><strong>Steel beam design (RSJs):</strong> calculating the size, grade, and bearing requirements of steel beams that replace load-bearing walls. This is the most common structural task in London home improvements -- opening up a kitchen by removing a wall requires a beam to carry the load above.</li>
      <li><strong>Foundation design:</strong> specifying the type, depth, and dimensions of foundations for extensions. In London, ground conditions vary significantly between boroughs, and clay soils (common in south and west London) require deeper foundations than sandy soils.</li>
      <li><strong>Load path analysis:</strong> tracing how loads (the weight of the roof, floors, walls, furniture, and people) travel through the building to the ground. This is essential when you change the structure -- removing a wall, adding a storey, or converting a loft.</li>
      <li><strong>Loft conversion steelwork:</strong> designing the steel beams and columns needed to support a new floor, new roof structure, and dormer or mansard walls.</li>
      <li><strong>Underpinning design:</strong> for basement conversions or when extending near trees on clay soil, the engineer may design underpinning to existing foundations.</li>
      <li><strong>Temporary works:</strong> specifying the propping and support needed during construction while walls are removed and beams installed.</li>
    </ul>


    <h2 id="when-needed" class="reveal">When do you need a structural engineer?</h2>

    <p>You need a structural engineer for any project that changes the structural behaviour of your building. In London residential work, the most common triggers are:</p>

    <h3>Extensions (rear, side return, wraparound)</h3>
    <p>Every extension needs foundations (designed by the engineer) and usually requires a steel beam where the extension meets the existing house (to open up the back wall). The engineer sizes the beam based on the loads above and specifies the foundation type and depth based on the ground conditions and proximity to trees.</p>

    <h3>Loft conversions</h3>
    <p>Loft conversions are structurally complex because you are converting a roof structure (designed only to support its own weight and wind loads) into a habitable floor (designed to support people, furniture, and partition walls). The engineer designs new floor joists or steels, reinforces the roof structure, and designs any dormer or mansard steelwork.</p>

    <h3>Internal wall removal</h3>
    <p>Removing a load-bearing wall to create an open-plan layout is one of the most common structural tasks in London. The engineer determines whether the wall is load-bearing (not always obvious), designs the replacement beam, specifies bearing pads, and provides drawings for building regulations and the builder.</p>

    <h3>Basement conversions</h3>
    <p>Basements are the most structurally complex residential project. The engineer designs underpinning to the existing foundations, waterproofing systems, retaining walls, and the new floor slab. In boroughs like Kensington and Chelsea, Camden, and Westminster, specialist basement engineers are essential. See our <a href="basement-conversion-guide-london.html">basement conversion guide</a>.</p>

    <h3>Mansard roofs</h3>
    <p>A mansard roof replaces the existing roof structure entirely. The engineer designs the new mansard walls (which are structural, not just cladding), the new roof structure, and any necessary reinforcement to the existing walls and foundations to support the additional weight.</p>


    <h2 id="costs" class="reveal">Structural engineer costs in London</h2>

    <div class="article-table-wrap reveal">
      <table class="article-table">
        <thead>
          <tr><th>Project type</th><th>Structural engineer fee</th></tr>
        </thead>
        <tbody>
          <tr><td>Single beam calculation (wall removal)</td><td>&pound;300&ndash;&pound;600</td></tr>
          <tr><td>Rear or side extension</td><td>&pound;800&ndash;&pound;1,500</td></tr>
          <tr><td>Loft conversion (dormer or Velux)</td><td>&pound;1,000&ndash;&pound;1,800</td></tr>
          <tr><td>Mansard roof conversion</td><td>&pound;1,200&ndash;&pound;2,000</td></tr>
          <tr><td>Basement conversion</td><td>&pound;2,000&ndash;&pound;5,000+</td></tr>
          <tr><td>Full structural package (extension + loft + internal alterations)</td><td>&pound;1,500&ndash;&pound;2,500</td></tr>
        </tbody>
      </table>
    </div>

    <p>Our Complete package from &pound;1,750 includes structural calculations as part of the building regulations submission. We work with a panel of experienced structural engineers across London and coordinate the structural design with our architectural drawings, so everything is consistent and submission-ready.</p>


    <h2 id="architect-vs-engineer" class="reveal">Architect vs structural engineer: what's the difference?</h2>

    <p>This is a common point of confusion. The architect (or architectural technologist) designs what your home looks like and how the spaces work -- the floor plan layout, the room sizes, the window positions, the materials. The structural engineer designs how the building stands up -- the beams, columns, foundations, and load paths.</p>

    <p>Both are essential. You cannot get building regulations approval without structural calculations. You cannot get planning permission without architectural drawings. On most London projects, the two professionals work together: the architect produces the design drawings, the structural engineer produces the structural calculations, and both are submitted together for building regulations approval.</p>

    <p>At Architectural Drawings London, we coordinate this process. When you choose our Complete package, we commission the structural engineer, coordinate the design, and submit everything as a single package. You do not need to find or manage the structural engineer yourself.</p>


    <h2 id="find" class="reveal">How to find a good structural engineer</h2>

    <p>If you need to find a structural engineer independently, look for:</p>

    <ul>
      <li><strong>Chartered status:</strong> CEng (Chartered Engineer) or IStructE (Institution of Structural Engineers) membership. These are the gold standards for structural engineering qualifications.</li>
      <li><strong>London residential experience:</strong> structural engineering for London terraced houses is different from new-build commercial work. Look for engineers who regularly work on Victorian and Edwardian properties.</li>
      <li><strong>Professional indemnity insurance:</strong> any structural engineer you use should carry PI insurance (minimum &pound;1 million). This protects you if there is an error in their calculations.</li>
      <li><strong>Clear communication:</strong> a good structural engineer explains their design decisions in plain English, not just in technical calculations. They should be willing to discuss options (e.g. steel beam vs timber beam) and their cost implications.</li>
      <li><strong>Reasonable turnaround:</strong> structural calculations for a typical extension or loft conversion should take 1&ndash;2 weeks. If an engineer is quoting 4&ndash;6 weeks, they may be overloaded.</li>
    </ul>

    <blockquote>We work with a panel of IStructE and ICE chartered structural engineers across London. When you instruct our Complete package from &pound;1,750, structural calculations are included -- we handle the coordination so you do not have to. <a href="../quote.html">Get a free quote</a>.</blockquote>


    <h2 id="building-regs" class="reveal">Structural engineers and building regulations</h2>

    <p>Structural calculations are required for building regulations approval under <strong>Part A (Structure)</strong> of the Building Regulations. The building control body (either the council's Building Control team or a private Approved Inspector) will review the structural engineer's calculations and drawings as part of the Full Plans application.</p>

    <p>Common structural elements reviewed include:</p>

    <ul>
      <li>Steel beam sizes and connections</li>
      <li>Foundation types, depths, and reinforcement</li>
      <li>Floor joist sizes and spans (especially in loft conversions)</li>
      <li>Roof structure adequacy</li>
      <li>Lateral stability (bracing to prevent the building from racking)</li>
      <li>Load calculations for new floors, walls, and roofs</li>
    </ul>

    <p>Without structural calculations, building control will not approve your plans, and your builder cannot legally start the structural work. This is not optional -- it is a legal requirement.</p>

    <div class="price-box reveal">
      <h4>Our fees (structural included)</h4>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
      <div class="price-row">
        <span class="label">Building regulations only (with structural)</span>
        <span class="amount">from &pound;1,225</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html" class="btn btn-primary">Get a free quote &rarr;</a></p>
""",
    faqs=[
        ("Do I need a structural engineer for a house extension?", "Yes. Every extension needs foundation design and usually a steel beam where the new extension meets the existing house. Structural calculations are required for building regulations approval under Part A (Structure). Our Complete package from &pound;1,750 includes structural calculations."),
        ("How much does a structural engineer cost in London?", "Costs range from &pound;300&ndash;&pound;600 for a single beam calculation to &pound;1,500&ndash;&pound;2,500 for a full structural package (extension + loft + internal alterations). Basement conversions can be &pound;2,000&ndash;&pound;5,000+. Our Complete package includes structural at &pound;1,750."),
        ("What is the difference between an architect and a structural engineer?", "The architect designs how your home looks and how the spaces work -- layouts, aesthetics, materials. The structural engineer designs how the building stands up -- beams, columns, foundations. Both are essential for most London projects."),
        ("Do I need a structural engineer to remove a wall?", "If the wall is load-bearing, yes. A structural engineer determines whether the wall is load-bearing, designs the replacement beam, specifies bearings, and provides calculations for building regulations. Not all internal walls are load-bearing -- the engineer will confirm."),
        ("How do I find a good structural engineer in London?", "Look for Chartered status (CEng or IStructE membership), London residential experience, professional indemnity insurance, and a reasonable turnaround of 1&ndash;2 weeks. Or instruct our Complete package and we coordinate the structural engineer for you."),
    ],
    faq_schemas=[
        ("Do I need a structural engineer for a house extension in London?", "Yes. Every extension needs foundation design and usually a steel beam calculation. Structural calculations are required for building regulations approval under Part A. A structural engineer for a London extension typically costs 800-1,500 pounds."),
        ("How much does a structural engineer cost in London?", "Costs range from 300-600 pounds for a single beam calculation to 1,500-2,500 pounds for a full structural package covering an extension, loft conversion, and internal alterations. Basement conversions can cost 2,000-5,000+ pounds."),
        ("What is the difference between an architect and a structural engineer?", "The architect designs how the home looks and functions -- layouts, aesthetics, materials. The structural engineer designs the structural elements -- beams, columns, foundations, load paths. Both are essential for most London residential projects."),
        ("Do I need a structural engineer to remove a load-bearing wall?", "Yes. A structural engineer determines whether the wall is load-bearing, designs the replacement steel beam, specifies bearing requirements, and provides calculations for building regulations approval."),
        ("How do I find a good structural engineer in London?", "Look for Chartered Engineer status (CEng) or IStructE membership, London residential experience, professional indemnity insurance of at least 1 million pounds, and a turnaround time of 1-2 weeks."),
    ],
    relateds=[
        ("party-wall-guide-london.html", "Party Wall Guide London 2026", "When notices are needed, the surveyor process, costs, timelines, and dispute resolution..."),
        ("extension-cost-guide-london.html", "House Extension Cost Guide London 2026", "Full cost breakdown for London extensions: build costs per sqm, drawing fees, hidden costs..."),
        ("hip-to-gable-loft-guide.html", "Hip to Gable Loft Conversion London", "What it is, PD rules, cost vs dormer, structural considerations for London semis..."),
    ],
    cta_h2='Need drawings with <span class="accent">structural included?</span>',
    cta_p="Complete package from &pound;1,750 includes architectural drawings, building regulations, and structural calculations.",
    cta1_href="../quote.html",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services/building-regulations.html",
    cta2_text="Building regulations service",
)

##############################################################################
# POST 6: garden-room-planning-london
##############################################################################
build(
    slug="garden-room-planning-london",
    title="Garden Room Planning Rules London 2026 | AD",
    og_title="Garden Room Planning Rules in London 2026: The Complete Guide",
    desc="Garden room planning rules in London 2026. Permitted Development limits for outbuildings, habitable vs incidental use, building regulations for heated spaces, costs, and design tips.",
    breadcrumb="Garden Room Planning Rules",
    eyebrow="Guide",
    h1='Garden room planning rules in London: <em style="color: var(--accent); font-weight: 300;">what you can build in 2026</em>',
    minutes="13",
    tldrs=[
        "Most garden rooms are Permitted Development (no planning needed)",
        "Maximum height: 2.5m within 2m of boundary, otherwise 4m (dual pitch) or 3m (flat/mono)",
        "Must be &ldquo;incidental to the dwelling&rdquo; &mdash; not a separate dwelling or bedroom",
        "Must not cover more than 50% of the garden area",
        "Building regs needed if heated, has plumbing, or is a sleeping accommodation",
        "Typical garden room cost: &pound;15,000&ndash;&pound;45,000 depending on size and spec",
    ],
    img_ph="IMAGE PLACEHOLDER -- contemporary garden room with floor-to-ceiling glazing in a London terraced house garden, used as a home office",
    body="""
    <h2 id="pd-rules" class="reveal">Permitted Development rules for garden rooms</h2>

    <p>Garden rooms, garden offices, studios, and outbuildings in London fall under <strong>Class E of Part 1</strong> of the General Permitted Development Order (GPDO). This means most garden rooms can be built without planning permission, provided they meet certain size and use conditions.</p>

    <h3>The key PD conditions</h3>

    <ul>
      <li><strong>Height limits:</strong> maximum 2.5 metres if within 2 metres of the boundary (measured to the highest point, including the roof). Otherwise, maximum 4 metres for a dual-pitch roof or 3 metres for a flat or mono-pitch roof.</li>
      <li><strong>Area limit:</strong> the garden room, combined with all other outbuildings, extensions, and additions, must not cover more than 50% of the total garden area (excluding the footprint of the original house).</li>
      <li><strong>Use:</strong> the building must be <strong>incidental to the enjoyment of the dwelling house</strong>. This means a home office, studio, gym, workshop, playroom, or garden room for relaxation. It does NOT mean a self-contained dwelling, a rental unit, a bedroom, or a commercial premises.</li>
      <li><strong>Location:</strong> the building must not be in front of the principal elevation (front of the house).</li>
      <li><strong>Not a flat:</strong> PD rights for outbuildings only apply to houses, not to flats or maisonettes.</li>
      <li><strong>Not a listed building:</strong> if your house is listed, any outbuilding within its curtilage may require listed building consent.</li>
    </ul>

    <h3>Conservation areas: additional restrictions</h3>

    <p>In conservation areas (which cover large parts of inner London), garden buildings are still generally PD under Class E, but with one important restriction: the building must not be more than 10 cubic metres in total volume if positioned to the side of the house. For rear gardens, the standard rules apply. However, some boroughs have Article 4 Directions that remove outbuilding PD rights in conservation areas.</p>


    <h2 id="habitable" class="reveal">Habitable vs incidental: the critical distinction</h2>

    <p>The most important planning rule for garden rooms is the "incidental" use test. This is where most homeowners get confused, and where councils are increasingly strict.</p>

    <h3>Incidental use (PD applies)</h3>

    <ul>
      <li>Home office or study</li>
      <li>Art or music studio</li>
      <li>Home gym</li>
      <li>Workshop or hobby room</li>
      <li>Garden room for relaxation, reading, entertaining</li>
      <li>Playroom for children</li>
      <li>Storage</li>
    </ul>

    <h3>Non-incidental use (planning permission required)</h3>

    <ul>
      <li>Self-contained dwelling (even for family members)</li>
      <li>Bedroom or sleeping accommodation</li>
      <li>Independent rental unit (Airbnb, lodger)</li>
      <li>Commercial premises open to the public</li>
      <li>Separate kitchen or bathroom that makes the building self-contained</li>
    </ul>

    <p>The test is about the use, not the specification. A garden room with a toilet and kitchenette used as a home office is incidental. The same building used as a self-contained flat for rental is not. Councils look at the totality of the arrangement: does the building have its own entrance, kitchen, bathroom, and sleeping area? If so, it is likely to be treated as a separate dwelling requiring planning permission and potentially council tax.</p>

    <blockquote>If you want to use a garden room as a <strong>home office</strong>, which is the most common use, it is almost certainly incidental and does not need planning permission (assuming it meets the PD size limits). We can confirm this for you as part of a free quote. <a href="../quote.html">Get started</a>.</blockquote>


    <h2 id="building-regs" class="reveal">Building regulations for garden rooms</h2>

    <p>Even if your garden room is Permitted Development and does not need planning permission, you may still need <strong>building regulations approval</strong> in certain circumstances:</p>

    <ul>
      <li><strong>Heated spaces:</strong> if the garden room has fixed heating (underfloor heating, radiators, electric panel heaters), it must comply with Part L (Conservation of fuel and power) of the Building Regulations. This means insulation levels, U-values, and air tightness standards must be met.</li>
      <li><strong>Sleeping accommodation:</strong> if anyone sleeps in the garden room (even occasionally), it must comply with Part B (Fire safety) -- including fire detection, escape routes, and fire-resistant construction.</li>
      <li><strong>Electrical work:</strong> any new electrical circuits must comply with Part P (Electrical safety) and be signed off by a registered electrician.</li>
      <li><strong>Plumbing:</strong> if the garden room has a toilet, sink, or shower, it must comply with Part G (Sanitation, hot water, and water efficiency) and Part H (Drainage).</li>
      <li><strong>Structural:</strong> if the garden room is large or has unusual spans, Part A (Structure) may apply.</li>
    </ul>

    <p>In practice, most modern insulated garden rooms with heating will need a building regulations application. Our <a href="../services/building-regulations.html">building regulations package</a> from &pound;1,225 covers this.</p>


    <h2 id="costs" class="reveal">Garden room costs in London</h2>

    <div class="price-box reveal">
      <h4>Typical garden room costs (2026)</h4>
      <div class="price-row">
        <span class="label">Basic insulated garden room (3m x 3m)</span>
        <span class="amount">&pound;15,000&ndash;&pound;22,000</span>
      </div>
      <div class="price-row">
        <span class="label">Mid-range with bi-folds (4m x 3m)</span>
        <span class="amount">&pound;22,000&ndash;&pound;32,000</span>
      </div>
      <div class="price-row">
        <span class="label">High-spec with green roof (5m x 4m)</span>
        <span class="amount">&pound;30,000&ndash;&pound;45,000</span>
      </div>
      <div class="price-row">
        <span class="label">Bespoke architect-designed</span>
        <span class="amount">&pound;40,000&ndash;&pound;60,000+</span>
      </div>
      <div class="price-row">
        <span class="label">Groundworks and foundations</span>
        <span class="amount">&pound;2,000&ndash;&pound;5,000</span>
      </div>
      <div class="price-row">
        <span class="label">Electrics (supply, lighting, sockets)</span>
        <span class="amount">&pound;1,500&ndash;&pound;3,000</span>
      </div>
    </div>


    <h2 id="design" class="reveal">Design considerations for London gardens</h2>

    <p>London gardens are typically small -- 6 to 12 metres deep and 4 to 6 metres wide for a Victorian terraced house. This constrains garden room design in several ways:</p>

    <ul>
      <li><strong>The 50% rule:</strong> your garden room cannot push you over the 50% coverage limit. Measure your total garden area and subtract all existing outbuildings, extensions, and sheds before sizing your garden room.</li>
      <li><strong>The 2-metre boundary rule:</strong> if the garden room is within 2 metres of any boundary (which it usually is in a London garden), the maximum height is 2.5 metres. This effectively limits you to a flat-roof design with about 2.3 metres of internal headroom -- tight but workable.</li>
      <li><strong>Overlooking:</strong> while not a PD condition, consider your neighbours' privacy. Large windows facing directly into a neighbour's garden or house can cause complaints and sour relationships, even if the building is technically PD.</li>
      <li><strong>Drainage:</strong> the garden room needs a surface water drainage strategy. In London's clay soils, a soakaway may not be effective, so you may need to connect to the existing surface water drain.</li>
      <li><strong>Green roofs:</strong> increasingly popular in London, green roofs (sedum or wildflower) improve biodiversity, manage surface water, and can be required by some boroughs for new outbuildings in certain areas.</li>
    </ul>


    <h2 id="our-service" class="reveal">How we can help</h2>

    <p>If your garden room needs planning permission (non-incidental use, listed building, or exceeds PD limits), we provide full planning drawings and submission. If it needs building regulations (heated, has plumbing, or is used for sleeping), we provide building regulations drawings and structural calculations.</p>

    <div class="price-box reveal">
      <h4>Our fees</h4>
      <div class="price-row">
        <span class="label">Essentials (planning drawings if needed)</span>
        <span class="amount">from &pound;840</span>
      </div>
      <div class="price-row">
        <span class="label">Building regulations drawings</span>
        <span class="amount">from &pound;1,225</span>
      </div>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html" class="btn btn-primary">Get a free quote &rarr;</a></p>
""",
    faqs=[
        ("Do I need planning permission for a garden room in London?", "Most garden rooms are Permitted Development and do not need planning permission, provided they meet the height, area, and use conditions. The key requirements: maximum 2.5m height within 2m of the boundary, must not cover more than 50% of the garden, and must be incidental to the dwelling (not a separate home or bedroom)."),
        ("Can I use a garden room as a bedroom?", "A garden room used as sleeping accommodation is generally not considered incidental to the dwelling and may require planning permission. It will also need building regulations approval for fire safety (Part B). If you want a habitable garden room with sleeping, consult us for a planning assessment."),
        ("Do I need building regulations for a garden room?", "Building regulations are needed if the garden room has fixed heating, plumbing, electrical circuits, or is used for sleeping. In practice, most modern insulated garden rooms with heating need a building regulations application for Part L (energy efficiency) and Part P (electrics)."),
        ("How close to the boundary can I build a garden room?", "You can build right up to the boundary, but if the garden room is within 2 metres of any boundary, the maximum height is 2.5 metres (to the ridge). Beyond 2 metres from the boundary, you can build up to 4 metres (dual pitch) or 3 metres (flat/mono pitch)."),
        ("How much does a garden room cost in London?", "A basic insulated garden room (3m x 3m) costs &pound;15,000&ndash;&pound;22,000. A mid-range garden room with bi-fold doors (4m x 3m) costs &pound;22,000&ndash;&pound;32,000. High-spec or bespoke designs range from &pound;30,000 to &pound;60,000+. Add &pound;2,000&ndash;&pound;5,000 for groundworks and &pound;1,500&ndash;&pound;3,000 for electrics."),
    ],
    faq_schemas=[
        ("Do I need planning permission for a garden room in London?", "Most garden rooms are Permitted Development and do not need planning. Key conditions: max 2.5m height within 2m of boundary, must not cover more than 50% of garden, must be incidental to dwelling. Conservation areas have additional side-extension restrictions."),
        ("Can I use a garden room as a bedroom in London?", "Using a garden room as sleeping accommodation generally requires planning permission as it is not considered incidental. It also needs building regulations for fire safety under Part B."),
        ("Do I need building regulations for a garden room?", "Yes, if the garden room has fixed heating, plumbing, electrical work, or sleeping use. Most modern insulated garden rooms with heating need building regulations for Part L energy efficiency and Part P electrical safety."),
        ("How close to the boundary can I build a garden room?", "You can build to the boundary, but within 2 metres the maximum height is 2.5 metres. Beyond 2 metres, up to 4 metres dual pitch or 3 metres flat roof."),
        ("How much does a garden room cost in London?", "Basic insulated garden rooms start at 15,000-22,000 pounds for a 3x3m unit. Mid-range with bi-folds costs 22,000-32,000 pounds. High-spec or bespoke designs range from 30,000 to 60,000+ pounds."),
    ],
    relateds=[
        ("permitted-development-rules-2026.html", "Permitted Development Rules 2026", "The complete guide to what you can build without planning permission in London..."),
        ("outbuilding-planning-guide.html", "Outbuilding Planning Guide London", "Planning rules for sheds, summerhouses, and garden buildings in London..."),
        ("flat-roof-extension-guide.html", "Flat Roof Extension London Guide", "Modern flat roof vs pitched, costs, planning, green roofs, drainage, insulation..."),
    ],
    cta_h2='Planning a <span class="accent">garden room?</span>',
    cta_p="Fixed fees from &pound;840. MCIAT chartered. We confirm your PD position and handle building regulations if needed.",
    cta1_href="../quote.html",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services.html",
    cta2_text="All our services",
)

##############################################################################
# POST 7: basement-conversion-guide-london
##############################################################################
build(
    slug="basement-conversion-guide-london",
    title="Basement Conversion London 2026 Guide | AD",
    og_title="Basement Conversion London 2026: The Complete Guide",
    desc="Complete guide to basement conversions in London. Cellar vs new dig, waterproofing, underpinning, costs (3-5k/sqm), planning, Party Wall, and borough-specific policies.",
    breadcrumb="Basement Conversion Guide",
    eyebrow="Guide",
    h1='Basement conversion in London: <em style="color: var(--accent); font-weight: 300;">the complete 2026 guide</em>',
    minutes="16",
    tldrs=[
        "Cellar conversion (existing cellar): &pound;1,500&ndash;&pound;2,500/sqm",
        "New basement dig (lowering floor): &pound;3,000&ndash;&pound;5,000/sqm",
        "Planning permission required in most London boroughs",
        "Party Wall Act almost always applies",
        "Waterproofing is critical &mdash; cavity drain or tanking system",
        "Several boroughs restrict new basements (RBKC, Camden, Westminster)",
    ],
    img_ph="IMAGE PLACEHOLDER -- cross-section diagram of a London terraced house showing a basement conversion with underpinning, waterproofing, and lightwell",
    body="""
    <h2 id="types" class="reveal">Cellar conversion vs new basement dig</h2>

    <p>There are two fundamentally different types of basement project in London, and the cost, complexity, and planning implications differ enormously.</p>

    <h3>Cellar conversion</h3>

    <p>Many London houses -- particularly Georgian and early Victorian properties -- already have a cellar. A cellar conversion transforms this existing underground space into a habitable room without significantly increasing the excavation depth. The work typically involves tanking or installing a cavity drain waterproofing system, improving ventilation, adding lighting and electrical services, insulating the walls and floor, and creating a proper staircase access.</p>

    <p>Cellar conversions are simpler, cheaper, and often do not require planning permission (the space already exists and the external appearance does not change). They typically cost <strong>&pound;1,500&ndash;&pound;2,500 per square metre</strong>.</p>

    <h3>New basement dig (lowering or new excavation)</h3>

    <p>A new basement dig involves excavating below the existing ground floor level to create a new basement storey. This is a major structural project that involves underpinning the existing foundations (so the house does not collapse into the hole), excavating and removing soil, constructing new retaining walls, installing waterproofing, and building a new reinforced concrete floor slab.</p>

    <p>New basement digs are complex, expensive, and almost always require planning permission. They typically cost <strong>&pound;3,000&ndash;&pound;5,000 per square metre</strong>, with total project costs for a typical London terraced house ranging from &pound;150,000 to &pound;400,000+.</p>


    <h2 id="costs" class="reveal">Basement conversion costs in London</h2>

    <div class="price-box reveal">
      <h4>Cost breakdown by type</h4>
      <div class="price-row">
        <span class="label">Cellar conversion (existing cellar, per sqm)</span>
        <span class="amount">&pound;1,500&ndash;&pound;2,500</span>
      </div>
      <div class="price-row">
        <span class="label">Floor lowering (existing cellar, increase height, per sqm)</span>
        <span class="amount">&pound;2,000&ndash;&pound;3,500</span>
      </div>
      <div class="price-row">
        <span class="label">New basement dig (no existing cellar, per sqm)</span>
        <span class="amount">&pound;3,000&ndash;&pound;5,000</span>
      </div>
      <div class="price-row">
        <span class="label">Lightwell excavation</span>
        <span class="amount">&pound;8,000&ndash;&pound;15,000</span>
      </div>
      <div class="price-row">
        <span class="label">Waterproofing (cavity drain system)</span>
        <span class="amount">&pound;3,000&ndash;&pound;8,000</span>
      </div>
      <div class="price-row">
        <span class="label">Structural engineer</span>
        <span class="amount">&pound;2,000&ndash;&pound;5,000</span>
      </div>
      <div class="price-row">
        <span class="label">Party Wall surveyors (both sides)</span>
        <span class="amount">&pound;2,000&ndash;&pound;5,000</span>
      </div>
      <div class="price-row">
        <span class="label">Architectural drawings (our fees)</span>
        <span class="amount">&pound;1,750&ndash;&pound;3,500</span>
      </div>
    </div>


    <h2 id="planning" class="reveal">Planning permission for basements in London</h2>

    <p>Whether you need planning permission depends on the type of basement project and the borough:</p>

    <h3>Cellar conversion (no external changes)</h3>
    <p>If you are converting an existing cellar without any external changes (no lightwell, no changes to the front area, no extension of the basement footprint), you typically do <strong>not</strong> need planning permission. The work is treated as an internal alteration. However, you will need building regulations approval.</p>

    <h3>New basement dig or external changes</h3>
    <p>If you are digging a new basement, lowering the floor level, adding a lightwell, or making any external changes, you will almost certainly need <strong>planning permission</strong>. Many London boroughs have specific basement policies that go beyond general planning rules.</p>

    <h3>Borough-specific basement policies</h3>

    <p>Several London boroughs have introduced or strengthened basement policies due to the disruption caused by large-scale basement projects:</p>

    <ul>
      <li><strong>Kensington and Chelsea (RBKC):</strong> restricts basements to a single storey below the original lowest floor level. No multi-storey or "iceberg" basements. Maximum 50% of the garden at basement level. Construction management plans required.</li>
      <li><strong>Camden:</strong> restrictive policy on basements -- limits on size, requires construction impact assessments, and restricts basements under gardens.</li>
      <li><strong>Westminster:</strong> detailed basement policy requiring structural methodology statements, construction management plans, and restrictions on size.</li>
      <li><strong>Islington:</strong> generally permits single-storey basements but requires detailed structural and drainage assessments.</li>
      <li><strong>Wandsworth:</strong> relatively permissive but requires detailed applications for new basement excavations.</li>
    </ul>


    <h2 id="waterproofing" class="reveal">Waterproofing: the most critical element</h2>

    <p>Waterproofing is not an optional extra for a London basement -- it is the single most important element of the project. London's clay soils hold water, and the water table is relatively high in many areas. A basement that is not properly waterproofed will leak, and the damage from water ingress can be catastrophic.</p>

    <h3>The three approaches</h3>

    <ol>
      <li><strong>Type A -- Tanked protection (barrier):</strong> a waterproof membrane applied to the external face of the walls and under the floor. Effective but relies on the membrane being continuous and undamaged. Difficult to repair if it fails.</li>
      <li><strong>Type B -- Structurally integral (waterproof concrete):</strong> the basement structure itself is made waterproof using specialist concrete mixes and construction techniques. Requires very high-quality workmanship.</li>
      <li><strong>Type C -- Drained protection (cavity drain):</strong> a dimpled membrane is fitted to the internal walls and floor, creating a cavity that collects any water ingress and channels it to a sump pump, which pumps it to a drain. This is the most common system in London because it is the most forgiving -- it does not try to stop water entering, it manages it.</li>
    </ol>

    <p>Most London basement specialists recommend a <strong>combination approach</strong>: Type C cavity drain system with a Type A or B external barrier as a belt-and-braces solution. Always insist on a 10-year insurance-backed waterproofing guarantee.</p>


    <h2 id="party-wall" class="reveal">Party Wall implications</h2>

    <p>Basement conversions almost always trigger the <a href="party-wall-guide-london.html">Party Wall Act</a>. Underpinning the existing foundations involves excavating within 3 metres of your neighbour's building below their foundation level (Section 6). If the party wall between your house and the neighbour's is being underpinned, Section 2 also applies.</p>

    <p>Party Wall surveyor costs for basement projects are typically higher than for simple extensions because the work is more complex and the risk to the neighbouring property is greater. Budget <strong>&pound;2,000&ndash;&pound;5,000</strong> for Party Wall costs on a basement project.</p>


    <h2 id="structural" class="reveal">Structural engineering</h2>

    <p>A basement conversion requires specialist <a href="structural-engineer-guide.html">structural engineering</a>. The engineer designs:</p>

    <ul>
      <li>The underpinning sequence (which sections of foundation are underpinned first, and in what order, to prevent settlement)</li>
      <li>The retaining wall design (to resist the lateral pressure of the surrounding soil)</li>
      <li>The reinforced concrete floor slab</li>
      <li>Any new internal columns or beams</li>
      <li>Temporary works (propping and shoring during construction)</li>
    </ul>

    <p>Structural engineer fees for basement projects are &pound;2,000&ndash;&pound;5,000+. We coordinate with specialist basement engineers as part of our service.</p>

    <div class="price-box reveal">
      <h4>Our drawing fees for basements</h4>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
      <div class="price-row">
        <span class="label">Complex basement projects</span>
        <span class="amount">quoted individually</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html" class="btn btn-primary">Get a free quote &rarr;</a></p>
""",
    faqs=[
        ("How much does a basement conversion cost in London?", "A cellar conversion costs &pound;1,500&ndash;&pound;2,500 per sqm. A new basement dig costs &pound;3,000&ndash;&pound;5,000 per sqm. A typical London terraced house basement (40&ndash;60 sqm) ranges from &pound;150,000 to &pound;400,000+ total including waterproofing, structural engineering, Party Wall, and professional fees."),
        ("Do I need planning permission for a basement conversion?", "A simple cellar conversion with no external changes typically does not need planning. A new basement dig, floor lowering, or any external changes (lightwells, garden excavation) almost always require planning. Several boroughs (RBKC, Camden, Westminster) have specific restrictive basement policies."),
        ("What waterproofing system is best for a London basement?", "Most London specialists recommend a Type C cavity drain system, often combined with an external barrier (Type A). The cavity drain system manages water rather than trying to stop it, which is more forgiving in London&rsquo;s clay soils. Always insist on a 10-year insurance-backed guarantee."),
        ("Does the Party Wall Act apply to basement conversions?", "Yes, almost always. Underpinning foundations involves excavating within 3 metres of your neighbour at a depth below their foundations (Section 6). If you are also working on the shared party wall, Section 2 applies. Budget &pound;2,000&ndash;&pound;5,000 for Party Wall costs."),
        ("Which London boroughs restrict basement conversions?", "Kensington and Chelsea, Camden, and Westminster have the most restrictive basement policies, limiting basements to single storey and imposing construction management requirements. Islington and other boroughs have lighter-touch policies but still require detailed applications."),
    ],
    faq_schemas=[
        ("How much does a basement conversion cost in London?", "A cellar conversion costs 1,500-2,500 pounds per sqm. A new basement dig costs 3,000-5,000 pounds per sqm. Total costs for a typical London terraced house range from 150,000 to 400,000+ pounds including all professional fees."),
        ("Do I need planning permission for a basement conversion in London?", "Simple cellar conversions without external changes typically do not need planning. New basement digs, floor lowering, or external changes almost always require planning. RBKC, Camden, and Westminster have specific restrictive basement policies."),
        ("What waterproofing system is best for a London basement?", "Most specialists recommend a Type C cavity drain system combined with an external barrier. This manages water rather than trying to stop it, which is more reliable in London clay soils. Always require a 10-year insurance-backed guarantee."),
        ("Does the Party Wall Act apply to basement conversions?", "Yes, almost always. Underpinning involves excavating near neighbours at depth. Budget 2,000-5,000 pounds for Party Wall surveyor costs on a basement project."),
        ("Which London boroughs restrict basement conversions?", "Kensington and Chelsea, Camden, and Westminster have the most restrictive policies, limiting basements to single storey with construction management requirements."),
    ],
    relateds=[
        ("party-wall-guide-london.html", "Party Wall Guide London 2026", "When notices are needed, the surveyor process, costs, timelines, and dispute resolution..."),
        ("structural-engineer-guide.html", "Do I Need a Structural Engineer?", "When required, what they do, beam calcs, foundation design, costs, how to find one..."),
        ("extension-cost-guide-london.html", "House Extension Cost Guide London 2026", "Full cost breakdown for London extensions: build costs per sqm, drawing fees..."),
    ],
    cta_h2='Planning a <span class="accent">basement project?</span>',
    cta_p="Fixed fees from &pound;1,750. MCIAT chartered. We coordinate structural engineers and manage the planning process.",
    cta1_href="../quote.html",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services/building-regulations.html",
    cta2_text="Building regulations service",
)

##############################################################################
# POST 8: hip-to-gable-loft-guide
##############################################################################
build(
    slug="hip-to-gable-loft-guide",
    title="Hip to Gable Loft Conversion London | AD",
    og_title="Hip to Gable Loft Conversion in London: The Complete Guide",
    desc="Hip to gable loft conversion guide for London. What it is, PD rules (semis and detached only), cost vs dormer, structural design, and how it maximises loft space.",
    breadcrumb="Hip to Gable Loft Guide",
    eyebrow="Guide",
    h1='Hip to gable loft conversion in London: <em style="color: var(--accent); font-weight: 300;">maximise your loft space</em>',
    minutes="13",
    tldrs=[
        "Hip to gable extends the sloping hip end of a roof to a vertical gable wall",
        "Only available for semi-detached and detached houses (not terraced)",
        "Usually Permitted Development (no planning permission needed)",
        "Cost: &pound;45,000&ndash;&pound;65,000 including all finishes",
        "Often combined with a rear dormer for maximum space",
        "Structural design required &mdash; new gable wall carries roof loads",
    ],
    img_ph="IMAGE PLACEHOLDER -- before and after 3D render showing a London semi-detached house with a hipped roof converted to a gable end with rear dormer",
    body="""
    <h2 id="what" class="reveal">What is a hip to gable loft conversion?</h2>

    <p>A hip to gable conversion is a type of loft conversion that extends the sloping hip end of a roof outwards to create a vertical gable wall. The "hip" is the sloping triangular section at the side of the roof (where the roof slopes inward to meet the ridge). By replacing this slope with a vertical wall (the "gable"), you create a much larger, more usable loft space with full head height extending right to the side wall of the house.</p>

    <p>This type of conversion is most commonly done on <strong>semi-detached houses</strong>, where one end of the roof is hipped (the side not adjoining the neighbour). It can also be done on detached houses, which may have hipped ends on both sides. It is <strong>not possible on terraced houses</strong>, which do not have hipped ends.</p>

    <p>In London, hip to gable conversions are extremely popular on 1930s semi-detached houses in outer boroughs like Barnet, Ealing, Hounslow, Bromley, Croydon, and Merton, where this house type dominates.</p>


    <h2 id="pd" class="reveal">Permitted Development rules</h2>

    <p>Hip to gable loft conversions typically fall under <strong>Permitted Development</strong> (Class B of Part 1 of the GPDO), meaning no planning application is needed. The key conditions are:</p>

    <ul>
      <li>The additional roof space created must not exceed <strong>50 cubic metres</strong> for a semi-detached house or <strong>50 cubic metres</strong> for a detached house (this is a generous allowance that most hip to gable conversions fall within)</li>
      <li>The new gable wall must not extend beyond the plane of the existing front elevation</li>
      <li>The new gable wall must not be higher than the highest part of the existing roof</li>
      <li>Materials used on the exterior must be similar in appearance to the existing house</li>
      <li>No verandas, balconies, or raised platforms</li>
      <li>Side-facing windows must be obscure-glazed and non-opening below 1.7m from the floor</li>
      <li>The property must not be in a conservation area with an Article 4 Direction that removes roof extension PD rights</li>
    </ul>

    <blockquote>We always recommend a <strong>Lawful Development Certificate</strong> (&pound;129 council fee) for hip to gable conversions. This provides legal proof that the conversion is PD, which is invaluable when you come to sell the property. We can prepare and submit the LDC application as part of our service.</blockquote>


    <h2 id="cost" class="reveal">Hip to gable costs in London</h2>

    <div class="article-table-wrap reveal">
      <table class="article-table">
        <thead>
          <tr><th>Cost element</th><th>Typical range</th></tr>
        </thead>
        <tbody>
          <tr><td>Build cost (hip to gable only)</td><td>&pound;35,000&ndash;&pound;50,000</td></tr>
          <tr><td>Build cost (hip to gable + rear dormer)</td><td>&pound;45,000&ndash;&pound;65,000</td></tr>
          <tr><td>Architectural drawings (our fees)</td><td>&pound;840&ndash;&pound;1,750</td></tr>
          <tr><td>Building regulations + structural</td><td>from &pound;1,225</td></tr>
          <tr><td>Bathroom fit-out (en-suite)</td><td>&pound;4,000&ndash;&pound;8,000</td></tr>
          <tr><td>Staircase</td><td>&pound;2,000&ndash;&pound;4,000</td></tr>
          <tr><td>Electrics and plumbing</td><td>&pound;3,000&ndash;&pound;5,000</td></tr>
          <tr><td>Plastering and decoration</td><td>&pound;2,000&ndash;&pound;4,000</td></tr>
          <tr><td><strong>Total project cost</strong></td><td><strong>&pound;55,000&ndash;&pound;80,000</strong></td></tr>
        </tbody>
      </table>
    </div>


    <h2 id="vs-dormer" class="reveal">Hip to gable vs dormer: what is the difference?</h2>

    <p>A hip to gable and a rear dormer are complementary, not competing, options. Most hip to gable conversions in London also include a rear dormer to maximise the loft space. Here is how they compare:</p>

    <ul>
      <li><strong>Hip to gable:</strong> extends the side of the roof from a slope to a vertical wall. Gains width and headroom at the sides of the loft. Most effective on semi-detached houses with hipped roofs.</li>
      <li><strong>Rear dormer:</strong> a box-shaped extension from the rear roof slope. Gains depth, headroom, and floor area across the back of the loft. Can be done on any house type (terraced, semi, or detached).</li>
      <li><strong>Combined hip to gable + rear dormer:</strong> the most common configuration for semi-detached houses in London. The hip to gable provides width; the dormer provides depth. Together, they create a loft with a usable floor area similar to the first floor below.</li>
    </ul>

    <p>For our detailed comparison of dormer types, see our <a href="dormer-vs-velux-loft.html">dormer vs Velux loft conversion guide</a>.</p>


    <h2 id="structural" class="reveal">Structural considerations</h2>

    <p>A hip to gable conversion is a significant structural alteration. The new gable wall replaces the hipped roof rafters and must carry the roof loads that were previously distributed across the hip. A <a href="structural-engineer-guide.html">structural engineer</a> designs:</p>

    <ul>
      <li><strong>The new gable wall:</strong> typically blockwork or timber frame with a brick or render external finish to match the existing house</li>
      <li><strong>A steel beam or ridge beam:</strong> to support the ridge where it previously met the hip</li>
      <li><strong>New floor joists:</strong> the existing ceiling joists in a hipped roof area are rarely adequate to support a habitable floor; the engineer specifies new joists or steel beams</li>
      <li><strong>Lateral bracing:</strong> to ensure the new gable wall is stable against wind loads</li>
      <li><strong>Foundation check:</strong> the existing external wall below the new gable must be capable of supporting the additional load; the engineer verifies this</li>
    </ul>


    <h2 id="process" class="reveal">Our design process for hip to gable</h2>

    <p>We have designed hip to gable conversions across all 33 London boroughs. Our process:</p>

    <ol>
      <li><strong>Measured survey</strong> of the existing property (included in all packages)</li>
      <li><strong>Design development</strong> -- we produce floor plans, elevations, and sections showing the proposed conversion, dormer (if included), staircase position, and room layout</li>
      <li><strong>PD assessment</strong> -- we confirm the conversion is Permitted Development and prepare a Lawful Development Certificate application if needed</li>
      <li><strong>Building regulations drawings</strong> -- detailed construction drawings and structural calculations for building control approval</li>
      <li><strong>Submission and liaison</strong> -- we submit all applications and manage the approval process</li>
    </ol>

    <div class="price-box reveal">
      <h4>Loft conversion drawing fees</h4>
      <div class="price-row">
        <span class="label">Essentials (planning/LDC drawings)</span>
        <span class="amount">from &pound;840</span>
      </div>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,225</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html?service=loft" class="btn btn-primary">Get a free quote for your loft &rarr;</a></p>
""",
    faqs=[
        ("What is a hip to gable loft conversion?", "A hip to gable conversion extends the sloping hip end of a roof outwards to create a vertical gable wall, dramatically increasing usable loft space. It is most common on semi-detached houses with hipped roofs and is often combined with a rear dormer for maximum space."),
        ("Do I need planning permission for a hip to gable in London?", "Most hip to gable conversions are Permitted Development and do not need planning permission, provided they stay within the 50 cubic metre volume allowance and meet the other PD conditions. Properties in conservation areas with Article 4 Directions may need planning. We recommend a Lawful Development Certificate for legal proof."),
        ("How much does a hip to gable loft conversion cost?", "A hip to gable conversion in London typically costs &pound;35,000&ndash;&pound;50,000 for the build. Combined with a rear dormer, the total build cost is &pound;45,000&ndash;&pound;65,000. Including all finishes, bathroom, staircase, and professional fees, the total project cost is &pound;55,000&ndash;&pound;80,000."),
        ("Can I do a hip to gable on a terraced house?", "No. Terraced houses have party walls on both sides and do not have hipped roof ends. Hip to gable conversions are only possible on semi-detached houses (one hip end) and detached houses (potentially both hip ends). Terraced houses typically use rear dormers or mansard conversions instead."),
        ("Is a hip to gable better than a dormer?", "They serve different purposes and are often combined. A hip to gable gives width and headroom at the side; a dormer gives depth and headroom at the rear. The most popular configuration for London semi-detached houses is hip to gable plus rear dormer, which maximises the usable loft floor area."),
    ],
    faq_schemas=[
        ("What is a hip to gable loft conversion?", "A hip to gable conversion extends the sloping hip end of a roof to a vertical gable wall, increasing usable loft space. It is most common on semi-detached houses and often combined with a rear dormer."),
        ("Do I need planning permission for a hip to gable conversion in London?", "Most hip to gable conversions are Permitted Development within the 50 cubic metre volume allowance. Properties in conservation areas with Article 4 Directions may need planning permission."),
        ("How much does a hip to gable loft conversion cost in London?", "Build cost is 35,000-50,000 pounds for hip to gable alone, or 45,000-65,000 combined with a rear dormer. Total project cost including finishes is 55,000-80,000 pounds."),
        ("Can you do a hip to gable on a terraced house?", "No. Terraced houses do not have hipped roof ends. Hip to gable is only for semi-detached and detached houses. Terraced houses use rear dormers or mansard conversions."),
        ("Is a hip to gable better than a dormer loft conversion?", "They serve different purposes and are often combined. Hip to gable gives width at the side; a dormer gives depth at the rear. Combined, they maximise usable loft space."),
    ],
    relateds=[
        ("dormer-vs-velux-loft.html", "Dormer vs Velux Loft Conversion", "Which loft conversion type is right for your London home? Cost, space, and planning comparison..."),
        ("loft-vs-mansard.html", "Loft Conversion vs Mansard Extension", "Comparing standard loft conversions with mansard roof extensions in London..."),
        ("structural-engineer-guide.html", "Do I Need a Structural Engineer?", "When required, what they do, beam calcs, foundation design, costs, how to find one..."),
    ],
    cta_h2='Ready to convert your <span class="accent">loft?</span>',
    cta_p="Fixed fees from &pound;840. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.",
    cta1_href="../quote.html?service=loft",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services/loft-conversions.html",
    cta2_text="Loft conversion service",
)

##############################################################################
# POST 9: flat-roof-extension-guide
##############################################################################
build(
    slug="flat-roof-extension-guide",
    title="Flat Roof Extension London 2026 | AD",
    og_title="Flat Roof Extension in London 2026: The Complete Guide",
    desc="Flat roof extension guide for London homeowners. Modern flat roof vs pitched, costs, planning rules, green roofs, parapets, drainage, and Part L insulation requirements.",
    breadcrumb="Flat Roof Extension Guide",
    eyebrow="Guide",
    h1='Flat roof extension in London: <em style="color: var(--accent); font-weight: 300;">modern design that works</em>',
    minutes="12",
    tldrs=[
        "Flat roofs are the most common extension roof type in London",
        "Modern flat roofs use single-ply membrane (EPDM, TPO) with 20&ndash;30 year guarantees",
        "Must have a minimum fall of 1:40 (not truly flat &mdash; water must drain)",
        "Parapets create a clean, modern edge and hide the roof from street level",
        "Part L 2021 insulation: U-value of 0.18 W/m&sup2;K or better for flat roofs",
        "Green roofs (sedum) increasingly popular and sometimes required by boroughs",
    ],
    img_ph="IMAGE PLACEHOLDER -- contemporary single-storey rear extension with a flat roof, parapet edge, and rooflight on a London Victorian terraced house",
    body="""
    <h2 id="why-flat" class="reveal">Why flat roofs dominate London extensions</h2>

    <p>Walk through any residential street in London and look at the rear of the houses. The vast majority of single-storey extensions have flat roofs. This is not a compromise -- it is a deliberate design choice driven by planning policy, practical constraints, and modern aesthetics.</p>

    <h3>Planning reasons</h3>
    <p>Under <a href="permitted-development-rules-2026.html">Permitted Development</a>, single-storey rear extensions have a maximum eaves height of 3 metres. A pitched roof at this eaves height creates a ridge that is higher than 4 metres (the overall height limit), so it often will not fit. A flat roof keeps the overall height at or below 3 metres, comfortably within PD limits.</p>

    <h3>Neighbour impact</h3>
    <p>A flat roof is lower than a pitched roof, which means less impact on neighbours in terms of overshadowing and visual dominance. This makes planning approval easier even when a full planning application is required.</p>

    <h3>Design appeal</h3>
    <p>Modern flat-roof extensions have a clean, contemporary aesthetic that contrasts attractively with the traditional pitched roofs of Victorian and Edwardian houses. With a parapet edge (a low wall around the perimeter of the roof), rooflights, and high-quality glazing, a flat-roof extension can transform the rear of a period property.</p>


    <h2 id="construction" class="reveal">Modern flat roof construction</h2>

    <p>The flat roofs of the 1960s and 1970s had a terrible reputation for leaking. Modern flat roof construction is entirely different and, when properly specified and installed, is extremely reliable.</p>

    <h3>Structure</h3>
    <p>The roof structure is typically engineered timber joists (or steel beams for larger spans) with a plywood or OSB deck. The joists are sized to carry the dead load (the weight of the roof itself, insulation, and any green roof) and the imposed load (snow, maintenance access).</p>

    <h3>Insulation</h3>
    <p>Modern building regulations (Part L 2021) require a U-value of <strong>0.18 W/m&sup2;K or better</strong> for a new flat roof. This typically requires 120&ndash;160mm of rigid insulation (PIR board such as Kingspan or Celotex) above the deck. The insulation is installed as a "warm roof" -- above the structure, below the membrane -- which is the modern standard and prevents condensation.</p>

    <h3>Membrane</h3>
    <p>The waterproofing membrane is the critical layer. Modern options include:</p>

    <ul>
      <li><strong>EPDM (ethylene propylene diene monomer):</strong> a synthetic rubber membrane. Very durable, UV-resistant, and comes in large sheets that reduce the number of joints. Lifespan: 30&ndash;50 years. This is the most common choice for residential flat roofs.</li>
      <li><strong>TPO (thermoplastic polyolefin):</strong> a white or light-coloured membrane that reflects heat. Hot-air welded seams are extremely strong. Lifespan: 25&ndash;30 years.</li>
      <li><strong>GRP (glass-reinforced plastic):</strong> a fibreglass system laid in situ. Very hard-wearing and can be walked on. Lifespan: 25&ndash;30 years. More expensive than EPDM.</li>
      <li><strong>Single-ply PVC:</strong> similar to TPO but with added plasticisers. Common on commercial roofs but also used on residential. Lifespan: 20&ndash;25 years.</li>
    </ul>


    <h2 id="drainage" class="reveal">Drainage design</h2>

    <p>A flat roof is not actually flat. It must have a <strong>minimum fall of 1:40</strong> (some designers specify 1:60, but 1:40 is safer) to ensure water drains to the outlet rather than ponding. The fall is created using tapered insulation boards or by setting the joists at a slight angle.</p>

    <p>Drainage options include:</p>

    <ul>
      <li><strong>Internal outlet:</strong> a circular drain in the roof surface, connected to a downpipe that runs inside or alongside the building. Clean and discreet.</li>
      <li><strong>External gutter and downpipe:</strong> a conventional gutter at the low edge of the roof. Less visually clean but simpler to install and maintain.</li>
      <li><strong>Overflow outlets:</strong> building regulations require overflow outlets positioned 25mm below the main outlet level, discharging visibly to the outside so you can see if the main drain is blocked.</li>
    </ul>


    <h2 id="parapets" class="reveal">Parapets: the design detail that makes the difference</h2>

    <p>A parapet is a low wall around the edge of the flat roof, typically 150&ndash;300mm above the roof surface. Parapets serve three functions:</p>

    <ul>
      <li><strong>Aesthetics:</strong> the parapet hides the roof membrane, flashing, and any green roof substrate from view, creating a clean, sharp edge when viewed from the garden or from upper floor windows. This is the single most important design detail for a modern flat-roof extension.</li>
      <li><strong>Weather protection:</strong> the parapet provides an upstand at the edge of the roof, preventing water from running over the edge and staining the walls.</li>
      <li><strong>Safety:</strong> on roofs that may be accessed for maintenance, the parapet provides a low barrier.</li>
    </ul>

    <p>Parapets are typically formed in blockwork or timber frame, rendered or clad to match the extension walls. The top of the parapet has a coping (a cap to shed water) in stone, metal, or precast concrete.</p>


    <h2 id="green-roofs" class="reveal">Green roofs</h2>

    <p>Green roofs -- roofs covered with sedum, wildflower, or other planting -- are increasingly popular on London flat-roof extensions. Some boroughs (particularly in areas with biodiversity action plans) actively encourage or require green roofs on new flat-roof extensions.</p>

    <h3>Benefits</h3>
    <ul>
      <li><strong>Surface water management:</strong> a green roof absorbs and slows rainwater, reducing the load on drains. This can be a planning benefit in areas with surface water flooding risk.</li>
      <li><strong>Biodiversity:</strong> provides habitat for bees, butterflies, and birds.</li>
      <li><strong>Thermal performance:</strong> the soil and planting provide additional insulation, reducing heat gain in summer.</li>
      <li><strong>Visual amenity:</strong> a green roof looks better than a black membrane when viewed from upper floors or neighbouring properties.</li>
    </ul>

    <h3>Costs</h3>
    <p>A sedum green roof system (substrate, drainage layer, filter fleece, and pre-grown sedum mat) costs &pound;50&ndash;&pound;100 per square metre installed. For a 20 sqm extension, that is &pound;1,000&ndash;&pound;2,000 -- a modest addition to the total project cost.</p>

    <p>The roof structure must be designed to support the additional weight (a saturated sedum roof weighs approximately 80&ndash;120 kg/sqm). This is factored into the structural design.</p>


    <h2 id="costs" class="reveal">Flat roof extension costs in London</h2>

    <div class="price-box reveal">
      <h4>Cost comparison: flat roof options</h4>
      <div class="price-row">
        <span class="label">EPDM membrane flat roof (per sqm)</span>
        <span class="amount">&pound;80&ndash;&pound;120</span>
      </div>
      <div class="price-row">
        <span class="label">GRP fibreglass flat roof (per sqm)</span>
        <span class="amount">&pound;100&ndash;&pound;150</span>
      </div>
      <div class="price-row">
        <span class="label">Green roof system (per sqm)</span>
        <span class="amount">&pound;50&ndash;&pound;100</span>
      </div>
      <div class="price-row">
        <span class="label">Rooflight (fixed, per unit)</span>
        <span class="amount">&pound;600&ndash;&pound;2,000</span>
      </div>
      <div class="price-row">
        <span class="label">Parapet construction (per linear metre)</span>
        <span class="amount">&pound;150&ndash;&pound;300</span>
      </div>
    </div>

    <p>These are roof-specific costs only. For total extension costs including build, structural, and professional fees, see our <a href="extension-cost-guide-london.html">extension cost guide</a>.</p>

    <div class="price-box reveal">
      <h4>Our drawing fees</h4>
      <div class="price-row">
        <span class="label">Essentials (planning drawings)</span>
        <span class="amount">from &pound;840</span>
      </div>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html?service=extension" class="btn btn-primary">Get a free quote &rarr;</a></p>
""",
    faqs=[
        ("Are flat roof extensions any good?", "Yes. Modern flat roofs use single-ply membranes (EPDM, TPO) with 20&ndash;30 year guarantees and are extremely reliable when properly specified. They are the most common extension roof type in London because they work within PD height limits, minimise neighbour impact, and create a clean modern aesthetic."),
        ("How long does a flat roof last?", "A modern EPDM membrane flat roof lasts 30&ndash;50 years. TPO and GRP systems last 25&ndash;30 years. The key is correct installation with proper falls (minimum 1:40), adequate drainage outlets, and overflow provision. Old-style felt flat roofs that leaked have been entirely replaced by these modern systems."),
        ("Do flat roof extensions need planning permission?", "Most single-storey flat roof rear extensions fall under Permitted Development if they meet the height and depth limits. The flat roof is actually an advantage for PD because it keeps the overall height below 3 metres, well within the 4-metre PD limit. Conservation areas may require planning for side extensions."),
        ("What insulation does a flat roof extension need?", "Under Part L 2021, flat roofs on new extensions need a U-value of 0.18 W/m&sup2;K or better. This typically requires 120&ndash;160mm of PIR rigid insulation (Kingspan, Celotex) installed as a warm roof above the deck and below the membrane. Our building regulations drawings specify the correct insulation build-up."),
        ("Should I get a green roof on my extension?", "Green roofs (sedum) cost &pound;50&ndash;&pound;100 per sqm installed and offer genuine benefits: surface water management, biodiversity, thermal performance, and a better view from upper floors. Some London boroughs encourage or require them. They add modest cost (&pound;1,000&ndash;&pound;2,000 for a typical extension) for significant benefits."),
    ],
    faq_schemas=[
        ("Are modern flat roof extensions reliable?", "Yes. Modern flat roofs use single-ply membranes like EPDM and TPO with 20-50 year lifespans. They are the most common extension roof type in London because they meet PD height limits and create a clean modern look."),
        ("How long does a modern flat roof last?", "EPDM membranes last 30-50 years. TPO and GRP systems last 25-30 years. Correct installation with proper falls and drainage is key to longevity."),
        ("Do flat roof extensions need planning permission in London?", "Most single-storey flat roof rear extensions are Permitted Development. The flat roof helps meet PD height limits as it keeps overall height below 3 metres."),
        ("What insulation is required for a flat roof extension?", "Part L 2021 requires a U-value of 0.18 W/m2K or better, typically needing 120-160mm of PIR rigid insulation installed as a warm roof above the deck."),
        ("Should I install a green roof on my London extension?", "Green roofs cost 50-100 pounds per sqm and offer surface water management, biodiversity, and thermal benefits. Some London boroughs encourage or require them on new extensions."),
    ],
    relateds=[
        ("rear-vs-side-extension.html", "Rear vs Side Extension London", "Which adds more space? Cost comparison, planning, and design impact for London homes..."),
        ("extension-cost-guide-london.html", "House Extension Cost Guide London 2026", "Full cost breakdown for London extensions: build costs per sqm, drawing fees..."),
        ("garden-room-planning-london.html", "Garden Room Planning Rules London", "PD limits for outbuildings, habitable vs incidental, building regs, costs..."),
    ],
    cta_h2='Planning a flat roof <span class="accent">extension?</span>',
    cta_p="Fixed fees from &pound;840. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.",
    cta1_href="../quote.html?service=extension",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services/house-extensions.html",
    cta2_text="Extension drawings service",
)

##############################################################################
# POST 10: pre-application-advice-london
##############################################################################
build(
    slug="pre-application-advice-london",
    title="Pre-Application Advice London Guide | AD",
    og_title="Pre-Application Advice in London: Is It Worth It?",
    desc="Pre-application advice guide for London homeowners. What it is, costs (200-600 pounds), when it is worth the fee, how to apply, what to include, and borough response times.",
    breadcrumb="Pre-Application Advice Guide",
    eyebrow="Guide",
    h1='Pre-application advice in London: <em style="color: var(--accent); font-weight: 300;">is it worth the cost?</em>',
    minutes="12",
    tldrs=[
        "Pre-app is informal, paid advice from the council before you apply formally",
        "Cost: &pound;200&ndash;&pound;600 for householder pre-app (varies by borough)",
        "Response time: 4&ndash;8 weeks in most London boroughs",
        "Non-binding &mdash; positive pre-app does NOT guarantee planning approval",
        "Most valuable for conservation areas, complex sites, and controversial schemes",
        "Not necessary for simple PD schemes or straightforward extensions",
    ],
    img_ph="IMAGE PLACEHOLDER -- planning officer at a desk reviewing a pre-application submission with architectural drawings and a site plan",
    body="""
    <h2 id="what" class="reveal">What is pre-application advice?</h2>

    <p>Pre-application advice (commonly called "pre-app") is a paid service offered by every London borough council. You submit an informal proposal -- typically a brief description of the project, some sketch drawings or plans, and photographs -- and a planning officer reviews it against local and national planning policy. They then provide written feedback on whether the scheme is likely to be approved, what changes would improve its chances, and what documents you would need for a formal application.</p>

    <p>Pre-app is <strong>not</strong> a planning application. It is a conversation with the council before you commit to a formal submission. The council's response is informal, non-binding, and does not constitute a decision. However, it gives you a strong indication of how the planning officer views the proposal, which can save significant time and money.</p>


    <h2 id="costs" class="reveal">Pre-application costs by borough</h2>

    <p>Every London borough sets its own pre-app fees. Here are typical charges for householder pre-app (extensions, loft conversions, alterations to a single dwelling) in 2026:</p>

    <div class="article-table-wrap reveal">
      <table class="article-table">
        <thead>
          <tr><th>Borough</th><th>Householder pre-app fee</th><th>Includes meeting?</th></tr>
        </thead>
        <tbody>
          <tr><td>Camden</td><td>&pound;300&ndash;&pound;450</td><td>Written response only</td></tr>
          <tr><td>Islington</td><td>&pound;250&ndash;&pound;350</td><td>Written response only</td></tr>
          <tr><td>Hackney</td><td>&pound;200&ndash;&pound;300</td><td>Written response, meeting on request</td></tr>
          <tr><td>Westminster</td><td>&pound;400&ndash;&pound;600</td><td>Written response, meeting available</td></tr>
          <tr><td>Kensington &amp; Chelsea</td><td>&pound;350&ndash;&pound;500</td><td>Written response + meeting</td></tr>
          <tr><td>Wandsworth</td><td>&pound;200&ndash;&pound;300</td><td>Written response only</td></tr>
          <tr><td>Lambeth</td><td>&pound;250&ndash;&pound;350</td><td>Written response only</td></tr>
          <tr><td>Southwark</td><td>&pound;250&ndash;&pound;400</td><td>Written response only</td></tr>
          <tr><td>Tower Hamlets</td><td>&pound;250&ndash;&pound;350</td><td>Written response only</td></tr>
          <tr><td>Lewisham</td><td>&pound;200&ndash;&pound;300</td><td>Written response only</td></tr>
        </tbody>
      </table>
    </div>

    <p>These fees are in addition to the formal planning application fee (&pound;258 for householder) and any professional fees for drawings and agent services. Pre-app is an additional cost, which is why the decision of whether it is worth it matters.</p>


    <h2 id="when-worth" class="reveal">When pre-app is worth the cost</h2>

    <p>Pre-app is most valuable when the outcome of a formal application is genuinely uncertain. Here are the scenarios where we recommend it:</p>

    <h3>Conservation areas</h3>
    <p>If your property is in a conservation area, planning policy is stricter and the officer's subjective assessment of "preserving or enhancing the character of the area" plays a larger role. Pre-app lets you test the design with the conservation officer before committing to a formal application.</p>

    <h3>Complex or unusual sites</h3>
    <p>Properties on corner plots, with multiple boundaries, near listed buildings, in flood zones, or with tree preservation orders benefit from pre-app because the planning constraints may not be obvious from the outside.</p>

    <h3>Controversial or large schemes</h3>
    <p>If your extension is significantly larger than the norm for the street, if it involves a mansard roof in an area where mansards are contentious, or if you expect neighbour objections, pre-app helps you understand the officer's position before you invest in detailed drawings.</p>

    <h3>When you have already been refused</h3>
    <p>If a previous planning application has been refused, pre-app for the revised scheme can help you understand exactly what changes the officer needs to see before the resubmission.</p>


    <h2 id="when-not" class="reveal">When pre-app is NOT worth the cost</h2>

    <h3>Simple Permitted Development schemes</h3>
    <p>If your extension clearly falls within <a href="permitted-development-rules-2026.html">Permitted Development</a> limits and you do not need planning permission at all, pre-app is unnecessary. A Lawful Development Certificate (&pound;129) is the appropriate route instead.</p>

    <h3>Straightforward householder applications</h3>
    <p>If you are proposing a standard rear extension that is similar in scale and design to others on the street, in an area with no conservation designation, the approval rate for professional submissions is already 90&ndash;95%+. Pre-app adds cost and 4&ndash;8 weeks of delay for minimal additional certainty.</p>

    <h3>When you have an experienced agent</h3>
    <p>An experienced agent who regularly works in your borough already knows the planning officer's likely position on common scheme types. Our MCIAT chartered team has submitted across all 33 London boroughs and can assess your scheme's prospects without pre-app in most cases. We will always recommend pre-app when we think it is genuinely needed.</p>


    <h2 id="how-to" class="reveal">How to apply for pre-app</h2>

    <ol>
      <li><strong>Find the council's pre-app form.</strong> Each borough has its own pre-app application form, usually available on their planning pages. Some boroughs accept pre-app via the Planning Portal; others have their own forms.</li>
      <li><strong>Prepare your submission.</strong> A good pre-app submission includes: a completed application form, a site location plan (1:1250), a site block plan (1:500), sketch floor plans and elevations showing the proposed development, a brief description of the project, and photographs of the site and surrounding area.</li>
      <li><strong>Pay the fee.</strong> Fees are paid at the time of submission, usually by card or bank transfer.</li>
      <li><strong>Wait for the response.</strong> Response times are typically 4&ndash;6 weeks for householder pre-apps, up to 8 weeks in busy boroughs. Some boroughs offer a meeting with the officer; others provide only a written response.</li>
      <li><strong>Review and act on the advice.</strong> The officer's response will indicate whether the scheme is likely to be supported, what changes would improve it, and what documents are needed for a formal application. Use this to refine the design before submitting formally.</li>
    </ol>


    <h2 id="what-to-include" class="reveal">What to include in your pre-app submission</h2>

    <p>The quality of the pre-app response depends heavily on the quality of the submission. Vague descriptions and poor sketches result in vague responses. Here is what to include for the most useful feedback:</p>

    <ul>
      <li><strong>Clear description:</strong> what you want to build, its dimensions, materials, and use</li>
      <li><strong>Scale drawings:</strong> even at pre-app stage, to-scale floor plans and elevations are far more useful than sketches. Our Essentials package from &pound;840 includes professional drawings suitable for pre-app</li>
      <li><strong>Photographs:</strong> of the front, rear, and sides of the property, the garden, neighbouring properties, and the street scene</li>
      <li><strong>Site plan:</strong> showing the property boundary, the proposed extension footprint, and the relationship to neighbouring buildings</li>
      <li><strong>Questions:</strong> specific questions you want the officer to address (e.g. "is a mansard roof acceptable on this street?" or "would you support a contemporary design in this conservation area?")</li>
    </ul>


    <h2 id="our-service" class="reveal">How we help with pre-app</h2>

    <p>We can prepare and submit a pre-app on your behalf, including professional drawings, site photographs, and a clear description of the proposal. This maximises the quality of the council's response and saves you time.</p>

    <p>More importantly, we assess every project at the outset and advise whether pre-app is genuinely worth the cost. In many cases, our experience across all 33 London boroughs means we can predict the planning officer's likely response without pre-app, saving you &pound;200&ndash;&pound;600 and 4&ndash;8 weeks.</p>

    <div class="price-box reveal">
      <h4>Our fees</h4>
      <div class="price-row">
        <span class="label">Essentials (drawings suitable for pre-app or planning)</span>
        <span class="amount">from &pound;840</span>
      </div>
      <div class="price-row">
        <span class="label">Complete (planning + building regs + structural)</span>
        <span class="amount">from &pound;1,750</span>
      </div>
    </div>

    <p style="margin-top: 24px;"><a href="../quote.html" class="btn btn-primary">Get a free quote &rarr;</a></p>
""",
    faqs=[
        ("What is pre-application advice in planning?", "Pre-app is a paid, informal service where you submit a proposal to the council before making a formal planning application. A planning officer reviews it against policy and provides written feedback on whether it is likely to be approved and what changes would help. It is non-binding and does not constitute a decision."),
        ("How much does pre-app cost in London?", "Householder pre-app fees in London range from &pound;200 to &pound;600 depending on the borough. Camden charges &pound;300&ndash;&pound;450, Westminster &pound;400&ndash;&pound;600, and Wandsworth &pound;200&ndash;&pound;300. This is in addition to the formal planning fee (&pound;258) and any professional fees."),
        ("How long does pre-app take?", "Response times are typically 4&ndash;6 weeks for householder pre-apps in most London boroughs, up to 8 weeks in busy boroughs like Camden, Westminster, and Kensington and Chelsea. Some boroughs offer a meeting with the officer; others provide a written response only."),
        ("Is pre-app advice binding?", "No. Pre-app advice is informal and non-binding. The council can still refuse the formal application even after positive pre-app feedback, although this is rare if the scheme has not changed. Pre-app significantly reduces refusal risk but does not eliminate it."),
        ("When should I skip pre-app?", "Skip pre-app when: the project is clearly Permitted Development (use an LDC instead), the extension is a standard scheme similar to approved neighbours, you have an experienced agent who knows the borough, or the cost and 4&ndash;8 week delay are not justified by the risk. We advise on this case by case."),
    ],
    faq_schemas=[
        ("What is pre-application advice in planning?", "Pre-app is a paid informal service where you submit a proposal to the council before a formal application. A planning officer reviews it and provides written feedback on likely approval. It is non-binding but significantly reduces refusal risk."),
        ("How much does pre-application advice cost in London?", "Householder pre-app fees range from 200 to 600 pounds depending on the borough. This is in addition to the formal planning application fee of 258 pounds."),
        ("How long does pre-application advice take in London?", "Response times are typically 4-6 weeks for householder pre-apps, up to 8 weeks in busy boroughs like Camden and Westminster."),
        ("Is pre-application advice legally binding?", "No. Pre-app advice is informal and non-binding. The council can still refuse the formal application, although this is rare if the scheme has not changed from the pre-app submission."),
        ("When should I skip pre-application advice?", "Skip pre-app when the project is clearly Permitted Development, the extension is standard and similar to approved neighbours, or you have an experienced agent who knows the borough's policies."),
    ],
    relateds=[
        ("planning-agent-vs-diy.html", "Planning Agent vs DIY Application", "Should you submit your own planning application or use an agent? Success rates, costs..."),
        ("how-long-planning-permission.html", "How Long Does Planning Take London 2026", "8-week householder, 13-week major, pre-app timelines, and borough-specific waits..."),
        ("conservation-area-planning-london.html", "Conservation Area Planning London", "Planning rules for conservation areas: what you can and cannot build..."),
    ],
    cta_h2='Need planning drawings for <span class="accent">your project?</span>',
    cta_p="Fixed fees from &pound;840. MCIAT chartered. 98% first-time approval rate across all 33 London boroughs.",
    cta1_href="../quote.html",
    cta1_text="Get a free quote &rarr;",
    cta2_href="../services/planning-drawings.html",
    cta2_text="Planning drawings service",
)

print("\nAll 7 posts generated successfully.")
