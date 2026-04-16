#!/usr/bin/env python3
"""
gen_neighbourhoods.py
Generate neighbourhood-level landing pages under areas/neighbourhoods/.

Usage:
    cd architectural-drawings
    python scripts/gen_neighbourhoods.py

Generates 34 new neighbourhood pages (not the original 16).
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
# 34 new neighbourhoods
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
    for n in NEIGHBOURHOODS:
        page_html = generate_page(n)
        out_path = OUT_DIR / f"{n['slug']}.html"
        out_path.write_text(page_html, encoding="utf-8")
        size_kb = len(page_html.encode("utf-8")) / 1024
        generated.append((n["slug"], n["name"], size_kb))
        print(f"  + {out_path.name} ({size_kb:.1f} KB)")

    print(f"\nGenerated {len(generated)} neighbourhood pages in {OUT_DIR}")
    total_kb = sum(s for _, _, s in generated)
    print(f"Total: {total_kb:.0f} KB ({total_kb/1024:.1f} MB)")


if __name__ == "__main__":
    main()
