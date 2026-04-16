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

    "garage-conversions": {
        "name": "Garage Conversions",
        "h1_lead": "Garage Conversion Drawings",
        "short": "garage conversion drawings",
        "price_from": 995,
        "price_display": "£995",
        "turnaround": "3–4 weeks to submission",
        "hero_img": "blueprint-tablet",
        "kind": "residential",
        "summary": (
            "Turn your unused {location} garage into a bedroom, home office or open-plan "
            "kitchen-diner. Planning route assessment, full building regulations drawings "
            "with Part L thermal compliance, structural calculations for any removed walls, "
            "all fixed fee."
        ),
        "keywords": [
            "garage conversion", "garage conversion drawings", "garage to bedroom",
            "garage to office", "integral garage conversion", "detached garage conversion"
        ],
        "what_included": [
            ("Planning route assessment", "We check whether your {location} garage conversion needs planning permission or qualifies as Permitted Development — most integral garages don't need planning."),
            ("Measured survey", "Full laser-measured survey of the existing garage, plus adjacent rooms where walls are being removed."),
            ("Architectural drawings", "Existing and proposed floor plans, elevations and sections at 1:50 — full council-ready specification."),
            ("Part L thermal calculations", "Garage conversions must meet current energy-efficiency standards — upgraded insulation, glazing U-values, heating specification."),
            ("Structural calculations", "Steel beam and padstone design where garage doors are replaced with walls and windows, plus any load-bearing wall removals."),
            ("Building Control submission", "Full Plans submission to {building_control_route} with inspections coordinated through to completion certificate."),
        ],
        "local_faqs": [
            ("Do I need planning permission for a garage conversion in {location}?",
             "Most integral garage conversions in {location} do not require planning permission — they're classed as an internal alteration, which is not development under the TCPA 1990. However, if the conversion materially alters the external appearance (new windows, raising the roof), planning permission may be required. Detached garage conversions to habitable use always need planning. Article 4 Directions in {location} may also affect eligibility. We confirm the planning route before quoting."),
            ("How much does a garage conversion cost in {location}?",
             "Our fixed-fee architectural package for a {location} garage conversion starts at £995 (planning assessment + building regs + structural). Typical build costs in {location} are £15,000–£25,000 for an integral garage or £20,000–£40,000 for a detached garage, depending on insulation, flooring, and services."),
            ("Do I need building regulations for a garage conversion in {location}?",
             "Yes — every garage-to-habitable conversion in {location} needs Building Regulations approval. Key requirements include minimum insulation values (Part L), fire safety and escape routes (Part B), damp-proofing (Part C), ventilation (Part F), and structural adequacy if removing the garage door opening."),
            ("Will a garage conversion add value to my {location} property?",
             "Typically yes — a well-executed garage conversion in {location} adds 10–15% to property value and costs far less per square metre than an extension. In areas where parking is not at a premium, converting an underused garage is one of the most cost-effective ways to gain living space."),
            ("How long does a garage conversion take in {location}?",
             "A standard integral garage conversion in {location} typically takes 4–6 weeks to build once drawings are approved. Our architectural package takes 3–4 weeks from instruction to Building Control submission. Total timeline: approximately 3–4 months from initial survey to completion."),
        ],
    },

    "basement-conversions": {
        "name": "Basement Conversions",
        "h1_lead": "Basement Conversion Drawings",
        "short": "basement conversion drawings",
        "price_from": 1950,
        "price_display": "£1,950",
        "turnaround": "5–8 weeks to submission",
        "hero_img": "blueprint-correcting",
        "kind": "residential",
        "summary": (
            "Full architectural technology service for basement digs and cellar conversions "
            "in {location} — structural underpinning design, waterproofing strategy, "
            "Party Wall coordination, planning where required, and building regulations "
            "through to completion certificate."
        ),
        "keywords": [
            "basement conversion", "basement extension", "cellar conversion",
            "basement underpinning", "basement waterproofing", "basement dig"
        ],
        "what_included": [
            ("Feasibility &amp; structural survey", "Desktop study plus measured survey assessing existing foundations, ground conditions, water table level and underpinning viability for your {location} property."),
            ("Planning application (where required)", "New-build basements and lightwell extensions need planning permission. Cellar conversions of existing space are usually Permitted Development. We confirm the route and submit where needed."),
            ("Structural engineering package", "Underpinning sequence drawings, reinforced concrete design, temporary works strategy — all to Eurocode with chartered engineer sign-off."),
            ("Waterproofing strategy", "BS 8102:2022 compliant — cavity drain, cementitious tanking or membrane system specified for {location}'s ground conditions and water table."),
            ("Building Regulations submission", "Full Plans application to {building_control_route} covering structure (Part A), fire safety (Part B), damp-proofing (Part C), ventilation (Part F) and thermal performance (Part L)."),
            ("Party Wall &amp; Thames Water coordination", "Almost every {location} basement triggers Party Wall notices. We also manage Thames Water Build Over Agreements where within 3m of a public sewer."),
        ],
        "local_faqs": [
            ("Do I need planning permission for a basement conversion in {location}?",
             "Converting an existing cellar to habitable space in {location} usually does not require planning permission — it is an internal alteration. However, excavating a new basement, adding lightwells, or lowering floor levels to create a new storey typically does require planning. {basement_answer}"),
            ("How much does a basement conversion cost in {location}?",
             "Our fixed-fee architectural package for a {location} basement starts at £1,950 (planning + building regs + structural + waterproofing specification). Build costs in {location} range from £3,000–£5,000 per square metre — a typical 40m² basement is £120,000–£200,000 to construct. Costs are higher than extensions due to underpinning, waterproofing and temporary works."),
            ("Is my {location} property suitable for a basement conversion?",
             "Most properties in {location} can support a basement conversion, provided foundations are deep enough or can be underpinned, the water table is manageable, and there are no significant tree root or drainage constraints. Victorian and Edwardian houses in {location} often have existing cellars that can be deepened. We assess suitability at the initial survey."),
            ("What waterproofing does a {location} basement need?",
             "BS 8102:2022 requires a waterproofing strategy appropriate to the site's water table and ground conditions. In {location}, this typically means a Type C cavity drain membrane system (most reliable), sometimes combined with Type A barrier protection. The strategy must be specified by a qualified waterproofing designer — included in our package."),
            ("How long does a basement conversion take in {location}?",
             "A typical {location} basement conversion takes 6–12 months to build once drawings are approved. Our architectural package takes 5–8 weeks from instruction to Building Control submission. The longer build time reflects the sequential underpinning process, which must proceed in careful stages."),
        ],
    },

    "structural-calculations": {
        "name": "Structural Calculations",
        "h1_lead": "Structural Engineering Calculations",
        "short": "structural calculations",
        "price_from": 350,
        "price_display": "£350",
        "turnaround": "1–2 weeks",
        "hero_img": "tools-workplace",
        "kind": "structural",
        "summary": (
            "Chartered structural engineer calculations for every residential intervention in {location} "
            "— steel beams, lintels, pad foundations, wall removals, loft floor joists, "
            "underpinning. Eurocode-compliant, Building Control-ready, fixed fee."
        ),
        "keywords": [
            "structural calculations", "structural engineer", "steel beam calculation",
            "RSJ calculation", "load bearing wall removal", "structural survey"
        ],
        "what_included": [
            ("Load-bearing wall removal", "Steel beam (RSJ) and padstone design for opening up kitchens, knocking through reception rooms or creating open-plan layouts in your {location} property."),
            ("Loft conversion steelwork", "Ridge beam, purlin, dormer framing and floor joist upgrade calculations — essential for every habitable loft in {location}."),
            ("Extension foundations", "Pad, strip or trench-fill foundation design based on {location} ground conditions, tree proximity and drain locations."),
            ("Lintel design", "New window and door openings — steel, concrete or timber lintel specification with bearing calculations."),
            ("Underpinning &amp; basement", "Sequential underpinning design, reinforced concrete slab and retaining wall calculations for {location} basements."),
            ("Chartered engineer sign-off", "Every calculation set is signed by a chartered structural engineer (CEng MIStructE or MICE) — accepted by all Building Control bodies."),
        ],
        "local_faqs": [
            ("How much do structural calculations cost in {location}?",
             "Our fixed fees for structural calculations in {location} start at £350 for a single beam (wall removal) and £550–£1,050 for a full structural package (loft or extension). Complex basements and multi-storey interventions are quoted individually. All prices include chartered engineer sign-off."),
            ("Do I need a structural engineer for a wall removal in {location}?",
             "Yes — removing or altering any load-bearing wall in your {location} property requires structural calculations proving the replacement beam and supports can carry the loads. Building Control will not approve the work without chartered engineer-signed calculations. Even partition walls should be checked before removal."),
            ("How long do structural calculations take in {location}?",
             "We deliver structural calculations within 1–2 weeks of receiving the architectural drawings and site measurements. For urgent projects in {location}, we offer a fast-track service (3–5 working days) at a small premium."),
            ("What's the difference between a structural survey and structural calculations in {location}?",
             "A structural survey is a condition assessment of the existing building — identifying defects, movement, subsidence. Structural calculations are engineering designs for new work — beams, foundations, loft steelwork. For most {location} extension and loft projects, you need calculations (not a survey). We provide calculations; we can recommend surveyors if a condition survey is needed."),
            ("Can I get structural calculations without architectural drawings in {location}?",
             "Yes — we offer standalone structural calculations for {location} projects where you already have architectural drawings from another practice. Just send us the drawings and we quote a fixed fee for the engineering package. If you need both drawings and structural, our Complete package bundles them at a lower combined price."),
        ],
    },

    "party-wall": {
        "name": "Party Wall Services",
        "h1_lead": "Party Wall Drawings &amp; Notices",
        "short": "party wall services",
        "price_from": 450,
        "price_display": "£450",
        "turnaround": "1–2 weeks for notices",
        "hero_img": "blueprint-correcting",
        "kind": "party-wall",
        "summary": (
            "End-to-end Party Wall Act 1996 service for {location} — Section 1, 3 and 6 notices, "
            "schedule of condition surveys, party wall award coordination. We handle the "
            "process so your {location} build starts without neighbour disputes."
        ),
        "keywords": [
            "party wall", "party wall notice", "party wall surveyor", "party wall agreement",
            "party wall act", "party wall drawings"
        ],
        "what_included": [
            ("Party Wall assessment", "We review your {location} project and confirm which Party Wall Act sections apply — Section 1 (new wall on boundary), Section 3 (adjacent excavation) or Section 6 (line of junction)."),
            ("Notice drafting &amp; service", "Legally-compliant notices prepared and served on all adjoining owners, with 14-day or 1-month response periods tracked."),
            ("Schedule of condition survey", "Photographic and written record of neighbouring properties before work starts — protects you and your {location} neighbours from disputes."),
            ("Party wall drawings", "Technical drawings showing the proposed works in relation to the party wall, foundations and adjoining structures — required by the Act."),
            ("Surveyor appointment coordination", "If neighbours dissent, we coordinate the appointment of agreed surveyors or independent surveyors to prepare the Party Wall Award."),
            ("Award support", "Liaison through the award process — method statements, temporary works, access arrangements — until the award is agreed and you can start on site."),
        ],
        "local_faqs": [
            ("Do I need a party wall agreement in {location}?",
             "You need Party Wall Act notices if your {location} project involves: building on or astride a boundary (Section 1), cutting into a party wall or party structure (Section 3), or excavating within 3m/6m of an adjoining property's foundations (Section 6). Most loft conversions, extensions and basement digs in {location} trigger at least one section."),
            ("How much does a party wall notice cost in {location}?",
             "Our fixed fee for drafting and serving party wall notices in {location} starts at £450 for a single adjoining owner. If your neighbour consents, that's the total cost. If they dissent, surveyor fees typically add £700–£1,000 per neighbour for the Award process. We include party wall notices in our Complete architectural packages at no additional charge."),
            ("How long does the party wall process take in {location}?",
             "If all adjoining owners in {location} consent: 14 days (Section 3/6 notice) or 1 month (Section 1 notice). If they dissent and surveyors must be appointed, allow 6–8 weeks for the Award. We serve notices as early as possible so the process runs in parallel with your planning application."),
            ("Can I start building before the party wall award in {location}?",
             "No — starting notifiable works in {location} before serving valid notices or obtaining a Party Wall Award is a breach of the Party Wall Act 1996. It can result in injunctions, damages and loss of your statutory protections. We ensure notices are served at the right time so your build timeline is not delayed."),
            ("What happens if my {location} neighbour ignores my party wall notice?",
             "If an adjoining owner in {location} does not respond within 14 days, the Act deems them to have dissented. This triggers the surveyor appointment process — you appoint a surveyor, they can appoint their own (at your cost) or you can agree on a single 'agreed surveyor'. We manage this process and keep it moving."),
        ],
    },

    "rear-dormer": {
        "name": "Rear Dormer Loft Conversions",
        "h1_lead": "Rear Dormer Loft Conversion Drawings",
        "short": "rear dormer drawings",
        "price_from": 1225,
        "price_display": "£1,225",
        "turnaround": "3–5 weeks to submission",
        "hero_img": "technologist-working",
        "kind": "residential",
        "summary": (
            "London's most popular loft type — the full-width rear dormer. Planning or "
            "Permitted Development route assessed for your {location} property, "
            "building regulations, structural steelwork and Party Wall notices, all fixed fee."
        ),
        "keywords": [
            "rear dormer", "rear dormer loft conversion", "full width dormer",
            "box dormer", "flat roof dormer", "dormer loft london"
        ],
        "what_included": [
            ("PD eligibility check", "We confirm whether your {location} rear dormer qualifies for Permitted Development — checking volume limits (40m³ terraced, 50m³ semi/detached), Article 4, conservation area and prior extension history."),
            ("LDC or planning application", "If PD applies, we obtain a Lawful Development Certificate for certainty. If not, we submit full planning with Design &amp; Access Statement to {authority}."),
            ("Dormer design &amp; massing", "Full-width flat-roof rear dormer with matching materials, set in from party walls, cheeks clad to match existing roof — the design that {location_council} approves most readily."),
            ("Building Regulations package", "Part B fire escape (protected staircase, fire doors, smoke alarms), Part K staircase, Part L insulation, Part E acoustic separation."),
            ("Structural engineering", "Steel ridge beam, purlin supports, dormer framing, floor joist upgrade — chartered engineer sign-off for Building Control."),
            ("Party Wall coordination", "Most rear dormers in {location}'s terraced streets trigger Section 6 Party Wall notices. We draft, serve and coordinate the process."),
        ],
        "local_faqs": [
            ("Do I need planning permission for a rear dormer in {location}?",
             "{loft_planning_answer} Full-width rear dormers are the most common PD loft type in {location} — provided the volume, materials and setback conditions are met. We check every condition before committing to a route."),
            ("How much does a rear dormer loft conversion cost in {location}?",
             "Our fixed-fee architectural package for a {location} rear dormer starts at £1,225 (drawings + building regs + structural). Typical build costs in {location} are £45,000–£70,000 for a standard full-width rear dormer with en-suite, depending on access, floor area and specification."),
            ("How much space does a rear dormer add in {location}?",
             "A full-width rear dormer in {location} typically adds 15–25 square metres of habitable floor area — enough for a double bedroom with en-suite, or two single bedrooms. The flat roof gives full standing height across the entire width of the house, unlike a rooflight-only conversion which is constrained by the roof pitch."),
            ("Can I have a rear dormer in a conservation area in {location}?",
             "Rear dormers in {location}'s conservation areas usually need full planning permission because PD rights are restricted. However, because they face the rear (not the street), {location_council} typically views them more favourably than front dormers or mansards. A well-designed rear dormer with matching materials and sensitive proportions has a strong approval record."),
            ("How long does a rear dormer take to build in {location}?",
             "A standard rear dormer in {location} takes 8–12 weeks to build once on site. Our architectural package takes 3–5 weeks from instruction to submission. Building Control approval adds 2–4 weeks. Total timeline from survey to move-in: approximately 4–5 months."),
        ],
    },
}

SERVICE_SLUGS = list(SERVICES.keys())
