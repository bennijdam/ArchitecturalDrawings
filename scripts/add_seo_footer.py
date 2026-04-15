#!/usr/bin/env python3
"""Add SEO footer link grid to all pages that don't have it yet."""
import glob

FOOTER_SEO_CSS = """
/* Footer SEO link grid */
.footer-seo { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.5rem; padding-bottom: 3rem; margin-bottom: 3rem; border-bottom: 1px solid var(--line); }
@media (max-width: 820px) { .footer-seo { grid-template-columns: 1fr 1fr; gap: 2rem; } }
@media (max-width: 500px) { .footer-seo { grid-template-columns: 1fr; } }
.footer-seo h5 { font-family: var(--font-body); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.18em; color: var(--ink); margin-bottom: 1.1rem; }
.footer-seo ul { list-style: none; display: flex; flex-direction: column; gap: 0.55rem; }
.footer-seo a { font-size: 0.85rem; color: var(--ink-soft); transition: color 0.2s var(--ease); line-height: 1.4; }
.footer-seo a:hover { color: var(--accent-deep); }
"""

def get_seo_block(prefix=''):
    p = prefix
    return f"""
    <!-- SEO link grid -->
    <div class="footer-seo">
      <div>
        <h5>Services in London</h5>
        <ul>
          <li><a href="{p}services/planning-drawings.html">Planning permission drawings London</a></li>
          <li><a href="{p}services/building-regulations.html">Building regulations drawings London</a></li>
          <li><a href="{p}services/loft-conversions.html">Loft conversion drawings London</a></li>
          <li><a href="{p}services/house-extensions.html">House extension plans London</a></li>
          <li><a href="{p}services/mansard-roof.html">Mansard roof extensions London</a></li>
          <li><a href="{p}services.html">Measured survey London</a></li>
          <li><a href="{p}services.html">Lawful development certificate</a></li>
          <li><a href="{p}services.html">Permitted development drawings</a></li>
          <li><a href="{p}services.html">Party wall drawings</a></li>
          <li><a href="{p}services.html">Structural calculations</a></li>
        </ul>
      </div>
      <div>
        <h5>Loft conversions by borough</h5>
        <ul>
          <li><a href="{p}areas/camden/loft-conversions.html">Loft conversion Camden</a></li>
          <li><a href="{p}areas/islington/loft-conversions.html">Loft conversion Islington</a></li>
          <li><a href="{p}areas/hackney/loft-conversions.html">Loft conversion Hackney</a></li>
          <li><a href="{p}areas/tower-hamlets/loft-conversions.html">Loft conversion Tower Hamlets</a></li>
          <li><a href="{p}areas/westminster/loft-conversions.html">Loft conversion Westminster</a></li>
          <li><a href="{p}areas/kensington-and-chelsea/loft-conversions.html">Loft conversion Kensington</a></li>
          <li><a href="{p}areas/hammersmith-and-fulham/loft-conversions.html">Loft conversion Hammersmith</a></li>
          <li><a href="{p}areas/wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
          <li><a href="{p}areas/lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
          <li><a href="{p}areas/southwark/loft-conversions.html">Loft conversion Southwark</a></li>
        </ul>
      </div>
      <div>
        <h5>Extension plans by borough</h5>
        <ul>
          <li><a href="{p}areas/lewisham/house-extensions.html">Extension plans Lewisham</a></li>
          <li><a href="{p}areas/greenwich/house-extensions.html">Extension plans Greenwich</a></li>
          <li><a href="{p}areas/bromley/house-extensions.html">Extension plans Bromley</a></li>
          <li><a href="{p}areas/croydon/house-extensions.html">Extension plans Croydon</a></li>
          <li><a href="{p}areas/merton/house-extensions.html">Extension plans Merton</a></li>
          <li><a href="{p}areas/kingston-upon-thames/house-extensions.html">Extension plans Kingston</a></li>
          <li><a href="{p}areas/richmond-upon-thames/house-extensions.html">Extension plans Richmond</a></li>
          <li><a href="{p}areas/hounslow/house-extensions.html">Extension plans Hounslow</a></li>
          <li><a href="{p}areas/ealing/house-extensions.html">Extension plans Ealing</a></li>
          <li><a href="{p}areas/hillingdon/house-extensions.html">Extension plans Hillingdon</a></li>
          <li><a href="{p}areas/harrow/house-extensions.html">Extension plans Harrow</a></li>
          <li><a href="{p}areas/brent/house-extensions.html">Extension plans Brent</a></li>
        </ul>
      </div>
      <div>
        <h5>Planning drawings by borough</h5>
        <ul>
          <li><a href="{p}areas/barnet/planning-drawings.html">Planning drawings Barnet</a></li>
          <li><a href="{p}areas/haringey/planning-drawings.html">Planning drawings Haringey</a></li>
          <li><a href="{p}areas/enfield/planning-drawings.html">Planning drawings Enfield</a></li>
          <li><a href="{p}areas/waltham-forest/planning-drawings.html">Planning drawings Waltham Forest</a></li>
          <li><a href="{p}areas/redbridge/planning-drawings.html">Planning drawings Redbridge</a></li>
          <li><a href="{p}areas/newham/planning-drawings.html">Planning drawings Newham</a></li>
          <li><a href="{p}areas/bexley/planning-drawings.html">Planning drawings Bexley</a></li>
          <li><a href="{p}areas/havering/planning-drawings.html">Planning drawings Havering</a></li>
          <li><a href="{p}areas/sutton/planning-drawings.html">Planning drawings Sutton</a></li>
          <li><a href="{p}areas/barking-and-dagenham/planning-drawings.html">Planning drawings Barking</a></li>
          <li><a href="{p}areas/city-of-london/planning-drawings.html">Planning drawings City of London</a></li>
        </ul>
      </div>
    </div>
"""

# Pages to update
root_pages = ['services.html', 'pricing.html', 'about.html', 'quote.html', 'search.html', 'privacy.html', 'terms.html']
service_pages = glob.glob('services/*.html')
blog_pages = glob.glob('blog/*.html') + glob.glob('projects/*.html')

count = 0

for filepath in root_pages + service_pages + blog_pages:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'footer-seo' in content:
        print(f'  SKIP: {filepath}')
        continue

    # Determine prefix
    if '/' in filepath.replace('\\', '/'):
        prefix = '../'
    else:
        prefix = ''

    # 1. Add CSS before fail-safe reveal
    if '.footer-seo' not in content:
        content = content.replace(
            '/* ===== Fail-safe reveal',
            FOOTER_SEO_CSS + '\n/* ===== Fail-safe reveal'
        )

    # 2. Add SEO block before footer-grid or footer-bottom
    seo_block = get_seo_block(prefix)
    if '<div class="footer-grid">' in content:
        content = content.replace(
            '<div class="footer-grid">',
            seo_block + '\n    <div class="footer-grid">',
            1
        )
    elif '<div class="footer-bottom"' in content:
        content = content.replace(
            '<div class="footer-bottom"',
            seo_block + '\n    <div class="footer-bottom"',
            1
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f'  Updated: {filepath}')

print(f'\nTotal updated: {count}')
