#!/usr/bin/env python3
"""Add FAQ sections + FAQPage schema to 8 guide pages."""
import re
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent

# Guide-specific FAQ data
GUIDES_FAQ = {
    "guides/extensions/index.html": {
        "title": "House Extensions FAQs",
        "faqs": [
            ("Do I need planning permission for a house extension?", "Most single-storey rear extensions up to 4m (3m for semi-detached) and side-return infill extensions are permitted development. Extensions taller than 4m or protruding further require planning permission. We confirm at your free site visit."),
            ("What is the maximum size of a permitted development extension?", "Single-storey extensions can be up to 4m deep (3m for semis), 4m tall, and cannot exceed 50% of your original garden area. Two-storey extensions may be permitted development if they meet specific setback rules from your garden boundary."),
            ("How long does extension planning permission take?", "Most extension applications take 8-13 weeks from submission. Pre-application advice (2-3 weeks) reduces refusal risk. Appeals take 16-32 weeks depending on representation type. We manage the timeline and keep you updated."),
            ("What are the typical costs for extension drawings?", "Fixed-fee extension drawings start from £840 (Essentials package) to £1,750+ (Complete). Costs depend on extension type, complexity, and whether planning or building regulations approval is needed. We provide a fixed quote at no obligation."),
            ("Can I build an extension as a flat?", "Technically yes, but each flat needs separate planning permission and building regulations approval. Leasehold flats face additional challenges: landlord/freeholder consent and service charge negotiations. We handle the technical drawings; you'll need freeholder approval."),
        ]
    },
    "guides/lofts/index.html": {
        "title": "Loft Conversion FAQs",
        "faqs": [
            ("Are loft conversions permitted development in London?", "Most loft conversions are NOT permitted development in London — planning permission is required. Exception: a small rear dormer (up to 40% of roof depth) in conservation areas. Every case is different; we assess feasibility at your free site visit."),
            ("What types of loft conversions are possible in London homes?", "Common types: rear dormer (most frequent), hip-to-gable (semi-detached houses), mansard (period terraces), Velux conversion (if ridge height allows). We recommend the best structural and planning route for your home."),
            ("How much does a loft conversion cost?", "Fixed-fee loft conversion drawings start from £1,225 (Essentials) to £2,850+ (Complete). Total project cost (structure, building control, labour) ranges £50k–£120k depending on type and location. Our drawings are typically 8–10% of total cost."),
            ("Do I need building regulations approval for a loft conversion?", "Yes — every loft conversion requires Building Regulations approval. This covers structural safety, fire egress, insulation, and ventilation. We include all technical compliance in our Complete and Bespoke packages. Building Control sign-off is essential before occupation."),
            ("Will my loft conversion need Party Wall notices?", "Most loft conversions require Party Wall notices to adjoining neighbours — typically for new beams or raising the party wall. We co-ordinate the notice process; our engineer handles the structural element. Neighbours have 14 days to respond."),
        ]
    },
    "guides/planning/index.html": {
        "title": "Planning Permission FAQs",
        "faqs": [
            ("What is the difference between planning permission and permitted development?", "Permitted development is automatic rights for certain minor works (extensions up to 4m, small dormers, certain roof work). Planning permission is required for larger or sensitive schemes. We confirm which applies to your project; when in doubt, apply for planning permission to avoid enforcement action."),
            ("How do I apply for planning permission in London?", "Submit an application to your local council via their planning portal. Required documents: completed application form, site plans, proposed drawings (which we provide), design and access statement, and relevant drawings. Most councils accept applications within 7 days if complete. Decision typically takes 13 weeks."),
            ("What happens if my planning application is refused?", "You can appeal to the Planning Inspectorate within 12 weeks of refusal. Appeals are decided by written representation (16–20 weeks) or public hearing (24–32 weeks). We prepare appeal statements and revised drawings addressing the refusal reason."),
            ("Are planning applications in conservation areas different?", "Yes — stricter design scrutiny, smaller permitted development rights, and additional requirements (heritage statement, character assessment). Applications take longer (16+ weeks). We prepare comprehensive conservation-area applications with heritage context."),
            ("What is pre-application advice and should I use it?", "Pre-application advice (also called 'pre-app') is informal discussion with a council officer before formal submission. Cost: £25–150. Benefit: early feedback on viability, design concerns, and approval likelihood — reducing refusal risk by 60–70%. We recommend it for complex schemes."),
        ]
    },
    "guides/properties/victorian-terrace/index.html": {
        "title": "Victorian Terrace FAQs",
        "faqs": [
            ("What are my permitted development rights for a Victorian terrace?", "Victorian terraces have standard PD rights: single-storey rear extensions (up to 4m), side-return infill (if possible), roof dormers (with limits), and some roof work. Party Wall notices are almost always required because Victorian walls are party walls. We confirm exactly what's permitted at survey."),
            ("Do I need a Party Wall agreement for work on my Victorian terrace?", "Almost certainly yes. Victorian party walls require Party Wall notices and awards for: loft conversions, raising the roof, extensions touching the party wall, and structural alterations. The award costs £500–1,500 but protects neighbours and your indemnity. We co-ordinate the process."),
            ("What extension types suit Victorian terraces best?", "Rear extensions (single or double-storey), side-return infill (if side access exists), and hip-to-gable lofts (semi-detached only) are most common and least risky. Mansard extensions suit period terraces if in a conservation area with precedent. We assess your specific terrace layout and conservation status."),
            ("Are Victorian terraces often in conservation areas?", "Many are — Inner London conservation areas protect significant Victorian terraces. In conservation areas: stricter design rules, no PD for dormers, and heritage statements required. Refurbishment details matter (sash windows, original features). We handle conservation-area applications with appropriate heritage context."),
            ("What are typical costs for extending a Victorian terrace?", "Drawing fees: £840–£1,750+. Build cost for rear extension: £50k–£90k. Loft conversion: £60k–£110k. Party Wall award: £500–£1,500. Timing: 8–13 weeks for planning + 12–16 weeks building works. We provide fixed-fee drawings; you'll manage the build cost separately."),
        ]
    },
    "guides/properties/edwardian-semi/index.html": {
        "title": "Edwardian Semi-Detached House FAQs",
        "faqs": [
            ("Can I do a hip-to-gable loft conversion on my Edwardian semi?", "Yes — hip-to-gable conversions are very common on Edwardian semis (typically built 1900–1920). Planning permission is usually required unless you're on a side-elevation slope in a non-conservation area. We assess your specific roof pitch and orientation at survey. Most hip-to-gables yield 40–50m² of floor space."),
            ("What is the biggest extension I can build without planning on an Edwardian semi?", "You have standard permitted development: single-storey rear extension (4m max, 4m high), side-return infill (if it fits), and some roof dormers. For semis, rear extensions cannot touch the party wall. Double-storey extensions and changes to the front always need planning permission."),
            ("Do Edwardian semis need side-return extensions or rear extensions?", "Both are common. Side-returns (if you have side access) add kitchen/dining space narrowly. Rear extensions provide larger kitchens and dining areas but reduce garden. Wraparound extensions (side + rear) maximize gain on tight plots. We recommend the best layout at survey."),
            ("How much does a loft conversion cost on an Edwardian semi?", "Hip-to-gable loft conversion cost (drawings + build): £70k–£120k total. Drawing fees: £1,225–£2,850+. Structural steelwork for hip-to-gable: £8k–£15k. Building Control and certification: included in our Complete package. Most Edwardian semis suit hip-to-gable; Velux conversions are limited due to roof pitch."),
            ("What about Party Wall for Edwardian semis?", "Most structural work (loft conversions, extensions touching the party wall, raising the roof) requires Party Wall notices. Edwardian semis have party walls on both sides, so notice goes to one neighbour per wall. Cost: £600–£1,500 per award. We co-ordinate the process."),
        ]
    },
    "guides/properties/georgian-townhouse/index.html": {
        "title": "Georgian Townhouse FAQs",
        "faqs": [
            ("Can I extend a Georgian listed building?", "Extensions to listed buildings require Listed Building Consent (in addition to planning). Design must respect the original Georgian character: materials, proportion, fenestration. Rear extensions are usually safer (less visible) than front changes. We prepare heritage statements and conservation-compliant designs."),
            ("Are Georgian townhouses usually in conservation areas?", "Most Georgian townhouses are in conservation areas (Central London, Bath, Edinburgh, etc.). Conservation area status adds design scrutiny: stricter rules on materials, fenestration, and alterations. Original features (sash windows, cornicing, door cases) must be retained. We handle conservation-area applications."),
            ("What about mansard extensions on a Georgian townhouse?", "Mansards suit Georgian terraces architecturally (period precedent exists). However: listed building consent + planning permission both required. Design must match original eave line and materials. Cost higher due to heritage compliance. Planning approval timeline: 16–20 weeks."),
            ("Do Georgian townhouses need planning permission for internal alterations?", "Internal work typically does NOT need planning permission (unless it's listed building consent for structural removal of walls, chimneys, or original features). Structural alterations, new windows, or changes affecting the exterior require consent. We advise on what needs approval."),
            ("What are typical costs for a Georgian townhouse extension or refurb?", "Extension drawings: £1,200–£2,500+ (heritage premium). Listed building consent: ~£500 application fee. Rear extension build cost: £60k–£100k+. Mansard (if feasible): £80k–£150k+. Heritage compliance adds time and cost. We manage design and consent strategy."),
        ]
    },
    "guides/properties/1930s-semi/index.html": {
        "title": "1930s Semi-Detached House FAQs",
        "faqs": [
            ("Are 1930s semis good candidates for hip-to-gable loft conversions?", "Very good — 1930s semis typically have hip roofs and good ridge heights, making hip-to-gable conversions ideal. Planning permission required in most areas (not permitted development). Structural cost modest: ~£10k–£14k. We assess your specific roof pitch and dormer feasibility at survey."),
            ("What permitted development rights do 1930s semis have?", "Standard rights: single-storey rear extensions (4m, no party wall touch), side-return infill (if side access exists), roof dormers (40% roof depth max in some areas), and some roof work. Party Wall notices required for most structural work. We confirm exactly what's permitted for your semi."),
            ("Can I extend sideways on a 1930s semi?", "If you have side access, yes — side-return infill extensions are common on 1930s semis. They must not exceed the depth of the main house (typically 8–10m) and must respect neighbour amenity (light, privacy). Rear extensions are also very common and easier to approve."),
            ("What's the typical cost of a rear extension on a 1930s semi?", "Drawing fees: £840–£1,750+. Build cost: £45k–£80k for single-storey, £70k–£130k for double-storey. Planning timeline: 8–13 weeks. Building works: 12–16 weeks. Total: 5–7 months from sketch to completion. We provide fixed-fee drawings; you manage the builder separately."),
            ("Do 1930s semis suffer from subsidence or structural issues?", "Some 1930s semis (especially London clay areas) may have minor subsidence history. We don't diagnose subsidence — that's a surveyor's job. Our structural designs account for foundation depth and ground conditions. Building Control inspector verifies foundation adequacy during construction."),
        ]
    },
    "guides/properties/modern-flat/index.html": {
        "title": "Modern Flat FAQs",
        "faqs": [
            ("What changes require planning permission in a modern flat?", "Most internal alterations do NOT require planning (unless you're removing a load-bearing wall — building regulations, not planning). External changes always do: new windows, balcony extensions, or facade alterations. Leasehold restrictions often exceed planning rules."),
            ("Do I need freeholder/landlord permission to alter my flat?", "Yes — almost always. Leasehold flats require landlord or freeholder consent for structural alterations, new windows, external changes, and sometimes new kitchens/bathrooms. Cost: £200–£500. Without consent, the freeholder can take action. Always get written permission before work starts."),
            ("What's the difference between ground rent and service charge?", "Ground rent: annual fee to freeholder (ranges £10–£500+/year). Service charge: cost of maintaining shared areas (communal corridors, lift, roof, insurance) — ranges £1,500–£4,000+/year per flat. Our extension/alteration doesn't affect ground rent but may affect service charge if structural or involving building envelope."),
            ("Can modern flats have extensions like houses?", "Very limited — most flats cannot extend (balcony space is shared/limited). Ground-floor flats may have small garden extensions if freeholder consents. Loft/roof conversion possible only if you own the entire roof. We assess your flat's specific situation; most cannot extend internally beyond cosmetic renovations."),
            ("What building regulations apply to flat alterations?", "All structural work, new windows, wall removal, extensions, and mechanical/electrical work require Building Regulations approval. Modern flats in blocks trigger additional rules: fire safety, acoustic insulation (party walls), and ventilation. Building Control inspection is mandatory. We include all compliance in our packages."),
        ]
    },
}

def add_faqs_to_guide(filepath, guide_path):
    """Add FAQ section and schema to a guides page."""
    content = filepath.read_text(encoding="utf-8")

    if guide_path not in GUIDES_FAQ:
        print(f"[SKIP] {guide_path} — no FAQ data defined")
        return 0

    guide_data = GUIDES_FAQ[guide_path]
    faqs = guide_data["faqs"]
    title = guide_data["title"]

    # Check if FAQPage schema already exists
    if "application/ld+json" in content and "FAQPage" in content:
        print(f"[SKIP] {guide_path} — FAQ schema already present")
        return 0

    # Build FAQPage schema
    faq_items = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        }
        for q, a in faqs
    ]

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items
    }

    schema_json = json.dumps(faq_schema, indent=2)
    schema_tag = f'<script type="application/ld+json">\n{schema_json}\n</script>'

    # Add schema to head (before closing </head>)
    content = content.replace("</head>", f"{schema_tag}\n</head>", 1)

    # Build FAQ section HTML
    faq_html = f'<section id="faq" class="faq"><div class="container"><h2>Frequently Asked Questions</h2>\n'
    for q, a in faqs:
        faq_html += f'<details><summary>{q}</summary><p>{a}</p></details>\n'
    faq_html += '</div></section>\n'

    # Insert before <section class="cta-band (with optional additional classes like 'reveal')
    cta_pattern = r'<section class="cta-band[^"]*"'
    if re.search(cta_pattern, content):
        # Replace the first cta-band opening with FAQ + cta-band
        match = re.search(cta_pattern, content)
        if match:
            original_section_tag = match.group()
            content = content.replace(original_section_tag, faq_html + original_section_tag, 1)
    else:
        print(f"[WARN] {guide_path} — could not find CTA band to insert FAQ before")
        return 0

    filepath.write_text(content, encoding="utf-8")
    return 1

# Process all 8 guides
guide_files = [
    "guides/extensions/index.html",
    "guides/lofts/index.html",
    "guides/planning/index.html",
    "guides/properties/victorian-terrace/index.html",
    "guides/properties/edwardian-semi/index.html",
    "guides/properties/georgian-townhouse/index.html",
    "guides/properties/1930s-semi/index.html",
    "guides/properties/modern-flat/index.html",
]

total_updated = 0
for guide_path in guide_files:
    filepath = SCRIPT_DIR / guide_path
    if filepath.exists():
        updated = add_faqs_to_guide(filepath, guide_path)
        if updated:
            print(f"[OK] {guide_path} — added FAQ section + schema")
            total_updated += 1
    else:
        print(f"[SKIP] {guide_path} — file not found")

print(f"\n[OK] Processed {len(guide_files)} guide pages — updated {total_updated}")
