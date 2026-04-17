#!/usr/bin/env python3
"""Generate UK city remote-service pages under /areas/uk/{slug}/index.html + nationwide hub.

Pages sit 3 levels deep (/areas/uk/{slug}/) so asset paths are ../../../ relative.
"""
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "areas" / "uk"

DOMAIN = "https://www.architecturaldrawings.uk"

# Inlined CSS — mirrors the Victorian terrace reference page's compact ruleset.
INLINE_CSS = """:root{--bg:#FAFAF7;--bg-2:#F2EFE8;--surface:#FFFFFF;--ink:#0E1116;--ink-soft:#4A5260;--ink-softer:#6B7280;--line:rgba(14,17,22,0.08);--line-strong:rgba(14,17,22,0.14);--accent:#C8664A;--accent-deep:#9D4A32;--accent-soft:#F5E6DD;--accent-glow:rgba(200,102,74,0.12);--success:#47845A;--font-display:'Fraunces','Times New Roman',serif;--font-body:'Manrope',-apple-system,BlinkMacSystemFont,sans-serif;--r-sm:10px;--r-md:16px;--r-lg:24px;--r-xl:36px;--r-full:999px;--shadow-sm:0 1px 2px rgba(14,17,22,0.04),0 2px 6px rgba(14,17,22,0.04);--shadow-md:0 4px 12px rgba(14,17,22,0.06),0 12px 32px rgba(14,17,22,0.05);--shadow-lg:0 24px 60px rgba(14,17,22,0.08),0 8px 20px rgba(14,17,22,0.05);--shadow-glow:0 20px 60px rgba(200,102,74,0.18);--ease:cubic-bezier(0.22,1,0.36,1);--ease-spring:cubic-bezier(0.34,1.56,0.64,1);--container:1240px;--container-tight:960px;}*,*::before,*::after{box-sizing:border-box;}*{margin:0;padding:0;}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;}body{font-family:var(--font-body);font-weight:400;font-size:17px;line-height:1.55;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;overflow-x:hidden;}img,svg,video{display:block;max-width:100%;height:auto;}button{font-family:inherit;cursor:pointer;border:0;background:none;}a{color:inherit;text-decoration:none;}a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px;}::selection{background:var(--accent);color:#fff;}h1,h2,h3,h4{font-family:var(--font-display);font-weight:400;color:var(--ink);letter-spacing:-0.02em;line-height:1.05;}h1{font-size:clamp(2.8rem,6.5vw,5.5rem);font-variation-settings:"opsz" 144,"SOFT" 50;}h2{font-size:clamp(2.1rem,4.2vw,3.4rem);font-variation-settings:"opsz" 100,"SOFT" 40;}h3{font-size:clamp(1.5rem,2.4vw,2rem);font-variation-settings:"opsz" 60;}h4{font-size:1.3rem;font-variation-settings:"opsz" 36;}em{font-style:italic;}.eyebrow{font-family:var(--font-body);font-size:0.78rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--accent-deep);display:inline-flex;align-items:center;gap:8px;}.eyebrow::before{content:'';width:24px;height:1px;background:var(--accent);}.container{width:100%;max-width:var(--container);margin:0 auto;padding:0 24px;}.container-tight{max-width:var(--container-tight);margin:0 auto;padding:0 24px;}section{padding:clamp(60px,9vw,120px) 0;position:relative;}.nav{position:sticky;top:0;z-index:100;padding:14px 0;background:rgba(250,250,247,0.72);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid transparent;transition:border-color 0.3s var(--ease);}.nav.scrolled{border-bottom-color:var(--line);}.nav-inner{display:flex;align-items:center;justify-content:space-between;gap:32px;}.logo{display:inline-flex;align-items:center;gap:10px;font-family:var(--font-display);font-weight:500;font-size:1.5rem;letter-spacing:-0.02em;font-variation-settings:"opsz" 60;}.logo-mark{width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:var(--bg);border-radius:8px;font-family:var(--font-body);font-weight:700;font-size:0.95rem;}.nav-links{display:flex;align-items:center;gap:2px;list-style:none;}.nav-links a{padding:10px 14px;font-size:0.94rem;font-weight:500;border-radius:10px;transition:background 0.2s var(--ease);}.nav-links a:hover{background:rgba(14,17,22,0.05);}.nav-cta{display:flex;align-items:center;gap:10px;}@media(max-width:960px){.nav-links{display:none;}}.btn{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;font-size:0.95rem;font-weight:600;border-radius:var(--r-full);transition:transform 0.2s var(--ease),background 0.2s var(--ease),box-shadow 0.3s var(--ease);white-space:nowrap;cursor:pointer;line-height:1;}.btn-primary{background:var(--ink);color:var(--bg);}.btn-primary:hover{background:var(--accent-deep);transform:translateY(-1px);box-shadow:var(--shadow-glow);}.btn-ghost{background:transparent;color:var(--ink);padding:12px 18px;}.btn-lg{padding:18px 30px;font-size:1rem;}.btn-sm{padding:10px 16px;font-size:0.88rem;}.hero{padding:clamp(40px,7vw,100px) 0 clamp(60px,10vw,140px);position:relative;overflow:hidden;}.hero-lede{font-size:clamp(1.1rem,1.4vw,1.3rem);color:var(--ink-soft);max-width:620px;margin-bottom:20px;line-height:1.5;}.hero-cover{width:100%;height:clamp(220px,32vw,360px);border-radius:var(--r-lg);background:linear-gradient(135deg,#C8664A 0%,#9D4A32 45%,#5C2C1E 100%);position:relative;overflow:hidden;margin-top:28px;box-shadow:var(--shadow-lg);display:flex;align-items:center;justify-content:center;color:rgba(250,250,247,0.92);}.hero-cover::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 25% 25%,rgba(250,250,247,0.18),transparent 50%),radial-gradient(ellipse at 80% 80%,rgba(14,17,22,0.35),transparent 55%);pointer-events:none;}.hero-cover span{position:relative;z-index:2;font-family:var(--font-display);font-style:italic;font-weight:300;font-variation-settings:"opsz" 144,"SOFT" 80;font-size:clamp(2.8rem,7vw,5.4rem);letter-spacing:-0.02em;text-shadow:0 2px 24px rgba(14,17,22,0.3);}.cta-band{padding:clamp(60px,9vw,100px) 0;text-align:center;}.cta-band h2{font-size:clamp(2.4rem,5vw,4.2rem);max-width:820px;margin:0 auto 24px;}.cta-band h2 .accent{color:var(--accent);font-style:italic;font-weight:300;}.cta-band p{color:var(--ink-soft);max-width:560px;margin:0 auto 32px;font-size:1.1rem;}.footer{padding:80px 0 40px;background:var(--ink);color:rgba(250,250,247,0.6);}.footer .logo{color:var(--bg);margin-bottom:16px;}.footer .logo-mark{background:var(--bg);color:var(--ink);}.footer-bottom{padding-top:32px;border-top:1px solid rgba(255,255,255,0.1);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;font-size:0.82rem;color:rgba(250,250,247,0.5);}.footer-seo{display:grid;grid-template-columns:repeat(4,1fr);gap:2.5rem;padding-bottom:3rem;margin-bottom:3rem;border-bottom:1px solid rgba(255,255,255,0.08);}@media(max-width:820px){.footer-seo{grid-template-columns:1fr 1fr;}}@media(max-width:500px){.footer-seo{grid-template-columns:1fr;}}.footer-seo h5{font-family:var(--font-body);font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.2em;color:var(--bg);margin-bottom:1.25rem;}.footer-seo ul{list-style:none;display:flex;flex-direction:column;gap:0.55rem;}.footer-seo a{font-size:0.85rem;color:rgba(250,250,247,0.45);transition:color 0.3s var(--ease);line-height:1.4;}.footer-seo a:hover{color:var(--accent);}@keyframes __ad_safety_in{to{opacity:1;transform:none;}}.reveal{opacity:0;transform:translateY(20px);transition:opacity 0.8s var(--ease),transform 0.8s var(--ease);animation:__ad_safety_in 0.01s linear 1.5s forwards;}.reveal.in{animation:none;opacity:1;transform:none;}@media(prefers-reduced-motion:reduce){.reveal{animation:none;opacity:1;transform:none;}}.article-body{max-width:760px;margin:0 auto;}.article-body h2{font-size:clamp(1.7rem,3.2vw,2.3rem);margin:56px 0 20px;}.article-body h3{font-size:clamp(1.2rem,2vw,1.6rem);margin:36px 0 14px;}.article-body p{color:var(--ink-soft);font-size:1.05rem;line-height:1.7;margin-bottom:20px;}.article-body ul,.article-body ol{color:var(--ink-soft);font-size:1.05rem;line-height:1.7;margin:0 0 20px 24px;}.article-body li{margin-bottom:8px;}.article-body a{color:var(--accent-deep);font-weight:600;text-decoration:underline;text-underline-offset:3px;}.article-body a:hover{color:var(--accent);}.article-body strong{color:var(--ink);font-weight:600;}.tldr-box{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:28px 32px;margin:32px 0;}.tldr-box h3{margin:0 0 16px;font-size:1.1rem;color:var(--accent-deep);}.tldr-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}@media(max-width:600px){.tldr-grid{grid-template-columns:repeat(2,1fr);}}.tldr-label{font-size:0.78rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--ink-softer);margin-bottom:4px;}.tldr-value{font-size:1rem;color:var(--ink);font-weight:500;}.service-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:28px 0;}.svc-card{display:block;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);padding:20px 22px;transition:transform 0.2s var(--ease),border-color 0.2s var(--ease),box-shadow 0.3s var(--ease);}.svc-card:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:var(--shadow-md);}.svc-card strong{display:block;color:var(--ink);font-size:0.98rem;margin-bottom:4px;font-weight:600;}.svc-card span{font-size:0.84rem;color:var(--ink-soft);}details{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);padding:18px 22px;margin-bottom:12px;transition:border-color 0.2s var(--ease);}details[open]{border-color:var(--accent);}summary{font-weight:600;color:var(--ink);cursor:pointer;list-style:none;position:relative;padding-right:28px;font-size:1rem;}summary::-webkit-details-marker{display:none;}summary::after{content:'+';position:absolute;right:0;top:-2px;font-size:1.4rem;color:var(--accent);transition:transform 0.2s var(--ease);}details[open] summary::after{transform:rotate(45deg);}details p{margin-top:12px;color:var(--ink-soft);font-size:0.98rem;line-height:1.65;}.borough-chips{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 28px;}.borough-chips a{display:inline-block;padding:6px 14px;background:var(--bg-2);border:1px solid var(--line);border-radius:var(--r-full);font-size:0.82rem;color:var(--ink-soft);transition:all 0.2s var(--ease);}.borough-chips a:hover{background:var(--accent);color:#fff;border-color:var(--accent);}.meta-row{display:flex;flex-wrap:wrap;gap:16px;margin:20px 0 0;font-size:0.88rem;color:var(--ink-softer);}.meta-row span{display:inline-flex;align-items:center;gap:6px;}.meta-row span::before{content:'';width:4px;height:4px;border-radius:50%;background:var(--accent);}.notice{background:var(--accent-soft);border:1px solid rgba(200,102,74,0.22);border-left:4px solid var(--accent);border-radius:var(--r-md);padding:20px 24px;margin:28px 0;}.notice strong{color:var(--accent-deep);}.process-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:28px 0;}.process-step{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);padding:24px;position:relative;}.process-step .num{width:36px;height:36px;border-radius:50%;background:var(--accent);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:1.05rem;font-weight:500;margin-bottom:12px;}.process-step h4{font-size:1.1rem;margin-bottom:6px;}.process-step p{font-size:0.92rem;color:var(--ink-soft);line-height:1.55;margin:0;}.why-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:28px 0;}.why-card{background:var(--bg-2);border-radius:var(--r-md);padding:22px 24px;}.why-card strong{display:block;color:var(--ink);font-size:1rem;margin-bottom:6px;font-family:var(--font-display);font-weight:500;}.why-card span{font-size:0.92rem;color:var(--ink-soft);line-height:1.55;}"""

WHATSAPP_AND_SAFETY = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />"""

REVEAL_SCRIPT = """<script>(()=>{'use strict';const reveals=document.querySelectorAll('.reveal');if('IntersectionObserver' in window&&reveals.length){const io=new IntersectionObserver((entries)=>{entries.forEach((entry)=>{if(entry.isIntersecting){entry.target.classList.add('in');io.unobserve(entry.target);}});},{threshold:0.1,rootMargin:'0px 0px -60px 0px'});reveals.forEach((el)=>io.observe(el));}else{reveals.forEach((el)=>el.classList.add('in'));}const nav=document.getElementById('nav');if(nav){const onScroll=()=>{nav.classList.toggle('scrolled',window.scrollY>12);};onScroll();window.addEventListener('scroll',onScroll,{passive:true});}document.querySelectorAll('details').forEach((d)=>{d.addEventListener('toggle',()=>{d.classList.toggle('open',d.open);});});})();</script>"""

WHATSAPP_FAB = """<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;"><a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="Call us"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg></a><a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20for%20my%20project." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="WhatsApp"><svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a3.04 3.04 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg></a></div>"""


# ---- City data --------------------------------------------------------------

CITIES = {
    "manchester": {
        "name": "Manchester",
        "postcodes": "M1–M35",
        "region": "Greater Manchester",
        "council": "Manchester City Council",
        "housing": "Victorian red-brick terraces dominate the inner ring — Rusholme, Chorlton, Didsbury and Levenshulme — sitting alongside dense Edwardian semis and a fast-growing stock of converted mills and new-build apartments in the city core.",
        "conservation": "Manchester has around 37 designated conservation areas including the Northern Quarter, Castlefield, Ancoats, Deansgate/Peter Street, Didsbury and Victoria Park. Heritage policy is strictly enforced within these zones, and many inner-city streets carry Article 4 Directions restricting permitted development.",
        "notes": "Manchester is one of the fastest-growing UK cities and high-density infill is normal; the council is generally pragmatic on well-designed rear extensions and loft dormers outside conservation areas.",
        "blurb": "Manchester combines Victorian terrace density with one of the most progressive modern-tall-building policies in the UK.",
        "landmarks": "Northern Quarter, Castlefield, Ancoats",
    },
    "birmingham": {
        "name": "Birmingham",
        "postcodes": "B1–B98",
        "region": "West Midlands",
        "council": "Birmingham City Council",
        "housing": "Housing stock is dominated by 1930s semi-detached suburban houses across Edgbaston, Moseley, Kings Heath, Harborne and Bournville, alongside Victorian villas in Edgbaston and Moseley and Georgian terraces around the Jewellery Quarter.",
        "conservation": "Birmingham has 30 conservation areas including the Jewellery Quarter, Edgbaston, Moseley, Harborne, Bournville, and Sutton Coldfield Town. Article 4 Directions apply in several (most notably the Jewellery Quarter and Bournville) to protect shopfronts and terrace rhythms.",
        "notes": "Birmingham City Council runs a pragmatic validation process but heritage areas are tightly managed. Rear extensions under 4 metres on semis are a routine success provided materials and fenestration match.",
        "blurb": "Birmingham’s housing stock is built around the inter-war semi, with strong heritage clusters in the Jewellery Quarter and Edgbaston.",
        "landmarks": "Jewellery Quarter, Edgbaston, Bournville",
    },
    "leeds": {
        "name": "Leeds",
        "postcodes": "LS1–LS29",
        "region": "West Yorkshire",
        "council": "Leeds City Council",
        "housing": "Characteristic back-to-back and through terraces in Harehills, Hyde Park and Headingley, Victorian/Edwardian villas in Roundhay and Chapel Allerton, 1930s semis in the suburbs, and a growing rural hinterland covering Otley, Wetherby and Garforth.",
        "conservation": "Leeds has more than 70 conservation areas including Headingley Hill, Chapel Allerton, Roundhay, Hyde Park, and the Little Woodhouse / Woodhouse Square heritage belts. The LCC planning team enforces design continuity on stone and brick frontages.",
        "notes": "Leeds City Council is one of the larger planning authorities in England and serves a wide rural hinterland — we handle applications from central Leeds through to the villages of Otley, Wetherby and Collingham.",
        "blurb": "Leeds mixes dense inner-city Victorian terraces with a vast outlying semi-rural belt covering Wharfedale and the Wetherby area.",
        "landmarks": "Headingley, Roundhay, Chapel Allerton",
    },
    "liverpool": {
        "name": "Liverpool",
        "postcodes": "L1–L38",
        "region": "Merseyside",
        "council": "Liverpool City Council",
        "housing": "Liverpool 8 is famous for its Georgian townhouse stock — some of the finest outside Bath and London. Add large Victorian terrace belts through Toxteth, Kensington and Anfield, 1930s semis in West Derby, and a growing crop of reclaimed warehouse apartments in the Baltic Triangle.",
        "conservation": "Liverpool has 35 conservation areas including Canning, Rodney Street, Falkner Square, Sefton Park, Aigburth, and the city-centre World Heritage buffer zones. Many Georgian streets carry an Article 4 Direction and a significant proportion of Liverpool 8 is statutorily listed.",
        "notes": "Liverpool City Council is experienced with heritage applications. Georgian works almost always involve Listed Building Consent and a formal Heritage Statement, both of which our drawings packs include by default.",
        "blurb": "Liverpool holds one of the UK’s largest Georgian and Victorian heritage stocks outside London, concentrated in Liverpool 8.",
        "landmarks": "Georgian Quarter, Sefton Park, Baltic Triangle",
    },
    "bristol": {
        "name": "Bristol",
        "postcodes": "BS1–BS49",
        "region": "South West England",
        "council": "Bristol City Council",
        "housing": "Georgian terraces climb the hills of Clifton, Redland and Kingsdown; Victorian bay-fronted houses run through Bishopston, Southville and Totterdown; stone artisan cottages sit in Bedminster; and post-war semis fill the belt around Henleaze and Horfield.",
        "conservation": "Bristol has 33 conservation areas including Clifton, Cotham, Redland, Montpelier, Hotwells, and the central city core. Clifton in particular has very strict policies on fenestration, stucco rendering and rear dormers; the city is also hemmed in by Avon Green Belt to the south and east.",
        "notes": "Bristol City Council has a reputation for thorough conservation-led scrutiny in Clifton and Cotham. We produce Heritage Statements and conservation-area matching details as standard on any application above a simple rear extension.",
        "blurb": "Bristol ranges from Georgian stucco in Clifton to artisan stone cottages in Bedminster, all tightly managed by conservation and green-belt policies.",
        "landmarks": "Clifton, Redland, Southville",
    },
    "edinburgh": {
        "name": "Edinburgh",
        "postcodes": "EH1–EH17",
        "region": "Scotland (Lothian)",
        "council": "City of Edinburgh Council",
        "housing": "Dominated by Georgian New Town terraces (UNESCO World Heritage), tenement flats through Marchmont, Morningside, Bruntsfield and Leith, Victorian villas in Merchiston and Trinity, and inter-war bungalows in the outer suburbs.",
        "conservation": "The Old Town and New Town together form a UNESCO World Heritage Site, and Edinburgh has 50+ conservation areas across the city. Listed Building Consent is extremely common — around half of all central Edinburgh flats are listed, usually Category B or C.",
        "notes": "Edinburgh applications run under Scottish planning law (not English) — Planning Permission, Building Warrant and Listed Building Consent replace the English equivalents. We produce drawings to Scottish standards and can coordinate with the building warrant contractor on your behalf.",
        "blurb": "Edinburgh is one of the most heritage-dense UK cities — a UNESCO World Heritage Site with tenement flats forming the backbone of residential stock.",
        "landmarks": "New Town, Old Town, Stockbridge",
        "is_scotland": True,
    },
    "glasgow": {
        "name": "Glasgow",
        "postcodes": "G1–G78",
        "region": "Scotland (Strathclyde)",
        "council": "Glasgow City Council",
        "housing": "Red and blond sandstone tenements define the West End, Southside, Dennistoun and Partick; Victorian terraces run through Dowanhill and Pollokshields; 1930s semis fill Bearsden, Newton Mearns and Giffnock in the commuter belt.",
        "conservation": "Glasgow has 23 Outstanding Conservation Areas including Park, Glasgow West (Kelvinside, Dowanhill), Pollokshields, and the Merchant City. Many city-centre and West End tenements are Category B listed.",
        "notes": "Glasgow City Council operates under Scottish planning law. Tenement flats typically need common stair consent from co-owners and a full Building Warrant for any structural alteration. Our drawings packs include the information a Scottish building standards surveyor expects.",
        "blurb": "Glasgow’s residential stock is defined by its sandstone tenements — the West End and Southside contain some of the finest intact tenement streetscapes in Europe.",
        "landmarks": "West End, Southside, Dennistoun",
        "is_scotland": True,
    },
    "brighton": {
        "name": "Brighton",
        "postcodes": "BN1–BN3",
        "region": "East Sussex",
        "council": "Brighton & Hove City Council",
        "housing": "Regency seafront terraces in Kemptown and Brunswick, bay-fronted Victorian streets across Seven Dials, Preston Park and Fiveways, Edwardian villas in Hove, and increasingly dense conversion flats throughout.",
        "conservation": "Brighton & Hove has 34 conservation areas including Clifton Hill, Kemptown, Brunswick Town, Queen’s Park, Montpelier & Clifton Hill, and Seven Dials. Many are under Article 4 Directions, and the city includes a high density of Grade II and II* listings along the seafront crescents.",
        "notes": "Brighton & Hove City Council is alert to overdevelopment; loft conversions with rear dormers are often refused in conservation areas and pushed towards mansard or hip-to-gable alternatives. We handle these conversions regularly.",
        "blurb": "Brighton’s bohemian character is underpinned by Regency and Victorian heritage; a large share of its housing stock sits in conservation areas.",
        "landmarks": "Kemptown, Brunswick, Seven Dials",
    },
    "cambridge": {
        "name": "Cambridge",
        "postcodes": "CB1–CB5",
        "region": "Cambridgeshire",
        "council": "Cambridge City Council",
        "housing": "Victorian terraces through Mill Road, Romsey and Petersfield; Edwardian villas in Newnham and Chesterton; extensive collegiate and historic stock in the city centre; and a green belt ringing the outer boundary that limits new-build and heavy extensions.",
        "conservation": "Cambridge has 13 conservation areas covering almost the entire central city. Listed buildings are extremely prevalent — not just colleges but residential streets around Jesus Green, the Backs, and Brookside. The city lies inside the Cambridge Green Belt.",
        "notes": "Cambridge City Council takes a detailed, design-first approach and will reject extensions judged to diminish college-town character. We produce Design & Access Statements and heritage impact assessments on every central-Cambridge application.",
        "blurb": "Cambridge has unusually high conservation coverage for a city its size — almost every central street is in a conservation area.",
        "landmarks": "Mill Road, Newnham, Chesterton",
    },
    "oxford": {
        "name": "Oxford",
        "postcodes": "OX1–OX4",
        "region": "Oxfordshire",
        "council": "Oxford City Council",
        "housing": "Victorian brick terraces run through Jericho, East Oxford and Cowley; Edwardian villas sit in North Oxford and Summertown; large swathes of the centre are collegiate and listed; the city is ringed by the Oxford Green Belt.",
        "conservation": "Oxford has 18 conservation areas covering most of the central and inner-ring neighbourhoods. Listed buildings are very widespread — not just colleges and churches but tradesmens’ terraces in Jericho and North Oxford — and the View Cones policy protects key sightlines of the skyline.",
        "notes": "Oxford City Council is one of the stricter planning authorities in England. The View Cones policy can scupper a rear dormer or roof extension even where it would be accepted elsewhere. We design and model against the cones at the sketch stage.",
        "blurb": "Oxford is one of the most heritage-protected UK cities and is uniquely constrained by its View Cones policy.",
        "landmarks": "Jericho, North Oxford, Cowley",
    },
    "bath": {
        "name": "Bath",
        "postcodes": "BA1–BA2",
        "region": "Somerset (B&NES)",
        "council": "Bath and North East Somerset Council",
        "housing": "Almost the entire housing stock is Georgian or Regency Bath stone: terraces, crescents and townhouses across Lansdown, Bathwick, Widcombe and the centre. Outside the core you’ll find Victorian villas in Oldfield Park and inter-war semis on the fringes.",
        "conservation": "Bath is a UNESCO World Heritage City — the whole of central Bath is within a conservation area and a high proportion of the residential stock is statutorily listed, typically Grade II. Any external alteration will need Listed Building Consent.",
        "notes": "Bath and North East Somerset Council (B&NES) is one of the most conservation-led planning authorities in England. Listed Building Consent, matching-stone details and internal fabric reports are standard for almost any central-Bath project; we handle these routinely.",
        "blurb": "Bath is a UNESCO World Heritage City built almost entirely in Bath stone — Listed Building Consent is the norm, not the exception.",
        "landmarks": "Royal Crescent, Bathwick, Widcombe",
    },
    "york": {
        "name": "York",
        "postcodes": "YO1–YO32",
        "region": "North Yorkshire",
        "council": "City of York Council",
        "housing": "A medieval core inside the city walls (much of it listed), Georgian and Victorian terraces in Bishophill, Fulford and Bootham, Edwardian villas around Clifton, and 1930s semis through Acomb and Huntington in the outer ring.",
        "conservation": "York’s Central Historic Core Conservation Area covers most of the walled city, plus 33 further conservation areas across the authority. The Minster Setting policy protects long views of York Minster and can restrict ridge heights in surprising parts of the city.",
        "notes": "City of York Council applies strict heritage controls inside the walls and sets height limits under the Minster Setting policy. We model against both the conservation area appraisal and the Minster view points at concept stage.",
        "blurb": "York’s medieval walled core and Minster view cones create a planning environment unlike any other UK city.",
        "landmarks": "City Walls, Bishophill, Clifton",
    },
}

ORDER = ["manchester", "birmingham", "leeds", "liverpool", "bristol", "edinburgh",
         "glasgow", "brighton", "cambridge", "oxford", "bath", "york"]


# ---- Head / nav / footer helpers -------------------------------------------

def head(title, description, canonical_path, og_title=None, og_description=None):
    og_title = og_title or title
    og_description = og_description or description
    canonical = f"{DOMAIN}{canonical_path}"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="{canonical}" />
<link rel="manifest" href="/manifest.webmanifest" />
<link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="AD London" />
<meta name="application-name" content="Architectural Drawings London" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
<meta name="format-detection" content="telephone=no" />
<link rel="author" href="{DOMAIN}/about.html" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{og_title}" />
<meta property="og:description" content="{og_description}" />
<meta property="og:locale" content="en_GB" />
<meta property="og:site_name" content="Architectural Drawings London" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{og_title}" />
<meta name="twitter:description" content="{og_description}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>
<link rel="stylesheet" href="../../../assets/css/style.css" />
<style>{INLINE_CSS}</style>
{WHATSAPP_AND_SAFETY}"""


NAV = """<header class="nav" id="nav"><div class="container nav-inner"><a href="../../../" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a><nav><ul class="nav-links"><li><a href="../../../services.html">Services</a></li><li><a href="../../../pricing.html">Pricing</a></li><li><a href="../../../index.html#process">Process</a></li><li><a href="../../../about.html">About</a></li></ul></nav><div class="nav-cta"><a href="../../../portal/login.html" class="btn btn-ghost btn-sm">Sign in</a><a href="../../../quote.html" class="btn btn-primary btn-sm">Free quote</a></div></div></header>"""


FOOTER = """<footer class="footer"><div class="container"><div class="footer-seo"><div><h5>Core services</h5><ul><li><a href="../../../services/planning-drawings.html">Planning permission drawings</a></li><li><a href="../../../services/building-regulations.html">Building regulations drawings</a></li><li><a href="../../../services/loft-conversions.html">Loft conversion drawings</a></li><li><a href="../../../services/house-extensions.html">House extension plans</a></li><li><a href="../../../services/mansard-roof.html">Mansard roof extensions</a></li></ul></div><div><h5>UK cities</h5><ul><li><a href="../manchester/">Architectural drawings Manchester</a></li><li><a href="../birmingham/">Architectural drawings Birmingham</a></li><li><a href="../leeds/">Architectural drawings Leeds</a></li><li><a href="../liverpool/">Architectural drawings Liverpool</a></li><li><a href="../bristol/">Architectural drawings Bristol</a></li></ul></div><div><h5>Heritage cities</h5><ul><li><a href="../edinburgh/">Architectural drawings Edinburgh</a></li><li><a href="../glasgow/">Architectural drawings Glasgow</a></li><li><a href="../oxford/">Architectural drawings Oxford</a></li><li><a href="../cambridge/">Architectural drawings Cambridge</a></li><li><a href="../bath/">Architectural drawings Bath</a></li></ul></div><div><h5>London boroughs</h5><ul><li><a href="../../camden/">Camden</a></li><li><a href="../../islington/">Islington</a></li><li><a href="../../hackney/">Hackney</a></li><li><a href="../../wandsworth/">Wandsworth</a></li><li><a href="../../lambeth/">Lambeth</a></li></ul></div></div><div class="footer-bottom" style="border-top:0;padding-top:0;"><span>&copy; 2026 Architectural Drawings Ltd &middot; 86&ndash;90 Paul Street, London EC2A 4NE</span><span><a href="../../../">Home</a> &middot; <a href="../../../services.html">Services</a> &middot; <a href="../../../pricing.html">Pricing</a> &middot; <a href="../../../privacy.html">Privacy</a> &middot; <a href="../../../terms.html">Terms</a></span></div></div></footer>"""


# ---- City page builder ------------------------------------------------------

def city_page(slug):
    c = CITIES[slug]
    name = c["name"]
    title = f"Architectural Drawings in {name} | Remote Service | AD London"
    description = (
        f"Fixed-fee architectural drawings in {name} delivered remotely by MCIAT "
        f"chartered technologists. Planning, building regs, loft & extension plans from £840."
    )[:165]
    canonical_path = f"/areas/uk/{slug}/"

    related_chips = []
    for other in ORDER:
        if other == slug:
            continue
        related_chips.append(f'<a href="../{other}/">{CITIES[other]["name"]}</a>')
    related_html = "\n".join(related_chips)

    council = c["council"]
    postcodes = c["postcodes"]
    region = c["region"]
    housing = c["housing"]
    conservation = c["conservation"]
    notes = c["notes"]
    blurb = c["blurb"]
    landmarks = c["landmarks"]
    is_scot = c.get("is_scotland", False)

    # Scottish planning wording
    scot_note = ""
    if is_scot:
        scot_note = (
            "<p><strong>A note on Scottish planning.</strong> Applications in "
            f"{name} run under Scottish planning law — Planning Permission, "
            "Building Warrant and (where applicable) Listed Building Consent — "
            "not the English system. Our drawings packs are produced to Scottish "
            "standards and we liaise with your Building Warrant contractor as "
            "part of the fixed fee.</p>"
        )

    # ---- Schema blocks
    breadcrumb_schema = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"' + DOMAIN + '/"},'
        '{"@type":"ListItem","position":2,"name":"Areas","item":"' + DOMAIN + '/areas/"},'
        '{"@type":"ListItem","position":3,"name":"UK","item":"' + DOMAIN + '/areas/uk/nationwide/"},'
        '{"@type":"ListItem","position":4,"name":"' + name + '"}]}'
    )

    service_schema = (
        '{"@context":"https://schema.org","@type":"Service",'
        '"serviceType":"Architectural drawings",'
        '"name":"Architectural drawings in ' + name + '",'
        '"provider":{"@type":"Organization","name":"Architectural Drawings London",'
        '"url":"' + DOMAIN + '/",'
        '"telephone":"+44 20 7946 0000",'
        '"address":{"@type":"PostalAddress","streetAddress":"86–90 Paul Street",'
        '"addressLocality":"London","postalCode":"EC2A 4NE","addressCountry":"GB"}},'
        '"areaServed":{"@type":"City","name":"' + name + '"},'
        '"offers":{"@type":"Offer","priceCurrency":"GBP","price":"840",'
        '"priceSpecification":{"@type":"PriceSpecification","priceCurrency":"GBP","price":"840","valueAddedTaxIncluded":true}},'
        '"description":"Fixed-fee remote architectural drawings service covering ' + name + ' — planning, building regulations, loft conversions, extensions and mansard designs."}'
    )

    # FAQ — 5 Q&A
    faq_items = [
        (
            f"Can you really work outside London on a {name} project?",
            f"Yes. Around one in five of our active projects is outside London and we routinely deliver full planning and building regulations drawings into {council} remotely. Our drawings-first model doesn’t depend on being on-site daily — it depends on an accurate survey, solid policy knowledge, and responsive revisions, all of which we handle digitally.",
        ),
        (
            f"Do you visit the site in {name}?",
            "We offer two options. Most clients use our virtual survey — you provide photos and measurements using our illustrated checklist, we convert that into the CAD survey. For complex heritage or listed projects we can travel to site (chargeable at travel-cost, typically £180–£320 depending on city) and complete a full measured survey in person.",
        ),
        (
            "How does the virtual survey work?",
            "We send you a PDF survey pack with a one-page photo plan, room-by-room measurement checklist, and guidance on capturing floor-to-ceiling heights and window positions. You return it by email within a few days. We then produce existing drawings and send a verification call before proposed design work begins. Most clients complete the survey in 2–3 hours.",
        ),
        (
            f"Do you know {council}’s planning policies?",
            f"Yes. We research every authority’s local plan, supplementary planning documents and relevant Article 4 Directions before committing to a fixed fee. For {name} specifically we maintain a working file on {council}’s current validation requirements, design guides and conservation appraisals. Our 98% first-time approval rate is sustained across every English authority we’ve drawn into.",
        ),
        (
            f"What’s the cost difference versus a local {name} architect?",
            f"Local architects in {name} typically quote at hourly rates of £75–£110 and total project fees from £3,500 upwards for a house extension. Our fixed fees start at £840 and rarely exceed £2,500 even for complex jobs. The saving is roughly 30–50% — we make it work by removing the London-studio overhead and working entirely in digital delivery.",
        ),
    ]

    qa_schema_parts = []
    for q, a in faq_items:
        qa_schema_parts.append(
            '{"@type":"Question","name":' + _js(q) + ','
            '"answerCount":1,'
            '"acceptedAnswer":{"@type":"Answer","text":' + _js(a) + ','
            '"upvoteCount":0,"url":"' + DOMAIN + canonical_path + '",'
            '"author":{"@type":"Organization","name":"Architectural Drawings London"}}}'
        )
    qa_schema = (
        '{"@context":"https://schema.org","@type":"QAPage","mainEntity":[' +
        ",".join(qa_schema_parts) + ']}'
    )

    faq_html = "\n".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>"
        for q, a in faq_items
    )

    body = f"""<script type="application/ld+json">{breadcrumb_schema}</script>
<script type="application/ld+json">{service_schema}</script>
<script type="application/ld+json">{qa_schema}</script>
</head>
<body>
{NAV}

<section class="hero" style="padding-bottom:clamp(20px,4vw,40px);"><div class="container" style="max-width:820px;">
<nav style="font-size:0.85rem;color:var(--ink-soft);margin-bottom:16px;" aria-label="Breadcrumb"><a href="../../../">Home</a><span> / </span><a href="../../">Areas</a><span> / </span><a href="../nationwide/">UK</a><span> / </span><span style="color:var(--ink);">{name}</span></nav>
<span class="eyebrow">UK remote service &middot; {region}</span>
<h1 style="margin:16px 0 24px;font-size:clamp(2.2rem,5.2vw,3.8rem);">Architectural Drawings in <em style="color:var(--accent);font-weight:300;">{name}</em></h1>
<p class="hero-lede">Fixed-fee planning and building regulations drawings for homes across {name} and the wider {region} area &mdash; delivered remotely by MCIAT chartered architectural technologists, with a 98% first-time approval rate across every UK council we&rsquo;ve drawn into.</p>
<div class="meta-row"><span>From &pound;840 fixed fee</span><span>MCIAT chartered</span><span>Remote delivery</span><span>Last updated April 2026</span></div>
<div class="hero-cover" role="img" aria-label="Illustration representing {name} — {landmarks}"><span>{name}</span></div>
</div></section>

<section style="padding-top:0;"><div class="container" style="max-width:760px;">
<div class="article-body">

<div class="notice reveal"><strong>We&rsquo;re London-based, with a nationwide remote service.</strong> We deliver full architectural drawings packs into {council} without needing a local studio. You choose between a <strong>virtual survey</strong> (we guide you through capturing photos and measurements from your own property) or a <strong>site visit</strong> (chargeable at travel cost). Either way, fees, revisions and sign-off are fixed up front &mdash; no hourly billing.</div>

<div class="tldr-box reveal"><h3>The 30-second version</h3><div class="tldr-grid">
<div><div class="tldr-label">Location</div><div class="tldr-value">{name}</div></div>
<div><div class="tldr-label">Council</div><div class="tldr-value">{council}</div></div>
<div><div class="tldr-label">Postcodes</div><div class="tldr-value">{postcodes}</div></div>
<div><div class="tldr-label">Service type</div><div class="tldr-value">Remote + optional visit</div></div>
<div><div class="tldr-label">Fees from</div><div class="tldr-value">&pound;840</div></div>
<div><div class="tldr-label">Approval rate</div><div class="tldr-value">98% first time</div></div>
</div></div>

<h2 id="how">How our remote architectural service works in {name}</h2>
<p>Most {name} homeowners don&rsquo;t need a local architect &mdash; they need accurate drawings, correct planning policy interpretation, and a responsive team that turns revisions around quickly. That&rsquo;s a workflow that runs better digitally than on-site. {blurb}</p>

<div class="process-steps">
<div class="process-step"><div class="num">1</div><h4>Virtual or site survey</h4><p>You capture photos and measurements using our one-page checklist, or we travel to {name} for a full measured survey (chargeable at travel cost).</p></div>
<div class="process-step"><div class="num">2</div><h4>Existing drawings</h4><p>We produce CAD floor plans, elevations and sections from your survey, then verify everything on a 15-minute video call before design work starts.</p></div>
<div class="process-step"><div class="num">3</div><h4>Design &amp; policy check</h4><p>We design against {council} local plan, relevant Article 4 Directions, and any conservation area appraisal &mdash; before anything is committed to a drawing.</p></div>
<div class="process-step"><div class="num">4</div><h4>Submission</h4><p>We prepare the full application pack, submit to the council on the Planning Portal, and manage validation, revisions and officer queries through to decision.</p></div>
</div>

{scot_note}

<h2 id="services">Services and fixed fees</h2>
<p>Every package below is delivered end-to-end by a chartered technologist. Revisions and officer queries are included; no hourly billing.</p>
<div class="service-grid">
<a class="svc-card" href="../../../services/planning-drawings.html"><strong>Planning drawings</strong><span>From &pound;840 &middot; Conservation &amp; Article 4 aware</span></a>
<a class="svc-card" href="../../../services/building-regulations.html"><strong>Building regulations</strong><span>From &pound;1,050 &middot; Structural coordination included</span></a>
<a class="svc-card" href="../../../services/loft-conversions.html"><strong>Loft conversions</strong><span>From &pound;1,225 &middot; Dormer, mansard or Velux</span></a>
<a class="svc-card" href="../../../services/house-extensions.html"><strong>House extensions</strong><span>From &pound;1,750 &middot; Rear, side return, wraparound</span></a>
<a class="svc-card" href="../../../services/mansard-roof.html"><strong>Mansard roofs</strong><span>From &pound;1,575 &middot; Conservation-area friendly</span></a>
</div>

<h2 id="context">{name}&rsquo;s planning context</h2>
<p><strong>Housing stock.</strong> {housing}</p>
<p><strong>Conservation &amp; heritage.</strong> {conservation}</p>
<p><strong>Council approach.</strong> {notes}</p>

<h2 id="why-us">Why choose us for your {name} project</h2>
<div class="why-grid">
<div class="why-card"><strong>MCIAT chartered</strong><span>Every drawing set is signed off by a chartered architectural technologist &mdash; the CIAT-regulated equivalent of an architect for technical design and planning work.</span></div>
<div class="why-card"><strong>30% below local rates</strong><span>Our fixed fees typically run 30&ndash;50% below {name} architect hourly-rate quotes for the same scope of work.</span></div>
<div class="why-card"><strong>98% first-time approval</strong><span>Our national first-time approval rate across all UK authorities we&rsquo;ve drawn into. Revisions are always included if we miss.</span></div>
<div class="why-card"><strong>Fixed fees, no surprises</strong><span>Every package is quoted up front against your scope. Revisions, officer queries and minor policy pivots are included.</span></div>
<div class="why-card"><strong>Digital-native delivery</strong><span>All drawings, revisions and submissions handled via our client portal. No courier fees, no studio visits, no waiting a week for a callback.</span></div>
<div class="why-card"><strong>UK-wide policy coverage</strong><span>We maintain active notes on {council} validation and design guidance, so your drawings hit the ground ready for the local planning officer.</span></div>
</div>

<h2 id="faq">Frequently asked questions</h2>
{faq_html}

<h2 id="related">Architectural drawings in other UK cities</h2>
<p>We offer the same remote service across the UK&rsquo;s major cities. Pick a nearby location for region-specific guidance:</p>
<div class="borough-chips">
{related_html}
<a href="../nationwide/">Full UK coverage &rarr;</a>
</div>

</div></div></section>

<section class="cta-band reveal" style="background:var(--bg-2);"><div class="container"><h2>Planning a project in <span class="accent">{name}?</span></h2><p>Fixed-fee drawings from &pound;840, delivered remotely. MCIAT chartered. 98% first-time approval rate across every UK council we&rsquo;ve drawn into.</p><a href="../../../quote.html" class="btn btn-primary btn-lg">Get a free quote &rarr;</a></div></section>

{FOOTER}

{REVEAL_SCRIPT}

{WHATSAPP_FAB}

</body>
</html>
"""
    return body


def _js(s):
    """JSON-escape a string for schema.org blocks."""
    import json
    return json.dumps(s, ensure_ascii=False)


# ---- Nationwide hub ---------------------------------------------------------

def nationwide_page():
    title = "Architectural Drawings Across the UK | Nationwide Remote Service"
    description = (
        "We provide fixed-fee planning and building regulations drawings remotely "
        "across the UK — all 12 major cities covered. MCIAT chartered. From £840."
    )[:165]
    canonical_path = "/areas/uk/nationwide/"

    breadcrumb_schema = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"' + DOMAIN + '/"},'
        '{"@type":"ListItem","position":2,"name":"Areas","item":"' + DOMAIN + '/areas/"},'
        '{"@type":"ListItem","position":3,"name":"UK"}]}'
    )

    service_schema = (
        '{"@context":"https://schema.org","@type":"Service",'
        '"serviceType":"Architectural drawings",'
        '"name":"Nationwide UK architectural drawings",'
        '"provider":{"@type":"Organization","name":"Architectural Drawings London",'
        '"url":"' + DOMAIN + '/",'
        '"telephone":"+44 20 7946 0000",'
        '"address":{"@type":"PostalAddress","streetAddress":"86–90 Paul Street",'
        '"addressLocality":"London","postalCode":"EC2A 4NE","addressCountry":"GB"}},'
        '"areaServed":{"@type":"Country","name":"United Kingdom"},'
        '"offers":{"@type":"Offer","priceCurrency":"GBP","price":"840"},'
        '"description":"UK-wide remote architectural drawings service: planning, building regulations, loft conversions, extensions and mansard designs."}'
    )

    faq_items = [
        (
            "Do you cover the whole UK or just major cities?",
            "We cover every English, Scottish and Welsh planning authority. The 12 city pages here are our most-requested locations, but we take on projects in small towns and rural sites too — if there’s a council, we’ve drawn to their policies at some point.",
        ),
        (
            "Is the service quality the same outside London?",
            "Yes — every drawing set is signed off by the same chartered architectural technologists who produce our London work. Policy research, submission handling and revisions are identical regardless of location.",
        ),
        (
            "Do you visit the site?",
            "Optional. Most clients use our virtual survey at no extra cost. Where site visits are needed (listed buildings, complex existing conditions, listed fabric reports) we travel at cost — typically £180–£320 per visit depending on city, all quoted up front.",
        ),
        (
            "How do you handle Scottish planning?",
            "Scottish projects (Edinburgh, Glasgow and the wider Scottish councils) run under the Scottish planning system — Planning Permission and Building Warrant rather than the English Building Regulations system. Our Scottish drawings packs are produced to this standard and we liaise directly with Building Warrant contractors.",
        ),
        (
            "What’s the turnaround?",
            "Existing drawings from your survey: 5–10 working days. Proposed design set: 7–14 working days after brief sign-off. Full application ready for submission: typically 3 weeks from start. Same nationwide as in London.",
        ),
    ]

    qa_schema_parts = []
    for q, a in faq_items:
        qa_schema_parts.append(
            '{"@type":"Question","name":' + _js(q) + ','
            '"answerCount":1,'
            '"acceptedAnswer":{"@type":"Answer","text":' + _js(a) + ','
            '"upvoteCount":0,"url":"' + DOMAIN + canonical_path + '",'
            '"author":{"@type":"Organization","name":"Architectural Drawings London"}}}'
        )
    qa_schema = (
        '{"@context":"https://schema.org","@type":"QAPage","mainEntity":[' +
        ",".join(qa_schema_parts) + ']}'
    )

    faq_html = "\n".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>"
        for q, a in faq_items
    )

    # City grid
    city_cards = []
    for slug in ORDER:
        c = CITIES[slug]
        city_cards.append(
            f'<a class="svc-card" href="../{slug}/">'
            f'<strong>{c["name"]}</strong>'
            f'<span>{c["region"]} &middot; {c["council"]}</span></a>'
        )
    city_cards_html = "\n".join(city_cards)

    body = f"""<script type="application/ld+json">{breadcrumb_schema}</script>
<script type="application/ld+json">{service_schema}</script>
<script type="application/ld+json">{qa_schema}</script>
</head>
<body>
{NAV}

<section class="hero" style="padding-bottom:clamp(20px,4vw,40px);"><div class="container" style="max-width:820px;">
<nav style="font-size:0.85rem;color:var(--ink-soft);margin-bottom:16px;" aria-label="Breadcrumb"><a href="../../../">Home</a><span> / </span><a href="../../">Areas</a><span> / </span><span style="color:var(--ink);">UK</span></nav>
<span class="eyebrow">Nationwide remote service</span>
<h1 style="margin:16px 0 24px;font-size:clamp(2.2rem,5.2vw,3.8rem);">We Cover All of the <em style="color:var(--accent);font-weight:300;">United Kingdom</em></h1>
<p class="hero-lede">We&rsquo;re based in London but deliver fixed-fee architectural drawings into every UK planning authority remotely. Virtual surveys, chartered sign-off, 98% first-time approval &mdash; same studio, same prices, anywhere in Britain.</p>
<div class="meta-row"><span>From &pound;840 fixed fee</span><span>MCIAT chartered</span><span>All UK councils</span><span>Last updated April 2026</span></div>
<div class="hero-cover" role="img" aria-label="Illustration representing the United Kingdom"><span>UK-wide</span></div>
</div></section>

<section style="padding-top:0;"><div class="container" style="max-width:760px;">
<div class="article-body">

<div class="notice reveal"><strong>London studio, UK delivery.</strong> Our drawings-first workflow doesn&rsquo;t need a local branch. Around one in five of our active projects is outside London and we&rsquo;ve delivered into every type of UK authority &mdash; from Scottish tenements under the Building Warrant system to UNESCO-protected Bath stone. Pricing, revisions and turnaround match our London work.</div>

<h2 id="cities">12 major UK cities we cover</h2>
<p>Pick a location for city-specific planning context, housing stock notes and council policy guidance:</p>
<div class="service-grid">
{city_cards_html}
</div>

<h2 id="beyond">Beyond the 12 cities</h2>
<p>The pages above cover our most-requested UK cities but our remote service extends to <strong>every UK planning authority</strong>. Whether you&rsquo;re in a market town in Shropshire, a Cornish village, a Welsh valley or a Scottish island, the workflow is identical: virtual survey, design against your local plan, submission managed on the Planning Portal, revisions included in the fixed fee.</p>

<h2 id="how">How the remote service works</h2>
<div class="process-steps">
<div class="process-step"><div class="num">1</div><h4>Free initial call</h4><p>15-minute video call. We scope the project, check feasibility against local policy, and confirm a fixed fee.</p></div>
<div class="process-step"><div class="num">2</div><h4>Virtual survey</h4><p>We send a photo-and-measurement checklist. You complete it at your own pace; most clients finish in 2&ndash;3 hours. Site visits available if preferred (chargeable at travel cost).</p></div>
<div class="process-step"><div class="num">3</div><h4>Existing drawings</h4><p>CAD floor plans, elevations and sections produced from your survey. Verified on a second video call before design begins.</p></div>
<div class="process-step"><div class="num">4</div><h4>Design &amp; submission</h4><p>Full application pack prepared against your local authority&rsquo;s requirements, submitted on the Planning Portal, and managed through to decision.</p></div>
</div>

<h2 id="services">Services available UK-wide</h2>
<div class="service-grid">
<a class="svc-card" href="../../../services/planning-drawings.html"><strong>Planning drawings</strong><span>From &pound;840</span></a>
<a class="svc-card" href="../../../services/building-regulations.html"><strong>Building regulations</strong><span>From &pound;1,050</span></a>
<a class="svc-card" href="../../../services/loft-conversions.html"><strong>Loft conversions</strong><span>From &pound;1,225</span></a>
<a class="svc-card" href="../../../services/house-extensions.html"><strong>House extensions</strong><span>From &pound;1,750</span></a>
<a class="svc-card" href="../../../services/mansard-roof.html"><strong>Mansard roofs</strong><span>From &pound;1,575</span></a>
</div>

<h2 id="why">Why clients outside London choose us</h2>
<div class="why-grid">
<div class="why-card"><strong>Price</strong><span>Our fixed fees run 30&ndash;50% below typical local architect hourly quotes for the same scope of work.</span></div>
<div class="why-card"><strong>Specialism</strong><span>We do nothing but residential drawings. Most local generalist practices split attention between commercial and residential &mdash; we don&rsquo;t.</span></div>
<div class="why-card"><strong>Speed</strong><span>Digital-native workflow means faster turnaround on revisions and officer queries. No waiting a week for a callback.</span></div>
<div class="why-card"><strong>Chartered sign-off</strong><span>Every drawing set is produced under MCIAT chartered supervision &mdash; the CIAT-regulated equivalent of an architect for technical drawings and planning submissions.</span></div>
<div class="why-card"><strong>Policy coverage</strong><span>We maintain active working notes on all UK local plans, Article 4 Directions, conservation appraisals and listed-building guidance.</span></div>
<div class="why-card"><strong>Fixed fees</strong><span>No hourly billing. What we quote is what you pay, including revisions and officer queries.</span></div>
</div>

<h2 id="faq">Frequently asked questions</h2>
{faq_html}

</div></div></section>

<section class="cta-band reveal" style="background:var(--bg-2);"><div class="container"><h2>Got a project <span class="accent">outside London?</span></h2><p>Fixed-fee drawings from &pound;840, delivered remotely anywhere in the UK. MCIAT chartered. 98% first-time approval rate.</p><a href="../../../quote.html" class="btn btn-primary btn-lg">Get a free quote &rarr;</a></div></section>

{FOOTER}

{REVEAL_SCRIPT}

{WHATSAPP_FAB}

</body>
</html>
"""
    return body


# ---- Main -------------------------------------------------------------------

def main():
    # City pages
    for slug in ORDER:
        c = CITIES[slug]
        path = OUT / slug / "index.html"
        title = f"Architectural Drawings in {c['name']} | Remote Service | AD London"
        description = (
            f"Fixed-fee architectural drawings in {c['name']} delivered remotely by "
            f"MCIAT chartered technologists. Planning, building regs, loft & extension "
            f"plans from £840."
        )
        # Truncate if over 165 chars
        if len(description) > 165:
            description = description[:162] + "…"
        canonical_path = f"/areas/uk/{slug}/"
        head_html = head(title, description, canonical_path)
        body_html = city_page(slug)
        path.write_text(head_html + "\n" + body_html, encoding="utf-8")
        print(f"Wrote {path}  ({len(head_html + body_html):,} bytes)")

    # Nationwide hub
    path = OUT / "nationwide" / "index.html"
    title = "Architectural Drawings Across the UK | Nationwide Remote Service"
    description = (
        "Fixed-fee planning and building regulations drawings delivered remotely "
        "across the UK — all 12 major cities covered. MCIAT chartered. From £840."
    )
    if len(description) > 165:
        description = description[:162] + "…"
    canonical_path = "/areas/uk/nationwide/"
    head_html = head(title, description, canonical_path)
    body_html = nationwide_page()
    path.write_text(head_html + "\n" + body_html, encoding="utf-8")
    print(f"Wrote {path}  ({len(head_html + body_html):,} bytes)")


if __name__ == "__main__":
    main()
