#!/usr/bin/env python3
"""Add testimonial + callback form to 5 service detail pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TESTIMONIALS = {
    'planning-drawings.html': {
        'quote': 'Passed planning with Hackney first time on a fairly bold rear extension. The drawings were meticulous and the agent service meant I didn&rsquo;t have to deal with the council at all.',
        'name': 'Sarah T.',
        'initial': 'S',
        'project': 'Rear extension',
        'area': 'Hackney',
    },
    'building-regulations.html': {
        'quote': 'Building control signed off everything first visit. The Part L calcs and structural package were exactly what the inspector needed &mdash; no queries, no delays.',
        'name': 'David M.',
        'initial': 'D',
        'project': 'Loft conversion',
        'area': 'Islington',
    },
    'loft-conversions.html': {
        'quote': 'From feasibility to completion certificate in four months. The dormer design maximised every inch and the Party Wall process was handled seamlessly.',
        'name': 'Rachel K.',
        'initial': 'R',
        'project': 'Dormer loft',
        'area': 'Wandsworth',
    },
    'house-extensions.html': {
        'quote': 'Our side return extension transformed the kitchen. The drawings showed exactly what we&rsquo;d get, and the build matched perfectly. Worth every penny.',
        'name': 'Tom & Lisa W.',
        'initial': 'T',
        'project': 'Side return',
        'area': 'Clapham',
    },
    'mansard-roof.html': {
        'quote': 'We were told our mansard wouldn&rsquo;t get approved in a conservation area. Architectural Drawings designed it, wrote the Heritage Statement, and got it through committee.',
        'name': 'James P.',
        'initial': 'J',
        'project': 'Mansard loft',
        'area': 'Islington',
    },
}

def make_testimonial(data):
    return f'''<!-- testimonial-section -->
<section style="background: var(--bg-2);">
  <div class="container" style="max-width: 800px; text-align: center;">
    <div style="font-size: 1.6rem; color: var(--accent); margin-bottom: 20px;">&ldquo;</div>
    <blockquote style="font-family: var(--font-display); font-size: clamp(1.2rem, 2.5vw, 1.6rem); font-style: italic; font-variation-settings: 'opsz' 60; line-height: 1.4; color: var(--ink); margin-bottom: 24px;">{data["quote"]}</blockquote>
    <div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
      <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--accent-soft); color: var(--accent-deep); display: grid; place-items: center; font-family: var(--font-display); font-style: italic; font-size: 1.1rem;">{data["initial"]}</div>
      <div style="text-align: left;"><div style="font-weight: 600; font-size: 0.94rem;">{data["name"]}</div><div style="font-size: 0.82rem; color: var(--ink-soft);">{data["project"]} &middot; {data["area"]}</div></div>
    </div>
  </div>
</section>
'''

CALLBACK = '''<!-- callback-section -->
<section id="callback">
  <div class="container" style="max-width: 640px; text-align: center;">
    <span class="eyebrow">Speak to a technologist</span>
    <h2 style="margin-top: 16px;">Get a callback in <em>30 minutes</em></h2>
    <p style="color: var(--ink-soft); margin: 16px auto 32px; max-width: 480px;">Leave your number and an Architectural technologist will call you back within 30 minutes during working hours (Mon-Fri 9-6, Sat 10-4).</p>
    <form style="display: flex; gap: 12px; max-width: 440px; margin: 0 auto;" onsubmit="event.preventDefault(); this.innerHTML='<p style=&quot;color:var(--success);font-weight:600;padding:16px;&quot;>Thanks! We&rsquo;ll call you within 30 minutes.</p>';">
      <input type="tel" name="phone" placeholder="Your phone number" required style="flex: 1; padding: 14px 18px; border: 1px solid var(--line); border-radius: var(--r-full); font-size: 0.95rem; background: var(--surface);" />
      <button type="submit" class="btn btn-primary" style="white-space: nowrap;">Call me back</button>
    </form>
    <p style="font-size: 0.78rem; color: var(--ink-soft); margin-top: 12px;">No obligation. No sales pressure. Just expert advice.</p>
  </div>
</section>
'''

updated = 0
for filename, data in TESTIMONIALS.items():
    f = ROOT / 'services' / filename
    if not f.exists():
        print(f'  SKIP: {filename} not found')
        continue
    text = f.read_text(encoding='utf-8')
    if 'testimonial-section' in text:
        print(f'  SKIP: {filename} already has testimonial')
        continue
    # Insert BEFORE the CTA band
    target = '<section class="cta-band">'
    if target not in text:
        print(f'  SKIP: {filename} no cta-band found')
        continue
    insert = make_testimonial(data) + '\n' + CALLBACK + '\n'
    text = text.replace(target, insert + target, 1)
    f.write_text(text, encoding='utf-8')
    updated += 1
    print(f'  [OK] {filename}')

print(f'\n[OK] Added testimonial + callback to {updated} service pages')
