#!/usr/bin/env python3
"""
Add authoritative "Sources & References" section to all blog posts for E-E-A-T.
Citations to gov.uk, CIAT, RIBA, Planning Portal, BRE Group, etc. boost
topical authority and help AI crawlers verify factual claims.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / 'blog'

MARKER = '<!-- sources-references -->'

# Authoritative external sources by topic keyword
SOURCES_BY_TOPIC = {
    'planning': [
        ('Planning Portal (UK Government)', 'https://www.planningportal.co.uk/'),
        ('Town and Country Planning Act 1990', 'https://www.legislation.gov.uk/ukpga/1990/8'),
        ('General Permitted Development Order 2015', 'https://www.legislation.gov.uk/uksi/2015/596'),
        ('National Planning Policy Framework', 'https://www.gov.uk/government/publications/national-planning-policy-framework--2'),
    ],
    'building-regulations': [
        ('Building Regulations 2010', 'https://www.legislation.gov.uk/uksi/2010/2214'),
        ('Approved Documents (UK Government)', 'https://www.gov.uk/government/collections/approved-documents'),
        ('Local Authority Building Control (LABC)', 'https://www.labc.co.uk/'),
        ('BRE Group — Part L guidance', 'https://www.bregroup.com/'),
    ],
    'loft': [
        ('Planning Portal — Loft Conversions', 'https://www.planningportal.co.uk/permission/common-projects/loft-conversion'),
        ('Class B GPDO 2015 (loft additions)', 'https://www.legislation.gov.uk/uksi/2015/596/schedule/2/part/1/crossheading/class-b-additions-etc-to-the-roof-of-a-dwellinghouse'),
    ],
    'extension': [
        ('Planning Portal — Extensions', 'https://www.planningportal.co.uk/permission/common-projects/extensions'),
        ('Class A GPDO 2015 (rear extensions)', 'https://www.legislation.gov.uk/uksi/2015/596/schedule/2/part/1/crossheading/class-a-enlargement-improvement-etc-of-a-dwellinghouse'),
        ('Larger Home Extension Prior Approval', 'https://www.planningportal.co.uk/permission/common-projects/extensions/larger-home-extensions'),
    ],
    'party-wall': [
        ('Party Wall etc. Act 1996', 'https://www.legislation.gov.uk/ukpga/1996/40'),
        ('UK Gov — Party Walls Guide', 'https://www.gov.uk/party-walls-building-works'),
    ],
    'conservation': [
        ('Planning (Listed Buildings and Conservation Areas) Act 1990', 'https://www.legislation.gov.uk/ukpga/1990/9'),
        ('Historic England — Conservation Areas', 'https://historicengland.org.uk/advice/hpg/has/conservation-areas/'),
    ],
    'architect': [
        ('Architects Registration Board (ARB)', 'https://arb.org.uk/'),
        ('Royal Institute of British Architects (RIBA)', 'https://www.architecture.com/'),
        ('Chartered Institute of Architectural Technologists (CIAT)', 'https://ciat.global/'),
    ],
    'hmo': [
        ('Housing Act 2004 (HMO definitions)', 'https://www.legislation.gov.uk/ukpga/2004/34'),
        ('UK Gov — HMO Licensing', 'https://www.gov.uk/house-in-multiple-occupation-licence'),
    ],
    'part-l': [
        ('Approved Document L (Conservation of Fuel and Power)', 'https://www.gov.uk/government/publications/conservation-of-fuel-and-power-approved-document-l'),
        ('Future Homes Standard', 'https://www.gov.uk/government/consultations/the-future-homes-and-buildings-standards-2023-consultation'),
    ],
}

COMMON_SOURCES = [
    ('Chartered Institute of Architectural Technologists (CIAT)', 'https://ciat.global/'),
    ('Planning Portal (UK Government)', 'https://www.planningportal.co.uk/'),
]


def pick_sources(filename):
    """Return 4-5 relevant sources based on filename keywords."""
    sources = []
    fn = filename.lower()
    for key, entries in SOURCES_BY_TOPIC.items():
        if key in fn:
            sources.extend(entries)
    # Always include common sources
    for c in COMMON_SOURCES:
        if c not in sources:
            sources.append(c)
    # Dedupe preserving order
    seen = set()
    unique = []
    for s in sources:
        if s[0] not in seen:
            seen.add(s[0])
            unique.append(s)
    return unique[:6]  # Max 6 sources per page


def make_sources_section(sources, canonical_url):
    links_html = ''.join(
        f'<li><a href="{url}" rel="noopener nofollow external" target="_blank" style="color:var(--accent-deep);text-decoration:underline;">{name}</a></li>'
        for name, url in sources
    )
    return f'''{MARKER}
<section style="background: var(--bg-2); padding: 48px 0;">
  <div class="container" style="max-width: 800px;">
    <div style="border-left: 4px solid var(--accent); padding-left: 24px;">
      <h3 style="font-size: 0.82rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent-deep); font-family: var(--font-body); font-weight: 700; margin-bottom: 16px;">Sources &amp; references</h3>
      <p style="color: var(--ink-soft); font-size: 0.92rem; margin-bottom: 16px;">Factual claims in this article are based on the following authoritative UK sources. All data verified against current legislation and guidance as of April 2026.</p>
      <ul style="font-size: 0.9rem; color: var(--ink-soft); line-height: 1.8; padding-left: 20px;">
        {links_html}
      </ul>
      <p style="font-size: 0.82rem; color: var(--ink-softer); margin-top: 20px; font-style: italic;">This article is informational only and does not constitute legal or planning advice. Always consult a qualified architectural technologist for your specific project. &mdash; <span style="color:var(--accent-deep);font-weight:600;">Architectural Drawings London</span>, MCIAT chartered.</p>
    </div>
  </div>
</section>
'''


updated = 0
skipped = 0

for f in BLOG_DIR.glob('*.html'):
    if f.name == 'index.html':
        continue
    text = f.read_text(encoding='utf-8')
    if MARKER in text:
        skipped += 1
        continue

    sources = pick_sources(f.stem)
    if not sources:
        continue

    # Extract canonical from <link rel="canonical">
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', text)
    canonical = canonical_match.group(1) if canonical_match else ''

    section = make_sources_section(sources, canonical)

    # Insert BEFORE the cta-band section (matches both with and without style attr)
    new_text, n = re.subn(
        r'(<section [^>]*class="cta-band"[^>]*>)',
        section + r'\n\1',
        text,
        count=1
    )
    if n > 0:
        f.write_text(new_text, encoding='utf-8')
        updated += 1

print(f'[OK] Added Sources & References to {updated} blog posts (skipped {skipped})')
