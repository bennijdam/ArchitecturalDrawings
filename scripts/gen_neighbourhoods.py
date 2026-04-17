#!/usr/bin/env python3
"""
gen_neighbourhoods.py
Generate neighbourhood-level landing pages under areas/neighbourhoods/.

Usage:
    cd architectural-drawings
    python scripts/gen_neighbourhoods.py

Generates 104 neighbourhood pages (34 original + 30 batch 2 + 40 batch 3).
Existing HTML files in the output directory are skipped by default so already-
generated pages are preserved. Delete a file to force it to regenerate.
Each page matches the structure of areas/neighbourhoods/hampstead.html exactly.
"""

import os, json, html, pathlib, textwrap

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "areas" / "neighbourhoods"
CSS_FILE = BASE_DIR / "assets" / "css" / "style.css"

# ---------------------------------------------------------------------------
# Read external CSS for inlining
# ---------------------------------------------------------------------------
CSS_SOURCE = CSS_FILE.read_text(encoding="utf-8")
# Strip the @import line (fonts are loaded via <link> tags instead)
CSS_INLINE = "\n".join(
    line for line in CSS_SOURCE.splitlines()
    if not line.strip().startswith("@import")
)

# ---------------------------------------------------------------------------
# Service definitions (for service card links)
# ---------------------------------------------------------------------------
SERVICES = {
    "planning-drawings": {
        "name": "Planning Drawings",
        "price": "£840",
    },
    "building-regulations": {
        "name": "Building Regulations",
        "price": "£840",
    },
    "loft-conversions": {
        "name": "Loft Conversions",
        "price": "£1,225",
    },
    "house-extensions": {
        "name": "House Extensions",
        "price": "£1,225",
    },
    "mansard-roof": {
        "name": "Mansard Roof Extensions",
        "price": "£1,575",
    },
}

# Service descriptions per neighbourhood service type
SERVICE_DESCRIPTIONS = {
    "planning-drawings": "Full planning applications — heritage-sensitive drawings, Design & Access Statements, council officer liaison.",
    "building-regulations": "Construction-ready drawing packages compliant with all Approved Documents, submitted to local Building Control.",
    "loft-conversions": "Dormers, mansards, and Velux conversions designed for local roof profiles and planning constraints.",
    "house-extensions": "Rear extensions, side returns, wraparounds, and basement feasibility for local housing stock.",
    "mansard-roof": "Mansard roof extensions adding a full storey — planning strategy, structural design, and full submissions.",
}

# ---------------------------------------------------------------------------
# 104 neighbourhoods (34 original + 30 batch 2 + 40 batch 3)
# ---------------------------------------------------------------------------
NEIGHBOURHOODS = [
    {
        "name": "Shoreditch",
        "slug": "shoreditch",
        "borough": "Hackney",
        "borough_slug": "hackney",
        "postcodes": "E1, E2",
        "character": "Shoreditch is London's creative and tech hub, where Victorian warehouses and Georgian terraces sit alongside new-build mixed-use developments. The area's industrial heritage means many projects involve warehouse-to-residential conversions.",
        "housing_stock": "Victorian warehouses, Georgian terraces, converted industrial buildings, new-build apartments",
        "conservation_notes": "South Shoreditch Conservation Area covers much of the historic core",
        "planning_notes": "Hackney Council is receptive to contemporary design in Shoreditch but requires heritage sensitivity within conservation areas. Warehouse conversions often need change-of-use applications alongside building regulations approval.",
        "nearby": ["bethnal-green", "hackney-wick", "dalston", "angel-islington"],
        "popular_services": ["planning-drawings", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, warehouse conversions, loft extensions, and heritage-sensitive design for Shoreditch's mix of Victorian industrial architecture and contemporary living. MCIAT chartered, fixed fees, conservation area expertise built in.",
        "local_context_title": "Why Shoreditch demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Shoreditch sits at the western edge of Hackney, straddling the E1 and E2 postcodes and bordering the City of London. The area's transformation from industrial heartland to creative quarter has produced one of London's most architecturally diverse neighbourhoods, where every project demands drawings that navigate a complex planning landscape.",
            "<strong>South Shoreditch Conservation Area:</strong> The conservation area protects the area's Georgian and Victorian industrial character, including the distinctive warehouse buildings along Curtain Road, Rivington Street, and Shoreditch High Street. Article 4 Directions restrict external alterations, and Hackney Council requires Heritage Statements for most visible changes. Our MCIAT-chartered team understands these constraints and prepares applications that respect the industrial aesthetic while delivering modern living spaces.",
            "<strong>Warehouse conversions:</strong> Many Shoreditch projects involve converting former commercial or industrial buildings to residential use. These schemes require change-of-use planning applications (typically Class E to C3), building regulations compliance including fire safety and acoustic separation, and often structural engineering input for new floor openings and mezzanines. We handle the full package from feasibility through to building control sign-off.",
            "<strong>Loft conversions and roof extensions:</strong> The large-footprint Victorian warehouses and terraces in Shoreditch often have generous roof voids suitable for conversion. Within the conservation area, dormer design must be sympathetic to the existing industrial roofscape — traditional butterfly roofs, saw-tooth profiles, and parapet walls all influence what is achievable. We survey existing roof structures and advise on the most feasible conversion approach before committing to a planning strategy.",
            "<strong>New-build context:</strong> Shoreditch has seen extensive new development, particularly around Shoreditch High Street Overground station and the Tech City corridor. Where new-build schemes adjoin heritage assets, Hackney Council expects detailed contextual analysis demonstrating how the proposed design responds to its neighbours. Our drawings include accurate streetscape elevations and material specifications that satisfy both planning officers and design review panels.",
        ],
        "stats": [
            ("Conservation areas", "South Shoreditch CA"),
            ("Listed buildings", "Multiple (warehouses)"),
            ("Planning authority", "Hackney Council"),
            ("Key postcodes", "E1, E2"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a warehouse conversion in Shoreditch?",
                "Usually yes. Converting a commercial or industrial building to residential use requires a change-of-use planning application. Even where permitted development rights apply under Class MA, you still need prior approval from Hackney Council covering transport, contamination, flooding, and design. Within the South Shoreditch Conservation Area, full planning permission is almost always required. Our team handles the complete application process.",
            ),
            (
                "Can I build a loft conversion in Shoreditch?",
                "Loft conversions are popular and generally achievable in Shoreditch. For Victorian terraces outside the conservation area, rear dormers under permitted development are straightforward. Within the conservation area, dormer design must respect the existing roofscape and may require full planning permission. For warehouse buildings, roof extensions depend on structural capacity and planning constraints. We assess feasibility early in the process.",
            ),
            (
                "What are the planning restrictions in South Shoreditch Conservation Area?",
                "The South Shoreditch Conservation Area protects the area's Georgian and Victorian industrial character. Article 4 Directions remove permitted development rights for many external alterations, meaning changes to facades, windows, and roofs typically require planning permission. Heritage Statements are required for most applications. Our drawings are prepared to conservation-area standards with detailed material specifications.",
            ),
            (
                "How long does planning permission take in Hackney?",
                "Hackney Council targets 8 weeks for householder applications and 13 weeks for more complex schemes. In practice, applications in Shoreditch can take longer due to the volume of development and conservation area consultations. Pre-application advice is available and recommended for complex projects. We manage the timeline and handle any requests for additional information from the council.",
            ),
            (
                "What building regulations apply to Shoreditch conversions?",
                "Warehouse and loft conversions must comply with all relevant Approved Documents, with particular attention to Part B (fire safety), Part E (sound insulation), Part L (energy efficiency), and Part M (access). For warehouse conversions, structural assessments under Part A are critical. We prepare fully compliant building regulations drawings and coordinate with structural engineers.",
            ),
        ],
    },
    {
        "name": "Dalston",
        "slug": "dalston",
        "borough": "Hackney",
        "borough_slug": "hackney",
        "postcodes": "E8",
        "character": "Dalston is a rapidly gentrifying neighbourhood in central Hackney, known for its vibrant cultural scene and dense streets of Victorian terraces. Loft conversions and rear extensions are in constant demand.",
        "housing_stock": "Victorian terraces, Edwardian houses, post-war estates, converted shops",
        "conservation_notes": "Dalston Lane (West) Conservation Area; De Beauvoir Conservation Area nearby",
        "planning_notes": "Hackney Council encourages sensitive densification. Many properties have already been converted to flats, and further subdivision requires planning permission. Loft conversions under PD are common where Article 4 does not apply.",
        "nearby": ["stoke-newington", "hackney-wick", "shoreditch", "finsbury-park"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Dalston's Victorian terraces and period properties. MCIAT chartered, fixed fees, local planning expertise built in.",
        "local_context_title": "Why Dalston demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Dalston occupies a central position in the London Borough of Hackney, centred on the E8 postcode. The neighbourhood's Victorian terraced streets — many originally built for Hackney's artisan workers — are now among the most sought-after in east London, driving consistent demand for loft conversions, rear extensions, and internal reconfigurations.",
            "<strong>Victorian terraces and loft potential:</strong> Dalston's two- and three-storey Victorian terraces typically have good roof voids suitable for dormer loft conversions. Outside conservation areas, rear dormers can often be built under permitted development, adding a full bedroom and bathroom without planning permission. Our team surveys the existing roof structure, confirms PD eligibility, and prepares the building regulations drawings needed for Building Control sign-off.",
            "<strong>Rear and side-return extensions:</strong> Many Dalston terraces have narrow side returns and compact rear gardens, making single-storey rear extensions and side-return infills popular ways to create open-plan kitchen-dining spaces. Under permitted development, rear extensions up to 6 metres (detached) or 4 metres (semi/terrace) from the original rear wall are achievable without planning permission, subject to prior notification. We prepare the drawings and manage the notification process.",
            "<strong>Conservation areas:</strong> The Dalston Lane (West) Conservation Area and the nearby De Beauvoir Conservation Area impose additional constraints. Within these zones, Article 4 Directions may remove permitted development rights, requiring full planning permission for dormer conversions, replacement windows, and some rear extensions. Our MCIAT-chartered team prepares conservation-sensitive applications that satisfy Hackney's heritage officers.",
            "<strong>Flat conversions:</strong> Many Dalston properties have been subdivided into flats over the decades. Further subdivision or the addition of a self-contained unit (e.g., a basement flat) requires planning permission and must comply with Hackney's housing standards. We advise on feasibility and prepare the necessary applications.",
        ],
        "stats": [
            ("Conservation areas", "Dalston Lane (West) CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Hackney Council"),
            ("Key postcodes", "E8"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Dalston without planning permission?",
                "In many cases, yes. Victorian terraces outside conservation areas can add rear dormers under permitted development (Class B). The dormer must not exceed 50 cubic metres, must not be higher than the existing ridge, and must use materials matching the existing roof. Within the Dalston Lane Conservation Area, Article 4 Directions may require full planning permission. We confirm your PD eligibility and prepare the required drawings.",
            ),
            (
                "How much does a rear extension cost in Dalston?",
                "Our architectural drawings for a rear extension in Dalston start from £840 for the Essentials package (planning or building regs submission). The Complete package from £1,750 includes both planning and building regulations drawings plus structural calculations. Construction costs vary but typically range from £1,800 to £2,800 per square metre depending on specification.",
            ),
            (
                "What planning constraints apply in De Beauvoir Conservation Area?",
                "De Beauvoir is one of Hackney's most tightly controlled conservation areas. Article 4 Directions remove most permitted development rights, meaning planning permission is required for dormer conversions, replacement windows and doors, front boundary changes, and even some rear extensions. A Heritage Statement must accompany each application. Our team is experienced in preparing successful applications in De Beauvoir.",
            ),
            (
                "Can I convert my Dalston house into flats?",
                "Converting a house into flats requires planning permission from Hackney Council, plus Building Regulations approval. The council will assess the impact on neighbouring properties, parking, waste storage, and whether each unit meets minimum space standards. We prepare the full drawing set including floor plans, sections, and design statements required for the application.",
            ),
            (
                "How long does Hackney Council take to decide planning applications?",
                "Hackney targets 8 weeks for householder applications and 13 weeks for major applications. Pre-application advice typically takes 4-6 weeks and is recommended for complex projects or sites within conservation areas. We manage the application timeline and respond to any requests for additional information.",
            ),
        ],
    },
    {
        "name": "Camden Town",
        "slug": "camden-town",
        "borough": "Camden",
        "borough_slug": "camden",
        "postcodes": "NW1",
        "character": "Camden Town is a vibrant mixed-use neighbourhood combining Victorian terraces, mansion blocks, and canal-side warehouses with one of London's busiest markets. Residential projects must navigate multiple conservation areas.",
        "housing_stock": "Victorian terraces, mansion blocks, canal-side warehouses, Georgian townhouses",
        "conservation_notes": "Camden Town Conservation Area; Camden Square Conservation Area",
        "planning_notes": "Camden Council applies strict heritage controls within the multiple conservation areas around Camden Town. Market-facing properties face additional commercial use constraints. Canal-side developments may require Environment Agency consultation.",
        "nearby": ["kentish-town", "belsize-park", "hampstead", "angel-islington"],
        "popular_services": ["planning-drawings", "loft-conversions", "house-extensions"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and heritage-sensitive design for Camden Town's diverse mix of Victorian terraces, mansion blocks, and canal-side properties. MCIAT chartered, fixed fees, conservation area expertise built in.",
        "local_context_title": "Why Camden Town demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Camden Town sits at the heart of the London Borough of Camden, centred on the NW1 postcode. The neighbourhood spans from the Regent's Canal in the south to Chalk Farm in the north, encompassing some of London's most architecturally varied residential streets alongside the famous Camden Market complex.",
            "<strong>Camden Town Conservation Area:</strong> The conservation area covers the historic streets around Camden High Street and the canal, protecting a mix of early Victorian terraces, Georgian townhouses, and industrial heritage buildings. Article 4 Directions restrict permitted development rights for external alterations, and Camden Council requires Heritage Statements for most visible changes. Our MCIAT-chartered team prepares applications that meet the council's exacting heritage standards.",
            "<strong>Victorian terraces:</strong> Camden Town's residential streets are dominated by two- and three-storey Victorian terraces, many with rear additions and outriggers. These properties are prime candidates for loft conversions, rear extensions, and internal reconfigurations. The challenge is designing interventions that respect the existing streetscape while maximising interior space — side-return extensions and rear dormers are the most common project types we handle in NW1.",
            "<strong>Mansion blocks:</strong> Camden contains several significant mansion block developments where flat owners seek to reconfigure interiors, replace windows, or add balconies. These projects require freeholder consent alongside any planning permission, and the drawings must demonstrate compliance with the building's overall design language.",
            "<strong>Canal-side properties:</strong> Properties adjacent to the Regent's Canal may require Environment Agency consultation for any works affecting flood risk or waterway access. We include flood risk assessments where needed and coordinate with the relevant authorities.",
        ],
        "stats": [
            ("Conservation areas", "Camden Town CA"),
            ("Housing type", "Victorian terraces, mansion blocks"),
            ("Planning authority", "Camden Council"),
            ("Key postcodes", "NW1"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a loft conversion in Camden Town?",
                "It depends on your location. Outside conservation areas, rear dormers can often be built under permitted development. Within the Camden Town Conservation Area, Article 4 Directions typically require full planning permission for any roof alteration. Camden Council expects dormer designs that are subordinate to the existing roof and use matching materials. We confirm your property's status and advise on the best route.",
            ),
            (
                "What basement restrictions apply in Camden?",
                "Camden's basement development policy (Policy A5) restricts basements to single-storey only, with the excavation footprint limited to 50% of the garden area. Structural method statements, construction management plans, and often arboricultural assessments are required. We advise on feasibility and prepare compliant applications.",
            ),
            (
                "Can I extend a mansion block flat in Camden Town?",
                "Internal alterations to mansion block flats generally don't need planning permission but do require Building Regulations approval. External changes — replacement windows, balconies, facade alterations — usually need both planning permission and freeholder consent. Within conservation areas, even like-for-like window replacements may require planning permission. We handle the full application process.",
            ),
            (
                "How does Camden Council handle heritage applications?",
                "Camden has a dedicated conservation team that reviews all applications within conservation areas. They expect detailed Heritage Statements explaining how proposed works relate to the significance of the heritage asset. For listed buildings, Listed Building Consent is required in addition to planning permission. Our drawings include the level of architectural detail that Camden's conservation officers expect.",
            ),
            (
                "What are typical planning timescales in Camden?",
                "Camden Council targets 8 weeks for householder applications. Conservation area applications may take longer due to the 21-day public notification period and heritage officer review. Pre-application meetings are available and strongly recommended for complex schemes. We manage the full timeline and handle all council correspondence.",
            ),
        ],
    },
    {
        "name": "Kentish Town",
        "slug": "kentish-town",
        "borough": "Camden",
        "borough_slug": "camden",
        "postcodes": "NW5",
        "character": "Kentish Town is a popular family neighbourhood in Camden with long streets of well-proportioned Victorian terraces. Loft conversions and rear extensions are the most common project types.",
        "housing_stock": "Victorian terraces, Edwardian houses, some 1960s infill",
        "conservation_notes": "Parts fall within Kentish Town Conservation Area and Bartholomew Estate Conservation Area",
        "planning_notes": "Camden Council's policies favour sympathetic additions to Victorian properties. Basements restricted to single-storey under Policy A5. Many streets have consistent rooflines that influence dormer design.",
        "nearby": ["camden-town", "hampstead", "highgate", "holloway"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Kentish Town's Victorian terraces. MCIAT chartered, fixed fees, Camden planning expertise built in.",
        "local_context_title": "Why Kentish Town demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Kentish Town occupies a central position in the London Borough of Camden, centred on the NW5 postcode. Its long streets of two- and three-storey Victorian terraces — many with original period features intact — make it one of north London's most popular family neighbourhoods and a consistently busy area for residential architectural work.",
            "<strong>Victorian terrace conversions:</strong> The typical Kentish Town terrace has a rear outrigger, a compact side return, and a roof void with good headroom. This makes them ideal candidates for the three most common residential projects: rear dormers to add a loft bedroom, single-storey rear extensions to create open-plan ground floors, and side-return infills to widen narrow kitchens. We handle all three project types regularly in NW5.",
            "<strong>Conservation areas:</strong> Parts of Kentish Town fall within conservation areas, including the Kentish Town Conservation Area and the Bartholomew Estate Conservation Area. Within these zones, external alterations require planning permission and Heritage Statements. Our MCIAT-chartered team prepares applications that satisfy Camden's heritage officers while delivering the space our clients need.",
            "<strong>Camden basement policy:</strong> Camden's Policy A5 limits basements to single-storey with no more than 50% garden coverage. In Kentish Town, the relatively flat topography makes basements more straightforward than in hillier Camden neighbourhoods like Hampstead, but structural method statements and construction management plans are still required.",
            "<strong>Consistent rooflines:</strong> Many Kentish Town streets have remarkably consistent Victorian rooflines. Camden Council is protective of these streetscape views, which means dormer design must be carefully considered — rear dormers are generally acceptable but front-facing dormers are almost always refused. We advise on what is achievable before you invest in a full design.",
        ],
        "stats": [
            ("Conservation areas", "Kentish Town CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Camden Council"),
            ("Key postcodes", "NW5"),
        ],
        "faqs": [
            (
                "Can I add a loft conversion to my Kentish Town terrace?",
                "Yes, loft conversions are very common in Kentish Town. Outside conservation areas, rear dormers can usually be built under permitted development. Within the Kentish Town Conservation Area, planning permission is required but rear dormers are generally supported if they use matching materials and do not break the ridgeline. We survey your roof and confirm the best approach.",
            ),
            (
                "What size rear extension can I build in NW5?",
                "Under permitted development, you can build a single-storey rear extension up to 4 metres deep (for terraced houses) without planning permission, subject to prior notification. Larger extensions up to 6 metres may be possible under the larger homes scheme. Within conservation areas, planning permission is typically required for any extension. Our team advises on what is permissible for your specific property.",
            ),
            (
                "Are basements allowed in Kentish Town?",
                "Yes, subject to Camden's Policy A5. Basements must be single-storey and cover no more than 50% of the garden. A structural method statement and construction management plan are required with the application. The relatively flat topography in Kentish Town makes single-storey basements generally feasible, but each site needs individual assessment.",
            ),
            (
                "How much do architectural drawings cost in Kentish Town?",
                "Our Essentials package starts from £840 for a single submission (planning or building regulations). The Complete package from £1,750 covers both planning and building regulations drawings plus structural calculations. Bespoke packages for listed buildings or complex conservation area projects are priced individually.",
            ),
            (
                "Do I need party wall agreements for my extension?",
                "If your extension involves work on or near a shared boundary wall, you will likely need Party Wall Agreements under the Party Wall Act 1996. This is separate from planning permission and building regulations. We can advise on whether party wall matters are likely to arise and recommend specialist party wall surveyors.",
            ),
        ],
    },
    {
        "name": "Belsize Park",
        "slug": "belsize-park",
        "borough": "Camden",
        "borough_slug": "camden",
        "postcodes": "NW3",
        "character": "Belsize Park is a leafy, affluent neighbourhood in Camden known for its large Victorian and Edwardian houses, mansion blocks, and tree-lined avenues. Many properties are listed or within conservation areas.",
        "housing_stock": "Large Victorian/Edwardian detached and semi-detached houses, mansion blocks, converted flats",
        "conservation_notes": "Belsize Conservation Area covers most of the neighbourhood",
        "planning_notes": "Camden Council applies strict conservation controls. Most external works require planning permission due to Article 4 Directions. Large houses mean basement extensions are popular but restricted by Policy A5.",
        "nearby": ["hampstead", "camden-town", "kentish-town", "highgate"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, basement feasibility, extensions, and heritage-sensitive design for Belsize Park's large Victorian and Edwardian houses. MCIAT chartered, fixed fees, conservation area expertise built in.",
        "local_context_title": "Why Belsize Park demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Belsize Park sits between Hampstead and Camden Town in the NW3 postcode, occupying some of the finest residential streets in north London. The neighbourhood's grand Victorian and Edwardian houses, many now divided into flats, combine with substantial mansion block developments to create a distinctive architectural character that Camden Council is determined to protect.",
            "<strong>Belsize Conservation Area:</strong> The Belsize Conservation Area covers the majority of the neighbourhood and imposes strict controls on external alterations. Article 4 Directions remove most permitted development rights, meaning planning permission is required for roof alterations, replacement windows, and many rear extensions. Heritage Statements must accompany all applications. Our MCIAT-chartered team specialises in conservation-sensitive design that satisfies Camden's heritage officers.",
            "<strong>Large houses and basement demand:</strong> Belsize Park's substantial Victorian and Edwardian houses are among the most expensive residential properties in Camden. Homeowners frequently seek to maximise space through basement extensions. Camden's Policy A5 restricts basements to single-storey with no more than 50% garden coverage, and the area's mature trees add arboricultural constraints. We advise on feasibility and prepare compliant structural method statements.",
            "<strong>Mansion blocks:</strong> The area contains several notable mansion block developments, including those along Belsize Park Gardens and Belsize Avenue. Works to individual flats — window replacements, balcony additions, or internal reconfiguration — require careful coordination between planning permission, Building Regulations, and freeholder consent. We handle the architectural drawings for all three processes.",
            "<strong>Listed buildings:</strong> Several Belsize Park properties are individually listed, requiring Listed Building Consent for internal and external alterations. The level of architectural detail in the drawings must be significantly higher than standard householder applications. We produce detailed section drawings, joinery profiles, and material specifications.",
        ],
        "stats": [
            ("Conservation areas", "Belsize CA"),
            ("Listed buildings", "Numerous"),
            ("Planning authority", "Camden Council"),
            ("Key postcodes", "NW3"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Belsize Park?",
                "Almost certainly yes for external works. The Belsize Conservation Area and its Article 4 Directions remove most permitted development rights. Even replacement windows, roof changes, and some rear extensions require full planning permission with a Heritage Statement. Our MCIAT-chartered team prepares conservation-sensitive drawings that satisfy Camden Council's heritage officers.",
            ),
            (
                "Can I build a basement extension in Belsize Park?",
                "Subject to Camden's Policy A5, single-storey basements covering no more than 50% of the garden are permissible. Structural method statements, construction management plans, and arboricultural assessments are typically required. The area's mature tree canopy and proximity to neighbours add complexity. We advise on feasibility before you commit to a scheme.",
            ),
            (
                "How do I get permission for works on a mansion block flat?",
                "You'll typically need three consents: planning permission from Camden Council (especially within the conservation area), Building Regulations approval for structural or services changes, and freeholder consent under the terms of your lease. We prepare the architectural drawings needed for all three and coordinate the application process.",
            ),
            (
                "What is the process for Listed Building Consent in Belsize Park?",
                "Listed Building Consent is a separate application from planning permission. It requires detailed drawings showing existing and proposed conditions, a Heritage Impact Assessment, and often a schedule of materials. Camden's conservation officer will assess the impact on the building's significance. We prepare applications to the standard expected for listed buildings.",
            ),
            (
                "How long do planning decisions take in Belsize Park?",
                "Camden Council targets 8 weeks for householder applications but conservation area applications routinely take longer. The 21-day public notification period, heritage officer review, and amenity society consultations all add time. We recommend pre-application advice for complex schemes and manage the full timeline on your behalf.",
            ),
        ],
    },
    {
        "name": "Finsbury Park",
        "slug": "finsbury-park",
        "borough": "Haringey",
        "borough_slug": "haringey",
        "postcodes": "N4",
        "character": "Finsbury Park straddles the Haringey-Islington border and is popular with families drawn to its excellent transport links and streets of Victorian terraces. Loft conversions and rear extensions are the most common projects.",
        "housing_stock": "Victorian terraces, Edwardian houses, some post-war council estates",
        "conservation_notes": "Stroud Green Conservation Area covers parts of the neighbourhood",
        "planning_notes": "Properties on the Haringey side fall under Haringey Council; those on the Islington side under Islington Council. Planning approaches differ between the two boroughs. Confirming which authority has jurisdiction is the essential first step.",
        "nearby": ["crouch-end", "holloway", "stoke-newington", "tottenham"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Finsbury Park's Victorian terraces. MCIAT chartered, fixed fees, dual-borough expertise for both Haringey and Islington properties.",
        "local_context_title": "Why Finsbury Park demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Finsbury Park straddles the boundary between the London boroughs of Haringey and Islington, centred on the N4 postcode. The neighbourhood's well-proportioned Victorian terraces, excellent transport connections, and proximity to the park itself have made it one of north London's most popular family areas — and one of its busiest for residential planning applications.",
            "<strong>Dual-borough complexity:</strong> The most important first step for any Finsbury Park project is confirming which planning authority has jurisdiction. Properties west of the park generally fall under Haringey Council; those to the south and east under Islington Council. The two boroughs have different policies on dormer design, extension depths, and conservation area controls. Our team identifies the relevant authority and tailors the application accordingly.",
            "<strong>Victorian terraces and loft conversions:</strong> Finsbury Park's Victorian terraces — typically two or three storeys with slate roofs and rear outriggers — are ideal candidates for dormer loft conversions. Under permitted development, rear dormers can often be built without planning permission, adding a bedroom and en-suite bathroom. We survey the existing roof structure, confirm PD eligibility, and prepare building regulations drawings for Building Control approval.",
            "<strong>Stroud Green Conservation Area:</strong> The Stroud Green Conservation Area covers streets to the north and west of the park, including some of the area's finest Victorian housing. Within this zone, Haringey Council requires planning permission for most external alterations. Our MCIAT-chartered team prepares heritage-sensitive applications that meet the council's conservation standards.",
            "<strong>Rear extensions and open-plan living:</strong> Single-storey rear extensions to create open-plan kitchen-dining rooms are the second most common project type in Finsbury Park. Under permitted development, terraced houses can extend up to 4 metres from the original rear wall. Side-return infills are also popular on the wider Edwardian-era terraces.",
        ],
        "stats": [
            ("Conservation areas", "Stroud Green CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Haringey / Islington"),
            ("Key postcodes", "N4"),
        ],
        "faqs": [
            (
                "Which council handles planning in Finsbury Park?",
                "It depends on which side of the borough boundary your property falls. Properties to the west generally come under Haringey Council; those south and east under Islington Council. The two boroughs have different planning policies and application processes. We confirm your authority at the outset and tailor the application accordingly.",
            ),
            (
                "Can I build a loft conversion in Finsbury Park?",
                "Yes, loft conversions are very common in N4. Outside conservation areas, rear dormers can typically be built under permitted development. Within the Stroud Green Conservation Area, planning permission is usually required. We survey your roof, confirm PD eligibility, and advise on the most cost-effective approach.",
            ),
            (
                "What size extension can I build without planning permission?",
                "Under permitted development, terraced houses in Finsbury Park can build single-storey rear extensions up to 4 metres deep (or up to 6 metres under the larger homes scheme with prior notification). Semi-detached and detached houses have greater allowances. Within conservation areas, planning permission is usually required. We confirm what applies to your property.",
            ),
            (
                "How much do architectural drawings cost in Finsbury Park?",
                "Our Essentials package starts from £840 for a single planning or building regulations submission. The Complete package from £1,750 includes both planning and building regulations drawings plus structural calculations. We offer fixed fees with no hidden extras.",
            ),
            (
                "Is pre-application advice available in Haringey?",
                "Yes, both Haringey and Islington councils offer pre-application advice services. In Haringey, the householder pre-application service provides a written response within 4-6 weeks. We recommend pre-application advice for conservation area projects and complex extensions. Our team can submit the pre-app enquiry on your behalf.",
            ),
        ],
    },
    {
        "name": "Holloway",
        "slug": "holloway",
        "borough": "Islington",
        "borough_slug": "islington",
        "postcodes": "N7",
        "character": "Holloway is a densely built neighbourhood in Islington with streets of Victorian terraces increasingly popular with families. Many properties are HMOs or subdivided flats seeking reconfiguration.",
        "housing_stock": "Victorian terraces, Edwardian houses, post-war estates, converted HMOs",
        "conservation_notes": "Mercers Road / Tavistock Terrace Conservation Area; Hillmarton Conservation Area",
        "planning_notes": "Islington Council has strict policies on housing mix and resists further subdivision of family houses. HMO-to-single-dwelling conversions are generally supported. The borough has some of London's tightest design standards for extensions.",
        "nearby": ["angel-islington", "finsbury-park", "kentish-town", "camden-town"],
        "popular_services": ["loft-conversions", "planning-drawings", "house-extensions"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and HMO reconfiguration for Holloway's Victorian terraces. MCIAT chartered, fixed fees, Islington planning expertise built in.",
        "local_context_title": "Why Holloway demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Holloway occupies the N7 postcode in the London Borough of Islington, stretching along the Holloway Road corridor from Highbury Corner to Archway. Its dense streets of Victorian terraces — many originally built as artisan housing — are increasingly sought after by families and professionals, driving demand for loft conversions, extensions, and internal reconfigurations.",
            "<strong>Islington's design standards:</strong> Islington Council applies some of London's most rigorous design standards for residential alterations. The borough's Urban Design Guide sets specific requirements for extension depths, window proportions, and material palettes. Dormer design is particularly scrutinised — the council expects rear dormers to be set back from the eaves, set in from party walls, and constructed in materials matching the existing roof. Our MCIAT-chartered team is fluent in Islington's design language.",
            "<strong>HMO and flat conversions:</strong> Many Holloway properties were converted to Houses in Multiple Occupation (HMOs) or bedsit flats in previous decades. Islington Council generally supports the reconversion of HMOs back to single family dwellings. New HMO creation, however, requires planning permission and must comply with the borough's housing mix policies. We prepare applications for both directions of conversion.",
            "<strong>Conservation areas:</strong> Parts of Holloway fall within conservation areas including the Mercers Road / Tavistock Terrace Conservation Area and the Hillmarton Conservation Area. Within these zones, Article 4 Directions may apply, requiring planning permission for works that would otherwise be permitted development. Heritage Statements must accompany applications for visible external changes.",
            "<strong>Terraced house extensions:</strong> Single-storey rear extensions and side-return infills are the most common project types in Holloway. Islington's design standards typically limit rear extension depths and require the retention of adequate garden space. We design extensions that maximise space within the council's policy parameters.",
        ],
        "stats": [
            ("Conservation areas", "Mercers Road CA"),
            ("Housing type", "Victorian terraces, HMOs"),
            ("Planning authority", "Islington Council"),
            ("Key postcodes", "N7"),
        ],
        "faqs": [
            (
                "Can I convert an HMO back to a family house in Holloway?",
                "Islington Council generally supports the reconversion of HMOs back to single-family dwellings, as it aligns with their housing mix policy. Depending on the extent of previous conversion, you may need planning permission and Building Regulations approval. We prepare the drawings and handle the application for both.",
            ),
            (
                "What are Islington's rules for loft conversions?",
                "Islington has specific design requirements for loft dormers: they must be set back from the eaves, set in from party walls, and use matching materials. Outside conservation areas, rear dormers under permitted development are achievable if these criteria are met. Within conservation areas, full planning permission is required. We ensure your design complies before submission.",
            ),
            (
                "How deep can I extend my terrace in Holloway?",
                "Under permitted development, terraced houses can extend up to 4 metres from the original rear wall at single storey. Islington's design policies may impose additional constraints regarding retained garden length and neighbour amenity. Within conservation areas, planning permission is typically required for any extension. We confirm the maximum depth achievable for your property.",
            ),
            (
                "Do I need a party wall agreement for my Holloway extension?",
                "If your extension involves work on or adjacent to a shared boundary wall, a Party Wall Agreement under the Party Wall Act 1996 is usually required. This is a separate legal process from planning permission. We advise on whether party wall matters are likely and can recommend specialist surveyors.",
            ),
            (
                "How long does Islington Council take to decide applications?",
                "Islington targets 8 weeks for householder planning applications. Conservation area applications and more complex schemes can take longer. Pre-application advice is available and recommended for projects within conservation areas. We manage the timeline and handle all council correspondence.",
            ),
        ],
    },
    {
        "name": "Tooting",
        "slug": "tooting",
        "borough": "Wandsworth",
        "borough_slug": "wandsworth",
        "postcodes": "SW17",
        "character": "Tooting is a popular south London neighbourhood known for its Victorian terraces, diverse high street, and excellent transport links. Loft conversions and rear extensions are in very high demand.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war semis",
        "conservation_notes": "Totterdown Fields Conservation Area covers the grid of streets between the two commons",
        "planning_notes": "Wandsworth Council is generally supportive of sympathetic residential extensions. Permitted development rights are available outside conservation areas. Within the Totterdown Fields Conservation Area, Article 4 Directions require planning permission for most external works.",
        "nearby": ["balham", "streatham", "earlsfield", "wimbledon"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Tooting's Victorian terraces. MCIAT chartered, fixed fees, Wandsworth planning expertise built in.",
        "local_context_title": "Why Tooting demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Tooting sits in the heart of the London Borough of Wandsworth, centred on the SW17 postcode between Tooting Bec Common and Tooting Graveney. The neighbourhood's well-proportioned Victorian terraces and excellent Northern line connections have made it one of south London's most desirable family areas, driving consistently high demand for loft conversions and extensions.",
            "<strong>Victorian terraces and loft potential:</strong> Tooting's two- and three-storey Victorian terraces typically have slate roofs with good headroom in the loft space, making them ideal candidates for dormer conversions. Outside the Totterdown Fields Conservation Area, rear dormers can often be built under permitted development. Our team surveys the roof structure, confirms PD eligibility, and prepares building regulations drawings for Building Control approval.",
            "<strong>Totterdown Fields Conservation Area:</strong> The Totterdown Fields Conservation Area covers the distinctive grid of streets between the two commons — an area of remarkable architectural consistency. Article 4 Directions remove most permitted development rights within this zone, meaning planning permission is required for dormer conversions, replacement windows, and front boundary changes. Our MCIAT-chartered team prepares conservation-sensitive applications that satisfy Wandsworth's heritage officers.",
            "<strong>Rear extensions:</strong> Single-storey rear extensions to create open-plan kitchen-dining-living spaces are extremely popular in Tooting. Under permitted development, terraced houses can extend up to 4 metres (or up to 6 metres with prior notification under the larger homes scheme). Side-return infills are common on the wider corner plots and end-of-terrace properties.",
            "<strong>Loft and extension combinations:</strong> Many Tooting homeowners combine a loft conversion with a rear extension in a single project to maximise space. We design integrated schemes that work structurally and architecturally, submitting coordinated planning and building regulations applications where needed.",
        ],
        "stats": [
            ("Conservation areas", "Totterdown Fields CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Wandsworth Council"),
            ("Key postcodes", "SW17"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Tooting without planning permission?",
                "In many cases, yes. Victorian terraces outside the Totterdown Fields Conservation Area can add rear dormers under permitted development (Class B). The dormer must not exceed 50 cubic metres and must use matching materials. Within the conservation area, planning permission is required. We confirm your PD eligibility and prepare the required drawings.",
            ),
            (
                "What are the rules for extensions in Totterdown Fields?",
                "Within the Totterdown Fields Conservation Area, most external works require planning permission. Wandsworth Council expects extension designs that respect the consistent Victorian character of the area — matching materials, sympathetic proportions, and retention of garden space. Heritage Statements must accompany applications. Our team prepares compliant designs.",
            ),
            (
                "How much do architectural drawings cost in Tooting?",
                "Our Essentials package starts from £840 for a single submission (planning or building regulations). The Complete package from £1,750 includes both planning and building regulations drawings plus structural calculations — this is the most popular choice for Tooting loft conversions and extensions.",
            ),
            (
                "Can I combine a loft conversion and extension?",
                "Yes, and it is often the most cost-effective approach. We design integrated schemes where the loft conversion and extension work together structurally and aesthetically. A combined project typically needs building regulations drawings and, if either element requires planning permission, a single coordinated application.",
            ),
            (
                "How long does Wandsworth Council take for planning decisions?",
                "Wandsworth targets 8 weeks for householder applications. The borough is one of London's busier planning authorities, and applications within the Totterdown Fields Conservation Area may take slightly longer. Pre-application advice is available and recommended for complex projects.",
            ),
        ],
    },
    {
        "name": "Balham",
        "slug": "balham",
        "borough": "Wandsworth",
        "borough_slug": "wandsworth",
        "postcodes": "SW12",
        "character": "Balham is a popular residential neighbourhood in Wandsworth with broad streets of large Victorian and Edwardian terraces. Its family-friendly reputation drives strong demand for loft conversions and extensions.",
        "housing_stock": "Large Victorian terraces, Edwardian houses, 1930s semis",
        "conservation_notes": "Balham Conservation Area; Nightingale Lane area",
        "planning_notes": "Wandsworth Council is generally supportive of sympathetic residential extensions outside conservation areas. Within the Balham Conservation Area, Article 4 Directions apply and Heritage Statements are required for external works.",
        "nearby": ["tooting", "clapham", "earlsfield", "streatham"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Balham's large Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Wandsworth planning expertise built in.",
        "local_context_title": "Why Balham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Balham sits in the SW12 postcode within the London Borough of Wandsworth, positioned between Clapham Common to the north and Tooting to the south. Its broad, tree-lined streets of generously proportioned Victorian and Edwardian terraces make it one of south-west London's most sought-after family neighbourhoods — and one of its busiest for residential architectural work.",
            "<strong>Large terraces with extension potential:</strong> Balham's terraces are notably wider and deeper than those in many neighbouring areas, offering significant potential for rear extensions, side-return infills, and loft conversions. Many properties have rear gardens of 15-20 metres, giving ample scope for single or even double-storey rear extensions within Wandsworth's planning policies.",
            "<strong>Balham Conservation Area:</strong> The Balham Conservation Area covers key streets around Balham High Road, protecting the Victorian commercial and residential character. Within the conservation area, Article 4 Directions require planning permission for external alterations including replacement windows, front doors, and boundary walls. Our MCIAT-chartered team prepares applications that respect the conservation area's character.",
            "<strong>Loft conversions:</strong> Balham's Victorian and Edwardian terraces typically have generous roof spaces well suited to dormer loft conversions. Outside the conservation area, rear dormers can often be built under permitted development. Within the conservation area, planning permission is required but Wandsworth Council is generally supportive of well-designed rear dormers. We survey the roof structure and advise on the best approach for each property.",
            "<strong>Period features and design sensitivity:</strong> Many Balham properties retain original Victorian and Edwardian features — bay windows, decorative brickwork, tiled paths, and ornate plasterwork. Wandsworth Council expects new extensions and alterations to complement these features. Our designs balance contemporary functionality with sensitivity to the existing period character.",
        ],
        "stats": [
            ("Conservation areas", "Balham CA"),
            ("Housing type", "Large Victorian terraces"),
            ("Planning authority", "Wandsworth Council"),
            ("Key postcodes", "SW12"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Balham?",
                "Yes, loft conversions are extremely popular in Balham. Outside the conservation area, rear dormers can typically be built under permitted development. Within the Balham Conservation Area, planning permission is required but well-designed rear dormers are generally supported. We survey your roof and confirm the best approach.",
            ),
            (
                "What size rear extension can I build in Balham?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey, and detached houses up to 8 metres (subject to prior notification). Balham's generous garden depths often allow for larger extensions under full planning permission. We design extensions that maximise space within policy parameters.",
            ),
            (
                "What restrictions apply in the Balham Conservation Area?",
                "The Balham Conservation Area requires planning permission for most external works. Article 4 Directions cover replacement windows, front doors, boundary walls, and roof alterations. Heritage Statements must accompany applications. Our MCIAT-chartered team understands what Wandsworth's heritage officers expect.",
            ),
            (
                "Can I convert my Balham house into flats?",
                "Converting a house into flats requires planning permission from Wandsworth Council. The council assesses the impact on housing mix, parking, waste, and whether units meet minimum space standards. We prepare the full drawing set and design statement needed for the application.",
            ),
            (
                "How much do loft conversion drawings cost?",
                "Our Complete package from £1,750 is the most popular choice for loft conversions, covering planning drawings (if needed), building regulations drawings, and structural calculations. The Essentials package from £840 covers a single submission — either planning or building regulations.",
            ),
        ],
    },
    {
        "name": "Bermondsey",
        "slug": "bermondsey",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE1, SE16",
        "character": "Bermondsey is a riverside neighbourhood in Southwark known for its warehouse conversions, Victorian terraces, and ongoing regeneration. Projects range from warehouse loft conversions to extensions on period terraces.",
        "housing_stock": "Victorian terraces, converted warehouses, new-build apartments, post-war estates",
        "conservation_notes": "Bermondsey Street Conservation Area; Tower Bridge Conservation Area nearby",
        "planning_notes": "Southwark Council supports high-quality design in riverside locations. Warehouse conversions may require change-of-use applications. Flood risk assessments are required for Thames-adjacent properties.",
        "nearby": ["peckham", "deptford", "dulwich", "east-dulwich"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, warehouse conversions, extensions, and building regulations for Bermondsey's diverse housing stock. MCIAT chartered, fixed fees, Southwark planning expertise built in.",
        "local_context_title": "Why Bermondsey demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Bermondsey stretches across the SE1 and SE16 postcodes in the London Borough of Southwark, from Tower Bridge to the Surrey Quays peninsula. The neighbourhood's mix of Victorian terraces, converted warehouses, and new-build developments creates a diverse architectural landscape where every project requires drawings tailored to the specific property type.",
            "<strong>Warehouse conversions:</strong> Bermondsey's industrial heritage has produced some of London's most distinctive residential spaces — converted tanneries, biscuit factories, and riverside warehouses. These projects often involve change-of-use applications, structural engineering for new openings, and building regulations compliance covering fire safety, acoustic separation, and energy efficiency. Our MCIAT-chartered team handles the full package from feasibility to completion.",
            "<strong>Bermondsey Street Conservation Area:</strong> The conservation area protects the historic character of Bermondsey Street and its surroundings, including Georgian and Victorian commercial buildings. Within this zone, external alterations require planning permission and Heritage Statements. New development must respond sensitively to the existing streetscape.",
            "<strong>Flood risk:</strong> Properties close to the Thames must address flood risk in their planning applications. Southwark Council requires Flood Risk Assessments for developments in Flood Zones 2 and 3, and the Environment Agency is a statutory consultee. Our drawings include the necessary flood risk information and mitigation measures.",
            "<strong>Victorian terraces:</strong> Away from the riverside, Bermondsey's residential streets contain well-proportioned Victorian terraces suitable for loft conversions and rear extensions. Southwark Council is generally supportive of sympathetic residential extensions outside conservation areas, and permitted development rights are available for many standard projects.",
        ],
        "stats": [
            ("Conservation areas", "Bermondsey Street CA"),
            ("Flood zone", "Parts in Flood Zone 2/3"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE1, SE16"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a warehouse conversion in Bermondsey?",
                "Usually yes. Converting commercial or industrial space to residential use typically requires a change-of-use planning application. Permitted development rights under Class MA may apply in some cases, but Southwark Council still requires prior approval covering several assessment criteria. Within the Bermondsey Street Conservation Area, full planning permission is required.",
            ),
            (
                "Is a flood risk assessment required for my Bermondsey project?",
                "If your property is in Flood Zone 2 or 3 (most of the riverside area), a Flood Risk Assessment is required with your planning application. The Environment Agency will be consulted and may impose conditions on finished floor levels and flood-resilient construction. We incorporate flood risk requirements into the application from the outset.",
            ),
            (
                "Can I build a loft conversion on a Bermondsey terrace?",
                "Yes, loft conversions are common on Bermondsey's Victorian terraces. Outside conservation areas, rear dormers under permitted development are straightforward. Within the conservation area, planning permission is required. We survey your roof structure and advise on the most feasible conversion type.",
            ),
            (
                "What building regulations apply to warehouse conversions?",
                "Warehouse conversions must comply with all Approved Documents, with particular focus on Part B (fire safety — especially means of escape from upper floors), Part E (sound insulation between units), Part L (energy efficiency), and Part A (structural adequacy of existing elements). We prepare fully compliant building regulations drawings.",
            ),
            (
                "How much do architectural drawings cost in Bermondsey?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers both planning and building regulations plus structural calculations. Warehouse conversion projects are typically quoted on a bespoke basis reflecting their complexity.",
            ),
        ],
    },
    {
        "name": "Streatham",
        "slug": "streatham",
        "borough": "Lambeth",
        "borough_slug": "lambeth",
        "postcodes": "SW16",
        "character": "Streatham is a long, linear south London neighbourhood along the A23, known for its Victorian and Edwardian terraces. It offers some of the best value period housing in inner London, driving high demand for extensions and loft conversions.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, some 1960s blocks",
        "conservation_notes": "Streatham Lodge Conservation Area; Streatham Common Conservation Area",
        "planning_notes": "Lambeth Council is generally supportive of residential extensions that respect existing character. Permitted development rights are available outside conservation areas. The borough has specific guidance on dormer design.",
        "nearby": ["herne-hill", "brixton", "balham", "dulwich"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Streatham's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Lambeth planning expertise built in.",
        "local_context_title": "Why Streatham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Streatham stretches along the A23 in the SW16 postcode within the London Borough of Lambeth. Its long streets of Victorian and Edwardian terraces, relatively affordable compared to neighbouring areas, attract young families and professionals who invest in loft conversions and extensions to create the space they need.",
            "<strong>Victorian and Edwardian terraces:</strong> Streatham's housing stock is predominantly Victorian and Edwardian terraces in a variety of sizes — from compact two-bed cottages to substantial three-storey family houses. These properties are well suited to dormer loft conversions, rear extensions, and side-return infills. We design projects that work with the existing structure and proportions of each house type.",
            "<strong>Conservation areas:</strong> The Streatham Lodge Conservation Area and Streatham Common Conservation Area cover selected streets with particular architectural character. Within these zones, Article 4 Directions may restrict permitted development rights, and Heritage Statements are required for planning applications. Our MCIAT-chartered team prepares conservation-sensitive designs.",
            "<strong>Lambeth's dormer guidance:</strong> Lambeth Council has published specific guidance on dormer design for residential properties. The council expects rear dormers to be set back from the eaves, set in from party walls, and constructed in materials that match the existing roof. Front dormers are generally resisted on Victorian and Edwardian properties. We design dormers that comply with Lambeth's standards.",
            "<strong>Value-driven projects:</strong> Streatham's relatively lower property values (compared to Clapham, Balham, or Dulwich) mean that project budgets are often tighter. Our fixed-fee pricing from £840 makes professional architectural drawings accessible, and we design schemes that deliver maximum impact within realistic construction budgets.",
        ],
        "stats": [
            ("Conservation areas", "Streatham Lodge CA"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Lambeth Council"),
            ("Key postcodes", "SW16"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Streatham?",
                "Yes, loft conversions are very popular in Streatham. Outside conservation areas, rear dormers under permitted development are straightforward and can add a bedroom and bathroom without planning permission. Within conservation areas, planning permission is required. We survey your roof and confirm the best approach.",
            ),
            (
                "What size extension can I build in Streatham without planning permission?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey (up to 6 metres with prior notification). Semi-detached houses can extend up to 4 metres (or 6 metres with prior notification). Within conservation areas, planning permission is typically required. We confirm what applies to your specific property.",
            ),
            (
                "What does Lambeth Council look for in dormer designs?",
                "Lambeth expects rear dormers to be set back from the eaves by at least one tile course, set in from party walls by at least 200mm, and clad in materials matching the existing roof. The dormer should be subordinate to the existing roof form. Front dormers are generally refused on period properties. We design dormers that meet these standards.",
            ),
            (
                "How much do architectural drawings cost in Streatham?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden charges — particularly important for budget-conscious projects.",
            ),
            (
                "Can I add a side-return extension to my Streatham terrace?",
                "Side-return extensions are an excellent way to widen a narrow kitchen or dining room. They are often achievable under permitted development if the roof is no higher than 4 metres and the extension does not extend beyond the rear wall of the original house. We assess your property and design a scheme that maximises the available space.",
            ),
        ],
    },
    {
        "name": "Herne Hill",
        "slug": "herne-hill",
        "borough": "Lambeth",
        "borough_slug": "lambeth",
        "postcodes": "SE24",
        "character": "Herne Hill has a village-like feel with independent shops, a lido, and streets of attractive Victorian terraces. It straddles the Lambeth-Southwark border, adding planning complexity to projects.",
        "housing_stock": "Victorian terraces, Edwardian villas, some mansion flats",
        "conservation_notes": "Poets Corner Conservation Area; Herne Hill & Stradella Road Conservation Area",
        "planning_notes": "Properties may fall under either Lambeth or Southwark Council depending on their exact location. The area has multiple conservation areas with Article 4 Directions. Checking the relevant authority and conservation area status is essential before starting any project.",
        "nearby": ["dulwich", "brixton", "east-dulwich", "streatham"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Herne Hill's Victorian terraces. MCIAT chartered, fixed fees, dual-borough expertise for both Lambeth and Southwark properties.",
        "local_context_title": "Why Herne Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Herne Hill sits in the SE24 postcode, straddling the boundary between Lambeth and Southwark. Its village atmosphere, attractive Victorian housing, and proximity to Brockwell Park have made it one of south-east London's most desirable family neighbourhoods. The dual-borough complexity and multiple conservation areas make professional architectural guidance essential.",
            "<strong>Dual-borough planning:</strong> The first step for any Herne Hill project is confirming whether the property falls under Lambeth or Southwark Council. The borough boundary runs through the neighbourhood, and the two councils have different planning policies, application procedures, and conservation area controls. Our team identifies the relevant authority and tailors the application accordingly.",
            "<strong>Conservation areas:</strong> Herne Hill contains several conservation areas including the Poets Corner Conservation Area and the Herne Hill & Stradella Road Conservation Area. These zones have Article 4 Directions that remove most permitted development rights, requiring planning permission for dormer conversions, replacement windows, and many extensions. Heritage Statements are required for all applications within conservation areas.",
            "<strong>Victorian terraces:</strong> The neighbourhood's Victorian terraces are well proportioned with good roof voids for loft conversions and adequate garden depths for rear extensions. Many properties retain original period features that influence design decisions. Our MCIAT-chartered team designs extensions and conversions that complement the existing architecture.",
            "<strong>Rear extensions and open-plan living:</strong> Single-storey rear extensions creating open-plan kitchen-dining spaces are extremely popular in Herne Hill. The area's family demographic drives demand for larger ground-floor living areas. Side-return infills are common on properties with side passages.",
        ],
        "stats": [
            ("Conservation areas", "Poets Corner, Herne Hill CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Lambeth / Southwark"),
            ("Key postcodes", "SE24"),
        ],
        "faqs": [
            (
                "Which council handles planning in Herne Hill?",
                "It depends on which side of the borough boundary your property sits. The boundary runs through Herne Hill, with some streets under Lambeth and others under Southwark. The two councils have different policies and procedures. We confirm your authority at the outset.",
            ),
            (
                "Can I build a loft conversion in Herne Hill?",
                "Yes, loft conversions are popular in SE24. Outside conservation areas, rear dormers can often be built under permitted development. Within the multiple conservation areas, planning permission is required. We survey your property and advise on the best approach for your specific location.",
            ),
            (
                "What conservation areas are in Herne Hill?",
                "The main conservation areas are the Poets Corner Conservation Area, the Herne Hill & Stradella Road Conservation Area, and parts of the Ruskin Park Conservation Area. Article 4 Directions in these zones require planning permission for most external alterations. We check your property's conservation status as part of our initial assessment.",
            ),
            (
                "How much do architectural drawings cost in Herne Hill?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 includes planning, building regulations, and structural calculations. Both packages are fixed-fee with no hidden charges.",
            ),
            (
                "Can I extend into my side return in Herne Hill?",
                "Side-return extensions are a popular way to widen narrow Victorian kitchens. They are often achievable under permitted development outside conservation areas. Within conservation areas, planning permission is required. We design side-return extensions that work with the existing house proportions and comply with local planning policy.",
            ),
        ],
    },
    {
        "name": "Blackheath",
        "slug": "blackheath",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE3",
        "character": "Blackheath is an elegant south-east London neighbourhood centred on a historic village and open heath. Its Georgian and Victorian houses, many in conservation areas, require heritage-sensitive architectural design.",
        "housing_stock": "Georgian townhouses, Victorian villas, Edwardian houses, Span developments",
        "conservation_notes": "Blackheath Conservation Area (one of the largest in south-east London); Blackheath Park Conservation Area",
        "planning_notes": "Properties may fall under Lewisham or Greenwich Council. The extensive Blackheath Conservation Area imposes strict design controls. The Span estates have their own design guidelines.",
        "nearby": ["deptford", "dulwich", "woolwich", "sydenham"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and loft conversions for Blackheath's Georgian and Victorian properties. MCIAT chartered, fixed fees, conservation area expertise built in.",
        "local_context_title": "Why Blackheath demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Blackheath sits in the SE3 postcode, straddling the boundary between the London boroughs of Lewisham and Greenwich. The neighbourhood's elegant Georgian and Victorian architecture, centred on the village and heath, creates one of south-east London's most historically significant residential areas — and one of its most demanding planning environments.",
            "<strong>Blackheath Conservation Area:</strong> The Blackheath Conservation Area is one of the largest in south-east London, covering the village centre, the terraces facing the heath, and surrounding residential streets. Article 4 Directions restrict most permitted development rights. Planning permission and Heritage Statements are required for external alterations, and Lewisham's (or Greenwich's) conservation officers scrutinise proposals carefully.",
            "<strong>Georgian and Victorian heritage:</strong> Blackheath's Georgian townhouses and Victorian villas are among the finest in south-east London. Many are individually listed, requiring Listed Building Consent for internal and external works. Our MCIAT-chartered team produces the detailed architectural drawings and Heritage Impact Assessments that listed building applications demand.",
            "<strong>Span developments:</strong> Blackheath is home to several Span estates — the pioneering modernist housing developments designed by Eric Lyons in the 1950s-60s. These estates have their own design guidelines and management companies. Any alterations must respect the original design language. We understand the Span aesthetic and prepare proposals that satisfy the estate management companies.",
            "<strong>Dual-borough complexity:</strong> Properties on the west side of the heath generally fall under Lewisham Council, while those on the east may be in Greenwich. The two boroughs have different planning policies and conservation approaches. We confirm the relevant authority and tailor applications accordingly.",
        ],
        "stats": [
            ("Conservation areas", "Blackheath CA"),
            ("Listed buildings", "Numerous"),
            ("Planning authority", "Lewisham / Greenwich"),
            ("Key postcodes", "SE3"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Blackheath?",
                "Almost certainly yes for external works. The Blackheath Conservation Area removes most permitted development rights through Article 4 Directions. Even replacement windows, roof changes, and some rear extensions require planning permission with a Heritage Statement. Our MCIAT-chartered team specialises in conservation-area applications in Blackheath.",
            ),
            (
                "Which council manages planning in Blackheath?",
                "Blackheath straddles Lewisham and Greenwich. The borough boundary roughly follows the A2. Properties to the west generally fall under Lewisham; those east under Greenwich. The two councils have different planning policies. We confirm your authority and adapt the application accordingly.",
            ),
            (
                "Can I extend a Span estate property in Blackheath?",
                "Span estate alterations must respect the original Eric Lyons design. Most changes require estate management approval in addition to planning permission. We understand the Span design principles and prepare proposals that satisfy both the estate management company and the planning authority.",
            ),
            (
                "What is Listed Building Consent?",
                "Listed Building Consent is required for any works that affect the character of a listed building, whether internal or external. It is a separate application from planning permission. Our team prepares detailed drawings, Heritage Impact Assessments, and material schedules to the standard expected for listed building applications.",
            ),
            (
                "How much do conservation-area drawings cost?",
                "Our Essentials package from £840 covers a single submission. For conservation area and listed building projects, the Bespoke package provides the higher level of detail typically required, including Heritage Statements and detailed material specifications. Contact us for a bespoke quote.",
            ),
        ],
    },
    {
        "name": "Deptford",
        "slug": "deptford",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE8",
        "character": "Deptford is a rapidly regenerating neighbourhood in Lewisham with a creative arts scene, warehouse conversions, and streets of Victorian terraces alongside major new developments.",
        "housing_stock": "Victorian terraces, warehouse conversions, new-build apartments, post-war estates",
        "conservation_notes": "Deptford High Street Conservation Area; St Paul's Deptford Conservation Area",
        "planning_notes": "Lewisham Council supports regeneration and high-quality design. Warehouse conversions may require change-of-use applications. The Deptford area is a priority regeneration zone with specific planning policies.",
        "nearby": ["bermondsey", "peckham", "blackheath", "woolwich"],
        "popular_services": ["planning-drawings", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, warehouse conversions, loft extensions, and building regulations for Deptford's diverse housing stock. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why Deptford demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Deptford sits in the SE8 postcode within the London Borough of Lewisham, positioned between Greenwich and Bermondsey along the south bank of the Thames. The neighbourhood's mix of Victorian terraces, ex-industrial buildings, and major new developments creates a dynamic planning environment where every project demands carefully prepared architectural drawings.",
            "<strong>Regeneration context:</strong> Deptford is one of Lewisham's priority regeneration areas, with significant new development around Deptford station and the waterfront. This context means Lewisham Council is generally receptive to well-designed proposals that contribute to the area's renewal, but expects high-quality design and appropriate scale.",
            "<strong>Warehouse and industrial conversions:</strong> Deptford's creative reputation has been built partly on the conversion of former industrial buildings to studios, galleries, and residential use. These projects require change-of-use applications, structural assessments, and building regulations compliance. Our MCIAT-chartered team handles the full conversion process.",
            "<strong>Conservation areas:</strong> The Deptford High Street Conservation Area and the St Paul's Deptford Conservation Area protect the historic character of the town centre and its finest Georgian and Victorian buildings. Within these zones, planning permission and Heritage Statements are required for external alterations.",
            "<strong>Victorian terraces:</strong> Away from the main regeneration sites, Deptford's residential streets contain Victorian terraces suitable for loft conversions and rear extensions. These properties offer good value compared to neighbouring areas, and investment in extensions and conversions is common.",
        ],
        "stats": [
            ("Conservation areas", "Deptford High St CA"),
            ("Regeneration", "Priority area"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE8"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a warehouse conversion in Deptford?",
                "Usually yes. Converting commercial or industrial space to residential requires a change-of-use planning application. Permitted development rights under Class MA may apply in limited cases, but prior approval is still needed. Within conservation areas, full planning permission is required. Our team manages the complete application process.",
            ),
            (
                "Can I build a loft conversion in Deptford?",
                "Yes, loft conversions are achievable on Deptford's Victorian terraces. Outside conservation areas, rear dormers under permitted development are straightforward. Within conservation areas, planning permission is required. We survey the roof structure and advise on the most feasible approach.",
            ),
            (
                "What are the planning policies for Deptford regeneration areas?",
                "Lewisham Council has specific planning policies for Deptford's regeneration zones, including requirements for design quality, building heights, and affordable housing contributions for larger schemes. We ensure applications align with the relevant area-specific policies.",
            ),
            (
                "How much do architectural drawings cost in Deptford?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Warehouse conversion projects are quoted on a bespoke basis.",
            ),
            (
                "How long does planning permission take in Lewisham?",
                "Lewisham Council targets 8 weeks for householder applications and 13 weeks for major applications. Pre-application advice is available and recommended for complex projects. We manage the timeline and handle all council correspondence.",
            ),
        ],
    },
    {
        "name": "Woolwich",
        "slug": "woolwich",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE18",
        "character": "Woolwich is undergoing major regeneration centred on the Royal Arsenal development and the new Crossrail station. Projects range from new-build apartments to extensions on Victorian and Edwardian terraces.",
        "housing_stock": "Victorian terraces, Edwardian houses, new-build apartments, military heritage buildings",
        "conservation_notes": "Woolwich Common Conservation Area; Royal Arsenal Conservation Area",
        "planning_notes": "Royal Borough of Greenwich Council is supportive of regeneration. The Royal Arsenal area has specific heritage constraints. Flood risk assessments may be required near the Thames.",
        "nearby": ["blackheath", "deptford", "bermondsey"],
        "popular_services": ["planning-drawings", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and building regulations for Woolwich's mix of period terraces and regeneration-area properties. MCIAT chartered, fixed fees, Greenwich planning expertise built in.",
        "local_context_title": "Why Woolwich demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Woolwich sits in the SE18 postcode within the Royal Borough of Greenwich, positioned on the south bank of the Thames opposite Silvertown. The arrival of the Elizabeth Line has accelerated regeneration, creating a mix of new development and established residential streets where different project types require different planning approaches.",
            "<strong>Regeneration and new development:</strong> The Royal Arsenal development, Woolwich town centre regeneration, and Elizabeth Line arrival have transformed the area's property market. New-build apartment owners may seek interior reconfigurations, while terraced house owners pursue loft conversions and extensions. We handle both project types.",
            "<strong>Royal Arsenal Conservation Area:</strong> The Royal Arsenal site is a conservation area with Grade I and Grade II listed buildings, including the former military buildings now converted to residential use. Works to these properties require heritage-sensitive design and often Listed Building Consent. Our MCIAT-chartered team has experience with heritage buildings of this type.",
            "<strong>Victorian and Edwardian terraces:</strong> Woolwich's established residential streets contain Victorian and Edwardian terraces well suited to loft conversions and rear extensions. Greenwich Council is generally supportive of sympathetic residential extensions outside conservation areas.",
            "<strong>Flood risk:</strong> Properties near the Thames may require Flood Risk Assessments. The Thames Barrier provides protection, but planning applications must still address flood risk where relevant. We include the necessary assessments in our applications.",
        ],
        "stats": [
            ("Conservation areas", "Royal Arsenal CA"),
            ("Transport", "Elizabeth Line"),
            ("Planning authority", "Greenwich Council"),
            ("Key postcodes", "SE18"),
        ],
        "faqs": [
            (
                "Can I extend my Woolwich terrace?",
                "Yes, rear extensions and loft conversions are common on Woolwich's Victorian and Edwardian terraces. Outside conservation areas, permitted development rights allow single-storey rear extensions up to 4 metres (terraced) or 6 metres (detached) without planning permission. We confirm what is permissible for your property.",
            ),
            (
                "What heritage constraints apply at the Royal Arsenal?",
                "The Royal Arsenal is a conservation area with multiple listed buildings. Works to listed buildings require Listed Building Consent, and any development within the conservation area must respect the military heritage character. Heritage Statements and detailed design drawings are essential. Our team prepares applications to the required standard.",
            ),
            (
                "Is a flood risk assessment needed for my Woolwich project?",
                "If your property is in Flood Zone 2 or 3, a Flood Risk Assessment is required. While the Thames Barrier provides protection, planning applications must address residual flood risk. We incorporate the necessary assessments from the outset.",
            ),
            (
                "How much do architectural drawings cost in Woolwich?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Heritage projects at the Royal Arsenal are quoted on a bespoke basis.",
            ),
            (
                "How has Crossrail affected planning in Woolwich?",
                "The Elizabeth Line has intensified development interest, and Greenwich Council has updated planning policies for the town centre accordingly. Higher-density schemes may be acceptable near the station, but design quality expectations have also increased. We ensure applications meet current policy requirements.",
            ),
        ],
    },
    {
        "name": "Bow",
        "slug": "bow",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E3",
        "character": "Bow is a residential neighbourhood in Tower Hamlets with Victorian terraces alongside canal-side conversions and Olympic Park regeneration. Loft conversions and extensions are in strong demand.",
        "housing_stock": "Victorian terraces, canal-side conversions, post-war estates, new-build apartments",
        "conservation_notes": "Fairfield Road Conservation Area; parts of Victoria Park Conservation Area",
        "planning_notes": "Tower Hamlets Council applies specific design guidance for residential extensions. The borough has particular policies on housing density and mix. Canal-side properties may require additional environmental assessments.",
        "nearby": ["bethnal-green", "hackney-wick", "shoreditch"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Bow's Victorian terraces and canal-side properties. MCIAT chartered, fixed fees, Tower Hamlets planning expertise built in.",
        "local_context_title": "Why Bow demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Bow occupies the E3 postcode in the London Borough of Tower Hamlets, stretching from Victoria Park in the north to the Limehouse Cut in the south. Its mix of Victorian terraced streets, canal-side developments, and post-Olympic regeneration areas creates a varied planning landscape.",
            "<strong>Victorian terraces:</strong> Bow's Victorian terraces — many originally built for workers in the area's factories and docks — are now highly sought after by families. These properties are ideal candidates for rear dormers, single-storey rear extensions, and side-return infills. We design projects that maximise space while respecting the existing terrace proportions.",
            "<strong>Conservation areas:</strong> The Fairfield Road Conservation Area and parts of the Victoria Park Conservation Area protect Bow's finest Victorian streets. Article 4 Directions may restrict permitted development rights within these zones, and Heritage Statements are required for planning applications.",
            "<strong>Canal-side properties:</strong> Properties adjacent to the Regent's Canal or Limehouse Cut may require additional environmental assessments and Environment Agency consultation. Canal-side conversions of former industrial buildings are a specialty of our practice.",
            "<strong>Tower Hamlets design guidance:</strong> The borough has published specific guidance on residential extensions, including requirements for dormer design, extension depths, and retention of garden space. Our MCIAT-chartered team designs projects that comply with this guidance from the outset.",
        ],
        "stats": [
            ("Conservation areas", "Fairfield Road CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E3"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Bow?",
                "Yes, loft conversions are very popular in E3. Outside conservation areas, rear dormers under permitted development are straightforward for Victorian terraces. Within conservation areas, planning permission is required. We survey your roof and confirm the best approach.",
            ),
            (
                "What size rear extension can I build in Bow?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey without planning permission. Tower Hamlets has specific design guidance on extension depths and materials. Within conservation areas, planning permission is required. We confirm what is achievable for your property.",
            ),
            (
                "Are there special rules for canal-side properties?",
                "Canal-side properties may require Environment Agency consultation, and any works affecting the waterway or towpath need additional permissions. We incorporate these requirements into the application process and coordinate with the relevant authorities.",
            ),
            (
                "How much do architectural drawings cost in Bow?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "How long does Tower Hamlets take to decide applications?",
                "Tower Hamlets targets 8 weeks for householder applications. Conservation area applications may take longer. Pre-application advice is available and recommended for complex sites. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Bethnal Green",
        "slug": "bethnal-green",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E2",
        "character": "Bethnal Green is a dense, evolving neighbourhood in Tower Hamlets mixing Victorian terraces with former industrial buildings and council estates. Loft conversions and warehouse adaptations are common projects.",
        "housing_stock": "Victorian terraces, ex-industrial buildings, post-war estates, mansion blocks",
        "conservation_notes": "Several small conservation areas including Jesus Hospital Estate and Approach Road",
        "planning_notes": "Tower Hamlets Council has strong policies on housing mix and density. Many properties have been subdivided, and further subdivision faces scrutiny. Design standards for extensions are clearly defined in the borough's planning guidance.",
        "nearby": ["shoreditch", "bow", "hackney-wick", "dalston"],
        "popular_services": ["loft-conversions", "planning-drawings", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Bethnal Green's Victorian terraces and converted industrial properties. MCIAT chartered, fixed fees, Tower Hamlets planning expertise built in.",
        "local_context_title": "Why Bethnal Green demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Bethnal Green occupies the E2 postcode in the heart of Tower Hamlets, bordered by Shoreditch to the west, Bow to the east, and Mile End to the south. The neighbourhood's Victorian terraces, former industrial buildings, and significant council housing estates create a diverse built environment where each project type demands different architectural and planning expertise.",
            "<strong>Victorian terraces:</strong> Bethnal Green's compact Victorian terraces are ideal candidates for loft conversions and rear extensions that can transform a two-bedroom house into a family home. Outside conservation areas, rear dormers under permitted development are straightforward. Side-return extensions are less common due to the tight terrace layout, but rear extensions can significantly improve ground-floor living space.",
            "<strong>Conservation areas:</strong> Several small conservation areas protect Bethnal Green's most architecturally significant streets, including the Jesus Hospital Estate and parts of Approach Road. Article 4 Directions within these zones require planning permission for external works. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>Industrial conversions:</strong> Former workshops, warehouses, and light-industrial buildings continue to be converted to residential use in Bethnal Green. These projects require change-of-use planning applications, building regulations compliance, and often structural engineering input. We handle the complete process.",
            "<strong>Tower Hamlets housing policy:</strong> The borough has strong policies protecting family housing and resisting further subdivision of houses into flats. Any proposal to subdivide or convert a house must demonstrate compliance with the borough's housing mix policies. We advise on what is feasible and prepare applications that address policy requirements.",
        ],
        "stats": [
            ("Conservation areas", "Jesus Hospital Estate CA"),
            ("Housing type", "Victorian terraces, industrial"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E2"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Bethnal Green?",
                "Yes, loft conversions are very popular in E2. Outside conservation areas, rear dormers under permitted development are straightforward. Within conservation areas, planning permission is required but Tower Hamlets is generally supportive of well-designed dormers. We survey your roof and advise on the best approach.",
            ),
            (
                "Can I convert an industrial building to residential in Bethnal Green?",
                "Converting industrial or commercial space to residential use typically requires a change-of-use planning application. Permitted development rights under Class MA may apply in some cases. Building regulations compliance is also required, covering fire safety, sound insulation, and energy efficiency. Our team handles the full process.",
            ),
            (
                "Can I subdivide my house into flats?",
                "Tower Hamlets has strong policies protecting family housing. Subdivision requires planning permission and must demonstrate compliance with the borough's housing mix policies. Each unit must meet minimum space standards. We advise on feasibility and prepare applications where appropriate.",
            ),
            (
                "How much do architectural drawings cost in Bethnal Green?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Industrial conversion projects are quoted on a bespoke basis.",
            ),
            (
                "What building regulations apply to loft conversions?",
                "Loft conversions must comply with Approved Documents covering structure (Part A), fire safety (Part B — including means of escape and fire doors), energy efficiency (Part L), stairs (Part K), and sound insulation (Part E). We prepare fully compliant building regulations drawings and coordinate with Building Control.",
            ),
        ],
    },
    {
        "name": "Acton",
        "slug": "acton",
        "borough": "Ealing",
        "borough_slug": "ealing",
        "postcodes": "W3",
        "character": "Acton is a diverse west London neighbourhood with good transport links and streets of Victorian and Edwardian terraces. The Elizabeth Line has boosted property values and investment in home improvements.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, 1930s housing",
        "conservation_notes": "Acton Town Centre Conservation Area; Mill Hill Park Conservation Area",
        "planning_notes": "Ealing Council is generally supportive of sympathetic residential extensions. Permitted development rights are available outside conservation areas. The Elizabeth Line arrival has increased development interest in the area.",
        "nearby": ["chiswick", "wembley", "kilburn"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Acton's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Ealing planning expertise built in.",
        "local_context_title": "Why Acton demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Acton sits in the W3 postcode within the London Borough of Ealing, well connected to central London via the Elizabeth Line, Central Line, and North London Line. Its mix of Victorian terraces, Edwardian family houses, and inter-war semis provides a broad range of residential extension and conversion opportunities.",
            "<strong>Victorian and Edwardian terraces:</strong> Acton's older housing stock — concentrated in areas like South Acton and East Acton — includes well-proportioned Victorian and Edwardian terraces ideal for loft conversions and rear extensions. These properties typically have slate roofs with good headroom, making dormer conversions a popular and cost-effective way to add space.",
            "<strong>Conservation areas:</strong> The Acton Town Centre Conservation Area and Mill Hill Park Conservation Area protect the area's most architecturally significant streets. Within these zones, Article 4 Directions may restrict permitted development rights. Our MCIAT-chartered team prepares applications that satisfy Ealing Council's heritage officers.",
            "<strong>Elizabeth Line effect:</strong> The arrival of the Elizabeth Line at Acton Main Line has increased property values and investment in home improvements. Many homeowners are choosing to extend and improve rather than move, driving demand for loft conversions, rear extensions, and full refurbishment schemes.",
            "<strong>Inter-war housing:</strong> Parts of Acton have 1930s semi-detached houses with side access and generous gardens. These properties offer excellent potential for side and rear extensions, garage conversions, and hip-to-gable loft conversions. We design schemes that maximise the available space within Ealing's planning policies.",
        ],
        "stats": [
            ("Conservation areas", "Mill Hill Park CA"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Ealing Council"),
            ("Key postcodes", "W3"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Acton?",
                "Yes, loft conversions are very popular in Acton. Outside conservation areas, rear dormers under permitted development are straightforward. Hip-to-gable conversions on 1930s semis can significantly increase loft floor area. Within conservation areas, planning permission is required. We survey your roof and advise on the best approach.",
            ),
            (
                "What size extension can I build in Acton?",
                "Under permitted development, single-storey rear extensions up to 4 metres (terraced/semi) or 8 metres (detached) are achievable. Ealing Council also allows two-storey rear extensions up to 3 metres under certain conditions. Within conservation areas, planning permission is required. We confirm what applies to your property.",
            ),
            (
                "Are there planning restrictions near Acton station?",
                "The area around Acton Main Line station is subject to specific development policies due to the Elizabeth Line arrival. These primarily affect larger schemes and commercial development. Householder applications for residential extensions are generally handled under standard policies. We ensure your application complies with current requirements.",
            ),
            (
                "How much do architectural drawings cost in Acton?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "Can I convert my garage in Acton?",
                "Garage conversions are often achievable under permitted development and are a cost-effective way to add living space. Building regulations approval is required for the conversion to ensure adequate insulation, damp-proofing, and ventilation. We prepare the necessary drawings for both the planning and building regulations aspects.",
            ),
        ],
    },
    {
        "name": "Twickenham",
        "slug": "twickenham",
        "borough": "Richmond upon Thames",
        "borough_slug": "richmond-upon-thames",
        "postcodes": "TW1",
        "character": "Twickenham is a leafy suburban town in Richmond upon Thames known for the rugby stadium, Edwardian housing, and riverside setting. Extensions and loft conversions on period properties are the most common projects.",
        "housing_stock": "Edwardian houses, Victorian terraces, inter-war semis, riverside properties",
        "conservation_notes": "Twickenham Riverside Conservation Area; St Margarets Conservation Area",
        "planning_notes": "Richmond Council is one of London's most conservation-focused boroughs with extensive Article 4 coverage. The borough-wide character is protected, and design quality expectations are high for all applications.",
        "nearby": ["richmond", "teddington", "barnes"],
        "popular_services": ["house-extensions", "loft-conversions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and heritage-sensitive design for Twickenham's Edwardian and Victorian properties. MCIAT chartered, fixed fees, Richmond Council expertise built in.",
        "local_context_title": "Why Twickenham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Twickenham sits in the TW1 postcode within the London Borough of Richmond upon Thames, one of London's most architecturally protected boroughs. Its Edwardian houses, riverside setting, and extensive conservation area coverage make professional architectural guidance essential for virtually any external alteration.",
            "<strong>Conservation area coverage:</strong> Richmond upon Thames has one of the highest proportions of conservation area coverage in London. The Twickenham Riverside Conservation Area and St Margarets Conservation Area protect much of the town's historic core and residential streets. Article 4 Directions remove most permitted development rights within these zones, and Heritage Statements are required for all planning applications.",
            "<strong>Edwardian housing:</strong> Twickenham's residential streets are dominated by substantial Edwardian houses — many with bay windows, decorative tile work, and well-proportioned rooms. These properties are popular candidates for rear extensions, loft conversions, and internal reconfiguration. Richmond Council expects extension designs to complement the existing Edwardian character.",
            "<strong>Richmond Council design standards:</strong> Richmond Council applies particularly high design standards to all residential applications. The borough's planning policies require extensions to be subordinate to the original building, use matching or complementary materials, and maintain the character of the street. Our MCIAT-chartered team is experienced in meeting these standards.",
            "<strong>Riverside properties:</strong> Properties near the Thames may require flood risk assessments and Environment Agency consultation. Richmond Council also protects river views and the Thames-side character through specific planning policies.",
        ],
        "stats": [
            ("Conservation areas", "Twickenham Riverside CA"),
            ("Housing type", "Edwardian houses"),
            ("Planning authority", "Richmond Council"),
            ("Key postcodes", "TW1"),
        ],
        "faqs": [
            (
                "Do I need planning permission in Twickenham?",
                "For most external works, yes. Richmond Council's extensive conservation area coverage and Article 4 Directions mean that permitted development rights are removed for many properties. Even replacement windows and roof alterations may require planning permission. We check your property's status and advise on the requirements.",
            ),
            (
                "Can I build a loft conversion in Twickenham?",
                "Loft conversions are achievable but may require planning permission within conservation areas. Richmond Council has specific requirements for dormer design, including materials, proportions, and position on the roof. We design dormers that comply with the council's standards and submit the necessary applications.",
            ),
            (
                "What are Richmond Council's design expectations?",
                "Richmond Council applies some of the highest design standards in London. Extensions must be subordinate to the original building, use matching or complementary materials, and respect the existing streetscape. Design and Access Statements are required for most applications. Our MCIAT-chartered team is experienced in meeting these expectations.",
            ),
            (
                "How much do architectural drawings cost in Twickenham?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Bespoke packages for listed building and complex conservation area projects are priced individually.",
            ),
            (
                "Is a flood risk assessment needed for riverside properties?",
                "Properties near the Thames in Twickenham may require a Flood Risk Assessment with their planning application. The Environment Agency is a statutory consultee for developments in Flood Zones 2 and 3. We incorporate flood risk requirements into the application from the outset.",
            ),
        ],
    },
    {
        "name": "Teddington",
        "slug": "teddington",
        "borough": "Richmond upon Thames",
        "borough_slug": "richmond-upon-thames",
        "postcodes": "TW11",
        "character": "Teddington is a quiet, family-oriented town in Richmond upon Thames with Victorian and Edwardian housing, a riverside setting, and a village high street. Extensions and loft conversions are the main project types.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, riverside cottages",
        "conservation_notes": "Teddington Lock Conservation Area; parts of Broad Street Conservation Area",
        "planning_notes": "Richmond Council applies high design standards throughout the borough. Conservation area coverage is extensive. Flood risk assessments may be required for properties near the Thames.",
        "nearby": ["twickenham", "richmond", "barnes"],
        "popular_services": ["house-extensions", "loft-conversions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and building regulations for Teddington's Victorian and Edwardian properties. MCIAT chartered, fixed fees, Richmond Council expertise built in.",
        "local_context_title": "Why Teddington demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Teddington sits in the TW11 postcode at the southern edge of the London Borough of Richmond upon Thames, where the river passes Teddington Lock and becomes non-tidal. Its family-oriented character, excellent schools, and attractive Victorian and Edwardian housing make it one of south-west London's most desirable residential areas.",
            "<strong>Conservation area protection:</strong> Parts of Teddington fall within conservation areas including the Teddington Lock Conservation Area. Richmond Council applies Article 4 Directions that remove permitted development rights for many external alterations, meaning planning permission is required for roof changes, window replacements, and extensions within these zones.",
            "<strong>Victorian and Edwardian housing:</strong> Teddington's residential streets contain a mix of Victorian terraces, Edwardian semis, and inter-war houses. These properties are popular candidates for rear extensions, loft conversions, and whole-house refurbishment. Richmond Council expects designs that respect the existing character while meeting modern living standards.",
            "<strong>Riverside properties:</strong> Properties near the Thames and Teddington Lock may require flood risk assessments. The council protects the riverside character and views through specific planning policies. Our MCIAT-chartered team incorporates these requirements into applications from the outset.",
            "<strong>High design standards:</strong> Richmond Council maintains some of London's highest design standards for residential extensions. Materials, proportions, and detailing are all closely scrutinised. Our team designs extensions that meet these standards while delivering the space and functionality our clients need.",
        ],
        "stats": [
            ("Conservation areas", "Teddington Lock CA"),
            ("Housing type", "Victorian/Edwardian houses"),
            ("Planning authority", "Richmond Council"),
            ("Key postcodes", "TW11"),
        ],
        "faqs": [
            (
                "Can I extend my house in Teddington?",
                "Yes, extensions are very common in Teddington. Outside conservation areas, single-storey rear extensions under permitted development are straightforward. Within conservation areas, planning permission is required. Richmond Council has high design standards. We design extensions that comply with local policy and submit the necessary applications.",
            ),
            (
                "What are the rules for loft conversions in Teddington?",
                "Richmond Council requires dormer designs that respect the existing roof profile and use matching materials. Within conservation areas, planning permission is needed. Outside conservation areas, rear dormers under permitted development are achievable. We survey your roof and advise on the best conversion type.",
            ),
            (
                "Do I need a flood risk assessment in Teddington?",
                "Properties near the Thames or Teddington Lock may require a Flood Risk Assessment with their planning application. The Environment Agency is consulted for developments in Flood Zones 2 and 3. We advise on whether this applies to your property and coordinate the assessment.",
            ),
            (
                "How much do architectural drawings cost in Teddington?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Richmond Council take for planning decisions?",
                "Richmond Council targets 8 weeks for householder applications. Conservation area applications may take longer due to heritage officer review and the 21-day notification period. Pre-application advice is available and recommended for complex schemes.",
            ),
        ],
    },
    {
        "name": "Wembley",
        "slug": "wembley",
        "borough": "Brent",
        "borough_slug": "brent",
        "postcodes": "HA9",
        "character": "Wembley is a diverse suburban neighbourhood in Brent with inter-war and post-war housing alongside major regeneration around the stadium. Extensions and loft conversions are popular on the area's semi-detached houses.",
        "housing_stock": "1930s semi-detached, inter-war terraces, new-build apartments, some Victorian",
        "conservation_notes": "Barn Hill Conservation Area near Fryent Country Park",
        "planning_notes": "Brent Council supports residential extensions that comply with design guidance. The Wembley area is a regeneration zone with specific development policies for larger schemes. Householder applications are generally straightforward outside conservation areas.",
        "nearby": ["kilburn", "acton", "tottenham"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Wembley's semi-detached houses and terraces. MCIAT chartered, fixed fees, Brent planning expertise built in.",
        "local_context_title": "Why Wembley demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Wembley sits in the HA9 postcode within the London Borough of Brent, centred around the iconic stadium and stretching into established residential suburbs. The area's 1930s semi-detached houses and inter-war terraces offer significant potential for extensions and loft conversions, while the regeneration zone around the stadium is reshaping the neighbourhood.",
            "<strong>1930s semi-detached houses:</strong> Wembley's most common housing type is the inter-war semi-detached house with side access, a front bay window, and a rear garden of 10-15 metres. These properties are excellent candidates for hip-to-gable loft conversions (which can nearly double the loft floor area), side extensions, and rear extensions. We design schemes that make the most of the available space.",
            "<strong>Loft conversion potential:</strong> Hip-to-gable loft conversions combined with rear dormers are particularly popular on Wembley's 1930s semis. Under permitted development, these can often be built without planning permission, transforming the roof space into two additional rooms. We survey the roof structure, confirm PD eligibility, and prepare building regulations drawings.",
            "<strong>Regeneration zone:</strong> The Wembley Park area around the stadium is a designated regeneration zone with specific planning policies encouraging higher-density development. These policies primarily affect larger commercial and residential schemes rather than householder applications, but we ensure all applications comply with current area-specific requirements.",
            "<strong>Brent design guidance:</strong> Brent Council has published specific design guidance for residential extensions covering extension depths, dormer proportions, and materials. Our MCIAT-chartered team designs projects that comply with this guidance from the outset, avoiding costly redesigns after submission.",
        ],
        "stats": [
            ("Conservation areas", "Barn Hill CA"),
            ("Housing type", "1930s semi-detached"),
            ("Planning authority", "Brent Council"),
            ("Key postcodes", "HA9"),
        ],
        "faqs": [
            (
                "Can I build a hip-to-gable loft conversion in Wembley?",
                "Yes, hip-to-gable conversions are very popular on Wembley's 1930s semis. They can often be built under permitted development when combined with a rear dormer, provided the total roof volume increase does not exceed 50 cubic metres. We survey your roof and confirm PD eligibility.",
            ),
            (
                "What size extension can I build in Wembley?",
                "Under permitted development, semi-detached houses can build single-storey rear extensions up to 4 metres (or 6 metres with prior notification). Side extensions under permitted development are possible with restrictions. Within the Barn Hill Conservation Area, planning permission is required. We confirm what is permissible.",
            ),
            (
                "Can I build a side extension in Wembley?",
                "Side extensions on Wembley's semi-detached houses are achievable under permitted development if they meet specific criteria — single storey, no wider than half the width of the original house, and materials to match. Two-storey side extensions require planning permission. We design side extensions that comply with all requirements.",
            ),
            (
                "How much do architectural drawings cost in Wembley?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. The most popular choice for loft conversions is the Complete package.",
            ),
            (
                "How long does Brent Council take for planning decisions?",
                "Brent targets 8 weeks for householder applications. The borough is one of London's busier planning authorities. Pre-application advice is available. We manage the application timeline and handle all council correspondence.",
            ),
        ],
    },
    {
        "name": "Kilburn",
        "slug": "kilburn",
        "borough": "Brent",
        "borough_slug": "brent",
        "postcodes": "NW6",
        "character": "Kilburn straddles the Brent-Camden border and is known for its Victorian terraces, high conversion demand, and diverse community. Loft conversions and flat reconfiguration projects are in strong demand.",
        "housing_stock": "Victorian terraces, Edwardian houses, mansion blocks, converted flats",
        "conservation_notes": "Kilburn Conservation Area (Brent side); South Hampstead Conservation Area (Camden side)",
        "planning_notes": "Properties may fall under Brent or Camden Council depending on which side of the border. The two boroughs have different policies. Many properties have been converted to flats, adding complexity to extension projects.",
        "nearby": ["queens-park", "maida-vale", "belsize-park", "camden-town"],
        "popular_services": ["loft-conversions", "planning-drawings", "house-extensions"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Kilburn's Victorian terraces. MCIAT chartered, fixed fees, dual-borough expertise for Brent and Camden properties.",
        "local_context_title": "Why Kilburn demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Kilburn straddles the boundary between the London boroughs of Brent and Camden in the NW6 postcode. Its Victorian terraces, many converted into flats over previous decades, create a neighbourhood where planning and building regulations projects require careful navigation of dual-borough policies and multi-unit complexities.",
            "<strong>Dual-borough planning:</strong> The Kilburn High Road roughly marks the boundary between Brent and Camden. Properties on the west side generally fall under Brent; those on the east under Camden. The two boroughs have different planning policies, conservation area designations, and design expectations. Our team confirms the relevant authority and prepares applications tailored to the specific council.",
            "<strong>Victorian terraces and conversion demand:</strong> Kilburn's large Victorian terraces — many originally four or five bedrooms — have been extensively converted to flats. Current demand runs in both directions: some owners seek to subdivide further, while others want to reconvert buildings to single-family use. Both directions require planning permission and building regulations approval.",
            "<strong>Conservation areas:</strong> The Kilburn Conservation Area (Brent side) and the South Hampstead Conservation Area (Camden side) protect key streets. Article 4 Directions in both zones require planning permission for most external works. Heritage Statements must accompany applications.",
            "<strong>Loft conversions:</strong> Loft conversions on Kilburn's tall Victorian terraces can add significant value. Rear dormers, mansard conversions, and roof terrace additions are all achievable with the right design and planning approach. Our MCIAT-chartered team advises on what is feasible for each property.",
        ],
        "stats": [
            ("Conservation areas", "Kilburn CA (Brent)"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Brent / Camden"),
            ("Key postcodes", "NW6"),
        ],
        "faqs": [
            (
                "Which council handles planning in Kilburn?",
                "Kilburn straddles Brent and Camden. Properties west of the High Road are generally in Brent; those east in Camden. The two boroughs have different policies and application processes. We confirm your authority at the outset and tailor the application accordingly.",
            ),
            (
                "Can I convert my Kilburn house back to a single dwelling?",
                "Reconverting a multi-unit building to a single-family house generally requires planning permission. Both Brent and Camden have policies on housing mix that influence decisions. Building regulations approval is also needed for the conversion works. We prepare the full application package.",
            ),
            (
                "Can I build a loft conversion in Kilburn?",
                "Yes, loft conversions are popular in NW6. The tall Victorian terraces often have excellent loft potential. Outside conservation areas, rear dormers under permitted development are achievable. Within conservation areas, planning permission is required. We survey your property and advise on the best approach.",
            ),
            (
                "How much do architectural drawings cost in Kilburn?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no surprises.",
            ),
            (
                "What are the rules for dormer conversions in Camden vs Brent?",
                "Camden and Brent have different design requirements for dormers. Camden is generally stricter, requiring dormers to be set back and set in with specific proportions. Brent allows slightly more flexibility but still requires sympathetic design. We know the requirements for both boroughs and design accordingly.",
            ),
        ],
    },
    {
        "name": "Tottenham",
        "slug": "tottenham",
        "borough": "Haringey",
        "borough_slug": "haringey",
        "postcodes": "N17",
        "character": "Tottenham is a regenerating neighbourhood in Haringey with Victorian terraces, major new development around the stadium, and some of the most affordable period housing in inner London.",
        "housing_stock": "Victorian terraces, Edwardian houses, post-war estates, new-build apartments",
        "conservation_notes": "Bruce Castle Conservation Area; Tottenham Green Conservation Area",
        "planning_notes": "Haringey Council supports regeneration and investment in the existing housing stock. Permitted development rights are available outside conservation areas. The Tottenham area has specific regeneration policies for larger schemes.",
        "nearby": ["wood-green", "finsbury-park", "walthamstow"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Tottenham's Victorian terraces. MCIAT chartered, fixed fees from £840, Haringey planning expertise built in.",
        "local_context_title": "Why Tottenham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Tottenham occupies the N17 postcode in the London Borough of Haringey, stretching from Seven Sisters in the south to the borough boundary in the north. Its Victorian terraces, some of inner London's most affordable period housing, attract homeowners who invest in loft conversions and extensions to create the family space they need.",
            "<strong>Victorian terraces:</strong> Tottenham's housing stock is predominantly Victorian terraces — compact, well-built houses with slate roofs and rear outriggers. These are ideal candidates for dormer loft conversions, rear extensions, and side-return infills. Outside conservation areas, many projects can proceed under permitted development, keeping costs and timescales manageable.",
            "<strong>Regeneration context:</strong> The area around the football stadium has seen massive regeneration investment, including new housing, commercial space, and public realm improvements. Haringey Council is broadly supportive of investment in the existing housing stock, viewing residential extensions as contributing to the area's renewal.",
            "<strong>Conservation areas:</strong> The Bruce Castle Conservation Area and Tottenham Green Conservation Area protect the area's most historically significant buildings and spaces. Within these zones, Article 4 Directions may require planning permission for external alterations. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>Value-driven projects:</strong> Tottenham's relatively lower property values make cost-effective design particularly important. Our fixed-fee pricing from £840 ensures professional architectural drawings are accessible, and we design schemes that deliver maximum space within realistic budgets.",
        ],
        "stats": [
            ("Conservation areas", "Bruce Castle CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Haringey Council"),
            ("Key postcodes", "N17"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Tottenham?",
                "Yes, loft conversions are popular and cost-effective in N17. Outside conservation areas, rear dormers under permitted development are straightforward. Within conservation areas, planning permission is required. We survey your roof, confirm PD eligibility, and prepare the required drawings.",
            ),
            (
                "What size extension can I build in Tottenham?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey, and up to 6 metres with prior notification under the larger homes scheme. Within conservation areas, planning permission is required. We confirm what applies to your property.",
            ),
            (
                "How much do architectural drawings cost in Tottenham?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees make budgeting straightforward.",
            ),
            (
                "Does the regeneration zone affect my planning application?",
                "The regeneration zone policies primarily affect larger commercial and residential schemes. Householder applications for extensions and loft conversions are generally handled under standard planning policies. We ensure your application complies with all relevant policies.",
            ),
            (
                "Can I convert my Tottenham house to flats?",
                "Converting a house to flats requires planning permission. Haringey Council assesses the impact on housing mix and amenity. Each unit must meet minimum space standards. We advise on feasibility and prepare applications where appropriate.",
            ),
        ],
    },
    {
        "name": "Wood Green",
        "slug": "wood-green",
        "borough": "Haringey",
        "borough_slug": "haringey",
        "postcodes": "N22",
        "character": "Wood Green is a suburban neighbourhood in Haringey with Edwardian terraces, a busy town centre, and excellent transport links. Extensions and loft conversions are the most common project types.",
        "housing_stock": "Edwardian terraces, inter-war semis, 1960s apartments, some Victorian",
        "conservation_notes": "Trinity Gardens Conservation Area; Wood Green Common Conservation Area",
        "planning_notes": "Haringey Council is generally supportive of sympathetic residential extensions. The Wood Green town centre has specific regeneration policies. Permitted development rights are available outside conservation areas.",
        "nearby": ["tottenham", "crouch-end", "muswell-hill", "finsbury-park"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Wood Green's Edwardian terraces and family houses. MCIAT chartered, fixed fees, Haringey planning expertise built in.",
        "local_context_title": "Why Wood Green demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Wood Green sits in the N22 postcode within the London Borough of Haringey, positioned between the slopes of Muswell Hill to the west and Tottenham to the east. Its Edwardian terraces and suburban family houses, combined with excellent Piccadilly Line connections, make it a popular choice for families investing in home improvements.",
            "<strong>Edwardian terraces:</strong> Wood Green's residential streets are characterised by well-proportioned Edwardian terraces with bay windows, decorative tile work, and slate roofs. These properties are well suited to rear dormers, single-storey rear extensions, and side-return infills. We design schemes that complement the existing Edwardian character.",
            "<strong>Conservation areas:</strong> The Trinity Gardens Conservation Area and Wood Green Common Conservation Area protect key streets and open spaces. Within these zones, Article 4 Directions may restrict permitted development rights. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>Town centre regeneration:</strong> Wood Green town centre is earmarked for significant regeneration, which may affect planning policies for nearby residential properties. We ensure applications comply with the most current Haringey planning policies.",
            "<strong>Loft conversions:</strong> The Edwardian terraces in Wood Green typically have good roof voids suitable for dormer loft conversions. Outside conservation areas, rear dormers can often be built under permitted development. We survey the roof, confirm PD eligibility, and prepare building regulations drawings.",
        ],
        "stats": [
            ("Conservation areas", "Trinity Gardens CA"),
            ("Housing type", "Edwardian terraces"),
            ("Planning authority", "Haringey Council"),
            ("Key postcodes", "N22"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Wood Green?",
                "Yes, loft conversions are popular in N22. Outside conservation areas, rear dormers under permitted development are straightforward for Edwardian terraces. Within conservation areas, planning permission is required. We survey your roof and advise on the best approach.",
            ),
            (
                "What size rear extension is allowed in Wood Green?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Semi-detached houses can extend up to 4 metres (or 6 metres with prior notification). Within conservation areas, planning permission is required. We confirm the maximum for your property.",
            ),
            (
                "How much do architectural drawings cost in Wood Green?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden extras.",
            ),
            (
                "Does the town centre regeneration affect my house?",
                "The regeneration policies primarily affect commercial and larger residential schemes in the town centre. Standard householder applications are generally unaffected. We check whether any area-specific policies apply to your property.",
            ),
            (
                "Can I combine a loft conversion and extension?",
                "Yes, combining projects is often cost-effective. We design integrated schemes where the loft and extension work together. A combined project may need planning permission and will require building regulations approval. We coordinate all submissions.",
            ),
        ],
    },
    {
        "name": "Walthamstow",
        "slug": "walthamstow",
        "borough": "Waltham Forest",
        "borough_slug": "waltham-forest",
        "postcodes": "E17",
        "character": "Walthamstow — nicknamed 'Awesomestow' — is a vibrant east London neighbourhood with Victorian terraces, a village feel, and a creative community. Loft conversions and extensions are in very high demand.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, some 1960s infill",
        "conservation_notes": "Walthamstow Village Conservation Area; St Mary's Church Conservation Area",
        "planning_notes": "Waltham Forest Council has specific design guidance for residential extensions. The Walthamstow Village Conservation Area has strict controls. Outside conservation areas, permitted development rights are available.",
        "nearby": ["tottenham", "wood-green", "hackney-wick", "bow"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Walthamstow's Victorian terraces. MCIAT chartered, fixed fees, Waltham Forest planning expertise built in.",
        "local_context_title": "Why Walthamstow demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Walthamstow sits in the E17 postcode within the London Borough of Waltham Forest, connected to central London by the Victoria Line. The neighbourhood's Victorian terraces, village centre, and creative community have driven a transformation in property values and a corresponding boom in residential extension and conversion projects.",
            "<strong>Victorian terraces:</strong> Walthamstow's housing stock is predominantly Victorian terraces — well-built, well-proportioned houses with slate roofs and rear outriggers. These are prime candidates for dormer loft conversions, rear extensions, and side-return infills. The E17 postcode consistently records some of the highest volumes of householder planning applications in London.",
            "<strong>Walthamstow Village Conservation Area:</strong> The village conservation area protects the historic core around St Mary's Church and Orford Road. Article 4 Directions restrict permitted development rights within this zone. Our MCIAT-chartered team prepares conservation-sensitive applications that satisfy Waltham Forest's heritage officers.",
            "<strong>Loft conversion boom:</strong> Walthamstow has become one of London's busiest boroughs for loft conversions. Outside the conservation area, rear dormers under permitted development are straightforward and can add a bedroom and bathroom without planning permission. We survey the roof structure, confirm PD eligibility, and prepare building regulations drawings.",
            "<strong>Waltham Forest design guidance:</strong> The borough has published detailed design guidance for residential extensions, including requirements for dormer proportions, extension depths, and materials. Our team designs projects that comply with this guidance from the outset.",
        ],
        "stats": [
            ("Conservation areas", "Walthamstow Village CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Waltham Forest Council"),
            ("Key postcodes", "E17"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Walthamstow?",
                "Yes, loft conversions are extremely popular in E17. Outside the Walthamstow Village Conservation Area, rear dormers under permitted development are straightforward. Within the conservation area, planning permission is required. We survey your roof, confirm PD eligibility, and prepare the required drawings.",
            ),
            (
                "What size extension can I build in Walthamstow?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey (or 6 metres with prior notification). Semi-detached houses have similar allowances. Within conservation areas, planning permission is required. We confirm what applies to your property.",
            ),
            (
                "What are the dormer design rules in Waltham Forest?",
                "Waltham Forest expects rear dormers to be set back from the eaves, set in from party walls, and clad in materials matching the existing roof. The dormer should be subordinate to the existing roof form. Front dormers are generally refused on period properties. We design dormers that meet the borough's standards.",
            ),
            (
                "How much do architectural drawings cost in Walthamstow?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees — no hidden charges.",
            ),
            (
                "How long does Waltham Forest take for planning decisions?",
                "Waltham Forest targets 8 weeks for householder applications. The borough processes a high volume of applications but generally meets its targets. Pre-application advice is available and recommended for conservation area projects.",
            ),
        ],
    },
    {
        "name": "Sydenham",
        "slug": "sydenham",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE26",
        "character": "Sydenham is a leafy south-east London neighbourhood in Lewisham, bordering Crystal Palace. Its Victorian and Edwardian terraces offer good value and strong potential for loft conversions and extensions.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, some 1960s infill",
        "conservation_notes": "Sydenham Park Conservation Area; Sydenham Hill / Kirkdale Conservation Area",
        "planning_notes": "Lewisham Council is generally supportive of sympathetic residential extensions. Conservation areas have Article 4 Directions. The Crystal Palace border area has additional design sensitivity.",
        "nearby": ["forest-hill", "dulwich", "blackheath", "peckham"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Sydenham's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why Sydenham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Sydenham sits in the SE26 postcode within the London Borough of Lewisham, bordering Crystal Palace to the south and Forest Hill to the west. Its mix of Victorian and Edwardian terraces, relatively affordable compared to neighbouring areas, attracts families who invest in loft conversions and extensions.",
            "<strong>Victorian and Edwardian housing:</strong> Sydenham's residential streets contain well-proportioned Victorian and Edwardian terraces ideal for loft conversions and rear extensions. Many properties have good roof voids and generous gardens, offering scope for both upward and rearward expansion.",
            "<strong>Conservation areas:</strong> The Sydenham Park Conservation Area and parts of the Sydenham Hill / Kirkdale Conservation Area protect the neighbourhood's finest streets. Article 4 Directions restrict permitted development rights. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>Crystal Palace influence:</strong> Properties near the Crystal Palace border sit in an area of particular design sensitivity. The historic significance of the Crystal Palace site and its surrounding parkland influence planning decisions for nearby properties.",
            "<strong>Value-driven extensions:</strong> Sydenham offers some of the best value for period housing in inner London, making extension and conversion projects particularly worthwhile. Our fixed-fee pricing ensures professional architectural drawings are accessible.",
        ],
        "stats": [
            ("Conservation areas", "Sydenham Park CA"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE26"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Sydenham?",
                "Yes, loft conversions are popular in SE26. Outside conservation areas, rear dormers under permitted development are straightforward. Within conservation areas, planning permission is required. We survey your roof and confirm the best approach.",
            ),
            (
                "What size extension can I build in Sydenham?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Larger extensions are possible with planning permission. Within conservation areas, planning permission is required for most extensions. We confirm the maximum achievable for your property.",
            ),
            (
                "How much do architectural drawings cost in Sydenham?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "Are there special rules near Crystal Palace?",
                "Properties near the Crystal Palace border may face additional design scrutiny due to the area's historical significance. Lewisham Council expects high-quality design that respects the character of the Crystal Palace area. We ensure designs meet these expectations.",
            ),
            (
                "How long does Lewisham take for planning decisions?",
                "Lewisham targets 8 weeks for householder applications. Conservation area applications may take slightly longer. Pre-application advice is available and recommended for complex projects.",
            ),
        ],
    },
    {
        "name": "Forest Hill",
        "slug": "forest-hill",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE23",
        "character": "Forest Hill is a leafy residential neighbourhood in Lewisham with Victorian terraces, the Horniman Museum, and a village-like atmosphere. Extensions and loft conversions are the main project types.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war housing",
        "conservation_notes": "Forest Hill Conservation Area covers parts of the neighbourhood",
        "planning_notes": "Lewisham Council applies standard design guidance for residential extensions. Conservation area coverage is limited compared to neighbouring areas. Permitted development rights are available for most properties.",
        "nearby": ["sydenham", "dulwich", "peckham", "herne-hill"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Forest Hill's Victorian terraces. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why Forest Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Forest Hill sits in the SE23 postcode within the London Borough of Lewisham, positioned between Dulwich, Sydenham, and Brockley. Its attractive Victorian terraces, family-friendly atmosphere, and proximity to the Horniman Museum and gardens make it a sought-after neighbourhood where homeowners regularly invest in extensions and conversions.",
            "<strong>Victorian terraces:</strong> Forest Hill's housing stock is predominantly Victorian terraces in a range of sizes. These properties are well suited to dormer loft conversions, rear extensions, and side-return infills. The area's relatively generous plot sizes offer good extension potential.",
            "<strong>Forest Hill Conservation Area:</strong> The conservation area covers parts of the neighbourhood, protecting the most architecturally significant streets. Within this zone, planning permission and Heritage Statements are required for external works. Outside the conservation area, permitted development rights are available for most standard projects.",
            "<strong>Hillside topography:</strong> Forest Hill's sloping terrain means that some properties have complex level changes that influence extension design. We produce accurate topographic surveys and design schemes that work with the existing levels, minimising excavation and retaining-wall costs.",
            "<strong>Loft conversions:</strong> Victorian terraces in Forest Hill typically have good roof voids for dormer conversions. Outside the conservation area, rear dormers under permitted development are straightforward. We survey the roof structure and prepare building regulations drawings for Building Control.",
        ],
        "stats": [
            ("Conservation areas", "Forest Hill CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE23"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Forest Hill?",
                "Yes, loft conversions are very popular in SE23. Outside the conservation area, rear dormers under permitted development are straightforward. Within the conservation area, planning permission is required. We survey your roof and confirm the best approach.",
            ),
            (
                "What size extension can I build in Forest Hill?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Semi-detached houses can extend further. Within the conservation area, planning permission is typically required. We confirm the maximum achievable for your property.",
            ),
            (
                "Does the hillside terrain affect my extension design?",
                "Yes, Forest Hill's sloping terrain can complicate extension design, particularly regarding foundations, level changes, and drainage. We produce accurate surveys and design schemes that work with the existing topography, minimising cost and construction complexity.",
            ),
            (
                "How much do architectural drawings cost in Forest Hill?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "Can I combine a loft conversion and extension?",
                "Yes, combining a loft and extension project is often cost-effective. We design integrated schemes and submit coordinated applications. This is our most common project type in Forest Hill.",
            ),
        ],
    },
    {
        "name": "East Dulwich",
        "slug": "east-dulwich",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE22",
        "character": "East Dulwich has a strong village feel with independent shops, a popular market, and streets of Victorian terraces. It is one of south-east London's most family-friendly neighbourhoods.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war housing",
        "conservation_notes": "East Dulwich Estate Conservation Area; parts of Goose Green Conservation Area",
        "planning_notes": "Southwark Council applies standard design guidance for residential extensions. Conservation area coverage is moderate. The village centre has specific policies protecting its retail character.",
        "nearby": ["dulwich", "peckham", "herne-hill", "bermondsey"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for East Dulwich's Victorian terraces. MCIAT chartered, fixed fees, Southwark planning expertise built in.",
        "local_context_title": "Why East Dulwich demands specialist architectural drawings",
        "local_context_paragraphs": [
            "East Dulwich sits in the SE22 postcode within the London Borough of Southwark, positioned between Dulwich Village and Peckham. Its attractive Victorian terraces, independent shops along Lordship Lane, and strong community feel make it one of south-east London's most sought-after family neighbourhoods — and one of its busiest for residential planning applications.",
            "<strong>Victorian terraces:</strong> East Dulwich's housing is predominantly Victorian terraces, ranging from compact two-bedroom cottages to substantial four-bedroom family houses. These properties are ideal candidates for dormer loft conversions, rear extensions, and side-return infills. The area's consistent terrace patterns mean standard design approaches can be adapted efficiently.",
            "<strong>Conservation areas:</strong> The East Dulwich Estate Conservation Area and parts of the Goose Green Conservation Area protect key streets. Within these zones, planning permission and Heritage Statements are required for external works. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Family-driven demand:</strong> East Dulwich's family demographic drives consistent demand for extra bedrooms (via loft conversions) and open-plan kitchen-dining spaces (via rear extensions). Many projects combine both to maximise the transformation within a single build programme.",
            "<strong>Southwark design standards:</strong> Southwark Council applies specific design guidance for residential extensions, including requirements for dormer proportions, extension depths, and materials. We design projects that comply with this guidance from the outset.",
        ],
        "stats": [
            ("Conservation areas", "East Dulwich Estate CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE22"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in East Dulwich?",
                "Yes, loft conversions are extremely popular in SE22. Outside conservation areas, rear dormers under permitted development are straightforward. Within conservation areas, planning permission is required. We survey your roof and confirm the best approach.",
            ),
            (
                "What size extension can I build in East Dulwich?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Southwark has specific design guidance on extension proportions and materials. Within conservation areas, planning permission is required. We confirm what applies to your property.",
            ),
            (
                "How much do architectural drawings cost in East Dulwich?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. This is our most popular package in East Dulwich.",
            ),
            (
                "Can I combine a loft and extension in one project?",
                "Yes, combined loft-and-extension projects are our most common project type in East Dulwich. We design integrated schemes and coordinate all planning and building regulations submissions.",
            ),
            (
                "How long does Southwark take for planning decisions?",
                "Southwark targets 8 weeks for householder applications. Conservation area applications may take slightly longer. Pre-application advice is available. We manage the timeline and handle all council correspondence.",
            ),
        ],
    },
    {
        "name": "Earlsfield",
        "slug": "earlsfield",
        "borough": "Wandsworth",
        "borough_slug": "wandsworth",
        "postcodes": "SW18",
        "character": "Earlsfield is a quiet, residential neighbourhood in Wandsworth with Victorian and Edwardian terraces. Its proximity to Wandsworth Common and excellent schools make it popular with families.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war semis",
        "conservation_notes": "Wandsworth Common Conservation Area borders the neighbourhood",
        "planning_notes": "Wandsworth Council is generally supportive of sympathetic residential extensions. Permitted development rights are available outside conservation areas. Properties near Wandsworth Common may face additional design scrutiny.",
        "nearby": ["tooting", "balham", "putney", "wimbledon"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and building regulations for Earlsfield's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Wandsworth planning expertise built in.",
        "local_context_title": "Why Earlsfield demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Earlsfield sits in the SW18 postcode within the London Borough of Wandsworth, positioned between Wandsworth Common and Tooting. Its quiet, tree-lined streets of Victorian and Edwardian terraces make it one of south-west London's most popular family neighbourhoods, with consistently high demand for loft conversions and extensions.",
            "<strong>Victorian and Edwardian terraces:</strong> Earlsfield's housing stock is predominantly well-proportioned Victorian and Edwardian terraces, many with original period features. These properties offer good potential for dormer loft conversions, rear extensions, and side-return infills.",
            "<strong>Wandsworth Common proximity:</strong> Properties near Wandsworth Common may face additional design scrutiny. The Wandsworth Common Conservation Area borders the neighbourhood, and Wandsworth Council protects views and the character of Common-facing streets.",
            "<strong>Loft conversions:</strong> Rear dormers are the most popular project type in Earlsfield. Outside conservation areas, many can be built under permitted development. Wandsworth Council is generally supportive of well-designed dormers that use matching materials.",
            "<strong>Family-oriented extensions:</strong> Rear extensions to create open-plan kitchen-dining-living spaces are in constant demand. Under permitted development, terraced houses can extend up to 4 metres at single storey. We design extensions that maximise the ground-floor transformation.",
        ],
        "stats": [
            ("Nearby conservation", "Wandsworth Common CA"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Wandsworth Council"),
            ("Key postcodes", "SW18"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Earlsfield?",
                "Yes, loft conversions are the most popular project type in Earlsfield. Outside conservation areas, rear dormers under permitted development are straightforward. Near Wandsworth Common, additional design care may be needed. We survey your roof and advise on the best approach.",
            ),
            (
                "What size extension can I build in Earlsfield?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Semi-detached houses have slightly greater allowances. We confirm the maximum achievable for your property and design to that envelope.",
            ),
            (
                "Are there extra rules near Wandsworth Common?",
                "Properties within or adjacent to the Wandsworth Common Conservation Area may face additional design requirements. Planning permission may be needed for works that would otherwise be permitted development. We check your property's status at the outset.",
            ),
            (
                "How much do architectural drawings cost in Earlsfield?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Wandsworth take for planning decisions?",
                "Wandsworth targets 8 weeks for householder applications. The borough generally meets its targets. Pre-application advice is available for complex projects.",
            ),
        ],
    },
    {
        "name": "Putney",
        "slug": "putney",
        "borough": "Wandsworth",
        "borough_slug": "wandsworth",
        "postcodes": "SW15",
        "character": "Putney is a riverside neighbourhood in Wandsworth with large Victorian and Edwardian houses, a strong family community, and excellent green spaces. Extensions and loft conversions are popular on the area's spacious period properties.",
        "housing_stock": "Large Victorian houses, Edwardian villas, mansion flats, riverside apartments",
        "conservation_notes": "Putney Conservation Area; Oxford Road Conservation Area",
        "planning_notes": "Wandsworth Council applies high design standards in Putney's conservation areas. Riverside properties may require flood risk assessments. The area's large houses and generous plots offer significant extension potential.",
        "nearby": ["barnes", "earlsfield", "wimbledon", "fulham"],
        "popular_services": ["house-extensions", "loft-conversions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and heritage-sensitive design for Putney's large Victorian and Edwardian houses. MCIAT chartered, fixed fees, Wandsworth planning expertise built in.",
        "local_context_title": "Why Putney demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Putney sits in the SW15 postcode within the London Borough of Wandsworth, positioned on the south bank of the Thames between Putney Bridge and Roehampton. Its large Victorian and Edwardian houses, leafy streets, and proximity to Putney Heath and Wimbledon Common make it one of south-west London's most desirable residential areas.",
            "<strong>Large houses and extension potential:</strong> Putney's housing stock includes many large detached and semi-detached Victorian and Edwardian houses with generous gardens. These properties offer significant potential for rear and side extensions, basement additions (subject to Wandsworth's policies), and substantial loft conversions.",
            "<strong>Conservation areas:</strong> The Putney Conservation Area and Oxford Road Conservation Area protect key streets. Article 4 Directions require planning permission for most external alterations within these zones. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>Riverside properties:</strong> Properties near the Thames may require flood risk assessments. Wandsworth Council also protects riverside views and character through specific planning policies.",
            "<strong>Wandsworth design standards:</strong> Wandsworth Council applies careful design standards in Putney, particularly within conservation areas. Extensions must be subordinate to the original building and use complementary materials. Our team designs extensions that meet these requirements.",
        ],
        "stats": [
            ("Conservation areas", "Putney CA"),
            ("Housing type", "Large Victorian/Edwardian"),
            ("Planning authority", "Wandsworth Council"),
            ("Key postcodes", "SW15"),
        ],
        "faqs": [
            (
                "Can I extend my Putney house?",
                "Yes, Putney's large houses offer excellent extension potential. Outside conservation areas, permitted development allows substantial single-storey rear extensions. Within conservation areas, planning permission is required. We design schemes that maximise space within policy constraints.",
            ),
            (
                "Can I build a loft conversion in Putney?",
                "Yes, Putney's large Victorian and Edwardian houses often have generous roof spaces. Rear dormers, hip-to-gable conversions, and mansard extensions are all achievable with the right design. Conservation area properties need planning permission. We advise on the best approach.",
            ),
            (
                "Is a flood risk assessment needed for my Putney property?",
                "If your property is near the Thames in a designated flood zone, a Flood Risk Assessment will be required with your planning application. We incorporate flood risk requirements from the outset.",
            ),
            (
                "How much do architectural drawings cost in Putney?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Bespoke packages for large houses and listed buildings are priced individually.",
            ),
            (
                "What conservation area rules apply in Putney?",
                "The Putney Conservation Area requires planning permission for most external works. Heritage Statements accompany applications. Wandsworth Council expects designs that respect the area's Victorian and Edwardian character. We prepare compliant applications.",
            ),
        ],
    },
    {
        "name": "Barnes",
        "slug": "barnes",
        "borough": "Richmond upon Thames",
        "borough_slug": "richmond-upon-thames",
        "postcodes": "SW13",
        "character": "Barnes is a village-like Thames-side neighbourhood in Richmond upon Thames with strong conservation area protection, period housing, and a close-knit community. Heritage-sensitive design is essential for almost all projects.",
        "housing_stock": "Victorian cottages, Edwardian houses, riverside properties, some larger detached",
        "conservation_notes": "Barnes Conservation Area covers most of the village and surrounding streets",
        "planning_notes": "Richmond Council applies very strict design controls in Barnes. The Barnes Conservation Area and Article 4 Directions mean most external works require planning permission. The council expects high-quality design that respects the village character.",
        "nearby": ["putney", "richmond", "twickenham", "chiswick"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and loft conversions for Barnes's conservation-area properties. MCIAT chartered, fixed fees, Richmond Council expertise built in.",
        "local_context_title": "Why Barnes demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Barnes sits in the SW13 postcode within the London Borough of Richmond upon Thames, occupying a distinctive meander of the Thames. Its village atmosphere, historic housing, and extensive conservation area coverage make professional architectural guidance essential for virtually any building project.",
            "<strong>Barnes Conservation Area:</strong> The conservation area covers most of the village and surrounding residential streets, protecting the area's distinctive character. Article 4 Directions remove most permitted development rights, meaning planning permission is required for roof alterations, window replacements, extensions, and even front boundary changes. Heritage Statements must accompany all applications.",
            "<strong>Village character:</strong> Barnes has a carefully preserved village character with a mix of Victorian cottages, Edwardian houses, and larger riverside properties. Richmond Council expects all new work to respect this character, using materials and proportions that complement the existing streetscape.",
            "<strong>Riverside properties:</strong> Thames-side properties in Barnes may require flood risk assessments, and the council protects riverside views and character through specific planning policies. We incorporate these requirements into applications from the outset.",
            "<strong>Richmond Council design standards:</strong> Richmond Council maintains some of London's highest design standards. Extensions must be subordinate to the original building, use matching or complementary materials, and maintain the village character. Our MCIAT-chartered team is experienced in meeting these exacting standards.",
        ],
        "stats": [
            ("Conservation areas", "Barnes CA"),
            ("Housing type", "Victorian cottages, Edwardian"),
            ("Planning authority", "Richmond Council"),
            ("Key postcodes", "SW13"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Barnes?",
                "Almost certainly yes. The Barnes Conservation Area and Article 4 Directions remove most permitted development rights. Even replacement windows and minor external alterations typically require planning permission with a Heritage Statement. Our team specialises in Barnes conservation-area applications.",
            ),
            (
                "Can I extend my house in Barnes?",
                "Extensions are achievable but require planning permission within the conservation area. Richmond Council expects designs that are subordinate to the original building and respect the village character. We design extensions that meet these standards and submit the necessary applications.",
            ),
            (
                "What are the design requirements in Barnes?",
                "Richmond Council expects high-quality design using materials that match or complement the existing building. Extensions should be subordinate in scale, roof pitch should respond to the original, and the impact on neighbours must be considered. Our MCIAT-chartered team designs to these standards.",
            ),
            (
                "How much do architectural drawings cost in Barnes?",
                "Our Essentials package starts from £840. Given Barnes's conservation area coverage, most projects require the Complete or Bespoke package. The Complete from £1,750 includes planning, building regulations, and structural calculations.",
            ),
            (
                "Can I build a loft conversion in Barnes?",
                "Loft conversions are achievable but require planning permission within the conservation area. Richmond Council has specific requirements for dormer design, materials, and proportions. We design dormers that satisfy the council's heritage officers.",
            ),
        ],
    },
    {
        "name": "Maida Vale",
        "slug": "maida-vale",
        "borough": "Westminster",
        "borough_slug": "westminster",
        "postcodes": "W9",
        "character": "Maida Vale is an elegant residential neighbourhood in Westminster known for its mansion blocks, stucco terraces, and canal-side Little Venice. Heritage-sensitive design is required for most projects.",
        "housing_stock": "Mansion blocks, stucco terraces, canal-side properties, converted flats",
        "conservation_notes": "Maida Vale Conservation Area covers most of the neighbourhood",
        "planning_notes": "Westminster Council applies strict heritage controls. The Maida Vale Conservation Area covers most properties, and Article 4 Directions are extensive. Many buildings are listed. Westminster's design standards are among the highest in London.",
        "nearby": ["kilburn", "queens-park", "notting-hill"],
        "popular_services": ["planning-drawings", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, heritage-sensitive alterations, and building regulations for Maida Vale's mansion blocks and stucco terraces. MCIAT chartered, fixed fees, Westminster planning expertise built in.",
        "local_context_title": "Why Maida Vale demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Maida Vale sits in the W9 postcode within the City of Westminster, one of London's most heritage-sensitive planning authorities. Its grand mansion blocks, stucco-fronted terraces, and canal-side setting create an architecturally distinguished neighbourhood where every project demands careful design and detailed planning applications.",
            "<strong>Maida Vale Conservation Area:</strong> The conservation area covers most of the neighbourhood, protecting the Victorian and Edwardian streetscape. Article 4 Directions remove most permitted development rights. Planning permission and Heritage Statements are required for external alterations, and Westminster's conservation officers maintain exacting standards.",
            "<strong>Mansion blocks:</strong> Maida Vale contains many significant mansion block developments. Alterations to individual flats — window replacements, reconfiguration, bathroom/kitchen refits — may require planning permission (within the conservation area), Building Regulations approval, and freeholder consent. Our team handles the architectural drawings for all three processes.",
            "<strong>Listed buildings:</strong> Several buildings in Maida Vale are individually listed, requiring Listed Building Consent for both internal and external works. Westminster Council expects detailed drawings with full material specifications and Heritage Impact Assessments.",
            "<strong>Little Venice canal-side:</strong> Properties near the canal in Little Venice face additional design scrutiny. Westminster Council protects the canal-side character and requires developments to maintain the area's distinctive setting.",
        ],
        "stats": [
            ("Conservation areas", "Maida Vale CA"),
            ("Housing type", "Mansion blocks, stucco terraces"),
            ("Planning authority", "Westminster Council"),
            ("Key postcodes", "W9"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Maida Vale?",
                "Almost certainly yes for external works. The Maida Vale Conservation Area and Article 4 Directions mean that most alterations require planning permission. Even internal works to listed buildings need Listed Building Consent. Our team navigates Westminster's requirements on your behalf.",
            ),
            (
                "Can I alter my mansion block flat in Maida Vale?",
                "Internal alterations generally don't need planning permission but may require Building Regulations approval and freeholder consent. External changes — windows, balconies, facade alterations — almost always need planning permission within the conservation area. We handle all three processes.",
            ),
            (
                "What does Listed Building Consent involve?",
                "Listed Building Consent is required for any works affecting the character of a listed building. Westminster expects detailed drawings, Heritage Impact Assessments, and material schedules. The application runs alongside planning permission where both are needed. Our team prepares both applications concurrently.",
            ),
            (
                "How much do architectural drawings cost in Maida Vale?",
                "Our Essentials package starts from £840. Given Maida Vale's heritage constraints, most projects require the Complete (from £1,750) or Bespoke package. We provide fixed-fee quotes tailored to the complexity of each project.",
            ),
            (
                "How long does Westminster take for planning decisions?",
                "Westminster targets 8 weeks for householder applications but conservation area and listed building applications often take longer. The council's design and heritage officers maintain very high standards. Pre-application advice is strongly recommended for complex projects.",
            ),
        ],
    },
    {
        "name": "Hackney Wick",
        "slug": "hackney-wick",
        "borough": "Hackney",
        "borough_slug": "hackney",
        "postcodes": "E9",
        "character": "Hackney Wick is a canal-side creative quarter in Hackney with warehouse conversions, artists' studios, and new-build developments clustered around the Queen Elizabeth Olympic Park.",
        "housing_stock": "Warehouse conversions, new-build apartments, Victorian terraces, canal-side buildings",
        "conservation_notes": "Fish Island and White Post Lane Conservation Area",
        "planning_notes": "Hackney Council supports creative and mixed-use development. The LLDC (London Legacy Development Corporation) managed planning for the Olympic Park area until 2024; Hackney Council now manages most applications. Warehouse conversions may require change-of-use applications.",
        "nearby": ["bow", "shoreditch", "bethnal-green", "walthamstow"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, warehouse conversions, loft extensions, and building regulations for Hackney Wick's creative quarter. MCIAT chartered, fixed fees, Hackney planning expertise built in.",
        "local_context_title": "Why Hackney Wick demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Hackney Wick sits in the E9 postcode within the London Borough of Hackney, centred on the canal network and Queen Elizabeth Olympic Park. The neighbourhood's mix of converted warehouses, artists' studios, new-build developments, and remaining Victorian terraces creates a complex planning landscape.",
            "<strong>Warehouse conversions:</strong> Hackney Wick's industrial heritage — print works, furniture factories, and canal-side workshops — has produced a distinctive creative quarter where warehouse conversions to residential and live-work use are the most common project type. These require change-of-use applications, structural assessments, and building regulations compliance.",
            "<strong>Fish Island Conservation Area:</strong> The Fish Island and White Post Lane Conservation Area protects the area's industrial character. Within this zone, external alterations and change-of-use applications require Heritage Statements demonstrating how proposals respond to the area's industrial significance.",
            "<strong>Canal-side development:</strong> Properties adjacent to the Lee Navigation may require Environment Agency consultation. Hackney Council also applies specific policies protecting the canal-side character and encouraging public access to the waterway.",
            "<strong>Planning authority:</strong> Hackney Council manages most planning applications in Hackney Wick. The London Legacy Development Corporation previously had planning powers for areas near the Olympic Park, but these have transitioned to the local boroughs. We ensure applications are submitted to the correct authority.",
        ],
        "stats": [
            ("Conservation areas", "Fish Island CA"),
            ("Housing type", "Warehouses, new-build"),
            ("Planning authority", "Hackney Council"),
            ("Key postcodes", "E9"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a warehouse conversion in Hackney Wick?",
                "Usually yes. Converting industrial or commercial space to residential requires planning permission, particularly within the Fish Island Conservation Area. Permitted development rights under Class MA may apply in limited cases. Our team assesses your property and manages the application.",
            ),
            (
                "Who handles planning in Hackney Wick?",
                "Hackney Council manages most planning applications in Hackney Wick. Some areas near the Olympic Park were previously managed by the LLDC. We confirm the correct authority and submit to the right council.",
            ),
            (
                "Are there special rules for canal-side properties?",
                "Yes, canal-side properties may require Environment Agency consultation. Hackney Council applies specific policies on waterside development, including maintaining public access and protecting the canal's character. We incorporate these requirements into applications.",
            ),
            (
                "How much do architectural drawings cost in Hackney Wick?",
                "Our Essentials package starts from £840. Warehouse conversions are typically quoted on a bespoke basis reflecting their complexity. The Complete package from £1,750 covers standard residential projects.",
            ),
            (
                "Can I build a loft conversion in Hackney Wick?",
                "Loft conversions on Victorian terraces in Hackney Wick are straightforward outside conservation areas. For warehouse buildings, roof extensions depend on structural capacity and planning constraints. We assess feasibility and advise on the best approach.",
            ),
        ],
    },
    {
        "name": "Queens Park",
        "slug": "queens-park",
        "borough": "Brent",
        "borough_slug": "brent",
        "postcodes": "NW6, NW10",
        "character": "Queens Park is a desirable residential neighbourhood in Brent with Victorian terraces, a conservation area, and a family-friendly atmosphere centred on the park. Extensions and loft conversions are the main project types.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war semis",
        "conservation_notes": "Queens Park Estate Conservation Area covers the distinctive grid of terraces",
        "planning_notes": "Brent Council applies specific controls within the Queens Park Conservation Area. Article 4 Directions may restrict permitted development rights. Outside the conservation area, standard PD rights are available.",
        "nearby": ["kilburn", "maida-vale", "wembley"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Queens Park's Victorian terraces. MCIAT chartered, fixed fees, Brent planning expertise built in.",
        "local_context_title": "Why Queens Park demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Queens Park sits in the NW6 and NW10 postcodes within the London Borough of Brent, centred on the attractive park and the distinctive grid of Victorian terraces that surrounds it. Its family-friendly atmosphere, village feel, and excellent transport connections make it one of north-west London's most desirable neighbourhoods.",
            "<strong>Queens Park Conservation Area:</strong> The Queens Park Estate Conservation Area covers the distinctive grid of Victorian terraces built in the 1880s and 1890s. These houses have a consistent architectural character — red brick, bay windows, decorative tile paths — that Brent Council is determined to protect. Article 4 Directions may restrict permitted development rights within the conservation area.",
            "<strong>Victorian terraces:</strong> Queens Park's terraces are well proportioned with good roof voids for loft conversions and adequate garden depths for rear extensions. Outside the conservation area, rear dormers and single-storey rear extensions can often proceed under permitted development.",
            "<strong>Conservation-sensitive design:</strong> Within the conservation area, Brent Council requires Heritage Statements and expects designs that respect the Victorian character. Dormer design, material choices, and window proportions are all scrutinised. Our MCIAT-chartered team prepares applications that meet these standards.",
            "<strong>Loft conversions:</strong> Rear dormers are the most popular project type in Queens Park. Within the conservation area, dormers must use matching materials and be subordinate to the existing roof. Outside the conservation area, permitted development offers a simpler route. We advise on the best approach for each property.",
        ],
        "stats": [
            ("Conservation areas", "Queens Park Estate CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Brent Council"),
            ("Key postcodes", "NW6, NW10"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Queens Park Conservation Area?",
                "For most external works, yes. The Queens Park Conservation Area protects the Victorian character of the estate. Article 4 Directions may require planning permission for roof alterations, window replacements, and front boundary changes. Our team checks your property's status and advises on requirements.",
            ),
            (
                "Can I build a loft conversion in Queens Park?",
                "Yes, loft conversions are popular in Queens Park. Outside the conservation area, rear dormers under permitted development are straightforward. Within the conservation area, planning permission may be required and dormers must use matching materials. We survey your roof and advise on the best approach.",
            ),
            (
                "What size extension can I build in Queens Park?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey outside the conservation area. Within the conservation area, planning permission is usually required. We confirm the maximum achievable for your specific property.",
            ),
            (
                "How much do architectural drawings cost in Queens Park?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning, building regulations, and structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "How long does Brent take for planning decisions?",
                "Brent targets 8 weeks for householder applications. Conservation area applications may take slightly longer. Pre-application advice is available and recommended for properties within the conservation area.",
            ),
        ],
    },
    # ------------------------------------------------------------------
    # 30 additional neighbourhoods (batch 2)
    # ------------------------------------------------------------------
    {
        "name": "Canary Wharf",
        "slug": "canary-wharf",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E14",
        "character": "Canary Wharf is London's second financial district, defined by modern high-rise towers, riverside apartment complexes, and ongoing regeneration across the Isle of Dogs. Residential projects here typically involve fit-out reconfiguration, balcony enclosures, and building-regulations compliance for new-build apartments.",
        "housing_stock": "Modern high-rise apartments, riverside new-builds, converted Docklands warehouses, some Victorian terraces on the fringes",
        "conservation_notes": "Coldharbour Conservation Area preserves remnants of the original Docklands village",
        "planning_notes": "Tower Hamlets Council applies Isle of Dogs policies that encourage high-density residential development. Many apartment alterations are covered by freeholder consent and Building Regulations rather than planning permission. Tall building proposals near heritage assets trigger a design review.",
        "nearby": ["bermondsey", "bow", "bethnal-green", "deptford"],
        "popular_services": ["building-regulations", "planning-drawings", "house-extensions"],
        "hero_lede": "Architectural drawings for Canary Wharf apartments — building regulations, interior reconfiguration, and planning submissions for riverside living in E14. MCIAT chartered, fixed fees, Tower Hamlets expertise built in.",
        "local_context_title": "Why Canary Wharf demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Canary Wharf dominates the Isle of Dogs in the E14 postcode, within the London Borough of Tower Hamlets. What was once the world's busiest port is now one of London's densest residential and commercial districts, with modern apartment towers overlooking the Thames and the old dock basins.",
            "<strong>Modern apartment fit-outs:</strong> Most residential projects in Canary Wharf involve reconfiguring open-plan apartments — adding bedrooms, relocating kitchens, or enclosing balconies. These works require Building Regulations approval (particularly Part B fire safety and Part E acoustics) and usually freeholder consent, even where planning permission is not needed. Our team prepares compliant drawing packages that satisfy both Building Control and managing agents.",
            "<strong>Docklands warehouse conversions:</strong> On the fringes of the estate, converted Docklands warehouses and older buildings offer opportunities for more substantial projects. Change-of-use applications, mezzanine insertions, and roof extensions on these buildings require careful navigation of Tower Hamlets' planning policies and potential heritage constraints.",
            "<strong>Coldharbour Conservation Area:</strong> The Coldharbour Conservation Area preserves the remnants of the original Docklands village, including historic pubs and dock workers' cottages. Works within this zone require Heritage Statements and sympathetic design. Our MCIAT-chartered team prepares applications that respect this unique industrial heritage.",
            "<strong>Riverside and flood-risk considerations:</strong> Many E14 properties fall within flood-risk zones. Planning applications and Building Regulations submissions must address flood resilience, and Environment Agency consultation may be required. We include flood risk assessments where needed.",
        ],
        "stats": [
            ("Conservation areas", "Coldharbour CA"),
            ("Housing type", "Modern high-rise apartments"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E14"),
        ],
        "faqs": [
            (
                "Do I need planning permission to reconfigure my Canary Wharf apartment?",
                "Internal alterations to apartments generally do not require planning permission but do need Building Regulations approval, especially for structural changes, new bathrooms, and kitchen relocations. You will also need freeholder consent under the terms of your lease. We prepare the drawings for all required approvals.",
            ),
            (
                "Can I enclose a balcony in Canary Wharf?",
                "Enclosing a balcony typically requires both planning permission from Tower Hamlets Council and freeholder consent. The council will assess the impact on the building's external appearance and may require a design review. We prepare applications that address these concerns.",
            ),
            (
                "What building regulations apply to apartment fit-outs in E14?",
                "Key regulations include Part B (fire safety — critical in high-rise buildings), Part E (sound insulation between units), Part F (ventilation), and Part L (energy efficiency). Post-Grenfell fire safety requirements are particularly relevant for buildings over 18 metres. We ensure full compliance in our drawing packages.",
            ),
            (
                "How much do architectural drawings cost in Canary Wharf?",
                "Our Essentials package starts from £840 for a single submission. Apartment reconfiguration projects typically fall within our Complete package from £1,750. Complex high-rise schemes are priced individually following an initial consultation.",
            ),
            (
                "Are there flood risk considerations for E14 properties?",
                "Yes, many properties in E14 are within Environment Agency flood zones. Planning applications must include a Flood Risk Assessment, and Building Regulations submissions should address flood resilience measures. We incorporate these requirements into our drawing packages.",
            ),
        ],
    },
    {
        "name": "Mile End",
        "slug": "mile-end",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E1, E3",
        "character": "Mile End is a diverse east London neighbourhood centred on the Regent's Canal and Mile End Park. Its streets of Victorian terraces sit alongside post-war estates and new-build developments near Queen Mary University.",
        "housing_stock": "Victorian terraces, Edwardian houses, post-war council estates, canal-side new-builds",
        "conservation_notes": "Tredegar Square Conservation Area; Clinton Road Conservation Area",
        "planning_notes": "Tower Hamlets Council supports sensitive densification. Victorian terraces are prime candidates for loft conversions and rear extensions. Properties near the canal may require Environment Agency consultation.",
        "nearby": ["bow", "bethnal-green", "canary-wharf", "shoreditch"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and rear extensions for Mile End's Victorian terraces and canal-side properties. MCIAT chartered, fixed fees, Tower Hamlets expertise built in.",
        "local_context_title": "Why Mile End demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Mile End straddles the E1 and E3 postcodes in the London Borough of Tower Hamlets, centred on Mile End Road and the green corridor of Mile End Park. The neighbourhood's Victorian terraces — many well-proportioned with generous roof voids — are among the most popular in east London for loft conversions and rear extensions.",
            "<strong>Victorian terraces:</strong> Mile End's two- and three-storey terraces offer excellent potential for dormer loft conversions and single-storey rear extensions. Outside conservation areas, rear dormers under permitted development are straightforward. We survey existing roof structures and confirm PD eligibility before committing to a design.",
            "<strong>Tredegar Square Conservation Area:</strong> This conservation area covers one of east London's finest Georgian squares and its surrounding streets. Article 4 Directions restrict external alterations, and Tower Hamlets Council requires Heritage Statements for visible changes. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Canal-side properties:</strong> Properties along the Regent's Canal may require Environment Agency consultation for works affecting flood risk or waterway access. We include flood risk assessments where needed and coordinate with relevant authorities.",
            "<strong>Post-war estate improvements:</strong> Mile End contains several significant post-war housing estates where leaseholders seek to improve individual flats. These projects require coordination between Tower Hamlets Council, the housing association, and Building Control.",
        ],
        "stats": [
            ("Conservation areas", "Tredegar Square CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E1, E3"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Mile End?",
                "Yes, loft conversions are very popular in Mile End. Victorian terraces outside conservation areas can typically add rear dormers under permitted development. Within the Tredegar Square Conservation Area, planning permission is required. We survey your roof and advise on the best approach.",
            ),
            (
                "What size rear extension can I build in Mile End?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey without planning permission, subject to prior notification. Larger extensions or those within conservation areas require full planning permission. We confirm what is achievable for your property.",
            ),
            (
                "Are there special rules for canal-side properties in Mile End?",
                "Yes, properties near the Regent's Canal may fall within flood-risk zones and require Environment Agency consultation. Tower Hamlets Council also applies specific policies on waterside development. We incorporate these requirements into applications.",
            ),
            (
                "How long does Tower Hamlets take for planning decisions?",
                "Tower Hamlets Council targets 8 weeks for householder applications. Conservation area applications may take longer due to heritage officer review. Pre-application advice is available and recommended for complex projects.",
            ),
            (
                "How much do architectural drawings cost in Mile End?",
                "Our Essentials package starts from £840 for a single submission. The Complete package from £1,750 covers both planning and building regulations. Fixed fees with no hidden charges.",
            ),
        ],
    },
    {
        "name": "Stamford Hill",
        "slug": "stamford-hill",
        "borough": "Hackney",
        "borough_slug": "hackney",
        "postcodes": "N16",
        "character": "Stamford Hill is a distinctive north Hackney neighbourhood with a large Orthodox Jewish community. Its streets of substantial Victorian and Edwardian terraces see consistent demand for extensions, loft conversions, and internal reconfigurations to accommodate larger families.",
        "housing_stock": "Large Victorian terraces, Edwardian houses, some inter-war semis, converted flats",
        "conservation_notes": "Clapton Common Conservation Area overlaps parts of the area",
        "planning_notes": "Hackney Council applies standard policies but recognises the area's distinctive community character. Many properties have already been extended or subdivided, and further works must comply with current building regulations. Applications for HMO conversions are common.",
        "nearby": ["stoke-newington", "tottenham", "finsbury-park", "dalston"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and building regulations for Stamford Hill's large Victorian terraces. MCIAT chartered, fixed fees, Hackney planning expertise built in.",
        "local_context_title": "Why Stamford Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Stamford Hill occupies the N16 postcode in the northern part of the London Borough of Hackney. The neighbourhood's substantial Victorian and Edwardian terraces — many originally built as large family homes — continue to serve that purpose today, driving consistent demand for extensions, loft conversions, and internal reconfigurations.",
            "<strong>Large family homes:</strong> Stamford Hill's terraces are among the most generously proportioned in Hackney, with many properties retaining original large room sizes. Extensions and loft conversions are popular ways to add further space. Our team designs additions that respect the existing architectural character while maximising usable floor area.",
            "<strong>Loft conversions:</strong> The area's Victorian terraces typically have good roof voids suitable for dormer loft conversions. Outside the Clapton Common Conservation Area, rear dormers can often be built under permitted development. We survey existing roof structures and confirm eligibility.",
            "<strong>Clapton Common Conservation Area:</strong> Parts of Stamford Hill fall within the Clapton Common Conservation Area, which protects the character of the Victorian and Edwardian streets around the common. Article 4 Directions may restrict permitted development rights. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>HMO and subdivision projects:</strong> Many Stamford Hill properties have been subdivided or are used as Houses in Multiple Occupation. New HMO creation or further subdivision requires planning permission and must comply with Hackney's housing standards. We prepare the necessary applications and ensure compliance with space and amenity standards.",
        ],
        "stats": [
            ("Conservation areas", "Clapton Common CA"),
            ("Housing type", "Large Victorian terraces"),
            ("Planning authority", "Hackney Council"),
            ("Key postcodes", "N16"),
        ],
        "faqs": [
            (
                "Can I extend my Victorian terrace in Stamford Hill?",
                "Yes, extensions are very common in Stamford Hill. Under permitted development, single-storey rear extensions up to 4 metres for terraced houses are achievable without planning permission. Larger extensions or two-storey additions require full planning permission. We advise on the maximum achievable for your property.",
            ),
            (
                "Do I need planning permission for a loft conversion in Stamford Hill?",
                "Outside the conservation area, rear dormers can often be built under permitted development. Within the Clapton Common Conservation Area, planning permission may be required. We confirm your property's status and advise on the best route.",
            ),
            (
                "Can I convert my Stamford Hill house into flats?",
                "Converting a house into flats requires planning permission from Hackney Council and Building Regulations approval. The council assesses impact on neighbours, parking, waste storage, and minimum space standards. We prepare the full drawing set for the application.",
            ),
            (
                "What building regulations apply to extensions in Stamford Hill?",
                "Extensions must comply with all relevant Approved Documents, including Part B (fire safety), Part L (energy efficiency), Part M (access), and Part A (structural). We prepare fully compliant building regulations drawings and coordinate with structural engineers.",
            ),
            (
                "How much do architectural drawings cost in Stamford Hill?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations drawings plus structural calculations. Fixed fees with no surprises.",
            ),
        ],
    },
    {
        "name": "Lewisham",
        "slug": "lewisham",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE13",
        "character": "Lewisham is a busy south-east London town centre undergoing significant regeneration. Its residential streets contain a mix of Victorian terraces, Edwardian houses, and inter-war properties, with demand for loft conversions and extensions growing as families settle.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, post-war estates, new-build apartments",
        "conservation_notes": "Lewisham town centre does not fall within a conservation area, though nearby areas such as Blackheath do",
        "planning_notes": "Lewisham Council is generally supportive of residential extensions and loft conversions under permitted development. The borough's emerging Local Plan encourages densification near transport hubs. Pre-application advice is available.",
        "nearby": ["blackheath", "deptford", "catford", "forest-hill"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, extensions, and building regulations for Lewisham's Victorian and Edwardian properties. MCIAT chartered, fixed fees, SE13 planning expertise built in.",
        "local_context_title": "Why Lewisham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Lewisham sits in the SE13 postcode at the heart of the London Borough of Lewisham. The town centre is undergoing major regeneration, while its surrounding residential streets — lined with Victorian terraces and Edwardian houses — are increasingly popular with families looking to extend and improve rather than move.",
            "<strong>Victorian and Edwardian terraces:</strong> Lewisham's residential streets offer excellent potential for loft conversions, rear extensions, and side-return infills. The typical two- or three-storey terrace has a good roof void and adequate garden depth for single-storey extensions. We survey each property and advise on the most effective use of space.",
            "<strong>Permitted development opportunities:</strong> Much of residential Lewisham sits outside conservation areas, meaning permitted development rights are available for rear dormers, single-storey extensions, and outbuildings. We confirm PD eligibility and prepare the building regulations drawings needed for Building Control sign-off.",
            "<strong>Regeneration context:</strong> Lewisham town centre's ongoing regeneration means some adjacent residential streets are subject to area-specific planning policies. We check site-specific designations as part of every project assessment.",
            "<strong>Building regulations:</strong> All extensions and conversions must comply with current Building Regulations. We prepare fully detailed building regulations drawings covering structural, fire safety, thermal, and acoustic requirements.",
        ],
        "stats": [
            ("Conservation areas", "Limited (town centre)"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE13"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Lewisham?",
                "Yes, loft conversions are popular in Lewisham. Most Victorian terraces outside conservation areas can add rear dormers under permitted development. We survey your roof, confirm PD eligibility, and prepare building regulations drawings.",
            ),
            (
                "What size extension can I build in SE13?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey without planning permission. Semi-detached houses have a 6-metre allowance. Within any conservation areas, planning permission may be required. We confirm what applies to your property.",
            ),
            (
                "How long does Lewisham Council take for planning decisions?",
                "Lewisham targets 8 weeks for householder applications. Pre-application advice is available and typically takes 4-6 weeks. We manage the timeline and handle all council correspondence.",
            ),
            (
                "How much do architectural drawings cost in Lewisham?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations drawings plus structural calculations. Fixed fees with no hidden extras.",
            ),
            (
                "Do I need building regulations for a rear extension in Lewisham?",
                "Yes, all extensions require Building Regulations approval regardless of whether planning permission is needed. This covers structural safety, fire safety, insulation, drainage, and ventilation. We prepare compliant drawings for Building Control submission.",
            ),
        ],
    },
    {
        "name": "Catford",
        "slug": "catford",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE6",
        "character": "Catford is a suburban south-east London neighbourhood with a mix of 1930s semi-detached houses and Victorian terraces. Its affordability relative to neighbouring areas attracts families undertaking extensions and loft conversions.",
        "housing_stock": "1930s semi-detached houses, Victorian terraces, Edwardian houses, post-war estates",
        "conservation_notes": "Culverley Green Conservation Area covers a pocket of attractive Victorian streets",
        "planning_notes": "Lewisham Council is generally supportive of residential improvements. Most properties outside the Culverley Green Conservation Area benefit from full permitted development rights. 1930s semis are particularly suitable for side and rear extensions.",
        "nearby": ["lewisham", "forest-hill", "sydenham", "blackheath"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Catford's 1930s semis and Victorian terraces. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why Catford demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Catford occupies the SE6 postcode in the London Borough of Lewisham. The neighbourhood's mix of 1930s semi-detached houses and Victorian terraces provides excellent opportunities for side extensions, rear extensions, and loft conversions — projects that add significant value and living space.",
            "<strong>1930s semi-detached houses:</strong> Catford's inter-war semis typically have hipped roofs, generous side passages, and good garden depths. Two-storey side extensions, single-storey rear extensions, and hip-to-gable loft conversions are all popular and generally achievable under permitted development. We design schemes that maximise space while maintaining the street's character.",
            "<strong>Victorian terraces:</strong> The area's Victorian streets — particularly around Culverley Green — contain well-proportioned terraces suitable for rear dormers and single-storey rear extensions. We survey each property and confirm permitted development eligibility.",
            "<strong>Culverley Green Conservation Area:</strong> This conservation area protects a pocket of attractive Victorian streets. Within the zone, Article 4 Directions may restrict permitted development rights, and Heritage Statements are required for external works. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Affordable improvement area:</strong> Catford's relative affordability makes it a popular area for families buying properties to improve. We help homeowners maximise their investment by identifying the most impactful extensions and ensuring smooth planning and building regulations processes.",
        ],
        "stats": [
            ("Conservation areas", "Culverley Green CA"),
            ("Housing type", "1930s semis, Victorian terraces"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE6"),
        ],
        "faqs": [
            (
                "Can I build a side extension on my 1930s semi in Catford?",
                "Yes, two-storey side extensions are popular on Catford's semis. Under permitted development, single-storey side extensions are possible. Two-storey side extensions usually require planning permission. Lewisham Council generally supports well-designed side extensions that respect the character of the street.",
            ),
            (
                "Can I convert the loft in my 1930s semi in Catford?",
                "Yes, hip-to-gable loft conversions are very popular on 1930s semis. These involve squaring off the hipped roof to create a full-height gable wall, then adding a rear dormer. Under permitted development, this is achievable without planning permission outside conservation areas. We survey your roof and advise on the best approach.",
            ),
            (
                "What planning restrictions apply in Culverley Green Conservation Area?",
                "The Culverley Green Conservation Area protects the Victorian character of the streets around the green. Article 4 Directions may restrict permitted development rights, meaning planning permission could be required for roof alterations, window replacements, and extensions. We check your property's status and prepare appropriate applications.",
            ),
            (
                "How much do architectural drawings cost in Catford?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations drawings plus structural calculations. Fixed fees throughout.",
            ),
            (
                "Do I need party wall agreements for a side extension?",
                "If your extension involves work on or near a shared boundary wall, you will likely need Party Wall Agreements. This is separate from planning permission. We advise on party wall requirements and recommend specialist surveyors.",
            ),
        ],
    },
    {
        "name": "Eltham",
        "slug": "eltham",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE9",
        "character": "Eltham is a leafy suburban neighbourhood in south-east London, known for Eltham Palace and its tree-lined streets of 1930s semi-detached houses. Extensions and loft conversions are the dominant project types.",
        "housing_stock": "1930s semi-detached houses, some Victorian terraces, inter-war detached houses, post-war estates",
        "conservation_notes": "Eltham Palace and its grounds are a Scheduled Ancient Monument; several small conservation areas in the vicinity",
        "planning_notes": "Royal Borough of Greenwich applies standard policies. Most 1930s semis benefit from full permitted development rights. Hip-to-gable loft conversions and two-storey rear extensions are common and generally supported.",
        "nearby": ["blackheath", "woolwich", "charlton", "sydenham"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Eltham's 1930s semis and suburban houses. MCIAT chartered, fixed fees, Greenwich planning expertise built in.",
        "local_context_title": "Why Eltham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Eltham sits in the SE9 postcode within the Royal Borough of Greenwich. The neighbourhood's tree-lined avenues of 1930s semi-detached houses, combined with good schools and green spaces, make it one of south-east London's most popular family areas — and one where demand for residential extensions and loft conversions is consistently high.",
            "<strong>1930s semi-detached houses:</strong> Eltham's inter-war semis are ideal candidates for hip-to-gable loft conversions, single-storey and two-storey rear extensions, and side extensions. The typical hipped roof can be squared off to create a full gable, then a rear dormer added to create a generous loft room. Under permitted development, these works can often proceed without planning permission.",
            "<strong>Eltham Palace context:</strong> Properties near Eltham Palace and its grounds — a Scheduled Ancient Monument — may face additional planning scrutiny. English Heritage consultation may be required for works affecting the setting of the palace. Our team assesses each site's constraints before committing to a design.",
            "<strong>Suburban character:</strong> Greenwich Council is mindful of preserving Eltham's suburban character. Extensions that are overly dominant or materially inappropriate may face objections. We design schemes that complement the existing 1930s aesthetic while delivering modern living spaces.",
            "<strong>Permitted development:</strong> Most Eltham properties outside conservation areas enjoy full permitted development rights. We confirm eligibility, prepare building regulations drawings, and manage the prior notification process where required.",
        ],
        "stats": [
            ("Conservation areas", "Limited (near Palace)"),
            ("Housing type", "1930s semis"),
            ("Planning authority", "Royal Borough of Greenwich"),
            ("Key postcodes", "SE9"),
        ],
        "faqs": [
            (
                "Can I build a hip-to-gable loft conversion in Eltham?",
                "Yes, hip-to-gable loft conversions are very popular on Eltham's 1930s semis. Under permitted development, these can usually proceed without planning permission. The hipped roof is squared off to create a gable wall, with a rear dormer added for additional headroom. We survey your roof and confirm eligibility.",
            ),
            (
                "What size extension can I build in Eltham?",
                "Under permitted development, semi-detached houses can build single-storey rear extensions up to 6 metres without planning permission (subject to prior notification). Two-storey rear extensions up to 3 metres are also possible under PD. We confirm the maximum achievable for your specific property.",
            ),
            (
                "Are there special planning rules near Eltham Palace?",
                "Properties in the vicinity of Eltham Palace may face additional planning scrutiny due to its status as a Scheduled Ancient Monument. English Heritage may be consulted on applications that affect the palace's setting. We assess these constraints early in the process.",
            ),
            (
                "How much do architectural drawings cost in Eltham?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "How long does Greenwich Council take for planning decisions?",
                "The Royal Borough of Greenwich targets 8 weeks for householder applications. Pre-application advice is available and recommended for complex projects. We manage the application timeline on your behalf.",
            ),
        ],
    },
    {
        "name": "Charlton",
        "slug": "charlton",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE7",
        "character": "Charlton is a riverside neighbourhood in south-east London combining Victorian terraces on the hillside with new-build developments along the Thames. Ongoing regeneration around Charlton Riverside is transforming the area.",
        "housing_stock": "Victorian terraces, 1930s semis, new-build apartments, riverside developments",
        "conservation_notes": "Charlton Village Conservation Area protects the historic village core around St Luke's Church",
        "planning_notes": "Royal Borough of Greenwich applies specific policies for the Charlton Riverside Opportunity Area. Victorian properties on the hillside benefit from standard permitted development rights. Riverside developments may require flood risk assessment.",
        "nearby": ["woolwich", "blackheath", "eltham", "deptford"],
        "popular_services": ["planning-drawings", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and building regulations for Charlton's Victorian terraces and riverside properties. MCIAT chartered, fixed fees, Greenwich planning expertise built in.",
        "local_context_title": "Why Charlton demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Charlton occupies the SE7 postcode in the Royal Borough of Greenwich, climbing from the Thames riverfront up to Charlton Park. The neighbourhood combines Victorian terraces on the hillside with significant new-build development along the riverside, creating a varied architectural landscape.",
            "<strong>Victorian terraces:</strong> Charlton's hillside streets contain well-proportioned Victorian terraces suitable for loft conversions, rear extensions, and internal reconfigurations. Outside the Charlton Village Conservation Area, permitted development rights enable rear dormers and single-storey extensions without planning permission.",
            "<strong>Charlton Village Conservation Area:</strong> The historic village core around St Luke's Church is protected as a conservation area. Works within the zone require Heritage Statements and sympathetic design. Our MCIAT-chartered team prepares applications that respect the village character.",
            "<strong>Riverside regeneration:</strong> The Charlton Riverside Opportunity Area is undergoing major transformation with new residential and mixed-use development. Properties in this zone are subject to specific planning policies. We navigate these requirements for both new-build and conversion projects.",
            "<strong>Flood risk:</strong> Riverside properties may fall within flood-risk zones, requiring flood risk assessments with planning applications. We incorporate these requirements into our submissions.",
        ],
        "stats": [
            ("Conservation areas", "Charlton Village CA"),
            ("Housing type", "Victorian terraces, new-builds"),
            ("Planning authority", "Royal Borough of Greenwich"),
            ("Key postcodes", "SE7"),
        ],
        "faqs": [
            (
                "Can I extend my Victorian terrace in Charlton?",
                "Yes, rear extensions and loft conversions are popular on Charlton's hillside terraces. Outside the Charlton Village Conservation Area, permitted development rights usually apply. We confirm eligibility and prepare the required drawings.",
            ),
            (
                "What planning rules apply in Charlton Village Conservation Area?",
                "The conservation area protects the historic village character. Planning permission is typically required for external alterations, and Heritage Statements must accompany applications. Our team prepares conservation-sensitive designs.",
            ),
            (
                "Are there flood risk issues in Charlton?",
                "Riverside properties may be within flood-risk zones. Planning applications in these areas must include flood risk assessments. We handle this requirement as part of our drawing package.",
            ),
            (
                "How much do architectural drawings cost in Charlton?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations. Fixed fees with no hidden charges.",
            ),
            (
                "How long does planning take in Greenwich?",
                "The Royal Borough of Greenwich targets 8 weeks for householder applications. Pre-application advice is available. We manage the full application timeline.",
            ),
        ],
    },
    {
        "name": "Stratford",
        "slug": "stratford",
        "borough": "Newham",
        "borough_slug": "newham",
        "postcodes": "E15",
        "character": "Stratford has been transformed by the 2012 Olympics and ongoing regeneration, combining new-build apartment towers around the Queen Elizabeth Olympic Park with Victorian terraces in the older residential streets.",
        "housing_stock": "New-build apartments, Victorian terraces, Edwardian houses, post-war estates",
        "conservation_notes": "Sugar House Lane Conservation Area (edge of Stratford); Three Mills Conservation Area",
        "planning_notes": "Newham Council applies specific policies for the Stratford Metropolitan Centre and Olympic Park fringe. The London Legacy Development Corporation (LLDC) retains planning authority over parts of the Olympic Park. Victorian residential streets benefit from standard PD rights.",
        "nearby": ["bow", "mile-end", "forest-gate", "canary-wharf"],
        "popular_services": ["building-regulations", "planning-drawings", "loft-conversions"],
        "hero_lede": "Planning permission drawings, building regulations, and loft conversions for Stratford's Victorian terraces and new-build apartments. MCIAT chartered, fixed fees, Newham expertise built in.",
        "local_context_title": "Why Stratford demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Stratford sits in the E15 postcode within the London Borough of Newham, centred on one of east London's busiest transport hubs. The area's transformation since the 2012 Olympics has created a dual character: modern apartment towers and mixed-use developments around the Olympic Park, alongside traditional Victorian and Edwardian residential streets.",
            "<strong>Victorian terraces:</strong> Stratford's older residential streets contain Victorian and Edwardian terraces suitable for loft conversions, rear extensions, and internal reconfigurations. Under permitted development, rear dormers and single-storey extensions are straightforward outside conservation areas. We survey each property and advise on the best approach.",
            "<strong>Dual planning authorities:</strong> Some areas near the Olympic Park fall under the London Legacy Development Corporation (LLDC) rather than Newham Council. Confirming the correct planning authority is an essential first step. Our team identifies the relevant authority and submits to the right body.",
            "<strong>New-build apartments:</strong> Stratford's many new apartment blocks generate demand for interior reconfiguration, Building Regulations compliance, and occasional balcony or terrace alterations. These projects typically require freeholder consent alongside Building Control approval.",
            "<strong>Conservation areas:</strong> The Sugar House Lane and Three Mills Conservation Areas on the fringes of Stratford protect industrial heritage. Works within these zones require Heritage Statements. We prepare applications to the required standard.",
        ],
        "stats": [
            ("Conservation areas", "Sugar House Lane CA"),
            ("Housing type", "Mixed — Victorian to modern"),
            ("Planning authority", "Newham Council / LLDC"),
            ("Key postcodes", "E15"),
        ],
        "faqs": [
            (
                "Which planning authority covers Stratford?",
                "It depends on the exact location. Newham Council handles most planning applications, but properties near the Olympic Park may fall under the London Legacy Development Corporation. We confirm the correct authority before submitting.",
            ),
            (
                "Can I build a loft conversion in Stratford?",
                "Yes, Victorian terraces in Stratford are well suited to dormer loft conversions. Outside conservation areas, rear dormers under permitted development are straightforward. We survey your roof and confirm eligibility.",
            ),
            (
                "What building regulations apply to apartment alterations in Stratford?",
                "Apartment fit-outs must comply with Part B (fire safety), Part E (acoustics), Part F (ventilation), and Part L (energy efficiency). We prepare compliant drawing packages for Building Control submission.",
            ),
            (
                "How much do architectural drawings cost in Stratford?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations. Fixed fees with no hidden extras.",
            ),
            (
                "Are there conservation area restrictions in Stratford?",
                "The Sugar House Lane and Three Mills Conservation Areas on the fringes of Stratford impose additional controls. Heritage Statements are required for applications within these zones. We prepare conservation-sensitive drawings.",
            ),
        ],
    },
    {
        "name": "Forest Gate",
        "slug": "forest-gate",
        "borough": "Newham",
        "borough_slug": "newham",
        "postcodes": "E7",
        "character": "Forest Gate is a gentrifying east London neighbourhood popular with first-time buyers and young families. Its streets of Victorian terraces offer excellent potential for loft conversions and rear extensions at relatively affordable prices.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war properties",
        "conservation_notes": "Woodgrange Estate Conservation Area covers the distinctive Victorian garden suburb streets",
        "planning_notes": "Newham Council is generally supportive of residential extensions. The Woodgrange Estate Conservation Area imposes additional controls on its distinctive Victorian streets. Outside conservation areas, standard permitted development rights apply.",
        "nearby": ["stratford", "manor-park", "walthamstow", "mile-end"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Forest Gate's Victorian terraces. MCIAT chartered, fixed fees, Newham planning expertise built in.",
        "local_context_title": "Why Forest Gate demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Forest Gate occupies the E7 postcode in the London Borough of Newham. The neighbourhood's streets of well-proportioned Victorian terraces — many with original features intact — have attracted a wave of families and first-time buyers looking to extend and improve.",
            "<strong>Victorian terraces:</strong> Forest Gate's two- and three-storey terraces are prime candidates for dormer loft conversions and single-storey rear extensions. The typical terrace has a rear outrigger, compact side return, and roof void with adequate headroom for conversion. We design schemes that maximise space within planning constraints.",
            "<strong>Woodgrange Estate Conservation Area:</strong> The Woodgrange Estate Conservation Area protects a distinctive Victorian garden suburb with tree-lined streets, decorative facades, and consistent architectural character. Article 4 Directions may restrict permitted development rights. Heritage Statements are required for external alterations. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Affordable improvement:</strong> Forest Gate's relative affordability makes it a popular area for properties purchased to improve. We help homeowners identify the most impactful extensions and navigate the planning process efficiently.",
            "<strong>Permitted development:</strong> Outside the conservation area, standard permitted development rights enable rear dormers, single-storey rear extensions, and outbuildings without planning permission. We confirm PD eligibility and prepare building regulations drawings.",
        ],
        "stats": [
            ("Conservation areas", "Woodgrange Estate CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Newham Council"),
            ("Key postcodes", "E7"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Forest Gate?",
                "Yes, loft conversions are very popular in Forest Gate. Outside the Woodgrange Conservation Area, rear dormers under permitted development are straightforward. Within the conservation area, planning permission may be required. We survey your roof and advise.",
            ),
            (
                "What restrictions apply in Woodgrange Estate Conservation Area?",
                "The conservation area protects the Victorian character of the Woodgrange streets. Article 4 Directions may require planning permission for roof alterations, window replacements, and front boundary changes. Heritage Statements must accompany applications. We prepare conservation-sensitive designs.",
            ),
            (
                "What size rear extension can I build in Forest Gate?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Larger extensions require planning permission. Within the conservation area, planning permission may be needed for any extension. We confirm what is achievable.",
            ),
            (
                "How much do architectural drawings cost in Forest Gate?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Newham Council take for planning decisions?",
                "Newham targets 8 weeks for householder applications. Pre-application advice is available. We manage the timeline and respond to any information requests from the council.",
            ),
        ],
    },
    {
        "name": "Manor Park",
        "slug": "manor-park",
        "borough": "Newham",
        "borough_slug": "newham",
        "postcodes": "E12",
        "character": "Manor Park is an affordable residential neighbourhood in east London with streets of Edwardian terraces and some inter-war properties. Its accessibility and family-sized houses drive demand for extensions and loft conversions.",
        "housing_stock": "Edwardian terraces, Victorian houses, some inter-war semis",
        "conservation_notes": "No major conservation areas; standard planning policies apply across most of the neighbourhood",
        "planning_notes": "Newham Council applies standard policies. Most properties benefit from full permitted development rights, making loft conversions and rear extensions straightforward. Building regulations compliance is the primary requirement.",
        "nearby": ["forest-gate", "stratford", "ilford", "walthamstow"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Manor Park's Edwardian terraces. MCIAT chartered, fixed fees, Newham planning expertise built in.",
        "local_context_title": "Why Manor Park demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Manor Park occupies the E12 postcode in the London Borough of Newham. The neighbourhood's streets of Edwardian terraces and larger inter-war houses offer excellent potential for loft conversions, rear extensions, and internal reconfigurations at some of east London's most accessible prices.",
            "<strong>Edwardian terraces:</strong> Manor Park's terraces are well proportioned with good roof voids and adequate garden depths. Dormer loft conversions and single-storey rear extensions are the most popular project types. Under permitted development, these works can proceed without planning permission, requiring only Building Regulations approval.",
            "<strong>No major conservation area constraints:</strong> Manor Park benefits from the absence of major conservation area designations, meaning standard permitted development rights apply across most of the neighbourhood. This simplifies the planning process and reduces project timelines.",
            "<strong>Building regulations focus:</strong> With permitted development covering most common project types, the primary regulatory requirement in Manor Park is Building Regulations compliance. We prepare detailed building regulations drawings covering structural, fire safety, thermal, and acoustic requirements.",
            "<strong>Value-adding improvements:</strong> Manor Park's affordability makes it a popular area for property improvement. We help homeowners maximise their return by designing extensions and conversions that add maximum value and usable space.",
        ],
        "stats": [
            ("Conservation areas", "None significant"),
            ("Housing type", "Edwardian terraces"),
            ("Planning authority", "Newham Council"),
            ("Key postcodes", "E12"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a loft conversion in Manor Park?",
                "In most cases, no. Rear dormers on Manor Park's terraces can usually be built under permitted development, requiring only Building Regulations approval. We confirm PD eligibility and prepare the required drawings.",
            ),
            (
                "What size extension can I build in Manor Park?",
                "Under permitted development, terraced houses can build single-storey rear extensions up to 4 metres without planning permission. Semi-detached houses have a 6-metre allowance. We confirm the maximum for your property.",
            ),
            (
                "What building regulations apply to a loft conversion in Manor Park?",
                "Loft conversions must comply with Part A (structure), Part B (fire safety — including a protected staircase), Part C (moisture), Part F (ventilation), Part L (insulation), and Part P (electrics). We prepare fully compliant drawings.",
            ),
            (
                "How much do architectural drawings cost in Manor Park?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers both planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does the building regulations process take?",
                "Building Control typically reviews a full plans application within 5 weeks. Once approved, inspections are conducted at key stages during construction. We prepare drawings to the standard that secures first-time approval.",
            ),
        ],
    },
    {
        "name": "Ilford",
        "slug": "ilford",
        "borough": "Redbridge",
        "borough_slug": "redbridge",
        "postcodes": "IG1",
        "character": "Ilford is a busy suburban town centre in the London Borough of Redbridge with streets of inter-war semi-detached houses and some Victorian terraces. Extensions and loft conversions are the most common residential projects.",
        "housing_stock": "Inter-war semi-detached houses, Victorian terraces, 1930s detached houses, new-build apartments",
        "conservation_notes": "Valentines Mansion and its park are locally listed; limited conservation area coverage",
        "planning_notes": "Redbridge Council applies standard policies for residential extensions. Most inter-war semis benefit from full permitted development rights. The council has specific guidance on front garden paving and crossovers.",
        "nearby": ["manor-park", "romford", "forest-gate", "walthamstow"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Ilford's inter-war semis and Victorian terraces. MCIAT chartered, fixed fees, Redbridge planning expertise built in.",
        "local_context_title": "Why Ilford demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Ilford sits in the IG1 postcode at the centre of the London Borough of Redbridge. The town's residential streets — dominated by inter-war semi-detached houses — see consistent demand for hip-to-gable loft conversions, two-storey side extensions, and single-storey rear extensions.",
            "<strong>Inter-war semis:</strong> Ilford's 1930s semis are ideal candidates for extension. Typical projects include hip-to-gable loft conversions (squaring off the hipped roof), two-storey side extensions to fill the gap between houses, and single-storey rear extensions for open-plan kitchens. Under permitted development, many of these works proceed without planning permission.",
            "<strong>Permitted development:</strong> Most Ilford properties benefit from full PD rights. We confirm eligibility, prepare building regulations drawings, and manage the prior notification process where required. This streamlined approach saves time and cost.",
            "<strong>Redbridge planning standards:</strong> Redbridge Council has specific design guidance for extensions, including requirements for matching materials, roof pitches, and window proportions. The council also has policies on front garden paving and vehicle crossovers. We design schemes that comply with these local standards.",
            "<strong>Building regulations:</strong> All extensions and loft conversions require Building Regulations approval. We prepare detailed drawings covering structural safety, fire protection, thermal performance, and drainage — ensuring first-time approval from Building Control.",
        ],
        "stats": [
            ("Conservation areas", "Limited"),
            ("Housing type", "Inter-war semis"),
            ("Planning authority", "Redbridge Council"),
            ("Key postcodes", "IG1"),
        ],
        "faqs": [
            (
                "Can I build a side extension in Ilford?",
                "Yes, side extensions are very popular on Ilford's semis. Single-storey side extensions may be achievable under permitted development. Two-storey side extensions usually require planning permission. Redbridge Council expects matching materials and a set-back from the front building line. We design compliant schemes.",
            ),
            (
                "Can I convert the loft on my 1930s semi in Ilford?",
                "Yes, hip-to-gable loft conversions are common on Ilford's semis. Under permitted development, these can proceed without planning permission. We survey your roof, confirm eligibility, and prepare building regulations drawings.",
            ),
            (
                "What are Redbridge Council's rules on front garden paving?",
                "Redbridge has policies restricting impermeable front garden paving to reduce flood risk. Permeable paving materials are required for areas over 5 square metres. We advise on compliant solutions.",
            ),
            (
                "How much do architectural drawings cost in Ilford?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees with no surprises.",
            ),
            (
                "How long does Redbridge take for planning decisions?",
                "Redbridge Council targets 8 weeks for householder applications. Pre-application advice is available. We manage the full application timeline.",
            ),
        ],
    },
    {
        "name": "Bexleyheath",
        "slug": "bexleyheath",
        "borough": "Bexley",
        "borough_slug": "bexley",
        "postcodes": "DA6",
        "character": "Bexleyheath is a suburban town centre in south-east London with streets of 1930s semi-detached houses. Extensions and loft conversions are the dominant project types in this family-oriented neighbourhood.",
        "housing_stock": "1930s semi-detached houses, inter-war detached houses, some post-war properties",
        "conservation_notes": "Limited conservation area coverage; Red House (William Morris) is Grade I listed",
        "planning_notes": "Bexley Council applies standard suburban policies. Most 1930s semis enjoy full permitted development rights. The council has clear guidance on extension design, materials, and proportions.",
        "nearby": ["eltham", "woolwich", "charlton"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Bexleyheath's 1930s semis. MCIAT chartered, fixed fees, Bexley planning expertise built in.",
        "local_context_title": "Why Bexleyheath demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Bexleyheath sits in the DA6 postcode within the London Borough of Bexley. The town's residential streets are predominantly lined with 1930s semi-detached houses — properties with excellent potential for hip-to-gable loft conversions, rear extensions, and side extensions.",
            "<strong>1930s semis:</strong> Bexleyheath's inter-war semis are ideal for extension. Hip-to-gable loft conversions, single-storey and two-storey rear extensions, and side extensions are all popular. Under permitted development, many of these works can proceed without planning permission.",
            "<strong>Permitted development:</strong> Most Bexleyheath properties enjoy full PD rights. We confirm eligibility, prepare building regulations drawings, and manage any prior notification required. This keeps projects on track and costs down.",
            "<strong>Bexley design standards:</strong> Bexley Council has clear expectations for extension design, including matching materials, appropriate roof pitches, and sympathetic proportions. We design schemes that comply with local guidance from the outset.",
            "<strong>Red House and heritage context:</strong> The Grade I listed Red House (designed by Philip Webb for William Morris) is in Bexleyheath. Properties in its immediate vicinity may face additional planning scrutiny. We assess site-specific constraints as part of every project.",
        ],
        "stats": [
            ("Conservation areas", "Limited"),
            ("Housing type", "1930s semis"),
            ("Planning authority", "Bexley Council"),
            ("Key postcodes", "DA6"),
        ],
        "faqs": [
            (
                "Can I build a hip-to-gable loft conversion in Bexleyheath?",
                "Yes, hip-to-gable loft conversions are very popular on Bexleyheath's 1930s semis. Under permitted development, these typically proceed without planning permission. We survey your roof and prepare building regulations drawings.",
            ),
            (
                "What size extension can I build in Bexleyheath?",
                "Under permitted development, semi-detached houses can build single-storey rear extensions up to 6 metres. Two-storey rear extensions up to 3 metres are also possible under PD. We confirm the maximum for your property.",
            ),
            (
                "Do I need matching materials for my extension in Bexleyheath?",
                "Yes, Bexley Council expects extensions to use materials matching the existing house. This includes brick type, mortar colour, roof tiles, and window styles. We specify materials in our drawings to ensure compliance.",
            ),
            (
                "How much do architectural drawings cost in Bexleyheath?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Bexley Council take for planning decisions?",
                "Bexley targets 8 weeks for householder applications. Most straightforward extensions are decided within this timeframe. We manage the application process from start to finish.",
            ),
        ],
    },
    {
        "name": "Romford",
        "slug": "romford",
        "borough": "Havering",
        "borough_slug": "havering",
        "postcodes": "RM1",
        "character": "Romford is a major suburban town centre in east London with a mix of inter-war and modern housing. Extensions and loft conversions are popular among families seeking more space in this well-connected neighbourhood.",
        "housing_stock": "Inter-war semi-detached houses, 1930s detached, modern new-builds, some Victorian terraces",
        "conservation_notes": "Romford Conservation Area covers parts of the historic market town centre",
        "planning_notes": "Havering Council applies suburban policies that generally support residential extensions. Most inter-war properties benefit from full permitted development rights. The council has specific guidance on extension design and materials.",
        "nearby": ["ilford", "bexleyheath"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Romford's inter-war houses. MCIAT chartered, fixed fees, Havering planning expertise built in.",
        "local_context_title": "Why Romford demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Romford sits in the RM1 postcode within the London Borough of Havering. As one of east London's largest suburban centres, its residential streets — dominated by inter-war semi-detached and detached houses — see consistent demand for extensions, loft conversions, and modernisation projects.",
            "<strong>Inter-war housing:</strong> Romford's 1930s semis and detached houses are well suited to hip-to-gable loft conversions, two-storey side extensions, and single-storey rear extensions. These properties typically have generous plots, making larger extensions feasible under both permitted development and full planning permission.",
            "<strong>Romford Conservation Area:</strong> The Romford Conservation Area covers parts of the historic market town centre. Properties within this zone face additional planning controls, including potential Article 4 Directions. We check each property's status and advise on requirements.",
            "<strong>Permitted development:</strong> Most Romford residential properties enjoy full PD rights, enabling loft conversions, rear extensions, and outbuildings without planning permission. We confirm eligibility and prepare building regulations drawings for Building Control approval.",
            "<strong>Havering design standards:</strong> Havering Council has clear design expectations for residential extensions. We ensure our schemes comply with local guidance on materials, proportions, and streetscape impact.",
        ],
        "stats": [
            ("Conservation areas", "Romford CA (town centre)"),
            ("Housing type", "Inter-war semis and detached"),
            ("Planning authority", "Havering Council"),
            ("Key postcodes", "RM1"),
        ],
        "faqs": [
            (
                "Can I extend my inter-war house in Romford?",
                "Yes, extensions are very popular in Romford. Under permitted development, semi-detached houses can build rear extensions up to 6 metres at single storey. Two-storey rear and side extensions may require planning permission. We advise on what is achievable.",
            ),
            (
                "Can I convert the loft on my Romford semi?",
                "Yes, hip-to-gable loft conversions are common and typically proceed under permitted development. We survey your roof, confirm eligibility, and prepare building regulations drawings.",
            ),
            (
                "Are there conservation area restrictions in Romford?",
                "The Romford Conservation Area covers parts of the town centre. Properties within this zone may need planning permission for works that would otherwise be permitted development. We check your property's status.",
            ),
            (
                "How much do architectural drawings cost in Romford?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees with no surprises.",
            ),
            (
                "How long does Havering take for planning decisions?",
                "Havering Council targets 8 weeks for householder applications. Pre-application advice is available and recommended for complex projects. We manage the full application process.",
            ),
        ],
    },
    {
        "name": "Uxbridge",
        "slug": "uxbridge",
        "borough": "Hillingdon",
        "borough_slug": "hillingdon",
        "postcodes": "UB8",
        "character": "Uxbridge is a suburban town centre in west London at the end of the Metropolitan and Piccadilly lines. Its residential streets contain a mix of inter-war houses, post-war estates, and newer developments.",
        "housing_stock": "Inter-war semi-detached and detached houses, 1950s-60s estates, modern apartments",
        "conservation_notes": "Old Uxbridge Conservation Area covers the historic town centre around the Market House",
        "planning_notes": "Hillingdon Council applies suburban policies that are generally supportive of residential extensions. Most properties outside the conservation area benefit from full permitted development rights. The borough has specific SPDs on house extensions.",
        "nearby": ["southall", "harrow-on-the-hill", "northfields"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Uxbridge's suburban houses. MCIAT chartered, fixed fees, Hillingdon planning expertise built in.",
        "local_context_title": "Why Uxbridge demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Uxbridge sits in the UB8 postcode at the western edge of the London Borough of Hillingdon. The town's residential areas contain a mix of inter-war semi-detached houses, larger detached properties, and post-war estates — all offering opportunities for extension and improvement.",
            "<strong>Inter-war housing:</strong> Uxbridge's 1930s semis and detached houses are popular candidates for hip-to-gable loft conversions, rear extensions, and side extensions. The typically generous plots allow for larger extensions than are common in inner London. We design schemes that maximise space within planning and building regulations constraints.",
            "<strong>Old Uxbridge Conservation Area:</strong> The historic town centre around the Market House is protected as a conservation area. Properties within this zone face additional planning controls. We check each site's status and prepare appropriate applications.",
            "<strong>Hillingdon SPDs:</strong> Hillingdon Council has published Supplementary Planning Documents on residential extensions with specific guidance on extension depths, roof design, and materials. We design schemes that comply with this guidance from the outset, improving the chances of first-time approval.",
            "<strong>Permitted development:</strong> Most Uxbridge residential properties outside the conservation area enjoy full PD rights. We confirm eligibility and prepare building regulations drawings for a smooth Building Control process.",
        ],
        "stats": [
            ("Conservation areas", "Old Uxbridge CA"),
            ("Housing type", "Inter-war semis and detached"),
            ("Planning authority", "Hillingdon Council"),
            ("Key postcodes", "UB8"),
        ],
        "faqs": [
            (
                "Can I extend my house in Uxbridge?",
                "Yes, extensions are very popular in Uxbridge. Under permitted development, semi-detached houses can build rear extensions up to 6 metres at single storey. The generous plots common in UB8 often allow for larger schemes. We advise on the maximum achievable.",
            ),
            (
                "Can I convert the loft on my Uxbridge semi?",
                "Yes, hip-to-gable loft conversions are common in Uxbridge. Under permitted development, these typically proceed without planning permission. We survey your roof and prepare building regulations drawings.",
            ),
            (
                "What are Hillingdon's rules on extensions?",
                "Hillingdon has published SPDs with specific guidance on extension depths, roof pitches, and materials. We design schemes compliant with this guidance, reducing the risk of refusal.",
            ),
            (
                "How much do architectural drawings cost in Uxbridge?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Hillingdon take for planning decisions?",
                "Hillingdon Council targets 8 weeks for householder applications. Pre-application advice is available. We manage the timeline and handle all council correspondence.",
            ),
        ],
    },
    {
        "name": "Southall",
        "slug": "southall",
        "borough": "Ealing",
        "borough_slug": "ealing",
        "postcodes": "UB1, UB2",
        "character": "Southall is a culturally vibrant neighbourhood in west London with a diverse population and streets of Victorian terraces, inter-war houses, and post-war estates. Extensions and conversions are in high demand as families grow.",
        "housing_stock": "Victorian terraces, inter-war semis, Edwardian houses, post-war estates",
        "conservation_notes": "King Street Conservation Area preserves some of Southall's original Victorian High Street character",
        "planning_notes": "Ealing Council applies standard policies. The Southall Opportunity Area designates the neighbourhood for significant regeneration and growth. Most residential properties outside conservation areas benefit from full permitted development rights.",
        "nearby": ["hanwell", "northfields", "uxbridge", "harlesden"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Southall's Victorian terraces and family homes. MCIAT chartered, fixed fees, Ealing planning expertise built in.",
        "local_context_title": "Why Southall demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Southall occupies the UB1 and UB2 postcodes in the London Borough of Ealing. The neighbourhood's diverse housing stock — Victorian terraces, inter-war semis, and larger family homes — sees consistent demand for extensions, loft conversions, and internal reconfigurations as families seek more space.",
            "<strong>Victorian and Edwardian terraces:</strong> Southall's older streets contain terraced houses well suited to rear extensions, loft conversions, and side-return infills. Under permitted development, many of these works proceed without planning permission. We confirm PD eligibility and prepare building regulations drawings.",
            "<strong>Inter-war housing:</strong> The area's 1930s semis are popular candidates for hip-to-gable loft conversions and two-storey side extensions. We design schemes that maximise space while respecting the street character.",
            "<strong>Southall Opportunity Area:</strong> Southall is designated as an Opportunity Area in the London Plan, meaning significant regeneration and growth are planned. Properties near the Crossrail station may be subject to area-specific planning policies. We navigate these requirements as part of every project.",
            "<strong>Building regulations:</strong> All extensions and conversions require Building Regulations approval. We prepare detailed drawings covering structural safety, fire protection, thermal performance, and ventilation.",
        ],
        "stats": [
            ("Conservation areas", "King Street CA"),
            ("Housing type", "Victorian terraces, inter-war semis"),
            ("Planning authority", "Ealing Council"),
            ("Key postcodes", "UB1, UB2"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Southall?",
                "Yes, loft conversions are popular in Southall. Victorian terraces and inter-war semis are both well suited. Under permitted development, rear dormers and hip-to-gable conversions can often proceed without planning permission. We survey your roof and confirm eligibility.",
            ),
            (
                "What size extension can I build in Southall?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey, and semis up to 6 metres. Two-storey extensions usually require planning permission. We confirm the maximum for your property.",
            ),
            (
                "How does the Southall Opportunity Area affect planning?",
                "The Opportunity Area designation means Ealing Council is planning for significant growth in Southall. Properties near the station and town centre may be subject to area-specific policies. We check site designations as part of every project.",
            ),
            (
                "How much do architectural drawings cost in Southall?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Ealing take for planning decisions?",
                "Ealing Council targets 8 weeks for householder applications. Pre-application advice is available and recommended for complex schemes. We manage the full application process.",
            ),
        ],
    },
    {
        "name": "Hanwell",
        "slug": "hanwell",
        "borough": "Ealing",
        "borough_slug": "ealing",
        "postcodes": "W7",
        "character": "Hanwell is a quiet residential neighbourhood in west London with streets of Edwardian terraces, inter-war semis, and a community-focused village feel. Rear extensions and loft conversions are the most common projects.",
        "housing_stock": "Edwardian terraces, inter-war semi-detached houses, some Victorian properties",
        "conservation_notes": "Hanwell Village Green Conservation Area preserves the historic core around the church",
        "planning_notes": "Ealing Council applies standard residential policies. Most properties outside the small conservation area benefit from full permitted development rights. The Brent River and canal add flood-risk considerations for some properties.",
        "nearby": ["southall", "northfields", "acton"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Hanwell's Edwardian terraces and family homes. MCIAT chartered, fixed fees, Ealing planning expertise built in.",
        "local_context_title": "Why Hanwell demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Hanwell sits in the W7 postcode within the London Borough of Ealing. The neighbourhood's tree-lined streets of Edwardian terraces and inter-war semis, combined with good schools and green spaces along the Brent Valley, make it a popular family area with consistent demand for residential extensions.",
            "<strong>Edwardian terraces:</strong> Hanwell's Edwardian terraces are well proportioned with good roof voids and rear gardens. Rear extensions and dormer loft conversions are the most popular project types. Under permitted development, many of these works proceed without planning permission.",
            "<strong>Inter-war semis:</strong> The area's 1930s semis are ideal for hip-to-gable loft conversions, side extensions, and rear extensions. We design schemes that work with the existing roof profile and plot dimensions.",
            "<strong>Hanwell Village Green Conservation Area:</strong> The small conservation area around the historic village core imposes additional planning controls on properties within its boundary. We check each property's status and prepare appropriate applications.",
            "<strong>Brent Valley flood risk:</strong> Properties near the River Brent or the Grand Union Canal may fall within flood-risk zones. We include flood risk assessments where required and factor drainage into our building regulations submissions.",
        ],
        "stats": [
            ("Conservation areas", "Hanwell Village Green CA"),
            ("Housing type", "Edwardian terraces, inter-war semis"),
            ("Planning authority", "Ealing Council"),
            ("Key postcodes", "W7"),
        ],
        "faqs": [
            (
                "Can I extend my Edwardian terrace in Hanwell?",
                "Yes, rear extensions are very common in Hanwell. Under permitted development, terraced houses can extend up to 4 metres at single storey. We confirm PD eligibility and prepare the required drawings.",
            ),
            (
                "Can I build a loft conversion in Hanwell?",
                "Yes, both Edwardian terraces and inter-war semis in Hanwell are well suited to loft conversions. We survey your roof, confirm permitted development eligibility, and prepare building regulations drawings.",
            ),
            (
                "Are there flood risk issues in Hanwell?",
                "Properties near the River Brent or Grand Union Canal may be within flood-risk zones. Flood risk assessments may be required for planning applications. We assess your site and incorporate requirements into our submissions.",
            ),
            (
                "How much do architectural drawings cost in Hanwell?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Ealing take for planning decisions?",
                "Ealing Council targets 8 weeks for householder applications. We manage the timeline and handle all council correspondence on your behalf.",
            ),
        ],
    },
    {
        "name": "Harlesden",
        "slug": "harlesden",
        "borough": "Brent",
        "borough_slug": "brent",
        "postcodes": "NW10",
        "character": "Harlesden is a diverse neighbourhood in north-west London with streets of Victorian terraces undergoing gradual regeneration. Loft conversions and rear extensions are popular as families invest in improving the area's well-proportioned period houses.",
        "housing_stock": "Victorian terraces, Edwardian houses, some inter-war properties, post-war estates",
        "conservation_notes": "Harlesden Town Centre Conservation Area covers parts of the High Street",
        "planning_notes": "Brent Council applies standard policies for residential areas. Most Victorian terraces outside the conservation area benefit from full permitted development rights. The council's Design Guide SPD sets expectations for extension design.",
        "nearby": ["willesden", "wembley", "kilburn", "queens-park"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Harlesden's Victorian terraces. MCIAT chartered, fixed fees, Brent planning expertise built in.",
        "local_context_title": "Why Harlesden demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Harlesden occupies the NW10 postcode in the London Borough of Brent. The neighbourhood's streets of Victorian and Edwardian terraces — many well proportioned with generous room sizes — are increasingly popular with families looking to extend and improve rather than move to more expensive areas.",
            "<strong>Victorian terraces:</strong> Harlesden's terraces offer excellent potential for dormer loft conversions, single-storey rear extensions, and side-return infills. The typical Victorian terrace has a rear outrigger and adequate roof void for conversion. Under permitted development, rear dormers and rear extensions can often proceed without planning permission.",
            "<strong>Harlesden Conservation Area:</strong> The Harlesden Town Centre Conservation Area covers parts of the High Street and surrounding streets. Properties within this zone face additional planning controls. We check each property's status and advise on requirements.",
            "<strong>Brent Design Guide:</strong> Brent Council's Design Guide SPD sets specific expectations for extension design, including dormer proportions, material choices, and rear extension depths. Our MCIAT-chartered team designs schemes that comply with this guidance.",
            "<strong>Regeneration context:</strong> Harlesden is benefiting from gradual regeneration investment. We help homeowners make the most of their properties by designing extensions that add value and living space.",
        ],
        "stats": [
            ("Conservation areas", "Harlesden Town Centre CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Brent Council"),
            ("Key postcodes", "NW10"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Harlesden?",
                "Yes, loft conversions are popular in Harlesden. Outside the conservation area, rear dormers under permitted development are straightforward. We survey your roof, confirm eligibility, and prepare building regulations drawings.",
            ),
            (
                "What size extension can I build in Harlesden?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Larger extensions require planning permission. We confirm the maximum achievable for your property.",
            ),
            (
                "Are there planning restrictions in Harlesden Conservation Area?",
                "The conservation area covers parts of the town centre. Properties within may need planning permission for external works. We check your property's status and prepare appropriate applications.",
            ),
            (
                "How much do architectural drawings cost in Harlesden?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Brent take for planning decisions?",
                "Brent targets 8 weeks for householder applications. Pre-application advice is available. We manage the full application process on your behalf.",
            ),
        ],
    },
    {
        "name": "Willesden",
        "slug": "willesden",
        "borough": "Brent",
        "borough_slug": "brent",
        "postcodes": "NW2, NW10",
        "character": "Willesden is a diverse residential neighbourhood in Brent with streets of Victorian and Edwardian terraces. Its mix of family houses and converted flats generates demand for extensions, loft conversions, and internal reconfigurations.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, converted flats",
        "conservation_notes": "Mapesbury Conservation Area covers a significant area of Edwardian streets in Willesden Green",
        "planning_notes": "Brent Council applies specific controls within the Mapesbury Conservation Area. Outside conservation areas, standard permitted development rights apply. The council's Design Guide SPD provides detailed extension guidance.",
        "nearby": ["harlesden", "kilburn", "queens-park", "wembley"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Willesden's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Brent planning expertise built in.",
        "local_context_title": "Why Willesden demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Willesden spans the NW2 and NW10 postcodes in the London Borough of Brent. The neighbourhood's residential streets — from the grand Edwardian avenues of Mapesbury to the compact Victorian terraces of Willesden Junction — offer diverse opportunities for residential extension and improvement.",
            "<strong>Mapesbury Conservation Area:</strong> The Mapesbury Conservation Area covers one of north-west London's finest collections of Edwardian houses. Article 4 Directions restrict permitted development rights, meaning planning permission is required for most external alterations including dormer conversions, window replacements, and front boundary changes. Our MCIAT-chartered team specialises in conservation-sensitive applications that satisfy Brent's planning officers.",
            "<strong>Victorian terraces:</strong> Willesden's Victorian terraces outside the conservation area are prime candidates for rear dormers, single-storey rear extensions, and side-return infills under permitted development. We confirm PD eligibility and prepare building regulations drawings.",
            "<strong>Flat conversions:</strong> Many Willesden houses have been converted to flats. Further subdivision or reconversion projects require planning permission and must comply with Brent's housing standards. We prepare the necessary applications.",
            "<strong>Brent Design Guide:</strong> Brent's Design Guide SPD provides specific guidance on extension design. We design schemes that comply with this guidance, improving approval prospects.",
        ],
        "stats": [
            ("Conservation areas", "Mapesbury CA"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Brent Council"),
            ("Key postcodes", "NW2, NW10"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Mapesbury Conservation Area?",
                "For most external works, yes. The Mapesbury Conservation Area has Article 4 Directions that remove many permitted development rights. Dormer conversions, window replacements, and front alterations typically require planning permission. We prepare conservation-sensitive applications.",
            ),
            (
                "Can I build a loft conversion in Willesden?",
                "Outside the Mapesbury Conservation Area, rear dormers under permitted development are straightforward. Within the conservation area, planning permission is required. We survey your roof and advise on the best approach.",
            ),
            (
                "Can I convert my Willesden house into flats?",
                "Converting a house to flats requires planning permission from Brent Council and Building Regulations approval. We prepare the full drawing set including floor plans, sections, and design statements.",
            ),
            (
                "How much do architectural drawings cost in Willesden?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "How long does Brent take for planning decisions?",
                "Brent targets 8 weeks for householder applications. Conservation area applications may take longer. We manage the full timeline on your behalf.",
            ),
        ],
    },
    {
        "name": "Palmers Green",
        "slug": "palmers-green",
        "borough": "Enfield",
        "borough_slug": "enfield",
        "postcodes": "N13",
        "character": "Palmers Green is a suburban neighbourhood in north London with streets of Edwardian terraces and inter-war semis. Its family-friendly atmosphere and good transport links drive demand for loft conversions and rear extensions.",
        "housing_stock": "Edwardian terraces, inter-war semi-detached houses, some 1930s detached",
        "conservation_notes": "Broomfield House and its park are locally significant; limited conservation area coverage in the residential streets",
        "planning_notes": "Enfield Council applies standard suburban policies. Most properties benefit from full permitted development rights. The council has specific guidance on dormer design and extension proportions.",
        "nearby": ["winchmore-hill", "tottenham", "wood-green", "finsbury-park"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Palmers Green's Edwardian terraces and inter-war houses. MCIAT chartered, fixed fees, Enfield planning expertise built in.",
        "local_context_title": "Why Palmers Green demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Palmers Green sits in the N13 postcode within the London Borough of Enfield. The neighbourhood's tree-lined streets of Edwardian terraces and inter-war semis make it one of north London's most popular family areas, with consistent demand for loft conversions, rear extensions, and open-plan ground-floor reconfigurations.",
            "<strong>Edwardian terraces:</strong> Palmers Green's Edwardian terraces are well proportioned with good roof voids and decorative period features. Rear dormers are the most popular loft conversion type, adding bedrooms and en-suite bathrooms. Under permitted development, these can proceed without planning permission.",
            "<strong>Inter-war semis:</strong> The area's 1930s semis are ideal for hip-to-gable loft conversions, side extensions, and rear extensions. We design schemes that work with the existing roof profile and plot dimensions.",
            "<strong>Enfield design standards:</strong> Enfield Council has specific guidance on dormer design, extension depths, and materials. Dormers must be set back from the eaves and use materials matching the existing roof. We design schemes that comply from the outset.",
            "<strong>Permitted development:</strong> Most Palmers Green properties enjoy full PD rights, simplifying the process for common project types. We confirm eligibility and prepare building regulations drawings for Building Control approval.",
        ],
        "stats": [
            ("Conservation areas", "Limited"),
            ("Housing type", "Edwardian terraces, inter-war semis"),
            ("Planning authority", "Enfield Council"),
            ("Key postcodes", "N13"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Palmers Green?",
                "Yes, loft conversions are very popular in Palmers Green. Both Edwardian terraces and inter-war semis are well suited. Under permitted development, rear dormers and hip-to-gable conversions can proceed without planning permission. We survey your roof and confirm eligibility.",
            ),
            (
                "What size extension can I build in N13?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey, and semis up to 6 metres. Two-storey extensions usually require planning permission. We confirm the maximum for your property.",
            ),
            (
                "What are Enfield's rules on dormers?",
                "Enfield Council expects dormers to be set back from the eaves, set in from party walls, and constructed in materials matching the existing roof. Flat-roof dormers on the front elevation are generally refused. We design compliant dormers from the outset.",
            ),
            (
                "How much do architectural drawings cost in Palmers Green?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Enfield take for planning decisions?",
                "Enfield Council targets 8 weeks for householder applications. Pre-application advice is available. We manage the application process from start to finish.",
            ),
        ],
    },
    {
        "name": "Winchmore Hill",
        "slug": "winchmore-hill",
        "borough": "Enfield",
        "borough_slug": "enfield",
        "postcodes": "N21",
        "character": "Winchmore Hill is a leafy, affluent suburb in north London known for its large Edwardian houses, village green, and tree-lined streets. Extensions and loft conversions on its substantial family homes are the dominant project types.",
        "housing_stock": "Large Edwardian detached and semi-detached houses, some inter-war properties, Victorian villas",
        "conservation_notes": "Winchmore Hill Green Conservation Area preserves the historic village character around the green",
        "planning_notes": "Enfield Council applies specific controls within the conservation area. The large plots and substantial houses make extensions generally feasible. The council's design guidance emphasises sympathetic materials and proportions.",
        "nearby": ["palmers-green", "tottenham", "wood-green"],
        "popular_services": ["house-extensions", "loft-conversions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Winchmore Hill's large Edwardian houses. MCIAT chartered, fixed fees, Enfield planning expertise built in.",
        "local_context_title": "Why Winchmore Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Winchmore Hill sits in the N21 postcode within the London Borough of Enfield. The neighbourhood's tree-lined avenues of substantial Edwardian houses — many with large gardens, period features, and generous proportions — make it one of north London's most desirable family areas.",
            "<strong>Large Edwardian houses:</strong> Winchmore Hill's detached and semi-detached Edwardian houses offer extensive potential for rear extensions, side extensions, loft conversions, and garden studios. The generous plot sizes accommodate larger schemes than are typical in inner London.",
            "<strong>Winchmore Hill Green Conservation Area:</strong> The conservation area around the village green protects the historic character of the neighbourhood's core. Article 4 Directions may restrict permitted development rights. Heritage Statements are required for external alterations. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Substantial properties:</strong> Many Winchmore Hill houses are already substantial, and extensions are about adding high-quality living space rather than maximising footprint. We design schemes with attention to architectural quality, materials, and proportion.",
            "<strong>Enfield design guidance:</strong> Enfield Council's design guidance emphasises sympathetic extensions that complement the existing building. We ensure our schemes comply with local standards and enhance the character of the property.",
        ],
        "stats": [
            ("Conservation areas", "Winchmore Hill Green CA"),
            ("Housing type", "Large Edwardian houses"),
            ("Planning authority", "Enfield Council"),
            ("Key postcodes", "N21"),
        ],
        "faqs": [
            (
                "Can I extend my Edwardian house in Winchmore Hill?",
                "Yes, the generous plots in Winchmore Hill make extensions very feasible. Under permitted development, detached houses can build single-storey rear extensions up to 8 metres. Within the conservation area, planning permission may be required. We advise on the best approach.",
            ),
            (
                "Do I need planning permission in Winchmore Hill Conservation Area?",
                "For most external works within the conservation area, yes. Article 4 Directions may restrict permitted development rights. Heritage Statements are required with applications. We prepare conservation-sensitive drawings.",
            ),
            (
                "Can I build a loft conversion in Winchmore Hill?",
                "Yes, the large roof voids on Winchmore Hill's Edwardian houses are well suited to conversion. Outside the conservation area, dormers under permitted development are straightforward. We survey your roof and confirm eligibility.",
            ),
            (
                "How much do architectural drawings cost in Winchmore Hill?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Bespoke packages for larger schemes are priced individually.",
            ),
            (
                "How long does Enfield take for planning decisions?",
                "Enfield Council targets 8 weeks for householder applications. Conservation area applications may take slightly longer. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Harrow on the Hill",
        "slug": "harrow-on-the-hill",
        "borough": "Harrow",
        "borough_slug": "harrow",
        "postcodes": "HA1",
        "character": "Harrow on the Hill is a historic hilltop neighbourhood dominated by Harrow School and its Grade I listed buildings. The surrounding residential streets contain a mix of Victorian, Edwardian, and inter-war housing with strong conservation area controls.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, some large detached houses",
        "conservation_notes": "Harrow on the Hill Conservation Area covers the hilltop and school precinct with strict controls",
        "planning_notes": "Harrow Council applies stringent controls within the conservation area, which covers much of the hilltop. Article 4 Directions restrict permitted development rights. Outside the conservation area, standard PD rights apply. The hilltop setting means roof extensions are particularly scrutinised.",
        "nearby": ["pinner", "wembley", "harlesden"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, extensions, and heritage-sensitive design for Harrow on the Hill's period houses. MCIAT chartered, fixed fees, Harrow planning expertise built in.",
        "local_context_title": "Why Harrow on the Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Harrow on the Hill sits in the HA1 postcode within the London Borough of Harrow. The neighbourhood's hilltop position, crowned by the Grade I listed buildings of Harrow School, creates one of outer London's most distinctive and tightly controlled planning environments.",
            "<strong>Harrow on the Hill Conservation Area:</strong> The conservation area covers the hilltop and much of the surrounding residential streets. Article 4 Directions restrict permitted development rights, meaning planning permission is required for most external alterations. Heritage Statements must accompany all applications. Our MCIAT-chartered team is experienced in conservation-area work and prepares applications to the standard Harrow Council expects.",
            "<strong>Listed buildings context:</strong> The proximity of Harrow School's Grade I listed buildings means the setting of these heritage assets is a material planning consideration for residential projects in the vicinity. We assess the impact of proposed works on heritage settings as part of every application.",
            "<strong>Roof extensions:</strong> Harrow on the Hill's elevated position means roof extensions are visible across a wide area. The council scrutinises dormer and loft conversion proposals carefully. We design roof extensions that respect the hilltop skyline and satisfy conservation officers.",
            "<strong>Residential properties:</strong> Beyond the conservation area, Harrow on the Hill's residential streets contain a mix of Victorian terraces, Edwardian houses, and inter-war semis. We design extensions and conversions suited to each property type.",
        ],
        "stats": [
            ("Conservation areas", "Harrow on the Hill CA"),
            ("Listed buildings", "Harrow School (Grade I)"),
            ("Planning authority", "Harrow Council"),
            ("Key postcodes", "HA1"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Harrow on the Hill?",
                "Within the conservation area, planning permission is required for most external works. Article 4 Directions restrict permitted development rights. Heritage Statements must accompany applications. We prepare conservation-sensitive drawings.",
            ),
            (
                "Can I build a loft conversion on Harrow on the Hill?",
                "Loft conversions are possible but must be designed sensitively given the hilltop setting. Within the conservation area, planning permission is required and the council scrutinises roof extensions carefully. We design schemes that respect the skyline.",
            ),
            (
                "How does proximity to Harrow School affect planning?",
                "The Grade I listed buildings of Harrow School are a material planning consideration. Applications for works that affect the setting of these heritage assets face additional scrutiny. We assess heritage impact as part of every application.",
            ),
            (
                "How much do architectural drawings cost in Harrow on the Hill?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations. Bespoke packages for complex heritage projects are priced individually.",
            ),
            (
                "How long does Harrow take for planning decisions?",
                "Harrow Council targets 8 weeks for householder applications. Conservation area applications may take longer. We manage the full timeline and handle heritage consultations.",
            ),
        ],
    },
    {
        "name": "Pinner",
        "slug": "pinner",
        "borough": "Harrow",
        "borough_slug": "harrow",
        "postcodes": "HA5",
        "character": "Pinner is a metropolitan village in north-west London with a medieval High Street, Tudor and Edwardian buildings, and leafy residential streets. Its conservation area and village character require careful architectural design.",
        "housing_stock": "Tudor and medieval buildings (High Street), Edwardian detached houses, inter-war semis, 1930s detached",
        "conservation_notes": "Pinner High Street Conservation Area protects the historic village core with its medieval and Tudor buildings",
        "planning_notes": "Harrow Council applies strict controls within the conservation area. The village character is a key planning consideration. Outside the conservation area, standard PD rights apply to residential properties.",
        "nearby": ["harrow-on-the-hill", "wembley", "uxbridge"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, extensions, and heritage-sensitive design for Pinner's period houses and village properties. MCIAT chartered, fixed fees, Harrow planning expertise built in.",
        "local_context_title": "Why Pinner demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Pinner sits in the HA5 postcode within the London Borough of Harrow. The neighbourhood retains a distinctive village character centred on its medieval High Street, with residential streets of Edwardian and inter-war houses radiating outwards through leafy avenues.",
            "<strong>Pinner High Street Conservation Area:</strong> The conservation area protects Pinner's historic village core, including medieval and Tudor timber-framed buildings alongside Victorian and Edwardian shops and houses. Planning permission is required for most external works, and the council expects designs that respect the village character. Our MCIAT-chartered team prepares heritage-sensitive applications.",
            "<strong>Edwardian houses:</strong> Pinner's residential streets contain substantial Edwardian detached and semi-detached houses with generous gardens. These properties are well suited to rear extensions, loft conversions, and garden room additions. We design schemes that complement the existing architectural character.",
            "<strong>Inter-war housing:</strong> The area's 1930s semis and detached houses are popular candidates for hip-to-gable loft conversions, side extensions, and modernisation. Under permitted development, many of these works proceed without planning permission outside the conservation area.",
            "<strong>Village character:</strong> Harrow Council places particular emphasis on preserving Pinner's village character. Extensions and alterations must be designed to complement the existing streetscape. We ensure our schemes meet this expectation.",
        ],
        "stats": [
            ("Conservation areas", "Pinner High Street CA"),
            ("Housing type", "Tudor, Edwardian, inter-war"),
            ("Planning authority", "Harrow Council"),
            ("Key postcodes", "HA5"),
        ],
        "faqs": [
            (
                "Do I need planning permission for works in Pinner Conservation Area?",
                "For most external works within the conservation area, yes. The council protects the village character closely. Heritage Statements are required. We prepare applications to the standard Harrow Council expects.",
            ),
            (
                "Can I extend my Edwardian house in Pinner?",
                "Yes, Pinner's generous plots make extensions very feasible. Outside the conservation area, permitted development rights allow significant rear extensions. Within the conservation area, planning permission is required. We advise on the best approach.",
            ),
            (
                "Can I build a loft conversion in Pinner?",
                "Yes, both Edwardian houses and inter-war semis are well suited to loft conversions. Outside the conservation area, dormers under PD are straightforward. We survey your roof and prepare building regulations drawings.",
            ),
            (
                "How much do architectural drawings cost in Pinner?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How does Pinner's village character affect planning?",
                "Harrow Council places strong emphasis on preserving Pinner's village character. Extensions must complement the existing streetscape in terms of scale, materials, and design. We design schemes with this context in mind.",
            ),
        ],
    },
    {
        "name": "Kingston",
        "slug": "kingston",
        "borough": "Kingston upon Thames",
        "borough_slug": "kingston-upon-thames",
        "postcodes": "KT1",
        "character": "Kingston upon Thames is a riverside town in south-west London with a historic market square, diverse housing stock, and excellent transport connections. The town centre's conservation area and riverside location create specific planning constraints.",
        "housing_stock": "Victorian terraces, Edwardian houses, Georgian townhouses, riverside apartments, inter-war semis",
        "conservation_notes": "Kingston Old Town Conservation Area covers the historic market square and surrounding streets",
        "planning_notes": "Royal Borough of Kingston upon Thames applies specific policies for the town centre and riverside. The conservation area imposes additional controls. Riverside properties may require flood risk assessment. The council has clear design standards for residential extensions.",
        "nearby": ["surbiton", "twickenham", "wimbledon", "richmond"],
        "popular_services": ["planning-drawings", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and building regulations for Kingston's period houses and riverside properties. MCIAT chartered, fixed fees, Kingston upon Thames planning expertise built in.",
        "local_context_title": "Why Kingston demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Kingston upon Thames sits in the KT1 postcode within the Royal Borough of Kingston upon Thames. The town's mix of Georgian, Victorian, and Edwardian properties — combined with its riverside setting and historic market square — creates a varied and sometimes complex planning landscape.",
            "<strong>Kingston Old Town Conservation Area:</strong> The conservation area covers the historic market square and surrounding streets, including some fine Georgian and Victorian townhouses. Article 4 Directions may restrict permitted development rights. Heritage Statements are required for external works. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Victorian and Edwardian houses:</strong> Kingston's residential streets contain well-proportioned period houses suitable for loft conversions, rear extensions, and side-return infills. Outside the conservation area, standard permitted development rights apply. We confirm PD eligibility and prepare building regulations drawings.",
            "<strong>Riverside properties:</strong> Properties along the Thames may fall within flood-risk zones. Planning applications must include flood risk assessments, and Building Regulations submissions should address flood resilience. We incorporate these requirements into our drawing packages.",
            "<strong>Design standards:</strong> Kingston Council has clear expectations for residential extension design. We ensure our schemes comply with local guidance on materials, proportions, and streetscape impact.",
        ],
        "stats": [
            ("Conservation areas", "Kingston Old Town CA"),
            ("Housing type", "Georgian, Victorian, Edwardian"),
            ("Planning authority", "RB Kingston upon Thames"),
            ("Key postcodes", "KT1"),
        ],
        "faqs": [
            (
                "Do I need planning permission in Kingston Old Town?",
                "Within the conservation area, planning permission is required for most external works. Article 4 Directions may apply. Heritage Statements must accompany applications. We prepare conservation-sensitive drawings.",
            ),
            (
                "Can I extend my Victorian house in Kingston?",
                "Yes, extensions are common in Kingston. Outside the conservation area, permitted development rights enable rear extensions and loft conversions. Within the conservation area, planning permission is required. We advise on the best approach.",
            ),
            (
                "Are there flood risk issues for Kingston properties?",
                "Riverside properties may be within flood-risk zones. Flood risk assessments are required with planning applications. We handle this requirement as part of our drawing package.",
            ),
            (
                "How much do architectural drawings cost in Kingston?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Kingston Council take for planning decisions?",
                "Kingston targets 8 weeks for householder applications. Conservation area applications may take slightly longer. We manage the full application process.",
            ),
        ],
    },
    {
        "name": "Surbiton",
        "slug": "surbiton",
        "borough": "Kingston upon Thames",
        "borough_slug": "kingston-upon-thames",
        "postcodes": "KT6",
        "character": "Surbiton is a leafy suburban neighbourhood in south-west London with a strong community identity and streets of Victorian and Edwardian houses. Extensions and loft conversions on its well-proportioned family homes are consistently popular.",
        "housing_stock": "Victorian terraces, Edwardian semi-detached houses, inter-war detached, some 1930s semis",
        "conservation_notes": "Surbiton Residential Conservation Area covers several of the neighbourhood's best Victorian and Edwardian streets",
        "planning_notes": "Kingston Council applies specific controls within the conservation area. Outside conservation areas, standard PD rights apply. The council has detailed guidance on extension design, particularly for properties with period character.",
        "nearby": ["kingston", "wimbledon", "teddington"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Surbiton's Victorian and Edwardian family homes. MCIAT chartered, fixed fees, Kingston planning expertise built in.",
        "local_context_title": "Why Surbiton demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Surbiton sits in the KT6 postcode within the Royal Borough of Kingston upon Thames. The neighbourhood's streets of Victorian and Edwardian houses — many with generous gardens and period features — make it one of south-west London's most sought-after family areas.",
            "<strong>Victorian and Edwardian houses:</strong> Surbiton's period houses are well proportioned with good roof voids and adequate garden depths. Rear extensions, loft conversions, and side extensions are all popular project types. We design schemes that respect the existing architectural character while maximising living space.",
            "<strong>Surbiton Residential Conservation Area:</strong> The conservation area covers several of the neighbourhood's finest streets. Article 4 Directions may restrict permitted development rights. Heritage Statements are required for external works. Our MCIAT-chartered team prepares conservation-sensitive applications.",
            "<strong>Permitted development:</strong> Outside conservation areas, Surbiton's houses benefit from standard PD rights. Rear dormers, single-storey extensions, and outbuildings can proceed without planning permission. We confirm eligibility and prepare building regulations drawings.",
            "<strong>Period character:</strong> Kingston Council places emphasis on preserving the period character of Surbiton's streets. Extensions must complement the existing building in terms of materials, proportions, and architectural detailing. We ensure our designs meet these expectations.",
        ],
        "stats": [
            ("Conservation areas", "Surbiton Residential CA"),
            ("Housing type", "Victorian/Edwardian houses"),
            ("Planning authority", "RB Kingston upon Thames"),
            ("Key postcodes", "KT6"),
        ],
        "faqs": [
            (
                "Can I extend my Victorian house in Surbiton?",
                "Yes, extensions are very popular in Surbiton. Outside conservation areas, permitted development enables rear extensions and loft conversions. Within the conservation area, planning permission is required. We advise on the best route.",
            ),
            (
                "Do I need planning permission in Surbiton Conservation Area?",
                "For most external works within the conservation area, yes. Article 4 Directions may apply. Heritage Statements are required. We prepare conservation-sensitive drawings that satisfy Kingston Council.",
            ),
            (
                "Can I build a loft conversion in Surbiton?",
                "Yes, Surbiton's Victorian and Edwardian houses are well suited to loft conversions. Outside conservation areas, rear dormers under PD are straightforward. We survey your roof and confirm eligibility.",
            ),
            (
                "How much do architectural drawings cost in Surbiton?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Kingston take for planning decisions?",
                "Kingston targets 8 weeks for householder applications. Conservation area applications may take slightly longer. We manage the full timeline on your behalf.",
            ),
        ],
    },
    {
        "name": "Norbury",
        "slug": "norbury",
        "borough": "Croydon",
        "borough_slug": "croydon",
        "postcodes": "SW16, CR7",
        "character": "Norbury is an affordable residential neighbourhood straddling the Croydon and Lambeth border, with streets of Victorian terraces, Edwardian houses, and some inter-war properties. Extensions and loft conversions are popular as families seek to maximise space.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, some post-war infill",
        "conservation_notes": "Limited conservation area coverage; Norbury Hill area has some locally listed buildings",
        "planning_notes": "Croydon Council applies standard residential policies. Most properties benefit from full permitted development rights. The council's Place-Specific Guidance provides area-by-area design expectations.",
        "nearby": ["streatham", "crystal-palace", "sydenham"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Norbury's Victorian terraces and family homes. MCIAT chartered, fixed fees, Croydon planning expertise built in.",
        "local_context_title": "Why Norbury demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Norbury straddles the SW16 and CR7 postcodes, primarily within the London Borough of Croydon. The neighbourhood's mix of Victorian terraces, Edwardian houses, and inter-war properties offers excellent potential for extensions and loft conversions at some of south London's most accessible prices.",
            "<strong>Victorian and Edwardian terraces:</strong> Norbury's period terraces are well suited to rear dormers, single-storey rear extensions, and side-return infills. Under permitted development, many of these works can proceed without planning permission. We confirm PD eligibility and prepare building regulations drawings.",
            "<strong>Affordable improvement:</strong> Norbury's relative affordability makes it a popular area for families buying properties to extend and improve. We help homeowners identify the most impactful alterations and navigate the planning and building regulations process efficiently.",
            "<strong>Croydon design guidance:</strong> Croydon Council's Place-Specific Guidance provides area-by-area design expectations. We design schemes that comply with this guidance, improving the chances of first-time approval.",
            "<strong>Permitted development:</strong> Most Norbury properties benefit from full PD rights. Loft conversions, rear extensions, and outbuildings can typically proceed without planning permission. We confirm eligibility and prepare compliant building regulations drawings.",
        ],
        "stats": [
            ("Conservation areas", "Limited"),
            ("Housing type", "Victorian terraces, Edwardian houses"),
            ("Planning authority", "Croydon Council"),
            ("Key postcodes", "SW16, CR7"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Norbury?",
                "Yes, loft conversions are popular in Norbury. Most terraces and semis can add rear dormers under permitted development. We survey your roof, confirm eligibility, and prepare building regulations drawings.",
            ),
            (
                "What size extension can I build in Norbury?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey, and semis up to 6 metres. Larger extensions require planning permission. We confirm the maximum for your property.",
            ),
            (
                "Which council handles planning in Norbury?",
                "Most of Norbury falls within the London Borough of Croydon. Some properties near the northern boundary may fall under Lambeth. We confirm the correct authority before proceeding.",
            ),
            (
                "How much do architectural drawings cost in Norbury?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees with no hidden extras.",
            ),
            (
                "How long does Croydon take for planning decisions?",
                "Croydon Council targets 8 weeks for householder applications. Pre-application advice is available. We manage the application process from start to finish.",
            ),
        ],
    },
    {
        "name": "Crystal Palace",
        "slug": "crystal-palace",
        "borough": "Bromley",
        "borough_slug": "bromley",
        "postcodes": "SE19, SE20",
        "character": "Crystal Palace is a hilltop neighbourhood spanning several borough boundaries, known for its Victorian terraces, panoramic views, and the historic Crystal Palace Park. Its multi-borough location and conservation areas create specific planning challenges.",
        "housing_stock": "Victorian terraces, Edwardian houses, some large villas, post-war infill",
        "conservation_notes": "Crystal Palace Park, Westow Hill Conservation Area, and several neighbouring conservation areas across borough boundaries",
        "planning_notes": "Crystal Palace spans parts of Bromley, Southwark, Lambeth, Lewisham, and Croydon. Identifying the correct planning authority is essential. Conservation area controls vary between boroughs. The hilltop position means roof alterations are visible across wide areas.",
        "nearby": ["sydenham", "forest-hill", "norbury", "herne-hill"],
        "popular_services": ["planning-drawings", "loft-conversions", "house-extensions"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Crystal Palace's Victorian terraces and hilltop properties. MCIAT chartered, fixed fees, multi-borough expertise built in.",
        "local_context_title": "Why Crystal Palace demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Crystal Palace spans the SE19 and SE20 postcodes across parts of five London boroughs — Bromley, Southwark, Lambeth, Lewisham, and Croydon. This multi-borough location creates unique planning challenges, as policies and conservation area controls vary between authorities.",
            "<strong>Multi-borough complexity:</strong> The most important first step for any Crystal Palace project is confirming which planning authority has jurisdiction. The borough boundary runs through residential streets, and neighbouring houses may fall under different councils. Our team identifies the correct authority and tailors the application accordingly.",
            "<strong>Victorian terraces:</strong> Crystal Palace's Victorian terraces are well proportioned with good roof voids and period features. Loft conversions and rear extensions are popular, but the hilltop location means roof alterations are visible across wide areas and may face additional scrutiny from conservation officers.",
            "<strong>Conservation areas:</strong> Several conservation areas cover parts of Crystal Palace, including Westow Hill and areas around Crystal Palace Park. Conservation controls vary between boroughs. Our MCIAT-chartered team navigates these differences and prepares applications to the standard each council expects.",
            "<strong>Hilltop views:</strong> Crystal Palace's elevated position means roof extensions and dormers must be designed with particular care. We ensure designs are sympathetic to the skyline views that make the area distinctive.",
        ],
        "stats": [
            ("Conservation areas", "Westow Hill CA and others"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Multiple boroughs"),
            ("Key postcodes", "SE19, SE20"),
        ],
        "faqs": [
            (
                "Which council handles planning in Crystal Palace?",
                "Crystal Palace spans five boroughs. We confirm which authority covers your property — Bromley, Southwark, Lambeth, Lewisham, or Croydon — before proceeding. Policies differ between boroughs.",
            ),
            (
                "Can I build a loft conversion in Crystal Palace?",
                "Yes, but the hilltop position means roof alterations are visible across wide areas. Conservation area constraints may apply. We design dormers that are sympathetic to the skyline and comply with the relevant borough's standards.",
            ),
            (
                "Do conservation area rules vary between Crystal Palace boroughs?",
                "Yes, each borough applies its own conservation area policies and Article 4 Directions. What is permissible in one borough may require planning permission in another. We check the specific controls for your property.",
            ),
            (
                "How much do architectural drawings cost in Crystal Palace?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "Can I extend my Victorian terrace in Crystal Palace?",
                "Yes, rear extensions are popular on Crystal Palace's terraces. Under permitted development (outside conservation areas), single-storey extensions up to 4 metres are achievable. Within conservation areas, planning permission may be required.",
            ),
        ],
    },
    {
        "name": "Beckenham",
        "slug": "beckenham",
        "borough": "Bromley",
        "borough_slug": "bromley",
        "postcodes": "BR3",
        "character": "Beckenham is a leafy suburban neighbourhood in south London with streets of large Edwardian houses, inter-war semis, and a village-like High Street. Extensions and loft conversions on its substantial family homes are consistently in demand.",
        "housing_stock": "Large Edwardian detached and semi-detached houses, inter-war semis, some Victorian villas",
        "conservation_notes": "Beckenham Town Centre Conservation Area and several residential conservation areas",
        "planning_notes": "Bromley Council applies specific controls within conservation areas. The large plots and generous housing stock make extensions generally feasible. The council has detailed design guidance for residential extensions.",
        "nearby": ["crystal-palace", "sydenham", "forest-hill"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Beckenham's large Edwardian houses and family homes. MCIAT chartered, fixed fees, Bromley planning expertise built in.",
        "local_context_title": "Why Beckenham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Beckenham sits in the BR3 postcode within the London Borough of Bromley. The neighbourhood's tree-lined avenues of large Edwardian houses and well-proportioned inter-war semis make it one of south London's most desirable family areas, with consistent demand for extensions, loft conversions, and modernisation projects.",
            "<strong>Large Edwardian houses:</strong> Beckenham's substantial detached and semi-detached Edwardian houses offer extensive potential for rear extensions, side extensions, loft conversions, and garden studios. The generous plots accommodate larger schemes than are typical closer to central London.",
            "<strong>Conservation areas:</strong> Several conservation areas cover parts of Beckenham, including the Town Centre Conservation Area. Within these zones, planning permission is required for most external alterations. Heritage Statements must accompany applications. Our MCIAT-chartered team prepares conservation-sensitive designs.",
            "<strong>Inter-war semis:</strong> Beckenham's 1930s semis are ideal for hip-to-gable loft conversions, side extensions, and rear extensions. Under permitted development, many of these works proceed without planning permission outside conservation areas.",
            "<strong>Bromley design guidance:</strong> Bromley Council has detailed guidance on residential extension design, covering proportions, materials, and streetscape impact. We ensure our schemes comply from the outset.",
        ],
        "stats": [
            ("Conservation areas", "Beckenham Town Centre CA"),
            ("Housing type", "Large Edwardian houses, inter-war semis"),
            ("Planning authority", "Bromley Council"),
            ("Key postcodes", "BR3"),
        ],
        "faqs": [
            (
                "Can I extend my Edwardian house in Beckenham?",
                "Yes, Beckenham's generous plots make extensions very feasible. Under permitted development, detached houses can build rear extensions up to 8 metres at single storey. Within conservation areas, planning permission is required. We advise on the best approach.",
            ),
            (
                "Do I need planning permission in Beckenham Conservation Area?",
                "For most external works within conservation areas, yes. Heritage Statements are required. Bromley Council expects designs that respect the character of the conservation area. We prepare conservation-sensitive applications.",
            ),
            (
                "Can I build a loft conversion in Beckenham?",
                "Yes, both Edwardian houses and inter-war semis are well suited to loft conversions. Outside conservation areas, dormers under PD are straightforward. We survey your roof and prepare building regulations drawings.",
            ),
            (
                "How much do architectural drawings cost in Beckenham?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees with no hidden charges.",
            ),
            (
                "How long does Bromley take for planning decisions?",
                "Bromley Council targets 8 weeks for householder applications. Conservation area applications may take slightly longer. We manage the full application process.",
            ),
        ],
    },
    {
        "name": "Colliers Wood",
        "slug": "colliers-wood",
        "borough": "Merton",
        "borough_slug": "merton",
        "postcodes": "SW19",
        "character": "Colliers Wood is an affordable residential neighbourhood in south London along the River Wandle, with Victorian terraces, Edwardian houses, and inter-war properties. Its proximity to Wimbledon attracts families seeking value-for-money extensions and loft conversions.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, some post-war estates",
        "conservation_notes": "Wandle Valley Conservation Area covers the riverside corridor",
        "planning_notes": "Merton Council applies standard residential policies. Most properties outside the Wandle Valley Conservation Area benefit from full permitted development rights. Riverside properties may require flood risk assessment.",
        "nearby": ["wimbledon", "raynes-park", "tooting", "streatham"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Colliers Wood's Victorian terraces and riverside properties. MCIAT chartered, fixed fees, Merton planning expertise built in.",
        "local_context_title": "Why Colliers Wood demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Colliers Wood sits in the SW19 postcode within the London Borough of Merton. The neighbourhood's streets of Victorian terraces and Edwardian houses — combined with its riverside setting along the Wandle — offer excellent potential for extensions and loft conversions at more accessible prices than neighbouring Wimbledon.",
            "<strong>Victorian and Edwardian terraces:</strong> Colliers Wood's period terraces are well suited to rear dormers, single-storey rear extensions, and side-return infills. Under permitted development, many of these works can proceed without planning permission. We confirm PD eligibility and prepare building regulations drawings.",
            "<strong>Wandle Valley Conservation Area:</strong> The Wandle Valley Conservation Area covers the riverside corridor. Properties within this zone face additional planning controls. We check each property's status and prepare appropriate applications.",
            "<strong>Riverside properties:</strong> Properties near the River Wandle may fall within flood-risk zones. Flood risk assessments may be required for planning applications. We incorporate these requirements into our submissions.",
            "<strong>Value for space:</strong> Colliers Wood's affordability relative to Wimbledon makes it popular with families buying to improve. We help homeowners maximise their property's potential through well-designed extensions and conversions.",
        ],
        "stats": [
            ("Conservation areas", "Wandle Valley CA"),
            ("Housing type", "Victorian terraces, Edwardian houses"),
            ("Planning authority", "Merton Council"),
            ("Key postcodes", "SW19"),
        ],
        "faqs": [
            (
                "Can I build a loft conversion in Colliers Wood?",
                "Yes, loft conversions are popular in Colliers Wood. Most terraces can add rear dormers under permitted development. We survey your roof, confirm eligibility, and prepare building regulations drawings.",
            ),
            (
                "What size extension can I build in Colliers Wood?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey, and semis up to 6 metres. Larger extensions require planning permission. We confirm the maximum for your property.",
            ),
            (
                "Are there flood risk issues near the River Wandle?",
                "Properties near the River Wandle may be within flood-risk zones. Flood risk assessments may be required with planning applications. We assess your site and incorporate requirements.",
            ),
            (
                "How much do architectural drawings cost in Colliers Wood?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Merton take for planning decisions?",
                "Merton Council targets 8 weeks for householder applications. Pre-application advice is available. We manage the timeline on your behalf.",
            ),
        ],
    },
    {
        "name": "Raynes Park",
        "slug": "raynes-park",
        "borough": "Merton",
        "borough_slug": "merton",
        "postcodes": "SW20",
        "character": "Raynes Park is a quiet suburban neighbourhood in south-west London with streets of 1930s semi-detached houses and some Edwardian properties. Its village atmosphere and good schools make it popular with families seeking extensions and loft conversions.",
        "housing_stock": "1930s semi-detached houses, Edwardian terraces, some detached houses, post-war infill",
        "conservation_notes": "Limited conservation area coverage in the residential streets",
        "planning_notes": "Merton Council applies standard suburban policies. Most properties benefit from full permitted development rights. The council has specific guidance on dormer design and extension proportions in its residential extensions SPD.",
        "nearby": ["wimbledon", "colliers-wood", "kingston", "surbiton"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Raynes Park's 1930s semis and family homes. MCIAT chartered, fixed fees, Merton planning expertise built in.",
        "local_context_title": "Why Raynes Park demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Raynes Park sits in the SW20 postcode within the London Borough of Merton. The neighbourhood's tree-lined streets of 1930s semi-detached houses and Edwardian properties make it a popular family area with consistent demand for extensions and loft conversions.",
            "<strong>1930s semis:</strong> Raynes Park's inter-war semis are ideal for hip-to-gable loft conversions, side extensions, and rear extensions. The typical hipped roof can be squared off and a rear dormer added to create a generous loft room. Under permitted development, these works can proceed without planning permission.",
            "<strong>Edwardian properties:</strong> The area's Edwardian houses offer good roof voids for loft conversions and adequate garden depths for rear extensions. We design schemes that respect the period character while maximising usable space.",
            "<strong>Merton design guidance:</strong> Merton Council has published an SPD on residential extensions with specific guidance on dormer design, extension depths, and materials. We design schemes that comply with this guidance from the outset.",
            "<strong>Permitted development:</strong> Most Raynes Park properties enjoy full PD rights. We confirm eligibility, prepare building regulations drawings, and manage any prior notification required for larger extensions.",
        ],
        "stats": [
            ("Conservation areas", "Limited"),
            ("Housing type", "1930s semis, Edwardian houses"),
            ("Planning authority", "Merton Council"),
            ("Key postcodes", "SW20"),
        ],
        "faqs": [
            (
                "Can I build a hip-to-gable loft conversion in Raynes Park?",
                "Yes, hip-to-gable loft conversions are very popular on Raynes Park's 1930s semis. Under permitted development, these typically proceed without planning permission. We survey your roof and prepare building regulations drawings.",
            ),
            (
                "What size extension can I build in Raynes Park?",
                "Under permitted development, semi-detached houses can build single-storey rear extensions up to 6 metres. Two-storey rear extensions up to 3 metres are also possible under PD. We confirm the maximum for your property.",
            ),
            (
                "What are Merton's rules on dormer design?",
                "Merton's SPD requires dormers to be set back from the eaves, set in from party walls, and subordinate to the existing roof. Materials must match the existing roof covering. We design compliant dormers.",
            ),
            (
                "How much do architectural drawings cost in Raynes Park?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "Do I need party wall agreements for a side extension?",
                "If your extension involves work on or near a shared boundary, party wall agreements may be needed. This is separate from planning and building regulations. We advise and recommend specialist surveyors.",
            ),
        ],
    },
    {
        "name": "Northfields",
        "slug": "northfields",
        "borough": "Ealing",
        "borough_slug": "ealing",
        "postcodes": "W13",
        "character": "Northfields is a residential neighbourhood in west London centred on the Piccadilly line station, with streets of well-maintained Edwardian terraces and inter-war houses. Extensions and loft conversions are consistently popular.",
        "housing_stock": "Edwardian terraces, inter-war semi-detached houses, some 1930s detached",
        "conservation_notes": "Northfields Conservation Area covers the streets immediately surrounding the station",
        "planning_notes": "Ealing Council applies specific controls within the Northfields Conservation Area. Outside the conservation area, standard permitted development rights apply. The council has clear guidance on dormer design and extension proportions.",
        "nearby": ["hanwell", "acton", "southall", "chiswick"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Northfields' Edwardian terraces and family homes. MCIAT chartered, fixed fees, Ealing planning expertise built in.",
        "local_context_title": "Why Northfields demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Northfields sits in the W13 postcode within the London Borough of Ealing. The neighbourhood's well-maintained streets of Edwardian terraces and inter-war houses — centred on the Piccadilly line station — make it one of west London's most popular family areas.",
            "<strong>Edwardian terraces:</strong> Northfields' Edwardian terraces are among the best preserved in Ealing, with decorative features, good room proportions, and generous roof voids. Rear dormers and single-storey rear extensions are the most popular project types. We design schemes that respect the period character while maximising interior space.",
            "<strong>Northfields Conservation Area:</strong> The conservation area covers the streets immediately surrounding the station. Article 4 Directions restrict permitted development rights, meaning planning permission is required for dormer conversions, window replacements, and front alterations. Heritage Statements must accompany applications. Our MCIAT-chartered team prepares conservation-sensitive designs.",
            "<strong>Inter-war housing:</strong> Northfields' 1930s semis and detached houses are suitable for hip-to-gable loft conversions, side extensions, and rear extensions. Outside the conservation area, these can often proceed under permitted development.",
            "<strong>Ealing design standards:</strong> Ealing Council has clear design expectations for residential extensions. We ensure our schemes comply with local guidance on materials, proportions, and streetscape impact.",
        ],
        "stats": [
            ("Conservation areas", "Northfields CA"),
            ("Housing type", "Edwardian terraces, inter-war semis"),
            ("Planning authority", "Ealing Council"),
            ("Key postcodes", "W13"),
        ],
        "faqs": [
            (
                "Do I need planning permission in Northfields Conservation Area?",
                "For most external works within the conservation area, yes. Article 4 Directions restrict permitted development rights. Dormers, window replacements, and front alterations require planning permission. We prepare conservation-sensitive applications.",
            ),
            (
                "Can I build a loft conversion in Northfields?",
                "Yes, Northfields' Edwardian terraces have excellent loft conversion potential. Outside the conservation area, rear dormers under PD are straightforward. Within the conservation area, planning permission is required. We survey your roof and advise.",
            ),
            (
                "What size extension can I build in Northfields?",
                "Under permitted development, terraced houses can extend up to 4 metres at single storey. Within the conservation area, planning permission is required. We confirm the maximum achievable for your property.",
            ),
            (
                "How much do architectural drawings cost in Northfields?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Ealing take for planning decisions?",
                "Ealing Council targets 8 weeks for householder applications. Conservation area applications may take slightly longer. We manage the full application process.",
            ),
        ],
    },
    # -----------------------------------------------------------------------
    # Batch 3 — 40 additional neighbourhoods
    # -----------------------------------------------------------------------
    {
        "name": "Greenwich",
        "slug": "greenwich",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE10",
        "character": "Greenwich is a UNESCO World Heritage neighbourhood defined by Georgian and early Victorian streets around the Royal Park, the Naval College, and the Cutty Sark. Residential projects sit within one of London's most tightly protected heritage settings.",
        "housing_stock": "Georgian terraces, early Victorian townhouses, Maritime Greenwich listed buildings, converted riverside warehouses",
        "conservation_notes": "West Greenwich, East Greenwich, Ashburnham Triangle, and Maritime Greenwich Conservation Areas. World Heritage Site buffer zone applies.",
        "planning_notes": "Royal Borough of Greenwich applies strict heritage controls throughout SE10. Article 4 Directions cover most central streets. Maritime Greenwich World Heritage Site status means all visible alterations require heritage justification.",
        "nearby": ["blackheath", "deptford", "charlton", "greenwich-peninsula"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and building regulations for Greenwich's Georgian streets, listed properties, and World Heritage-adjacent homes. MCIAT chartered, fixed fees, conservation expertise built in.",
        "local_context_title": "Why Greenwich demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Greenwich occupies the southern bank of the Thames in the SE10 postcode within the Royal Borough of Greenwich. The neighbourhood's Georgian terraces, the Royal Park, the Old Royal Naval College, and the Queen's House together form the Maritime Greenwich UNESCO World Heritage Site — one of only four World Heritage Sites in London.",
            "<strong>World Heritage Site constraints:</strong> Any proposal visible from the World Heritage Site or within its buffer zone must demonstrate that it preserves the Outstanding Universal Value of the site. Greenwich Council requires detailed Heritage Impact Assessments, verified views, and material sample boards. Our MCIAT-chartered team has extensive experience preparing applications in this sensitive context.",
            "<strong>Georgian and Victorian housing:</strong> The streets of West Greenwich and Ashburnham Triangle contain some of London's finest preserved Georgian and early Victorian terraces. Rear extensions, loft conversions, and basement works are achievable, but every scheme must respect the period character. Sash windows, stock brick facades, and original roof profiles are protected elements.",
            "<strong>Article 4 coverage:</strong> Most of central Greenwich is covered by Article 4 Directions that remove permitted development rights for external alterations. Planning permission is required for dormers, window replacements, rooflights, front boundary changes, and side extensions. We prepare conservation-sensitive submissions tailored to Greenwich's heritage officers.",
            "<strong>Listed buildings:</strong> A significant proportion of Greenwich housing stock is listed — Grade II is common, with Grade II* and Grade I on key streets. Listed Building Consent runs in parallel with planning permission. We handle both applications and coordinate with Historic England where required.",
        ],
        "stats": [
            ("Conservation areas", "4 CAs + WHS buffer"),
            ("Listed buildings", "Hundreds (Grade II to I)"),
            ("Planning authority", "Royal Borough of Greenwich"),
            ("Key postcodes", "SE10"),
        ],
        "faqs": [
            (
                "Can I extend my Georgian house in Greenwich?",
                "Often yes, but every scheme requires planning permission and Listed Building Consent where applicable. Rear extensions must respect the Georgian proportions and use matching materials. We prepare the heritage-sensitive drawings and manage the full application through Greenwich Council.",
            ),
            (
                "What are the rules within the Maritime Greenwich World Heritage Site?",
                "Proposals within or visible from the World Heritage Site must demonstrate that Outstanding Universal Value is preserved. Heritage Impact Assessments, verified views, and detailed material specifications are required. We prepare WHS-compliant applications.",
            ),
            (
                "Do I need planning permission for a loft conversion in Greenwich?",
                "Within the conservation areas and Article 4 zones — yes. Dormers, rooflights, and hip-to-gable alterations all require planning permission. Outside the Article 4 zones, permitted development may still apply. We assess your property early.",
            ),
            (
                "How much do architectural drawings cost in Greenwich?",
                "Our Essentials package starts from £840. For listed buildings and World Heritage Site projects, the Complete package from £1,750 is typically needed to cover Heritage Statements and coordination with Historic England.",
            ),
            (
                "How long does Greenwich Council take to decide applications?",
                "Greenwich targets 8 weeks for householder applications and 13 weeks for complex or listed building schemes. Pre-application advice is strongly recommended for WHS-adjacent projects. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Blackfen",
        "slug": "blackfen",
        "borough": "Bexley",
        "borough_slug": "bexley",
        "postcodes": "DA15",
        "character": "Blackfen is a suburban residential neighbourhood in the London Borough of Bexley, characterised by 1930s semi-detached houses and bungalows on wide streets. Rear extensions, loft conversions, and side extensions are the dominant project types.",
        "housing_stock": "1930s semi-detached houses, inter-war bungalows, small post-war developments",
        "conservation_notes": "No conservation area coverage in Blackfen itself",
        "planning_notes": "Bexley Council applies standard planning policies. Permitted development rights are intact for most properties, making many extensions and conversions possible without planning permission.",
        "nearby": ["sidcup", "welling", "bexleyheath", "eltham"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, rear extensions, and loft conversions for Blackfen's 1930s semis and bungalows. MCIAT chartered, fixed fees, Bexley planning expertise built in.",
        "local_context_title": "Why Blackfen demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Blackfen sits in the DA15 postcode within the London Borough of Bexley, bordering Sidcup to the south and Welling to the north. The neighbourhood's 1930s housing stock and wide plot sizes make it one of south-east London's most extension-friendly areas.",
            "<strong>1930s semi-detached stock:</strong> The majority of Blackfen's housing is inter-war semi-detached with generous rear gardens and hipped roofs. These properties are ideal for hip-to-gable loft conversions, rear extensions, and side infills. We design schemes that maximise space while respecting the original character.",
            "<strong>Permitted development:</strong> Outside conservation areas, most Blackfen properties retain full permitted development rights. Rear extensions up to 6m (detached) or 4m (semi) under prior approval, hip-to-gable loft conversions under Class B, and two-storey side extensions in many cases. We confirm your PD eligibility and prepare the required drawings.",
            "<strong>Bexley planning standards:</strong> Bexley Council has clear design guidance emphasising subordinate, matching materials and respect for the existing streetscape. Applications that demonstrate compliance with council guidance typically receive straightforward approval.",
            "<strong>Bungalow conversions:</strong> Blackfen has a notable stock of 1930s bungalows. Converting the loft to create a first floor — or adding a full first-floor extension — is a popular way to increase family space without moving. Structural calculations and careful massing are essential.",
        ],
        "stats": [
            ("Conservation areas", "None in Blackfen"),
            ("Housing type", "1930s semis, bungalows"),
            ("Planning authority", "Bexley Council"),
            ("Key postcodes", "DA15"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a rear extension in Blackfen?",
                "In most cases, no. Rear extensions up to 6m (detached) or 4m (semi-detached) from the original rear wall can proceed under permitted development with a prior notification. Larger extensions or those in conservation areas require planning permission. We confirm your position and prepare drawings.",
            ),
            (
                "Can I convert my bungalow loft in Blackfen?",
                "Yes — bungalow loft conversions are common in Blackfen. A hip-to-gable conversion with a rear dormer is the typical pattern, and often falls within permitted development. Structural calculations are essential. We prepare the full drawing package.",
            ),
            (
                "What are Bexley Council's design requirements?",
                "Bexley emphasises subordinate extensions, matching materials, and respect for the streetscape. Two-storey side extensions must be set back and down from the main roof. We design to Bexley's published guidance.",
            ),
            (
                "How much do architectural drawings cost in Blackfen?",
                "Our Essentials package starts from £840 for a single planning or building regulations submission. The Complete package from £1,750 covers both plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Bexley take to decide planning applications?",
                "Bexley targets 8 weeks for householder applications. Lawful Development Certificates and prior approval notifications are typically faster. We manage the full application timeline.",
            ),
        ],
    },
    {
        "name": "Welling",
        "slug": "welling",
        "borough": "Bexley",
        "borough_slug": "bexley",
        "postcodes": "DA16",
        "character": "Welling is a suburban residential area in the London Borough of Bexley with a mix of 1930s semis, post-war housing, and small pockets of Victorian terraces. The neighbourhood is a steady source of loft, extension, and garage conversion work.",
        "housing_stock": "1930s semi-detached houses, post-war semis, small Victorian terraces, some 1970s detached",
        "conservation_notes": "No conservation area coverage in Welling itself",
        "planning_notes": "Bexley Council applies standard planning policies. Permitted development rights are generally intact outside any small conservation area pockets.",
        "nearby": ["blackfen", "bexleyheath", "eltham", "plumstead"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and garage conversions for Welling's 1930s and post-war homes. MCIAT chartered, fixed fees, Bexley planning expertise built in.",
        "local_context_title": "Why Welling demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Welling sits in the DA16 postcode within the London Borough of Bexley, centred on Welling High Street and the surrounding residential streets. The mix of 1930s semis and post-war housing generates consistent demand for extensions and loft conversions.",
            "<strong>1930s and post-war stock:</strong> Welling's housing stock is dominated by inter-war and post-war semis on standard plots. These properties typically have rear gardens suitable for 4–6m rear extensions and hipped roofs suitable for hip-to-gable loft conversions. We design schemes that add a full bedroom, en-suite, or open-plan kitchen-diner.",
            "<strong>Garage conversions:</strong> Many Welling properties have attached garages that are no longer used for parking. Converting the garage to habitable space — study, playroom, or extra bedroom — is a cost-effective way to add 12–15 square metres. We prepare the building regulations drawings required for the conversion.",
            "<strong>Permitted development:</strong> Outside any small conservation area pockets, Welling properties retain full PD rights. Rear extensions under prior approval, loft conversions under Class B, and two-storey side extensions within certain parameters. We confirm your eligibility and prepare the necessary drawings.",
            "<strong>Bexley's design expectations:</strong> Bexley Council publishes clear guidance on residential extensions. Two-storey side extensions should be set back and down. Roof extensions should match the existing roof profile. We design to these standards.",
        ],
        "stats": [
            ("Conservation areas", "None in Welling"),
            ("Housing type", "1930s and post-war semis"),
            ("Planning authority", "Bexley Council"),
            ("Key postcodes", "DA16"),
        ],
        "faqs": [
            (
                "Do I need planning permission for a garage conversion in Welling?",
                "Usually no — garage conversions within the existing footprint typically fall within permitted development. However, Building Regulations approval is always required to address thermal performance, ventilation, and structural changes. We prepare the building regs drawings.",
            ),
            (
                "Can I build a two-storey extension in Welling?",
                "Often yes. Two-storey rear extensions up to 3m are permitted development in many cases. Two-storey side extensions may require planning permission depending on proportions. We confirm the position and prepare appropriate drawings.",
            ),
            (
                "What about loft conversions in Welling?",
                "Welling's inter-war semis are ideal for hip-to-gable loft conversions with rear dormers. Most fall within PD. We design schemes that maximise headroom and include the structural calculations.",
            ),
            (
                "How much do architectural drawings cost in Welling?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Bexley Council take to decide?",
                "Bexley targets 8 weeks for householder applications and faster for LDCs and prior approval notifications. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Sidcup",
        "slug": "sidcup",
        "borough": "Bexley",
        "borough_slug": "bexley",
        "postcodes": "DA14",
        "character": "Sidcup is a residential town centre in the south of the London Borough of Bexley, with a mix of Edwardian villas, 1930s semis, and some more recent developments. The neighbourhood's larger plots make substantial extensions and full loft conversions possible.",
        "housing_stock": "Edwardian villas, 1930s semi-detached houses, post-war and 1970s detached, small pockets of modern developments",
        "conservation_notes": "Sidcup Place Conservation Area; small areas near the High Street",
        "planning_notes": "Bexley Council applies standard policies outside conservation areas. Within the Sidcup Place CA, heritage considerations apply. Most residential streets retain full permitted development rights.",
        "nearby": ["blackfen", "welling", "mottingham", "bexleyheath"],
        "popular_services": ["house-extensions", "loft-conversions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Sidcup's Edwardian villas and family homes. MCIAT chartered, fixed fees, Bexley planning expertise built in.",
        "local_context_title": "Why Sidcup demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Sidcup sits in the DA14 postcode in the south of the London Borough of Bexley. The town centre mixes retail and residential, while the surrounding streets contain some of Bexley's most substantial family homes.",
            "<strong>Edwardian villas:</strong> Sidcup has a stock of handsome Edwardian villas with generous room proportions, bay windows, and good roof voids. These properties are prime candidates for loft conversions and rear extensions. We respect the period character while creating modern family space.",
            "<strong>1930s semis:</strong> Much of residential Sidcup is 1930s semi-detached on generous plots. Hip-to-gable loft conversions with rear dormers, and 4m rear extensions under PD, are the most common projects. We prepare drawings efficiently using the prior approval route where it applies.",
            "<strong>Sidcup Place Conservation Area:</strong> This small CA around Sidcup Place requires heritage-sensitive design. Article 4 Directions may apply. We prepare conservation-sensitive applications that meet Bexley's heritage officer expectations.",
            "<strong>Larger plots:</strong> Sidcup's larger detached plots — particularly in the south — are suitable for substantial side and rear extensions, wraparounds, and even outbuildings used as home offices or studios. We design schemes that take advantage of the available space.",
        ],
        "stats": [
            ("Conservation areas", "Sidcup Place CA"),
            ("Housing type", "Edwardian villas, 1930s semis"),
            ("Planning authority", "Bexley Council"),
            ("Key postcodes", "DA14"),
        ],
        "faqs": [
            (
                "Can I extend my Edwardian villa in Sidcup?",
                "Yes — Edwardian villas are well-suited to rear and side-return extensions. Most fall within permitted development outside the conservation area. We design schemes that respect the period character.",
            ),
            (
                "Do I need planning permission for a wraparound extension?",
                "Wraparound extensions typically need a mix of PD and planning permission. The rear portion may fall within PD; the side portion beyond half the original width requires planning permission. We prepare the applications.",
            ),
            (
                "What's achievable on a Sidcup 1930s semi?",
                "A lot — hip-to-gable loft conversion, 4m rear extension, and sometimes a two-storey side extension, all potentially within PD. We maximise the achievable footprint.",
            ),
            (
                "How much do architectural drawings cost in Sidcup?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Bexley Council take to decide?",
                "Bexley targets 8 weeks for householder applications. Lawful Development Certificates take approximately 8 weeks. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Bromley Town Centre",
        "slug": "bromley",
        "borough": "Bromley",
        "borough_slug": "bromley",
        "postcodes": "BR1",
        "character": "Bromley town centre and the surrounding BR1 streets combine Victorian terraces, Edwardian villas, and mid-century family houses. The area sees consistent demand for extensions, loft conversions, and flat conversions.",
        "housing_stock": "Victorian terraces, Edwardian villas, 1930s semis, post-war detached",
        "conservation_notes": "Bromley Town Conservation Area; Martins Hill Conservation Area",
        "planning_notes": "Bromley Council applies standard policies with heritage controls in the town centre conservation area. Most residential streets outside the CA retain full permitted development rights.",
        "nearby": ["chislehurst", "beckenham", "west-wickham", "orpington"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, extensions, loft conversions, and building regulations for Bromley's Victorian terraces, Edwardian villas, and family homes. MCIAT chartered, fixed fees, Bromley planning expertise built in.",
        "local_context_title": "Why Bromley demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Bromley town centre and its surrounding residential streets occupy the BR1 postcode in the London Borough of Bromley. The mix of Victorian terraces, Edwardian villas, and mid-century houses — combined with one of south-east London's most active town centres — generates consistent residential project demand.",
            "<strong>Victorian terraces:</strong> The streets around Bromley South and Bromley North stations contain good stocks of Victorian terraces. Rear extensions, side-return infills, and rear dormer loft conversions are the typical patterns. We design schemes that add kitchen-dining space or an extra bedroom.",
            "<strong>Edwardian villas:</strong> Bromley's Edwardian stock, particularly in the streets east and south of the town centre, offers excellent extension potential. Side-return extensions, loft conversions, and occasionally basement works are the main project types.",
            "<strong>Bromley Town Conservation Area:</strong> The CA covers the historic core around Market Square and the High Street. Heritage-sensitive design is essential, and Article 4 Directions may apply. We prepare conservation-sensitive submissions for Bromley Council's heritage team.",
            "<strong>Flat conversions:</strong> Many larger Victorian and Edwardian houses have been converted to flats. Further subdivision requires planning permission and compliance with Bromley's housing standards, including minimum space standards and amenity requirements.",
        ],
        "stats": [
            ("Conservation areas", "Bromley Town CA, Martins Hill CA"),
            ("Housing type", "Victorian/Edwardian, 1930s"),
            ("Planning authority", "Bromley Council"),
            ("Key postcodes", "BR1"),
        ],
        "faqs": [
            (
                "Can I build a rear extension on my Bromley Victorian terrace?",
                "Yes — rear extensions up to 3m (terrace) under PD, or 6m under prior approval. Within the conservation area, planning permission is required. We prepare drawings for either route.",
            ),
            (
                "Do I need planning permission for a loft conversion in BR1?",
                "Outside the conservation area, rear dormers under PD are straightforward. Within the CA, planning permission is required. We confirm your position and prepare the drawings.",
            ),
            (
                "What's required to convert a Bromley house into flats?",
                "Planning permission from Bromley Council plus full Building Regulations approval. Each flat must meet minimum space standards. Sound insulation and fire separation are critical. We prepare the full drawing package.",
            ),
            (
                "How much do architectural drawings cost in Bromley?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Fixed fees throughout.",
            ),
            (
                "How long does Bromley Council take to decide?",
                "Bromley targets 8 weeks for householder applications and 13 weeks for major schemes. Conservation area applications may take slightly longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "West Wickham",
        "slug": "west-wickham",
        "borough": "Bromley",
        "borough_slug": "bromley",
        "postcodes": "BR4",
        "character": "West Wickham is a leafy suburban neighbourhood on the southern edge of Greater London, dominated by 1930s semi-detached houses and post-war bungalows on generous plots. Extensions and loft conversions are the staple project types.",
        "housing_stock": "1930s semi-detached houses, inter-war bungalows, post-war detached, some newer developments",
        "conservation_notes": "No conservation area coverage in West Wickham itself",
        "planning_notes": "Bromley Council applies standard policies. Permitted development rights are intact. The council publishes clear guidance on extensions and loft conversions.",
        "nearby": ["bromley", "beckenham", "sanderstead", "purley"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, rear extensions, and loft conversions for West Wickham's 1930s semis and bungalows. MCIAT chartered, fixed fees, Bromley planning expertise built in.",
        "local_context_title": "Why West Wickham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "West Wickham sits in the BR4 postcode in the south of the London Borough of Bromley, on the border with Croydon. The leafy streets, 1930s semis, and bungalows make this one of south London's most consistent extension markets.",
            "<strong>1930s semi-detached stock:</strong> The majority of West Wickham's housing is inter-war semi-detached on standard plots. These properties typically have rear gardens suitable for 4m+ extensions and hipped roofs suitable for hip-to-gable loft conversions with rear dormers.",
            "<strong>Bungalow conversions:</strong> West Wickham has a notable stock of 1930s bungalows. Loft conversions — adding a first floor via a full raise-the-roof or dormer — are popular. Full first-floor extensions are also achievable where the original roof allows.",
            "<strong>Permitted development:</strong> Outside conservation areas, most West Wickham properties retain full PD rights. Rear extensions under prior approval, loft conversions under Class B, and two-storey side extensions within parameters. We confirm eligibility and prepare drawings.",
            "<strong>Bromley design guidance:</strong> Bromley Council publishes clear design expectations. Two-storey side extensions must be subordinate and set back. Roof extensions should match existing materials. We design to these standards.",
        ],
        "stats": [
            ("Conservation areas", "None in West Wickham"),
            ("Housing type", "1930s semis, bungalows"),
            ("Planning authority", "Bromley Council"),
            ("Key postcodes", "BR4"),
        ],
        "faqs": [
            (
                "Can I add a first floor to my bungalow in West Wickham?",
                "Often yes — it depends on whether the addition falls within PD or requires planning permission. We assess the height, volume, and material constraints of Class A/B permitted development and advise the right route.",
            ),
            (
                "Do I need planning permission for a rear extension?",
                "In most cases no — rear extensions up to 6m (detached) or 4m (semi) fall within PD with prior approval. Larger schemes need planning permission. We confirm and prepare drawings.",
            ),
            (
                "What about loft conversions in West Wickham?",
                "Hip-to-gable loft conversions with rear dormers are the standard pattern and usually fall within PD. We prepare the planning notification and full building regs drawings.",
            ),
            (
                "How much do architectural drawings cost in West Wickham?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Bromley take to decide applications?",
                "Bromley targets 8 weeks for householder applications. Lawful Development Certificates are typically similar. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Chislehurst",
        "slug": "chislehurst",
        "borough": "Bromley",
        "borough_slug": "bromley",
        "postcodes": "BR7",
        "character": "Chislehurst is a historic, tightly controlled conservation-area neighbourhood in the London Borough of Bromley, with Georgian and Victorian villas, large detached family homes, and protected common land. Heritage-sensitive drawings are essential.",
        "housing_stock": "Georgian and Victorian villas, Edwardian family houses, inter-war detached, some substantial modern builds",
        "conservation_notes": "Chislehurst Conservation Area covers almost the entire neighbourhood; Article 4 Directions apply",
        "planning_notes": "Bromley Council applies strict heritage controls throughout Chislehurst. Article 4 Directions remove most permitted development rights. Design & Access Statements and Heritage Statements are required for most applications.",
        "nearby": ["bromley", "mottingham", "orpington", "sidcup"],
        "popular_services": ["planning-drawings", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and building regulations for Chislehurst's Georgian villas and period family homes. MCIAT chartered, fixed fees, Bromley conservation expertise built in.",
        "local_context_title": "Why Chislehurst demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Chislehurst sits in the BR7 postcode within the London Borough of Bromley, around Chislehurst Common and the historic High Street. The neighbourhood's almost complete conservation area coverage and protected commons make it one of the most tightly controlled suburban planning environments in south London.",
            "<strong>Chislehurst Conservation Area:</strong> The CA covers almost the entire neighbourhood. Article 4 Directions remove permitted development rights for most external alterations — extensions, roof changes, window replacements, and boundary treatments all typically require full planning permission. Our MCIAT-chartered team prepares conservation-grade applications that meet Bromley's heritage officer expectations.",
            "<strong>Georgian and Victorian stock:</strong> Chislehurst contains some of south London's most substantial period houses. These properties often have heritage features — sash windows, original joinery, and stock brick facades — that must be preserved. Our drawings include detailed material specifications.",
            "<strong>Protected common land:</strong> Properties backing onto or near Chislehurst Common face additional scrutiny. Views into and out of the common are protected. We prepare verified views and streetscape drawings where required.",
            "<strong>Tree Preservation Orders:</strong> Chislehurst has extensive TPO coverage. Any works affecting protected trees require separate consent from the council. We coordinate with arboricultural consultants where the site involves mature trees.",
        ],
        "stats": [
            ("Conservation areas", "Chislehurst CA (near-complete)"),
            ("Article 4", "Yes"),
            ("Planning authority", "Bromley Council"),
            ("Key postcodes", "BR7"),
        ],
        "faqs": [
            (
                "Do I need planning permission for an extension in Chislehurst?",
                "Almost certainly yes. Article 4 Directions remove permitted development rights throughout the conservation area. Even modest extensions, window replacements, and boundary changes typically need full planning permission. We prepare heritage-sensitive applications.",
            ),
            (
                "Can I do a loft conversion in Chislehurst?",
                "Loft conversions are possible but usually require full planning permission. Dormer design must be subordinate to the original roof and sympathetic to the streetscape. Rooflights are often preferred. We design appropriate schemes.",
            ),
            (
                "What's required for a Chislehurst planning application?",
                "Most applications require full planning drawings, Design & Access Statement, Heritage Statement, and often accurate streetscape and site context drawings. Our Complete package from £1,750 includes all this.",
            ),
            (
                "How much do architectural drawings cost in Chislehurst?",
                "For conservation-area projects, the Complete package from £1,750 is typically required to cover the Heritage Statement and detailed drawings. Essentials from £840 may suffice for very minor schemes.",
            ),
            (
                "How long does Bromley Council take to decide in Chislehurst?",
                "Chislehurst applications typically take 8–13 weeks. Heritage consultation adds time. Pre-application advice is recommended. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Orpington",
        "slug": "orpington",
        "borough": "Bromley",
        "borough_slug": "bromley",
        "postcodes": "BR6",
        "character": "Orpington is an outer London suburban town in the south of the London Borough of Bromley, dominated by 1930s and post-war semi-detached houses, detached family homes, and larger modern plots. Extensions and loft conversions are the mainstream project types.",
        "housing_stock": "1930s semis, post-war detached, inter-war bungalows, some Victorian pockets",
        "conservation_notes": "Orpington High Street has small conservation pockets; residential streets are largely unprotected",
        "planning_notes": "Bromley Council applies standard policies. Permitted development rights are intact for the vast majority of Orpington properties.",
        "nearby": ["bromley", "chislehurst", "west-wickham", "sidcup"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, rear extensions, and loft conversions for Orpington's 1930s semis and family homes. MCIAT chartered, fixed fees, Bromley planning expertise built in.",
        "local_context_title": "Why Orpington demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Orpington sits in the BR6 postcode in the south of the London Borough of Bromley, at the edge of the Greater London boundary. The town's extensive 1930s and post-war housing stock makes it one of south-east London's most consistent extension markets.",
            "<strong>1930s semi-detached stock:</strong> Much of Orpington is inter-war semi-detached on generous plots. Hip-to-gable loft conversions, 4–6m rear extensions, and two-storey side extensions are the core project mix. Most fall within permitted development.",
            "<strong>Detached family homes:</strong> Orpington's detached stock — particularly in the streets south and east of the town centre — offers substantial extension potential. Wraparounds, double-storey rear extensions, and garage conversions are all common.",
            "<strong>Bungalow upgrades:</strong> Orpington has a significant bungalow stock. Adding a first floor — via raise-the-roof loft conversion or full first-floor extension — is a popular way to create family homes from smaller bungalows. Structural calculations are critical.",
            "<strong>Permitted development:</strong> Outside the small town centre conservation pockets, Orpington properties retain full PD rights. We maximise the achievable scheme under PD where possible, saving time and cost.",
        ],
        "stats": [
            ("Conservation areas", "Small pockets"),
            ("Housing type", "1930s semis, post-war detached"),
            ("Planning authority", "Bromley Council"),
            ("Key postcodes", "BR6"),
        ],
        "faqs": [
            (
                "Can I build a two-storey extension in Orpington?",
                "Often yes. Two-storey rear extensions up to 3m are PD in many cases. Two-storey side extensions need planning permission once they exceed half the original width. We confirm and prepare drawings.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "For most Orpington properties outside the small conservation pockets — no. Rear dormers and hip-to-gable conversions typically fall within PD. We prepare the Lawful Development Certificate and building regs drawings.",
            ),
            (
                "What about bungalow first-floor additions?",
                "These can fall within PD depending on height and volume, or may require planning permission. We assess early and prepare either submission.",
            ),
            (
                "How much do architectural drawings cost in Orpington?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Bromley Council take to decide?",
                "Bromley targets 8 weeks for householder applications. Most Orpington applications are straightforward. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Sanderstead",
        "slug": "sanderstead",
        "borough": "Croydon",
        "borough_slug": "croydon",
        "postcodes": "CR2",
        "character": "Sanderstead is a leafy residential neighbourhood in the south of the London Borough of Croydon, characterised by inter-war detached houses and 1930s semis on generous plots. Extensions, loft conversions, and outbuildings are the common project types.",
        "housing_stock": "1930s detached houses, inter-war semis, post-war detached, some 1970s developments",
        "conservation_notes": "Sanderstead Conservation Area covers a small central area",
        "planning_notes": "Croydon Council applies standard policies outside the conservation area. The council has been responsive to well-designed householder applications and supports outbuildings, extensions, and loft conversions on standard PD terms.",
        "nearby": ["purley", "west-wickham", "thornton-heath", "south-norwood"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Sanderstead's 1930s family homes and detached houses. MCIAT chartered, fixed fees, Croydon planning expertise built in.",
        "local_context_title": "Why Sanderstead demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Sanderstead sits in the CR2 postcode in the south of the London Borough of Croydon, on the border with Surrey. The leafy streets, generous plots, and 1930s family housing make it one of south Croydon's most extension-friendly neighbourhoods.",
            "<strong>1930s detached stock:</strong> Sanderstead has a significant stock of inter-war detached houses on generous plots. These properties can often accommodate substantial rear extensions, side extensions, and loft conversions — frequently within permitted development.",
            "<strong>Loft conversions:</strong> The typical 1930s hipped roof in Sanderstead is ideal for a hip-to-gable conversion with a rear dormer. We design schemes that add a bedroom suite or home office.",
            "<strong>Outbuildings:</strong> Larger Sanderstead gardens are well-suited to substantial outbuildings — garden offices, gym studios, annexes. Most fall within PD under Class E if the height and coverage rules are met. We prepare the building regs drawings where required.",
            "<strong>Sanderstead Conservation Area:</strong> A small CA covers the central historic core. Within the CA, planning permission is required for most external works. Outside the CA, PD rights are intact.",
        ],
        "stats": [
            ("Conservation areas", "Sanderstead CA (small)"),
            ("Housing type", "1930s detached, semis"),
            ("Planning authority", "Croydon Council"),
            ("Key postcodes", "CR2"),
        ],
        "faqs": [
            (
                "Can I build a garden office in Sanderstead?",
                "Usually yes — outbuildings under Class E permitted development are achievable on most Sanderstead plots. Height, position, and use restrictions apply. We prepare drawings and confirm PD eligibility.",
            ),
            (
                "Do I need planning permission for a rear extension?",
                "For most Sanderstead properties outside the CA — no. Rear extensions up to 6m (detached) under prior approval. We prepare the notification and drawings.",
            ),
            (
                "What about loft conversions?",
                "Hip-to-gable loft conversions with rear dormers are the standard pattern and typically fall within PD outside the CA. We handle the full drawing package.",
            ),
            (
                "How much do architectural drawings cost in Sanderstead?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Croydon take to decide applications?",
                "Croydon targets 8 weeks for householder applications. We manage the timeline and respond to council requests.",
            ),
        ],
    },
    {
        "name": "Purley",
        "slug": "purley",
        "borough": "Croydon",
        "borough_slug": "croydon",
        "postcodes": "CR8",
        "character": "Purley is a south Croydon residential neighbourhood with a mix of Edwardian villas, 1930s semis, and substantial detached houses. The neighbourhood sees steady demand for extensions, loft conversions, and some substantial new-build projects on larger plots.",
        "housing_stock": "Edwardian villas, 1930s semis and detached, post-war detached, some new-build on larger plots",
        "conservation_notes": "Webb Estate and Upper Woodcote Conservation Areas cover some of the premium residential streets",
        "planning_notes": "Croydon Council applies standard policies outside conservation areas. Within Webb Estate and Upper Woodcote CAs, heritage controls apply. Article 4 Directions may affect some streets.",
        "nearby": ["sanderstead", "south-norwood", "thornton-heath", "norbury"],
        "popular_services": ["planning-drawings", "house-extensions", "loft-conversions"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Purley's Edwardian villas, 1930s homes, and larger detached properties. MCIAT chartered, fixed fees, Croydon planning expertise built in.",
        "local_context_title": "Why Purley demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Purley sits in the CR8 postcode in the south of the London Borough of Croydon. The neighbourhood's mix of Edwardian villas, 1930s houses, and substantial detached plots — together with the Webb Estate's Arts & Crafts heritage — generates a varied residential project pipeline.",
            "<strong>Edwardian villas:</strong> Purley has a stock of substantial Edwardian villas suitable for rear extensions, side-returns, and loft conversions. Many have been sensitively extended already; further alterations require careful design.",
            "<strong>Webb Estate Conservation Area:</strong> The Webb Estate is a celebrated early 20th-century garden suburb. Within the CA, Article 4 Directions restrict permitted development rights for most external alterations. Heritage Statements accompany applications. Our team prepares conservation-appropriate designs.",
            "<strong>Larger plots:</strong> Purley's larger detached plots — especially in Upper Woodcote and Webb Estate — can accommodate substantial extensions, outbuildings, or occasionally replacement dwellings. We advise on the full range of options.",
            "<strong>Tree constraints:</strong> Much of Purley has mature tree cover and extensive TPO coverage. Applications must address root protection zones and the impact on mature trees. We coordinate with arboricultural consultants where needed.",
        ],
        "stats": [
            ("Conservation areas", "Webb Estate, Upper Woodcote"),
            ("Housing type", "Edwardian, 1930s, detached"),
            ("Planning authority", "Croydon Council"),
            ("Key postcodes", "CR8"),
        ],
        "faqs": [
            (
                "Can I extend my Webb Estate house?",
                "Extensions are possible but all require planning permission under the Article 4 Directions. Heritage Statements and detailed material specifications are essential. We prepare conservation-sensitive applications.",
            ),
            (
                "Do I need planning permission for a loft conversion in Purley?",
                "Outside the CAs, rear dormers and hip-to-gable conversions usually fall within PD. Within the CAs, planning permission is required. We assess and prepare the right application.",
            ),
            (
                "What about replacement dwellings on larger plots?",
                "Possible but require full planning permission. Croydon will assess bulk, density, streetscape impact, and ecology. We prepare detailed schemes with all supporting documents.",
            ),
            (
                "How much do architectural drawings cost in Purley?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Conservation-area projects typically need Complete.",
            ),
            (
                "How long does Croydon take to decide?",
                "Croydon targets 8 weeks for householder applications and 13 weeks for majors. Conservation area applications may take longer. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Thornton Heath",
        "slug": "thornton-heath",
        "borough": "Croydon",
        "borough_slug": "croydon",
        "postcodes": "CR7",
        "character": "Thornton Heath is a dense residential neighbourhood in north Croydon, dominated by Victorian and Edwardian terraces, with pockets of inter-war housing. The area generates steady demand for rear extensions, loft conversions, and flat conversions.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, converted flats",
        "conservation_notes": "Small conservation pockets; most residential streets are unprotected",
        "planning_notes": "Croydon Council applies standard policies. Permitted development rights are generally intact. Flat conversion applications require compliance with Croydon's space standards.",
        "nearby": ["south-norwood", "norbury", "purley", "west-norwood"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and flat conversions for Thornton Heath's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Croydon planning expertise built in.",
        "local_context_title": "Why Thornton Heath demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Thornton Heath sits in the CR7 postcode in the north of the London Borough of Croydon. The dense streets of Victorian and Edwardian terraces — many already subdivided into flats — make it one of south London's most active residential conversion markets.",
            "<strong>Victorian terraces:</strong> The streets around Thornton Heath Pond and the railway station contain extensive Victorian terrace stock. Rear extensions, side-return infills, and rear dormer loft conversions are the main project types. Most fall within PD.",
            "<strong>Flat conversions:</strong> Many Thornton Heath houses have been converted to flats. Further subdivision requires planning permission and must meet Croydon's minimum space standards. Fire separation and sound insulation under Part E of the Building Regulations are critical.",
            "<strong>Edwardian stock:</strong> Pockets of larger Edwardian houses are suitable for substantial rear extensions and loft conversions. Some have potential for basement conversions where ground conditions allow.",
            "<strong>Croydon policies:</strong> Croydon Council has been active in addressing housing supply through householder extensions and subdivisions. Applications that meet design guidance typically receive straightforward approval.",
        ],
        "stats": [
            ("Conservation areas", "Small pockets"),
            ("Housing type", "Victorian/Edwardian terraces"),
            ("Planning authority", "Croydon Council"),
            ("Key postcodes", "CR7"),
        ],
        "faqs": [
            (
                "Can I convert my Thornton Heath house into flats?",
                "Planning permission from Croydon Council is required, plus full Building Regulations approval. Each flat must meet minimum space standards (37sqm for a studio, 50sqm for 1-bed, etc.). We prepare the full package.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "For most Thornton Heath terraces — no. Rear dormers up to 50 cubic metres (terrace) fall within PD. We prepare the Lawful Development Certificate and building regs drawings.",
            ),
            (
                "What size rear extension can I build?",
                "Under PD, terraced houses can extend up to 3m rear (or 6m with prior approval). Semi-detached can go to 4m (or 6m). We confirm PD eligibility.",
            ),
            (
                "How much do architectural drawings cost in Thornton Heath?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Croydon take to decide?",
                "Croydon targets 8 weeks for householder applications. Flat conversion applications may take 13 weeks. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "South Norwood",
        "slug": "south-norwood",
        "borough": "Croydon",
        "borough_slug": "croydon",
        "postcodes": "SE25",
        "character": "South Norwood is a residential neighbourhood straddling Croydon and bordering Lambeth and Bromley, with a mix of Victorian terraces, Edwardian villas, and pockets of inter-war housing. The area generates steady demand for extensions, loft conversions, and subdivisions.",
        "housing_stock": "Victorian terraces, Edwardian villas, inter-war semis, converted flats",
        "conservation_notes": "South Norwood and Croydon Road Conservation Areas cover central portions",
        "planning_notes": "Croydon Council applies standard policies with heritage controls in the conservation areas. Outside, PD rights are intact.",
        "nearby": ["thornton-heath", "crystal-palace", "west-norwood", "norbury"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and rear extensions for South Norwood's Victorian terraces and Edwardian family homes. MCIAT chartered, fixed fees, Croydon planning expertise built in.",
        "local_context_title": "Why South Norwood demands specialist architectural drawings",
        "local_context_paragraphs": [
            "South Norwood sits in the SE25 postcode in the north of the London Borough of Croydon. The mix of Victorian terraces, Edwardian villas, and converted flats — along with pockets of conservation — creates a varied residential project market.",
            "<strong>Victorian terraces:</strong> The dense streets around Norwood Junction station contain Victorian terraces on standard plots. Rear extensions, side-return infills, and rear dormer loft conversions are the main project types.",
            "<strong>Edwardian villas:</strong> South Norwood has a stock of Edwardian villas, particularly on streets south of the station. These properties suit substantial rear extensions and loft conversions. We design to respect the period character.",
            "<strong>Conservation areas:</strong> South Norwood and Croydon Road CAs cover central portions. Within the CAs, planning permission is required for most external works. We prepare heritage-sensitive applications.",
            "<strong>Flat conversions:</strong> Many houses have been subdivided. Further subdivision requires planning permission and compliance with space standards. We handle the full application package.",
        ],
        "stats": [
            ("Conservation areas", "South Norwood CA"),
            ("Housing type", "Victorian/Edwardian"),
            ("Planning authority", "Croydon Council"),
            ("Key postcodes", "SE25"),
        ],
        "faqs": [
            (
                "Do I need planning permission in South Norwood CA?",
                "For most external works — yes. Dormers, window replacements, and front alterations require planning permission within the CA. Heritage Statements are required. We prepare conservation-appropriate applications.",
            ),
            (
                "Can I build a side-return extension?",
                "Yes — side-return infills are popular and typically fall within PD outside the CA. Within the CA, planning permission is required. We prepare either submission.",
            ),
            (
                "What about loft conversions?",
                "Outside the CAs, rear dormers under PD are straightforward. Within the CAs, planning permission is required. We assess your property and prepare drawings.",
            ),
            (
                "How much do architectural drawings cost in South Norwood?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Croydon take to decide?",
                "Croydon targets 8 weeks for householder applications. Conservation area applications may take slightly longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "West Norwood",
        "slug": "west-norwood",
        "borough": "Lambeth",
        "borough_slug": "lambeth",
        "postcodes": "SE27",
        "character": "West Norwood is a residential neighbourhood in the south of the London Borough of Lambeth, with Victorian and Edwardian houses on hilly streets, the West Norwood Cemetery, and strong local heritage character. Extensions and loft conversions are the main project types.",
        "housing_stock": "Victorian terraces, Edwardian villas, inter-war semis, some Victorian detached",
        "conservation_notes": "West Norwood Cemetery Conservation Area; residential Article 4 pockets",
        "planning_notes": "Lambeth Council applies relatively strict policies with strong heritage protection around the cemetery. Most residential streets retain PD rights; Article 4 pockets require planning permission for alterations.",
        "nearby": ["tulse-hill", "herne-hill", "streatham", "south-norwood"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for West Norwood's Victorian and Edwardian homes. MCIAT chartered, fixed fees, Lambeth planning expertise built in.",
        "local_context_title": "Why West Norwood demands specialist architectural drawings",
        "local_context_paragraphs": [
            "West Norwood sits in the SE27 postcode in the south of the London Borough of Lambeth. The neighbourhood's hilly streets of Victorian and Edwardian houses, along with the West Norwood Cemetery and its conservation area, create a layered planning context.",
            "<strong>Victorian terraces and villas:</strong> West Norwood has excellent Victorian and Edwardian housing stock. Rear extensions, side-return infills, and rear dormer loft conversions are the core projects. The hilly topography means rear gardens often step down, creating opportunities for split-level extensions.",
            "<strong>Cemetery Conservation Area:</strong> West Norwood Cemetery is one of the 'Magnificent Seven' Victorian cemeteries. The surrounding conservation area protects views and setting. Properties facing or near the cemetery face additional heritage considerations.",
            "<strong>Article 4 pockets:</strong> Lambeth has designated Article 4 Directions in some residential areas of West Norwood, removing PD rights. Within these pockets, planning permission is required for dormers, rooflights, and front alterations. We confirm your property's status.",
            "<strong>Lambeth policies:</strong> Lambeth applies relatively high design standards. Heritage Statements, Design & Access Statements, and detailed materials are often required. Our drawings meet Lambeth's expectations.",
        ],
        "stats": [
            ("Conservation areas", "West Norwood Cemetery CA"),
            ("Housing type", "Victorian/Edwardian"),
            ("Planning authority", "Lambeth Council"),
            ("Key postcodes", "SE27"),
        ],
        "faqs": [
            (
                "Is my West Norwood property in an Article 4 zone?",
                "Possibly — Lambeth has designated several Article 4 pockets in West Norwood. We check your property's planning status early and advise on the required application route.",
            ),
            (
                "Can I build a rear extension?",
                "Outside Article 4 zones, rear extensions under PD are straightforward. Within Article 4 or the CA, planning permission is required. We prepare either route.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Outside Article 4 zones, rear dormers under PD are usually achievable. Within Article 4 or CA — planning permission required. We assess and prepare.",
            ),
            (
                "How much do architectural drawings cost in West Norwood?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Lambeth take to decide?",
                "Lambeth targets 8 weeks for householder applications. Conservation area and Article 4 applications may take longer. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Tulse Hill",
        "slug": "tulse-hill",
        "borough": "Lambeth",
        "borough_slug": "lambeth",
        "postcodes": "SE27",
        "character": "Tulse Hill is a south Lambeth neighbourhood of Victorian terraces, Edwardian villas, and some large detached houses on the elevated ridge. The area sees steady demand for extensions, loft conversions, and flat subdivisions.",
        "housing_stock": "Victorian terraces, Edwardian villas, large Victorian detached, some inter-war",
        "conservation_notes": "Tulse Hill and Roupell Park Conservation Areas cover premium streets",
        "planning_notes": "Lambeth Council applies strict policies with heritage protection in the conservation areas. Article 4 Directions may apply in conservation zones.",
        "nearby": ["west-norwood", "herne-hill", "streatham", "brixton"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Tulse Hill's Victorian terraces and Edwardian villas. MCIAT chartered, fixed fees, Lambeth planning expertise built in.",
        "local_context_title": "Why Tulse Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Tulse Hill sits in the SE27 postcode in the south of the London Borough of Lambeth, on the elevated ridge above Brixton. The neighbourhood's mix of Victorian terraces and substantial Edwardian villas — together with the Roupell Park and Tulse Hill conservation areas — generates a varied project mix.",
            "<strong>Victorian terraces:</strong> Tulse Hill's Victorian terraces are dense and street-facing. Rear extensions, side-return infills, and rear dormer loft conversions are the standard projects.",
            "<strong>Edwardian villas and larger detached:</strong> Tulse Hill has a stock of substantial Edwardian villas and some large Victorian detached. These properties suit extensive rear extensions, loft conversions, and sometimes basement conversions where ground conditions allow.",
            "<strong>Roupell Park Conservation Area:</strong> This tightly protected CA covers some of Tulse Hill's most handsome streets. Article 4 Directions restrict PD rights. Heritage Statements are required.",
            "<strong>Lambeth design standards:</strong> Lambeth Council has high expectations for householder applications, particularly in conservation areas. Materials, proportions, and streetscape impact all matter. Our drawings meet these standards.",
        ],
        "stats": [
            ("Conservation areas", "Tulse Hill, Roupell Park"),
            ("Housing type", "Victorian/Edwardian"),
            ("Planning authority", "Lambeth Council"),
            ("Key postcodes", "SE27"),
        ],
        "faqs": [
            (
                "Can I build a rear extension in Tulse Hill?",
                "Outside the CAs, rear extensions under PD are straightforward. Within Roupell Park or Tulse Hill CAs, planning permission is required. We prepare either submission.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Outside the CAs, rear dormers under PD usually work. Within the CAs, planning permission is required and dormer design must be sympathetic. We design appropriate schemes.",
            ),
            (
                "What about basement conversions?",
                "Possible for larger properties with suitable ground conditions. Lambeth has specific basement policy with clear tests. Structural engineer input is essential. We coordinate the full package.",
            ),
            (
                "How much do architectural drawings cost in Tulse Hill?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Lambeth take to decide?",
                "Lambeth targets 8 weeks for householder applications and 13 weeks for majors. Conservation area applications may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "West Hampstead",
        "slug": "west-hampstead",
        "borough": "Camden",
        "borough_slug": "camden",
        "postcodes": "NW6",
        "character": "West Hampstead is a dense, cosmopolitan Camden neighbourhood of Victorian mansion blocks, Edwardian terraces, and post-war flats. Flat conversions, loft conversions, and mansion block reconfigurations dominate the project pipeline.",
        "housing_stock": "Victorian mansion blocks, Edwardian terraces, post-war flats, Victorian villas",
        "conservation_notes": "West End Green and Fortune Green Conservation Areas cover significant portions",
        "planning_notes": "Camden Council applies strict heritage and design controls. Article 4 Directions are extensive across NW6 conservation areas. Basement conversions are tightly controlled under Camden's basement policy.",
        "nearby": ["kilburn", "swiss-cottage", "queens-park", "hampstead"],
        "popular_services": ["planning-drawings", "loft-conversions", "house-extensions"],
        "hero_lede": "Planning permission drawings, mansion block reconfigurations, loft conversions, and flat conversions for West Hampstead's Victorian and Edwardian housing. MCIAT chartered, fixed fees, Camden planning expertise built in.",
        "local_context_title": "Why West Hampstead demands specialist architectural drawings",
        "local_context_paragraphs": [
            "West Hampstead sits in the NW6 postcode within the London Borough of Camden. The neighbourhood's dense mix of Victorian mansion blocks, Edwardian terraces, and post-war flats — together with extensive conservation area coverage — makes it one of north-west London's most tightly controlled planning environments.",
            "<strong>Mansion blocks:</strong> West Hampstead has a significant stock of Victorian and Edwardian mansion blocks. Internal reconfigurations, window replacements, and balcony additions require freeholder consent alongside any Camden planning permission. Our drawings are prepared to meet Camden's requirements and typical freeholder expectations.",
            "<strong>Victorian and Edwardian terraces:</strong> The streets around West End Lane contain period terraces suitable for rear extensions, side-return infills, and loft conversions. Within the conservation areas, planning permission is usually required.",
            "<strong>Basement conversions:</strong> Camden has one of London's strictest basement policies. Lightwells, rear extensions of basements, and any subterranean works face tight controls. Our team understands Camden's basement requirements and prepares compliant schemes.",
            "<strong>Conservation and Article 4:</strong> West End Green and Fortune Green CAs cover significant portions of NW6. Article 4 Directions apply. Heritage Statements are required. We prepare conservation-grade applications.",
        ],
        "stats": [
            ("Conservation areas", "West End Green, Fortune Green"),
            ("Article 4", "Yes (extensive)"),
            ("Planning authority", "Camden Council"),
            ("Key postcodes", "NW6"),
        ],
        "faqs": [
            (
                "Can I extend my West Hampstead flat?",
                "Flat extensions are unusual but possible — rear additions, balcony additions, or mansion block reconfigurations. Freeholder consent is essential. We prepare the drawings and liaise with the freeholder's architects.",
            ),
            (
                "Do I need planning permission in NW6 conservation areas?",
                "For most external works — yes. Article 4 Directions remove PD rights. Heritage Statements are required. We prepare conservation-appropriate applications.",
            ),
            (
                "What about basement conversions?",
                "Camden's basement policy is strict. Lightwells are often allowed; rear basement extensions and second basement levels are tightly controlled. We prepare compliant schemes with structural engineer input.",
            ),
            (
                "How much do architectural drawings cost in West Hampstead?",
                "For conservation-area projects, the Complete package from £1,750 is typically required. Essentials from £840 may suffice for very minor work.",
            ),
            (
                "How long does Camden take to decide?",
                "Camden targets 8 weeks for householder applications and 13 weeks for majors. Conservation area applications may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Swiss Cottage",
        "slug": "swiss-cottage",
        "borough": "Camden",
        "borough_slug": "camden",
        "postcodes": "NW3",
        "character": "Swiss Cottage is a dense central Camden neighbourhood dominated by large mansion blocks, Edwardian villas, and substantial Victorian terraces. High-value residential reconfigurations and mansion block alterations are the core project types.",
        "housing_stock": "Large Edwardian mansion blocks, Victorian terraces, substantial detached villas, post-war apartments",
        "conservation_notes": "Fitzjohns/Netherhall Conservation Area; Swiss Cottage CA nearby",
        "planning_notes": "Camden Council applies strict heritage controls. Article 4 Directions are extensive in NW3. Basement policy is tight. Mansion block alterations require freeholder consent.",
        "nearby": ["hampstead", "belsize-park", "primrose-hill", "west-hampstead"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, mansion block reconfigurations, heritage-sensitive extensions, and building regulations for Swiss Cottage's Edwardian and Victorian housing. MCIAT chartered, fixed fees, Camden conservation expertise built in.",
        "local_context_title": "Why Swiss Cottage demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Swiss Cottage sits in the NW3 postcode within the London Borough of Camden, south of Hampstead and west of Primrose Hill. The neighbourhood's substantial Edwardian mansion blocks, Victorian villas, and high-value terraces make it one of London's most valuable — and tightly controlled — residential markets.",
            "<strong>Mansion blocks:</strong> Much of central Swiss Cottage is mansion block. Flat reconfigurations, new bathrooms, open-plan kitchen-living rooms, and balcony additions require planning permission, freeholder consent, and Building Regulations approval. Our drawings meet Camden's standards and typical freeholder requirements.",
            "<strong>Fitzjohns/Netherhall Conservation Area:</strong> This CA covers the handsome Victorian and Edwardian streets around Swiss Cottage. Article 4 Directions restrict PD rights. Heritage Statements are required for most applications. Our team prepares conservation-grade submissions.",
            "<strong>Basement works:</strong> Camden's basement policy is among the strictest in London. Subterranean developments must meet specific tests on hydrology, structural impact, and size. We prepare compliant schemes with full structural and hydrological input.",
            "<strong>Victorian and Edwardian villas:</strong> Swiss Cottage has substantial detached villas suitable for extensions and loft conversions. All require planning permission in the CA. We design heritage-sensitive schemes.",
        ],
        "stats": [
            ("Conservation areas", "Fitzjohns/Netherhall CA"),
            ("Article 4", "Yes"),
            ("Planning authority", "Camden Council"),
            ("Key postcodes", "NW3"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Swiss Cottage mansion flat?",
                "Yes, but planning permission and freeholder consent are typically required. Removing internal walls, creating open-plan spaces, and adding ensuites all need careful coordination. We prepare the drawings and liaise.",
            ),
            (
                "Do I need planning permission for external works in NW3?",
                "In the conservation area — almost always. Article 4 Directions remove PD rights. Heritage Statements are required. We prepare conservation-grade applications.",
            ),
            (
                "What about basement conversions?",
                "Camden's basement policy is tight. Ground conditions, hydrology, and impact on neighbours all matter. We prepare compliant schemes where the site allows.",
            ),
            (
                "How much do architectural drawings cost in Swiss Cottage?",
                "The Complete package from £1,750 is typically required for conservation-area and mansion-block projects. Essentials from £840 for minor interior works.",
            ),
            (
                "How long does Camden take to decide?",
                "Camden targets 8 weeks for householder applications and 13 weeks for majors. Pre-application advice is recommended for complex schemes. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Primrose Hill",
        "slug": "primrose-hill",
        "borough": "Camden",
        "borough_slug": "camden",
        "postcodes": "NW1",
        "character": "Primrose Hill is one of London's most desirable neighbourhoods — pastel-painted Victorian terraces, elegant Regency villas, and a tight conservation area covering the whole area. Every project requires conservation-sensitive drawings.",
        "housing_stock": "Victorian terraces, Regency villas, Georgian townhouses, mews houses",
        "conservation_notes": "Primrose Hill Conservation Area covers the whole neighbourhood; Article 4 Directions are extensive",
        "planning_notes": "Camden Council applies its strictest heritage controls in Primrose Hill. Article 4 Directions remove PD rights. Basement policy is among the tightest in London. Pre-application advice is strongly recommended.",
        "nearby": ["camden-town", "swiss-cottage", "belsize-park", "maida-vale"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and conservation-grade building regulations for Primrose Hill's Victorian and Regency housing. MCIAT chartered, fixed fees, Camden heritage expertise built in.",
        "local_context_title": "Why Primrose Hill demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Primrose Hill sits in the NW1 postcode within the London Borough of Camden, centred on Primrose Hill Park. The entire neighbourhood is a conservation area, with exceptionally high property values and correspondingly rigorous planning standards.",
            "<strong>Primrose Hill Conservation Area:</strong> Covers the whole neighbourhood. Article 4 Directions remove PD rights for virtually all external alterations. Heritage Statements are required for even minor works. Our MCIAT-chartered team has extensive experience preparing Primrose Hill submissions.",
            "<strong>Victorian terraces:</strong> The iconic pastel-painted Victorian terraces are protected both as heritage assets and for their contribution to the streetscape. Colour choices, window details, and roof alterations all require careful justification.",
            "<strong>Basement conversions:</strong> Camden's basement policy and Primrose Hill's conservation context combine to make basement works exceptionally tightly controlled. The scheme must pass the basement policy tests and avoid harm to the conservation area. We prepare compliant schemes only where feasible.",
            "<strong>Mews and rear properties:</strong> Primrose Hill has pockets of mews houses behind the main streets. These are often listed or within the CA. Any alterations require heritage justification. We handle mews projects with care.",
        ],
        "stats": [
            ("Conservation areas", "Primrose Hill CA (whole)"),
            ("Article 4", "Yes (extensive)"),
            ("Planning authority", "Camden Council"),
            ("Key postcodes", "NW1"),
        ],
        "faqs": [
            (
                "Can I extend my Primrose Hill house?",
                "Possibly, but every scheme requires planning permission, Heritage Statement, and often pre-application advice. Rear extensions must respect the period character and materials. We design heritage-sensitive schemes.",
            ),
            (
                "Do I need planning permission for any external work?",
                "Almost certainly yes. Article 4 Directions remove PD rights. Window changes, colour changes, rooflights, and boundary changes all typically need planning permission.",
            ),
            (
                "What about basement conversions?",
                "Camden's strictest basement policy applies. Schemes are possible but must pass hydrological, structural, and heritage tests. We advise on feasibility early.",
            ),
            (
                "How much do architectural drawings cost in Primrose Hill?",
                "The Complete package from £1,750 is essential for Primrose Hill projects. Conservation-grade drawings, Heritage Statements, and detailed materials are all included.",
            ),
            (
                "How long does Camden take to decide in Primrose Hill?",
                "Primrose Hill applications typically take 8–13 weeks, sometimes longer with heritage consultation. Pre-application advice adds 4–6 weeks but is strongly recommended. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Marylebone",
        "slug": "marylebone",
        "borough": "Westminster",
        "borough_slug": "westminster",
        "postcodes": "W1",
        "character": "Marylebone is a central Westminster neighbourhood of Georgian and Regency terraces, mansion blocks, and mews streets. Every project sits within one of London's most protected conservation contexts.",
        "housing_stock": "Georgian and Regency terraces, Victorian mansion blocks, mews houses, Edwardian flats",
        "conservation_notes": "Harley Street, Portman Estate, and Marylebone Conservation Areas cover the neighbourhood; many listed buildings",
        "planning_notes": "Westminster City Council applies its strictest heritage controls in W1. Article 4 Directions are extensive. Listed Building Consent is frequently required alongside planning permission.",
        "nearby": ["mayfair", "maida-vale", "primrose-hill", "victoria"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, Listed Building Consent, heritage-sensitive extensions, and building regulations for Marylebone's Georgian terraces and mansion flats. MCIAT chartered, fixed fees, Westminster heritage expertise built in.",
        "local_context_title": "Why Marylebone demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Marylebone sits in the W1 postcode within the City of Westminster. The neighbourhood's Georgian and Regency townhouses, Victorian mansion blocks, and mews streets — combined with near-complete conservation area coverage and extensive listing — make it one of London's most heritage-dense residential markets.",
            "<strong>Conservation areas:</strong> Harley Street, Portman Estate, and Marylebone CAs cover the neighbourhood. Article 4 Directions remove PD rights throughout. Heritage Statements and Design & Access Statements accompany every application.",
            "<strong>Listed buildings:</strong> A significant proportion of Marylebone housing is listed. Listed Building Consent runs in parallel with planning permission. Works to protected interiors — staircases, fireplaces, panelling — require particular care. We coordinate with Historic England where required.",
            "<strong>Mansion blocks:</strong> Marylebone has substantial Victorian and Edwardian mansion blocks. Flat reconfigurations, window replacements, and balcony additions require planning permission and freeholder consent. Our drawings meet Westminster's strict standards.",
            "<strong>Mews houses:</strong> The protected mews streets — Devonshire Mews, Queen Anne Mews, etc. — have their own design requirements. Rear additions, rooflights, and garage conversions all need planning permission.",
        ],
        "stats": [
            ("Conservation areas", "Multiple in W1"),
            ("Listed buildings", "Extensive"),
            ("Planning authority", "Westminster City Council"),
            ("Key postcodes", "W1"),
        ],
        "faqs": [
            (
                "Do I need Listed Building Consent for my Marylebone house?",
                "If your property is listed — yes, for virtually all internal and external works affecting character. Our team prepares the Listed Building Consent application alongside planning permission.",
            ),
            (
                "Can I extend my Marylebone townhouse?",
                "Possibly — rear extensions, roof alterations, and basement works may be achievable subject to heritage constraints. Every scheme requires planning permission. We prepare heritage-sensitive applications.",
            ),
            (
                "What about mansion flat reconfigurations?",
                "Internal reconfigurations usually need freeholder consent plus planning permission in listed buildings. Building Regulations approval is always required. We prepare the full package.",
            ),
            (
                "How much do architectural drawings cost in Marylebone?",
                "The Complete package from £1,750 is essential for Marylebone. Listed Building Consent projects may require bespoke pricing reflecting the heritage scope.",
            ),
            (
                "How long does Westminster take to decide?",
                "Westminster targets 8–13 weeks depending on scale. Listed Building Consent runs in parallel. Pre-application advice is strongly recommended. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Mayfair",
        "slug": "mayfair",
        "borough": "Westminster",
        "borough_slug": "westminster",
        "postcodes": "W1",
        "character": "Mayfair is central London's most prestigious residential neighbourhood — Georgian mansions, Regency townhouses, mews streets, and private squares. Every project is a heritage-led, high-value commission.",
        "housing_stock": "Georgian mansions, Regency townhouses, mews houses, private gated squares, luxury mansion blocks",
        "conservation_notes": "Mayfair Conservation Area covers the whole neighbourhood; extensive listed buildings; private estates (Grosvenor, Portland) apply additional controls",
        "planning_notes": "Westminster City Council applies its strictest heritage controls. Article 4 Directions are comprehensive. Listed Building Consent is routine. Private estate consent is also typically required.",
        "nearby": ["marylebone", "pimlico", "victoria", "mayfair"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, Listed Building Consent, and heritage-grade building regulations for Mayfair's Georgian townhouses, mews, and mansion flats. MCIAT chartered, fixed fees, Westminster heritage expertise built in.",
        "local_context_title": "Why Mayfair demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Mayfair sits in the W1 postcode at the centre of the City of Westminster. The neighbourhood is London's most prestigious residential address — Georgian mansions, Regency townhouses, and private squares all sitting within near-complete conservation area coverage and extensive listing.",
            "<strong>Mayfair Conservation Area:</strong> Covers the whole neighbourhood. Article 4 Directions remove PD rights. Heritage Statements are required for every application. Our MCIAT-chartered team prepares Mayfair-grade submissions with appropriate level of detail.",
            "<strong>Private estates:</strong> Mayfair includes the Grosvenor Estate, the Portland Estate, and other private freehold estates. These estates apply their own design codes alongside Westminster's planning controls. We prepare schemes that satisfy both.",
            "<strong>Listed buildings:</strong> A majority of Mayfair housing is listed — Grade II common, Grade II* and Grade I on premier streets. Listed Building Consent is routine. We coordinate with Historic England for higher-grade listings.",
            "<strong>Mews houses:</strong> Mayfair's mews streets — Adams Row, Charles Mews, Mount Row — have particular design codes. Garage conversions, rooflights, and rear alterations all require planning permission and often estate consent.",
        ],
        "stats": [
            ("Conservation areas", "Mayfair CA (whole)"),
            ("Listed buildings", "Extensive"),
            ("Planning authority", "Westminster + private estates"),
            ("Key postcodes", "W1"),
        ],
        "faqs": [
            (
                "Can I alter my Mayfair townhouse?",
                "Yes, but every scheme requires planning permission, Listed Building Consent where applicable, and estate consent. We prepare the full package.",
            ),
            (
                "What is the Grosvenor Estate's design code?",
                "The Grosvenor Estate has its own design guidance for properties it owns or controls. Applications to the estate are separate from Westminster planning. We prepare both in parallel.",
            ),
            (
                "Can I do a basement conversion in Mayfair?",
                "Very tightly controlled. Ground conditions, heritage impact, and estate consent all matter. We advise on feasibility early and prepare schemes only where achievable.",
            ),
            (
                "How much do architectural drawings cost in Mayfair?",
                "Mayfair projects are typically Complete package from £1,750 or bespoke pricing for listed buildings and larger schemes. We quote transparently at the outset.",
            ),
            (
                "How long does Westminster take to decide?",
                "Mayfair applications take 8–13 weeks, often longer with heritage consultation. Pre-application advice is strongly recommended. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Pimlico",
        "slug": "pimlico",
        "borough": "Westminster",
        "borough_slug": "westminster",
        "postcodes": "SW1",
        "character": "Pimlico is a central Westminster residential neighbourhood of white stucco Regency and early Victorian terraces, mansion blocks, and Churchill Gardens. Heritage-sensitive drawings are standard; stucco facade rules are strict.",
        "housing_stock": "White stucco Regency terraces, early Victorian terraces, mansion blocks, post-war Churchill Gardens estate",
        "conservation_notes": "Pimlico Conservation Area covers most of the neighbourhood; some buildings are listed",
        "planning_notes": "Westminster City Council applies strict heritage controls. Article 4 Directions remove PD rights. Stucco facade maintenance and colour controls are specific to Pimlico.",
        "nearby": ["victoria", "battersea-park", "vauxhall", "mayfair"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and building regulations for Pimlico's Regency stucco terraces and mansion flats. MCIAT chartered, fixed fees, Westminster heritage expertise built in.",
        "local_context_title": "Why Pimlico demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Pimlico sits in the SW1 postcode within the City of Westminster, south of Victoria and north of the Thames. The neighbourhood's iconic white stucco Regency and Victorian terraces — largely the work of Thomas Cubitt — sit within near-complete conservation area coverage.",
            "<strong>Pimlico Conservation Area:</strong> Covers the historic core. Article 4 Directions remove PD rights. Stucco facades are particularly protected — colour, detail, and maintenance regimes are all controlled. Heritage Statements accompany every application.",
            "<strong>Regency terraces:</strong> Thomas Cubitt's white stucco terraces are the defining built form. Rear extensions, loft conversions, and basement works are possible but all require planning permission. Rear elevations are typically brick; alterations must respect this distinction.",
            "<strong>Mansion blocks:</strong> Pimlico has a significant mansion block stock. Flat reconfigurations, window replacements, and balcony additions require planning permission and freeholder consent.",
            "<strong>Churchill Gardens estate:</strong> This post-war estate has its own planning considerations as a recognised example of mid-century housing.",
        ],
        "stats": [
            ("Conservation areas", "Pimlico CA"),
            ("Article 4", "Yes"),
            ("Planning authority", "Westminster City Council"),
            ("Key postcodes", "SW1"),
        ],
        "faqs": [
            (
                "Can I change the colour of my Pimlico stucco?",
                "No — the white-stucco colour scheme is strictly controlled. Painting in a different colour typically requires planning permission and is usually refused. Maintenance must use the approved lime-based regime.",
            ),
            (
                "Can I extend my Pimlico townhouse?",
                "Rear extensions, loft conversions, and basement works are all possible subject to heritage constraints. Every scheme requires planning permission. We prepare heritage-sensitive applications.",
            ),
            (
                "What about window replacements?",
                "Sash window replacements usually need planning permission within the CA. Materials, glazing bar profiles, and proportions all matter. We prepare detailed schedules.",
            ),
            (
                "How much do architectural drawings cost in Pimlico?",
                "The Complete package from £1,750 is typical for Pimlico projects. Listed buildings may require bespoke pricing.",
            ),
            (
                "How long does Westminster take to decide?",
                "Westminster targets 8 weeks for householders and 13 for majors. Conservation area applications may take longer. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Victoria",
        "slug": "victoria",
        "borough": "Westminster",
        "borough_slug": "westminster",
        "postcodes": "SW1",
        "character": "Victoria is a mixed central Westminster neighbourhood around the mainline station, with Regency and Victorian mansion blocks, post-war residential towers, and some period terraces. Mansion block reconfigurations and flat conversions are common.",
        "housing_stock": "Victorian and Edwardian mansion blocks, Regency terraces, post-war flats, modern developments",
        "conservation_notes": "Victoria Conservation Area covers central portions; multiple smaller CAs",
        "planning_notes": "Westminster applies strict controls. Article 4 Directions apply widely. Listed Building Consent needed for many properties. Mansion block alterations require freeholder consent.",
        "nearby": ["pimlico", "mayfair", "vauxhall", "marylebone"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, mansion block reconfigurations, and building regulations for Victoria's period and modern housing stock. MCIAT chartered, fixed fees, Westminster planning expertise built in.",
        "local_context_title": "Why Victoria demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Victoria sits in the SW1 postcode within the City of Westminster, around Victoria Station. The neighbourhood is a working hub with period residential side streets, substantial mansion blocks, and post-war developments.",
            "<strong>Mansion blocks:</strong> Victoria has a significant Victorian and Edwardian mansion block stock. Flat reconfigurations, new kitchens and bathrooms, and open-plan conversions are standard. Planning permission, freeholder consent, and Building Regulations approval are all typically required.",
            "<strong>Conservation areas:</strong> Victoria CA and surrounding heritage designations cover substantial portions. Article 4 Directions apply widely. Heritage Statements accompany most applications.",
            "<strong>Period terraces:</strong> Some streets retain period terraces — Regency and early Victorian. These require heritage-sensitive design for any alterations.",
            "<strong>Modern developments:</strong> New-build blocks require alignment with estate management and often freeholder consent for internal works.",
        ],
        "stats": [
            ("Conservation areas", "Victoria CA"),
            ("Housing type", "Mansion blocks, modern flats"),
            ("Planning authority", "Westminster City Council"),
            ("Key postcodes", "SW1"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Victoria mansion flat?",
                "Yes — internal reconfigurations typically need planning permission for listed buildings, freeholder consent, and Building Regulations approval. We prepare the full package.",
            ),
            (
                "Do I need planning permission for window replacement?",
                "Usually yes in the conservation areas. Materials and proportions matter. We prepare appropriate specifications.",
            ),
            (
                "What about adding a balcony?",
                "Possible but typically needs planning permission and freeholder consent. Structural input is essential. We prepare the full scheme.",
            ),
            (
                "How much do architectural drawings cost in Victoria?",
                "Our Complete package from £1,750 is typical for Victoria projects. Essentials from £840 for minor interior works.",
            ),
            (
                "How long does Westminster take to decide?",
                "Westminster targets 8–13 weeks. Conservation area and listed building applications may take longer. We manage the process.",
            ),
        ],
    },
    {
        "name": "Battersea Park",
        "slug": "battersea-park",
        "borough": "Wandsworth",
        "borough_slug": "wandsworth",
        "postcodes": "SW11",
        "character": "Battersea Park is the prestigious residential corridor along the park, with Victorian and Edwardian mansion blocks, period townhouses, and new-build luxury developments at Battersea Power Station and Prince of Wales Drive.",
        "housing_stock": "Victorian and Edwardian mansion blocks, period townhouses, Victorian terraces, new-build luxury apartments",
        "conservation_notes": "Battersea Park Conservation Area; some streets have Article 4 Directions",
        "planning_notes": "Wandsworth Council applies strict heritage controls near the park. New-build developments have specific estate management rules. Basement policy applies under Wandsworth.",
        "nearby": ["nine-elms", "vauxhall", "fulham", "clapham"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, mansion block reconfigurations, and heritage-sensitive extensions for Battersea Park's period and luxury new-build properties. MCIAT chartered, fixed fees, Wandsworth planning expertise built in.",
        "local_context_title": "Why Battersea Park demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Battersea Park sits in the SW11 postcode within the London Borough of Wandsworth, along the south bank of the Thames opposite Chelsea. The neighbourhood combines historic mansion blocks and period townhouses facing the park with substantial new-build developments at Battersea Power Station and Prince of Wales Drive.",
            "<strong>Mansion blocks:</strong> The streets facing Battersea Park — Prince of Wales Drive, Albert Bridge Road — contain substantial Victorian and Edwardian mansion blocks. Flat reconfigurations and external alterations require planning permission, freeholder consent, and sometimes Heritage Statements.",
            "<strong>Period townhouses:</strong> The streets south of the park contain Victorian townhouses suitable for rear extensions, loft conversions, and basement works. Wandsworth's basement policy applies.",
            "<strong>New-build developments:</strong> Battersea Power Station and Prince of Wales Drive include substantial new-build residential. Internal alterations in new-build flats often have design codes from the estate management company alongside Wandsworth planning.",
            "<strong>Battersea Park Conservation Area:</strong> The CA protects the park setting and the handsome mansion terraces facing it. Heritage Statements are required for most alterations.",
        ],
        "stats": [
            ("Conservation areas", "Battersea Park CA"),
            ("Housing type", "Mansion blocks, townhouses, new-build"),
            ("Planning authority", "Wandsworth Council"),
            ("Key postcodes", "SW11"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Battersea Park mansion flat?",
                "Yes — internal reconfigurations are common. Planning permission may be needed for listed buildings; freeholder consent and Building Regulations approval are essential. We prepare the full package.",
            ),
            (
                "Do I need planning permission for a rear extension?",
                "Most period townhouses need planning permission within the CA. Wandsworth also has basement policy. We advise on feasibility early.",
            ),
            (
                "What about alterations in the new-build developments?",
                "Internal alterations in new-build flats typically need estate management consent alongside Building Regulations approval. Some works may need planning. We prepare the right submissions.",
            ),
            (
                "How much do architectural drawings cost in Battersea Park?",
                "Our Complete package from £1,750 is typical for conservation-area and mansion-block projects. Essentials from £840 for minor interior works.",
            ),
            (
                "How long does Wandsworth take to decide?",
                "Wandsworth targets 8 weeks for householders and 13 for majors. Conservation area applications may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Nine Elms",
        "slug": "nine-elms",
        "borough": "Wandsworth",
        "borough_slug": "wandsworth",
        "postcodes": "SW8",
        "character": "Nine Elms is a rapidly developing riverside area of Wandsworth dominated by new-build luxury apartment towers around Battersea Power Station and the US Embassy. Internal reconfigurations, balcony additions, and new-build interior works dominate.",
        "housing_stock": "New-build apartment towers, Battersea Power Station conversion, some period terraces on the edges",
        "conservation_notes": "Edges border Battersea Park CA; core is new-build",
        "planning_notes": "Wandsworth Council applies site-specific planning frameworks for Nine Elms. Estate management consent is typical. Internal reconfigurations in new-build require freeholder agreement.",
        "nearby": ["battersea-park", "vauxhall", "kennington", "fulham"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, internal reconfigurations, and building regulations for Nine Elms' new-build apartments and the wider regeneration area. MCIAT chartered, fixed fees, Wandsworth planning expertise built in.",
        "local_context_title": "Why Nine Elms demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Nine Elms sits in the SW8 postcode within the London Borough of Wandsworth. The area has been transformed over the past decade by the Nine Elms Vauxhall Opportunity Area — Battersea Power Station conversion, the US Embassy, and multiple high-rise residential developments.",
            "<strong>New-build apartments:</strong> The majority of Nine Elms residential stock is new-build. Internal reconfigurations — removing walls, adding ensuites, creating open-plan spaces — require freeholder consent and Building Regulations approval. Some works may need planning permission.",
            "<strong>Battersea Power Station:</strong> The converted Power Station and surrounding Circus West Village include substantial residential. Apartments within the Grade II* listed Power Station building have particular Listed Building Consent requirements.",
            "<strong>Estate management:</strong> Most Nine Elms developments have active estate management companies with their own design codes. Internal works typically need estate consent alongside any statutory applications.",
            "<strong>Wandsworth basement policy:</strong> Ground floor apartments with garden terraces may have scope for basement works; subject to Wandsworth's basement policy and structural constraints.",
        ],
        "stats": [
            ("Conservation areas", "Borders only"),
            ("Housing type", "New-build apartments"),
            ("Planning authority", "Wandsworth Council"),
            ("Key postcodes", "SW8"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Nine Elms new-build apartment?",
                "Yes — internal reconfigurations are common. Freeholder and estate management consent are essential. Building Regulations approval is required. Some works may need planning. We prepare the full package.",
            ),
            (
                "Do I need Listed Building Consent in the Power Station?",
                "For apartments within the Grade II* listed Battersea Power Station — yes, for works affecting heritage fabric. We prepare Listed Building Consent applications.",
            ),
            (
                "Can I add a balcony or terrace?",
                "Typically requires planning permission, estate consent, and structural input. Possible on suitable apartments. We advise and prepare the full scheme.",
            ),
            (
                "How much do architectural drawings cost in Nine Elms?",
                "Our Essentials package starts from £840 for minor interior works. Complete from £1,750 for more substantial reconfigurations.",
            ),
            (
                "How long does Wandsworth take to decide?",
                "Wandsworth targets 8 weeks for householder and 13 for major applications. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Vauxhall",
        "slug": "vauxhall",
        "borough": "Lambeth",
        "borough_slug": "lambeth",
        "postcodes": "SE11",
        "character": "Vauxhall is a central Lambeth neighbourhood transformed by the Nine Elms Opportunity Area — new-build towers along the river, with period terraces and estates on the inland streets. Mixed new-build and period residential projects.",
        "housing_stock": "New-build towers, Victorian terraces, post-war estates, Victorian mansion blocks",
        "conservation_notes": "Vauxhall Gardens Conservation Area; Lambeth Walk CA nearby",
        "planning_notes": "Lambeth Council applies the Nine Elms Vauxhall Opportunity Area framework to new-build areas. Period residential streets face standard Lambeth policies with heritage controls in CAs.",
        "nearby": ["nine-elms", "kennington", "walworth", "pimlico"],
        "popular_services": ["planning-drawings", "building-regulations", "house-extensions"],
        "hero_lede": "Planning permission drawings, extensions, and building regulations for Vauxhall's period terraces and new-build developments. MCIAT chartered, fixed fees, Lambeth planning expertise built in.",
        "local_context_title": "Why Vauxhall demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Vauxhall sits in the SE11 postcode within the London Borough of Lambeth, along the south bank of the Thames. The neighbourhood combines substantial new-build regeneration — part of the Nine Elms Vauxhall Opportunity Area — with period residential streets inland.",
            "<strong>New-build tower apartments:</strong> The recent regeneration has added substantial high-rise residential stock. Internal reconfigurations, balcony additions, and internal layout changes are the typical projects.",
            "<strong>Period terraces:</strong> Inland streets retain Victorian terraces and Edwardian houses. These are suitable for rear extensions, loft conversions, and side-return infills. Most fall within PD outside the CAs.",
            "<strong>Vauxhall Gardens Conservation Area:</strong> The CA protects the historic core around Vauxhall Pleasure Gardens. Within the CA, planning permission is required for most works.",
            "<strong>Lambeth design standards:</strong> Lambeth applies high design standards. Heritage Statements and Design & Access Statements are required for most applications.",
        ],
        "stats": [
            ("Conservation areas", "Vauxhall Gardens CA"),
            ("Housing type", "New-build, Victorian terraces"),
            ("Planning authority", "Lambeth Council"),
            ("Key postcodes", "SE11"),
        ],
        "faqs": [
            (
                "Can I extend my Vauxhall terrace?",
                "Rear extensions and loft conversions are common. Outside the CA, most fall within PD. Within the CA, planning permission is required. We prepare either submission.",
            ),
            (
                "What about new-build apartment alterations?",
                "Internal reconfigurations need freeholder consent and Building Regulations approval. Some alterations may need planning. We prepare the right package.",
            ),
            (
                "Do I need planning permission in the CA?",
                "For most external works — yes. Heritage Statements accompany applications. We prepare conservation-sensitive drawings.",
            ),
            (
                "How much do architectural drawings cost in Vauxhall?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Lambeth take to decide?",
                "Lambeth targets 8 weeks for householder and 13 for major applications. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Kennington",
        "slug": "kennington",
        "borough": "Lambeth",
        "borough_slug": "lambeth",
        "postcodes": "SE11",
        "character": "Kennington is a central Lambeth neighbourhood of Georgian and Victorian terraces, handsome squares, and some post-war estates. Heritage-sensitive extensions, loft conversions, and flat conversions are the main project types.",
        "housing_stock": "Georgian terraces, Victorian terraces, post-war estates, some Edwardian mansion blocks",
        "conservation_notes": "Kennington Conservation Area; Cleaver Square CA; Walcot Estate CA",
        "planning_notes": "Lambeth Council applies strict heritage controls in the Kennington CAs. Article 4 Directions apply widely. Heritage Statements are routine.",
        "nearby": ["vauxhall", "walworth", "camberwell", "nine-elms"],
        "popular_services": ["planning-drawings", "loft-conversions", "house-extensions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and loft conversions for Kennington's Georgian and Victorian terraces. MCIAT chartered, fixed fees, Lambeth heritage expertise built in.",
        "local_context_title": "Why Kennington demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Kennington sits in the SE11 postcode within the London Borough of Lambeth. The neighbourhood's Georgian terraces, handsome squares (Cleaver Square, Kennington Park), and Victorian streets are among south London's best-preserved period residential stock.",
            "<strong>Georgian terraces:</strong> Kennington has some of south London's finest Georgian terraces. Rear extensions and loft conversions are achievable but all require planning permission within the CAs. We design heritage-sensitive schemes.",
            "<strong>Victorian stock:</strong> The wider neighbourhood has extensive Victorian terraces suitable for standard rear extensions, side-return infills, and rear dormer loft conversions. Most fall within Article 4 zones requiring planning permission.",
            "<strong>Cleaver Square Conservation Area:</strong> Cleaver Square is a tightly protected Georgian square. Article 4 Directions remove PD rights. Heritage Statements are required. Our team prepares Cleaver Square-grade submissions.",
            "<strong>Lambeth basement policy:</strong> Kennington properties with suitable ground conditions may have basement conversion potential. Lambeth's basement policy applies.",
        ],
        "stats": [
            ("Conservation areas", "Kennington, Cleaver Square, Walcot"),
            ("Article 4", "Yes"),
            ("Planning authority", "Lambeth Council"),
            ("Key postcodes", "SE11"),
        ],
        "faqs": [
            (
                "Can I extend my Kennington Georgian house?",
                "Possibly — rear extensions and basement works may be achievable. Every scheme requires planning permission. Heritage Statements are essential. We prepare heritage-sensitive designs.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Within the Article 4 zones — yes. Dormer design must be sympathetic. Rooflights often preferred. We design appropriate schemes.",
            ),
            (
                "What about Cleaver Square?",
                "Cleaver Square is one of Lambeth's most tightly controlled CAs. Every external alteration typically needs planning permission. Pre-application advice is recommended.",
            ),
            (
                "How much do architectural drawings cost in Kennington?",
                "The Complete package from £1,750 is typically required for CA projects. Essentials from £840 for minor interior works.",
            ),
            (
                "How long does Lambeth take to decide?",
                "Lambeth targets 8 weeks for householder and 13 for major applications. Conservation area applications may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Walworth",
        "slug": "walworth",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE17",
        "character": "Walworth is a central Southwark neighbourhood of Victorian terraces, Georgian survivals, and substantial post-war estates. Rear extensions, loft conversions, and flat conversions are the typical project types.",
        "housing_stock": "Victorian terraces, Georgian survivals, post-war estates (Heygate/Elephant legacy), converted flats",
        "conservation_notes": "Walworth Conservation Area; Liverpool Grove CA; Pullens Estate CA",
        "planning_notes": "Southwark Council applies heritage controls in the CAs. Article 4 Directions apply. Outside CAs, standard Southwark policies with PD rights.",
        "nearby": ["kennington", "camberwell", "bermondsey", "peckham"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and flat conversions for Walworth's Victorian terraces and period properties. MCIAT chartered, fixed fees, Southwark planning expertise built in.",
        "local_context_title": "Why Walworth demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Walworth sits in the SE17 postcode within the London Borough of Southwark. The neighbourhood's Victorian terraces, Georgian survivals, and the Pullens Estate — a rare preserved Victorian artisan estate — sit within a rapidly regenerating wider context around Elephant & Castle.",
            "<strong>Victorian terraces:</strong> Walworth has extensive Victorian terrace stock. Rear extensions, side-return infills, and rear dormer loft conversions are the main projects. Outside the CAs, most fall within PD.",
            "<strong>Pullens Estate Conservation Area:</strong> The Pullens Estate is an exceptional preserved Victorian artisan yard and housing estate. Within the CA, Article 4 Directions apply and Heritage Statements are required.",
            "<strong>Flat conversions:</strong> Many Walworth houses have been subdivided. Further subdivision requires planning permission and must meet Southwark's space standards. We prepare the full package.",
            "<strong>Regeneration context:</strong> Walworth sits next to the major regeneration around Elephant & Castle. The wider policy context is shifting; Southwark has published updated guidance on densification and design.",
        ],
        "stats": [
            ("Conservation areas", "Walworth, Liverpool Grove, Pullens"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE17"),
        ],
        "faqs": [
            (
                "Can I convert my Walworth house into flats?",
                "Yes, with planning permission from Southwark. Each flat must meet minimum space standards. Sound insulation and fire separation are critical. We prepare the full package.",
            ),
            (
                "Do I need planning permission in Pullens Estate?",
                "Almost always — Pullens is tightly controlled. Article 4 Directions remove PD rights. Heritage Statements are essential. We prepare conservation-grade applications.",
            ),
            (
                "What about rear extensions elsewhere in Walworth?",
                "Outside the CAs, rear extensions under PD or prior approval are straightforward. Within the CAs, planning permission is required.",
            ),
            (
                "How much do architectural drawings cost in Walworth?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Southwark take to decide?",
                "Southwark targets 8 weeks for householders and 13 for majors. Conservation area applications may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Camberwell",
        "slug": "camberwell",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE5",
        "character": "Camberwell is a south Southwark neighbourhood of Victorian and Edwardian terraces, Georgian survivals around Camberwell Green, and Edwardian mansion blocks. Loft conversions, rear extensions, and flat reconfigurations dominate.",
        "housing_stock": "Victorian terraces, Edwardian villas, Georgian survivals, Edwardian mansion blocks, post-war estates",
        "conservation_notes": "Camberwell Grove CA; Camberwell Green CA; Addington Square CA",
        "planning_notes": "Southwark Council applies heritage controls in the multiple Camberwell CAs. Article 4 Directions apply. Most streets outside CAs retain PD rights.",
        "nearby": ["peckham", "walworth", "east-dulwich", "herne-hill"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Camberwell's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Southwark planning expertise built in.",
        "local_context_title": "Why Camberwell demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Camberwell sits in the SE5 postcode within the London Borough of Southwark. The neighbourhood's mix of Victorian terraces, Edwardian villas, Georgian survivals around Camberwell Green, and multiple conservation areas generates a varied residential project market.",
            "<strong>Camberwell Grove CA:</strong> One of south London's finest Georgian streets. Tightly controlled — Article 4 Directions remove PD rights. Heritage Statements are essential. We prepare Grove-grade applications.",
            "<strong>Victorian terraces:</strong> Extensive Victorian terrace stock outside the CAs is suitable for standard rear extensions, side-return infills, and rear dormer loft conversions. Most fall within PD.",
            "<strong>Edwardian villas:</strong> Pockets of substantial Edwardian villas, particularly south of Camberwell Green, suit larger extensions and loft conversions.",
            "<strong>Flat conversions:</strong> Many larger Camberwell houses have been subdivided. Further subdivision requires planning permission and compliance with Southwark's space standards.",
        ],
        "stats": [
            ("Conservation areas", "Camberwell Grove, Camberwell Green"),
            ("Housing type", "Victorian/Edwardian"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE5"),
        ],
        "faqs": [
            (
                "Can I extend my Camberwell Grove house?",
                "Possibly, but every scheme requires planning permission. Camberwell Grove is tightly controlled. Heritage Statements are essential. We prepare Grove-grade applications.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Outside the CAs, rear dormers under PD are usually straightforward. Within the CAs, planning permission is required. We assess and prepare.",
            ),
            (
                "What about rear extensions?",
                "Outside the CAs, most rear extensions fall within PD. Within the CAs, planning permission is required with heritage considerations.",
            ),
            (
                "How much do architectural drawings cost in Camberwell?",
                "Our Essentials package starts from £840. The Complete package from £1,750 covers planning and building regulations plus structural calculations. Conservation-grade projects typically need Complete.",
            ),
            (
                "How long does Southwark take to decide?",
                "Southwark targets 8 weeks for householders and 13 for majors. Camberwell Grove applications may take longer. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Nunhead",
        "slug": "nunhead",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE15",
        "character": "Nunhead is a south Southwark residential neighbourhood of Victorian terraces and Edwardian houses, centred on the picturesque Nunhead Cemetery. Rear extensions, loft conversions, and flat conversions dominate.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war pockets, some converted flats",
        "conservation_notes": "Nunhead Cemetery Conservation Area; Telegraph Hill nearby",
        "planning_notes": "Southwark Council applies heritage controls near the cemetery. Most streets retain PD rights. Flat conversions require compliance with space standards.",
        "nearby": ["peckham", "brockley", "east-dulwich", "camberwell"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, rear extensions, and flat conversions for Nunhead's Victorian and Edwardian housing. MCIAT chartered, fixed fees, Southwark planning expertise built in.",
        "local_context_title": "Why Nunhead demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Nunhead sits in the SE15 postcode within the London Borough of Southwark. The neighbourhood's Victorian and Edwardian terraces — arranged around the picturesque Nunhead Cemetery — are increasingly popular as Peckham prices push buyers further south.",
            "<strong>Victorian terraces:</strong> Nunhead's Victorian terraces are the dominant stock. Rear extensions, side-return infills, and rear dormer loft conversions are the core projects. Most fall within PD outside the small CA.",
            "<strong>Nunhead Cemetery Conservation Area:</strong> The cemetery is one of the 'Magnificent Seven' Victorian cemeteries. The surrounding CA protects views. Properties facing or adjacent require heritage-sensitive design.",
            "<strong>Edwardian stock:</strong> Some streets have larger Edwardian houses suitable for more substantial extensions.",
            "<strong>Flat conversions:</strong> Subdivided houses are common. Further subdivision requires planning permission and compliance with Southwark's space standards.",
        ],
        "stats": [
            ("Conservation areas", "Nunhead Cemetery CA"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE15"),
        ],
        "faqs": [
            (
                "Can I build a rear extension in Nunhead?",
                "Yes — most fall within PD. Up to 3m for terraces or 6m with prior approval. We prepare drawings and notification.",
            ),
            (
                "Do I need planning permission near the cemetery?",
                "Within the Nunhead Cemetery CA — yes for most works. Heritage Statements are required. We prepare conservation-sensitive applications.",
            ),
            (
                "What about loft conversions?",
                "Rear dormers under PD are usually straightforward on Victorian terraces outside the CA. We prepare the LDC and building regs drawings.",
            ),
            (
                "How much do architectural drawings cost in Nunhead?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Southwark take to decide?",
                "Southwark targets 8 weeks for householders and 13 for majors. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Brockley",
        "slug": "brockley",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE4",
        "character": "Brockley is a Lewisham neighbourhood of handsome Victorian villas on tree-lined streets, with substantial period housing stock and strong conservation area coverage across much of the neighbourhood.",
        "housing_stock": "Victorian villas, Victorian terraces, Edwardian houses, some Victorian detached",
        "conservation_notes": "Brockley Conservation Area covers much of the neighbourhood; Article 4 Directions apply",
        "planning_notes": "Lewisham Council applies strict heritage controls in the Brockley CA. Article 4 Directions remove PD rights. Heritage Statements are routine.",
        "nearby": ["new-cross", "lewisham", "nunhead", "forest-hill"],
        "popular_services": ["planning-drawings", "loft-conversions", "house-extensions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, and loft conversions for Brockley's Victorian villas and conservation-area terraces. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why Brockley demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Brockley sits in the SE4 postcode within the London Borough of Lewisham. The neighbourhood's handsome Victorian villas on tree-lined streets — within the extensive Brockley Conservation Area — make it one of south-east London's most sought-after period housing markets.",
            "<strong>Brockley Conservation Area:</strong> Covers much of the neighbourhood. Article 4 Directions remove PD rights for most external alterations. Heritage Statements accompany every application. Our team prepares conservation-grade submissions.",
            "<strong>Victorian villas:</strong> Brockley's double-fronted and semi-detached Victorian villas are among south-east London's finest. Substantial rear extensions, side-return infills, and loft conversions are achievable but all require planning permission within the CA.",
            "<strong>Victorian terraces:</strong> The tighter terraced streets suit standard rear extensions and rear dormer loft conversions, all with planning permission required.",
            "<strong>Lewisham design standards:</strong> Lewisham applies clear design guidance emphasising subordinate extensions, matching materials, and respect for the Victorian streetscape.",
        ],
        "stats": [
            ("Conservation areas", "Brockley CA"),
            ("Article 4", "Yes"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE4"),
        ],
        "faqs": [
            (
                "Can I extend my Brockley Victorian villa?",
                "Yes — substantial rear extensions and side-return infills are achievable. Every scheme requires planning permission. Heritage Statements are essential. We prepare conservation-sensitive designs.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Within the Brockley CA — yes. Dormer design must be subordinate and sympathetic. Rooflights are often preferred on front elevations. We design appropriate schemes.",
            ),
            (
                "What about window replacements?",
                "Sash window replacements within the CA typically need planning permission. Materials and glazing bar profiles matter. We prepare detailed schedules.",
            ),
            (
                "How much do architectural drawings cost in Brockley?",
                "The Complete package from £1,750 is typically required for Brockley CA projects. Essentials from £840 for minor interior works.",
            ),
            (
                "How long does Lewisham take to decide?",
                "Lewisham targets 8 weeks for householder and 13 for major applications. Conservation area applications may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "New Cross",
        "slug": "new-cross",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE14",
        "character": "New Cross is a Lewisham neighbourhood around Goldsmiths University, with Victorian terraces, post-war estates, and a dense student/young professional population. Flat conversions, rear extensions, and loft conversions are common.",
        "housing_stock": "Victorian terraces, Edwardian houses, post-war estates, converted HMOs",
        "conservation_notes": "Telegraph Hill Conservation Area nearby; small pockets in New Cross",
        "planning_notes": "Lewisham applies standard policies. HMO licensing and Article 4 Directions affect some streets. Flat conversions require compliance with space standards.",
        "nearby": ["brockley", "deptford", "peckham", "nunhead"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, flat conversions, and extensions for New Cross' Victorian terraces and HMO properties. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why New Cross demands specialist architectural drawings",
        "local_context_paragraphs": [
            "New Cross sits in the SE14 postcode within the London Borough of Lewisham, centred on New Cross Gate and Goldsmiths University. The neighbourhood's Victorian terraces, HMO stock, and post-war estates generate a specific project pipeline around conversions and extensions.",
            "<strong>Victorian terraces:</strong> New Cross has extensive Victorian terrace stock. Rear extensions and rear dormer loft conversions are the core projects. Most fall within PD outside conservation pockets.",
            "<strong>HMO conversions:</strong> Many New Cross properties are HMOs serving Goldsmiths students and young professionals. HMO licensing is mandatory under Lewisham's Additional Licensing scheme. Conversion to or from HMO use may require planning permission. We prepare the drawings and licensing documentation.",
            "<strong>Article 4 pockets:</strong> Lewisham has designated some Article 4 Directions affecting PD rights in New Cross. We check your property's status early.",
            "<strong>Flat conversions:</strong> Conversion of larger houses into flats requires planning permission and compliance with Lewisham's space standards.",
        ],
        "stats": [
            ("Conservation areas", "Small pockets"),
            ("Housing type", "Victorian terraces, HMOs"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE14"),
        ],
        "faqs": [
            (
                "Can I convert my New Cross house to an HMO?",
                "Converting to an HMO typically requires planning permission from Lewisham (under Article 4 where it applies) plus an HMO licence. We prepare the drawings and advise on licensing.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Outside any Article 4 zones, rear dormers under PD are straightforward. Within Article 4 — planning permission required. We check your property's status.",
            ),
            (
                "What about rear extensions?",
                "Rear extensions under PD are typically straightforward for Victorian terraces outside Article 4 zones. We prepare drawings and notifications.",
            ),
            (
                "How much do architectural drawings cost in New Cross?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Lewisham take to decide?",
                "Lewisham targets 8 weeks for householders and 13 for majors. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Greenwich Peninsula",
        "slug": "greenwich-peninsula",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE10",
        "character": "Greenwich Peninsula is a regenerating riverside area of the Royal Borough of Greenwich, dominated by new-build apartment towers around the O2 Arena, Design District, and the Greenwich Millennium Village. New-build residential interior works dominate.",
        "housing_stock": "New-build apartment towers, Millennium Village townhouses, Design District residential",
        "conservation_notes": "Core is new-build; no significant conservation coverage on the peninsula itself",
        "planning_notes": "Royal Borough of Greenwich applies the Peninsula-specific planning framework. Internal alterations in new-build require estate management and freeholder consent.",
        "nearby": ["greenwich", "charlton", "isle-of-dogs", "canary-wharf"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, internal reconfigurations, and building regulations for Greenwich Peninsula's new-build apartments and Millennium Village. MCIAT chartered, fixed fees, Greenwich planning expertise built in.",
        "local_context_title": "Why Greenwich Peninsula demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Greenwich Peninsula sits in the SE10 postcode within the Royal Borough of Greenwich, at the northern tip of the peninsula jutting into the Thames. The area is a regeneration zone — new-build apartment towers, the O2 Arena, Design District, and Millennium Village.",
            "<strong>New-build apartments:</strong> The majority of Peninsula residential stock is new-build. Internal reconfigurations need freeholder and estate management consent. Some works may require planning. Building Regulations approval is essential for all structural or service changes.",
            "<strong>Greenwich Millennium Village:</strong> The Millennium Village at the north of the Peninsula includes townhouses and low-rise apartments with specific design codes. Alterations must respect the village character.",
            "<strong>Design District:</strong> The Design District mixes residential with creative workspace. Residential alterations follow the standard Peninsula framework.",
            "<strong>Peninsula-specific planning:</strong> Greenwich has published site-specific guidance for the Peninsula. Major alterations require consultation with the masterplan team.",
        ],
        "stats": [
            ("Conservation areas", "None on peninsula"),
            ("Housing type", "New-build apartments"),
            ("Planning authority", "Royal Borough of Greenwich"),
            ("Key postcodes", "SE10"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Greenwich Peninsula apartment?",
                "Yes — internal reconfigurations are common. Freeholder and estate management consent are essential. Building Regulations approval is required. Some works may need planning. We prepare the full package.",
            ),
            (
                "What about Millennium Village townhouses?",
                "The Village has specific design codes. Extensions and external alterations require planning permission and consultation with the estate. We prepare compliant schemes.",
            ),
            (
                "Do I need planning for balcony enclosures?",
                "Usually yes — enclosing a balcony changes the external appearance and typically needs planning permission. We prepare the drawings and application.",
            ),
            (
                "How much do architectural drawings cost in Greenwich Peninsula?",
                "Our Essentials package starts from £840 for minor interior works. Complete from £1,750 for more substantial reconfigurations.",
            ),
            (
                "How long does Greenwich take to decide?",
                "Greenwich targets 8 weeks for householder and 13 for major applications. Peninsula applications may have additional consultation. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Plumstead",
        "slug": "plumstead",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE18",
        "character": "Plumstead is a residential neighbourhood of the Royal Borough of Greenwich with Victorian terraces on hilly streets, Edwardian houses, and post-war estates. Extensions, loft conversions, and flat conversions are the mainstream project types.",
        "housing_stock": "Victorian terraces, Edwardian houses, post-war estates, 1930s semis in some pockets",
        "conservation_notes": "Plumstead Common CA; small additional pockets",
        "planning_notes": "Royal Borough of Greenwich applies standard policies with heritage controls in the small CAs. Outside CAs, PD rights are intact.",
        "nearby": ["woolwich", "welling", "eltham", "charlton"],
        "popular_services": ["loft-conversions", "house-extensions", "building-regulations"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Plumstead's Victorian terraces and Edwardian homes. MCIAT chartered, fixed fees, Greenwich planning expertise built in.",
        "local_context_title": "Why Plumstead demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Plumstead sits in the SE18 postcode within the Royal Borough of Greenwich, east of Woolwich. The hilly streets of Victorian and Edwardian terraces — stepping up from the Thames — create a specific residential market.",
            "<strong>Victorian terraces:</strong> Plumstead's Victorian terraces are dense and street-facing. Rear extensions, side-return infills, and rear dormer loft conversions are the main projects. Most fall within PD outside the small CAs.",
            "<strong>Edwardian stock:</strong> Pockets of larger Edwardian houses suit more substantial extensions.",
            "<strong>Plumstead Common CA:</strong> Covers the handsome streets facing Plumstead Common. Article 4 Directions may apply. Heritage Statements are required within the CA.",
            "<strong>Hilly topography:</strong> The sloping streets create specific challenges for rear extensions — stepped sections, retaining walls, and terracing are often necessary. We design accordingly.",
        ],
        "stats": [
            ("Conservation areas", "Plumstead Common CA"),
            ("Housing type", "Victorian/Edwardian"),
            ("Planning authority", "Royal Borough of Greenwich"),
            ("Key postcodes", "SE18"),
        ],
        "faqs": [
            (
                "Can I build a rear extension on sloping ground?",
                "Yes — sloping rear gardens often benefit from stepped or split-level extensions. Structural engineering is essential. We design schemes that work with the topography.",
            ),
            (
                "Do I need planning permission in Plumstead Common CA?",
                "Yes for most external works. Heritage Statements are required. We prepare conservation-sensitive applications.",
            ),
            (
                "What about loft conversions?",
                "Outside the CAs, rear dormers under PD are straightforward. Within the CA — planning permission is required. We assess and prepare.",
            ),
            (
                "How much do architectural drawings cost in Plumstead?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Greenwich take to decide?",
                "Greenwich targets 8 weeks for householders and 13 for majors. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Mottingham",
        "slug": "mottingham",
        "borough": "Greenwich",
        "borough_slug": "greenwich",
        "postcodes": "SE9",
        "character": "Mottingham is a suburban neighbourhood straddling Greenwich and Bromley, with inter-war semis, bungalows, and some post-war developments. Extensions, loft conversions, and outbuildings are the staple projects.",
        "housing_stock": "1930s semi-detached houses, inter-war bungalows, post-war developments, some Edwardian",
        "conservation_notes": "Mottingham Conservation Area covers a small historic core",
        "planning_notes": "Royal Borough of Greenwich applies standard policies. Outside the small CA, PD rights are intact. Bromley Council covers properties on the Bromley side.",
        "nearby": ["eltham", "chislehurst", "sidcup", "plumstead"],
        "popular_services": ["house-extensions", "loft-conversions", "building-regulations"],
        "hero_lede": "Planning permission drawings, extensions, and loft conversions for Mottingham's 1930s semis and bungalows. MCIAT chartered, fixed fees, Greenwich and Bromley planning expertise built in.",
        "local_context_title": "Why Mottingham demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Mottingham sits in the SE9 postcode, straddling the borough boundary between the Royal Borough of Greenwich and the London Borough of Bromley. The neighbourhood's inter-war housing stock makes it one of south-east London's consistent extension markets.",
            "<strong>1930s semi-detached stock:</strong> Mottingham's inter-war semis typically have hipped roofs and generous rear gardens. Hip-to-gable loft conversions, 4–6m rear extensions, and two-storey side extensions are all common. Most fall within PD.",
            "<strong>Bungalows:</strong> Mottingham has a stock of 1930s bungalows. Loft conversions to add a first floor are popular, as are garage conversions.",
            "<strong>Cross-borough awareness:</strong> Properties on the Bromley side of Mottingham fall under Bromley Council; Greenwich side under the Royal Borough. We check your address early to ensure the application goes to the right authority.",
            "<strong>Small CA:</strong> The Mottingham Conservation Area covers a small historic core. Within the CA, Article 4 Directions may apply.",
        ],
        "stats": [
            ("Conservation areas", "Mottingham CA (small)"),
            ("Housing type", "1930s semis, bungalows"),
            ("Planning authority", "Greenwich / Bromley"),
            ("Key postcodes", "SE9"),
        ],
        "faqs": [
            (
                "Which council handles my Mottingham application?",
                "It depends on which side of the borough boundary your property sits. Greenwich Council covers the north; Bromley Council the south. We check the boundary early.",
            ),
            (
                "Can I add a first floor to my Mottingham bungalow?",
                "Often yes under PD subject to height, volume, and material rules. Alternatively, planning permission may be required. We assess and prepare.",
            ),
            (
                "What about rear extensions?",
                "Outside the small CA, rear extensions under PD or prior approval are straightforward. We prepare drawings and notifications.",
            ),
            (
                "How much do architectural drawings cost in Mottingham?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long do the councils take to decide?",
                "Both councils target 8 weeks for householders and 13 for majors. We manage the full process for either authority.",
            ),
        ],
    },
    {
        "name": "Hither Green",
        "slug": "hither-green",
        "borough": "Lewisham",
        "borough_slug": "lewisham",
        "postcodes": "SE13",
        "character": "Hither Green is a Lewisham neighbourhood of Victorian and Edwardian terraces, inter-war pockets, and some Victorian villas. A steady extension and loft-conversion market with increasing gentrification.",
        "housing_stock": "Victorian terraces, Edwardian houses, inter-war semis, pockets of Victorian villas",
        "conservation_notes": "Ennersdale CA; Corbett Estate CA",
        "planning_notes": "Lewisham Council applies heritage controls in the CAs. Article 4 Directions apply. Outside CAs, standard Lewisham policies with PD rights.",
        "nearby": ["lewisham", "catford", "blackheath", "brockley"],
        "popular_services": ["loft-conversions", "house-extensions", "planning-drawings"],
        "hero_lede": "Planning permission drawings, loft conversions, and extensions for Hither Green's Victorian and Edwardian terraces. MCIAT chartered, fixed fees, Lewisham planning expertise built in.",
        "local_context_title": "Why Hither Green demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Hither Green sits in the SE13 postcode within the London Borough of Lewisham, east of Lewisham itself. The neighbourhood's Victorian and Edwardian terraces — with pockets of the Corbett Estate's distinctive Victorian planning — create a varied residential market.",
            "<strong>Victorian terraces:</strong> Hither Green's Victorian terraces are the dominant stock. Rear extensions, side-return infills, and rear dormer loft conversions are the core projects.",
            "<strong>Corbett Estate CA:</strong> This large Victorian estate is a designated conservation area. Article 4 Directions apply. Heritage Statements are required for most external works.",
            "<strong>Ennersdale CA:</strong> Covers a smaller pocket. Heritage-sensitive design is required.",
            "<strong>Lewisham design standards:</strong> Lewisham publishes clear design guidance. Extensions must be subordinate and match materials. We design to these standards.",
        ],
        "stats": [
            ("Conservation areas", "Corbett Estate, Ennersdale"),
            ("Housing type", "Victorian terraces"),
            ("Planning authority", "Lewisham Council"),
            ("Key postcodes", "SE13"),
        ],
        "faqs": [
            (
                "Do I need planning permission in the Corbett Estate?",
                "Yes for most external works. Article 4 Directions apply. Heritage Statements are required. We prepare conservation-sensitive applications.",
            ),
            (
                "Can I build a rear extension outside the CA?",
                "Yes — most fall within PD or prior approval. We prepare drawings and notifications.",
            ),
            (
                "What about loft conversions?",
                "Outside the CAs, rear dormers under PD are straightforward. Within the CAs, planning permission is required.",
            ),
            (
                "How much do architectural drawings cost in Hither Green?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations.",
            ),
            (
                "How long does Lewisham take to decide?",
                "Lewisham targets 8 weeks for householders and 13 for majors. CA applications may take longer. We manage the timeline.",
            ),
        ],
    },
    {
        "name": "Rotherhithe",
        "slug": "rotherhithe",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE16",
        "character": "Rotherhithe is a riverside Southwark neighbourhood of Georgian and Victorian maritime heritage buildings, converted warehouses, and substantial new-build developments. Mixed period and new-build residential with heritage complexity.",
        "housing_stock": "Georgian maritime houses, converted warehouses, Victorian terraces, substantial new-build",
        "conservation_notes": "Rotherhithe Conservation Area covers much of the historic riverside; Rotherhithe Village CA",
        "planning_notes": "Southwark Council applies strict heritage controls in the Rotherhithe CAs. Article 4 Directions apply. Some buildings are listed. New-build estates have estate management.",
        "nearby": ["surrey-quays", "bermondsey", "isle-of-dogs", "wapping"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, warehouse conversions, heritage-sensitive extensions, and building regulations for Rotherhithe's maritime and new-build housing. MCIAT chartered, fixed fees, Southwark heritage expertise built in.",
        "local_context_title": "Why Rotherhithe demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Rotherhithe sits in the SE16 postcode within the London Borough of Southwark, on the south bank of the Thames opposite Wapping and Canary Wharf. The neighbourhood's Georgian and Victorian maritime heritage — warehouses, shipbuilding yards, and the Thames Tunnel's southern portal — sits alongside substantial new-build residential.",
            "<strong>Rotherhithe Conservation Area:</strong> Protects the historic riverside. Article 4 Directions remove PD rights. Heritage Statements are essential. Our MCIAT-chartered team prepares Rotherhithe-grade submissions.",
            "<strong>Warehouse conversions:</strong> Rotherhithe has a stock of converted warehouses and some remaining industrial stock awaiting conversion. Change-of-use applications combined with Building Regulations for fire, sound, and energy are typical.",
            "<strong>Georgian maritime houses:</strong> Some of London's most atmospheric Georgian houses line the riverside. Many are listed. Listed Building Consent runs in parallel with planning permission.",
            "<strong>New-build developments:</strong> Surrey Quays and the surrounding regeneration have added substantial new-build. Internal alterations need estate management and Building Regulations approval.",
        ],
        "stats": [
            ("Conservation areas", "Rotherhithe CA"),
            ("Article 4", "Yes"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE16"),
        ],
        "faqs": [
            (
                "Can I convert a Rotherhithe warehouse?",
                "Yes — warehouse conversions are a core Rotherhithe project type. Change-of-use planning permission, Heritage Statements (if in a CA), and full Building Regulations approval are all required. We handle the full package.",
            ),
            (
                "Do I need Listed Building Consent for my Georgian house?",
                "If your property is listed — yes. Internal and external works affecting character need LBC. We prepare the parallel applications.",
            ),
            (
                "What about new-build apartment reconfigurations?",
                "Internal reconfigurations need freeholder and estate consent plus Building Regulations. Some works may need planning. We prepare the right package.",
            ),
            (
                "How much do architectural drawings cost in Rotherhithe?",
                "For heritage and warehouse projects, the Complete package from £1,750 is typical. Essentials from £840 for minor new-build interior works.",
            ),
            (
                "How long does Southwark take to decide?",
                "Southwark targets 8–13 weeks. Listed buildings and CAs may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Surrey Quays",
        "slug": "surrey-quays",
        "borough": "Southwark",
        "borough_slug": "southwark",
        "postcodes": "SE16",
        "character": "Surrey Quays is a regenerating Southwark neighbourhood around the former docks, dominated by late 20th-century and new-build apartment developments, with ongoing major regeneration. New-build interior works and some period adjacent streets.",
        "housing_stock": "Late 20th-century and new-build apartments, some period terraces on the edges, dockland housing",
        "conservation_notes": "Rotherhithe CA nearby; core is new-build",
        "planning_notes": "Southwark Council applies the Canada Water masterplan and wider regeneration framework. Internal alterations in new-build require estate management consent.",
        "nearby": ["rotherhithe", "bermondsey", "isle-of-dogs", "canary-wharf"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, internal reconfigurations, and building regulations for Surrey Quays' new-build and dockland apartments. MCIAT chartered, fixed fees, Southwark planning expertise built in.",
        "local_context_title": "Why Surrey Quays demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Surrey Quays sits in the SE16 postcode within the London Borough of Southwark, on the former dock basin south of Rotherhithe. The neighbourhood has been redeveloped since the 1980s with dockland housing and is currently subject to the Canada Water masterplan — one of central London's largest live regeneration schemes.",
            "<strong>New-build apartments:</strong> The majority of Surrey Quays residential is new-build or late 20th-century. Internal reconfigurations need freeholder and estate consent. Building Regulations approval is essential.",
            "<strong>Canada Water masterplan:</strong> The ongoing redevelopment will add thousands of new homes. Southwark has published detailed policy guidance. Major alterations require consultation with the masterplan team.",
            "<strong>Dockland housing:</strong> Some 1980s/90s dockland housing has distinctive architectural character. Alterations should respect the original design.",
            "<strong>Period edges:</strong> Streets at the edges towards Rotherhithe include period terraces with heritage considerations.",
        ],
        "stats": [
            ("Conservation areas", "Edges only"),
            ("Housing type", "New-build apartments, dockland"),
            ("Planning authority", "Southwark Council"),
            ("Key postcodes", "SE16"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Surrey Quays apartment?",
                "Yes — internal reconfigurations are common. Freeholder and estate management consent are essential. Building Regulations approval is required. We prepare the full package.",
            ),
            (
                "What about balcony enclosures?",
                "Usually require planning permission. Structural input is essential. We prepare the drawings and application.",
            ),
            (
                "Do I need to consult the Canada Water masterplan?",
                "For major alterations or new-build proposals on adjoining sites — yes. Southwark's masterplan team coordinates. We prepare appropriate supporting documentation.",
            ),
            (
                "How much do architectural drawings cost in Surrey Quays?",
                "Our Essentials package starts from £840 for minor interior works. Complete from £1,750 for more substantial projects.",
            ),
            (
                "How long does Southwark take to decide?",
                "Southwark targets 8–13 weeks. Masterplan consultations may add time. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Isle of Dogs",
        "slug": "isle-of-dogs",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E14",
        "character": "Isle of Dogs is the Tower Hamlets neighbourhood centred on Canary Wharf and the surrounding Docklands residential developments. New-build apartment towers dominate alongside some period pockets at the southern tip.",
        "housing_stock": "New-build apartment towers, Canary Wharf residential, late 20th-century dockland, Victorian pockets at Cubitt Town",
        "conservation_notes": "Coldharbour CA; some isolated heritage pockets",
        "planning_notes": "Tower Hamlets applies the Canary Wharf and Isle of Dogs planning frameworks. Internal alterations in new-build require estate management consent alongside Building Regulations.",
        "nearby": ["canary-wharf", "limehouse", "greenwich-peninsula", "rotherhithe"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, internal reconfigurations, and building regulations for Isle of Dogs' Canary Wharf and Docklands apartments. MCIAT chartered, fixed fees, Tower Hamlets planning expertise built in.",
        "local_context_title": "Why Isle of Dogs demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Isle of Dogs sits in the E14 postcode within the London Borough of Tower Hamlets, in the loop of the Thames containing Canary Wharf and the southern Docklands. The neighbourhood is dominated by new-build apartment towers with substantial regeneration continuing.",
            "<strong>Canary Wharf residential:</strong> The Canary Wharf estate includes substantial high-rise residential. Internal reconfigurations require Canary Wharf Group consent alongside Tower Hamlets planning and Building Regulations.",
            "<strong>Docklands apartments:</strong> The wider Isle of Dogs has extensive late 20th-century and new-build residential. Estate management consent is routine for internal works.",
            "<strong>Coldharbour and Cubitt Town:</strong> Pockets of Victorian and Georgian heritage remain at the southern tip. Coldharbour CA protects historic dock cottages. Heritage-sensitive design is essential for any CA works.",
            "<strong>Tower Hamlets policy:</strong> Tower Hamlets has published detailed policy for the Isle of Dogs emphasising high-density, high-quality design.",
        ],
        "stats": [
            ("Conservation areas", "Coldharbour CA"),
            ("Housing type", "New-build apartments"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E14"),
        ],
        "faqs": [
            (
                "Can I reconfigure my Canary Wharf apartment?",
                "Yes — internal reconfigurations are common. Canary Wharf Group and freeholder consent are essential. Building Regulations approval is required. Some works may need planning. We prepare the full package.",
            ),
            (
                "What about Coldharbour heritage properties?",
                "Coldharbour is tightly controlled. Every external work needs planning permission and Heritage Statement. Many buildings are listed. We prepare conservation-grade submissions.",
            ),
            (
                "Can I add a mezzanine in my double-height apartment?",
                "Possibly — subject to freeholder consent, structural checks, and Building Regulations (fire escape, headroom). Planning permission may or may not be needed. We advise.",
            ),
            (
                "How much do architectural drawings cost in Isle of Dogs?",
                "Our Essentials package starts from £840 for minor interior works. Complete from £1,750 for reconfigurations. Canary Wharf projects may require bespoke pricing.",
            ),
            (
                "How long does Tower Hamlets take to decide?",
                "Tower Hamlets targets 8 weeks for householder and 13 for majors. Canary Wharf consultations may add time. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Limehouse",
        "slug": "limehouse",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E14",
        "character": "Limehouse is an east London Tower Hamlets neighbourhood of converted warehouses, Georgian maritime heritage, and new-build apartments along the Limehouse Basin. Heritage-sensitive warehouse conversions and new-build interior works dominate.",
        "housing_stock": "Converted warehouses, Georgian maritime houses, Victorian terraces, new-build apartments around Limehouse Basin",
        "conservation_notes": "Narrow Street Conservation Area; Limehouse Cut CA; multiple listed buildings",
        "planning_notes": "Tower Hamlets applies strict heritage controls in the Limehouse CAs. Article 4 Directions apply. Listed Building Consent common. New-build estates have estate management.",
        "nearby": ["wapping", "isle-of-dogs", "mile-end", "canary-wharf"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, warehouse conversions, heritage-sensitive extensions, and building regulations for Limehouse's maritime and new-build housing. MCIAT chartered, fixed fees, Tower Hamlets heritage expertise built in.",
        "local_context_title": "Why Limehouse demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Limehouse sits in the E14 postcode within the London Borough of Tower Hamlets, east of Wapping along the Thames. The neighbourhood's Georgian maritime heritage, converted warehouses, and new-build apartments around Limehouse Basin make it one of east London's most architecturally varied residential markets.",
            "<strong>Warehouse conversions:</strong> Limehouse has a significant stock of converted and convertible warehouses. Change-of-use planning permission combined with full Building Regulations approval is typical. Our team handles the full package.",
            "<strong>Georgian Narrow Street:</strong> Narrow Street is one of London's most atmospheric Georgian riverside streets. Conservation area protection is strong. Many buildings are listed. Listed Building Consent is routine.",
            "<strong>Limehouse Basin:</strong> The marina development includes substantial new-build residential. Internal reconfigurations need estate management consent and Building Regulations approval.",
            "<strong>Tower Hamlets design standards:</strong> Tower Hamlets applies high design standards in Limehouse reflecting the heritage context.",
        ],
        "stats": [
            ("Conservation areas", "Narrow Street, Limehouse Cut"),
            ("Listed buildings", "Multiple"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E14"),
        ],
        "faqs": [
            (
                "Can I convert a Limehouse warehouse?",
                "Yes — change-of-use planning permission, Heritage Statement (if in CA), Listed Building Consent (if listed), and full Building Regulations approval are all typically required. We handle the full package.",
            ),
            (
                "Do I need Listed Building Consent on Narrow Street?",
                "Many Narrow Street properties are listed. LBC is required for most works affecting character. We prepare LBC alongside planning.",
            ),
            (
                "Can I alter my Limehouse Basin apartment?",
                "Internal reconfigurations need freeholder and estate consent plus Building Regulations. We prepare the full package.",
            ),
            (
                "How much do architectural drawings cost in Limehouse?",
                "For heritage and warehouse projects, Complete from £1,750 is typical. Essentials from £840 for minor new-build interior works.",
            ),
            (
                "How long does Tower Hamlets take to decide?",
                "Tower Hamlets targets 8–13 weeks. Listed buildings and CAs may take longer. We manage the full process.",
            ),
        ],
    },
    {
        "name": "Wapping",
        "slug": "wapping",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E1W",
        "character": "Wapping is a riverside Tower Hamlets neighbourhood of converted Georgian and Victorian warehouses, historic maritime infrastructure, and some new-build. Heritage-sensitive warehouse conversions and listed building works dominate.",
        "housing_stock": "Converted warehouses, Georgian maritime houses, Victorian terraces, some new-build apartments",
        "conservation_notes": "Wapping Wall CA; St Katharine Docks CA; many listed buildings",
        "planning_notes": "Tower Hamlets applies strict heritage controls throughout Wapping. Article 4 Directions apply. Listed Building Consent routine. World Heritage Site (Tower of London) buffer extends close.",
        "nearby": ["limehouse", "whitechapel", "isle-of-dogs", "bermondsey"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, warehouse conversions, Listed Building Consent, and heritage-sensitive building regulations for Wapping's maritime and Georgian housing. MCIAT chartered, fixed fees, Tower Hamlets heritage expertise built in.",
        "local_context_title": "Why Wapping demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Wapping sits in the E1W postcode within the London Borough of Tower Hamlets, on the north bank of the Thames east of the Tower of London. The neighbourhood's Georgian maritime heritage — docks, warehouses, and riverside cottages — is among the most complete in London.",
            "<strong>Warehouse conversions:</strong> Wapping has extensive converted warehouse stock. Further conversions face strict heritage controls. Every scheme requires planning permission, Heritage Statement, and often Listed Building Consent. Our team handles the full package.",
            "<strong>Wapping Wall CA:</strong> Covers the historic riverside. Article 4 Directions remove PD rights. Heritage Statements essential.",
            "<strong>Listed buildings:</strong> A high proportion of Wapping housing is listed — many Grade II, some Grade II*. Listed Building Consent is routine. We coordinate with Historic England where needed.",
            "<strong>Tower of London WHS buffer:</strong> Parts of Wapping sit within the Tower of London World Heritage Site buffer zone. Proposals visible from the Tower need additional heritage justification.",
        ],
        "stats": [
            ("Conservation areas", "Wapping Wall, St Katharine's"),
            ("Listed buildings", "Extensive"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E1W"),
        ],
        "faqs": [
            (
                "Can I alter my Wapping warehouse apartment?",
                "Internal alterations in listed warehouses need Listed Building Consent. External alterations also need planning permission. We prepare both.",
            ),
            (
                "Do I need a Heritage Impact Assessment?",
                "For major works or works in the Tower of London WHS buffer — yes. We prepare detailed HIAs including verified views.",
            ),
            (
                "Can I add a rooflight in a listed building?",
                "Possibly — subject to design, position, and LBC. Conservation officers typically prefer concealed or minimally visible rooflights. We prepare appropriate schemes.",
            ),
            (
                "How much do architectural drawings cost in Wapping?",
                "Listed and heritage projects typically require Complete from £1,750 or bespoke pricing for major listed buildings. Essentials from £840 for minor new-build works.",
            ),
            (
                "How long does Tower Hamlets take to decide?",
                "Wapping applications typically take 8–13 weeks. Listed Building Consent runs in parallel. Historic England consultation may add time for higher-grade listings. We manage the full timeline.",
            ),
        ],
    },
    {
        "name": "Whitechapel",
        "slug": "whitechapel",
        "borough": "Tower Hamlets",
        "borough_slug": "tower-hamlets",
        "postcodes": "E1",
        "character": "Whitechapel is a Tower Hamlets neighbourhood of Victorian terraces, Georgian survivals, post-war estates, and major new-build regeneration. Mixed heritage-sensitive and new-build residential work with major regeneration around Whitechapel station.",
        "housing_stock": "Victorian terraces, Georgian survivals, Victorian warehouses, post-war estates, substantial new-build",
        "conservation_notes": "Whitechapel High Street CA; Fournier Street CA (Spitalfields edges)",
        "planning_notes": "Tower Hamlets applies heritage controls in the CAs. Article 4 Directions apply. Major Elizabeth line regeneration around Whitechapel station has its own planning framework.",
        "nearby": ["wapping", "shoreditch", "mile-end", "limehouse"],
        "popular_services": ["planning-drawings", "building-regulations", "loft-conversions"],
        "hero_lede": "Planning permission drawings, heritage-sensitive extensions, warehouse conversions, and building regulations for Whitechapel's Victorian and new-build housing. MCIAT chartered, fixed fees, Tower Hamlets planning expertise built in.",
        "local_context_title": "Why Whitechapel demands specialist architectural drawings",
        "local_context_paragraphs": [
            "Whitechapel sits in the E1 postcode within the London Borough of Tower Hamlets, east of the City. The neighbourhood's Victorian terraces, Georgian survivals, and ongoing regeneration around Whitechapel Elizabeth line station create a mixed planning environment.",
            "<strong>Victorian terraces:</strong> Whitechapel's Victorian terraces are dense. Rear extensions, loft conversions, and flat conversions are common. Article 4 Directions affect some streets.",
            "<strong>Georgian survivals:</strong> Some streets retain Georgian and early Victorian stock of significant heritage value, particularly near Fournier Street at the Spitalfields edge. Many are listed.",
            "<strong>Whitechapel High Street CA:</strong> Covers the historic core. Article 4 Directions apply. Heritage Statements required.",
            "<strong>Regeneration context:</strong> The Whitechapel Elizabeth line station has catalysed substantial redevelopment. Major new-build schemes are underway or complete. Policy context is actively shifting.",
        ],
        "stats": [
            ("Conservation areas", "Whitechapel High Street CA"),
            ("Housing type", "Victorian, new-build"),
            ("Planning authority", "Tower Hamlets Council"),
            ("Key postcodes", "E1"),
        ],
        "faqs": [
            (
                "Can I convert my Whitechapel Victorian house into flats?",
                "With planning permission from Tower Hamlets and compliance with space and amenity standards. HMO licensing may also apply. We prepare the full package.",
            ),
            (
                "Do I need planning permission for a loft conversion?",
                "Outside Article 4 zones, rear dormers under PD are straightforward. Within the CA or Article 4 — planning permission required. We check your property.",
            ),
            (
                "What about warehouse conversions?",
                "Change-of-use planning, Heritage Statement, and full Building Regulations approval are typically required. We handle the full package.",
            ),
            (
                "How much do architectural drawings cost in Whitechapel?",
                "Our Essentials package starts from £840. Complete from £1,750 covers planning and building regulations plus structural calculations. Conservation-grade projects typically need Complete.",
            ),
            (
                "How long does Tower Hamlets take to decide?",
                "Tower Hamlets targets 8–13 weeks. Conservation area and listed building applications may take longer. We manage the full process.",
            ),
        ],
    },
]


# ---------------------------------------------------------------------------
# HTML Template
# ---------------------------------------------------------------------------

def esc(s):
    """HTML-escape text."""
    return html.escape(s, quote=True)


def generate_page(n):
    """Generate a complete HTML page for neighbourhood dict `n`."""

    name = n["name"]
    slug = n["slug"]
    borough = n["borough"]
    borough_slug = n["borough_slug"]
    postcodes = n["postcodes"]
    postcodes_esc = esc(postcodes)

    title = f"Architectural Drawings {name} | Planning & Loft | AD"
    description = f"Architectural drawings in {name}, {postcodes} — planning, loft conversions & extensions. MCIAT chartered, fixed fees from £840. {borough} specialists."
    canonical = f"https://www.architecturaldrawings.uk/areas/neighbourhoods/{slug}.html"

    # FAQs for schema
    faq_schema_items = []
    for q, a in n["faqs"]:
        faq_schema_items.append(
            f'{{"@type":"Question","name":{json.dumps(q)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a)}}}}}'
        )
    faq_schema = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ",".join(faq_schema_items) + "]}"

    # Breadcrumb schema
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.architecturaldrawings.uk/"},
            {"@type": "ListItem", "position": 2, "name": "Areas", "item": "https://www.architecturaldrawings.uk/areas/"},
            {"@type": "ListItem", "position": 3, "name": borough, "item": f"https://www.architecturaldrawings.uk/areas/{borough_slug}/"},
            {"@type": "ListItem", "position": 4, "name": name, "item": canonical},
        ],
    }, indent=2)

    # Service schema
    service_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Architectural Drawings",
        "provider": {
            "@type": "ProfessionalService",
            "name": "Architectural Drawings London",
            "@id": "https://www.architecturaldrawings.uk/#business",
            "url": "https://www.architecturaldrawings.uk/",
            "telephone": "+44 20 7946 0000",
            "priceRange": "££",
        },
        "areaServed": {
            "@type": "Place",
            "name": f"{name}, London",
            "containedInPlace": {"@type": "AdministrativeArea", "name": borough},
        },
        "offers": {"@type": "Offer", "price": "840", "priceCurrency": "GBP"},
        "description": f"Architectural drawings in {name} — planning permission, loft conversions, extensions. MCIAT chartered team. Fixed fees from £840.",
    }, indent=2)

    # Trust badge items
    trust_items = [
        "From £840 fixed fee",
        f"MCIAT chartered, {borough}",
        f"{postcodes_esc} postcodes",
    ]

    # Local context paragraphs
    context_paragraphs = ""
    for p in n["local_context_paragraphs"]:
        context_paragraphs += f'      <p style="color: var(--ink-soft); margin-bottom: 20px;">{p}</p>\n\n'

    # Stats grid
    stats_html = ""
    for label, value in n["stats"]:
        stats_html += f'        <div class="local-stat"><div class="local-stat-label">{esc(label)}</div><div class="local-stat-value">{esc(value)}</div></div>\n'

    # FAQ items
    faq_items_html = ""
    for q, a in n["faqs"]:
        faq_items_html += f'        <details class="faq-item"><summary class="faq-q">{esc(q)}<span class="faq-q-icon"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 2v8M2 6h8"/></svg></span></summary><div class="faq-a"><p>{esc(a)}</p></div></details>\n'

    # Nearby neighbourhoods
    # Combine existing and new slugs for linking
    all_neighbourhood_slugs = {nn["slug"]: nn for nn in NEIGHBOURHOODS}
    # Also add existing 16
    EXISTING_NEIGHBOURHOODS = {
        "angel-islington": {"name": "Angel & Islington", "borough": "Islington", "postcodes": "N1"},
        "battersea": {"name": "Battersea", "borough": "Wandsworth", "postcodes": "SW11"},
        "brixton": {"name": "Brixton", "borough": "Lambeth", "postcodes": "SW2, SW9"},
        "chiswick": {"name": "Chiswick", "borough": "Hounslow", "postcodes": "W4"},
        "clapham": {"name": "Clapham", "borough": "Lambeth", "postcodes": "SW4, SW11"},
        "crouch-end": {"name": "Crouch End", "borough": "Haringey", "postcodes": "N8"},
        "dulwich": {"name": "Dulwich", "borough": "Southwark", "postcodes": "SE21"},
        "fulham": {"name": "Fulham", "borough": "Hammersmith & Fulham", "postcodes": "SW6"},
        "hampstead": {"name": "Hampstead", "borough": "Camden", "postcodes": "NW3, NW11"},
        "highgate": {"name": "Highgate", "borough": "Haringey/Camden", "postcodes": "N6"},
        "muswell-hill": {"name": "Muswell Hill", "borough": "Haringey", "postcodes": "N10"},
        "notting-hill": {"name": "Notting Hill", "borough": "Kensington & Chelsea", "postcodes": "W11"},
        "peckham": {"name": "Peckham", "borough": "Southwark", "postcodes": "SE15"},
        "richmond": {"name": "Richmond", "borough": "Richmond upon Thames", "postcodes": "TW9, TW10"},
        "stoke-newington": {"name": "Stoke Newington", "borough": "Hackney", "postcodes": "N16"},
        "wimbledon": {"name": "Wimbledon", "borough": "Merton", "postcodes": "SW19"},
    }

    nearby_html = ""
    for ns in n["nearby"]:
        if ns in all_neighbourhood_slugs:
            nn = all_neighbourhood_slugs[ns]
            nearby_html += f'      <a href="{ns}.html" class="adjacent-card"><strong>{esc(nn["name"])}</strong><span>{esc(nn["borough"])}, {esc(nn["postcodes"])}</span></a>\n'
        elif ns in EXISTING_NEIGHBOURHOODS:
            en = EXISTING_NEIGHBOURHOODS[ns]
            nearby_html += f'      <a href="{ns}.html" class="adjacent-card"><strong>{esc(en["name"])}</strong><span>{esc(en["borough"])}, {esc(en["postcodes"])}</span></a>\n'
        else:
            # Fallback: link to borough hub
            nearby_html += f'      <a href="../{ns}/" class="adjacent-card"><strong>{ns.replace("-", " ").title()}</strong><span>Borough hub</span></a>\n'

    # Service cards
    service_cards_html = ""
    for svc_slug in n["popular_services"]:
        svc = SERVICES.get(svc_slug, {})
        svc_name = svc.get("name", svc_slug.replace("-", " ").title())
        svc_price = svc.get("price", "£840")
        svc_desc = SERVICE_DESCRIPTIONS.get(svc_slug, "Professional architectural drawings and planning submissions.")
        service_cards_html += f'      <a href="../../services/{svc_slug}.html" class="service-card"><h3>{esc(svc_name)}</h3><p>{esc(svc_desc)}</p><div class="service-card-footer"><span class="service-card-price"><span class="from">from</span> {svc_price}</span><span class="service-card-link">View</span></div></a>\n'

    # Build the page
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#FAFAF7" />

<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="{canonical}" />

<!-- Open Graph -->
<meta property="og:type" content="article" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(description)}" />
<meta property="og:locale" content="en_GB" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1116'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' fill='%23FAFAF7' font-family='Georgia,serif' font-weight='500' font-size='17' font-style='italic'%3EA%3C/text%3E%3C/svg%3E" />

<!-- Schema: Service -->
<script type="application/ld+json">
{service_schema}
</script>

<!-- Schema: FAQPage (AEO) -->
<script type="application/ld+json">
{faq_schema}
</script>

<!-- Schema: BreadcrumbList -->
<script type="application/ld+json">
{breadcrumb_schema}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>
<style>
{CSS_INLINE}

/* ===== pSEO additions ===== */
.tldr {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  border-radius: var(--r-lg);
  padding: 28px 32px;
  margin: 32px 0;
}}
.tldr h3 {{
  font-size: 0.82rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-deep);
  font-family: var(--font-body);
  font-weight: 700;
  margin-bottom: 14px;
}}
.tldr dl {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px 32px;
}}
@media (max-width: 720px) {{ .tldr dl {{ grid-template-columns: 1fr; }} }}
.tldr dt {{
  font-size: 0.84rem;
  color: var(--ink-soft);
  margin-bottom: 2px;
}}
.tldr dd {{
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-variation-settings: "opsz" 36;
  letter-spacing: -0.005em;
  color: var(--ink);
}}

.local-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 32px 0;
}}
@media (max-width: 900px) {{ .local-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
.local-stat {{
  background: var(--bg-2);
  border-radius: var(--r-md);
  padding: 20px 22px;
}}
.local-stat-label {{ font-size: 0.78rem; color: var(--ink-soft); margin-bottom: 6px; }}
.local-stat-value {{
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-variation-settings: "opsz" 60;
  letter-spacing: -0.01em;
  line-height: 1.2;
}}

.adjacent-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin: 20px 0;
}}
.adjacent-card {{
  padding: 16px 20px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  transition: all 0.2s var(--ease);
  display: block;
}}
.adjacent-card:hover {{
  border-color: var(--accent);
  background: var(--accent-soft);
  transform: translateY(-2px);
}}
.adjacent-card strong {{ display: block; color: var(--ink); font-size: 0.96rem; }}
.adjacent-card span {{ font-size: 0.82rem; color: var(--ink-soft); }}

.related-services {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
  margin: 20px 0;
}}

/* Image placeholder */
.img-placeholder {{
  background: var(--bg-2);
  border: 1px dashed var(--line-strong);
  border-radius: var(--r-lg);
  padding: 60px 32px;
  text-align: center;
  color: var(--ink-soft);
  font-size: 0.92rem;
}}
.img-placeholder strong {{ display: block; margin-bottom: 4px; color: var(--ink); }}

/* Reveal safety net */
@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ opacity: 0; transform: translateY(20px); transition: opacity 0.8s var(--ease), transform 0.8s var(--ease); animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}

@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }}
  .reveal {{ opacity: 1; transform: none; }}
}}

/* Print */
@media print {{
  .nav, .footer, .cta-band {{ display: none; }}
  body {{ background: white; color: black; }}
}}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="../../" class="logo" aria-label="Architectural Drawings London home">
      <span class="logo-mark">A</span>
      <span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
        <li><a href="../../services.html">Services</a></li>
        <li><a href="../../pricing.html">Pricing</a></li>
        <li><a href="../../areas/">Areas</a></li>
        <li><a href="../../about.html">About</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a href="../../portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="../../quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<!-- ===== HERO ===== -->
<section class="hero">
  <div class="container hero-grid">
    <div>
      <nav aria-label="Breadcrumb" style="font-size: 0.85rem; color: var(--ink-soft); margin-bottom: 20px;">
        <a href="../../" style="color: var(--ink-soft);">Home</a> /
        <a href="../" style="color: var(--ink-soft);">Areas</a> /
        <a href="../{borough_slug}/" style="color: var(--ink-soft);">{esc(borough)}</a> /
        <strong style="color: var(--ink);">{esc(name)}</strong>
      </nav>
      <span class="eyebrow">{esc(borough)}</span>
      <h1 style="margin: 16px 0 24px;">Architectural drawings in <span style="color: var(--accent); font-style: italic; font-weight: 300;">{esc(name)}</span></h1>
      <p class="hero-lede">{esc(n["hero_lede"])}</p>
      <div class="hero-ctas">
        <a href="../../quote.html?location={slug}" class="btn btn-primary btn-lg">Get a free quote</a>
        <a href="#pricing" class="btn btn-outline btn-lg">See pricing</a>
      </div>
      <div class="hero-trust" style="margin-top: 32px;">
        <span class="hero-trust-item"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>{esc(trust_items[0])}</span>
        <span class="hero-trust-item"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>{esc(trust_items[1])}</span>
        <span class="hero-trust-item"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>{esc(trust_items[2])}</span>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-img-main">
        <picture>
          <source type="image/avif" srcset="../../assets/img/blueprint-tablet-640.avif 640w, ../../assets/img/blueprint-tablet-1024.avif 1024w, ../../assets/img/blueprint-tablet-1600.avif 1600w" sizes="(max-width: 960px) 100vw, 50vw" />
          <source type="image/webp" srcset="../../assets/img/blueprint-tablet-640.webp 640w, ../../assets/img/blueprint-tablet-1024.webp 1024w, ../../assets/img/blueprint-tablet-1600.webp 1600w" sizes="(max-width: 960px) 100vw, 50vw" />
          <img src="../../assets/img/blueprint-tablet-1600.jpg" alt="Architectural drawings for {esc(name)} properties" width="1600" height="945" fetchpriority="high" />
        </picture>
      </div>
    </div>
  </div>
</section>

<!-- ===== TL;DR ===== -->
<section style="padding-top: 0;">
  <div class="container">
    <div class="tldr">
      <h3>Quick facts -- Architectural drawings in {esc(name)}</h3>
      <dl>
        <div><dt>Nearest borough hub</dt><dd><a href="../{borough_slug}/" style="color: var(--accent-deep);">{esc(borough)}</a></dd></div>
        <div><dt>Postcodes</dt><dd>{postcodes_esc}</dd></div>
        <div><dt>Conservation status</dt><dd>{esc(n["conservation_notes"])}</dd></div>
        <div><dt>Typical housing</dt><dd>{esc(n["housing_stock"])}</dd></div>
        <div><dt>Our fee from</dt><dd>&pound;840 + VAT</dd></div>
        <div><dt>Key planning note</dt><dd>{esc(n["planning_notes"][:200])}</dd></div>
      </dl>
    </div>
  </div>
</section>

<!-- ===== PLACEHOLDER IMAGES ===== -->
<section style="padding-top: 0;">
  <div class="container" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div class="img-placeholder">
      <strong>Image: {esc(name)} streetscape</strong>
      Aerial or street-level view of {esc(name)}'s characteristic housing, showing the local architectural character and streetscape.
    </div>
    <div class="img-placeholder">
      <strong>Image: Architectural drawings detail</strong>
      Close-up of scaled planning drawings for a {esc(name)} property, showing existing and proposed elevations with planning annotations.
    </div>
  </div>
</section>

<!-- ===== LOCAL CONTEXT ===== -->
<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Local context</span>
      <h2 style="margin-top: 16px;">{n["local_context_title"].replace(name, f"<em>{name}</em>")}</h2>
    </div>
    <div style="max-width: 800px;">
{context_paragraphs}
      <div class="local-grid">
{stats_html}      </div>
    </div>
  </div>
</section>

<!-- ===== PRICING ===== -->
<section id="pricing">
  <div class="container">
    <div class="section-header" style="text-align: center; margin: 0 auto;">
      <span class="eyebrow">Fixed fee -- 30% below London architects</span>
      <h2 style="margin-top: 16px;">Architectural drawings pricing in {esc(name)}</h2>
    </div>
    <div class="pricing-grid">
      <div class="pricing-card">
        <h3>Essentials</h3>
        <p class="muted">Single planning or regs submission.</p>
        <div class="pricing-price"><span class="from">from</span><span class="amount">&pound;840</span></div>
        <ul class="pricing-features">
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Measured survey</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Drawings &amp; submission</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Unlimited revisions</li>
        </ul>
        <a href="../../quote.html?location={slug}&amp;tier=essentials" class="btn btn-outline btn-block">Start Essentials</a>
      </div>
      <div class="pricing-card popular">
        <span class="pricing-popular-tag">Most popular</span>
        <h3>Complete</h3>
        <p style="color: rgba(250,250,247,0.7);">Planning + building regs + structural.</p>
        <div class="pricing-price"><span class="from">from</span><span class="amount">&pound;1,750</span></div>
        <ul class="pricing-features">
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Everything in Essentials</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Building regs drawings</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Structural calculations</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Heritage Statement if needed</li>
        </ul>
        <a href="../../quote.html?location={slug}&amp;tier=complete" class="btn btn-accent btn-block">Start Complete</a>
      </div>
      <div class="pricing-card">
        <h3>Bespoke</h3>
        <p class="muted">Listed, conservation, complex sites.</p>
        <div class="pricing-price"><span class="amount serif">Custom</span></div>
        <ul class="pricing-features">
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Everything in Complete</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Listed Building Consent</li>
          <li><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 10 3 3 7-7"/></svg>Committee representation</li>
        </ul>
        <a href="../../quote.html?location={slug}&amp;tier=bespoke" class="btn btn-outline btn-block">Discuss Bespoke</a>
      </div>
    </div>
  </div>
</section>

<!-- ===== FAQ ===== -->
<section class="faq">
  <div class="container">
    <div class="faq-grid">
      <div class="faq-aside">
        <span class="eyebrow">{esc(name)} FAQs</span>
        <h2 style="margin-top: 16px;">Architectural drawings in {esc(name)} — <em>your questions answered.</em></h2>
        <p>Direct answers to the questions {esc(name)} homeowners ask us every week about planning, extensions, and loft conversions.</p>
        <a href="../../quote.html?location={slug}" class="btn btn-primary">Start a free quote</a>
      </div>
      <div class="faq-list">
{faq_items_html}      </div>
    </div>
  </div>
</section>

<!-- ===== ADJACENT NEIGHBOURHOODS ===== -->
<section>
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Nearby neighbourhoods</span>
      <h2 style="margin-top: 16px;">Architectural drawings in areas <em>near {esc(name)}</em></h2>
      <p>We cover every London neighbourhood. Here are areas adjacent to {esc(name)} where we work regularly.</p>
    </div>
    <div class="adjacent-grid">
{nearby_html}    </div>
  </div>
</section>

<!-- ===== RELATED SERVICES ===== -->
<section style="background: var(--bg-2);">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Services in {esc(name)}</span>
      <h2 style="margin-top: 16px;">Specialist services for <em>{esc(name)} properties</em></h2>
      <p>Every service you need for a {esc(name)} project, from a single chartered team.</p>
    </div>
    <div class="services-grid">
{service_cards_html}    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="cta-band">
  <div class="container">
    <h2>Start your {esc(name)} project <span class="accent">this week.</span></h2>
    <p>Free quote in 60 seconds. Fixed fee from &pound;840. MCIAT chartered. Conservation area expertise included.</p>
    <a href="../../quote.html?location={slug}" class="btn btn-primary btn-lg">Get my free quote</a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div><h5>Services in London</h5><ul>
        <li><a href="../../services/planning-drawings.html">Planning permission drawings London</a></li>
        <li><a href="../../services/building-regulations.html">Building regulations drawings London</a></li>
        <li><a href="../../services/loft-conversions.html">Loft conversion drawings London</a></li>
        <li><a href="../../services/house-extensions.html">House extension plans London</a></li>
        <li><a href="../../services/mansard-roof.html">Mansard roof extensions London</a></li>
      </ul></div>
      <div><h5>Loft conversions by borough</h5><ul>
        <li><a href="../camden/loft-conversions.html">Loft conversion Camden</a></li>
        <li><a href="../islington/loft-conversions.html">Loft conversion Islington</a></li>
        <li><a href="../hackney/loft-conversions.html">Loft conversion Hackney</a></li>
        <li><a href="../wandsworth/loft-conversions.html">Loft conversion Wandsworth</a></li>
        <li><a href="../lambeth/loft-conversions.html">Loft conversion Lambeth</a></li>
      </ul></div>
      <div><h5>Extension plans by borough</h5><ul>
        <li><a href="../lewisham/house-extensions.html">Extension plans Lewisham</a></li>
        <li><a href="../greenwich/house-extensions.html">Extension plans Greenwich</a></li>
        <li><a href="../bromley/house-extensions.html">Extension plans Bromley</a></li>
        <li><a href="../croydon/house-extensions.html">Extension plans Croydon</a></li>
        <li><a href="../merton/house-extensions.html">Extension plans Merton</a></li>
      </ul></div>
      <div><h5>Neighbourhoods</h5><ul>
        <li><a href="clapham.html">Architectural drawings Clapham</a></li>
        <li><a href="dulwich.html">Architectural drawings Dulwich</a></li>
        <li><a href="muswell-hill.html">Architectural drawings Muswell Hill</a></li>
        <li><a href="notting-hill.html">Architectural drawings Notting Hill</a></li>
        <li><a href="crouch-end.html">Architectural drawings Crouch End</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom" style="border-top: 0; padding-top: 0;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; Serving {esc(name)} and all 33 London boroughs</span>
      <span><a href="../../">Home</a> &middot; <a href="../../services.html">All services</a> &middot; <a href="../../pricing.html">Pricing</a> &middot; <a href="../../areas/">All areas</a> &middot; <a href="../../privacy.html">Privacy</a> &middot; <a href="../../terms.html">Terms</a></span>
    </div>
  </div>
</footer>

<script>
// Reveal + nav scroll
document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
const nav = document.getElementById('nav');
if (nav) {{
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 12);
  onScroll();
  window.addEventListener('scroll', onScroll, {{ passive: true }});
}}
document.querySelectorAll('.faq-item').forEach(i => i.addEventListener('toggle', () => i.classList.toggle('open', i.open)));
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="Call us"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg></a>
  <a href="https://wa.me/442079460000" target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="WhatsApp"><svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a3.04 3.04 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg></a>
</div>

</body>
</html>'''

    return page


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    skipped = []
    for n in NEIGHBOURHOODS:
        out_path = OUT_DIR / f"{n['slug']}.html"
        if out_path.exists():
            skipped.append(n["slug"])
            continue
        page_html = generate_page(n)
        out_path.write_text(page_html, encoding="utf-8")
        size_kb = len(page_html.encode("utf-8")) / 1024
        generated.append((n["slug"], n["name"], size_kb))
        print(f"  + {out_path.name} ({size_kb:.1f} KB)")

    print(f"\nGenerated {len(generated)} new neighbourhood pages in {OUT_DIR}")
    print(f"Skipped {len(skipped)} existing pages (already on disk)")
    if generated:
        total_kb = sum(s for _, _, s in generated)
        print(f"Total new: {total_kb:.0f} KB ({total_kb/1024:.1f} MB)")


if __name__ == "__main__":
    main()
