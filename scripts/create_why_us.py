#!/usr/bin/env python3
"""Create why-us.html with competitor comparison."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
ref = (ROOT / 'faq/index.html').read_text(encoding='utf-8')
style_match = re.search(r'<style>(.*?)</style>', ref, re.DOTALL)
style_content = style_match.group(1) if style_match else ''

html = '''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Why Choose Us | Architectural Drawings London</title>
<meta name="description" content="Why choose Architectural Drawings London: MCIAT chartered, 30% below architects, 98% approval rate, fixed fees, all 33 London boroughs. Side-by-side comparison." />
<link rel="canonical" href="https://www.architecturaldrawings.uk/why-us.html" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://www.architecturaldrawings.uk/why-us.html" />
<meta property="og:title" content="Why Choose Architectural Drawings London" />
<meta property="og:description" content="MCIAT chartered, 30% below architects, 98% approval rate. Compare us with competitors." />
<meta property="og:locale" content="en_GB" />

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.architecturaldrawings.uk/"},{"@type":"ListItem","position":2,"name":"Why Choose Us"}]}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />

<style>
__STYLE__
.compare-table{width:100%;border-collapse:collapse;margin:32px 0;font-size:0.92rem;}
.compare-table th,.compare-table td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left;}
.compare-table th{font-family:var(--font-body);font-weight:700;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--ink-soft);background:var(--bg-2);}
.compare-table th.us{background:var(--ink);color:var(--bg);}
.compare-table td.us{background:var(--accent-soft);font-weight:600;color:var(--ink);}
.reasons-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin:40px 0;}
.reason-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:28px;}
.reason-icon{width:48px;height:48px;border-radius:12px;background:var(--accent-soft);color:var(--accent-deep);display:grid;place-items:center;margin-bottom:16px;}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="/" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav><ul class="nav-links">
      <li><a href="services.html">Services</a></li>
      <li><a href="pricing.html">Pricing</a></li>
      <li><a href="areas/">Areas</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="blog/">Blog</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<section class="hero">
  <div class="container">
    <nav aria-label="Breadcrumb" style="font-size:0.85rem;color:var(--ink-soft);margin-bottom:20px;">
      <a href="/" style="color:var(--ink-soft);">Home</a> / <strong style="color:var(--ink);">Why Choose Us</strong>
    </nav>
    <span class="eyebrow">The honest comparison</span>
    <h1 style="margin:16px 0 24px;max-width:920px;">Why choose <span style="color:var(--accent);font-style:italic;font-weight:300;">Architectural Drawings London?</span></h1>
    <p style="color:var(--ink-soft);max-width:680px;font-size:1.15rem;">We sit between budget online drawing services and traditional architects &mdash; MCIAT chartered, fixed fees, 30% below architect rates, with a 98% first-time approval rate across all 33 London boroughs.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Side-by-side</span>
      <h2 style="margin-top:16px;">Us vs <em>budget services</em> vs <em>architects</em></h2>
    </div>
    <div style="overflow-x:auto;">
      <table class="compare-table">
        <thead>
          <tr><th>Feature</th><th>Budget service</th><th class="us">Us (AD London)</th><th>RIBA Architect</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Qualification</strong></td><td>None / unregulated</td><td class="us">MCIAT Chartered</td><td>RIBA / ARB</td></tr>
          <tr><td><strong>Fees (extension)</strong></td><td>&pound;300-600</td><td class="us">&pound;1,225 fixed</td><td>&pound;8,000-15,000</td></tr>
          <tr><td><strong>Fee model</strong></td><td>Fixed</td><td class="us">Fixed</td><td>8-15% of build cost</td></tr>
          <tr><td><strong>Measured survey</strong></td><td>Sometimes</td><td class="us">Always included</td><td>Always included</td></tr>
          <tr><td><strong>Building regs</strong></td><td>Extra cost</td><td class="us">Included (Complete)</td><td>Included</td></tr>
          <tr><td><strong>Structural calcs</strong></td><td>Not included</td><td class="us">Included (Complete)</td><td>Extra cost</td></tr>
          <tr><td><strong>Council submission</strong></td><td>DIY</td><td class="us">Full agent service</td><td>Full agent service</td></tr>
          <tr><td><strong>PI insurance</strong></td><td>Often none</td><td class="us">&pound;2m</td><td>&pound;1-5m</td></tr>
          <tr><td><strong>Approval rate</strong></td><td>~60%</td><td class="us">98%</td><td>~90%</td></tr>
          <tr><td><strong>Turnaround</strong></td><td>1-2 weeks</td><td class="us">3-4 weeks</td><td>6-12 weeks</td></tr>
          <tr><td><strong>Revisions</strong></td><td>Limited</td><td class="us">Unlimited</td><td>Depends on contract</td></tr>
          <tr><td><strong>All 33 boroughs</strong></td><td>Varies</td><td class="us">Yes</td><td>Varies</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section style="background:var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Six reasons</span>
      <h2 style="margin-top:16px;">Why London homeowners <em>choose us</em></h2>
    </div>
    <div class="reasons-grid">
      <div class="reason-card"><div class="reason-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L3 7v6c0 5 4 8 9 10 5-2 9-5 9-10V7l-9-5z"/></svg></div><h3>MCIAT chartered</h3><p>Not "designers" &mdash; genuinely chartered architectural technologists with CIAT accreditation and &pound;2m PI insurance.</p></div>
      <div class="reason-card"><div class="reason-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><h3>30% below architects</h3><p>Fixed fees from &pound;840. Same planning and building regs outcomes, typically 30-40% cheaper than RIBA architect fees.</p></div>
      <div class="reason-card"><div class="reason-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></div><h3>98% approval rate</h3><p>Out of 287 applications, 98% get approved first-time. We know what London planners look for because we do this every day.</p></div>
      <div class="reason-card"><div class="reason-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><h3>Fixed fees, no surprises</h3><p>Essentials &pound;840, Complete &pound;1,750, Bespoke custom. No hourly rates, no scope creep, no percentage-of-build-cost shocks.</p></div>
      <div class="reason-card"><div class="reason-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><h3>All 33 London boroughs</h3><p>Deep experience with every borough's Article 4 Directions, conservation areas, and local planning quirks.</p></div>
      <div class="reason-card"><div class="reason-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg></div><h3>One team, everything</h3><p>Planning, building regs, structural calcs, Party Wall &mdash; one chartered team handles it all. No coordinating 3 contractors.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="container" style="max-width:800px;text-align:center;">
    <div style="font-size:1.6rem;color:var(--accent);margin-bottom:20px;">&ldquo;</div>
    <blockquote style="font-family:var(--font-display);font-size:clamp(1.2rem,2.5vw,1.6rem);font-style:italic;font-variation-settings:'opsz' 60;line-height:1.4;color:var(--ink);margin-bottom:24px;">Passed planning with Hackney first time on a fairly bold mansard proposal. Better drawings than the architect quote we'd been sitting on for six months, at less than half the price.</blockquote>
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;">
      <div style="width:44px;height:44px;border-radius:50%;background:var(--accent-soft);color:var(--accent-deep);display:grid;place-items:center;font-family:var(--font-display);font-style:italic;font-size:1.1rem;">A</div>
      <div style="text-align:left;"><div style="font-weight:600;font-size:0.94rem;">Anna K.</div><div style="font-size:0.82rem;color:var(--ink-soft);">Mansard loft &middot; Hackney</div></div>
    </div>
    <p style="margin-top:32px;color:var(--ink-soft);"><strong>287 projects</strong> &middot; <strong>4.9/5 rating</strong> &middot; <strong>98% first-time approval</strong></p>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Ready to <span class="accent">start your project?</span></h2>
    <p>Free quote in 60 seconds. Fixed fee from &pound;840. MCIAT chartered.</p>
    <a href="quote.html" class="btn btn-primary btn-lg">Get my free quote &rarr;</a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="services/planning-drawings.html">Planning permission drawings London</a></li>
        <li><a href="services/building-regulations.html">Building regulations drawings London</a></li>
        <li><a href="services/loft-conversions.html">Loft conversion drawings London</a></li>
        <li><a href="services/house-extensions.html">House extension plans London</a></li>
        <li><a href="services/mansard-roof.html">Mansard roof extensions London</a></li>
      </ul></div>
      <div><h5>Loft by borough</h5><ul>
        <li><a href="areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
      </ul></div>
      <div><h5>Extensions by borough</h5><ul>
        <li><a href="areas/lewisham/house-extensions.html">Extension Lewisham</a></li>
        <li><a href="areas/greenwich/house-extensions.html">Extension Greenwich</a></li>
        <li><a href="areas/bromley/house-extensions.html">Extension Bromley</a></li>
        <li><a href="areas/croydon/house-extensions.html">Extension Croydon</a></li>
        <li><a href="areas/merton/house-extensions.html">Extension Merton</a></li>
      </ul></div>
      <div><h5>Planning by borough</h5><ul>
        <li><a href="areas/barnet/planning-drawings.html">Planning Barnet</a></li>
        <li><a href="areas/haringey/planning-drawings.html">Planning Haringey</a></li>
        <li><a href="areas/enfield/planning-drawings.html">Planning Enfield</a></li>
        <li><a href="areas/newham/planning-drawings.html">Planning Newham</a></li>
        <li><a href="areas/bexley/planning-drawings.html">Planning Bexley</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom" style="border-top:0;padding-top:0;">
      <span>&copy; 2026 Architectural Drawings Ltd</span>
      <span><a href="/">Home</a> &middot; <a href="privacy.html">Privacy</a> &middot; <a href="terms.html">Terms</a></span>
    </div>
  </div>
</footer>

<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="Call us"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg></a>
  <a href="https://wa.me/442079460000" target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="WhatsApp"><svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 0 0 .613.613l4.458-1.495A11.952 11.952 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.39-1.586l-.386-.232-2.644.886.886-2.644-.232-.386A9.94 9.94 0 0 1 2 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg></a>
</div>
</body>
</html>
'''.replace('__STYLE__', style_content)

(ROOT / 'why-us.html').write_text(html, encoding='utf-8')
print(f'[OK] why-us.html created ({len(html):,} chars)')
