#!/usr/bin/env python3
"""
Service data for pSEO pages. Each service has:
- name, slug, short description
- service-specific content adapted per location
- FAQ templates with location placeholders
- price range
- hero image
"""

SERVICES = {
    "planning-drawings": {
        "name": "Planning Drawings",
        "h1_lead": "Planning Permission Drawings",
        "short": "planning permission drawings",
        "price_from": 840,
        "price_display": "£840",
        "turnaround": "3–4 weeks to submission",
        "hero_img": "blueprint-tablet",
        "kind": "planning",
        "summary": (
            "A fixed-fee, end-to-end service — measured survey, scaled drawings, "
            "Design & Access Statement where required, Planning Portal submission, "
            "and full agent liaison until the council's decision."
        ),
        "keywords": [
            "planning drawings", "planning permission drawings", "planning application",
            "planning consultant", "householder planning", "full planning"
        ],
        "what_included": [
            ("Measured site survey", "A chartered technologist visits and laser-measures every room. Typically 60–90 minutes on site."),
            ("Existing &amp; proposed plans", "Drafted in Revit or AutoCAD at 1:100 or 1:50. Fully annotated and council-ready."),
            ("Design iterations", "Unlimited revisions until you approve. Shadow studies for committee-sensitive applications."),
            ("Supporting documents", "Site location plan, block plan, Design &amp; Access Statement where required."),
            ("Planning Portal submission", "We lodge the application with {authority} and pay statutory fees directly."),
            ("Agent service to decision", "Every officer query, consultation response and amendment handled through to determination."),
        ],
        "local_faqs": [
            ("How much do planning drawings cost in {location}?",
             "Our fixed-fee householder planning package for {location} starts at £840. Full planning applications (major works, change of use, flat conversions) start at £1,750. {location_council} charges a separate statutory fee of £258 for householder or £578 for full dwellinghouse applications."),
            ("How long does {location_council} take to decide planning applications?",
             "Once validated, {location_council} aims to decide householder applications within 8 weeks and major applications within 13 weeks — consistent with statutory targets. Our typical end-to-end timeline from instruction to submission is 3–4 weeks."),
            ("Does {location} have Article 4 Directions?",
             "{article_4_answer}"),
            ("Which conservation areas are in {location}?",
             "{location} has {conservation_count} designated conservation areas, including {conservation_list}. Planning applications within conservation areas require additional heritage consideration and often a Heritage Statement."),
            ("Do I need a planning consultant for {location}?",
             "For most householder work in {location}, a chartered architectural technologist delivers the same planning outcomes as a dedicated consultant — usually at lower cost. Our MCIAT-chartered team handles drawings, submission and agent liaison as one package."),
        ],
    },

    "building-regulations": {
        "name": "Building Regulations Drawings",
        "h1_lead": "Building Regulations Drawings",
        "short": "building regulations drawings",
        "price_from": 840,
        "price_display": "£840",
        "turnaround": "3–4 weeks to submission",
        "hero_img": "blueprint-correcting",
        "kind": "building-control",
        "summary": (
            "A construction-ready drawing package compliant with every Approved Document "
            "— Part A structure, Part B fire, Part L thermal, Part M accessibility — "
            "submitted to LABC or your approved inspector with structural calculations coordinated."
        ),
        "keywords": [
            "building regulations drawings", "building control", "building regs",
            "LABC", "Part L compliance", "structural calculations"
        ],
        "what_included": [
            ("Full construction drawings", "Plans, sections and elevations at 1:50 with full annotation and material specification."),
            ("Thermal (Part L) calculations", "U-values for walls, roof, floor and glazing; SAP or SBEM where required; compliance statement."),
            ("Structural calculations", "Chartered engineer sign-off on beams, pad foundations, lintels, roof structure."),
            ("Fire safety (Part B) strategy", "Escape routes, compartmentation, smoke alarms, fire-rated construction detail."),
            ("Drainage &amp; services layout", "Soil and vent pipe routes, MVHR coordination, EV charging (Part S)."),
            ("Building Control submission", "Full Plans submission to {building_control_route} with inspections coordinated through to completion certificate."),
        ],
        "local_faqs": [
            ("Can I use LABC or an approved inspector in {location}?",
             "In {location}, you can submit building regulations applications to either {location_council}'s in-house Building Control (LABC route) or to a private approved inspector. Both routes produce the same legally-valid completion certificate. We submit to whichever suits your project and builder."),
            ("How much do building regulations drawings cost in {location}?",
             "Fixed fees in {location} start at £840 for a straightforward extension or loft. Complex projects (HMOs, basement conversions, flat splits) range £1,500–£2,500. Structural calculations are £350–£1,050 depending on the intervention."),
            ("Do I need building regs for a loft conversion in {location}?",
             "Yes — every habitable loft conversion in {location} (and across England) requires Building Regulations approval covering fire escape, floor structure, insulation and staircase. This is independent of whether you also need planning permission."),
            ("What's Part L compliance for extensions in {location}?",
             "Part L of the Building Regulations sets minimum energy-efficiency standards — insulation, glazing U-values, air permeability, heating efficiency. New extensions in {location} must meet the 2025 uplift (Future Homes Standard transition). We include full Part L calculations and a compliance statement in every Complete package."),
            ("How long does building control take in {location}?",
             "Once submitted, {location_council} Building Control reviews Full Plans within 5–8 weeks. Approved inspectors typically review in 2–4 weeks. On-site inspections run through the build — typically 6–10 visits depending on scope."),
        ],
    },

    "loft-conversions": {
        "name": "Loft Conversions",
        "h1_lead": "Loft Conversion Drawings",
        "short": "loft conversion drawings",
        "price_from": 1225,
        "price_display": "£1,225",
        "turnaround": "3–5 weeks to submission",
        "hero_img": "technologist-working",
        "kind": "residential",
        "summary": (
            "Every loft type across every {location} roof line — dormer, mansard, hip-to-gable, "
            "L-shape, Velux. LDC or full planning route, building regulations, structural calculations "
            "and party wall notices, all fixed price."
        ),
        "keywords": [
            "loft conversion", "dormer loft", "mansard loft", "hip-to-gable",
            "loft conversion drawings", "loft planning permission"
        ],
        "what_included": [
            ("Feasibility &amp; head-height check", "We confirm before quoting whether your {location} loft has the head height and structural capacity."),
            ("LDC or planning route", "Most {location} loft conversions qualify for a Lawful Development Certificate. We check Article 4 and conservation constraints first."),
            ("Dormer, mansard or hip-to-gable design", "Option studies including massing, internal layout and roof geometry."),
            ("Full building regulations package", "Staircase Part K compliance, Part B fire escape, Part L insulation, Part E acoustic separation."),
            ("Structural engineering", "Ridge beam, purlins, steelwork, floor joist upgrade, dormer framing — chartered engineer sign-off."),
            ("Party Wall Act support", "Almost every {location} loft triggers Party Wall notices. We draft notices and coordinate with surveyors."),
        ],
        "local_faqs": [
            ("Do I need planning permission for a loft conversion in {location}?",
             "{loft_planning_answer}"),
            ("How much does a loft conversion cost in {location}?",
             "Our architectural technology fees for a {location} loft conversion start at £1,225 (planning + building regs + structural). Typical construction build-cost in {location} is £45,000–£80,000 for a standard dormer and £65,000–£110,000 for a mansard."),
            ("Can I have a mansard loft in {location}?",
             "{mansard_answer}"),
            ("What's the minimum head height for a loft conversion in {location}?",
             "2.3m measured from existing ceiling joist to existing ridge is the practical minimum for a standard conversion in {location}. Below 2.2m usually requires dropping the ceiling below (reducing rooms on the floor beneath) or redesigning as a mansard."),
            ("Will my neighbours in {location} affect my loft conversion?",
             "Most {location} loft conversions trigger Party Wall Act notices — legal notices to all adjoining owners. Rear dormers can also prompt right-to-light considerations in dense terraced streets, particularly in {conservation_first}. We handle both processes."),
        ],
    },

    "house-extensions": {
        "name": "House Extensions",
        "h1_lead": "House Extension Drawings",
        "short": "house extension drawings",
        "price_from": 1225,
        "price_display": "£1,225",
        "turnaround": "3–5 weeks to submission",
        "hero_img": "blueprint-tablet",
        "kind": "residential",
        "summary": (
            "The whole spectrum — rear extensions, side returns, wraparounds, double-storey, "
            "basement digs. Planning-led design with detailed technical phase, ideal for "
            "{typical_housing_short} typical of {location}."
        ),
        "keywords": [
            "house extension", "rear extension", "side return extension", "wraparound extension",
            "double storey extension", "home extension drawings"
        ],
        "what_included": [
            ("Site survey &amp; feasibility", "Measured existing survey, photographic record, Article 4 and conservation check specific to {location} before we quote."),
            ("Design option studies", "2–3 design options at concept stage — alternative layouts, glazing, roof forms."),
            ("Planning package", "Site location plan, existing and proposed plans, elevations, sections, D&amp;AS where required."),
            ("Full building regulations", "Part L thermal, Part B fire, Part M accessibility, structural strategy."),
            ("Structural calculations", "Steel beam, foundation, lintel design. Chartered engineer sign-off."),
            ("Party wall and Build Over", "Party Wall notices where needed; Thames Water Build Over Agreement where within 3m of a public sewer."),
        ],
        "local_faqs": [
            ("Do I need planning permission for an extension in {location}?",
             "{extension_planning_answer}"),
            ("How big can a rear extension be in {location} under permitted development?",
             "Standard permitted development allows single-storey rear extensions up to 3m (attached house) or 4m (detached) in {location}. Larger extensions up to 6m/8m are allowed under Prior Approval (Class AA). Flats, listed buildings and Article 4 areas in {location} are excluded from these PD rights."),
            ("How much does a house extension cost in {location}?",
             "Our fixed-fee architectural package starts at £1,225 for a {location} extension (planning + building regs + structural). Typical {location} build costs are £2,400–£3,500 per square metre including VAT — so a 25m² side return extension is £60,000–£87,500 to construct."),
            ("Can I do a basement extension in {location}?",
             "{basement_answer}"),
            ("Do I need a side return extension or a rear extension in {location}?",
             "Most Victorian terraces in {location} (particularly in {conservation_first}) benefit from both — a side return extension infills the narrow side passage to create a wider kitchen, a rear extension projects back into the garden. A wraparound combines the two. We recommend the best option at the free site visit."),
        ],
    },

    "mansard-roof": {
        "name": "Mansard Roof Extensions",
        "h1_lead": "Mansard Roof Extensions",
        "short": "mansard roof extensions",
        "price_from": 1575,
        "price_display": "£1,575",
        "turnaround": "4–6 weeks to submission",
        "hero_img": "technologist-working",
        "kind": "residential",
        "summary": (
            "{location}'s most space-efficient loft solution when PD-route dormers are blocked. "
            "Our chartered team designs mansards that get approved in {location} conservation areas "
            "— with heritage statements and planning officer negotiation built in."
        ),
        "keywords": [
            "mansard roof", "mansard extension", "mansard loft", "rear mansard",
            "conservation mansard", "mansard planning permission"
        ],
        "what_included": [
            ("Conservation area design review", "We check against {location_council}'s mansard design guide and design to match the terrace."),
            ("Heritage Statement", "Required for {location}'s conservation areas — demonstrates the mansard respects character and townscape."),
            ("Street elevation massing", "Accurate photomontage showing how the mansard sits alongside neighbours — often decisive at {location_council} committee."),
            ("Party Wall and structural", "Mansards invariably trigger Party Wall notices in {location}'s dense terraced streets. Structural package includes new ridge, tie beams, floor joists."),
            ("Planning submission &amp; agent service", "Full liaison with {location_council} planning officer, committee representation if called in."),
            ("Full building regs package", "Part L thermal, Part B fire (critical on mansards), Part E acoustic separation."),
        ],
        "local_faqs": [
            ("Will {location_council} approve a mansard loft?",
             "{mansard_answer}"),
            ("What's the ideal mansard pitch for {location}?",
             "A 70° front slope is typical for {location} mansards — steep enough to maximise floor area while reading as a roof rather than a full additional storey. Front dormers should be small and symmetrical. {location_council}'s design guide (where published) takes precedence on detail."),
            ("Can I have a mansard if my neighbours don't in {location}?",
             "Often yes, but {location_council} favours applications supported by wider street precedents. Where mansards already exist nearby in {location}, approval is far more likely. We review street precedents at the feasibility stage."),
            ("How much does a mansard cost in {location}?",
             "Our architectural fees for a {location} mansard start at £1,575 (planning + building regs + structural + heritage statement). Typical {location} build costs are £90,000–£150,000 depending on size, complexity and access."),
            ("How much headroom does a mansard give me in {location}?",
             "Full-height — typically 2.3–2.5m ceiling from the new floor. Unlike a dormer, which gives partial head height, a mansard provides a complete additional storey within {location}'s {typical_housing_short} terraced context."),
        ],
    },
}

SERVICE_SLUGS = list(SERVICES.keys())
